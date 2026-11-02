"""Evidence-backed AAR extraction tests; authentic trace stays outside Git."""

import hashlib
import importlib.util
import io
import json
import math
import os
import copy
from pathlib import Path
import struct
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "aar_events", ROOT / "instrumentation" / "aar_events.py"
)
aar = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aar)

TRACE = Path(os.environ.get(
    "WGRD_AAR_TRACE",
    Path.home() / ".hermes" / "artifacts" / "wgrd-replay" / "combat-20261101"
    / "damage-state-combat-02.jsonl",
))
CLASSIFIED = Path(os.environ.get(
    "WGRD_AAR_CLASSIFIED",
    Path.home() / ".hermes" / "artifacts" / "wgrd-replay" / "combat-20261101"
    / "battle-timeline-classified.json",
))
RUNTIME_TRACE = Path(os.environ.get(
    "WGRD_AAR_RUNTIME_TRACE",
    Path.home() / ".hermes" / "artifacts" / "wgrd-replay" / "aar-20261102T050816Z"
    / "wgrd-aar-combat-20261102-01.jsonl",
))
RUNTIME_INDEX = Path(os.environ.get(
    "WGRD_AAR_RUNTIME_INDEX",
    Path.home() / ".hermes" / "artifacts" / "wgrd-replay" / "aar-20261102T050816Z"
    / "units" / "unit-index-131544.json",
))
V3_ROOT = Path.home() / ".hermes" / "artifacts" / "wgrd-replay" / "aar-v3-20261102T082918Z"
RUNTIME_V3_TRACE = Path(os.environ.get("WGRD_AAR_V3_TRACE",
                                       V3_ROOT / "native-v3b-replay.jsonl"))
RUNTIME_V3_INFLIGHT = Path(os.environ.get("WGRD_AAR_V3_INFLIGHT",
                                          V3_ROOT / "native-v3b-inflight-snapshot.jsonl"))
FAKE_SHA = "0" * 64
_RUNTIME_CACHE = {}


def _float_hex(value):
    return struct.pack("<f", value).hex()


def _float_bits(value):
    return struct.unpack("<I", struct.pack("<f", value))[0]


def _read(module, offset, value_hex, phase):
    return {
        "source": "ecx", "phase": phase, "offset": offset, "size": 4,
        "address": "0x%08x" % (module + offset), "indirect": False, "chain": [],
        "target": None, "result": {"ok": True, "hex": value_hex},
    }


def _event(module=0x401e78e0, handle=31, mode=1, arg0=100.0, ordinal=1,
           call_id=1000, parent_recorded=False, before190=0.0, after190=100.0,
           before19c=0.0, after19c=0.0, second=0.0):
    if mode == 2:
        before190 = after190 = before190
        after19c = 10.0
    timestamp = "2026-11-02T01:00:%06.3fZ" % second
    enter = {
        "event": "enter", "hook": aar.IMPACT_HOOK, "call_id": call_id,
        "parent_call_id": call_id - 1, "parent_recorded": parent_recorded,
        "stale_frames_discarded": 0, "stack_pointer": "0xd000000",
        "ordinal": ordinal, "thread_id": 7, "return_address": aar.RETURN_ADDRESS,
        "ecx": "0x%08x" % module, "edx": "0x%08x" % (module + 0x100),
        "args": ["0x%08x" % _float_bits(arg0), "0x0", "0x0",
                 "0x%08x" % (module + 0x10), "0x%x" % mode],
        "reads": [
            _read(module, 8, struct.pack("<I", handle).hex(), "enter"),
            _read(module, 400, _float_hex(before190), "enter"),
            _read(module, 412, _float_hex(before19c), "enter"),
            _read(module, 416, _float_hex(0.0), "enter"),
        ],
        "timestamp_utc": timestamp,
    }
    leave = {
        "event": "leave", "hook": aar.IMPACT_HOOK, "call_id": call_id,
        "thread_id": 7, "stack_match": True, "retval": "0xd000100",
        "reads": [
            _read(module, 400, _float_hex(after190), "leave"),
            _read(module, 412, _float_hex(after19c), "leave"),
            _read(module, 416, _float_hex(0.0), "leave"),
        ],
        "timestamp_utc": timestamp,
    }
    return enter, leave


def make_rows(events):
    start = {
        "event": "start", "timestamp_utc": "2026-11-02T01:00:00.000Z",
        "revision": aar.REVISION, "sha256": aar.EXECUTABLE_SHA256,
        "hooks": [{
            "name": aar.IMPACT_HOOK, "va": aar.IMPACT_ADDRESS, "args": 5,
            "sample_every": 1,
            "reads": [
                {"source": "ecx", "offset": 8, "size": 4, "phase": "enter"},
                {"source": "ecx", "offset": 400, "size": 4, "phase": "both"},
                {"source": "ecx", "offset": 412, "size": 4, "phase": "both"},
                {"source": "ecx", "offset": 416, "size": 4, "phase": "both"},
            ],
        }],
    }
    identity = {
        "event": "identity_verified", "timestamp_utc": "2026-11-02T01:00:00.001Z",
        "module": {
            "name": "wargame3.exe", "arch": "ia32", "pointer_size": 4,
            "base": "0x400000", "size": aar.IMAGE_SIZE,
            "entries": [{"name": aar.IMPACT_HOOK, "address": aar.IMPACT_ADDRESS,
                         "executable": True}],
        },
    }
    summary = {
        "event": "summary", "timestamp_utc": "2026-11-02T01:00:30.000Z",
        "counts": {aar.IMPACT_HOOK: len(events)},
        "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
        "stack_mismatches": 0, "outstanding_threads": 0,
        "gate_read_failures": 0, "gate_ambiguities": 0,
    }
    rows = [start, identity,
            {"event": "hooks_installed", "timestamp_utc": "2026-11-02T01:00:00.002Z"},
            ]
    call_id = 1000
    for index, kwargs in enumerate(events, 1):
        kwargs = dict(kwargs, ordinal=kwargs.get("ordinal", index),
                      call_id=kwargs.get("call_id", call_id))
        call_id += 2
        rows.extend(_event(**kwargs))
    rows.extend([
        summary,
        {"event": "detached", "timestamp_utc": "2026-11-02T01:00:30.001Z"},
        {"event": "end", "timestamp_utc": "2026-11-02T01:00:30.002Z",
         "cleanup_errors": 0},
    ])
    return rows


def extract(events, **kwargs):
    rows = make_rows(events)
    return aar.extract(rows, "synthetic.jsonl", FAKE_SHA, len(rows), **kwargs)


def extract_rows(rows, **kwargs):
    return aar.extract(rows, "synthetic.jsonl", FAKE_SHA, len(rows), **kwargs)


def run_main(arguments):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return aar.main(arguments)


def classified_for(manifest):
    events = []
    for event in manifest["events"]:
        events.append({
            "ordinal": event["ordinal"],
            "call_id": event["call"]["call_id"],
            "thread_id": event["call"]["thread_id"],
            "source": {"enter_line": event["source"]["enter_line"],
                       "leave_line": event["source"]["leave_line"]},
            "runtime_module_address": event["module"]["address"],
            "runtime_handle_raw_u32": event["module"]["raw_handle_u32"],
            "kind": event["kind"],
            "changed_fields": event["changed_fields"],
            "arg0_float32": event["arg0_float32"],
            "observed_delta": event["observed_delta"],
            "frame": None, "simulation_time": None,
            "unit_identity": None, "player_identity": None,
            "before": {field: {"float32": event["fields"][field]["before"]}
                       for field in ("0x190", "0x19c", "0x1a0")},
            "after": {field: {"float32": event["fields"][field]["after"]}
                      for field in ("0x190", "0x19c", "0x1a0")},
        })
    return {
        "trace_sha256": manifest["source"]["sha256"],
        "executable_sha256": aar.EXECUTABLE_SHA256,
        "events": events,
    }


class ReconstructionTests(unittest.TestCase):
    def test_recomputes_transitions_and_keeps_identity_time_kill_unknown(self):
        manifest = extract([
            {"arg0": 117.6766, "after190": 117.6766},
            {"module": 0x401eadd0, "handle": 33, "mode": 2, "arg0": 28.0,
             "after190": 0.0},
        ])
        self.assertEqual([event["kind"] for event in manifest["events"]],
                         ["suppression_increase", "physical_damage_increase"])
        self.assertEqual(manifest["events"][1]["fields"]["0x19c"]["after"], 10.0)
        self.assertEqual(manifest["events"][1]["observed_delta"], 10.0)
        for event in manifest["events"]:
            self.assertIsNone(event["identity"]["unit"])
            self.assertIsNone(event["identity"]["player"])
            self.assertIsNone(event["time"]["frame"])
            self.assertIsNone(event["time"]["simulation_time"])
            self.assertIsNone(event["time"]["game_time"])
            self.assertIsNone(event["kill"]["outcome"])
            self.assertFalse(event["kill"]["destruction_observed"])
            self.assertFalse(event["module"]["image_membership"]["inside_image"])
        self.assertEqual([module["event_count"] for module in manifest["modules"]], [1, 1])
        self.assertEqual(manifest["events"][0]["time"]["relative_wallclock_seconds"], 0.0)

    def test_rejects_missing_pair(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        rows = [row for row in rows if not (row.get("event") == "leave")]
        with self.assertRaisesRegex(aar.AarTraceError, "missing impact pair"):
            extract_rows(rows)

    def test_rejects_suppressed_events(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        [row for row in rows if row.get("event") == "summary"][0]["suppressed"] = 1
        with self.assertRaisesRegex(aar.AarTraceError, "summary failure:suppressed"):
            extract_rows(rows)

    def test_rejects_sampled_impact_hook(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        [row for row in rows if row.get("event") == "start"][0]["hooks"][0]["sample_every"] = 61
        with self.assertRaisesRegex(aar.AarTraceError, "sampling failure"):
            extract_rows(rows)

    def test_rejects_failed_read(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        enter = [row for row in rows if row.get("event") == "enter"][0]
        enter["reads"][1]["result"] = {"ok": False, "error": "unreadable"}
        with self.assertRaisesRegex(aar.AarTraceError, "read failure"):
            extract_rows(rows)

    def test_rejects_mode_and_changed_field_mismatch(self):
        rows = make_rows([{"mode": 1, "arg0": 10.0, "after190": 0.0,
                           "after19c": 10.0}])
        with self.assertRaisesRegex(aar.AarTraceError, "do not match mode"):
            extract_rows(rows)

    def test_rejects_effective_damage_above_input(self):
        rows = make_rows([{"mode": 2, "arg0": 5.0, "after190": 0.0,
                           "after19c": 10.0}])
        with self.assertRaisesRegex(aar.AarTraceError, "exceeds input"):
            extract_rows(rows)

    def test_rejects_noncontiguous_ordinals(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0},
                          {"arg0": 10.0, "after190": 10.0, "ordinal": 3}])
        with self.assertRaisesRegex(aar.AarTraceError, "not contiguous"):
            extract_rows(rows)

    def test_classification_crosscheck_enumerates_every_event(self):
        manifest = extract([{"arg0": 10.0, "after190": 10.0},
                            {"module": 0x401eadd0, "mode": 2, "arg0": 28.0,
                             "after190": 0.0}])
        classified = classified_for(manifest)
        checked = extract_rows(
            make_rows([{"arg0": 10.0, "after190": 10.0},
                       {"module": 0x401eadd0, "mode": 2, "arg0": 28.0,
                        "after190": 0.0}]),
            classified=classified, classified_sha256="c" * 64,
        )
        self.assertEqual(checked["integrity"]["classification"]["matched_events"], 2)
        self.assertEqual(checked["integrity"]["classification"]["status"], "match")

    def test_classification_crosscheck_rejects_invented_kind(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        manifest = extract_rows(rows)
        classified = classified_for(manifest)
        classified["events"][0]["kind"] = "kill"
        with self.assertRaisesRegex(aar.AarTraceError, "differs in: kind"):
            extract_rows(rows, classified=classified, classified_sha256="c" * 64)

    def test_exclusive_create_preserves_existing_output(self):
        manifest = extract([{"arg0": 10.0, "after190": 10.0}])
        with tempfile.TemporaryDirectory() as directory:
            first = aar.write_outputs(manifest, directory)
            before = {path.name: path.read_bytes() for path in first}
            with self.assertRaisesRegex(aar.AarTraceError, "refusing to overwrite"):
                aar.write_outputs(manifest, directory)
            self.assertEqual({path.name: path.read_bytes() for path in first}, before)

    def test_chronology_lists_every_event_with_unknowns(self):
        manifest = extract([{"arg0": 10.0, "after190": 10.0},
                            {"module": 0x401eadd0, "mode": 2, "arg0": 28.0,
                             "after190": 0.0}])
        text = aar.render_chronology(manifest)
        self.assertIn(manifest["source"]["sha256"], text)
        for event in manifest["events"]:
            self.assertIn(event["source"]["line_ref"], text)
            self.assertIn("unit=UNKNOWN", text)
            self.assertIn("kill=UNKNOWN", text)
        self.assertIn("H3 (three kills from three transitions): rejected", text)

    def test_module_below_image_base_exits_2_with_documented_error(self):
        for events in ([{"module": 0x1000, "arg0": 10.0, "after190": 10.0}],
                       [{"module": 0x1000, "arg0": 10.0, "after190": 10.0},
                        {"module": 0x401e78e0, "arg0": 10.0, "after190": 10.0}]):
            with self.assertRaisesRegex(aar.AarTraceError, "below image base"):
                extract_rows(make_rows(events))
        rows = make_rows([{"module": 0x1000, "arg0": 10.0, "after190": 10.0}])
        data = ("\n".join(json.dumps(row) for row in rows) + "\n").encode()
        digest = hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.jsonl"
            trace.write_bytes(data)
            output = Path(directory) / "events"
            stderr = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                code = aar.main([str(trace), "--out", str(output),
                                 "--expect-sha256", digest])
            self.assertEqual(code, 2)
            self.assertTrue(stderr.getvalue().startswith("aar_events: "))
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertNotIn("TypeError", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_in_image_module_correction_is_computed_from_observation(self):
        inside = extract([{"module": 0x401000, "arg0": 10.0, "after190": 10.0}])
        correction = inside["corrections"][0]
        self.assertTrue(inside["modules"][0]["image_membership"]["inside_image"])
        self.assertEqual(correction["observed"]["inside_image"], 1)
        self.assertEqual(correction["observed"]["outside_image"], 0)
        self.assertEqual(correction["status"], "confirmed_by_arithmetic")
        self.assertNotIn("far outside", correction["detail"])
        self.assertNotIn("at least", correction["detail"])
        outside = extract([{"module": 0x401e78e0, "arg0": 10.0, "after190": 10.0}])
        correction = outside["corrections"][0]
        self.assertEqual(correction["status"], "rejected_by_arithmetic")
        self.assertEqual(correction["observed"]["inside_image"], 0)
        self.assertEqual(correction["observed"]["outside_image"], 1)
        self.assertIn("outside", correction["detail"])
        self.assertEqual(correction["observed"]["minimum_offset_bytes"], 1071544544)
        mixed = extract([{"module": 0x401000, "arg0": 10.0, "after190": 10.0},
                         {"module": 0x401e78e0, "arg0": 10.0, "after190": 10.0}])
        correction = mixed["corrections"][0]
        self.assertEqual(correction["status"], "partially_confirmed_by_arithmetic")
        self.assertEqual(correction["observed"]["inside_image"], 1)
        self.assertEqual(correction["observed"]["outside_image"], 1)
        self.assertIn("1 of 2", correction["detail"])

    def test_timing_reports_no_quantum_seconds_or_step_prediction(self):
        manifest = extract([
            {"arg0": 300.0, "after190": 28.2, "second": 0.0},
            {"arg0": 300.0, "before190": 27.6, "after190": 300.0, "second": 23.171},
        ])
        timing = manifest["timing"]
        observation = timing["decay_observations"][0]
        self.assertAlmostEqual(observation["observed_loss"], 0.6, places=5)
        self.assertNotIn("quanta", observation)
        self.assertNotIn("wallclock_seconds_per_quantum", observation)
        self.assertEqual(
            [fit["divisor"] for fit in observation["divisor_fits"] if fit["integral"]],
            [0.6, 0.3, 0.2, 0.1, 0.05])
        summary = timing["decay_summary"]
        self.assertIsNone(summary["unique_divisor"])
        self.assertEqual(summary["divisor_fit_counts"],
                         {"0.6": 1, "0.3": 1, "0.2": 1, "0.1": 1, "0.05": 1})
        text = json.dumps(manifest, allow_nan=False)
        self.assertNotIn("seconds_per_quantum", text)
        self.assertNotIn("quanta/s", text)
        self.assertNotIn("9.38", text)
        reason = timing["hypotheses"][0]["reason"]
        self.assertIn("not quantized on a resolvable time base", reason)
        self.assertIn("no engine step count", reason)
        self.assertEqual(timing["hypotheses"][0]["status"], "not_supported_by_trace")

    def test_image_membership_arithmetic_rejects_the_old_claim(self):
        module = aar.image_membership(0x401e78e0)
        self.assertFalse(module["inside_image"])
        self.assertEqual(module["offset_bytes"], 1071544544)
        self.assertEqual(aar.image_membership(0xC95200)["inside_image"], True)
        manifest = extract([{"arg0": 10.0, "after190": 10.0}])
        correction = manifest["corrections"][0]
        self.assertEqual(correction["status"], "rejected_by_arithmetic")
        self.assertEqual(correction["observed"]["inside_image"], 0)

    def test_load_trace_rejects_hash_mismatch_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.jsonl"
            path.write_text("{not json}\n", encoding="utf-8")
            with self.assertRaisesRegex(aar.AarTraceError, "sha256 mismatch"):
                aar.load_trace(path, FAKE_SHA)

    def test_cli_fails_closed_then_exclusively_creates(self):
        rows = make_rows([{"arg0": 10.0, "after190": 10.0}])
        data = ("\n".join(json.dumps(row) for row in rows) + "\n").encode()
        digest = hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.jsonl"
            trace.write_bytes(data)
            output = Path(directory) / "events"
            self.assertEqual(run_main([str(trace), "--out", str(output),
                                       "--expect-sha256", "f" * 64]), 2)
            self.assertFalse(output.exists())
            self.assertEqual(run_main([str(trace), "--out", str(output),
                                       "--expect-sha256", digest]), 0)
            self.assertTrue((output / "events.json").exists())
            self.assertEqual(run_main([str(trace), "--out", str(output),
                                       "--expect-sha256", digest]), 2)


class AuthenticTraceTests(unittest.TestCase):
    """Integration checks against the hash-pinned trace; skip when absent."""

    def test_authentic_trace_recomputation_and_classified_crosscheck(self):
        if not TRACE.exists() or not CLASSIFIED.exists():
            self.skipTest("authentic damage trace/classified timeline unavailable")
        manifest = aar.extract_file(
            TRACE, aar.TRACE_SHA256, CLASSIFIED, aar.CLASSIFIED_SHA256)
        events = manifest["events"]
        self.assertEqual(len(events), 28)
        self.assertEqual(sum(event["mode"] == 1 for event in events), 25)
        self.assertEqual(sum(event["mode"] == 2 for event in events), 3)
        self.assertEqual([module["raw_handle_u32"] for module in manifest["modules"]],
                         [31, 32, 33, 34, 39, 40])
        self.assertEqual(manifest["modules"][3]["suppression"]["observed_peak"], 800.0)
        self.assertEqual(manifest["integrity"]["classification"]["matched_events"], 28)
        self.assertEqual(manifest["integrity"]["parent_unrecorded"], 27)
        self.assertEqual(manifest["timing"]["frame"], None)
        self.assertEqual(manifest["timing"]["simulation_time"], None)
        hypotheses = {item["id"]: item["status"] for item in manifest["timing"]["hypotheses"]}
        self.assertEqual(hypotheses, {
            "H1_5.01_fps": "not_supported_by_trace",
            "H2_battle_start_frame_2914": "not_supported_by_trace",
            "H3_three_kills_from_three_transitions": "rejected",
        })
        correction = manifest["corrections"][0]
        self.assertEqual(correction["status"], "rejected_by_arithmetic")
        self.assertEqual(correction["observed"]["inside_image"], 0)
        self.assertEqual(correction["observed"]["outside_image"], 6)
        self.assertEqual(correction["observed"]["minimum_offset_bytes"], 1071544544)
        decay = manifest["timing"]["decay_summary"]
        self.assertEqual(decay["declines"], 19)
        self.assertIsNone(decay["unique_divisor"])
        self.assertEqual(decay["divisor_fit_counts"],
                         {"0.6": 19, "0.3": 19, "0.2": 19, "0.1": 19, "0.05": 19})
        self.assertNotIn("quanta/s", manifest["timing"]["hypotheses"][0]["reason"])
        self.assertTrue(all(not event["module"]["image_membership"]["inside_image"]
                            for event in events))
        self.assertTrue(all(event["identity"]["unit"] is None for event in events))
        self.assertTrue(all(event["kill"]["outcome"] is None for event in events))
        refs = [event["source"]["line_ref"] for event in events]
        self.assertEqual(len(set(refs)), 28)
        for event in events:
            self.assertLess(event["source"]["enter_line"], event["source"]["leave_line"])
            self.assertEqual(event["source"]["trace_sha256"], aar.TRACE_SHA256)
        chronology = aar.render_chronology(manifest)
        for ref in refs:
            self.assertIn(ref, chronology)
        self.assertEqual(
            hashlib.sha256(TRACE.read_bytes()).hexdigest(), aar.TRACE_SHA256)


class RuntimeProfileTests(unittest.TestCase):
    """Build-131544 runtime profile checked against the hash-pinned capture."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        if not RUNTIME_TRACE.exists() or not RUNTIME_INDEX.exists():
            raise unittest.SkipTest("runtime trace/unit index unavailable")
        data = RUNTIME_TRACE.read_bytes()
        cls.trace_bytes = data
        cls.rows = aar.parse_trace(data)
        cls.index = json.loads(RUNTIME_INDEX.read_text(encoding="utf-8"))
        cls.manifest = aar.extract_runtime(
            cls.rows, RUNTIME_TRACE.name, aar.RUNTIME_TRACE_SHA256, len(cls.rows),
            cls.index, RUNTIME_INDEX.name, aar.RUNTIME_INDEX_SHA256)

    def runtime_extract(self, rows, index=None, name=None, sha=None):
        return aar.extract_runtime(
            rows, name or RUNTIME_TRACE.name, sha or aar.RUNTIME_TRACE_SHA256,
            len(rows), index or self.index, RUNTIME_INDEX.name,
            aar.RUNTIME_INDEX_SHA256)

    def test_runtime_unknown_source_and_raw_secondary_field_are_not_overclaimed(self):
        nulls = [event for event in self.manifest["events"]
                 if event["reported_source"]["arg1_raw"] == "0x0"]
        self.assertEqual(len(nulls), 11)
        for event in nulls:
            self.assertEqual(event["reported_source"]["role"], "unresolved_owner")
            self.assertIn("source=unresolved_owner", aar._rt_event_line(event))
        for event in self.manifest["events"]:
            self.assertIn("owner_field_0x24_raw", event["target"])
            self.assertNotIn("descriptor_tag", event["target"])
            expected = ("observed_sampled_lookup_plus_destroy_header"
                        if event["destruction"]["observed"] else "observed_sampled_lookup")
            self.assertEqual(event["confidence"]["target_owner"], expected)

    def test_runtime_file_authenticates_retained_capture_sources(self):
        manifest = aar.extract_runtime_file(RUNTIME_TRACE, RUNTIME_INDEX)
        records = manifest["provenance"]["capture_source_verification"]
        self.assertEqual(len(records), 3)
        self.assertTrue(all(item["status"] == "matched" for item in records))
        self.assertEqual({item["name"] for item in records},
                         {"hooks.js", "wgrd_frida.py", "aar-capture-131544.json"})

    def test_runtime_source_archive_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "hooks.js").write_text("not the captured hook source")
            with self.assertRaisesRegex(aar.AarTraceError, "capture source sha256 mismatch"):
                aar._rt_verify_capture_sources(Path(directory))

    def test_runtime_recomputes_counts_handles_and_join_identity(self):
        manifest = self.manifest
        events = manifest["events"]
        self.assertEqual(len(events), 28)
        self.assertEqual(sum(event["mode"] == 1 for event in events), 25)
        self.assertEqual(sum(event["mode"] == 2 for event in events), 3)
        self.assertEqual(sorted({event["damage_object"]["handle_u32"] for event in events}),
                         [31, 32, 33, 34, 39, 40])
        for event in events:
            self.assertEqual(event["target"]["join"]["status"],
                             "2_of_2_exact_guid_and_token")
            self.assertEqual(event["target"]["join"]["debug_name"], "Unit_VTT_323_NK")
            self.assertEqual(event["target"]["join"]["unit_type_id"], "20147")
            if event["reported_source"]["owner_handle_u32"] is not None:
                source = event["reported_source"]["join"]
                self.assertEqual(source["status"], "2_of_2_exact_guid_and_token")
                self.assertEqual(source["debug_name"], "Unit_Merkava_IIIB_Baz")
                self.assertEqual(source["unit_type_id"], "19537")
                self.assertEqual(event["reported_source"]["role"],
                                 "inferred_damage_source_owner")
                self.assertEqual(event["reported_source"]["confidence"],
                                 "inferred_not_static_proven")
            else:
                self.assertIsNone(event["reported_source"]["join"])
                self.assertEqual(event["reported_source"]["arg1_read_status"], "null")
        source_counts = {}
        for event in events:
            key = event["reported_source"]["arg1_raw"]
            source_counts[key] = source_counts.get(key, 0) + 1
        self.assertEqual(source_counts, {"0x54b14220": 10, "0x50397c20": 7, "0x0": 11})

    def test_runtime_check_uses_al_low_byte_not_upper_eax(self):
        events = self.manifest["events"]
        lethal = [event for event in events if event["check"]["al_u8"] == 1]
        nonlethal = [event for event in events if event["check"]["al_u8"] == 0]
        self.assertEqual([event["ordinal"] for event in lethal], [3, 7, 21])
        self.assertEqual(len(nonlethal), 25)
        for event in nonlethal:
            self.assertEqual(event["check"]["retval_raw"], "0x3c221900")
            self.assertFalse(event["check"]["threshold_met_low_byte"])
            self.assertFalse(event["destruction"]["observed"])
        for event in lethal:
            self.assertEqual(event["check"]["retval_raw"], "0x1")
            self.assertTrue(event["check"]["threshold_met_low_byte"])

    def test_runtime_damage_lifecycle_chains_are_observed_not_kills(self):
        chains = self.manifest["damage_lifecycle_observations"]
        self.assertEqual([item["impact_ordinal"] for item in chains], [3, 7, 21])
        self.assertEqual([item["damaged_handle_u32"] for item in chains], [33, 31, 39])
        self.assertEqual([item["reported_source_owner_handle_u32"] for item in chains],
                         [75, 74, 75])
        for item in chains:
            self.assertEqual(item["threshold"]["al_u8"], 1)
            self.assertEqual(item["victim_unit"], "Unit_VTT_323_NK")
            self.assertEqual(item["reported_source_unit"], "Unit_Merkava_IIIB_Baz")
            self.assertEqual(item["destruction_call"]["argument_raw"], "0x1")
        for event in self.manifest["events"]:
            if event["destruction"]["observed"]:
                self.assertEqual(event["destruction"]["return_address"], "0xc9c0ce")
                self.assertEqual(event["destruction"]["join"],
                                 "destroy_header_matches_lookup_object_and_descriptor")
                self.assertIsNone(event["destruction"]["kill_outcome"])
        cleanup = self.manifest["end_cleanup_destructions"]
        self.assertEqual([item["operand_handle_u32"] for item in cleanup], [0, 74, 75])
        self.assertEqual([item["retval_raw"] for item in cleanup], ["0x1", "0x2", "0x3"])
        for item in cleanup:
            self.assertEqual(item["return_address"], "0xb7c408")
            self.assertEqual(item["argument_raw"], "0x6")
            self.assertIsNone(item["kill_outcome"])

    def test_runtime_deterministic_time_is_scoped_and_unknowns_stay_null(self):
        events = self.manifest["events"]
        values = {event["ordinal"]: event["time"]["deterministic_time_seconds"]
                  for event in events}
        self.assertEqual(values[1], 806.4000244140625)
        self.assertEqual(values[7], 806.6000366210938)
        self.assertEqual(values[21], 830.7999877929688)
        for event in events:
            time = event["time"]
            self.assertEqual(time["proof_level"],
                             "engine_named_clock_static_path_and_observed_module_store")
            for field in ("epoch", "frame", "replay_frame", "simulation_time", "game_time",
                          "battle_time"):
                self.assertIsNone(time[field])
            self.assertTrue(time["quantization_check"]["matches_quantization"])
        clock = self.manifest["clock"]
        self.assertEqual(clock["samples"], 459)
        self.assertEqual(len(clock["discontinuities"]), 1)
        boundary = clock["discontinuities"][0]
        self.assertEqual(boundary["kind"], "receiver_change")
        self.assertNotEqual(boundary["from_container"], boundary["to_container"])
        self.assertEqual(clock["scale_constant"]["bits"], "0x3e4ccccd")
        self.assertEqual(clock["first"]["counter"], 2195)
        self.assertEqual(clock["last"]["counter"], 4164)
        for field in ("epoch", "frame", "replay_frame", "simulation_time", "game_time",
                      "battle_time"):
            self.assertIsNone(clock[field])

    def test_runtime_integrity_and_reference_probe(self):
        integrity = self.manifest["integrity"]
        self.assertEqual(integrity["records"], 12382)
        self.assertEqual(integrity["emitted_records"], 12376)
        self.assertEqual(integrity["paired_calls"], 6188)
        self.assertEqual(integrity["impact_enters"], 28)
        self.assertEqual(integrity["owner_lookups"], 365)
        self.assertEqual(integrity["owner_lookup_distinct_handles"], 71)
        self.assertEqual(integrity["owner_lookup_handle_matches_plus_0x20"], 365)
        self.assertEqual(integrity["lifecycle_destroys"], 3)
        self.assertEqual(integrity["cleanup_destroys"], 3)
        self.assertTrue(integrity["destroy_headers_identical"])
        probe = self.manifest["identity_probes"]["reference_lookup"]
        self.assertEqual(probe["calls"], 5277)
        self.assertEqual(probe["successful_header_reads"], 243)
        self.assertEqual(probe["unreadable_returns"], 5034)
        self.assertEqual(probe["header_plus_0x1c_equals_arg0"], 243)
        self.assertEqual(probe["member_addresses_checked"], 8)
        self.assertEqual(probe["member_address_matches"], 0)
        self.assertEqual(probe["status"], "does_not_authenticate_member_objects")

    def test_runtime_line_refs_resolve_in_the_pinned_trace(self):
        rows = self.rows
        for event in self.manifest["events"]:
            refs = event["refs"]
            enter = rows[refs["enter_line"] - 1]
            leave = rows[refs["leave_line"] - 1]
            check_enter = rows[refs["check_enter_line"] - 1]
            self.assertEqual(enter["event"], "enter")
            self.assertEqual(enter["hook"], aar.RUNTIME_IMPACT_HOOK)
            self.assertEqual(enter["ordinal"], event["ordinal"])
            self.assertEqual(leave["event"], "leave")
            self.assertEqual(leave["call_id"], enter["call_id"])
            self.assertEqual(check_enter["event"], "enter")
            self.assertEqual(check_enter["hook"], aar.RUNTIME_CHECK_HOOK)
            self.assertEqual(check_enter["ordinal"], event["ordinal"])
            self.assertEqual(check_enter["ecx"], enter["ecx"])
            if event["destruction"]["observed"]:
                destroy = rows[refs["destroy_enter_line"] - 1]
                self.assertEqual(destroy["event"], "enter")
                self.assertEqual(destroy["hook"], aar.RUNTIME_DESTROY_HOOK)
                self.assertEqual(destroy["call_id"], event["destruction"]["call_id"])
                self.assertEqual(destroy["parent_call_id"], event["check"]["call_id"])
        for chain in self.manifest["damage_lifecycle_observations"]:
            self.assertLess(chain["impact_refs"]["enter_line"],
                            chain["destruction_call"]["line_refs"][0])

    def test_runtime_missing_leave_pair_fails_closed(self):
        rows = [row for row in self.rows
                if not (row.get("event") == "leave"
                        and row.get("hook") == aar.RUNTIME_IMPACT_HOOK)]
        with self.assertRaisesRegex(aar.AarTraceError, "missing pair"):
            self.runtime_extract(rows)

    def test_runtime_duplicate_leave_pair_fails_closed(self):
        rows = list(self.rows)
        leave = next(row for row in rows
                     if row.get("event") == "leave"
                     and row.get("hook") == aar.RUNTIME_IMPACT_HOOK)
        rows.insert(rows.index(leave) + 1, copy.deepcopy(leave))
        with self.assertRaisesRegex(aar.AarTraceError, "duplicate impact_apply_candidate leave"):
            self.runtime_extract(rows)

    def test_runtime_threshold_without_destroy_fails_closed(self):
        rows = copy.deepcopy(self.rows)
        checks = [row for row in rows
                  if row.get("event") == "leave"
                  and row.get("hook") == aar.RUNTIME_CHECK_HOOK]
        victim = next(row for row in checks if row["retval"] == "0x3c221900")
        victim["retval"] = "0x1"
        with self.assertRaisesRegex(aar.AarTraceError, "threshold check without nested destroy"):
            self.runtime_extract(rows)

    def test_runtime_non_boolean_al_fails_closed(self):
        rows = copy.deepcopy(self.rows)
        checks = [row for row in rows
                  if row.get("event") == "leave"
                  and row.get("hook") == aar.RUNTIME_CHECK_HOOK]
        victim = next(row for row in checks if row["retval"] == "0x3c221900")
        victim["retval"] = "0x3c221902"
        with self.assertRaisesRegex(aar.AarTraceError, "AL is not boolean"):
            self.runtime_extract(rows)

    def test_runtime_token_mismatch_does_not_assert_identity(self):
        index = copy.deepcopy(self.index)
        index["unit_types"]["20147"]["name_token"] = "0011223344556677"
        manifest = self.runtime_extract(self.rows, index=index)
        for event in manifest["events"]:
            self.assertEqual(event["target"]["join"]["status"], "candidate_token_mismatch")
            self.assertEqual(event["target"]["join"]["confidence"], "none")
            self.assertIsNone(event["target"]["join"]["unit_type_id"])
            self.assertEqual(event["target"]["identity_status"],
                             "observed_handle_but_type_join_unverified")

    def test_runtime_duplicate_index_token_is_not_unique(self):
        index = copy.deepcopy(self.index)
        index["unit_types"]["19537"]["name_token"] = "15460c84e7810000"
        manifest = self.runtime_extract(self.rows, index=index)
        statuses = {(event["target"]["join"]["status"]) for event in manifest["events"]}
        self.assertEqual(statuses, {"token_not_unique"})
        for event in manifest["events"]:
            self.assertFalse(event["target"]["join"]["token_unique"])
            self.assertIsNone(event["target"]["join"]["unit_type_id"])

    def test_runtime_outputs_are_exclusive_and_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            targets = aar.write_runtime_outputs(self.manifest, directory)
            names = sorted(path.name for path in targets)
            self.assertEqual(names, ["chronology.md", "events.json", "summary.json",
                                     "units.json"])
            before = {path.name: path.read_bytes() for path in targets}
            with self.assertRaisesRegex(aar.AarTraceError, "refusing to overwrite"):
                aar.write_runtime_outputs(self.manifest, directory)
            self.assertEqual({path.name: path.read_bytes() for path in targets}, before)
            events = json.loads((Path(directory) / "events.json").read_text(encoding="utf-8"))
            units = json.loads((Path(directory) / "units.json").read_text(encoding="utf-8"))
            self.assertEqual(len(events["events"]), 28)
            self.assertEqual(len(units["units"]), 9)
            text = (Path(directory) / "chronology.md").read_text(encoding="utf-8")
            for event in events["events"]:
                self.assertIn(event["line_ref"], text)
            self.assertNotIn("/Users/", text)

    def test_runtime_cli_requires_index_and_does_not_fall_through(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "events"
            self.assertEqual(run_main([str(RUNTIME_TRACE), "--runtime", "--out",
                                       str(output)]), 2)
            self.assertFalse(output.exists())
            self.assertEqual(run_main([str(RUNTIME_TRACE), "--runtime", "--unit-index",
                                       str(RUNTIME_INDEX), "--out", str(output),
                                       "--expect-sha256", "f" * 64]), 2)
            self.assertFalse(output.exists())
            self.assertEqual(run_main([str(RUNTIME_TRACE), "--out", str(output)]), 2)
            self.assertFalse(output.exists())
            self.assertEqual(run_main([str(RUNTIME_TRACE), "--profile", "runtime",
                                       "--unit-index", str(RUNTIME_INDEX),
                                       "--out", str(output)]), 0)
            self.assertTrue((output / "units.json").exists())
            self.assertEqual(run_main([str(RUNTIME_TRACE), "--runtime", "--unit-index",
                                       str(RUNTIME_INDEX), "--out", str(output)]), 2)

    def test_runtime_index_hash_is_pinned(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unit-index.json"
            path.write_text(json.dumps({"game_build": aar.RUNTIME_REVISION}),
                            encoding="utf-8")
            with self.assertRaisesRegex(aar.AarTraceError, "unit index sha256 mismatch"):
                aar.extract_runtime_file(RUNTIME_TRACE, path)

    def test_runtime_clock_quantization_is_not_a_counter_proof(self):
        check = aar._rt_clock_quantization(806.4)
        self.assertEqual(check["quantization_units"], 4032)
        self.assertIsNone(check["counter_claim"])
        self.assertTrue(check["matches_quantization"])
        text = json.dumps(self.manifest, allow_nan=False)
        self.assertNotIn('"counter": 4032', text)
        for event in self.manifest["events"]:
            self.assertNotIn("counter", event["time"])


def _v3_read(source, offset, size, phase, hexdata, **extra):
    read = {"source": source, "phase": phase, "offset": offset, "size": size,
            "address": "0x%08x" % (0x10000000 + offset), "indirect": False,
            "chain": [], "target": None, "result": {"ok": True, "hex": hexdata}}
    read.update(extra)
    return read


def _v3_lookup(handle, owner, descriptor, pointer, xyz_hex):
    header = bytearray(128)
    struct.pack_into("<I", header, 0x20, handle)
    struct.pack_into("<I", header, 0x28, descriptor)
    target = (pointer & 0xFFFFFFFC) + aar.RUNTIME_V3_POSITION_OFFSET
    return {
        "event": "leave", "hook": "owner_lookup_candidate", "call_id": 1,
        "thread_id": 9, "ecx": "0x%08x" % owner, "retval": "0x%08x" % owner,
        "reads": [
            _v3_read("retval", 0, 128, "leave", header.hex()),
            _v3_read("retval", 40, 128, "leave", bytes(128).hex(), indirect=True,
                     chain=["0x%08x" % descriptor], target="0x%08x" % descriptor),
            _v3_read("retval", 228, 12, "leave", xyz_hex, indirect=True,
                     chain=["0x%08x" % pointer], target="0x%08x" % target,
                     raw_pointer="0x%08x" % pointer, applied_mask="0xfffffffc",
                     target_offset=aar.RUNTIME_V3_POSITION_OFFSET,
                     final_target="0x%08x" % target),
        ],
    }


def _v3_xyz(x, y, z):
    return struct.pack("<3f", x, y, z).hex()


class RuntimeV3ProfileTests(unittest.TestCase):
    """Ten-hook V3 profile with masked descriptor and position reads."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        if not RUNTIME_V3_TRACE.exists() or not RUNTIME_INDEX.exists():
            raise unittest.SkipTest("v3 capture or unit index unavailable")
        cls.trace_bytes = RUNTIME_V3_TRACE.read_bytes()
        cls.rows = aar.parse_trace(cls.trace_bytes)
        cls.index = json.loads(RUNTIME_INDEX.read_text(encoding="utf-8"))
        cls.manifest = aar.extract_runtime(
            cls.rows, RUNTIME_V3_TRACE.name, aar.RUNTIME_V3_TRACE_SHA256,
            len(cls.rows), cls.index, RUNTIME_INDEX.name,
            aar.RUNTIME_V3_INDEX_SHA256)

    def v3_extract(self, rows, profile="runtime-v3", index=None):
        return aar.extract_runtime(
            rows, RUNTIME_V3_TRACE.name, aar.RUNTIME_V3_TRACE_SHA256,
            len(rows), index or self.index, RUNTIME_INDEX.name,
            aar.RUNTIME_V3_INDEX_SHA256, profile)

    def test_v3_profile_is_selected_only_by_an_exact_known_hook_set(self):
        self.assertEqual(self.manifest["profile"]["name"], "runtime-v3")
        self.assertEqual(self.manifest["schema"], aar.RUNTIME_V3_SCHEMA)
        self.assertEqual(len(self.manifest["profile"]["position_hooks"]), 2)
        self.assertEqual(aar._rt_detect_profile(self.rows)["name"], "runtime-v3")
        short = copy.deepcopy(self.rows)
        short[0]["hooks"] = [hook for hook in short[0]["hooks"]
                             if hook["name"] != "phase_change_candidate"]
        with self.assertRaisesRegex(aar.AarTraceError, "unknown hook profile"):
            aar._rt_detect_profile(short)
        with self.assertRaisesRegex(aar.AarTraceError, "read shape mismatch"):
            self.v3_extract(short, profile="runtime")
        extra = copy.deepcopy(self.rows)
        extra[0]["hooks"].append({"name": "shell_candidate", "va": "0x1", "args": 0,
                                  "sample_every": 1, "reads": []})
        with self.assertRaisesRegex(aar.AarTraceError, "unknown hook profile"):
            aar._rt_detect_profile(extra)

    def test_v3_indirect_mask_and_offset_are_validated(self):
        for key, value, message in (("indirect_mask", "fffffffe", "indirect mask mismatch"),
                                    ("indirect_offset", 52, "indirect offset mismatch")):
            rows = copy.deepcopy(self.rows)
            hook = next(item for item in rows[0]["hooks"]
                        if item["name"] == "owner_lookup_candidate")
            read = next(item for item in hook["reads"] if item["offset"] == 228)
            read[key] = value
            with self.assertRaisesRegex(aar.AarTraceError, message):
                self.v3_extract(rows)

    def test_v3_incomplete_capture_is_never_exported(self):
        for dropped in ("summary", "detached", "end"):
            rows = [row for row in self.rows if row.get("event") != dropped]
            with self.assertRaisesRegex(aar.AarTraceError,
                                        "incomplete capture: missing %s" % dropped):
                self.v3_extract(rows)
        if not RUNTIME_V3_INFLIGHT.exists():
            return
        inflight = RUNTIME_V3_INFLIGHT.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "events"
            self.assertEqual(run_main([
                str(RUNTIME_V3_INFLIGHT), "--profile", "runtime-v3", "--unit-index",
                str(RUNTIME_INDEX), "--expect-sha256",
                hashlib.sha256(inflight).hexdigest(), "--out", str(output)]), 2)
            self.assertFalse(output.exists())

    def test_v3_positions_are_descriptor_resolved_and_finite(self):
        self.assertEqual(self.manifest["integrity"].get("position_descriptor_read_failures"), 0)
        self.assertEqual(self.manifest["integrity"].get("gate_counter_status"),
                         "not_reported_by_pinned_v3_source; no_gate_zero_claim")
        observations = self.manifest["position_observations"]
        self.assertEqual(len(observations), 371)
        self.assertEqual(sum(item["hook"] == "owner_lookup_candidate"
                             for item in observations), 365)
        self.assertEqual(sum(item["hook"] == "owner_destroy_candidate"
                             for item in observations), 6)
        self.assertEqual(self.manifest["integrity"]["position_read_failures"], 0)
        self.assertEqual(self.manifest["integrity"]["position_identity_tracks"], 71)
        for observation in observations:
            anchor = observation["anchor"]
            self.assertEqual(anchor["status"], "read_ok")
            self.assertEqual(len(anchor["xyz"]), 3)
            self.assertTrue(all(math.isfinite(value) for value in anchor["xyz"]))
            self.assertEqual(anchor["target"], "0x%08x" % (
                (int(anchor["raw_pointer"], 16) & 0xFFFFFFFC)
                + aar.RUNTIME_V3_POSITION_OFFSET))
            self.assertEqual(len(bytes.fromhex(anchor["raw_hex"])), 12)
            self.assertEqual(observation["identity"]["key"],
                             "h%d|%s|%s" % (observation["identity"]["handle_u32"],
                                            observation["identity"]["owner_object"],
                                            observation["identity"]["descriptor_pointer"]))
        first = observations[0]
        self.assertEqual(first["identity"]["key"], "h15|0x79ac9dd0|0x50f51710")
        self.assertEqual(first["line"], 8359)
        self.assertEqual(first["anchor"]["xyz"], [575043.9375, 1593865.75, 32760.0])
        self.assertEqual(first["identity"]["descriptor_join"]["debug_name"],
                         "Unit_Motorstrelki")
        self.assertEqual(first["identity"]["descriptor_join"]["status"],
                         "2_of_2_exact_guid_and_token")

    def test_v3_identity_mismatch_is_kept_as_separate_tracks(self):
        observations, failures = aar._rt_position_observations(
            [_v3_lookup(5, 0x2000, 0x3000, 0x4000, _v3_xyz(1, 2, 3)),
             _v3_lookup(5, 0x2100, 0x3000, 0x5000, _v3_xyz(1, 2, 3))],
            aar.RUNTIME_PROFILE_V3, None)
        self.assertEqual(failures, 0)
        aar._rt_apply_clock_brackets(observations, [])
        report = aar._rt_position_identity(observations)
        self.assertEqual(report["tracks"], 2)
        self.assertEqual([item["field"] for item in report["conflicts"]], ["handle"])
        self.assertEqual(aar._rt_position_changes(observations), [])

    def test_v3_changes_need_one_identity_and_one_anchor_target(self):
        same = _v3_xyz(1, 2, 3)
        observations, _ = aar._rt_position_observations(
            [_v3_lookup(7, 0x2200, 0x3000, 0x4000, same),
             _v3_lookup(7, 0x2200, 0x3000, 0x4000, same),
             _v3_lookup(7, 0x2200, 0x3000, 0x4000, _v3_xyz(4, 6, 3))],
            aar.RUNTIME_PROFILE_V3, None)
        aar._rt_apply_clock_brackets(observations, [])
        changes = aar._rt_position_changes(observations)
        self.assertEqual(len(changes), 1)
        change = changes[0]
        self.assertEqual(change["kind"], "position_anchor_changed")
        self.assertEqual((change["from"]["line"], change["to"]["line"]), (2, 3))
        self.assertEqual(change["delta_raw_f32"], [3.0, 4.0, 0.0])
        self.assertEqual(change["displacement_raw_f32"], 5.0)
        self.assertEqual(change["units"], "unknown_unmapped_raw_f32")
        rebound, _ = aar._rt_position_observations(
            [_v3_lookup(7, 0x2200, 0x3000, 0x4000, same),
             _v3_lookup(7, 0x2200, 0x3000, 0x4010, _v3_xyz(9, 9, 9))],
            aar.RUNTIME_PROFILE_V3, None)
        aar._rt_apply_clock_brackets(rebound, [])
        kinds = aar._rt_position_changes(rebound)
        self.assertEqual([item["kind"] for item in kinds], ["position_anchor_rebound"])
        self.assertFalse(kinds[0]["comparable"])

    def test_v3_anchor_arithmetic_and_finiteness_are_enforced(self):
        base = [_v3_lookup(5, 0x2000, 0x3000, 0x4000, _v3_xyz(1, 2, 3))]
        cases = ((("final_target", "0x1"), "anchor final target mismatch"),
                 (("applied_mask", "0xfffffffe"), "anchor mask mismatch"),
                 (("target_offset", 44), "anchor target offset mismatch"))
        for (field, value), message in cases:
            rows = copy.deepcopy(base)
            rows[0]["reads"][2][field] = value
            with self.assertRaisesRegex(aar.AarTraceError, message):
                aar._rt_position_observations(rows, aar.RUNTIME_PROFILE_V3, None)
        non_finite = copy.deepcopy(base)
        non_finite[0]["reads"][2]["result"]["hex"] = _v3_xyz(float("nan"), 0, 0)
        with self.assertRaisesRegex(aar.AarTraceError, "non-finite position"):
            aar._rt_position_observations(non_finite, aar.RUNTIME_PROFILE_V3, None)
        unreadable = copy.deepcopy(base)
        unreadable[0]["reads"][2]["result"] = {"ok": False, "reason": "unreadable"}
        observations, failures = aar._rt_position_observations(
            unreadable, aar.RUNTIME_PROFILE_V3, None)
        self.assertEqual(failures, 1)
        self.assertEqual(observations[0]["anchor"]["status"], "position_read_failed")
        self.assertIsNone(observations[0]["anchor"]["xyz"])

    def test_v3_clock_brackets_are_adjacent_and_never_interpolated(self):
        observations = self.manifest["position_observations"]
        bracketed = [item for item in observations
                     if item["time"]["bracket"]["bracketed"]]
        self.assertEqual(len(bracketed), 363)
        self.assertEqual([item["index"] for item in observations
                          if not item["time"]["bracket"]["bracketed"]],
                         list(range(1, 9)))
        clock_lines = [number for number, row in enumerate(self.rows, 1)
                       if row.get("event") == "enter"
                       and row.get("hook") == "clock_sample_candidate"]
        previous = {}
        for index, line in enumerate(clock_lines):
            previous[line] = clock_lines[index - 1] if index else None
        for observation in bracketed:
            bracket = observation["time"]["bracket"]
            self.assertLess(bracket["lower"]["line"], observation["line"])
            self.assertLess(observation["line"], bracket["upper"]["line"])
            self.assertEqual(bracket["lower"]["receiver"], bracket["upper"]["receiver"])
            self.assertEqual(bracket["counter_span"],
                             bracket["upper"]["counter"] - bracket["lower"]["counter"])
            self.assertEqual(previous[bracket["upper"]["line"]], bracket["lower"]["line"])
        self.assertEqual([(item["index"], item["samples"])
                          for item in self.manifest["clock_epochs"]], [(0, 1), (1, 458)])
        for observation in observations:
            for key in ("frame", "simulation_time", "game_time", "battle_time",
                        "counter_ticks"):
                self.assertIsNone(observation["time"][key])
        self.assertNotIn("wallclock", json.dumps(observations).lower())
        samples = [{"ordinal": 1, "counter": 1, "container": "0x1", "enter_line": 2,
                    "leave_line": 3},
                   {"ordinal": 2, "counter": 2, "container": "0x2", "enter_line": 10,
                    "leave_line": 11}]
        synthetic = [{"line": 5, "index": 1, "hook": "h", "phase": "p", "anchor": {}}]
        aar._rt_apply_clock_brackets(synthetic, samples)
        self.assertFalse(synthetic[0]["time"]["bracket"]["bracketed"])
        self.assertEqual(synthetic[0]["time"]["bracket"]["reason"],
                         "adjacent_clock_samples_span_an_epoch_change")

    def test_v3_outputs_and_line_refs_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            targets = aar.write_runtime_outputs(self.manifest, directory)
            self.assertEqual(sorted(path.name for path in targets),
                             ["chronology.md", "events.json", "positions.json",
                              "summary.json", "units.json"])
            positions = json.loads((Path(directory) / "positions.json")
                                   .read_text(encoding="utf-8"))
            self.assertEqual(positions["schema"], aar.RUNTIME_V3_POSITIONS_SCHEMA)
            self.assertEqual(len(positions["observations"]), 371)
            self.assertEqual(len(positions["anchor_changes"]), 153)
            text = (Path(directory) / "chronology.md").read_text(encoding="utf-8")
            self.assertIn("## Position observations (raw tagged anchors)", text)
            self.assertIn("raw value transitions, not movements", text)
        for observation in self.manifest["position_observations"]:
            row = self.rows[observation["line"] - 1]
            self.assertEqual(row["hook"], observation["hook"])
            self.assertEqual(row["event"], observation["phase"])
            source = ("retval" if observation["hook"] == "owner_lookup_candidate"
                      else "ecx")
            read = next(item for item in row["reads"]
                        if item["source"] == source and item["offset"] == 228
                        and item["size"] == 12)
            self.assertEqual(read["result"]["hex"], observation["anchor"]["raw_hex"])
            self.assertEqual(hashlib.sha256(bytes.fromhex(read["result"]["hex"]))
                             .hexdigest(), observation["anchor"]["sha256"])
        for change in self.manifest["position_anchor_changes"]:
            self.assertLess(change["from"]["line"], change["to"]["line"])
            self.assertIn("not_derived", change)
            self.assertTrue(math.isclose(
                change["displacement_raw_f32"],
                math.sqrt(sum(value * value for value in change["delta_raw_f32"]))))

    def test_v3_file_export_authenticates_sources_and_is_exclusive(self):
        manifest = aar.extract_runtime_file(
            RUNTIME_V3_TRACE, RUNTIME_INDEX, aar.RUNTIME_V3_TRACE_SHA256,
            aar.RUNTIME_V3_INDEX_SHA256, "runtime-v3")
        records = manifest["provenance"]["capture_source_verification"]
        self.assertEqual({item["name"] for item in records},
                         {"wgrd_frida.py", "hooks.js", "aar-capture-131544-v3.json"})
        self.assertTrue(all(item["status"] == "matched" for item in records))
        self.assertEqual(manifest["provenance"]["capture_config_pin"]["file"],
                         "aar-capture-131544-v3.json")
        self.assertEqual(len(manifest["profile"]["position_hooks"]), 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            self.assertEqual(run_main([str(RUNTIME_V3_TRACE), "--profile", "runtime-v3",
                                       "--unit-index", str(RUNTIME_INDEX),
                                       "--out", str(output)]), 0)
            self.assertTrue((output / "positions.json").exists())
            self.assertEqual(run_main([str(RUNTIME_V3_TRACE), "--profile", "runtime-v3",
                                       "--unit-index", str(RUNTIME_INDEX),
                                       "--out", str(output)]), 2)


class ConfiguredDescriptorIdentity(unittest.TestCase):
    def fixture(self):
        guid = "000000000500000001000000e8030000"
        token = "4c06010000000000"
        index = {
            "descriptors": {guid: {"source_nodes": ["20843"], "candidates": []}},
            "unit_types": {
                "20843": {"source_node": "20843", "descriptor_guid_hex": guid,
                          "name_token": token, "ndf_class": "TUniteDescriptor",
                          "debug_name": "Building_FOB_ISR"},
                "other": {"source_node": "other", "descriptor_guid_hex": "11" * 16,
                          "name_token": token},
            },
        }
        row = _v3_lookup(4, 0x2200, 0x3000, 0x4000, _v3_xyz(1, 2, 3))
        descriptor = bytearray(128)
        descriptor[0x0c:0x1c] = bytes.fromhex(guid)
        descriptor[0x60:0x68] = bytes.fromhex(token)
        row["reads"][1]["result"]["hex"] = descriptor.hex()
        return row, index

    def test_shared_token_configured_class_does_not_relax_member_join(self):
        row, index = self.fixture()
        observations, _ = aar._rt_position_observations([row], aar.RUNTIME_PROFILE_V3, index)
        identity = observations[0]["identity"]
        configured = identity.get("configured_descriptor", {})
        self.assertEqual(configured.get("debug_name"), "Building_FOB_ISR")
        self.assertEqual(configured["ndf_class"], "TUniteDescriptor")
        self.assertEqual(configured["source_node"], "20843")
        self.assertFalse(configured["token_unique"])
        self.assertEqual(configured["status"], "unique_guid_compatible_token")
        self.assertEqual(identity["descriptor_join"]["status"], "ambiguous_or_missing_candidates")
        self.assertIsNone(identity["descriptor_join"]["unit_type_id"])


    def test_configured_class_rejects_mismatched_token(self):
        row, index = self.fixture()
        data = bytearray.fromhex(row["reads"][1]["result"]["hex"])
        data[0x60:0x68] = bytes.fromhex("aa" * 8)
        row["reads"][1]["result"]["hex"] = data.hex()
        observations, _ = aar._rt_position_observations([row], aar.RUNTIME_PROFILE_V3, index)
        configured = observations[0]["identity"]["configured_descriptor"]
        self.assertEqual(configured["status"], "token_mismatch")
        self.assertIsNone(configured["ndf_class"])
        self.assertIsNone(configured["debug_name"])

    def test_configured_class_rejects_nonunique_guid(self):
        row, index = self.fixture()
        index["unit_types"]["other"]["descriptor_guid_hex"] = (
            index["unit_types"]["20843"]["descriptor_guid_hex"])
        observations, _ = aar._rt_position_observations([row], aar.RUNTIME_PROFILE_V3, index)
        configured = observations[0]["identity"]["configured_descriptor"]
        self.assertEqual(configured["status"], "guid_not_unique")
        self.assertIsNone(configured["source_node"])

    def test_configured_class_rejects_disagreeing_source_node(self):
        row, index = self.fixture()
        next(iter(index["descriptors"].values()))["source_nodes"] = ["other"]
        observations, _ = aar._rt_position_observations([row], aar.RUNTIME_PROFILE_V3, index)
        configured = observations[0]["identity"]["configured_descriptor"]
        self.assertEqual(configured["status"], "descriptor_source_disagreement")
        self.assertIsNone(configured["debug_name"])

    def test_configured_class_does_not_invent_unreadable_descriptor(self):
        row, index = self.fixture()
        row["reads"][1]["result"] = {"ok": False, "reason": "unreadable"}
        observations, _ = aar._rt_position_observations([row], aar.RUNTIME_PROFILE_V3, index)
        configured = observations[0]["identity"]["configured_descriptor"]
        self.assertEqual(configured["status"], "descriptor_bytes_unreadable")
        self.assertIsNone(configured["debug_name"])


class PositionTransitionTiming(unittest.TestCase):
    def test_v3_source_authentication_requires_all_retained_files(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(aar.AarTraceError, "capture source missing"):
                aar._rt_verify_capture_sources(directory, aar.RUNTIME_PROFILE_V3)
            legacy = aar._rt_verify_capture_sources(directory, aar.RUNTIME_PROFILE_V2)
            self.assertTrue(all(item["status"] == "missing" for item in legacy))

    def test_change_interval_covers_both_position_observations(self):
        observations, _ = aar._rt_position_observations(
            [_v3_lookup(7, 0x2200, 0x3000, 0x4000, _v3_xyz(1, 2, 3)),
             _v3_lookup(7, 0x2200, 0x3000, 0x4000, _v3_xyz(4, 6, 3))],
            aar.RUNTIME_PROFILE_V3, None)
        observations[0]["line"], observations[1]["line"] = 15, 45
        clocks = [{"enter_line": line, "container": "0x5000", "counter": tick}
                  for line, tick in [(10, 100), (20, 110), (40, 200), (50, 210)]]
        aar._rt_apply_clock_brackets(observations, clocks)
        change = aar._rt_position_changes(observations)[0]
        bracket = change["time"]["bracket"]
        self.assertTrue(bracket["bracketed"])
        self.assertEqual(bracket["lower"]["counter"], 100)
        self.assertEqual(bracket["upper"]["counter"], 210)
        self.assertEqual(bracket["counter_span"], 110)


if __name__ == "__main__":
    unittest.main()
