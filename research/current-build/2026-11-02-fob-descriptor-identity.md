# Configured FOB descriptors versus member-unit joins — build 131544

Status: verified static descriptor classification, not ownership or deployment
inference. The V3 position exporter reports it separately from its existing
strict member-unit join.

## Authenticated inputs

- Native archive SHA-256: `172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b`.
- Retained native index SHA-256: `73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d`.
- File-witnessed runtime trace SHA-256: `6d88cefc03e1cf6a9bc4a3ddb70318569789d124266a37ffea1e5f5121601617`.

The archive and index hashes were recomputed against their exact retained paths.
No archive or dataset was modified or re-extracted.

## The two previously unlabelled descriptor tracks

| Capture-local handle | Raw descriptor ID | Native node | Class | Debug name |
| --- | --- | --- | --- | --- |
| 4 | `000000000500000001000000e8030000` | 20843 | `TUniteDescriptor` | `Building_FOB_ISR` |
| 8 | `000000000000000001000000ef030000` | 20846 | `TUniteDescriptor` | `Building_FOB_NK` |

Seven position observations in the new trace belong to these two tracks. Their
raw descriptor IDs uniquely identify those native nodes; the observed name token
`4c06010000000000` agrees with each node but is shared by 23 FOB descriptors.
It is not an independent unique identity leg.

The descriptor index has no member-unit candidate path for either node. Its
retained module graph reaches a company descriptor, not a member leaf selected
by the existing join. That does not prove that a FOB cannot be deployed. Nor do
the debug-name suffixes establish a player's faction or runtime ownership.
The static selector's `ParamId 11 == 1` condition was not evaluated at runtime.

## Additive report contract

V3 position identities gain a separate `configured_descriptor` annotation:

- Require exactly one native index entry for the captured descriptor ID.
- Require the captured name token to agree with that entry, even when shared.
- Require the descriptor index's source-node list to agree with the same node.
- Report the configured class/debug name with status
  `unique_guid_compatible_token` and confidence `static_descriptor_identity_only`.
- Leave class/name unknown on unreadable bytes, missing or nonunique IDs,
  mismatched tokens, or disagreeing source-node records.

The existing `descriptor_join` is unchanged. These seven observations still do
not satisfy `2_of_2_exact_guid_and_token` and receive no member `unit_type_id`.
No ownership, lifetime, combat-source role, kill credit or movement semantics
are inferred from the annotation.

The annotation applies only to V3 position reporting. Earlier runtime output
files remain byte-identical. Removing just `configured_descriptor` from the
new V3 JSON recovers the previous V3 contents; the chronology is unchanged.
Original exports and their independent review are retained, never overwritten.

## Verification scope

A portable production-path regression first failed because the configured
building name was absent, then passed. Controls reject token mismatch, duplicate
IDs, source-node disagreement and unreadable descriptor bytes. The focused AAR
module passed 55 tests; the full canonical suite passed 334 tests with two
existing skips. Ruff, syntax, 72-file documentation and preservation checks
passed. No tests were repeated for hook bookkeeping.

Read-only independent review approved the exact source/test hashes before
commit. It confirmed fail-closed metadata population, unchanged member joins,
V3-only scope and the explicit static-only proof level. Review digest:
`4cb18036f88feaa91e14479dbbefef8222b882fe0e28be62938b75bbb2b1e41e`.
The reviewer checked the pinned native index; the parent separately recomputed
the archive digest. This is not represented as two independent archive rehashes.
All 356 new annotations were also compared directly against the retained index.

Private analysis: `ansi-live-01/unjoined-descriptor-analysis.json`. This records
the static module-chain investigation and its limits; it does not replace the
raw trace, native index or separately reviewed file/epoch provenance.
