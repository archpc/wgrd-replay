"""Current-executable order options, separate from historical kind evidence."""
import copy
import struct
import unittest

from test_orders import fields
from test_corpus import replay_bytes
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline
from wgrd_orders import decode_standard_order


class QueueOption(unittest.TestCase):
    def test_option_four_selects_append_not_dispatch_mode(self):
        for raw, policy in ((0, 'replace'), (1, 'append'), (2, 'append'), (255, 'append')):
            for mode in range(4):
                f = fields(39, mode=mode)
                option = bytearray.fromhex(f['obj_d0_hex'])
                option[4] = raw
                option[9:12] = b'\xff\x81\x7f'
                f['obj_d0_hex'] = option.hex()
                before = copy.deepcopy(f)
                result = decode_standard_order(f, False, replay_version='131544')
                p = result['parameters']
                q = p['queue_request']
                self.assertEqual((q['raw_u8'], q['policy']), (raw, policy))
                self.assertEqual(q['evidence_build'], '131544')
                self.assertEqual(q['status'], 'verified')
                self.assertIsNone(q['effective_queue_policy'])
                self.assertIsNone(p['effective_order_kind'])
                self.assertEqual(p['order_selection'], 'runtime_dependent')
                self.assertEqual(f, before)
                self.assertEqual(result['status'], 'inferred')  # Existing kind evidence unchanged.

    def test_other_build_and_unspecified_build_stay_inferred(self):
        for version in (None, '59638', '430000610', '510131544'):
            p = decode_standard_order(fields(), True, replay_version=version)['parameters']
            self.assertEqual(p['queue_request']['status'], 'inferred')

    def test_timeline_threads_exact_version_and_retains_stop_limits(self):
        f = fields(10)
        raw = (b'\x07' + struct.pack('<I', 1) + bytes.fromhex(f['obj_04_array']['items_hex'])
               + struct.pack('<I', 0) + bytes.fromhex(f['obj_bc_hex'] + f['obj_c8_hex'] + f['obj_d0_hex'])
               + struct.pack('<IH', 1, 0))
        parsed = parse_replay(replay_bytes(raw, version='131544'))
        p = build_timeline(parsed)['events'][0]['interpretation']['parameters']
        self.assertEqual(p['queue_request']['status'], 'verified')
        self.assertIsNone(p['queue_request']['effective_queue_policy'])
        self.assertEqual(p['position_status'], 'not_interpreted_for_stop_request')
        self.assertIn('Stop', ' '.join(p['queue_request']['limitations']))
