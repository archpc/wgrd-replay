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


def run_main(arguments):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return aar.main(arguments)



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

    def test_descriptor_captured_at_lists_each_impact_once(self):
        refs = [ref for item in self.manifest["descriptor_joins"] for ref in item["captured_at"]]
        self.assertEqual(len(refs), len(set(refs)))
        self.assertEqual(len(refs), len(self.manifest["events"]))

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
                                 "engine_credited_damage_source")
                self.assertEqual(event["reported_source"]["confidence"],
                                 "static_xp_credit_and_producer_dataflow")
            else:
                self.assertIsNone(event["reported_source"]["join"])
                self.assertEqual(event["reported_source"]["arg1_read_status"], "null")
        source_counts = {}
        for event in events:
            key = event["reported_source"]["arg1_raw"]
            source_counts[key] = source_counts.get(key, 0) + 1
        self.assertEqual(source_counts, {"0x54b14220": 10, "0x50397c20": 7, "0x0": 11})

    def test_runtime_owning_refs_and_killed_token_levels(self):
        refs = {unit["handle_u32"]: unit["owning_object_ref"]["raw"]
                for unit in self.manifest["units"]}
        self.assertEqual({refs[handle] for handle in (31, 32, 33, 34, 39, 40)},
                         {"0x00020005"})
        self.assertEqual({refs[handle] for handle in (0, 74, 75)}, {"0x00020004"})
        self.assertNotIn("ownership", self.manifest)
        for item in self.manifest["damage_lifecycle_observations"]:
            token = item["killed_token"]
            self.assertTrue(token["value"])
            self.assertEqual(token["level"], "static_mapping_of_observed_check_al")
            self.assertFalse(token["combat_message_captured"])
            self.assertFalse(token["scored_kill_confirmed"])

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


class FrameCorrelationTests(unittest.TestCase):
    """Mechanics of joining event lines to tick-hook frame brackets."""

    HOOK = "tick_step"

    def _tick_rows(self, call_id, enter, leave, frame_in, frame_out):
        def make(event, stamp, frame):
            return {"event": event, "hook": self.HOOK, "call_id": call_id,
                    "timestamp_utc": stamp,
                    "reads": [
                        {"source": "ecx", "phase": event, "offset": 108, "size": 4,
                         "result": {"ok": True, "hex": struct.pack("<I", frame).hex()}},
                        {"source": "ecx", "phase": event, "offset": 165, "size": 1,
                         "result": {"ok": True, "hex": "01"}},
                    ]}
        return [make("enter", enter, frame_in), make("leave", leave, frame_out)]

    def _marker(self, stamp):
        # A plain event line: no hook, so it cannot disturb pairing checks.
        return {"event": "enter", "call_id": 9999, "timestamp_utc": stamp, "reads": []}

    def test_event_inside_a_tick_call_keeps_both_frame_edges(self):
        rows = self._tick_rows(1, "2026-01-01T00:00:00.000Z", "2026-01-01T00:00:00.010Z", 40, 41)
        rows.append(self._marker("2026-01-01T00:00:00.005Z"))
        joins, summary = aar.correlate_tick_frames(rows, [{"ordinal": 1, "refs": {"enter_line": "L3"}}])
        join = joins[1]
        self.assertEqual(join["status"], "inside_tick_call")
        self.assertEqual((join["frame_low"], join["frame_high"]), (40, 41))
        self.assertEqual(join["bracket_before_seconds"], 0.0)
        self.assertEqual(summary["status_counts"], {"inside_tick_call": 1})

    def test_event_between_close_calls_is_bracketed_to_one_frame(self):
        rows = self._tick_rows(1, "2026-01-01T00:00:00.000Z", "2026-01-01T00:00:00.002Z", 40, 40)
        rows += self._tick_rows(2, "2026-01-01T00:00:00.100Z", "2026-01-01T00:00:00.102Z", 40, 41)
        rows.append(self._marker("2026-01-01T00:00:00.050Z"))
        joins, _ = aar.correlate_tick_frames(rows, [{"ordinal": 1, "refs": {"enter_line": "L5"}}])
        join = joins[1]
        self.assertEqual(join["status"], "bracketed")
        self.assertEqual((join["frame_low"], join["frame_high"]), (40, 40))
        self.assertAlmostEqual(join["bracket_before_seconds"], 0.048, places=6)
        self.assertAlmostEqual(join["bracket_after_seconds"], 0.05, places=6)

    def test_wide_gap_and_missing_side_stay_unresolved(self):
        rows = self._tick_rows(1, "2026-01-01T00:00:00.000Z", "2026-01-01T00:00:00.002Z", 40, 40)
        rows += self._tick_rows(2, "2026-01-01T00:00:05.000Z", "2026-01-01T00:00:05.002Z", 41, 41)
        rows.append(self._marker("2026-01-01T00:00:02.000Z"))
        rows.append(self._marker("2026-01-01T00:00:09.000Z"))
        events = [{"ordinal": 1, "refs": {"enter_line": "L5"}},
                  {"ordinal": 2, "refs": {"enter_line": "L6"}}]
        joins, summary = aar.correlate_tick_frames(rows, events)
        self.assertEqual(joins[1]["status"], "wide_bracket")
        self.assertEqual(joins[1]["frame_low"], 40)
        self.assertEqual(joins[2]["status"], "unbracketed")
        self.assertIsNone(joins[2]["frame_low"])
        self.assertEqual(summary["status_counts"], {"unbracketed": 1, "wide_bracket": 1})

    def test_no_tick_hook_leaves_manifest_untouched(self):
        manifest = {"events": [{"ordinal": 1, "time": {"frame": None}}]}
        rows = [self._marker("2026-01-01T00:00:00.000Z")]
        self.assertIs(aar._rt_attach_frame_correlation(manifest, rows), manifest)
        self.assertNotIn("frame_correlation", manifest)

    def test_supersedes_the_naive_frame_hypothesis(self):
        rows = self._tick_rows(1, "2026-01-01T00:00:00.000Z", "2026-01-01T00:00:00.002Z", 7, 7)
        rows.append(self._marker("2026-01-01T00:00:00.001Z"))
        manifest = {"events": [{"ordinal": 1, "refs": {"enter_line": "L3"},
                                "time": {"replay_frame_hypothesis": {"value": 35,
                                                                     "status": "hypothesis_0p2s_per_replay_frame"}}}]}
        aar._rt_attach_frame_correlation(manifest, rows)
        event = manifest["events"][0]
        self.assertEqual(event["time"]["replay_frame_hypothesis"]["status"],
                         "superseded_by_tick_frame_correlation")
        self.assertEqual(event["time"]["frame_correlation"]["frame_low"], 7)
        self.assertEqual(manifest["frame_correlation"]["tick_intervals"], 1)


class CombatFrameCaptureTests(unittest.TestCase):
    """V4 export: every combat callback carries a bounded replay frame."""

    TRACE = Path(os.environ.get(
        "WGRD_AAR_V4_TRACE",
        Path.home() / ".hermes" / "artifacts" / "wgrd-replay"
        / "combat-frames-20261103" / "run07" / "run-07.jsonl"))
    SHA256 = "acb8ecdc9f264c2784590180e1b316822a3ade6db13cd3c4969c9046f90d6f21"

    @classmethod
    def setUpClass(cls):
        if not cls.TRACE.exists() or not RUNTIME_INDEX.exists():
            raise unittest.SkipTest("v4 combat trace/unit index unavailable")
        cls.rows = aar.parse_trace(cls.TRACE.read_bytes())
        cls.index = json.loads(RUNTIME_INDEX.read_text(encoding="utf-8"))
        cls.manifest = aar.extract_runtime(
            cls.rows, cls.TRACE.name, cls.SHA256, len(cls.rows), cls.index,
            RUNTIME_INDEX.name, aar.RUNTIME_INDEX_SHA256, "runtime-v4")

    def test_every_impact_carries_an_inside_tick_frame(self):
        events = self.manifest["events"]
        self.assertEqual(len(events), 28)
        for event in events:
            join = event["time"]["frame_correlation"]
            self.assertEqual(join["status"], "inside_tick_call")
            self.assertEqual(join["bracket_before_seconds"], 0.0)
            self.assertEqual(join["frame_high"] - join["frame_low"], 1)
        self.assertEqual(events[0]["time"]["frame_correlation"]["frame_low"], 4042)
        self.assertEqual(events[-1]["time"]["frame_correlation"]["frame_low"], 4165)

    def test_engine_seconds_fall_inside_the_derived_bounds(self):
        for event in self.manifest["events"]:
            observed = event["time"]["deterministic_time_seconds"]
            low, high = event["time"]["frame_correlation"]["estimated_deterministic_seconds_bounds"]
            self.assertGreaterEqual(observed, low - 1e-6)
            self.assertLessEqual(observed, high + 1e-6)

    def test_summary_reports_only_the_tick_tail_as_unpaired(self):
        correlation = self.manifest["frame_correlation"]
        self.assertEqual(correlation["status_counts"], {"inside_tick_call": 28})
        self.assertEqual(correlation["unpaired_calls"], {"tick_step": 1})

    def test_lifecycle_destroys_keep_their_frames(self):
        destroys = [event for event in self.manifest["events"]
                    if (event.get("destruction") or {}).get("kind") == "damage_lifecycle"]
        self.assertEqual(len(destroys), 3)
        frames = [event["time"]["frame_correlation"]["frame_low"] for event in destroys]
        self.assertEqual(frames, [4042, 4043, 4164])
