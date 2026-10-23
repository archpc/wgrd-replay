# NEXT-STEPS.md (prioritized)

Milestone: **594/594 multi-command blocks split**, with exact count and EOF.
571 complete layouts; 23 explicitly opaque-framed blocks. 31 tests pass.
See research/COMMAND-LAYOUTS.md, research/coverage.json and research/evidence/.

1. **Decode 0d serializer interiors.** Boundary is proven: 18+L from root
   FUN_00b584e0 -> child FUN_00b580a0. Field bodies FUN_00c06ba0 (variant2) and
   FUN_00c06c20 (1/3) use nested scopes, helper reads and runtime references.
   Current output reports framed/opaque, not complete. 514 opaque commands total.
2. **Remaining 112 single-command blocks:** 0c=47, 18=44, 13=16, 02=5.
   Recover exact creators/helpers before implementing; no more multi blocks
   are blocked by these opcodes in the authenticated sample set.
3. **Parser alignment decision.** SHA-224 is verified. Version <=1 and fields A/B
   differ from current strict policy; retain policy until separately decided.
4. **Digest handling.** Locate this[5] origin and fatal/nonfatal mismatch handling.
5. **Second independent sample source and matching Sample2 executable.** Existing
   three samples share one source; Sample2 Version 510117427 differs from 59638.
6. **Frame duration and star L=34/60 payloads.** Unknown; no seconds conversion.
7. **Opcode08 meanings.** Analyse execute/apply before naming type0/1/2 or raw16.

Reproduce census: python3 -B research/coverage.py > research/coverage.json
Tests: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
