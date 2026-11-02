"""Source contracts for deterministic WGRD Win32 input; guest compilation is separate."""
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "research/current-build/tools/WgrdUi.cs"


class Win32InputContracts(unittest.TestCase):
    def test_client_input_has_geometry_process_and_focus_guards(self):
        text = SOURCE.read_text()
        self.assertIn("public static string ClickClient(", text)
        self.assertIn("GetClientRect", text)
        self.assertIn("ClientToScreen", text)
        self.assertIn("GetWindowThreadProcessId", text)
        self.assertIn("expectedWidth", text)
        self.assertIn("expectedPid", text)
        self.assertIn("WaitForeground", text)
        self.assertIn("SendInput", text)

    def test_input_only_methods_do_not_capture_or_use_fixed_focus_sleep(self):
        text = SOURCE.read_text()
        self.assertIn("public static string Key(", text)
        start = text.index("public static string WindowState(")
        stop = text.index("public static string Capture(", start)
        block = text[start:stop]
        self.assertNotIn("CopyFromScreen", block)
        self.assertNotIn("Thread.Sleep(600)", block)
        self.assertIn("Stopwatch.StartNew()", block)
        self.assertIn("timeoutMs", block)
        self.assertIn("input_attempted", block)


if __name__ == "__main__":
    unittest.main()
