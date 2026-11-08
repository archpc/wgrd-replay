#!/usr/bin/env python3
"""Attribute addresses to functions, RTTI vtable owners, and callers.

Consumes two artifacts produced once per binary:
  * `rizin -c 'aaa; afl'` function list
  * scripts/ai_rtti.py --slot-map JSON (vtable slot VA -> Class[slot])

Then answers, for an address of interest: which function contains it, whether
that function overrides a virtual, and which functions call it (with the same
attribution), so a static report can name a code path without a PDB.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import struct
import sys

from ai_rtti import load_pe32


def load_functions(path: str) -> list[tuple[int, int, str]]:
    rows = []
    with open(path) as fh:
        for line in fh:
            m = re.match(r"0x([0-9a-f]+)\s+\d+\s+(\d+)\s+(\S+)", line)
            if m:
                va, size, name = int(m.group(1), 16), int(m.group(2)), m.group(3)
                rows.append((va, va + size, name))
    rows.sort()
    return rows


class Attributor:
    def __init__(self, funcs, slot_map: dict[str, list[str]]):
        self.starts = [f[0] for f in funcs]
        self.funcs = funcs
        self.owner = {int(k, 16): v for k, v in slot_map.items()}

    def func_at(self, va: int) -> tuple[int, int, str] | None:
        i = bisect.bisect_right(self.starts, va) - 1
        if i < 0:
            return None
        f = self.funcs[i]
        return f if f[0] <= va < f[1] else None

    def name(self, start: int) -> str:
        owners = self.owner.get(start)
        return f"{owners[0]}" if owners else "-"

    def callers(self, image, target: int) -> list[int]:
        """Call sites reaching *target* via rel32 (e8) or jump tables (ff /2)."""
        hits = []
        for s in image.sections:
            if not s.executable:
                continue
            data = s.data
            for i in range(len(data) - 5):
                if data[i] == 0xE8:
                    rel = struct.unpack_from("<i", data, i + 1)[0]
                    if s.va + i + 5 + rel == target:
                        hits.append(s.va + i)
        return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", required=True)
    ap.add_argument("--afl", required=True)
    ap.add_argument("--slotmap", required=True)
    ap.add_argument("--va", action="append", required=True)
    ap.add_argument("--max-callers", type=int, default=12)
    args = ap.parse_args(argv)

    image = load_pe32(args.exe)
    funcs = load_functions(args.afl)
    slot_map = json.load(open(args.slotmap))["slot_map"]
    at = Attributor(funcs, slot_map)
    print(f"functions={len(funcs)} named_slots={len(slot_map)}")
    for raw in args.va:
        va = int(raw, 16)
        f = at.func_at(va)
        print(f"\n0x{va:08x}")
        if not f:
            print("  not inside a detected function")
            continue
        print(f"  func 0x{f[0]:08x}-0x{f[1]:08x} size={f[1]-f[0]} vtable_owner={at.name(f[0])}")
        calls = at.callers(image, f[0])
        print(f"  callers={len(calls)}")
        for site in calls[: args.max_callers]:
            cf = at.func_at(site)
            label = at.name(cf[0]) if cf else "?"
            print(f"    0x{site:08x} in 0x{cf[0]:08x} {label}" if cf else f"    0x{site:08x} (no func)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
