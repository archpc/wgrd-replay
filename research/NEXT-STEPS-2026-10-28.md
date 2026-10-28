# Archived priorities: pre-rationalization checkpoint

Source: root NEXT-STEPS.md at remote main 460a3ab (2026-10-28), SHA-256
`d2f5931c03fe67d1c71076aabfdf0bdb733447676d15a0444f2e199b5a74e3a0`. Original text below; only relative
Markdown links adjusted for this location. Current priorities: [NEXT-STEPS.md](../NEXT-STEPS.md).

# NEXT-STEPS.md (prioritized)

## Current checkpoint (2026-10-28)

Acquisition and game launch are no longer blocked. A new offline revision-131544
recording was decoded and played back; two additional historical archive samples passed
the same runner. The full experiment, helper source/history, bounded ground-truth
findings, and unresolved questions are in [the controlled experiment
report](current-build/2026-10-28-controlled-experiment.md). Hash-pinned
expectations: samples/cross-build-manifest.json. General frame-to-seconds conversion,
movement outcomes, coordinate mapping, and marker/production-change/cancellation
validation remain unresolved. No version-specific decoder patch was required by these
samples.

Next controlled timing and movement work: [Phase 2
handoff](current-build/PHASE-2-HANDOFF.md). It is a plan, not authorization to
operate the VM.

## Prior priorities (2026-10-26; historical)

The acquisition/authorization blockers below are superseded by the checkpoint above;
retain the original record.

1. **Ground-truth replay.** Record a scripted match on the Parallels guest and validate
   07/08/0a/0c/0d/18 semantics, frame duration and coordinates against the action log.
   Prerequisites verified, blockers and protocol:
   research/GROUND-TRUTH-PREREQUISITES.md. Needs user authorization to launch.
2. **Frame duration.** Depends on 1; static passes failed (item 7 below).
3. **Player slot -> identity; coordinate axes.** Depends on 1 (items 7, 8).
4. **0x0C consumer trace** for obj+0x34 enum and obj+0xe8 float hypotheses
   (research/CHANGEPRODUCTION-0C.md; deferred, executable analysis).
5. **Preserve work/ evidence** per research/maintenance/WORK-ARTIFACTS.md (archival
   risk: original .asm excerpts and raw REA responses are ignored files).

Status counts below are historical checkpoints; research/coverage.json and
research/timeline-coverage.json are authoritative. Provenance: research/INDEX.md.

## Status and detailed items (2026-10-26; historical)

Milestone: **594/594 multi-command blocks split**, with exact count and EOF. 571
complete layouts; 23 explicitly opaque-framed blocks. All 10,942 non-empty blocks (multi
and single) are complete or framed; zero unresolved. 129 tests pass (1 skip without the
public unit snapshot). See research/COMMAND-LAYOUTS.md, research/coverage.json and
research/evidence/.

Timeline milestone: `--timeline` retains all 11,565 authentic commands. 08/09 marker
create/remove request semantics verified against 59638; 07 explicit requested subtypes
recovered; contextual39 partial. Sample2 semantics inferred only (different build).
Default CLI output matches starting commit byte-for-byte on all samples. See
research/TIMELINE-SEMANTICS.md, timeline-coverage.json, timeline-cli-validation.json.

### Item 1. Matching-NDF enrichment and localization implemented; useful timeline analysis next

Original 59638 archive size/SHA1 verified; everything.ndfbin extracted read-only. 2121
explicit CompanyUnit -> selector Default -> CompanyDescriptor paths; all inverse
cardinalities 1, no observed ambiguity. All 685 matching-build references have
configured static unit types/source debug names; Sample2's 41 stay inferred. Conditions
retained unevaluated; no live member identities.

Research artifacts: research/NDF59638-BRIDGE.md and ndf59638-bridge-coverage.json.
Optional --timeline --unit-data research/unit-data/build59638-v1.json.gz now consumes
the versioned index. Original 59638 US dictionary resolves all 2121 configured types;
all 685 matching references get names, Sample2's 41 inferred. Shared provenance nodes,
raw selector conditions, ambiguous/missing states preserved. No alias/debug substitution
for absent dictionary names. Source strings retain markup. See
research/TIMELINE-59638.md; exporter and input hashes committed with compact index.
Original archives remain unchanged.

Timeline currently retains 1797 explicit requested kinds and 8578 contextual39 requests
requiring live flags/module state and earlier path results. Do not pursue simulation
reconstruction; filters/reference history/request summaries can make existing facts
useful. No GUID arithmetic, ownership inference, condition evaluation or effective-order
claims from static type association.

Bounded original-playback feasibility now recorded in
research/RUNTIME59638-FEASIBILITY.md. Local ARM Mac lacks a checked compatible execution
environment and most candidate assets; no game execution attempted. Stored-vector
observation candidate da4d20 found, but individual-member identity/position unproven.
Establish playback on a complete matching install before deeper world-loop analysis.
Sample3 has 30 actor references under multiple slots: commanding slot cannot be assumed
to establish ownership.

### Item 2. Production request milestone implemented in the optional timeline

All 514 observed 0d interiors decoded with exact consumption (490 matching59638, 24
Sample2 inferred). Three declared type references, grouped quantities, deployment-point
arguments and neutral controls recovered. Existing NDF index supplies exact static
names/candidates, with missing candidates kept explicit. 80 matching-build 0a
cancellation requests expose manager channel and queue request ID; purchase correlation
remains unresolved. Variant2 scalar roles, 0c ChangeProduction interiors and 0b
semantics remain open.

Default parser and first battle report unchanged. See research/PRODUCTION-COMMANDS.md,
production-coverage.json and production59638-native.json. Owner's next milestone, once
matching playback works: targeted world observation for positions, combat, and
destruction. Parallels Windows guest proposed; playback not yet verified.

### Item 3. Single-command blocks: all 112 now have layouts; zero unresolved

- 0c ChangeProduction (47/47 exact fit; Sample2 structural only, inferred):
  research/CHANGEPRODUCTION-0C.md, research/op0c_layout.py, tests/test_op0c_decoder.py.
- 02/13/18 (5 + 16 + 44 exact fit): research/FIXED-OPCODES-02-13-18.md,
  research/op_fixed_layout.py, tests/test_fixed_opcodes.py. Field meanings still open.
- Assessment and ranked plan: research/ROADMAP-2026-10-26.md.

### Item 4. Parser alignment decision

SHA-224 is verified. Version <=1 and fields A/B differ from current strict policy;
retain policy until separately decided.

### Item 5. Digest handling

Locate this[5] origin and fatal/nonfatal mismatch handling.

### Item 6. Second independent sample source and matching Sample2 executable

Existing three samples share one source; Sample2 Version 510117427 differs from 59638.

### Item 7. Frame duration / player identities / star L=34/60 payloads

Unknown; two bounded clock passes did not establish seconds conversion. Metadata keys do
not establish recorded slot identities. Preserve raw frames and slots.

### Item 8. Opcode08 remaining fields

Types 0/1/2, raw16 context reference details, coordinate axes/units, marker-ID
correlation remain unresolved.

```
Reproduce census: python3 -B research/coverage.py > research/coverage.json
Timeline census: python3 -B research/timeline_coverage.py > research/timeline-coverage.json
Tests: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
```
