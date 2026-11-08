# Effective NDF values for the AI tunables (build 131544)

Date: 2026-11-08. Read-only. No game launch, no VM interaction.
Branch: `research/ndf-effective-values` (PR #26 is frozen and does not contain this).

This note answers the question PR #26 had to leave open: what values does the
shipped data actually contain for the AI economy and information levers?

Method is not hand-parsing. The container is unpacked with
[`wgrd_cons_parsers`](https://github.com/ev1313/wgrd-cons-parsers) 0.3
(`python -m wgrd_cons_parsers.edat`), and the compiled NDF is read by a small
port of the open-source [moddingSuite](https://github.com/TK3600/moddingSuite)
reader (`BL/Ndf/NdfbinReader.cs`, `Model/Ndfbin`). `scripts/ndf_read.py` is that
port; it reads, and never writes, game data.

## Provenance

| item | value |
|---|---|
| archive | `Data/WarGame/PC/131544/NDF_Win.dat` |
| archive SHA-256 | `172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b` |
| blob | `pc/ndf/patchable/gfx/gdconstanteoriginal.ndfbin` |
| blob offset in archive | `0x250000`, 5841 bytes, SHA-256 `e8e7faf3…` |
| blob header | `EUG0…CNDF`, compressed body (0x80), zlib from +44 |
| decompressed | 18478 bytes, SHA-256 `4d9285186d95ab0e2939e386f52b6510fbe1d4753c1ded2eeea64b3d270b08d2` |
| classes in blob | `TTunableConstante` (144 props), `TModernWarfareTunableConstante` (101), `TWargameTunableConstante` (12) |
| objects | 3 |

The decompressed bytes were reconstructed **from the archive slice itself**
(`blob[:40] + zlib(blob[44:])`) and hash to the value above. That is the
archive-byte check: the values below are not read out of a repacked or
synthesised file.

## Overlays and revisions

`Data/WarGame/PC/` holds 11 revision snapshots. Their NDF archives are **not**
all distinct — there are five distinct contents, and later revisions reuse
earlier ones:

```
172e481d… 131544            660fbf2d… 130278            97d7442e… 59638, 68335
33fa28cd… 116084, 72352     ef067549… 48574, 49125       ef2a0edc… 58710      c6c041e7… 49964
```

The tunables blob is **byte-identical** across 59638, 130278 and 131544
(all three decompress to `4d928518…`). So whatever an "override" model would
say, this file did not change across those revisions: no revision drift, no
newer patch layer.

Inside one archive the file exists once, under `patchable/`. There is no
`nonpatchable/` counterpart and no second file defining these properties, so
within build 131544 there is no competing definition to resolve.

## Recovered values

Base object (`TTunableConstante`), verbatim from the blob:

| property | type | value |
|---|---|---|
| `IgnoreInvisibleUnit` | bool | **true** |
| `InfluenceMapAlwaysKnowAllUnits` | — | **absent from shipped data** |
| `BonusIAMoneyForSkirmish` | i32 | **500** |
| `StockDeviseSupplementaireFacile` | i32 | **72** |
| `StockDeviseSupplementaireMoyen` | i32 | absent |
| `StockDeviseSupplementaireDifficile` | i32 | absent |
| `DefaultDifficulty` | i32 | 2 (medium) |
| `QteDeviseParCamion` | — | absent |
| `VisibilityMemoTimer` | i32 | 30 |
| `MultiplicateurSeuilPinnedEtMortJoueurFacile` | f32 | 1.5 |
| `MultiplicateurSeuilPinnedEtMortIAFacile` | f32 | 0.75 |
| `MultiplicateurSeuilPinnedEtMortJoueurMoyen` | f32 | 1.0 |
| `MultiplicateurSeuilPinnedEtMortIAMoyen` | f32 | 1.0 |
| `MultiplicateurSeuilPinnedEtMortJoueurDifficile` | f32 | 0.75 |
| `MultiplicateurSeuilPinnedEtMortIADifficile` | f32 | 1.25 |
| `MultiplicateurDegatInfligeParLeJoueur_Facile/Moyen/Difficile` | f32 | 1.0 / 1.0 / 1.0 |
| `FumigeneTimeout` | f32 | 60.0 |
| `PlaneSuperiority` | f32 | 2.5 |
| `RatioSupplyHealth` / `RatioSupplyAmmoAndFuel` / `RatioSupplyToStartAMission` | f32 | 0.1 / 0.2 / 0.4 |

`TWargameTunableConstante` (the subclass object) adds economy plumbing:

| property | value |
|---|---|
| `IncomeMultiplierInPercent` | `[0, 60, 80, 100, 120, 140]` |
| `DefaultIncomeMultiplierIndex` | 3 → **100%** |
| `TimeBeforeEarningCommandPoints` | 4.0 |
| `TimeBeforeEarningConquestPoints` | 4.0 |

## What this means for "are the hidden advantages enabled?"

### Information axis

* `IgnoreInvisibleUnit` is **shipped true**. The byte the executable reads at
  `0x020263a1` therefore arrives set from data, and the consumer at
  `0x01037775` is live in a normal game.
* `InfluenceMapAlwaysKnowAllUnits` is **not defined in the shipped blob at
  all**. The loader at `0x00b914c0` reads a fixed field list, so for an
  undefined property it copies the descriptor's constructor default, not a data
  value. That default is not recoverable from the NDF, so the honest statement
  is: **no shipped value enables the influence-map bypass**; whether the code
  default is 0 or 1 is unresolved statically.

### Economy axis

* `BonusIAMoneyForSkirmish` ships as **500**, but its global `0x02026390` has
  exactly one code reference — the loader store at `0x00b92035` — and no
  reader was found in the executable. Either it is consumed by a script layer
  not present in this installation, or it is inert. Unresolved, not a cheat.
* `StockDeviseSupplementaire` defines **only the Easy variant (72)**. The
  difficulty initialiser at `0x00bb2740` selects one of three globals by
  difficulty (`0x02026360`/`0x02026364`/`0x02026368`); the Medium and Hard
  globals have no data behind them. On the shipped `DefaultDifficulty = 2`
  (medium), the stock bonus is therefore **not** the 72 Easy value.
* The difficulty asymmetry is real and shipped, but it is **not** a damage
  cheat: `MultiplicateurDegatInfligeParLeJoueur_*` is 1.0 on all three. What
  scales is the pinned/death threshold pair — player 1.5 / 1.0 / 0.75 against
  IA 0.75 / 1.0 / 1.25. Which direction of that pair favours the AI depends on
  how the threshold is consumed, which this note does not establish.

### Standings

| claim | status |
|---|---|
| `IgnoreInvisibleUnit` ships true and is read | proven (data + `0x01037775`) |
| `InfluenceMapAlwaysKnowAllUnits` is unset in shipped data | proven (absence in blob) |
| Its effective default is 0/false | **unresolved** (constructor default, not in NDF) |
| `BonusIAMoneyForSkirmish` = 500 | proven (data) |
| It reaches an AI decision | **unresolved** (no consumer found) |
| Difficulty scales economy stock | proven mechanism, Easy-only value |
| Difficulty scales player damage | refuted: all 1.0 |
| Difficulty scales pinned/death thresholds asymmetrically | proven values, direction unresolved |

## Reproduce

```bash
# 1. unpack the archive (read-only; writes only to the output directory)
uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python wgrd_cons_parsers==0.3
.venv/bin/python -m wgrd_cons_parsers.edat \
  Data/WarGame/PC/131544/NDF_Win.dat -o out131544

# 2. decompress the blob (the unpacker keeps the compressed flag set)
.venv/bin/python -c "from wgrd_cons_parsers.decompress_ndfbin import decompress_ndfbin as d; \
  import pathlib; pathlib.Path('gdconst.bin').write_bytes(d(pathlib.Path( \
  'out131544/pc/ndf/patchable/gfx/gdconstanteoriginal.ndfbin').read_bytes()))"

# 3. read values
python3 scripts/ndf_read.py gdconst.bin --list-classes
python3 scripts/ndf_read.py gdconst.bin --prop IgnoreInvisibleUnit \
  --prop BonusIAMoneyForSkirmish --prop StockDeviseSupplementaireFacile
```

## Unresolved gaps

1. Descriptor constructor defaults for properties absent from NDF
   (`InfluenceMapAlwaysKnowAllUnits`, `StockDeviseSupplementaireMoyen/Difficile`,
   `QteDeviseParCamion`). Static only if the default writer is found.
2. A consumer for `BonusIAMoneyForSkirmish`. Not in this executable.
3. Direction of the pinned/death threshold multipliers.
4. Whether skirmish setup selects a non-default `IncomeMultiplierIndex`; the
   data default is 3 (100%).
5. Whether Lua or another script layer ships values this install does not
   contain.
