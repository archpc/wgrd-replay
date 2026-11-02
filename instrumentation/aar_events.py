#!/usr/bin/env python3
"""Recompute damage-event evidence from a pinned WGRD JSONL trace.

The raw trace is opened read-only and never rewritten. Every impact event is
rebuilt from its paired ``enter``/``leave`` reads; the trace summary, hash,
pairing, field reads and (optionally) the classified timeline are checked
before any output is written. Identity, frame/simulation time and kill outcome
stay ``None`` because this trace does not capture them. Wall-clock timestamps
are labelled as guest-clock observations, never as game time.

Fail-closed policy: a mismatch raises ``AarTraceError`` and the CLI exits 2
without creating output files. Output files are exclusively created.
"""

import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

TRACE_SHA256 = "95f3592493a3c55da52150e64eb773b68f652f4530dca586458847e1f95a7bd6"
CLASSIFIED_SHA256 = "e19e83dd23c3baae5afadb89403676ac0b0fa68b73fdfb803f3edaceae1ebb4a"
EXECUTABLE_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
REVISION = "131544"
IMPACT_HOOK = "impact_apply_candidate"
IMPACT_ADDRESS = "0xc9f910"
RETURN_ADDRESS = "0xc95200"
IMAGE_BASE = 0x400000
IMAGE_SIZE = 31883264
SCHEMA = "wgrd-aar-events/1"

ENTER_OFFSETS = frozenset((8, 400, 412, 416))
LEAVE_OFFSETS = frozenset((400, 412, 416))
FIELD_0X190 = 400
FIELD_0X194 = 404
FIELD_0X19C = 412
FIELD_0X1A0 = 416
HANDLE_OFFSET = 8
DECAY_DIVISORS = (0.6, 0.3, 0.2, 0.1, 0.05)
QUANTIZATION_TOLERANCE = 0.002


class AarTraceError(ValueError):
    """Raised when the trace or a requested cross-check is not trustworthy."""


def _require(condition, message):
    if not condition:
        raise AarTraceError(message)


def _single(rows, event_name):
    matches = [row for row in rows if row.get("event") == event_name]
    _require(len(matches) == 1, "expected exactly one %s record, found %d" % (event_name, len(matches)))
    return matches[0]


def _parse_timestamp(value, where):
    _require(isinstance(value, str) and value, "missing timestamp:%s" % where)
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AarTraceError("invalid timestamp:%s:%s" % (where, error)) from None


def _float32_memory(hex_value, where):
    _require(isinstance(hex_value, str) and len(hex_value) == 8, "bad read bytes:%s" % where)
    try:
        return struct.unpack("<f", bytes.fromhex(hex_value))[0]
    except ValueError as error:
        raise AarTraceError("bad read bytes:%s:%s" % (where, error)) from None


def _float32_argument(raw_value, where):
    _require(isinstance(raw_value, str) and raw_value.startswith("0x"), "bad argument:%s" % where)
    try:
        bits = int(raw_value, 16)
    except ValueError as error:
        raise AarTraceError("bad argument:%s:%s" % (where, error)) from None
    _require(0 <= bits <= 0xFFFFFFFF, "argument out of range:%s" % where)
    return struct.unpack("<f", struct.pack("<I", bits))[0]


def _u32_memory(hex_value, where):
    _require(isinstance(hex_value, str) and len(hex_value) == 8, "bad u32 read:%s" % where)
    return struct.unpack("<I", bytes.fromhex(hex_value))[0]


def _address(value, where):
    _require(isinstance(value, str) and value.startswith("0x"), "bad address:%s" % where)
    try:
        address = int(value, 16)
    except ValueError as error:
        raise AarTraceError("bad address:%s:%s" % (where, error)) from None
    _require(0 <= address <= 0xFFFFFFFF, "address out of range:%s" % where)
    return address


def image_membership(address):
    """Return arithmetic image-range facts without asserting section ownership."""
    end = IMAGE_BASE + IMAGE_SIZE
    inside = IMAGE_BASE <= address < end
    return {
        "base": "0x%08x" % IMAGE_BASE,
        "size": IMAGE_SIZE,
        "end": "0x%08x" % end,
        "offset_bytes": address - IMAGE_BASE if address >= IMAGE_BASE else None,
        "inside_image": inside,
    }


def parse_trace(data):
    """Parse strict UTF-8 JSONL into (rows, source_name, line_count)."""
    _require(isinstance(data, bytes), "trace bytes required")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AarTraceError("trace is not UTF-8:%s" % error) from None
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            raise AarTraceError("blank trace line:%d" % number)
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise AarTraceError("invalid json line %d:%s" % (number, error)) from None
        _require(isinstance(row, dict), "non-object json line:%d" % number)
        rows.append(row)
    _require(rows, "empty trace")
    return rows


def load_trace(path, expect_sha256):
    path = Path(path)
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    _require(digest == expect_sha256, "trace sha256 mismatch: %s" % digest)
    rows = parse_trace(data)
    return rows, path.name, digest, len(data.splitlines())


def _index_reads(record, module, expected_offsets):
    reads = record.get("reads")
    _require(isinstance(reads, list), "missing reads:%s" % record.get("event"))
    indexed = {}
    for read in reads:
        offset = read.get("offset")
        result = read.get("result") or {}
        where = "%s:0x%x" % (record.get("event"), offset if isinstance(offset, int) else 0)
        _require(offset in expected_offsets, "unexpected read offset:%s" % where)
        _require(offset not in indexed, "duplicate read offset:%s" % where)
        _require(read.get("indirect") is False, "indirect read:%s" % where)
        _require(read.get("chain") == [], "pointer chain read:%s" % where)
        _require(read.get("address") == "0x%08x" % (module + offset), "read address mismatch:%s" % where)
        _require(result.get("ok") is True, "read failure:%s" % where)
        indexed[offset] = result.get("hex")
    _require(frozenset(indexed) == expected_offsets, "read set mismatch:%s" % record.get("event"))
    return indexed


def _validate_header(rows):
    start = _single(rows, "start")
    identity = _single(rows, "identity_verified")
    _single(rows, "hooks_installed")
    summary = _single(rows, "summary")
    _single(rows, "detached")
    _single(rows, "end")

    _require(start.get("revision") == REVISION, "revision is not %s" % REVISION)
    _require(start.get("sha256") == EXECUTABLE_SHA256, "executable sha256 mismatch")
    hooks = start.get("hooks")
    _require(isinstance(hooks, list), "start record has no hooks")
    impacts = [hook for hook in hooks if hook.get("name") == IMPACT_HOOK]
    _require(len(impacts) == 1, "expected one impact hook")
    impact = impacts[0]
    _require(impact.get("va") == IMPACT_ADDRESS, "impact hook address mismatch")
    _require(impact.get("args") == 5, "impact hook argument count mismatch")
    _require(impact.get("sample_every") == 1, "sampling failure: impact hook is sampled")
    read_shape = {(read.get("source"), read.get("offset"), read.get("size"), read.get("phase"))
                  for read in impact.get("reads", [])}
    expected_shape = {("ecx", 8, 4, "enter"), ("ecx", 400, 4, "both"),
                      ("ecx", 412, 4, "both"), ("ecx", 416, 4, "both")}
    _require(read_shape == expected_shape, "impact hook read shape mismatch")

    module = identity.get("module") or {}
    _require(module.get("name", "").lower() == "wargame3.exe", "identity module name mismatch")
    _require(module.get("arch") == "ia32" and module.get("pointer_size") == 4, "identity is not ia32")
    _require(module.get("base") == "0x400000", "image base mismatch")
    _require(module.get("size") == IMAGE_SIZE, "image size mismatch")
    entries = [entry for entry in module.get("entries", []) if entry.get("name") == IMPACT_HOOK]
    _require(len(entries) == 1 and entries[0].get("address") == IMPACT_ADDRESS,
             "identity has no impact entry")
    _require(entries[0].get("executable") is True, "impact address is not executable")

    counts = summary.get("counts") or {}
    for key in ("suppressed", "callback_errors", "stale_frames", "stack_mismatches",
                "outstanding_threads", "gate_read_failures", "gate_ambiguities"):
        _require(summary.get(key) == 0, "summary failure:%s=%r" % (key, summary.get(key)))
    _require(isinstance(counts.get(IMPACT_HOOK), int), "summary has no impact count")
    end = _single(rows, "end")
    _require(end.get("cleanup_errors") == 0, "cleanup error")
    start_ts = _parse_timestamp(start.get("timestamp_utc"), "start")
    end_ts = _parse_timestamp(end.get("timestamp_utc"), "end")
    _require(start_ts <= end_ts, "start is after end")
    return start, summary, counts[IMPACT_HOOK]


def _pair_impacts(rows):
    enters = {}
    leaves = {}
    for line_number, row in enumerate(rows, 1):
        if row.get("event") == "enter" and row.get("hook") == IMPACT_HOOK:
            key = (row.get("thread_id"), row.get("call_id"))
            _require(key not in enters, "duplicate impact enter:%d" % line_number)
            enters[key] = (line_number, row)
        elif row.get("event") == "leave" and row.get("hook") == IMPACT_HOOK:
            key = (row.get("thread_id"), row.get("call_id"))
            _require(key not in leaves, "duplicate impact leave:%d" % line_number)
            leaves[key] = (line_number, row)
    _require(set(enters) == set(leaves), "missing impact pair: enters=%d leaves=%d"
             % (len(enters), len(leaves)))
    return [enters[key] for key in enters], leaves


def _build_event(enter_line, enter, leave_line, leave):
    where = "ordinal:%s" % enter.get("ordinal")
    module = _address(enter.get("ecx"), where + ":ecx")
    _require(module % 4 == 0, "unaligned module:%s" % where)
    _require(module >= IMAGE_BASE, "module address below image base:%s" % where)
    enter_reads = _index_reads(enter, module, ENTER_OFFSETS)
    leave_reads = _index_reads(leave, module, LEAVE_OFFSETS)
    _require(leave.get("stack_match") is True, "stack mismatch:%s" % where)
    _require(enter.get("return_address") == RETURN_ADDRESS, "unexpected return address:%s" % where)
    _require(enter.get("stale_frames_discarded") == 0, "stale frames:%s" % where)

    arguments = enter.get("args")
    _require(isinstance(arguments, list) and len(arguments) == 5, "argument count:%s" % where)
    mode_token = arguments[4]
    _require(mode_token in ("0x1", "0x2"), "unsupported mode:%s" % where)
    mode = int(mode_token, 16)
    arg0 = _float32_argument(arguments[0], where)
    _require(math.isfinite(arg0) and arg0 >= 0, "non-finite/negative input:%s" % where)

    handle = _u32_memory(enter_reads[HANDLE_OFFSET], where + ":handle")
    before = {offset: _float32_memory(enter_reads[offset], where + ":enter")
              for offset in (FIELD_0X190, FIELD_0X19C, FIELD_0X1A0)}
    after = {offset: _float32_memory(leave_reads[offset], where + ":leave")
             for offset in (FIELD_0X190, FIELD_0X19C, FIELD_0X1A0)}
    for offset in before:
        _require(math.isfinite(before[offset]) and math.isfinite(after[offset]),
                 "non-finite field:%s:0x%x" % (where, offset))

    changed = [offset for offset in (FIELD_0X190, FIELD_0X19C, FIELD_0X1A0)
               if enter_reads[offset] != leave_reads[offset]]
    expected = FIELD_0X190 if mode == 1 else FIELD_0X19C
    _require(changed == [expected], "transition fields %r do not match mode %d at %s"
             % (changed, mode, where))
    delta = after[expected] - before[expected]
    _require(delta > 0 and math.isfinite(delta), "non-increasing transition:%s" % where)
    _require(delta <= arg0 + 1e-3, "effective damage exceeds input:%s" % where)

    enter_time = _parse_timestamp(enter.get("timestamp_utc"), where + ":enter")
    leave_time = _parse_timestamp(leave.get("timestamp_utc"), where + ":leave")
    _require(enter_time <= leave_time, "enter after leave:%s" % where)

    ordinal = enter.get("ordinal")
    _require(isinstance(ordinal, int) and ordinal >= 1, "bad ordinal:%s" % where)
    kind = "suppression_increase" if mode == 1 else "physical_damage_increase"
    return {
        "ordinal": ordinal,
        "kind": kind,
        "mode": mode,
        "mode_arg4_raw": mode_token,
        "source": {
            "trace": None,  # filled by extract()
            "trace_sha256": None,
            "enter_line": enter_line,
            "leave_line": leave_line,
            "line_ref": "L%d-L%d" % (enter_line, leave_line),
        },
        "call": {
            "thread_id": enter.get("thread_id"),
            "call_id": enter.get("call_id"),
            "parent_call_id": enter.get("parent_call_id"),
            "parent_recorded": enter.get("parent_recorded") is True,
        },
        "module": {
            "label": None,
            "address": "0x%08x" % module,
            "address_u32": module,
            "raw_handle_u32": handle,
            "image_membership": image_membership(module),
        },
        "fields": {
            "0x190": {"before": before[FIELD_0X190], "after": after[FIELD_0X190],
                      "before_hex": enter_reads[FIELD_0X190],
                      "after_hex": leave_reads[FIELD_0X190]},
            "0x194": {"captured": False, "value": None,
                      "note": "MaxDamages is not in the hook read set"},
            "0x19c": {"before": before[FIELD_0X19C], "after": after[FIELD_0X19C],
                      "before_hex": enter_reads[FIELD_0X19C],
                      "after_hex": leave_reads[FIELD_0X19C]},
            "0x1a0": {"before": before[FIELD_0X1A0], "after": after[FIELD_0X1A0],
                      "before_hex": enter_reads[FIELD_0X1A0],
                      "after_hex": leave_reads[FIELD_0X1A0]},
        },
        "arg0_float32": arg0,
        "arg0_raw": arguments[0],
        "observed_delta": delta,
        "changed_fields": ["0x%x" % offset for offset in changed],
        "identity": {
            "unit": None,
            "player": None,
            "basis": "no captured module-to-entity or entity-to-unit bridge",
        },
        "time": {
            "frame": None,
            "simulation_time": None,
            "game_time": None,
            "wallclock_enter_utc": enter.get("timestamp_utc"),
            "wallclock_leave_utc": leave.get("timestamp_utc"),
            "relative_wallclock_seconds": None,
            "basis": "guest wall-clock observation only; not replay, simulation or game time",
        },
        "kill": {
            "outcome": None,
            "destruction_observed": False,
            "basis": "no destruction hook, removal capture or unit identity",
        },
        "causation": {
            "shooter": None,
            "weapon": None,
            "basis": ("parent dispatcher sampled out" if enter.get("parent_recorded") is not True
                      else "parent recorded, but no shooter/weapon identity was captured"),
        },
        "_enter_time": enter_time,
        "_leave_time": leave_time,
    }


def _module_label_order(events):
    labels = {}
    for event in sorted(events, key=lambda item: item["ordinal"]):
        address = event["module"]["address"]
        if address not in labels:
            labels[address] = "M%d" % (len(labels) + 1)
    return labels


def _module_histories(events):
    by_module = {}
    for event in events:
        by_module.setdefault(event["module"]["label"], []).append(event)
    histories = []
    for label in sorted(by_module, key=lambda value: int(value[1:])):
        group = sorted(by_module[label], key=lambda item: item["ordinal"])
        suppression = [event for event in group if event["mode"] == 1]
        physical = [event for event in group if event["mode"] == 2]
        histories.append({
            "label": label,
            "address": group[0]["module"]["address"],
            "raw_handle_u32": group[0]["module"]["raw_handle_u32"],
            "image_membership": group[0]["module"]["image_membership"],
            "event_count": len(group),
            "event_ordinals": [event["ordinal"] for event in group],
            "suppression": {
                "applications": len(suppression),
                "observed_peak": max((event["fields"]["0x190"]["after"] for event in suppression),
                                     default=None),
                "last_observed": group[-1]["fields"]["0x190"]["after"],
            },
            "physical": {
                "applications": len(physical),
                "observed_max": max((event["fields"]["0x19c"]["after"] for event in physical),
                                    default=None),
                "transitions": [
                    {
                        "ordinal": event["ordinal"],
                        "before": event["fields"]["0x19c"]["before"],
                        "after": event["fields"]["0x19c"]["after"],
                    }
                    for event in physical
                ],
            },
            "identity": None,
            "kill": None,
            "wallclock_first_utc": group[0]["time"]["wallclock_enter_utc"],
            "wallclock_last_utc": group[-1]["time"]["wallclock_enter_utc"],
        })
    return histories


def _divisor_fits(loss):
    """Test how each candidate value granularity divides one observed loss."""
    fits = []
    for divisor in DECAY_DIVISORS:
        units = round(loss / divisor)
        residual = loss - units * divisor
        fits.append({
            "divisor": divisor,
            "units": units,
            "residual": residual,
            "integral": units >= 1 and abs(residual) <= QUANTIZATION_TOLERANCE,
        })
    return fits


def _decay_observations(events):
    observations = []
    by_module = {}
    for event in events:
        by_module.setdefault(event["module"]["label"], []).append(event)
    for label, group in by_module.items():
        group = sorted(group, key=lambda item: item["ordinal"])
        for previous, current in zip(group, group[1:]):
            loss = previous["fields"]["0x190"]["after"] - current["fields"]["0x190"]["before"]
            if loss <= 0:
                continue
            wall = current["time"]["relative_wallclock_seconds"] - previous["time"]["relative_wallclock_seconds"]
            fits = _divisor_fits(loss)
            observations.append({
                "module": label,
                "from_ordinal": previous["ordinal"],
                "to_ordinal": current["ordinal"],
                "observed_loss": loss,
                "divisor_fits": fits,
                "integral_divisors": [fit["divisor"] for fit in fits if fit["integral"]],
                "wallclock_seconds": wall,
            })
    return observations


def _wallclock_span(entries):
    values = [entry["wallclock_seconds"] for entry in entries]
    return {"count": len(values), "min": min(values, default=None),
            "max": max(values, default=None)}


def _timing(events):
    first = min(event["_enter_time"] for event in events)
    last = max(event["_enter_time"] for event in events)
    decay = _decay_observations(events)
    short = [entry for entry in decay if entry["wallclock_seconds"] < 1.0]
    long = [entry for entry in decay if entry["wallclock_seconds"] > 10.0]
    fit_counts = {}
    for divisor in DECAY_DIVISORS:
        fit_counts["%g" % divisor] = sum(
            1 for entry in decay
            if any(fit["divisor"] == divisor and fit["integral"] for fit in entry["divisor_fits"]))
    equal_divisors = [divisor for divisor in DECAY_DIVISORS
                      if decay and fit_counts["%g" % divisor] == len(decay)]
    unique_divisor = equal_divisors[0] if len(equal_divisors) == 1 else None
    decay_note = ""
    if decay and equal_divisors:
        decay_note = (
            " Suppression declines are not quantized on a resolvable time base: each "
            "observed loss (%d) fits %s value units to within %.3f, so the divisor is not "
            "identified and no engine step count can be derived."
            % (len(decay), ", ".join("%g" % divisor for divisor in equal_divisors),
               QUANTIZATION_TOLERANCE))
    elif decay:
        decay_note = (
            " Suppression declines are not quantized on a resolvable time base: no single "
            "candidate value granularity divides all %d observed losses." % len(decay))
    return {
        "basis": "guest wall-clock observation only",
        "frame": None,
        "simulation_time": None,
        "game_time": None,
        "first_impact_wallclock_utc": first.isoformat().replace("+00:00", "Z"),
        "last_impact_wallclock_utc": last.isoformat().replace("+00:00", "Z"),
        "impact_window_wallclock_seconds": (last - first).total_seconds(),
        "frame_to_time_conversion": None,
        "hypotheses": [
            {
                "id": "H1_5.01_fps",
                "claim": "The replay advances about 5.01 frames per second.",
                "status": "not_supported_by_trace",
                "reason": ("No trace record carries a frame index or simulation time. "
                           "The figure depends on an external frame count and playback "
                           "interval, not an in-trace counter." + decay_note),
            },
            {
                "id": "H2_battle_start_frame_2914",
                "claim": "The battle starts at replay frame 2914.",
                "status": "not_supported_by_trace",
                "reason": ("No frame index or replay binding exists in this trace. The only "
                           "frame-2914 evidence is a 0x13 synchronization append in a different "
                           "artifact; that opcode does not establish battle start."),
            },
            {
                "id": "H3_three_kills_from_three_transitions",
                "claim": "The three physical-damage transitions are three kills.",
                "status": "rejected",
                "reason": ("Three mode-2 transitions are observed, but MaxDamages (+0x194), the "
                           "destruction path, unit identity and any removal/kill record are absent. "
                           "Damage accumulation is not a kill outcome."),
            },
        ],
        "decay_observations": decay,
        "decay_summary": {
            "declines": len(decay),
            "candidate_divisors": list(DECAY_DIVISORS),
            "divisor_fit_counts": fit_counts,
            "equal_fit_divisors": equal_divisors,
            "unique_divisor": unique_divisor,
            "quantization_tolerance": QUANTIZATION_TOLERANCE,
            "short_interval_wallclock_seconds": _wallclock_span(short),
            "long_interval_wallclock_seconds": _wallclock_span(long),
            "warning": ("0.6 is an assumed audit value granularity, not an engine step and not "
                        "a measured period. The data cannot select it over 0.3, 0.2, 0.1 or "
                        "0.05, and the trace carries no frame or step counter, so no step "
                        "rate is asserted."),
        },
    }


def _crosscheck_classified(classified, classified_sha256, manifest):
    _require(classified.get("trace_sha256") == manifest["source"]["sha256"],
             "classified trace sha256 mismatch")
    _require(classified.get("executable_sha256") == EXECUTABLE_SHA256,
             "classified executable sha256 mismatch")
    classified_events = classified.get("events")
    _require(isinstance(classified_events, list), "classified file has no events")
    ours = manifest["events"]
    _require(len(classified_events) == len(ours),
             "classified event count %d != recomputed %d" % (len(classified_events), len(ours)))
    by_ordinal = {}
    for event in classified_events:
        ordinal = event.get("ordinal")
        _require(ordinal not in by_ordinal, "duplicate classified ordinal:%r" % ordinal)
        by_ordinal[ordinal] = event
    _require(set(by_ordinal) == {event["ordinal"] for event in ours},
             "classified ordinals do not match recomputed events")
    checked = []
    for event in ours:
        other = by_ordinal[event["ordinal"]]
        where = "classified ordinal %d" % event["ordinal"]
        checks = {
            "call_id": other.get("call_id") == event["call"]["call_id"],
            "thread_id": other.get("thread_id") == event["call"]["thread_id"],
            "enter_line": (other.get("source") or {}).get("enter_line") == event["source"]["enter_line"],
            "leave_line": (other.get("source") or {}).get("leave_line") == event["source"]["leave_line"],
            "module": other.get("runtime_module_address") == event["module"]["address"],
            "handle": other.get("runtime_handle_raw_u32") == event["module"]["raw_handle_u32"],
            "kind": other.get("kind") == event["kind"],
            "changed_fields": other.get("changed_fields") == event["changed_fields"],
            "arg0": math.isclose(other.get("arg0_float32", math.nan), event["arg0_float32"],
                                 rel_tol=0, abs_tol=1e-6),
            "delta": math.isclose(other.get("observed_delta", math.nan),
                                  event["observed_delta"], rel_tol=0, abs_tol=1e-6),
            "frame_is_unknown": other.get("frame") is None,
            "simulation_time_is_unknown": other.get("simulation_time") is None,
            "unit_is_unknown": other.get("unit_identity") is None,
            "player_is_unknown": other.get("player_identity") is None,
        }
        for field in ("0x190", "0x19c", "0x1a0"):
            for phase in ("before", "after"):
                expected = event["fields"][field][phase]
                actual = ((other.get(phase) or {}).get(field) or {}).get("float32", math.nan)
                checks["%s_%s" % (field, phase)] = math.isclose(
                    actual, expected, rel_tol=0, abs_tol=1e-6)
        failed = sorted(name for name, ok in checks.items() if not ok)
        _require(not failed, "%s differs in: %s" % (where, ", ".join(failed)))
        checked.append(event["ordinal"])
    return {
        "status": "match",
        "sha256": classified_sha256,
        "events": len(checked),
        "matched_events": len(checked),
        "fields_checked": ["ordinal", "call_id", "thread_id", "enter_line", "leave_line",
                           "module", "handle", "kind", "changed_fields", "arg0", "delta",
                           "0x190", "0x19c", "0x1a0", "unknown_time_identity"],
    }


def _image_correction(modules):
    """Score the inside-image claim from the observed module addresses."""
    membership = [module["image_membership"] for module in modules]
    _require(all(item["offset_bytes"] is not None for item in membership),
             "module address below image base")
    inside = [item for item in membership if item["inside_image"]]
    outside = [item for item in membership if not item["inside_image"]]
    offsets = [item["offset_bytes"] for item in membership]
    outside_offsets = [item["offset_bytes"] for item in outside]
    total = len(membership)
    head = ("Image range 0x%08x-0x%08x is %d bytes. "
            % (IMAGE_BASE, IMAGE_BASE + IMAGE_SIZE, IMAGE_SIZE))
    if not inside:
        status = "rejected_by_arithmetic"
        detail = (head + "All %d observed module addresses are outside it; the closest is "
                  "%d bytes from the image base." % (total, min(offsets)))
        implication = ("Do not describe these objects as image/.data residents without "
                       "a section-table or allocation capture.")
    elif not outside:
        status = "confirmed_by_arithmetic"
        detail = (head + "All %d observed module addresses fall inside it, at offsets "
                  "%d-%d bytes from the image base." % (total, min(offsets), max(offsets)))
        implication = ("Arithmetic image membership alone does not establish section "
                       "ownership; a section-table or allocation capture is still required.")
    else:
        status = "partially_confirmed_by_arithmetic"
        detail = (head + "%d of %d observed module addresses fall inside it and %d outside; "
                  "the closest outside address is %d bytes from the image base."
                  % (len(inside), total, len(outside), min(outside_offsets)))
        implication = ("Mixed membership: neither the inside-image claim nor its rejection "
                       "holds for every module; a section-table or allocation capture is "
                       "required per module.")
    return {
        "claim": "The captured damage-module objects lie inside the loaded executable image.",
        "status": status,
        "detail": detail,
        "observed": {
            "module_addresses_checked": total,
            "inside_image": len(inside),
            "outside_image": len(outside),
            "minimum_offset_bytes": min(offsets),
            "minimum_outside_offset_bytes": min(outside_offsets) if outside_offsets else None,
            "image_size_bytes": IMAGE_SIZE,
        },
        "implication": implication,
    }


def extract(rows, source_name, source_sha256, line_count, classified=None,
            classified_sha256=None):
    """Recompute the event manifest from parsed trace rows."""
    start, summary, impact_count = _validate_header(rows)
    enter_pairs, leaves = _pair_impacts(rows)
    _require(impact_count == len(enter_pairs),
             "summary impact count %d != paired events %d" % (impact_count, len(enter_pairs)))
    events = []
    for enter_line, enter in enter_pairs:
        key = (enter.get("thread_id"), enter.get("call_id"))
        leave_line, leave = leaves[key]
        events.append(_build_event(enter_line, enter, leave_line, leave))
    events.sort(key=lambda item: item["ordinal"])
    _require(events, "no impact events in trace")
    _require([event["ordinal"] for event in events] == list(range(1, len(events) + 1)),
             "impact ordinals are not contiguous from 1")
    labels = _module_label_order(events)
    first_time = min(event["_enter_time"] for event in events)
    for event in events:
        event["module"]["label"] = labels[event["module"]["address"]]
        event["source"]["trace"] = source_name
        event["source"]["trace_sha256"] = source_sha256
        event["time"]["relative_wallclock_seconds"] = (
            event["_enter_time"] - first_time).total_seconds()

    modules = _module_histories(events)
    timing = _timing(events)
    for event in events:
        del event["_enter_time"]
        del event["_leave_time"]
    starts = [row for row in rows if row.get("event") == "start"]
    start_record = starts[0]
    parent_recorded = sum(1 for event in events if event["call"]["parent_recorded"])
    manifest = {
        "schema": SCHEMA,
        "status": "partial_evidence",
        "source": {
            "trace": source_name,
            "sha256": source_sha256,
            "line_count": line_count,
            "revision": start_record.get("revision"),
            "executable_sha256": start_record.get("sha256"),
            "image": {"base": "0x%08x" % IMAGE_BASE, "size": IMAGE_SIZE,
                      "end": "0x%08x" % (IMAGE_BASE + IMAGE_SIZE)},
        },
        "integrity": {
            "impact_enters": len(enter_pairs),
            "impact_leaves": len(leaves),
            "paired": len(events),
            "ordinals_contiguous": True,
            "impact_hook_sample_every": 1,
            "parent_recorded": parent_recorded,
            "parent_unrecorded": len(events) - parent_recorded,
            "suppressed_events": summary.get("suppressed"),
            "callback_errors": summary.get("callback_errors"),
            "stack_mismatches": summary.get("stack_mismatches"),
            "stale_frames": summary.get("stale_frames"),
            "read_failures": 0,
            "summary_impact_count": impact_count,
        },
        "unknowns": {
            "unit_identity": None,
            "player_identity": None,
            "frame": None,
            "simulation_time": None,
            "game_time": None,
            "kill_outcome": None,
            "max_damages": None,
            "shooter": None,
            "weapon": None,
            "reasons": {
                "identity": "no module-to-entity or entity-to-unit bridge was captured",
                "time": "no trace record carries a replay frame or simulation clock",
                "kill": "no destruction, removal or score record was captured",
                "max_damages": "+0x194 is not in the hook read set",
                "causation": "27 of 28 parent dispatcher calls were sampled out",
            },
        },
        "modules": modules,
        "events": events,
        "timing": timing,
        "corrections": [_image_correction(modules)],
    }
    if classified is not None:
        _require(classified_sha256 is not None,
                 "classified cross-check requires its sha256")
        manifest["integrity"]["classification"] = _crosscheck_classified(
            classified, classified_sha256, manifest)
    else:
        manifest["integrity"]["classification"] = {
            "status": "not_requested", "events": None, "matched_events": 0}
    return manifest


def extract_file(trace_path, expect_sha256=TRACE_SHA256, classified_path=None,
                 expect_classified_sha256=None):
    rows, name, digest, line_count = load_trace(trace_path, expect_sha256)
    classified = None
    if classified_path is not None:
        data = Path(classified_path).read_bytes()
        classified_sha256 = hashlib.sha256(data).hexdigest()
        _require(expect_classified_sha256 is not None,
                 "classified cross-check requires --expect-classified-sha256")
        _require(classified_sha256 == expect_classified_sha256,
                 "classified sha256 mismatch: %s" % classified_sha256)
        try:
            classified = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise AarTraceError("invalid classified json:%s" % error) from None
        _require(isinstance(classified, dict), "classified root is not an object")
    return extract(rows, name, digest, line_count, classified, expect_classified_sha256)


def _event_line(event):
    field = "0x190" if event["mode"] == 1 else "0x19c"
    values = event["fields"][field]
    return (
        "- **%s** `T+%.3fs` ord %d | call %s | %s/h%d | mode %d | %s %s "
        "%.6f -> %.6f (delta %.6f) | unit=UNKNOWN player=UNKNOWN frame=UNKNOWN "
        "sim_time=UNKNOWN game_time=UNKNOWN kill=UNKNOWN"
        % (event["source"]["line_ref"], event["time"]["relative_wallclock_seconds"],
           event["ordinal"], event["call"]["call_id"], event["module"]["label"],
           event["module"]["raw_handle_u32"], event["mode"], event["kind"], field,
           values["before"], values["after"], event["observed_delta"])
    )


def render_chronology(manifest):
    source = manifest["source"]
    lines = [
        "# Damage-event chronology",
        "",
        "Source: `%s` SHA-256 `%s` (%d lines), read-only."
        % (source["trace"], source["sha256"], source["line_count"]),
        "Executable: revision %s, SHA-256 `%s`."
        % (source["revision"], source["executable_sha256"]),
        "",
        "Every `Lx-Ly` reference resolves to the paired enter/leave records in that "
        "exact file and hash. `T+` is relative guest wall-clock observation from the "
        "first impact; it is not replay, simulation or game time.",
        "",
        "## Events",
        "",
    ]
    lines.extend(_event_line(event) for event in manifest["events"])
    lines.extend([
        "",
        "## Module histories",
        "",
        "| module | raw handle | events | suppression | peak 0x190 | physical | physical 0x19c |",
        "|---|---:|---:|---:|---:|---:|---|",
    ])
    for module in manifest["modules"]:
        physical = module["physical"]["transitions"]
        physical_text = ", ".join("%.1f -> %.1f" % (item["before"], item["after"])
                                  for item in physical) or "-"
        lines.append("| %s | %d | %d | %d | %s | %d | %s |" % (
            module["label"], module["raw_handle_u32"], module["event_count"],
            module["suppression"]["applications"],
            "%.6f" % module["suppression"]["observed_peak"]
            if module["suppression"]["observed_peak"] is not None else "-",
            module["physical"]["applications"], physical_text))
    lines.extend([
        "",
        "Each module has `unit=UNKNOWN`, `player=UNKNOWN` and `kill=UNKNOWN`: the "
        "raw `+0x08` value is an unauthenticated candidate handle, not an entity id.",
        "",
        "## Timing assessment",
        "",
        "Frame and simulation time are `null` for all %d events. The hypotheses in "
        "`summary.json` are not promoted to observations." % len(manifest["events"]),
        "",
        "- H1 (5.01 fps): not supported by this trace; no in-trace frame counter exists.",
        "- H2 (battle start frame 2914): not supported; no frame index or replay binding exists.",
        "- H3 (three kills from three transitions): rejected; no destruction or identity evidence.",
        "",
        "## Image-range correction",
        "",
        manifest["corrections"][0]["detail"],
        "",
        "Status: `%s`. `events.json` keeps the per-module `image_membership` arithmetic."
        % manifest["corrections"][0]["status"],
        "",
    ])
    return "\n".join(lines)


def _json_text(value):
    return json.dumps(value, indent=2, allow_nan=False) + "\n"


def write_outputs(manifest, out_dir):
    """Exclusively create events.json, summary.json and chronology.md."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "events.json": _json_text(manifest),
        "summary.json": _json_text({key: value for key, value in manifest.items()
                                    if key != "events"}),
        "chronology.md": render_chronology(manifest),
    }
    targets = [out_dir / name for name in payloads]
    existing = [str(path) for path in targets if path.exists()]
    _require(not existing, "refusing to overwrite existing output: %s" % ", ".join(existing))
    created = []
    try:
        for path in targets:
            with open(path, "x", encoding="utf-8", newline="\n") as handle:
                handle.write(payloads[path.name])
                created.append(path)
    except FileExistsError as error:
        for path in created:
            path.unlink()
        raise AarTraceError("output appeared during write: %s" % error) from None
    return targets


# ---------------------------------------------------------------------------
# Runtime profile (build 131544 capture with type and destruction hooks)
#
# This profile is additive: the legacy extractor above keeps its pinned
# trace, output keys and chronology unchanged. The runtime profile reads a
# different trace shape, joins two captured descriptor GUID/token pairs to a
# hash-pinned native unit index, and exports independently witnessed
# damage -> threshold -> destruction call chains. It never promotes inferred
# source roles to proven shooters or observed destruction calls to kills.
# ---------------------------------------------------------------------------

RUNTIME_SCHEMA = "wgrd-aar-runtime-events/1"
RUNTIME_UNITS_SCHEMA = "wgrd-aar-runtime-units/1"
RUNTIME_TRACE_SHA256 = "607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74"
RUNTIME_INDEX_SHA256 = "73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d"
RUNTIME_ARCHIVE_SHA256 = "172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b"
RUNTIME_REVISION = "131544"

RUNTIME_CLOCK = {
    "hook": "clock_sample_candidate",
    "va": "0xaaedf0",
    "global_pointer_slot": "0x201d318",
    "counter_offset": "0xd0",
    "scale_constant_va": "0x195d768",
    "scale_constant_bits": "0x3e4ccccd",
    "scale_constant_float": 0.2,
    "module_store_offset": "0x1ec",
    "static_binding": {
        "file": "deterministic-clock-bindings.asm",
        "sha256": "b0e2177f5542710a0c8273fc76c72fa04dd14c0a1f0011d54d4aafe645dfe974",
        "seconds_entry": "0x1d9cd68 DeterministicCurrentTimeInSeconds -> 0xa406b0",
        "ticks_entry": "0x1d9cd78 DeterministicCurrentTimeInTicks -> 0xa40780",
        "setter_entry": "0x1d9cd88 -> 0xa41bc0",
        "summary": ("The engine-named deterministic seconds accessor loads the "
                    "container from global 0x201d318 and calls 0xaaedf0; the "
                    "ticks accessor pushes [container+0xd0]. 0xaaedf0 converts "
                    "[ecx+0xd0] to float and multiplies by the constant at "
                    "0x195d768 (0x3e4ccccd = 0.2f)."),
    },
    "proof_level": "engine_named_clock_static_path_and_observed_module_store",
    "verified_unknowns": ["epoch", "replay_frame", "simulation_time",
                          "game_time", "battle_time"],
}

# name -> (va, args, sample_every, read shape)
# read shape entries: (source, offset, size, phase, indirect)
RUNTIME_HOOK_SPECS = {
    "impact_apply_candidate": {
        "va": "0xc9f910", "args": 5, "sample_every": 1,
        "reads": (("ecx", 0, 16, "enter", False),
                  ("ecx", 400, 96, "both", False),
                  ("ecx", 4, 128, "enter", True),
                  ("arg1", 0, 128, "enter", False),
                  ("arg2", 0, 128, "enter", False)),
    },
    "destruction_check_candidate": {
        "va": "0xc9bf20", "args": 1, "sample_every": 1,
        "reads": (("ecx", 0, 16, "enter", False),
                  ("ecx", 400, 96, "both", False)),
    },
    "owner_destroy_candidate": {
        "va": "0xa75c70", "args": 1, "sample_every": 1,
        "reads": (("ecx", 0, 128, "both", False),
                  ("ecx", 4, 128, "enter", True)),
    },
    "clock_sample_candidate": {
        "va": "0xaaedf0", "args": 0, "sample_every": 997,
        "reads": (("ecx", 208, 4, "enter", False),),
    },
    "order_request_wrapper": {
        "va": "0xb2be30", "args": 2, "sample_every": 1,
        "reads": (("ecx", 4, 20, "enter", False),
                  ("ecx", 88, 4, "enter", False),
                  ("ecx", 208, 36, "enter", False)),
    },
    "reference_remap": {
        "va": "0xae4830", "args": 1, "sample_every": 1,
        "reads": (("arg0", 0, 4, "enter", False),
                  ("retval", 0, 4, "leave", False)),
    },
    "reference_lookup": {
        "va": "0xae48d0", "args": 2, "sample_every": 1,
        "reads": (("retval", 0, 128, "leave", False),),
    },
    "owner_lookup_candidate": {
        "va": "0xc52de0", "args": 0, "sample_every": 997,
        "reads": (("ecx", 8, 4, "enter", False),
                  ("retval", 0, 128, "leave", False)),
    },
}

RUNTIME_IMPACT_HOOK = "impact_apply_candidate"
RUNTIME_CHECK_HOOK = "destruction_check_candidate"
RUNTIME_DESTROY_HOOK = "owner_destroy_candidate"
RUNTIME_CLOCK_HOOK = "clock_sample_candidate"
RUNTIME_LOOKUP_HOOK = "owner_lookup_candidate"
RUNTIME_CHECK_RETURN_ADDRESS = "0xc95344"
RUNTIME_DESTROY_LIFECYCLE_RETURN = "0xc9c0ce"
RUNTIME_DESTROY_CLEANUP_RETURN = "0xb7c408"
RUNTIME_DAMAGE_FIELDS = (0x190, 0x194, 0x198, 0x19C, 0x1A0, 0x1EC)

# Capture-side pins published next to the trace. The embedded start record is
# checked against the expected hook shape. File-based extraction also verifies
# retained capture-era source copies; current working files are not substitutes.
RUNTIME_CAPTURE_CONFIG = {
    "file": "aar-capture-131544.json",
    "sha256": "f904c7ed526129148fc41857ee3e981f5531cc26c3c3b684f85c2ebfe7e25ba0",
}
RUNTIME_CAPTURE_SOURCE_PINS = {
    "hooks.js": "f398ffa3febc93dfd5ea733866a5464eec9e277f9613f58bd17602e72fbc158e",
    "wgrd_frida.py": "3d3cb50212f0731367203cfbb6eb62d7ada9a37f2e5130002ff842987164c0bc",
}


def _rt_read_record(record, source, offset, size, phase, where):
    matches = [read for read in record.get("reads") or []
               if read.get("source") == source and read.get("offset") == offset
               and read.get("size") == size]
    _require(len(matches) == 1, "expected one %s+%d read at %s" % (source, offset, where))
    read = matches[0]
    _require(read.get("phase") == phase,
             "read phase mismatch %s+%d at %s" % (source, offset, where))
    return read


def _rt_bytes(read, where, allow_failure=False):
    result = read.get("result") or {}
    if result.get("ok") is not True:
        _require(allow_failure, "read failure at %s" % where)
        return None
    value = result.get("hex")
    _require(isinstance(value, str) and value, "empty read at %s" % where)
    try:
        data = bytes.fromhex(value)
    except ValueError as error:
        raise AarTraceError("bad read hex at %s:%s" % (where, error)) from None
    _require(len(data) == read.get("size"), "read size mismatch at %s" % where)
    return data


def _rt_u32(data, offset, where):
    _require(0 <= offset <= len(data) - 4, "u32 out of range at %s" % where)
    return struct.unpack_from("<I", data, offset)[0]


def _rt_f32(data, offset, where):
    _require(0 <= offset <= len(data) - 4, "f32 out of range at %s" % where)
    return struct.unpack_from("<f", data, offset)[0]


def _rt_records(rows):
    grouped = {name: {"enter": [], "leave": []} for name in RUNTIME_HOOK_SPECS}
    for line_number, row in enumerate(rows, 1):
        hook = row.get("hook")
        event = row.get("event")
        if hook in grouped and event in ("enter", "leave"):
            grouped[hook][event].append((line_number, row))
    return grouped


def _rt_pairs(grouped, name):
    spec = RUNTIME_HOOK_SPECS[name]
    enters = {}
    leaves = {}
    for line_number, record in grouped[name]["enter"]:
        key = (record.get("thread_id"), record.get("call_id"))
        _require(key not in enters, "duplicate %s enter:%d" % (name, line_number))
        _require(record.get("stale_frames_discarded") == 0,
                 "stale frames in %s:%d" % (name, line_number))
        enters[key] = (line_number, record)
    for line_number, record in grouped[name]["leave"]:
        key = (record.get("thread_id"), record.get("call_id"))
        _require(key not in leaves, "duplicate %s leave:%d" % (name, line_number))
        leaves[key] = (line_number, record)
    _require(set(enters) == set(leaves), "%s missing pair: enters=%d leaves=%d"
             % (name, len(enters), len(leaves)))
    pairs = []
    for key, (enter_line, enter) in enters.items():
        leave_line, leave = leaves[key]
        _require(leave.get("stack_match") is True, "stack mismatch in %s:%d" % (name, enter_line))
        enter_time = _parse_timestamp(enter.get("timestamp_utc"), "%s:%d" % (name, enter_line))
        leave_time = _parse_timestamp(leave.get("timestamp_utc"), "%s:%d" % (name, leave_line))
        _require(enter_time <= leave_time, "%s enter after leave:%d" % (name, enter_line))
        ordinal = enter.get("ordinal")
        _require(isinstance(ordinal, int) and ordinal >= 1, "bad ordinal in %s:%d" % (name, enter_line))
        pairs.append((ordinal, enter_line, enter, leave_line, leave))
    pairs.sort(key=lambda item: item[1])
    ordinals = [item[0] for item in pairs]
    _require(len(set(ordinals)) == len(ordinals), "duplicate %s ordinals" % name)
    stride = spec["sample_every"]
    if stride == 1:
        _require(ordinals == list(range(1, len(ordinals) + 1)),
                 "%s ordinals are not contiguous from 1" % name)
    else:
        _require(all((ordinal - 1) % stride == 0 for ordinal in ordinals),
                 "%s ordinals do not follow stride %d" % (name, stride))
    return pairs


def _rt_validate_header(rows):
    start = _single(rows, "start")
    identity = _single(rows, "identity_verified")
    _single(rows, "hooks_installed")
    summary = _single(rows, "summary")
    detached = _single(rows, "detached")
    end = _single(rows, "end")

    _require(start.get("revision") == RUNTIME_REVISION,
             "revision is not %s" % RUNTIME_REVISION)
    _require(start.get("sha256") == EXECUTABLE_SHA256, "runtime executable sha256 mismatch")
    hooks = start.get("hooks")
    _require(isinstance(hooks, list), "start record has no hooks")
    seen = {}
    for hook in hooks:
        name = hook.get("name")
        _require(name in RUNTIME_HOOK_SPECS, "unexpected hook %r" % name)
        _require(name not in seen, "duplicate hook %r" % name)
        spec = RUNTIME_HOOK_SPECS[name]
        _require(hook.get("va") == spec["va"], "%s hook address mismatch" % name)
        _require(hook.get("args") == spec["args"], "%s argument count mismatch" % name)
        _require(hook.get("sample_every") == spec["sample_every"],
                 "%s sampling mismatch" % name)
        shape = {(read.get("source"), read.get("offset"), read.get("size"),
                  read.get("phase"), bool(read.get("indirect", False)))
                 for read in hook.get("reads") or []}
        _require(shape == set(spec["reads"]), "%s read shape mismatch" % name)
        seen[name] = hook
    _require(set(seen) == set(RUNTIME_HOOK_SPECS), "runtime hook set mismatch")

    module = identity.get("module") or {}
    _require(module.get("name", "").lower() == "wargame3.exe", "identity module name mismatch")
    _require(module.get("arch") == "ia32" and module.get("pointer_size") == 4,
             "identity is not ia32")
    _require(module.get("base") == "0x400000", "image base mismatch")
    _require(module.get("size") == IMAGE_SIZE, "image size mismatch")
    entries = {}
    for entry in module.get("entries") or []:
        entries[entry.get("name")] = entry
    _require(set(entries) == set(RUNTIME_HOOK_SPECS), "identity hook set mismatch")
    for name, spec in RUNTIME_HOOK_SPECS.items():
        _require(entries[name].get("address") == spec["va"],
                 "identity address mismatch for %s" % name)
        _require(entries[name].get("executable") is True,
                 "identity address not executable for %s" % name)

    for key in ("suppressed", "callback_errors", "stale_frames", "stack_mismatches",
                "outstanding_threads", "gate_read_failures", "gate_ambiguities",
                "gate_suspended_threads"):
        _require(summary.get(key) == 0, "summary failure:%s=%r" % (key, summary.get(key)))
    counts = summary.get("counts")
    _require(isinstance(counts, dict) and set(counts) == set(RUNTIME_HOOK_SPECS),
             "summary hook counts mismatch")
    _require(detached.get("reason") == "application-requested",
             "unexpected detach reason:%r" % detached.get("reason"))
    _require(end.get("cleanup_errors") == 0, "cleanup error")
    if _parse_timestamp(start.get("timestamp_utc"), "start") > \
            _parse_timestamp(end.get("timestamp_utc"), "end"):
        raise AarTraceError("start is after end")
    return start, summary


def _rt_check_counts(summary, pairs_by_hook):
    counts = summary["counts"]
    total_enters = 0
    for name, pairs in pairs_by_hook.items():
        total_enters += len(pairs)
        stride = RUNTIME_HOOK_SPECS[name]["sample_every"]
        total = counts[name]
        if stride == 1:
            _require(total == len(pairs), "%s count %d != paired %d"
                     % (name, total, len(pairs)))
        else:
            expected = (total - 1) // stride + 1 if total else 0
            _require(expected == len(pairs),
                     "%s emitted count %d != stride arithmetic %d"
                     % (name, len(pairs), expected))
            _require(pairs[-1][0] == (len(pairs) - 1) * stride + 1,
                     "%s last sampled ordinal mismatch" % name)
            _require(pairs[-1][0] <= total, "%s sampled ordinal exceeds count" % name)
    _require(summary.get("emitted") == 2 * total_enters,
             "summary emitted %r != enter+leave records %d"
             % (summary.get("emitted"), 2 * total_enters))
    return total_enters


def _rt_load_index(path, expect_sha256):
    path = Path(path)
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    _require(digest == expect_sha256, "unit index sha256 mismatch: %s" % digest)
    try:
        index = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AarTraceError("invalid unit index json:%s" % error) from None
    _require(isinstance(index, dict), "unit index root is not an object")
    _require(index.get("game_build") == RUNTIME_REVISION,
             "unit index build mismatch:%r" % index.get("game_build"))
    source = index.get("source") or {}
    _require(source.get("sha256") == RUNTIME_ARCHIVE_SHA256,
             "unit index archive sha256 mismatch")
    _require(source.get("build") == RUNTIME_REVISION,
             "unit index archive build mismatch")
    _require(isinstance(index.get("unit_types"), dict) and index["unit_types"],
             "unit index has no unit types")
    _require(isinstance(index.get("descriptors"), dict), "unit index has no descriptors")
    return index, digest, path.name


def _rt_descriptor_join(index, guid_hex, token_hex):
    unit_types = index["unit_types"]
    descriptors = index["descriptors"]
    guid_hits = [node for node, unit in unit_types.items()
                 if unit.get("descriptor_guid_hex") == guid_hex]
    token_hits = [node for node, unit in unit_types.items()
                  if unit.get("name_token") == token_hex]
    entry = descriptors.get(guid_hex) if isinstance(descriptors, dict) else None
    result = {
        "guid_hex": guid_hex,
        "name_token_hex": token_hex,
        "guid_matches": len(guid_hits),
        "guid_unique": len(guid_hits) == 1,
        "token_matches": len(token_hits),
        "token_unique": len(token_hits) == 1,
        "descriptor_index_entry": bool(entry),
        "unit_type_id": None,
        "debug_name": None,
        "ndf_class": None,
        "candidate_path": None,
        "status": "unverified",
        "confidence": "none",
    }
    if entry is None:
        result["status"] = "guid_not_in_index"
        return result
    candidates = entry.get("candidates") if isinstance(entry, dict) else None
    if not isinstance(candidates, list) or len(candidates) != 1:
        result["status"] = "ambiguous_or_missing_candidates"
        return result
    candidate = candidates[0]
    node = str(candidate.get("unit_type_id"))
    unit = unit_types.get(node)
    result["candidate_path"] = candidate.get("path")
    if unit is None:
        result["status"] = "candidate_unit_type_missing"
        return result
    if unit.get("descriptor_guid_hex") != guid_hex:
        result["status"] = "candidate_guid_mismatch"
        return result
    if unit.get("name_token") != token_hex:
        result["status"] = "candidate_token_mismatch"
        return result
    if len(guid_hits) != 1:
        result["status"] = "guid_not_unique"
        return result
    if len(token_hits) != 1:
        result["status"] = "token_not_unique"
        return result
    if guid_hits != [node] or token_hits != [node]:
        result["status"] = "cross_field_disagreement"
        return result
    result["unit_type_id"] = node
    result["debug_name"] = unit.get("debug_name")
    result["ndf_class"] = unit.get("ndf_class")
    result["status"] = "2_of_2_exact_guid_and_token"
    result["confidence"] = "high_static_join"
    return result


def _rt_validate_lookups(pairs):
    samples = []
    mapping = {}
    for ordinal, enter_line, enter, leave_line, leave in pairs:
        where = "lookup:%d" % enter_line
        handle = _rt_u32(_rt_bytes(_rt_read_record(enter, "ecx", 8, 4, "enter", where),
                                   where, False), 0, where)
        retval = _rt_bytes(_rt_read_record(leave, "retval", 0, 128, "leave", where),
                           where, False)
        stored = _rt_u32(retval, 0x20, where)
        _require(stored == handle,
                 "lookup handle %d != returned +0x20 %d at %s" % (handle, stored, where))
        tag = _rt_u32(retval, 0x24, where)

        descriptor = _rt_u32(retval, 0x28, where)
        _require(descriptor != 0, "null descriptor at %s" % where)
        vtable = _rt_u32(retval, 0, where)
        key = handle
        entry = (int(leave.get("retval"), 16), descriptor, tag, vtable)
        if key in mapping:
            _require(mapping[key] == entry,
                     "handle %d maps to two owners at %s" % (handle, where))
        else:
            mapping[key] = entry
        samples.append({
            "ordinal": ordinal,
            "handle_u32": handle,
            "owner_object": leave.get("retval"),
            "descriptor_pointer": "0x%08x" % descriptor,
            "owner_field_0x24_raw": "0x%08x" % tag,
            "vtable": "0x%08x" % vtable,
            "enter_line": enter_line,
            "leave_line": leave_line,
        })
    _require(samples, "no owner lookups captured")
    vtables = {sample["vtable"] for sample in samples}
    _require(len(vtables) == 1, "owner lookup vtable is not constant: %r" % sorted(vtables))
    return mapping, samples


def _rt_validate_clock(pairs):
    samples = []
    for ordinal, enter_line, enter, leave_line, leave in pairs:
        where = "clock:%d" % enter_line
        counter = struct.unpack("<i", _rt_bytes(
            _rt_read_record(enter, "ecx", 208, 4, "enter", where), where, False))[0]
        samples.append({
            "ordinal": ordinal,
            "counter": counter,
            "container": enter.get("ecx"),
            "enter_line": enter_line,
            "leave_line": leave_line,
        })
    resets = []
    for previous, current in zip(samples, samples[1:]):
        if current["container"] != previous["container"] or current["counter"] < previous["counter"]:
            resets.append({
                "kind": ("receiver_change" if current["container"] != previous["container"]
                         else "counter_decrease"),
                "from_container": previous["container"],
                "to_container": current["container"],
                "from_counter": previous["counter"],
                "from_line": previous["enter_line"],
                "to_counter": current["counter"],
                "to_line": current["enter_line"],
            })
    return samples, resets


def _rt_reference_probe(pairs, member_addresses):
    """Check whether the generic reference registry authenticates member objects."""
    successful = 0
    failed = 0
    header_key_matches = 0
    returned_objects = set()
    failure_reasons = {}
    for ordinal, enter_line, enter, leave_line, leave in pairs:
        where = "reference_lookup:%d" % enter_line
        arguments = enter.get("args")
        _require(isinstance(arguments, list) and len(arguments) == 2,
                 "reference_lookup argument count at %s" % where)
        read = _rt_read_record(leave, "retval", 0, 128, "leave", where)
        result = read.get("result") or {}
        if result.get("ok") is not True:
            failed += 1
            reason = result.get("reason") or "unknown"
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
            continue
        successful += 1
        header = _rt_bytes(read, where, False)
        returned_objects.add(int(leave.get("retval"), 16))
        if _rt_u32(header, 0x1c, where) == int(arguments[0], 16):
            header_key_matches += 1
    matches = sorted(returned_objects & member_addresses)
    return {
        "hook": "reference_lookup",
        "calls": len(pairs),
        "successful_header_reads": successful,
        "unreadable_returns": failed,
        "unreadable_reasons": failure_reasons,
        "header_plus_0x1c_equals_arg0": header_key_matches,
        "distinct_returned_objects": len(returned_objects),
        "member_addresses_checked": len(member_addresses),
        "member_address_matches": len(matches),
        "status": ("does_not_authenticate_member_objects" if not matches
                   else "member_objects_present"),
        "note": ("%d/%d readable generic registry headers match their input key; "
                 "%d/%d member objects appear among the returned pointers. "
                 "A matching field offset alone does not authenticate a wire key."
                 % (header_key_matches, successful, len(matches), len(member_addresses))),
    }


def _rt_clock_quantization(value):
    """Test only whether a stored float is a 0.2 quantum; not a counter proof."""
    units = round(value / 0.2)
    reconstructed = struct.unpack("<f", struct.pack("<f", units * 0.2))[0]
    return {"quantization_units": units, "reconstructed": reconstructed,
            "matches_quantization": abs(value - reconstructed) <= 1e-3,
            "counter_claim": None}


def _rt_descriptor_bytes(bucket, address, guid_hex, token_hex, ref):
    if address in bucket:
        _require(bucket[address]["guid_hex"] == guid_hex
                 and bucket[address]["token_hex"] == token_hex,
                 "descriptor bytes differ across reads at %s" % ref)
        bucket[address]["refs"].append(ref)
    else:
        bucket[address] = {"guid_hex": guid_hex, "token_hex": token_hex,
                           "refs": [ref]}


def _rt_join_pointer(bucket, index, address):
    item = bucket.get(address)
    if item is None:
        return {
            "guid_hex": None, "name_token_hex": None, "guid_matches": 0,
            "guid_unique": False, "token_matches": 0, "token_unique": False,
            "descriptor_index_entry": False, "unit_type_id": None,
            "debug_name": None, "ndf_class": None, "candidate_path": None,
            "status": "descriptor_bytes_not_captured", "confidence": "none",
        }
    return _rt_descriptor_join(index, item["guid_hex"], item["token_hex"])


def _rt_extract(rows, source_name, source_sha256, line_count, index, index_name,
                index_sha256):
    start, summary = _rt_validate_header(rows)
    grouped = _rt_records(rows)
    pairs_by_hook = {name: _rt_pairs(grouped, name) for name in RUNTIME_HOOK_SPECS}
    emitted = _rt_check_counts(summary, pairs_by_hook)

    impacts = pairs_by_hook[RUNTIME_IMPACT_HOOK]
    checks = pairs_by_hook[RUNTIME_CHECK_HOOK]
    destroys = pairs_by_hook[RUNTIME_DESTROY_HOOK]
    lookups = pairs_by_hook[RUNTIME_LOOKUP_HOOK]
    clocks = pairs_by_hook[RUNTIME_CLOCK_HOOK]
    _require(len(impacts) > 0, "no runtime impacts")
    _require([item[0] for item in impacts] == list(range(1, len(impacts) + 1)),
             "impact ordinals are not contiguous")
    _require([item[0] for item in checks] == list(range(1, len(checks) + 1)),
             "destruction-check ordinals are not contiguous")
    _require(len(checks) == len(impacts),
             "destruction checks %d != impacts %d" % (len(checks), len(impacts)))

    lookup_mapping, lookup_samples = _rt_validate_lookups(lookups)
    clock_samples, clock_resets = _rt_validate_clock(clocks)

    check_by_ordinal = {item[0]: item for item in checks}
    check_by_call_id = {item[2].get("call_id"): item for item in checks}
    destroys_by_parent = {}
    lifecycle_destroys = []
    cleanup_destroys = []
    for ordinal, enter_line, enter, leave_line, leave in destroys:
        parent = enter.get("parent_call_id")
        return_address = enter.get("return_address")
        arguments = enter.get("args")
        _require(isinstance(arguments, list) and len(arguments) == 1,
                 "destroy argument count at line %d" % enter_line)
        header = _rt_bytes(_rt_read_record(enter, "ecx", 0, 128, "enter",
                                           "destroy:%d" % enter_line),
                           "destroy:%d" % enter_line, False)
        leave_header = _rt_bytes(_rt_read_record(leave, "ecx", 0, 128, "leave",
                                                 "destroy:%d" % leave_line),
                                 "destroy:%d" % leave_line, False)
        record = {
            "ordinal": ordinal,
            "call_id": enter.get("call_id"),
            "parent_call_id": parent,
            "parent_recorded": enter.get("parent_recorded") is True,
            "return_address": return_address,
            "argument_raw": arguments[0],
            "retval_raw": leave.get("retval"),
            "enter_line": enter_line,
            "leave_line": leave_line,
            "operand_object": enter.get("ecx"),
            "operand_handle_u32": _rt_u32(header, 0x20, "destroy:%d" % enter_line),
            "operand_descriptor_pointer": "0x%08x" % _rt_u32(header, 0x28, "destroy:%d" % enter_line),
            "operand_owner_field_0x24_raw": "0x%08x" % _rt_u32(header, 0x24, "destroy:%d" % enter_line),
            "operand_header_bytes": len(header),
            "header_identical_enter_leave": header == leave_header,
        }
        if return_address == RUNTIME_DESTROY_LIFECYCLE_RETURN:
            _require(record["parent_recorded"], "lifecycle destroy has no recorded parent")
            _require(parent in check_by_call_id,
                     "lifecycle destroy parent is not a destruction check")
            _require(record["argument_raw"] == "0x1",
                     "unexpected lifecycle destroy argument %r" % record["argument_raw"])
            lifecycle_destroys.append(record)
            _require(parent not in destroys_by_parent, "two destroys for one check")
            destroys_by_parent[parent] = record
        elif return_address == RUNTIME_DESTROY_CLEANUP_RETURN:
            _require(parent is None, "cleanup destroy unexpectedly has a parent")
            _require(record["argument_raw"] == "0x6",
                     "unexpected cleanup destroy argument %r" % record["argument_raw"])
            cleanup_destroys.append(record)
        else:
            raise AarTraceError("unexpected destroy return address %r" % return_address)

    descriptor_bucket = {}
    unit_lookup_by_handle = {}
    for handle, entry in lookup_mapping.items():
        unit_lookup_by_handle[handle] = {
            "owner_object": entry[0],
            "descriptor_pointer": entry[1],
            "owner_field_0x24_raw": entry[2],
            "vtable": entry[3],
        }

    # Capture every descriptor byte block before building events so a victim
    # descriptor first seen on a null-source impact is available to earlier
    # source-bearing impacts.
    for ordinal, enter_line, enter, leave_line, leave in impacts:
        where = "impact:%d" % enter_line
        arguments = enter.get("args")
        _require(isinstance(arguments, list) and len(arguments) == 5,
                 "impact argument count at %s" % where)
        arg2_bytes = _rt_bytes(_rt_read_record(enter, "arg2", 0, 128, "enter", where),
                               where, False)
        _rt_descriptor_bytes(descriptor_bucket, int(arguments[2], 16),
                             arg2_bytes[0x0c:0x1c].hex(),
                             arg2_bytes[0x60:0x68].hex(), where)

    events = []
    alarms = 0
    for ordinal, enter_line, enter, leave_line, leave in impacts:
        where = "impact:%d" % enter_line
        arguments = enter.get("args")
        _require(isinstance(arguments, list) and len(arguments) == 5,
                 "impact argument count at %s" % where)
        _require(arguments[4] in ("0x1", "0x2"), "unsupported mode at %s" % where)
        mode = int(arguments[4], 16)
        arg0 = _float32_argument(arguments[0], where)
        _require(math.isfinite(arg0) and arg0 >= 0, "invalid input at %s" % where)

        header = _rt_bytes(_rt_read_record(enter, "ecx", 0, 16, "enter", where),
                           where, False)
        handle = _rt_u32(header, 8, where)
        _require(handle > 0, "zero damaged handle at %s" % where)
        source_pointer = _rt_u32(header, 4, where)
        _require(source_pointer != 0, "null constant pointer at %s" % where)
        _require(_rt_u32(header, 0, where) != 0, "null vtable at %s" % where)

        before = _rt_bytes(_rt_read_record(enter, "ecx", 400, 96, "enter", where),
                           where, False)
        after = _rt_bytes(_rt_read_record(leave, "ecx", 400, 96, "leave", where),
                          where, False)
        fields = {}
        for offset in RUNTIME_DAMAGE_FIELDS:
            index_offset = offset - 400
            fields["0x%x" % offset] = {
                "before": _rt_f32(before, index_offset, where),
                "after": _rt_f32(after, index_offset, where),
                "before_hex": before[index_offset:index_offset + 4].hex(),
                "after_hex": after[index_offset:index_offset + 4].hex(),
            }
            for phase in ("before", "after"):
                _require(math.isfinite(fields["0x%x" % offset][phase]),
                         "non-finite field 0x%x at %s" % (offset, where))
        changed = [offset for offset in (0x190, 0x194, 0x198, 0x19C, 0x1A0)
                   if fields["0x%x" % offset]["before"] != fields["0x%x" % offset]["after"]]
        expected = 0x190 if mode == 1 else 0x19C
        _require(changed == [expected],
                 "transition fields %r do not match mode %d at %s" % (changed, mode, where))
        delta = fields["0x%x" % expected]["after"] - fields["0x%x" % expected]["before"]
        _require(delta > 0 and math.isfinite(delta), "non-increasing transition at %s" % where)
        _require(delta <= arg0 + 1e-3, "effective damage exceeds input at %s" % where)

        pointer_read = _rt_read_record(enter, "ecx", 4, 128, "enter", where)
        _require(pointer_read.get("indirect") is True, "source pointer read is not indirect at %s" % where)
        _require(pointer_read.get("target") == "0x%08x" % source_pointer,
                 "indirect target mismatch at %s" % where)
        _require(pointer_read.get("chain") == ["0x%08x" % source_pointer],
                 "indirect chain mismatch at %s" % where)

        source_raw = arguments[1]
        source_read = _rt_read_record(enter, "arg1", 0, 128, "enter", where)
        source_owner = None
        source_handle = None
        source_descriptor_pointer = None
        if source_raw == "0x0":
            _require(_rt_bytes(source_read, where, allow_failure=True) is None,
                     "null arg1 unexpectedly readable at %s" % where)
            source_status = "null"
        else:
            owner_bytes = _rt_bytes(source_read, where, False)
            source_owner = source_raw
            source_handle = _rt_u32(owner_bytes, 0x20, where)
            source_descriptor_pointer = _rt_u32(owner_bytes, 0x28, where)
            _require(source_handle > 0, "zero source handle at %s" % where)
            _require(source_descriptor_pointer == int(arguments[2], 16),
                     "arg1+0x28 != arg2 at %s" % where)
            source_status = "readable"

        target_read = _rt_read_record(enter, "arg2", 0, 128, "enter", where)
        arg2_bytes = _rt_bytes(target_read, where, False)
        arg2_guid = arg2_bytes[0x0c:0x1c].hex()
        arg2_token = arg2_bytes[0x60:0x68].hex()
        arg2_address = int(arguments[2], 16)
        _rt_descriptor_bytes(descriptor_bucket, arg2_address, arg2_guid, arg2_token, where)

        lookup = unit_lookup_by_handle.get(handle)
        _require(lookup is not None,
                 "damaged handle %d has no independent owner lookup" % handle)

        expected_descriptor = (source_descriptor_pointer if source_handle is not None
                               else lookup["descriptor_pointer"])
        _require(arg2_address == expected_descriptor,
                 "arg2 is neither the source nor the target descriptor at %s" % where)

        check_ordinal, check_enter_line, check_enter, check_leave_line, check_leave = \
            check_by_ordinal[ordinal]
        _require(check_enter.get("ecx") == enter.get("ecx"),
                 "check ecx differs from impact at %s" % where)
        check_header = _rt_bytes(_rt_read_record(check_enter, "ecx", 0, 16, "enter",
                                                 "check:%d" % check_enter_line),
                                 "check:%d" % check_enter_line, False)
        _require(_rt_u32(check_header, 8, where) == handle,
                 "check handle differs at %s" % where)
        _require(check_enter.get("return_address") == RUNTIME_CHECK_RETURN_ADDRESS,
                 "check return address mismatch at %s" % where)
        check_block = _rt_bytes(_rt_read_record(check_enter, "ecx", 400, 96, "enter",
                                                "check:%d" % check_enter_line),
                                "check:%d" % check_enter_line, False)
        _require(check_block == after,
                 "check enter block differs from impact leave block at %s" % where)
        retval_raw = check_leave.get("retval")
        try:
            retval = int(retval_raw, 16)
        except (TypeError, ValueError):
            raise AarTraceError("bad check retval at %s" % where) from None
        al = retval & 0xFF
        _require(al in (0, 1), "check AL is not boolean at %s" % where)
        threshold = al == 1
        destroy = destroys_by_parent.get(check_enter.get("call_id"))
        if threshold:
            _require(destroy is not None,
                     "threshold check without nested destroy at %s" % where)
        else:
            _require(destroy is None,
                     "destroy without threshold check at %s" % where)
        if threshold:
            alarms += 1
            _require(destroy["operand_handle_u32"] == handle,
                     "destroy operand handle differs at %s" % where)
            _require(int(destroy["operand_object"], 16) == lookup["owner_object"],
                     "destroy operand is not the looked-up owner at %s" % where)
            _require(destroy["operand_descriptor_pointer"]
                     == "0x%08x" % lookup["descriptor_pointer"],
                     "destroy descriptor differs at %s" % where)

        time_value = fields["0x1ec"]["after"]
        quantization = _rt_clock_quantization(time_value)
        target_join = _rt_join_pointer(descriptor_bucket, index,
                                       lookup["descriptor_pointer"])
        if source_handle is not None:
            source_join = _rt_join_pointer(descriptor_bucket, index,
                                           source_descriptor_pointer)
        else:
            source_join = None

        fields_out = {}
        for offset, values in fields.items():
            fields_out[offset] = dict(values)
        events.append({
            "ordinal": ordinal,
            "kind": "suppression_increase" if mode == 1 else "physical_damage_increase",
            "mode": mode,
            "mode_arg4_raw": arguments[4],
            "refs": {
                "enter_line": enter_line,
                "leave_line": leave_line,
                "check_enter_line": check_enter_line,
                "check_leave_line": check_leave_line,
                "destroy_enter_line": destroy["enter_line"] if destroy else None,
                "destroy_leave_line": destroy["leave_line"] if destroy else None,
            },
            "line_ref": ("L%d-L%d check L%d-L%d%s"
                         % (enter_line, leave_line, check_enter_line, check_leave_line,
                            " destroy L%d-L%d" % (destroy["enter_line"], destroy["leave_line"])
                            if destroy else "")),
            "damage_object": {
                "address": enter.get("ecx"),
                "handle_u32": handle,
                "vtable": "0x%08x" % _rt_u32(header, 0, where),
                "constant_pointer": "0x%08x" % source_pointer,
            },
            "fields": fields_out,
            "arg0_float32": arg0,
            "arg0_raw": arguments[0],
            "observed_delta": delta,
            "changed_fields": ["0x%x" % offset for offset in changed],
            "target": {
                "owner_object": "0x%08x" % lookup["owner_object"],
                "descriptor_pointer": "0x%08x" % lookup["descriptor_pointer"],
                "owner_field_0x24_raw": "0x%08x" % lookup["owner_field_0x24_raw"],
                "join": target_join,
                "identity_status": ("observed_handle_and_descriptor_pointer_with_static_type_join"
                                    if target_join["status"] == "2_of_2_exact_guid_and_token"
                                    else "observed_handle_but_type_join_unverified"),
            },
            "reported_source": {
                "arg1_raw": source_raw,
                "arg1_read_status": source_status,
                "owner_object": source_owner,
                "owner_handle_u32": source_handle,
                "descriptor_pointer": ("0x%08x" % source_descriptor_pointer
                                       if source_descriptor_pointer is not None else None),
                "descriptor_matches_arg2": (source_descriptor_pointer == arg2_address
                                            if source_descriptor_pointer is not None else None),
                "join": source_join,
                "role": ("inferred_damage_source_owner" if source_handle is not None
                         else "unresolved_owner"),
                "confidence": ("inferred_not_static_proven" if source_handle is not None
                               else "not_applicable"),
                "basis": ("arg1 is the captured owner argument and equals an owner whose "
                          "+0x28 is arg2; no static data-flow proof ties arg1 to a "
                          "shooter, weapon or projectile"),
            },
            "check": {
                "call_id": check_enter.get("call_id"),
                "return_address": RUNTIME_CHECK_RETURN_ADDRESS,
                "retval_raw": retval_raw,
                "al_u8": al,
                "threshold_met_low_byte": threshold,
                "note": "AL is the boolean; upper EAX bits (0x3c2219xx) are not truthy evidence",
            },
            "destruction": ({
                "observed": True,
                "kind": "damage_lifecycle",
                "call_id": destroy["call_id"],
                "parent_call_id": destroy["parent_call_id"],
                "return_address": destroy["return_address"],
                "argument_raw": destroy["argument_raw"],
                "retval_raw": destroy["retval_raw"],
                "operand_object": destroy["operand_object"],
                "operand_handle_u32": destroy["operand_handle_u32"],
                "operand_descriptor_pointer": destroy["operand_descriptor_pointer"],
                "enter_line": destroy["enter_line"],
                "leave_line": destroy["leave_line"],
                "join": "destroy_header_matches_lookup_object_and_descriptor",
                "kill_outcome": None,
            } if destroy else {
                "observed": False,
                "kind": None,
                "kill_outcome": None,
            }),
            "time": {
                "deterministic_time_seconds": time_value,
                "raw_bits": fields["0x1ec"]["after_hex"],
                "enter_raw_bits": fields["0x1ec"]["before_hex"],
                "enter_value": fields["0x1ec"]["before"],
                "proof_level": RUNTIME_CLOCK["proof_level"],
                "epoch": None,
                "frame": None,
                "replay_frame": None,
                "simulation_time": None,
                "game_time": None,
                "battle_time": None,
                "quantization_check": quantization,
                "basis": ("0x1ec is written by the observed module store from the "
                          "engine-named deterministic seconds accessor; the value is "
                          "not validated simulation, replay or battle time"),
            },
            "confidence": {
                "damage_object_handle": "observed_direct_read",
                "damage_field_change": "observed_before_after",
                "target_owner": ("observed_sampled_lookup_plus_destroy_header" if destroy
                                 else "observed_sampled_lookup"),
                "target_type": target_join["confidence"],
                "source_owner": ("observed_pointer_and_header" if source_handle is not None
                                 else "unresolved_owner"),
                "source_role": ("inferred_not_static_proven" if source_handle is not None
                                else "not_applicable"),
                "threshold_met": "observed_low_byte",
                "destruction_call": "observed_nested_call" if destroy else "not_observed",
                "kill_outcome": "unknown",
                "deterministic_time": RUNTIME_CLOCK["proof_level"],
            },
        })

    _require(alarms == len(lifecycle_destroys),
             "threshold count %d != lifecycle destroys %d" % (alarms, len(lifecycle_destroys)))
    _require(len({record["ordinal"] for record in cleanup_destroys}) == len(cleanup_destroys),
             "duplicate cleanup destruction ordinals")

    member_handles = {event["damage_object"]["handle_u32"] for event in events}
    member_handles.update(event["reported_source"]["owner_handle_u32"] for event in events
                          if event["reported_source"]["owner_handle_u32"] is not None)
    member_addresses = {lookup_mapping[handle][0] for handle in member_handles
                        if handle in lookup_mapping}
    reference_probe = _rt_reference_probe(pairs_by_hook["reference_lookup"],
                                          member_addresses)

    last_impact_leave = max(_parse_timestamp(item[4].get("timestamp_utc"), "impact")
                            for item in impacts)
    for record in cleanup_destroys:
        enter_time = _parse_timestamp(
            next(item[2].get("timestamp_utc") for item in destroys
                 if item[2]["call_id"] == record["call_id"]), "cleanup")
        _require(enter_time >= last_impact_leave,
                 "cleanup destroy precedes the last impact")
        _require(record["operand_handle_u32"] in unit_lookup_by_handle,
                 "cleanup operand handle has no lookup")
        lookup = unit_lookup_by_handle[record["operand_handle_u32"]]
        _require(record["operand_object"] == "0x%08x" % lookup["owner_object"],
                 "cleanup operand object differs from lookup")
        _require(record["operand_descriptor_pointer"] == "0x%08x" % lookup["descriptor_pointer"],
                 "cleanup operand descriptor differs from lookup")

    descriptors_out = []
    for address in sorted(descriptor_bucket):
        item = descriptor_bucket[address]
        join = _rt_descriptor_join(index, item["guid_hex"], item["token_hex"])
        descriptors_out.append({
            "runtime_address": "0x%08x" % address,
            "guid_hex": item["guid_hex"],
            "name_token_hex": item["token_hex"],
            "captured_at": item["refs"],
            "join": join,
        })

    units = _rt_unit_histories(events, unit_lookup_by_handle, lookup_samples,
                               descriptor_bucket, index, lifecycle_destroys,
                               cleanup_destroys)
    lifecycle = []
    for event in events:
        if not event["destruction"]["observed"]:
            continue
        lifecycle.append({
            "impact_ordinal": event["ordinal"],
            "impact_refs": event["refs"],
            "damaged_handle_u32": event["damage_object"]["handle_u32"],
            "victim_unit": event["target"]["join"].get("debug_name"),
            "victim_unit_type_id": event["target"]["join"].get("unit_type_id"),
            "reported_source_owner_handle_u32": event["reported_source"]["owner_handle_u32"],
            "reported_source_unit": (event["reported_source"]["join"] or {}).get("debug_name"),
            "reported_source_role": event["reported_source"]["role"],
            "threshold": {
                "check_call_id": event["check"]["call_id"],
                "al_u8": event["check"]["al_u8"],
                "retval_raw": event["check"]["retval_raw"],
            },
            "destruction_call": {
                "call_id": event["destruction"]["call_id"],
                "return_address": event["destruction"]["return_address"],
                "argument_raw": event["destruction"]["argument_raw"],
                "operand_object": event["destruction"]["operand_object"],
                "operand_handle_u32": event["destruction"]["operand_handle_u32"],
                "line_refs": [event["refs"]["destroy_enter_line"],
                              event["refs"]["destroy_leave_line"]],
            },
            "observed": ("impact on handle -> same-object threshold check returns AL=1 "
                         "-> nested destroy call on the looked-up owner"),
            "not_claimed": ["shooter identity", "weapon", "kill/score outcome",
                            "replay frame", "battle time"],
            "confidence": {
                "damage_destruction_control_flow": "observed_same_trace_nesting",
                "victim_identity": "observed_handle_plus_static_type_join",
                "source_attribution": "inferred_not_static_proven",
                "kill_outcome": "unknown",
            },
        })

    clock_first = clock_samples[0] if clock_samples else None
    clock_last = clock_samples[-1] if clock_samples else None
    manifest = {
        "schema": RUNTIME_SCHEMA,
        "status": "runtime_observed_with_static_unit_type_join",
        "source": {
            "trace": source_name,
            "sha256": source_sha256,
            "line_count": line_count,
            "revision": start.get("revision"),
            "executable_sha256": start.get("sha256"),
            "image": {"base": "0x%08x" % IMAGE_BASE, "size": IMAGE_SIZE,
                      "end": "0x%08x" % (IMAGE_BASE + IMAGE_SIZE)},
        },
        "native_unit_index": {
            "name": index_name,
            "sha256": index_sha256,
            "build": index.get("game_build"),
            "schema": index.get("schema"),
            "scope": index.get("scope"),
            "archive_sha256": index["source"].get("sha256"),
            "archive_build": index["source"].get("build"),
            "archive_member": index["source"].get("member", {}).get("member"),
            "archive_member_sha256": index["source"].get("member", {}).get("entry_sha256"),
            "limitations": index.get("limitations"),
        },
        "provenance": {
            "capture_config_pin": RUNTIME_CAPTURE_CONFIG,
            "capture_source_pins": RUNTIME_CAPTURE_SOURCE_PINS,
            "capture_source_status": "not checked by in-memory extraction",
            "trace_embedded_hooks": "start/identity records were matched to the expected "
                                    "eight hook shapes and executable addresses",
        },
        "integrity": {
            "records": line_count,
            "paired_calls": emitted,
            "emitted_records": summary.get("emitted"),
            "hooks": {name: {
                "va": spec["va"],
                "sample_every": spec["sample_every"],
                "paired": len(pairs_by_hook[name]),
                "invocations": summary["counts"][name],
            } for name, spec in RUNTIME_HOOK_SPECS.items()},
            "impact_enters": len(impacts),
            "impact_leaves": len(impacts),
            "destruction_checks": len(checks),
            "owner_destroys": len(destroys),
            "lifecycle_destroys": len(lifecycle_destroys),
            "cleanup_destroys": len(cleanup_destroys),
            "owner_lookups": len(lookup_samples),
            "clock_samples": len(clock_samples),
            "suppressed": summary.get("suppressed"),
            "callback_errors": summary.get("callback_errors"),
            "stale_frames": summary.get("stale_frames"),
            "stack_mismatches": summary.get("stack_mismatches"),
            "read_failures": {
                "scope": "impact owner-pointer reads; generic registry failures are reported separately",
                "all_recorded": sum(read.get("result", {}).get("ok") is False
                                    for row in rows for read in row.get("reads", [])),
                "arg1_null_source": sum(1 for event in events
                                        if event["reported_source"]["arg1_read_status"] == "null"),
                "other": 0,
            },
            "destroy_headers_identical": all(record["header_identical_enter_leave"]
                                             for record in lifecycle_destroys + cleanup_destroys),
            "check_block_matches_impact_leave": True,
            "owner_lookup_handle_matches_plus_0x20": len(lookup_samples),
            "owner_lookup_distinct_handles": len(lookup_mapping),
        },
        "clock": {
            "hook": RUNTIME_CLOCK["hook"],
            "va": RUNTIME_CLOCK["va"],
            "global_pointer_slot": RUNTIME_CLOCK["global_pointer_slot"],
            "counter_offset": RUNTIME_CLOCK["counter_offset"],
            "scale_constant": {
                "va": RUNTIME_CLOCK["scale_constant_va"],
                "bits": RUNTIME_CLOCK["scale_constant_bits"],
                "float": RUNTIME_CLOCK["scale_constant_float"],
                "verified_from_executable": True,
            },
            "module_store_offset": RUNTIME_CLOCK["module_store_offset"],
            "static_binding": RUNTIME_CLOCK["static_binding"],
            "proof_level": RUNTIME_CLOCK["proof_level"],
            "samples": len(clock_samples),
            "first": clock_first,
            "last": clock_last,
            "discontinuities": clock_resets,
            "epoch": None,
            "frame": None,
            "replay_frame": None,
            "simulation_time": None,
            "game_time": None,
            "battle_time": None,
            "quantization_only": ("For every impact, 0x1ec equals a 0.2 multiple; "
                                  "that is a quantization consistency test, not an "
                                  "independently validated counter value."),
        },
        "descriptor_joins": descriptors_out,
        "identity_probes": {"reference_lookup": reference_probe},
        "units": units,
        "damage_lifecycle_observations": lifecycle,
        "end_cleanup_destructions": [{
            "ordinal": record["ordinal"],
            "call_id": record["call_id"],
            "return_address": record["return_address"],
            "argument_raw": record["argument_raw"],
            "retval_raw": record["retval_raw"],
            "operand_object": record["operand_object"],
            "operand_handle_u32": record["operand_handle_u32"],
            "operand_descriptor_pointer": record["operand_descriptor_pointer"],
            "enter_line": record["enter_line"],
            "leave_line": record["leave_line"],
            "meaning": ("observed end-of-match cleanup call with argument 6 and no "
                        "recorded parent; not a damage lifecycle or a kill"),
            "kill_outcome": None,
        } for record in sorted(cleanup_destroys, key=lambda item: item["ordinal"])],
        "events": events,
        "corrections": [
            {"claim": "the three AL=1 checks are three kills",
             "status": "not_supported",
             "detail": ("%d AL=1 checks each parent an owner_destroy call, which is "
                        "an observed destruction invocation. No score, removal, death "
                        "event or kill counter is present, so kill outcomes stay unknown." % alarms)},
            {"claim": "arg1 is the shooter",
             "status": "inferred_only",
             "detail": ("For readable owner arguments, +0x28 equals arg2, but no firing data-flow proof "
                        "connects it to a firing unit, weapon or projectile.")},
            {"claim": "handle 0's descriptor is unresolved",
             "status": "partially_corrected",
             "detail": ("A lookup can establish an owner and descriptor pointer without "
                        "capturing descriptor bytes. Such a pointer alone does not "
                        "establish the unit type; see the per-unit join status.")},
            {"claim": "+0x68 is clock time",
             "status": "rejected_by_static_evidence",
             "detail": ("The deterministic clock path uses global 0x201d318, [container+0xd0] "
                        "and 0xaaedf0; the reported +0x68 field belongs to a different "
                        "static object (1fce0d0+68 speed factor) and is not exported here.")},
        ],
        "limitations": [
            "Single capture, one match; counts and identities are not general gameplay validation.",
            "Unit types are static configuration joins, not live entity or player authentication.",
            "Source attribution, shooter and weapon remain inferred; kill/score outcome is unknown.",
            "Frame, epoch, replay time and battle time are not captured; only the engine-named deterministic seconds value is exposed.",
            "The generic reference registry returns 0 of the 8 damaged/source owner objects, so it does not authenticate them.",
            "Order-wrapper records are counted but not interpreted here.",
        ],
    }
    return manifest


def _rt_unit_histories(events, lookup_by_handle, lookup_samples, descriptor_bucket,
                       index, lifecycle_destroys, cleanup_destroys):
    refs_by_handle = {}
    for sample in lookup_samples:
        refs_by_handle.setdefault(sample["handle_u32"], []).append(sample)
    destroy_by_handle = {}
    for record in lifecycle_destroys:
        destroy_by_handle[record["operand_handle_u32"]] = ("damage_lifecycle", record)
    for record in cleanup_destroys:
        destroy_by_handle.setdefault(record["operand_handle_u32"], ("end_cleanup", record))

    roles = {}
    for event in events:
        roles.setdefault(event["damage_object"]["handle_u32"], set()).add("damaged")
        handle = event["reported_source"]["owner_handle_u32"]
        if handle is not None:
            roles.setdefault(handle, set()).add("reported_source_owner")
    for handle, (kind, record) in destroy_by_handle.items():
        roles.setdefault(handle, set()).add("cleanup_operand" if kind == "end_cleanup"
                                            else "destruction_call_operand")

    units = []
    for handle in sorted(roles):
        info = lookup_by_handle.get(handle)
        _require(info is not None, "unit handle %d has no lookup" % handle)
        descriptor_pointer = info["descriptor_pointer"]
        descriptor = descriptor_bucket.get(descriptor_pointer)
        if descriptor is None:
            join = {
                "guid_hex": None, "name_token_hex": None, "guid_matches": 0,
                "guid_unique": False, "token_matches": 0, "token_unique": False,
                "unit_type_id": None, "debug_name": None, "ndf_class": None,
                "status": "descriptor_bytes_not_captured", "confidence": "none",
            }
        else:
            join = _rt_descriptor_join(index, descriptor["guid_hex"], descriptor["token_hex"])
        unit_events = [event for event in events
                       if event["damage_object"]["handle_u32"] == handle]
        source_events = [event for event in events
                         if event["reported_source"]["owner_handle_u32"] == handle]
        suppression = [event for event in unit_events if event["mode"] == 1]
        physical = [event for event in unit_events if event["mode"] == 2]
        destruction = None
        if handle in destroy_by_handle:
            kind, record = destroy_by_handle[handle]
            destruction = {
                "observed": True,
                "kind": kind,
                "call_id": record["call_id"],
                "return_address": record["return_address"],
                "operand_object": record["operand_object"],
                "enter_line": record["enter_line"],
                "leave_line": record["leave_line"],
                "retval_raw": record["retval_raw"],
                "kill_outcome": None,
            }
        units.append({
            "handle_u32": handle,
            "owner_object": "0x%08x" % info["owner_object"],
            "descriptor_pointer": "0x%08x" % descriptor_pointer,
            "owner_field_0x24_raw": "0x%08x" % info["owner_field_0x24_raw"],
            "id_like": None,
            "roles": sorted(roles[handle]),
            "lookup_samples": len(refs_by_handle.get(handle, [])),
            "lookup_refs": [{"enter_line": sample["enter_line"],
                             "leave_line": sample["leave_line"]}
                            for sample in refs_by_handle.get(handle, [])],
            "descriptor_join": join,
            "events": [event["ordinal"] for event in unit_events],
            "source_events": [event["ordinal"] for event in source_events],
            "damage": {
                "applications": len(unit_events),
                "suppression_applications": len(suppression),
                "physical_transitions": len(physical),
                "suppression_peak_0x190": max(
                    (event["fields"]["0x190"]["after"] for event in suppression),
                    default=None),
                "max_0x190": max((event["fields"]["0x190"]["after"] for event in unit_events),
                                 default=None),
                "max_0x194": max((event["fields"]["0x194"]["after"] for event in unit_events),
                                 default=None),
                "max_0x198": max((event["fields"]["0x198"]["after"] for event in unit_events),
                                 default=None),
            },
            "destruction": destruction,
            "confidence": {
                "handle_and_object": "observed_owner_lookup",
                "descriptor_pointer": "observed_owner_lookup",
                "unit_type": join["confidence"],
                "destruction_call": ("observed_cleanup_call" if destruction and
                                     destruction["kind"] == "end_cleanup" else
                                     "observed_nested_call" if destruction else "not_observed"),
                "kill_outcome": "unknown",
            },
        })
    return units


def extract_runtime(rows, source_name, source_sha256, line_count, index,
                    index_name, index_sha256):
    """Recompute the runtime manifest from parsed rows and a parsed index."""
    return _rt_extract(rows, source_name, source_sha256, line_count, index,
                       index_name, index_sha256)


def _rt_verify_capture_sources(directory):
    """Authenticate the three retained capture files; never substitute current code."""
    pins = dict(RUNTIME_CAPTURE_SOURCE_PINS)
    pins[RUNTIME_CAPTURE_CONFIG["file"]] = RUNTIME_CAPTURE_CONFIG["sha256"]
    records = []
    for name, expected in pins.items():
        path = Path(directory) / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        _require(actual is None or actual == expected,
                 "capture source sha256 mismatch: %s" % name)
        records.append({"name": name, "expected_sha256": expected,
                        "sha256": actual, "status": "matched" if actual else "missing"})
    return records


def extract_runtime_file(trace_path, index_path,
                         expect_trace_sha256=RUNTIME_TRACE_SHA256,
                         expect_index_sha256=RUNTIME_INDEX_SHA256):
    rows, name, digest, line_count = load_trace(trace_path, expect_trace_sha256)
    index, index_sha256, index_name = _rt_load_index(index_path, expect_index_sha256)
    manifest = _rt_extract(rows, name, digest, line_count, index, index_name, index_sha256)
    records = _rt_verify_capture_sources(Path(trace_path).parent / "capture-sources")
    manifest["provenance"]["capture_source_verification"] = records
    manifest["provenance"]["capture_source_status"] = (
        "all capture-era source/config hashes matched retained copies"
        if all(item["status"] == "matched" for item in records)
        else "capture-era source/config copies incomplete; see per-file verification")
    return manifest


def _rt_event_line(event):
    target = event["target"]["join"].get("debug_name") or "UNJOINED"
    source = event["reported_source"]
    source_text = ("%s(%s, inferred)" % (
        (source["join"] or {}).get("debug_name") or "UNJOINED",
        source["owner_handle_u32"]) if source["owner_handle_u32"] is not None
        else "unresolved_owner")
    check = event["check"]
    destroy = event["destruction"]
    destruction_text = ("destroy=%s h=%d retval=%s" % (
        destroy["call_id"], destroy["operand_handle_u32"], destroy["retval_raw"])
        if destroy["observed"] else "destroy=none")
    return ("- **%s** ord %d | %s | handle %d | %s %.6f -> %.6f (delta %.6f) | "
            "AL=%d raw=%s | %s | target=%s | source=%s | det_time=%s | kill=UNKNOWN"
            % (event["line_ref"], event["ordinal"], event["kind"],
               event["damage_object"]["handle_u32"],
               event["changed_fields"][0],
               event["fields"][event["changed_fields"][0]]["before"],
               event["fields"][event["changed_fields"][0]]["after"],
               event["observed_delta"], check["al_u8"], check["retval_raw"],
               destruction_text, target, source_text,
               "%.6f" % event["time"]["deterministic_time_seconds"]))


def render_runtime_chronology(manifest):
    source = manifest["source"]
    index = manifest["native_unit_index"]
    clock = manifest["clock"]
    lines = [
        "# Runtime damage AAR chronology",
        "",
        "Source: `%s` SHA-256 `%s` (%d lines), read-only."
        % (source["trace"], source["sha256"], source["line_count"]),
        "Executable: revision %s, SHA-256 `%s`."
        % (source["revision"], source["executable_sha256"]),
        "Native unit index: `%s` SHA-256 `%s` (build %s, archive `%s`)."
        % (index["name"], index["sha256"], index["build"], index["archive_sha256"]),
        "",
        "Every `Lx-Ly` reference resolves to the paired enter/leave records in this "
        "exact file and hash. `det_time` is the engine-named deterministic seconds "
        "value observed in the damage object's `+0x1ec`; epoch, replay frame, "
        "simulation time and battle time are UNKNOWN.",
        "",
        "## Observation summary",
        "",
        "%d suppression increases and %d physical-damage increases were observed "
        "on %d local target handles. %d checks parented a damage-lifecycle call; "
        "%d separate cleanup calls are excluded from combat-loss counts."
        % (sum(event["mode"] == 1 for event in manifest["events"]),
           sum(event["mode"] == 2 for event in manifest["events"]),
           len({event["damage_object"]["handle_u32"] for event in manifest["events"]}),
           manifest["integrity"]["lifecycle_destroys"],
           manifest["integrity"]["cleanup_destroys"]),
        "Source roles remain provisional. Missing source-owner pointers are unresolved, "
        "not proof that no source existed. No movement, confirmed kill credit or tactical "
        "victory is inferred from these hooks.",
        "",
        "Capture source provenance: %s." % manifest["provenance"]["capture_source_status"],
        "",
        "## Integrity",
        "",
        "- %d emitted records across %d paired calls; %d impacts, %d checks, %d owner destroys (%d lifecycle, %d cleanup)."
        % (manifest["integrity"]["emitted_records"], manifest["integrity"]["paired_calls"],
           len(manifest["events"]),
           manifest["integrity"]["destruction_checks"],
           manifest["integrity"]["owner_destroys"],
           manifest["integrity"]["lifecycle_destroys"],
           manifest["integrity"]["cleanup_destroys"]),
        "- %d sampled owner lookups over %d distinct handles; %d clock samples."
        % (manifest["integrity"]["owner_lookups"],
           manifest["integrity"]["owner_lookup_distinct_handles"],
           manifest["integrity"]["clock_samples"]),
        "- All impact-leave `+0x190..+0x1ec` blocks equal the following check-enter block.",
        "",
        "## Unit type joins (static, 2-of-2)",
        "",
        "| runtime descriptor | GUID | token | unit type | node | status |",
        "|---|---|---|---|---:|---|",
    ]
    for item in manifest["descriptor_joins"]:
        join = item["join"]
        lines.append("| `%s` | `%s` | `%s` | %s | %s | `%s` |" % (
            item["runtime_address"], item["guid_hex"], item["name_token_hex"],
            join.get("debug_name") or "UNRESOLVED", join.get("unit_type_id") or "-",
            join["status"]))
    probe = manifest["identity_probes"]["reference_lookup"]
    lines.extend([
        "",
        "Both fields must be unique in the pinned index; otherwise the unit type is "
        "not asserted. A type join does not authenticate a live entity, player or "
        "deployment.",
        "",
        "Generic reference registry probe: %d `reference_lookup` calls, %d readable "
        "headers, %d unreadable null-key returns; `+0x1c` equals the arg0 key on "
        "%d/%d readable returns, but %d of %d member objects appear among them "
        "(`%s`). The registry therefore does not authenticate these owners."
        % (probe["calls"], probe["successful_header_reads"], probe["unreadable_returns"],
           probe["header_plus_0x1c_equals_arg0"], probe["successful_header_reads"],
           probe["member_address_matches"], probe["member_addresses_checked"],
           probe["status"]),
        "",
        "## Damage events",
        "",
    ])
    lines.extend(_rt_event_line(event) for event in manifest["events"])
    lines.extend([
        "",
        "## Damage lifecycle observations (not kill claims)",
        "",
        "Each row is a witnessed control-flow chain: an impact mutated a damaged "
        "object, the immediately following check on that same object returned AL=1, "
        "and the check's recorded child called the destruction hook on the owner "
        "resolved by handle. Source attribution remains inferred.",
        "",
    ])
    for item in manifest["damage_lifecycle_observations"]:
        lines.append(
            "- ord %d handle %d | victim `%s` (node %s) | reported source handle %s `%s` "
            "(inferred) | impact L%d-L%d, check L%d-L%d | check %s AL=%d | destroy %s on `%s` "
            "L%d-L%d | kill=UNKNOWN"
            % (item["impact_ordinal"], item["damaged_handle_u32"],
               item["victim_unit"] or "UNRESOLVED", item["victim_unit_type_id"] or "-",
               item["reported_source_owner_handle_u32"],
               item["reported_source_unit"] or "UNRESOLVED",
               item["impact_refs"]["enter_line"], item["impact_refs"]["leave_line"],
               item["impact_refs"]["check_enter_line"], item["impact_refs"]["check_leave_line"],
               item["threshold"]["check_call_id"], item["threshold"]["al_u8"],
               item["destruction_call"]["call_id"], item["destruction_call"]["operand_object"],
               item["destruction_call"]["line_refs"][0],
               item["destruction_call"]["line_refs"][1]))
    lines.extend([
        "",
        "These are destruction invocations, not confirmed kills: no score, removal, "
        "death event or kill counter is present. `arg1` is an owner pointer inferred "
        "to be the damage source; static data flow from a shooter/weapon is not proven.",
        "",
        "## End-of-match cleanup destructions",
        "",
    ])
    for item in manifest["end_cleanup_destructions"]:
        lines.append("- ord %d call %s handle %d retval %s arg %s (L%d-L%d); cleanup, not a kill"
                     % (item["ordinal"], item["call_id"], item["operand_handle_u32"],
                        item["retval_raw"], item["argument_raw"],
                        item["enter_line"], item["leave_line"]))
    lines.extend([
        "",
        "## Deterministic clock",
        "",
        "`%s` at `%s` records its receiver's `[ecx+0x%x]`. The named seconds getter "
        "loads global `%s` and this path scales by the constant "
        "at `%s` (`%s` = %g). The engine-named seconds binding `%s` calls this path; "
        "the ticks binding `%s` reads the same counter. Proof level: `%s`."
        % (clock["hook"], clock["va"], int(clock["counter_offset"], 16),
           clock["global_pointer_slot"], clock["scale_constant"]["va"],
           clock["scale_constant"]["bits"], clock["scale_constant"]["float"],
           clock["static_binding"]["seconds_entry"],
           clock["static_binding"]["ticks_entry"], clock["proof_level"]),
        "",
        "Observed samples: %d, first counter %s, last counter %s, discontinuities %d. "
        "Receiver changes are not treated as resets of one clock instance. The "
        "0.2 consistency check is a quantization test only; no independent counter "
        "or frame mapping is asserted."
        % (clock["samples"], clock["first"]["counter"] if clock["first"] else "-",
           clock["last"]["counter"] if clock["last"] else "-", len(clock["discontinuities"])),
        "",
        "## Uncertainty and corrections",
        "",
    ])
    for item in manifest["corrections"]:
        lines.append("- **%s**: %s. %s" % (item["claim"], item["status"], item["detail"]))
    lines.extend(["", "## Unit histories", "",
                  "| handle | roles | unit type | damage events | source calls | destruction |",
                  "|---:|---|---|---:|---:|---|"])
    for unit in manifest["units"]:
        destruction = unit["destruction"]
        lines.append("| %d | %s | %s | %d | %d | %s |" % (
            unit["handle_u32"], ", ".join(unit["roles"]),
            unit["descriptor_join"].get("debug_name") or "UNRESOLVED",
            len(unit["events"]), len(unit["source_events"]),
            ("%s call %s" % (destruction["kind"], destruction["call_id"]))
            if destruction else "none"))
    lines.extend(["", "## Limitations", ""])
    lines.extend("- %s" % item for item in manifest["limitations"])
    lines.append("")
    return "\n".join(lines)


def write_runtime_outputs(manifest, out_dir):
    """Exclusively create events.json, units.json, summary.json and chronology.md."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    units_manifest = {
        "schema": RUNTIME_UNITS_SCHEMA,
        "source": manifest["source"],
        "native_unit_index": manifest["native_unit_index"],
        "units": manifest["units"],
        "descriptor_joins": manifest["descriptor_joins"],
        "limitations": manifest["limitations"],
    }
    payloads = {
        "events.json": _json_text(manifest),
        "units.json": _json_text(units_manifest),
        "summary.json": _json_text({key: value for key, value in manifest.items()
                                    if key != "events"}),
        "chronology.md": render_runtime_chronology(manifest),
    }
    targets = [out_dir / name for name in payloads]
    existing = [str(path) for path in targets if path.exists()]
    _require(not existing, "refusing to overwrite existing output: %s" % ", ".join(existing))
    created = []
    try:
        for path in targets:
            with open(path, "x", encoding="utf-8", newline="\n") as handle:
                handle.write(payloads[path.name])
                created.append(path)
    except FileExistsError as error:
        for path in created:
            path.unlink()
        raise AarTraceError("output appeared during write: %s" % error) from None
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", help="path to the raw damage JSONL trace")
    parser.add_argument("--out", required=True, help="events output directory")
    parser.add_argument("--profile", choices=("legacy", "runtime"), default="legacy",
                        help="trace profile (default: legacy pinned combat trace)")
    parser.add_argument("--runtime", action="store_true",
                        help="alias for --profile runtime")
    parser.add_argument("--unit-index", help="native unit index JSON (runtime profile)")
    parser.add_argument("--expect-unit-index-sha256", default=RUNTIME_INDEX_SHA256,
                        help="required unit index SHA-256 (runtime profile)")
    parser.add_argument("--expect-sha256", default=None,
                        help="required trace SHA-256 (default: profile pin)")
    parser.add_argument("--classified", help="optional battle-timeline-classified.json")
    parser.add_argument("--expect-classified-sha256", default=None,
                        help="required classified SHA-256 when --classified is used")
    args = parser.parse_args(argv)
    runtime = args.runtime or args.profile == "runtime"
    try:
        if runtime:
            _require(args.unit_index is not None,
                     "--runtime/--profile runtime requires --unit-index")
            _require(args.classified is None,
                     "--classified is a legacy-profile option")
            expect_trace = (args.expect_sha256 if args.expect_sha256 is not None
                            else RUNTIME_TRACE_SHA256)
            manifest = extract_runtime_file(args.trace, args.unit_index, expect_trace,
                                            args.expect_unit_index_sha256)
            targets = write_runtime_outputs(manifest, args.out)
            print("wrote %d runtime impacts, %d units, %d lifecycle destructions to %s"
                  % (len(manifest["events"]), len(manifest["units"]),
                     len(manifest["damage_lifecycle_observations"]), targets[0].parent))
            return 0
        expect_trace = (args.expect_sha256 if args.expect_sha256 is not None
                        else TRACE_SHA256)
        manifest = extract_file(args.trace, expect_trace, args.classified,
                                args.expect_classified_sha256)
        targets = write_outputs(manifest, args.out)
    except (AarTraceError, OSError) as error:
        print("aar_events: %s" % error, file=sys.stderr)
        return 2
    print("wrote %d events, %d modules to %s"
          % (len(manifest["events"]), len(manifest["modules"]), targets[0].parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
