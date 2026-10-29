# Research index: provenance map for wgrd-replay

[Project overview](../README.md) · [Documentation map](../docs/README.md) · [Format reference](../FORMAT.md) · [Evidence conventions](../docs/ARCHITECTURE.md#evidence-conventions)

**Reading the record (2026-10-28):** the subject tables retain milestone findings
and their original evidence. For current implemented behavior, use the
[architecture](../docs/ARCHITECTURE.md) and [format reference](../FORMAT.md).
In particular, `0x0D` interiors are opaque **in the parser**, while the timeline's
production layer decodes supported interiors (section 7 below). The older
“open interiors” item at the end is superseded for those layouts, not for every
possible serializer. `opaque` is a structural label, not an interpretation status.
No historical finding is promoted to general gameplay verification by the
controlled experiment.

## Current-executable offline corpus research (2026-10-29)

[Report](current-build/2026-10-29-offline-corpus.md): 71 hash-pinned archive
recordings; archive 119 slot-ID correction; revision-131544 Ghidra traces for
order queue options and synchronization membership; larger production shapes.
[Measurements](current-build/2026-10-29-corpus-summary.json),
[native excerpts](current-build/2026-10-29-native-excerpts.json),
[manifest](../samples/offline-corpus-manifest.json),
[reproduction script](offline_corpus.py). No runtime or VM execution in this pass.

## Current-build experiment (2026-10-28)

[Comprehensive controlled-experiment report](current-build/2026-10-28-controlled-experiment.md): Steam build 15652829, internal revision 131544, actual launched executable identity; black Parallels capture versus working guest GDI; portable C# input/capture helper and its history; offline Death Row recording and completed playback; sample-specific fuel-toggle corroboration; replay/battle time-base distinction; two additional historical recordings from one archive; regression runner and validation.

Evidence: [screenshot hashes and controlled command locations](current-build/2026-10-28-evidence.json), [external regression manifest](../samples/cross-build-manifest.json), [helper](current-build/tools/WgrdUi.cs), [initial helper](current-build/history/WgrdUi-v1.cs), and tests/test_cross_build_corpus.py. [The Oshkosh Incident gallery](current-build/README.md) includes curated screenshots and links the complete versioned screenshot archive. Replay bytes and private player metadata remain external.

Next experiment: [Phase 2 handoff](current-build/PHASE-2-HANDOFF.md). It does not authorize VM operation.

[Approach assessment (2026-10-29)](current-build/2026-10-29-approach-assessment.md): compares further command interpretation, static consumer modeling and engine emulation. Recommends gated, instrumented original playback (engine as oracle), starting with a probe of the guest's pinned 59638 executable. Assessment only; no execution, and priorities remain in NEXT-STEPS.md until adopted.

Dated correction to the historical sections below: ground-truth work is no longer wholly absent, and the earlier acquisition/launch blockers in GROUND-TRUTH-PREREQUISITES.md are superseded for this experiment. Only the specific observed relationships in the new report are corroborated; this does not promote all historical or current-build semantics to verified. Prior notes and evidence are retained unchanged.

Purpose: locate the original investigation, evidence, reproduction script and
tests behind every current technical claim. Organized by subject and
dependency, not alphabetically. Historical notes are archival: they are not
rewritten when superseded; corrections live in the canonical documents listed
here and link back.

The original three recordings share one independent source, as recorded in
[the sample manifest](../samples/manifest.json). Later acquisition and controlled
recording are documented above; they do not retroactively broaden the original
census or establish universal compatibility.

Conventions used below:

- Build: WarGame3.exe build 59638 unless stated, SHA-256
  `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`
  (inventory: `samples/game-binaries.json`). File offset = VA - 0x401000 + 0x400.
- Samples: `samples/manifest.json` (Sample1, Sample3 build 59638; Sample2 build
  510117427, semantics `inferred`). Replays and binaries are external
  prerequisites, not in Git.
- Evidence records: `research/evidence/ev_<sha256>.json` are REA MCP captures
  (operation, parameters, raw result). Notes cite them by `ev_` prefix.
- Provenance status codes: **S** standalone reproduction script, **T**
  automated regression tests, **E** archived static-analysis evidence file,
  **N** historical notes only, **G** validated against observed gameplay
  (none in the historical rows below; the current-build observation is linked above), **X** not independently reproduced.
- Generated counts: `research/coverage.json` (structural),
  `research/timeline-coverage.json` (timeline), regenerated by
  `research/coverage.py` and `research/timeline_coverage.py`.

Preservation baseline for the 2026-10-26 maintenance milestone:
`research/maintenance/preservation-manifest.json` (tracked research files;
verify with `research/maintenance/preservation_manifest.py verify`) and
`research/maintenance/work-artifacts-manifest.json` (git-ignored `work/`
artifacts; see `research/maintenance/WORK-ARTIFACTS.md`, verify with
`research/maintenance/work_artifacts_verify.py`).

Evidence recovery: eight REA evidence IDs cited in `REA-NOTES-59638.md`
Sessions 1-3 (ev_b44efd7d, ev_7841a093, ev_4ea358ce, ev_1e924a6e, ev_37b97e85,
ev_d3d3f966, ev_0ea526f5, ev_06018019) had no record file in `research/evidence/`
at the start of the maintenance milestone. They were recovered from 2026-10-23
session transcripts and added; provenance and limitations in
`research/evidence/RECOVERED-2026-10-26.md`. Rows citing them are marked **E\*** (record
recovered from transcript, not from the original REA store).

## 1. ESAV container and integrity validation

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| ESAV v1 header, declared length, SHA-224 over file[0x28:], 'rply' JSON chunk | `FORMAT.md` | `REPLAY-RESEARCH.md` Phase 2; `REA-NOTES-59638.md` Findings 1-6 (FUN_010b9300 header reader, FUN_010b9790 ntohl u32, SHA-224 init FUN_016fd070) | ev_b44efd7d…, ev_7841a093… (Ghidra; recovered); rizin pd sites in notes | E\*, T (`tests/test_wgrd_replay.py`) |
| Executable accepts version <= 1; decoder accepts only 1 (policy, NEXT-STEPS 4) | `FORMAT.md`, `NEXT-STEPS.md` | `REA-NOTES-59638.md` Parser comparison | notes | N |
| this[5] digest origin / mismatch fatality | open | `REA-NOTES-59638.md` Open | none | X |

## 2. Replay framing and command extraction

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| star / pact x S / endt frame; pact = u32 frame, u32 slot, u32 count, u16 len + block | `FORMAT.md` | `REA-NOTES-59638.md` Session 3 items 11-14 (FUN_00b3db10 frame loop, FUN_00b3ea20 pact consumer, FUN_00b29440 block reader, FUN_00b2c170 store) | ev_4ea358ce…, ev_1e924a6e…, ev_37b97e85…, ev_d3d3f966… (recovered) | E\*, T |
| Counted command loop (count copied from third pact u32; NULL creator continues; exact-EOF is decoder policy) | `FORMAT.md`, `research/COMMAND-LAYOUTS.md` | `research/count-loop.md`; `REA-NOTES-59638.md` Session 4 | ev_* cited in count-loop.md; `research/chatgpt-session-2026-10-23/outputs/wgrd-count-loop-*` | E, T |
| 594/594 multi-command blocks split; 571 complete, 23 framed (opaque 0x0D) | `research/coverage.json` | `research/COMMAND-LAYOUTS.md`; `REPLAY-RESEARCH.md` counted-block milestone | coverage script | S (`research/coverage.py`), T |
| Frame duration (tick -> seconds) | open | `REA-NOTES-59638.md`; `research/TIMELINE-SEMANTICS.md` "Player identity and time" | two bounded clock passes, negative | X |

## 3. Dispatcher and executable function analysis

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| Opcode dispatcher FUN_00b24050, jump table 0xb241f4 (33 dwords), case = push esi; call creator | `REA-NOTES-59638.md` Session 3 items 15-16 | same | rizin pd; Python table read | E, S (`research/op0c_layout.py`, `research/op_fixed_layout.py` re-resolve the table), T (`tests/test_fixed_opcodes.py`) |
| RTTI class names 0x02..0x22 (TNetworkAction*) | `wgrd_replay.py` OPCODE_CLASSES | `REA-NOTES-59638.md` Session 3 | RTTI | E |
| Packet reader TNetworkPacketReaderFromStream::Read (vtbl slot 1), raw LE copies | `REA-NOTES-59638.md` item 19 | same | rizin pd | E |
| Generic helper readers: FUN_00b35cd0 (u32 count + u32 array), FUN_00b35fc0 (same, element <= 0x0e), FUN_00b290c0 (count + 16-byte point, kind <= 6), FUN_00b29080 (u32 + raw16), FUN_008fb4a0 (u16 string) | `research/CHANGEPRODUCTION-0C.md`; `REA-NOTES-59638.md` | same | rizin pdf (2026-10-26) | S, T |

## 4. Individual opcode layouts

Canonical table: `research/COMMAND-LAYOUTS.md`. Implementation:
`wgrd_replay.py::_decode_command`.

| Opcode | Class | Creator | Original note | Repro | Tests | Status |
|---|---|---|---|---|---|---|
| 0x02 Surrender | 22 B fixed | FUN_00b30660 | `research/FIXED-OPCODES-02-13-18.md`; evidence `research/evidence/rizin-creators-02-13-18-59638.txt` | `research/op_fixed_layout.py` | `tests/test_fixed_opcodes.py` | S, T, E |
| 0x04 CommitOptionPlayer, 0x09 CancelFumigene, 0x0A AnnuleProduction | FUN_00b2edc0 / FUN_00b2e870 | `research/COMMAND-LAYOUTS.md` | ev_* in note | coverage | `tests/test_wgrd_replay.py`, `tests/test_production.py` | E, T |
| 0x07 GiveOrderStandard | FUN_00b2f850, helper FUN_00b35e30 (20-byte references) | `research/OP07-ORDERS.md`, `research/OP07-PLAN.md` (plan) | ev_* in note; `research/op07_coverage.py` | `tests/test_orders.py` | E, T |
| 0x08 LaunchFumigene | FUN_00b2fbc0, 39+T bytes | `REA-NOTES-59638.md` Session 3 | ev_0ea526f5…, ev_06018019… (recovered) | `tests/test_wgrd_replay.py` | E\*, T |
| 0x0C ChangeProduction | FUN_00b2eeb0, variable | `research/CHANGEPRODUCTION-0C.md` | `research/op0c_layout.py` | `tests/test_op0c_layout.py`, `tests/test_op0c_decoder.py`, `tests/test_timeline_0c.py` | S, T |
| 0x0D ProductionUnite | FUN_00b28ef0 -> FUN_00b584e0 / FUN_00b580a0 serializer envelope; interiors per `research/PRODUCTION-COMMANDS.md` | `research/PRODUCTION-COMMANDS.md`, `research/PRODUCTION-PLAN.md`; `research/evidence/production59638-native.json` | `research/production_coverage.py`, `research/production_evidence.py` | `tests/test_production.py` | E, T |
| 0x0E ItemFinished, 0x17 DeactivateWeapon | FUN_00b2f9e0, FUN_00b2f3b0 | `research/COMMAND-LAYOUTS.md` | ev_* in note | | `tests/test_wgrd_replay.py` | E, T |
| 0x13 PlayerSynchroServiceAction | 13 B fixed, FUN_00b2fdd0 | `research/FIXED-OPCODES-02-13-18.md` | `research/op_fixed_layout.py` | `tests/test_fixed_opcodes.py` | S, T, E |
| 0x18 DeactivateSupply | 10 B fixed, FUN_00b2f2e0 | `research/FIXED-OPCODES-02-13-18.md` | `research/op_fixed_layout.py` | `tests/test_fixed_opcodes.py` | S, T, E |
| 0x0B, 0x0F-0x12, 0x14-0x16, 0x19-0x22 | no authentic occurrences | `REA-NOTES-59638.md` Session 3 | RTTI only | | X |

## 5. Entity references and GUID relationships

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| 0x07 wire reference = u32 registry key + 16-byte validation GUID (b2e070, 4f715e `%x:%x:%x:%x`) | `research/ENTITY-CONTEXT.md` | same; `research/ENTITY-CONTEXT-PLAN.md` | ev_* in note; `research/entity_coverage.py`, `entity-coverage.json`, `entity-cli-validation.json` | E, T (`tests/test_entities.py`) |
| Reference catalog (per-replay IDs, lookup_key_ambiguous, shared GUIDs not merged) | `wgrd_entities.py::build_reference_catalog` | `research/ENTITY-CONTEXT.md` | coverage | T |
| 0x18 obj+0x04 is a 0x07 registry key (18/18, chance <= 2.7e-10) | `research/OP18-REFERENCE-KEYS.md` | same | data-only | S (`research/op18_reference_keys.py`), T (`tests/test_op18_reference_keys.py`) |
| 0x18 targets resolve uniquely; all 44 are supply unit types (independent corroboration of RTTI name) | `research/OP18-SUPPLY-TARGETS.md`; `research/TIMELINE-SEMANTICS.md` 0x18 section | same | data + static NDF | S (`research/op18_supply_targets.py`), T (`tests/test_timeline_0x18.py`) |
| Validation GUID = unit descriptor GUID (public datasets, 726/726 exact) | `research/PUBLIC-UNIT-MAPPING.md` | same; `research/PUBLIC-UNIT-PLAN.md` | `public-unit-coverage.json`, `public-unit-sources.json`, `research/public_unit_coverage.py` | E, T (`tests/test_unit_data.py`, skips without snapshot) |

## 6. NDF data and unit descriptors

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| Original 59638 NDF archive integrity, everything.ndfbin extraction (read-only, outputs in ignored `work/ndf59638/`; see `research/maintenance/WORK-ARTIFACTS.md`) | `research/NDF59638-BRIDGE.md` | same; `research/ndf59638_unpack.py`, `ndf59638_parse.py`, `ndf59638-extraction.json`, `ndf59638-format-sources.json` | archive SHA1/size in note | S (needs the original archive), E |
| CompanyUnit -> selector -> CompanyDescriptor static bridge (2121 paths, no ambiguity) | `research/NDF59638-BRIDGE.md`, `research/COMPANY-BRIDGE.md` | `research/COMPANY-BRIDGE-PLAN.md` (plan) | `research/ndf59638_bridge.py`, `ndf59638-bridge-coverage.json`, ev_c71bc22a…, ev_1de49c5f…, ev_5c5c9e64… | S, E |
| Versioned unit index `research/unit-data/build59638-v1.json.gz` + manifest and source hashes; localization | `research/TIMELINE-59638.md` | `research/TIMELINE-59638-PLAN.md`; `research/export_unit_index59638.py` | `research/unit-data/*.json` | S, T (`tests/test_unit_index.py`) |

## 7. Production and deployment commands

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| 0x0D variants 1/2/3 interiors (type bundle, deployment points, group quantities), 0x0A cancellation fields | `research/PRODUCTION-COMMANDS.md` | `research/PRODUCTION-PLAN.md` | `research/evidence/production59638-native.json`; `production-coverage.json` | E, T |
| 0x0C ChangeProduction raw-field interpretation (change_production_request) | `research/TIMELINE-SEMANTICS.md` 0x0C section | `research/CHANGEPRODUCTION-0C.md` | | T |
| Purchase correlation for 0x0A, 0x0B semantics, 0x0C field meanings | open | `research/PRODUCTION-COMMANDS.md`, `NEXT-STEPS.md` | | X |

## 8. Timeline reconstruction

| Finding | Canonical | Original note | Evidence | Status |
|---|---|---|---|---|
| `wgrd_timeline/1` event list; status vocabulary verified/partial/opaque/unknown/inferred | `research/TIMELINE-SEMANTICS.md` (export contract) | `research/TIMELINE-PLAN.md` | `timeline-coverage.json`, `timeline-cli-validation.json` | S (`research/timeline_coverage.py`), T (`tests/test_timeline.py`) |
| 08/09 marker create/remove execution handlers | `research/TIMELINE-SEMANTICS.md` | same | ev_* in note | E, T |
| Sample1 enriched timeline validation and battle report | `research/SAMPLE1-TIMELINE-VALIDATION.md`, `research/reports/sample1/` | `research/sample1_battle_report.py`; archived `research/chatgpt-session-2026-10-23/outputs/` | measurements JSON | S, N |

## 9. Semantic interpretation

| Topic | State | Where |
|---|---|---|
| Player slot -> metadata identity | unresolved | `research/TIMELINE-SEMANTICS.md`, `NEXT-STEPS.md` 7 |
| Player-id convention 0xC000001E + slot in 0x08/0x0C/0x02 | observed, consistent across three opcodes | `REA-NOTES-59638.md`, `research/CHANGEPRODUCTION-0C.md`, `research/FIXED-OPCODES-02-13-18.md` |
| Coordinates (axes, units), 0x08 types 0/1/2 | unresolved | `NEXT-STEPS.md` 8 |
| 0x0C obj+0x34 enum, obj+0xe8 float-like values | TENTATIVE, consumer not traced (deferred) | `research/CHANGEPRODUCTION-0C.md`, `research/ROADMAP-2026-10-26.md` |
| Outcomes (kills, positions over time, scores) | not observed in three samples; absence from format not established | `README.md`, `research/ROADMAP-2026-10-26.md` |

## 10. Runtime and ground-truth feasibility

| Finding | Canonical | Original note | Status |
|---|---|---|---|
| Local macOS cannot run the original; prerequisites census; TPositionModule candidate | `research/RUNTIME59638-FEASIBILITY.md` | same; `research/runtime59638_prerequisites.py`, `runtime59638-*.json` | S, N |
| 2026-10-26 checkpoint: Parallels guest has WRD fully installed incl. exact 59638 binary and NDF; no replays found then; blockers and recording protocol | `research/GROUND-TRUTH-PREREQUISITES.md` | same | N (Parallels MCP probe output quoted; see current-build correction above) |

## 11. Historical session archives

- `research/chatgpt-session-2026-10-23/`: outputs (Sample1 battle report HTML/MD/CSV, count-loop evidence and report) and work (REA MCP probe script, tool schemas, raw MCP responses, stderr log). Archival; do not edit.
- `research/*-PLAN.md`, `research/PLAN.md`: bounded plans that preceded each milestone. Archival.
- `research/ROADMAP-2026-10-26.md`: assessment and ranked plan from the Fable evaluation session; priorities now maintained in `NEXT-STEPS.md`.
- `REPLAY-RESEARCH.md`: phase log of the initial investigation.
- `research/evidence/work-archive-2026-10-26/`: hash-verified copies of the rizin .asm excerpts, raw REA MCP responses, probe scripts and logs that previously existed only in git-ignored `work/` (mapping in `research/maintenance/work-artifacts-manifest.json`).
- `research/reports/sample1/app-content/`: authored content of the Sample1 report app (runtime not tracked).
- `research/maintenance/`: preservation manifests and verifiers, link checker.
- `research/session-records/`: per-session reports.

## 12. Open investigations and unresolved evidence

Maintained in `NEXT-STEPS.md`. Current open items with evidence pointers:
this[5] digest origin; frame duration; player identities and star L=34/60
payloads; 0x08 remaining fields; 0x0D nested serializer interiors (23 framed
blocks); 0x0A purchase correlation; 0x0C consumer trace; FUN_004e6d80,
FUN_004fcc00, FUN_004f94a0, FUN_00522ec0 semantics; further controlled ground-truth recordings.

## External prerequisites (not in Git)

| Artifact | Location convention | Identity |
|---|---|---|
| Replay samples | `WGRD_SAMPLES_DIR`, default `~/.hermes/artifacts/wgrd-replay/samples/raw/` | `samples/manifest.json` SHA-256 |
| WarGame3.exe builds | `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/<build>/`; `WGRD_EXE_59638` | `samples/game-binaries.json` |
| Original 59638 NDF archive and `work/ndf59638/` extraction | local, regenerated by `research/ndf59638_unpack.py` | size/SHA1 in `research/NDF59638-BRIDGE.md` |
| Public unit snapshot | `WGRD_UNIT_DATA`, default `work/public-units/wargame-data` | `research/public-unit-sources.json` |

## Project credits

The repository owner directed and reviewed the work. Earlier research and
implementation ran through [Hermes Agent](https://hermes-agent.nousresearch.com)
and the Nous Portal; this documentation redesign was carried out in OpenAI Codex.

| Contributor | Work |
|---|---|
| Claude Fable 5.1 (Anthropic) | Technical lead for the 2026-10-26 build-59638 investigation: `0x0C` creator/helpers, fixed `0x02`/`0x13`/`0x18` layouts and `0x18` reference keys; assessment, roadmap, review and integration |
| Claude Haiku 5.5 (Anthropic) | Decoder implementation, regression tests, coverage and implementation docs for those opcodes, including the `0x0C` timeline; isolated worktrees under lead review. Bounded support for the October 28 experiment is recorded in its report |
| GPT-6 Astra (OpenAI) | Lead for the October 28 controlled recording and playback experiment; VM control, interpretation, integration and verification |
| GPT-6.1 Terra (OpenAI) | October 28 follow-up work, maintenance and documentation |
| OpenAI Codex | Repository-wide documentation audit and redesign, technical reference corrections, navigation and publication |
| ASCII cow in `wgrd_orders.py` | Maintainer |

### Historical acknowledgment

GLM 5.3-flash: The context-collapse spiral. Not every contribution advances the decoder.

Earlier container, framing, command, NDF and timeline investigations are recorded
in [the investigation log](../REPLAY-RESEARCH.md), [REA notes](../REA-NOTES-59638.md)
and [the session archive](chatgpt-session-2026-10-23/).
The [October 28 experiment report](current-build/2026-10-28-controlled-experiment.md#11-model-attribution-and-cost-accounting)
records its model roles and usage. The [research index](INDEX.md) connects
findings to evidence, reproduction scripts and tests; not every historical finding
has a standalone reproducer.

Tools used include rizin, Ghidra, REA MCP and Python's standard library.
The [Sample1 battle report](reports/sample1/) was authored with
Codex/ChatGPT's `build-report` skill on OpenAI's `data-app` runtime. Authored
content and a self-contained HTML build are preserved; the runtime is external.

The [archived priorities](NEXT-STEPS-2026-10-28.md) retain the earlier roadmap and milestone details. Current priorities live in the root [NEXT-STEPS.md](../NEXT-STEPS.md).
