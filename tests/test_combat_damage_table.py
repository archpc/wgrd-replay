"""Tests for the Phase 2b table-backed adapter (TGameplayArmeArmureContainer).

Evidence classes stay separate:

* SYNTHETIC documents are constructed JSON payloads. They test validation
  rules only and are not game data.
* ENGINE OBSERVATIONS are the hash-pinned private extraction of the NDF object
  at record offset ``0x104f2f7``. Tests that need it skip explicitly when the
  fixture is absent.

Only the table lookup is added. No Arme encoding, range, crit, accuracy or
falloff behaviour is asserted.
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
import combat_damage_table  # noqa: E402

_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")

TABLE = Path(os.environ.get(
    "WGRD_ARME_ARMURE_TABLE",
    Path.home() / ".hermes/artifacts/wgrd-replay"
    "/combat-damage-static-20261109/arme-armure-table.json"))
TABLE_SHA256 = "9004d7765a201027171eacad15d176010347e3471767654399202985c7d12834"


def f32(value):
    return _F32.unpack(_F32.pack(value))[0]


def bits(value):
    return "0x%08x" % _U32.unpack(_F32.pack(f32(value)))[0]


def valid_document():
    """SYNTHETIC: minimal shape accepted by the loader, all zeros."""
    rows = {str(family): [0.0] * 30 for family in range(65)}
    rows["2"] = [0.0] * 25
    return {
        "source": "synthetic",
        "packed_sha256": combat_damage_table.PACKED_SHA256,
        "decompressed_sha256": combat_damage_table.DECOMPRESSED_SHA256,
        "record_offset": combat_damage_table.RECORD_OFFSET,
        "class_id": combat_damage_table.CLASS_ID,
        "property_id": combat_damage_table.PROPERTY_ID,
        "rows": rows,
    }


def parse(document):
    payload = json.dumps(document).encode()
    expected = hashlib.sha256(payload).hexdigest()
    return combat_damage_table.parse_arme_armure_table(payload, expected_sha256=expected)


class TestSyntheticTableValidation(unittest.TestCase):
    """SYNTHETIC: loader rules, not engine data."""

    def test_valid_document_is_padded_to_35_columns(self):
        table = parse(valid_document())
        self.assertEqual(table.family_count, 65)
        self.assertEqual(table.armor_count, 35)
        self.assertTrue(all(len(row) == 35 for row in table.rows))

    def test_short_row_is_padded_with_zero(self):
        document = valid_document()
        document["rows"]["2"] = [1.5] * 25
        table = parse(document)
        self.assertEqual(table.lookup(2, 24), 1.5)
        self.assertEqual(table.lookup(2, 25), 0.0)
        self.assertEqual(table.lookup(2, 34), 0.0)

    def test_rows_30_to_34_are_zero_filled(self):
        document = valid_document()
        document["rows"]["8"] = [2.0] * 30
        table = parse(document)
        for armor in range(30, 35):
            self.assertEqual(bits(table.lookup(8, armor)), "0x00000000")

    def test_hash_mismatch_is_rejected(self):
        payload = json.dumps(valid_document()).encode()
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            combat_damage_table.parse_arme_armure_table(payload, expected_sha256="0" * 64)

    def test_missing_family_row_is_rejected(self):
        document = valid_document()
        del document["rows"]["64"]
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_extra_family_row_is_rejected(self):
        document = valid_document()
        document["rows"]["65"] = [0.0] * 30
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_wrong_row_length_is_rejected(self):
        for length in (24, 26, 29, 31, 36):
            with self.subTest(length=length):
                document = valid_document()
                document["rows"]["7"] = [0.0] * length
                with self.assertRaises(combat_damage_table.CombatDamageTableError):
                    parse(document)

    def test_non_numeric_element_is_rejected(self):
        document = valid_document()
        document["rows"]["8"][3] = "8.0"
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_integer_element_is_rejected(self):
        # The pinned extraction writes float literals; an int changes the type.
        document = valid_document()
        document["rows"]["8"][3] = 8
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_non_float32_element_is_rejected(self):
        document = valid_document()
        document["rows"]["8"][3] = 0.1  # not exactly representable in binary32
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_non_finite_element_is_rejected(self):
        for value in (float("nan"), float("inf")):
            with self.subTest(value=value):
                document = valid_document()
                document["rows"]["8"][3] = value
                with self.assertRaises(combat_damage_table.CombatDamageTableError):
                    parse(document)

    def test_record_metadata_mismatch_is_rejected(self):
        cases = [
            ("packed_sha256", "0" * 64),
            ("decompressed_sha256", "0" * 64),
            ("record_offset", "0x0"),
            ("class_id", 0),
            ("property_id", 0),
        ]
        for key, value in cases:
            with self.subTest(key=key):
                document = valid_document()
                document[key] = value
                with self.assertRaises(combat_damage_table.CombatDamageTableError):
                    parse(document)

    def test_missing_document_key_is_rejected(self):
        document = valid_document()
        del document["rows"]
        with self.assertRaises(combat_damage_table.CombatDamageTableError):
            parse(document)

    def test_invalid_indices_raise(self):
        table = parse(valid_document())
        for family, armor in ((-1, 0), (65, 0), (0, -1), (0, 35)):
            with self.subTest(family=family, armor=armor):
                with self.assertRaises(IndexError):
                    table.lookup(family, armor)
        for family, armor in (("0", 0), (0, "0"), (True, 0), (0, False), (1.0, 0)):
            with self.subTest(family=family, armor=armor):
                with self.assertRaises(TypeError):
                    table.lookup(family, armor)

    def test_missing_fixture_raises(self):
        with self.assertRaises(FileNotFoundError):
            combat_damage_table.load_arme_armure_table(
                Path("/nonexistent/arme-armure-table.json"))


class TestPrivateTableObservations(unittest.TestCase):
    """ENGINE OBSERVATION: the hash-pinned private extraction."""

    @classmethod
    def setUpClass(cls):
        if not TABLE.exists():
            raise unittest.SkipTest("private arme-armure table unavailable: " + str(TABLE))
        cls.table = combat_damage_table.load_arme_armure_table(TABLE)

    def test_dimensions_and_padding(self):
        self.assertEqual(self.table.family_count, 65)
        self.assertEqual(self.table.armor_count, 35)
        self.assertEqual(len(self.table.rows), 65)
        self.assertTrue(all(len(row) == 35 for row in self.table.rows))

    def test_extracted_cells_keep_exact_float32_values(self):
        cells = [
            ((8, 3), "0x41000000"),   # 8.0
            ((8, 4), "0x41000000"),
            ((8, 5), "0x40800000"),   # 4.0
            ((24, 3), "0x42200000"),  # 40.0
            ((64, 29), "0x40600000"),  # 3.5
            ((0, 2), "0x3f800000"),   # 1.0
        ]
        for (family, armor), expected in cells:
            with self.subTest(family=family, armor=armor):
                self.assertEqual(bits(self.table.lookup(family, armor)), expected)

    def test_fractional_cell_is_not_reinterpreted(self):
        # T[0][3] is the float32 nearest 0.1, not the double 0.1.
        value = self.table.lookup(0, 3)
        self.assertEqual(bits(value), "0x3dcccccd")
        self.assertEqual(value, 0.10000000149011612)

    def test_zero_filled_columns_30_to_34(self):
        for family in range(65):
            for armor in range(30, 35):
                with self.subTest(family=family, armor=armor):
                    self.assertEqual(bits(self.table.lookup(family, armor)), "0x00000000")

    def test_short_row_2_beyond_stored_values_is_zero(self):
        self.assertEqual(bits(self.table.lookup(2, 24)), "0x00000000")
        self.assertEqual(bits(self.table.lookup(2, 25)), "0x00000000")
        self.assertEqual(bits(self.table.lookup(2, 34)), "0x00000000")

    def test_record_metadata_is_pinned(self):
        self.assertEqual(self.table.packed_sha256, combat_damage_table.PACKED_SHA256)
        self.assertEqual(self.table.decompressed_sha256,
                         combat_damage_table.DECOMPRESSED_SHA256)
        self.assertEqual(self.table.record_offset, "0x104f2f7")
        self.assertEqual(self.table.class_id, 236)
        self.assertEqual(self.table.property_id, 1419)


class TestSyntheticEndToEndFromObservedCell(unittest.TestCase):
    """SYNTHETIC arithmetic through a verified table cell.

    H, P, K, C and F are constructed; only T comes from the observation.
    """

    @classmethod
    def setUpClass(cls):
        if not TABLE.exists():
            raise unittest.SkipTest("private arme-armure table unavailable: " + str(TABLE))
        cls.table = combat_damage_table.load_arme_armure_table(TABLE)

    def test_damage_amount_with_table_cell(self):
        amount = combat_damage.damage_amount(
            0.3, 0.7, self.table.lookup(8, 3), 1.1, 0.9, 1.3)
        self.assertEqual(bits(amount), "0x400a60d5")
        self.assertEqual(amount, 2.1621601581573486)

    def test_fractional_table_cell_rounds_after_each_multiply(self):
        amount = combat_damage.damage_amount(
            0.1, 0.3, self.table.lookup(24, 3), 1.0, 1.0, 1.0)
        self.assertEqual(bits(amount), "0x3f99999a")


if __name__ == "__main__":
    unittest.main()
