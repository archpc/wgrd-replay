"""Offline corpus checks. Private inputs require WGRD_CORPUS_DIR; absence skips."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from research.offline_corpus import census, measure
from test_corpus import replay_bytes
from test_production import fields, wire
from test_sparse_slots import replay_with_slots
from wgrd_replay import ReplayFormatError, parse_replay
from wgrd_timeline import build_timeline

ROOT = Path(__file__).resolve().parents[1]


class CensusMechanics(unittest.TestCase):
    def test_synthetic_census_requires_pinned_identity(self):
        data = replay_with_slots([[1], [1]])
        row = measure(data)
        self.assertEqual(row['commands'], 2)
        self.assertEqual(row['slots'], [1])
        self.assertEqual(row['counts']['synchro_member_matches_slot'], {'True': 2})
        sample = {k: row[k] for k in ('sha256', 'version', 'size', 'commands')}
        sample['archive_id'] = 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'synthetic.wargamerpl2'
            path.write_bytes(data)
            result = census(Path(tmp), {'samples': [sample]})
            self.assertEqual((result['files'], result['commands']), (1, 2))
            path.write_bytes(data[:-1])
            with self.assertRaisesRegex(ValueError, 'missing or altered'):
                census(Path(tmp), {'samples': [sample]})

    def test_measure_rejects_whole_frame_and_command_errors(self):
        with self.assertRaises(ReplayFormatError):
            measure(replay_with_slots([[1], [2]]))
        with self.assertRaises(ValueError):
            measure(replay_bytes(b'\xff', 1))
        with self.assertRaises(ReplayFormatError):
            measure(replay_bytes(b'\x07', 1))

    def test_large_production_and_empty_nested_arrays_remain_supported(self):
        for nested in ([[1]] * 12, [], [[7, 9], []]):
            raw = wire(fields(3, positions=[(1., 2., 3., 2)] * 12, counts=[1] * 12, nested=nested))
            event = build_timeline(parse_replay(replay_bytes(raw)))['events'][0]
            p = event['interpretation']['parameters']
            self.assertEqual(event['interpretation']['payload_layout_status'], 'complete')
            self.assertEqual(p['requested_quantity'], 12)
            self.assertEqual(p['obj_98_nested_u32'], nested)
            self.assertIsNone(p['effective_deployment_positions'])
            self.assertEqual(event['interpretation']['execution_outcome'], 'unknown')
            # Observed quantity/nested equality is not a parser acceptance rule.
            self.assertTrue(p['parallel_group_counts_agree'])


class AuthenticOfflineCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        location = os.environ.get('WGRD_CORPUS_DIR')
        if location is None:
            raise unittest.SkipTest('private corpus unavailable: set WGRD_CORPUS_DIR')
        cls.directory = Path(location)
        cls.manifest = json.loads((ROOT/'samples/offline-corpus-manifest.json').read_text())
        # An explicitly supplied but missing/altered corpus is a failure, not a skip.
        cls.report = census(cls.directory, cls.manifest)

    def test_every_pinned_file_whole_parses_and_exports_all_commands(self):
        self.assertEqual((self.report['files'], self.report['commands']), (71, 208666))
        self.assertEqual(len({r['sha256'] for r in self.report['replays']}), 71)
        row = next(r for r in self.report['replays'] if r['archive_id'] == 119)
        self.assertTrue(row['digest_valid'])
        self.assertEqual((row['frames'], row['pacts'], row['commands'], row['slots']), (3979, 3979, 126, [1]))
        self.assertEqual(row['counts']['opcodes']['0x0d'], 15)

    def test_order_and_synchro_observations_are_corpus_scoped(self):
        c = self.report['counts']
        self.assertEqual(c['opcodes']['0x07'], 181888)
        self.assertEqual(c['dispatch_modes'], {'1': 181888})
        self.assertEqual(c['queue_option'], {'0': 178342, '1': 3546})
        self.assertEqual(c['synchro_member_matches_slot'], {'True': 222})
        self.assertEqual(c['synchro_service'], {'0': 222})
        self.assertEqual(c['synchro_operation'], {'0': 181, '1': 41})
        self.assertEqual(c['synchro_transitions'], {'0:1': 41, '1:0': 34})
        self.assertTrue({str(v) for v in (4, 7, 8, 9, 11, 12, 15, 17, 19)} <= set(c['synchro_member']))

    def test_production_shapes_and_both_twelve_group_records(self):
        c = self.report['counts']
        self.assertEqual(c['opcodes']['0x0d'], 18556)
        self.assertEqual(c['nested_quantity_relation'], {'empty_outer': 774, 'equal': 15646})
        row = next(r for r in self.report['replays'] if r['archive_id'] == 194)
        examples = [e for e in row['large_groups'] if e['shape'][0] == 12]
        self.assertEqual([(e['frame'], e['slot'], e['file_offset']) for e in examples],
                         [(1816, 19, 1285317), (20963, 6, 14847550)])
        self.assertTrue(all(e['quantities'] == [1] * 12 for e in examples))
        # The whole-source identity remains pinned after analysis.
        expected = {s['sha256'] for s in self.manifest['samples']}
        actual = {hashlib.sha256(p.read_bytes()).hexdigest() for p in self.directory.rglob('*.wargamerpl2')}
        self.assertTrue(expected <= actual)
