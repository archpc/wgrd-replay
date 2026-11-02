#!/usr/bin/env python3
"""Complete structural timeline export: every frame, pact and command, with coverage.

Layered over wgrd_replay.parse_replay and wgrd_timeline.build_timeline; adds
no decoding. Writes timeline.json (machine-readable) and timeline.md
(human-readable) with exclusive create. Output is deterministic for one input.

Time domains are kept separate. Only the replay frame index is known for each
event. Deterministic ticks, game/battle time and wall-clock time are null:
no evidence binds a replay frame to the engine counter (see CLOCK_MAPPING).
Runtime AAR observations are not merged, because no frame correlation exists.
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

SCHEMA = "wgrd_structural_timeline/1"
ROOT = Path(__file__).resolve().parent
SOURCES = ("wgrd_replay.py", "wgrd_timeline.py", "wgrd_orders.py", "wgrd_entities.py",
           "wgrd_production.py", "wgrd_timeline_report.py")

# Evidence for frame -> simulation-clock mapping, revision 131544. Every value
# below is a measurement or static fact; none is applied to events.
CLOCK_MAPPING = {
    "status": "unresolved",
    "frame_to_deterministic_tick": None,
    "frame_duration_seconds": None,
    "verified": [
        "Static: DeterministicCurrentTimeInSeconds (0x1d9cd68 -> 0xa406b0) returns "
        "[container+0xd0] * 0.2 via 0xaaedf0 (constant 0x195d768 = 0x3e4ccccd). "
        "This scales engine ticks to deterministic seconds; it does not relate ticks to replay frames.",
        "Observed (trace native-v3b-replay.jsonl, replay abf6a5e9...): frame_apply_candidate "
        "(0xb2b310) returning to 0xb3dcd2 received keys 0..4173, one per replay frame, within "
        "0.385 s of guest wall clock and before the main clock receiver's first sample. At that "
        "call site all frames arrive in one burst, so the call does not mark per-tick simulation.",
        "Observed (same trace): the main clock receiver's counter is non-decreasing and its maximum "
        "sample (4164) is below the replay's 4174 frames.",
    ],
    "hypotheses": [
        {"id": "H1", "claim": "one replay frame = one deterministic tick, origin frame 0",
         "status": "tested_not_proven", "test": "tests/test_aar_hypotheses.py"},
        {"id": "H2", "claim": "battle time starts at the opcode-0x13 frame",
         "status": "tested_not_proven", "test": "tests/test_aar_hypotheses.py"},
    ],
    "evidence": ["research/current-build/2026-11-02-aar-release.md#6-timing-evidence",
                 "research/current-build/2026-11-02-causal-chain.md"],
}
TIME_DOMAINS = {
    "frame_index": "known: replay star index, contiguous from 0",
    "deterministic_ticks": None,
    "deterministic_seconds": None,
    "game_time": None,
    "battle_time": None,
    "wall_clock": None,
    "origins": {"frame_index": "first star chunk", "deterministic_ticks": "unknown",
                "battle_time": "unknown (H2 untested at runtime)",
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
            "time": {"frame_index": e["frame"], "deterministic_ticks": None, "game_time": None,
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
        "aar_integration": AAR_INTEGRATION,
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
            "timing": {"frame_index": len(rows), "deterministic_ticks": 0, "game_time": 0,
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
              "Timing: frame index for %d/%d commands; deterministic ticks, game time and wall clock 0." %
              (c["timing"]["frame_index"], c["commands"]), "",
              "## Time", "",
              "Frame index is the only per-event time. Frame-to-tick mapping: %s. "
              "Hypotheses H1/H2 are tested, not proven, and are not applied." % report["clock_mapping"]["status"],
              "", "## Integrity", "",
              "Frame gaps 0, ordering violations 0, pact bytes covered exactly once. "
              "Identical raw commands in the same frame and slot (retained): %d." %
              len(i["identical_raw_commands_in_same_frame_and_slot"]),
              "", "## Commands", "",
              "| # | frame | slot | opcode | class | decode | interpretation | action | flags |",
              "|---:|---:|---:|---|---|---|---|---|---|"]
    for e in report["events"]:
        lines.append("| %d | %d | %d | 0x%02x | %s | %s | %s | %s | %s |" % (
            e["command_order"], e["frame"], e["player_slot"], e["opcode"], e["class"] or "unknown",
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
