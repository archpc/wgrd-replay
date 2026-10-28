#!/usr/bin/env python3
"""Reproduce the opcode 0x0C (TNetworkActionChangeProduction) layout finding.

Build 59638 creator FUN_00b2eeb0 (VA; file offset = VA - 0x401000 + 0x400),
reached from dispatcher jump table 0xb241f4[opcode - 2]. Read sequence:

    read(obj+0x04, 4)                u32 A      (observed 0xC000001E + slot)
    read(obj+0x08, 16)               raw16 B
    FUN_00b35cd0(obj+0x18)           u32 n, n x u32
    FUN_00b35fc0(obj+0x34)           u32 n, n x u32, each <= 0x0e
    FUN_00b290c0(obj+0x50)           u32 m, m x (12 raw + u32 <= 6)
    FUN_00b290c0(obj+0x9c)           u32 m, m x (12 raw + u32 <= 6)
    FUN_00b35cd0(obj+0xe8)           u32 n, n x u32
    FUN_00b29080(obj+0x104)          u32 C, raw16 D

Usage:
    python3 -B research/op0c_layout.py EXE REPLAY [REPLAY ...]

Part 1 reads the jump table from EXE and prints the 0x0C case stub and
creator address. Part 2 walks each replay with wgrd_replay.parse_replay,
parses every single-command block whose opcode is 0x0C with the sequence
above, and asserts exact consumption. Read-only; writes nothing.
"""
import glob
import os
from pathlib import Path
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import wgrd_replay as w  # noqa: E402

JUMP_TABLE_VA = 0xB241F4


def va2off(va):
    return va - 0x401000 + 0x400


def creator_from_table(exe, opcode):
    case = struct.unpack_from("<I", exe, va2off(JUMP_TABLE_VA) + (opcode - 2) * 4)[0]
    o = va2off(case)
    stub = exe[o:o + 12]
    i = stub.find(b"\xe8")
    rel = struct.unpack_from("<i", stub, i + 1)[0]
    return case, stub.hex(), case + i + 5 + rel


def parse_0c(b):
    o = 0

    def u32():
        nonlocal o
        if o + 4 > len(b):
            raise ValueError("short u32 at %d" % o)
        v = struct.unpack_from("<I", b, o)[0]
        o += 4
        return v

    def raw(n):
        nonlocal o
        if o + n > len(b):
            raise ValueError("short raw%d at %d" % (n, o))
        v = b[o:o + n]
        o += n
        return v

    if b[0] != 0x0C:
        raise ValueError("not opcode 0c")
    o = 1
    r = {"A": u32(), "B": raw(16).hex()}
    r["arr18"] = [u32() for _ in range(u32())]
    r["arr34"] = [u32() for _ in range(u32())]
    if any(v > 0x0E for v in r["arr34"]):
        raise ValueError("arr34 element > 0x0e")

    def points():
        out = []
        for _ in range(u32()):
            xyz = struct.unpack_from("<3f", raw(12))
            k = u32()
            if k > 6:
                raise ValueError("point kind > 6")
            out.append(xyz + (k,))
        return out

    r["pts50"] = points()
    r["pts9c"] = points()
    r["arrE8"] = [u32() for _ in range(u32())]
    r["C"] = u32()
    r["D"] = raw(16).hex()
    if o != len(b):
        raise ValueError("remainder %d bytes" % (len(b) - o))
    r["len"] = len(b)
    return r


def blocks_0c(path):
    rep = w.parse_replay(Path(path).read_bytes())
    out = []

    def walk(x):
        if isinstance(x, dict):
            bh = x.get("block_hex")
            if bh and bh[:2] == "0c" and x.get("count") in (1, None):
                out.append((x.get("frame"), x.get("slot"), bytes.fromhex(bh)))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(rep)
    return out


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    exe = Path(argv[1]).read_bytes()
    for op in (0x0C, 0x0D):
        case, stub, tgt = creator_from_table(exe, op)
        print("op %02x: case VA %08x stub %s -> creator VA %08x (file 0x%x)"
              % (op, case, stub, tgt, va2off(tgt)))
    rc = 0
    for pattern in argv[2:]:
        for path in sorted(glob.glob(os.path.expanduser(pattern))):
            fit, fails, sizes = 0, [], {}
            for fr, sl, b in blocks_0c(path):
                try:
                    r = parse_0c(b)
                    fit += 1
                    sizes[r["len"]] = sizes.get(r["len"], 0) + 1
                except ValueError as e:
                    fails.append((fr, sl, len(b), str(e)))
            print("%s: 0c single blocks fit=%d fail=%d sizes=%s"
                  % (os.path.basename(path), fit, len(fails), sizes))
            for f in fails[:5]:
                print("  FAIL frame=%s slot=%s len=%d %s" % f)
            if fails:
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
