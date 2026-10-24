# Original59638 NDF — company/member type bridge

Start57019cf. Research only; replay decoder and tests untouched. Original archive
opened read-only. Extracted game data and replay-specific paths stay ignored in
work/ndf59638/. No game execution, archive repacking or simulation reconstruction.

## Integrity / extraction

Original: ~/.hermes/artifacts/wgrd-replay/game/win64/Data/WarGame/PC/59638/NDF_Win.dat.

-24,199,168 bytes. SHA1bfd6c3e8affaad83a08ccff3271f6e4a5447e590 matches the
 cached Steam manifest target in matching-ndf-target.json.
- Independent SHA25697d7442eecff5d0f836d5caee4d01cdf93bd7fe262ff12fef75f59fbc84638c0.
- EDAT dictionary:2,664 entries; dictionary MD5 verified. Only
 pc/ndf/patchable/gfx/everything.ndfbin extracted.
- Entry offset843776, size1,505,922; MD5
 5b782ad5e6acd2d5af8e967609ae2ac4 verified before expansion.
- Compressed entry SHA256327361b98ddb5764eb535a573686a1c3788252d49a0c54202939d55f346a5468.
- Expanded20,229,318 bytes; both declared expanded lengths match. Expanded SHA256
 0f11779d9e5592f3fa6e46602d63f1a5022c913f823121d451a385b9c74a6f31.

Zlib stream uses a full-flush ending, without an EOF marker. Published compressor
uses Z_FULL_FLUSH. Expansion consumes all compressed bytes, leaves no unused/tail
input and matches both lengths. Not described as an independently finalized zlib
checksum. Source-header bytes retained in scratch; compressed flag deliberately
not rewritten. Expanded file is an analysis artifact, not a repacked game file.
Steam manifest signature not independently revalidated; file bytes now match its
previously pinned size/content hash. Full acquisition/parse facts:
ndf59638-extraction.json.

## Reader checks

Stdlib research reader; no dependency installed or third-party extractor executed.
Published EDAT/NDF layouts checked against original archive; pinned format-source
revisions/hashes in ndf59638-format-sources.json. Public unit values not used.

- Nine footer blocks cover the expanded body exactly, without gaps/overlap.
-375 classes,1,996 properties,29,016 strings,15,653 import paths.
-120,516 objects, exactly matching CHNK declared count.
- One cursor consumes all17,783,473 OBJE bytes. Reads typed values and object
 terminators; no searching/resynchronizing on ABAB bytes in payloads.
-367,499 non-null object references checked for in-range object index and exact
 class ID;398 explicit null references retained. Table-string/import indices checked.
- Unknown value types fail closed. Missing source types0x1f(EugInt2),0x21(EugFloat2)
 and unsigned16 handling verified against moddingSuite's type definitions; no guessed
 lengths. Early reader assertions for zlib finalization/CHNK leading word/null refs
 were resolved against source format before accepting the data.

## Actual static bridge

Recovered the explicit direction already proven in matching executable REA:

```
unit descriptor.Modules[CompanyUnit]
  -> TModuleSelector.Default
  -> TCompanyUnitModuleDescriptor.CompanyDescriptor
  -> company TUniteDescriptor
```

No GUID changes, debug-name substitutions, arithmetic on IDs, or spreadsheet joins.
Actual59638 NDF object indices differ from58710 indices; links checked within59638.
All4628 unit descriptor GUIDs in the two unit tables are unique.

Counts:

| Table / relation | Count |
|---|---:|
|TUniteAuSolDescriptor|2099|
|TUniteDescriptor|2529|
|TModuleSelector|10422|
|TCompanyUnitModuleDescriptor|2121|
|TUnitListCompanyModuleDescriptor|7|
|Resolved unit -> company paths|2121|
|Distinct inverse company GUIDs|2121|
|Inverse links with exactly one configured unit candidate|2121|
|Missing/null company links|0|
|Observed ambiguous inverse links|0|

Inverse entries remain arrays of complete paths. Zero/multiple matches remain
unresolved/ambiguous if encountered; uniqueness is measured here, not imposed.
This includes2099 ground-unit-table paths and22 other unit-table paths.

All2121 CompanyUnit selectors also have a Selection entry: shared object32739,
TModuleSelectorFilter -> Condition45051, TModuleSelectorCondition_ParamEquals_Integer
with ParamId11 / ParamValue1. Filter records contain a condition, no alternative
module reference in this file. Retained as an **unevaluated condition**. No name
assigned to parameter11 and no claim that the module is enabled for a live entity.
The mapping describes configured static type association through Default.

Example: original Unit_Bo_105CB_Hornisse object19320 -> selector29594 ->
company module41907 -> CompanyDescriptor53200 Company_Bo_105CB_Hornisse.
Individual GUID0000000000000000000000005f080000; company GUID
0000000000000000030000005f080000. These are observed explicit endpoints, not a
rule to replace GUID word3. Matching executable property RTTI confirms that
CompanyDescriptor is refptr<TUniteDescriptor>; PorteurDescriptor remains graphics.

## Authentic replay comparison

Replay hashes verified against samples/manifest.json; existing parser used read-only.
No timeline output or unit_identity field changed.

| Sample/build | References | Inverse company paths | Direct unit GUID | Ambiguous/missing |
|---|---:|---:|---:|---:|
|1 /59638|285|284|1|0|
|3 /59638|400|397|3|0|
|2 /510117427 **inferred**|41|41|0|0|

**685/685 matching-build references resolve to one configured static unit type.**
All685 have a source ClassNameForDebug. Source AliasName present on571 references;
it is not automatically a verified display label. NameInMenuToken hashes retained;
matching localization dictionary not supplied/extracted, so exact localized UI
names remain unresolved. No substitution from older public card names.

Sample2's41 associations are layout/build transfer only; remain inferred even
though its GUIDs match this file. Counts: ndf59638-bridge-coverage.json.
Full per-reference candidates and exact object/file offsets remain in ignored
work/ndf59638/replay-bridge-details.json; full static paths in bridge-paths.json.
No raw replay/game data added to Git.

## Boundary / stopping point

Static type bridge recovered. Missing NDF blocker removed; **simulation is not
needed to associate a declared company descriptor with its configured unit type**.
This does not establish accepted runtime identity, current members/counts,
ownership, damage, position or which selector condition currently holds.
Runtime key translation can bypass descriptor validation; request wire descriptor
is not proof of actual registry acceptance.

Effective order39 still needs live member/module flags/state and earlier-path
results. Static type association does not resolve those values. No effective-order
classification or simulation behavior reconstructed.

Potential later decoder work, outside this request: consume this matching-data
static index with explicit type-association provenance, retaining condition filters
and ambiguous candidates. Localized display text needs matching dictionary data.
Current milestone stops at verified research artifacts; decoder unchanged.

## Reproduction / REA

Run from repository root. Writes ignored scratch only; source archive read-only:

```
python3 -B research/ndf59638_unpack.py
python3 -B research/ndf59638_parse.py
python3 -B research/ndf59638_bridge.py
```

Current REA evidence: ev_c71bc22a… reconfirms CompanyDescriptor+18/refptr type and
company-list static fields in59638 executable. Byte views ev_1de49c5f… / ev_5c5c9e64… of expanded
NDF capture header and sample selector/module/company endpoints. Earlier
COMPANY-BRIDGE.md records full executable chain. No Ghidra/reviewer loop.
Validation consists of actual archive checksums, size/count/EOF/reference checks
and authentic replay joins above; no redundant decoder regression run.
