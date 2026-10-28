"""CI checks must reject new broken links and malformed Python without writes."""
import importlib.util
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocumentationChecks(unittest.TestCase):
    def test_links_resolve_only_to_tracked_targets(self):
        docs = load_script('check_docs')
        tracked = {'docs/guide.md', 'README.md', 'docs/space name.md'}
        self.assertEqual(docs.check_line('docs/guide.md', '[root](../README.md#top)', tracked, {}), [])
        self.assertEqual(docs.check_line('docs/guide.md', '[space](<space name.md>)', tracked, {}), [])
        self.assertEqual(docs.check_line('docs/guide.md', '[title](missing.md "Title")', tracked, {}), ['missing.md'])
        self.assertEqual(docs.check_line('docs/guide.md', '[local](work/local.json)', tracked, {}), ['work/local.json'])
        self.assertEqual(docs.check_line('docs/guide.md', 'this[5](match) [WgrdUi]::Capture(x)', tracked, {}), [])
        self.assertEqual(docs.check_line('docs/guide.md', '[web](https://example.com) [anchor](#top)', tracked, {}), [])


class SyntaxChecks(unittest.TestCase):
    def test_compile_rejects_syntax_and_leaves_no_bytecode(self):
        syntax = load_script('check_python')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'example.py'
            path.write_text('return 1\n')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertFalse(syntax.check_files([path]))
            path.write_text('value = 1\n')
            self.assertTrue(syntax.check_files([path]))
            self.assertEqual(list(Path(directory).iterdir()), [path])


class PrivateFixtureGuards(unittest.TestCase):
    def test_missing_private_sample_skips_but_corruption_fails(self):
        import hashlib
        from private_fixtures import require_private_samples
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = {'file': 'private.bin', 'size': 3, 'sha256': hashlib.sha256(b'abc').hexdigest()}
            with self.assertRaises(unittest.SkipTest):
                require_private_samples(root, [sample])
            (root / 'private.bin').write_bytes(b'abc')
            require_private_samples(root, [sample])
            (root / 'private.bin').write_bytes(b'bad')
            with self.assertRaises(AssertionError):
                require_private_samples(root, [sample])
            # An absent sibling must not mask evidence corruption that is present.
            with self.assertRaises(AssertionError):
                require_private_samples(root, [dict(sample, file='missing.bin'), sample])


class PartialPrivateCorpus(unittest.TestCase):
    def test_present_sample_runs_when_siblings_are_missing(self):
        import json
        import os
        from unittest.mock import patch
        import test_entities
        manifest = json.loads((ROOT / 'samples/manifest.json').read_text())['samples']
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home() / '.hermes/artifacts/wgrd-replay/samples/raw')))
        source = samples / manifest[0]['file']
        if not source.exists():
            self.skipTest('private replay fixture unavailable for partial-corpus regression')

        class RecordingResult(unittest.TestResult):
            def __init__(self):
                super().__init__()
                self.passed_samples = 0

            def addSubTest(self, test, subtest, error):
                super().addSubTest(test, subtest, error)
                if error is None:
                    self.passed_samples += 1

        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / source.name).symlink_to(source.resolve())
            with patch.dict(os.environ, {'WGRD_SAMPLES_DIR': directory}):
                case = test_entities.AuthenticEntityCatalog('test_all_samples_reference_counts_and_links')
                result = RecordingResult()
                case.run(result)
        self.assertTrue(result.wasSuccessful(), (result.errors, result.failures))
        self.assertEqual(result.passed_samples, 1)
        self.assertEqual(len(result.skipped), 2)


class PreservationChecks(unittest.TestCase):
    def test_evidence_revision_manifest_and_cow_corruption_fail(self):
        import json
        import shutil
        from unittest.mock import patch
        check = load_script('check_preservation')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ['research/maintenance/preservation-manifest.json',
                     'research/maintenance/work-artifacts-manifest.json', 'wgrd_orders.py']
            historical = json.loads((ROOT / paths[0]).read_text())
            copies = json.loads((ROOT / paths[1]).read_text())
            paths += [e.get('moved_to') or e['path'] for e in historical['entries']]
            paths += [e['copied_to'] for e in copies['entries'] if e.get('copied_to')]
            for path in set(paths):
                dest = root / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, dest)
            with patch.object(check, 'ROOT', root):
                self.assertEqual(check.problems(), [])
                for path in ['research/op0c_layout.py',
                             next(e['copied_to'] for e in copies['entries'] if e.get('copied_to')),
                             paths[0], paths[1], 'wgrd_orders.py']:
                    target = root / path
                    original = target.read_bytes()
                    target.write_bytes(original.replace(b'(oo)', b'(xx)') if path == 'wgrd_orders.py'
                                       else original + b'\n')
                    self.assertTrue(check.problems(), path)
                    target.write_bytes(original)
                evidence = root / next(e['copied_to'] for e in copies['entries'] if e.get('copied_to'))
                evidence.unlink()
                self.assertTrue(check.problems(), 'missing archived evidence')
                shutil.copyfile(ROOT / evidence.relative_to(root), evidence)
                (root / 'README.md').unlink()
                self.assertTrue(check.problems(), 'allowed_changes still requires existence')


class MarkdownLinkSemantics(unittest.TestCase):
    def test_links_are_relative_to_document_not_repo_fallback(self):
        docs = load_script('check_docs')
        self.assertEqual(docs.check_line('docs/guide.md', '[x](README.md)', {'README.md'}, {}), ['README.md'])

    def test_prose_is_not_a_link_and_examples_are_not_links(self):
        docs = load_script('check_docs')
        self.assertEqual(docs.check_line('docs/guide.md', '`unknown.py` and `[x](example.md)`', set(), {}), [])

    def test_fenced_examples_are_ignored_but_prose_links_fail(self):
        from unittest.mock import patch
        docs = load_script('check_docs')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'README.md'
            path.write_text('```markdown\n[x](missing.md)\n```\n'
                            '~~~~\n[x](missing.md)\n~~~\n[x](missing.md)\n~~~~\n')
            with patch.object(docs, 'ROOT', root), \
                    patch.object(docs.subprocess, 'check_output', return_value=b'README.md\0'), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(docs.main(), 0)
                path.write_text(path.read_text() + '[real link](missing.md)\n')
                self.assertEqual(docs.main(), 1)
