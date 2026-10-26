# Opcodes 0x02, 0x13, 0x18: fixed-size creator layouts (build 59638)

Session 2026-10-26 (Claude Fable 5.1 via Nous Portal). Read-only static analysis.

## Objective

Recover the serialized layouts of the three remaining unresolved single-command
opcodes (after 0x0C) so that every authentic single-command block in the corpus
has a creator-backed layout.

## Artifacts

- WarGame3.exe build 59638, SHA-256
  `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`
  (local path `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe`;
  not redistributed). Address conversion: file offset = VA - 0x401000 + 0x400.
- Samples per samples/manifest.json (Sample1/Sample3 build 59638; Sample2 build
  510117427, semantics inferred only).
- Tools: rizin 0.9.1 (`af; pdf`, no full analysis), Python 3 stdlib.
- Evidence: research/evidence/rizin-creators-02-13-18-59638.txt (bounded
  disassembly of the three creators, comments stripped).

## Method

Dispatcher FUN_00b24050 indexes jump table 0xb241f4 by opcode-2 (REA-NOTES
Session 3). Each case stub is `push esi; call creator; add esp,4; pop esi; ret`.
Creators allocate the action object, install the RTTI vtable, then call the
packet reader's vtbl slot 1 `Read(dst, n)` for each field; any failed read
destroys the object and returns NULL.

## Result

| Opcode | Class (RTTI) | Case stub | Creator | Obj size | Vtable | Reads in order | Total bytes |
|---|---|---|---|---|---|---|---|
| 0x02 | TNetworkActionSurrender | 0xb24085 | FUN_00b30660 | 0x1c | 0x019a1854 | u32 -> +0x04; raw16 -> +0x08; u8 -> +0x18 | 22 |
| 0x13 | TNetworkActionPlayerSynchroServiceAction | 0xb24140 | FUN_00b2fdd0 | 0x10 | 0x019a19a8 | u32 -> +0x04; u32 -> +0x08; u32 -> +0x0c | 13 |
| 0x18 | TNetworkActionDeactivateSupply | 0xb24177 | FUN_00b2f2e0 | 0x10 | 0x019a1a0c | u32 -> +0x04; u32 -> +0x08; u8 -> +0x0c | 10 |

Totals include the opcode byte. No arrays, strings, or value bounds checks in
any of the three creators. Read call sites (VA): 0x02: 0xb306e5, 0xb306f8,
0xb3070b. 0x13: 0xb2fe41, 0xb2fe74, 0xb2fe87. 0x18: 0xb2f351, 0xb2f384, 0xb2f397.

Byte-level confirmation of the read sequences (push imm8 size ... lea
eax,[esi+disp] ... call edx) is performed by research/op_fixed_layout.py, which
also re-resolves the jump table.

## Corpus fit

| Opcode | Sample1 | Sample3 | Sample2 | Total | Sizes |
|---|---:|---:|---:|---:|---|
| 0x02 | 0 | 3 | 2 | 5 | all 22 |
| 0x13 | 10 | 4 | 2 | 16 | all 13 |
| 0x18 | 19 | 25 | 0 | 44 | all 10 |

65/65 authentic single-command blocks match the fixed sizes. Together with 0x0C
(47/47) this accounts for all 112 single-command blocks previously listed as
unresolved in NEXT-STEPS item 3.

## Observed values (data, not semantics)

- 0x02: +0x04 = 0xC000001E + slot on all 5 (same player-id convention as 0x08
  and 0x0C); +0x08 = `00*12 32000000` (same raw16 as 0x08/0x0C); +0x18 = 0.
- 0x13: +0x04 = 0 on all 16; +0x08 in {0, 1}; +0x0c in 0..16.
- 0x18: +0x04 = 0xC0000xxx values that are NOT the player id (e.g. 0xc00006e5,
  0xc0000ec7), several distinct per slot; +0x08 in {0, 1, 2}; +0x0c in {0, 1}.

## Confidence

- Creator identity, read order, sizes: CONFIRMED (jump table + disassembly +
  65/65 exact fit, reproducible by script).
- 0x02 player-id convention for +0x04: STRONGLY SUPPORTED (5/5, matches two
  other opcodes).
- 0x18 +0x04 as a non-player entity reference: TENTATIVE (high-bit pattern
  only; no consumer traced). Meaning of 0x13 fields: UNRESOLVED.

## Reproduce

    python3 -B research/op_fixed_layout.py \
        ~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe \
        '~/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample*'

Expected: three `(OK)` creator lines with reads `+0x04:4 +0x08:16 +0x18:1`,
`+0x04:4 +0x08:4 +0x0c:4`, `+0x04:4 +0x08:4 +0x0c:1`; per-sample size
histograms as in the table above; exit 0.

## Relationship to existing findings

Extends REA-NOTES Session 3 opcode table; closes the 02/13/18 entries in the
"Open" list. Decoder implementation tracked separately.
