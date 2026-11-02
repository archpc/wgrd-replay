"""Tests for the build-131544 native descriptor index and GUID joins.

Synthetic NDF cases exercise mechanics without game data. The authenticated
131544 cases run only when the pinned private archive and replays are present.
"""
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'research'))
import aar_unit_index as aar
import wgrd_replay as replay

ARTIFACTS = Path(os.environ.get('WGRD_ARTIFACTS_DIR', str(Path.home()/'.hermes/artifacts/wgrd-replay')))
NDF = Path(os.environ.get('WGRD_AAR_NDF', str(ARTIFACTS/'game/win64/Data/WarGame/PC/131544/NDF_Win.dat')))
REPLAY_COMBAT = ARTIFACTS/'combat-20261101/replay_2026-11-01_19-10-26.wargamerpl2'
REPLAY_CONTROLLED = ARTIFACTS/'current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2'

G_UNIT_A = bytes(range(16)).hex()
G_UNIT_C = bytes(range(16, 32)).hex()
G_COMPANY_B = bytes(range(32, 48)).hex()

CLASSES = ['TUniteAuSolDescriptor', 'TUniteDescriptor', 'TCompanyUnitModuleDescriptor',
           'TModuleSelector', 'TModuleSelectorFilter', 'TCondition', 'TGfxDescriptorPorteur',
           'TUnitListCompanyModuleDescriptor']
STRINGS = ['CompanyUnit', 'UnitListCompany', 'Unit_A', 'A alias', 'Unit_C', 'C alias',
           '_Dummy', 'GfxPorteurB', 'Descriptor_Company_B']
PROPS = ['DescriptorId', 'ClassNameForDebug', 'AliasName', 'Modules', 'Selection',
         'Default', 'Condition', 'CompanyDescriptor', 'UnitListCompany',
         'PorteurDescriptor', 'NbUniteInCompagnieToSpawn', 'NbUniteInCompagnieMax',
         '_ShortDatabaseName']


def u32(value):
    return struct.pack('<I', value)


def table_string(text):
    raw = text.encode('latin1')
    return u32(len(raw))+raw


def guid_value(text):
    return u32(26)+bytes.fromhex(text)


def string_value(index):
    return u32(7)+u32(index)


def ref_value(index, class_id):
    return u32(0xbbbbbbbb)+u32(index)+u32(class_id)


def array_value(values):
    return u32(17)+u32(len(values))+b''.join(values)


def map_array_value(pairs):
    return u32(18)+u32(len(pairs))+b''.join(key+value for key, value in pairs)


def scalar_int(value):
    return u32(3)+u32(value)


def object_bytes(class_id, properties):
    out = u32(class_id)
    for property_id, value in properties:
        out += u32(property_id)+value
    return out+u32(0xabababab)


def synthetic_objects():
    properties = {name: index for index, name in enumerate(PROPS)}

    def prop(name):
        return properties[name]

    unit_a = object_bytes(0, [
        (prop('DescriptorId'), guid_value(G_UNIT_A)),
        (prop('ClassNameForDebug'), string_value(STRINGS.index('Unit_A'))),
        (prop('AliasName'), string_value(STRINGS.index('A alias'))),
        (prop('Modules'), array_value([])),
    ])
    company_module = object_bytes(2, [
        (prop('CompanyDescriptor'), ref_value(2, 1)),
    ])
    company = object_bytes(1, [
        (prop('DescriptorId'), guid_value(G_COMPANY_B)),
        (prop('_ShortDatabaseName'), string_value(STRINGS.index('Descriptor_Company_B'))),
        (prop('Modules'), map_array_value([
            (string_value(STRINGS.index('UnitListCompany')),
             ref_value(6, 7))])),
    ])
    unit_c = object_bytes(0, [
        (prop('DescriptorId'), guid_value(G_UNIT_C)),
        (prop('ClassNameForDebug'), string_value(STRINGS.index('Unit_C'))),
        (prop('AliasName'), string_value(STRINGS.index('C alias'))),
        (prop('Modules'), map_array_value([
            (string_value(STRINGS.index('CompanyUnit')), ref_value(4, 3))])),
    ])
    selector = object_bytes(3, [
        (prop('Selection'), array_value([ref_value(5, 4)])),
        (prop('Default'), ref_value(1, 2)),
    ])
    selector_filter = object_bytes(4, [
        (prop('Condition'), ref_value(7, 5)),
    ])
    unit_list = object_bytes(7, [
        (prop('PorteurDescriptor'), ref_value(8, 6)),
        (prop('NbUniteInCompagnieToSpawn'), scalar_int(1)),
        (prop('NbUniteInCompagnieMax'), scalar_int(4)),
    ])
    condition = object_bytes(5, [])
    gfx = object_bytes(6, [
        (prop('_ShortDatabaseName'), string_value(STRINGS.index('GfxPorteurB'))),
    ])
    return [unit_a, company_module, company, unit_c, selector, selector_filter,
            unit_list, condition, gfx]


def synthetic_expanded():
    objects = synthetic_objects()
    bodies = {
        'CLAS': b''.join(table_string(name) for name in CLASSES),
        'STRG': b''.join(table_string(text) for text in STRINGS),
        'TRAN': b'',
        'PROP': b''.join(table_string(name)+u32(0) for name in PROPS),
        'OBJE': b''.join(objects),
        'CHNK': struct.pack('<II', 0, len(objects)),
    }
    offset = 40
    layout, entries = b'', []
    for name in ('OBJE', 'CLAS', 'PROP', 'STRG', 'TRAN', 'CHNK'):
        blob = bodies[name]
        entries.append((name, offset, len(blob)))
        layout += blob
        offset += len(blob)
    toc = 40+len(layout)
    header = bytearray(40)
    header[:4] = b'EUG0'
    header[8:12] = b'CNDF'
    # Every observed NDF_Win.dat member keeps the compressed flag in the
    # expanded form too, so the fixture header matches that.
    struct.pack_into('<I', header, 12, 128)
    struct.pack_into('<I', header, 16, toc)
    struct.pack_into('<I', header, 24, 40)
    struct.pack_into('<I', header, 32, toc+8+24*len(entries))
    table = b'TOC0'+u32(len(entries))
    # Real 131544 TOC records are 24 bytes: 4-byte tag, 4 reserved bytes, then
    # the 8-byte body offset and 8-byte size (measured at file offset 21188418).
    for name, start, size in entries:
        table += name.encode('latin1')+b'\0'*4+struct.pack('<QQ', start, size)
    return bytes(header)+layout+table


def synthetic_archive():
    expanded = synthetic_expanded()
    # Observed ndfbin container: 40-byte CNDF prefix, u32 declared body size,
    # then the (here zlib-compressed) body.
    raw = expanded[:40]+u32(len(expanded)-40)+zlib.compress(expanded[40:])
    member = 'pc\\ndf\\patchable\\gfx\\everything.ndfbin'
    name = member.encode('utf-8')+b'\0'
    body = struct.pack('<4I', 0, 0, len(raw), 0)+hashlib.md5(raw).digest()+name
    if (8+len(body)) % 2:
        body += b'\0'
    node = struct.pack('<2I', 0, 8+len(body))+body
    dictionary = b'\x0a\0\0\0'+b'\0'*6+node
    doff, boff = 65, 65+len(dictionary)
    header = bytearray(65)
    header[:8] = b'edat\x02\0\0\0'
    struct.pack_into('<4I', header, 25, doff, len(dictionary), boff, len(raw))
    header[49:65] = hashlib.md5(dictionary).digest()
    return bytes(header)+dictionary+raw


class SyntheticIndex(unittest.TestCase):
    def setUp(self):
        self.index = aar.index_from_expanded(synthetic_expanded(), {'build': 'synthetic'})

    def test_company_member_chain_follows_module_and_selector(self):
        descriptor = self.index['descriptors'][G_COMPANY_B]
        self.assertEqual(descriptor['source_nodes'], ['2'])
        self.assertEqual(len(descriptor['candidates']), 1)
        candidate = descriptor['candidates'][0]
        self.assertEqual(candidate['relation'], 'company_default')
        self.assertEqual(candidate['conditions_evaluated'], False)
        self.assertEqual(candidate['selector_filters'], ['5'])
        join = aar._join_one(self.index, G_COMPANY_B)
        self.assertEqual(join['join_status'], 'exact_guid')
        member = join['configured_member_units'][0]
        self.assertEqual((member['debug_name'], member['alias_name']), ('Unit_C', 'C alias'))
        self.assertEqual([step['role'] for step in member['member_chain']],
                         ['company_descriptor', 'company_unit_module', 'module_selector',
                          'member_unit_type'])
        self.assertEqual(member['member_chain'][0]['debug_name'], None)
        self.assertEqual(member['member_chain'][-1]['node'], '3')
        modules = join['company_modules']
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0]['module_class'], 'TUnitListCompanyModuleDescriptor')
        self.assertEqual(modules[0]['porteur_descriptor']['ndf_class'], 'TGfxDescriptorPorteur')
        self.assertEqual(modules[0]['porteur_descriptor']['short_name'], 'GfxPorteurB')
        self.assertEqual((modules[0]['units_to_spawn'], modules[0]['units_max']), (1, 4))

    def test_direct_unit_chain_is_itself(self):
        join = aar._join_one(self.index, G_UNIT_A)
        self.assertEqual(join['join_status'], 'exact_guid')
        self.assertEqual(join['descriptor_classes'], ['TUniteAuSolDescriptor'])
        chain = join['configured_member_units'][0]['member_chain']
        self.assertEqual([step['role'] for step in chain], ['unit_descriptor'])

    def test_missing_and_ambiguous_joins_fail_closed(self):
        self.assertEqual(aar._join_one(self.index, '00'*16)['join_status'], 'missing')
        ambiguous = copy.deepcopy(self.index)
        ambiguous['descriptors'][G_COMPANY_B]['source_nodes'].append('3')
        join = aar._join_one(ambiguous, G_COMPANY_B)
        self.assertEqual(join['join_status'], 'ambiguous_descriptor')
        self.assertEqual(join['configured_member_units'][0]['debug_name'], 'Unit_C')

    def test_archive_authentication_is_exact(self):
        with self.assertRaises(replay.ReplayFormatError):
            aar.authenticate_archive(b'\0'*100)
        with self.assertRaises(replay.ReplayFormatError):
            aar.authenticate_archive(b'\0'*aar.ARCHIVE_SIZE)
        blob = synthetic_archive()
        with self.assertRaises(replay.ReplayFormatError):
            aar.authenticate_archive(blob)

    def test_synthetic_container_round_trips_before_authentication(self):
        # Authentication is a separate gate; extraction still works on unpinned bytes.
        expanded, source = aar.extract_everything(synthetic_archive())
        self.assertEqual(expanded, synthetic_expanded())
        self.assertEqual(source['compression_flag'], 128)
        self.assertEqual(source['declared_body_size'], len(expanded)-40)
        self.assertEqual(source['declared_total_size'], len(expanded))


class FailClosed(unittest.TestCase):
    def test_edat_checksum_and_member_hash_mismatch(self):
        blob = bytearray(synthetic_archive())
        blob[49] ^= 0xff
        with self.assertRaises(replay.ReplayFormatError):
            aar.read_edat(bytes(blob))
        blob = bytearray(synthetic_archive())
        blob[-1] ^= 0xff
        with self.assertRaises(replay.ReplayFormatError):
            aar.extract_everything(bytes(blob))

    def test_unknown_value_type_is_not_guessed(self):
        with self.assertRaises(replay.ReplayFormatError):
            aar._value(aar._Reader(u32(0x77)), [], [])

    def test_truncated_toc_is_rejected(self):
        expanded = synthetic_expanded()
        with self.assertRaises(replay.ReplayFormatError):
            aar.parse_ndf(expanded[:-1])
        with self.assertRaises(replay.ReplayFormatError):
            aar.parse_ndf(b'EUG0'+b'\0'*8)

    def test_cli_refuses_wrong_archive_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory)/'NDF_Win.dat'
            archive.write_bytes(b'not the pinned archive')
            output = Path(directory)/'out'
            with contextlib.redirect_stderr(io.StringIO()):
                code = aar.main(['--archive', str(archive), '--output', str(output)])
            self.assertEqual(code, 2)
            self.assertFalse((output/'unit-index-131544.json').exists())

    def test_cli_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output/'unit-index-131544.json').write_text('keep')
            archive = Path(directory)/'NDF_Win.dat'
            archive.write_bytes(b'not the pinned archive')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(aar.main(['--archive', str(archive), '--output', str(output)]), 2)
            self.assertEqual((output/'unit-index-131544.json').read_text(), 'keep')


class Authenticated131544(unittest.TestCase):
    """Real pinned archive/replay checks; skipped when private artifacts are absent."""

    @classmethod
    def setUpClass(cls):
        for path in (NDF, REPLAY_COMBAT, REPLAY_CONTROLLED):
            if not path.is_file():
                raise unittest.SkipTest('private artifact missing: '+str(path))
        cls.blob = NDF.read_bytes()
        cls.index = aar.build_index(cls.blob, NDF)

    def test_archive_and_projection_counts(self):
        source = self.index['source']
        self.assertEqual(source['sha256'], aar.ARCHIVE_SHA256)
        self.assertEqual(source['size'], aar.ARCHIVE_SIZE)
        self.assertEqual(source['member']['entry_sha256'],
                         '6b829a65c485346a03117f9074b1772198acc3fc28195abe923513b8799dc2c8')
        self.assertEqual(source['member']['expanded_sha256'],
                         '640c66c2336f6e54bb1e0183a76eecd2d1defe7fafe67ed56e7f82a5021ed032')
        self.assertFalse(source['member']['zlib_eof_marker'])
        self.assertEqual((len(self.index['descriptors']), len(self.index['unit_types'])),
                         (4845, 2227))
        self.assertEqual(self.index['parse']['objects'], 126019)
        self.assertEqual(self.index['parse']['non_null_references'], 385391)
        self.assertEqual(self.index['parse']['null_references'], 421)

    def test_both_controlled_replays_join_independently(self):
        expected = {
            REPLAY_COMBAT: ('abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121',
                            '00000000050000000300000014040000',
                            'Company_Merkava_IIIB_Baz', 'Unit_Merkava_IIIB_Baz'),
            REPLAY_CONTROLLED: ('1b060d2ab2e5501c6c8731fcb87ac0c7ac6dc4598387dcdb261ab8bb06bc8d70',
                                '00000000050000000300000019040000',
                                'Company_Oshkosh', 'Unit_Oshkosh'),
        }
        seen = set()
        for path, (sha, guid, company, member) in expected.items():
            with self.subTest(replay=path.name):
                doc = aar.join_replay(self.index, path.read_bytes(), path, expected_sha256=sha)
                self.assertEqual(doc['replay']['sha256'], sha)
                self.assertTrue(doc['replay']['version_matches_index'])
                self.assertEqual([join['validation_guid_hex'] for join in doc['joins']], [guid])
                join = doc['joins'][0]
                self.assertEqual(join['join_status'], 'exact_guid')
                self.assertEqual(join['descriptor_classes'], ['TUniteDescriptor'])
                self.assertIsNone(join['runtime_identity'])
                self.assertEqual(join['identity_status'], 'static_guid_join_only')
                chain = join['configured_member_units'][0]['member_chain']
                self.assertEqual([step['role'] for step in chain],
                                 ['company_descriptor', 'company_unit_module',
                                  'module_selector', 'member_unit_type'])
                self.assertEqual(chain[0]['debug_name'], company)
                self.assertEqual(chain[-1]['debug_name'], member)
                self.assertFalse(join['configured_member_units'][0]['conditions_evaluated'])
                seen.add(guid)
        self.assertEqual(len(seen), 2)

    def test_wrong_replay_hash_fails_closed(self):
        with self.assertRaises(replay.ReplayFormatError):
            aar.join_replay(self.index, REPLAY_COMBAT.read_bytes(), REPLAY_COMBAT,
                            expected_sha256='0'*64)

    def test_cli_writes_index_and_join_once(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'units'
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(aar.main(['--archive', str(NDF), '--output', str(output),
                                           '--replay', str(REPLAY_COMBAT)]), 0)
            manifest = json.loads((output/'unit-index-131544.manifest.json').read_text())
            index_bytes = (output/'unit-index-131544.json').read_bytes()
            self.assertEqual(hashlib.sha256(index_bytes).hexdigest(), manifest['index_sha256'])
            self.assertEqual(manifest['counts']['descriptors'], 4845)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(aar.main(['--archive', str(NDF), '--output', str(output)]), 2)


if __name__ == '__main__':
    unittest.main()
