"""Opcode 0x0C ChangeProduction: structural decoder tests (wgrd_replay._decode_command).

Layout from creator FUN_00b2eeb0 (build 59638); see research/CHANGEPRODUCTION-0C.md.
Field meanings are unconfirmed, so tests pin raw values only. Sample2 is a different
build (510117427): its 0x0C blocks are checked structurally and labelled inferred.
Corpus tests skip when samples are absent (WGRD_SAMPLES_DIR, default
~/.hermes/artifacts/wgrd-replay/samples/raw). Same pattern as tests/test_op0c_layout.py.
"""
import importlib.util
import json
import os
import struct
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import wgrd_replay as w  # noqa: E402

_spec = importlib.util.spec_from_file_location("op0c_layout", ROOT / "research" / "op0c_layout.py")
op0c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(op0c)

SAMPLES = Path(os.environ.get("WGRD_SAMPLES_DIR",
                              str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))


def u(*values):
    return struct.pack("<" + "I" * len(values), *values)


def block(a=1, b=bytes(16), arr18=(), arr34=(), pts50=(), pts9c=(), arrE8=(), c=0, d=bytes(16)):
    pts = lambda ps: u(len(ps)) + b"".join(struct.pack("<3fI", *p) for p in ps)
    return (bytes([0x0C]) + u(a) + b + u(len(arr18), *arr18) + u(len(arr34), *arr34)
            + pts(pts50) + pts(pts9c) + u(len(arrE8), *arrE8) + u(c) + d)


def fl(v):
    """Undo the strict-JSON non-finite marker used for float32 point components."""
    if isinstance(v, dict):
        return {"+Infinity": float("inf"), "-Infinity": float("-inf"), "NaN": float("nan")}[v["nonfinite"]]
    return v


def decode1(blk, slot=0):
    return w.decode_command_block(blk, 1, slot)


class DecoderLayout(unittest.TestCase):
    def test_minimal_61_byte_block_exact_consumption(self):
        blk = block(a=0xC000001E, c=7)
        self.assertEqual(len(blk), 61)
        r = decode1(blk)
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["consumed_bytes"], 61)
        self.assertEqual(r["remaining_hex"], "")
        cmd = r["commands"][0]
        self.assertEqual((cmd["opcode"], cmd["class"], cmd["length"]), (0x0C, "TNetworkActionChangeProduction", 61))
        self.assertEqual(cmd["field_decode_status"], "layout")
        f = cmd["fields"]
        self.assertEqual(f["obj_04_u32"], 0xC000001E)
        self.assertEqual(f["obj_08_hex"], "00" * 16)
        self.assertEqual(f["obj_18_array"], {"count_u32": 0, "items_hex": "", "items_u32": []})
        self.assertEqual(f["obj_34_array"]["count_u32"], 0)
        self.assertEqual(f["obj_50_points"], {"count_u32": 0, "items_hex": "", "items": []})
        self.assertEqual(f["obj_9c_points"]["count_u32"], 0)
        self.assertEqual(f["obj_e8_array"]["count_u32"], 0)
        self.assertEqual(f["obj_104_u32"], 7)
        self.assertEqual(f["obj_108_hex"], "00" * 16)
        self.assertEqual(cmd["raw_hex"], blk.hex())

    def test_variable_length_arrays_consume_exactly(self):
        pts50 = [(1.0, 2.0, 3.0, 2), (4.5, -5.5, 6.25, 0)]
        pts9c = [(float("inf"), float("inf"), float("inf"), 0), (7.0, 8.0, 9.0, 6), (0.5, 0.25, 0.125, 1)]
        blk = block(a=5, b=bytes(range(16)), arr18=(1, 2, 3), arr34=(3, 8, 14),
                    pts50=pts50, pts9c=pts9c, arrE8=(0x4030DD88, 0xBF3E831A), c=0x11, d=bytes(range(16, 32)))
        r = decode1(blk)
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["consumed_bytes"], len(blk))
        f = r["commands"][0]["fields"]
        self.assertEqual(f["obj_18_array"]["items_u32"], [1, 2, 3])
        self.assertEqual(f["obj_18_array"]["count_u32"], 3)
        self.assertEqual(f["obj_34_array"]["items_u32"], [3, 8, 14])
        self.assertEqual(f["obj_50_points"]["count_u32"], 2)
        self.assertEqual([p["kind_u32"] for p in f["obj_50_points"]["items"]], [2, 0])
        self.assertEqual(f["obj_50_points"]["items"][1]["xyz_f32"], [4.5, -5.5, 6.25])
        self.assertEqual(len(f["obj_9c_points"]["items"]), 3)
        self.assertEqual(f["obj_9c_points"]["items"][0]["xyz_f32"], [{"nonfinite": "+Infinity"}] * 3)
        self.assertEqual(f["obj_9c_points"]["items"][2]["xyz_f32"], [0.5, 0.25, 0.125])
        self.assertEqual(f["obj_9c_points"]["items"][1]["kind_u32"], 6)
        self.assertEqual(len(f["obj_9c_points"]["items_hex"]), 3 * 16 * 2)
        self.assertEqual(f["obj_e8_array"]["items_u32"], [0x4030DD88, 0xBF3E831A])
        self.assertEqual(f["obj_104_u32"], 0x11)
        self.assertEqual(f["obj_108_hex"], bytes(range(16, 32)).hex())
        self.assertEqual(r["commands"][0]["raw_hex"], blk.hex())
        json.dumps(r, allow_nan=False)  # strict JSON: no bare NaN/Infinity tokens

    def test_obj34_element_above_14_rejected(self):
        self.assertEqual(decode1(block(arr34=(14,)))["status"], "complete")
        r = decode1(block(arr34=(0x0F,)))
        self.assertEqual(r["status"], "malformed")
        self.assertIn("0c obj+0x34", r["reason"])
        with self.assertRaises(w.ReplayFormatError):
            w._decode_command(w._CommandCursor(block(arr34=(15,))), 0)

    def test_point_kind_above_6_rejected_in_either_array(self):
        for kw in ("pts50", "pts9c"):
            self.assertEqual(decode1(block(**{kw: [(0., 0., 0., 6)]}))["status"], "complete")
            r = decode1(block(**{kw: [(0., 0., 0., 7)]}))
            self.assertEqual(r["status"], "malformed", kw)
            self.assertIn("kind 7", r["reason"])

    def test_truncated_block_malformed(self):
        blk = block(pts50=[(1., 2., 3., 2)])
        r = decode1(blk[:-1])
        self.assertEqual(r["status"], "malformed")
        self.assertEqual(r["consumed_bytes"], 0)
        self.assertEqual(decode1(blk[:60])["status"], "malformed")

    def test_trailing_bytes_after_count_one_block_malformed(self):
        r = decode1(block(c=3) + b"\x00")
        self.assertEqual(r["status"], "malformed")
        self.assertEqual(r["reason"], "trailing bytes after declared command count")
        self.assertEqual(r["consumed_bytes"], 61)

    def test_huge_count_does_not_scan_past_block(self):
        bad = bytes([0x0C]) + u(1) + bytes(16) + u(0xFFFFFFFF)
        r = decode1(bad)
        self.assertEqual(r["status"], "malformed")


def _corpus_records(path):
    for rec in w.parse_replay(path.read_bytes())["commands"]:
        if rec["count"] == 1 and rec["block_hex"][:2] == "0c":
            yield rec


class CorpusDecode(unittest.TestCase):
    EXPECTED_SINGLE = {"koppeltar-Sample1.wargamerpl2": 13,
                       "koppeltar-Sample3.wargamerpl2": 28,
                       "koppeltar-Sample2.wargamerpl2": 6}  # Sample2: different build, inferred

    def setUp(self):
        manifest = json.loads((ROOT / "samples" / "manifest.json").read_text())["samples"]
        self.paths = {s["file"]: SAMPLES / s["file"] for s in manifest}
        if not all(p.exists() for p in self.paths.values()):
            self.skipTest("authentic samples not cached; set WGRD_SAMPLES_DIR")

    def test_every_single_0c_block_is_complete(self):
        for name, expected in self.EXPECTED_SINGLE.items():
            recs = list(_corpus_records(self.paths[name]))
            self.assertEqual(len(recs), expected, name)
            for rec in recs:
                dec = rec["command_decode"]
                self.assertEqual(dec["status"], "complete", (name, rec["frame"], rec["slot"], dec.get("reason")))
                self.assertEqual(dec["consumed_bytes"], rec["block_length"])
                self.assertEqual(dec["commands"][0]["field_decode_status"], "layout")

    def test_sample1_golden_fields(self):
        recs = list(_corpus_records(self.paths["koppeltar-Sample1.wargamerpl2"]))
        self.assertEqual(len(recs), 13)
        for rec in recs:
            f = rec["command_decode"]["commands"][0]["fields"]
            self.assertEqual(f["obj_04_u32"], 0xC000001E + rec["slot"], (rec["frame"], rec["slot"]))
            self.assertEqual(f["obj_08_hex"], "00" * 12 + "32000000")

    def test_sample1_agrees_with_standalone_parser(self):
        path = self.paths["koppeltar-Sample1.wargamerpl2"]
        recs = list(_corpus_records(path))
        ref = [op0c.parse_0c(bytes.fromhex(r["block_hex"])) for r in recs]
        self.assertEqual(len(ref), 13)
        for rec, r in zip(recs, ref):
            f = rec["command_decode"]["commands"][0]["fields"]
            self.assertEqual(f["obj_04_u32"], r["A"])
            self.assertEqual(f["obj_08_hex"], r["B"])
            self.assertEqual(f["obj_18_array"]["items_u32"], r["arr18"])
            self.assertEqual(f["obj_34_array"]["items_u32"], r["arr34"])
            self.assertEqual([tuple(fl(c) for c in p["xyz_f32"]) + (p["kind_u32"],)
                              for p in f["obj_50_points"]["items"]], r["pts50"])
            self.assertEqual([tuple(fl(c) for c in p["xyz_f32"]) + (p["kind_u32"],)
                              for p in f["obj_9c_points"]["items"]], r["pts9c"])
            self.assertEqual(f["obj_e8_array"]["items_u32"], r["arrE8"])
            self.assertEqual(f["obj_104_u32"], r["C"])
            self.assertEqual(f["obj_108_hex"], r["D"])
            json.dumps(rec["command_decode"], allow_nan=False)


if __name__ == "__main__":
    unittest.main()
