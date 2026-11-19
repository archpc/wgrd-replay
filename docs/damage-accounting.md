# Damage accounting: kernel chain and the WGRD-CICS batch

Companion to [ARCHITECTURE.md](ARCHITECTURE.md). That document covers the replay
decoder; this one covers the direct-fire damage fragments recovered from build
131544 and the COBOL batch program that recomputes them as an armor-loss
register. Read the evidence conventions there before using any label here.

## 1. Purpose and evidence scope

The chain exists to do one thing exactly: turn terms the engine read out of
memory into the same float32 bit pattern the engine produced, and book it. It is
not a weapon simulator and not a damage predictor. Every production input
(`H`, `P`, `K`, `C`, `F`, armor, family, or the ammunition fields that select one)
arrives on the batch record.

Proven, in the research note's OBS sense
(`research/current-build/2026-11-09-combat-damage-model.md`):

- amount order `((((H * P) * T) * K) * C) * F`, scalar SSE, rounded to binary32
  after every multiply, at `0xcfa2ae`..`0xcfa2e6` ("FP operation order");
- mode-2 HP application `min(amount, max - current)` then
  `max(current + applied, 0)`, at `0xc9fa4f`..`0xc9fc37` ("Application");
- gate `ProjectileType == 0`, `5 <= Arme <= 64`, `EfficaciteSelonPortee != 0`,
  and the index `Arme + trunc(max(0, rmax - d) / 13000)` with cap 34/64 and
  floor 5, at `0xc2ce00` / `0xda3410` (gate in the "Amount" family paragraph,
  arithmetic in "Phase 2c");
- the table object: 65 MAPLIST rows of FLOAT32 at NDF record offset
  `0x104f2f7`, stride 35, columns 30..34 zero ("Milestone 1b").

Modeled or supplied rather than proven: `H` is `R+0x48`, a damage factor whose
producer chain is untraced (INF, "Milestone 1c"), and `P`, `C`, `F` are named
from the property registrar with production out of scope. Mode 1 is amount-only —
the additive `+0x190` suppression path is observed (25 of 28 capture pairs) but
has no verified formula, so no clamp is coded (`src/cobol/README.md`, "Known
discrepancies and limits"). The 13000.0 step is used as a raw number; range
units are not established. The row index is a table row only — calling it AP, or
naming a row after a weapon kind, is unsupported (note, "Milestone 1b", INF
paragraph).

The COBOL program adds no evidence. It is a second implementation in another
runtime, and what it buys is that agreement is bit equality, not restatement.

## 2. Module map and ownership

```
engine (131544)                     observation, not code
   |  OBS instructions 0xcfa2ae.., 0xc9fa4f.., 0xda3410, 0xc2ce00
   v
research/combat_damage.py           pure arithmetic, no inputs resolved
research/combat_damage_range.py     gate + family index, no table access
research/combat_damage_table.py     private extraction -> padded 65x35
   |
   +--> scripts/gen_table_cards.py   matrix -> 80-column card deck
   +--> scripts/cics_oracle.py       batch + deck -> 72-byte journal lines
   |
   v
src/cobol/WGRDCICS.cob              same arithmetic, COMP-1, batch report
```

| Artifact | Owns | Does not own |
|---|---|---|
| `scripts/cics_spec.py` | batch/journal/card layouts, encode/decode, `f32`, `bits`, `exact_float32` | any field meaning |
| `research/combat_damage.py` | the two arithmetic fragments | which terms to use, mode 1 |
| `research/combat_damage_range.py` | gate, class -> range field, row index | table contents, range units |
| `research/combat_damage_table.py` | extraction validation, 35-column padding | committing the matrix, Arme encoding |
| `scripts/cics_oracle.py` | reject precedence, journal projection, totals | the arithmetic (it calls the kernels) |
| `src/cobol/WGRDCICS.cob` | report rendering, control-card reconciliation, exit codes | the layouts (it mirrors `cics_spec.py`) |

`cics_spec.py` is the only definition. `WGRDCICS.cob` re-declares the offsets in
`WS-BATCH-LAYOUT`, `WS-JOURNAL-LAYOUT` and `WS-TABLE-ROW-CARD` because
fixed-format COBOL has no shared copybook here; those declarations mirror the
spec, they do not extend it. Anything describing a record links to
`cics_spec.py` instead of restating columns.

The oracle re-parses the deck and batch from `cics_spec.py` and imports the
research kernels (`scripts/cics_oracle.py:25-27`), so a disagreement with COBOL
is about arithmetic or reject order, not two hand-copied offset tables.

## 3. Numerical contract

**Storage.** Every term is IEEE-754 binary32. Python uses
`f32()` via `struct.pack('<f')` (`research/combat_damage.py:20-25`). COBOL uses
`COMP-1`, which in GnuCOBOL 3.2 is true binary32 and rounds once on store; the
source says so and why that removes the need for a C shim
(`src/cobol/README.md`, "Evidence scope").

**Inputs are rounded before use.** The kernel rounds each factor as it consumes
it (`combat_damage.py:31-32`), the observable consequence of T, P, C and F
arriving through x87 as `fstp dword`. The oracle converts decoded decimal text
to binary32 before calling the kernel (`cics_oracle.py:136-143`); COBOL moves the
packed-decimal field into `COMP-1` (`WGRDCICS.cob:441-448`), which rounds in the
same place. An 8-decimal batch field therefore does not carry 8 decimals of
arithmetic precision: the first thing that happens to it is binary32 rounding.

**Order and rounding points.** Left to right, one rounding per step: start at
`f32(h)`, then `f32(value * f32(factor))` for each of `(p, t, k, c, f)` in order
(`research/combat_damage.py:28-33`). COBOL expresses the same sequence as
`MOVE WS-H TO WS-ACC` then five `MULTIPLY ... BY WS-ACC` (`WGRDCICS.cob:515-521`),
each store rounding. Association matters: the grouping `((H*P)*(T*K))*(C*F)`
produces a different bit pattern, and `tests/test_combat_damage.py:78-85` pins a
case where it does.

**Mode-2 clamp.** `room = f32(f32(max) - f32(cur))`, `applied` is the smaller of
amount and room, `new = f32(f32(cur) + applied)` floored at 0
(`combat_damage.py:36-44`). COBOL mirrors it with `COMPUTE WS-ROOM`,
`IF WS-AMOUNT < WS-ROOM`, `COMPUTE WS-NEWHP` (`WGRDCICS.cob:528-538`). Because
`room` is itself a rounded binary32 difference, computing it in double and
rounding once is measurably different near the boundary.

**Truncation.** The family index divides, then truncates toward zero:
`math.trunc(f32(remaining / f32(RANGE_STEP)))`
(`combat_damage_range.py:106-109`). COBOL uses
`FUNCTION INTEGER-PART(WS-QUOT)` (`WGRDCICS.cob:490`) — the same rule as the
engine's `cvttsd2si`. `remaining` is floored at 0 before the divide, so the
negative-quotient case is unexercised by the engine path, though both
implementations agree on it.

**Journal hex.** `cics_spec.bits()` packs the value back to binary32 and prints
eight uppercase hex digits (`cics_spec.py:125-126`). COBOL builds the same eight
digits by walking the four bytes of a `COMP-1` REDEFINES and indexing a literal
hex table with `FUNCTION ORD(...) - 1` (`WGRDCICS.cob:119-122`, `9000-BUILD-HEX`
at `800-816`); `ORD` is 1-based, hence the subtraction. The byte loop runs
`VARYING WS-IDX FROM 4 BY -1`, reversing little-endian storage so the text reads
big-endian.

**Journal text.** `J-AMT-TEXT PIC 9(9).9(8)` is filled by `MOVE WS-AMOUNT`
(`WGRDCICS.cob:592`), which truncates; the oracle quantizes with `ROUND_DOWN` to
eight places (`cics_oracle.py:97-101`). This field is display. The bit fields are
the contract.

**Transport.** Table cells travel as 21-digit implied-decimal integers with 18
decimal places (`scripts/gen_table_cards.py:43-49`, `cics_spec.exact_float32`).
Each is `Decimal(repr(cell)) * 10**18`, so the deck carries a decimal within well
under half a binary32 ULP of the cell, and the COBOL `MOVE` of `PIC 9(3)V9(18)`
into `COMP-1` (`WGRDCICS.cob:360-366`) lands on the same bit pattern: the
conversion rounds, but the decimal sits within half a ULP, so it rounds back
to the original cell. Both generators assert the scaled value is an integer and raise
otherwise. All 2275 cells of the private extraction need at most 18 decimal
places and round-trip through the deck unchanged — verified by direct probe of
the private file, not asserted here as a repo invariant.

**Totals.** The deck header carries the double-precision sum of the padded matrix
in row-major order, in thousandths (`gen_table_cards.py:52-56,113-118`). The
loader recomputes it in the same order into `COMP-2` and compares with a one-unit
tolerance (`WGRDCICS.cob:349-354`); the oracle recomputes it in Python floats the
same way (`cics_oracle.py:87-93`). The journal trailer instead accumulates
accepted amounts one at a time in binary32 — `f32(total + amount)`
(`cics_oracle.py:211`) against `ADD WS-AMOUNT TO WS-RUN-AMOUNT`
(`WGRDCICS.cob:522`) — so it is order-dependent and must not be recomputed as a
single sum.

## 4. Invariants

1. **One layout.** `cics_spec.py` is authoritative; documents and tests link to
   it. `tests/test_cics.py:169-183` pins contiguity and non-overlap. Offsets
   restated in prose become a second copy that drifts: the distance field was
   widened once without regenerating the committed samples, which is why
   `TestSampleFixtureProvenance` (`tests/test_cics.py:202-250`) now pins the
   batch against the builder output.
2. **COMP-1 is binary32, and it is the only float in the batch.** Were it
   binary64, every intermediate would keep extra precision and the journal bits
   would drift on nearly every transaction. Nothing in the source asserts the
   representation; `TestDifferential` (`tests/test_cics.py:531-597`) is the
   only guard.
3. **No reassociation.** Grouping, hoisting or fusing the multiplies changes bits;
   any rewrite, in either language, loses the equality.
4. **Hex, not decimal, closes the loop.** The journal carries both, and only the
   bit fields are compared byte-for-byte. Decimal comparison at four or eight
   places hides exactly the rounding differences the chain exists to reproduce.
5. **The matrix is private.** `research/combat_damage_table.py` validates a
   hash-pinned external extraction and pads it to 35 columns; nothing in Git
   holds the cells. The committed deck is labelled `SYNTHETIC-NOT-GAMEDATA`
   (`gen_table_cards.py:81-93`) and the loader refuses a blank tag
   (`WGRDCICS.cob:316-319`).
6. **Absent is not zero.** `range_max_for_class` raises on a missing or null
   property (`combat_damage_range.py:95-97`); COBOL rejects a zero range field
   with `R004` instead of defaulting. The engine's own behavior for an absent
   field is unmodelled (note, "Not established").

## 5. Failure modes

**Table load** fails on any of: header absent, dataset name mismatch, build
mismatch, dimensions not 65x35, blank provenance tag, truncated deck, non-`R`
card, family sequence broken, column index past 35, negative or out-of-band cell,
extra cards after the matrix, control total disagreement. All take
`9100-TABLE-ABEND`: two `DISPLAY` lines, `RETURN-CODE 12`, no journal — it fires
before the journal is opened (`WGRDCICS.cob:296-356`, `818-822`; opened at 274).
The oracle raises `OracleError` for the equivalent conditions
(`cics_oracle.py:36-94`).

**Record rejects** are `R001`..`R008`, written to the journal with `RJ` status and
to the report with a fixed reason text. The codes, meanings and `WS-REASON-TEXTS`
wording are owned by
[src/cobol/README.md](../src/cobol/README.md#reject-codes); do not duplicate the
table here. Two properties matter when reading the code:

- Precedence is validation (`R002`, then `R005`, then `R007`), then family
  selection (`R006`, `R004`), then bounds (`R003`, `R008`). The oracle follows
  the same order (`cics_oracle.py:125-167`), so a record with two defects reports
  the same code in both implementations.
- `R003` is reachable only through the closed gate, where the family comes from
  the card. The kinetic path clamps to 34 or 64 and cannot emit an out-of-range
  family.

**Exit codes**: 0 completed; 8 completed but the control-card count did not
reconcile (or no control card was seen); 12 refused before processing. Owned by
the README ("Run").

**Environment note.** `scripts/gen_table_cards.py:121` and
`scripts/cics_oracle.py:230` call `Path.write_text(..., newline=...)`, which needs
Python 3.10+. The default `python3` on this host is 3.9.6, where the private-deck
path raises `TypeError` after building the deck. The synthetic deck and the COBOL
suite are unaffected: the tests call `oracle.run()` directly.

## 6. Test map

| File | Pins |
|---|---|
| `tests/test_combat_damage.py` | input rounding (:50); one rounding per multiply, shown to differ from a single final rounding (:61); left-to-right association (:78); clamped, unclamped, floor and zero-room branches (:88); mode-2 capture pairs bit-exact (:116, SHA-256 `e4eaaad0…5654`, private, skips); mode-1 pairs declared out of scope (:160) |
| `tests/test_combat_damage_range.py` | gate truth table and boundaries (:54); 13000 step boundaries and float32 division before truncation (:86); cap 34/64 and floor 5 (:123); two shipped `TAmmunition` records with their absent fields (:217, SHA-256 `5909779c…33e24`, private, skips) |
| `tests/test_combat_damage_table.py` | loader rules against synthetic payloads only — hash, metadata, shape, element type, float32 representability, index guards (:69); extracted cells and zero-filled columns (:183, private, skips) |
| `tests/test_cics.py` | layout contiguity and round-trip (:166); sample equals builder output and TX5 reaches the cap (:202); journal byte-identical to the oracle for the sample, 250 and 300 randomized transactions (:268, :554), and through the real matrix (:586, private); real cells through COBOL and through the generated deck (:611, private); loader refusals (:637); every reject code and exit 8 (:683); report/journal cross-check across page breaks (:321); display rounding is report-only (:428); fixed-format source and required constructs (:745) |

Synthetic tests pin the arithmetic contract and run everywhere; engine-observation
tests pin a hash of a private fixture and skip with an explicit message when it is
absent, rather than passing. A green run without the private directory proves the
two implementations agree with each other, not that they agree with the engine.
The COBOL classes skip as a whole when `cobc` is missing.

The hash pins keep those fixtures honest: they live outside Git, so an edited
fixture is otherwise indistinguishable from a corrected one.

## 7. Evidence links

- `research/current-build/2026-11-09-combat-damage-model.md` — "Amount",
  "FP operation order", "Application", "Milestone 1b", "Phase 2a/2b/2c" (the
  kernels and their test classes), "Not established".
- [src/cobol/README.md](../src/cobol/README.md) — evidence table, build, run,
  exit codes, reject codes, verification, known limits.
- `scripts/cics_spec.py` module docstring — record layouts and the table-cell
  transport rule.
- `tests/test_cics.py` module docstring — why the journal is diffed as bits.
- [ARCHITECTURE.md](ARCHITECTURE.md#evidence-conventions) — OBS/INF versus
  `verified`/`inferred`/`unknown`, and the rule that structure, confidence and
  meaning are separate labels.

Private artifacts the code reads, outside Git, under
`~/.hermes/artifacts/wgrd-replay/combat-damage-static-20261109/`:
`arme-armure-table.json`, `delegates/B/hp_clamp-fixtures.json`,
`phase2c-ammunition-crosscheck.json`.
