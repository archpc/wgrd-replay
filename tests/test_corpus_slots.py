"""Corpus IDs come from pacts, including slots that never issue a command."""
from contextlib import redirect_stdout
import hashlib
from io import StringIO
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest

from test_corpus import replay_bytes
from test_sparse_slots import replay_with_slots
from wgrd_corpus import inventory, main
from wgrd_replay import iter_chunks, parse_replay


class CorpusSlots(unittest.TestCase):
    def inspect_bytes(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.wargamerpl2'
            path.write_bytes(data)
            return inventory([path])['replays'][0]

    def test_all_empty_nonzero_slot_is_observed_without_counting_empty_blocks(self):
        row = self.inspect_bytes(replay_with_slots([[7], [7]], empty=True))
        self.assertEqual(row['compatibility'], 'structurally_compatible')
        self.assertEqual(row['observed_slots'], [7])
        self.assertEqual(row['slots_per_frame'], 1)
        self.assertEqual(row['block_statuses'], {})
        self.assertEqual(row['declared_commands'], 0)
        self.assertEqual(row['decoded_commands'], 0)
        self.assertEqual(row['decoded_opcodes'], {})
        self.assertEqual(row['timeline']['events'], 0)

    def test_mixed_active_and_empty_slots_preserve_nonempty_block_metrics(self):
        body = b''
        for _, tag, payload in iter_chunks(replay_bytes(), 40):
            if tag == b'pact':
                payload = payload[:4] + struct.pack('<I', 5) + payload[8:]
            body += tag + struct.pack('>III', 0, len(payload), 0) + payload
            if tag == b'pact':
                empty = struct.pack('<IIIH', 0, 9, 0, 0)
                body += b'pact' + struct.pack('>III', 0, len(empty), 0) + empty
        data = b'ESAV' + struct.pack('>II', 1, 40 + len(body)) + hashlib.sha224(body).digest() + body
        # A default parse alone cannot recover the empty-only slot 9.
        self.assertEqual([r['slot'] for r in parse_replay(data)['commands']], [5])
        row = self.inspect_bytes(data)
        self.assertEqual(row['compatibility'], 'structurally_compatible')
        self.assertEqual(row['observed_slots'], [5, 9])
        self.assertEqual(row['slots_per_frame'], 2)
        self.assertEqual(row['block_statuses'], {'complete': 1})
        self.assertEqual(row['declared_commands'], 1)
        self.assertEqual(row['decoded_commands'], 1)
        self.assertEqual(row['decoded_opcodes'], {'0x18': 1})
        self.assertEqual(row['timeline']['events'], 1)

    def test_archive_119_cli_reports_recorded_slot_one(self):
        location = os.environ.get('WGRD_CORPUS_DIR')
        if location is None:
            self.skipTest('private corpus unavailable: set WGRD_CORPUS_DIR')
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'samples/offline-corpus-manifest.json').read_text())
        sample = next(s for s in manifest['samples'] if s['archive_id'] == 119)
        paths = [p for p in Path(location).rglob('*.wargamerpl2')
                 if hashlib.sha256(p.read_bytes()).hexdigest() == sample['sha256']]
        self.assertTrue(paths, 'missing or altered archive 119')
        path = paths[0]
        self.assertEqual(path.stat().st_size, sample['size'])
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main([str(path)]), 0)
        row = json.loads(output.getvalue())['replays'][0]
        self.assertEqual(row['sha256'], sample['sha256'])
        self.assertTrue(row['digest_valid'])
        self.assertEqual(row['compatibility'], 'structurally_compatible')
        self.assertEqual(row['observed_slots'], [1])
        self.assertEqual(row['slots_per_frame'], 1)
        self.assertEqual(row['frames'], 3979)
        self.assertEqual(row['declared_commands'], 126)
        self.assertEqual(row['decoded_commands'], 126)
        self.assertEqual(row['timeline']['events'], 126)
        self.assertIsNone(row['slot_to_player_identity'])
