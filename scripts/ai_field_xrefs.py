#!/usr/bin/env python3
"""Find and confirm x86 memory operands of the form [reg+disp32].

Used to locate consumers of NDF-registered struct fields when neither a PDB
symbol nor a type exists.

Two stages, deliberately separate:

1. `find_disp_xrefs` scans for displacement dwords whose preceding bytes decode
   as a disp32 ModRM operand. Cheap, and a **candidate** list only.
2. `RizinOracle.confirm_many` asks Rizin for the containing function's real
   disassembly and keeps only candidates that are instruction starts whose
   operand text shows the displacement.

Byte order inside an instruction is opcode, ModRM, [SIB], disp32. With *i* at
the first displacement byte: ModRM is at i-1 (no SIB) or i-2 (SIB at i-1).
`[ebp+disp32]` (ModRM mod=10, rm=5) and SIB base=ebp are register operands, not
absolute addresses. Two-byte 0F opcodes are reported as 0x0F00|second_byte,
because the byte before the ModRM is the second opcode byte, not a standalone
opcode.

Read-only over file bytes. Never loads or executes the target.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

from ai_rtti import Image, load_pe32

REGS = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]

PREFIXES = {0x66, 0x67, 0xF2, 0xF3}
RM_OPCODES = (set(range(0x00, 0x3C)) | {0x62, 0x63, 0x69, 0x6B}
              | set(range(0x80, 0x90)) | {0xC0, 0xC1, 0xC6, 0xC7, 0xD0, 0xD1,
                                          0xD2, 0xD3, 0xF6, 0xF7, 0xFE, 0xFF})


def _opcode(p: bytes, modrm_at: int) -> tuple[int, int] | None:
    """Return (opcode_value, opcode_offset), skipping legacy prefixes."""
    i = modrm_at - 1
    while i >= 0 and p[i] in PREFIXES:
        i -= 1
    if i < 0:
        return None
    second = p[i]
    if i >= 1 and p[i - 1] == 0x0F:
        return 0x0F00 | second, i - 1
    return second, i


def _instruction_start(p: bytes, opcode_off: int) -> int:
    i = opcode_off
    while i - 1 >= 0 and p[i - 1] in PREFIXES:
        i -= 1
    return i


def _accepts_memory(opcode: int) -> bool:
    if opcode >> 8 == 0x0F:      # two-byte SSE/system forms
        return True
    return opcode in RM_OPCODES


def _decode(p: bytes, i: int) -> tuple[int, str] | None:
    """Decode a disp32 memory operand whose displacement starts at *i*.

    Returns (instruction_start_offset, base_label) or None.
    """
    # SIB form: ModRM at i-2 (rm=4), SIB at i-1.
    if i - 2 >= 0 and (p[i - 2] >> 6) == 2 and (p[i - 2] & 7) == 4:
        found = _opcode(p, i - 2)
        if found is None or not _accepts_memory(found[0]):
            return None
        sib = p[i - 1]
        base = sib & 7
        index = (sib >> 3) & 7
        scale = 1 << (sib >> 6) if index != 4 else 0
        scaled = f"+{REGS[index]}*{scale}" if scale else ""
        # ModRM mod is 10 here, so base=5 is EBP, never "no base".
        label = f"[ebp{scaled}]" if base == 5 else f"[{REGS[base]}{scaled}]"
        return _instruction_start(p, found[1]), label

    if i - 1 < 0:
        return None
    modrm = p[i - 1]
    if modrm >> 6 != 2 or (modrm & 7) == 4:
        return None
    found = _opcode(p, i - 1)
    if found is None or not _accepts_memory(found[0]):
        return None
    return _instruction_start(p, found[1]), f"[{REGS[modrm & 7]}]"


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
                insn_off, base = decoded
                hits.append({"site": s.va + insn_off, "base": base, "disp": disp})
            start = s.data.find(needle, start + 1)
    return hits


class RizinOracle:
    """Instruction-boundary oracle for candidate sites and call targets.

    A linear `pdj` sweep from a function start desynchronises on real functions
    that contain embedded data or unreachable bytes, so this asks Rizin for
    analysis once, then for `pdfj` of each containing function in the same
    process.
    """

    def __init__(self, exe: str, rizin: str = "rizin", afl_path: str | None = None,
                 image: Image | None = None):
        self.exe = exe
        self.rizin = rizin
        self.afl_path = afl_path
        self.image = image
        self._funcs: list[tuple[int, int]] | None = None
        self._listing: dict[int, str] = {}

    def _run(self, commands: list[str]) -> str:
        args = [self.rizin, "-q", "-e", "scr.color=0", "-e", "scr.colour=0"]
        for cmd in commands:
            args += ["-c", cmd]
        args.append(self.exe)
        proc = subprocess.run(args, capture_output=True, text=True, timeout=3600)
        return proc.stdout

    def functions(self) -> list[tuple[int, int]]:
        if self._funcs is None:
            text = (Path(self.afl_path).read_text() if self.afl_path
                    else self._run(["aaa", "afl"]))
            rows = []
            for line in text.splitlines():
                m = re.match(r"0x([0-9a-f]+)\s+\d+\s+(\d+)", line)
                if m:
                    start = int(m.group(1), 16)
                    rows.append((start, start + int(m.group(2))))
            rows.sort()
            self._funcs = rows
        return self._funcs

    def function_of(self, va: int) -> int | None:
        funcs = self.functions()
        i = bisect.bisect_right([f[0] for f in funcs], va) - 1
        if i < 0:
            return None
        start, end = funcs[i]
        return start if start <= va < end else None

    def load(self, addresses: list[int]) -> None:
        """Disassemble the containing functions of *addresses* in one process."""
        wanted = sorted({fn for fn in (self.function_of(a) for a in addresses)
                         if fn is not None and fn not in self._listing})
        orphans = sorted({a for a in addresses if self.function_of(a) is None})
        anchors = {}
        for va in orphans:
            anchor = self._padding_anchor(va)
            if anchor is not None:
                anchors[anchor] = max(anchors.get(anchor, 16), min((va - anchor) + 32, 4000))
        commands = ["aaa"] if (wanted or anchors) else []
        for fn in wanted:
            commands += [f"pdfj @ 0x{fn:x}"]
        for anchor, _count in sorted(anchors.items()):
            # No function covers the site: create one at the padding anchor so
            # Rizin analyses it honestly instead of drifting through a linear
            # sweep that desynchronises on embedded bytes.
            commands += [f"af @ 0x{anchor:x}", f"pdfj @ 0x{anchor:x}"]
        if not commands:
            return
        out = self._run(commands)
        decoder = json.JSONDecoder()
        i = 0
        while i < len(out):
            if out[i] not in "{[":
                i += 1
                continue
            try:
                data, end = decoder.raw_decode(out, i)
            except json.JSONDecodeError:
                i += 1
                continue
            items = data.get("ops", []) if isinstance(data, dict) else data
            try:
                for item in items:
                    self._listing[int(item["offset"])] = item.get("opcode", "")
            except (KeyError, TypeError, AttributeError):
                pass
            i = end

    def _padding_anchor(self, va: int, limit: int = 0x2000) -> int | None:
        """Start of the int3 padding run immediately preceding *va*, if any.

        Used only when Rizin has no function covering the address. A run of
        0xCC bytes is alignment padding, so the byte after it begins an
        instruction; decoding forward from there reaches (or refutes) the site.
        """
        if self.image is None:
            return None
        sec = self.image.section_of(va)
        if sec is None:
            return None
        end = min(va - sec.va, len(sec.data))
        start = max(0, end - limit)
        window = sec.data[start:end]
        idx = window.rfind(b"\xcc\xcc")
        if idx == -1:
            return None
        while idx + 1 < len(window) and window[idx + 1] == 0xCC:
            idx += 1
        anchor = sec.va + start + idx + 1
        return anchor if anchor < va else None

    def confirm_many(self, queries: list[tuple[int, int]]) -> dict[int, tuple[bool, str]]:
        """queries: (site_va, displacement). Returns site -> (ok, disassembly)."""
        self.load([q[0] for q in queries])
        results = {}
        for va, disp in queries:
            text = self._listing.get(va)
            if text is None:
                results[va] = (False, "not an instruction start")
            elif not re.search(rf"\+0x{disp:x}\]", text):
                # Require the closing bracket: a bare immediate that equals the
                # displacement is not a memory operand.
                results[va] = (False, f"operand not shown: {text}")
            else:
                results[va] = (True, text)
        return results

    def confirm(self, va: int, disp: int) -> tuple[bool, str]:
        return self.confirm_many([(va, disp)])[va]

    def confirm_calls(self, queries: list[tuple[int, int]]) -> dict[int, bool]:
        """queries: (call_site_va, callee_va)."""
        self.load([q[0] for q in queries])
        out = {}
        for site, callee in queries:
            text = self._listing.get(site, "")
            out[site] = text.startswith("call") and f"0x{callee:x}" in text
        return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", required=True)
    ap.add_argument("--disp", action="append", required=True,
                    help="hex displacement, e.g. 0x271 (repeatable)")
    ap.add_argument("--json")
    ap.add_argument("--validate", action="store_true",
                    help="keep only sites Rizin decodes as instruction starts")
    ap.add_argument("--rizin", default="rizin")
    ap.add_argument("--afl", help="reuse a saved 'aaa; afl' listing")
    args = ap.parse_args(argv)
    image = load_pe32(args.exe)
    out = {}
    for raw in args.disp:
        disp = int(raw, 16)
        hits = find_disp_xrefs(image, disp)
        if args.validate and hits:
            oracle = RizinOracle(args.exe, args.rizin, args.afl, image)
            verdicts = oracle.confirm_many([(h["site"], disp) for h in hits])
            kept = []
            for hit in hits:
                ok, text = verdicts[hit["site"]]
                if ok:
                    kept.append({**hit, "text": text})
                else:
                    print(f"   reject 0x{hit['site']:08x}: {text}")
            hits = kept
        out[raw] = hits
        print(f"disp 0x{disp:04x}: {len(hits)} confirmed site(s)")
        for h in hits:
            print(f"   0x{h['site']:08x}  {h['base']}+0x{disp:x}")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
