# Opcode 0x18 DeactivateSupply targets: unique 0x07 references, all supply unit types

Session 2026-10-26 (Claude Fable 5.1). Extends research/OP18-REFERENCE-KEYS.md.

## Objective

Decide whether 0x18 events can be attributed to a specific entity reference
(and through the existing catalog to a GUID and static unit type) without
guessing, and test the DeactivateSupply class name against independent data.

## Resolution rule

Per replay: a 0x18 registry key (obj+0x04) is attributed to a 0x07 wire
reference only if (a) exactly one `entity_references` catalog entry carries
that key (`lookup_key_ambiguous` False), and (b) the 0x18 issuing player slot is
in that entry's `observed_player_slots`. The 0x18 frame's position relative to
the entry's first/last 0x07 order is recorded (before_first / inside /
after_last) but is not a gate: 20/44 events precede the entity's first order
and 10 follow its last, which is compatible with a registry key assigned at
spawn and valid until removal. Unit names are attached only via the existing
`configured_unit_types` with status `unique`; otherwise candidates are listed
and no name is assigned.

## Results (build 59638 samples, unit data research/unit-data/build59638-v1.json.gz)

| Sample | 0x18 events | unique key | slot ok | type unique | all candidates supply type | window before/inside/after | baseline supply share of catalog |
|---|---:|---:|---:|---:|---:|---|---:|
| Sample1 | 19 | 19 | 19 | 19 | 19 | 8 / 1 / 10 | 0.042 |
| Sample3 | 25 | 25 | 25 | 25 | 25 | 12 / 13 / 0 | 0.062 |

Resolved types: Unit_Terra_865BM_KPI (22), Unit_MAN_Kat1_6x6 (6),
Unit_M35_Cargo (4), Unit_ZIL_130_NK (3), Unit_Ural_4320 (3), Unit_T815_Kolos
(2), Unit_Star_266 (2), Unit_MI_4_CZ_LOG (1), Unit_MD_Jupiter_cargo (1). Every
one is a supply truck or logistics helicopter in the static data. With a
baseline of 4-6% supply candidates in each catalog, 44/44 by chance is below
1e-40 even treating the 18 distinct keys as the trials (0.06^18 ~ 1e-22).

## Interpretation

Structural (CONFIRMED): 0x18 carries a registry key that uniquely identifies
one 0x07 wire reference in each sample, issued by a slot that also orders it.

Semantic (STRONGLY SUPPORTED): the referenced entity is a supply unit, so the
RTTI name TNetworkActionDeactivateSupply is corroborated by two independent
sources (class name in the executable; static NDF unit types joined through the
validation GUID). Whether obj+0x08 {0,1,2} selects a supply category and
obj+0x0c {0,1} is an on/off flag remains UNRESOLVED; "deactivate" direction is
not demonstrated for either value.

Not shown: that the key refers to a single physical vehicle rather than a group
(PUBLIC-UNIT-MAPPING caveats apply), or that the action succeeded.

## Reproduce

    python3 -B research/op18_supply_targets.py \
        '~/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample*'

Expected: Sample1 19/19/19/19/19, Sample3 25/25/25/25/25, exit 0. Exit 1 on any
key that is not unique, any slot mismatch, or any non-supply candidate.

## Limitations

- Supply classification is a debug-name token list (see script); it is an
  evaluation aid, not decoder logic.
- Key uniqueness is per replay; no cross-replay identity.
- No consumer of the 0x18 object was traced.
