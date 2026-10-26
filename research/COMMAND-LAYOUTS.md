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

## 0x0c — FUN_00b2eeb0 (ChangeProduction); structural layout

Creator 0xb2eeb0, dispatcher 0xb241f4[0x0c-2]. Read order (reader Read(dst,n)):
u32 -> obj+04; raw16 -> obj+08; u32 n + n x u32 (FUN_00b35cd0) -> obj+18;
u32 n + n x u32, each <= 0x0e (FUN_00b35fc0) -> obj+34; u32 m + m x (3 x float32 +
u32 kind <= 6) (FUN_00b290c0) -> obj+50; same -> obj+9c; u32 n + n x u32 (FUN_00b35cd0)
-> obj+e8; u32 -> obj+104; raw16 -> obj+108 (FUN_00b29080). Minimum 61 bytes incl. opcode.
Decoder emits obj_04_u32, obj_08_hex, obj_18_array, obj_34_array, obj_50_points,
obj_9c_points, obj_e8_array, obj_104_u32, obj_108_hex; arrays carry count_u32, items_hex
and items_u32 (point arrays: items with xyz_f32, kind_u32). field_decode_status=layout.
Field meanings unconfirmed; raw values only. See research/CHANGEPRODUCTION-0C.md.

Corpus, single-command blocks, exact consumption: Sample1 (59638) 13 x 105 bytes;
Sample3 (59638) 28 x 105 bytes; Sample2 (510117427, inferred, structural only)
4 x 105 + 2 x 281 (11 extra 16-byte point elements). 47/47 complete.
Observed (matching build): obj_04 = 0xC000001E + slot; obj_08 = `00*12 32000000`.

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

## 0x17 — FUN_00b2f3b0

Dispatch wrapper 0xb2416c calls 0xb2f3b0 (not adjacent creator 0xb2f580).
Evidence ev_73ef1cc98c73a8423375b40ae4cb5f819e8fd7c1c1dab4bc81aeb06b2dad2656;
wrapper table in ev_1a54f3c80ea18ed0a60fa1041204c9118bfcbb72cd111b49833aed492b68d985.
Creator 0xb2f3b0..0xb2f57b: read4 -> obj+4 (0xb2f43f), read4 ->
array count (0xb2f45c), loop read4/read4 per entry (0xb2f504/0xb2f51b),
read1 -> obj+0x18 (0xb2f541). Zero count skips array. Allocation branches do
not read wire bytes. All read failures reach cleanup 0xb2f55b -> NULL 0xb2f568.
Trailing byte is raw, no bool value validation. Total 10+8*N.
53 authentic singles: 43*18, 9*26, 1*34 bytes. All exactly consumed.
27 tests pass. Multi coverage 571/594. Remaining 23 blocked at 0d serializer.

## 0x0d — proven envelope; internal fields remain opaque

Creator FUN_00b2fea0 delegates to FUN_00b28ef0 (ev_8a4d9f595e4b7f61ffaac879e810067a50341049b1779f92d053eac14c146f07).
The latter reads a u32 variant at 0xb28f29; only 1/2/3 select an object:
1/3 -> constructor 0xc08340, vtable 0x19b0180; 2 -> 0xc080e0,
vtable 0x19b01b4. Failed selector reads or 0/>3 yield no object and false;
creator then cleans up and returns NULL at 0xb2ff1d.

Proven serialized boundary (offsets relative to opcode):

| Offset | Bytes | Wire observation |
|---|---|---|
| 0 | 1 | opcode |
| 1 | 4 | variant, 1..3 |
| 5 | 4 | root serializer header, raw u32 |
| 9 | 1 | root serializer header, raw byte |
| 10 | 4 | child section header, raw u32 |
| 14 | 4 | child payload length L |
| 18 | L | opaque serializer payload |

Root constructor FUN_00b584e0 reads 4 then 1 bytes directly from the packet
reader (0xb58556 / 0xb58571). Virtual slot +0x10 at 0xb28fd6 resolves via
vtable reads (ev_73ef1cc98c73a8423375b40ae4cb5f819e8fd7c1c1dab4bc81aeb06b2dad2656)
to 0xc0fad0 (variants 1/3) or 0xc0f530 (2). Both invoke FUN_00b580a0 before
any field-level deserialization (ev_565d7694a729fd90408b7840d63449bc242c9f724283cea5c4a9ecd9ca5295dd).

FUN_00b580a0 reads exactly 8 bytes at 0xb5812a into two u32s; second is L.
It then reads exactly L bytes at 0xb581a1 into a private buffer and wraps that
buffer at 0xb581b6. Further nested serializers operate on that buffer, not on
the shared command stream. False reads set the parent error byte +0x10;
FUN_00b589a0 propagates child errors (0xb589af), and FUN_00b28ef0 checks the
root error at 0xb28fe2 before returning true/false. Evidence:
ev_d830cd29948f71bb887d0d8f105d18afd926a7f4b55f40ad4e01c2572eae77a2 and
ev_50a31a0d558533a4160dee39615039a4ff4241910ed7650c770aeb47d021e1bd.

Thus 18+L is an instruction-backed boundary, not a fitted sample-length rule.
All 470 authentic single-command 0d records match it; all 44 additional 0d
commands in multi blocks fit the declared count and reassemble exactly.

Deliberate limit: fields inside the private buffer are NOT fully recovered or
validated. Traced bodies FUN_00c06ba0 / FUN_00c06c20 delegate through nested
serializer helpers; repeated identifier/length envelopes and runtime reference
resolution remain. These commands have field_decode_status=opaque. A complete
count/byte split containing one reports status=framed, NEVER complete. This
proves only the envelope, not creator success, nested field validity, runtime
reference resolution, or game behavior. Empty or structurally invalid opaque
payloads may still be framed; that is not an acceptance claim.

## 0x0e — FUN_00b2f9e0

Complete creator 0xb2f9e0..0xb2fac5 is retained in
ev_354985ababe3b3b821b3960ff5f8494d7d05bacc8a735eb0c58c50867bbfa0b3.
Reads 4 -> obj+4 (0xb2fa65), 4 -> +8 (0xb2fa78), 16 -> +0x0c
(0xb2fa8b). All false branches -> cleanup 0xb2faa5 -> NULL 0xb2fab2.
Total 25; no enum/conditional read. 26 authentic singles and 6 occurrences in
multi blocks (after 0d) validate boundaries. No item/production semantics inferred.

## Final milestone — 2026-10-23

31 tests pass. All 594 multi blocks split exactly (290 / 4 / 300).
571 have complete supported field layouts (285 / 2 / 284); 23 are explicitly
opaque-framed (5 / 2 / 16). No multi block remains boundary-unresolved.
Across nonempty blocks: 10,830 / 10,942 split; 112 single-command blocks remain
unresolved: 02=5, 0c=47, 13=16, 18=44. No authentic block is malformed.
514 total 0d envelopes remain opaque (470 singles + 44 commands in multi blocks).
Coverage is structural, not proof of gameplay semantics or cross-build equivalence.

Reproduce: python3 -B research/coverage.py > research/coverage.json.
The census checks manifest size/SHA-256, container digest, command count,
contiguous offsets, exact reassembly and EOF for every split block. It emits no
sample bytes. Source samples and the executable remain outside Git.
