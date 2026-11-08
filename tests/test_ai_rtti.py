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
    STORES = [
        "            0x00b91b0b      movss xmm0, dword [edi+0x1b4]\n",
        "            0x00b91b13      mov   eax, dword [0x1da4048]               ; [0x1da4048:4]=0x20265f4\n",
        "            0x00b91b18      movss dword [0x2026348], xmm0\n",
        "            0x00b9214f      movzx eax, byte [edi+0x270]\n",
        "            0x00b92156      mov   byte [0x20263a1], al\n",
    ]
    REGISTRY = [
        "            0x00b94129      push  0x1ec                                ; 492\n",
        "            0x00b9412e      push  0x00\n",
        "            0x00b94130      push  str.DefaultDifficulty\n",
        "            0x00b94135      call  0x544050\n",
        "            0x00b94211      push  0x2b8                                ; 696\n",
        "            0x00b94216      push  0x00\n",
        "            0x00b94218      push  str.BonusDissimulationDesUnites\n",
    ]

    def test_pairs_load_with_store_across_intervening_instruction(self):
        mapping = ai_tunable_map.parse_stores(self.STORES)
        self.assertEqual(mapping[0x1B4][0]["global"], "0x02026348")
        self.assertEqual(mapping[0x270][0]["global"], "0x020263a1")
        self.assertEqual(mapping[0x1B4][0]["store_site"], "0x00b91b18")

    def test_store_register_must_match_the_load(self):
        listing = [
            "            0x00b9202f      mov   eax, dword [edi+0x264]\n",
            "            0x00b92035      mov   dword [0x2026390], ecx\n",
            "            0x00b9203b      mov   dword [0x2026394], eax\n",
        ]
        mapping = ai_tunable_map.parse_stores(listing)
        self.assertEqual(mapping[0x264][0]["global"], "0x02026394")

    def test_registry_pairs_offset_with_name(self):
        table = ai_tunable_map.parse_registry(self.REGISTRY)
        self.assertEqual(table[0x1EC], "DefaultDifficulty")
        self.assertEqual(table[0x2B8], "BonusDissimulationDesUnites")

    def test_registry_honours_address_bounds(self):
        table = ai_tunable_map.parse_registry(self.REGISTRY, lo=None, hi=0xB94200)
        self.assertEqual(set(table), {0x1EC})

    def test_no_pair_without_store(self):
        self.assertEqual(ai_tunable_map.parse_stores(self.STORES[:1]), {})


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
        self.assertEqual(hits[0]["site"], base)          # instruction start

    def test_ebp_disp32_is_a_valid_base(self):
        base = 0x400000
        # mov ecx, [ebp+0x271]: modrm 0xad is mod=10, rm=5. With mod=10 rm=5
        # means EBP base; rejecting it would drop real locals-derived reads.
        body = bytes([0x8B, 0xAD]) + struct.pack("<I", 0x271)
        image = ai_rtti.Image(imagebase=base, size_of_image=0x2000, sections=[
            ai_rtti.Section(name=".text", va=base, vsize=len(body), data=body,
                            characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
        ])
        hits = ai_field_xrefs.find_disp_xrefs(image, 0x271)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["base"], "[ebp]")
        self.assertEqual(hits[0]["site"], base)          # instruction start

    def test_sib_follows_modrm(self):
        base = 0x400000
        # mov eax, [edi+ecx*4+0x271]: modrm 0x84 (mod=10, rm=4), then SIB 0x8f
        # (scale=2, index=ecx, base=edi), then disp32. The ModRM must be read at
        # the byte before the SIB, not at the SIB itself.
        body = bytes([0x8B, 0x84, 0x8F]) + struct.pack("<I", 0x271)
        image = ai_rtti.Image(imagebase=base, size_of_image=0x2000, sections=[
            ai_rtti.Section(name=".text", va=base, vsize=len(body), data=body,
                            characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
        ])
        hits = ai_field_xrefs.find_disp_xrefs(image, 0x271)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["base"], "[edi+ecx*4]")
        self.assertEqual(hits[0]["site"], base)          # instruction start


    def test_two_byte_0f_opcode_is_accepted(self):
        base = 0x400000
        # movzx eax, byte [edi+0x270]: 0F B6 87 <disp32>. The byte before the
        # ModRM is the second opcode byte, not a single-byte opcode.
        body = bytes([0x0F, 0xB6, 0x87]) + struct.pack("<I", 0x270)
        image = ai_rtti.Image(imagebase=base, size_of_image=0x2000, sections=[
            ai_rtti.Section(name=".text", va=base, vsize=len(body), data=body,
                            characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
        ])
        hits = ai_field_xrefs.find_disp_xrefs(image, 0x270)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["site"], base)          # instruction start
        self.assertEqual(hits[0]["base"], "[edi]")

    def test_sib_ebp_base_is_not_no_base(self):
        base = 0x400000
        # mov edx, [ebp+ecx*4+0x270]: modrm 0x94 (mod=10, rm=4), sib 0x8d
        # (scale=2, index=ecx, base=5). With mod != 0, base=5 means EBP.
        body = bytes([0x8B, 0x94, 0x8D]) + struct.pack("<I", 0x270)
        image = ai_rtti.Image(imagebase=base, size_of_image=0x2000, sections=[
            ai_rtti.Section(name=".text", va=base, vsize=len(body), data=body,
                            characteristics=ai_rtti.IMAGE_SCN_MEM_EXECUTE),
        ])
        hits = ai_field_xrefs.find_disp_xrefs(image, 0x270)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["base"], "[ebp+ecx*4]")


class TestOracle(unittest.TestCase):
    def test_confirm_requires_instruction_start_and_operand(self):
        oracle = ai_field_xrefs.RizinOracle("unused")
        oracle._funcs = [(0x1000, 0x1100)]
        oracle._listing = {0x1010: "movzx eax, byte [edi+0x270]"}
        self.assertTrue(oracle.confirm_many([(0x1010, 0x270)])[0x1010][0])
        self.assertFalse(oracle.confirm_many([(0x1011, 0x270)])[0x1011][0])
        self.assertFalse(oracle.confirm_many([(0x1010, 0x271)])[0x1010][0])

    def test_confirm_rejects_immediate_with_same_value(self):
        oracle = ai_field_xrefs.RizinOracle("unused")
        oracle._funcs = [(0x1000, 0x1100)]
        oracle._listing = {0x1010: "mov eax, 0x270"}
        self.assertFalse(oracle.confirm_many([(0x1010, 0x270)])[0x1010][0])

    def test_confirm_calls_checks_mnemonic_and_target(self):
        oracle = ai_field_xrefs.RizinOracle("unused")
        oracle._funcs = [(0x2000, 0x2100)]
        oracle._listing = {0x2010: "call 0x10828a5"}
        self.assertTrue(oracle.confirm_calls([(0x2010, 0x10828A5)])[0x2010])
        self.assertFalse(oracle.confirm_calls([(0x2010, 0x1082800)])[0x2010])


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

    def test_registry_and_globals_artifacts_agree(self):
        registry = json.loads((REPO / "research/current-build/ai-field-registry.json").read_text())
        globals_map = json.loads(TUNABLE_GLOBALS.read_text())
        self.assertEqual(len(registry), 167)
        registered = {int(k, 16) for k in registry}
        stored = {int(k, 16) for k in globals_map}
        # 155 registered fields reach a fixed global through a matched pair;
        # the rest are address-taken, packed, or copied into a heap array.
        self.assertEqual(len(registered & stored), 155)

    def test_tunable_globals_cover_the_named_fields(self):
        globals_map = json.loads(TUNABLE_GLOBALS.read_text())
        self.assertEqual(len(globals_map), 162)
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
