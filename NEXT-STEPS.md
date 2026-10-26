# NEXT-STEPS.md (prioritized)

Milestone: **594/594 multi-command blocks split**, with exact count and EOF.
571 complete layouts; 23 explicitly opaque-framed blocks. All 10,942 non-empty
blocks (multi and single) are complete or framed; zero unresolved. 120 tests pass.
See research/COMMAND-LAYOUTS.md, research/coverage.json and research/evidence/.

Timeline milestone: `--timeline` retains all 11,565 authentic commands. 08/09
marker create/remove request semantics verified against 59638; 07 explicit requested subtypes recovered; contextual39
partial. Sample2 semantics inferred only (different build). Default CLI output
matches starting commit byte-for-byte on all samples. See
research/TIMELINE-SEMANTICS.md, timeline-coverage.json, timeline-cli-validation.json.

1. **Matching-NDF enrichment and localization implemented; useful timeline analysis next.** Original
   59638 archive size/SHA1 verified; everything.ndfbin extracted read-only.
   2121 explicit CompanyUnit -> selector Default -> CompanyDescriptor paths;
   all inverse cardinalities1, no observed ambiguity. All685 matching-build
   references have configured static unit types/source debug names; Sample2's41
   stay inferred. Conditions retained unevaluated; no live member identities.
   Research artifacts: research/NDF59638-BRIDGE.md and ndf59638-bridge-coverage.json.
   Optional --timeline --unit-data research/unit-data/build59638-v1.json.gz now
   consumes the versioned index. Original59638 US dictionary resolves all2121
   configured types; all685 matching references get names, Sample2's41 inferred.
   Shared provenance nodes, raw selector conditions, ambiguous/missing states
   preserved. No alias/debug substitution for absent dictionary names. Source
   strings retain markup. See research/TIMELINE-59638.md; exporter and input hashes
   committed with compact index. Original archives remain unchanged.
   Timeline currently retains1797 explicit requested kinds and8578 contextual39
   requests requiring live flags/module state and earlier path results. Do not
   pursue simulation reconstruction; filters/reference history/request summaries
   can make existing facts useful. No GUID arithmetic, ownership inference,
   condition evaluation or effective-order claims from static type association.
   Bounded original-playback feasibility now recorded in
   research/RUNTIME59638-FEASIBILITY.md. Local ARM Mac lacks a checked compatible
   execution environment and most candidate assets; no game execution attempted.
   Stored-vector observation candidate da4d20 found, but individual-member
   identity/position unproven. Establish playback on a complete matching install
   before deeper world-loop analysis. Sample3 has30 actor references under
   multiple slots: commanding slot cannot be assumed to establish ownership.
2. **Production request milestone implemented in the optional timeline.** All514
   observed 0d interiors decoded with exact consumption (490 matching59638,
   24 Sample2 inferred). Three declared type references, grouped quantities,
   deployment-point arguments and neutral controls recovered. Existing NDF index
   supplies exact static names/candidates, with missing candidates kept explicit.
   80 matching-build0a cancellation requests expose manager channel and queue
   request ID; purchase correlation remains unresolved. Variant2 scalar roles,
   0c ChangeProduction interiors and0b semantics remain open. Default parser and
   first battle report unchanged. See research/PRODUCTION-COMMANDS.md,
   production-coverage.json and production59638-native.json. User's next milestone:
   once matching playback works, targeted world observation for positions, combat
   and destruction. Parallels Windows guest proposed; playback not yet verified.
3. **Single-command blocks: all 112 now have layouts; zero unresolved.**
   0c ChangeProduction (47/47 exact fit; Sample2 structural only, inferred):
   research/CHANGEPRODUCTION-0C.md, research/op0c_layout.py, tests/test_op0c_decoder.py.
   02/13/18 (5 + 16 + 44 exact fit): research/FIXED-OPCODES-02-13-18.md,
   research/op_fixed_layout.py, tests/test_fixed_opcodes.py. Field meanings still open.
   Assessment and ranked plan: research/ROADMAP-2026-10-26.md.
4. **Parser alignment decision.** SHA-224 is verified. Version <=1 and fields A/B
   differ from current strict policy; retain policy until separately decided.
5. **Digest handling.** Locate this[5] origin and fatal/nonfatal mismatch handling.
6. **Second independent sample source and matching Sample2 executable.** Existing
   three samples share one source; Sample2 Version 510117427 differs from 59638.
7. **Frame duration / player identities / star L=34/60 payloads.** Unknown;
   two bounded clock passes did not establish seconds conversion. Metadata keys
   do not establish recorded slot identities. Preserve raw frames and slots.
8. **Opcode08 remaining fields.** Types0/1/2, raw16 context reference details,
   coordinate axes/units, marker-ID correlation remain unresolved.

Reproduce census: python3 -B research/coverage.py > research/coverage.json
Timeline census: python3 -B research/timeline_coverage.py > research/timeline-coverage.json
Tests: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
