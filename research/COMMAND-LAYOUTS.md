# Command layout recovery — build 59638

Target SHA-256: 1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.
REA 6.7.0 MCP execute_rizin_command; complete canonical records under evidence/.
Object offsets are storage destinations, not inferred game semantics.

## 0x09 — FUN_00b2edc0

Evidence ev_5beddcfc57a56ee2431c86c302a6f0b7e0aee73b8fa6d7039ff2dd73033655cc.
Creator body 0xb2edc0..0xb2eea5; vtable 0x19a18e0.
After opcode: read(obj+4,4) at 0xb2ee45; read(obj+8,16) at 0xb2ee58;
read(obj+0x18,4) at 0xb2ee6b. Total 1+4+16+4=25.
False from any read -> 0xb2ee85 -> virtual cleanup +8 when object non-NULL
-> xor eax,eax at 0xb2ee92 -> return. No serialized length, enum check,
conditional field, or reader helper. Allocation-failure behavior is outside decoder scope.

Authentic boundary validation: 31 count==1 records across all three SHA-256-bound
samples; all exactly 25 bytes, fully consumed. No field meanings assigned.

## Decoder policy

One cursor shared by declared commands. Output command_decode.status is complete,
unresolved (unknown creator), or malformed (bounded read/count/EOF violation).
commands contains only verified complete prefixes; consumed_bytes is the end of that
prefix, remaining_hex preserves the rest. Original block_hex remains on every pact.
Only complete status contributes to coverage. Exact EOF is decoder policy, not a
claim about executable acceptance. Existing opcode-08 decoded output stays compatible.
layout_build=59638 discloses the binary provenance, including for structurally matching
Sample2 (different game version; no matching binary available).

## Milestone 1

22 tests pass. 31 opcode-09 single blocks + 226 opcode-08 single blocks supported.
Multi-command coverage remains 0/594; unknown frontiers: 07=523, 04=25, 0a=25,
0d=19, 17=2. Next: 07 helper FUN_00b35e30, then frontier-driven recovery.

## 0x07 — FUN_00b2f850

Evidence ev_354985ababe3b3b821b3960ff5f8494d7d05bacc8a735eb0c58c50867bbfa0b3
and ev_ac9dc415e39c0efd355eca9626c09a8f6ebaeb2a251b72d006128b82a3f9d410.
Creator body 0xb2f850..0xb2f9d4. Reads two FUN_00b35e30 sections at
0xb2f908 / 0xb2f91d (destinations obj+4 / obj+0x60). Helper reads a u32
count at 0xb35e60; zero count bypasses element reads; each iteration reads
4 then 16 bytes at 0xb35f5c / 0xb35f73. Its small-vector capacity branches
change memory allocation only, not serialized reads. False from count or element
read returns false at 0xb35fa6.

Then creator reads raw 12 (obj+0xbc), 8 (+0xc8), 36 (+0xd0), u32 (+0xf4).
It rejects unsigned +0xf4 >3 (0xb2f985..0xb2f988). FUN_008fb4a0 at 0xb2f999
reads u16 T then T raw bytes into +0xf8; no terminator or alignment on the wire.
Every failure reaches cleanup 0xb2f9b5/0xb2f9b9 then NULL at 0xb2f9c2.
Total = 71 + 20*(count1+count2) + T. Entire creator and all read dependencies
inspected. No order/target/action interpretation assigned to these fields.

Milestone 2: 25 tests pass; authentic single-command 07 records match the independent
length formula; all 523 multi blocks starting with 07 fully split with exact count
and EOF. No malformed authentic blocks. Coverage now 523/594 (Sample1 274,
Sample2 0, Sample3 249). Remaining first unsupported opcodes: 04=25, 0a=25,
0d=19, 17=2. Shared-cursor tests cross helper count 4/5 capacity boundaries,
include both empty arrays, nonempty strings, oversized counts and enum rejection.

## 0x04 / 0x0a — FUN_00b2f0a0 / FUN_00b2e870

Evidence ev_e55fd6aa691971ccecf10c9c1896a1eb22d2c9b6c4805de45a58d9a8e7083729.
04 reads 4 -> obj+4, 16 -> +8, 4 -> +0x18 (calls 0xb2f125, 0xb2f138,
0xb2f14b); each false branches cleanup 0xb2f165; NULL at 0xb2f172.
No extra checks; identical wire layout to 09, total 25.
0a reads 4 -> +4, 16 -> +8, u32 -> +0x18; unsigned value must <=14
(0xb2e924..0xb2e927), then 4 -> +0x1c. Total 29. Failed reads or enum
check -> cleanup 0xb2e953/0xb2e957 -> NULL 0xb2e960. Full bodies inspected.
Authentic singles: 04=3, 0a=16; all exact boundaries. 26 tests pass, including
all truncation lengths and enum 14 accepted / 15 rejected.

Milestone 3: 569/594 multi blocks split (283 / 2 / 284). Remaining frontiers
0d=23 and 17=2; four 0d commands appeared after newly decoded prefixes.
