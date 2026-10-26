# Opcode 0x18 DeactivateSupply: obj+0x04 is a 0x07 registry key (build 59638)

Session 2026-10-26 (Claude Fable 5.1). Data-only cross-reference; no new
executable analysis.

## Objective

Determine whether the u32 at obj+0x04 of opcode 0x18 (layout in
research/FIXED-OPCODES-02-13-18.md; values 0xC0000xxx, not the player id)
belongs to the entity reference space used by opcode 0x07 GiveOrderStandard.

## Background

ENTITY-CONTEXT.md: a 0x07 wire reference is a 20-byte entry = u32 registry key
+ 16-byte validation GUID (b2e070). 0x18 carries a bare u32 with no GUID.

## Observation (samples, build 59638)

| Sample | 0x18 rows | distinct keys | found as 0x07 registry key | issuer slot == only ordering slot | rows before key's first 0x07 mention | chance all match |
|---|---:|---:|---:|---:|---:|---:|
| Sample1 | 19 | 7 | 7/7 | 19/19 | 8 | 2.7e-10 |
| Sample3 | 25 | 11 | 11/11 | 23/25 | 12 | 1.0e-17 |

Sample2 (other build) has no 0x18 blocks. The two Sample3 slot disagreements are
keys ordered by more than one slot, matching the "actor references under
multiple slots" observation already in NEXT-STEPS item 1.

Chance baseline = (|0x07 keys| / key-span)^(distinct 0x18 keys), i.e. the
probability that random keys from the observed range all land on 0x07 keys.

## Interpretation

0x18 obj+0x04 is a registry key in the same space as 0x07 actor references.
The issuing slot is the slot that orders that entity (42/44 rows). 0x18 rows
can precede the entity's first 0x07 order (20/44), so the key is not derived
from orders; both reference a shared registry.

## Confidence

- Same key space as 0x07 references: STRONGLY SUPPORTED (18/18 distinct keys
  across two independent matches, chance <= 1e-9; no executable consumer traced).
- "DeactivateSupply targets the player's own unit": TENTATIVE (slot agreement
  plus RTTI class name only).
- obj+0x08 in {0,1,2} and obj+0x0c in {0,1}: UNRESOLVED.

## Reproduce

    python3 -B research/op18_reference_keys.py \
        '~/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample*'

Expected: matched == distinct keys for Sample1 (7) and Sample3 (11); exit 0.
Exit 1 if any 0x18 key is missing from the 0x07 key set.

## Next

Entity-resolution layer (wgrd_entities) could attach the 0x07 GUID / public
descriptor already resolved for that key to 0x18 events, giving "supply
deactivated on <unit type>" with the existing provenance caveats.
