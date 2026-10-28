"""Lossless command timeline layered over the strict replay parser.

Interpretations are limited to offline execution traces in build 59638. An action
request is not proof that it succeeded in the running game.

Time: entries are ordered by replay frame and recorded slot, never by seconds.
The frame-to-seconds mapping is unresolved (time_basis). No repo source
establishes a tick rate; any ~5 Hz figure is an unvalidated hypothesis and is
not used here.
"""
from collections import Counter
import math

from wgrd_replay import CHUNK_HEADER_SIZE, OPCODE_CLASSES, ReplayFormatError

BUILD = "59638"
EXECUTION_EVIDENCE = [
    "research/evidence/ev_304797cebbe41bb5691f58b705012b4f3d976142c7e8861636100ab4200e3fe1.json",
    "research/evidence/ev_a4e70aaf2f167f9309aa8f3fff82967ae4bcdb593b776ed5a5c9bfaae4979d12.json",
    "research/evidence/ev_fa646c3ab4e806adc03f0016a8fe2da0032d194b16aa74087f528aaadcab2d52.json",
]


def _json_safe(value):
    """JSON has no NaN/Infinity. Keep their presence explicit; raw bytes survive."""
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite": "NaN" if math.isnan(value) else ("+Infinity" if value > 0 else "-Infinity")}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    return value


def _interpretation(opcode, fields, matched, slot=None):
    if opcode == 0x0c and fields is not None:
        from wgrd_production import decode_change_production
        return decode_change_production(fields, matched, slot)
    if opcode in (0x0a, 0x0d):
        from wgrd_production import decode_production_action
        try:
            production = decode_production_action(opcode, fields, None, matched)
        except ReplayFormatError as error:
            return {"status": "unknown", "action": None, "parameters": None,
                    "evidence": [], "payload_layout_status": "malformed",
                    "payload_layout_reason": str(error), "execution_outcome": "unknown"}
        if production is not None:
            return production
    result = {"status": "unknown", "action": None, "parameters": None, "evidence": []}
    if fields is None or opcode not in (0x07, 0x08, 0x09):
        return result
    result.update(status="verified" if matched else "inferred",
                  evidence=EXECUTION_EVIDENCE, evidence_build=BUILD,
                  execution_outcome="unknown")
    if not matched:
        result["limitation"] = "Replay build differs from executable; semantics transferred by layout only."
    # Requests only: execution, acceptance and success stay unknown. 08/09 use
    # the marker interpretation below; 07 delegates to the order decoder.
    if opcode == 0x08:
        # Requests a marker at a transmitted float3 with type and optional text.
        # Not a unit position observation or smoke deployment (TIMELINE-SEMANTICS 08).
        position = fields["position_f32"]
        result.update(action="create_map_marker", parameters={
            "position_f32": position if all(math.isfinite(v) for v in position) else None,
            "marker_type_u32": fields["type_u32"],
            "text_utf8": fields.get("text"),
            "text_bytes_hex": fields.get("text_hex", fields.get("text", "").encode("utf-8").hex()),
        })
        result["limitations"] = [
            "Position axes, units and map transform unresolved.",
            "Type 3 displays nonempty text; meanings of types 0/1/2 unresolved.",
            "Marker ID assigned at execution; cannot correlate removals from this command alone.",
        ]
        if result["parameters"]["position_f32"] is None:
            result["limitations"].append("Nonfinite position; inspect original bytes, no usable location asserted.")
    elif opcode == 0x09:
        # The ID is manager-local, assigned during simulation. Whether a marker
        # was removed is unknown from this command alone (TIMELINE-SEMANTICS 09).
        result.update(action="remove_map_marker", parameters={"marker_id_u32": fields["obj_18_u32"]})
        result["limitations"] = ["ID scoped to resolved player marker manager; affected marker and success unknown."]
    else:
        from wgrd_orders import decode_standard_order
        return decode_standard_order(fields, matched)
    return result


def build_timeline(parsed, unit_data=None):
    """Preserve commands in frame / recorded slot / serialized command order.

    Unknown single-command tails have a known boundary. Unknown tails containing
    multiple commands produce placeholders linked to one retained span. No byte
    scan or guessed opcode offsets. Malformed known layouts fail timeline export;
    the existing parser's diagnostic representation is unchanged.

    Ordering: records sort by (frame, chunk file offset). FORMAT.md section 4 says
    pact slots appear in slot order within a frame, so file offset stands in for
    recorded slot order. command_order is the global export index;
    frame_command_order counts across all slots in one frame; slot_command_order
    is the index inside one pact block. None of these is execution order,
    wall-clock time, or command completion.

    !! TRAP: frame index is not seconds. The replay clock and the battle clock
    !! have separate origins (controlled-experiment note, section 5). Do not
    !! divide frame count by a battle duration.
    """
    events, spans = [], []
    frame_orders = Counter()
    matched = str(parsed["header"]["game_version"]) == BUILD
    records = sorted(parsed["commands"], key=lambda r: (r["frame"], r["offset"]))
    for record in records:
        decoded = record["command_decode"]
        if decoded["status"] == "malformed":
            raise ReplayFormatError("timeline: malformed command block at 0x%x: %s" %
                                    (record["offset"], decoded.get("reason", "invalid command layout")))
        # 14 = pact payload prefix (frame, slot, count and length, FORMAT.md section 4
        # +0..+13) before the command block. Offsets are relative to the file.
        block_start = record["offset"] + CHUNK_HEADER_SIZE + 14

        def append(index, opcode, fields, raw, offset, length, boundary, status, span=None):
            frame = record["frame"]
            event = {
                "command_order": len(events), "frame": frame,
                "frame_command_order": frame_orders[frame],
                "player_slot": record["slot"], "player_identity": None,
                "slot_command_order": index,
                "opcode": opcode, "class": OPCODE_CLASSES.get(opcode),
                "class_status": "rtti_build_59638" if opcode in OPCODE_CLASSES else "unknown",
                "parameters": fields, "raw_hex": raw, "decode_status": status,
                "layout_status": "matching_build" if matched else "inferred_build_59638",
                "source": {"chunk_offset": record["offset"], "block_offset": offset,
                           "file_offset": block_start + offset if offset is not None else None,
                           "length": length, "boundary_known": boundary},
                "interpretation": _interpretation(opcode, fields, matched, record["slot"]),
            }
            if span is not None:
                event["source"]["unresolved_span"] = span
            events.append(event)
            frame_orders[frame] += 1

        commands = decoded["commands"]
        for index, command in enumerate(commands):
            append(index, command["opcode"], command["fields"], command["raw_hex"],
                   command["offset"], command["length"], True, command["field_decode_status"])
        remaining = record["count"] - len(commands)
        if remaining:
            raw = decoded["remaining_hex"]
            if remaining > len(raw) // 2:
                raise ReplayFormatError("timeline: remaining command count exceeds opcode bytes at 0x%x" %
                                        (block_start + decoded["consumed_bytes"]))
            first_opcode = int(raw[:2], 16)
            if remaining == 1:
                append(len(commands), first_opcode, None, raw, decoded["consumed_bytes"],
                       len(raw) // 2, True, "unknown")
            else:
                span_id = len(spans)
                spans.append({"id": span_id, "chunk_offset": record["offset"],
                              "block_offset": decoded["consumed_bytes"],
                              "file_offset": block_start + decoded["consumed_bytes"],
                              "remaining_command_count": remaining, "raw_hex": raw,
                              "reason": decoded["reason"]})
                for i in range(remaining):
                    append(len(commands) + i, first_opcode if i == 0 else None, None, None,
                           decoded["consumed_bytes"] if i == 0 else None, None, False,
                           "unresolved_boundary", span_id)
    from wgrd_entities import build_reference_catalog, contextual_fallback_rules
    reference_catalog = build_reference_catalog(events, parsed["sha256"], matched)
    production_types = None
    if unit_data is not None:
        from wgrd_production import enrich_production_types
        production_types = enrich_production_types(events, unit_data, str(parsed["header"]["game_version"]))
        from wgrd_unit_data import enrich_references
        enrich_references(reference_catalog, unit_data, str(parsed["header"]["game_version"]))
    from wgrd_entities import attribute_supply_requests
    attribute_supply_requests(events, reference_catalog, matched, unit_data is not None)
    return _json_safe({
        "schema": "wgrd_timeline/1", "sha256": parsed["sha256"], "size": parsed["size"],
        "header": parsed["header"], "metadata": parsed["metadata"],
        "time_basis": {"unit": "replay_frame", "frame_duration_seconds": None,
                       "status": "frame_to_seconds_unresolved"},
        "player_mapping": {"status": "unresolved", "basis": "recorded pact slot; metadata identities not linked"},
        "order_basis": "frame, recorded pact slot order, serialized command order; zero-based",
        "semantic_evidence": {"build": BUILD,
                              "executable_sha256": "1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46",
                              "notes": "research/TIMELINE-SEMANTICS.md"},
        "stats": {"events": len(events), "container": parsed["stats"],
                  "interpretations": dict(Counter(e["interpretation"]["status"] for e in events)),
                  "decode_status": dict(Counter(e["decode_status"] for e in events)),
                  "unresolved_spans": len(spans)},
        "events": events, "unresolved_spans": spans, "unknown_chunks": parsed["unknown_chunks"],
        "entity_references": reference_catalog,
        "production_types": production_types,
        "contextual_order_rules": contextual_fallback_rules(),
    })
