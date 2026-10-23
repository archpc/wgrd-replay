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
    """Opcode 0x08: handle, 12 reserved, u32 k, 3x f32, u32 type, u16 len, text.

    Field meanings beyond layout are UNKNOWN/INFERRED; see FORMAT.md.
    Returns None if the block does not exactly match the layout.
    """
    if len(block) < 39 or block[0] != 0x08:
        return None
    handle, = struct.unpack_from("<I", block, 1)
    reserved = block[5:17]
    k, = struct.unpack_from("<I", block, 17)
    x, y, z = struct.unpack_from("<fff", block, 21)
    mtype, tlen = struct.unpack_from("<IH", block, 33)
    if 39 + tlen != len(block):
        return None
    raw_text = block[39:]
    out = {
        "opcode": 0x08,
        "player_handle": "0x%08x" % handle,
        "handle_matches_slot": handle == HANDLE_BASE + slot,
        "reserved_hex": reserved.hex(),
        "u32_at_17": k,
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


def parse_replay(b, include_empty=False, verify_digest=True):
    header, metadata = parse_header(b)
    frames = 0
    stats = {"star": 0, "pact": 0, "endt": 0, "empty_pact": 0, "unknown_chunks": 0}
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
                   "block_hex": block.hex()}
            dec = decode_op08(block, slot) if count == 1 else None
            if dec is not None:
                rec["decoded"] = dec
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
    return {"decoder": "wgrd_replay/0.2", "sha256": hashlib.sha256(b).hexdigest(),
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
