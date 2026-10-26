# Entity references and contextual orders — build59638

Follow-up: PUBLIC-UNIT-MAPPING.md establishes the GUID's descriptor role and
exact public58710 matches for all726 references. This note records the earlier
state of evidence. Unique runtime identity and effective-order limits still hold.

Start4946be4a0f5b953ba09aec960d5c9d4f6963f84a. REA6.7.0 MCP / Rizin,
read-only PE32/x86. Executable SHA256
1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.
No game execution. Sample2 remains inferred: build510117427 differs.

## Reference resolution

Wire reference = u32 registry key +16-byte validation identifier. b2e070 reads
first word separately, copies remaining16 bytes through4f70d0 atb2e138,
advances20 bytes per entry atb2e229. Helper family4f70d0/4f70f0 represents
four-word GUID material:4f715e parses `%x:%x:%x:%x`; failure reports
`Wrong GUID Format`. validation_guid_hex/u32/text preserves word order;
text uses four LE u32 words, not RFC UUID ordering. Component meanings unknown.

- ae5690: registry translation keyed by firstu32; miss returns input key pointer.
- ae5730: translated handle -> live object pointer; missing lookup -> null.
- b5abd0 -> b5a630: saved-object map keyed by all16 trailing bytes.524ca0 hashes
  XOR of four words;945d40 compares all four words. Miss -> null.
- b2e192 reads live object+28. b2e1bc resolves trailing GUID; b2e1e3 repeats key
  translation. If translation equals original key, b2e1ef..f5 rejects when saved
  object pointer differs from live object+28. A translated key bypasses this
  comparison. Null/sentinel live-object paths also skip the reference.

This does **not** prove GUID = unique unit identity, generation, unit descriptor,
or stable cross-replay key. Different registry keys share the same GUID in
samples. No key->multiple-GUID collision observed; not proof against key reuse.

Exporter correlates exact20-byte references within one replay SHA256.
reference_id = SHA256 + ':' + reference_hex. Same key/different GUID remains
separate, flagged ambiguous. Shared GUIDs never merge keys. Catalog records
first/last command occurrence, actor/target counts including duplicates, and
observed player slots. Slots describe command provenance, not ownership.
unit_identity remains null. Only opcode07 actor/target arrays covered.

## Conditional fallback, not an effective-order classifier

c972a0 has earlier actor/target/module/token paths. Only actors reaching c9a140
with requested kind39 use this fallback. Reachability unknown offline.

| Runtime test | Selected kind within fallback |
|---|---|
| cc0210 module exists; module+28 ==1 |32 AirplaneTakeOff|
| cc0210 module exists; module+28 !=1 |33 AirplanePatrol|
| module absent; ca0620 true |4 Move|
| module absent; ca0620 false |9 DoNothing|

cc0210 indexes module registry at global201f660+108 using actor local ID.
c9a210 tests module+28. ca0620 obtains members through registry+1f8 and
6e2140 (module+30 pointer/+34 count); a95090 obtains128-bit runtime flags
from registry+74 per member. ca06d8..ca073a tests mask0x10 in firstu32,
zero masks in other three; false upon any set bit, true when all clear,
including empty list. No recovered name for this flag.

TAirplaneModule RTTI/vtable19b1008 and ctorc283b3 independently recovered;
ctor initializes+28=1. c318f6 reads andc31ac9 writes its+28 runtime state.
**Registry+108 not linked conclusively to this class.** Do not infer class
from branch names or constructor defaults. CanMove reflection strings found
elsewhere do not establish a name for mask0x10.

Timeline exports build59638 conditional metadata. Contextual events retain
fallback_reached:null and effective_order_kind:null. Sample2 contextual
resolution evidence_status=inferred. No branch selected from reference words,
target presence, transmitted coordinates, or observed correlations.

## Runtime-state blocker / milestone

Command07 serializes neither registry resolution nor module presence/state nor
member flags. Catalog supplies correlation, not those values. Effective kinds
also need earlier-path results, target relations, live group membership and
possibly state changes before each command. Initial/runtime data may exist in
still-opaque0d payloads; not decoded here. Matching executable alone cannot
supply per-frame values. Full game simulation out of scope.

Available local game artifact tree: executables, DLLs, redistributables; no
game data archives/descriptor name database located there. Named unit identity
unresolved. No downloads or guessed descriptor mapping.

| Sample | Full references | GUID tails | Occurrences | Contextual39 |
|---|---:|---:|---:|---:|
|1 matching59638|285|103|4552|3318|
|2 inferred510117427|41|29|136|55|
|3 matching59638|400|181|8968|5260|

726 replay-scoped reference IDs;13,656 linked occurrences.685 matched references,
41 inferred. No new effective kinds assigned:1797 matched explicit request
classifications retained;8578 matched contextual requests unresolved.
594/594 multi blocks split:571 complete layouts +23 opaque-framed.

Counts: `python3 -B research/entity_coverage.py`.
Validation:56 tests, including6 new reference/context tests; malformed lengths,
duplicate occurrences, key/GUID collisions, input immutability, all3 authentic
catalogs, strict JSON, Sample2 separation. CLI compatibility/determinism results:
entity-cli-validation.json. Raw replay bytes/exports outside Git.

Principal canonical REA evidence under research/evidence/:

- ev_b1d6856e…: aligned b2e070 resolution and failure paths.
- ev_3f7491c7…: ae5690/ae5730, b5abd0, b2ddd0, cc0210, ca0620.
- ev_efa16b2a…: b5a630, a95090,6e2140, complete c9a140.
- ev_f747e188… / ev_ace17251…: GUID text constructor, hash/comparison.
- ev_c8b71d9c…: exact no-module fallback, pointer validation branch.
- ev_4e31b3d6… / ev_5f87a2e4…: airplane RTTI/ctor/state; class-link limit above.

Exploratory mid-instruction ranges/unrelated reflection hits retained as
provenance, not semantic proof. No second Ghidra import after prior120s startup
failure. Single bounded static review: no actionable findings. No test/review loop.

0x18 DeactivateSupply targets are attributed per replay by unique registry key plus issuing slot; see research/OP18-SUPPLY-TARGETS.md.
