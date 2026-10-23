# NEXT-STEPS.md (prioritized)

1. **Per-opcode field layouts from the creators.** Dispatcher FUN_00b24050 and the jump table
   at 0xb241f4 are mapped (REA-NOTES-59638.md). Decompile the creators for the observed opcodes
   (02 04 07 09 0a 0c 0d 0e 13 17 18) to get exact lengths, then split count>1 blocks.
   Also trace the dispatcher's caller to confirm it runs `count` times per block.
2. **Split the 594 multi-command blocks** (290 + 4 + 300 across Samples 1/2/3) using the
   creator-derived lengths from step 1; require exact consumption.
3. **Parser alignment decision (user call).** SHA-224 is now verified. Decide whether
   to relax version (<= 1) and the field A/B zero checks to match the executable.
4. **Digest handling.** Find where this[5] (the digest-check trigger offset) is set and whether a
   mismatch aborts loading.
5. **Second independent sample source.** Retry Wayback CDX for files.canned-catfood.com/wargame/
   and rd.wargame.tools; Sample2's Version 510117427 has no matching executable build.
6. **Frame duration.** Not yet located in the executable or the file.
7. **star payload L=34/60 in Sample3**: decode alongside the 20-player lobby context.
8. Opcode 0x08 type values 0/1/2 and the 16-byte block: analyse the LaunchFumigene
   execute/apply vtable slot (vtbl 0x19a18cc) before naming them.
