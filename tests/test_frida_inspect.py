import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    "trace_inspect", Path(__file__).resolve().parents[1] / "instrumentation" / "trace_inspect.py"
)
trace_inspect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace_inspect)


class TraceInspectionTests(unittest.TestCase):
    def test_one_parent_can_have_multiple_nested_calls(self):
        events = [
            {"event": "enter", "hook": "request", "call_id": 1, "thread_id": 3, "parent_call_id": None},
            {"event": "enter", "hook": "dispatch", "call_id": 2, "thread_id": 3, "parent_call_id": 1, "parent_recorded": True},
            {"event": "leave", "hook": "dispatch", "call_id": 2, "thread_id": 3, "stack_match": True},
            {"event": "enter", "hook": "dispatch", "call_id": 3, "thread_id": 3, "parent_call_id": 1, "parent_recorded": True},
            {"event": "leave", "hook": "dispatch", "call_id": 3, "thread_id": 3, "stack_match": True},
            {"event": "leave", "hook": "request", "call_id": 1, "thread_id": 3, "stack_match": True},
            {"event": "summary", "suppressed": 0, "callback_errors": 0, "stack_mismatches": 0},
            {"event": "end", "cleanup_errors": 0},
        ]
        result = trace_inspect.summarize(events)
        self.assertEqual(result["relations"], [{"parent": 1, "child": 2}, {"parent": 1, "child": 3}])
        self.assertEqual(result["issues"], [])

    def test_reports_missing_events_and_unrecorded_parent(self):
        events = [
            {"event": "enter", "hook": "dispatch", "call_id": 8, "thread_id": 2,
             "parent_call_id": 7, "parent_recorded": False},
            {"event": "summary", "suppressed": 1, "callback_errors": 0, "stack_mismatches": 0},
            {"event": "end", "cleanup_errors": 0},
        ]
        result = trace_inspect.summarize(events)
        self.assertEqual(result["relations"], [])
        self.assertIn("unrecorded_parent", result["issues"])
        self.assertIn("unmatched_enter", result["issues"])
        self.assertIn("events_suppressed", result["issues"])

    def test_rejects_non_top_parent_on_same_thread(self):
        events = [
            {"event": "enter", "hook": "a", "call_id": 1, "thread_id": 1, "parent_call_id": None},
            {"event": "enter", "hook": "b", "call_id": 2, "thread_id": 1, "parent_call_id": 1, "parent_recorded": True},
            {"event": "enter", "hook": "c", "call_id": 3, "thread_id": 1, "parent_call_id": 1, "parent_recorded": True},
            {"event": "summary", "suppressed": 0, "callback_errors": 0, "stack_mismatches": 0},
            {"event": "end", "cleanup_errors": 0},
        ]
        result = trace_inspect.summarize(events)
        self.assertEqual(result["relations"], [{"parent": 1, "child": 2}])
        self.assertIn("invalid_parent", result["issues"])

    def test_rejects_cross_thread_parent_correlation(self):
        events = [
            {"event": "enter", "hook": "a", "call_id": 1, "thread_id": 1, "parent_call_id": None},
            {"event": "enter", "hook": "b", "call_id": 2, "thread_id": 2, "parent_call_id": 1, "parent_recorded": True},
            {"event": "summary", "suppressed": 0, "callback_errors": 0, "stack_mismatches": 0},
            {"event": "end", "cleanup_errors": 0},
        ]
        result = trace_inspect.summarize(events)
        self.assertEqual(result["relations"], [])
        self.assertIn("invalid_parent", result["issues"])


class JavaScriptSimulationTests(unittest.TestCase):
    def test_hook_callbacks_with_simulated_frida_api(self):
        import shutil
        import subprocess
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js unavailable for JavaScript callback simulation")
        script = Path(__file__).with_name("frida_hooks_sim.js")
        result = subprocess.run([node, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WGRD_JS_SIMULATION_OK", result.stdout)


class ReplayMatchingTests(unittest.TestCase):
    def data(self):
        actor, structure = "ab" * 20, "cd" * 36
        timeline = {"sha256": "a" * 64, "header": {"game_version": "131544", "digest_valid": True}, "events": [
            {"opcode": 7, "frame": 100, "player_slot": 0, "source": {"file_offset": 1234},
             "parameters": {"obj_04_array": {"count_u32": 1, "items_hex": actor}, "obj_d0_hex": structure}}
        ]}
        events = [{"event": "start", "revision": "131544",
                   "sha256": "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"},
                  {"event": "identity_verified", "module": {"name": "wargame3.exe"}},
                  {"event": "enter", "hook": "order_request_wrapper", "call_id": 5,
                   "reads": [{"source": "ecx", "offset": 4, "result": {"ok": True, "hex": actor + "00" * 12}},
                             {"source": "ecx", "offset": 208, "result": {"ok": True, "hex": structure}}]}]
        return events, timeline

    def test_exact_match_reports_locator_without_execution_claim(self):
        events, timeline = self.data()
        result = trace_inspect.match_order_requests(events, timeline)
        self.assertEqual(result[0]["call_id"], 5)
        self.assertEqual(result[0]["candidates"], [{"frame": 100, "slot": 0, "file_offset": 1234}])

    def test_multi_actor_request_matches_all_reference_bytes(self):
        events, timeline = self.data()
        actors = "ab" * 20 + "ef" * 20
        timeline["events"][0]["parameters"]["obj_04_array"] = {"count_u32": 2, "items_hex": actors}
        events[2]["reads"][0]["result"]["hex"] = actors + "00" * 40
        self.assertEqual(trace_inspect.match_order_requests(events, timeline)[0]["candidates"],
                         [{"frame": 100, "slot": 0, "file_offset": 1234}])

    def test_repeated_replay_matches_remain_ambiguous(self):
        events, timeline = self.data()
        duplicate = dict(timeline["events"][0])
        duplicate["frame"] = 200
        timeline["events"].append(duplicate)
        self.assertEqual(len(trace_inspect.match_order_requests(events, timeline)[0]["candidates"]), 2)

    def test_cli_matches_available_authenticated_recording(self):
        import json
        import subprocess
        import sys
        root = Path.home() / ".hermes/artifacts/wgrd-replay"
        replay = root / "current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2"
        trace = root / "frida-traces/replay-01.private.jsonl"
        if not replay.exists() or not trace.exists():
            self.skipTest("private controlled replay or trace unavailable")
        result = subprocess.run([sys.executable, str(Path(trace_inspect.__file__)), str(trace),
                                 "--replay", str(replay)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["request_candidates"][0]["candidates"],
                         [{"frame": 1352, "slot": 0, "file_offset": 112616}])

    def test_failed_read_and_other_revision_do_not_match(self):
        events, timeline = self.data()
        events[2]["reads"][0]["result"]["ok"] = False
        self.assertEqual(trace_inspect.match_order_requests(events, timeline)[0]["candidates"], [])
        timeline["header"]["game_version"] = "59638"
        with self.assertRaises(ValueError):
            trace_inspect.match_order_requests(events, timeline)


if __name__ == "__main__":
    unittest.main()
