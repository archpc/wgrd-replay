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
