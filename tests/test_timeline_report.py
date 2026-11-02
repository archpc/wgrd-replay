"""Structural timeline export: full frame/command coverage, integrity checks, pins."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import wgrd_replay as w  # noqa: E402
import wgrd_timeline_report as report  # noqa: E402
from test_timeline import OP09, OPAQUE, op08, replay  # noqa: E402

ARTIFACTS = Path(os.environ.get("WGRD_ARTIFACTS_DIR", Path.home() / ".hermes" / "artifacts" / "wgrd-replay"))
# Revision-131544 replays: (path, replay SHA-256, frames, commands,
# SHA-256 of timeline.json without "generator", SHA-256 of timeline.md).
AUTHENTIC = {
    "controlled": ("current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2",
                   "1b060d2ab2e5501c6c8731fcb87ac0c7ac6dc4598387dcdb261ab8bb06bc8d70", 1784, 12,
                   "1b65da0916ea45e5a5baebd30785fd7fa6cde0ff049e3fe28d3bb2d67b34ea54",
                   "d71abb0fc7f749f5e81c112ebeeb627da8d8ef32982808f29bb5da6fe50fb80a"),
    "combat": ("combat-20261101/replay_2026-11-01_19-10-26.wargamerpl2",
               "abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121", 4174, 14,
               "193641eeaa73a2a77dd8a2014cff97604117affc638d88cd075c91f98183ac72",
               "70e4f84a1839c86aa725b684141b02d456b7e4173011b6fb635ae3ef3521d391"),
}


def content_sha(result):
    stripped = dict(result)
    stripped.pop("generator")
    return hashlib.sha256(json.dumps(stripped, sort_keys=True).encode()).hexdigest()


class StructuralTimeline(unittest.TestCase):
    def setUp(self):
        # Two slots per frame. Frame 0 repeats one command; frame 1 is empty; frame 2 is opaque.
        self.data = replay([[(2, OP09 + OP09), (1, op08())], [(0, b""), (0, b"")], [(1, OPAQUE), (0, b"")]])
        self.result = report.build_report(self.data)

    def test_every_frame_pact_and_command_is_preserved(self):
        r = self.result
        self.assertEqual([f["frame"] for f in r["frames"]], [0, 1, 2])
        self.assertEqual([len(f["pacts"]) for f in r["frames"]], [2, 2, 2])
        self.assertEqual([f["command_orders"] for f in r["frames"]], [[0, 1, 2], [], [3]])
        self.assertEqual(r["integrity"]["declared_commands"], 4)
        self.assertEqual(r["integrity"]["silently_discarded_commands"], 0)
        for f in r["frames"]:
            self.assertEqual(self.data[f["star_offset"]:f["star_offset"] + 4], b"star")
            self.assertEqual(self.data[f["endt_offset"]:f["endt_offset"] + 4], b"endt")
        for e in r["events"]:
            s = e["source"]
            self.assertEqual(bytes.fromhex(e["raw_hex"]), self.data[s["file_offset"]:s["file_offset"] + s["length"]])

    def test_duplicates_flagged_not_merged_and_unknowns_flagged(self):
        r = self.result
        self.assertEqual(r["integrity"]["identical_raw_commands_in_same_frame_and_slot"],
                         [{"command_order": 1, "duplicate_of": 0, "frame": 0, "player_slot": 0}])
        self.assertEqual(len(r["events"]), 4)
        opaque = r["events"][3]
        self.assertIn("payload_opaque", opaque["undecoded"])

    def test_time_domains_never_invent_values(self):
        r = self.result
        for e in r["events"]:
            self.assertEqual(e["time"], {"frame_index": e["frame"],
                                         "t_from_replay_load_seconds": round(e["frame"] * 0.2, 3),
                                         "t_basis": "derived_from_static_tick_quantum",
                                         "estimated_deterministic_time_seconds":
                                             round((e["frame"] - 10.5) * 0.2, 3),
                                         "estimated_deterministic_time_bounds_seconds": [
                                             round((e["frame"] - 11) * 0.2, 3),
                                             round((e["frame"] - 10) * 0.2, 3)],
                                         "estimated_time_basis": "single_capture_statistic",
                                         "deterministic_ticks": None, "game_time": None,
                                         "wall_clock": None})
            self.assertIsNone(e["player_identity"])
        self.assertIsNone(r["clock_mapping"]["frame_to_deterministic_tick"])
        self.assertIsNone(r["time_domains"]["deterministic_ticks"])
        self.assertEqual(r["aar_integration"]["status"], "not_integrated")
        self.assertIsNone(r["teams"]["slot_to_player"])
        self.assertEqual(r["coverage"]["timing"],
                         {"frame_index": 4, "derived_seconds": 4, "estimated_deterministic_time": 4,
                          "deterministic_ticks": 0, "game_time": 0, "battle_time": 0,
                          "wall_clock": 0})

    def test_tick_quantum_is_static_and_labelled(self):
        r = self.result
        self.assertEqual(r["schema"], "wgrd_structural_timeline/2")
        clock = r["clock_mapping"]
        self.assertEqual(clock["frame_seconds"], 0.2)
        self.assertEqual(clock["frame_seconds_basis"], "static_engine_tick_quantum_and_observed_5hz")
        self.assertEqual(clock["status"],
                         "clock_rate_observed_frame_tick_difference_unresolved_battle_start_unknown")
        self.assertIn("replay_load", clock["frame_origin"])
        self.assertTrue(any("0xb34060" in line for line in clock["verified"]))
        self.assertTrue(any("0xb349bd" in line for line in clock["verified"]))
        # Integer observations stay distinct from the statistical midpoint.
        self.assertEqual(clock["frame_tick_difference_observed"], [10, 11])
        self.assertEqual(clock["frame_tick_difference_samples"], {"10": 48, "11": 47})
        self.assertEqual(clock["frame_tick_difference_estimate_frames"], 10.5)
        self.assertEqual(clock["frame_tick_difference_status"],
                         "integer_10_or_11_observed_boundary_unresolved")
        self.assertIsNone(clock["verified_battle_time"])
        self.assertTrue(any("4.995 frames/s" in line for line in clock["verified"]))
        self.assertTrue(any("13:53" in line for line in clock["verified"]))
        self.assertTrue(any("not identity" in line for line in clock["verified"]))
        boundary = [u for u in clock["unknowns"]
                    if u["field"].startswith("exact frame/tick")]
        self.assertEqual(len(boundary), 1)
        self.assertEqual(boundary[0]["status"], "unresolved")
        # Battle start stays an explicit unknown with its experiment.
        phase = [u for u in clock["unknowns"] if u["field"].startswith("battle start")]
        self.assertEqual(len(phase), 1)
        self.assertIn("0xab4780", phase[0]["detail"])
        self.assertIn("0x6d17e0", phase[0]["smallest_experiment"])
        h4 = [h for h in clock["hypotheses"] if h["id"] == "H4"][0]
        self.assertEqual(h4["status"], "corrected_by_measured_offset")
        self.assertIn("4164..4165", h4["detail"])
        # Derived seconds must never present as observed engine time.
        for e in r["events"]:
            self.assertIsNone(e["time"]["deterministic_ticks"])
            self.assertIsNone(e["time"]["game_time"])
            self.assertEqual(e["time"]["estimated_time_basis"], "single_capture_statistic")
            low, high = e["time"]["estimated_deterministic_time_bounds_seconds"]
            self.assertLess(low, high)
            self.assertLessEqual(low, e["time"]["estimated_deterministic_time_seconds"])
            self.assertLessEqual(e["time"]["estimated_deterministic_time_seconds"], high)

    def test_execution_model_separates_load_from_tick(self):
        r = self.result
        model = r["execution_model"]
        self.assertEqual(model["status"], "static_dispatch_path_with_unproven_outcomes")
        self.assertIn("0xb3dbc0", model["bulk_load"]["reader"])
        self.assertIn("0xb2b310", model["bulk_load"]["store"])
        self.assertEqual(model["per_tick"]["quantum_seconds"], 0.2)
        self.assertIn("0xb34060", model["per_tick"]["step"])
        self.assertIn("0xb35650", model["per_tick"]["missing_frame_padding"])
        self.assertEqual(model["order_apply"]["class"], "TNetworkActionGiveOrderStandard")
        self.assertIn("0xb2be30", model["order_apply"]["method"])
        self.assertIn("intra-tick ordering across slots", model["not_claimed"])
        self.assertIn("## Execution model", report.render_markdown(r))
        self.assertIn("t+ (s)", report.render_markdown(r))

    def test_checks_fail_closed_on_dropped_reordered_or_altered_events(self):
        frames = report._frame_table(self.data)
        events = [dict(e) for e in report.build_timeline(w.parse_replay(self.data))["events"]]
        cases = {"declares 2 commands, 1 exported": events[1:],
                 "ordering violation": [events[1], events[0]] + events[2:],
                 "covered exactly once": [dict(events[0], raw_hex="00")] + events[1:]}
        for message, tampered in cases.items():
            with self.subTest(message=message), self.assertRaisesRegex(w.ReplayFormatError, message):
                report._checks(frames, tampered, self.data)

    def test_outputs_are_deterministic_and_exclusive(self):
        with tempfile.TemporaryDirectory() as d:
            first = report.write_outputs(report.build_report(self.data), Path(d) / "a")
            second = report.write_outputs(report.build_report(self.data), Path(d) / "b")
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
            with self.assertRaises(FileExistsError):
                report.write_outputs(self.result, Path(d) / "a")
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                source = Path(d) / "in.wargamerpl2"
                source.write_bytes(self.data)
                self.assertEqual(report.main([str(source), "--out", str(Path(d) / "a")]), 2)
                self.assertEqual(report.main([str(source), "--out", str(Path(d) / "c")]), 0)
            json.loads((Path(d) / "c" / "timeline.json").read_text())

    def test_generator_pins_actual_source_hashes(self):
        for name, sha in self.result["generator"]["sources"].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), sha)


class AuthenticRevision131544(unittest.TestCase):
    def test_full_coverage_and_pinned_outputs(self):
        for name, (path, sha, frames, commands, json_sha, md_sha) in AUTHENTIC.items():
            with self.subTest(replay=name):
                source = ARTIFACTS / path
                if not source.exists():
                    self.skipTest("private replay unavailable: " + source.name)
                data = source.read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), sha)
                r = report.build_report(data)
                self.assertEqual(r["replay"]["game_version"], "131544")
                self.assertEqual(r["coverage"]["frames"], frames)
                self.assertEqual(r["coverage"]["pacts"], frames)
                self.assertEqual(r["coverage"]["commands"], commands)
                self.assertEqual(r["integrity"]["silently_discarded_commands"], 0)
                self.assertEqual(r["coverage"]["unresolved_spans"], 0)
                # Independent count of declared commands straight from pact headers.
                header, _ = w.parse_header(data)
                declared = sum(struct.unpack_from("<IIIH", p)[2]
                               for _, tag, p in w.iter_chunks(data, header["payload_offset"]) if tag == b"pact")
                self.assertEqual(declared, commands)
                self.assertEqual(content_sha(r), json_sha)
                self.assertEqual(hashlib.sha256(report.render_markdown(r).encode()).hexdigest(), md_sha)
                self.assertEqual(r["coverage"]["timing"]["deterministic_ticks"], 0)


if __name__ == "__main__":
    unittest.main()
