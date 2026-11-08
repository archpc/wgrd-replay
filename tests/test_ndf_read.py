"""Tests for the ndfbin reader used to recover shipped AI tunable values.

The parser is pinned against a synthetic ndfbin built here byte by byte (exact,
always runs) and against the retained 131544 blob when the artifact is present
(skipped, not failed, when absent). The synthetic fixture follows the layout
documented in scripts/ndf_read.py: EUG0/CNDF header, TOC0 footer, CLAS, PROP,
STRG, CHNK and OBJE sections.
"""
import os
import struct
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

import ndf_read  # noqa: E402

BLOB = Path(os.environ.get(
    "WGRD_NDF_BLOB",
    Path.home() / ".hermes/cache/scratch/ndf/gdconst-59638.bin"))


def u32(v):
    return struct.pack("<I", v)


def u64(v):
    return struct.pack("<Q", v)


def lp(s):
    b = s.encode("latin-1")
    return u32(len(b)) + b


def build_ndf(objects, classes, properties, strings=()):
    """Assemble a minimal ndfbin. Offsets are fixed by two passes."""
    header_size = 40  # EUG0+CNDF+flags+footer+header_size+size
    body = bytearray(b"\0" * header_size)

    def add(blob):
        off = len(body)
        body.extend(blob)
        return off, len(blob)

    clas = add(b"".join(lp(c) for c in classes))
    prop = add(b"".join(lp(n) + u32(cid) for n, cid in properties))
    strg = add(b"".join(lp(s) for s in strings))
    chnk = add(u32(0) + u32(len(objects)))

    obje = bytearray()
    for class_id, values in objects:
        obje += struct.pack("<i", class_id)
        for pid, tag, payload in values:
            obje += u32(pid) + u32(tag) + payload
        obje += u32(0xABABABAB)
    obj = add(bytes(obje))

    footer_off = len(body)
    entries = [("OBJE", obj), ("CLAS", clas), ("PROP", prop),
               ("STRG", strg), ("CHNK", chnk)]
    toc = bytearray(b"TOC0" + u32(len(entries)))
    for name, (off, size) in entries:
        toc += name.encode().ljust(8, b"\0") + u64(off) + u64(size)
    body.extend(toc)

    header = (b"EUG0" + u32(0) + b"CNDF" + u32(0) + u64(footer_off)
              + u64(header_size) + u64(len(body)))
    body[:header_size] = header
    return bytes(body)


class TestSyntheticNdf(unittest.TestCase):
    def setUp(self):
        data = build_ndf(
            objects=[(0, [
                (0, ndf_read.BOOL, bytes([1])),
                (1, ndf_read.INT32, struct.pack("<i", 500)),
                (2, ndf_read.LIST, u32(2) + u32(ndf_read.INT32) + u32(60)
                 + u32(ndf_read.INT32) + u32(80)),
            ])],
            classes=["TTunableConstante"],
            properties=[("IgnoreInvisibleUnit", 0), ("BonusIAMoneyForSkirmish", 0),
                        ("IncomeMultiplierInPercent", 0)],
            strings=["unused"],
        )
        self.ndf = ndf_read.NdfFile(data)

    def test_classes_and_properties(self):
        self.assertEqual([c.name for c in self.ndf.classes], ["TTunableConstante"])
        self.assertEqual(len(self.ndf.properties), 3)
        self.assertEqual(self.ndf.properties[0].name, "IgnoreInvisibleUnit")

    def test_values_decode_with_types(self):
        values = self.ndf.objects[0].values
        self.assertEqual(values[0].type, "bool")
        self.assertIs(values[0].value, True)
        self.assertEqual(values[1].type, "i32")
        self.assertEqual(values[1].value, 500)
        self.assertEqual(values[2].type, "list")
        self.assertEqual(values[2].value, [60, 80])

    def test_rejects_non_ndf(self):
        with self.assertRaises(ndf_read.NdfError):
            ndf_read.NdfFile(b"not an ndf at all" + b"\0" * 64)


@unittest.skipUnless(BLOB.is_file(), "retained 131544 tunables blob not present")
class TestShippedValues(unittest.TestCase):
    """Pin the shipped values this note cites."""

    @classmethod
    def setUpClass(cls):
        cls.ndf = ndf_read.NdfFile(BLOB.read_bytes())
        cls.props = {}
        for obj in cls.ndf.objects:
            for pid, value in obj.values.items():
                prop = cls.ndf.properties.get(pid)
                if prop:
                    cls.props[prop.name] = value.value

    def test_identity(self):
        names = [c.name for c in self.ndf.classes]
        self.assertIn("TTunableConstante", names)
        self.assertIn("TWargameTunableConstante", names)

    def test_information_levers(self):
        self.assertIs(self.props["IgnoreInvisibleUnit"], True)
        self.assertNotIn("InfluenceMapAlwaysKnowAllUnits", self.props)

    def test_economy_levers(self):
        self.assertEqual(self.props["BonusIAMoneyForSkirmish"], 500)
        self.assertEqual(self.props["StockDeviseSupplementaireFacile"], 72)
        self.assertNotIn("StockDeviseSupplementaireMoyen", self.props)
        self.assertNotIn("StockDeviseSupplementaireDifficile", self.props)

    def test_difficulty_scaling(self):
        self.assertEqual(self.props["MultiplicateurSeuilPinnedEtMortJoueurFacile"], 1.5)
        self.assertEqual(self.props["MultiplicateurSeuilPinnedEtMortIAFacile"], 0.75)
        self.assertEqual(self.props["MultiplicateurSeuilPinnedEtMortIADifficile"], 1.25)
        for suffix in ("Facile", "Moyen", "Difficile"):
            self.assertEqual(self.props[f"MultiplicateurDegatInfligeParLeJoueur_{suffix}"], 1.0)


if __name__ == "__main__":
    unittest.main()
