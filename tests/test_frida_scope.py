"""Scoped hook and return-value capture mechanics, not engine semantics."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scope_controller', ROOT/'instrumentation/wgrd_frida.py')
assert spec is not None and spec.loader is not None
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)

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

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable for Frida callback simulation')
    def test_scope_is_thread_local_and_filtered_calls_do_not_corrupt_stack(self):
        result = subprocess.run(['node',str(ROOT/'tests/frida_scope_sim.js')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('WGRD_SCOPE_SIM_OK',result.stdout)

if __name__ == '__main__':
    unittest.main()
