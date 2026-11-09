#!/usr/bin/env python3
"""Differential oracle for WGRD-CICS.

Reimplements the COBOL batch program in Python using the verified research
kernels:

* ``research/combat_damage.py``      -- float32 product and mode-2 clamp
* ``research/combat_damage_range.py`` -- gate and kinetic family index

The oracle is independent of the COBOL source: it re-parses the card deck and
the batch records from ``scripts/cics_spec.py`` and emits the same 72-byte
journal lines. Journal amount fields are IEEE-754 bit patterns, so equality is
bit equality, not decimal tolerance.
"""
import argparse
import sys
from decimal import Decimal, ROUND_DOWN
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for extra in (REPO / "research", REPO / "scripts"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

import cics_spec  # noqa: E402
import combat_damage  # noqa: E402
import combat_damage_range  # noqa: E402

RANGE_STEP = Decimal(13000)


class OracleError(Exception):
    pass


def load_cards(path):
    """Parse and validate the 80-column deck; return rows[f][a] float32."""
    lines = Path(path).read_text().splitlines()
    if not lines:
        raise OracleError("empty deck")
    header = lines[0].ljust(80)
    if header[0] != "H":
        raise OracleError("header card absent")
    if header[1:17].rstrip() != "ARME-ARMURE":
        raise OracleError("dataset name mismatch: %r" % header[1:17])
    if header[17:23] != "131544":
        raise OracleError("build mismatch")
    rows = int(header[23:26])
    cols = int(header[26:29])
    control = int(header[29:40])
    if (rows, cols) != (65, 35):
        raise OracleError("dimensions %d x %d" % (rows, cols))
    if not header[40:64].strip():
        raise OracleError("provenance tag absent")

    body = lines[1:]
    if len(body) != rows * 12:
        raise OracleError("card count %d, expected %d"
                          % (len(body), rows * 12))
    matrix = []
    for family in range(rows):
        row = []
        for sequence in range(1, 13):
            card = body[family * 12 + sequence - 1].ljust(80)
            if card[0] != "R":
                raise OracleError("row card type invalid")
            if int(card[1:4]) != family:
                raise OracleError("family sequence broken")
            if int(card[4:6]) != sequence:
                raise OracleError("sequence broken")
            count = 3 if sequence < 12 else 2
            for index in range(count):
                start = 6 + index * 24
                raw = card[start:start + 21]
                if not raw.isdigit():
                    raise OracleError("non-numeric cell")
                value = cics_spec.f32(float(Decimal(raw).scaleb(-18)))
                if not 0.0 <= value <= 1000.0:
                    raise OracleError("cell outside sanity band")
                row.append(value)
        if len(row) != cols:
            raise OracleError("row length %d" % len(row))
        matrix.append(row)
    if len(matrix) != rows:
        raise OracleError("row count")

    total = 0.0
    for row in matrix:
        for value in row:
            total += value
    if abs(round(total * 1000) - control) > 1:
        raise OracleError("control total differs: %.3f vs %d"
                          % (total, control))
    return matrix


def amount_text(amount):
    """COBOL MOVE of a binary32 to PIC 9(9).9(8) truncates."""
    value = Decimal(float(amount)).quantize(Decimal("0.00000001"),
                                            rounding=ROUND_DOWN)
    return "%018.8f" % value


def process(fields, matrix):
    """Return one journal record dict; ``fields`` is a decoded record."""
    record = {
        "type": "D",
        "id": fields["id"],
        "status": "OK",
        "code": "0000",
        "family": "---",
        "armor": "---",
        "amt_bits": "--------",
        "applied_bits": "--------",
        "cur_bits": "--------",
        "amt_text": "000000000.00000000",
    }

    def reject(code, kind):
        record["type"] = "R"
        record["status"] = "RJ"
        record["code"] = code
        return record, kind

    mode = fields["mode_value"]
    if mode not in (1, 2):
        return reject("R002", None)
    for name in ("h", "p", "k", "c", "f", "dist", "r_bateaux", "r_max",
                 "r_tba", "r_ha", "r_proj"):
        if fields[name + "_value"] is None:
            return reject("R005", None)
    for name in ("maxhp", "curhp"):
        if fields[name + "_value"] is None:
            return reject("R007", None)

    h = cics_spec.f32(float(fields["h_value"]))
    p = cics_spec.f32(float(fields["p_value"]))
    k = cics_spec.f32(float(fields["k_value"]))
    c = cics_spec.f32(float(fields["c_value"]))
    f = cics_spec.f32(float(fields["f_value"]))
    distance = cics_spec.f32(float(fields["dist_value"]))
    max_hp = cics_spec.f32(float(fields["maxhp_value"]))
    cur_hp = cics_spec.f32(float(fields["curhp_value"]))
    armor = int(fields["armor"] or 0)
    arme = int(fields["arme"] or 0)
    proj = int(fields["proj"] or 0)
    eff = int(fields["eff"] or 0)

    gate = (proj == 0 and 5 <= arme <= 64 and eff != 0)
    if gate:
        target_class = int(fields["tclass"] or 0)
        names = {1: "r_bateaux", 2: "r_max", 3: "r_tba", 4: "r_tba",
                 5: "r_ha", 6: "r_proj"}
        if target_class not in names:
            return reject("R006", None)
        rmax = cics_spec.f32(float(fields[names[target_class] + "_value"]))
        if rmax == 0.0:
            return reject("R004", None)
        family = combat_damage_range.kinetic_family_index(
            arme, rmax, distance)
    else:
        family = int(fields["family"])

    if family > 64:
        return reject("R003", None)
    if armor > 34:
        return reject("R008", None)

    t = matrix[family][armor]
    amount = combat_damage.damage_amount(h, p, t, k, c, f)
    record["family"] = "%03d" % family
    record["armor"] = "%03d" % armor
    record["amt_bits"] = cics_spec.bits(amount)
    record["amt_text"] = amount_text(amount)

    new_hp = None
    if mode == 2:
        applied, new_hp = combat_damage.apply_mode2(amount, max_hp, cur_hp)
        record["applied_bits"] = cics_spec.bits(applied)
        record["cur_bits"] = cics_spec.bits(new_hp)
    return record, amount


def run(table_path, batch_path):
    """Return (journal lines, accepted, rejected, amount total bits)."""
    matrix = load_cards(table_path)
    lines = []
    accepted = 0
    rejected = 0
    total = cics_spec.f32(0.0)
    for raw in Path(batch_path).read_text().splitlines():
        fields = cics_spec.decode(raw)
        kind = fields["type"]
        if kind == "Z":
            continue
        if kind != "D":
            fields["id"] = fields["id"]
            record = {
                "type": "R", "id": fields["id"], "status": "RJ",
                "code": "R001", "family": "---", "armor": "---",
                "amt_bits": "--------", "applied_bits": "--------",
                "cur_bits": "--------", "amt_text": "000000000.00000000",
            }
            lines.append(cics_spec.journal_line(record))
            rejected += 1
            continue
        record, amount = process(fields, matrix)
        lines.append(cics_spec.journal_line(record))
        if record["status"] == "OK":
            accepted += 1
            total = cics_spec.f32(total + amount)
        else:
            rejected += 1
    trailer = [" "] * cics_spec.JOURNAL_LEN
    trailer[0] = "T"
    trailer[1:8] = "%07d" % accepted
    trailer[8:15] = "%07d" % rejected
    trailer[15:23] = cics_spec.bits(total)
    lines.append("".join(trailer).rstrip())
    return lines, accepted, rejected, cics_spec.bits(total)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--journal", required=True)
    args = parser.parse_args(argv)
    lines, accepted, rejected, total = run(args.table, args.batch)
    Path(args.journal).write_text("\n".join(lines) + ("\n" if lines else ""),
                                  newline="\n")
    print("ACCEPTED %d REJECTED %d TOTAL %s" % (accepted, rejected, total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
