# AGENTS.md

Instructions for AI agents working in this repository. Facts only; the linked files hold the details.

## 1. Project purpose

wgrd-replay is a stdlib-only Python decoder for Wargame: Red Dragon `.wargamerpl2` replay files.

- **Parsing (done for build 59638):** the ESAV container, SHA-224 digest, star/pact/endt chunks, and the
  command-block split are checked strictly. Container violations raise `ReplayFormatError`; malformed command blocks retain diagnostics and fail timeline export. Metadata object shapes are validated explicitly (section 13).
- **Interpreting (partial):** a subset of opcodes is given action meanings, with status labels and evidence references.
  Gameplay meaning is not established for most fields, and execution outcomes are never asserted.

Byte-level layout: `FORMAT.md`. Pipeline and status vocabularies: `docs/ARCHITECTURE.md`.

## 2. Repository map

Verified paths at the repo root:

- `wgrd_replay.py` — container, chunks, `_decode_command`, `parse_replay`, CLI (`main`, argparse near line 408).
- `wgrd_timeline.py` — `build_timeline`, per-event interpretation, reference catalog and unit-data hook.
- `wgrd_entities.py` — `reference_components`, `build_reference_catalog`, `attribute_supply_requests`.
- `wgrd_orders.py` — opcode 0x07 interpretation.
- `wgrd_production.py` — opcode 0x0A/0x0D/0x0C interpretation.
- `wgrd_unit_data.py`, `wgrd_unit_index.py` — static build 59638 NDF index join (opt-in).
- `README.md`, `FORMAT.md`, `REA-NOTES-59638.md`, `REPLAY-RESEARCH.md`, `NEXT-STEPS.md` — root docs.
- `docs/ARCHITECTURE.md` — canonical pipeline overview.
- `tests/` — `unittest` suite (`test_*.py`).
- `samples/manifest.json`, `samples/game-binaries.json` — external artifact inventory (no bytes in Git).
- `research/` — per-topic notes (`*.md`), `*-PLAN.md` historical plans, reproduction scripts (`*.py`),
  generated coverage JSON, `research/evidence/` (REA `ev_*.json` records and disassembly excerpts),
  `research/unit-data/` (versioned index and manifest), `research/chatgpt-session-2026-10-23/` (archived outputs).
- `research/INDEX.md` — research provenance index.
- `research/current-build/` — revision 131544 experiment, evidence ledger, helper history and Phase 2 handoff.
- `work/` — git-ignored local scratch (NDF extraction outputs). Not committable.

## 3. Start here

Read in this order:

1. `README.md` — usage and scope.
2. `NEXT-STEPS.md` — current priorities.
3. `docs/ARCHITECTURE.md` — pipeline, status vocabularies, opcode-to-file map.
4. `research/INDEX.md` — where prior findings are recorded.
5. For revision 131544, read `research/current-build/PHASE-2-HANDOFF.md` and its linked experiment and evidence; otherwise read the task-specific research note.
6. `tests/` and the code in the relevant module.

## 4. Current technical baseline

Definitions used across the docs:

- **structurally decoded** — bytes parsed by a layout with exact consumption; proves boundaries, not meaning.
- **framed-opaque** — boundary known from a length prefix; interior not decoded (0x0D serializer body).
- **semantically interpreted (partial)** — an action meaning is assigned with a `partial` or `verified` status and listed limitations.
- **inferred** — the same layout/meaning applied to a replay whose build is not 59638.
- **ground-truth verified** — sample-specific UI/recording evidence now exists for the controlled 131544 experiment; no general execution-outcome guarantee. See `research/current-build/2026-10-28-controlled-experiment.md`.

Authoritative counts are in `research/coverage.json` and `research/timeline-coverage.json`. Do not copy numbers into docs;
read the files or regenerate them.

## 5. Build awareness

- All verified layouts apply to `WarGame3.exe` build **59638**, SHA-256
  `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`.
- Hashes for other builds are in `samples/game-binaries.json`.
- `Sample2` is build `510117427` and its interpretations are marked `inferred`.
- The controlled experiment used internal revision **131544** and Steam content build **15652829**; these are different identifiers. See the current-build report and cross-build manifest.
- Do not assume the installed game's root executable is 59638. Check its SHA-256 before using it as evidence.

## 6. Research workflow

1. Search `research/INDEX.md` and existing notes before starting. Do not redo recorded work.
2. State a falsifiable hypothesis (what byte pattern, value, or control flow would prove or disprove it).
3. For executable research, identify and hash the matching build before targeted rizin/REA queries. The existing creator and consumer traces concern historical build 59638, not automatically revision 131544. Do not repeat completed analysis without a specific question.
4. Preserve evidence under `research/evidence/` (hash-named JSON) or as a note; do not keep only in chat.
5. Separate observation (bytes, disassembly, sample values) from interpretation (names, meanings). Label each.
6. Validate against the relevant authenticated samples in `samples/manifest.json` and `samples/cross-build-manifest.json`. A result on one sample is not a general claim.
7. Add or update a reproduction script that exits non-zero on failure.
8. Add or update tests in `tests/`.
9. Update the canonical document for the topic (`docs/ARCHITECTURE.md`) and link the new evidence.

## 7. Evidence standards

Every claim about the binary or format cites:

- build and executable SHA-256 (59638 unless stated);
- virtual address (VA) and file offset, where **file offset = VA − 0x401000 + 0x400** for the `.text` section
  (`REA-NOTES-59638.md`);
- the bytes or disassembly excerpt, or the evidence record path;
- sample identity (file name and SHA-256 from `samples/manifest.json`);
- a reproduction command;
- test results, if code depends on the claim.

Confidence labels, as used in `REA-NOTES-59638.md`:

- **CONFIRMED** — reproduced from bytes or code, with the evidence above.
- **STRONGLY SUPPORTED** — multiple consistent observations; one step not directly reproduced.
- **TENTATIVE** — plausible from one source; stated as such.
- **UNRESOLVED** — not determined. Say so; do not fill the gap.

Exact byte consumption proves the structure of a block. It does not prove what a field means.

## 8. Coding conventions

Verified from the code:

- Python 3 standard library only. No third-party imports.
- Container violations raise `ReplayFormatError`. Command-block violations are retained as `malformed` diagnostics; timeline export rejects them. Do not skip, guess, or silently truncate.
- Raw bytes are preserved in output (`raw_hex`, `remaining_hex`, `*_hex` fields).
- Field names follow `obj_XX_u32 | obj_XX_hex | obj_XX_u8 | obj_XX_array | obj_XX_points`, where XX is the creator
  object offset. Semantic names are added only with cited evidence.
- CLI output is strict JSON. Non-finite values are written as `{"nonfinite": "+Infinity"}` (or `NaN` / `-Infinity`); parser dictionaries may retain floats.
- Do not rename or remove existing output keys. Add new keys beside them.
- Coverage JSON is regenerated by the scripts in `research/`. Explain the diff in the commit message or the note.
- Do not hand-edit generated JSON.

## 9. Testing and verification

Run from the repo root. The commands below were run in this worktree; re-run after changes.

```
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

Report the actual run and skips, not a fixed expected total. The pinned public-unit snapshot test skips when its data is absent; other external corpus or executable tests can also skip when their artifacts are unavailable. The 2026-10-28 run had 139 tests and no skips with its artifacts available; see the current-build report for that historical result. A later run at commit 2bde168 (2026-10-28) executed 148 tests, OK, with no skips. Both figures are dated records; neither is the standing count.

```
python3 -B research/maintenance/check_links.py
```

Exits 1 for references it cannot resolve; path-like prose and intentionally external references can produce warnings. It does not modify files. The 2026-10-28 baseline had 32 warnings. At commit 2bde168 the same checker reported 31 missing references; the difference from the 32 in the experiment report has not been reconciled. Compare and classify findings rather than assuming each is a broken link.

Corpus tests skip when authentic samples are absent. Environment variables:

- `WGRD_SAMPLES_DIR` — default `~/.hermes/artifacts/wgrd-replay/samples/raw`.
- `WGRD_ARTIFACTS_DIR` — default `~/.hermes/artifacts/wgrd-replay`; used by cross-build corpus tests.
- `WGRD_EXE_59638` — default `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe`.
- `WGRD_UNIT_DATA` — path to a unit index or pinned public directory.

A skip is not a pass. Report skip counts and reasons when reporting results.

CLI check, after tests:

```
python3 wgrd_replay.py SAMPLE --summary
python3 wgrd_replay.py SAMPLE --timeline [--unit-data research/unit-data/build59638-v1.json.gz]
```

`SAMPLE` is a replay path, e.g. `~/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample1.wargamerpl2`.
`--unit-data` requires `--timeline` (otherwise exit 2).

## 10. Git and worktree practices

- Keep changes focused. One topic per commit.
- One writer per worktree. Do not run two agents in the same worktree.
- Review diffs before merging. Run the tests after integration, not only before.
- Stage files explicitly (`git add <path>`). Do not use `git add -A` or `git add .`.
- Never force-push. Never reset or rewrite published history.
- After pushing, verify the remote with `git ls-remote origin <branch>` or equivalent.
- This file does not grant permission for destructive operations (delete, reset, force, history rewrite, cleanup of
  research material). Those require explicit user approval.

## 11. Research preservation

- Do not discard research notes, evidence files, hashes, or addresses during cleanup.
- Use `research/INDEX.md` to locate findings. Keep it updated when files move.
- When moving a file, keep its provenance (where it came from, which sample or build it used) in the new location.
- Correct errors by adding a dated correction note or a "superseded by" line. Do not rewrite history.
- Historical plans (`*-PLAN.md`) are records, not current instructions. Read `NEXT-STEPS.md` for priorities.

## 12. Security and artifact handling

- Do not commit secrets, credentials, personal data, game binaries, game assets, or replay files.
- Replay bytes are untrusted input. Parse them only with the strict decoder; do not evaluate or execute content.
- Do not run unknown executables. Analysis of `WarGame3.exe` is static (rizin/REA) unless the user explicitly asks for runtime work.
- Do not commit large dumps. Keep bulk output in `work/` (git-ignored) and cite its path and hash instead.
- Sample redistribution is unclear (`samples/manifest.json`). Keep bytes outside Git.

## 13. Known limitations and next steps

- Ground-truth validation now includes the bounded 131544 controlled recording and completed playback documented in `research/current-build/2026-10-28-controlled-experiment.md`; general gameplay execution and most field semantics remain unverified.
- Field semantics for most opcodes are unconfirmed; `execution_outcome` is always `unknown`.
- All verified layouts are specific to build 59638. Other builds are inferred.
- The interior of 0x0D serializer bodies is opaque (boundary only).
- The 0x0C consumer analysis is deferred; field meanings there are TENTATIVE or unresolved.
- Entity attribution for 0x18 depends on per-replay key uniqueness and is not cross-replay identity.
- **2026-10-28 correction:** `parse_header` now raises `ReplayFormatError` for non-object metadata roots or present non-object `game` values. The earlier `AttributeError` leak (reproduced with `[]`) is fixed; see `tests/test_header_metadata.py`. Missing `game` or `Version` remains accepted.
- Priorities and open questions: `NEXT-STEPS.md`. Do not add a second roadmap in this file.
