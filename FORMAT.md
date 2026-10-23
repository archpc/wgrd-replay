# FORMAT.md — Wargame: Red Dragon replay (.wargamerpl2)

Status legend: VERIFIED = holds on every byte of all 3 samples (see samples/manifest.json);
INFERRED = consistent with evidence, meaning not proven; UNKNOWN = not determined.

Samples: koppeltar-Sample1/2/3 (game Version 59638, 510117427, 59638). Only one
container version (1) observed. No version-specific layout differences observed.

## 1. File header (big-endian) — VERIFIED

| Offset | Size | Field | Evidence (Sample2) |
|---|---|---|---|
| 0x00 | 4 | magic `ESAV` | `45534156` |
| 0x04 | 4 | u32 BE container version = 1 (name INFERRED) | `00000001` |
| 0x08 | 4 | u32 BE total file size | `0007f5c9` = 521673 = actual size (all 3 match) |
| 0x0C | 28 | UNKNOWN; differs per file; not MD5/SHA1/SHA256 of file, file[0x28:], or file[0x2c:] (tested) | `dbaeabcd…cc5d7106` |
| 0x28 | 4 | tag `rply` | `72706c79` |
| 0x2C | 4 | u32 BE, always 0 | `00000000` |
| 0x30 | 4 | u32 BE JSON length N | `00000933` = 2355 |
| 0x34 | 4 | u32 BE, always 0 | `00000000` |
| 0x38 | N | UTF-8 JSON metadata `{"game":{…},"player_<id>":{…},…}` | `7b2267616d65223a` |

Payload starts at 0x38+N (Sample1 0x9a4, Sample2 0x96b, Sample3 0x2826).
JSON is a flat-string-valued object (Version, Map, Seed, InitMoney, TimeLimit,
ScoreLimit, VictoryCond, per-player PlayerName, PlayerDeckContent, PlayerAlliance…).

## 2. Chunk stream — VERIFIED

Repeated to EOF, no padding, no trailing bytes (walk ends exactly at file size in all 3):

| Rel | Size | Field |
|---|---|---|
| +0 | 4 | tag: `star`, `pact`, `endt` (no other tag observed) |
| +4 | 4 | u32 BE, always 0 (may be high half of a u64 length: UNKNOWN) |
| +8 | 4 | u32 BE payload length L |
| +12 | 4 | u32 BE, always 0 |
| +16 | L | payload (little-endian internals) |

Evidence: Sample2 0x96b `73746172 00000000 00000008 00000000` + 8 bytes, next
`pact` at 0x983 = 0x96b+16+8. Confirmed independently via REA/Ghidra 12.1.4
read_bytes/search_bytes (evidence ids ev_fbeb6905…, ev_0d8a7293…).

## 3. Frames — VERIFIED

`star` … `pact`×S … `endt` forms one frame. S = slots per frame, constant per file
(Sample1 4, Sample2 2, Sample3 20), equals game.NbMaxPlayer in all 3 samples.

- `star` payload: u32 LE frame index (0,1,2,… no gaps) + remainder. Remainder is
  4 zero bytes (L=8) in Samples 1–2; Sample3 also has L=34 (2188×) and L=60 (2×): UNKNOWN content, preserved.
- `endt` payload (L=12): u32 LE frame index + 8 zero bytes.
- Counts: frames = star = endt; pact = frames × S (76132 = 19033×4; 9026 = 4513×2; 223300 = 11165×20).

Frame-to-time mapping: UNKNOWN (no tick length found in file).

## 4. `pact` payload (little-endian) — VERIFIED framing

| Rel | Size | Field |
|---|---|---|
| +0 | 4 | u32 frame index (= enclosing star) |
| +4 | 4 | u32 slot (0..S-1, in order) |
| +8 | 4 | u32 count (0 ⇔ empty; observed 0–6) |
| +12 | 2 | u16 block length B |
| +14 | B | command block (14+B = L for all 10,942 non-empty pacts) |

Empty pact: L=14, count 0, B 0 (297,516 of 308,458 pacts).
Block = `count` concatenated commands, each starting with an opcode byte. Commands are
NOT individually length-prefixed; splitting count>1 blocks needs per-opcode lengths (UNKNOWN for most).
Observed opcodes (count==1): 02 04 07 08 09 0a 0c 0d 0e 13 17 18. Fixed lengths seen:
09/0e/04 = 25, 0a = 29, 13 = 13, 18 = 10, 02 = 22, 0c = 105 (+281 once). 07 = 91+20k. 08 = 39+text.

Common pattern in many opcodes: `op | u32 handle | 12 zero bytes | u32 0x32 | …`.
Handle = 0xC000001E + slot (VERIFIED for opcode 08; also seen in 04/09/0a/0c/0e). Other handles
(e.g. 0xc00000ba in op 07, 0xc00001a3 in op 17) are UNKNOWN object ids.

## 5. Opcode 0x08 — layout VERIFIED, meaning INFERRED

| Rel | Size | Field |
|---|---|---|
| 0 | 1 | 0x08 |
| 1 | 4 | u32 player handle (= 0xC000001E + slot, 226/226) |
| 5 | 12 | zero (226/226) |
| 17 | 4 | u32 = 0x32 (observed) |
| 21 | 12 | 3 × f32 (values in same range as op 0x0c positions; INFERRED world position x,y,z) |
| 33 | 4 | u32 type: 0,1,2,3 |
| 37 | 2 | u16 text length T (T>0 ⇔ type 3, 226/226) |
| 39 | T | UTF-8 text |

Length = 39+T exactly, all 226 instances. Example Sample1 frame 131 slot 2 (block at 0x69a7):
text "leave your cv at base". Texts are contextual tactical chat ("smoke", "tank",
"we need a cv here"), consistent with the in-game map-flare/marker command. Type
meanings (0/1/2) UNKNOWN.

## 6. Inputs vs. outcomes

Stream structure (one input packet per slot per frame, mostly empty) matches lockstep
input recording. No kill/hit/score/position-snapshot records identified. Outcomes very
likely require simulation reconstruction (INFERRED, not proven).
