"""Exact descriptor GUID joins; never runtime-key, truncated-GUID or company rewrites."""
import copy
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import ReplayFormatError, parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import ndf_guid_hex, descriptor_index, load_unit_data, enrich_references

# Mixed-endian .NET GUID fields; second word must retain all four bytes.
GUID = '00000000-0007-0000-0300-00005f080000'
COMPANY = struct.pack('<4I', 0, 7, 3, 2143).hex()
UNIT = struct.pack('<4I', 0, 7, 0, 2143).hex()
UNITS = '''<TUniteAuSolDescriptors><TUniteAuSolDescriptor id="12">
<DescriptorId>00000000-0007-0000-0000-00005f080000</DescriptorId>
<ClassNameForDebug>Unit_Example</ClassNameForDebug><Modules>
<collectionelement>Map: Flags : 84 : 88 (False) - TFlagsModuleDescriptor</collectionelement>
</Modules></TUniteAuSolDescriptor></TUniteAuSolDescriptors>'''
COMPANIES = '''<TUniteDescriptors><TUniteDescriptor id="34">
<DescriptorId>00000000-0007-0000-0300-00005f080000</DescriptorId>
<ClassNameForDebug>Company_Example</ClassNameForDebug><Modules>
<collectionelement>Map: UnitListCompany : 156 : 45 (False) - TUnitListCompanyModuleDescriptor</collectionelement>
<collectionelement>Map: Selection : 83 : 90 (False) - TModuleSelector</collectionelement>
</Modules></TUniteDescriptor></TUniteDescriptors>'''
SELECTORS = '''<TModuleSelectors><TModuleSelector id="90">
<Default>112 : 100 (False) - TSelectionModuleDescriptor</Default>
</TModuleSelector></TModuleSelectors>'''
CARDS = 'ID,Name,MovementType,IsCommandUnit,IsShip,IsTransporter,Amphibious\n12,Example,Wheeled,False,False,True,\n'


def fixture():
    return descriptor_index(UNITS.encode(), COMPANIES.encode(), SELECTORS.encode(), CARDS.encode())


def catalog():
    return {'entries': [{'validation_guid_hex': COMPANY, 'lookup_key_u32': 12, 'unit_identity': None},
                        {'validation_guid_hex': UNIT, 'lookup_key_u32': 34, 'unit_identity': None},
                        {'validation_guid_hex': 'ff'*16, 'lookup_key_u32': 12, 'unit_identity': None}]}


class UnitData(unittest.TestCase):
    def test_ndf_guid_byte_order_and_strict_length(self):
        self.assertEqual(ndf_guid_hex(GUID), COMPANY)
        for bad in ('', COMPANY, GUID+'0', 'zzzzzzzz-0000-0000-0000-000000000000'):
            with self.assertRaises(ReplayFormatError): ndf_guid_hex(bad)

    def test_company_and_unit_distinct_exact_guids_and_module_defaults(self):
        idx = fixture()
        self.assertEqual(idx[COMPANY]['debug_name'], 'Company_Example')
        self.assertIsNone(idx[COMPANY]['unit_card'])
        self.assertEqual(idx[COMPANY]['modules'][0]['reference_class'], 'TUnitListCompanyModuleDescriptor')
        self.assertIsNone(idx[COMPANY]['modules'][0]['default'])
        self.assertEqual(idx[COMPANY]['modules'][1]['default']['class'], 'TSelectionModuleDescriptor')
        card = idx[UNIT]['unit_card']
        self.assertEqual(card['name'], 'Example')
        self.assertFalse(card['is_command_unit']); self.assertTrue(card['is_transporter'])
        self.assertIsNone(card['amphibious'])

    def test_exact_join_ignores_runtime_keys_and_preserves_unknowns(self):
        cat = catalog(); idx = fixture(); before = copy.deepcopy(idx)
        enrich_references(cat, {'descriptors':idx, 'source': {'dataset_version':'58710'}}, '59638')
        a,b,c = cat['entries']
        self.assertEqual(a['static_descriptor']['ndf_instance_id'], '34')
        self.assertEqual(b['static_descriptor']['ndf_instance_id'], '12')
        self.assertIsNone(c['static_descriptor'])
        self.assertTrue(all(x['unit_identity'] is None for x in cat['entries']))
        self.assertEqual(a['descriptor_match_status'], 'exact_guid_cross_version')
        self.assertEqual(cat['descriptor_data']['reference_mapping_status'], 'verified_build_59638')
        self.assertEqual(idx, before)
        self.assertEqual(cat['descriptor_data']['matched_references'], 2)

    def test_mismatched_replay_never_verified(self):
        cat=catalog(); enrich_references(cat, {'descriptors':fixture(), 'source':{'dataset_version':'58710'}}, '510117427')
        self.assertEqual(cat['descriptor_data']['reference_mapping_status'], 'inferred_build_59638')
        self.assertTrue(all(x['descriptor_match_status']!='verified' for x in cat['entries']))

    def test_duplicate_guids_bad_xml_and_invalid_card_values_fail_closed(self):
        for units,desc,cards in [(UNITS, COMPANIES.replace('0300-','0000-'), CARDS),
                                 (UNITS, '<broken', CARDS),
                                 (UNITS, COMPANIES, CARDS.replace('True','maybe'))]:
            with self.assertRaises(ReplayFormatError):
                descriptor_index(units.encode(),desc.encode(),SELECTORS.encode(),cards.encode())

    def test_absent_or_modified_pinned_data_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ReplayFormatError): load_unit_data(d)
        result = subprocess.run([sys.executable,'-B',str(ROOT/'wgrd_replay.py'),'missing','--unit-data','missing'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2);self.assertIn('requires --timeline',result.stderr)


class AuthenticPublicData(unittest.TestCase):
    def test_all_726_exact_matches_no_contextual_resolution(self):
        public = Path(os.environ.get('WGRD_UNIT_DATA',str(ROOT/'work/public-units/wargame-data')))
        if not public.exists(): self.skipTest('pinned public snapshot not cached; set WGRD_UNIT_DATA')
        data=load_unit_data(public)
        # NOTE: the public-snapshot skip above does not cover samples; absent samples raise FileNotFoundError.
        samples=Path(os.environ.get('WGRD_SAMPLES_DIR',str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')))
        for sample,n,names in zip(json.loads((ROOT/'samples/manifest.json').read_text())['samples'],[285,41,400],[1,0,3]):
            parsed=parse_replay((samples/sample['file']).read_bytes()); before=copy.deepcopy(parsed)
            base=build_timeline(parsed); enriched=build_timeline(parsed,unit_data=data)
            self.assertEqual(enriched['events'],base['events'])
            cat=enriched['entity_references']
            self.assertEqual(cat['descriptor_data']['replay_version'],sample['game_version'])
            self.assertEqual(cat['descriptor_data']['reference_mapping_status'],
                             'verified_build_59638' if sample['game_version']=='59638' else 'inferred_build_59638')
            self.assertEqual(cat['descriptor_data']['matched_references'],n)
            self.assertEqual(sum(bool(e['static_descriptor']['unit_card']) for e in cat['entries']),names)
            self.assertTrue(all(e['unit_identity'] is None for e in cat['entries']))
            self.assertTrue(all(e['descriptor_match_status']=='exact_guid_cross_version' for e in cat['entries']))
            self.assertEqual(parsed,before)
            json.dumps(enriched,allow_nan=False)
        # A changed dataset must fail even if its XML remains well formed.
        import unittest.mock
        with unittest.mock.patch('wgrd_unit_data.hashlib.sha256') as sha:
            sha.return_value.hexdigest.return_value='0'*64
            with self.assertRaises(ReplayFormatError):load_unit_data(public)


if __name__=='__main__': unittest.main()
