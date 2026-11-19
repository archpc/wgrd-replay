"""Tests for WGRD-CICS (GnuCOBOL 131544 damage accounting).

Evidence classes stay separate:

* SYNTHETIC decks and batches test mechanics. The committed 65x35 deck is
  labelled ``SYNTHETIC-NOT-GAMEDATA`` and is not game data.
* ENGINE OBSERVATIONS are the hash-pinned private table and the verified
  research kernels imported by the oracle. Tests that need the private table
  skip explicitly when it is absent.

The differential test compares the 72-byte journal byte for byte, including
IEEE-754 binary32 bit patterns, so agreement is bit equality.
"""
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for extra in (REPO / "scripts", REPO / "research"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

import cics_oracle  # noqa: E402
import cics_spec  # noqa: E402
import combat_damage_range  # noqa: E402
import combat_damage_table  # noqa: E402
import make_cics_fixtures  # noqa: E402

COBC = shutil.which("cobc") or ""
SOURCE = REPO / "src/cobol/WGRDCICS.cob"
SYNTHETIC = REPO / "samples/cics/synthetic-table.cards"
SAMPLE = REPO / "samples/cics/sample-batch.dat"
SAMPLE_REPORT = REPO / "samples/cics/sample-report.txt"
PRIVATE_JSON = Path(os.environ.get(
    "WGRD_ARME_ARMURE_TABLE",
    Path.home() / ".hermes/artifacts/wgrd-replay"
    "/combat-damage-static-20261109/arme-armure-table.json"))
WORK = Path(tempfile.mkdtemp(prefix="wgrd-cics-test-"))
BINARY = WORK / "wgrdcics"

PYTHON = sys.executable or "python3"

_F32 = struct.Struct("<f")


DETAIL_RE = re.compile(
    r"^ (?P<id>\S+) +MODE (?P<mode>[12])  FAM +(?P<family>\d+)"
    r"  ARM +(?P<armor>\d+)  AMOUNT +(?P<amount>\d+\.\d+)$")
REJECT_RE = re.compile(r"^ (?P<id>\S+) +(?P<code>R\d{3})  ")
CLAIM_RE = re.compile(
    r"^\s+CLAIM APPLIED +(?P<applied>-?\s*\d+\.\d+)"
    r"  HP REGISTER NOW +(?P<hp>-?\s*\d+\.\d+)"
    r"  CHARGE TO ACCOUNTS PAYABLE$")


def parse_report(report):
    """Return (records, pages) from a printed register.

    ``records`` preserves transaction order; each entry carries the id, kind,
    printed amount and, for mode 2, the printed applied and new-HP fields.
    ``pages`` counts page headings, so a lost line at a page break shows up as a
    missing id rather than a silent gap.
    """
    records = []
    pages = 0
    for raw in report.splitlines():
        line = raw.replace("\f", "")
        if "PAGE " in line and "BUILD 131544" in line:
            pages += 1
            continue
        match = DETAIL_RE.match(line)
        if match:
            records.append({
                "id": match.group("id"),
                "kind": "D",
                "mode": int(match.group("mode")),
                "family": int(match.group("family")),
                "armor": int(match.group("armor")),
                "amount": match.group("amount"),
                "applied": None,
                "hp": None,
            })
            continue
        match = REJECT_RE.match(line)
        if match:
            records.append({
                "id": match.group("id"),
                "kind": "R",
                "code": match.group("code"),
                "amount": None,
                "applied": None,
                "hp": None,
            })
            continue
        match = CLAIM_RE.match(line)
        if match:
            if not records or records[-1]["kind"] != "D":
                raise AssertionError("orphan claim line: " + raw)
            if records[-1]["applied"] is not None:
                raise AssertionError("duplicate claim line: " + raw)
            records[-1]["applied"] = match.group("applied").replace(" ", "")
            records[-1]["hp"] = match.group("hp").replace(" ", "")
    return records, pages


def truncate(text, places):
    """Journal text truncates at its stored precision."""
    return Decimal(text).quantize(Decimal(1).scaleb(-places),
                                  rounding=ROUND_DOWN)


def round_display(value, places):
    """COBOL ``COMPUTE ... ROUNDED`` rounds half away from zero."""
    dec = value if isinstance(value, Decimal) else Decimal(repr(value))
    return dec.quantize(Decimal(1).scaleb(-places),
                        rounding=ROUND_HALF_UP)


def f32(value):
    return _F32.unpack(_F32.pack(value))[0]


def run_program(table, batch, env_extra=None):
    journal = WORK / "journal.txt"
    report = WORK / "report.txt"
    for path in (journal, report):
        if path.exists():
            path.unlink()
    env = os.environ.copy()
    env.update({
        "WGRD_CICS_TABLE": str(table),
        "WGRD_CICS_BATCH": str(batch),
        "WGRD_CICS_JOURNAL": str(journal),
        "WGRD_CICS_REPORT": str(report),
    })
    if env_extra:
        env.update(env_extra)
    done = subprocess.run([str(BINARY)], env=env, capture_output=True,
                          text=True)
    return (done.returncode,
            journal.read_text() if journal.exists() else "",
            report.read_text() if report.exists() else "",
            done.stdout + done.stderr)


def write_batch(path, records, tamper=None):
    lines = [cics_spec.encode_detail(record) for record in records]
    if tamper:
        lines = tamper(lines)
    lines.append(cics_spec.encode_control(len(records)))
    Path(path).write_text("\n".join(lines) + "\n")


def private_table_available():
    return PRIVATE_JSON.is_file()


class TestRecordSpecification(unittest.TestCase):
    """SYNTHETIC: the one authoritative layout."""

    def test_batch_fields_are_contiguous_and_inside_the_record(self):
        cursor = 0
        for name, start, length, _ in cics_spec.BATCH_FIELDS:
            self.assertEqual(start - 1, cursor, name)
            cursor += length
        self.assertLessEqual(cursor, cics_spec.BATCH_LEN)
        self.assertEqual(len(set(field[0] for field in cics_spec.BATCH_FIELDS)),
                         len(cics_spec.BATCH_FIELDS))

    def test_journal_fields_are_contiguous(self):
        cursor = 0
        for name, start, length in cics_spec.JOURNAL_FIELDS:
            self.assertEqual(start - 1, cursor, name)
            cursor += length
        self.assertLessEqual(cursor, cics_spec.JOURNAL_LEN)

    def test_raw_engine_distance_survives_transport(self):
        values = make_cics_fixtures.base(1)
        values["dist"] = 169000.0
        line = cics_spec.encode_detail(values)
        self.assertEqual(len(line), cics_spec.BATCH_LEN)
        decoded = cics_spec.decode(line)
        self.assertEqual(float(decoded["dist_value"]), 169000.0)

    def test_encode_decode_roundtrip(self):
        record = make_cics_fixtures.base(1)
        line = cics_spec.encode_detail(record)
        self.assertEqual(len(line), cics_spec.BATCH_LEN)
        decoded = cics_spec.decode(line)
        self.assertEqual(decoded["id"], record["id"])
        self.assertEqual(float(decoded["h_value"]), record["h"])


class TestSampleFixtureProvenance(unittest.TestCase):
    """SYNTHETIC: the committed sample pair must match builder and spec.

    cceb664 widened the distance field without regenerating samples/cics.
    The COBOL/oracle differential stayed self-consistent under either layout
    while the committed report drifted, so these pins fail on any future
    spec change that forgets the fixtures. No cobc required.
    """

    def test_committed_batch_is_exactly_the_builder_output(self):
        records = make_cics_fixtures.sample_records()
        lines = [cics_spec.encode_detail(record) for record in records]
        lines.append(cics_spec.encode_control(len(records)))
        self.assertEqual(SAMPLE.read_text(), "\n".join(lines) + "\n")

    def test_tx5_scenario_reaches_the_family_cap(self):
        # TX5 must exercise the CAPPED range-gate path: arme 60 plus 6
        # range steps overshoots HIGH_CAP, so family 64 proves the cap was
        # applied, not a below-cap result or the family floor.
        line = [raw for raw in SAMPLE.read_text().splitlines()
                if raw[1:11] == "TX00000005"][0]
        decoded = cics_spec.decode(line)
        self.assertEqual(float(decoded["dist_value"]), 26000.0)
        self.assertEqual(float(decoded["r_proj_value"]), 104000.0)
        self.assertEqual(int(decoded["arme_value"]), 60)
        self.assertEqual(int(decoded["eff_value"]), 1)
        self.assertEqual(int(decoded["tclass_value"]), 6)
        self.assertTrue(combat_damage_range.range_family_applies(
            int(decoded["proj_value"]), int(decoded["arme_value"]),
            int(decoded["eff_value"])))
        rmax = float(decoded["r_proj_value"])
        dist = float(decoded["dist_value"])
        arme = int(decoded["arme_value"])
        remaining = f32(f32(rmax) - f32(dist))
        steps = math.trunc(f32(remaining
                               / f32(combat_damage_range.RANGE_STEP)))
        self.assertEqual(steps, 6)
        self.assertGreater(arme + steps, combat_damage_range.HIGH_CAP)
        self.assertEqual(
            combat_damage_range.kinetic_family_index(arme, rmax, dist), 64)
        expected, accepted, rejected, _ = cics_oracle.run(SYNTHETIC, SAMPLE)
        self.assertEqual((accepted, rejected), (6, 5))
        tx5 = [row for row in expected if row[1:11] == "TX00000005"][0]
        self.assertEqual(tx5[17:20], "064")
        matrix = cics_oracle.load_cards(SYNTHETIC)
        self.assertEqual(matrix[64][3], 17.5)
        # H=K=C=F=1, P=10: amount = 10 * T[64][3] = 175.0, exact in binary32.
        self.assertEqual(tx5[23:31], cics_spec.bits(f32(10.0 * 17.5)))


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestCompileAndSample(unittest.TestCase):
    """ACCEPTANCE: real build, sample batch, multi-page report."""

    @classmethod
    def setUpClass(cls):
        done = subprocess.run(
            [COBC, "-x", "-fixed", "-std=default", "-o", str(BINARY),
             str(SOURCE)], capture_output=True, text=True)
        if done.returncode != 0:
            raise AssertionError("compile failed:\n" + done.stdout
                                 + done.stderr)

    def test_compiles_without_errors(self):
        self.assertTrue(BINARY.is_file())

    def test_sample_journal_is_bit_identical_to_the_oracle(self):
        code, journal, _, _ = run_program(SYNTHETIC, SAMPLE)
        self.assertEqual(code, 0)
        expected, accepted, rejected, _ = cics_oracle.run(SYNTHETIC, SAMPLE)
        self.assertEqual(journal.splitlines(), expected)
        self.assertEqual((accepted, rejected), (6, 5))

    def test_committed_report_matches_actual_run(self):
        # The report is deterministic (RUN DATE is fixed in the source), so
        # the committed register is pinned byte for byte. A stale fixture or
        # a rendering drift fails here instead of passing the differential.
        code, _, report, output = run_program(SYNTHETIC, SAMPLE)
        self.assertEqual(code, 0, output)
        self.assertEqual(report, SAMPLE_REPORT.read_text())

    def test_tx5_journal_family_is_capped_at_64(self):
        code, journal, _, output = run_program(SYNTHETIC, SAMPLE)
        self.assertEqual(code, 0, output)
        tx5 = [row for row in journal.splitlines()
               if row[1:11] == "TX00000005"][0]
        self.assertEqual(tx5[17:20], "064")
        self.assertEqual(tx5[23:31], cics_spec.bits(175.0))

    def test_report_is_multipage_and_reconciled(self):
        _, _, report, _ = run_program(SYNTHETIC, SAMPLE)
        pages = [line for line in report.splitlines() if line.startswith("\f")]
        self.assertGreaterEqual(report.count("PAGE 000"), 2)
        self.assertIn("PAGE 0002", report)
        self.assertIn("CONTROL CARD COUNT AGREES WITH REGISTER", report)
        self.assertIn("ARMOR LOSS NOT RECOGNIZED UNTIL FORM DD-131544 IS",
                      report)
        for line in report.splitlines():
            self.assertLessEqual(len(line.replace("\f", "")), 133)
        self.assertTrue(pages or report.startswith("\f"))

    def test_every_reject_code_in_the_sample_has_a_register_row(self):
        _, _, report, _ = run_program(SYNTHETIC, SAMPLE)
        for code in ("R002", "R003", "R004", "R006", "R008"):
            self.assertIn(code, report)

    def test_report_paginates_a_long_register(self):
        records = make_cics_fixtures.random_records(180, seed=4242)
        batch = WORK / "long.dat"
        write_batch(batch, records)
        code, _, report, _ = run_program(SYNTHETIC, batch)
        self.assertEqual(code, 0)
        self.assertIn("PAGE 0002", report)
        self.assertIn("PAGE 0003", report)
        headings = report.count("DEPARTMENT OF DEFENSE")
        self.assertEqual(headings, report.count("PAGE "))
        self.assertGreaterEqual(headings, 3)


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestReportJournalCrossCheck(unittest.TestCase):
    """ACCEPTANCE: every printed transaction matches the journal.

    The report is a separate rendering path from the journal, and an earlier
    defect dropped the pending detail line when a page break intervened. These
    tests walk page boundaries on purpose and require each journal transaction
    to appear exactly once, with the same amount and clamp figures.
    """

    @classmethod
    def setUpClass(cls):
        if not BINARY.is_file():
            subprocess.run([COBC, "-x", "-fixed", "-std=default", "-o",
                            str(BINARY), str(SOURCE)], check=True,
                           capture_output=True)
        cls.cross_checked = 0

    def cross_check(self, table, batch, label):
        code, journal, report, output = run_program(table, batch)
        self.assertEqual(code, 0, output)
        records, pages = parse_report(report)
        journal_lines = [line for line in journal.splitlines()
                         if not line.startswith("T")]
        self.assertEqual(len(records), len(journal_lines), label)
        self.assertGreaterEqual(pages, 1, label)
        self.assertGreater(len(records), 0, label)
        self.assertEqual(pages,
                         report.count("BUILD 131544   PAGE "), label)
        for entry, line in zip(records, journal_lines):
            self.assertEqual(entry["id"], line[1:11], label)
            status = line[11:13]
            code_field = line[13:17]
            if status == "OK":
                self.assertEqual(entry["kind"], "D", label)
                self.assertEqual(code_field, "0000", label)
                self.assertEqual(entry["family"], int(line[17:20]), label)
                self.assertEqual(entry["armor"], int(line[20:23]), label)
                amount_bits = struct.unpack(
                    "<f", struct.pack("<I", int(line[23:31], 16)))[0]
                self.assertEqual(Decimal(entry["amount"]),
                                 round_display(amount_bits, 4),
                                 label + " " + entry["id"])
                if line[31:39] != "--------":
                    self.assertEqual(entry["mode"], 2, label)
                    self.assertIsNotNone(entry["applied"], label)
                    applied = struct.unpack(
                        "<f", struct.pack("<I", int(line[31:39], 16)))[0]
                    new_hp = struct.unpack(
                        "<f", struct.pack("<I", int(line[39:47], 16)))[0]
                    self.assertEqual(Decimal(entry["applied"]),
                                     round_display(applied, 4),
                                     label + " " + entry["id"])
                    self.assertEqual(Decimal(entry["hp"]),
                                     round_display(new_hp, 3),
                                     label + " " + entry["id"])
                else:
                    self.assertEqual(entry["mode"], 1, label)
                    self.assertIsNone(entry["applied"], label)
            else:
                self.assertEqual(entry["kind"], "R", label)
                self.assertEqual(entry["code"], code_field, label)
                self.assertIsNone(entry["amount"], label)
                self.assertIsNone(entry["applied"], label)
            self.cross_checked += 1

    def test_sample_report_matches_journal(self):
        self.cross_check(SYNTHETIC, SAMPLE, "sample")

    def test_long_register_matches_journal(self):
        records = make_cics_fixtures.random_records(180, seed=4242)
        batch = WORK / "cross-long.dat"
        write_batch(batch, records)
        self.cross_check(SYNTHETIC, batch, "long")

    def test_every_pagination_boundary_keeps_its_transaction(self):
        # A mode-2 claim is a second printed line, so a detail can land on the
        # last line of a page at many alignments; each must survive the break.
        for count in range(1, 47):
            values_list = []
            for index in range(count):
                values = make_cics_fixtures.base(index)
                values.update({"mode": 2, "h": 1.0, "p": 1.0, "k": 1.0,
                               "c": 1.0, "f": 1.0, "proj": 1,
                               "family": 8, "armor": 8,
                               "maxhp": 10.0, "curhp": 0.0})
                values_list.append(values)
            batch = WORK / ("boundary-%d.dat" % count)
            write_batch(batch, values_list)
            code, journal, report, output = run_program(SYNTHETIC, batch)
            self.assertEqual(code, 0, output)
            records, pages = parse_report(report)
            self.assertEqual(len(records), count, "count %d" % count)
            self.assertEqual([entry["id"] for entry in records],
                             [value["id"] for value in values_list],
                             "count %d" % count)
            for entry in records:
                self.assertEqual(entry["kind"], "D")
                self.assertIsNotNone(entry["applied"],
                                     "lost claim for %s at count %d"
                                     % (entry["id"], count))
            self.assertEqual(len(journal.splitlines()), count + 1)
            self.assertGreaterEqual(pages, 1)
            if count > 22:
                self.assertGreaterEqual(pages, 2, "count %d" % count)


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestReportRounding(unittest.TestCase):
    """ACCEPTANCE: report-only rounding must not touch the kernel.

    The line printer rounds half away from zero at the printed precision.
    Journal amount fields keep their exact binary32 bit pattern and their
    eight-decimal truncated text; only the register display changed.
    """

    @classmethod
    def setUpClass(cls):
        if not BINARY.is_file():
            subprocess.run([COBC, "-x", "-fixed", "-std=default", "-o",
                            str(BINARY), str(SOURCE)], check=True,
                           capture_output=True)

    def run_cases(self, cases, label):
        records = []
        for index, (p, max_hp, cur_hp) in enumerate(cases, start=1):
            values = make_cics_fixtures.base(index)
            # T[0][8] = 4.0 in the synthetic deck; H=0.25 makes amount = P.
            values.update({"mode": 2, "h": 0.25, "p": p, "k": 1.0,
                           "c": 1.0, "f": 1.0, "proj": 1,
                           "family": 0, "armor": 8,
                           "maxhp": max_hp, "curhp": cur_hp})
            records.append(values)
        batch = WORK / (label + ".dat")
        write_batch(batch, records)
        return run_program(SYNTHETIC, batch)

    def test_engine_values_print_at_four_decimals(self):
        code, journal, report, _ = self.run_cases(
            [(0.04, 10.0, 0.0), (0.03, 10.0, 0.0)], "rounding")
        self.assertEqual(code, 0)
        lines = journal.splitlines()
        self.assertEqual(lines[0][23:31], "3D23D70A")
        self.assertEqual(lines[1][23:31], "3CF5C28F")
        self.assertRegex(report, r"AMOUNT\s+0\.0400")
        self.assertRegex(report, r"AMOUNT\s+0\.0300")
        self.assertRegex(report, r"CLAIM APPLIED\s+0\.0400")
        self.assertRegex(report, r"CLAIM APPLIED\s+0\.0300")
        self.assertRegex(report, r"HP REGISTER NOW\s+0\.040")
        self.assertRegex(report, r"HP REGISTER NOW\s+0\.030")

    def test_negative_applied_keeps_sign_and_rounding(self):
        code, journal, report, _ = self.run_cases(
            [(1.0, 5.0, 20.0)], "negative")
        self.assertEqual(code, 0)
        self.assertEqual(journal.splitlines()[0][31:39], "C1700000")
        self.assertRegex(report, r"AMOUNT\s+1\.0000")
        self.assertRegex(report, r"CLAIM APPLIED\s+-\s*15\.0000")
        self.assertRegex(report, r"HP REGISTER NOW\s+5\.000")

    def test_near_ties_follow_the_printed_boundary(self):
        code, journal, report, _ = self.run_cases(
            [(0.00005, 10.0, 0.0), (0.00015, 10.0, 0.0)], "ties")
        self.assertEqual(code, 0)
        # binary32 cannot represent an exact four-decimal tie, so the nearest
        # values sit either side of the half step and must round down/up.
        self.assertRegex(report, r"AMOUNT\s+0\.0000")
        self.assertRegex(report, r"AMOUNT\s+0\.0002")

    def test_exact_decimal_ties_round_away_from_zero(self):
        # Presentation contract test: COBOL ROUNDED is half away from zero.
        self.assertEqual(round_display(Decimal("0.00005"), 4),
                         Decimal("0.0001"))
        self.assertEqual(round_display(Decimal("-0.00005"), 4),
                         Decimal("-0.0001"))

    def test_rounding_survives_page_breaks(self):
        cases = [(0.04, 10.0, 0.0)] * 30
        code, journal, report, _ = self.run_cases(cases, "rounding-pages")
        self.assertEqual(code, 0)
        entries, pages = parse_report(report)
        self.assertEqual(len(entries), 30)
        self.assertGreaterEqual(pages, 2)
        self.assertTrue(all(entry["amount"] == "0.0400" for entry in entries))
        self.assertTrue(all(entry["applied"] == "0.0400" for entry in entries))
        self.assertEqual(len(journal.splitlines()), 31)

    def test_report_amounts_agree_with_journal_bits(self):
        cases = [(0.04, 10.0, 0.0), (0.03, 10.0, 0.0), (1.0, 5.0, 20.0),
                 (0.00005, 10.0, 0.0), (0.00015, 10.0, 0.0)]
        code, journal, report, _ = self.run_cases(cases, "rounding-mix")
        self.assertEqual(code, 0)
        entries, _ = parse_report(report)
        journal_lines = [line for line in journal.splitlines()
                         if not line.startswith("T")]
        self.assertEqual(len(entries), len(journal_lines))
        for entry, line in zip(entries, journal_lines):
            amount = struct.unpack(
                "<f", struct.pack("<I", int(line[23:31], 16)))[0]
            applied = struct.unpack(
                "<f", struct.pack("<I", int(line[31:39], 16)))[0]
            hp = struct.unpack(
                "<f", struct.pack("<I", int(line[39:47], 16)))[0]
            self.assertEqual(Decimal(entry["amount"]),
                             round_display(amount, 4))
            self.assertEqual(Decimal(entry["applied"]),
                             round_display(applied, 4))
            self.assertEqual(Decimal(entry["hp"]), round_display(hp, 3))


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestDifferential(unittest.TestCase):
    """Bit-exact differential against the Python kernels."""

    @classmethod
    def setUpClass(cls):
        if not BINARY.is_file():
            done = subprocess.run(
                [COBC, "-x", "-fixed", "-std=default", "-o", str(BINARY),
                 str(SOURCE)], capture_output=True, text=True)
            if done.returncode != 0:
                raise AssertionError(done.stderr)

    def assert_batch_matches(self, table, records, label):
        batch = WORK / (label + ".dat")
        write_batch(batch, records)
        code, journal, _, output = run_program(table, batch)
        self.assertEqual(code, 0, output)
        expected, accepted, rejected, _ = cics_oracle.run(table, batch)
        self.assertEqual(len(journal.splitlines()), len(records) + 1)
        self.assertEqual(journal.splitlines(), expected, label)
        self.assertGreater(accepted + rejected, 0)

    def test_synthetic_table_random_batch_matches_bit_for_bit(self):
        self.assert_batch_matches(SYNTHETIC,
                                  make_cics_fixtures.random_records(250, 131544),
                                  "random-synthetic")

    def test_random_precision_batch_matches_bit_for_bit(self):
        import random
        from decimal import Decimal
        rng = random.Random(20261109)

        def pick(low, high, places):
            return Decimal(rng.randint(int(low * 10 ** places),
                                       int(high * 10 ** places))
                           ).scaleb(-places)

        records = []
        for index in range(300):
            values = make_cics_fixtures.base(index)
            values.update({
                "mode": rng.choice((1, 2)),
                "h": pick(0, 9, 8),
                "p": pick(0, 9999, 8),
                "k": pick(0, 9, 8),
                "c": pick(0, 9, 8),
                "f": pick(0, 9, 8),
                "dist": pick(0, 99999, 6),
                "maxhp": pick(0, 99999, 3),
                "curhp": pick(0, 99999, 3),
            })
            records.append(values)
        self.assert_batch_matches(SYNTHETIC, records, "random-precision")

    @unittest.skipUnless(private_table_available(),
                         "private arme-armure-table.json absent")
    def test_private_table_random_batch_matches_bit_for_bit(self):
        cards = WORK / "private.cards"
        subprocess.run([PYTHON, "-B",
                        str(REPO / "scripts/gen_table_cards.py"),
                        "--private", str(PRIVATE_JSON),
                        "--out", str(cards)], check=True,
                       capture_output=True)
        self.assert_batch_matches(cards,
                                  make_cics_fixtures.random_records(300, 4107205),
                                  "random-private")


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestTableSemantics(unittest.TestCase):
    """ENGINE OBSERVATIONS: real cells and loader refusal."""

    @classmethod
    def setUpClass(cls):
        if not BINARY.is_file():
            subprocess.run([COBC, "-x", "-fixed", "-std=default", "-o",
                            str(BINARY), str(SOURCE)], check=True,
                           capture_output=True)

    @unittest.skipUnless(private_table_available(),
                         "private arme-armure-table.json absent")
    def test_known_cells_reproduce_through_cobol(self):
        table = combat_damage_table.load_arme_armure_table(PRIVATE_JSON)
        cards = WORK / "cells.cards"
        subprocess.run([PYTHON, "-B",
                        str(REPO / "scripts/gen_table_cards.py"),
                        "--private", str(PRIVATE_JSON), "--out", str(cards)],
                       check=True, capture_output=True)
        cells = [(8, 3), (24, 3), (64, 3), (0, 3), (8, 0), (2, 25)]
        records = []
        for index, (family, armor) in enumerate(cells):
            values = make_cics_fixtures.base(index)
            values.update({"mode": 1, "h": 1.0, "p": 1.0, "k": 1.0,
                           "c": 1.0, "f": 1.0, "proj": 1,
                           "armor": armor, "family": family})
            records.append(values)
        batch = WORK / "cells.dat"
        write_batch(batch, records)
        code, journal, _, _ = run_program(cards, batch)
        self.assertEqual(code, 0)
        for line, (family, armor) in zip(journal.splitlines(), cells):
            expected = table.lookup(family, armor)
            self.assertEqual(line[23:31], cics_spec.bits(expected),
                             "T[%d][%d]" % (family, armor))

    def test_loader_refuses_a_broken_control_total(self):
        cards = WORK / "tampered.cards"
        text = SYNTHETIC.read_text().splitlines()
        header = text[0]
        text[0] = header[:29] + "99999999999" + header[40:]
        cards.write_text("\n".join(text) + "\n")
        code, journal, _, output = run_program(cards, SAMPLE)
        self.assertEqual(code, 12)
        self.assertIn("CONTROL TOTAL DISAGREES", output)
        self.assertEqual(journal, "")

    def test_loader_refuses_a_broken_family_sequence(self):
        cards = WORK / "sequence.cards"
        text = SYNTHETIC.read_text().splitlines()
        card = list(text[5])
        card[1:4] = "999"
        text[5] = "".join(card)
        cards.write_text("\n".join(text) + "\n")
        code, _, _, output = run_program(cards, SAMPLE)
        self.assertEqual(code, 12)
        self.assertIn("FAMILY SEQUENCE BROKEN", output)

    def test_loader_refuses_extra_cards(self):
        cards = WORK / "extra.cards"
        cards.write_text(SYNTHETIC.read_text() + " " * 80 + "\n")
        code, _, _, output = run_program(cards, SAMPLE)
        self.assertEqual(code, 12)
        self.assertIn("EXTRA CARDS AFTER MATRIX", output)

    @unittest.skipUnless(private_table_available(),
                         "private arme-armure-table.json absent")
    def test_generated_cards_carry_every_real_cell_exactly(self):
        table = combat_damage_table.load_arme_armure_table(PRIVATE_JSON)
        cards = WORK / "exact.cards"
        subprocess.run([PYTHON, "-B",
                        str(REPO / "scripts/gen_table_cards.py"),
                        "--private", str(PRIVATE_JSON), "--out", str(cards)],
                       check=True, capture_output=True)
        matrix = cics_oracle.load_cards(cards)
        for family in (0, 2, 8, 24, 64):
            for armor in (0, 3, 9, 24, 30, 34):
                self.assertEqual(matrix[family][armor],
                                 f32(table.lookup(family, armor)),
                                 "T[%d][%d]" % (family, armor))


@unittest.skipUnless(COBC, "GnuCOBOL cobc not installed")
class TestRejectPaths(unittest.TestCase):
    """SYNTHETIC: every reject code and the reconciliation return code."""

    @classmethod
    def setUpClass(cls):
        if not BINARY.is_file():
            subprocess.run([COBC, "-x", "-fixed", "-std=default", "-o",
                            str(BINARY), str(SOURCE)], check=True,
                           capture_output=True)

    def single(self, **overrides):
        values = make_cics_fixtures.base(1)
        values.update(overrides)
        return [values]

    def journal_for(self, records, tamper=None):
        batch = WORK / "case.dat"
        write_batch(batch, records, tamper=tamper)
        return run_program(SYNTHETIC, batch)

    def test_unknown_record_type(self):
        code, journal, _, _ = self.journal_for(
            self.single(), tamper=lambda lines: ["X" + lines[0][1:]])
        self.assertEqual(code, 0)
        self.assertIn("R001", journal)
        self.assertTrue(journal.splitlines()[0].startswith("R"))

    def test_non_numeric_amount_term(self):
        def tamper(lines):
            card = list(lines[0])
            card[12:24] = ["A"] * 12
            return ["".join(card)]
        _, journal, _, _ = self.journal_for(self.single(), tamper=tamper)
        self.assertIn("R005", journal)

    def test_non_numeric_hp_field(self):
        def tamper(lines):
            card = list(lines[0])
            card[148:156] = ["B"] * 8
            return ["".join(card)]
        _, journal, _, _ = self.journal_for(self.single(), tamper=tamper)
        self.assertIn("R007", journal)

    def test_control_count_mismatch_returns_eight(self):
        batch = WORK / "mismatch.dat"
        lines = [cics_spec.encode_detail(make_cics_fixtures.base(1))]
        lines.append(cics_spec.encode_control(99))
        batch.write_text("\n".join(lines) + "\n")
        code, _, report, _ = run_program(SYNTHETIC, batch)
        self.assertEqual(code, 8)
        self.assertIn("CONTROL CARD COUNT DISAGREES", report)

    def test_missing_control_card_returns_eight(self):
        batch = WORK / "nocontrol.dat"
        batch.write_text(cics_spec.encode_detail(make_cics_fixtures.base(1))
                         + "\n")
        code, _, report, _ = run_program(SYNTHETIC, batch)
        self.assertEqual(code, 8)
        self.assertIn("CONTROL CARD ABSENT", report)


class TestSourceContract(unittest.TestCase):
    """SYNTHETIC: genuine fixed-format source, no free-format drift."""

    def test_fixed_format_columns_and_uppercase(self):
        lines = SOURCE.read_text().splitlines()
        self.assertGreater(len(lines), 600)
        for number, line in enumerate(lines, start=1):
            self.assertLessEqual(len(line), 72, number)
            self.assertEqual("%06d" % number, line[:6], number)
            self.assertEqual(line[6], " ", number)
            self.assertEqual(line, line.upper(), number)
            self.assertNotIn("\t", line, number)

    def test_required_cobol_constructs_are_present(self):
        text = SOURCE.read_text()
        for token in ("OCCURS 65 TIMES", "OCCURS 35 TIMES",
                      "COMPUTE WS-QUOT = WS-REM / 13000.0",
                      "FUNCTION INTEGER-PART",
                      "MULTIPLY WS-P BY WS-ACC",
                      "EVALUATE TRX-CLASS",
                      "PERFORM 1100-STORE-CARD"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
