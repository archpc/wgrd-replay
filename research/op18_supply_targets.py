#!/usr/bin/env python3
"""Check: every 0x18 DeactivateSupply event resolves, via its registry key, to
exactly one 0x07 wire reference whose configured unit type is a supply unit.

Resolution rule (per replay): the key must match exactly one entity_references
catalog entry (lookup_key_ambiguous False) and the issuing player slot must be
among that entry's observed_player_slots. Temporal position relative to the
entry's 0x07 window is reported, not used as a gate.

Supply classification uses the NDF debug name token list below (static build
59638 unit data, research/unit-data/build59638-v1.json.gz). The baseline is the
share of all catalog candidates that match the same tokens.

Usage:
    python3 -B research/op18_supply_targets.py REPLAY [REPLAY ...]
Exit 1 if any 0x18 event fails to resolve uniquely, or if any resolved target's
unit-type candidates are not all supply units. Read-only.
"""
import collections
import glob
from pathlib import Path
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
import wgrd_replay as w          # noqa: E402
import wgrd_timeline as t        # noqa: E402
import wgrd_unit_data as ud      # noqa: E402

UNIT_DATA = os.path.join(ROOT, "research", "unit-data", "build59638-v1.json.gz")
SUPPLY_TOKENS = ("_log", "cargo", "kpi", "kolos", "kat1", "m35", "zil_130", "ural_4320",
                 "star_266", "supply", "ravit", "fob")


def is_supply(debug_name):
    n = debug_name.lower()
    return any(tok in n for tok in SUPPLY_TOKENS)


def analyse(path, unit_data):
    tl = t.build_timeline(w.parse_replay(Path(path).read_bytes()), unit_data)
    cat = tl["entity_references"]
    by_key = collections.defaultdict(list)
    for e in cat["entries"]:
        by_key[e["lookup_key_u32"]].append(e)
    res = {"file": os.path.basename(path), "events": 0, "unique": 0, "slot_ok": 0,
           "supply_all": 0, "type_unique": 0, "window": collections.Counter(),
           "names": collections.Counter(), "failures": []}
    for ev in tl["events"]:
        if ev["opcode"] != 0x18:
            continue
        res["events"] += 1
        key = ev["parameters"]["obj_04_u32"]
        cands = by_key.get(key, [])
        if len(cands) != 1 or cands[0]["lookup_key_ambiguous"]:
            res["failures"].append(("key", ev["frame"], ev["player_slot"], "0x%08x" % key, len(cands)))
            continue
        ref = cands[0]
        res["unique"] += 1
        if ev["player_slot"] not in ref["observed_player_slots"]:
            res["failures"].append(("slot", ev["frame"], ev["player_slot"], "0x%08x" % key, ref["observed_player_slots"]))
            continue
        res["slot_ok"] += 1
        f, l = ref["first_seen"]["frame"], ref["last_seen"]["frame"]
        res["window"]["before_first" if ev["frame"] < f else ("after_last" if ev["frame"] > l else "inside")] += 1
        cu = ref["configured_unit_types"]
        names = sorted({c["debug_name"] for c in cu["candidates"]})
        if cu["status"] == "unique":
            res["type_unique"] += 1
        res["names"][tuple(names)] += 1
        if names and all(is_supply(n) for n in names):
            res["supply_all"] += 1
        else:
            res["failures"].append(("type", ev["frame"], ev["player_slot"], "0x%08x" % key, names))
    all_c = [c["debug_name"] for e in cat["entries"] for c in e["configured_unit_types"]["candidates"]]
    res["baseline_supply_share"] = (sum(map(is_supply, all_c)) / len(all_c)) if all_c else float("nan")
    return res


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    unit_data = ud.load_unit_data(UNIT_DATA)
    rc = 0
    for pattern in argv[1:]:
        for path in sorted(glob.glob(os.path.expanduser(pattern))):
            r = analyse(path, unit_data)
            print("%s: 0x18 events=%d unique-key=%d slot-ok=%d type-unique=%d all-supply=%d | window=%s | baseline supply share=%.3f"
                  % (r["file"], r["events"], r["unique"], r["slot_ok"], r["type_unique"], r["supply_all"],
                     dict(r["window"]), r["baseline_supply_share"]))
            for names, n in r["names"].most_common():
                print("   %2d  %s" % (n, ", ".join(names)))
            for f in r["failures"][:10]:
                print("   FAIL", f)
            if r["failures"]:
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
