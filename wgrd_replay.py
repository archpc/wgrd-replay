"""Minimal, strict decoder for Wargame: Red Dragon replay files (.wargamerpl2).

Scope: only structures verified against authentic samples (see FORMAT.md).
Stdlib only, offline, deterministic. Container violations raise ReplayFormatError;
malformed command layouts are retained as diagnostics. Unknown records
and undecoded command blocks are preserved as raw hex.

Byte order and offsets (as the code below implements them):
  - ESAV header and every chunk header: big-endian (struct ">").
  - Chunk payloads, pact headers and command blocks: little-endian ("<").
  - Reported "offset" values are absolute file offsets for chunks and
    frame-level records; command "offset" values are relative to their block.
Integrity: SHA-224 over file[0x28:EOF] is checked after the structural walk.
parse_replay(verify_digest=False) (CLI --no-verify-digest) does not reject a
digest mismatch; digest_valid still reports the comparison result.
Unknown chunk tags are preserved in unknown_chunks. There is no opcode
scanning or resynchronisation: a command is split only where its creator-proven
reads say it ends.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import sys

# Container constants (FORMAT.md section 1). Header fields are big-endian.
MAGIC = b"ESAV"
# Strict policy: exact match. The executable accepts <= 1 (FUN_010b9300).
SUPPORTED_CONTAINER_VERSIONS = {1}
# Fixed header size; the JSON metadata starts here and runs for its declared length.
HEADER_SIZE = 0x38
# SHA-224 is stored at 0x0C..0x28 and covers file[0x28:EOF], starting at the rply chunk.
DIGEST_START = 0x28
# Chunk header: tag (4) | field A u32 BE | payload length u32 BE | field B u32 BE.
CHUNK_HEADER_SIZE = 16
# Currently unused: parse_replay dispatches on the literal tags, and any other tag
# (including cmpg, which the executable handles but no sample contains) goes to
# unknown_chunks. Kept as documentation of the tags the walk recognises.
KNOWN_TAGS = (b"star", b"pact", b"endt")
# Observed in every sample: command player handle == 0xC000001E + pact slot.
# Verified for opcode 0x08 per FORMAT.md section 5 (per-field counts there).
# Used only to report handle_matches_slot; it never rejects a block.
HANDLE_BASE = 0xC000001E
# Opcode -> action class, build 59638. Source: dispatcher FUN_00b24050 (movzx opcode;
# sub 2; cmp 0x20; jmp [eax*4+0xb241f4]); each case calls a creator whose body installs
# the named class's vtable (RTTI). Opcodes outside 0x02..0x22 take the default path.
OPCODE_CLASSES = {
    0x02: "TNetworkActionSurrender", 0x03: "TNetworkActionRetreat",
    0x04: "TNetworkActionCommitOptionPlayer", 0x05: "TNetworkActionStop",
    0x06: "TNetworkActionCreateGroup", 0x07: "TNetworkActionGiveOrderStandard",
    0x08: "TNetworkActionLaunchFumigene", 0x09: "TNetworkActionCancelFumigene",
    0x0A: "TNetworkActionAnnuleProduction", 0x0B: "TNetworkActionAnnuleLastProductionOfType",
    0x0C: "TNetworkActionChangeProduction", 0x0D: "TNetworkActionProductionUnite",
    0x0E: "TNetworkActionItemFinished", 0x0F: "TNetworkActionKill",
    0x10: "TNetworkActionAddMaterial", 0x11: "TNetworkActionSpawnUnit",
    0x12: "TNetworkActionSpawnUnitV2", 0x13: "TNetworkActionPlayerSynchroServiceAction",
    0x14: "TNetworkActionSetTechnoResearch", 0x15: "TNetworkActionStopTechnoResearch",
    0x16: "TNetworkActionDynamicCampaignEndTurn", 0x17: "TNetworkActionDeactivateWeapon",
    0x18: "TNetworkActionDeactivateSupply", 0x19: "TNetworkActionGiveOrderBattleGroup",
    0x1A: "TNetworkActionAutoBattleResolution", 0x1B: "TNetworkActionAvoidBattle",
    0x1C: "TNetworkActionCancelBattle", 0x1D: "TNetworkActionLaunchStrategicAction",
    0x1E: "TNetworkActionBuyBattleGroup", 0x1F: "TNetworkActionCancelBattleGroup",
    0x20: "TNetworkActionEventPopup", 0x21: "TNetworkActionRetreatFromBattle",
    0x22: "TNetworkActionResolveConflictInZone",
}


class ReplayFormatError(ValueError):
    """Raised for recognized container and timeline format violations."""


def json_safe(value):
    """Represent non-finite floats explicitly for strict JSON serialization."""
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite": "NaN" if math.isnan(value) else ("+Infinity" if value > 0 else "-Infinity")}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    return value


def _u32be(b, o):
    if o + 4 > len(b):
        raise ReplayFormatError("u32be read past end at 0x%x" % o)
    return struct.unpack_from(">I", b, o)[0]


def parse_header(b):
    """Validate the fixed ESAV header and return (header_dict, metadata).

    Layout (big-endian): magic 0x00, container version 0x04, declared size 0x08,
    SHA-224 0x0C..0x28, rply chunk header at 0x28 (its reserved field A at 0x2C,
    length at 0x30, reserved field B at 0x34), JSON metadata at 0x38.
    The digest is not checked here; parse_replay checks it after the chunk walk.
    """
    if len(b) < HEADER_SIZE:
        raise ReplayFormatError("file shorter than fixed header (%d bytes)" % len(b))
    if b[0:4] != MAGIC:
        raise ReplayFormatError("bad magic %r at 0x0" % b[0:4])
    version = _u32be(b, 0x04)
    if version not in SUPPORTED_CONTAINER_VERSIONS:
        raise ReplayFormatError("unsupported container version %d at 0x4" % version)
    declared = _u32be(b, 0x08)
    # Equality, not <=: truncated or padded files are rejected before any chunk is read.
    # The executable does not compare this field; the exact match is decoder policy.
    if declared != len(b):
        raise ReplayFormatError("declared size %d at 0x8 != actual %d" % (declared, len(b)))
    if b[0x28:0x2C] != b"rply":
        raise ReplayFormatError("expected 'rply' at 0x28, got %r" % b[0x28:0x2C])
    # 0x2C and 0x34 are the rply chunk's reserved fields. Zero in every sample; the
    # executable does not test them, so this is strictness, not executable parity.
    for off in (0x2C, 0x34):
        if _u32be(b, off) != 0:
            raise ReplayFormatError("reserved u32 at 0x%x is non-zero (unobserved)" % off)
    # 0x30 is the rply chunk length, and the JSON is that chunk's whole payload.
    json_len = _u32be(b, 0x30)
    end = HEADER_SIZE + json_len
    if end > len(b):
        raise ReplayFormatError("JSON length %d overruns file" % json_len)
    try:
        # json.loads also accepts NaN/Infinity tokens, which are not strict JSON.
        # Metadata is echoed back to the caller as-is.
        metadata = json.loads(b[HEADER_SIZE:end].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ReplayFormatError("metadata JSON invalid: %s" % e)
    if not isinstance(metadata, dict):
        raise ReplayFormatError("metadata JSON root must be an object")
    game = metadata.get("game", {})
    if not isinstance(game, dict):
        raise ReplayFormatError("metadata game must be an object")
    return {
        "magic": MAGIC.decode(),
        "container_version": version,
        "declared_file_size": declared,
        "sha224_hex": b[0x0C:0x28].hex(),
        "json_offset": HEADER_SIZE,
        "json_length": json_len,
        "payload_offset": end,
        "game_version": game.get("Version"),
    }, metadata


def iter_chunks(b, start):
    """Yield (offset, tag, payload) for each chunk from start to EOF.

    Chunks are contiguous: no padding and no trailing bytes, so the walk must end
    exactly at len(b). Field A and field B must be zero in this decoder (a policy
    choice; field A's meaning is UNKNOWN per FORMAT.md). Offsets are absolute.
    This is a generator, so violations raise during iteration, not at the call.
    """
    o = start
    while o < len(b):
        if o + CHUNK_HEADER_SIZE > len(b):
            raise ReplayFormatError("truncated chunk header at 0x%x" % o)
        tag = b[o:o + 4]
        r1, length, r2 = struct.unpack_from(">III", b, o + 4)
        if r1 != 0 or r2 != 0:
            raise ReplayFormatError("non-zero reserved chunk field at 0x%x" % o)
        if o + CHUNK_HEADER_SIZE + length > len(b):
            raise ReplayFormatError("chunk at 0x%x length %d overruns file" % (o, length))
        yield o, tag, b[o + CHUNK_HEADER_SIZE:o + CHUNK_HEADER_SIZE + length]
        o += CHUNK_HEADER_SIZE + length
    # Effectively unreachable: the loop exits only when o >= len(b), and any overrun
    # is raised above. Kept as a final assertion of exact EOF consumption.
    if o != len(b):
        raise ReplayFormatError("chunk walk ended at 0x%x, file is 0x%x" % (o, len(b)))


def decode_op08(block, slot):
    """Opcode 0x08 = TNetworkActionLaunchFumigene (build 59638 dispatcher FUN_00b24050,
    jump table 0xb241f4 -> creator FUN_00b2fbc0). The creator reads, after the opcode:
    4 bytes (obj+0x04), 16 bytes (obj+0x08), 12 bytes (obj+0x18), 4 bytes (obj+0x24),
    then a u16-length-prefixed byte string (FUN_008fb4a0). Reads are raw (native LE).
    Field names below beyond that layout are INFERRED from replay data; see FORMAT.md.
    Returns None if the block does not exactly match the layout.
    """
    if len(block) < 39 or block[0] != 0x08:
        return None
    # Opcode 0x08 block. Offsets count from block start; byte 0 is the opcode.
    # Layout verified from the executable (FORMAT.md section 5). Meanings are not.
    #
    #   off  size  wire type   field        interpretation
    #     1     4  u32 LE      handle       INFERRED player handle
    #     5    16  raw         unknown16    UNKNOWN
    #    21    12  3 x f32 LE  position     INFERRED map position
    #    33     4  u32 LE      type         UNKNOWN (0..3 observed)
    #    37     2  u16 LE      text length  layout only: T
    #    39     T  bytes       text         INFERRED label
    #
    # The block must be exactly 39 + T bytes. Text is decoded as UTF-8 when valid.
    handle, = struct.unpack_from("<I", block, 1)
    x, y, z = struct.unpack_from("<fff", block, 21)
    mtype, tlen = struct.unpack_from("<IH", block, 33)
    if 39 + tlen != len(block):
        return None
    raw_text = block[39:]
    out = {
        "opcode": 0x08,
        "class": OPCODE_CLASSES[0x08],
        "player_handle": "0x%08x" % handle,
        "handle_matches_slot": handle == HANDLE_BASE + slot,
        "unknown16_hex": block[5:21].hex(),
        "position_f32": [x, y, z],
        "type_u32": mtype,
        "text_length": tlen,
    }
    try:
        out["text"] = raw_text.decode("utf-8")
    except UnicodeDecodeError:
        out["text_decode_error"] = True
        out["text_hex"] = raw_text.hex()
    return out


class _CommandCursor:
    """One bounded, shared cursor; never scan ahead for an opcode."""

    def __init__(self, block):
        self.block, self.offset = block, 0

    def take(self, size):
        # Slices silently truncate; reject the overrun before advancing the cursor.
        # Negative sizes are rejected defensively, not read from the wire.
        if size < 0 or size > len(self.block) - self.offset:
            raise ReplayFormatError("command read of %d bytes overruns block at 0x%x"
                                    % (size, self.offset))
        start = self.offset
        self.offset += size
        return self.block[start:self.offset]

    def uint(self, size):
        return int.from_bytes(self.take(size), "little")


def _read_array(cursor, width):
    # Bound the entire untrusted count in take(); do not allocate per element first.
    count = cursor.uint(4)
    return {"count_u32": count, "items_hex": cursor.take(count * width).hex()}


def _read_string(cursor):
    length = cursor.uint(2)
    return {"length_u16": length, "bytes_hex": cursor.take(length).hex()}


def _read_u32_array(cursor):
    count = cursor.uint(4)
    raw = cursor.take(count * 4)
    return {"count_u32": count, "items_hex": raw.hex(),
            "items_u32": [int.from_bytes(raw[i:i + 4], "little") for i in range(0, len(raw), 4)]}


# Compatibility name for point-field JSON normalization.
_f32_json = json_safe


def _read_points(cursor):
    # Element: 12 raw bytes (3 x float32 LE) then u32 kind; kind bound 6 per creator.
    count = cursor.uint(4)
    raw = cursor.take(count * 16)
    items = []
    for i in range(0, len(raw), 16):
        kind = int.from_bytes(raw[i + 12:i + 16], "little")
        if kind > 6:
            raise ReplayFormatError("point kind %d exceeds creator bound 6" % kind)
        xyz = [_f32_json(v) for v in struct.unpack_from("<3f", raw, i)]
        items.append({"xyz_f32": xyz, "kind_u32": kind})
    return {"count_u32": count, "items_hex": raw.hex(), "items": items}


def _decode_command(cursor, slot):
    """Decode one command at the cursor, or return None if the opcode has no layout.

    Returning None is not an error here: the caller marks the block "unresolved"
    and stops. Each branch reads fields in the creator's order. Field names are
    storage offsets (obj_XX), not game meanings. Layouts were recovered from build
    59638 only (AGENTS.md section 5).
    """
    start = cursor.offset
    # DRAGON (layout trust): these layouts were recovered from build 59638 only. A replay
    # from another build can split to the exact byte count and still carry different
    # field meanings. Exact consumption proves structure, not semantics (AGENTS.md 7).
    #                                /\                     /\
    #                               /  \                   /  \
    #                              / |  \                 / |  \
    #                             /  |\  \               /  |\  \
    #                            /   | \  \             /   | \  \
    #                           /    |  \  \           /    |  \  \
    #                          /  _  |   \  \         /  _  |   \  \
    #                         /.-' \_|____\  \_______/.-' \_|____\  \
    #              /\  /\    /  \    \     \ /  \    \     \    \  \
    #         ____/  \/  \__/    \    \____ V    \    \____ V    \  \
    #     ___/    o         \     \     /\        \     /\        \  \
    #   _/  _                \     \___/  \________\___/  \_______/   \__
    #  /   / \________        /\          /\  /\  /\  /\              \  `-._
    # /___/  v v v v  \______/  \________/  \/  \/  \/  \______________\      `-._
    # \___\_^_^_^_^___/        \                                       \          `-._
    #      \____________________\____  ____  ____  ____  ____  ____  ___\___         `-.
    #                               ||    ||    ||    ||    ||    ||    ||  `-.__       `
    #                               ||    ||    ||    ||    ||    ||    ||
    #                               ||    ||    ||    ||    ||    ||    ||
    #                               ||____||    ||____||    ||____||    ||
    #                              /_|__       /_|__       /_|__       /_|__
    #                             /_/_/       /_/_/       /_/_/       /_/_/
    # "It parsed cleanly" is a structural claim.
    # Read it as bytes, not as game actions.
    # Dragon identification: inferred. The cow won. Further funding was denied.
    opcode = cursor.uint(1)
    field_status = "layout"
    if opcode == 0x07:
        # FUN_00b2f850; two FUN_00b35e30 arrays: u32 count, 20 bytes/entry.
        # Creator bound: obj+f4 <= 3 (checked below). Total 71 + 20*(N1+N2) + T.
        fields = {"obj_04_array": _read_array(cursor, 20),
                  "obj_60_array": _read_array(cursor, 20),
                  "obj_bc_hex": cursor.take(12).hex(),
                  "obj_c8_hex": cursor.take(8).hex(),
                  "obj_d0_hex": cursor.take(36).hex(), "obj_f4_u32": cursor.uint(4)}
        if fields["obj_f4_u32"] > 3:
            raise ReplayFormatError("opcode 07 obj+0xf4 exceeds creator bound 3")
        fields["obj_f8_string"] = _read_string(cursor)
    elif opcode in (0x04, 0x09, 0x0A):
        # FUN_00b2edc0: read(obj+4,4), read(obj+8,16), read(obj+0x18,4).
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_hex": cursor.take(16).hex(),
                  "obj_18_u32": cursor.uint(4)}
        if opcode == 0x0A:
            # FUN_00b2e870 additionally checks +0x18 <=14 and reads +0x1c.
            if fields["obj_18_u32"] > 14:
                raise ReplayFormatError("opcode 0a obj+0x18 exceeds creator bound 14")
            fields["obj_1c_u32"] = cursor.uint(4)
    elif opcode == 0x08:
        cursor.take(36)
        cursor.take(cursor.uint(2))
        fields = decode_op08(cursor.block[start:cursor.offset], slot)
    elif opcode == 0x17:
        # FUN_00b2f3b0: u32, u32 count with two u32 per entry, raw byte.
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_array": _read_array(cursor, 8),
                  "obj_18_u8": cursor.uint(1)}
    elif opcode == 0x0D:
        # FUN_00b28ef0 -> root FUN_00b584e0 -> child FUN_00b580a0.
        # Child constructor copies the complete length-delimited body up front.
        # This proves the command boundary, not the interior serializer layout.
        variant = cursor.uint(4)
        if variant not in (1, 2, 3):
            raise ReplayFormatError("opcode 0d unsupported creator variant %d" % variant)
        fields = {"variant_u32": variant, "serializer_header_u32": cursor.uint(4),
                  "serializer_header_u8": cursor.uint(1), "serializer_section_u32": cursor.uint(4),
                  "serializer_length_u32": cursor.uint(4)}
        fields["serializer_payload_hex"] = cursor.take(fields["serializer_length_u32"]).hex()
        field_status = "opaque"
    elif opcode == 0x0C:
        # FUN_00b2eeb0, build 59638; research/CHANGEPRODUCTION-0C.md.
        # Helper         wire layout (LE)
        # FUN_00b35cd0   u32 count + count x u32
        # FUN_00b35fc0   same, with each element <= 0x0e
        # FUN_00b290c0   u32 count + count x {3 x f32, u32 kind <= 6}
        # FUN_00b29080   u32 + raw16
        # These are read layouts; field meanings remain unconfirmed.
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_hex": cursor.take(16).hex(),
                  "obj_18_array": _read_u32_array(cursor)}
        obj_34 = _read_u32_array(cursor)
        if any(v > 0x0E for v in obj_34["items_u32"]):
            raise ReplayFormatError("opcode 0c obj+0x34 element exceeds creator bound 14")
        fields["obj_34_array"] = obj_34
        fields["obj_50_points"] = _read_points(cursor)
        fields["obj_9c_points"] = _read_points(cursor)
        fields["obj_e8_array"] = _read_u32_array(cursor)
        fields["obj_104_u32"] = cursor.uint(4)
        fields["obj_108_hex"] = cursor.take(16).hex()
    elif opcode == 0x0E:
        # FUN_00b2f9e0: 4 -> obj+4, 4 -> obj+8, 16 -> obj+0x0c.
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_u32": cursor.uint(4),
                  "obj_0c_hex": cursor.take(16).hex()}
    elif opcode == 0x02:
        # FUN_00b30660 (build 59638): 4 -> obj+4, 16 -> obj+8, 1 -> obj+0x18.
        # The creator has no bounds checks; this decoder's cursor still bounds every read.
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_hex": cursor.take(16).hex(),
                  "obj_18_u8": cursor.uint(1)}
    elif opcode in (0x13, 0x18):
        # FUN_00b2fdd0 (0x13): 4 -> obj+4, 4 -> obj+8, 4 -> obj+0x0c.
        # FUN_00b2f2e0 (0x18): 4 -> obj+4, 4 -> obj+8, 1 -> obj+0x0c.
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_u32": cursor.uint(4)}
        if opcode == 0x13:
            fields["obj_0c_u32"] = cursor.uint(4)
        else:
            fields["obj_0c_u8"] = cursor.uint(1)
    else:
        return None
    return {"opcode": opcode, "class": OPCODE_CLASSES[opcode], "offset": start,
            "length": cursor.offset - start, "fields": fields,
            "field_decode_status": field_status,
            "raw_hex": cursor.block[start:cursor.offset].hex()}


def decode_command_block(block, count, slot):
    """Creator-backed split. Opaque serializer bodies are framed, not decoded.

    Exact count and byte consumption are strict decoder policy (the executable's
    count loop itself does not enforce EOF). Original block bytes stay on the pact.
    """
    cursor, commands = _CommandCursor(block), []
    status, reason = "complete", None
    # Each command needs an opcode byte. Reject impossible counts before the loop.
    if count < 0 or count > len(block):
        status, reason = "malformed", "command count exceeds available opcode bytes"
    else:
        for _ in range(count):
            start = cursor.offset
            try:
                command = _decode_command(cursor, slot)
            except ReplayFormatError as error:
                # Retain the whole failed command in remaining_hex, including reads
                # that succeeded before the error. A partial read is not a split.
                cursor.offset = start
                status, reason = "malformed", str(error)
                break
            if command is None:
                cursor.offset = start
                status, reason = "unresolved", "unsupported opcode 0x%02x at 0x%x" % (block[start], start)
                break
            commands.append(command)
        if status == "complete" and cursor.offset != len(block):
            status, reason = "malformed", "trailing bytes after declared command count"
        if status == "complete" and any(c["field_decode_status"] == "opaque" for c in commands):
            status = "framed"
    result = {"status": status, "layout_build": "59638", "commands": commands,
              "consumed_bytes": cursor.offset, "remaining_hex": block[cursor.offset:].hex()}
    if reason is not None:
        result["reason"] = reason
    return result


def parse_replay(b, include_empty=False, verify_digest=True):
    """Decode a whole replay into a result dict; format checks raise ReplayFormatError.

    Walk: header, then chunks. star opens a frame and its index must equal the running
    frame count (no gaps). Each pact is one slot's block: u32 frame, u32 slot,
    u32 count, u16 block length, then the block, all little-endian. Slots must appear
    in strictly increasing order, with the same IDs in every frame; IDs need not
    start at zero or be contiguous. These are decoder policies. endt closes the
    frame. Empty pacts (count 0) are counted in stats but omitted from commands
    unless include_empty is set. The SHA-224 check runs last, so structural
    errors are reported before digest errors.
    """
    header, metadata = parse_header(b)
    frames = 0
    stats = {"star": 0, "pact": 0, "endt": 0, "empty_pact": 0, "unknown_chunks": 0,
             "multi_command_blocks": 0, "fully_decoded_multi_blocks": 0,
             "fully_decoded_nonempty_blocks": 0, "fully_split_multi_blocks": 0,
             "fully_split_nonempty_blocks": 0}
    commands, unknown = [], []
    cur, slots, expected_slots = None, [], None
    for off, tag, p in iter_chunks(b, header["payload_offset"]):
        if tag == b"star":
            if cur is not None:
                raise ReplayFormatError("star at 0x%x before endt of frame %d" % (off, cur))
            if len(p) < 8:
                raise ReplayFormatError("star payload too short at 0x%x" % off)
            fi = struct.unpack_from("<I", p, 0)[0]
            if fi != frames:
                raise ReplayFormatError("frame %d at 0x%x, expected %d" % (fi, off, frames))
            cur, slots = fi, []
            stats["star"] += 1
        elif tag == b"pact":
            if cur is None or len(p) < 14:
                raise ReplayFormatError("pact outside frame or too short at 0x%x" % off)
            fi, slot, count, blen = struct.unpack_from("<IIIH", p, 0)
            if fi != cur:
                raise ReplayFormatError("pact frame %d != current %d at 0x%x" % (fi, cur, off))
            if slots and slot <= slots[-1]:
                raise ReplayFormatError("pact slot %d out of order at 0x%x" % (slot, off))
            if 14 + blen != len(p):
                raise ReplayFormatError("pact block length mismatch at 0x%x" % off)
            if (count == 0) != (blen == 0):
                raise ReplayFormatError("pact count/length inconsistent at 0x%x" % off)
            slots.append(slot)
            stats["pact"] += 1
            if count == 0:
                stats["empty_pact"] += 1
                if not include_empty:
                    continue
            block = p[14:]
            rec = {"frame": fi, "slot": slot, "offset": off, "count": count,
                   "block_length": blen, "first_opcode": block[0] if block else None,
                   "first_opcode_class": OPCODE_CLASSES.get(block[0]) if block else None,
                   "block_hex": block.hex()}
            decoded = decode_command_block(block, count, slot)
            rec["command_decode"] = decoded
            if count > 1:
                stats["multi_command_blocks"] += 1
            if count and decoded["status"] in ("complete", "framed"):
                stats["fully_split_nonempty_blocks"] += 1
                if count > 1:
                    stats["fully_split_multi_blocks"] += 1
            if count and decoded["status"] == "complete":
                stats["fully_decoded_nonempty_blocks"] += 1
                if count > 1:
                    stats["fully_decoded_multi_blocks"] += 1
                elif block[0] == 0x08:
                    rec["decoded"] = decoded["commands"][0]["fields"]
            commands.append(rec)
        elif tag == b"endt":
            if cur is None or len(p) < 4 or struct.unpack_from("<I", p, 0)[0] != cur:
                raise ReplayFormatError("endt mismatch at 0x%x" % off)
            stats["endt"] += 1
            frames += 1
            cur = None
            if stats.get("slots_per_frame") is None:
                stats["slots_per_frame"] = len(slots)
                expected_slots = slots
            elif stats["slots_per_frame"] != len(slots):
                raise ReplayFormatError("slot count changed at frame %d" % frames)
            elif slots != expected_slots:
                raise ReplayFormatError("slot IDs changed at frame %d" % (frames - 1))
        else:
            stats["unknown_chunks"] += 1
            unknown.append({"offset": off, "tag_hex": tag.hex(), "payload_hex": p.hex()})
    if cur is not None:
        raise ReplayFormatError("file ended inside frame %d" % cur)
    stats["frames"] = frames
    # 0x0C..0x27 = SHA-224(file[0x28:EOF]): verified on all samples and in the
    # executable (FUN_010b9500 hashes every chunk; FUN_016fd070 = SHA-224 init).
    # Checked after the structural walk so structural errors are reported first.
    # DRAGON (integrity): the digest proves the bytes match the header. It does not prove
    # the replay is genuine, and with verify_digest=False this function still returns
    # the full parsed structure for a file whose digest is wrong.
    #        __/ \__      HERE BE DRAGONS: a matching SHA-224 means the
    #       (  o  o  )     bytes agree with the header. It is not proof of
    #        \_/\_/        authenticity, and the dragon does not read receipts.
    actual = hashlib.sha224(b[DIGEST_START:]).digest()
    header["digest_valid"] = actual == b[0x0C:0x28]
    if verify_digest and not header["digest_valid"]:
        raise ReplayFormatError("SHA-224 mismatch: header %s, computed %s"
                                % (b[0x0C:0x28].hex(), actual.hex()))
    return {"decoder": "wgrd_replay/0.4", "sha256": hashlib.sha256(b).hexdigest(),
            "size": len(b), "header": header, "metadata": metadata,
            "stats": stats, "commands": commands, "unknown_chunks": unknown}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("replay")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--summary", action="store_true", help="omit command list")
    ap.add_argument("--timeline", action="store_true", help="export ordered command timeline with evidence status")
    ap.add_argument("--unit-data", metavar="INDEX_OR_ROOT", help="annotate timeline with build59638 index file or pinned public58710 directory (offline)")
    ap.add_argument("--no-verify-digest", action="store_true",
                    help="report digest_valid instead of failing on SHA-224 mismatch")
    a = ap.parse_args(argv)
    if a.unit_data and not a.timeline:
        ap.error("--unit-data requires --timeline")
    with open(a.replay, "rb") as f:
        b = f.read()
    format_errors = (ReplayFormatError,)
    if a.timeline:
        from wgrd_timeline import build_timeline, ReplayFormatError as TimelineFormatError
        # Direct script invocation and module imports can have distinct class identities.
        format_errors += (TimelineFormatError,)
    try:
        r = parse_replay(b, include_empty=a.include_empty,
                         verify_digest=not a.no_verify_digest)
        if a.timeline:
            if a.unit_data:
                from wgrd_unit_data import load_unit_data
                r = build_timeline(r, unit_data=load_unit_data(a.unit_data))
            else:
                r = build_timeline(r)
    except format_errors as e:
        print("ReplayFormatError: %s" % e, file=sys.stderr)
        return 2
    if a.summary:
        r.pop("events" if a.timeline else "commands")
    json.dump(json_safe(r), sys.stdout, sort_keys=True, ensure_ascii=False, indent=1,
              allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
