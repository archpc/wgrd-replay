"""Opcode 0x18 DeactivateSupply obj+0x04 registry-key check: regression tests for
research/op18_reference_keys.py.

Corpus tests pin the counts in research/OP18-REFERENCE-KEYS.md (build 59638) and
skip when the authentic samples are not cached (WGRD_SAMPLES_DIR, default
~/.hermes/artifacts/wgrd-replay/samples/raw). The negative control never touches
the sample files: it patches wgrd_replay.parse_replay with a synthetic structure.
"""
import importlib.util
import os
import struct
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("op18_reference_keys", ROOT / "research" / "op18_reference_keys.py")
op18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(op18)

SAMPLES = Path(os.environ.get("WGRD_SAMPLES_DIR",
                              str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))


def _pact_0x18(frame, slot, key):
    block_hex = (bytes([0x18]) + struct.pack("<I", key)).hex()
    return {"frame": frame, "slot": slot, "count": 1, "block_hex": block_hex}


def _pact_0x07(frame, slot, keys):
    items = b"".join(struct.pack("<I", k) + bytes(16) for k in keys)  # 20-byte entries: key + GUID
    return {"frame": frame, "slot": slot, "command_decode": {"commands": [
        {"opcode": 0x07, "fields": {"obj_04_array": {"items_hex": items.hex()}}}]}}


class CorpusAssertions(unittest.TestCase):
    EXPECTED = {
        "koppeltar-Sample1.wargamerpl2": {"rows18": 19, "distinct18": 7, "matched": 7, "missing": [],
                                          "same_slot_rows": 19},
        "koppeltar-Sample3.wargamerpl2": {"rows18": 25, "distinct18": 11, "matched": 11, "missing": [],
                                          "same_slot_rows": 23},
        "koppeltar-Sample2.wargamerpl2": {"rows18": 0},
    }

    def setUp(self):
        self.paths = {n: SAMPLES / n for n in self.EXPECTED}
        if not all(p.exists() for p in self.paths.values()):
            self.skipTest("authentic samples not cached; set WGRD_SAMPLES_DIR")

    def test_corpus_counts(self):
        for name, want in self.EXPECTED.items():
            r = op18.analyse(str(self.paths[name]))
            for k, v in want.items():
                self.assertEqual(r[k], v, (name, k))

    def test_chance_baseline_sample1(self):
        r = op18.analyse(str(self.paths["koppeltar-Sample1.wargamerpl2"]))
        self.assertLess(r["chance_all_match"], 1e-6)


class NegativeControl(unittest.TestCase):
    def test_unmatched_0x18_key_is_reported_missing(self):
        fake_rep = {"commands": [
            _pact_0x07(10, 0, [0x11111111, 0x22222222]),
            _pact_0x18(20, 0, 0x11111111),   # present as a 0x07 key
            _pact_0x18(30, 1, 0xFFFFFFFF),   # absent from every 0x07 array
        ]}
        with tempfile.NamedTemporaryFile(suffix=".wargamerpl2", dir=os.environ.get("TMPDIR")) as f:
            f.write(b"synthetic")
            f.flush()
            with mock.patch.object(op18.w, "parse_replay", return_value=fake_rep):
                r = op18.analyse(f.name)
        self.assertEqual(r["missing"], [0xFFFFFFFF])
        self.assertEqual(r["rows18"], 2)
        self.assertEqual(r["distinct18"], 2)
        self.assertEqual(r["matched"], 1)


if __name__ == "__main__":
    unittest.main()
