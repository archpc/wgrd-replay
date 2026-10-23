"""Tests against authentic sample bytes. Samples live outside Git.

Set WGRD_SAMPLES_DIR to override the default sample location. Missing or
altered samples FAIL (no skip), so a green run always means real bytes.
"""
import hashlib
import json
import os
import struct
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import wgrd_replay as w  # noqa: E402

SAMPLES = os.environ.get("WGRD_SAMPLES_DIR",
                         os.path.expanduser("~/.hermes/artifacts/wgrd-replay/samples/raw"))
MANIFEST = json.load(open(os.path.join(ROOT, "samples", "manifest.json")))

# Independently computed expectations (see REPLAY-RESEARCH.md, survey script).
EXPECTED = {
    "koppeltar-Sample1.wargamerpl2": dict(json_length=2412, payload_offset=0x9A4, frames=19033,
                                          pact=76132, slots=4, nonempty=3866, version="59638"),
    "koppeltar-Sample2.wargamerpl2": dict(json_length=2355, payload_offset=0x96B, frames=4513,
                                          pact=9026, slots=2, nonempty=127, version="510117427"),
    "koppeltar-Sample3.wargamerpl2": dict(json_length=10222, payload_offset=0x2826, frames=11165,
                                          pact=223300, slots=20, nonempty=6949, version="59638"),
}


def load(name):
    with open(os.path.join(SAMPLES, name), "rb") as f:
        return f.read()


class RealSamples(unittest.TestCase):
    def test_manifest_checksums(self):
        for s in MANIFEST["samples"]:
            b = load(s["file"])
            self.assertEqual(hashlib.sha256(b).hexdigest(), s["sha256"])
            self.assertEqual(len(b), s["size"])

    def test_header_and_framing(self):
        for name, e in EXPECTED.items():
            r = w.parse_replay(load(name))
            h, st = r["header"], r["stats"]
            self.assertEqual(h["json_length"], e["json_length"], name)
            self.assertEqual(h["payload_offset"], e["payload_offset"], name)
            self.assertEqual(h["game_version"], e["version"], name)
            self.assertTrue(h["digest_valid"], name)
            self.assertEqual(st["frames"], e["frames"], name)
            self.assertEqual(st["star"], st["endt"])
            self.assertEqual(st["pact"], e["pact"], name)
            self.assertEqual(st["slots_per_frame"], e["slots"], name)
            self.assertEqual(st["pact"], st["frames"] * st["slots_per_frame"])
            self.assertEqual(st["pact"] - st["empty_pact"], e["nonempty"], name)
            self.assertEqual(st["unknown_chunks"], 0)

    def test_first_star_bytes(self):
        b = load("koppeltar-Sample2.wargamerpl2")
        self.assertEqual(b[0x96B:0x97B].hex(), "73746172000000000000000800000000")

    def test_op08_known_record(self):
        # Sample1 frame 131 slot 2: chunk at 0x6985, block at 0x69a7.
        r = w.parse_replay(load("koppeltar-Sample1.wargamerpl2"))
        rec = [c for c in r["commands"] if c["frame"] == 131 and c["slot"] == 2][0]
        self.assertEqual(rec["offset"], 0x69A7 - 16 - 14)
        d = rec["decoded"]
        self.assertEqual(d["class"], "TNetworkActionLaunchFumigene")
        self.assertEqual(d["player_handle"], "0xc0000020")
        self.assertTrue(d["handle_matches_slot"])
        self.assertEqual(d["unknown16_hex"], "00" * 12 + "32000000")
        self.assertEqual(d["type_u32"], 3)
        self.assertEqual(d["text"], "leave your cv at base")
        self.assertEqual(d["text_length"], 21)
        # Byte boundaries per creator FUN_00b2fbc0: 1+4+16+12+4 then u16 len + text.
        blk = bytes.fromhex(rec["block_hex"])
        self.assertEqual(len(blk), 1 + 4 + 16 + 12 + 4 + 2 + 21)
        self.assertEqual(blk[:5].hex(), "08200000c0")
        self.assertEqual(blk[37:39].hex(), "1500")
        self.assertEqual(blk[39:], b"leave your cv at base")

    def test_op08_invariants_all_samples(self):
        n = 0
        types = {}
        for name in EXPECTED:
            for c in w.parse_replay(load(name))["commands"]:
                d = c.get("decoded")
                if not d:
                    continue
                n += 1
                self.assertEqual(d["class"], "TNetworkActionLaunchFumigene")
                self.assertTrue(d["handle_matches_slot"], (name, c["offset"]))
                self.assertEqual(d["unknown16_hex"], "00" * 12 + "32000000")
                self.assertEqual(d["text_length"] > 0, d["type_u32"] == 3)
                types[d["type_u32"]] = types.get(d["type_u32"], 0) + 1
        self.assertEqual(n, 39 + 2 + 185)
        self.assertEqual(types, {0: 69, 1: 50, 2: 27, 3: 80})

    def test_op08_layout_mismatch_not_decoded(self):
        r = w.parse_replay(load("koppeltar-Sample1.wargamerpl2"))
        rec = [c for c in r["commands"] if c["frame"] == 131 and c["slot"] == 2][0]
        blk = bytes.fromhex(rec["block_hex"])
        self.assertIsNone(w.decode_op08(blk[:-1], 2))
        self.assertIsNone(w.decode_op08(blk + b"\x00", 2))

    def test_first_opcodes_within_dispatcher_range(self):
        # Dispatcher FUN_00b24050 accepts opcodes 0x02..0x22 only.
        seen = set()
        for name in EXPECTED:
            for c in w.parse_replay(load(name))["commands"]:
                seen.add(c["first_opcode"])
                self.assertIsNotNone(c["first_opcode_class"], (name, c["offset"]))
        self.assertEqual(sorted(seen), [0x02, 0x04, 0x07, 0x08, 0x09, 0x0A, 0x0C,
                                        0x0D, 0x0E, 0x13, 0x17, 0x18])

    def test_deterministic_output(self):
        b = load("koppeltar-Sample2.wargamerpl2")
        a1 = json.dumps(w.parse_replay(b), sort_keys=True)
        a2 = json.dumps(w.parse_replay(b), sort_keys=True)
        self.assertEqual(a1, a2)


class Malformed(unittest.TestCase):
    def setUp(self):
        self.b = bytearray(load("koppeltar-Sample2.wargamerpl2"))

    def expect_error(self, b, msg):
        with self.assertRaisesRegex(w.ReplayFormatError, msg):
            w.parse_replay(bytes(b))

    def test_bad_magic(self):
        self.b[0:4] = b"XSAV"
        self.expect_error(self.b, "bad magic")

    def test_unsupported_version(self):
        struct.pack_into(">I", self.b, 4, 2)
        self.expect_error(self.b, "unsupported container version")

    def test_truncated(self):
        self.expect_error(self.b[:-1], "declared size")

    def test_chunk_length_overrun(self):
        struct.pack_into(">I", self.b, 0x96B + 8, 0x7FFFFFFF)
        self.expect_error(self.b, "overruns file")

    def test_frame_gap(self):
        struct.pack_into("<I", self.b, 0xA3F + 16, 5)  # second star frame index
        self.expect_error(self.b, "expected 1")

    def test_digest_mismatch_payload_byte(self):
        # Flip the last byte of Sample2's frame-0 slot-0 command block (pact at 0x983,
        # payload 64 bytes). Structure is unchanged; only the digest can catch it.
        last = 0x983 + 16 + 64 - 1
        self.b[last] ^= 0xFF
        self.expect_error(self.b, "SHA-224 mismatch")

    def test_digest_mismatch_reported_when_not_verifying(self):
        self.b[0x0C] ^= 0x01
        r = w.parse_replay(bytes(self.b), verify_digest=False)
        self.assertFalse(r["header"]["digest_valid"])

    def test_digest_covers_json(self):
        # Change one JSON byte (same length) without fixing the digest -> mismatch.
        i = self.b.find(b'"IsNetworkMode":"1"') + len('"IsNetworkMode":"')
        self.b[i] = ord("0")
        self.expect_error(self.b, "SHA-224 mismatch")

    def test_unknown_tag_preserved_not_dropped(self):
        b = bytes(self.b) + b"zzzz" + struct.pack(">III", 0, 2, 0) + b"\x01\x02"
        b = bytearray(b)
        struct.pack_into(">I", b, 8, len(b))
        b[0x0C:0x28] = hashlib.sha224(bytes(b[0x28:])).digest()
        r = w.parse_replay(bytes(b))
        self.assertTrue(r["header"]["digest_valid"])
        self.assertEqual(r["unknown_chunks"], [{"offset": len(b) - 18,
                                                "tag_hex": "7a7a7a7a", "payload_hex": "0102"}])


if __name__ == "__main__":
    unittest.main()
