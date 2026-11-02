"""Falsification checks for AAR hypotheses H1-H3, on hash-pinned private evidence.

H1: one replay frame is one 0.2 s deterministic tick, origin at frame 0.
H2: the battle clock starts at the opcode-0x13 frame.
H3: replay actor 0xC0000066 is the company that owns runtime units 0xC0000067/68.
These tests record agreement with the available evidence; they do not prove
any hypothesis. A new replay with known UI times should extend DISPLAYED.
"""

import hashlib
import json
import math
import os
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import wgrd_replay  # noqa: E402
from wgrd_timeline import build_timeline  # noqa: E402

ARTIFACTS = Path(os.environ.get("WGRD_ARTIFACTS_DIR",
                                Path.home() / ".hermes" / "artifacts" / "wgrd-replay"))
TICK = 0.2
# Displayed UI clocks with their sources (whole seconds; the UI truncates).
DISPLAYED = {
    # combat-20261101/AAR-provisional.md, results screen wgrd-terra-skirmish-21.png
    "combat": {"path": "combat-20261101/replay_2026-11-01_19-10-26.wargamerpl2",
               "sha256": "abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121",
               "battle_seconds": 251, "points": []},
    # archived: research/current-build/2026-10-28-controlled-experiment.md lines 15 and 352
    "controlled": {"path": "current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2",
                   "sha256": "1b060d2ab2e5501c6c8731fcb87ac0c7ac6dc4598387dcdb261ab8bb06bc8d70",
                   "battle_seconds": 144, "replay_total_seconds": 355,
                   "points": [(269, 58)]},  # replay 4:29 shows battle 0:58
}
V3_TRACE = ARTIFACTS / "aar-v3-20261102T082918Z" / "native-v3b-replay.jsonl"
V3_SHA256 = "d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec"


def _load(case):
    path = ARTIFACTS / case["path"]
    if not path.exists():
        raise unittest.SkipTest("private replay unavailable: %s" % path.name)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != case["sha256"]:
        raise AssertionError("private replay integrity mismatch: %s" % path)
    timeline = build_timeline(wgrd_replay.parse_replay(data))
    frames = timeline["stats"]["container"]["frames"]
    op13 = [event["frame"] for event in timeline["events"] if event["opcode"] == 0x13]
    end = [event["frame"] for event in timeline["events"] if event["opcode"] == 0x02]
    return frames, op13, end


class BattleOriginHypothesis(unittest.TestCase):
    def test_op13_to_surrender_matches_displayed_battle_duration(self):
        for name, case in DISPLAYED.items():
            with self.subTest(replay=name):
                frames, op13, end = _load(case)
                self.assertEqual(len(op13), 1)
                self.assertEqual(end, [frames - 1])
                battle = (end[0] - op13[0]) * TICK
                self.assertEqual(math.floor(battle + 1e-9), case["battle_seconds"])

    def test_mid_battle_ui_point_and_replay_total(self):
        case = DISPLAYED["controlled"]
        frames, op13, _ = _load(case)
        self.assertLessEqual(abs(frames * TICK - case["replay_total_seconds"]), 2.0)
        for replay_seconds, battle_seconds in case["points"]:
            # A truncated UI second spans one whole second of possible frames.
            low = (replay_seconds / TICK - op13[0]) * TICK
            high = ((replay_seconds + 1) / TICK - op13[0]) * TICK
            self.assertTrue(low - 1 <= battle_seconds <= high, (low, high))


class TickHypothesis(unittest.TestCase):
    def test_impact_clock_equals_tick_times_engine_counter(self):
        if not V3_TRACE.exists():
            raise unittest.SkipTest("v3 trace unavailable")
        data = V3_TRACE.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), V3_SHA256)
        frames, _, _ = _load(DISPLAYED["combat"])
        samples, registered, impacts = [], [], []
        for line in data.splitlines():
            row = json.loads(line)
            hook, event = row.get("hook"), row.get("event")
            if hook == "clock_sample_candidate" and event == "enter":
                raw = row["reads"][0]["result"]["hex"]
                samples.append((row["ecx"], struct.unpack("<i", bytes.fromhex(raw))[0]))
            elif hook == "frame_apply_candidate" and event == "enter":
                registered.append(int(row["args"][0], 16))
            elif hook == "impact_apply_candidate" and event == "leave":
                block = next(r for r in row["reads"] if r["offset"] == 400)["result"]["hex"]
                time = struct.unpack_from("<f", bytes.fromhex(block), 0x1ec - 400)[0]
                impacts.append((time, samples[-1][1] if samples else None))
        self.assertEqual([key for key in registered if key < 5000], list(range(frames)))
        main = [value for receiver, value in samples if receiver == samples[-1][0]]
        self.assertEqual(main, sorted(main))
        self.assertLess(max(main), frames)
        self.assertEqual(len(impacts), 28)
        for time, last in impacts:
            ticks = time / TICK
            self.assertAlmostEqual(ticks, round(ticks), places=2)
            # The clock never runs ahead of the last sampled counter by more
            # than the sampling gap, and never behind it.
            self.assertGreaterEqual(round(ticks), last)
            self.assertLessEqual(round(ticks) - last, 3)


class ActorGroupHypothesis(unittest.TestCase):
    """H3: replay actor 0xC0000066 is the company owning runtime 0xC0000067/68."""

    INDEX = (ARTIFACTS / "aar-20261102T050816Z" / "units-parent-verified"
             / "unit-index-131544.json")
    INDEX_SHA256 = "73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d"

    def test_actor_guid_is_merkava_company_and_runtime_members_follow_its_key(self):
        if not self.INDEX.exists() or not V3_TRACE.exists():
            raise unittest.SkipTest("unit index or v3 trace unavailable")
        index_bytes = self.INDEX.read_bytes()
        self.assertEqual(hashlib.sha256(index_bytes).hexdigest(), self.INDEX_SHA256)
        index = json.loads(index_bytes)
        case = DISPLAYED["combat"]
        data = (ARTIFACTS / case["path"]).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), case["sha256"])
        timeline = build_timeline(wgrd_replay.parse_replay(data))
        actors = [entry for entry in timeline["entity_references"]["entries"]
                  if entry["occurrences"]["actor"]]
        self.assertEqual([entry["lookup_key_u32"] for entry in actors], [0xC0000066])
        guid = actors[0]["validation_guid_hex"]
        descriptor = index["descriptors"][guid]
        self.assertEqual(descriptor["source_nodes"], ["51786"])
        self.assertEqual(index["nodes"]["51786"]["properties"]["ClassNameForDebug"],
                         "Company_Merkava_IIIB_Baz")
        self.assertEqual([c["unit_type_id"] for c in descriptor["candidates"]], ["19537"])
        # Runtime owner headers: +0x1c key, +0x28 descriptor (V3 owner reads).
        keys_by_descriptor = {}
        for line in V3_TRACE.read_bytes().splitlines():
            row = json.loads(line)
            for read in row.get("reads", []):
                result = read.get("result", {})
                if read["offset"] == 0 and read["size"] == 128 and result.get("ok"):
                    header = bytes.fromhex(result["hex"])
                    if header[:4] == bytes.fromhex("0c449901"):
                        key, = struct.unpack_from("<I", header, 0x1c)
                        desc, = struct.unpack_from("<I", header, 0x28)
                        keys_by_descriptor.setdefault(desc, set()).add(key)
        merkava_keys = [keys for keys in keys_by_descriptor.values()
                        if 0xC0000067 in keys]
        self.assertEqual(merkava_keys, [{0xC0000067, 0xC0000068}])
        self.assertNotIn(0xC0000066, set().union(*keys_by_descriptor.values()))


if __name__ == "__main__":
    unittest.main()
