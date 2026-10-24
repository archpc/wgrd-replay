# Sample1 enriched timeline validation

Implementation f5e41cc. User-created /tmp/sample1.timeline.json read directly;
valid JSON, byte-identical to a fresh export from authenticated Sample1 and bundled
59638 index. Machine-readable evidence: unit-data/sample1-timeline-validation.json.
Large timeline remains local in /tmp; not committed.

## Reproduce

```sh
python3 -B /Users/sein/Code/wgrd-replay/wgrd_replay.py \
  /Users/sein/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample1.wargamerpl2 \
  --timeline \
  --unit-data /Users/sein/Code/wgrd-replay/research/unit-data/build59638-v1.json.gz \
  > /tmp/sample1.timeline.json
```

Exact file: 16,917,666 bytes; SHA256
c8cd1b668f889b404651be59a8dcde8d432a0e44b63a50bfe6ece79def7b51ef.
Schema wgrd_timeline/1. Source replay SHA256
c5f8eff1298cf38c1d9967d29f98a22dfc869c150405630f9f695bb80a521df8;
SHA224 valid. Build59638; map Destruction_2x3_Tohoku_Alt.

## Observed contents

| Measure | Count |
|---|---:|
| Recorded frames | 19033 |
| Recorded player slots per frame | 4 |
| Command events | 4162 |
| Multi-command blocks split | 290/290 |
| Multi-command blocks with complete layouts | 285 |
| Events with known layouts | 3887 |
| Events with opaque interiors | 233 |
| Events with unknown layouts | 42 |
| Replay-scoped references | 285 |
| Distinct configured unit types | 102 |
| References with unique configured type and localized name | 285/285 |
| Ambiguous or missing type mappings | 0 |
| Projected provenance nodes | 410 |

285 references does not mean285 observed live units. Some declarations identify
companies; static type association does not establish runtime acceptance,
membership, existence, ownership or lifetime. Catalog covers decoded opcode07
actor/target arrays, not every possible entity reference in the replay.

Localized examples present: VAB VDAA, AH-64 TD, T-72M1 WILK, KORPS MARINIERS,
JÄÄKÄRI '90. Names retained in entity_references.entries[].configured_unit_types
candidate records. Join each event actor/target reference_id to catalog reference_id;
use localized_name only with its mapping/evidence status. Source strings retain
original markup/spacing. Events carry references rather than duplicated names.

## Standard-order requests

| Requested kind | Commands |
|---|---:|
| 39 contextual, effective kind unresolved | 3318 |
| 4 Move | 153 |
| 19 Shoot | 136 |
| 14 UnloadFromTransport | 83 |
| 10 Stop | 56 |
| 27 Reverse | 34 |
| 1 Land | 7 |
| 20 SplitCompany | 4 |
| 15 MergeCompany | 3 |
| Total standard-order commands | 3794 |

Counts describe input commands, not successful actions, individual units or
outcomes. A command may address multiple actors. Contextual39 cannot be relabeled
Move/Shoot from configured type or position arguments.

## Safeguards and usability limits

All runtime unit_identity values null. Every candidate's conditions_evaluated
false. Raw selector condition ParamId11/ParamValue1 retained, not interpreted.
All3318 contextual requests keep effective kind and fallback_reached null.
Frame duration unknown; metadata TimeLimit is not measured match duration.
Player names exist in metadata but recorded-slot mapping remains unresolved.
No kills, successful attacks, actual trajectories or match outcomes established.

Raw bytes, original offsets, repeated references and provenance make this a large
audit/export file. It is not yet a compact player-facing match summary. Zero
unresolved_spans does not imply full decoding: opaque/unknown event counts above
remain explicit.

Known wording issue: legacy catalog/event limitation strings say descriptor names
are unresolved. Those generic strings predate optional configured-type enrichment.
Specific candidate records now contain verified source labels; accepted runtime
identity and company membership remain unknown. Recorded here; no output-contract
or decoder change in this notes-only commit.

Implementation validation at f5e41cc: 71 tests passed. This notes-only follow-up
rechecked the actual artifact, source/index hashes, fresh-export equality, counts
and safeguards. Full suite not repeated; no executable code changed.
