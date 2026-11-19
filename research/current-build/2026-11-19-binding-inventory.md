# Revision 131544: complete CPython binding-table inventory (2026-11-19)

Companion to the [sysutils binding note](2026-11-19-sysutils-cpython-bindings.md):
that note proves the interface and the clock tables; this one enumerates the
whole Python API surface of the engine. Interpreter is CPython **2.5.1**
(version proof: sysutils note §1). Offline static, worker-enumerated,
parent-recomputed: an independent stride-4 scan with the same predicate
reproduces **28 tables / 271 entries exactly** (base→count map identical).
Full machine-readable inventory and report: local evidence records
`~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/binding-inventory.json`
and `binding-inventory-report.md`.

## Method (and the trap)

16-byte `PyMethodDef` entries `{ml_name, ml_meth, ml_flags=1, ml_doc=NULL}`,
run ≥ 2, immediately followed by a 16-byte null terminator; `ml_name` must
dereference to a printable C string, `ml_meth` must lie in `.text`.

**Stride 4, not 16.** The tables are 8-byte aligned (`0x1d9cc78 % 16 == 8`);
a 16-byte-grid scan misses even the two previously known tables. `.data`
only: the same predicate over `.rdata` yields 0 tables. Loosening
`ml_doc == 0` adds nothing. Installer confirmation: `push <table base>`
inside the one-shot-guard + `push 0x3f5` + `call 0x1537830` + SIP-lookup
sequence; 27 of 28 located and byte-matched (spot-verified `_world`,
`_network`, `_dynamic_campaign` installers and name slots read back).

## The 28 tables

| # | module | base | entries | terminator | installer |
|---|--------|------|---------|------------|-----------|
| 1 | `(unresolved)` | `0x1d7efe0` | 5 | `0x1d7f030` | `**none**` |
| 2 | `_manager` | `0x1d7f268` | 2 | `0x1d7f288` | `0x9b5ed0` |
| 3 | `_cameratarget` | `0x1d81670` | 2 | `0x1d81690` | `0x9dd8e0` |
| 4 | `_constantes` | `0x1d818b0` | 16 | `0x1d819b0` | `0x9de370` |
| 5 | `_cutscene` | `0x1d81b84` | 2 | `0x1d81ba4` | `0x9debf0` |
| 6 | `_dynamic_campaign` | `0x1d839a0` | 45 | `0x1d83c70` | `0x9e64f0` |
| 7 | `_front_game_rules` | `0x1d87e30` | 2 | `0x1d87e50` | `0x9ecad0` |
| 8 | `_group_helper` | `0x1d93b68` | 4 | `0x1d93ba8` | `0xa228a0` |
| 9 | `_identifiable_object` | `0x1d9436c` | 2 | `0x1d9438c` | `0xa24880` |
| 10 | `_input` | `0x1d95ab8` | 2 | `0x1d95ad8` | `0xa292b0` |
| 11 | `_interface_manager` | `0x1d96048` | 2 | `0x1d96068` | `0xa29af0` |
| 12 | `_leveldesign` | `0x1d96e58` | 4 | `0x1d96e98` | `0xa2e350` |
| 13 | `_misc` | `0x1d97ad8` | 32 | `0x1d97cd8` | `0xa32ba0` |
| 14 | `_mission` | `0x1d98ab8` | 4 | `0x1d98af8` | `0xa36d60` |
| 15 | `_modular_unit` | `0x1d98e10` | 3 | `0x1d98e40` | `0xa376a0` |
| 16 | `_network` | `0x1d99e70` | 34 | `0x1d9a090` | `0xa3afe0` |
| 17 | `_order` | `0x1d9ab48` | 3 | `0x1d9ab78` | `0xa3c250` |
| 18 | `_pack_signaux_condition` | `0x1d9b090` | 4 | `0x1d9b0d0` | `0xa3cb20` |
| 19 | `_piggybank` | `0x1d9b418` | 3 | `0x1d9b448` | `0xa3d790` |
| 20 | `_saveable` | `0x1d9bc2c` | 2 | `0x1d9bc4c` | `0xa3e650` |
| 21 | `_script_break_point` | `0x1d9bd30` | 3 | `0x1d9bd60` | `0xa3e7a0` |
| 22 | `_sound` | `0x1d9c3c8` | 10 | `0x1d9c468` | `0xa3fde0` |
| 23 | `_sysutils` | `0x1d9cc78` | 51 | `0x1d9cfa8` | `0xa42790` |
| 24 | `_team` | `0x1d9edb8` | 5 | `0x1d9ee08` | `0xa4cf00` |
| 25 | `_unite` | `0x1da00a0` | 8 | `0x1da0120` | `0xa51030` |
| 26 | `_world` | `0x1da3b48` | 12 | `0x1da3c08` | `0xa5ed60` |
| 27 | `marshal` | `0x1dcba58` | 2 | `0x1dcba78` | `0x15359b0` |
| 28 | `sip` | `0x1dcc928` | 7 | `0x1dcc998` | `0x1544624` |

## Clock, phase and determinism surface

- `_sysutils` (51) carries the dual clock and the determinism/speed controls:
  `DeterministicCurrentTimeInSeconds/InTicks`,
  `SetDeterministicCurrentTimeInTicks`, `RealtimeCurrentTime`,
  `SetRealtimeCurrentTime`, `OnGamePhaseChanged`, `SetNextGamePhase`,
  `TerminateGamePhaseManager`, `NeedDesynchroLogFromNow`,
  `DontNeedDesynchroLogFromNow`, `StartDesynchroLogNowIFN`,
  `DontRequireDeterminismFromNowOn`, `RequireDeterminismFromNowOn`,
  `DecreaseGameSpeed`, `IncreaseGameSpeed`, `ResetGameSpeed`, `ResetTime`
  (names decoded from the table, parent-verified).
- `_misc` (32): `WorldTickEnd`, `CreateNamedActionWithTimer`,
  `DestroyNamedActionWithTimer`,
  `RequestSynchroWith3DBeforeNextEffetMap`,
  `SetSynchroWith3DBetweenEffetMapListener`.
- `_network` (34): `RequestEndLoadingPhase`,
  `RegisterSynchronizationDoneListener`,
  `UnregisterSynchronizationDoneListener`, `GetTimeLimit`.
- Smaller hooks: `_constantes.GetTimeLimitTable`, `_team.SetTeamNextFrame`,
  `_modular_unit.ResetModularUnitIdCheck`,
  `_script_break_point.NoMoreScriptToExecuteInFrame`, `_manager.resetcount`.

The deterministic/realtime pair is independently script-writable — the seam
for replay/time control. `RequireDeterminismFromNowOn` /
`DontRequireDeterminismFromNowOn` are newly surfaced controls whose semantics
are unverified; they are candidates for the determinism-boundary question,
not answers. `NoMoreScriptToExecuteInFrame` is consistent with a per-frame
script execution boundary (relevant to the open script-drives-the-clock
hypothesis, sysutils note §9) but proves nothing by itself.

## Caveats

- `0x1d7efe0` (5 entries, frozen-importer-style API): structurally valid,
  installer unlocated, module name unresolved — not guessed.
- `_manager` is registered twice (`0x9b5ed0`, `0x9d63c1`), same guard
  `ds:0x201eca8`.
- `marshal` / `sip` installers have no one-shot guard (bootstrap path).
- Entry names are decoded; per-function semantics beyond the clock note are
  not established here.

## Reproduction

```sh
# stride-4 scan of .data (VA 0x1d6b000, raw 0x1969000, size 0x261c00):
# entry = name_ptr(.rdata/.data printable cstring) + fn_ptr(.text) + 1 + 0,
# run >= 2, then 16 zero bytes. See binding-inventory.json for the full list.
EXE=~/.hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe
OD=/opt/homebrew/opt/binutils/bin/objdump
$OD -s --start-address=0x1d9cc78 --stop-address=0x1d9cca8 "$EXE"  # _sysutils head
grep -n 'push   0x1da3b48' ~/REA/wgrd-131544/wgrd_131544_full.lst  # _world installer
```
