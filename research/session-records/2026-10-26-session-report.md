# Session record: 2026-10-26 (Fable evaluation, development, maintenance)

Lead: Claude Fable 5.1 (Anthropic) via Nous Portal on Hermes Agent. Delegated
implementation: Claude Haiku 5.5, low reasoning effort, one writer per git
worktree, reviewed before merge. Direction and review gates: repository owner.

## 1. Development results

Starting state (8f2f64d): container, digest, framing and 594/594 multi-command
block splitting verified; layouts for 04/07/08/09/0A/0D(envelope)/0E/17; 112
single-command blocks unresolved (0c=47, 18=44, 13=16, 02=5); 81 tests.

Ending state (03e1a20 + this record): every one of the 10,942 non-empty blocks
is `complete` or `framed` (23 opaque 0x0D envelopes); zero unresolved blocks;
129 tests (1 skip without the public unit snapshot).

Opcode layouts recovered and implemented (all build 59638, exact corpus fit):

| Opcode | Creator | Layout | Corpus fit | Research | Tests |
|---|---|---|---|---|---|
| 0x0C ChangeProduction | FUN_00b2eeb0 | variable (helpers b35cd0, b35fc0, b290c0 x2, b29080) | 47/47 (two 281-byte variable blocks on Sample2) | research/CHANGEPRODUCTION-0C.md, op0c_layout.py | test_op0c_layout, test_op0c_decoder, test_timeline_0c |
| 0x02 Surrender | FUN_00b30660 | 22 B fixed | 5/5 | research/FIXED-OPCODES-02-13-18.md, op_fixed_layout.py | test_fixed_opcodes |
| 0x13 PlayerSynchroServiceAction | FUN_00b2fdd0 | 13 B fixed | 16/16 | same | same |
| 0x18 DeactivateSupply | FUN_00b2f2e0 | 10 B fixed | 44/44 | same | same |

Semantic/entity results:

- 0x18 obj+0x04 is a registry key in the 0x07 wire-reference space (18/18
  distinct keys, chance <= 2.7e-10). STRONGLY SUPPORTED. research/OP18-REFERENCE-KEYS.md.
- All 44 0x18 events resolve to exactly one 0x07 reference by a per-replay
  uniqueness + issuing-slot rule, and every resolved static unit type is a
  supply truck or logistics helicopter (baseline 4-6%). Independent
  corroboration of the RTTI class name. research/OP18-SUPPLY-TARGETS.md.
- Timeline: 0x0C events carry a raw-field `change_production_request`
  interpretation (status partial/inferred); 0x18 events carry
  `deactivate_supply_request` with target_reference (reference_id, GUID, unit
  type) assigned only when unambiguous; otherwise resolution is reported and
  nothing is assigned.
- Non-finite float32 values are emitted as `{"nonfinite": ...}` markers so the
  default CLI output is strict JSON.

Ground truth: the Parallels guest has WRD fully installed with the exact 59638
binary and NDF; no replays yet; blockers and a recording protocol are in
research/GROUND-TRUTH-PREREQUISITES.md.

## 2. Verification

- Test suite: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q`
  -> 129 tests OK, 1 skip (`test_all_726_exact_matches_no_contextual_resolution`,
  public unit snapshot not cached). Corpus and executable tests ran against
  the real samples and binary on this machine.
- Reproduction scripts, all exit 0 against the local artifacts:
  research/op0c_layout.py, op_fixed_layout.py, op18_reference_keys.py,
  op18_supply_targets.py.
- research/coverage.py and research/timeline_coverage.py regenerate
  byte-identical research/coverage.json and research/timeline-coverage.json.
- CLI `--timeline --unit-data` output on Sample1 parses as strict JSON (4162 events).
- Limitations: all semantics remain unverified against observed gameplay;
  Sample2 (build 510117427) is structural/inferred only; 0x0D interiors (23
  framed multi blocks, 514 envelopes) remain opaque; 0x0C/0x13/0x18 field
  meanings unconfirmed; frame duration and player identities unknown.

## 3. Research artifacts added

Notes: CHANGEPRODUCTION-0C.md, FIXED-OPCODES-02-13-18.md, OP18-REFERENCE-KEYS.md,
OP18-SUPPLY-TARGETS.md, GROUND-TRUTH-PREREQUISITES.md, ROADMAP-2026-10-26.md.
Scripts: op0c_layout.py, op_fixed_layout.py, op18_reference_keys.py,
op18_supply_targets.py. Evidence: research/evidence/rizin-creators-02-13-18-59638.txt
and eight recovered REA records (research/evidence/RECOVERED-2026-10-26.md).
Index: research/INDEX.md.

## 4. Repository maintenance

- No files were moved or deleted. Structure audited; existing layout kept.
- Added: AGENTS.md, docs/ARCHITECTURE.md, research/INDEX.md,
  research/maintenance/ (preservation_manifest.py + preservation-manifest.json,
  work_artifacts_verify.py + work-artifacts-manifest.json, WORK-ARTIFACTS.md,
  check_links.py), this record.
- Reconciled: FORMAT.md layout table (02/0C/13/18 rows), NEXT-STEPS.md
  (current priorities section; generated coverage declared authoritative),
  REA-NOTES-59638.md 0x0C section, README.md (status, documentation map,
  reproduction commands, next milestone, credits scoped accurately).
- Canonical references: FORMAT.md (format), research/COMMAND-LAYOUTS.md +
  per-opcode notes (layouts), research/TIMELINE-SEMANTICS.md (timeline),
  research/ENTITY-CONTEXT.md + OP18 notes (entities), docs/ARCHITECTURE.md
  (architecture), NEXT-STEPS.md (priorities), research/INDEX.md (provenance).
- Link check: remaining reports are external transcript filenames in
  RECOVERED-2026-10-26.md, filenames inside described work/ directories in
  WORK-ARTIFACTS.md, and one vocabulary string; no broken repository paths.
- Historical notes (research/*-PLAN.md, COMMAND-LAYOUTS chronology,
  chatgpt-session archive, REPLAY-RESEARCH.md) left byte-identical.

## 5. Preservation audit

1. All original research records present: yes (182 tracked research files in
   preservation-manifest.json verify OK; 4 intentional active-doc edits listed).
2. Original evidence artifacts present: yes; 93 evidence JSON records parse.
3. Historical files modified: none. Active docs modified: FORMAT.md,
   REA-NOTES-59638.md (2026-10-26 section only), NEXT-STEPS.md, README.md.
4. Files moved: none. 5. Files deleted: none.
6. Evidence identifiers discoverable: yes. Eight IDs cited by REA-NOTES
   Sessions 1-3 had no record file; recovered verbatim from 2026-10-23 session
   transcripts (Time Machine unreadable from this session: no Full Disk Access,
   APFS snapshot mount refused). Byte identity with the original REA store is
   not provable; schema and procedure addresses match the notes.
7. Hashes and function addresses preserved: yes (notes unchanged; INDEX cites them).
8. Reproduction scripts work: yes, all four plus coverage scripts.
9. Historical findings linked from the index: yes, with status codes.
10. Original investigation locatable from a current claim: yes via research/INDEX.md.

Archival risk remaining (not resolved this session, by design): git-ignored
work/ holds the only copies of 21 rizin .asm excerpts, 19 raw REA responses,
probe scripts, logs and the Sample1 report app source (about 11 MB). Manifest
and a recommended preservation strategy: research/maintenance/WORK-ARTIFACTS.md.
Nothing under work/ was changed.

## 6. Contributions

- Claude Fable 5.1: all executable analysis (jump table, creators, helper
  readers), data cross-references (0x18 keys, supply types), Parallels
  prerequisite probes, evidence recovery, provenance index, preservation
  manifests, documentation reconciliation, review and integration of every
  delegated change, commits and pushes.
- Claude Haiku 5.5 (five delegated runs, each in an isolated worktree):
  decoder branches for 0x0C and 0x02/0x13/0x18, timeline interpretations for
  0x0C and 0x18 attribution, regression tests (test_op0c_decoder,
  test_fixed_opcodes, test_timeline_0c, test_timeline_0x18,
  test_op18_reference_keys), coverage regeneration, AGENTS.md and
  docs/ARCHITECTURE.md drafts, check_links.py.
- Earlier sessions: see research/INDEX.md section 11.

## 7. Git history (all on origin/main, verified after each push)

e7fd1b9, e0039c6, e656eb6, 38e35d0, 586f196, 487d053, 995ca82, e30d5af,
3a4800a, fab8d6f, 080a027, e0223f1, 9f8e46f, 02b0c35, 681d8ee, c3b0698,
528e435, 478f3a3, 03e1a20, plus the README/session-record commit that adds
this file. 51 files changed, ~10k insertions since 8f2f64d.

## 8. Remaining work (priority order, see NEXT-STEPS.md)

1. Ground-truth replay acquisition and validation (user-authorized launch).
2. Frame-duration calibration (depends on 1).
3. Player slot identity and coordinate axes (depends on 1).
4. Deferred 0x0C consumer analysis (obj+0x34 enum, obj+0xe8 float).
5. Preserve work/ evidence per WORK-ARTIFACTS.md; 0x0D interiors; 0x0A
   purchase correlation; this[5] digest origin.

## 9. Cost and usage

Correction: an earlier version of this section said no telemetry was available.
That was wrong. Hermes state (~/.hermes/state.db, tables sessions and
session_model_usage) holds per-model token and call counts for this work.
actual_cost_usd is 0.0 on every row, so cost is an estimate only.

Measured token usage (from state.db; main session local-eb6ddffce182…,
subagent sessions 20261026_184523_97dd0f, 20261026_184523_3885e3,
20261026_190013_367b92, 20261026_191749_c9f8ef):

| Route | Calls | Input | Output | Cache read | Cache write | Reasoning | Est. cost |
|---|---|---|---|---|---|---|---|
| Fable 5.1 (lead) | 217 | 512 | 166,769 | 43,837,979 | 1,169,425 | 27,110 | 33.92 |
| gpt-6.1-sol (before switch) | 2 | 21,623 | 46 | 21,536 | 0 | 0 | 0.046 |
| Haiku 5.5 approval (lead) | 49 | 47,793 | 2,114 | 0 | 0 | 1,770 | 0.006 |
| Haiku 5.5 background_review | 21 | 54 | 29,723 | 1,242,968 | 458,625 | 17,933 | 0.085 |
| Haiku 5.5 subagents (4 sessions) | 72 | 168 | 69,821 | 3,902,152 | 245,391 | 19,763 | 0.105 |
| Haiku 5.5 approval (subagents) | 21 | 20,047 | 148 | 0 | 0 | 0 | 0.002 |
| Total | 382 | 90,197 | 268,621 | 49,004,635 | 1,873,441 | 66,576 | ~34.16 |

Notes: the lead's "input" column is small because most input was served from
cache (cache read). Subagent sessions count 93 calls in total (72 + 21).

Cost status: $34.16 is an ESTIMATE from pricing tables, not verified
expenditure. The user-reported spend of $11.87 of a $22 cap before Milestone 3
is lower than this estimate. The actual Nous Portal charge is not yet
reconciled. Do not treat either figure as final until it is.

Not measured: cost per completed, validated milestone, split by
investigation, implementation, review, and maintenance. Needs a per-phase
tagging scheme before it can be computed.
