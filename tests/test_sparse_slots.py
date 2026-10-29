"""Synthetic whole-container regressions for recorded slot IDs, not player identities."""
import hashlib
import json
import struct
import unittest

from wgrd_replay import ReplayFormatError, parse_replay
from wgrd_timeline import build_timeline


def replay_with_slots(frames, empty=False):
    def chunk(tag, payload):
        return tag + struct.pack('>III', 0, len(payload), 0) + payload

    body = chunk(b'rply', json.dumps({'game': {'Version': '430000244'}}).encode())
    for frame, slots in enumerate(frames):
        body += chunk(b'star', struct.pack('<II', frame, 0))
        for slot in slots:
            block = b'' if empty else b'\x13' + struct.pack('<III', 0, 0, slot)
            body += chunk(b'pact', struct.pack('<IIIH', frame, slot, not empty, len(block)) + block)
        body += chunk(b'endt', struct.pack('<I', frame))
    return b'ESAV' + struct.pack('>II', 1, 40 + len(body)) + hashlib.sha224(body).digest() + body


class RecordedSlots(unittest.TestCase):
    def test_nonzero_slot_survives_whole_parse_and_timeline(self):
        data = replay_with_slots([[1], [1]])
        parsed = parse_replay(data)
        self.assertTrue(parsed['header']['digest_valid'])
        self.assertEqual(parsed['stats']['frames'], 2)
        self.assertEqual(parsed['stats']['slots_per_frame'], 1)
        events = build_timeline(parsed)['events']
        self.assertEqual([(e['frame'], e['player_slot']) for e in events], [(0, 1), (1, 1)])
        self.assertTrue(all(e['player_identity'] is None for e in events))

    def test_sparse_increasing_roster_preserves_ids_and_empty_pacts(self):
        for empty in (False, True):
            parsed = parse_replay(replay_with_slots([[1, 3], [1, 3]], empty), include_empty=True)
            self.assertEqual([r['slot'] for r in parsed['commands']], [1, 3, 1, 3])
            self.assertEqual(parsed['stats']['slots_per_frame'], 2)

    def test_duplicate_descending_and_changed_rosters_rejected(self):
        for frames in ([[1, 1]], [[3, 1]], [[1], [2]], [[1, 3], [1]], [[1], []], [[], [1]]):
            with self.subTest(frames=frames), self.assertRaises(ReplayFormatError):
                parse_replay(replay_with_slots(frames))

    def test_bad_digest_still_rejected_after_valid_sparse_walk(self):
        data = bytearray(replay_with_slots([[1]]))
        data[12] ^= 1
        with self.assertRaisesRegex(ReplayFormatError, 'SHA-224'):
            parse_replay(bytes(data))

    def test_frame_mismatch_and_unclosed_frame_still_rejected(self):
        data = replay_with_slots([[1]])
        for tag in (b'pact', b'endt'):
            damaged = bytearray(data)
            offset = damaged.index(tag) + 16
            struct.pack_into('<I', damaged, offset, 7)
            with self.subTest(tag=tag), self.assertRaises(ReplayFormatError):
                parse_replay(bytes(damaged), verify_digest=False)
        truncated = data[:data.index(b'endt')]
        truncated = truncated[:8] + struct.pack('>I', len(truncated)) + truncated[12:]
        with self.assertRaisesRegex(ReplayFormatError, 'inside frame'):
            parse_replay(truncated, verify_digest=False)
