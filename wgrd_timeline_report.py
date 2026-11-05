#!/usr/bin/env python3
"""Complete structural timeline export: every frame, pact and command, with coverage.

Layered over wgrd_replay.parse_replay and wgrd_timeline.build_timeline; adds
no decoding. Writes timeline.json (machine-readable) and timeline.md
(human-readable) with exclusive create. Output is deterministic for one input.

Time domains are kept separate. The replay frame index is known for each event.
The engine tick quantum (0.2 s per frame, static and observed at 5 Hz) gives
seconds since replay load. One capture observed the deterministic clock lagging
the frame counter by an integer 10 or 11 frames; the 10.5 midpoint is only a
statistic, so each event carries an estimate with bounds. Verified battle time,
battle start, game time, deterministic ticks per event and wall clock stay null
(see CLOCK_MAPPING). Runtime AAR observations are not merged, because no
frame correlation exists.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys

from wgrd_replay import CHUNK_HEADER_SIZE, ReplayFormatError, iter_chunks, json_safe, parse_header, parse_replay
from wgrd_timeline import build_timeline

SCHEMA = "wgrd_structural_timeline/2"
ROOT = Path(__file__).resolve().parent
SOURCES = ("wgrd_replay.py", "wgrd_timeline.py", "wgrd_orders.py", "wgrd_entities.py",
           "wgrd_production.py", "wgrd_timeline_report.py")

# Engine tick quantum: 0.2 s per consumed frame, taken from the pinned bytes of
# 0xb34060 (comiss/subss against 0x195d768 = 0x3e4ccccd, the same constant that
# 0xaaedf0 uses to scale deterministic ticks into seconds). Applied to events as
# a derived offset from replay load, never as battle time.
FRAME_SECONDS = 0.2

# One authorized 131544 playback (2026-11-02, trace b3a60af4...) observed the
# deterministic tick counter one tick per frame, lagging the frame counter by an
# integer difference of 10 or 11 frames (48 and 47 samples, 462 s, no drift).
# The 10.5 midpoint is a sample statistic, not an observed synchronization
# boundary; it is applied only as a labelled estimate with frame bounds, and
# never as verified battle time.
FRAME_TICK_DIFFERENCE_OBSERVED = (10, 11)
FRAME_TICK_DIFFERENCE_ESTIMATE = 10.5

# Evidence for frame -> simulation-clock mapping, revision 131544. Every value
# below is a measurement or static fact. Only the derived offset is applied to
# events; deterministic ticks and battle time are not.
CLOCK_MAPPING = {
    "status": "clock_rate_observed_frame_tick_difference_unresolved_battle_start_unknown",
    "frame_seconds": FRAME_SECONDS,
    "frame_seconds_basis": "static_engine_tick_quantum_and_observed_5hz",
    "frame_tick_difference_observed": list(FRAME_TICK_DIFFERENCE_OBSERVED),
    "frame_tick_difference_samples": {"10": 48, "11": 47},
    "frame_tick_difference_estimate_frames": FRAME_TICK_DIFFERENCE_ESTIMATE,
    "frame_tick_difference_basis": "single_capture_statistic_2026-11-02_speed_1",
    "frame_tick_difference_status": "integer_10_or_11_observed_boundary_unresolved",
    "frame_to_deterministic_tick": None,
    "frame_origin": "replay_load (frame counter zeroed by 0xb2cfe0)",
    "verified_battle_time": None,
    "derived_event_fields": {
        "time.t_from_replay_load_seconds": "frame * 0.2 (frame counter, origin at load)",
        "time.estimated_deterministic_time_seconds": "(frame - 10.5) * 0.2, statistic, with "
                                                    "bounds (frame - 11) .. (frame - 10)",
    },
    "verified": [
        "Observed (authorized playback, replay abf6a5e9..., trace b3a60af4...): frame 0 at "
        "22:38:42.856Z with the replay byte +0xa5 = 1; 2311 frames in 462.65 s = 4.995 frames/s.",
        "Observed (same trace): all 10965 paired tick_step calls move the frame index by 0 (8576) "
        "or +1 (2389). No skip, repeat or multi-frame advance.",
        "Observed (same trace): 95 clock samples spanning deterministic ticks 13..2293 give "
        "frame - tick = 10 (48 samples) or 11 (47 samples), no drift over 462 s, so the tick "
        "counter is one tick per frame and lags the frame counter by an integer 10 or 11 "
        "frames; the exact synchronization boundary is unresolved.",
        "Observed (same trace): the replay HUD showed 00:00:00 - 00:13:53. (4174 - 11..10) * 0.2 "
        "= 832.6..832.8 s also displays as 13:53, so the duration is consistent with the "
        "deterministic clock. Consistency is not identity: the HUD clock was not read directly.",
        "Static: the per-tick step 0xb34060 accumulates real seconds in +0x68 and, at "
        "0xb3473a/0xb34758, compares against and subtracts 0.2f (0x195d768 = 0x3e4ccccd), "
        "then advances the frame index by exactly one at 0xb349bd. One quantum, one frame.",
        "Static: the same 0.2f constant scales [TGameplayServices+0xd0] to deterministic "
        "seconds in 0xaaedf0 (binding 0x1d9cd68 -> 0xa406b0).",
        "Static: the frame counter is zeroed by the manager reset 0xb2cfe0, so frame 0 is "
        "the replay-load origin, not battle start.",
        "Observed (trace native-v3b-replay.jsonl, replay abf6a5e9...): frame_apply_candidate "
        "(0xb2b310) returning to 0xb3dcd2 received keys 0..4173, one per replay frame, within "
        "0.385 s of guest wall clock and before the main clock receiver's first sample. At that "
        "call site all frames arrive in one burst, so the call does not mark per-tick simulation.",
        "Observed (same trace): the main clock receiver's counter is non-decreasing and its maximum "
        "sample (4164) is below the replay's 4174 frames.",
    ],
    "hypotheses": [
        {"id": "H1", "claim": "one replay frame = one deterministic tick, origin frame 0",
         "status": "rate_observed_offset_integer_10_or_11_boundary_unresolved",
         "detail": "Rate confirmed at 1:1 in a live replay. The counters do not share an origin; "
                   "the exact integer frame/tick boundary is unresolved (10 and 11 both observed).",
         "test": "tests/test_aar_hypotheses.py"},
        {"id": "H2", "claim": "battle time starts at the opcode-0x13 frame",
         "status": "untested_runtime_phase_hook_never_fired",
         "detail": "0xab4780 produced 0 calls in 481.8 s of load and playback.",
         "test": "tests/test_aar_hypotheses.py"},
        {"id": "H4", "claim": "damage-clock seconds / 0.2 place AAR events on replay frames",
         "status": "corrected_by_measured_offset",
         "detail": "frame = seconds/0.2 is off by an unresolved 10- or 11-frame difference: "
                   "806.4 s -> frames 4042..4043, 830.8 s -> frames 4164..4165. The earlier 4154 "
                   "match is withdrawn; no capture yet carries both hooks.",
         "test": "tests/test_timeline_report.py"},
    ],
    "unknowns": [
        {"field": "battle start / phase boundary",
         "status": "unknown",
         "detail": "0xab4780 was never called in 481.8 s of load and playback, so it is not the "
                   "replay phase path. Deployment length and the battle-start frame are unknown.",
         "smallest_experiment": "Hook the phase manager store 0x6d17e0 and the gameplay-services "
                                "flags +0x20..0x22 for one full-length playback."},
        {"field": "exact frame/tick synchronization boundary",
         "status": "unresolved",
         "detail": "Samples give frame - tick = 10 or 11 with no drift. The 10.5 midpoint is a "
                   "statistic; nothing observed a tick and a frame advance at the same instant.",
         "smallest_experiment": "Hook the tick store and the frame increment in the same call path "
                                "with a monotonic sequence number, or read both in one hook entry."},
        {"field": "offset generalization",
         "status": "single_observation",
         "detail": "The 10/11-frame difference comes from one replay at speed 1 on one machine. "
                   "Other speeds, replays or process epochs are unmeasured; no universal offset "
                   "may be applied.",
         "smallest_experiment": "Repeat the same two hooks once at speed 2 and once on another replay."},
    ],
    "evidence": ["research/current-build/2026-11-02-frame-tick-capture.md",
                 "research/current-build/2026-11-02-frame-clock-consumption.md",
                 "research/current-build/2026-11-02-aar-release.md#6-timing-evidence",
                 "research/current-build/2026-11-02-causal-chain.md"],
}

# How recorded commands reach the simulation, from the same static pass.
EXECUTION_MODEL = {
    "status": "static_dispatch_path_with_unproven_outcomes",
    "bulk_load": {
        "reader": "0xb3ccb0 -> 0xb3dbc0 (TNetworkEventSourceFromReplay vtable slot 1)",
        "store": "0xb2b310 keyed insertion, frame -> per-slot payload map",
        "meaning": "whole-file load; no simulation runs between inserted frames",
        "observed": "4176 insertions, keys 0..4173, one 0.385 s burst (trace native-v3b-replay.jsonl)",
    },
    "per_tick": {
        "step": "0xb34060",
        "quantum_seconds": FRAME_SECONDS,
        "frame_advance": "exactly one frame index per consumed quantum (0xb349bd)",
        "missing_frame_padding": "0xb35650 inserts the shared empty payload (DAT_02039d00) for "
                                 "unrecorded frames up to the current index",
        "dispatch": "0xb34060 loops the slot array (+0x7c/+0x80) for entries whose pending frame "
                    "equals frame - [manager+0xb0], applies the slot queue ([+0xcc] vtable +4/+8), "
                    "then dispatches that slot's payload ([+0x8c] vtable +0x10)",
    },
    "order_apply": {"class": "TNetworkActionGiveOrderStandard",
                    "method": "0xb2be30 (vtable slot 1, observed as order_request_wrapper)",
                    "outcome": "unknown; a request path, no trace observes its return"},
    "not_claimed": ["intra-tick ordering across slots",
                    "command success or rejection",
                    "player identity from the recorded slot"],
}
TIME_DOMAINS = {
    "frame_index": "known: replay star index, contiguous from 0",
    "t_from_replay_load_seconds": "derived: frame * 0.2 (static tick quantum; origin = replay load)",
    "estimated_deterministic_time_seconds": "statistic: (frame - 10.5) * 0.2 from one capture, with "
                                            "bounds (frame - 11) * 0.2 .. (frame - 10) * 0.2; "
                                            "negative values are pre-roll frames",
    "deterministic_ticks": None,
    "deterministic_seconds": None,
    "game_time": None,
    "battle_time": None,
    "wall_clock": None,
    "origins": {"frame_index": "first star chunk", "deterministic_ticks": "unknown",
                "battle_time": "replay load, per the displayed replay timeline",
                "t_from_replay_load_seconds": "frame counter zero (0xb2cfe0 reset)",
                "wall_clock": "replay carries no wall-clock field"},
}
AAR_INTEGRATION = {
    "status": "not_integrated",
    "reason": "Retained AAR traces bind to replay abf6a5e9... by manifest hash and content, "
              "but no observation carries a replay frame; merging would invent timestamps.",
    "see": "research/current-build/2026-11-02-aar-release.md",
}


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _frame_table(b):
    """Independent chunk walk: star/pact/endt per frame, nothing dropped."""
    header, _ = parse_header(b)
    frames, current = [], None
    for offset, tag, payload in iter_chunks(b, header["payload_offset"]):
        if tag == b"star":
            index = struct.unpack_from("<I", payload, 0)[0]
            current = {"frame": index, "star_offset": offset,
                       "star_tail_hex": payload[4:].hex(), "pacts": []}
        elif tag == b"pact":
            frame, slot, count, length = struct.unpack_from("<IIIH", payload, 0)
            current["pacts"].append({"slot": slot, "declared_commands": count,
                                     "block_length": length, "chunk_offset": offset,
                                     "block_file_offset": offset + CHUNK_HEADER_SIZE + 14,
                                     "frame_field": frame})
        elif tag == b"endt":
            current["endt_offset"] = offset
            current["endt_frame_field"] = struct.unpack_from("<I", payload, 0)[0]
            current["endt_tail_hex"] = payload[4:].hex()
            frames.append(current)
            current = None
    return frames


def _checks(frames, events, b):
    """Gaps, ordering, duplicates and exact byte coverage. Failures raise."""
    failures = []
    if [f["frame"] for f in frames] != list(range(len(frames))):
        failures.append("frame indices are not contiguous from 0")
    for f in frames:
        if f["endt_frame_field"] != f["frame"] or any(p["frame_field"] != f["frame"] for p in f["pacts"]):
            failures.append("frame field mismatch in frame %d" % f["frame"])
        slots = [p["slot"] for p in f["pacts"]]
        if slots != sorted(set(slots)):
            failures.append("slot order violation in frame %d" % f["frame"])
    if [e["command_order"] for e in events] != list(range(len(events))):
        failures.append("command_order is not contiguous")
    keys = [(e["frame"], e["source"]["chunk_offset"], e["slot_command_order"]) for e in events]
    if keys != sorted(keys) or len(set(keys)) != len(keys):
        failures.append("event ordering violation or duplicate event key")
    by_chunk = {}
    for e in events:
        by_chunk.setdefault(e["source"]["chunk_offset"], []).append(e)
    declared = 0
    for f in frames:
        for p in f["pacts"]:
            declared += p["declared_commands"]
            group = by_chunk.pop(p["chunk_offset"], [])
            if len(group) != p["declared_commands"]:
                failures.append("pact 0x%x declares %d commands, %d exported"
                                % (p["chunk_offset"], p["declared_commands"], len(group)))
            start = p["block_file_offset"]
            block = b[start:start + p["block_length"]]
            if all(e["raw_hex"] is not None for e in group):
                if b"".join(bytes.fromhex(e["raw_hex"]) for e in group) != block:
                    failures.append("pact 0x%x raw bytes not covered exactly once" % p["chunk_offset"])
    if by_chunk:
        failures.append("events reference unknown pact chunks")
    if failures:
        raise ReplayFormatError("structural timeline: " + "; ".join(failures))
    duplicates = []
    seen = {}
    for e in events:
        key = (e["frame"], e["player_slot"], e["raw_hex"])
        if e["raw_hex"] is not None and key in seen:
            duplicates.append({"command_order": e["command_order"], "duplicate_of": seen[key],
                               "frame": e["frame"], "player_slot": e["player_slot"]})
        else:
            seen.setdefault(key, e["command_order"])
    return {"frame_gaps": 0, "ordering_violations": 0, "duplicate_event_keys": 0,
            "declared_commands": declared, "exported_commands": len(events),
            "silently_discarded_commands": declared - len(events),
            "pact_bytes_covered_exactly_once": True,
            "identical_raw_commands_in_same_frame_and_slot": duplicates,
            "duplicate_note": "Identical raw commands are flagged, retained and not merged; "
                              "repetition can be genuine input."}


def _undecoded(event):
    flags = []
    if event["decode_status"] != "layout":
        flags.append("payload_" + event["decode_status"])
    interpretation = event["interpretation"]
    if interpretation["status"] == "unknown":
        flags.append("interpretation_unknown")
    if interpretation.get("execution_outcome") == "unknown":
        flags.append("execution_outcome_unknown")
    if event["layout_status"] != "matching_build":
        flags.append("layout_inferred_from_build_59638")
    return flags


def _actors(event):
    parameters = event["interpretation"].get("parameters") or {}
    out = {}
    for role in ("actor_references", "target_references"):
        if parameters.get(role):
            out[role] = [r["reference_id"] for r in parameters[role]]
    return out


def build_report(b):
    parsed = parse_replay(b, include_empty=True)
    timeline = build_timeline(parsed)
    frames = _frame_table(b)
    events = timeline["events"]
    checks = _checks(frames, events, b)
    rows = []
    for e in events:
        rows.append({
            "command_order": e["command_order"], "frame": e["frame"],
            "player_slot": e["player_slot"], "player_identity": None,
            "slot_command_order": e["slot_command_order"],
            "frame_command_order": e["frame_command_order"],
            "opcode": e["opcode"], "class": e["class"], "raw_hex": e["raw_hex"],
            "source": e["source"], "decode_status": e["decode_status"],
            "layout_status": e["layout_status"], "parameters": e["parameters"],
            "interpretation": e["interpretation"],
            "time": {"frame_index": e["frame"],
                     "t_from_replay_load_seconds": round(e["frame"] * FRAME_SECONDS, 3),
                     "t_basis": "derived_from_static_tick_quantum",
                     "estimated_deterministic_time_seconds":
                         round((e["frame"] - FRAME_TICK_DIFFERENCE_ESTIMATE) * FRAME_SECONDS, 3),
                     "estimated_deterministic_time_bounds_seconds": [
                         round((e["frame"] - FRAME_TICK_DIFFERENCE_OBSERVED[1]) * FRAME_SECONDS, 3),
                         round((e["frame"] - FRAME_TICK_DIFFERENCE_OBSERVED[0]) * FRAME_SECONDS, 3)],
                     "estimated_time_basis": "single_capture_statistic",
                     "deterministic_ticks": None, "game_time": None,
                     "wall_clock": None},
            "references": _actors(e), "undecoded": _undecoded(e),
        })
    for f in frames:
        f["command_orders"] = [r["command_order"] for r in rows if r["frame"] == f["frame"]]
    by_opcode = {}
    for r in rows:
        bucket = by_opcode.setdefault("0x%02x" % r["opcode"], Counter())
        bucket[r["interpretation"]["status"]] += 1
    game = parsed["metadata"].get("game", {})
    alliances = {k: v.get("PlayerAlliance") for k, v in sorted(parsed["metadata"].items())
                 if k.startswith("player_") and isinstance(v, dict)}
    flagged = Counter(flag for r in rows for flag in r["undecoded"])
    report = {
        "schema": SCHEMA,
        "generator": {"sources": {name: _sha256((ROOT / name).read_bytes()) for name in SOURCES}},
        "replay": {"sha256": parsed["sha256"], "size": parsed["size"],
                   "game_version": parsed["header"]["game_version"],
                   "digest_valid": parsed["header"]["digest_valid"],
                   "map": game.get("Map"), "unknown_chunks": len(parsed["unknown_chunks"])},
        "teams": {"metadata_alliance_by_player_key": alliances,
                  "recorded_slots": sorted({p["slot"] for f in frames for p in f["pacts"]}),
                  "slot_to_player": None,
                  "status": "slot-to-player and slot-to-alliance links are unproven"},
        "time_domains": TIME_DOMAINS, "clock_mapping": CLOCK_MAPPING,
        "execution_model": EXECUTION_MODEL, "aar_integration": AAR_INTEGRATION,
        "integrity": checks,
        "coverage": {
            "frames": len(frames),
            "frames_with_commands": sum(1 for f in frames if f["command_orders"]),
            "pacts": sum(len(f["pacts"]) for f in frames),
            "commands": len(rows),
            "unresolved_spans": len(timeline["unresolved_spans"]),
            "decode_status": dict(sorted(Counter(r["decode_status"] for r in rows).items())),
            "interpretation_status": dict(sorted(Counter(r["interpretation"]["status"] for r in rows).items())),
            "interpretation_status_by_opcode": {k: dict(sorted(v.items())) for k, v in sorted(by_opcode.items())},
            "undecoded_flags": dict(sorted(flagged.items())),
            "commands_with_references": sum(1 for r in rows if r["references"]),
            "verified_fields": {
                "queue_request": sum(1 for r in rows if ((r["interpretation"].get("parameters") or {})
                                                        .get("queue_request") or {}).get("status") == "verified"),
                "note": "Field-level request semantics verified for this replay Version; "
                        "the enclosing event status stays as reported."},
            "timing": {"frame_index": len(rows), "derived_seconds": len(rows),
                       "estimated_deterministic_time": len(rows),
                       "deterministic_ticks": 0, "game_time": 0, "battle_time": 0,
                       "wall_clock": 0},
        },
        "frames": frames, "events": rows,
        "unresolved_spans": timeline["unresolved_spans"],
        "entity_references": timeline["entity_references"],
    }
    return json_safe(report)


def render_markdown(report):
    c, r, i = report["coverage"], report["replay"], report["integrity"]
    lines = ["# Structural timeline", "",
             "Replay SHA-256 `%s`, version %s, %d bytes, digest valid: %s." %
             (r["sha256"], r["game_version"], r["size"], r["digest_valid"]), "",
             "## Coverage", "",
             "| measure | value |", "|---|---:|"]
    for key in ("frames", "frames_with_commands", "pacts", "commands", "unresolved_spans",
                "commands_with_references"):
        lines.append("| %s | %d |" % (key, c[key]))
    lines.append("| silently discarded commands | %d |" % i["silently_discarded_commands"])
    lines += ["", "Interpretation status: " + ", ".join("%s %d" % kv for kv in c["interpretation_status"].items()),
              "Decode status: " + ", ".join("%s %d" % kv for kv in c["decode_status"].items()),
              "Undecoded flags: " + ", ".join("%s %d" % kv for kv in c["undecoded_flags"].items()),
              "Verified request fields: queue_request %d." % c["verified_fields"]["queue_request"],
              "Timing: frame index, t+ and the estimated deterministic time for %d/%d commands; "
              "verified battle time, game time and wall clock stay null." %
              (c["timing"]["estimated_deterministic_time"], c["commands"]), "",
              "## Time", "",
              "Per event, `t+` is `frame * 0.2` seconds since the replay was loaded. `est` is "
              "`(frame - 10.5) * 0.2`, a statistic from one capture whose observed integer "
              "frame/tick difference is 10 or 11 frames; every event also carries its bounds "
              "(negative values are pre-roll frames). The 0.2 s quantum and the "
              "one-frame-per-tick advance (`0xb34060`) are static and were observed at 5.00 Hz. "
              "Frame-to-tick mapping: %s. Verified battle time, battle start, game time and "
              "deterministic ticks per event stay null." %
              report["clock_mapping"]["status"],
              "", "## Execution model", "",
              "Load and execution are separate. The reader stores every frame in one burst; "
              "the simulation then consumes exactly one frame per 0.2 s tick, applies that "
              "frame's command payload per slot, and pads unrecorded frames with an explicit "
              "empty payload. A recorded command is a request: its execution outcome is unknown.",
              "", "## Unplaced native observations", "",
              "Retained AAR traces carry damage and destruction events with engine deterministic "
              "seconds but no replay frame. They are not merged here: H4 (seconds/0.2 as a frame "
              "index) is arithmetic consistency only, not a proven shared origin.",
              "", "## Integrity", "",
              "Frame gaps 0, ordering violations 0, pact bytes covered exactly once. "
              "Identical raw commands in the same frame and slot (retained): %d." %
              len(i["identical_raw_commands_in_same_frame_and_slot"]),
              "", "## Command history (chronological)", "",
              "| # | frame | t+ (s) | est (s) | slot | opcode | class | decode | interpretation | action | flags |",
              "|---:|---:|---:|---:|---:|---|---|---|---|---|---|"]
    for e in report["events"]:
        lines.append("| %d | %d | %.1f | %.1f | %d | 0x%02x | %s | %s | %s | %s | %s |" % (
            e["command_order"], e["frame"], e["time"]["t_from_replay_load_seconds"],
            e["time"]["estimated_deterministic_time_seconds"],
            e["player_slot"], e["opcode"], e["class"] or "unknown",
            e["decode_status"], e["interpretation"]["status"], e["interpretation"].get("action") or "-",
            ", ".join(e["undecoded"]) or "-"))
    lines += ["", "## Frames", ""]
    run_start = None
    frames = report["frames"]
    for index, f in enumerate(frames):
        empty = not f["command_orders"]
        if empty and run_start is None:
            run_start = f["frame"]
        if run_start is not None and (not empty or index == len(frames) - 1):
            end = f["frame"] if empty else f["frame"] - 1
            lines.append("- frames %d-%d: no commands" % (run_start, end) if end > run_start
                         else "- frame %d: no commands" % run_start)
            run_start = None
        if not empty:
            lines.append("- frame %d: commands %s" % (f["frame"], ", ".join(map(str, f["command_orders"]))))
    return "\n".join(lines) + "\n"


def write_outputs(report, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    payloads = {"timeline.json": json.dumps(report, sort_keys=True, indent=1, ensure_ascii=False,
                                            allow_nan=False) + "\n",
                "timeline.md": render_markdown(report)}
    targets = [out / name for name in payloads]
    existing = [str(t) for t in targets if t.exists()]
    if existing:
        raise FileExistsError("refusing to overwrite: " + ", ".join(existing))
    for target in targets:
        with open(target, "x", encoding="utf-8") as handle:
            handle.write(payloads[target.name])
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("replay")
    parser.add_argument("--out", required=True, help="output directory (files are exclusively created)")
    args = parser.parse_args(argv)
    try:
        report = build_report(Path(args.replay).read_bytes())
        targets = write_outputs(report, args.out)
    except (ReplayFormatError, OSError) as error:
        print("wgrd_timeline_report: %s" % error, file=sys.stderr)
        return 2
    c = report["coverage"]
    print("wrote %d frames, %d commands (%d discarded) to %s"
          % (c["frames"], c["commands"], report["integrity"]["silently_discarded_commands"], targets[0].parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
