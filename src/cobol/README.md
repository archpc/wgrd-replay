# WGRD-CICS: Combat Impact Calculation System

A GnuCOBOL batch program that recomputes the verified build 131544 direct-fire
damage fragments and books the result as an armor-loss register. Fixed-format
source, 65x35 private Arme/Armure matrix, line-printer report, batch rejects,
reconciliation totals.

ARMOR LOSS SHALL NOT BE RECOGNIZED UNTIL FORM DD-131544 HAS BEEN PROCESSED BY
ACCOUNTS PAYABLE.

## Evidence scope

Implemented, from `research/current-build/2026-11-09-combat-damage-model.md`:

| Term | Source | Implementation |
|---|---|---|
| table lookup | `T[family][armor]`, stride 35, zero based | `WS-CELL(family + 1, armor + 1)` |
| amount | `((((H*P)*T)*K)*C)*F` at `0xcfa2ae`..`0xcfa2e6` | six `MULTIPLY` steps into `COMP-1` |
| rounding | scalar SSE binary32 after every step | `COMP-1` store rounds each result |
| mode-2 clamp | `min(amount, max-current)`, floor 0 | `2410-CLAMP` |
| range gate | `ProjectileType==0`, `5<=Arme<=64`, `EfficaciteSelonPortee!=0` | `2300-SELECT-FAMILY` |
| range family | `Arme + trunc(max(0, rmax-distance)/13000)`, cap 34/64, floor 5 | `2320-KINETIC` |
| target class | 1 boats, 2 max, 3/4 TBA, 5 HA, 6 projectile | `2310-RANGE-BY-CLASS` |

Not modelled, and never defaulted: H/P/C/F production, accuracy, hit roll,
facing, splash falloff arrays, mode-1 accumulation, suppression, kill
publication, Arme naming, range units. Those inputs arrive on the batch card.

`COMP-1` is a true IEEE-754 binary32 in GnuCOBOL 3.2; storing each product
rounds once, which is why no C shim is used. `probe` checks in this worktree
matched Python `struct.pack('<f')` bit patterns, and the differential suite
compares 4000+ randomized transactions on bit patterns, not decimals.

## Authoritative record specification

`scripts/cics_spec.py` is the single definition of the batch, journal and card
layouts. Do not restate offsets elsewhere. The COBOL declarations mirror it.

Batch: 176-byte records, implied decimals, zero filled, no decimal point.
Summary: type 1, id 2-11, mode 12, H/P/K/C/F 12 bytes each from column 13,
armor 73, family 75, projectile type 77, Arme 79, Efficacite 81, target class
82, distance 83, five range fields 94-148, MaxDamages 149, current HP 157,
filler 165-176. Control card: `Z` plus a 7-digit detail count.

Journal: 72 bytes; accepted `D`, rejected `R`, final `T` trailer with accepted
and rejected counts and the float32 grand-total bit pattern.

Table deck: `H` header (name, build, 65, 35, control total in thousandths,
provenance tag) then 12 `R` cards per family. Values are 21-digit
implied-decimal integers carrying the exact decimal expansion of each binary32
cell, so the COBOL numeric move reconstructs the cell without rounding.

## Build

Requires GnuCOBOL 3.2 (`brew install gnucobol`; already present on this host).

```sh
cobc -x -fixed -std=default -o build/wgrdcics src/cobol/WGRDCICS.cob
```

## Data

The 65x35 matrix is private evidence and is not committed. Generate its card
deck from the hash-pinned extraction:

```sh
python3 scripts/gen_table_cards.py \
  --private ~/.hermes/artifacts/wgrd-replay/combat-damage-static-20261109/arme-armure-table.json \
  --out ~/.hermes/artifacts/wgrd-cics/arme-armure-131544.cards
```

For a run without private data, the committed deck
`samples/cics/synthetic-table.cards` is labelled `SYNTHETIC-NOT-GAMEDATA`.

## Run

```sh
export WGRD_CICS_TABLE=samples/cics/synthetic-table.cards
export WGRD_CICS_BATCH=samples/cics/sample-batch.dat
export WGRD_CICS_JOURNAL=build/sample.jrn
export WGRD_CICS_REPORT=build/sample.rpt
./build/wgrdcics
```

Exit codes: 0 completed, 8 completed but the control-card count did not
reconcile (also reported), 12 refused before processing (path, table
identification, structure, or control-total failure).

Sample output: `samples/cics/sample-report.txt` (synthetic deck, two pages).
Journal lines are trailing-blank trimmed by LINE SEQUENTIAL; all semantic
fields end in non-blank data.

## Reject codes

| Code | Meaning |
|---|---|
| R001 | record type not `D` or `Z` |
| R002 | mode not 1 or 2 |
| R003 | family index above 64 |
| R004 | selected range field is zero (absent, not defaulted) |
| R005 | non-numeric amount/range field |
| R006 | target class not 1..6 |
| R007 | non-numeric HP accounting field |
| R008 | armor index above 34 |

## Verify

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_cics -v
```

The suite compiles the program, runs the sample deck, compares the journal
byte-for-byte with `scripts/cics_oracle.py` (which imports the verified
`research/combat_damage.py` and `combat_damage_range.py` kernels), fuzzes
randomized precision cases, checks four known real cells
(`T[8][3]=8`, `T[24][3]=40`, `T[64][3]=60`, `T[0][3]=0x3DCCCCCD`), and tampers
with the deck to prove the loader refuses. Where the private table is present
the suite also diffs a randomized batch through the real matrix.

## Known discrepancies and limits

- Mode 1 is amount-only. The engine's additive `+0x190` suppression path is
  observed empirically but has no verified formula, so no clamp is coded.
- The engine skips application when `amount <= 0`. The clamp here is
  unconditional, which is equivalent for `amount == 0` and cannot occur for
  negative amounts; no case with a negative amount exists.
- `H`, `P`, `C`, `F` remain caller-supplied. The batch card is an accounting
  voucher, not a weapon simulator.
- Table loading validates name, build, dimensions, family and sequence order,
  numeric cells, sanity band and the control total. Exact binary32 transport is
  guaranteed by the generator and proven by the differential suite; it is not
  re-derived inside COBOL.
- Report formatting is not diffed byte-for-byte, only the numeric journal.
