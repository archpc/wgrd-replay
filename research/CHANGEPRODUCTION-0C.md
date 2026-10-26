# Opcode 0x0C TNetworkActionChangeProduction (build 59638)

Session: 2026-10-26, Claude Fable 5.1 via Nous Portal. Read-only static
analysis with rizin `af; pdf` on the 59638 WarGame3.exe (no Ghidra import).
Reproduce: `python3 -B research/op0c_layout.py EXE SAMPLE1 SAMPLE3`.

## Result

Creator FUN_00b2eeb0 recovered via dispatcher jump table 0xb241f4[0x0c-2]
(case stub 0xb240f3: `56 e8 b7 ad 00 00` -> call 0xb2eeb0). Object size
0x118, vtable 0x019a191c. Read sequence (reader vtbl slot 1 = Read(dst, n)):

| Order | Call | Dest | Bytes consumed | Constraint |
|---|---|---|---|---|
| 1 | Read | obj+0x04 | 4 (u32 A) | none |
| 2 | Read | obj+0x08 | 16 (raw B) | none |
| 3 | FUN_00b35cd0 | obj+0x18 | 4 + 4n | small-buffer vector of u32 |
| 4 | FUN_00b35fc0 | obj+0x34 | 4 + 4n | each u32 <= 0x0e (cmp at 0xb360ff) |
| 5 | FUN_00b290c0 | obj+0x50 | 4 + 16m | per element: 12 raw + u32 <= 6 (cmp at 0xb29162) |
| 6 | FUN_00b290c0 | obj+0x9c | 4 + 16m | same |
| 7 | FUN_00b35cd0 | obj+0xe8 | 4 + 4n | u32 array |
| 8 | FUN_00b29080 | obj+0x104 | 4 + 16 (u32 C, raw D) | none |

Any short read or constraint failure -> vtbl slot 2 destructor, creator
returns NULL (0xb2f073..0xb2f080). Minimum block size 61 bytes incl. opcode.

Helpers are generic readers reusable for other opcodes:
- FUN_00b35cd0: count + u32 array into a small-buffer vector (inline cap 4,
  heap ptr +0x10, size +0x14, cap +0x18).
- FUN_00b35fc0: same with element bound 0x0e.
- FUN_00b290c0: count + array of 16-byte {12 raw, u32 kind <= 6} via resize
  FUN_00b38180.
- FUN_00b29080: u32 + raw16.

## Corpus fit

| Sample | Build | 0x0C blocks | Fit | Sizes |
|---|---|---|---|---|
| Sample1 | 59638 | 13 | 13 | 105 x13 |
| Sample3 | 59638 | 28 | 28 | 105 x28 |
| Sample2 | 510117427 (inferred) | 6 | 6 | 105 x4, 281 x2 |

All 47 authentic blocks consume exactly. The two 281-byte Sample2 blocks are
105 + 11*16, i.e. eleven extra 16-byte point elements, so the variable-length
array path is exercised in data (on the non-matching build only).

## Observed values, matching build (41 blocks, every count = 1)

- A = 0xC000001E + slot (same player-id convention as opcode 0x08).
- B = 16 zero bytes. C = 0. D = 16 zero bytes.
- arr18[0] in 1..10 (small index).
- arr34[0] in {3, 8, 10, 13} (bounded enum, <= 14).
- pts50[0] = (x, y, z, kind 2); x,y in 1.3e5..1.2e6, z in 32310..37243.
- pts9c[0] = (+inf, +inf, +inf, kind 0): unset-point sentinel.
- arrE8[0] bit patterns are valid float32 (0x4030dd88 = 2.76, 0xbf3e831a =
  -0.744), constant per player side within a match.

## Confidence

- Creator identity, read order, sizes: CONFIRMED (disassembly + 47/47 exact fit).
- Variable-length arrays: CONFIRMED in code; exercised only by Sample2 data.
- Field meanings (position, heading, production-type enum): TENTATIVE. No
  consumer/Execute analysis, no ground truth. Do not emit semantic labels
  beyond raw values until a consumer is traced or a ground-truth replay exists.

## Not done

- No decoder implementation yet (see NEXT-STEPS item 3).
- No REA evidence IDs recorded (REA session was closed; rizin used directly).
- Consumer of obj+0x34 / obj+0xe8 not traced.
