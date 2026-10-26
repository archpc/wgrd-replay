"""Opcode 0x0C timeline interpretation: raw-field parameters, no semantic claims."""
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wgrd_replay as w
import wgrd_timeline as t


def u(*values):
    return struct.pack('<' + 'I' * len(values), *values)


def replay(slots, version='59638'):
    metadata = json.dumps({'game': {'Version': version}, 'player_99': {'name': 'unmapped'}}).encode()
    def chunk(tag, payload):
        return tag + struct.pack('>III', 0, len(payload), 0) + payload
    body = b'rply' + struct.pack('>III', 0, len(metadata), 0) + metadata
    body += chunk(b'star', struct.pack('<II', 0, 0))
    for slot, (count, block) in enumerate(slots):
        body += chunk(b'pact', struct.pack('<IIIH', 0, slot, count, len(block)) + block)
    body += chunk(b'endt', struct.pack('<I', 0))
    return b'ESAV' + struct.pack('>II', 1, 40 + len(body)) + hashlib.sha224(body).digest() + body


def op0c(player_id=0xc000001e, arr18=(1,), arr34=(3,), pts50=((1.0, 2.0, 3.0, 2),),
         pts9c=(((float('inf'), float('inf'), float('inf'), 0)),), arr_e8=(0x4030dd88,), c=0):
    body = b'\x0c' + u(player_id) + bytes(16) + u(len(arr18), *arr18) + u(len(arr34), *arr34)
    body += u(len(pts50)) + b''.join(struct.pack('<3fI', *p[:3], p[3]) for p in pts50)
    body += u(len(pts9c)) + b''.join(struct.pack('<3fI', *p[:3], p[3]) for p in pts9c)
    body += u(len(arr_e8), *arr_e8) + u(c) + bytes(16)
    return body


def _only_0c(out):
    events = [e for e in out['events'] if e['opcode'] == 0x0c]
    assert len(events) == 1, events
    return events[0]


class SyntheticChangeProduction(unittest.TestCase):
    def build(self, block, slot=0):
        slots = [(0, b'')] * slot + [(1, block)]
        return t.build_timeline(w.parse_replay(replay(slots)))

    def test_matching_build_raw_parameters_partial(self):
        block = op0c()
        out = self.build(block)
        e = _only_0c(out)
        i = e['interpretation']
        self.assertEqual(e['decode_status'], 'layout')
        self.assertEqual(i['status'], 'partial')
        self.assertEqual(i['action'], 'change_production_request')
        self.assertEqual(i['execution_outcome'], 'unknown')
        self.assertEqual(i['payload_layout_status'], 'complete')
        self.assertEqual(i['evidence_build'], '59638')
        p = i['parameters']
        self.assertEqual(p['player_id_u32'], 0xc000001e)
        self.assertTrue(p['slot_consistent'])
        self.assertEqual(p['obj_08_hex'], bytes(16).hex())
        self.assertEqual(p['obj_18_u32_items'], [1])
        self.assertEqual(p['obj_34_u32_items'], [3])
        self.assertEqual(p['obj_50_points'], [{'xyz_f32': [1.0, 2.0, 3.0], 'kind_u32': 2}])
        self.assertEqual(p['obj_9c_points'], [{'xyz_f32': [{'nonfinite': '+Infinity'}] * 3, 'kind_u32': 0}])
        self.assertEqual(p['obj_e8_u32_items'], [0x4030dd88])
        self.assertEqual(p['obj_104_u32'], 0)
        self.assertEqual(p['obj_108_hex'], bytes(16).hex())
        for forbidden in ('position', 'heading', 'production_type', 'quantity'):
            self.assertFalse(any(forbidden in k for k in p), forbidden)
        self.assertTrue(any('unconfirmed' in s for s in i['limitations']))
        self.assertTrue(any('consumer' in s.lower() for s in i['limitations']))
        self.assertTrue(any('research/CHANGEPRODUCTION-0C.md' in s for s in i['evidence']))
        self.assertTrue(any('FUN_00b2eeb0' in s for s in i['evidence']))
        self.assertNotIn('limitation', i)
        self.assertEqual(bytes.fromhex(e['raw_hex']), block)
        json.dumps(out, allow_nan=False)

    def test_slot_consistent_true_on_second_slot(self):
        e = _only_0c(self.build(op0c(player_id=0xc000001e + 1), slot=1))
        self.assertEqual(e['player_slot'], 1)
        self.assertTrue(e['interpretation']['parameters']['slot_consistent'])

    def test_slot_consistent_false_when_id_mismatches_slot(self):
        e = _only_0c(self.build(op0c(player_id=0xc000001e + 1), slot=0))
        self.assertEqual(e['interpretation']['parameters']['player_id_u32'], 0xc000001f)
        self.assertFalse(e['interpretation']['parameters']['slot_consistent'])

    def test_variable_length_arrays_preserved_in_order(self):
        pts = ((1.0, 2.0, 3.0, 1), (4.0, 5.0, 6.0, 6))
        e = _only_0c(self.build(op0c(arr18=(2, 5, 9), arr34=(0, 14), pts50=pts)))
        p = e['interpretation']['parameters']
        self.assertEqual(p['obj_18_u32_items'], [2, 5, 9])
        self.assertEqual(p['obj_34_u32_items'], [0, 14])
        self.assertEqual([x['kind_u32'] for x in p['obj_50_points']], [1, 6])

    def test_inferred_on_other_build(self):
        out = t.build_timeline(w.parse_replay(replay([(1, op0c())], version='other')))
        i = _only_0c(out)['interpretation']
        self.assertEqual(i['status'], 'inferred')
        self.assertEqual(i['action'], 'change_production_request')
        self.assertIn('limitation', i)
        self.assertTrue(any('not 59638' in s for s in i['limitations']))

    def test_no_0c_event_left_unknown(self):
        out = self.build(op0c())
        self.assertNotEqual(_only_0c(out)['interpretation']['status'], 'unknown')


class AuthenticChangeProduction(unittest.TestCase):
    def test_corpus_counts_and_status(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'samples/manifest.json').read_text())
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home() / '.hermes/artifacts/wgrd-replay/samples/raw')))
        expected = {'Sample1': (13, 'partial'), 'Sample3': (28, 'partial'), 'Sample2': (6, 'inferred')}
        present = [s for s in manifest['samples'] if (samples / s['file']).exists()]
        if not present:
            self.skipTest('authentic samples not present under ' + str(samples))
        for sample in manifest['samples']:
            key = next(k for k in expected if k in sample['file'])
            path = samples / sample['file']
            if not path.exists():
                self.skipTest('missing sample ' + sample['file'])
            count, status = expected[key]
            out = t.build_timeline(w.parse_replay(path.read_bytes()))
            events = [e for e in out['events'] if e['opcode'] == 0x0c]
            with self.subTest(sample=key):
                self.assertEqual(len(events), count)
                self.assertTrue(all(e['interpretation']['action'] == 'change_production_request' for e in events))
                self.assertTrue(all(e['interpretation']['status'] == status for e in events))
                self.assertFalse(any(e['interpretation']['status'] == 'unknown' for e in events))
                self.assertTrue(all(e['interpretation']['execution_outcome'] == 'unknown' for e in events))
                json.dumps(out, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
