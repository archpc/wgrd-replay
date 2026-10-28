"""0x07 semantics from recorded 59638 execution evidence, no simulated outcomes."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import sys
import unittest
from private_fixtures import require_private_samples

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wgrd_replay as w
import wgrd_orders as orders
import wgrd_timeline as timeline


def fields(kind=4, actors=None, targets=None, position=(12., 24., 36.), mode=1):
    actors = [bytes.fromhex('ba0000c00000000000000000030000005f080000')] if actors is None else actors
    targets = [] if targets is None else targets
    options = bytearray(36)
    options[:4] = bytes([0, 0, 1, 0])
    struct.pack_into('<II', options, 16, kind, 3)
    block = (b'\x07' + struct.pack('<I', len(actors)) + b''.join(actors)
             + struct.pack('<I', len(targets)) + b''.join(targets)
             + struct.pack('<fff', *position) + struct.pack('<ff', math.inf, math.inf)
             + options + struct.pack('<IH', mode, 0))
    decoded = w.decode_command_block(block, 1, 0)
    assert decoded['status'] == 'complete'
    return decoded['commands'][0]['fields']


class StandardOrders(unittest.TestCase):
    def test_discriminator_enum_and_mode_independence(self):
        expected = {1: 'Land', 4: 'Move', 6: 'Attack', 10: 'Stop', 14: 'UnloadFromTransport',
                    15: 'MergeCompany', 16: 'MoveAndAttack', 19: 'Shoot', 20: 'SplitCompany',
                    27: 'Reverse', 28: 'Spread'}
        for kind, name in expected.items():
            for mode in range(4):
                with self.subTest(kind=kind, mode=mode):
                    out = orders.decode_standard_order(fields(kind, mode=mode), True)
                    p = out['parameters']
                    self.assertEqual(p['order_kind_u32'], kind)
                    self.assertEqual(p['order_kind'], name)
                    self.assertEqual(p['dispatch_mode_u32'], mode)
                    self.assertEqual(out['status'], 'verified')
                    self.assertEqual(p['order_selection'], 'explicit_request')
                    self.assertIsNone(p['effective_order_kind'])

    def test_contextual_sentinel_never_claims_move_or_attack(self):
        out = orders.decode_standard_order(fields(39), True)
        p = out['parameters']
        self.assertEqual(p['order_kind'], None)
        self.assertEqual(p['order_kind_enum_name'], 'Length')
        self.assertEqual(p['order_selection'], 'runtime_dependent')
        self.assertEqual(out['status'], 'partial')
        self.assertIsNone(p['effective_order_kind'])

    def test_unknown_kind_stays_partial_and_retains_all_bytes(self):
        f = fields(0xffffffff)
        before = copy.deepcopy(f)
        out = orders.decode_standard_order(f, True)
        self.assertIsNone(out['parameters']['order_kind'])
        self.assertEqual(out['parameters']['order_selection'], 'unknown')
        self.assertEqual(out['status'], 'partial')
        self.assertEqual(out['parameters']['order_structure_hex'], f['obj_d0_hex'])
        self.assertEqual(f, before)

    def test_actor_target_roles_and_complete_reference_identity(self):
        a = bytes.fromhex('ba0000c00000000000000000030000005f080000')
        # Same lookup key, different remaining identity bytes: never merge these.
        other = a[:4] + bytes([1]) + a[5:]
        out = orders.decode_standard_order(fields(6, [a, other], [other, a]), True)
        p = out['parameters']
        self.assertEqual([r['reference_hex'] for r in p['actor_references']], [a.hex(), other.hex()])
        self.assertEqual([r['reference_hex'] for r in p['target_references']], [other.hex(), a.hex()])
        self.assertEqual(p['actor_references'][0]['lookup_key_u32'], 0xc00000ba)
        self.assertNotEqual(p['actor_references'][0], p['actor_references'][1])
        self.assertEqual(p['reference_resolution'], 'runtime_required')
        self.assertEqual(out['execution_outcome'], 'unknown')

    def test_position_argument_and_absent_nonfinite_cases(self):
        p = orders.decode_standard_order(fields(), True)['parameters']
        self.assertEqual(p['target_position_argument_f32'], [12., 24., 36.])
        self.assertEqual(p['position_status'], 'transmitted_argument')
        self.assertIsNone(p['effective_target_position_f32'])
        for position, status in [((math.inf,)*3, 'absent_sentinel'),
                                 ((math.nan, 0., 1.), 'nonfinite'),
                                 ((math.inf, 0., 1.), 'nonfinite')]:
            p = orders.decode_standard_order(fields(position=position), True)['parameters']
            self.assertIsNone(p['target_position_argument_f32'])
            self.assertEqual(p['position_status'], status)
            json.dumps(p, allow_nan=False)
        # Stop's zeros are bytes, not a destination claim.
        p = orders.decode_standard_order(fields(10, position=(0.,)*3), True)['parameters']
        self.assertEqual(p['position_status'], 'not_interpreted_for_stop_request')
        self.assertIsNone(p['target_position_argument_f32'])

    def test_other_build_never_verified(self):
        for kind in (4, 6, 39, 0xffffffff):
            self.assertEqual(orders.decode_standard_order(fields(kind), False)['status'], 'inferred')

    def test_bad_decoded_field_lengths_rejected(self):
        for key, replacement in [('obj_d0_hex', '00'), ('obj_bc_hex', '00'), ('obj_c8_hex', 'zz')]:
            f = fields(); f[key] = replacement
            with self.assertRaises(w.ReplayFormatError): orders.decode_standard_order(f, True)
        f = fields(); f['obj_04_array']['count_u32'] += 1
        with self.assertRaises(w.ReplayFormatError): orders.decode_standard_order(f, True)

    def test_timeline_uses_new_semantics(self):
        out = timeline._interpretation(7, fields(6), True)
        self.assertEqual(out['parameters']['order_kind'], 'Attack')
        self.assertEqual(out['status'], 'verified')


class AuthenticOrders(unittest.TestCase):
    def test_all_10461_order_requests_and_raw_fields(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'samples/manifest.json').read_text())
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home() / '.hermes/artifacts/wgrd-replay/samples/raw')))
        expected = [(3794, 476, 3318), (86, 31, 55), (6581, 1321, 5260)]
        for sample, (total, explicit, contextual) in zip(manifest['samples'], expected):
            with self.subTest(sample=sample['file']):
                require_private_samples(samples, [sample])
                b = (samples / sample['file']).read_bytes()
                self.assertEqual(hashlib.sha256(b).hexdigest(), sample['sha256'])
                parsed = w.parse_replay(b)
                result = timeline.build_timeline(parsed)
                events = [e for e in result['events'] if e['opcode'] == 7]
                self.assertEqual(len(events), total)
                counts = {'explicit_request': 0, 'runtime_dependent': 0}
                for e in events:
                    p = e['interpretation']['parameters']; f = e['parameters']
                    counts[p['order_selection']] += 1
                    self.assertEqual(p['order_kind_u32'], struct.unpack_from('<I', bytes.fromhex(f['obj_d0_hex']), 16)[0])
                    for name, field in [('actor_references', 'obj_04_array'), ('target_references', 'obj_60_array')]:
                        self.assertEqual(''.join(r['reference_hex'] for r in p[name]), f[field]['items_hex'])
                        self.assertEqual(len(p[name]), f[field]['count_u32'])
                    source = e['source']
                    self.assertEqual(bytes.fromhex(e['raw_hex']), b[source['file_offset']:source['file_offset']+source['length']])
                    if sample['game_version'] != '59638': self.assertEqual(e['interpretation']['status'], 'inferred')
                self.assertEqual(counts, {'explicit_request': explicit, 'runtime_dependent': contextual})
                json.dumps(result, allow_nan=False)


if __name__ == '__main__': unittest.main()
