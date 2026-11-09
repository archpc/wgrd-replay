"""Tests for the Phase 2c kinetic range family-index kernel (0xda3410).

Evidence classes stay separate:

* SYNTHETIC cases pin the arithmetic and gate contract with constructed values.
* ENGINE OBSERVATIONS are two shipped ``TAmmunition`` records extracted from the
  hash-pinned 131544 NDF. They are raw property values, not names or AP levels.
  Tests that need them skip explicitly when the fixture is absent.

The function returns a damage-table row index only. No Arme name, AP meaning,
accuracy, crit, facing or splash behaviour is asserted.
"""
import hashlib
import json
import math
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
import combat_damage_range  # noqa: E402
import combat_damage_table  # noqa: E402

_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")

CROSSCHECK = Path(os.environ.get(
    "WGRD_RANGE_CROSSCHECK",
    Path.home() / ".hermes/artifacts/wgrd-replay"
    "/combat-damage-static-20261109/phase2c-ammunition-crosscheck.json"))
CROSSCHECK_SHA256 = "5909779c5b4c3b63c73728d641a3b5ab6278b75bca8cfc8c875257630bc33e24"

TABLE = Path(os.environ.get(
    "WGRD_ARME_ARMURE_TABLE",
    Path.home() / ".hermes/artifacts/wgrd-replay"
    "/combat-damage-static-20261109/arme-armure-table.json"))


def f32(value):
    return _F32.unpack(_F32.pack(value))[0]


def bits(value):
    return "0x%08x" % _U32.unpack(_F32.pack(f32(value)))[0]


class TestSyntheticGate(unittest.TestCase):
    """SYNTHETIC: the 0xc2ce00 gate plus the call-site flag test."""

    def test_enabled_at_arme_boundaries(self):
        for arme in (5, 30, 64):
            with self.subTest(arme=arme):
                self.assertTrue(combat_damage_range.range_family_applies(0, arme, 1))

    def test_disabled_by_projectile_type(self):
        for projectile_type in (1, 2, 3, 4, 5):
            with self.subTest(projectile_type=projectile_type):
                self.assertFalse(
                    combat_damage_range.range_family_applies(projectile_type, 8, 1))

    def test_disabled_by_arme_bounds(self):
        for arme in (0, 4, 65):
            with self.subTest(arme=arme):
                self.assertFalse(combat_damage_range.range_family_applies(0, arme, 1))

    def test_disabled_by_flag(self):
        for flag in (0, False):
            with self.subTest(flag=flag):
                self.assertFalse(combat_damage_range.range_family_applies(0, 8, flag))

    def test_gate_rejects_non_integer_inputs(self):
        cases = [(True, 8, 1), ("0", 8, 1), (0, "8", 1), (0, 8, "1")]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    combat_damage_range.range_family_applies(*args)


class TestSyntheticRangeSteps(unittest.TestCase):
    """SYNTHETIC: float32 subtraction, division, and truncation boundaries."""

    def test_step_boundaries(self):
        cases = [
            ((8, 12999.0, 0.0), 8),
            ((8, 12999.9, 0.0), 8),
            ((8, 12999.999, 0.0), 8),
            ((8, 13000.0, 0.0), 9),
            ((8, 13000.001, 0.0), 9),
            ((8, 25999.999, 0.0), 9),
            ((8, 26000.0, 0.0), 10),
            ((8, 39000.0, 0.0), 11),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(
                    combat_damage_range.kinetic_family_index(*args), expected)

    def test_zero_remaining_range(self):
        self.assertEqual(combat_damage_range.kinetic_family_index(8, 156000.0, 156000.0), 8)

    def test_negative_remaining_range_is_clipped(self):
        self.assertEqual(combat_damage_range.kinetic_family_index(8, 10000.0, 13000.0), 8)

    def test_negative_range_max_is_clipped(self):
        self.assertEqual(combat_damage_range.kinetic_family_index(8, -1000.0, 0.0), 8)

    def test_negative_distance_increases_remaining(self):
        self.assertEqual(combat_damage_range.kinetic_family_index(8, 0.0, -13000.0), 9)

    def test_float32_division_is_not_double_division(self):
        # SYNTHETIC: the quotient is rounded to float32 before truncation.
        value = 12999.9990234375  # largest float32 below 13000.0
        self.assertEqual(combat_damage_range.kinetic_family_index(8, value, 0.0), 8)


class TestSyntheticCapsAndFloor(unittest.TestCase):
    """SYNTHETIC: min(cap, ...) and max(5, ...) integer selection."""

    def test_low_arme_caps_at_34(self):
        self.assertEqual(
            combat_damage_range.kinetic_family_index(33, 13000.0 * 100, 0.0), 34)

    def test_arme_34_caps_at_64(self):
        self.assertEqual(
            combat_damage_range.kinetic_family_index(34, 13000.0 * 100, 0.0), 64)

    def test_arme_64_caps_at_64(self):
        self.assertEqual(
            combat_damage_range.kinetic_family_index(64, 13000.0 * 100, 0.0), 64)

    def test_floor_is_5(self):
        for arme in (0, 4):
            with self.subTest(arme=arme):
                self.assertEqual(combat_damage_range.kinetic_family_index(arme, 0.0, 0.0), 5)

    def test_realistic_full_range_step_count(self):
        self.assertEqual(
            combat_damage_range.kinetic_family_index(8, 156000.0, 0.0), 20)


class TestSyntheticInvalidInputs(unittest.TestCase):
    """SYNTHETIC: type and finiteness guards, not engine behaviour."""

    def test_non_integer_arme(self):
        for arme in ("8", 8.0, True, None):
            with self.subTest(arme=arme):
                with self.assertRaises(TypeError):
                    combat_damage_range.kinetic_family_index(arme, 1.0, 0.0)

    def test_non_numeric_range(self):
        for rmax, distance in (("1", 0.0), (1.0, "0"), (None, 0.0), (1.0, None)):
            with self.subTest(rmax=rmax, distance=distance):
                with self.assertRaises(TypeError):
                    combat_damage_range.kinetic_family_index(8, rmax, distance)

    def test_non_finite_range(self):
        for rmax, distance in ((math.nan, 0.0), (math.inf, 0.0), (0.0, math.inf)):
            with self.subTest(rmax=rmax, distance=distance):
                with self.assertRaises(ValueError):
                    combat_damage_range.kinetic_family_index(8, rmax, distance)

    def test_class_selector_rejects_bad_classes(self):
        properties = {"PorteeMaximale": 1.0}
        for target_class in (0, 7, -1):
            with self.subTest(target_class=target_class):
                with self.assertRaises(ValueError):
                    combat_damage_range.range_max_for_class(properties, target_class)
        for target_class in ("2", 2.0, True):
            with self.subTest(target_class=target_class):
                with self.assertRaises(TypeError):
                    combat_damage_range.range_max_for_class(properties, target_class)

    def test_class_selector_requires_present_property(self):
        with self.assertRaises(KeyError):
            combat_damage_range.range_max_for_class({}, 2)
        with self.assertRaises(KeyError):
            combat_damage_range.range_max_for_class({"PorteeMaximale": None}, 2)

    def test_class_selector_rejects_non_finite_value(self):
        with self.assertRaises(ValueError):
            combat_damage_range.range_max_for_class({"PorteeMaximale": math.nan}, 2)


class TestSyntheticTableBackedLookup(unittest.TestCase):
    """SYNTHETIC range inputs, ENGINE OBSERVATION cell."""

    @classmethod
    def setUpClass(cls):
        if not TABLE.exists():
            raise unittest.SkipTest("private arme-armure table unavailable: " + str(TABLE))
        cls.table = combat_damage_table.load_arme_armure_table(TABLE)

    def test_family_index_selects_observed_table_cell(self):
        family = combat_damage_range.kinetic_family_index(8, 156000.0, 0.0)
        self.assertEqual(family, 20)
        self.assertEqual(bits(self.table.lookup(family, 3)), "0x42000000")

    def test_zero_distance_keeps_base_family(self):
        family = combat_damage_range.kinetic_family_index(8, 0.0, 0.0)
        self.assertEqual(family, 8)
        self.assertEqual(bits(self.table.lookup(family, 3)), "0x41000000")

    def test_end_to_end_damage_amount(self):
        family = combat_damage_range.kinetic_family_index(8, 156000.0, 0.0)
        amount = combat_damage.damage_amount(
            0.3, 0.7, self.table.lookup(family, 3), 1.1, 0.9, 1.3)
        self.assertEqual(bits(amount), "0x410a60d5")


class TestEngineNdfObservations(unittest.TestCase):
    """ENGINE OBSERVATION: two shipped TAmmunition records."""

    @classmethod
    def setUpClass(cls):
        if not CROSSCHECK.exists():
            raise unittest.SkipTest("private ammunition cross-check unavailable: "
                                    + str(CROSSCHECK))
        raw = CROSSCHECK.read_bytes()
        if hashlib.sha256(raw).hexdigest() != CROSSCHECK_SHA256:
            raise AssertionError("ammunition cross-check integrity mismatch: "
                                 + str(CROSSCHECK))
        cls.document = json.loads(raw)
        cls.records = {record["ndf_index"]: record for record in cls.document["records"]}

    def test_source_is_the_pinned_131544_extraction(self):
        source = self.document["source"]
        self.assertEqual(source["build"], "131544")
        self.assertEqual(source["archive_sha256"],
                         "172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b")
        self.assertEqual(source["expanded_sha256"],
                         "640c66c2336f6e54bb1e0183a76eecd2d1defe7fafe67ed56e7f82a5021ed032")
        self.assertEqual(source["ammunition_objects"], 2092)
        self.assertEqual(len(self.records), 2)

    def test_two_raw_arme_indices(self):
        expected = {112911: 8, 89611: 3}
        for ndf_index, arme in expected.items():
            with self.subTest(ndf_index=ndf_index):
                record = self.records[ndf_index]
                self.assertEqual(record["class"], "TAmmunition")
                value = record["properties"]["Arme"]
                self.assertIs(type(value), int)
                self.assertEqual(value, arme)
                self.assertTrue(0 <= value <= 64)

    def test_record_a_range_fields_and_absence(self):
        record = self.records[112911]
        properties = record["properties"]
        self.assertEqual(properties["PorteeMaximale"], 156000.0)
        self.assertEqual(properties["PorteeMaximaleBateaux"], 156000.0)
        self.assertEqual(properties["PorteeMaximaleTBA"], 156000.0)
        self.assertEqual(properties["PorteeMaximaleHA"], 104000.0)
        self.assertEqual(properties["EfficaciteSelonPortee"], True)
        self.assertIn("PorteeMaximaleProjectile", record["absent_properties"])
        self.assertIn("ProjectileType", record["absent_properties"])

    def test_record_b_range_fields_and_absence(self):
        record = self.records[89611]
        properties = record["properties"]
        self.assertEqual(properties["PorteeMaximale"], 234000.0)
        self.assertEqual(properties["PorteeMaximaleBateaux"], 234000.0)
        self.assertEqual(properties["PorteeMaximaleTBA"], 156000.0)
        self.assertEqual(properties["PorteeMaximaleHA"], 104000.0)
        self.assertEqual(properties["PorteeMaximaleProjectile"], 208000.0)
        self.assertIn("EfficaciteSelonPortee", record["absent_properties"])

    def test_class_selector_reads_observed_fields(self):
        a = self.records[112911]["properties"]
        self.assertEqual(combat_damage_range.range_max_for_class(a, 1), 156000.0)
        self.assertEqual(combat_damage_range.range_max_for_class(a, 2), 156000.0)
        self.assertEqual(combat_damage_range.range_max_for_class(a, 3), 156000.0)
        self.assertEqual(combat_damage_range.range_max_for_class(a, 4), 156000.0)
        self.assertEqual(combat_damage_range.range_max_for_class(a, 5), 104000.0)
        with self.assertRaises(KeyError):
            combat_damage_range.range_max_for_class(a, 6)
        b = self.records[89611]["properties"]
        self.assertEqual(combat_damage_range.range_max_for_class(b, 6), 208000.0)

    def test_observed_record_end_to_end(self):
        a = self.records[112911]["properties"]
        rmax = combat_damage_range.range_max_for_class(a, 2)
        family = combat_damage_range.kinetic_family_index(a["Arme"], rmax, 0.0)
        self.assertEqual(family, 20)


if __name__ == "__main__":
    unittest.main()
