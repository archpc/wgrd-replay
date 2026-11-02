# Next steps

The revision-131544 controlled recording and playback completed without a
version-specific decoder change. See the [experiment report](research/current-build/2026-10-28-controlled-experiment.md)
and [cross-build manifest](samples/cross-build-manifest.json) for the bounded results.
Layout compatibility does not establish gameplay outcomes.

## Active original-engine AAR work

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

Next: integrate the corrected state observer, validate phase/clock mapping and
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
