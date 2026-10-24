# Production request decoding plan

Checkpoint: 79ff879. User selects two milestones: production request semantics,
then targeted world observation once matching playback is available. Existing
OP07-PLAN.md authorizes autonomous evidence-backed decoder work in this checkout.

Goal: recover 0x0d requested type bundles, grouped quantities and deployment
arguments, plus supported cancellation semantics. Do not reinterpret contextual39
orders or claim accepted purchases, spawned units, positions, combat or destruction.

Approach: follow the existing optional timeline layer. Keep default parser output
and the first battle report unchanged. Native Rizin reads the immutable 59638 PE;
REA wrapper launch failed in this session. Capture reproducible disassembly and
hashes. No target execution, installation, dependency changes or downloads.

Files / interfaces:
- wgrd_production.py: decode_production(fields, matched) interprets the bounded
  serializer payload. decode_production_action(opcode, fields, raw_hex, matched)
  handles supported production/cancellation requests; unknowns remain unknown.
- wgrd_timeline.py: route production interpretations and enrich declared type GUIDs
  using existing static-index enrichment; no changes to default replay parsing.
- tests/test_production.py: synthetic distinct-word GUIDs, nested scope boundaries,
  zero/four/five entries, variable arrays, hostile lengths/counts, nonfinite points,
  variant2, unmatched-build downgrade, cancellation and integration retention.
- research/production_coverage.py and production-coverage.json: authenticate samples,
  census variants, names, quantities, cancellations, and verify default compatibility.
- research/PRODUCTION-COMMANDS.md and evidence: instruction addresses, request
  semantics, unevaluated runtime dependencies, remaining blockers.

Implementation:
- [x] Trace both field bodies, serializer scopes, reference reads and consumers.
- [x] Write focused failing tests; run them before implementation.
- [x] Implement bounded optional timeline decoding and static type enrichment.
- [x] Run complete tests and authenticated all-sample census; verify default output.
- [x] Record findings and remaining 0x0c/controls/outcome limits. Review one pass.

Review focus: nested lengths never escape payload bounds; count loops bounded
before allocation; redundant group counts need not agree; no guessed queue ID
correlation; Sample2 remains inferred; nonfinite coordinates stay JSON-safe;
nonzero unknown GUIDs remain unresolved, zero references remain explicit.
