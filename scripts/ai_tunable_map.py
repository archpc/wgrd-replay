#!/usr/bin/env python3
"""Parse a Rizin listing of the tunables loader into a field -> global map.

Input is `rizin -e scr.color=0 -c 'pd N @ <start>' WarGame3.exe` on stdout.
The loader moves each NDF field into a fixed global through a scratch register
(`movzx eax, byte [edi+0x270]` then `mov byte [0x020263a1], al`), so the
mapping is recovered by pairing the load with the following store.

This is evidence extraction, not execution: nothing is loaded or run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

LOAD = re.compile(r"\s*0x([0-9a-f]{8})\s+(movzx|movss|mov)\s+\w+,\s*(?:byte|dword) \[edi\+(0x[0-9a-f]+)\]")
STORE = re.compile(r"\s*0x([0-9a-f]{8})\s+(?:mov|movss|movzx)\s+(byte|dword) \[(0x[0-9a-f]{6,8})\],\s*(\w+)")


def parse(lines) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {}
    pending: tuple[int, int, str] | None = None
    age = 0
    for line in lines:
        lm = LOAD.match(line)
        if lm:
            pending = (int(lm.group(3), 16), int(lm.group(1), 16), lm.group(2))
            age = 0
            continue
        age += 1
        sm = STORE.match(line)
        if sm and pending and age <= 3:
            out.setdefault(pending[0], []).append({
                "global": f"0x{int(sm.group(3), 16):08x}",
                "width": sm.group(2),
                "load_site": f"0x{pending[1]:08x}",
                "store_site": f"0x{int(sm.group(1), 16):08x}",
            })
            pending = None
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", help="write the map here")
    args = ap.parse_args(argv)
    mapping = parse(sys.stdin)
    payload = {f"0x{off:04x}": v for off, v in sorted(mapping.items())}
    print(f"fields with runtime globals: {len(payload)}")
    for off, entries in sorted(mapping.items()):
        for e in entries:
            print(f"  0x{off:04x} -> {e['global']} ({e['width']})")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
