"""Synthetic metadata-shape regressions; no external replay artifacts required."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from wgrd_corpus import inventory
from wgrd_replay import ReplayFormatError, parse_header, parse_replay


def replay_with_metadata(metadata):
    payload = json.dumps(metadata).encode('utf-8')
    body = b'rply' + struct.pack('>III', 0, len(payload), 0) + payload
    return (b'ESAV' + struct.pack('>II', 1, 40 + len(body))
            + hashlib.sha224(body).digest() + body)


class HeaderMetadataTests(unittest.TestCase):
    def test_rejects_nonobject_metadata_root(self):
        for value in (None, [], 'text', 42, 1.5, True):
            for parser in (parse_header, parse_replay):
                with self.subTest(value=value, parser=parser.__name__):
                    with self.assertRaisesRegex(ReplayFormatError, 'metadata.*object'):
                        parser(replay_with_metadata(value))

    def test_rejects_present_nonobject_game(self):
        for value in (None, [], 'text', 42, 1.5, False):
            for parser in (parse_header, parse_replay):
                with self.subTest(value=value, parser=parser.__name__):
                    with self.assertRaisesRegex(ReplayFormatError, 'game.*object'):
                        parser(replay_with_metadata({'game': value}))

    def test_preserves_objects_and_optional_game_version(self):
        for metadata, version in (({}, None), ({'game': {}}, None),
                                  ({'game': {'Version': '59638'}, 'other': [1]}, '59638')):
            with self.subTest(metadata=metadata):
                header, actual = parse_header(replay_with_metadata(metadata))
                self.assertEqual(actual, metadata)
                self.assertEqual(header['game_version'], version)

    def test_cli_reports_format_error_without_traceback(self):
        cli = Path(__file__).resolve().parents[1] / 'wgrd_replay.py'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.wargamerpl2'
            for metadata in ([], {'game': None}):
                path.write_bytes(replay_with_metadata(metadata))
                for flags in ([], ['--summary'], ['--timeline']):
                    with self.subTest(metadata=metadata, flags=flags):
                        result = subprocess.run([sys.executable, '-B', str(cli), str(path), *flags],
                                                capture_output=True, text=True)
                        self.assertEqual(result.returncode, 2)
                        self.assertEqual(result.stdout, '')
                        self.assertTrue(result.stderr.startswith('ReplayFormatError: '), result.stderr)
                        self.assertNotIn('Traceback', result.stderr)

    def test_cli_normalizes_nonfinite_metadata(self):
        cli = Path(__file__).resolve().parents[1] / 'wgrd_replay.py'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'nonfinite.wargamerpl2'
            path.write_bytes(replay_with_metadata({'values': [float('nan'), float('inf'), -float('inf')]}))
            for flags in ([], ['--summary'], ['--timeline']):
                with self.subTest(flags=flags):
                    result = subprocess.run([sys.executable, '-B', str(cli), str(path), *flags],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    out = json.loads(result.stdout, parse_constant=lambda s: self.fail(s))
                    self.assertEqual(out['metadata']['values'], [{'nonfinite': 'NaN'},
                        {'nonfinite': '+Infinity'}, {'nonfinite': '-Infinity'}])

    def test_corpus_classifies_shape_errors_as_expected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.wargamerpl2'
            for metadata in ([], {'game': None}):
                path.write_bytes(replay_with_metadata(metadata))
                for headers_only in (False, True):
                    with self.subTest(metadata=metadata, headers_only=headers_only):
                        row = inventory([path], headers_only=headers_only)['replays'][0]
                        self.assertEqual(row['compatibility'], 'error')
                        self.assertEqual(row['errors'][0]['stage'], 'header')
                        self.assertFalse(row['errors'][0].get('unexpected', False))


if __name__ == '__main__':
    unittest.main()
