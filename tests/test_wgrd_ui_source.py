"""Offline source contracts for the Windows helper; not runtime tests."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "research/current-build/tools/WgrdUi.cs"


class WgrdUiSourceContracts(unittest.TestCase):
    def test_source_rejects_blank_capture_paths_before_input(self):
        source = HELPER.read_text(encoding="utf-8")
        for name in ("Capture", "CaptureRight", "CaptureOnly"):
            self.assertRegex(source, rf"public static string {name}\(.*?"
                             r"String\.IsNullOrWhiteSpace\(file\).*?throw.*?CaptureAction")

    def test_historical_v2_source_matches_experiment_digest(self):
        path = ROOT / "research/current-build/history/WgrdUi-v2.cs"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         "27d754195dc6f7ad701ede32b240e91f8e4fa35a5ff3768b71f5034c58f124df")

    def test_original_capture_entry_points_remain_in_source(self):
        source = HELPER.read_text(encoding="utf-8")
        for name, right in (("Capture", "false"), ("CaptureRight", "true")):
            self.assertRegex(source, rf"public static string {name}\(string file,int x,int y\).*?"
                             rf"CaptureAction\(file,x,y,{right}\)")
        self.assertLess(source.index('if(file==null) return'), source.index('Thread.Sleep(1500)'))
        self.assertLess(source.index('if(file==null) return'), source.index('CopyFromScreen'))

    def test_source_orders_safety_checks_before_mouse_event(self):
        source = HELPER.read_text(encoding="utf-8")
        body = source[source.index('static string CaptureAction('):]
        mouse = body.index('mouse_event(')
        for check in ('File.Exists(file)', 'SetProcessDPIAware()',
                      'Process.GetProcessesByName("WarGame3")', 'ps.Length!=1',
                      'h==IntPtr.Zero', 'GetForegroundWindow()!=h',
                      'x>=screenWidth || y>=screenHeight', '!SetCursorPos(x,y)'):
            self.assertLess(body.index(check), mouse, check)
        self.assertIn('if(x>=0 && y>=0)', body)  # v2 capture-only sentinel
        self.assertIn('right?8u:2u', body)
        self.assertIn('right?16u:4u', body)

    def test_source_checks_click_against_primary_display_bounds(self):
        source = HELPER.read_text(encoding="utf-8")
        self.assertIn('x>=screenWidth || y>=screenHeight', source)
        self.assertIn('screenWidth<=0 || screenHeight<=0', source)

    def test_failed_cursor_placement_is_guarded_in_source(self):
        source = HELPER.read_text(encoding="utf-8")
        self.assertIn('if(!SetCursorPos(x,y)) throw', source)

    def test_capture_uses_exclusive_create_for_evidence(self):
        source = HELPER.read_text(encoding="utf-8")
        self.assertIn("FileMode.CreateNew", source)
        self.assertIn("Refusing overwrite", source)

    def test_capture_only_entry_point_uses_no_click_sentinel(self):
        source = HELPER.read_text(encoding="utf-8")
        self.assertRegex(
            source,
            r"public static string CaptureOnly\(string file\).*?"
            r"CaptureAction\(file,-1,-1,false\)",
        )

    def test_input_only_entry_points_do_not_request_capture(self):
        source = HELPER.read_text(encoding="utf-8")
        for name, right in (("Click", "false"), ("ClickRight", "true")):
            self.assertRegex(
                source,
                rf"public static string {name}\(int x,int y\).*?"
                rf"if\(x<0 \|\| y<0\) throw.*?CaptureAction\(null,x,y,{right}\)",
            )


if __name__ == "__main__":
    unittest.main()
