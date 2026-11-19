#!/usr/bin/env python3
"""Emit 80-column card images for the 65x35 Arme/Armure damage table.

The COBOL loader (WGRDCICS) reads only this deck. Two modes exist:

* ``--private`` reads the hash-pinned extraction with the verified Python
  adapter (``research/combat_damage_table.py``) and writes the real matrix.
* ``--synthetic`` writes a deterministic, clearly labelled matrix for tests and
  for the committed sample run. It is not game data.

Card format (80 columns, uppercase, fixed width)::

    H<name:16><build:6><rows:3><cols:3><sum:26><tag:24><filler:1>
    R<family:3><seq:2>[<value:21><filler:3>]x3<filler:2>

Values are transported as 21-digit implied-decimal integers, 18 decimal
places, zero filled. Every transport integer is derived with Decimal arithmetic
from the exact binary32 value, so the COBOL ``MOVE`` reconstructs the same
float32 bit pattern with no rounding. The header sum is the double-precision
sum of the padded matrix in row-major order, and the COBOL loader recomputes it.
"""
import argparse
import hashlib
import sys
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "research"
if str(RESEARCH) not in sys.path:
    sys.path.insert(0, str(RESEARCH))

import combat_damage_table  # noqa: E402

DECIMALS = 18
SCALE = 10 ** DECIMALS
FAMILIES = 65
COLUMNS = 35
NAME = "ARME-ARMURE"
BUILD = "131544"


def transport(value):
    """Return the 21-digit implied-decimal integer for an exact float32."""
    scaled = Decimal(repr(value)) * SCALE
    assert scaled == scaled.to_integral_value(), value
    digits = int(scaled)
    assert 0 <= digits < 10 ** 21, digits
    return "%021d" % digits


def header(rows, columns, total, tag):
    thousandths = "%011d" % int(round(total * 1000.0))
    line = ("H" + NAME.ljust(16) + BUILD + "%03d" % rows + "%03d" % columns
            + thousandths + tag.ljust(24) + " " * 16)
    return line.ljust(80)


def card_rows(matrix):
    for family, row in enumerate(matrix):
        assert len(row) == COLUMNS
        chunks = [row[index:index + 3] for index in range(0, COLUMNS, 3)]
        # 35 columns = 11 full cards of 3 plus one card of 2.
        for sequence, chunk in enumerate(chunks, start=1):
            body = "R" + "%03d" % family + "%02d" % sequence
            for value in chunk:
                body += transport(value) + "   "
            yield body.ljust(80)


def padded(matrix):
    return [tuple(row[index] if index < len(row) else 0.0
                  for index in range(COLUMNS)) for row in matrix]


def private_matrix(path):
    table = combat_damage_table.load_arme_armure_table(path)
    return [list(row) for row in table.rows], "PRIVATE-131544"


def synthetic_matrix():
    # Deterministic, exactly representable, not game data: zero in columns
    # 0..2, then (family*0.25 + column*0.5) capped at 60.0, zero tail.
    matrix = []
    for family in range(FAMILIES):
        row = []
        for column in range(COLUMNS):
            if column < 3 or column > 29:
                row.append(0.0)
            else:
                row.append(min(60.0, family * 0.25 + column * 0.5))
        matrix.append(row)
    return matrix, "SYNTHETIC-NOT-GAMEDATA"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--private", metavar="JSON",
                        help="hash-pinned arme-armure-table.json")
    source.add_argument("--synthetic", action="store_true",
                        help="write the labelled synthetic deck")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    label = "SYNTHETIC-NOT-GAMEDATA"
    if args.synthetic:
        matrix, label = synthetic_matrix()
    else:
        matrix, label = private_matrix(args.private)
    matrix = padded(matrix)

    total = 0.0
    for row in matrix:
        for value in row:
            total += value

    lines = [header(FAMILIES, COLUMNS, total, label)]
    lines.extend(card_rows(matrix))
    payload = "\n".join(lines) + "\n"
    Path(args.out).write_text(payload, newline="\n")

    print("cards=%d values=%d sum=%.17g tag=%s sha256=%s"
          % (len(lines), FAMILIES * COLUMNS, total, label,
             hashlib.sha256(payload.encode()).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
