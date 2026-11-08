#!/usr/bin/env python3
"""Find candidate x86 memory operands of the form [reg+disp32].

Used to locate consumers of NDF-registered struct fields when neither a PDB
symbol nor a type exists. Only ModRM bytes with mod=10 (disp32) are decoded,
and the byte before the ModRM must be a plausible r/m opcode, so a bare
immediate that happens to equal the displacement is usually rejected.

Hits are **candidates, not proof**: in a dense instruction stream any byte can
be read as an opcode, so a hit must be confirmed by disassembling its site with
Rizin before it is cited. Recorded as such in the AI decision-model note.

Read-only over file bytes.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys

from ai_rtti import Image, load_pe32

REGS = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]

# Opcodes that take a ModRM operand whose mod=10 form carries a disp32. The
# check exists because an immediate byte (for example `b8`, `mov eax, imm32`)
# decodes as mod=10/reg=7/rm=0 and would otherwise look like an operand.
PREFIXES = {0x66, 0x67, 0xF2, 0xF3}
RM_OPCODES = (set(range(0x00, 0x3C)) | {0x62, 0x63, 0x69, 0x6B}
              | set(range(0x80, 0x90)) | {0xC0, 0xC1, 0xC6, 0xC7, 0xD0, 0xD1,
                                          0xD2, 0xD3, 0xF6, 0xF7, 0xFE, 0xFF})


def _opcode_before(p: bytes, modrm_at: int) -> int | None:
    """Walk back over prefixes to the opcode byte preceding a ModRM."""
    i = modrm_at - 1
    steps = 0
    while i >= 0 and steps < 4:
        b = p[i]
        if b in PREFIXES:
            i -= 1
            steps += 1
            continue
        return b
    return None


def _decode(p: bytes, i: int) -> tuple[int, str] | None:
    """Decode a ModRM+SIB disp32 operand whose disp32 ends at *i*."""
    if i - 1 < 0:
        return None
    modrm = p[i - 1]
    if modrm >> 6 != 2:
        return None
    opcode = _opcode_before(p, i - 1)
    if opcode != 0x0F and opcode not in RM_OPCODES:
        return None
    rm = modrm & 7
    if rm == 4:  # SIB follows the ModRM
        sib = p[i - 2]
        base = sib & 7
        if base == 5 and (sib >> 6) == 0:
            return None
        return i - 2, f"[{REGS[base]}]sib"
    if rm == 5:
        return None
    return i - 1, f"[{REGS[rm]}]"


def find_disp_xrefs(image: Image, disp: int) -> list[dict]:
    needle = struct.pack("<I", disp)
    hits: list[dict] = []
    for s in image.sections:
        if not s.executable:
            continue
        start = s.data.find(needle)
        while start != -1:
            decoded = _decode(s.data, start)
            if decoded is not None:
                operand_off, base = decoded
                hits.append({
                    "site": s.va + operand_off,
                    "base": base,
                    "disp": disp,
                })
            start = s.data.find(needle, start + 1)
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", required=True)
    ap.add_argument("--disp", action="append", required=True,
                    help="hex displacement, e.g. 0x271 (repeatable)")
    ap.add_argument("--json")
    args = ap.parse_args(argv)
    image = load_pe32(args.exe)
    out = {}
    for raw in args.disp:
        disp = int(raw, 16)
        hits = find_disp_xrefs(image, disp)
        out[raw] = hits
        print(f"disp 0x{disp:04x}: {len(hits)} operand site(s)")
        for h in hits:
            print(f"   0x{h['site']:08x}  {h['base']}+0x{disp:x}")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
