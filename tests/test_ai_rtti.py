"""Tests for the AI static-analysis tooling and the findings ledger.

The RTTI resolver is pinned against a synthetic fixture (exact, always runs) and
against the retained 131544 binary when its artifact is present (skipped, not
failed, when absent). The tunable-map parser is exercised with a synthetic
Rizin listing so its pairing rules are tested without the binary.
"""
import json
import os
import struct
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ai_rtti  # noqa: E402
import ai_tunable_map  # noqa: E402
import ai_field_xrefs  # noqa: E402

CURRENT_EXE = Path(os.environ.get(
    "WGRD_CURRENT_EXE",
    Path.home() / ".hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe"))
CURRENT_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"

LEDGER = REPO / "research/current-build/ai-findings-ledger.json"
TUNABLE_GLOBALS = REPO / "research/current-build/ai-tunable-globals.json"


def synthetic_image():
    """Build a minimal image holding one TypeDescriptor -> COL -> vftable."""
    base = 0x400000
    rdata = bytearray(0x200)
    text = bytearray(b"\xc3" * 0x20)

    def put(buf, va, data):
        buf[va - base:va - base + len(data)] = data

    td_va = base + 0x20
    col_va = base + 0x60
    vt_va = base + 0x90
    text_va = base + 0x200

    rdata_text = b".?AVTFoo@Eugen@@\0"

    def w(va, value):
        struct.pack_into("<I", rdata, va - base, value)

    put(rdata, td_va + 8, rdata_text)          # name at TD+8
    w(td_va, base + 0x180)                     # TD vftable pointer (plausible)
    w(td_va + 4, 0)
    w(col_va, 1)                               # signature
    w(col_va + 4, 0)
    w(col_va + 8, 0)
    w(col_va + 12, td_va)                      # pTypeDescriptor
    w(col_va + 16, base + 0x1c0)               # pClassDescriptor
    w(vt_va - 4, col_va)                       # vftable[-1]
    w(vt_va, text_va)                          # slot 0
    w(vt_va + 4, text_va + 4)                  # slot 1

    image = ai_rtti.Image(imagebase=base, size_of_image=0x1000, sections=[
        ai_rtti.Section(name=".rdata", va=base, vsize=len(rdata), data=bytes(rdata)),
        ai_rtti.Section(name=".text", va=text_va, vsize=len(text), data=bytes(text),
                        characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
    ])
    image.build_pointer_index()
    return image, td_va, col_va, vt_va, text_va


class TestRttiResolver(unittest.TestCase):
    def test_resolves_type_descriptor_to_vtable(self):
        image, td, col, vt, text_va = synthetic_image()
        result = ai_rtti.resolve_class(image, ".?AVTFoo@Eugen@@")
        self.assertEqual(result["type_descriptor"], td)
        self.assertIn(col, result["locators"])
        self.assertIn(vt, result["vtables"])
        self.assertEqual(ai_rtti.vtable_slots(image, vt), [text_va, text_va + 4])

    def test_missing_class_raises(self):
        image, *_ = synthetic_image()
        with self.assertRaises(ai_rtti.ImageError):
            ai_rtti.resolve_class(image, ".?AVTNotThere@Eugen@@")

    def test_vtable_stops_at_non_executable(self):
        image, _, _, vt, text_va = synthetic_image()
        # slot 2 points into .rdata, so the walk must stop after two slots
        self.assertEqual(len(ai_rtti.vtable_slots(image, vt)), 2)

    @unittest.skipUnless(CURRENT_EXE.is_file(), "retained 131544 executable not present")
    def test_real_binary_pins(self):
        image = ai_rtti.load_pe32(str(CURRENT_EXE))
        self.assertEqual(image.imagebase, 0x00400000)
        result = ai_rtti.resolve_class(image, ".?AVTWargameCheatLogic_Impl@Wargame@Eugen@@")
        self.assertEqual(result["type_descriptor"], 0x01F98690)
        self.assertIn(0x01C32FFC, result["locators"])
        self.assertIn(0x01A130AC, result["vtables"])
        slots = ai_rtti.vtable_slots(image, 0x01A130AC)
        self.assertEqual(slots[:3], [0x01326670, 0x01344000, 0x004D7B40])


class TestTunableMap(unittest.TestCase):
    LISTING = [
        "            0x00b91b0b      movss xmm0, dword [edi+0x1b4]\n",
        "            0x00b91b13      mov   eax, dword [0x1da4048]               ; [0x1da4048:4]=0x20265f4\n",
        "            0x00b91b18      movss dword [0x2026348], xmm0\n",
        "            0x00b9214f      movzx eax, byte [edi+0x270]\n",
        "            0x00b92156      mov   byte [0x20263a1], al\n",
        "            0x00b9215b      movzx eax, byte [edi+0x271]\n",
        "            0x00b92162      mov   byte [0x20263a2], al\n",
    ]

    def test_pairs_load_with_store_across_intervening_instruction(self):
        mapping = ai_tunable_map.parse(self.LISTING)
        self.assertEqual(mapping[0x1B4][0]["global"],
                         "0x02026348")
        self.assertEqual(mapping[0x270][0]["global"], "0x020263a1")
        self.assertEqual(mapping[0x270][0]["width"], "byte")
        self.assertEqual(mapping[0x1B4][0]["store_site"], "0x00b91b18")

    def test_no_pair_without_store(self):
        mapping = ai_tunable_map.parse(self.LISTING[:1])
        self.assertEqual(mapping, {})


class TestDispXrefs(unittest.TestCase):
    def test_matches_reg_disp_and_ignores_immediate(self):
        base = 0x400000
        # 0x81 0x87 <disp32>  -> add dword [edi+disp], imm32 (mod=10, rm=7)
        real = bytes([0x81, 0x87]) + struct.pack("<I", 0x271) + b"\x00\x00\x00\x00"
        # ret, then mov eax, imm32: the same value must not be reported, because
        # the byte before it (0xc3) is not an r/m opcode.
        fake = b"\xc3\xb8" + struct.pack("<I", 0x271)
        body = real + fake
        image = ai_rtti.Image(imagebase=base, size_of_image=0x2000, sections=[
            ai_rtti.Section(name=".text", va=base, vsize=len(body), data=body,
                            characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
        ])
        hits = ai_field_xrefs.find_disp_xrefs(image, 0x271)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["base"], "[edi]")
        self.assertEqual(hits[0]["site"], base + 1)


class TestLedger(unittest.TestCase):
    def test_ledger_is_consistent(self):
        ledger = json.loads(LEDGER.read_text())
        legend = set(ledger["status_legend"])
        ids = [c["id"] for c in ledger["claims"]]
        self.assertEqual(len(ids), len(set(ids)), "claim ids must be unique")
        for claim in ledger["claims"]:
            self.assertIn(claim["axis"], {"meta", "economy", "information", "mechanics"})
            self.assertIn(claim["status"], legend)
            self.assertTrue(claim["claim"].strip())
        proven = {c["id"] for c in ledger["claims"] if c["status"] == "proven"}
        self.assertTrue({"P1", "P2", "P3", "P4", "P5", "P6"} <= proven)

    def test_economy_and_information_axes_are_separate(self):
        ledger = json.loads(LEDGER.read_text())
        axes = {c["id"]: c["axis"] for c in ledger["claims"]}
        self.assertEqual(axes["P4"], "economy")
        self.assertEqual(axes["P5"], "information")

    def test_tunable_globals_cover_the_named_fields(self):
        globals_map = json.loads(TUNABLE_GLOBALS.read_text())
        self.assertEqual(len(globals_map), 65)
        expected = {
            "0x01f0": "0x02026360",
            "0x01fc": "0x02026364",
            "0x0208": "0x02026368",
            "0x0264": "0x02026390",
            "0x0268": "0x020263a4",
            "0x0270": "0x020263a1",
            "0x0271": "0x020263a2",
        }
        for offset, global_va in expected.items():
            self.assertIn(offset, globals_map)
            self.assertEqual(globals_map[offset][0]["global"], global_va)


if __name__ == "__main__":
    unittest.main()
