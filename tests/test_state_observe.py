"""Counter mechanics only, not engine time validation."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("state_observe", Path(__file__).resolve().parents[1] / "instrumentation/state_observe.py")
assert spec is not None and spec.loader is not None
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)

class CounterObservation(unittest.TestCase):
    def test_advancing_counter_reports_raw_rate_without_time_semantics(self):
        out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"},
                               {"counter": 20, "monotonic_ns": 1000000000, "container": "0x1"}])
        self.assertEqual(out["counter_delta"], 10)
        self.assertEqual(out["counter_per_wall_second"], 10)
        self.assertEqual(out["observation"], "advancing_counter")
        self.assertFalse(out["simulation_time_validated"])

    def test_stable_counter_is_not_called_paused(self):
        out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"},
                               {"counter": 10, "monotonic_ns": 1000000000, "container": "0x1"}])
        self.assertEqual(out["observation"], "stable_counter")
        self.assertIsNone(out["ui_state"])

    def test_game_ended_flag_is_independent_of_stationary_counter(self):
        samples = [{"counter": 4165, "monotonic_ns": 0, "container": "0x1", "container_prefix_hex": (bytes(0x22) + b"\x01" + bytes(221)).hex()},
                   {"counter": 4165, "monotonic_ns": 1000000000, "container": "0x1", "container_prefix_hex": (bytes(0x22) + b"\x01" + bytes(221)).hex()}]
        self.assertTrue(state.summarize(samples)["engine_game_ended"])
        samples[-1]["container_prefix_hex"] = bytes(256).hex()
        self.assertFalse(state.summarize(samples)["engine_game_ended"])

    def test_reset_or_container_change_is_discontinuity(self):
        for end in [{"counter": 1, "monotonic_ns": 1, "container": "0x1"},
                    {"counter": 11, "monotonic_ns": 1, "container": "0x2"}]:
            out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"}, end])
            self.assertEqual(out["observation"], "discontinuity")

if __name__ == "__main__":
    unittest.main()
