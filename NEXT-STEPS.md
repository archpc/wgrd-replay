# NEXT-STEPS.md (prioritized)

Milestone: **594/594 multi-command blocks split**, with exact count and EOF.
571 complete layouts; 23 explicitly opaque-framed blocks. 71 tests pass.
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
2. **Decode 0d serializer interiors.** Boundary is proven: 18+L from root
   FUN_00b584e0 -> child FUN_00b580a0. Field bodies FUN_00c06ba0 (variant2) and
   FUN_00c06c20 (1/3) use nested scopes, helper reads and runtime references.
   Current output reports framed/opaque, not complete. 514 opaque commands total.
3. **Remaining 112 single-command blocks:** 0c=47, 18=44, 13=16, 02=5.
   Recover exact creators/helpers before implementing; no more multi blocks
   are blocked by these opcodes in the authenticated sample set.
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
