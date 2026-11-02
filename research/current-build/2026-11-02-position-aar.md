# V3 position AAR: masked anchor observations, 2026-11-02

Evidence note for the additive `runtime-v3` profile in
`instrumentation/aar_events.py`. Everything below is recomputed from the
hash-pinned Wargame Red Dragon 131544 capture; the trace is opened read-only.

## Capture identity

| item | value |
|---|---|
| trace | `native-v3b-replay.jsonl` (under `aar-v3-20261102T082918Z/`) |
| trace SHA-256 | `d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec` |
| records | 10182 lines, 5088 enter / 5088 leave pairs across ten hook types, plus start/identity/hooks_installed/summary/detached/end |
| executable | revision 131544, SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d` |
| unit index | `aar-20261102T050816Z/units/unit-index-131544.json`, SHA-256 `73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d` |
| archive pin | `172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b` |
| capture-source pins | `wgrd_frida.py` `8c32f864…e821`, `hooks.js` `751960dd…8d19`, `aar-capture-131544-v3.json` `e0290192…3eefd` |

The three retained capture-source copies matched their pins for the run that
produced the exports below. The trace's own `start`/`identity_verified` records
matched all ten hook shapes and executable addresses.

An in-flight snapshot of the same session (`native-v3b-inflight-snapshot.jsonl`,
SHA-256 `fa119ef7…76a2`) has no `summary`, `detached` or `end` record. It is
rejected with `incomplete capture: missing summary, detached, end`; no output is
created from it. Export requires the completed capture.

## Profile

`--profile runtime-v3` (or autodetection from the exact ten-hook start-record
set, which cannot match the eight-hook `runtime` set). Hook set, VA, argument
count, sample stride and read shape are validated strictly; the masked reads
must declare `indirect_mask`/`indirect_offset` exactly:

- `owner_lookup_candidate` `0xc52de0`, leave: `retval+0x00` header (128 B, local
  handle at `+0x20`, descriptor pointer at `+0x28`), `retval+0x28` indirect
  descriptor bytes (GUID at `+0x0c`, name token at `+0x60`), `retval+0xe4`
  indirect 12 B anchor.
- `owner_destroy_candidate` `0xa75c70`, enter: same three reads on `ecx`.
- Anchor read contract: chain is exactly the raw pointer, `applied_mask` is
  `0xfffffffc`, `target_offset` is 48, `final_target == target ==
  (raw & 0xfffffffc) + 0x30`, and all three float32 coordinates are finite.

`runtime` and `legacy` profile behaviour, output keys and the 19 legacy tests are
unchanged.

## Recomputed result

Damage pipeline (unchanged semantics, new capture): 28 impacts, 28 checks, 6
owner destroys (3 lifecycle, 3 cleanup), 25 suppression and 3 physical-damage
transitions on handles 31, 32, 33, 34, 39, 40; lifecycle ordinals 3, 7, 21.
365 sampled owner lookups from 363897 invocations (stride 997), covering 71 local
handles; no identity conflict was observed in the sampled records. This is not
population-wide lifetime evidence.

Position observations (371 total: 365 lookup leaves + 6 destroy enters):

- 371 successful anchor reads, 0 read failures, all coordinates finite.
- 71 identity tracks keyed on `handle_u32 + owner_object + descriptor_pointer`.
  No handle, owner or anchor pointer is shared by two tracks. 11 descriptor
  *pointers* are shared by several units of one type; that is type sharing, not
  an identity conflict, and is reported separately.
- 153 `position_anchor_changed` transitions across 56 of 71 tracks. No
  `position_anchor_rebound` occurred: each track kept one anchor target, so the
  compared reads are structurally comparable.
- Clock brackets: 459 clock-enter samples in 2 receiver epochs (one isolated
  sample at line 6 with counter 12102; then 458 samples, counter 242 → 4164,
  lines 8374 → 10178). 363 observations are bracketed by the two *adjacent*
  same-epoch clock enters; the first 8 (lines 8359–8373, before the first sample
  of the stable epoch) are unbracketed. No interpolation, counter extrapolation
  or wall-clock substitution is performed.
- Descriptor joins for the observation identities: 365 exact 2-of-2 GUID+token,
  6 `ambiguous_or_missing_candidates` at lookup observations for handles 4 and 8.
  All six destroy-enter anchors have exact joins. The unresolved lookup samples
  remain unjoined, not guessed.
- `frame_apply_candidate` 4176/4176 and `phase_change_candidate` 1/1 are exported
  as raw unmapped observations; neither is treated as a frame, epoch or phase.

## Explicit non-claims

- Coordinates are unmapped raw float32 triples. They are not metres, world units
  or a visual centre, and the anchor object's own semantics are unproven.
- A `position_anchor_changed` row is a raw value transition, not a movement,
  heading, speed, arrival or movement intent. No rate is derived, and the 153
  rows are not a count of unit movements.
- The lookup-only sample has 55 handle groups with differing vectors. Including
  destroy-enter observations gives 56 changed tracks. Both count raw byte
  differences, not verified movements or allocation generations.
- Position-change timing uses the outer bounds of both endpoint observations,
  not just the later observation's bracket. For example, one real transition
  spans possible counters 3006–3117; assigning only 3114–3117 would be too narrow.
  A missing endpoint bound or receiver-epoch change keeps transition timing unknown.
- Position times remain counter-bracketed: no replay frame, exact simulation time
  or battle time is assigned. Damage records retain the independently named engine
  deterministic timestamp; its battle origin and replay-frame mapping remain unknown.
- Source role stays `inferred_damage_source_owner`; no shooter, weapon or kill
  outcome is promoted.
- The native `CreateFileW` watch did not observe an open of the trace target
  file; source-file binding stays unknown, and coverage is stated as execution
  coverage, not as a file-open proof.
- `phase_change_candidate` is one raw observation with argument `0x2`; it does
  not establish a battle phase.

## Review corrections and validation scope

The original V3 export is retained unchanged. Reviewed exports use the wider
two-observation transition intervals described above. V3 file extraction now
requires all three retained capture-source/config copies; a missing copy fails
closed. The older runtime profile preserves its existing optional-copy behavior
and explicit missing-source status.

The pinned V3 script does not implement gate counters. Their absence is reported
as `not_reported_by_pinned_v3_source; no_gate_zero_claim`, not as observed zero
gate failures. A reported nonzero gate counter still rejects the capture.
Anchor-read failures and descriptor-read failures are counted separately; an
ambiguous descriptor join is not itself a failed memory read.

## Outputs

Written exclusively to `…/aar-v3-20261102T082918Z/runtime-aar-v3/`:

`events.json`, `summary.json`, `units.json`, `positions.json` (observations,
anchor changes, clock epochs, identity report), `chronology.md` (adds a position
section with per-observation line/hash references and a change list).

## Independent interval review

A read-only independent reconstruction, without importing the exporter, checked
all 153 transitions against the pinned raw trace. Every interval matched the
outer bounds of both observations; no negative spans, epoch-boundary crossings,
line-coverage violations, anchor-byte mismatches or decoded-vector mismatches
were found. The review also reproduced the 459 clock samples and two observed
receiver epochs. Source SHA-256:
`458008accd4b7d40b9e063970979681f7332670f49811e42872d0e58708e4619`.
The private review artifact digest is
`287a8b5f71070713829595fe89eb4e897d57a036b76ab3ae1edc9a2a5ae2e3a4`.

The interval-level missing-bound/epoch-change fallback has no dedicated test;
this is a documented coverage gap, not evidence that it was exercised by the
real trace. No tests were rerun for this review. The implementation commit had
already been published before the later explicit review gate; this review is
post-commit, not represented as pre-commit approval.

## Tests

The lead review added two portable regressions for transition-time coverage and
required V3 source copies. Final focused result: 50 tests passed. Full canonical
suite: 327 tests, two existing corpus skips; Ruff, Python syntax, documentation
(70 tracked Markdown files, no missing links), and preservation checks passed.
All four previous runtime output files also reproduced byte-for-byte.

`tests/test_aar_events.py` initially grew from 38 to 48 tests (all passing on Python 3.14):
the 38 existing legacy/runtime tests are preserved, plus 10 focused V3 tests for
strict hook/mask validation, profile autodetection, incomplete-capture rejection
(synthetic and the real in-flight snapshot), descriptor-resolved observation
identity, non-merged identity mismatches, anchor arithmetic/finiteness, bounded
clock brackets, raw-value change semantics, line/hash reference resolution, and
exclusive CLI export with capture-source authentication.
