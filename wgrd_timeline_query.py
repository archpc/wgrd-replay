"""Pure query helpers over an exported timeline's event list.

Read-only views: filtering, per-reference history and request counts. These
functions never mutate their inputs, never reclassify interpretations, and
never assign execution outcomes. Contextual kind-39 requests and unknown
execution outcomes are counted as reported, not resolved.

Usage:
    from wgrd_replay import parse_replay
    from wgrd_timeline import build_timeline
    from wgrd_timeline_query import filter_events, reference_history, request_summary

    events = build_timeline(parse_replay(path.read_bytes()))["events"]
    impacts = filter_events(events, opcode=0x07, frame_min=4042, frame_max=4166)
    history = reference_history(events, reference_id)
    counts = request_summary(events)

Event dicts are shared with the input timeline (shallow); do not mutate them.
"""
import re

_SCOPED_ID = re.compile(r"[0-9a-f]{64}:.+\Z")


def filter_events(events, *, opcode=None, slot=None, frame_min=None,
                  frame_max=None, action=None, status=None):
    """Return events matching ALL given criteria, in input order.

    opcode: int 0..255. slot: non-negative int (recorded pact slot).
    frame_min/frame_max: inclusive non-negative int bounds. action/status:
    exact strings matched against interpretation fields; events with a None
    action match only when no action filter is given, or when action="None"
    (which selects the summary's None-action bucket). opcode=None means no
    opcode filter; unresolved tail events (opcode None) are selectable via
    action="None".
    """
    if opcode is not None and (not isinstance(opcode, int) or isinstance(opcode, bool)
                               or not 0 <= opcode <= 0xFF):
        raise ValueError("opcode must be an int in 0..255")
    for name, value in (("slot", slot), ("frame_min", frame_min), ("frame_max", frame_max)):
        if value is not None and (not isinstance(value, int) or isinstance(value, bool)
                                  or value < 0):
            raise ValueError("%s must be a non-negative int" % name)
    if frame_min is not None and frame_max is not None and frame_min > frame_max:
        raise ValueError("frame_min must not exceed frame_max")
    for name, value in (("action", action), ("status", status)):
        if value is not None and not isinstance(value, str):
            raise ValueError("%s must be a string" % name)
    out = []
    for e in events:
        if opcode is not None and e["opcode"] != opcode:
            continue
        if slot is not None and e["player_slot"] != slot:
            continue
        if frame_min is not None and e["frame"] < frame_min:
            continue
        if frame_max is not None and e["frame"] > frame_max:
            continue
        interpretation = e["interpretation"]
        if action is not None:
            # "None" selects the summary's None-action bucket (unresolved
            # tails and uninterpreted requests); no real action is named None.
            if action == "None":
                if interpretation["action"] is not None:
                    continue
            elif interpretation["action"] != action:
                continue
        if status is not None and interpretation["status"] != status:
            continue
        out.append(e)
    return out


def reference_history(events, reference_id):
    """Return events referencing reference_id, ordered by command_order.

    Checks interpretation.parameters actor_references, target_references and
    the singular target_reference (0x18 supply requests) for the catalog
    reference_id (a scoped string "<replay_sha256>:<ref_hex>").
    No resolution or identity is inferred.
    """
    if not isinstance(reference_id, str) or not _SCOPED_ID.match(reference_id):
        raise ValueError(
            "reference_id must be a scoped catalog id '<64-hex sha256>:<ref_hex>'")
    out = []
    for e in events:
        params = e["interpretation"].get("parameters") or {}
        for role in ("actor_references", "target_references"):
            refs = params.get(role) or ()
            if any(r.get("reference_id") == reference_id for r in refs):
                out.append(e)
                break
        else:
            single = params.get("target_reference")
            if isinstance(single, dict) and single.get("reference_id") == reference_id:
                out.append(e)
    out.sort(key=lambda e: e["command_order"])
    return out


def request_summary(events):
    """Count requests by action, status, slot, opcode; report kind-39 and
    execution-outcome distributions exactly as interpreted. No semantics.

    None actions/outcomes are counted under the string "None"; unresolved
    tail events (opcode None) likewise count under by_opcode "None".
    by_slot keys are ints; by_opcode keys are lowercase "0x%02x" strings.
    contextual_kind39 counts interpretation.parameters.order_kind_u32 == 39
    independently of the action counts (kind-39 requests keep their reported
    action/status).
    """
    by_action, by_status, by_slot, by_opcode, outcomes = {}, {}, {}, {}, {}
    kind39 = 0
    for e in events:
        interpretation = e["interpretation"]
        action = str(interpretation["action"])
        by_action[action] = by_action.get(action, 0) + 1
        status = interpretation["status"]
        by_status[status] = by_status.get(status, 0) + 1
        slot = e["player_slot"]
        by_slot[slot] = by_slot.get(slot, 0) + 1
        op = "0x%02x" % e["opcode"] if e["opcode"] is not None else "None"
        by_opcode[op] = by_opcode.get(op, 0) + 1
        outcome = str(interpretation.get("execution_outcome"))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        params = interpretation.get("parameters") or {}
        if params.get("order_kind_u32") == 39:
            kind39 += 1
    return {
        "total": len(events),
        "by_action": dict(sorted(by_action.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_slot": dict(sorted(by_slot.items())),
        "by_opcode": dict(sorted(by_opcode.items())),
        "contextual_kind39": kind39,
        "execution_outcomes": dict(sorted(outcomes.items())),
    }