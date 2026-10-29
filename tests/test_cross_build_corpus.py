"""Hash-pinned external replays: one current recording and two historical sources.

No replay bytes in Git. WGRD_ARTIFACTS_DIR overrides the local artifact root (default
~/.hermes/artifacts/wgrd-replay). Expected values come from samples/cross-build-manifest.json
(the sample's "id" is the lookup key). Per-sample behaviour:
  * file missing      -> skipTest (reported as SKIPPED, never as a pass);
  * file present, SHA-256 or size differs -> test FAILS (altered evidence, not a skip);
  * otherwise selected manifest fields must match and the timeline must have one event per
    declared command with zero unresolved spans.
Build labels: the 131544 recording and the two historical archives are all
"inferred_from_59638" for layout purposes; none is verified against build 59638.
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
        """Verify one manifest sample and return its parsed structure for further assertions.

        The missing-file skip happens before any hash check, so a run with no artifacts reports
        every test here as skipped. Counts are the decoder's output compared with the values
        recorded in the manifest, so a decoder regression fails the test.
        """
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
        """Sample-specific recording observation, not a general 0x18 semantic.

        Two 0x18 events corroborate the observed Oshkosh Fuel OFF then ON toggles in this
        recording, not a general causal mapping. Tuple fields are RAW: obj_04_u32 is 3221225609 (0xC0000089,
        an opaque registry key), obj_08_u32 is raw value 2, and obj_0c_u8 carries the final-byte
        values 0 then 1. These raw supply fields are not generally confirmed meanings.
        Only 0x13 gains partial interpretation from the revision-131544 consumer;
        other top-level statuses stay inferred/unknown and every outcome stays unknown.
        """
        parsed = self.check_sample("controlled-131544")
        timeline = build_timeline(parsed)
        toggles = [e for e in timeline["events"] if e["opcode"] == 0x18]
        self.assertEqual([(e["frame"], e["parameters"]["obj_04_u32"],
                           e["parameters"]["obj_08_u32"], e["parameters"]["obj_0c_u8"])
                          for e in toggles], [(1638, 3221225609, 2, 0), (1771, 3221225609, 2, 1)])
        # ASCII WARNING: promotion needs matching executable evidence. Only the
        # newly traced 0x13 consumer qualifies here; other interpretations retain their status.
        #   ,---.
        #   |o_o|  promoted to "verified"? -> this test must fail
        #   |_^_|
        for event in timeline["events"]:
            if event['opcode'] == 0x13:
                self.assertEqual(event['interpretation']['status'], 'partial')
                self.assertEqual(event['interpretation']['evidence_build'], '131544')
                self.assertEqual(event['interpretation']['parameters']['membership_operation'], 'add_member')
            else:
                self.assertIn(event["interpretation"]["status"], ("inferred", "unknown"))
            self.assertEqual(event["interpretation"].get("execution_outcome", "unknown"), "unknown")
        self.assertEqual(parsed["metadata"]["game"]["IsNetworkMode"], "0")

    def test_historical_archive_218(self):
        """Historical 510061340: structural fit, not a verified build-specific layout."""
        self.check_sample("getuploader-218")

    def test_historical_archive_219(self):
        """Historical 510064564: structural fit, not a verified build-specific layout."""
        self.check_sample("getuploader-219")


if __name__ == "__main__":
    unittest.main()
