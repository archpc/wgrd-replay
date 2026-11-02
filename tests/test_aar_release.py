"""Release pins for the evidence-bounded revision-131544 AAR.

Re-exports both retained, hash-pinned traces with the maintained exporter and
checks the exact output SHA-256s published in
research/current-build/2026-11-02-aar-release.md. Absent private evidence
skips explicitly; present but altered evidence fails.
"""

import hashlib
import importlib.util
import io
import json
import os
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("aar_events", ROOT / "instrumentation" / "aar_events.py")
aar = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aar)

ARTIFACTS = Path(os.environ.get("WGRD_ARTIFACTS_DIR",
                                Path.home() / ".hermes" / "artifacts" / "wgrd-replay"))
INDEX = ARTIFACTS / "aar-20261102T050816Z" / "units" / "unit-index-131544.json"
TRACES = {
    "runtime": ARTIFACTS / "aar-20261102T050816Z" / "wgrd-aar-combat-20261102-01.jsonl",
    "runtime-v3": ARTIFACTS / "aar-v3-20261102T082918Z" / "native-v3b-replay.jsonl",
}
TRACE_SHA256 = {
    "runtime": "607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74",
    "runtime-v3": "d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec",
}
INDEX_SHA256 = "73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d"
# Measured with python3.14 and python3.15 (identical) from this commit's exporter.
OUTPUT_SHA256 = {
    "runtime": {
        "chronology.md": "a2e401b311ed27201287fb41bac487a7e511fddea628598e5d9b7d6e9e696e0a",
        "events.json": "d8f26e83f725f1b3f19f750ddb22b6efaf269e6f0378c22a780a2c6bf2c0b706",
        "summary.json": "8d3d1e7afb45a3397e38e18d1c3ac53bdf245378c2f316f1b0d8d664b4f357c8",
        "units.json": "ebe43d9e34ca87d0a0f7aef533f3766c8a989fa0d0051756017a7698a4cf0baa",
    },
    "runtime-v3": {
        "chronology.md": "c744d2760834ae594725637d74b70c569057f54f957fe90225bf5e385b805b3e",
        "events.json": "ae3752078b482753b862253a01568cb6a11ae49eb4cdcff01c019129646f58ac",
        "positions.json": "6645cb4b3a7d361968fd19d9a8c8c46adaf2f6b969cf973d19907f896c2c396b",
        "summary.json": "c9b20e8bab79890143b877f080af0a50c71dcead9b22db24bf9e308b7f9bb487",
        "units.json": "ce19f1732b4d06729c1fd0916b738446650972a40b5bf13ee156b409a61a725e",
    },
}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _combat_projection(events):
    """Observation fields that must agree between two captures of one replay."""
    rows = []
    for event in events:
        source = event.get("reported_source") or {}
        destruction = event.get("destruction") or {}
        rows.append((event["ordinal"], event["kind"], event["damage_object"]["handle_u32"],
                     sorted((k, v["before_hex"], v["after_hex"]) for k, v in event["fields"].items()),
                     event["target"]["join"].get("debug_name"), source.get("owner_handle_u32"),
                     (source.get("join") or {}).get("debug_name"), event["check"]["al_u8"],
                     destruction.get("observed"), destruction.get("operand_handle_u32")))
    return rows


class EvidenceBoundedAarRelease(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        missing = [p.name for p in [INDEX, *TRACES.values()] if not p.exists()]
        if missing:
            raise unittest.SkipTest("private AAR evidence unavailable: " + ", ".join(missing))
        if _sha(INDEX) != INDEX_SHA256:
            raise AssertionError("unit index integrity mismatch: %s" % INDEX)
        for profile, path in TRACES.items():
            if _sha(path) != TRACE_SHA256[profile]:
                raise AssertionError("trace integrity mismatch: %s" % path)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = {}
        for profile, path in TRACES.items():
            out = Path(cls.tmp.name) / profile
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = aar.main([str(path), "--profile", profile, "--unit-index", str(INDEX),
                                 "--out", str(out)])
            if code != 0:
                raise AssertionError("export failed for %s" % profile)
            cls.out[profile] = out

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_outputs_match_published_hashes(self):
        for profile, expected in OUTPUT_SHA256.items():
            with self.subTest(profile=profile):
                files = sorted(p.name for p in self.out[profile].iterdir())
                self.assertEqual(files, sorted(expected))
                self.assertEqual({n: _sha(self.out[profile] / n) for n in files}, expected)

    def test_both_traces_agree_on_every_combat_observation(self):
        events = {p: json.loads((o / "events.json").read_text())["events"] for p, o in self.out.items()}
        self.assertEqual(len(events["runtime"]), 28)
        self.assertEqual(_combat_projection(events["runtime"]), _combat_projection(events["runtime-v3"]))

    def test_unobserved_outcomes_stay_unknown(self):
        for profile, out in self.out.items():
            with self.subTest(profile=profile):
                summary = json.loads((out / "summary.json").read_text())
                lifecycle = summary["damage_lifecycle_observations"]
                self.assertEqual([d["impact_ordinal"] for d in lifecycle], [3, 7, 21])
                for item in lifecycle:
                    self.assertFalse(item["killed_token"]["scored_kill_confirmed"])
                    self.assertFalse(item["killed_token"]["combat_message_captured"])
                for key in ("epoch", "frame", "replay_frame", "simulation_time", "game_time", "battle_time"):
                    self.assertIsNone(summary["clock"][key])
                for unit in summary["units"]:
                    self.assertIn("no player, faction or team is assigned", unit["owning_object_ref"]["basis"])
                text = (out / "chronology.md").read_text()
                self.assertNotIn("/Users/", text)
                self.assertEqual(text.count("kill=UNKNOWN"), 28)


if __name__ == "__main__":
    unittest.main()
