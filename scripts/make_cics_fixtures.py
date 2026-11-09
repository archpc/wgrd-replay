#!/usr/bin/env python3
"""Build the deterministic WGRD-CICS sample batch and randomized batches.

The sample deck exercises every accepted path and every reject code. It uses no
game-specific weapon identity: inputs are the explicit kernel terms recovered
from build 131544 plus range-gate fields.
"""
import argparse
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

import cics_spec  # noqa: E402


def base(index, **overrides):
    values = {
        "id": "TX%08d" % index,
        "mode": 2,
        "h": 0.85,
        "p": 28.0,
        "k": 1.5,
        "c": 1.0,
        "f": 1.0,
        "armor": 8,
        "family": 8,
        "proj": 1,
        "arme": 8,
        "eff": 0,
        "tclass": 2,
        "dist": 1000.0,
        "r_bateaux": 0.0,
        "r_max": 0.0,
        "r_tba": 0.0,
        "r_ha": 0.0,
        "r_proj": 0.0,
        "maxhp": 10.0,
        "curhp": 0.0,
    }
    values.update(overrides)
    return values


def sample_records():
    """Deterministic sample: accepted paths first, then one of each reject."""
    records = [
        base(1, maxhp=10.0, curhp=0.0),
        base(2, h=0.5, p=4.0, k=1.0, armor=5, family=8,
             maxhp=100.0, curhp=90.0),
        base(3, mode=1, h=1.0, p=10.0, k=1.0, armor=3, family=24),
        base(4, h=1.0, p=10.0, k=1.0, armor=3, family=0,
             proj=0, arme=8, eff=1, tclass=2, dist=1000.0,
             r_max=156000.0, maxhp=10.0, curhp=0.0),
        base(5, h=1.0, p=10.0, k=1.0, armor=3, family=0,
             proj=0, arme=60, eff=1, tclass=6, dist=26000.0,
             r_proj=104000.0, maxhp=10.0, curhp=0.0),
        base(6, mode=7),
        base(7, family=99, proj=1),
        base(8, armor=40, proj=1),
        base(9, proj=0, arme=8, eff=1, tclass=5, r_ha=0.0, family=0),
        base(10, proj=0, arme=8, eff=1, tclass=0, family=0,
             r_max=1000.0),
        base(11, mode=1, h=1.0, p=10.0, k=1.0, armor=4, family=24,
             proj=0, arme=8, eff=1, tclass=2, dist=1000.0,
             r_max=156000.0),
    ]
    return records


def write_batch(path, records, tamper=None):
    lines = [cics_spec.encode_detail(record) for record in records]
    if tamper:
        lines = tamper(lines)
    lines.append(cics_spec.encode_control(len(records)))
    Path(path).write_text("\n".join(lines) + "\n", newline="\n")


def random_records(count, seed):
    rng = random.Random(seed)
    out = []
    for index in range(count):
        mode = rng.choice((1, 2, 2))
        gate = rng.random() < 0.45
        values = base(index + 1)
        values["mode"] = mode
        values["h"] = rng.choice((0.5, 0.85, 0.9125, 1.0, 1.3375,
                                  2.0, 3.1415, 0.0001))
        values["p"] = rng.choice((1.0, 4.0, 10.0, 28.0, 37.5, 100.0))
        values["k"] = rng.choice((1.0, 1.5, 0.75, 2.0))
        values["c"] = rng.choice((0.5, 1.0, 0.25))
        values["f"] = rng.choice((1.0, 0.5, 0.125, 0.875))
        values["armor"] = rng.randint(0, 34)
        values["proj"] = 0 if gate else 1
        values["eff"] = 1 if gate else 0
        values["arme"] = rng.randint(5, 64) if gate else rng.randint(0, 64)
        values["family"] = rng.randint(0, 64)
        values["tclass"] = rng.choice((1, 2, 3, 4, 5, 6))
        values["dist"] = rng.choice((0.0, 500.0, 1000.0, 6500.0, 13000.0,
                                     26000.0, 26001.0, 99999.5))
        for name in ("r_bateaux", "r_max", "r_tba", "r_ha", "r_proj"):
            values[name] = rng.choice((0.0, 104000.0, 156000.0, 260000.0))
        values["maxhp"] = rng.choice((10.0, 20.0, 100.0, 800.0))
        values["curhp"] = rng.choice((0.0, 5.0, 10.0, 90.0,
                                      values["maxhp"] - 0.5))
        out.append(values)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--count", type=int, default=0)
    parser.add_argument("--seed", type=int, default=131544)
    args = parser.parse_args(argv)
    if args.sample:
        records = sample_records()
    else:
        records = random_records(args.count, args.seed)
    write_batch(args.out, records)
    print("records=%d %s" % (len(records), args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
