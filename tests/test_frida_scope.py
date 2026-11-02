"""Scoped hook and return-value capture mechanics, not engine semantics."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scope_controller', ROOT/'instrumentation/wgrd_frida.py')
assert spec is not None and spec.loader is not None
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)

PINNED_PE = Path(os.environ.get('WGRD_ENGINE_PE', str(
    Path.home()/'.hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe')))
V3_CONFIG = ROOT/'instrumentation/aar-capture-131544-v3.json'

class ScopedHooks(unittest.TestCase):
    def config(self):
        return {'module':'wargame3.exe','revision':'131544','sha256':'a'*64,'ghidra_base':'0x400000',
                'hooks':[{'name':'root','va':'0x401000','args':0},
                         {'name':'owner','va':'0x401010','args':0,'within':['root'],
                          'reads':[{'source':'retval','phase':'leave','offset':40,'size':128,'indirect':True}]}]}

    def test_scoped_return_capture_config(self):
        controller.validate_config(self.config())

    def test_unknown_or_malformed_scope_is_rejected(self):
        for value in ['root', [], ['missing'], [1]]:
            config = self.config()
            config['hooks'][1]['within'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                controller.validate_config(config)

    def test_masked_indirect_read_is_accepted(self):
        for read in ({'indirect_mask':'FFFFFFFC','indirect_offset':0x30},
                     {'indirect_mask':'0xfffffffc'},
                     {'indirect_offset':0}):
            config = self.config()
            config['hooks'][1]['reads'][0].update(read)
            with self.subTest(read=read):
                controller.validate_config(config)

    def test_mask_and_offset_are_rejected_when_not_indirect(self):
        for key, value in (('indirect_mask','FFFFFFFC'), ('indirect_offset',0x30)):
            config = self.config()
            config['hooks'][1]['reads'][0]['indirect'] = False
            config['hooks'][1]['reads'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                controller.validate_config(config)

    def test_malformed_mask_or_offset_is_rejected(self):
        for key, value in (('indirect_mask', True), ('indirect_mask', 0xFFFFFFFC),
                           ('indirect_mask', 'FFFFFFFZ'), ('indirect_mask', '1FFFFFFFC'),
                           ('indirect_mask', '0x1FFFFFFFC'), ('indirect_mask', ''),
                           ('indirect_offset', True), ('indirect_offset', -1),
                           ('indirect_offset', 0x1001), ('indirect_offset', 16.0),
                           ('indirect_offset', '0x30')):
            config = self.config()
            config['hooks'][1]['reads'][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                controller.validate_config(config)


class PositionCaptureConfig(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(V3_CONFIG.read_text(encoding='utf-8'))

    def test_v3_config_validates_and_is_revision_pinned(self):
        controller.validate_config(self.config)
        self.assertEqual(self.config['revision'], '131544')
        self.assertEqual(len(self.config['hooks']), 10)
        self.assertEqual(self.config['sha256'],
                         '5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d')

    def test_every_hook_entry_is_file_backed_in_the_pinned_pe(self):
        if not PINNED_PE.is_file():
            self.skipTest('pinned PE is unavailable')
        image = PINNED_PE.read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(), self.config['sha256'])
        self.assertIn(b'####SVNREVISION####0000131544####SVNREVISION####', image)
        base = int(self.config['ghidra_base'], 0)
        for hook in self.config['hooks']:
            with self.subTest(hook=hook['name']):
                self.assertEqual(len(controller.pe_bytes_at_rva(image, int(hook['va'], 0) - base, 16)), 16)

    def test_sparse_owner_and_clock_sampling_is_unscoped(self):
        hooks = {hook['name']: hook for hook in self.config['hooks']}
        for name in ('owner_lookup_candidate', 'clock_sample_candidate'):
            self.assertEqual(hooks[name]['sample_every'], 997)
            self.assertNotIn('within', hooks[name])
        self.assertEqual(hooks['owner_lookup_candidate']['reads'][-1]['indirect_offset'], 0x30)

    def test_owner_destroy_position_read_is_enter_only(self):
        hooks = {hook['name']: hook for hook in self.config['hooks']}
        reads = [r for r in hooks['owner_destroy_candidate']['reads']
                 if r['source'] == 'ecx' and r['offset'] == 0xE4]
        self.assertEqual(len(reads), 1)
        self.assertEqual(reads[0]['phase'], 'enter')
        self.assertTrue(reads[0]['indirect'])
        self.assertEqual(reads[0]['size'], 12)

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable for Frida callback simulation')
    def test_scope_is_thread_local_and_filtered_calls_do_not_corrupt_stack(self):
        result = subprocess.run(['node',str(ROOT/'tests/frida_scope_sim.js')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('WGRD_SCOPE_SIM_OK',result.stdout)

class PortableConfigCoverage(unittest.TestCase):
    def test_only_image_bytes_require_the_private_executable(self):
        result = unittest.TestResult()
        with mock.patch.dict(globals(), {'PINNED_PE': ROOT/'__missing_private_engine__.exe'}):
            unittest.defaultTestLoader.loadTestsFromTestCase(PositionCaptureConfig).run(result)
        self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
        allowed = {'test_every_hook_entry_is_file_backed_in_the_pinned_pe'}
        if not shutil.which('node'):
            allowed.add('test_scope_is_thread_local_and_filtered_calls_do_not_corrupt_stack')
        self.assertEqual({test._testMethodName for test, _ in result.skipped}, allowed)


if __name__ == '__main__':
    unittest.main()
