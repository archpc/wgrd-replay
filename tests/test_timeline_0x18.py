"""Opcode 0x18 DeactivateSupply: attribution to 0x07 wire references (synthetic + corpus)."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import wgrd_replay as w
import wgrd_timeline as t
import wgrd_unit_data as ud


def replay(frames, version='59638'):
    metadata = json.dumps({'game': {'Version': version}, 'player_99': {'name': 'unmapped'}}).encode()

    def chunk(tag, payload):
        return tag + struct.pack('>III', 0, len(payload), 0) + payload
    body = b'rply' + struct.pack('>III', 0, len(metadata), 0) + metadata
    for frame, slots in enumerate(frames):
        body += chunk(b'star', struct.pack('<II', frame, 0))
        for slot, commands in enumerate(slots):
            block = b''.join(commands)
            body += chunk(b'pact', struct.pack('<IIIH', frame, slot, len(commands), len(block)) + block)
        body += chunk(b'endt', struct.pack('<I', frame))
    return b'ESAV' + struct.pack('>II', 1, 40 + len(body)) + hashlib.sha224(body).digest() + body


def ref(key, guid_byte):
    return struct.pack('<I', key) + bytes([guid_byte]) * 16


def op07(*actor_refs):
    """0x07: obj_04 array of 20-byte refs, empty obj_60 array, fixed tails, u32 f4=0, empty string."""
    arr = struct.pack('<I', len(actor_refs)) + b''.join(actor_refs)
    return (b'\x07' + arr + struct.pack('<I', 0) + bytes(12 + 8 + 36) + struct.pack('<I', 0)
            + struct.pack('<H', 0))


def op18(key, obj08=1, obj0c=1):
    return b'\x18' + struct.pack('<IIB', key, obj08, obj0c)


def events_of(out, opcode):
    return [e for e in out['events'] if e['opcode'] == opcode]


def target(event):
    return event['interpretation']['parameters']['target_reference']


class SupplyAttribution(unittest.TestCase):
    K, G = 0x11223344, 1

    def build(self, frames, version='59638', unit_data=None):
        return t.build_timeline(w.parse_replay(replay(frames, version)), unit_data)

    def test_positive_after_last(self):
        out = self.build([[[op07(ref(self.K, self.G))], []],
                          [[op18(self.K)], []]])
        e, = events_of(out, 0x18)
        i = e['interpretation']
        self.assertEqual(i['action'], 'deactivate_supply_request')
        self.assertEqual(i['status'], 'partial')
        self.assertEqual(i['execution_outcome'], 'unknown')
        self.assertEqual(i['parameters']['registry_key_u32'], self.K)
        self.assertEqual(i['parameters']['obj_08_u32'], 1)
        self.assertEqual(i['parameters']['obj_0c_u8'], 1)
        cat = out['entity_references']
        entry, = cat['entries']
        tr = target(e)
        self.assertEqual(tr['resolution'], 'unique_key')
        self.assertEqual(tr['reference_id'], entry['reference_id'])
        self.assertEqual(tr['validation_guid_hex'], entry['validation_guid_hex'])
        self.assertTrue(tr['issuing_slot_in_observed_slots'])
        self.assertEqual(tr['temporal_relation'], 'after_last')
        self.assertEqual(tr['candidate_reference_ids'], [entry['reference_id']])
        self.assertIsNone(tr['unit_type'])
        self.assertEqual(entry['supply_request_occurrences'], 1)
        self.assertIn('research/OP18-SUPPLY-TARGETS.md', i['evidence'])
        self.assertFalse(any('not 59638' in s for s in i['limitations']))
        json.dumps(out, allow_nan=False)

    def test_positive_before_first(self):
        out = self.build([[[op18(self.K)], []],
                          [[op07(ref(self.K, self.G))], []]])
        e, = events_of(out, 0x18)
        self.assertEqual(target(e)['resolution'], 'unique_key')
        self.assertEqual(target(e)['temporal_relation'], 'before_first')

    def test_unreferenced_key(self):
        out = self.build([[[op07(ref(self.K, self.G)), op18(0xdead)], []]])
        e, = events_of(out, 0x18)
        tr = target(e)
        self.assertEqual(tr['resolution'], 'unreferenced_key')
        self.assertIsNone(tr['reference_id'])
        self.assertIsNone(tr['validation_guid_hex'])
        self.assertEqual(tr['candidate_reference_ids'], [])
        self.assertIsNone(tr['issuing_slot_in_observed_slots'])
        self.assertIsNone(tr['temporal_relation'])
        self.assertIsNone(tr['unit_type'])

    def test_ambiguous_key_never_assigns(self):
        out = self.build([[[op07(ref(self.K, 1), ref(self.K, 2)), op18(self.K)], []]])
        e, = events_of(out, 0x18)
        tr = target(e)
        self.assertEqual(tr['resolution'], 'ambiguous_key')
        self.assertIsNone(tr['reference_id'])
        self.assertIsNone(tr['validation_guid_hex'])
        self.assertIsNone(tr['unit_type'])
        self.assertEqual(len(tr['candidate_reference_ids']), 2)
        entries = out['entity_references']['entries']
        self.assertEqual(len(entries), 2)
        self.assertTrue(all(en['lookup_key_ambiguous'] for en in entries))
        self.assertEqual(sorted(tr['candidate_reference_ids']), sorted(en['reference_id'] for en in entries))
        self.assertTrue(all(en['supply_request_occurrences'] == 0 for en in entries))

    def test_slot_mismatch(self):
        # 0x07 by slot 0 only (frame 0), 0x18 by slot 1 in frame 1.
        out = self.build([[[op07(ref(self.K, self.G))], []], [[], [op18(self.K)]]])
        e, = events_of(out, 0x18)
        tr = target(e)
        self.assertEqual(e['player_slot'], 1)
        self.assertEqual(tr['resolution'], 'slot_mismatch')
        self.assertIsNone(tr['reference_id'])
        self.assertIsNone(tr['validation_guid_hex'])
        self.assertFalse(tr['issuing_slot_in_observed_slots'])
        self.assertEqual(len(tr['candidate_reference_ids']), 1)
        self.assertIsNone(tr['unit_type'])

    def test_unit_data_absent_status_partial_on_59638(self):
        out = self.build([[[op07(ref(self.K, self.G))], []], [[op18(self.K)], []]])
        e, = events_of(out, 0x18)
        self.assertEqual(e['interpretation']['status'], 'partial')
        self.assertIsNone(target(e)['unit_type'])

    def test_other_build_inferred_and_limitation(self):
        out = self.build([[[op07(ref(self.K, self.G))], []], [[op18(self.K)], []]], version='other')
        e, = events_of(out, 0x18)
        self.assertEqual(e['interpretation']['status'], 'inferred')
        self.assertEqual(target(e)['resolution'], 'unique_key')
        self.assertTrue(any('Sample build is not 59638; layout inferred.' == s
                            for s in e['interpretation']['limitations']))


class AuthenticSupplyAttribution(unittest.TestCase):
    UNIT_DATA = ROOT / 'research' / 'unit-data' / 'build59638-v1.json.gz'

    def samples(self):
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR',
                                      str(Path.home() / '.hermes/artifacts/wgrd-replay/samples/raw')))
        manifest = json.loads((ROOT / 'samples/manifest.json').read_text())
        found = {}
        for sample in manifest['samples']:
            path = samples / sample['file']
            if path.exists():
                for key in ('Sample1', 'Sample2', 'Sample3'):
                    if key in sample['file']:
                        found[key] = path
        if not found:
            self.skipTest('authentic samples not present')
        return found

    @staticmethod
    def _op18_analyse():
        spec = importlib.util.spec_from_file_location('op18_supply_targets',
                                                      ROOT / 'research' / 'op18_supply_targets.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_corpus_resolution_and_unit_types(self):
        samples = self.samples()
        unit_data = ud.load_unit_data(str(self.UNIT_DATA))
        expected_names = {
            'Sample1': (19, {'Unit_Terra_865BM_KPI', 'Unit_T815_Kolos', 'Unit_MI_4_CZ_LOG', 'Unit_MD_Jupiter_cargo'}),
            'Sample2': (0, set()),
            'Sample3': (25, {'Unit_Terra_865BM_KPI', 'Unit_MAN_Kat1_6x6', 'Unit_M35_Cargo', 'Unit_ZIL_130_NK',
                             'Unit_Ural_4320', 'Unit_Star_266'}),
        }
        op18 = self._op18_analyse()
        for key, (count, names) in expected_names.items():
            if key not in samples:
                continue
            with self.subTest(sample=key):
                out = t.build_timeline(w.parse_replay(samples[key].read_bytes()), unit_data)
                events = events_of(out, 0x18)
                self.assertEqual(len(events), count)
                self.assertTrue(all(target(e)['resolution'] == 'unique_key' for e in events))
                self.assertTrue(all(target(e)['unit_type']['status'] == 'unique' for e in events))
                got = {c['debug_name'] for e in events for c in target(e)['unit_type']['candidates']}
                self.assertEqual(got, names)
                self.assertTrue(all(e['interpretation']['status'] == 'partial' for e in events))
                analysis = op18.analyse(str(samples[key]), unit_data)
                self.assertEqual(analysis['events'], count)
                self.assertEqual(analysis['unique'], count)
                self.assertEqual(analysis['slot_ok'], count)
                self.assertEqual(analysis['failures'], [])
                json.dumps(out, allow_nan=False)

    def test_corpus_without_unit_data(self):
        samples = self.samples()
        for key, count in (('Sample1', 19), ('Sample3', 25)):
            if key not in samples:
                continue
            with self.subTest(sample=key):
                out = t.build_timeline(w.parse_replay(samples[key].read_bytes()))
                events = events_of(out, 0x18)
                self.assertEqual(len(events), count)
                self.assertTrue(all(target(e)['resolution'] == 'unique_key' for e in events))
                self.assertTrue(all(target(e)['unit_type'] is None for e in events))


if __name__ == '__main__':
    unittest.main()
