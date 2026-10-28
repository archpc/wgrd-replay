"""Synthetic fixtures, not redistributed replay bytes.

Each fixture is built by replay_bytes(): a 40-byte ESAV header (magic, container v1, total size,
SHA-224 over bytes 0x28.., then "rply"), followed by chunks. In these fixtures a chunk header is
16 bytes: 4-byte tag plus three big-endian uint32 (0, payload length, 0). Fixture payload structs
are little-endian. These tests pin the corpus CLI/inventory contract: provenance fields, error
isolation, the baseline comparison, and exit codes. They do NOT test the decoder's layouts.
"""
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest

from wgrd_corpus import inventory


def replay_bytes(block=b"\x18" + bytes(9), count=1, version="131544", extra=b""):
    """Build a minimal valid replay: one frame, one pact holding `block` declared as `count` commands.

    `extra` is appended after endt as raw trailing bytes. No current test passes it, so it is
    an unexercised knob; it is not a chunk and is not covered by the chunk-header description.
    Default block is a 10-byte 0x18 command; the default version 131544 yields
    layout_evidence "inferred_from_59638".
    """
    metadata = {"game": {"Version": version, "Map": "synthetic_map",
                         "GameMode": "1", "TimeLimit": "2400"},
                "player_9": {"PlayerName": "synthetic", "PlayerAlliance": "0"}}
    def chunk(tag, payload):
        return tag + struct.pack(">III", 0, len(payload), 0) + payload
    body = chunk(b"rply", json.dumps(metadata).encode())
    body += chunk(b"star", struct.pack("<II", 0, 0))
    body += chunk(b"pact", struct.pack("<IIIH", 0, 0, count, len(block)) + block)
    body += chunk(b"endt", struct.pack("<I", 0)) + extra
    return b"ESAV" + struct.pack(">II", 1, 40 + len(body)) + hashlib.sha224(body).digest() + body


class CorpusTests(unittest.TestCase):
    def test_inventory_preserves_provenance_and_separates_identity_time(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.wargamerpl2"
            data = replay_bytes()
            p.write_bytes(data)
            report = inventory([p])
            self.assertEqual(p.read_bytes(), data)
            self.assertEqual(report["totals"]["files"], 1)
            row = report["replays"][0]
            self.assertEqual(row["source_path"], str(p.resolve()))
            self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(row["game_version"], "131544")
            self.assertEqual(row["frames"], 1)
            self.assertEqual(row["declared_commands"], 1)
            self.assertEqual(row["decoded_opcodes"], {"0x18": 1})
            self.assertEqual(row["compatibility"], "structurally_compatible")
            self.assertEqual(row["layout_evidence"], "inferred_from_59638")
            self.assertEqual(row["observed_slots"], [0])
            self.assertIsNone(row["slot_to_player_identity"])
            self.assertIsNone(row["duration_seconds"])
            self.assertEqual(row["configured_time_limit_raw"], "2400")  # config, not match duration
            self.assertEqual(row["players"]["player_9"]["PlayerName"], "synthetic")
            self.assertEqual(row["timeline"]["events"], 1)


    # Non-object metadata must fail only that file; the neighbour in the same run stays valid.
    def test_nonobject_metadata_is_reported_without_losing_other_files(self):
        with tempfile.TemporaryDirectory() as d:
            bad, good = Path(d) / "bad.wargamerpl2", Path(d) / "good.wargamerpl2"
            body = b"rply" + struct.pack(">III", 0, 2, 0) + b"[]"
            bad.write_bytes(b"ESAV" + struct.pack(">II", 1, 40 + len(body)) + hashlib.sha224(body).digest() + body)
            good.write_bytes(replay_bytes())
            report = inventory([bad, good])
            self.assertEqual(report["totals"]["files"], 2)
            self.assertEqual(report["replays"][0]["compatibility"], "error")
            self.assertEqual(report["replays"][0]["errors"][0]["stage"], "header")
            self.assertEqual(report["replays"][1]["compatibility"], "structurally_compatible")

    # Non-finite JSON numbers (NaN, Infinity, 1e999) must not reach the output: the CLI output is
    # strict JSON (allow_nan=False). Each case runs both full and --headers-only modes.
    def test_nonfinite_metadata_is_isolated_and_cli_json_stays_valid(self):
        import subprocess
        import sys
        cli = Path(__file__).resolve().parents[1] / "wgrd_corpus.py"
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "good.wargamerpl2").write_bytes(replay_bytes())
            for value in ("NaN", "Infinity", "-Infinity", "1e999"):
                metadata = ('{"game":{"Version":"131544"},"player_9":{"x":' + value + '}}').encode()
                body = b"rply" + struct.pack(">III", 0, len(metadata), 0) + metadata
                (root / "bad.wargamerpl2").write_bytes(b"ESAV" + struct.pack(">II", 1, 40 + len(body)) + hashlib.sha224(body).digest() + body)
                for mode in ([], ["--headers-only"]):
                    result = subprocess.run([sys.executable, "-B", str(cli), str(root)] + mode,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    report = json.loads(result.stdout)
                    self.assertEqual(report["totals"]["files"], 2)
                    self.assertEqual(report["replays"][0]["compatibility"], "error")
                    self.assertEqual(report["replays"][0]["errors"][0]["stage"], "header")
                    self.assertIn(report["replays"][1]["compatibility"], ("structurally_compatible", "not_checked"))

    # Offsets asserted below: the 0x18 command is 10 bytes, so the stray 0xFF starts at command
    # offset 10; file_offset must point at that byte within the file. "malformed" is a block whose
    # 0x18 command is truncated. "digest" is a valid-looking file whose last byte is replaced
    # with 0x01, which breaks the SHA-224 check.
    def test_failures_keep_boundaries_without_scanning_tails(self):
        with tempfile.TemporaryDirectory() as d:
            cases = {"unknown": replay_bytes(b"\x18" + bytes(9) + b"\xff\x07", 2),
                     "malformed": replay_bytes(b"\x18\x00", 1),
                     "digest": replay_bytes()[:-1] + b"\x01"}
            paths = []
            for name, data in cases.items():
                p = Path(d) / (name + ".wargamerpl2")
                p.write_bytes(data)
                paths.append(p)
            rows = {r["filename"]: r for r in inventory(paths)["replays"]}
            unknown = rows["unknown.wargamerpl2"]
            self.assertEqual(unknown["compatibility"], "unsupported")
            self.assertEqual(unknown["decoded_opcodes"], {"0x18": 1})
            failure = unknown["decode_failures"][0]
            self.assertEqual(failure["command_offset"], 10)
            self.assertEqual(failure["next_byte_hex"], "ff")
            self.assertEqual(failure["undecoded_commands"], 1)
            self.assertEqual(cases["unknown"][failure["file_offset"]], 255)
            self.assertEqual(rows["malformed.wargamerpl2"]["decode_failures"][0]["status"], "malformed")
            self.assertEqual(rows["digest.wargamerpl2"]["compatibility"], "error")

    # Headers-only validates header/metadata and digest, but not the command stream. Zeroing
    # the SHA-224 field (bytes 12..40) must make the digest check report "error".
    # Note: inventory([p, p]) dedupes the path, so totals.files is 1.
    def test_headers_only_does_not_claim_command_compatibility(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "unknown.wargamerpl2"
            p.write_bytes(replay_bytes(b"\xff", 1))
            report = inventory([p, p], headers_only=True)
            self.assertEqual(report["totals"]["files"], 1)
            row = report["replays"][0]
            self.assertEqual(row["compatibility"], "not_checked")
            self.assertNotIn("frames", row)
            p.write_bytes(p.read_bytes()[:12] + bytes(28) + p.read_bytes()[40:])
            self.assertEqual(inventory([p], headers_only=True)["replays"][0]["compatibility"], "error")

    # Exit codes under test: empty directory -> 2 (usage), missing path -> 1 with a "read" error
    # row (not a crash), unsupported -> 1.
    def test_cli_empty_missing_and_unsupported_fail(self):
        import subprocess
        import sys
        cli = Path(__file__).resolve().parents[1] / "wgrd_corpus.py"
        with tempfile.TemporaryDirectory() as d:
            command = [sys.executable, "-B", str(cli)]
            self.assertEqual(subprocess.run(command + [d], capture_output=True).returncode, 2)
            missing = subprocess.run(command + [str(Path(d) / "missing")], capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertEqual(json.loads(missing.stdout)["replays"][0]["errors"][0]["stage"], "read")
            p = Path(d) / "unknown.wargamerpl2"
            p.write_bytes(replay_bytes(b"\xff", 1))
            result = subprocess.run(command + [str(p)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["totals"]["compatibility"], {"unsupported": 1})

    # Directory walk must match an uppercase ".WARGAMERPL2" suffix. The baseline round-trip is the
    # regression guard: the same tree must match its own output, and a changed build version must
    # make --expect fail with exit 1 while still emitting the new inventory on stdout.
    def test_cli_directory_and_regression_baseline(self):
        import subprocess
        import sys
        cli = Path(__file__).resolve().parents[1] / "wgrd_corpus.py"
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / "sample.WARGAMERPL2"
            p.write_bytes(replay_bytes())
            command = [sys.executable, "-B", str(cli), str(root)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue(first.stdout.strip(), "CLI must emit an inventory")
            report = json.loads(first.stdout)
            self.assertEqual(report["totals"]["files"], 1)
            baseline = root / "manifest.json"
            baseline.write_text(first.stdout)
            checked = subprocess.run(command + ["--expect", str(baseline)], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            p.write_bytes(replay_bytes(version="59638"))
            changed = subprocess.run(command + ["--expect", str(baseline)], capture_output=True, text=True)
            self.assertEqual(changed.returncode, 1)
            self.assertIn("baseline mismatch", changed.stderr)
            self.assertEqual(json.loads(changed.stdout)["totals"]["files"], 1)


if __name__ == "__main__":
    unittest.main()
