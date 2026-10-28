# Next steps

The revision-131544 controlled recording and playback completed without a
version-specific decoder change. See the [experiment report](research/current-build/2026-10-28-controlled-experiment.md)
and [cross-build manifest](samples/cross-build-manifest.json) for the bounded results.
Layout compatibility does not establish gameplay outcomes.

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
