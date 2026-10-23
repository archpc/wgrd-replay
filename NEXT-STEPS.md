# NEXT-STEPS.md (prioritized)

Milestone: **594/594 multi-command blocks split**, with exact count and EOF.
571 complete layouts; 23 explicitly opaque-framed blocks. 41 tests pass.
See research/COMMAND-LAYOUTS.md, research/coverage.json and research/evidence/.

Timeline milestone: `--timeline` retains all 11,565 authentic commands. 08/09
marker create/remove request semantics verified against 59638; 07 order dispatch
partial. Sample2 semantics inferred only (different build). Default CLI output
matches starting commit byte-for-byte on all samples. See
research/TIMELINE-SEMANTICS.md, timeline-coverage.json, timeline-cli-validation.json.

1. **07 tactical order kind and references.** Highest value: 10,461 commands.
   Trace b32690 -> c972a0 and downstream enum handlers; establish actor/target
   roles and move/attack/stop kinds before naming fields. No unit identities yet.
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
