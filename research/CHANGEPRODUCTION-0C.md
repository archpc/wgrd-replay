# Opcode 0x0C — TNetworkActionProductionUnite (build 59638)

Class-name correction (2026-11-19, parent-verified): the original title said
`TNetworkActionChangeProduction`. The creator's vtable record `0x019a191c`
carries descriptor `0x1b9aa54` → TypeDescriptor `0x1eabbf0`, whose name reads
back `.?AVTNetworkActionProductionUnite@IA@Eugen@@`.
`TNetworkActionChangeProduction` exists in the image only as an unreferenced
TypeDescriptor (`0x1eaa7bc`; zero COL/record references in .rdata) — the
original label came from string scanning, not the dispatch record. The file
name and the timeline action `change_production_request` are kept as project
labels (API surface); they are not the engine class name. Field meanings
remain unverified regardless of the class name.

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
- B = `00*12 32000000` on all 47 blocks (all three samples), identical to the
  opcode 0x08 raw16 at obj+0x08. C = 0. D = 16 zero bytes. (An earlier draft
  of this note stated B was all zeros; that came from a truncated print and
  was caught by tests/test_op0c_layout.py.)
- arr18[0] in 1..10 (small index).
- arr34[0] in {3, 8, 10, 13} (bounded enum, <= 14).
- pts50[0] = (x, y, z, kind 2); x,y in 1.3e5..1.2e6, z in 32310..37243.
- pts9c[0] = (+inf, +inf, +inf, kind 0): unset-point sentinel.
- arrE8[0] bit patterns are valid float32 (0x4030dd88 = 2.76, 0xbf3e831a =
  -0.744), constant per player side within a match.

## Confidence

- Creator identity, read order, sizes: CONFIRMED (disassembly + 47/47 exact fit).
- Variable-length arrays: CONFIRMED in code; exercised only by Sample2 data.
- Field meanings (position, heading, production-type enum): TENTATIVE.
  Consumer/Execute path traced statically 2026-11-19 (below) to a
  type-dependent dispatch boundary; still no ground truth. Do not emit
  semantic labels beyond raw values until a consumer's concrete target or a
  ground-truth replay exists.

## Consumer / Execute path (static, 2026-11-19; parent-verified)

Worker trace on the pinned 59638 image; full report with byte excerpts:
local evidence record
`~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/op0c-consumer-trace.md`.
Section map for this build: .rdata VA `0x1914000` raw `0x1513000`, .data VA
`0x1d6c000` raw `0x196b000` (differs from 131544 — derive from headers).

Vtable record `0x019a191c` is 5 dwords (4 code slots + descriptor), tiled at
stride 0x14: slot0 `0x561c50` (`mov al,1 ; ret` — constant true; the 0x0d
family uses `0x5127a0`, constant false), slot1 `0xb2c6c0` = APPLY
(`0xb2c6c0..0xb2c8f7`, ret 8), slot2 `0xb2b8c0` = scalar deleting dtor
(push 0x118 → sized delete `0x1807170` at `0xb2b9aa` — confirms object size),
slot3 `0xb30ec0` = wire writer (opcode 0x0c + fields), +0x10 descriptor
`0x1b9aa54`. Text references to the record: creator `0xb2ef0a`, dtor
`0xb2b8e7`, copy-ctor `0xb2a805`.

Chain (all sites parent-reverified):

1. `0xb35aea: call 0xb24050` — the dispatcher's ONLY call site in .text
   (recomputed over a full disassembly); produces the parsed object.
2. `0xb35b14: call 0xb24580` with ctx `[ds:0x201e2d8+0x54]`; inside,
   `0xb2459f: mov esi,[eax+4]` (APPLY slot), `0xb245a2: call 0xbb2300`
   (u32 id), `0xb245ae: call esi` → `0xb2c6c0(obj, id, ctx)`. APPLY has
   zero direct call sites — vtable-only.
3. APPLY resolves keys obj+0x04/+0x08 and obj+0x104/+0x108 via `0xb28a70`
   (registry lookup; internals untraced), reads `[B+0x20]`, then
   `0xb2c842: call 0xba59b0`.
4. `0xba59b0` loops `i < count(obj+0x18)`: `0xba5a75: call 0xc182a0` with
   index `obj+0x34[i]` → manager; walks manager+0x18..+0x1c; matches
   `[entry+8] == obj+0x18[i]` at `0xba5aa2`; loads `[entry vptr+0x44]` at
   `0xba5ab6`; `0xba5ad3: movss xmm0,[eax]` (the float `obj+0xe8[i]`),
   passes it with `&obj+0x50[i]`, `&obj+0x9c[i]`, `[B+0x20]`;
   `0xba5b20: call esi`.
5. Back in the driver: `0xb35b20: call [eax+8]` = dtor `0xb2b8c0(obj, 1)`.
   Lifetime is parse → apply → free within one loop iteration; the copy-ctor
   `0xb2a7c0` has a single caller (`0xb36d75`); no stored copy escapes.

Field verdicts (the note's two open items, now closed statically):

- **obj+0x34**: inline array 0x34..0x43, heap ptr +0x44, size +0x48, cap
  +0x4c. Elements are used as ARRAY SUBSCRIPTS (`0xc182a0`), not counts or
  sizes; the loop bound is the obj+0x18 count. Readers: creator, APPLY
  (copy/forward), `0xba59b0` (index), wire writer, dtor. No equality check
  between the two arrays found on this path.
- **obj+0xe8**: inline 0xe8..0xf7, heap ptr +0xf8, size +0xfc, cap +0x100.
  Elements are **float32** — `movss` at both the writer (`0xb30ff1`) and the
  apply side (`0xba5ad3`); supersedes the earlier "valid float32 bit
  patterns" hedge. Type settled; meaning not.

State touched (offsets only, no semantics assigned): object reads +0x04,
+0x08, +0x18, +0x34, +0x50, +0x9c, +0xe8, +0x104, +0x108; the applier writes
nothing to the object. Globals: `0x201e2d8+0x54` (apply ctx),
`0x201f660+0xe0` (selects entry of `0x20286d8`, a list-owner array),
`0xbb2300` (id source). Driver context object: +0x9c u32 countdown, +0xa1
gate, +0xa5 (clears +0xa6), +0xa8.

Trace boundary (explicit): the chain stops at the manager entries' vtable
slot +0x44 — concrete targets are type-dependent and untraced. The driver
`0xb34ec0` has a single caller `0xa39641` in `0xa395d0`, which has no direct
call site and appears once as data at .rdata `0x19990d4` (installed function
pointer / tick-callback table). Untraced: slot +0x44 targets, `0xb28a70`
internals, `0xbb2300` id generator, identities of `0x201e2d8` / `0x201f660`
/ `0x20286d8`, the `0x19990d4` table, and the gate branch selection at
`0xb34f2a..0xb34f48`. Inferred, not proven: `[A+0x20]` indexes the
`0x20286d8` list; `0xb28a70` is a save-registry lookup keyed by
(id, ctx, 20-byte key).

## Not done

- Decoder implemented in wgrd_replay._decode_command (tests/test_op0c_decoder.py).
- No REA evidence IDs recorded (REA session was closed; rizin used directly).
- Consumer of obj+0x34 / obj+0xe8 traced statically 2026-11-19 (see the
  Consumer / Execute path section): subscripts and float32 respectively;
  concrete apply targets beyond vtable slot +0x44 remain untraced.
