"""Hash-pinned external replays: one current recording and two historical sources.

No replay bytes in Git. WGRD_ARTIFACTS_DIR overrides the local artifact root.
Missing external files skip explicitly; altered files fail.
"""
import hashlib
import json
import os
from pathlib import Path
import unittest

from wgrd_corpus import inventory
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "samples/cross-build-manifest.json").read_text())
ARTIFACTS = Path(os.environ.get("WGRD_ARTIFACTS_DIR", "~/.hermes/artifacts/wgrd-replay")).expanduser()


class CrossBuildCorpus(unittest.TestCase):
    def check_sample(self, sample_id):
        expected = next(s for s in MANIFEST["samples"] if s["id"] == sample_id)
        path = ARTIFACTS / expected["artifact_path"]
        if not path.is_file():
            self.skipTest("external replay missing; set WGRD_ARTIFACTS_DIR: " + str(path))
        data = path.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), expected["sha256"])
        self.assertEqual(len(data), expected["size"])
        row = inventory([path])["replays"][0]
        for key in ("game_version", "map", "game_mode_raw", "frames", "slots_per_frame",
                    "declared_commands", "decoded_opcodes", "block_statuses"):
            self.assertEqual(row[key], expected[key], key)
        self.assertEqual(row["compatibility"], "structurally_compatible")
        self.assertEqual(row["errors"], [])
        self.assertEqual(row["decode_failures"], [])
        self.assertEqual(row["unknown_chunks"], [])
        self.assertTrue(row["digest_valid"])
        self.assertEqual(row["timeline"]["events"], expected["declared_commands"])
        self.assertEqual(row["timeline"]["unresolved_spans"], 0)
        self.assertEqual(row["layout_evidence"], "inferred_from_59638")
        self.assertIsNone(row["duration_seconds"])
        self.assertIsNone(row["slot_to_player_identity"])
        return parse_replay(data)

    def test_current_131544_recording_and_observed_fuel_pair(self):
        parsed = self.check_sample("controlled-131544")
        timeline = build_timeline(parsed)
        toggles = [e for e in timeline["events"] if e["opcode"] == 0x18]
        self.assertEqual([(e["frame"], e["parameters"]["obj_04_u32"],
                           e["parameters"]["obj_08_u32"], e["parameters"]["obj_0c_u8"])
                          for e in toggles], [(1638, 3221225609, 2, 0), (1771, 3221225609, 2, 1)])
        # Recording observations are sample-specific; the general decoder must
        # not promote all non-59638 actions or assert execution success.
        for event in timeline["events"]:
            self.assertIn(event["interpretation"]["status"], ("inferred", "unknown"))
            self.assertEqual(event["interpretation"].get("execution_outcome", "unknown"), "unknown")
        self.assertEqual(parsed["metadata"]["game"]["IsNetworkMode"], "0")

    def test_historical_archive_218(self):
        self.check_sample("getuploader-218")

    def test_historical_archive_219(self):
        self.check_sample("getuploader-219")


if __name__ == "__main__":
    unittest.main()
