# NEXT-STEPS.md (prioritized)

1. **Second independent sample source.** Retry Wayback CDX for files.canned-catfood.com/wargame/
   and rd.wargame.tools once archive.org is back; or ask the community. Required by mission criteria.
2. **Per-opcode lengths to split count>1 blocks** (most useful next experiment). Fixed-length
   opcodes (09/0e/04=25, 0a=29, 13=13, 18=10, 02=22) can be tested: split all 594 multi-command
   blocks (290 + 4 + 300 across Samples 1/2/3) greedily with known lengths and check exact consumption. Op 07 = 91+20k suggests a
   20-byte repeated element (unit list?) with count at +1.
3. **Frame duration.** Correlate frame count with a known match length (needs a sample with
   recorded duration, or game run). 19033 frames vs TimeLimit 3600 s is not conclusive.
4. **28-byte field at 0x0C.** Test HMAC/CRC/SHA-224 variants, or wait for executable evidence.
5. **star payload L=34/60 in Sample3** — decode alongside the 20-player lobby context.
6. **Executable analysis.** If the user owns Red Dragon on Steam (macOS build exists), install
   it legitimately and use REA (Ghidra) to locate ESAV/rply string xrefs → loader and opcode dispatch.
7. Opcode 0x08 type values 0/1/2: map to in-game flare kinds only with game-execution evidence.
