# FORMAT.md — Wargame: Red Dragon replay (.wargamerpl2)

Status legend: VERIFIED = holds on every byte of all 3 samples (see samples/manifest.json);
INFERRED = consistent with evidence, meaning not proven; UNKNOWN = not determined.

Samples: koppeltar-Sample1/2/3 (game Version 59638, 510117427, 59638). Only one
container version (1) observed. No version-specific layout differences observed.

## 1. File header (big-endian) — VERIFIED

| Offset | Size | Field | Evidence (Sample2) |
|---|---|---|---|
| 0x00 | 4 | magic `ESAV` | `45534156` |
| 0x04 | 4 | u32 BE container version = 1 (name INFERRED). Executable 59638 accepts <= 1 (FUN_010b9300) | `00000001` |
| 0x08 | 4 | u32 BE total file size (read via ntohl, FUN_010b9790; no equality check found in the executable) | `0007f5c9` = 521673 = actual size (all 3 match) |
| 0x0C | 28 | SHA-224 of file[0x28:EOF]. VERIFIED on all 3 samples; the executable initializes SHA-224 (FUN_016fd070) and compares 28 bytes | `dbaeabcd…cc5d7106` |
| 0x28 | 16 | chunk 0 header: tag `rply`, field A = 0, length N, field B = 0 (same layout as section 2; executable treats it as an ordinary chunk) | `72706c79 00000000 00000933 00000000` |
| 0x38 | N | chunk 0 payload: UTF-8 JSON metadata `{"game":{…},"player_<id>":{…},…}` | `7b2267616d65223a` |

Payload starts at 0x38+N (Sample1 0x9a4, Sample2 0x96b, Sample3 0x2826).
JSON is a flat-string-valued object (Version, Map, Seed, InitMoney, TimeLimit,
ScoreLimit, VictoryCond, per-player PlayerName, PlayerDeckContent, PlayerAlliance…).

## 2. Chunk stream — VERIFIED

Repeated to EOF, no padding, no trailing bytes (walk ends exactly at file size in all 3):

| Rel | Size | Field |
|---|---|---|
| +0 | 4 | tag: `star`, `pact`, `endt` (and `rply` as chunk 0). Executable also handles `cmpg` (not seen) |
| +4 | 4 | u32 BE field A, always 0 in samples; executable passes it to the visitor (meaning UNKNOWN) |
| +8 | 4 | u32 BE payload length L; executable rejects L > remaining bytes |
| +12 | 4 | u32 BE field B, always 0 in samples; executable reads and discards it |
| +16 | L | payload, handed raw to the visitor (little-endian internals) |

Executable path (build 59638, details in REA-NOTES-59638.md): FUN_010b9500 reads the 4
header words via ntohl, bounds-checks L, hashes header+payload into SHA-224, and calls
visitor vtbl[+8](tag, A, ptr, L).

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
not universally length-prefixed; splitting uses creator-proven reads. Count linkage is
verified in research/count-loop.md; layouts and evidence in research/COMMAND-LAYOUTS.md.
Observed opcodes (count==1): 02 04 07 08 09 0a 0c 0d 0e 13 17 18. Fixed lengths seen:
09/0e/04 = 25, 0a = 29, 13 = 13, 18 = 10, 02 = 22, 0c = 105 (+281 once). 07 = 91+20k. 08 = 39+text.

Common pattern in many opcodes: `op | u32 handle | 12 zero bytes | u32 0x32 | …`.
Handle = 0xC000001E + slot (VERIFIED for opcode 08; also seen in 04/09/0a/0c/0e). Other handles
(e.g. 0xc00000ba in op 07, 0xc00001a3 in op 17) are UNKNOWN object ids.

## 5. Opcode 0x08: TNetworkActionLaunchFumigene. Layout VERIFIED from the executable; field meanings INFERRED

Executable (build 59638): dispatcher FUN_00b24050 reads the opcode byte and indexes the jump
table at 0xb241f4 (opcodes 0x02..0x22). Case 0x08 calls creator FUN_00b2fbc0, which installs
the TNetworkActionLaunchFumigene vtable and reads fields with raw (little-endian) copies.
Full opcode table: REA-NOTES-59638.md and OPCODE_CLASSES in wgrd_replay.py.

| Rel | Size | Executable read | Data observation |
|---|---|---|---|
| 0 | 1 | opcode 0x08 | |
| 1 | 4 | obj+0x04 | u32 = 0xC000001E + slot (226/226); INFERRED player handle |
| 5 | 16 | obj+0x08, raw | `00`×12 `32000000` (226/226); meaning UNKNOWN |
| 21 | 12 | obj+0x18, raw | 3 × f32 in map-coordinate range; INFERRED position |
| 33 | 4 | obj+0x24 | u32 0..3 (0:69, 1:50, 2:27, 3:80); text non-empty iff 3 |
| 37 | 2 | FUN_008fb4a0: u16 T | |
| 39 | T | FUN_008fb4a0: T bytes, narrow string | ASCII in all samples (UTF-8 decode attempted, errors flagged) |

Length = 39+T exactly (226/226). Example: Sample1 frame 131 slot 2, block at 0x69a7:
text "leave your cv at base". Class name plus position plus label suggest a map flare
(INFERRED). Type meanings 0/1/2: UNKNOWN.

## 6. Implemented command splitting (decoder 0.4)

New layouts: 04, 07, 09, 0a, 0e, 17; existing 08 now shares the block cursor.
0d has a proven length-delimited serializer envelope; interior fields stay opaque.
New field names identify object storage offsets, without assigning game meanings.

| Opcode | Total command bytes | Verified read layout after opcode |
|---|---|---|
| 02 | 22 | u32, raw16, u8 (research/FIXED-OPCODES-02-13-18.md) |
| 04 / 09 | 25 | u32, raw16, u32 |
| 07 | 71+20*(N1+N2)+T | twice (u32 N, raw20*N), raw12, raw8, raw36, u32 <=3, u16 T, T bytes |
| 08 | 39+T | section 5 |
| 0a | 29 | u32, raw16, u32 <=14, u32 |
| 0c | 61+4*(n1+n2+n3)+16*(m1+m2) | u32, raw16, (u32 n1, u32*n1), (u32 n2, u32*n2 each <=0x0e), twice (u32 m, (raw12, u32 <=6)*m), (u32 n3, u32*n3), u32, raw16 (research/CHANGEPRODUCTION-0C.md) |
| 0d | 18+L | u32 variant 1..3, raw4, raw1, raw4, u32 L, opaque L-byte serializer payload |
| 0e | 25 | u32, u32, raw16 |
| 13 | 13 | u32, u32, u32 (research/FIXED-OPCODES-02-13-18.md) |
| 17 | 10+8*N | u32, u32 N, raw8*N, raw1 |
| 18 | 10 | u32, u32, u8 (research/FIXED-OPCODES-02-13-18.md) |

Each pact preserves block_hex and adds command_decode:
- complete: count commands, full supported field layouts, exact EOF.
- framed: count command boundaries and exact EOF, with opaque serializer content.
  Interior validity and creator acceptance are unverified. Not counted as decoded.
- unresolved: unsupported opcode; retain verified prefix and unconsumed bytes.
- malformed: proven read, count, enum or exact-EOF violation; retain raw block.

Each command records offset, length, raw_hex, fields, field_decode_status.
On unsupported/truncated commands, consumed_bytes ends at the last complete command;
remaining_hex includes the entire unresolved command. No opcode scanning/resync.
Only complete/framed blocks increment fully_split counts; only complete blocks
increment fully_decoded counts. Exact EOF is strict decoder policy, not executable parity.

SHA-256-authenticated census: 594/594 multi blocks split; 571 complete +23 framed.
All new binary evidence is build 59638; Sample2's structural match does not establish
its executable behavior. See research/coverage.json for per-sample counts.

## 7. Inputs vs. outcomes

Stream structure (one input packet per slot per frame, mostly empty) matches lockstep
input recording. No kill/hit/score/position-snapshot records identified. Outcomes very
likely require simulation reconstruction (INFERRED, not proven).

## 8. Optional timeline export

`python3 wgrd_replay.py REPLAY --timeline` produces `wgrd_timeline/1` JSON.
Default JSON unchanged; `--timeline --summary` omits events but keeps counts,
metadata, uncertainty and unresolved raw spans. SHA-224 enforced by default.

Events: zero-based global `command_order`, raw `frame`, `frame_command_order`,
`player_slot`, `slot_command_order`, opcode, RTTI class, original decoded
`parameters`, `raw_hex`, `decode_status`, layout-build status and `source` offsets.
Source offsets in bytes, zero-based: chunk header; command relative to block;
absolute file position; length. Each event's raw bytes cover exactly that range.
`interpretation` separately holds action, semantic parameters, evidence and limits.
`verified` / `partial` require matching 59638; other builds use `inferred`.
Marker create/remove and opcode07 requested kinds are supported interpretations.
Effective orders/outcomes unresolved. See research/TIMELINE-SEMANTICS.md.

Raw frames have no verified duration. Player slots have no verified metadata-name
mapping; identity is null. Full metadata and unknown chunks retained.
Unknown single commands retain entire raw bytes; multi-command unresolved tails
use one placeholder per declared command and one shared raw span, with individual
boundaries unknown. Known malformed blocks fail export instead of generating
misleading events. Opaque 0d interiors remain opaque. Raw bytes also preserve
nonfinite floats; timeline JSON uses explicit nonfinite objects and null semantic
positions. No NaN/Infinity JSON tokens.

### 8.1 Opcode07 requested order subtypes

`interpretation.parameters.order_kind_u32`: object+e0, u32 at order-structure+10.
`order_kind`: executable enum name for explicit requests; null for contextual39
or unnamed values. `order_selection`: explicit_request / runtime_dependent / unknown.
`effective_order_kind` remains null: execution may choose different kinds per actor.
Matching-build explicit request classification is verified; contextual/unnamed
kinds partial; mismatched builds inferred. Status describes request classification.

`actor_references` from obj+04, `target_references` from obj+60: each entry preserves
all20 bytes and exposes its leading registry lookup key. Do not identify entities
or deduplicate references by this first word alone. Entity type/name/group expansion
requires runtime state. `target_position_argument_f32` is transmitted finite float3
from obj+bc, with raw bytes retained; actual position can be clamped or taken from
target state. All+Infinity -> absent sentinel; other nonfinite -> null. Exporter
omits Stop's positional interpretation. No effective destination is asserted.
`secondary_vector_hex`, dispatch token/mode, order_structure_hex and original raw
parameters remain available without guessed option semantics.

Execution addresses, enum table, request-vs-effective limits and census:
research/OP07-ORDERS.md, research/op07-coverage.json.

### 8.2 Replay-scoped reference catalog and conditional context rules

Each actor/target reference also exposes trailing16 bytes as validation_guid_hex,
four LE u32 words, and four-word colon text (not RFC UUID ordering).
reference_id = full replay SHA256 + ':' + full20-byte reference_hex.
entity_references catalogs these IDs: first/last frame and global command order,
actor/target occurrence counts, observed command player slots. Duplicate array
entries count separately. Same key/different GUID remains separate and flagged;
shared GUIDs do not merge registry keys. No unit type/name, ownership, live
registry acceptance or cross-replay identity asserted. unit_identity:null.
Catalog covers decoded opcode07 arrays only; retained by --timeline --summary.

contextual_order_rules describes build59638 c9a140 fallback branches. It is
conditional metadata, not a complete classifier or observed outcome. Kind39
events add contextual_resolution with fallback_reached:null and effective kind
null. Runtime module/member flags and earlier path results unavailable here.
Sample2 event evidence remains inferred. See research/ENTITY-CONTEXT.md and
research/entity-coverage.json for executable conditions, evidence and limits.

### 8.3 Optional public descriptor snapshot

`--timeline --unit-data ROOT` reads four hash-pinned ResidentMario/wargame-data
58710 files beneath ROOT; offline, no automatic downloads. URLs and hashes:
research/public-unit-sources.json. Exact16-byte validation GUID match only.
NDF XML GUIDs use mixed-endian .NET notation, converted with UUID.bytes_le.
Runtime lookup keys, NDF instance IDs and deck indices are separate namespaces.

Reference catalog gains static_descriptor, descriptor_match_status and top-level
descriptor_data provenance. Descriptor fields: NDF class/instance ID/debug name,
module reference and selector Default references; direct TUniteAuSolDescriptor
card values where available. Card flags describe the static source snapshot.
All current samples differ from58710: exact_guid_cross_version, no verified
matching-build names/capabilities. Sample2 reference-purpose mapping inferred.
No company/member GUID rewriting; unit_identity stays null; order39 unresolved.
Events unchanged. Without --unit-data, both default and plain timeline outputs
unchanged. See research/PUBLIC-UNIT-MAPPING.md for counts and missing bridge.

### 8.4 Original59638 configured-type index and localized names

`--timeline --unit-data research/unit-data/build59638-v1.json.gz` loads the
bundled `wgrd_unit_index/1` index. Plain JSON index files also accepted. Offline;
the existing58710 directory mode and outputs remain compatible.

Each reference gains `configured_unit_types`: `status` unique/ambiguous/missing,
`evidence_status`, original source descriptor object IDs, and candidate arrays.
Candidates expose configured type GUID/class, debug name, raw alias, localized
name/status/candidates and mapping provenance. `localized_name` is populated only
for exactly one dictionary record; never falls back to alias/debug text. Original
dictionary markup retained. Duplicate translations and inverse mappings retained
as candidate arrays. Missing source descriptors/paths/names remain explicit.

Exact wire validation GUID joins to original descriptor GUIDs. Inverse paths retain
unit -> CompanyUnit selector Default -> module -> CompanyDescriptor object IDs;
direct AuSol GUID matches remain separate. Shared `descriptor_data.nodes` records
contain original classes, absolute expanded-NDF offsets and mapping/name properties,
including raw filter conditions. `descriptor_data` also carries index/archive/
member/expanded/parsed-object/dictionary hashes and locale. Node properties are a
projection, not complete object/module dumps. Conditions never evaluated.

59638 match means configured static type association, not live registry acceptance,
membership, ownership, active modules or capabilities. Sample2 remains
`inferred_build_59638`. `unit_identity` stays null; event parameters, classification,
effective kinds and contextual39 outcomes unchanged. Default/plain timeline output
byte-identical to02b4081 on all samples. See research/TIMELINE-59638.md.
