# Timeline execution evidence — 59638

07 update: requested subtypes, actor/target roles and positional argument now
recovered; see [OP07-ORDERS.md](OP07-ORDERS.md). The original partial-dispatch
findings below describe the prior milestone; contextual39 remains unresolved.

Scope: static REA 6.7.0 MCP `execute_rizin_command`, installed Rizin provider.
No Windows execution. Each canonical evidence JSON records tool request, addresses,
stdout, immutable-source hashes and `artifact_changed:false`.
Target SHA-256: 1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.
Baseline for this milestone: 5be10ad11cdf1d1c8c4dd31206886100852a0d5a.

## Execution dispatch, beyond RTTI

`FUN_00b24580` invokes action vtable +4 (`call` at b245ae). Vtables:
07=19a18b8 -> b2cc90; 08=19a18cc -> b2ced0; 09=19a18e0 -> b2c680.
Evidence `ev_801a59e6…`; handler bodies `ev_304797ce…`.

### 08 — create graphical map marker

- b2ced0 loads obj+18/+1c/+20 using `movss`: three transmitted float32s.
  obj+24 and obj+28 string passed with this vector to aa3d00 through the resolved
  player context's +124 manager (context reference resolved by b2e4f0).
- aa3d00 allocates 0x30-byte marker record: position +0c/+10/+14, type +18,
  string +1c; increments manager+4 to assign record+4 ID. Network command has no
  corresponding explicit marker ID. Capacity eviction can call aa0620.
- aa74b0 creates graphical record via a9d730, copies position into graphical
  +18/+1c/+20 and applies transform helpers. Graphics and label resource names
  `GfxFumigene`/`GfxFumigeneEtiquette` are registered at a76339/a76352; their
  descriptor offsets +54/+58 are consumed by a9d730/aa6a50.
- aa6a50 compares graphical type+24 with 3 and checks nonempty text+28 before
  assigning label text+5c. Graphics include player/alliance/color checks.
- Conclusion: marker creation request at a transmitted position, with type and
  optional text. Not a unit position observation or smoke-weapon deployment.
  World axes/units/map projection and types 0/1/2 remain unknown. Text's UTF-8
  presentation follows existing parser convention; raw text bytes retained.

Evidence: `ev_304797ce…`, `ev_a4e70aaf…`, `ev_c9aa4fd0…`, `ev_5768ef0f…`,
`ev_79ad196d…`, `ev_fa646c3a…`.

### 09 — remove graphical map marker by manager-local ID

- b2c680 resolves same 20-byte context reference, checks context and manager+124;
  pushes transmitted obj+18 to aa0620. Null context/manager: no removal call.
- aa0620 scans marker deque, compares record+4 with argument at aa0677.
  Empty deque or no matching ID returns without effect (aa0644/aa067f/aa0688).
- Match: cancel callback +28 when active, remove graphic via aa3900 when present,
  destroy strings, free record and erase deque element (aa068b..aa0740).
- aa3900 removes graphics/label and owner+ID display association. No unit lookup,
  health change or kill inference.
- Conclusion: remove-marker request with `marker_id_u32`. ID belongs to resolved
  player manager. Cannot prove success or correlate with prior 08 using input
  bytes alone: 08 ID is assigned during simulation, including capacity eviction.

Evidence: `ev_304797ce…`, `ev_a4e70aaf…`, `ev_5768ef0f…`, `ev_db6a7159…`.

### 07 — partial: entity references and standard-order dispatch

b2cc90 resolves both serialized 20-byte-reference arrays via b2e070; passes both,
float vectors, structured payload, mode and string to b31e30. b31e30 translates
resolved handles into network identifiers, then b32270 resolves via entity registry
ae5730 and passes retained entity handles to b32480. b32480 separates a classified
entity group (cc0210) from remaining batch, dispatches b32690; b32690 reaches
order creation c972a0. This establishes order dispatch and reference resolution.
It does not establish which array is actor/target, movement vs attack, coordinate
meaning, entity IDs stable across replay, or outcome. Timeline marks `partial`;
no tactical subtype or unit identity assigned. Further enum/handler reconstruction
is substantial investigation; stop at minimum milestone.

Evidence: `ev_304797ce…`, `ev_a4e70aaf…`, `ev_c9aa4fd0…`, `ev_5768ef0f…`,
`ev_79ad196d…`.

## 0x18 — deactivate_supply_request (target attribution, build 59638)

- Class `TNetworkActionDeactivateSupply`. Raw fields: `obj_04_u32` registry key,
  `obj_08_u32`, `obj_0c_u8`. Layout from FUN_00b2f2e0.
- `parameters.target_reference` attributes the key to a 0x07 wire reference
  only by the rule in research/OP18-SUPPLY-TARGETS.md: exactly one catalog entry
  with that key (`unique_key`) and the issuing slot among its observed slots.
  Otherwise `unreferenced_key`, `ambiguous_key` (several entries; never assigned),
  or `slot_mismatch`. Only `unique_key` carries `reference_id`, GUID and
  `unit_type` (configured static type, present only when unit data is supplied).
- `temporal_relation` (before_first / inside / after_last) is reported, not a gate.
- `status: partial` on build 59638, `inferred` otherwise; `execution_outcome: unknown`.
- Limitations: per-replay key uniqueness only; no consumer traced; obj_08/obj_0c
  meanings and action direction unresolved.

## Player identity and time: unresolved

Metadata inspection on SHA-256-authenticated samples: player_N keys have no direct
slot field. Sample2 has two recorded slots but four metadata player records (two
sentinel UserIds); Sample3 keys are noncontiguous (e.g. player_294). Metadata key,
JSON insertion order and user ID are not proven slot mappings. b34480 resolves
pact slot through a runtime hash table (+7c/+80), not through metadata identities.
Preserve slot number; `player_identity:null`; full metadata retained separately.
08's observed handle=0xc000001e+slot does not prove human identity.

Two bounded time passes: replay loop b3db10..b3dda7, time/tick string search and
references to `DeterministicCurrentTimeInTicks` (a41618 registry binding). No
frame-period relationship recovered. The other raw pointer search hit a42a68
is not sufficient evidence of a code reference (unaligned disassembly). No
seconds conversion; TimeLimit metadata is not measured replay duration.
Evidence `ev_fa646c3a…`, `ev_9ca2938f…`, `ev_db6a7159…`.

## Confidence / export contract

- 59638 replay: 08/09 `verified` request semantics; 07 `partial`; rest `unknown`.
- Sample2 Version 510117427: above interpretations `inferred`, never verified
  against an unavailable matching executable. Layout match alone is insufficient.
- Every command represented in source frame/slot/command order. These are recorded
  input orders, not wall-clock execution timestamps or success/outcome events.
- Known lengths require exact count+EOF. 0d bodies stay `opaque`.
- Unknown single command: entire tail is exact raw command. Unknown multi tail:
  one placeholder per remaining declared command; only first opcode known; one
  shared `unresolved_spans` raw payload; no individual lengths or scanned offsets.
- Known malformed layouts refuse timeline export with ReplayFormatError, exit 2.
  Default parser diagnostic behavior remains unchanged.
- Nonfinite floats become explicit `{nonfinite:...}` parameter values; semantic
  marker position becomes null. Original raw bytes retained. Strict JSON output.

Canonical records: `research/evidence/ev_<full SHA>.json`. Prefixes above uniquely
identify records in this repository. Timeline embeds the principal handler and
marker-manager/graphics evidence paths; this note records the complete chain.

Single bounded review: one adopted correction, reject unresolved tails with more
declared commands than available opcode bytes. Default parser behavior preserved.
Focused regression added; no recursive review.

## 0x0C — change_production_request (structural only)

Action `change_production_request` (class TNetworkActionChangeProduction). Creator
FUN_00b2eeb0 and the 0x0C layout are documented in [CHANGEPRODUCTION-0C.md](CHANGEPRODUCTION-0C.md).

- Status `partial` on build 59638 (layout verified, semantics not); `inferred` on other builds (Sample2).
- Parameters are raw wire fields only: `player_id_u32` (with `slot_consistent` against
  0xC000001E + recorded pact slot), `obj_08_hex`, `obj_18_u32_items`, `obj_34_u32_items`,
  `obj_50_points` / `obj_9c_points` (nonfinite markers as decoded), `obj_e8_u32_items`,
  `obj_104_u32`, `obj_108_hex`. No position, heading or production-type names.
- `execution_outcome: unknown`. No consumer was traced, so the effect on production state is not known.
- Limitations: field meanings unconfirmed; point kinds and enum-like values unassigned; Sample2 layout inferred.
