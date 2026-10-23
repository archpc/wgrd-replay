"""Minimal, strict decoder for Wargame: Red Dragon replay files (.wargamerpl2).

Scope: only structures verified against authentic samples (see FORMAT.md).
Stdlib only, offline, deterministic. Any structural violation raises
ReplayFormatError; nothing is guessed or silently skipped. Unknown records
and undecoded command blocks are preserved as raw hex.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys

MAGIC = b"ESAV"
SUPPORTED_CONTAINER_VERSIONS = {1}
HEADER_SIZE = 0x38
DIGEST_START = 0x28
CHUNK_HEADER_SIZE = 16
KNOWN_TAGS = (b"star", b"pact", b"endt")
# Observed in every sample: command player handle == 0xC000001E + pact slot.
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
    """Raised for any violation of the verified layout."""


def _u32be(b, o):
    if o + 4 > len(b):
        raise ReplayFormatError("u32be read past end at 0x%x" % o)
    return struct.unpack_from(">I", b, o)[0]


def parse_header(b):
    if len(b) < HEADER_SIZE:
        raise ReplayFormatError("file shorter than fixed header (%d bytes)" % len(b))
    if b[0:4] != MAGIC:
        raise ReplayFormatError("bad magic %r at 0x0" % b[0:4])
    version = _u32be(b, 0x04)
    if version not in SUPPORTED_CONTAINER_VERSIONS:
        raise ReplayFormatError("unsupported container version %d at 0x4" % version)
    declared = _u32be(b, 0x08)
    if declared != len(b):
        raise ReplayFormatError("declared size %d at 0x8 != actual %d" % (declared, len(b)))
    if b[0x28:0x2C] != b"rply":
        raise ReplayFormatError("expected 'rply' at 0x28, got %r" % b[0x28:0x2C])
    for off in (0x2C, 0x34):
        if _u32be(b, off) != 0:
            raise ReplayFormatError("reserved u32 at 0x%x is non-zero (unobserved)" % off)
    json_len = _u32be(b, 0x30)
    end = HEADER_SIZE + json_len
    if end > len(b):
        raise ReplayFormatError("JSON length %d overruns file" % json_len)
    try:
        metadata = json.loads(b[HEADER_SIZE:end].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ReplayFormatError("metadata JSON invalid: %s" % e)
    return {
        "magic": MAGIC.decode(),
        "container_version": version,
        "declared_file_size": declared,
        "sha224_hex": b[0x0C:0x28].hex(),
        "json_offset": HEADER_SIZE,
        "json_length": json_len,
        "payload_offset": end,
        "game_version": metadata.get("game", {}).get("Version"),
    }, metadata


def iter_chunks(b, start):
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
        if size < 0 or size > len(self.block) - self.offset:
            raise ReplayFormatError("command read of %d bytes overruns block at 0x%x"
                                    % (size, self.offset))
        start = self.offset
        self.offset += size
        return self.block[start:self.offset]

    def uint(self, size):
        return int.from_bytes(self.take(size), "little")


def _read_array(cursor, width):
    count = cursor.uint(4)
    return {"count_u32": count, "items_hex": cursor.take(count * width).hex()}


def _read_string(cursor):
    length = cursor.uint(2)
    return {"length_u16": length, "bytes_hex": cursor.take(length).hex()}


def _decode_command(cursor, slot):
    start = cursor.offset
    opcode = cursor.uint(1)
    if opcode == 0x07:
        # FUN_00b2f850; two FUN_00b35e30 arrays: u32 count, 20 bytes/entry.
        fields = {"obj_04_array": _read_array(cursor, 20),
                  "obj_60_array": _read_array(cursor, 20),
                  "obj_bc_hex": cursor.take(12).hex(),
                  "obj_c8_hex": cursor.take(8).hex(),
                  "obj_d0_hex": cursor.take(36).hex(), "obj_f4_u32": cursor.uint(4)}
        if fields["obj_f4_u32"] > 3:
            raise ReplayFormatError("opcode 07 obj+0xf4 exceeds creator bound 3")
        fields["obj_f8_string"] = _read_string(cursor)
    elif opcode == 0x09:
        # FUN_00b2edc0: read(obj+4,4), read(obj+8,16), read(obj+0x18,4).
        fields = {"obj_04_u32": cursor.uint(4), "obj_08_hex": cursor.take(16).hex(),
                  "obj_18_u32": cursor.uint(4)}
    elif opcode == 0x08:
        cursor.take(36)
        cursor.take(cursor.uint(2))
        fields = decode_op08(cursor.block[start:cursor.offset], slot)
    else:
        return None
    return {"opcode": opcode, "class": OPCODE_CLASSES[opcode], "offset": start,
            "length": cursor.offset - start, "fields": fields,
            "raw_hex": cursor.block[start:cursor.offset].hex()}


def decode_command_block(block, count, slot):
    """Creator-backed split. Partial prefixes are explicitly unresolved/malformed.

    Exact count and byte consumption are strict decoder policy (the executable's
    count loop itself does not enforce EOF). Original block bytes stay on the pact.
    """
    cursor, commands = _CommandCursor(block), []
    status, reason = "complete", None
    if count < 0 or count > len(block):
        status, reason = "malformed", "command count exceeds available opcode bytes"
    else:
        for _ in range(count):
            start = cursor.offset
            try:
                command = _decode_command(cursor, slot)
            except ReplayFormatError as error:
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
    result = {"status": status, "layout_build": "59638", "commands": commands,
              "consumed_bytes": cursor.offset, "remaining_hex": block[cursor.offset:].hex()}
    if reason is not None:
        result["reason"] = reason
    return result


def parse_replay(b, include_empty=False, verify_digest=True):
    header, metadata = parse_header(b)
    frames = 0
    stats = {"star": 0, "pact": 0, "endt": 0, "empty_pact": 0, "unknown_chunks": 0,
             "multi_command_blocks": 0, "fully_decoded_multi_blocks": 0,
             "fully_decoded_nonempty_blocks": 0}
    commands, unknown = [], []
    cur, slots = None, []
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
            if slot != len(slots):
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
            elif stats["slots_per_frame"] != len(slots):
                raise ReplayFormatError("slot count changed at frame %d" % frames)
        else:
            stats["unknown_chunks"] += 1
            unknown.append({"offset": off, "tag_hex": tag.hex(), "payload_hex": p.hex()})
    if cur is not None:
        raise ReplayFormatError("file ended inside frame %d" % cur)
    stats["frames"] = frames
    # 0x0C..0x27 = SHA-224(file[0x28:EOF]): verified on all samples and in the
    # executable (FUN_010b9500 hashes every chunk; FUN_016fd070 = SHA-224 init).
    # Checked after the structural walk so structural errors are reported first.
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
    ap.add_argument("--no-verify-digest", action="store_true",
                    help="report digest_valid instead of failing on SHA-224 mismatch")
    a = ap.parse_args(argv)
    with open(a.replay, "rb") as f:
        b = f.read()
    try:
        r = parse_replay(b, include_empty=a.include_empty,
                         verify_digest=not a.no_verify_digest)
    except ReplayFormatError as e:
        print("ReplayFormatError: %s" % e, file=sys.stderr)
        return 2
    if a.summary:
        r.pop("commands")
    json.dump(r, sys.stdout, sort_keys=True, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
