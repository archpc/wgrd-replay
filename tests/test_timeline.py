"""Timeline boundaries/provenance; authentic samples remain outside Git."""
import contextlib
import hashlib
import io
import json
import math
import os
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wgrd_replay as w
import wgrd_timeline as t


def replay(frames, version="59638"):
    metadata = json.dumps({"game": {"Version": version}, "player_99": {"name": "unmapped"}}).encode()
    def chunk(tag, payload):
        return tag + struct.pack(">III", 0, len(payload), 0) + payload
    body = b"rply" + struct.pack(">III", 0, len(metadata), 0) + metadata
    for frame, slots in enumerate(frames):
        body += chunk(b"star", struct.pack("<II", frame, 0))
        for slot, (count, block) in enumerate(slots):
            body += chunk(b"pact", struct.pack("<IIIH", frame, slot, count, len(block)) + block)
        body += chunk(b"endt", struct.pack("<I", frame))
    return b"ESAV" + struct.pack(">II", 1, 40 + len(body)) + hashlib.sha224(body).digest() + body


def op08(text=b"hello", position=(1., 2., 3.)):
    return b"\x08" + struct.pack("<I", 0xc000001e) + bytes(16) + struct.pack("<fffIH", *position, 3, len(text)) + text


OP09 = b"\x09" + struct.pack("<I", 0xc000001e) + bytes(16) + struct.pack("<I", 7)
OPAQUE = b"\x0d" + struct.pack("<IIBII", 1, 0, 0, 0, 3) + b"abc"


class Timeline(unittest.TestCase):
    def test_order_provenance_and_verified_interpretations(self):
        b = replay([[(2, op08() + OP09), (1, OP09)], [(0, b""), (1, op08())]])
        parsed = w.parse_replay(b)
        out = t.build_timeline(parsed)
        events = out["events"]
        self.assertEqual(len(events), 4)
        self.assertEqual([e["command_order"] for e in events], list(range(4)))
        self.assertEqual([(e["frame"], e["frame_command_order"], e["player_slot"], e["slot_command_order"]) for e in events],
                         [(0, 0, 0, 0), (0, 1, 0, 1), (0, 2, 1, 0), (1, 0, 1, 0)])
        for e in events:
            s = e["source"]
            raw = bytes.fromhex(e["raw_hex"])
            self.assertEqual(raw, b[s["file_offset"]:s["file_offset"] + s["length"]])
            self.assertIsNone(e["player_identity"])
            self.assertEqual(e["interpretation"]["status"], "verified")
        self.assertEqual(events[0]["interpretation"]["action"], "create_map_marker")
        self.assertEqual(events[0]["interpretation"]["parameters"]["position_f32"], [1., 2., 3.])
        self.assertEqual(events[1]["interpretation"]["parameters"], {"marker_id_u32": 7})
        self.assertEqual(out["time_basis"]["frame_duration_seconds"], None)
        self.assertEqual(out["metadata"], parsed["metadata"])
        self.assertEqual(parsed, w.parse_replay(b))  # no mutation

    def test_opaque_and_unknown_single(self):
        out = t.build_timeline(w.parse_replay(replay([[(1, OPAQUE), (1, b"\x0babc")]])))
        opaque, unknown = out["events"]
        self.assertEqual(opaque["decode_status"], "opaque")
        self.assertEqual(opaque["parameters"]["serializer_payload_hex"], b"abc".hex())
        self.assertEqual(unknown["decode_status"], "unknown")
        self.assertEqual(unknown["raw_hex"], b"\x0babc".hex())
        self.assertTrue(unknown["source"]["boundary_known"])
        self.assertEqual(unknown["interpretation"]["status"], "unknown")

    def test_unknown_multi_preserves_span_without_inventing_boundaries(self):
        tail = b"\x0babc\x09junk"
        b = replay([[(3, OP09 + tail)]])
        out = t.build_timeline(w.parse_replay(b))
        known, first, second = out["events"]
        self.assertEqual(first["opcode"], 0x0B)
        self.assertIsNone(second["opcode"])
        for e in (first, second):
            self.assertEqual(e["decode_status"], "unresolved_boundary")
            self.assertIsNone(e["raw_hex"])
            self.assertFalse(e["source"]["boundary_known"])
            self.assertIsNone(e["source"]["length"])
            self.assertEqual(e["source"]["unresolved_span"], 0)
        span, = out["unresolved_spans"]
        self.assertEqual(span["raw_hex"], tail.hex())
        self.assertEqual(span["remaining_command_count"], 2)
        self.assertEqual(bytes.fromhex(known["raw_hex"] + span["raw_hex"]), OP09 + tail)

    def test_malformed_commands_fail_closed(self):
        for count, block in [(1, OP09[:-1]), (1, OP09 + b"x"),
                             (1, op08()[:-1]), (1, OPAQUE[:-1]), (2, OP09),
                             (1, b"\x07" + struct.pack("<I", 0xffffffff))]:
            with self.subTest(count=count, block=block.hex()):
                parsed = w.parse_replay(replay([[(count, block)]]))
                self.assertEqual(parsed["commands"][0]["command_decode"]["status"], "malformed")
                with self.assertRaises(w.ReplayFormatError):
                    t.build_timeline(parsed)

    def test_unknown_tail_cannot_have_more_commands_than_bytes(self):
        parsed = w.parse_replay(replay([[(3, OP09 + b"\x0b")]]))
        self.assertEqual(parsed["commands"][0]["command_decode"]["status"], "unresolved")
        with self.assertRaisesRegex(w.ReplayFormatError, "remaining command count exceeds opcode bytes"):
            t.build_timeline(parsed)

    def test_wrong_build_inference_and_nonfinite_raw_preservation(self):
        b = replay([[(1, op08(position=(math.inf, math.nan, 3.))) ]], version="other")
        out = t.build_timeline(w.parse_replay(b))
        e, = out["events"]
        self.assertEqual(e["interpretation"]["status"], "inferred")
        self.assertIsNone(e["interpretation"]["parameters"]["position_f32"])
        self.assertIn("nonfinite", e["parameters"]["position_f32"][0])
        self.assertEqual(e["raw_hex"], op08(position=(math.inf, math.nan, 3.)).hex())
        json.dumps(out, allow_nan=False)

    def test_digest_enforced_before_timeline(self):
        b = bytearray(replay([[(1, OP09)]]))
        b[-21] ^= 1  # last action byte, preceding endt; container remains valid
        with self.assertRaisesRegex(w.ReplayFormatError, "SHA-224 mismatch"):
            w.parse_replay(b)

    def test_cli_default_unchanged_and_timeline_summary(self):
        import tempfile
        with tempfile.NamedTemporaryFile() as f:
            b = replay([[(1, OP09)]])
            f.write(b)
            f.flush()
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(w.main([f.name]), 0)
            self.assertEqual(json.loads(stdout.getvalue()), w.parse_replay(b))
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(w.main([f.name, "--timeline", "--summary"]), 0)
            out = json.loads(stdout.getvalue())
            self.assertNotIn("events", out)
            self.assertEqual(out["stats"]["events"], 1)

    def test_parser_cli_emits_strict_json_for_nonfinite_floats(self):
        import tempfile
        with tempfile.NamedTemporaryFile() as f:
            f.write(replay([[(1, op08(position=(math.inf, math.nan, 3.)))]]))
            f.flush()
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(w.main([f.name]), 0)
            out = json.loads(stdout.getvalue(), parse_constant=lambda s: self.fail(s))
            self.assertEqual(out['commands'][0]['decoded']['position_f32'][:2],
                             [{'nonfinite': '+Infinity'}, {'nonfinite': 'NaN'}])

    def test_cli_malformed_timeline_reports_error(self):
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile() as f:
            f.write(replay([[(1, OP09[:-1])]]))
            f.flush()
            result = subprocess.run([sys.executable, w.__file__, f.name, "--timeline"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("ReplayFormatError: timeline: malformed", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


class AuthenticTimeline(unittest.TestCase):
    def test_all_samples_count_bytes_order_and_semantic_coverage(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "samples/manifest.json").read_text())
        # NOTE: no skip guard. Absent samples raise FileNotFoundError (error, not skip); see AGENTS.md section 9.
        samples = Path(os.environ.get("WGRD_SAMPLES_DIR", str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))
        expected = [(4162, 769, 3350, 233, 0), (132, 0, 0, 24, 0), (7271, 1851, 5313, 257, 0)]
        for sample, (count, verified, partial, opaque, unknown) in zip(manifest["samples"], expected):
            b = (samples / sample["file"]).read_bytes()
            self.assertEqual(hashlib.sha256(b).hexdigest(), sample["sha256"])
            parsed = w.parse_replay(b)
            out = t.build_timeline(parsed)
            self.assertEqual(len(out["events"]), count)
            self.assertEqual(out["stats"]["interpretations"].get("verified", 0), verified)
            self.assertEqual(out["stats"]["interpretations"].get("partial", 0), partial)
            self.assertEqual(out["stats"]["decode_status"].get("opaque", 0), opaque)
            self.assertEqual(out["stats"]["decode_status"].get("unknown", 0), unknown)
            production = [e for e in out['events'] if e['opcode'] == 0x0d]
            self.assertEqual(len(production), opaque)
            self.assertTrue(all(e['interpretation']['payload_layout_status'] == 'complete'
                                for e in production))
            self.assertTrue(all(e['interpretation']['execution_outcome'] == 'unknown'
                                for e in production))
            self.assertEqual(out["unresolved_spans"], [])
            # Independent container walk: each declared command represented, each byte once.
            header, _ = w.parse_header(b)
            by_chunk = {}
            for event in out["events"]:
                by_chunk.setdefault(event["source"]["chunk_offset"], []).append(event)
            total = 0
            for off, tag, p in w.iter_chunks(b, header["payload_offset"]):
                if tag != b"pact":
                    continue
                frame, slot, n, length = struct.unpack_from("<IIIH", p)
                total += n
                events = by_chunk.get(off, [])
                self.assertEqual(len(events), n)
                self.assertEqual(b"".join(bytes.fromhex(e["raw_hex"]) for e in events), p[14:])
                for i, e in enumerate(events):
                    self.assertEqual((e["frame"], e["player_slot"], e["slot_command_order"]), (frame, slot, i))
                    s = e["source"]
                    self.assertEqual(bytes.fromhex(e["raw_hex"]), b[s["file_offset"]:s["file_offset"]+s["length"]])
            self.assertEqual(total, count)
            self.assertEqual([(e["frame"], e["frame_command_order"]) for e in out["events"]],
                             sorted((e["frame"], e["frame_command_order"]) for e in out["events"]))
            json.dumps(out, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
