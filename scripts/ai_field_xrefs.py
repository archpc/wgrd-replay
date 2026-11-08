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
import re
import struct
import sys
from pathlib import Path

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
    """Decode one disp32 memory operand whose displacement ends at *i*.

    Two encodings reach this shape, and the order inside the instruction is
    always opcode, ModRM, [SIB], disp32:

    * no SIB  — ModRM at i-1, encoding [reg+disp32]; rm=5 is valid here
                because mod=10 means EBP base, not an absolute address.
    * with SIB — SIB at i-2 and ModRM at i-3, because a SIB byte sits between
                the ModRM and the displacement. Reading ModRM at i-1 for this
                case is the classic ordering bug: it decodes the SIB byte.

    Returns (operand_start_offset, base_label) or None.
    """
    # *i* is the first byte of the displacement, so the byte order backwards is
    # disp, [SIB], ModRM, opcode. SIB form first: reachable only when the
    # ModRM at i-2 says rm=4.
    if i - 2 >= 0 and (p[i - 2] >> 6) == 2 and (p[i - 2] & 7) == 4:
        opcode = _opcode_before(p, i - 2)
        if opcode == 0x0F or opcode in RM_OPCODES:
            sib = p[i - 1]
            base = sib & 7
            index = (sib >> 3) & 7
            scaled = "" if index == 4 else f"+{REGS[index]}*{1 << (sib >> 6)}"
            if base == 5 and (sib >> 6) == 0:
                return i - 2, f"[disp32{scaled}]"
            return i - 2, f"[{REGS[base]}{scaled}]"
        return None

    if i - 1 < 0:
        return None
    modrm = p[i - 1]
    if modrm >> 6 != 2 or (modrm & 7) == 4:
        return None
    opcode = _opcode_before(p, i - 1)
    if opcode != 0x0F and opcode not in RM_OPCODES:
        return None
    rm = modrm & 7
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


class RizinOracle:
    """Instruction-boundary oracle backed by one Rizin process per query set.

    Raw byte scanning cannot prove that a candidate address is an instruction
    start. This asks Rizin for the disassembly of the containing function once,
    then answers boundary and operand-text questions from that listing.
    """

    def __init__(self, exe: str, rizin: str = "rizin", afl_path: str | None = None):
        self.exe = exe
        self.rizin = rizin
        self.afl_path = afl_path
        self._funcs: list[tuple[int, int]] | None = None
        self._cache: dict[int, dict[int, str]] = {}

    def _run(self, script: str) -> str:
        import subprocess
        proc = subprocess.run(
            [self.rizin, "-q", "-e", "scr.colour=0", "-e", "scr.color=0",
             "-c", script, self.exe],
            capture_output=True, text=True, timeout=1800)
        return proc.stdout

    def functions(self) -> list[tuple[int, int]]:
        if self._funcs is None:
            rows = []
            text = (Path(self.afl_path).read_text() if self.afl_path
                    else self._run("aaa; afl"))
            for line in text.splitlines():
                m = re.match(r"0x([0-9a-f]+)\s+\d+\s+(\d+)", line)
                if m:
                    start = int(m.group(1), 16)
                    rows.append((start, start + int(m.group(2))))
            rows.sort()
            self._funcs = rows
        return self._funcs

    def function_of(self, va: int) -> int | None:
        import bisect
        funcs = self.functions()
        starts = [f[0] for f in funcs]
        i = bisect.bisect_right(starts, va) - 1
        if i < 0:
            return None
        start, end = funcs[i]
        return start if start <= va < end else None

    def instructions(self, func_start: int, func_size: int) -> dict[int, str]:
        if func_start not in self._cache:
            listing = {}
            # pdfj needs in-session analysis; pdj linearly disassembles from a
            # known function start, which is enough to test membership.
            raw = self._run(f"pdj {max(func_size, 16)} @ 0x{func_start:x}")
            start = raw.find("[")
            if start != -1:
                try:
                    for item in json.loads(raw[start:]):
                        listing[int(item["offset"])] = item.get("opcode", "")
                except (json.JSONDecodeError, KeyError, TypeError):
                    listing = {}
            self._cache[func_start] = listing
        return self._cache[func_start]

    def confirm(self, va: int, disp: int) -> tuple[bool, str]:
        """True when *va* is an instruction start whose listing shows disp."""
        fn = self.function_of(va)
        if fn is None:
            return False, "no containing function"
        size = dict(self.functions())[fn] - fn
        text = self.instructions(fn, size).get(va)
        if text is None:
            return False, "not an instruction start"
        if f"0x{disp:x}" not in text:
            return False, f"operand not visible: {text}"
        return True, text


    def confirm_call(self, va: int, target: int) -> bool:
        """True when *va* is a call instruction on a real boundary."""
        fn = self.function_of(va)
        if fn is None:
            return False
        size = dict(self.functions())[fn] - fn
        text = self.instructions(fn, size).get(va, "")
        return text.startswith("call") and f"0x{target:x}" in text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", required=True)
    ap.add_argument("--disp", action="append", required=True,
                    help="hex displacement, e.g. 0x271 (repeatable)")
    ap.add_argument("--json")
    ap.add_argument("--validate", action="store_true",
                    help="confirm each candidate on a Rizin instruction boundary")
    ap.add_argument("--rizin", default="rizin")
    ap.add_argument("--afl", help="reuse a saved 'aaa; afl' listing instead of re-analysing")
    args = ap.parse_args(argv)
    image = load_pe32(args.exe)
    oracle = RizinOracle(args.exe, args.rizin, args.afl) if args.validate else None
    out = {}
    for raw in args.disp:
        disp = int(raw, 16)
        hits = find_disp_xrefs(image, disp)
        confirmed = []
        for hit in hits:
            if oracle is None:
                confirmed.append(hit)
                continue
            ok, text = oracle.confirm(hit["site"], disp)
            if ok:
                confirmed.append({**hit, "confirmed_text": text})
            else:
                print(f"   reject 0x{hit['site']:08x}: {text}")
        out[raw] = confirmed
        print(f"disp 0x{disp:04x}: {len(hits)} candidate(s), {len(confirmed)} confirmed")
        for h in confirmed:
            print(f"   0x{h['site']:08x}  {h['base']}+0x{disp:x}")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
