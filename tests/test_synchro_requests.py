"""0x13 request-side membership operations from the revision-131544 consumer."""
import struct
import unittest

from test_corpus import replay_bytes
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline


class SynchroRequests(unittest.TestCase):
    def event(self, service=0, operation=0, member=0, version='131544'):
        raw = b'\x13' + struct.pack('<III', service, operation, member)
        event = build_timeline(parse_replay(replay_bytes(raw, version=version)))['events'][0]
        self.assertEqual(event['raw_hex'], raw.hex())
        self.assertEqual(event['parameters'], {'obj_04_u32': service, 'obj_08_u32': operation, 'obj_0c_u32': member})
        return event

    def test_add_remove_requests_preserve_raw_fields_without_outcome(self):
        for operation, label in ((0, 'add_member'), (1, 'remove_member')):
            event = self.event(operation=operation)
            interpretation = event['interpretation']
            self.assertEqual(interpretation['action'], 'player_synchro_service_request')
            self.assertEqual(interpretation['status'], 'partial')
            self.assertEqual(interpretation['execution_outcome'], 'unknown')
            p = interpretation['parameters']
            self.assertEqual(p['membership_operation'], label)
            self.assertEqual(p['service_index_u32'], 0)
            self.assertEqual(p['member_value_u32'], 0)
            self.assertTrue(p['member_matches_recorded_slot'])
            self.assertIsNone(p['effective_membership'])

    def test_noncorpus_values_are_not_rejected_or_assigned_a_phase(self):
        event = self.event(service=17, operation=99, member=0xffffffff)
        p = event['interpretation']['parameters']
        self.assertEqual(p['service_index_u32'], 17)
        self.assertEqual(p['operation_u32'], 99)
        self.assertIsNone(p['membership_operation'])
        self.assertEqual(p['member_value_u32'], 0xffffffff)
        self.assertFalse(p['member_matches_recorded_slot'])
        self.assertIsNone(event['player_identity'])
        self.assertIsNone(p['effective_membership'])

    def test_all_archive_novel_values_are_members_not_counts(self):
        for value in (4, 7, 8, 9, 11, 12, 15, 17, 19):
            p = self.event(member=value)['interpretation']['parameters']
            self.assertEqual(p['member_value_u32'], value)
            self.assertFalse(p['member_matches_recorded_slot'])

    def test_other_versions_remain_inferred(self):
        for version in ('59638', '430000244', '510131544'):
            self.assertEqual(self.event(version=version)['interpretation']['status'], 'inferred')
