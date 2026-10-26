"""Opcodes 0x02, 0x13, 0x18: fixed-size creator layouts (wgrd_replay._decode_command).

Layouts from research/FIXED-OPCODES-02-13-18.md and research/op_fixed_layout.py (build 59638).
Field names are data-only (obj_XX offsets); semantics are unconfirmed. Synthetic tests pin exact
consumption; corpus tests skip when authentic samples are absent (WGRD_SAMPLES_DIR, default
~/.hermes/artifacts/wgrd-replay/samples/raw). The EXE test skips when WarGame3.exe is absent
(WGRD_EXE_59638 overrides the default path).
"""
import importlib.util
import json
import os
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import wgrd_replay as w  # noqa: E402

_spec = importlib.util.spec_from_file_location("op_fixed_layout", ROOT / "research" / "op_fixed_layout.py")
ofl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ofl)

SAMPLES = Path(os.environ.get("WGRD_SAMPLES_DIR",
                              str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))
EXE = Path(os.environ.get("WGRD_EXE_59638",
                          str(Path.home() / ".hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe")))

SLOT_BASE = 0xC000001E


def u32(v):
    return struct.pack("<I", v)


def blk02(a=SLOT_BASE, b=bytes(12) + u32(0x32), c=0):
    return bytes([0x02]) + u32(a) + b + bytes([c])


def blk13(a=0, b=0, c=0):
    return bytes([0x13]) + u32(a) + u32(b) + u32(c)


def blk18(a=0, b=0, c=0):
    return bytes([0x18]) + u32(a) + u32(b) + bytes([c])


SIZES = {0x02: 22, 0x13: 13, 0x18: 10}


def decode1(blk, slot=0):
    return w.decode_command_block(blk, 1, slot)


class SyntheticLayouts(unittest.TestCase):
    def test_0x02_exact_consumption_and_fields(self):
        blk = blk02(a=SLOT_BASE + 3, c=0x7F)
        self.assertEqual(len(blk), 22)
        r = decode1(blk)
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["consumed_bytes"], 22)
        self.assertEqual(r["remaining_hex"], "")
        cmd = r["commands"][0]
        self.assertEqual((cmd["opcode"], cmd["class"], cmd["length"]),
                         (0x02, "TNetworkActionSurrender", 22))
        self.assertEqual(cmd["field_decode_status"], "layout")
        self.assertEqual(cmd["fields"], {"obj_04_u32": SLOT_BASE + 3,
                                         "obj_08_hex": "00" * 12 + "32000000",
                                         "obj_18_u8": 0x7F})
        self.assertEqual(cmd["raw_hex"], blk.hex())

    def test_0x13_exact_consumption_and_fields(self):
        blk = blk13(a=0, b=1, c=16)
        self.assertEqual(len(blk), 13)
        r = decode1(blk)
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["consumed_bytes"], 13)
        cmd = r["commands"][0]
        self.assertEqual((cmd["opcode"], cmd["class"], cmd["length"]),
                         (0x13, "TNetworkActionPlayerSynchroServiceAction", 13))
        self.assertEqual(cmd["field_decode_status"], "layout")
        self.assertEqual(cmd["fields"], {"obj_04_u32": 0, "obj_08_u32": 1, "obj_0c_u32": 16})
        self.assertEqual(cmd["raw_hex"], blk.hex())

    def test_0x18_exact_consumption_and_fields(self):
        blk = blk18(a=0xC00006E5, b=2, c=1)
        self.assertEqual(len(blk), 10)
        r = decode1(blk)
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["consumed_bytes"], 10)
        cmd = r["commands"][0]
        self.assertEqual((cmd["opcode"], cmd["class"], cmd["length"]),
                         (0x18, "TNetworkActionDeactivateSupply", 10))
        self.assertEqual(cmd["field_decode_status"], "layout")
        self.assertEqual(cmd["fields"], {"obj_04_u32": 0xC00006E5, "obj_08_u32": 2, "obj_0c_u8": 1})
        self.assertEqual(cmd["raw_hex"], blk.hex())

    def test_truncated_blocks_are_malformed(self):
        for blk in (blk02(), blk13(), blk18()):
            for cut in range(1, len(blk)):
                r = decode1(blk[:cut])
                self.assertEqual(r["status"], "malformed", (hex(blk[0]), cut))
                self.assertEqual(r["consumed_bytes"], 0, (hex(blk[0]), cut))
                self.assertIn("overruns block", r["reason"])

    def test_trailing_byte_in_count_one_block_is_malformed(self):
        for blk in (blk02(), blk13(), blk18()):
            r = decode1(blk + b"\x00")
            self.assertEqual(r["status"], "malformed", hex(blk[0]))
            self.assertEqual(r["reason"], "trailing bytes after declared command count")
            self.assertEqual(r["consumed_bytes"], len(blk))

    def test_wrapper_split_matches_size(self):
        for op, size in SIZES.items():
            blk = {0x02: blk02, 0x13: blk13, 0x18: blk18}[op]()
            self.assertEqual(len(blk), size)
            cur = w._CommandCursor(blk)
            cmd = w._decode_command(cur, 0)
            self.assertEqual(cur.offset, size)
            self.assertEqual(cmd["length"], size)


def _corpus_records(path):
    for rec in w.parse_replay(path.read_bytes())["commands"]:
        if rec["count"] == 1 and rec["block_hex"][:2] in ("02", "13", "18"):
            yield rec


class CorpusDecode(unittest.TestCase):
    # (sample file) -> {opcode: expected single-command block count}
    EXPECTED = {
        "koppeltar-Sample1.wargamerpl2": {0x02: 0, 0x13: 10, 0x18: 19},
        "koppeltar-Sample3.wargamerpl2": {0x02: 3, 0x13: 4, 0x18: 25},
        "koppeltar-Sample2.wargamerpl2": {0x02: 2, 0x13: 2, 0x18: 0},  # different build: inferred
    }

    def setUp(self):
        manifest = json.loads((ROOT / "samples" / "manifest.json").read_text())["samples"]
        self.paths = {s["file"]: SAMPLES / s["file"] for s in manifest}
        if not all(p.exists() for p in self.paths.values()):
            self.skipTest("authentic samples not cached; set WGRD_SAMPLES_DIR")

    def test_per_sample_counts_and_all_complete(self):
        for name, expected in self.EXPECTED.items():
            counts = {op: 0 for op in SIZES}
            for rec in _corpus_records(self.paths[name]):
                op = int(rec["block_hex"][:2], 16)
                counts[op] += 1
                dec = rec["command_decode"]
                self.assertEqual(dec["status"], "complete",
                                 (name, rec["frame"], rec["slot"], dec.get("reason")))
                self.assertEqual(dec["consumed_bytes"], rec["block_length"])
                self.assertEqual(dec["commands"][0]["field_decode_status"], "layout")
                self.assertEqual(rec["block_length"], SIZES[op], (name, hex(op)))
            self.assertEqual(counts, expected, name)

    def test_0x02_golden_fields(self):
        for name in ("koppeltar-Sample3.wargamerpl2", "koppeltar-Sample2.wargamerpl2"):
            recs = [r for r in _corpus_records(self.paths[name]) if r["block_hex"][:2] == "02"]
            self.assertTrue(recs, name)
            for rec in recs:
                f = rec["command_decode"]["commands"][0]["fields"]
                self.assertEqual(f["obj_04_u32"], 0xC000001E + rec["slot"], (name, rec["frame"], rec["slot"]))
                self.assertEqual(f["obj_08_hex"], "00" * 12 + "32000000", (name, rec["frame"]))
                json.dumps(rec["command_decode"], allow_nan=False)


class LayoutAgreement(unittest.TestCase):
    def test_block_lengths_match_op_fixed_layout(self):
        for op, (_creator, total, _reads) in ofl.LAYOUTS.items():
            self.assertEqual(total, SIZES[op], hex(op))
            if op == 0x02:
                blk = blk02()
            elif op == 0x13:
                blk = blk13()
            else:
                blk = blk18()
            self.assertEqual(len(blk), total, hex(op))
            r = decode1(blk)
            self.assertEqual(r["status"], "complete", hex(op))
            self.assertEqual(r["commands"][0]["length"], total, hex(op))

    def test_decoder_field_offsets_and_widths_match_layout(self):
        # Decoder field names encode dest offset (obj_XX) and width (u32/u8/hex16).
        for op, (_creator, _total, reads) in ofl.LAYOUTS.items():
            blk = {0x02: blk02, 0x13: blk13, 0x18: blk18}[op]()
            fields = decode1(blk)["commands"][0]["fields"]
            decoded = []
            for key, value in fields.items():
                off = int(key.split("_")[1], 16)
                if key.endswith("_hex"):
                    width = len(value) // 2
                elif key.endswith("_u8"):
                    width = 1
                else:
                    width = 4
                decoded.append((off, width))
            self.assertEqual(sorted(decoded), sorted(reads), hex(op))


@unittest.skipUnless(EXE.exists(), "WarGame3.exe build 59638 not present; set WGRD_EXE_59638")
class ExecutableLayouts(unittest.TestCase):
    def test_creator_from_table_resolves_to_layout_creators(self):
        exe = EXE.read_bytes()
        for op, (creator, _total, _reads) in ofl.LAYOUTS.items():
            _case, _stub, target = ofl.creator_from_table(exe, op)
            self.assertEqual(target, creator, hex(op))

    def test_read_pushes_in_order_matches_layouts(self):
        exe = EXE.read_bytes()
        for op, (creator, _total, reads) in ofl.LAYOUTS.items():
            self.assertEqual(ofl.read_pushes_in_order(exe, creator), list(reads), hex(op))


if __name__ == "__main__":
    unittest.main()
