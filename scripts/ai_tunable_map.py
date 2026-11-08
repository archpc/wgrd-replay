#!/usr/bin/env python3
"""Extract NDF field tables from a Rizin listing.

Two modes, both fed a `rizin -c 'pd N @ <start>'` listing on stdin:

`--mode registry`
    Recovers `(offset, name)` pairs from a descriptor-registration block, whose
    shape is `push <offset> / push 0x0 / push str.<Name>`.

`--mode stores`
    Recovers field -> fixed-global mappings from the loader that copies a
    descriptor into process globals. Each value moves through a scratch
    register (`movzx eax, byte [edi+0x270]` ... `mov byte [0x020263a1], al`), so
    a store is paired with a load only when the register matches.

Bound the listing with --min-addr/--max-addr. Listings routinely run past the
end of the function they started in, and an unbounded parse silently picks up a
neighbouring descriptor's fields.

Evidence extraction only: nothing is loaded or executed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

LOAD = re.compile(
    r"\s*0x([0-9a-f]{8})\s+(movzx|movss|mov)\s+(\w+),\s*(?:byte|dword) \[edi\+(0x[0-9a-f]+)\]")
STORE = re.compile(
    r"\s*0x([0-9a-f]{8})\s+(?:mov|movss|movzx)\s+(?:byte|dword) \[(0x[0-9a-f]{6,8})\],\s*(\w+)")
PUSH = re.compile(r"\s*0x([0-9a-f]{8})\s+push\s+0x([0-9a-f]+)")
PUSH_ZERO = re.compile(r"\s*0x[0-9a-f]{8}\s+push\s+0x0+\b")
PUSH_NAME = re.compile(r"\s*0x[0-9a-f]{8}\s+push\s+str\.([A-Za-z0-9_]+)")

_ALIASES = {"al": "eax", "ax": "eax", "cl": "ecx", "dl": "edx", "bl": "ebx",
            "sil": "esi", "dil": "edi"}


def _canon(reg: str) -> str:
    r = reg.lower()
    return _ALIASES.get(r, r)


def _in_range(addr: int, lo: int | None, hi: int | None) -> bool:
    if lo is not None and addr < lo:
        return False
    if hi is not None and addr >= hi:
        return False
    return True


def parse_stores(lines, lo=None, hi=None) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {}
    pending: tuple[int, str, int] | None = None
    age = 0
    for line in lines:
        lm = LOAD.match(line)
        if lm:
            addr = int(lm.group(1), 16)
            if _in_range(addr, lo, hi):
                pending = (int(lm.group(4), 16), _canon(lm.group(3)), addr)
                age = 0
            continue
        age += 1
        sm = STORE.match(line)
        if sm and pending and age <= 6 and _canon(sm.group(3)) == pending[1]:
            out.setdefault(pending[0], []).append({
                "global": f"0x{int(sm.group(2), 16):08x}",
                "load_site": f"0x{pending[2]:08x}",
                "store_site": f"0x{int(sm.group(1), 16):08x}",
            })
            pending = None
    return out


def parse_registry(lines, lo=None, hi=None) -> dict[int, str]:
    out: dict[int, str] = {}
    lines = list(lines)
    for i, line in enumerate(lines):
        m = PUSH.match(line)
        if not m or not _in_range(int(m.group(1), 16), lo, hi):
            continue
        if i + 2 >= len(lines) or not PUSH_ZERO.match(lines[i + 1]):
            continue
        n = PUSH_NAME.match(lines[i + 2])
        if n:
            out[int(m.group(2), 16)] = n.group(1)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=("stores", "registry"), default="stores")
    ap.add_argument("--json")
    ap.add_argument("--min-addr", help="first instruction address to accept (hex)")
    ap.add_argument("--max-addr", help="exclusive upper bound (hex)")
    ap.add_argument("--only-offsets", help="JSON file whose keys are offsets to keep")
    ap.add_argument("--format", choices=("lines", "rizin-json"), default="lines",
                    help="input shape: rizin `pd` text or `pdfj` JSON")
    args = ap.parse_args(argv)

    lo = int(args.min_addr, 16) if args.min_addr else None
    hi = int(args.max_addr, 16) if args.max_addr else None
    raw = sys.stdin.read()
    if args.format == "rizin-json":
        # pdfj emits {"name":...,"ops":[{"offset":..,"opcode":..}, ...]}
        data = json.loads(raw)
        ops = data.get("ops", []) if isinstance(data, dict) else data
        # `disasm` keeps the symbolic operand (push str.Name); `opcode` does not.
        lines = [f" 0x{int(op['offset']):08x}  {op.get('disasm') or op.get('opcode', '')}\n"
                 for op in ops]
    else:
        lines = raw.splitlines(keepends=True)

    if args.mode == "registry":
        table = parse_registry(lines, lo, hi)
        print(f"registered fields: {len(table)}")
        for off, name in sorted(table.items()):
            print(f"  0x{off:04x}  {name}")
        if args.json:
            with open(args.json, "w") as fh:
                json.dump({f"0x{o:04x}": n for o, n in sorted(table.items())},
                          fh, indent=2)
        return 0

    stores = parse_stores(lines, lo, hi)
    if args.only_offsets:
        keep = {int(k, 16) for k in json.load(open(args.only_offsets))}
        stores = {o: v for o, v in stores.items() if o in keep}
    print(f"fields with runtime globals: {len(stores)}")
    for off, entries in sorted(stores.items()):
        for e in entries:
            print(f"  0x{off:04x} -> {e['global']}")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump({f"0x{o:04x}": v for o, v in sorted(stores.items())},
                      fh, indent=2, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
