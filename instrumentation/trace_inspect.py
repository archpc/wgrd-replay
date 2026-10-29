#!/usr/bin/env python3
"""Inspect WGRD Frida JSONL calls without assigning gameplay semantics."""


import argparse
from collections import Counter
import json
from pathlib import Path


def summarize(events):
    """Report observed per-thread nesting; never promote it to game semantics."""
    active = {}
    thread_stacks = {}
    seen = set()
    issues = set()
    counts = Counter()
    relations = []
    summary = None
    ended = False
    for event in events:
        kind = event.get("event")
        if kind == "enter":
            call = event["call_id"]
            counts[event["hook"]] += 1
            if call in seen:
                issues.add("duplicate_call_id")
            seen.add(call)
            thread = event["thread_id"]
            stack = thread_stacks.setdefault(thread, [])
            if event.get("stale_frames_discarded", 0):
                issues.add("stale_frames_discarded")
                stack.clear()
            parent_id = event.get("parent_call_id")
            if parent_id is not None:
                if not event.get("parent_recorded"):
                    issues.add("unrecorded_parent")
                else:
                    parent = active.get(parent_id)
                    if (parent is None or parent["thread_id"] != thread or
                            not stack or stack[-1] != parent_id):
                        issues.add("invalid_parent")
                    else:
                        relations.append({"parent": parent_id, "child": call})
            elif stack:
                issues.add("missing_parent_in_stack")
                stack.clear()
            active[call] = event
            stack.append(call)
        elif kind == "leave":
            thread = event["thread_id"]
            stack = thread_stacks.setdefault(thread, [])
            prior = active.pop(event["call_id"], None)
            if prior is None:
                issues.add("unmatched_leave")
            elif prior["thread_id"] != thread or prior["hook"] != event["hook"]:
                issues.add("leave_identity_mismatch")
            if not event.get("stack_match", False) or not stack or stack[-1] != event["call_id"]:
                issues.add("stack_mismatch")
                stack.clear()
            else:
                stack.pop()
        elif kind == "summary":
            summary = event
            if event.get("suppressed", 0):
                issues.add("events_suppressed")
            if event.get("callback_errors", 0):
                issues.add("callback_error")
            if event.get("stack_mismatches", 0):
                issues.add("stack_mismatch")
            if event.get("stale_frames", 0):
                issues.add("stale_frames_discarded")
            if event.get("outstanding_threads", 0):
                issues.add("outstanding_threads")
        elif kind in ("failure", "script_error", "callback_error", "cleanup_error"):
            issues.add(kind)
        elif kind == "end":
            ended = True
            if event.get("cleanup_errors", 0):
                issues.add("cleanup_error")
    if active:
        issues.add("unmatched_enter")
    if summary is None:
        issues.add("missing_summary")
    if not ended:
        issues.add("missing_end")
    return {"observed_enters": dict(counts), "relations": relations,
            "unmatched_enters": len(active), "issues": sorted(issues), "summary": summary}


def match_order_requests(events, timeline):
    """Find replay candidates whose raw fields equal captured wrapper bytes."""
    digest = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
    starts = [e for e in events if e.get("event") == "start"]
    identities = [e for e in events if e.get("event") == "identity_verified"]
    if (len(starts) != 1 or len(identities) != 1 or starts[0].get("sha256") != digest or
            starts[0].get("revision") != "131544" or
            identities[0].get("module", {}).get("name", "").lower() != "wargame3.exe" or
            timeline.get("header", {}).get("game_version") != "131544" or
            timeline.get("header", {}).get("digest_valid") is not True):
        raise ValueError("matching requires identity-verified revision 131544 and a digest-valid timeline")
    candidates = []
    for event in timeline["events"]:
        if event.get("opcode") != 7:
            continue
        params = event["parameters"]
        actors = params["obj_04_array"]
        count = actors["count_u32"]
        if not 1 <= count <= 4:
            continue
        actor = bytes.fromhex(actors["items_hex"])
        structure = bytes.fromhex(params["obj_d0_hex"])
        if len(actor) != 20 * count or len(structure) != 36:
            raise ValueError("unexpected actor-reference or structure length")
        candidates.append((actor, structure, {"frame": event["frame"], "slot": event["player_slot"],
                                               "file_offset": event["source"]["file_offset"]}))
    matches = []
    for event in events:
        if event.get("event") != "enter" or event.get("hook") != "order_request_wrapper":
            continue
        reads = {r["offset"]: r["result"] for r in event.get("reads", []) if r.get("source") == "ecx"}
        found = []
        a, s = reads.get(4, {}), reads.get(208, {})
        if a.get("ok") and s.get("ok"):
            captured = bytes.fromhex(a["hex"])
            structure = bytes.fromhex(s["hex"])
            if len(structure) == 36:
                found = [location for raw_actor, raw_struct, location in candidates
                         if len(captured) >= len(raw_actor) and captured[:len(raw_actor)] == raw_actor
                         and structure == raw_struct]
        matches.append({"call_id": event["call_id"], "candidates": found})
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--relations", action="store_true", help="include all observed call-id relations")
    parser.add_argument("--replay", type=Path, help="strictly parse a private revision-131544 replay")
    args = parser.parse_args()
    with args.trace.open(encoding="utf-8") as source:
        events = [json.loads(line) for line in source if line.strip()]
    result = summarize(events)
    if args.replay:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        import wgrd_replay
        import wgrd_timeline
        timeline = wgrd_timeline.build_timeline(wgrd_replay.parse_replay(args.replay.read_bytes()))
        result["replay_sha256"] = timeline["sha256"]
        result["request_candidates"] = match_order_requests(events, timeline)
    if not args.relations:
        result["relation_count"] = len(result.pop("relations"))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
