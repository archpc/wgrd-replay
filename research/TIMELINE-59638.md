# Original59638 timeline enrichment

Static bridge baseline02b4081 retained. No new disassembly or simulation.

## Use

```sh
python3 -B wgrd_replay.py REPLAY.wargamerpl2 --timeline \
  --unit-data research/unit-data/build59638-v1.json.gz > output.timeline.json
```

Optional path only. Default/plain timeline unchanged; old pinned58710 directory
mode unchanged. --summary retains enriched reference catalog and provenance.
Join events' replay-scoped reference_id to entity_references.entries. Candidate
localized_name is the configured type's source label, not proof of a live unit.

## Compact index

Bundled research/unit-data/build59638-v1.json.gz; schema wgrd_unit_index/1,
game_build59638. Deterministic canonical JSON, sorted keys, UTF8, newline;
gzip mtime0, no source filename. Export manifest pins compressed and JSON hashes.
~367KB compressed; 4628 source descriptors, 2121 configured types, 8872 projected
source nodes, 2088 distinct name tokens. No replay bytes or complete game DB.

Nodes retain source class IDs and absolute expanded-file object offsets. Descriptor
nodes contain only DescriptorId, ClassNameForDebug, AliasName, NameInMenuToken,
CompanyUnit slots. Selector/module/filter/condition nodes preserve mapping fields.
All references in this projected graph resolve and class-check. Index loader
re-derives candidates from graph edges; rejects inconsistent paths, evaluated
conditions, duplicate JSON keys, malformed names, bad/truncated gzip and schemas.

Configured candidates use explicit inverse CompanyUnit -> selector Default ->
CompanyDescriptor edges or exact direct TUniteAuSolDescriptor GUIDs. Candidate
arrays preserve ambiguity; all4628 source descriptors retained even if no mapping.
No GUID arithmetic, debug-name matching, registry-key/static-ID joins or deck IDs.

## Matching localization

User downloaded Steam app251060/depot251062/manifest7569342467126442184 member
Data/WarGame/PC/59095/59638/ZZ_Win.dat. Size1875968; SHA1
743a93ec96fc3f90caab466cd9ebe60b8c7b24b2, verified against cached manifest.
EDAT directory MD5 verified; 24 entries. Selected US member
pc\localisation\us\localisation\unites.dic: offset1728512, size146404,
MD5 131961df111e7caa602e3fbc809166cf. SHA256s in export manifest.

TRAD header declares3487 records. Each has exact raw8 token, absolute u32 byte
offset and u32 UTF16 code-unit count. All strings bounds-checked, decoded strictly;
3487 distinct tokens, no duplicate records. All2121 configured types resolve
within this59638 member. No ancestor/future dictionary merging needed for those
tokens. Format source: pinned fmdostoyevskiy/wgrd-toolbox scripts/extract.py,
commit69b0b662fd6aa799474432d2391e7ececcf8a44f, manifest public-unit-sources.json.

NameInMenuToken bytes matched directly, no endian/GUID conversion. Example:
Unit_Bo_105CB_Hornisse token372d318d11083403 -> `Bo 105M/VBH #reco2`;
Unit_US_SEAL tokend6f274dd07000000 -> `NAVY SEALS #reco2`.
Dictionary markup/spacing retained verbatim. AliasName and debug_name remain
separate raw fields; neither is relabeled as a localized name.

## Authentic replay result

| Sample | Replay build | References | Unique configured type + localized name | Evidence |
|---|---:|---:|---:|---|
| Sample1 | 59638 | 285 | 285 | matching static configuration |
| Sample2 | 510117427 | 41 | 41 | inferred from59638 |
| Sample3 | 59638 | 400 | 400 | matching static configuration |

Matching-build685/685; total726/726 including inferred Sample2. No observed
ambiguous/missing matches in these samples; synthetic tests exercise both.
All11,565 events unchanged. Runtime unit_identity null; selector conditions
unevaluated; effective order39 kind/outcome unknown. Static module/condition
configuration cannot establish active modules, flags, company members or ownership.
No new capability claims.

## Reproduction and checks

```sh
python3 -B research/export_unit_index59638.py
python3 -B -m unittest discover -s tests
```

Exporter requires cached objects/expanded NDF plus original NDF and localization
archives; paths adjustable via --help. Inputs opened read-only. NDF/archive,
expanded data and parsed objects pinned. source-artifacts.json records parser/hash
binding: existing parser rerun once against authenticated expanded bytes; cached
objects reproduced byte-for-byte. Export refuses a changed parsed-object input.

Focused integration tests: exact company/direct joins, complete node/filter
provenance, ambiguous/missing associations and names, Sample2 inference, unchanged
events/source index, authenticated replay counts, deterministic enrichment/CLI,
malformed schemas/graphs/UTF16/string lengths/gzip and altered export input.
Bundled index tested without external game files; authentic replay test skips
only when samples unavailable. Existing public58710 integration also retained.

Full default and plain timeline CLI stdout compared byte-for-byte to02b4081 on
all3 samples: research/unit-data/cli-compatibility.json. Review found input-object
authentication and invalid-DEFLATE error gaps; both fixed with focused tests.

User-created Sample1 export inspected directly and reproduced byte-for-byte:
research/SAMPLE1-TIMELINE-VALIDATION.md and unit-data/sample1-timeline-validation.json.
285/285 references localized; 102 configured types; 4162 events. Legacy generic
limitations still say names unresolved; enrichment candidate records supersede
that wording for configured static labels only. Runtime identity remains unknown.
