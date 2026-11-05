#!/usr/bin/env python3
"""Build the revision-131544 AAR from an authenticated original-engine trace.

The raw trace is opened read-only, hash-pinned and never rewritten. Every
impact is rebuilt from paired ``enter``/``leave`` reads, joined to a pinned
native unit index and to its nested threshold/destruction calls. Inferred
roles, hypotheses and unknowns stay labelled; wall-clock timestamps are guest
observations, never game time.

Fail-closed policy: a mismatch raises ``AarTraceError`` and the CLI exits 2
without creating output files. Output files are exclusively created.

The legacy profile for the 2026-11-01 sampled trace was retired. To reproduce
its archived outputs byte-for-byte, run this file from commit 71c4f8e
(``git show 71c4f8e:instrumentation/aar_events.py``); see instrumentation/README.md.
"""

import argparse
import bisect
import datetime
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

EXECUTABLE_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
IMAGE_BASE = 0x400000
IMAGE_SIZE = 31883264


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


def _float32_argument(raw_value, where):
    _require(isinstance(raw_value, str) and raw_value.startswith("0x"), "bad argument:%s" % where)
    try:
        bits = int(raw_value, 16)
    except ValueError as error:
        raise AarTraceError("bad argument:%s:%s" % (where, error)) from None
    _require(0 <= bits <= 0xFFFFFFFF, "argument out of range:%s" % where)
    return struct.unpack("<f", struct.pack("<I", bits))[0]


def _address(value, where):
    _require(isinstance(value, str) and value.startswith("0x"), "bad address:%s" % where)
    try:
        address = int(value, 16)
    except ValueError as error:
        raise AarTraceError("bad address:%s:%s" % (where, error)) from None
    _require(0 <= address <= 0xFFFFFFFF, "address out of range:%s" % where)
    return address


def parse_trace(data):
    """Parse strict UTF-8 JSONL into a list of row objects."""
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


def _json_text(value):
    return json.dumps(value, indent=2, allow_nan=False) + "\n"


# ---------------------------------------------------------------------------
# Runtime profiles (build 131544 capture with type and destruction hooks)
#
# Read the runtime trace shape, join captured descriptor GUID/token pairs to a
# hash-pinned native unit index, and export independently witnessed
# damage -> threshold -> destruction call chains.
# ---------------------------------------------------------------------------

RUNTIME_SCHEMA = "wgrd-aar-runtime-events/1"
# Static basis for arg1 (research/current-build/2026-11-02-causal-chain.md).
SOURCE_ROLE = "engine_credited_damage_source"
SOURCE_CONFIDENCE = "static_xp_credit_and_producer_dataflow"
SOURCE_BASIS = ("0xc9f910 credits arg1 with an ExperienceMessage for this damage, with a "
                "lethal-hit bonus (0xc9fa75-0xc9fc08); arg1 is resolved from the queued "
                "entry's copied impact record (0xcf8490 -> 0xcf95e0 -> 0xcf7f40 -> 0xc58a70). "
                "Weapon and projectile identity are not captured")
FRAME_TICK_SECONDS = 0.2
# 0xc95344 stores the threshold check's AL as the Killed token of the per-entry
# composition posted at 0xc954f9; 0xa72ae0 resolves owner+0x24 as a type-2
# owning-object reference whose +0x5c is the team number.
KILLED_TOKEN_BASIS = "check AL stored at 0xc95344 is the Killed token posted at 0xc954f9"
OWNING_REF_BASIS = ("owner+0x24 is the owning-object reference resolved by 0xa72ae0; "
                    "its +0x5c team number is not captured, so no player, faction "
                    "or team is assigned")

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

# ---------------------------------------------------------------------------
# Additive V3 profile: ten hooks, masked descriptor and tagged anchor reads.
#
# The V3 capture keeps every earlier hook and adds a phase candidate plus a
# tagged anchor read (mask 0xfffffffc, +0x30) on the owner lookup (leave) and
# owner destroy (enter) hooks. The runtime profile above is unchanged: this
# profile only widens header validation and adds position
# observations with bounded clock brackets. Nothing here promotes an anchor
# to metres, a visual centre, a movement intent or a game-time source.
# ---------------------------------------------------------------------------

RUNTIME_V3_SCHEMA = "wgrd-aar-runtime-v3/1"
RUNTIME_V3_POSITIONS_SCHEMA = "wgrd-aar-runtime-positions/1"
RUNTIME_V3_TRACE_SHA256 = "d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec"
RUNTIME_V3_INDEX_SHA256 = RUNTIME_INDEX_SHA256
RUNTIME_V3_POSITION_MASK = "fffffffc"
RUNTIME_V3_POSITION_OFFSET = 48

_V3_ANCHOR_MASK = (RUNTIME_V3_POSITION_MASK, RUNTIME_V3_POSITION_OFFSET)
# V3 keeps every runtime hook and read; it widens three hooks and adds two.
RUNTIME_V3_HOOK_SPECS = {name: dict(spec, masks={}) for name, spec in RUNTIME_HOOK_SPECS.items()}
RUNTIME_V3_HOOK_SPECS["owner_destroy_candidate"].update(
    reads=(("ecx", 0, 128, "both", False),
           ("ecx", 40, 128, "enter", True),
           ("ecx", 228, 12, "enter", True)),
    masks={("ecx", 228): _V3_ANCHOR_MASK})
RUNTIME_V3_HOOK_SPECS["reference_lookup"]["reads"] += (("retval", 40, 128, "leave", True),)
RUNTIME_V3_HOOK_SPECS["owner_lookup_candidate"].update(
    reads=RUNTIME_HOOK_SPECS["owner_lookup_candidate"]["reads"]
    + (("retval", 40, 128, "leave", True), ("retval", 228, 12, "leave", True)),
    masks={("retval", 228): _V3_ANCHOR_MASK})
RUNTIME_V3_HOOK_SPECS["frame_apply_candidate"] = {
    "va": "0xb2b310", "args": 2, "sample_every": 1, "reads": (), "masks": {}}
RUNTIME_V3_HOOK_SPECS["phase_change_candidate"] = {
    "va": "0xab4780", "args": 1, "sample_every": 1,
    "reads": (("ecx", 208, 4, "both", False),
              ("ecx", 56, 16, "both", True),
              ("ecx", 32, 4, "both", False)),
    "masks": {}}
RUNTIME_V3_FRAME_HOOK = "frame_apply_candidate"
RUNTIME_V3_PHASE_HOOK = "phase_change_candidate"

# Capture-era source copies retained under <artifact root>/capture-sources.
RUNTIME_V3_CAPTURE_CONFIG = {
    "file": "aar-capture-131544-v3.json",
    "sha256": "e02901924b5465b0ab58a29cce1c537d45139d2054333d950aeed265e3a3eefd",
}
RUNTIME_V3_CAPTURE_SOURCE_PINS = {
    "wgrd_frida.py": "8c32f864bf75f8345077ad44958216362a8429cf6a3d2944745bee806f81e821",
    "hooks.js": "751960dd2ef863b6af50035d5ec51ad73f6c808877c24cb204f51091abdd8d19",
}

RUNTIME_PROFILE_V2 = {
    "name": "runtime",
    "schema": RUNTIME_SCHEMA,
    "capture_config_pin": RUNTIME_CAPTURE_CONFIG,
    "capture_source_pins": RUNTIME_CAPTURE_SOURCE_PINS,
    "hooks": RUNTIME_HOOK_SPECS,
    "position_hooks": {},
    "extra_limitations": (),
}

RUNTIME_PROFILE_V3 = {
    "name": "runtime-v3",
    "schema": RUNTIME_V3_SCHEMA,
    "capture_config_pin": RUNTIME_V3_CAPTURE_CONFIG,
    "capture_source_pins": RUNTIME_V3_CAPTURE_SOURCE_PINS,
    "hooks": RUNTIME_V3_HOOK_SPECS,
    "position_hooks": {
        # (source, offset, size) blocks read in the named phase of that hook.
        "owner_lookup_candidate": {"phase": "leave", "owner_source": "retval",
                                   "header": 0, "anchor": 228,
                                   "descriptor": 40},
        "owner_destroy_candidate": {"phase": "enter", "owner_source": "ecx",
                                    "header": 0, "anchor": 228,
                                    "descriptor": 40},
    },
    "extra_limitations": (
        "Position anchors are raw tagged-pointer reads; coordinates are unmapped "
        "raw float32 triples, not metres, world units or a visual centre.",
        "Position times are only bracketed by adjacent clock-enter samples inside "
        "one clock epoch; no interpolation, wall-clock or game time is derived.",
        "frame_apply_candidate invocations are counted as unmapped calls; the "
        "argument count is not a frame index and no frame is inferred.",
        "phase_change_candidate is recorded as a raw unmapped observation; its "
        "argument does not establish a battle phase or epoch.",
    ),
}

# ---------------------------------------------------------------------------
# Additive V4 profile: V3 plus the tick/frame step hook.
#
# `0xb34060` is the per-tick step: it accumulates seconds, consumes one 0.2 s
# quantum and advances the manager frame index (+0x6c) by exactly one. Hooking
# its entry/leave with the entry-time manager pointer gives, for any later
# callback, the frame interval it fell inside and the wall-time distance to the
# bracketing calls. It does not give an exact interleaving guarantee, so every
# join carries its bracket and a status; a wide bracket stays unresolved.
# ---------------------------------------------------------------------------

RUNTIME_V4_SCHEMA = "wgrd-aar-runtime-v4/1"
RUNTIME_V4_HOOK = "tick_step"
RUNTIME_V4_BRACKET_TOLERANCE_SECONDS = 1.0
RUNTIME_V4_HOOK_SPECS = {name: dict(spec) for name, spec in RUNTIME_V3_HOOK_SPECS.items()}
RUNTIME_V4_HOOK_SPECS[RUNTIME_V4_HOOK] = {
    "va": "0xb34060", "args": 1, "sample_every": 1,
    "reads": (("ecx", 104, 4, "both", False),   # +0x68 accumulator seconds
              ("ecx", 108, 4, "both", False),   # +0x6c frame index
              ("ecx", 160, 1, "both", False),   # +0xa0
              ("ecx", 164, 1, "both", False),   # +0xa4
              ("ecx", 165, 1, "both", False)),  # +0xa5 replay byte
    "masks": {},
}
RUNTIME_V4_CAPTURE_CONFIG = {
    "file": "aar-capture-131544-v4.json",
    "sha256": "ab7810a27470d37b9571241ed60f507d4deeaaef87101fc8f3d2b8c0a5752de1",
}
# The run reuses the retained capture-era controller pair unchanged.
RUNTIME_V4_CAPTURE_SOURCE_PINS = RUNTIME_CAPTURE_SOURCE_PINS

RUNTIME_PROFILE_V4 = {
    "name": "runtime-v4",
    "schema": RUNTIME_V4_SCHEMA,
    "capture_config_pin": RUNTIME_V4_CAPTURE_CONFIG,
    "capture_source_pins": RUNTIME_V4_CAPTURE_SOURCE_PINS,
    "hooks": RUNTIME_V4_HOOK_SPECS,
    "position_hooks": RUNTIME_PROFILE_V3["position_hooks"],
    "extra_limitations": RUNTIME_PROFILE_V3["extra_limitations"] + (
        "Frame joins come from one tick hook's entry/leave reads; an event is "
        "assigned an exact frame only when it lies inside a tick call or between "
        "two calls closer than the tolerance, otherwise its frame stays a bracket.",
        "The frame/tick difference is carried as observed integers (10 or 11); no "
        "midpoint is applied and no battle start is derived.",
    ),
}


def _norm_mask(value):
    return value.lower().replace("0x", "")


def _rt_profile(name):
    profiles = {profile["name"]: profile for profile in
                (RUNTIME_PROFILE_V2, RUNTIME_PROFILE_V3, RUNTIME_PROFILE_V4)}
    _require(name in profiles, "unknown profile %r" % name)
    return profiles[name]


def _rt_detect_profile(rows):
    """Select a profile only from the exact, known hook-name sets."""
    starts = [row for row in rows if row.get("event") == "start"]
    _require(len(starts) == 1, "expected exactly one start record, found %d" % len(starts))
    hooks = starts[0].get("hooks")
    _require(isinstance(hooks, list), "start record has no hooks")
    names = {hook.get("name") for hook in hooks}
    for profile in (RUNTIME_PROFILE_V4, RUNTIME_PROFILE_V3, RUNTIME_PROFILE_V2):
        if names == set(profile["hooks"]):
            return profile
    raise AarTraceError("unknown hook profile: %s"
                        % ", ".join(sorted(str(name) for name in names)))


def _rt_require_complete(rows):
    """A completed capture is required before any export can be written."""
    names = [row.get("event") for row in rows]
    required = ("start", "identity_verified", "hooks_installed", "summary",
                "detached", "end")
    missing = [name for name in required if name not in names]
    _require(not missing,
             "incomplete capture: missing %s; a completed capture (summary, "
             "detached and end records) is required before export"
             % ", ".join(missing))


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


def _rt_records(rows, profile):
    grouped = {name: {"enter": [], "leave": []} for name in profile["hooks"]}
    for line_number, row in enumerate(rows, 1):
        hook = row.get("hook")
        event = row.get("event")
        if hook in grouped and event in ("enter", "leave"):
            grouped[hook][event].append((line_number, row))
    return grouped


def _rt_pairs(grouped, name, profile):
    spec = profile["hooks"][name]
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
    if profile["name"] == "runtime-v4" and name == RUNTIME_V4_HOOK:
        # The high-frequency tick hook can still be inside a call at detach.
        # Only this hook may drop its last enter, and only one; the frame join
        # then works from the completed intervals and reports the gap.
        without_leave = set(enters) - set(leaves)
        _require(not (set(leaves) - set(enters)), "%s leave without enter" % name)
        _require(len(without_leave) <= 1, "%s has %d unpaired enters"
                 % (name, len(without_leave)))
        for key in without_leave:
            enters.pop(key)
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


def _rt_validate_header(rows, profile):
    hook_specs = profile["hooks"]
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
        _require(name in hook_specs, "unexpected hook %r" % name)
        _require(name not in seen, "duplicate hook %r" % name)
        spec = hook_specs[name]
        _require(hook.get("va") == spec["va"], "%s hook address mismatch" % name)
        _require(hook.get("args") == spec["args"], "%s argument count mismatch" % name)
        _require(hook.get("sample_every") == spec["sample_every"],
                 "%s sampling mismatch" % name)
        shape = {(read.get("source"), read.get("offset"), read.get("size"),
                  read.get("phase"), bool(read.get("indirect", False)))
                 for read in hook.get("reads") or []}
        _require(shape == set(spec["reads"]), "%s read shape mismatch" % name)
        masks = spec.get("masks") or {}
        for read in hook.get("reads") or []:
            key = (read.get("source"), read.get("offset"))
            expected = masks.get(key)
            actual = read.get("indirect_mask")
            actual_offset = read.get("indirect_offset")
            if expected is None:
                _require(actual is None and actual_offset is None,
                         "%s unexpected indirect mask at %r" % (name, key))
            else:
                _require(isinstance(actual, str) and _norm_mask(actual) == expected[0],
                         "%s indirect mask mismatch at %r" % (name, key))
                _require(actual_offset == expected[1],
                         "%s indirect offset mismatch at %r" % (name, key))
        seen[name] = hook
    _require(set(seen) == set(hook_specs), "runtime hook set mismatch")

    module = identity.get("module") or {}
    _require(module.get("name", "").lower() == "wargame3.exe", "identity module name mismatch")
    _require(module.get("arch") == "ia32" and module.get("pointer_size") == 4,
             "identity is not ia32")
    _require(module.get("base") == "0x400000", "image base mismatch")
    _require(module.get("size") == IMAGE_SIZE, "image size mismatch")
    entries = {}
    for entry in module.get("entries") or []:
        entries[entry.get("name")] = entry
    _require(set(entries) == set(hook_specs), "identity hook set mismatch")
    for name, spec in hook_specs.items():
        _require(entries[name].get("address") == spec["va"],
                 "identity address mismatch for %s" % name)
        _require(entries[name].get("executable") is True,
                 "identity address not executable for %s" % name)

    for key in ("suppressed", "callback_errors", "stale_frames", "stack_mismatches"):
        _require(summary.get(key) == 0, "summary failure:%s=%r" % (key, summary.get(key)))
    # V4 adds a high-frequency tick hook. One thread can still be inside it at
    # detach; every event hook must stay fully paired, which is checked against
    # the rows in _rt_attach_frame_correlation before any join is emitted.
    outstanding = summary.get("outstanding_threads")
    if profile["name"] == "runtime-v4":
        _require(outstanding in (0, 1), "summary failure:outstanding_threads=%r" % (outstanding,))
    else:
        _require(outstanding == 0, "summary failure:outstanding_threads=%r" % (outstanding,))
    for key in ("gate_read_failures", "gate_ambiguities", "gate_suspended_threads"):
        # The V3 capture summary omits the gate counters; when present they
        # must be zero, and the V2 profile continues to require them.
        if key in summary or profile["name"] == "runtime":
            _require(summary.get(key) == 0, "summary failure:%s=%r" % (key, summary.get(key)))
    counts = summary.get("counts")
    _require(isinstance(counts, dict) and set(counts) == set(hook_specs),
             "summary hook counts mismatch")
    _require(detached.get("reason") == "application-requested",
             "unexpected detach reason:%r" % detached.get("reason"))
    _require(end.get("cleanup_errors") == 0, "cleanup error")
    if _parse_timestamp(start.get("timestamp_utc"), "start") > \
            _parse_timestamp(end.get("timestamp_utc"), "end"):
        raise AarTraceError("start is after end")
    return start, summary


def _rt_check_counts(summary, pairs_by_hook, profile):
    counts = summary["counts"]
    total_enters = 0
    for name, pairs in pairs_by_hook.items():
        total_enters += len(pairs)
        stride = profile["hooks"][name]["sample_every"]
        total = counts[name]
        if stride == 1:
            # V4's tick hook may report one enter whose leave never arrived at
            # detach; that single tail is already excluded from the pairs.
            allowance = 1 if (profile["name"] == "runtime-v4"
                              and name == RUNTIME_V4_HOOK) else 0
            _require(total == len(pairs) + allowance, "%s count %d != paired %d"
                     % (name, total, len(pairs)))
        else:
            expected = (total - 1) // stride + 1 if total else 0
            _require(expected == len(pairs),
                     "%s emitted count %d != stride arithmetic %d"
                     % (name, len(pairs), expected))
            _require(pairs[-1][0] == (len(pairs) - 1) * stride + 1,
                     "%s last sampled ordinal mismatch" % name)
            _require(pairs[-1][0] <= total, "%s sampled ordinal exceeds count" % name)
    # A lone tick-hook enter without a leave explains exactly one missing record.
    tail = 1 if (profile["name"] == "runtime-v4"
                 and summary.get("outstanding_threads") == 1) else 0
    _require(summary.get("emitted") == 2 * total_enters + tail,
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


def _rt_chain(read, where):
    chain = read.get("chain")
    _require(isinstance(chain, list), "missing indirect chain at %s" % where)
    values = []
    for value in chain:
        try:
            values.append(int(value, 16))
        except (TypeError, ValueError):
            raise AarTraceError("bad indirect chain at %s" % where) from None
    return values


def _rt_anchor_read(record, source, offset, size, phase, where, mask, mask_offset):
    """Read one tagged anchor block; a failed read is reported, never invented."""
    read = _rt_read_record(record, source, offset, size, phase, where)
    result = read.get("result") or {}
    if result.get("ok") is not True:
        return {"status": "position_read_failed", "reason": result.get("reason"),
                "raw_hex": None, "sha256": None, "xyz": None,
                "raw_pointer": None, "target": None, "size": size}
    _require(read.get("indirect") is True, "anchor read is not indirect at %s" % where)
    data = _rt_bytes(read, where, False)
    _require(len(data) == 12, "anchor read is not 12 bytes at %s" % where)
    raw_pointer = read.get("raw_pointer")
    if not isinstance(raw_pointer, str):
        # A successful read without a retained pointer cannot be turned into an
        # observation; record the missing evidence instead of inventing a chain.
        return {"status": "position_read_failed", "reason": "no_raw_pointer",
                "raw_hex": None, "sha256": None, "xyz": None,
                "raw_pointer": None, "target": None, "size": size}
    pointer = _address(raw_pointer, where + ":raw_pointer")
    applied = read.get("applied_mask")
    _require(isinstance(applied, str) and _norm_mask(applied) == mask,
             "anchor mask mismatch at %s" % where)
    _require(read.get("target_offset") == mask_offset,
             "anchor target offset mismatch at %s" % where)
    _require(_rt_chain(read, where) == [pointer], "anchor chain mismatch at %s" % where)
    target = (pointer & int(mask, 16)) + mask_offset
    _require(read.get("final_target") == "0x%08x" % target,
             "anchor final target mismatch at %s" % where)
    _require(read.get("target") == "0x%08x" % target,
             "anchor target mismatch at %s" % where)
    xyz = list(struct.unpack_from("<3f", data, 0))
    _require(all(math.isfinite(value) for value in xyz),
             "non-finite position at %s" % where)
    return {"status": "read_ok", "raw_hex": data.hex(),
            "sha256": hashlib.sha256(data).hexdigest(), "xyz": xyz,
            "raw_pointer": "0x%08x" % pointer, "target": "0x%08x" % target,
            "size": size}


def _rt_configured_descriptor(index, guid_hex, token_hex):
    """Annotate a native descriptor, never a member-unit or ownership join."""
    result = {"status": "not_checked", "source_node": None, "ndf_class": None,
              "debug_name": None, "token_unique": None, "confidence": "none"}
    if index is None:
        return result
    if guid_hex is None or token_hex is None:
        result["status"] = "descriptor_bytes_unreadable"
        return result
    units = index["unit_types"]
    hits = [(node, unit) for node, unit in units.items()
            if unit.get("descriptor_guid_hex") == guid_hex]
    result["token_unique"] = sum(unit.get("name_token") == token_hex
                                 for unit in units.values()) == 1
    if len(hits) != 1:
        result["status"] = "guid_not_unique" if hits else "guid_not_in_index"
        return result
    node, unit = hits[0]
    if unit.get("name_token") != token_hex:
        result["status"] = "token_mismatch"
        return result
    entry = index["descriptors"].get(guid_hex, {})
    if entry.get("source_nodes") != [node]:
        result["status"] = "descriptor_source_disagreement"
        return result
    result.update({"status": "unique_guid_compatible_token", "source_node": node,
                   "ndf_class": unit.get("ndf_class"), "debug_name": unit.get("debug_name"),
                   "confidence": "static_descriptor_identity_only"})
    return result


def _rt_position_observations(rows, profile, index):
    """Descriptor-resolved position anchors, one per successful anchor read."""
    observations = []
    read_failures = 0
    for line, row in enumerate(rows, 1):
        hook = row.get("hook")
        spec = profile["position_hooks"].get(hook)
        if spec is None or row.get("event") != spec["phase"]:
            continue
        phase = spec["phase"]
        source = spec["owner_source"]
        where = "position:%s:%d" % (hook, line)
        header = _rt_bytes(_rt_read_record(row, source, spec["header"], 128, phase, where),
                           where, False)
        handle = _rt_u32(header, 0x20, where)
        descriptor_pointer = _rt_u32(header, 0x28, where)
        _require(descriptor_pointer != 0, "null descriptor pointer at %s" % where)
        owner = _address(row.get(source), where + ":owner")

        descriptor_read = _rt_read_record(row, source, spec["descriptor"], 128, phase, where)
        _require(descriptor_read.get("indirect") is True,
                 "descriptor read is not indirect at %s" % where)
        _require(_rt_chain(descriptor_read, where) == [descriptor_pointer],
                 "descriptor chain does not resolve +0x28 at %s" % where)
        descriptor = _rt_bytes(descriptor_read, where, allow_failure=True)
        if descriptor is None:
            guid_hex = token_hex = None
            join = {"guid_hex": None, "name_token_hex": None, "unit_type_id": None,
                    "debug_name": None, "ndf_class": None, "candidate_path": None,
                    "status": "descriptor_bytes_unreadable", "confidence": "none"}
        else:
            guid_hex = descriptor[0x0c:0x1c].hex()
            token_hex = descriptor[0x60:0x68].hex()
            join = (_rt_descriptor_join(index, guid_hex, token_hex)
                    if index is not None else
                    {"guid_hex": guid_hex, "name_token_hex": token_hex,
                     "unit_type_id": None, "debug_name": None, "ndf_class": None,
                     "candidate_path": None, "status": "index_not_loaded",
                     "confidence": "none"})

        mask, mask_offset = profile["hooks"][hook]["masks"][(source, spec["anchor"])]
        anchor = _rt_anchor_read(row, source, spec["anchor"], 12, phase, where,
                                 mask, mask_offset)
        if anchor["status"] != "read_ok":
            read_failures += 1
        owner_hex = "0x%08x" % owner
        descriptor_hex = "0x%08x" % descriptor_pointer
        observations.append({
            "index": len(observations) + 1,
            "hook": hook,
            "phase": phase,
            "line": line,
            "identity": {
                "key": "h%d|%s|%s" % (handle, owner_hex, descriptor_hex),
                "handle_u32": handle,
                "owner_object": owner_hex,
                "descriptor_pointer": descriptor_hex,
                "descriptor_guid_hex": guid_hex,
                "descriptor_name_token_hex": token_hex,
                "descriptor_join": join,
                "configured_descriptor": _rt_configured_descriptor(index, guid_hex, token_hex),
                "basis": ("same-capture handle string plus owner object plus "
                          "descriptor pointer; never merged across mismatches"),
            },
            "anchor": anchor,
            "time": None,
        })
    return observations, read_failures


def _rt_clock_epochs(clock_samples):
    """Maximal runs of one receiver with a non-decreasing counter."""
    epochs = []
    for sample in clock_samples:
        if (epochs and sample["container"] == epochs[-1]["receiver"]
                and sample["counter"] >= epochs[-1]["last_counter"]):
            epochs[-1]["samples"].append(sample)
            epochs[-1]["last_counter"] = sample["counter"]
            epochs[-1]["last_line"] = sample["enter_line"]
        else:
            epochs.append({"index": len(epochs), "receiver": sample["container"],
                           "first_counter": sample["counter"],
                           "last_counter": sample["counter"],
                           "first_line": sample["enter_line"],
                           "last_line": sample["enter_line"],
                           "samples": [sample]})
    return epochs


def _rt_apply_clock_brackets(observations, clock_samples):
    """Bracket each position by adjacent same-epoch clock enter samples."""
    epochs = _rt_clock_epochs(clock_samples)
    ordered = []
    for epoch in epochs:
        for sample in epoch["samples"]:
            ordered.append((sample["enter_line"], epoch["index"], sample))
    ordered.sort(key=lambda item: item[0])
    lines = [item[0] for item in ordered]
    for observation in observations:
        position = bisect.bisect_left(lines, observation["line"])
        lower = ordered[position - 1] if position > 0 else None
        upper = ordered[position] if position < len(ordered) else None
        bracket = {
            "bracketed": False, "epoch": None, "lower": None, "upper": None,
            "counter_span": None,
            "basis": "adjacent clock_sample_candidate enter records",
            "note": ("Bounded only by the two adjacent clock samples that share one "
                     "clock epoch; no interpolation, wall-clock or game-time "
                     "conversion is performed."),
        }
        if lower is not None and upper is not None and lower[1] == upper[1]:
            bracket.update({
                "bracketed": True,
                "epoch": lower[1],
                "lower": {"line": lower[0], "counter": lower[2]["counter"],
                          "receiver": lower[2]["container"]},
                "upper": {"line": upper[0], "counter": upper[2]["counter"],
                          "receiver": upper[2]["container"]},
                "counter_span": upper[2]["counter"] - lower[2]["counter"],
            })
        elif lower is not None and upper is not None:
            bracket["reason"] = "adjacent_clock_samples_span_an_epoch_change"
        else:
            bracket["reason"] = "no_clock_sample_on_one_side"
        observation["time"] = {
            "clock_epoch": bracket["epoch"],
            "bracket": bracket,
            "counter_ticks": None,
            "frame": None,
            "simulation_time": None,
            "game_time": None,
            "battle_time": None,
            "basis": ("clock counters only; the anchor value has no captured time "
                      "base of its own"),
        }
    return epochs


def _rt_position_tracks(observations):
    tracks = {}
    for observation in observations:
        tracks.setdefault(observation["identity"]["key"], []).append(observation)
    return tracks


def _rt_position_changes(observations):
    """Explicit anchor-value transitions per exact identity track."""
    changes = []
    tracks = _rt_position_tracks(observations)
    for key in sorted(tracks):
        track = sorted(tracks[key], key=lambda item: item["line"])
        for previous, current in zip(track, track[1:]):
            before, after = previous["anchor"], current["anchor"]
            if before["status"] != "read_ok" or after["status"] != "read_ok":
                continue
            from_ref = {"line": previous["line"], "index": previous["index"],
                        "hook": previous["hook"], "phase": previous["phase"]}
            to_ref = {"line": current["line"], "index": current["index"],
                      "hook": current["hook"], "phase": current["phase"]}
            if before["target"] != after["target"]:
                changes.append({
                    "kind": "position_anchor_rebound",
                    "identity_key": key,
                    "from": from_ref,
                    "to": to_ref,
                    "anchor_before": before["target"],
                    "anchor_after": after["target"],
                    "comparable": False,
                    "reason": ("the tagged anchor target changed for one identity; "
                               "the two reads are not compared as one position"),
                })
                continue
            if before["raw_hex"] == after["raw_hex"]:
                continue
            delta = [after_value - before_value
                     for before_value, after_value in zip(before["xyz"], after["xyz"])]
            earlier = previous["time"]["bracket"]
            later = current["time"]["bracket"]
            interval = {
                "bracketed": False, "epoch": None, "lower": None, "upper": None,
                "counter_span": None,
                "basis": "outer clock bounds of both position observations",
                "note": "The value changed between two samples, not necessarily near the later sample.",
            }
            if (earlier["bracketed"] and later["bracketed"]
                    and earlier["epoch"] == later["epoch"]):
                interval.update({
                    "bracketed": True, "epoch": earlier["epoch"],
                    "lower": dict(earlier["lower"]), "upper": dict(later["upper"]),
                    "counter_span": later["upper"]["counter"] - earlier["lower"]["counter"],
                })
            else:
                interval["reason"] = "missing_endpoint_bound_or_clock_epoch_change"
            changes.append({
                "kind": "position_anchor_changed",
                "identity_key": key,
                "from": from_ref,
                "to": to_ref,
                "raw_before_hex": before["raw_hex"],
                "raw_after_hex": after["raw_hex"],
                "raw_before_sha256": before["sha256"],
                "raw_after_sha256": after["sha256"],
                "xyz_before": before["xyz"],
                "xyz_after": after["xyz"],
                "delta_raw_f32": delta,
                "displacement_raw_f32": math.sqrt(sum(value * value for value in delta)),
                "units": "unknown_unmapped_raw_f32",
                "comparable": True,
                "time": {"bracket": interval},
                "not_derived": ["metres", "speed", "heading", "movement intent",
                                "arrival", "replay frame", "game time"],
            })
    return changes


def _rt_position_identity(observations):
    """Report identity reuse instead of merging it away."""
    tracks = _rt_position_tracks(observations)
    fields = {"handle": {}, "owner_object": {}, "descriptor_pointer": {},
              "anchor_pointer": {}}
    for observation in observations:
        identity = observation["identity"]
        fields["handle"].setdefault(identity["handle_u32"], set()).add(identity["key"])
        fields["owner_object"].setdefault(identity["owner_object"], set()).add(identity["key"])
        fields["descriptor_pointer"].setdefault(
            identity["descriptor_pointer"], set()).add(identity["key"])
        anchor = observation["anchor"]
        if anchor["status"] == "read_ok":
            fields["anchor_pointer"].setdefault(
                anchor["raw_pointer"], set()).add(identity["key"])
    conflicts = []
    # A descriptor describes a unit type, so several units legitimately share
    # one descriptor pointer; only an identity field that must be unique is a
    # conflict. Descriptor sharing is reported separately below.
    for field in ("handle", "owner_object", "anchor_pointer"):
        for value, keys in sorted(fields[field].items(), key=lambda item: str(item[0])):
            if len(keys) > 1:
                conflicts.append({"field": field, "value": str(value),
                                  "identity_keys": sorted(keys),
                                  "status": "kept_separate_not_merged"})
    shared_descriptors = sorted(
        (value, sorted(keys)) for value, keys in fields["descriptor_pointer"].items()
        if len(keys) > 1)
    joined = {}
    for observation in observations:
        status = observation["identity"]["descriptor_join"].get("status")
        joined[status] = joined.get(status, 0) + 1
    changed_tracks = 0
    for track in tracks.values():
        values = [item["anchor"]["raw_hex"] for item in track
                  if item["anchor"]["status"] == "read_ok"]
        if len(set(values)) > 1:
            changed_tracks += 1
    bounded = sum(1 for observation in observations
                  if observation["time"]["bracket"]["bracketed"])
    return {
        "key": "handle_u32 + owner_object + descriptor_pointer",
        "observations": len(observations),
        "tracks": len(tracks),
        "tracks_with_single_observation": sum(1 for track in tracks.values()
                                              if len(track) == 1),
        "tracks_with_changed_bytes": changed_tracks,
        "bracketed_observations": bounded,
        "unbracketed_observations": len(observations) - bounded,
        "descriptor_join_status": joined,
        "shared_descriptor_pointers": len(shared_descriptors),
        "conflicts": conflicts,
        "note": ("Records that share one field but not the whole identity key stay "
                 "in separate tracks; shared anchor pointers are reported as reuse, "
                 "never merged. Descriptor pointers are shared by design between "
                 "units of one type and are not treated as an identity conflict."),
    }


def _rt_extract(rows, source_name, source_sha256, line_count, index, index_name,
                index_sha256, profile=None):
    _rt_require_complete(rows)
    profile = profile or _rt_detect_profile(rows)
    start, summary = _rt_validate_header(rows, profile)
    grouped = _rt_records(rows, profile)
    pairs_by_hook = {name: _rt_pairs(grouped, name, profile) for name in profile["hooks"]}
    emitted = _rt_check_counts(summary, pairs_by_hook, profile)

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
    # V4's tick hook sits between event callbacks on the stack, so a destroy's
    # nearest recorded parent can be the tick call rather than the destruction
    # check. That is recorded as an interrupted link, never guessed.
    tick_call_ids = {item[2].get("call_id")
                     for item in pairs_by_hook.get(RUNTIME_V4_HOOK, ())}
    destroys_by_parent = {}
    lifecycle_destroys = []
    cleanup_destroys = []
    for ordinal, enter_line, enter, leave_line, leave in destroys:
        parent = enter.get("parent_call_id")
        parent_link = "recorded"
        if parent in tick_call_ids:
            parent = None
            parent_link = "interrupted_by_tick_hook"
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
            "parent_link": parent_link,
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
            if parent_link == "interrupted_by_tick_hook":
                record["lifecycle_parent"] = "unresolved_tick_hook_interposed"
            else:
                _require(record["parent_recorded"], "lifecycle destroy has no recorded parent")
                _require(parent in check_by_call_id,
                         "lifecycle destroy parent is not a destruction check")
            _require(record["argument_raw"] == "0x1",
                     "unexpected lifecycle destroy argument %r" % record["argument_raw"])
            lifecycle_destroys.append(record)
            if parent is not None:
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

        # arg2's descriptor bytes were recorded once per impact above.
        arg2_address = int(arguments[2], 16)

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
            "fields": fields,
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
                "role": (SOURCE_ROLE if source_handle is not None
                         else "unresolved_owner"),
                "confidence": (SOURCE_CONFIDENCE if source_handle is not None
                               else "not_applicable"),
                "basis": (SOURCE_BASIS if source_handle is not None else
                          "arg1 is null: the entry carries no engine-credited source; "
                          "the producing impact record was not captured"),
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
                "replay_frame_hypothesis": ({
                    "value": round(time_value / FRAME_TICK_SECONDS),
                    "status": "hypothesis_0p2s_per_replay_frame",
                } if time_value is not None and time_value >= 0 else None),
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
                "source_role": (SOURCE_CONFIDENCE if source_handle is not None
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
            "killed_token": {
                "value": event["check"]["al_u8"] == 1,
                "level": "static_mapping_of_observed_check_al",
                "combat_message_captured": False,
                "scored_kill_confirmed": False,
                "basis": KILLED_TOKEN_BASIS,
            },
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
            "not_claimed": ["weapon", "scored kill", "replay frame", "battle time"],
            "confidence": {
                "damage_destruction_control_flow": "observed_same_trace_nesting",
                "victim_identity": "observed_handle_plus_static_type_join",
                "source_attribution": SOURCE_CONFIDENCE,
                "kill_outcome": "unknown",
            },
        })

    position_observations = []
    position_read_failures = 0
    position_epochs = []
    position_changes = []
    position_identity = None
    if profile["position_hooks"]:
        position_observations, position_read_failures = _rt_position_observations(
            rows, profile, index)
        position_epochs = _rt_apply_clock_brackets(position_observations, clock_samples)
        position_changes = _rt_position_changes(position_observations)
        position_identity = _rt_position_identity(position_observations)

    clock_first = clock_samples[0] if clock_samples else None
    clock_last = clock_samples[-1] if clock_samples else None
    manifest = {
        "schema": profile["schema"],
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
            "capture_config_pin": profile["capture_config_pin"],
            "capture_source_pins": profile["capture_source_pins"],
            "capture_source_status": "not checked by in-memory extraction",
            "trace_embedded_hooks": (
                "start/identity records were matched to the expected eight hook shapes and executable addresses"
                if profile["name"] == "runtime" else
                "start/identity records were matched to the expected %d hook shapes and executable addresses"
                % len(profile["hooks"])),
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
            } for name, spec in profile["hooks"].items()},
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
    if profile["position_hooks"]:
        manifest["profile"] = {
            "name": profile["name"],
            "hooks": len(profile["hooks"]),
            "position_hooks": sorted(profile["position_hooks"]),
            "position_mask": "0x" + RUNTIME_V3_POSITION_MASK,
            "position_indirect_offset": RUNTIME_V3_POSITION_OFFSET,
            "selection": ("explicit runtime-v3 profile or an exact known ten-hook "
                          "start-record set; arbitrary hook sets are rejected"),
        }
        manifest["integrity"].update({
            "position_observations": len(position_observations),
            "position_read_failures": position_read_failures,
            "position_descriptor_read_failures": sum(
                item["identity"]["descriptor_join"].get("status") == "descriptor_bytes_unreadable"
                for item in position_observations),
            "gate_counter_status": (
                "reported_counters_validated_zero" if any(
                    key in summary for key in ("gate_read_failures", "gate_ambiguities",
                                                "gate_suspended_threads")) else
                "not_reported_by_pinned_v3_source; no_gate_zero_claim"),
            "position_identity_tracks": len(_rt_position_tracks(position_observations)),
            "position_anchor_changes": len(position_changes),
            "clock_epochs": len(position_epochs),
            "position_identity_conflicts": len(position_identity["conflicts"]),
        })
        manifest["position_observations"] = position_observations
        manifest["position_identity"] = position_identity
        manifest["position_anchor_changes"] = position_changes
        manifest["clock_epochs"] = [{
            "index": epoch["index"],
            "receiver": epoch["receiver"],
            "first_counter": epoch["first_counter"],
            "last_counter": epoch["last_counter"],
            "first_line": epoch["first_line"],
            "last_line": epoch["last_line"],
            "samples": len(epoch["samples"]),
            "basis": ("one receiver with a non-decreasing observed counter; a "
                      "receiver change or counter decrease starts a new run and is "
                      "not interpreted as a game epoch"),
        } for epoch in position_epochs]
        unmapped = {"note": ("Captured hooks that are counted and exported raw but "
                             "not assigned semantics.")}
        if RUNTIME_V3_FRAME_HOOK in pairs_by_hook:
            frames = pairs_by_hook[RUNTIME_V3_FRAME_HOOK]
            unmapped["frame_apply"] = {
                "hook": RUNTIME_V3_FRAME_HOOK,
                "pairs": len(frames),
                "invocations": summary["counts"].get(RUNTIME_V3_FRAME_HOOK),
                "first_arguments": [enter.get("args") for _, _, enter, _, _ in frames[:3]],
                "frame_index": None,
                "basis": ("the invocation count and arguments are captured raw; the "
                          "count is not a frame index and no replay frame is inferred"),
            }
        if RUNTIME_V3_PHASE_HOOK in pairs_by_hook:
            phases = []
            for ordinal, enter_line, enter, leave_line, leave in pairs_by_hook[RUNTIME_V3_PHASE_HOOK]:
                reads = {}
                for read in enter.get("reads") or []:
                    reads[str(read.get("offset"))] = {
                        "enter_hex": (read.get("result") or {}).get("hex"),
                        "leave_hex": next(
                            ((other.get("result") or {}).get("hex")
                             for other in leave.get("reads") or []
                             if other.get("offset") == read.get("offset")), None),
                    }
                phases.append({
                    "ordinal": ordinal,
                    "enter_line": enter_line,
                    "leave_line": leave_line,
                    "argument_raw": (enter.get("args") or [None])[0],
                    "reads": reads,
                    "semantics": None,
                })
            unmapped["phase_change"] = {
                "hook": RUNTIME_V3_PHASE_HOOK,
                "pairs": len(phases),
                "records": phases,
                "basis": ("the argument and reads are captured raw; no battle phase, "
                          "epoch or transition semantics are asserted"),
            }
        manifest["unmapped_observations"] = unmapped
        manifest["limitations"] = list(manifest["limitations"]) + list(
            profile["extra_limitations"])
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
            "owning_object_ref": {"raw": "0x%08x" % info["owner_field_0x24_raw"],
                                  "basis": OWNING_REF_BASIS},
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


def _rt_utc_seconds(value):
    """Parse the trace's ISO-8601 UTC timestamp into epoch seconds."""
    text = str(value).replace("Z", "+00:00")
    return datetime.datetime.fromisoformat(text).timestamp()


def _rt_read_bytes(row, offset, phase=None):
    for read in row.get("reads") or ():
        if read.get("offset") != offset:
            continue
        if phase is not None and read.get("phase") != phase:
            continue
        result = read.get("result") or {}
        if result.get("ok") is True and result.get("hex"):
            return bytes.fromhex(result["hex"])
    return None


def _rt_raw_u32(raw):
    return struct.unpack("<I", raw)[0] if raw else None


def _rt_tick_intervals(rows, hook=RUNTIME_V4_HOOK):
    """Pair the tick hook's enter/leave reads into frame intervals.

    Each interval carries the frame index read at entry and at leave plus the
    UTC seconds of both edges. Frames only change inside such an interval, so an
    event outside every interval has a constant frame between the neighbouring
    calls; the distance to those calls is the join's real uncertainty.
    """
    enters = {}
    leaves = {}
    for row in rows:
        if row.get("hook") != hook:
            continue
        if row.get("event") == "enter":
            enters[row.get("call_id")] = row
        elif row.get("event") == "leave":
            leaves[row.get("call_id")] = row
    intervals = []
    for call_id, enter in enters.items():
        leave = leaves.get(call_id)
        if leave is None:
            continue
        frame_enter = _rt_raw_u32(_rt_read_bytes(enter, 108))
        frame_leave = _rt_raw_u32(_rt_read_bytes(leave, 108))
        if frame_enter is None or frame_leave is None:
            continue
        intervals.append({
            "call_id": call_id,
            "enter_seconds": _rt_utc_seconds(enter["timestamp_utc"]),
            "leave_seconds": _rt_utc_seconds(leave["timestamp_utc"]),
            "frame_enter": frame_enter,
            "frame_leave": frame_leave,
            "replay_byte": (_rt_read_bytes(enter, 165) or b"\x00")[0],
        })
    intervals.sort(key=lambda item: item["enter_seconds"])
    return intervals


def correlate_tick_frames(rows, events, tolerance_s=RUNTIME_V4_BRACKET_TOLERANCE_SECONDS):
    """Join each event line to the tick intervals that bracket it.

    Returns ``(joins, summary)``. A join is exact only when the event line lies
    inside a tick call or strictly between two calls no farther apart than the
    tolerance; otherwise ``frame_low``/``frame_high`` stay a bracket and the
    status says why. No nearest-timestamp substitution is used.
    """
    intervals = _rt_tick_intervals(rows)
    starts = [item["enter_seconds"] for item in intervals]
    joins = {}
    counts = {}
    for event in events:
        refs = event.get("refs") or {}
        line_ref = refs.get("enter_line") or refs.get("destroy_enter_line") or ""
        digits = "".join(ch for ch in str(line_ref) if ch.isdigit())
        if not digits:
            joins[event.get("ordinal")] = {"status": "no_line_reference"}
            counts["no_line_reference"] = counts.get("no_line_reference", 0) + 1
            continue
        index = int(digits) - 1
        if not 0 <= index < len(rows):
            joins[event.get("ordinal")] = {"status": "line_out_of_range"}
            counts["line_out_of_range"] = counts.get("line_out_of_range", 0) + 1
            continue
        when = _rt_utc_seconds(rows[index]["timestamp_utc"])
        position = bisect.bisect_right(starts, when)
        previous = intervals[position - 1] if position else None
        following = intervals[position] if position < len(intervals) else None
        if previous is not None and previous["enter_seconds"] <= when <= previous["leave_seconds"]:
            join = {
                "status": "inside_tick_call",
                "frame_low": previous["frame_enter"],
                "frame_high": previous["frame_leave"],
                "bracket_before_seconds": 0.0,
                "bracket_after_seconds": 0.0,
                "tick_call_id": previous["call_id"],
                "replay_byte": previous["replay_byte"],
            }
        elif previous is None or following is None:
            join = {
                "status": "unbracketed",
                "frame_low": None,
                "frame_high": None,
                "bracket_before_seconds": (round(when - previous["leave_seconds"], 6)
                                           if previous else None),
                "bracket_after_seconds": (round(following["enter_seconds"] - when, 6)
                                          if following else None),
            }
        else:
            before = when - previous["leave_seconds"]
            after = following["enter_seconds"] - when
            join = {
                "status": ("bracketed" if before <= tolerance_s and after <= tolerance_s
                           else "wide_bracket"),
                "frame_low": previous["frame_leave"],
                "frame_high": previous["frame_leave"],
                "bracket_before_seconds": round(before, 6),
                "bracket_after_seconds": round(after, 6),
                "tick_call_id": previous["call_id"],
                "next_tick_call_id": following["call_id"],
                "replay_byte": previous["replay_byte"],
            }
        if join["frame_low"] is not None:
            join["estimated_deterministic_seconds_bounds"] = [
                round((join["frame_low"] - 11) * 0.2, 3),
                round((join["frame_high"] - 10) * 0.2, 3),
            ]
        join["event_utc"] = rows[index]["timestamp_utc"]
        joins[event.get("ordinal")] = join
        counts[join["status"]] = counts.get(join["status"], 0) + 1
    summary = {
        "hook": RUNTIME_V4_HOOK,
        "tick_intervals": len(intervals),
        "tolerance_seconds": tolerance_s,
        "status_counts": dict(sorted(counts.items())),
        "basis": "tick_hook_entry_leave_frame_reads",
        "note": "A bracketed frame is exact only within the recorded bracket; "
                "wide or unbracketed joins stay unresolved.",
    }
    return joins, summary


def _rt_attach_frame_correlation(manifest, rows):
    """Attach tick-frame joins to every event that has one."""
    hook = RUNTIME_V4_HOOK
    if not any(row.get("hook") == hook for row in rows):
        return manifest
    unpaired = {}
    for row in rows:
        name = row.get("hook")
        if not name:
            continue
        if row.get("event") == "enter":
            unpaired[name] = unpaired.get(name, 0) + 1
        elif row.get("event") == "leave":
            unpaired[name] = unpaired.get(name, 0) - 1
    leftovers = {name: count for name, count in unpaired.items() if count}
    _require(set(leftovers) <= {hook}, "unpaired call outside the tick hook: %r" % (leftovers,))
    joins, summary = correlate_tick_frames(rows, manifest.get("events") or ())
    summary["unpaired_calls"] = leftovers
    summary["unpaired_note"] = (
        "unpaired calls are confined to the tick hook; no event hook lost a pair")
    for event in manifest.get("events") or ():
        join = joins.get(event.get("ordinal"))
        if join is None:
            continue
        time_block = event.setdefault("time", {})
        time_block["frame_correlation"] = join
        if "replay_frame_hypothesis" in time_block:
            time_block["replay_frame_hypothesis"]["status"] = (
                "superseded_by_tick_frame_correlation")
    manifest["frame_correlation"] = summary
    return manifest


def extract_runtime(rows, source_name, source_sha256, line_count, index,
                    index_name, index_sha256, profile=None):
    """Recompute the runtime manifest from parsed rows and a parsed index.

    ``profile`` may be ``None`` (autodetect from the exact known hook set), a
    profile name such as ``"runtime"``/``"runtime-v3"``, or a profile mapping.
    """
    if isinstance(profile, str):
        profile = _rt_profile(profile)
    manifest = _rt_extract(rows, source_name, source_sha256, line_count, index,
                           index_name, index_sha256, profile)
    return _rt_attach_frame_correlation(manifest, rows)


def _rt_verify_capture_sources(directory, profile=None):
    """Authenticate the three retained capture files; never substitute current code."""
    profile = profile or RUNTIME_PROFILE_V2
    pins = dict(profile["capture_source_pins"])
    pins[profile["capture_config_pin"]["file"]] = profile["capture_config_pin"]["sha256"]
    records = []
    for name, expected in pins.items():
        path = Path(directory) / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if profile["name"] in ("runtime-v3", "runtime-v4"):
            _require(actual is not None, "capture source missing: %s" % name)
        _require(actual is None or actual == expected,
                 "capture source sha256 mismatch: %s" % name)
        records.append({"name": name, "expected_sha256": expected,
                        "sha256": actual, "status": "matched" if actual else "missing"})
    return records


def extract_runtime_file(trace_path, index_path,
                         expect_trace_sha256=RUNTIME_TRACE_SHA256,
                         expect_index_sha256=RUNTIME_INDEX_SHA256,
                         profile=None):
    rows, name, digest, line_count = load_trace(trace_path, expect_trace_sha256)
    index, index_sha256, index_name = _rt_load_index(index_path, expect_index_sha256)
    if isinstance(profile, str):
        profile = _rt_profile(profile)
    manifest = _rt_extract(rows, name, digest, line_count, index, index_name,
                           index_sha256, profile)
    manifest = _rt_attach_frame_correlation(manifest, rows)
    resolved = profile or _rt_detect_profile(rows)
    records = _rt_verify_capture_sources(Path(trace_path).parent / "capture-sources",
                                         resolved)
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


def _rt_position_lines(manifest):
    observations = manifest["position_observations"]
    changes = manifest["position_anchor_changes"]
    identity = manifest["position_identity"]
    lines = [
        "",
        "## Position observations (raw tagged anchors)",
        "",
        "Each row reads the 12-byte block addressed by the tagged pointer at "
        "`[owner+0x%x]`, masked with `0x%s` and offset by `+0x%x`, from the same "
        "object whose `+0x20` handle and `+0x28` descriptor pointer are recorded."
        % (228, RUNTIME_V3_POSITION_MASK, RUNTIME_V3_POSITION_OFFSET),
        "The three coordinates are unmapped raw float32 values, not metres, world "
        "units or a visual centre, and the anchor object's own semantics are "
        "unproven.",
        "",
        "Identity is the same-capture triple `handle_u32 + owner_object + "
        "descriptor_pointer`: %d observations in %d tracks (%d single-observation "
        "tracks). %d observations are bracketed by adjacent clock-enter samples in "
        "one clock epoch and %d are not; identity conflicts: %d."
        % (identity["observations"], identity["tracks"],
           identity["tracks_with_single_observation"],
           identity["bracketed_observations"], identity["unbracketed_observations"],
           len(identity["conflicts"])),
        "",
        "| track | handle | owner | descriptor | unit | obs | changed |",
        "|---|---:|---|---|---|---:|---:|",
    ]
    tracks = _rt_position_tracks(observations)
    for key in sorted(tracks):
        track = tracks[key]
        first = track[0]["identity"]
        versions = {item["anchor"]["raw_hex"] for item in track
                    if item["anchor"]["status"] == "read_ok"}
        join = first["descriptor_join"]
        lines.append("| `%s` | %d | `%s` | `%s` | %s | %d | %s |" % (
            key, first["handle_u32"], first["owner_object"],
            first["descriptor_pointer"],
            (join.get("debug_name") or "UNRESOLVED") +
            ("" if join.get("status") == "2_of_2_exact_guid_and_token"
             else " (`%s`)" % join.get("status")),
            len(track), "yes" if len(versions) > 1 else "no"))
    lines.extend(["", "### Observation list", ""])
    for observation in observations:
        anchor = observation["anchor"]
        bracket = observation["time"]["bracket"]
        if anchor["status"] == "read_ok":
            values = "(%s)" % ", ".join("%.6g" % value for value in anchor["xyz"])
            detail = "raw `%s` sha256 `%s`" % (anchor["raw_hex"],
                                               anchor["sha256"][:16])
        else:
            values = "-"
            detail = "position read failed: %s" % (anchor.get("reason") or "unknown")
        if bracket["bracketed"]:
            time_text = "bracket [%d..%d] L%d-L%d (%d ticks)" % (
                bracket["lower"]["counter"], bracket["upper"]["counter"],
                bracket["lower"]["line"], bracket["upper"]["line"],
                bracket["counter_span"])
        else:
            time_text = "unbracketed (%s)" % bracket.get("reason", "unknown")
        lines.append("- pos %d L%d %s %s handle %d h=%s %s | %s | %s" % (
            observation["index"], observation["line"], observation["hook"],
            observation["phase"], observation["identity"]["handle_u32"],
            observation["identity"]["owner_object"], values, detail, time_text))
    lines.extend([
        "",
        "### Position anchor changes (raw value transitions, not movements)",
        "",
        "Each row compares two reads of one identity track with the same anchor "
        "target. %d explicit changes were observed. A change is a raw value "
        "difference only: no displacement in metres, speed, heading, path, "
        "movement intent, arrival, frame or game time is derived." % len(changes),
        "",
    ])
    for index, change in enumerate(changes, 1):
        if change["kind"] != "position_anchor_changed":
            lines.append("- change %d **%s** `%s` L%d -> L%d (not comparable)"
                         % (index, change["kind"], change["identity_key"],
                            change["from"]["line"], change["to"]["line"]))
            continue
        bracket = change["time"]["bracket"]
        if bracket["bracketed"]:
            time_text = "bracket [%d..%d] L%d-L%d" % (
                bracket["lower"]["counter"], bracket["upper"]["counter"],
                bracket["lower"]["line"], bracket["upper"]["line"])
        else:
            time_text = "unbracketed"
        lines.append(
            "- change %d `%s` L%d -> L%d | d=(%s) raw | |d|=%g raw | %s | "
            "sha `%s` -> `%s`"
            % (index, change["identity_key"], change["from"]["line"],
               change["to"]["line"],
               ", ".join("%.6g" % value for value in change["delta_raw_f32"]),
               change["displacement_raw_f32"], time_text,
               change["raw_before_sha256"][:16], change["raw_after_sha256"][:16]))
    return lines


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
        "Source owners are engine-credited (static XP-credit path), not weapon-resolved. "
        "Missing source-owner pointers are unresolved, "
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
        "resolved by handle. Statically, the check's AL is the entry's Killed token; "
        "the message itself and debrief scoring are not captured.",
        "",
    ])
    for item in manifest["damage_lifecycle_observations"]:
        lines.append(
            "- ord %d handle %d | victim `%s` (node %s) | reported source handle %s `%s` "
            "(engine-credited) | impact L%d-L%d, check L%d-L%d | check %s AL=%d | destroy %s "
            "on `%s` L%d-L%d | Killed token=%d (static mapping; message not captured)"
            % (item["impact_ordinal"], item["damaged_handle_u32"],
               item["victim_unit"] or "UNRESOLVED", item["victim_unit_type_id"] or "-",
               item["reported_source_owner_handle_u32"],
               item["reported_source_unit"] or "UNRESOLVED",
               item["impact_refs"]["enter_line"], item["impact_refs"]["leave_line"],
               item["impact_refs"]["check_enter_line"], item["impact_refs"]["check_leave_line"],
               item["threshold"]["check_call_id"], item["threshold"]["al_u8"],
               item["destruction_call"]["call_id"], item["destruction_call"]["operand_object"],
               item["destruction_call"]["line_refs"][0],
               item["destruction_call"]["line_refs"][1],
               item["killed_token"]["value"]))
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
    if "position_observations" in manifest:
        lines.extend(_rt_position_lines(manifest))
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
    if "frame_correlation" in manifest:
        payloads["combat_frames.json"] = _json_text({
            "schema": "wgrd-aar-combat-frames/1",
            "source": manifest["source"],
            "profile": manifest.get("profile"),
            "frame_correlation": manifest["frame_correlation"],
            "events": [{"ordinal": event.get("ordinal"),
                        "kind": event.get("kind"),
                        "line_ref": event.get("line_ref"),
                        "frame_correlation": (event.get("time") or {}).get("frame_correlation")}
                       for event in manifest.get("events") or ()],
            "limitations": manifest["limitations"],
        })
    if "position_observations" in manifest:
        payloads["positions.json"] = _json_text({
            "schema": RUNTIME_V3_POSITIONS_SCHEMA,
            "source": manifest["source"],
            "profile": manifest.get("profile"),
            "clock_epochs": manifest["clock_epochs"],
            "position_identity": manifest["position_identity"],
            "observations": manifest["position_observations"],
            "anchor_changes": manifest["position_anchor_changes"],
            "limitations": manifest["limitations"],
        })
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
    parser.add_argument("trace", help="path to the raw runtime JSONL trace")
    parser.add_argument("--out", required=True, help="events output directory")
    parser.add_argument("--profile", choices=("runtime", "runtime-v3", "runtime-v4"),
                        default="runtime",
                        help="trace profile (default: runtime)")
    parser.add_argument("--runtime", action="store_true",
                        help="compatibility alias for --profile runtime")
    parser.add_argument("--unit-index", help="native unit index JSON (required)")
    parser.add_argument("--expect-unit-index-sha256", default=RUNTIME_INDEX_SHA256,
                        help="required unit index SHA-256")
    parser.add_argument("--expect-sha256", default=None,
                        help="required trace SHA-256 (default: profile pin)")
    args = parser.parse_args(argv)
    if args.unit_index is None:
        print("aar_events: --unit-index is required", file=sys.stderr)
        return 2
    selected = args.profile
    expect_trace = args.expect_sha256
    if expect_trace is None and selected != "runtime-v4":
        expect_trace = (RUNTIME_V3_TRACE_SHA256 if selected == "runtime-v3"
                        else RUNTIME_TRACE_SHA256)
    try:
        manifest = extract_runtime_file(args.trace, args.unit_index, expect_trace,
                                        args.expect_unit_index_sha256, selected)
        targets = write_runtime_outputs(manifest, args.out)
    except (AarTraceError, OSError) as error:
        print("aar_events: %s" % error, file=sys.stderr)
        return 2
    message = ("wrote %d runtime impacts, %d units, %d lifecycle destructions"
               % (len(manifest["events"]), len(manifest["units"]),
                  len(manifest["damage_lifecycle_observations"])))
    if "position_observations" in manifest:
        message += (", %d position observations, %d anchor changes"
                    % (len(manifest["position_observations"]),
                       len(manifest["position_anchor_changes"])))
    print("%s to %s" % (message, targets[0].parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
