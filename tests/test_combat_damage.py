"""Tests for the Phase 2a direct-fire damage kernel.

Two evidence classes are kept separate on purpose:

* SYNTHETIC cases are constructed inputs with expected IEEE-754 float32 bit
  patterns. They test the arithmetic contract only; they are not game data.
* ENGINE OBSERVATIONS are the retained 28 enter/leave pairs from
  ``run-07.jsonl``. Only the three mode-2 pairs exercise the HP clamp. The 25
  mode-1 pairs are additive suppression, and this kernel does not predict them.

No weapon identity, facing label, accuracy term or falloff table is asserted
here; none is available from the retained evidence.
"""
import hashlib
import json
import os
import struct
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "research"
if str(RESEARCH) not in sys.path:
    sys.path.insert(0, str(RESEARCH))

import combat_damage  # noqa: E402

_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")

FIXTURES = Path(os.environ.get(
    "WGRD_COMBAT_DAMAGE_FIXTURES",
    Path.home() / ".hermes/artifacts/wgrd-replay"
    "/combat-damage-static-20261109/delegates/B/hp_clamp_fixtures.json"))
FIXTURES_SHA256 = "e4eaaad06df3fe4925e9ed887142d781b552fd2cc77e9817396508d4837c5654"


def f32(value):
    return _F32.unpack(_F32.pack(value))[0]


def bits(value):
    return "0x%08x" % _U32.unpack(_F32.pack(f32(value)))[0]


class TestSyntheticAmountOrder(unittest.TestCase):
    """SYNTHETIC: the verified left-to-right float32 product order."""

    def test_inputs_are_rounded_to_float32_first(self):
        self.assertEqual(bits(0.1), "0x3dcccccd")
        self.assertEqual(combat_damage.damage_amount(0.1, 1.0, 1.0, 1.0, 1.0, 1.0),
                         f32(0.1))

    def test_exact_power_of_two_product(self):
        # SYNTHETIC: no intermediate rounding is observable here.
        self.assertEqual(
            bits(combat_damage.damage_amount(2.0, 0.5, 8.0, 0.25, 1.0, 4.0)),
            "0x41000000")

    def test_rounds_after_every_multiply(self):
        # SYNTHETIC: per-step float32 rounding differs from one final rounding
        # of the double-precision product. Expected bits are fixed constants.
        cases = [
            ((0.1, 0.1, 3.0, 1.0, 1.0, 0.1), "0x3b449ba7"),
            ((1.1, 1.1, 1.1, 1.1, 1.1, 1.1), "0x3fe2c284"),
            ((0.3, 0.7, 1.3, 1.7, 0.9, 1.1), "0x3eeb3e35"),
        ]
        for inputs, expected in cases:
            with self.subTest(inputs=inputs):
                product = 1.0
                for value in inputs:
                    product *= f32(value)
                self.assertEqual(bits(combat_damage.damage_amount(*inputs)), expected)
                self.assertNotEqual(bits(f32(product)), expected,
                                    "case does not distinguish per-step rounding")

    def test_left_to_right_association_differs_from_pair_grouping(self):
        # SYNTHETIC: ((H*P)*(T*K))*(C*F) gives a different bit pattern.
        inputs = (0.355, 1.71, 1.551, 0.585, 1.041, 0.954)
        grouped = f32(f32(f32(f32(inputs[0]) * f32(inputs[1]))
                          * f32(f32(inputs[2]) * f32(inputs[3])))
                      * f32(f32(inputs[4]) * f32(inputs[5])))
        self.assertEqual(bits(combat_damage.damage_amount(*inputs)), "0x3f0c0884")
        self.assertEqual(bits(grouped), "0x3f0c0883")


class TestSyntheticMode2Clamp(unittest.TestCase):
    """SYNTHETIC: all three branches of the mode-2 HP clamp."""

    def test_clamped_branch(self):
        applied, current = combat_damage.apply_mode2(28.0, 10.0, 0.0)
        self.assertEqual((bits(applied), bits(current)), ("0x41200000", "0x41200000"))

    def test_unclamped_branch(self):
        applied, current = combat_damage.apply_mode2(3.0, 10.0, 4.0)
        self.assertEqual((bits(applied), bits(current)), ("0x40400000", "0x40e00000"))

    def test_floor_branch(self):
        # A negative amount drives the sum below zero; current floors at 0.
        applied, current = combat_damage.apply_mode2(-2.0, 10.0, 1.0)
        self.assertEqual((bits(applied), bits(current)), ("0xc0000000", "0x00000000"))

    def test_current_addition_rounds_to_float32(self):
        # SYNTHETIC: 1.0 + 1e-8 rounds back to 1.0 in float32, so a tiny
        # amount is applied but does not move the stored current.
        applied, current = combat_damage.apply_mode2(1e-8, 10.0, 1.0)
        self.assertEqual(bits(applied), "0x322bcc77")
        self.assertEqual(bits(current), "0x3f800000")

    def test_zero_room_clamps_to_zero(self):
        applied, current = combat_damage.apply_mode2(20.0, 10.0, 10.0)
        self.assertEqual((bits(applied), bits(current)), ("0x00000000", "0x41200000"))


class TestEngineMode2Observations(unittest.TestCase):
    """ENGINE OBSERVATION: the retained 28-pair fixture."""

    @classmethod
    def setUpClass(cls):
        if not FIXTURES.exists():
            raise unittest.SkipTest("retained damage fixture unavailable: " + str(FIXTURES))
        raw = FIXTURES.read_bytes()
        if hashlib.sha256(raw).hexdigest() != FIXTURES_SHA256:
            raise AssertionError("retained damage fixture integrity mismatch: " + str(FIXTURES))
        cls.fixture = json.loads(raw)
        cls.pairs = cls.fixture["fixtures"]

    def test_fixture_shape(self):
        self.assertEqual(self.fixture["schema"], "wgrd-hp-clamp-fixtures/1")
        self.assertEqual(len(self.pairs), 28)
        self.assertEqual(sum(pair["mode"] == 2 for pair in self.pairs), 3)
        self.assertEqual(sum(pair["mode"] == 1 for pair in self.pairs), 25)

    def test_mode2_pairs_are_bit_exact(self):
        checked = 0
        for pair in self.pairs:
            if pair["mode"] != 2:
                continue
            with self.subTest(call_id=pair["call_id"]):
                before = pair["decoded_before"]
                amount = pair["amount_decoded"]["value"]
                applied, current = combat_damage.apply_mode2(
                    amount,
                    before["0x194_max_damages"]["value"],
                    before["0x19c_current_damage"]["value"])
                check = pair["mode2_check"]
                self.assertEqual(bits(applied), check["predicted_bits"])
                self.assertEqual(bits(current), check["observed_bits"])
                self.assertEqual(bits(applied), bits(check["applied_f32"]))
                checked += 1
        self.assertEqual(checked, 3)

    def test_mode2_fixture_covers_only_the_clamped_branch(self):
        # The observation set does not exercise the unclamped or floor branch;
        # those are covered by synthetic cases above, not claimed as observed.
        mode2 = [pair for pair in self.pairs if pair["mode"] == 2]
        self.assertTrue(all(pair["mode2_check"]["applied_clamped"] for pair in mode2))

    def test_mode1_pairs_are_out_of_scope(self):
        # Additive suppression is not part of this kernel. The fixture is
        # retained as evidence that these pairs exist, not as a prediction.
        mode1 = [pair for pair in self.pairs if pair["mode"] == 1]
        self.assertEqual(len(mode1), 25)
        self.assertTrue(all("mode1_empirical" in pair for pair in mode1))


if __name__ == "__main__":
    unittest.main()
