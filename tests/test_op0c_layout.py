"""Opcode 0x0C ChangeProduction layout: regression tests for research/op0c_layout.py.

Pins the creator-derived read sequence (FUN_00b2eeb0, build 59638) with synthetic
blocks, and the corpus fit on authentic samples when they are cached. Corpus tests
skip when WGRD_SAMPLES_DIR (default ~/.hermes/artifacts/wgrd-replay/samples/raw)
is absent. See research/CHANGEPRODUCTION-0C.md.
"""
import importlib.util
import json
import math
import os
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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


class SyntheticLayout(unittest.TestCase):
    def test_minimum_block_is_61_bytes(self):
        r = op0c.parse_0c(block(a=1, c=7))
        self.assertEqual(r["len"], 61)
        self.assertEqual((r["A"], r["C"]), (1, 7))
        self.assertEqual(r["arr18"], [])
        self.assertEqual(r["pts9c"], [])

    def test_arrays_consume_exactly(self):
        blk = block(arr18=(5,), arr34=(13,), pts50=[(1., 2., 3., 2)], pts9c=[(4., 5., 6., 0), (7., 8., 9., 1)],
                    arrE8=(0x4030DD88,))
        r = op0c.parse_0c(blk)
        self.assertEqual(r["len"], len(blk))
        self.assertEqual(r["pts50"], [(1., 2., 3., 2)])
        self.assertEqual(len(r["pts9c"]), 2)
        self.assertEqual(r["arrE8"], [0x4030DD88])

    def test_arr34_bound_0x0e(self):
        op0c.parse_0c(block(arr34=(0x0E,)))
        with self.assertRaises(ValueError):
            op0c.parse_0c(block(arr34=(0x0F,)))

    def test_point_kind_bound_6(self):
        op0c.parse_0c(block(pts50=[(0., 0., 0., 6)]))
        with self.assertRaises(ValueError):
            op0c.parse_0c(block(pts50=[(0., 0., 0., 7)]))
        with self.assertRaises(ValueError):
            op0c.parse_0c(block(pts9c=[(0., 0., 0., 7)]))

    def test_trailing_and_truncated_rejected(self):
        blk = block(pts50=[(1., 2., 3., 2)])
        with self.assertRaises(ValueError):
            op0c.parse_0c(blk + b"\0")
        with self.assertRaises(ValueError):
            op0c.parse_0c(blk[:-1])
        with self.assertRaises(ValueError):
            op0c.parse_0c(b"\x0d" + blk[1:])


class CorpusFit(unittest.TestCase):
    EXPECTED = {
        "koppeltar-Sample1.wargamerpl2": {105: 13},
        "koppeltar-Sample3.wargamerpl2": {105: 28},
        "koppeltar-Sample2.wargamerpl2": {105: 4, 281: 2},
    }

    def setUp(self):
        manifest = json.load(open(ROOT / "samples" / "manifest.json"))["samples"]
        self.paths = {s["file"]: SAMPLES / s["file"] for s in manifest}
        if not all(p.exists() for p in self.paths.values()):
            self.skipTest("authentic samples not cached; set WGRD_SAMPLES_DIR")

    def _parsed(self, name):
        return [(fr, sl, op0c.parse_0c(b)) for fr, sl, b in op0c.blocks_0c(str(self.paths[name]))]

    def test_all_47_blocks_fit_exactly(self):
        for name, sizes in self.EXPECTED.items():
            got = {}
            for _, _, r in self._parsed(name):
                got[r["len"]] = got.get(r["len"], 0) + 1
            self.assertEqual(got, sizes, name)

    def test_sample1_golden_values(self):
        rows = self._parsed("koppeltar-Sample1.wargamerpl2")
        self.assertEqual(len(rows), 13)
        for fr, slot, r in rows:
            self.assertEqual(r["A"], 0xC000001E + slot, (fr, slot))
            self.assertEqual(r["B"], "00" * 12 + "32000000")  # same raw16 as opcode 0x08
            self.assertEqual((r["C"], r["D"]), (0, "00" * 16))
            self.assertEqual([len(r[k]) for k in ("arr18", "arr34", "pts50", "pts9c", "arrE8")], [1] * 5)
            self.assertIn(r["arr34"][0], {3, 8, 10, 13})
            self.assertEqual(r["pts50"][0][3], 2)
            x, y, z, k = r["pts9c"][0]
            self.assertTrue(all(map(math.isinf, (x, y, z))) and k == 0, (fr, r["pts9c"]))
        self.assertEqual([r["arr34"][0] for _, _, r in rows], [3, 3, 3, 3, 3, 3, 10, 3, 3, 13, 10, 8, 13])


if __name__ == "__main__":
    unittest.main()
