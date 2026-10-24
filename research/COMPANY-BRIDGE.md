# Company/member bridge — matching executable59638

Follow-up: original NDF acquired and verified. NDF59638-BRIDGE.md records2121
explicit static paths and unique configured type associations for all685
matching-build replay references. Missing-file discussion below is historical.
Live membership, selector conditions and effective order remain unresolved.

Baseline4b77c21. Bounded REA6.7.0 MCP / Rizin pass. No game execution,
NDF download, registry mutation, public-table substitution or simulation.

## Result

**Static schema link found, values unavailable locally.** This is not evidence
that actual unit-type reconstruction requires simulation. Static descriptor
association and current live company membership are separate tasks.

The useful direction is **unit -> company**, then invert verified references:

```
TUniteAuSolDescriptor
  Modules[CompanyUnit]
    TModuleSelector.Default
      TCompanyUnitModuleDescriptor.CompanyDescriptor
        -> TUniteDescriptor (company)
```

Build59638 evidence:

- c51593 names TCompanyUnitModuleDescriptor, size1c. Constructorc54470
  installs vtable19b3bc4 and initializes its+18 reference to null.
- c55fb0 reflects CompanyDescriptor at offset18. Property helperc1f730 installs
  vtable19b2344. RTTI at1ed35a8 identifies a refptr<TUniteDescriptor> property.
  **The field is a static descriptor reference, not a runtime entity ID.**
- Older public58710 XML provides2099 explicit CompanyUnit slot references,
  all selector defaults typed TCompanyUnitModuleDescriptor. This supports the
  graph shape only. That table's values are omitted from the public export;
  neither its values nor cardinality are transferred to59638.

An inverse index must retain zero/multiple matches and duplicate/variant cases;
no assumption that one company descriptor corresponds to exactly one unit type.
No GUID-word substitution or Company_ -> Unit_ string substitution.

## Important correction: PorteurDescriptor is graphics

The missing TUnitListCompanyModuleDescriptor is not the direct member-unit link:

- d9fe80 registers size30 and constructordab7d0 installs vtable19c09c4.
- dad680 reflects PorteurDescriptor+18, CompanyMergeRadius+1c,
  NbUniteInCompagnieToSpawn+20, NbUniteInCompagnieMax+24,
  EspaceEntreMembreCompany+28, CanBeSupplied+2c.
- PorteurDescriptor helpera6a5d0 installs vtable1998104. Its RTTI at1e99ed0
  is refptr<TGfxDescriptorPorteur>, **not a unit descriptor**.
- These fields describe company configuration, spawn count/spacing and graphics;
  names alone do not establish current member references or member-unit type.

Earlier PUBLIC-UNIT-MAPPING.md identified the absent table as a likely bridge.
This pass narrows the real bridge to TCompanyUnitModuleDescriptor.CompanyDescriptor.

## Original asset located in cached Steam manifest

No NDF_Win.dat/everything.ndfbin found in local artifacts, workspace, Downloads,
known Steam/Wine installation locations or indexed filename search. This is a
bounded local search, not proof that no unindexed/external copy exists.
Existing cache contains only binaries/DLLs/redistributables and depot metadata.
No original NDF bytes available to extract or authenticate.

Cached Windows data depot entry:

- App251060; depot251062; manifest7569342467126442184.
- Data/WarGame/PC/59638/NDF_Win.dat.
- Size24,199,168 bytes; expected content SHA1
  bfd6c3e8affaad83a08ccff3271f6e4a5447e590.
-26 chunks; compressed chunk sizes sum4,790,480 bytes. Not an archive size promise.
- Cached manifest SHA25609747c171db5743e2ad8b5bcd52d0369ae2ff91f5856960ea56676e749c5510c.

These are manifest expectations, not hashes of an acquired NDF. Manifest
signature not independently revalidated. File path version agrees with replay
executable59638; loaded NDF dependencies/localization still need verification.
No need to fetch the full game to obtain this one file from an owned install.

Durable target: matching-ndf-target.json. Read-only reproduction:

```
python3 -B research/ndf_manifest_target.py CACHED_MANIFEST
```

Field definitions: SteamTracking/Protobufs content_manifest.proto; FileMapping
filename1,size2,sha_content5,chunks6; metadata depot1,manifest2,encryption4.
File content hash semantics cross-checked with ValvePython/steam manifest.py.
Sources:
https://github.com/SteamTracking/Protobufs/blob/master/steam/content_manifest.proto
https://github.com/ValvePython/steam/blob/master/steam/core/manifest.py

## Static identity vs simulation boundary

Next bounded task once original file is available:

1. Validate file SHA1 against the pinned manifest entry; record independent SHA256.
2. Read only everything.ndfbin and the needed unit/module/selector tables.
3. Follow actual CompanyUnit -> selector Default -> CompanyDescriptor references.
   Invert to candidate unit descriptors; keep ambiguous/missing links explicit.
4. Resolve unit DescriptorIds/debug names/localization from matching data and its
   verified dependencies. Compare all685 matching-build references; Sample2's41
   remain inferred until matching executable/data available.
5. Enrich only static type association. Do not infer current member count,
   individual member runtime IDs, ownership, position or effective order.

Current member arrays and per-member module flags/state are live data. Earlier
ca0620 evidence reads a live array through6e2140 and tests runtime flag0x10;
c9a140/earlier paths also need current state. TUnitListCompanyModule itself is
allocated atd9f6c0 with separate mutable fields; daf210/daf350/daf470 implement
runtime load/save/copy paths. A static CompanyDescriptor link cannot substitute
for this state. No new effective order39 classifications.

Decision: pursue **one matching-data extraction pass**, not simulation. If data
is unavailable, park static name recovery; do not extend REA/spreadsheet inference.
Useful next timeline work can operate on the current facts: frame/slot filters,
reference-linked order history and requested-order/target summaries. Unknown
seconds, identities, order39 choices and execution outcomes stay unknown.
No timeline feature added during this schema-only pass.

## Evidence and validation

Canonical records under research/evidence/:

- ev_7be47b1c…: class/type names; live-array accessor6e2140.
- ev_56c195ed…: d9fee3/c51593 class registration arguments.
- ev_80f7d249…: aligned dab7d0/c54470 constructors.
- ev_5a0ebdad…: complete dad680 and c55fb0 field registration.
- ev_c4c3078f…: typed property helper constructors; runtime copy path.
- ev_01688e53…: exact property RTTI confirms GfxDescriptorPorteur vs Unité type.
- ev_ba600a04… / ev_b5e90ca1…: runtime module allocation/state serialization.

Exploratory unaligned starts are not supporting proof. No repeated Ghidra import
or reviewer loop. Executable/sample bytes unchanged. Product decoder unchanged;
no redundant63-test regression rerun. Manifest target reader exercised against
actual cached manifest, declared chunk sizes reassemble expected total length.
