# Evidence index

[Project overview](../README.md) · [Format reference](../FORMAT.md) · [Architecture](../docs/ARCHITECTURE.md) · [Status](../NEXT-STEPS.md)

This index lists the evidence behind current claims. Current behavior is defined by the code, [FORMAT.md](../FORMAT.md) and [ARCHITECTURE.md](../docs/ARCHITECTURE.md). Notes in `research/` are dated evidence records. They are not rewritten when superseded, and they are not instructions.

Status codes: **S** reproduction script, **T** regression tests, **E** static-analysis evidence file (**E\*** recovered from a session transcript), **N** notes only, **X** not independently reproduced.

## Conventions

- **Historical build:** WarGame3.exe build 59638, SHA-256 `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`. Its file offset is VA - 0x401000 + 0x400.
- **Current build:** internal revision 131544, SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
- **Inventories:** samples are in [`samples/manifest.json`](../samples/manifest.json) and binaries in [`samples/game-binaries.json`](../samples/game-binaries.json). Replays and executables live outside Git.
- **Evidence files:** `evidence/ev_<sha256>.json` records are REA captures. Notes cite them by their `ev_` prefix. The repository keeps only the records cited by code or by a kept note.

## Current build (revision 131544): original-engine AAR

| Topic | Note | Code and tests |
|---|---|---|
| **Evidence-bounded AAR release (final)** | [AAR release](current-build/2026-11-02-aar-release.md) | `instrumentation/aar_events.py`, `tests/test_aar_release.py` |
| Damage producer, source credit, Killed token, ownership | [causal chain](current-build/2026-11-02-causal-chain.md) | `instrumentation/aar_events.py`, `tests/test_aar_events.py` |
| Runtime lifecycle export | [runtime AAR](current-build/2026-11-02-runtime-aar.md) | same |
| Native positions (V3) | [position AAR](current-build/2026-11-02-position-aar.md) | same |
| Build-matched unit index | [unit data](current-build/2026-11-02-unit-data.md) | `research/aar_unit_index.py`, `tests/test_aar_unit_index.py` |
| Engine state and guarded guest input | [engine state](current-build/2026-11-02-engine-state.md) | `instrumentation/state_observe.py`, `instrumentation/WgrdUi.cs` |
| Offline corpus and order queue on the current executable | [offline corpus](current-build/2026-10-29-offline-corpus.md) | `research/offline_corpus.py`, `tests/test_offline_corpus.py` |
| Clock and actor hypotheses (H1-H3) | [NEXT-STEPS.md](../NEXT-STEPS.md) | `tests/test_aar_hypotheses.py` |

The 2026-10-28 controlled recording ("Oshkosh Incident") report is archived. Its screenshots are in the GitHub release `oshkosh-incident-2026-10-28-v1`. Its playback regression manifest is still maintained: [`samples/cross-build-manifest.json`](../samples/cross-build-manifest.json), checked by `tests/test_cross_build_corpus.py`.

## Format and decoder evidence (build 59638)

| Subject | Canonical note | Repro / tests | Status |
|---|---|---|---|
| ESAV header, SHA-224 over file[0x28:], chunk reader, `rply` JSON chunk | [REA notes](REA-NOTES-59638.md) Findings 1-10 | `tests/test_wgrd_replay.py` | E\*, T |
| Frames, pact layout, counted command loop | [REA notes](REA-NOTES-59638.md) Sessions 3-4; [count loop](count-loop.md) | `tests/test_wgrd_replay.py` | E, T |
| Dispatcher, jump table, RTTI opcode classes | [REA notes](REA-NOTES-59638.md) Session 3 | `research/op_fixed_layout.py`, `tests/test_fixed_opcodes.py` | E, S, T |
| Per-opcode layouts (04/07/08/09/0A/0E/17) | [command layouts](COMMAND-LAYOUTS.md) | `tests/test_wgrd_replay.py`, `tests/test_production.py` | E, T |
| 0x02 / 0x13 / 0x18 fixed layouts | [fixed opcodes](FIXED-OPCODES-02-13-18.md) | `research/op_fixed_layout.py`, `tests/test_fixed_opcodes.py` | E, S, T |
| 0x07 orders: requested kind, references | [0x07 orders](OP07-ORDERS.md) | `tests/test_orders.py` | E, T |
| 0x0C ChangeProduction | [0x0C](CHANGEPRODUCTION-0C.md) | `research/op0c_layout.py`, `tests/test_op0c_decoder.py`, `tests/test_timeline_0c.py` | S, T |
| 0x0D / 0x0A production interiors | [production commands](PRODUCTION-COMMANDS.md); `evidence/production59638-native.json` | `tests/test_production.py` | E, T |
| References: u32 registry key + 16-byte validation GUID | [entity context](ENTITY-CONTEXT.md) | `tests/test_entities.py` | E, T |
| 0x18 registry keys and supply targets | [reference keys](OP18-REFERENCE-KEYS.md), [supply targets](OP18-SUPPLY-TARGETS.md) | `research/op18_reference_keys.py`, `research/op18_supply_targets.py`, `tests/test_op18_reference_keys.py`, `tests/test_timeline_0x18.py` | S, T |
| Validation GUID = unit descriptor GUID (public data) | [public unit mapping](PUBLIC-UNIT-MAPPING.md) | `tests/test_unit_data.py` | E, T |
| Original NDF extraction, company bridge, unit index | [NDF bridge](NDF59638-BRIDGE.md) | `research/ndf59638_unpack.py`, `research/ndf59638_parse.py`, `research/ndf59638_bridge.py`, `research/export_unit_index59638.py`, `tests/test_unit_index.py` | S, E, T |
| Timeline contract and handler semantics | [timeline semantics](TIMELINE-SEMANTICS.md) | `tests/test_timeline.py` | E, T |

Unresolved items are in [NEXT-STEPS.md](../NEXT-STEPS.md).

## Archive

On 2026-11-02, the research files not listed above were retired from the active tree. They are plans, roadmaps, handoffs, reviews, session records, superseded dated notes, generated coverage reports and their generators, raw REA/rizin dumps, the ChatGPT session export, the Sample1 report and the 2026-10-28 report and screenshots. Two independent copies exist:

- **Git:** `git show 6a728b7:<path>` restores any file. That commit is the parent of the removal commit and is on the remote.
- **Private archive:** `~/.hermes/artifacts/wgrd-replay/research-archive-20261102/` holds a `git archive` tarball plus `MANIFEST.json` (path, size, SHA-256, blob ID). Its README gives the restore check, which was verified for every file before removal.

Text that still names an archived file marks it `(archived: path)`.

## External prerequisites (not in Git)

| Artifact | Location convention | Identity |
|---|---|---|
| Replay samples | `WGRD_SAMPLES_DIR`, default `~/.hermes/artifacts/wgrd-replay/samples/raw/` | `samples/manifest.json` SHA-256 |
| WarGame3.exe builds | `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/<build>/`; `WGRD_EXE_59638` | `samples/game-binaries.json` |
| Original 59638 NDF archive and `work/ndf59638/` extraction | local, regenerated by `research/ndf59638_unpack.py` | size/SHA1 in `research/NDF59638-BRIDGE.md` |
| Public unit snapshot | `WGRD_UNIT_DATA`, default `work/public-units/wargame-data` | `research/public-unit-sources.json` |
| AAR traces, 131544 unit index, static REA envelopes | `~/.hermes/artifacts/wgrd-replay/aar-*` | hashes pinned in `tests/test_aar_hypotheses.py` and the notes |

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

Tools used include rizin, Ghidra, REA MCP and Python's standard library. The
October 28 experiment report (archived) records its model roles and usage.
[The ASCII Dragon Incident](DRAGON-INCIDENT.md) explains another well-defended
corner of the project.
