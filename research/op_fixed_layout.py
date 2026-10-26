#!/usr/bin/env python3
"""Reproduce the fixed-size creator layouts for opcodes 0x02, 0x13, 0x18 (build 59638).

Creators reached from dispatcher jump table 0xb241f4[opcode - 2]
(VA; file offset = VA - 0x401000 + 0x400):

  0x02 TNetworkActionSurrender                  FUN_00b30660  obj 0x1c  vtbl 0x19a1854
        read(obj+0x04, 4) u32; read(obj+0x08, 16) raw; read(obj+0x18, 1) u8     -> 22 bytes
  0x13 TNetworkActionPlayerSynchroServiceAction FUN_00b2fdd0  obj 0x10  vtbl 0x19a19a8
        read(obj+0x04, 4) u32; read(obj+0x08, 4) u32; read(obj+0x0c, 4) u32     -> 13 bytes
  0x18 TNetworkActionDeactivateSupply           FUN_00b2f2e0  obj 0x10  vtbl 0x19a1a0c
        read(obj+0x04, 4) u32; read(obj+0x08, 4) u32; read(obj+0x0c, 1) u8      -> 10 bytes

Sizes include the opcode byte. No arrays, strings, or bounds checks.

Usage:
    python3 -B research/op_fixed_layout.py EXE REPLAY [REPLAY ...]

Part 1 reads the jump table from EXE and checks each case stub resolves to the
creator above AND that the creator body contains the expected read-size pushes
in order. Part 2 walks each replay, collects every single-command block whose
opcode is 02/13/18, and asserts its length equals the layout size. Exit 1 on
any mismatch. Read-only.
"""
import glob
import os
import re
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import wgrd_replay as w  # noqa: E402

JUMP_TABLE_VA = 0xB241F4
LAYOUTS = {
    # opcode: (creator VA, total size, [(dest offset, read size), ...])
    0x02: (0x00B30660, 22, [(0x04, 4), (0x08, 16), (0x18, 1)]),
    0x13: (0x00B2FDD0, 13, [(0x04, 4), (0x08, 4), (0x0C, 4)]),
    0x18: (0x00B2F2E0, 10, [(0x04, 4), (0x08, 4), (0x0C, 1)]),
}


def va2off(va):
    return va - 0x401000 + 0x400


def creator_from_table(exe, opcode):
    case = struct.unpack_from("<I", exe, va2off(JUMP_TABLE_VA) + (opcode - 2) * 4)[0]
    o = va2off(case)
    stub = exe[o:o + 12]
    i = stub.find(b"\xe8")
    rel = struct.unpack_from("<i", stub, i + 1)[0]
    return case, stub.hex(), case + i + 5 + rel


def read_pushes_in_order(exe, creator_va, size=240):
    """Return [(dest_offset, read_size), ...] for each reader call in the body.

    Each read is `push imm8 (size)` ... `lea eax,[esi+d8]` or `lea eax,[ebx+d8]`
    ... `push eax` ... `call edx`, i.e. bytes 6a SS .. 8d 46|43 DD .. 50 ff d2.
    Up to 12 bytes may sit between the push and the lea (mov edx,[eax+4] etc).
    FUN_00b30660 passes ebx (= esi+4) directly for its first read: 6a 04 53 ..
    ff d0, and uses ebx-relative lea for the second, so ebx-based dests add 4.
    """
    body = exe[va2off(creator_va):va2off(creator_va) + size]
    out = []
    pat = rb"\x6a(.)(?:.{0,12}?\x8d([\x46\x43])(.)\x50.{0,4}?\xff\xd2|\x53.{0,16}?\xff\xd0)"
    for m in re.finditer(pat, body, re.S):
        n = m.group(1)[0]
        if m.group(2) is None:            # push ebx form (ebx = esi+4)
            out.append((0x04, n))
        else:
            base = 0x04 if m.group(2) == b"\x43" else 0x00
            out.append((base + m.group(3)[0], n))
    return out


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    rc = 0
    exe = open(argv[1], "rb").read()
    for op, (creator, total, reads) in sorted(LAYOUTS.items()):
        case, stub, tgt = creator_from_table(exe, op)
        ok = tgt == creator
        pushes = read_pushes_in_order(exe, creator)
        expected = list(reads)
        ok_p = pushes == expected
        print("op %02x: case %08x -> creator %08x (%s); reads %s (%s)"
              % (op, case, tgt, "OK" if ok else "MISMATCH expected %08x" % creator,
                 ["+0x%02x:%d" % r for r in pushes], "OK" if ok_p else "MISMATCH expected %s" % expected))
        if not (ok and ok_p):
            rc = 1
    for pattern in argv[2:]:
        for path in sorted(glob.glob(os.path.expanduser(pattern))):
            rep = w.parse_replay(open(path, "rb").read())
            seen = {op: {} for op in LAYOUTS}
            bad = []

            def walk(x):
                if isinstance(x, dict):
                    bh = x.get("block_hex")
                    if bh and x.get("count") in (1, None) and int(bh[:2], 16) in LAYOUTS:
                        op, n = int(bh[:2], 16), len(bh) // 2
                        seen[op][n] = seen[op].get(n, 0) + 1
                        if n != LAYOUTS[op][1]:
                            bad.append((op, x.get("frame"), x.get("slot"), n))
                    for v in x.values():
                        walk(v)
                elif isinstance(x, list):
                    for v in x:
                        walk(v)

            walk(rep)
            print("%s: %s%s" % (os.path.basename(path),
                                " ".join("%02x=%s" % (op, seen[op]) for op in sorted(seen) if seen[op]),
                                "" if not bad else "  MISMATCH %s" % bad[:5]))
            if bad:
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
