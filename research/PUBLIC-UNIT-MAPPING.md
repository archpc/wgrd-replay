# Public unit datasets / descriptor bridge

Baseline06d1351. Native REA6.7.0 MCP / Rizin, build59638. No game execution.
Executable SHA2561c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.

## Sources, namespaces, versions

Pinned sources and downloaded-file SHA256s: public-unit-sources.json.
Third-party data stays ignored in work/public-units/. No ResidentMario license
found; toolbox license reserves game content to Eugen. No bulk data redistributed.
No third-party code imported/executed; importer uses Python stdlib.

- [ResidentMario/wargame-data](https://github.com/ResidentMario/wargame-data/tree/1863c5e00f098272aa0299f07ec85eca6004d969),
  commit1863c5e,2021-10-07. Inspected README, export/clean scripts,58710 raw
  descriptor CSV/XML and final_data.csv. Dataset versions include58710,49964,
  510064564 and older; neither59638 nor510117427 present. Version ordering is
  not inferred numerically across the short/long version-number schemes.
- [wgrd-toolbox](https://github.com/fmdostoyevskiy/wgrd-toolbox/tree/69b0b662fd6aa799474432d2391e7ececcf8a44f),
  commit69b0b66,2026-10-02. Inspected extract/enrich scripts, master.json,
  deck_indices.json, README/license. No exact game build recorded for master.
  Commit date is not an executable/data version. Enrichment includes manually
  patched stats and tags; not used as executable proof or runtime capability data.

| Namespace | Actual meaning | Join used |
|---|---|---|
| Replay firstu32 | runtime registry translation key | never static unit ID |
| Replay trailing16 bytes | declared validation descriptor GUID | exact16-byte GUID only |
| ResidentMario final_data.ID | NDF object instance index from XML id | same-snapshot TUniteAuSolDescriptor.id only |
| ResidentMario DeckID | index from TShowRoomDeckSerializer side list | not used for entity lookup |
| NDF DescriptorId |16-byte GUID property | XML/CSV .NET GUID -> bytes_le |
| Toolbox id | DescriptorId raw bytes as32 hex chars | comparison only, no transformed join |
| Toolbox deck index | side-specific10-bit serialization value | not used for entity lookup |
| NameInMenuToken | localization hash | source display name, never entity key |

Sources: export.py get_id/get_deck_id/serialize_unit; toolbox extract.py
NDF_GUID branch returns raw.hex(), _extract_unit_identity assigns DescriptorId;
extract_deck_indices uses explicit descriptor references and side indices.

Important endian detail: ResidentMario's XML/CSV GUID string is .NET Guid
notation. First8/4/4 hex groups reverse within their fields; remaining8 bytes
retain order. Use uuid.UUID(text).bytes_le. Earlier scratch UUID.bytes comparison
missed nonzero second-word GUIDs; corrected before implementation. Toolbox id is
already raw bytes, so no UUID conversion. Test exercises second word7.

## Executable authentication

b2e070 copies trailing16 bytes, resolves b5abd0 -> b5a630, conditionally compares
returned pointer with live object+28. ae5690/ae5730 resolve first-word runtime
handle separately. Translation can bypass descriptor validation; catalog match
is the descriptor transmitted in the request, not proof of live entity acceptance.

b5bf60 reflects DescriptorId at offset0c. b58aa0 installs TSaveableDescriptor
vtable19a30cc, copies object+0c through4f70d0 and removes matching16-byte key from
manager203b890+10 through524ca0/945d40/9487e0. b5a630 looks up that same map;
all four words compared, XOR hashing is not an identity truncation.

b2d263 resolves a GUID through b5abd0, then b2d288..b2d29b dynamically casts the
result from TModularUnitDescriptor to TUniteDescriptor. RTTI chain confirms
TUniteDescriptor -> TModularUnitDescriptor -> TSaveableDescriptor (base offset0).
Together with DescriptorId+0c and the same-map lookup/removal, this identifies the
trailing payload as descriptor GUID material. It is not a unique runtime unit ID.

Canonical evidence in research/evidence/:

- ev_b1d6856e… (prior): complete aligned b2e070 resolution and validation.
- ev_f854a432…: b5abd0/b5a630, b2ddd0.
- ev_a170f55f…: DescriptorId reflection at+0c.
- ev_2679b34d…: aligned b58aa0 descriptor-key removal; b2e pointer comparison.
- ev_31396b02…: b2d200 flow and descriptor RTTI dynamic cast.
- ev_091f83c9…: named RTTI strings and base-class records.

Scratch ranges beginning mid-instruction are not supporting evidence. One REA
call used unsupported psz and returned no stdout; retained as failed-command
provenance, not proof. Corrected ps ascii/pxw ranges captured. No Ghidra retry.

## Authentic comparison

Source hashes checked before parsing every comparison input. Replay SHA256s
checked against samples/manifest.json. No numeric runtime keys equal static
NDF instance IDs in the726 catalog entries; numeric coincidence would not be proof.

| Sample/build | References | TUniteDescriptor exact GUID | TUniteAuSolDescriptor exact GUID | Toolbox direct GUID |
|---|---:|---:|---:|---:|
|1 /59638|285|284|1|1|
|2 /510117427 inferred|41|41|0|0|
|3 /59638|400|397|3|3|

**726/726 exact descriptor GUID matches in snapshot58710.** All722 matches in
TUniteDescriptor have Company_ debug names. Company descriptors include
UnitListCompany, Orderable, Selection and other explicit module references.
Their GUIDs differ from individual units: e.g. public Company_Bo_105CB_Hornisse
has words[0,0,3,2143], Unit_Bo_105CB_Hornisse has[0,0,0,2143]. This observed
pattern is not a verified company/member rule. **No GUID-word rewriting.**

Four direct individual-unit matches have source-snapshot card names:
COMMANDOS PARA (Sample1); BTR-90, COMMANDO-MARINE, PPK FAGOT (Sample3).
These labels/capabilities remain cross-version snapshot data, not verified
matching-build unit identities. No Sample2 card name assigned. All four occur once as target references;
no actor card identity recovered.

Snapshot has2099 TUniteAuSolDescriptor rows,2529 TUniteDescriptor rows.
Toolbox has2202 entries:2075 exact GUID overlaps with the former,22 with the latter.
None of the722 observed company GUIDs directly matches toolbox unit IDs.
This is why linking replay key/counter directly to an armory ID is unsafe.

Counts and role occurrences: public-unit-coverage.json.
Reproduce: python3 -B research/public_unit_coverage.py work/public-units

## Implementation

Opt-in only; plain --timeline and default parser output unchanged:

```sh
python3 -B wgrd_replay.py REPLAY --timeline --unit-data work/public-units/wargame-data
```

ROOT contains the four pinned files listed in wgrd_unit_data.FILES, preserving
repository paths. SHA256 mismatch/missing input fails export. URLs/hash records
in public-unit-sources.json allow reconstructing this small cache without cloning
all historical data. No runtime network access or online name lookup.

entity_references entries gain static_descriptor and descriptor_match_status.
Exact full GUID join; source class/instance ID/debug name, module references,
selector Default references, optional direct unit_card fields. Card ID join only
within58710 TUniteAuSolDescriptor; never across classes or versions. Unit card:
name, movement type, nation, tab, command/transporter/ship/amphibious flags.
Empty values stay null. Static module defaults are not live module presence.

Catalog descriptor_data includes source URLs/commit/file hashes, dataset/replay
versions, mapping evidence, counts and limits. Exact matches here are all
exact_guid_cross_version. Reference-purpose mapping verified for59638, inferred
for Sample2; source values never relabeled matching-build facts. unit_identity
remains null; event interpretations/order classifications/raw bytes unchanged.

## Demonstrated blocker / stopping point

Public58710 company descriptors explicitly reference TUnitListCompanyModuleDescriptor,
but that table is absent from ResidentMario's exported tree. Toolbox flattened
master omits company/member relationships. Cannot prove company -> unit GUID
membership or expand current group composition from these exports. Static
membership would still differ from current runtime membership after split/merge.

Need matching59638 NDF data, company list/module tables and runtime membership
before asserting actual unit types/names for722 company references. Sample2 also
needs matching executable/data. Older static cards do not provide per-frame
module state, member flag0x10 or earlier selection-path results needed for39.
No contextual orders newly resolved. No simulation or speculative identity fill.

Validation:63 tests pass,7 new tests. Exact mixed-endian GUIDs, company/unit
separation, runtime-key collision trap, unknowns, immutable source index,
malformed/duplicate records, missing/modified cache, replay version provenance,
Sample2 inference and all726 authentic joins. Tests using public snapshot skip
if cache absent; set WGRD_UNIT_DATA. Full suite here ran with cache present.
CLI checks: default/plain timeline unchanged against06d1351; two enriched exports
identical per sample; stripping only catalog annotations reproduces plain output.
11,565 events retained;594/594 multi blocks split (571 complete,23 opaque-framed).
Single bounded static review: no actionable findings. See public-unit-cli-validation.json.
