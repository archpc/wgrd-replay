# Next steps

The revision-131544 controlled recording and playback completed without a
version-specific decoder change. See the [experiment report](research/current-build/2026-10-28-controlled-experiment.md)
and [cross-build manifest](samples/cross-build-manifest.json) for the bounded results.
Layout compatibility does not establish gameplay outcomes.

## Active original-engine AAR work

Production source and documentation edits belong in the canonical checkout,
`~/Code/wgrd-replay/`, on `feat/frida-wgrd-instrumentation`. The former artifact
worktree is preserved on local branch `wip/frida-preserved-pre-canonical`; it is
not the active editing location. Migration retained its dirty diff and untracked
files byte-for-byte and left the former CI branch intact. Local `main` was
fast-forwarded to `origin/main`; stale remote-tracking references were pruned
without deleting local branches, worktrees or evidence. Recheck live branch/ref
state before publishing; no history rewrite or unrelated merge was performed.

Revision-131544 AAR work is in progress on the Frida feature branch. Current
verified milestones are indexed in [research](research/INDEX.md):

- Native 131544 descriptor extraction and exact configured-type joins work.
- Engine deterministic ticks/seconds have original Lua binding names and a
  verified computation path. Replay-frame and battle-clock origins remain open.
- Live owner/type snapshots resolve the impacted VTT-323 instances and two
  Merkava source candidates. Three damage-threshold/lifecycle chains are distinct
  from three end-cleanup calls. Source-role semantics and corroborated killer
  attribution remain open.
- Guarded Win32 input and read-only Frida counter/GameEnded observations work.
  A complete menu/browser/loading/replay cycle with state gates is not yet validated.

- The [expanded state observer](research/current-build/2026-11-02-engine-state.md)
  is integrated with the reviewed fixes, preserving the original counter records and
  rejecting unproved menu/loading/replay-active predicates. Native file-open
  observation remains unverified. Live main-menu evidence disproved the former
  GameStarted-to-ingame inference; the predicate now stays unknown.
- The [V3 position AAR](research/current-build/2026-11-02-position-aar.md) integrates
  the completed native capture: raw position anchors, capture-local type joins,
  clock brackets and value transitions, with no invented movement/arrival semantics.
  The complete guest evidence export is hash-verified; source-owner provenance
  remains a separate static research thread.

Next: target the engine's imported CreateFileA path for an actual file-open witness,
validate phase/clock mapping and
the full replay cycle only when a specific live experiment is ready, corroborate
combat-source semantics, and capture movement where supported. The retained-capture
structured AAR exporter is integrated; its current coverage and explicit unknowns
are in [the runtime AAR note](research/current-build/2026-11-02-runtime-aar.md).
Raw evidence remains private, exported to the Mac and hash-verified
before any baseline restore. These status notes do not grant future VM authorization.

## Priorities

1. **Timing and movement validation.** Follow the [Phase 2 handoff](research/current-build/PHASE-2-HANDOFF.md)
   for independent recordings, clock anchors and observed movement. Frame duration,
   coordinate mapping and arrival remain unresolved. The handoff does not authorize
   VM operation or game launch.
2. **Make recorded requests useful.** Filters, reference history and request
   summaries can build on the existing timeline without reconstructing simulation
   state. Preserve contextual kind 39, unknown execution outcomes and replay-scoped
   identities.
3. **Resolve targeted format questions.** Trace the `0x0C` consumer before naming
   the enum/float-like fields; investigate `0x0A` purchase correlation, `0x0B`,
   marker types 0/1/2 and marker IDs. Use the [research index](research/INDEX.md)
   to avoid repeating completed traces.
4. **Broaden independent validation.** Obtain independent, authenticated samples
   and identify the matching Sample2 executable. Keep cross-build layout inference
   separate from executable-backed semantics.

## Open constraints

Retain the strict container acceptance policy until evidence justifies changing
it. The digest origin/fatality in the game, slot-to-player identity, extended
`star` payloads and remaining field meanings are still unknown. Static NDF types
cannot establish ownership, live member identity, effective orders or outcomes.

Current counts and reproduction scripts are linked from [architecture](docs/ARCHITECTURE.md#4-generated-files-and-their-scripts).
The full earlier roadmap, negative results and milestone details remain in the
[dated priorities archive](research/NEXT-STEPS-2026-10-28.md). Those historical
blockers and test totals are not current requirements.
