#!/usr/bin/env python3
"""Check: opcode 0x18 DeactivateSupply obj+0x04 is a registry key in the same
reference space as opcode 0x07 GiveOrderStandard actor references.

For each build-59638 replay, every 0x18 single-command block's u32 at block[1:5]
must equal the leading u32 (registry key) of at least one 20-byte entry in some
0x07 obj_04_array. Also reports: slot agreement between the 0x18 issuer and the
slots that ordered that key, how many 0x18 rows precede the key's first 0x07
mention, and a chance-match baseline (fraction of the observed key span that is
covered by 0x07 keys, raised to the number of distinct 0x18 keys).

Usage:
    python3 -B research/op18_reference_keys.py REPLAY [REPLAY ...]

Exit 1 if any 0x18 key is absent from the 0x07 key set. Read-only.
"""
import collections
import glob
import os
from pathlib import Path
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import wgrd_replay as w  # noqa: E402


def analyse(path):
    rep = w.parse_replay(Path(path).read_bytes())
    rows18, keys07, slots07, first07 = [], set(), collections.defaultdict(set), {}
    for pact in rep["commands"]:
        bh = pact.get("block_hex")
        if bh and bh[:2] == "18" and pact.get("count") in (1, None):
            b = bytes.fromhex(bh)
            rows18.append((pact["frame"], pact["slot"], struct.unpack_from("<I", b, 1)[0]))
        for c in pact.get("command_decode", {}).get("commands", []):
            if c["opcode"] != 0x07:
                continue
            raw = bytes.fromhex(c["fields"]["obj_04_array"]["items_hex"])
            for i in range(0, len(raw), 20):
                k = struct.unpack_from("<I", raw, i)[0]
                keys07.add(k)
                slots07[k].add(pact["slot"])
                first07.setdefault(k, pact["frame"])
    keys18 = {k for _, _, k in rows18}
    missing = sorted(keys18 - keys07)
    same_slot = sum(1 for _, s, k in rows18 if slots07.get(k) == {s})
    before = sum(1 for f, _, k in rows18 if k in first07 and f < first07[k])
    span = (max(keys07) - min(keys07) + 1) if keys07 else 0
    chance = (len(keys07) / span) ** len(keys18) if span and keys18 else float("nan")
    return {"file": os.path.basename(path), "rows18": len(rows18), "distinct18": len(keys18),
            "keys07": len(keys07), "matched": len(keys18) - len(missing), "missing": missing,
            "same_slot_rows": same_slot, "rows_before_first_07": before,
            "key_span": span, "chance_all_match": chance}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    rc = 0
    for pattern in argv[1:]:
        for path in sorted(glob.glob(os.path.expanduser(pattern))):
            r = analyse(path)
            print("%(file)s: 0x18 rows=%(rows18)d distinct keys=%(distinct18)d matched in 0x07=%(matched)d "
                  "| 0x07 keys=%(keys07)d span=%(key_span)d | same-slot rows=%(same_slot_rows)d "
                  "| rows before first 0x07 mention=%(rows_before_first_07)d | chance all match=%(chance_all_match).2e" % r)
            if r["missing"]:
                print("  MISSING:", ["0x%08x" % k for k in r["missing"]])
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
