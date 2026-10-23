# NEXT-STEPS.md (prioritized)

1. **Find the pact consumer (opcode dispatch).** FUN_00b3c5d0 queues raw pact payloads;
   locate the code that drains that container (this+0x10/+0x1c) and dispatches on the
   opcode byte. This confirms the little-endian field layout and opcode 0x08 from the executable.
2. **Per-opcode lengths to split count>1 blocks.** Fixed-length opcodes (09/0e/04=25, 0a=29,
   13=13, 18=10, 02=22) can be tested: split all 594 multi-command blocks (290 + 4 + 300 across
   Samples 1/2/3) greedily and check exact consumption. Better: take lengths from the dispatcher (step 1).
3. **Parser alignment decision (user call).** Optionally verify the SHA-224 digest; decide whether
   to relax version (<= 1) and the field A/B zero checks to match the executable.
4. **Digest handling.** Find where this[5] (the digest-check trigger offset) is set and whether a
   mismatch aborts loading.
5. **Second independent sample source.** Retry Wayback CDX for files.canned-catfood.com/wargame/
   and rd.wargame.tools; Sample2's Version 510117427 has no matching executable build.
6. **Frame duration.** Not yet located in the executable or the file.
7. **star payload L=34/60 in Sample3**: decode alongside the 20-player lobby context.
8. Opcode 0x08 type values 0/1/2: name only with executable or game-execution evidence.
