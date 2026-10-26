"""Original-build static configuration enrichment; no runtime identity inference."""
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import ReplayFormatError, parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import load_unit_data, enrich_references
from wgrd_unit_index import export_index, canonical_bytes, parse_dictionary
from research.export_unit_index59638 import authenticate_objects

UNIT, COMPANY = '01'*16, '02'*16
TOKEN = '03'*8


def fixture(ambiguous=False):
    def obj(i, kind, props):
        return {'index': i, 'class': kind, 'class_id': i+100, 'offset': i*100, 'properties': props}
    def ref(i): return {'ref_index': i, 'ref_class_id': i+100}
    def guid(g): return {'raw_hex': g, 'ndf_type': 26}
    objects = [
        obj(0, 'TUniteAuSolDescriptor', {'DescriptorId': guid(UNIT), 'ClassNameForDebug': 'Unit_Test',
            'NameInMenuToken': {'raw_hex': TOKEN, 'ndf_type': 29}, 'AliasName': 'raw alias',
            'Modules': [{'key': 'CompanyUnit', 'value': ref(1)}]}),
        obj(1, 'TModuleSelector', {'ControllerName': 'CompanyUnitController', 'Default': ref(2), 'Selection': [ref(4)]}),
        obj(2, 'TCompanyUnitModuleDescriptor', {'CompanyDescriptor': ref(3)}),
        obj(3, 'TUniteDescriptor', {'DescriptorId': guid(COMPANY), 'ClassNameForDebug': 'Company_Test'}),
        obj(4, 'TModuleSelectorFilter', {'Condition': ref(5)}),
        obj(5, 'TModuleSelectorCondition_ParamEquals_Integer', {'ParamId': 11, 'ParamValue': 1})]
    if ambiguous:
        other = copy.deepcopy(objects[0]); other.update(index=6, offset=600)
        other['properties']['DescriptorId'] = guid('04'*16)
        objects.append(other)
    dictionary = {TOKEN: [{'text': 'PLAYER NAME #reco2', 'record_index': 0, 'offset': 24, 'length': 18}]}
    return export_index(objects, {'ndf': {'archive_sha256': 'a'*64}}, dictionary,
                        {'locale': 'us', 'dictionary_sha256': 'b'*64})


def catalog():
    return {'entries': [{'validation_guid_hex': g, 'unit_identity': None} for g in (COMPANY, UNIT, 'ff'*16)]}


class UnitIndex(unittest.TestCase):
    def test_company_direct_missing_and_full_provenance(self):
        index = fixture(); before = copy.deepcopy(index); cat = catalog()
        enrich_references(cat, {'index': index, 'source': {'index_sha256': 'c'*64}}, '59638')
        company, direct, missing = [e['configured_unit_types'] for e in cat['entries']]
        self.assertEqual([company['status'], direct['status'], missing['status']], ['unique', 'unique', 'missing'])
        unit = company['candidates'][0]
        self.assertEqual(unit['debug_name'], 'Unit_Test')
        self.assertEqual(unit['localized_name'], 'PLAYER NAME #reco2')
        self.assertEqual(unit['provenance']['path'], ['0', '1', '2', '3'])
        nodes = cat['descriptor_data']['nodes']
        self.assertEqual(nodes['5']['properties'], {'ParamId': 11, 'ParamValue': 1})
        self.assertEqual(unit['provenance']['selector_filters'], ['4'])
        self.assertFalse(unit['provenance']['conditions_evaluated'])
        self.assertEqual(direct['candidates'][0]['provenance']['relation'], 'direct')
        self.assertEqual(company['evidence_status'], 'matching_build_static_configuration')
        self.assertTrue(all(e['unit_identity'] is None for e in cat['entries']))
        self.assertEqual(index, before)

    def test_ambiguity_missing_localization_and_sample2_inferred(self):
        index = fixture(True)
        index['names'][TOKEN].append({'text': 'OTHER', 'record_index': 1, 'offset': 60, 'length': 5})
        cat = catalog(); enrich_references(cat, {'index': index, 'source': {}}, '510117427')
        match = cat['entries'][0]['configured_unit_types']
        self.assertEqual(match['status'], 'ambiguous')
        self.assertEqual(len(match['candidates']), 2)
        self.assertEqual(match['evidence_status'], 'inferred_build_59638')
        for candidate in match['candidates']:
            self.assertIsNone(candidate['localized_name'])
            self.assertEqual(candidate['name_status'], 'ambiguous')
            self.assertEqual(len(candidate['name_candidates']), 2)
        del index['names'][TOKEN]
        cat = catalog(); enrich_references(cat, {'index': index, 'source': {}}, '59638')
        self.assertEqual(cat['entries'][1]['configured_unit_types']['candidates'][0]['name_status'], 'missing')
        self.assertIsNone(cat['entries'][1]['configured_unit_types']['candidates'][0]['localized_name'])

    def test_index_file_loader_determinism_and_malformed_graph(self):
        index = fixture()
        self.assertEqual(canonical_bytes(index), canonical_bytes(json.loads(canonical_bytes(index))))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'index.json'; path.write_bytes(canonical_bytes(index))
            self.assertEqual(load_unit_data(path)['index'], index)
            packed = Path(d)/'index.json.gz'; packed.write_bytes(gzip.compress(canonical_bytes(index), mtime=0))
            self.assertEqual(load_unit_data(packed)['index'], index)
            packed.write_bytes(packed.read_bytes()[:-4])
            with self.assertRaises(ReplayFormatError): load_unit_data(packed)
            packed.write_bytes(bytes.fromhex('1f8b0800000000000203')+b'\x07'+b'\0'*8)
            with self.assertRaises(ReplayFormatError): load_unit_data(packed)
            for mutate in [lambda x: x.update(schema='unknown'),
                           lambda x: x.update(game_build='58710'),
                           lambda x: x['nodes'].pop('2'),
                           lambda x: x['descriptors'][COMPANY]['candidates'][0].update(conditions_evaluated=True),
                           lambda x: x['descriptors'][COMPANY]['candidates'][0].update(path=['0','3'])]:
                broken = copy.deepcopy(index); mutate(broken); path.write_bytes(canonical_bytes(broken))
                with self.assertRaises(ReplayFormatError): load_unit_data(path)
            path.write_text('{"schema":1,"schema":2}')
            with self.assertRaises(ReplayFormatError): load_unit_data(path)

    def test_known_descriptor_without_inverse_is_explicitly_missing(self):
        objects = [{'index': 0, 'class': 'TUniteDescriptor', 'class_id': 1, 'offset': 0,
                    'properties': {'DescriptorId': {'raw_hex': COMPANY, 'ndf_type': 26}}}]
        index = export_index(objects, {'ndf': {}}, {}, None)
        cat = catalog(); enrich_references(cat, {'index': index, 'source': {}}, '59638')
        match = cat['entries'][0]['configured_unit_types']
        self.assertEqual(match['status'], 'missing')
        self.assertEqual(match['source_descriptors'], ['0'])
        self.assertEqual(match['candidates'], [])

    def test_dictionary_bounds_utf16_and_duplicate_hashes(self):
        blob = b'TRAD'+struct.pack('<I', 2)
        blob += bytes.fromhex(TOKEN)+struct.pack('<II', 40, 1)
        blob += bytes.fromhex(TOKEN)+struct.pack('<II', 42, 1)+ 'AB'.encode('utf-16-le')
        parsed = parse_dictionary(blob)
        self.assertEqual([r['text'] for r in parsed[TOKEN]], ['A', 'B'])
        for bad in (blob[:7], b'NOPE'+blob[4:], blob[:-1],
                    blob[:16]+struct.pack('<II', 8, 1)+blob[24:],
                    blob[:16]+struct.pack('<II', 40, 0xffffffff)+blob[24:],
                    blob[:-2]+b'\x00\xd8'):
            with self.assertRaises(ReplayFormatError): parse_dictionary(bad)

    def test_export_rejects_altered_parsed_objects(self):
        objects, expanded = b'original objects', b'authenticated expanded NDF'
        record = {'objects_sha256': hashlib.sha256(objects).hexdigest(),
                  'expanded_sha256': hashlib.sha256(expanded).hexdigest()}
        authenticate_objects(objects, expanded, record)
        for a, b in [(objects+b' ', expanded), (objects, expanded+b'!')]:
            with self.assertRaises(ValueError): authenticate_objects(a, b, record)


class BundledIndex(unittest.TestCase):
    def test_versioned_export_hashes_and_canonical_payload(self):
        path = ROOT/'research/unit-data/build59638-v1.json.gz'
        manifest = json.loads(path.with_name('build59638-v1.manifest.json').read_text())
        raw = path.read_bytes(); payload = gzip.decompress(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), manifest['index_sha256'])
        self.assertEqual(hashlib.sha256(payload).hexdigest(), manifest['canonical_json_sha256'])
        data = load_unit_data(path)
        self.assertEqual(payload, canonical_bytes(data['index']))
        self.assertEqual(manifest['counts']['configured_unit_types'], 2121)
        self.assertEqual(manifest['counts']['unit_types_with_unique_localized_name'], 2121)
        self.assertTrue(all(len(data['index']['names'][u['name_token']]) == 1
                            for u in data['index']['unit_types'].values()))

    def test_authentic_replays_names_safeguards_and_determinism(self):
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')))
        manifest = json.loads((ROOT/'samples/manifest.json').read_text())['samples']
        if not all((samples/s['file']).exists() for s in manifest): self.skipTest('authentic samples not cached')
        path = ROOT/'research/unit-data/build59638-v1.json.gz'; data = load_unit_data(path)
        before = canonical_bytes(data)
        for sample, count in zip(manifest, [285, 41, 400]):
            raw = (samples/sample['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), sample['sha256'])
            parsed = parse_replay(raw); base = build_timeline(parsed)
            enriched = build_timeline(parsed, unit_data=data)
            # Only 0x18 target_reference.unit_type may differ: it is the one event-level join.
            def without_op18_unit_type(events):
                out = []
                for e in events:
                    if e['opcode'] == 0x18 and e['interpretation']['parameters'] is not None:
                        e = json.loads(json.dumps(e))
                        e['interpretation']['parameters']['target_reference']['unit_type'] = None
                    out.append(e)
                return out
            self.assertEqual(without_op18_unit_type(enriched['events']), base['events'])
            cat = enriched['entity_references']
            self.assertEqual(cat['descriptor_data']['mapping_counts'], {'unique': count, 'ambiguous': 0, 'missing': 0})
            expected = 'matching_build_static_configuration' if sample['game_version'] == '59638' else 'inferred_build_59638'
            self.assertEqual(cat['descriptor_data']['evidence_status'], expected)
            for entry in cat['entries']:
                self.assertIsNone(entry['unit_identity'])
                match = entry['configured_unit_types']
                self.assertEqual(match['evidence_status'], expected)
                unit = match['candidates'][0]
                self.assertTrue(unit['debug_name']); self.assertTrue(unit['localized_name'])
                self.assertEqual(unit['name_status'], 'localized')
                self.assertFalse(unit['provenance']['conditions_evaluated'])
            self.assertEqual(canonical_bytes(enriched), canonical_bytes(build_timeline(parsed, unit_data=data)))
        self.assertEqual(before, canonical_bytes(data))
        # Real CLI file mode. Mismatched Sample2 remains inferred, including summary.
        command = [sys.executable, '-B', str(ROOT/'wgrd_replay.py'), str(samples/manifest[1]['file']),
                   '--timeline', '--summary', '--unit-data', str(path)]
        one = subprocess.run(command, capture_output=True, check=True).stdout
        two = subprocess.run(command, capture_output=True, check=True).stdout
        self.assertEqual(one, two)
        self.assertEqual(json.loads(one)['entity_references']['descriptor_data']['evidence_status'], 'inferred_build_59638')


if __name__ == '__main__': unittest.main()
