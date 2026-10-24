# Opcode 07 — requested tactical orders, build 59638

Baseline 902e1368e60dd9302b750e98cfb45564f15d5060. REA 6.7.0 MCP, installed
Rizin provider; immutable PE32/x86 executable SHA-256
1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.
No game execution. Canonical evidence under research/evidence/.

## Discriminator and independent fields

Creator b2f850 layout unchanged. b2cc90 copies obj+d0 through abb0d0, which
copies byte offsets 0..8, u32 offsets 0c/10/14/18/1c, bytes20..23 (36 bytes).
Copy goes through b31e30, b32270, b32480 into b32690 arg+18, then c972a0 arg+1c.

- **Requested order kind:** u32 LE at order structure+10 = object+e0.
  Wire offset relative to command: `45 + 20*(N_actor+N_target)`.
  c97414, c97e51, c993b2 and c9a18e consume this field as a kind.
- **Dispatch token:** u32 at structure+14 = object+e4. Compared with interned
  order tokens in singleton203bee0; not the same numeric namespace as kind.
  Preserve raw integer, no hardcoded replay-token-name mapping.
- **Dispatch mode:** object+f4, creator bound <=3. Every authentic 07 has mode1.
  No move/attack classification from this field. Queue/append meaning unproven.
- Remaining bytes/flags retained as order_structure_hex and original parameters.
  No speculative fast-move/road/fire-at-will names.

Reflection descriptor at 1d868b8 pairs name pointer198e3a8 (`OrderType`) with
name/value table1d86488. Example rows: Move=4, Attack=6, Stop=10,
UnloadFromTransport=14, MoveAndAttack=16, Shoot=19, Reverse=27, Length=39.
Exact raw pairs, strings and descriptor are executable data, not sample heuristics.
Names0..35 recovered; values36..38 are not named by this table. No guessed names
for these slots. `Length`39 is handled specially by code and never exported as a
specific tactical subtype.

PE mappings independently read from section headers:
.text VA401000 file400; .rdata VA1914000 file1513000;
.data VA1d6c000 file196b000. Do not use one constant for every section.
An initial exploratory string-pointer search used an incorrect .rdata delta;
its unrelated hits and unaligned pD output are not supporting evidence.
Final table/strings checked using correct mappings and REA virtual addresses.

## Requested kind -> execution paths

b32690 calls c972a0 to group actors by concrete order kind. Each group occupies
20 bytes; b32a00 indexes with `20*kind`; b341b4 bounds the loop to39 groups,
excluding sentinel39. Requested kind is not guaranteed to equal every actor's
resolved kind. Actor validity, capabilities, target relation and modules intervene.

| Request | Entry / routing evidence | Limit |
|---|---|---|
| 4 Move | c97e51 compares4; ca0620 chooses4 or9; c99cb0 fills group4 position | May become DoNothing; no guaranteed movement |
| 6 Attack | c993b2 compares6; c9a26d..c9a2c8 routes groups4/9/16 by target/capability checks; explicit attack-target paths also checked in c98xxx/c99xxx | No hit/kill/success assertion |
| 10 Stop | named enum request; generic group -> b33bf1 -> abd410 | Position bytes not interpreted as destination by exporter policy |
| 14 UnloadFromTransport | c97414 treats14 specially; c99e10 fills group14 position; generic dispatch | No passenger identities or observed unloading |
| 19 Shoot | group19 -> b3341a; target position fetched via c7e350 or copied b33554 from transmitted point when no target; parameter construction b33896 | Target state can replace transmitted point |
| 27 Reverse | c97fd5 compares27; specific group construction and generic dispatch | No speed/heading/outcome inferred |
| 1 Land,15 MergeCompany,20 SplitCompany,28 Spread | enum/table names; request consumed by the same kind grouping and generic dispatch | Names classify requests; no simulated effect |

Most concrete kinds take b33bf1: b33c5f pushes the concrete kind to abd410.
abd410 copies actor/target vectors through ab6660, records the kind in typed
input field0x48 (abd5e0..abd5fb), position in field0x4b (abd761..abd7a6),
secondary vector in0x4c, complete order structure in0x4d (abb0d0 atabd8a5),
then submits through af9f60 atabdb75. This is execution-path evidence of a
requested order, not just RTTI or enum naming. The final per-unit state machine
and effects are outside this offline request decoder.

Named order-token singleton initialized by b67c00: `Move` at+18, `Stop`+1c,
`Attack`+24, `MoveAndAttack`+4c, `Reverse`+58, airplane tokens+6c/+70/+80/+84.
These are interned token fields, not stable numeric kind values. The earlier
unaligned dumps beginning b67c70/b67c80 were discarded for interpretation;
b67c00 and b67d27 are aligned supporting instruction starts.

### Contextual kind39 — established blocker

c9a18e compares the requested kind with39. Depending on cc0210 and runtime
module fields, c9a19a..c9a235 selects Move4, DoNothing9, AirplaneTakeOff32 or
AirplanePatrol33. Other earlier c972a0 branches test target relation, modules,
capabilities and order tokens. The same request can split into several groups.
Do not label all39 requests Move. A matching executable alone does not supply
runtime world state. Need actor/module descriptors and state reconstruction to
recover effective kinds; options or target presence alone are insufficient.

## Reference roles and positions

b2cc90: obj+60 resolves atb2cd44, obj+04 resolves atb2cd5c; b2cd7e/7f pass
obj+04 first, obj+60 second into b31e30. Subsequent wrappers preserve roles.
b32690 filters the first list, copies the second list; c972a0 iterates the
first list (arg+10, c975e1 onward) as recipients and uses second list (arg+14)
for target lookup/relation and target slots (e.g. c99d3d..47). Therefore:

- obj+04 array: actor/recipient entity references (can include groups).
- obj+60 array: target entity references. Preserve every entry and order; some
  handlers use only first or derive positions from targets.

Each wire reference is20 bytes: leading u32 lookup key plus16 additional bytes.
b2e070 builds lookup material, calls ae5690 then ae5730, performs context/identity
checks before appending resolved handle. No lookup failure means unit name unknown;
no dropped reference or fabricated unit type. Preserve full reference_hex.
First word alone is not a safe deduplication key; exporter never merges by it.
No claim that reference bytes identify a stable global unit across samples.

obj+bc..c4 are float32 target-position argument; moved by movss in b2cc90,
passed as float3 through wrappers, copied b32708..29. bb19b0 clamps first two
components against runtime world bounds (+margin). c99cb0 fills concrete Move
positions; b33554 supplies Shoot position when no target list. If targets exist,
b334dc/c7e350 can fetch target state instead. obj+c8/cc is a secondary float2
argument, used in spatial lookups when non-Infinity, but roles/units remain
unresolved; export raw bytes only. No heading/direction label.

Export finite transmitted target argument, not reconstructed destination.
All+Infinity is the sentinel checked atb32743; mixed Inf/NaN -> null/nonfinite.
Stop position omitted as conservative interpretation policy, not a claim that
its bytes are absent from the stream. Raw position bytes always retained.

## Implementation and coverage

wgrd_orders.py layers request interpretation over existing proven layouts;
wgrd_replay.py default parser unchanged. `--timeline` gains kind enum/name,
selection status, actor/target references, finite target-position argument,
raw options/token/mode and null effective kind/position. Matching59638 explicit
requests `verified`; contextual/unnamed kinds `partial`; every unmatched build
`inferred`, including Sample2. Verified means static request classification only.

| Sample | 07 commands | Explicit | Contextual39 | Semantics |
|---|---:|---:|---:|---|
| 1 | 3794 | 476 | 3318 | matching59638 |
| 2 | 86 | 31 | 55 | inferred510117427 |
| 3 | 6581 | 1321 | 5260 | matching59638 |

Matching-build explicit counts: Move481, Attack399, Stop187, Unload229,
Shoot330, Reverse111, Merge25, Split25, Land9, Spread1 =1797.
Sample2 separately: Move22, Attack4, Stop3, Unload2 =31 inferred explicit.
All10461 retain raw bytes, options and complete reference sets.
Census: research/op07-coverage.json; reproduce research/op07_coverage.py.

Principal evidence:
- ev_5fb36533…: full c972a0, b32690, b2e070 and abb0d0 assembly.
- ev_4d4a3f06…: raw reflected enum pairs.
- ev_8126786a…: aligned token constructor; abd410 request submission; enum descriptor.
- ev_88d6d3f0…: c9a140 contextual selection; position clamp and structure helpers.
- ev_426991a5…: c9aa40 grouping / parameter factories.
- ev_304797ce… (previous milestone): 07 execution-wrapper fields and argument order.
Ghidra decompile unavailable: fresh lazy import exceeded120s startup deadline;
closed only this task's failed provider session. Continued with REA/Rizin.
Native Rizin was used for scratch triage during the pending decompile; final
supporting ranges also captured through REA. No source binary/sample modified.

Validation:50 tests pass, including nine new order tests. All three authenticated
samples: two CLI timeline runs byte-identical, default CLI output byte-identical
to baseline902e136. All11565 events retained;594/594 multi blocks still split
(571 complete layouts,23 opaque-framed). Samples unchanged. CLI results recorded
in research/op07-cli-validation.json. Single bounded review: no actionable findings.
