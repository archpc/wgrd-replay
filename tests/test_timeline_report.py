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
                   "ae9cfd110b49fedb350f6f9bf88f850fc3cc58cbe72ef0c48319f39bbcc56b55",
                   "e94a84cfa482803b78468deacc812342eee359e65c03754add67c819faa60a71"),
    "combat": ("combat-20261101/replay_2026-11-01_19-10-26.wargamerpl2",
               "abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121", 4174, 14,
               "b0f8998f8234003ae7f955e7148874dee22391f2625837b648226630e54c3b17",
               "f6443f72183517123c7c56d8e53db1b3714050b4d12067d7943ca0482b4b00ca"),
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
            self.assertEqual(e["time"], {"frame_index": e["frame"], "deterministic_ticks": None,
                                         "game_time": None, "wall_clock": None})
            self.assertIsNone(e["player_identity"])
        self.assertIsNone(r["clock_mapping"]["frame_to_deterministic_tick"])
        self.assertIsNone(r["clock_mapping"]["frame_duration_seconds"])
        self.assertEqual(r["aar_integration"]["status"], "not_integrated")
        self.assertIsNone(r["teams"]["slot_to_player"])
        self.assertEqual(r["coverage"]["timing"],
                         {"frame_index": 4, "deterministic_ticks": 0, "game_time": 0, "wall_clock": 0})

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
