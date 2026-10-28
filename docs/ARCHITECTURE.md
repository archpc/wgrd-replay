# Architecture

Canonical overview of the decoder pipeline. Byte-level format: `FORMAT.md`.
Current findings and priorities: `NEXT-STEPS.md` and `research/INDEX.md`.

## Status vocabularies

Three separate questions, three separate vocabularies. They are not interchangeable and should not be mapped onto one another.

| Question | Vocabulary | Meaning | Defined in |
|---|---|---|---|
| Did the decoder consume the bytes exactly? | `complete`, `framed`, `unresolved`, `malformed`; per command `layout` or `opaque` | Structure only. Proves boundaries and consumption, not meaning. | Block status table, section 1 |
| How sure is a byte-level or executable claim? | FORMAT.md: `VERIFIED`, `INFERRED`, `UNKNOWN`. REA-NOTES-59638.md: `CONFIRMED`, `STRONGLY SUPPORTED`, `TENTATIVE`, `UNRESOLVED`. | Evidence confidence for a specific claim. The two scales are separate and are not mapped one-to-one. | FORMAT.md legend; AGENTS.md section 7 |
| What does an event mean? | `verified`, `partial`, `inferred`, `unknown` | Semantic interpretation per event. `verified` and `partial` apply only when `game_version` is 59638. | Interpretation status, below |

`complete` means the bytes add up. It says nothing about what they mean, and for most opcodes the meanings are still `UNKNOWN`. AGENTS.md section 4 describes the same three questions in prose.

## 1. Container and command split (`wgrd_replay.py`)

```
bytes
 -> parse_header(b)            ESAV magic, container v1, declared size, SHA-224 at 0x0C..0x28 over b[0x28:], "rply" at 0x28
 -> iter_chunks(b, payload)    16-byte chunk headers; tags star / pact / endt; unknown -> unknown_chunks
 -> frames / pacts             star opens a frame (index must equal the running count); pact = one slot's command block; endt closes
 -> decode_command_block(block, count, slot)
      -> _decode_command(cursor, slot)   per-opcode creator-backed layout
 -> parse_replay(b)            JSON-ready dict: header, metadata, stats, commands, unknown_chunks
```

- `iter_chunks` raises `ReplayFormatError` on any violation.
- `parse_header` raises `ReplayFormatError` on any violation it checks, with one known gap: a metadata JSON whose root, or whose `game` value, is not an object raises `AttributeError` instead (reproduced 2026-10-28; not fixed).
- `_decode_command` returns `None` for opcodes without a layout; the block is then `unresolved`.
- Layouts are keyed by opcode: 0x07, 0x04/0x09/0x0A, 0x08 (`decode_op08`), 0x17, 0x0D, 0x0C, 0x0E, 0x02, 0x13, 0x18.
  Field names follow `obj_XX_u32|hex|u8|array|points` (XX = creator object offset in hex).
- Other opcodes are present in `OPCODE_CLASSES` (class name by RTTI) but have no field layout in this file.
- Command boundaries are exact; a block must consume its declared count and all bytes.

### Block status (`decode_command_block`)

| status       | meaning                                                                          |
|--------------|----------------------------------------------------------------------------------|
| `complete`   | all declared commands decoded with known layouts, exact byte consumption         |
| `framed`     | boundaries known, but at least one command is opaque (0x0D serializer body)     |
| `unresolved` | an opcode without a layout stopped the split; remaining bytes kept as hex        |
| `malformed`  | count out of range, creator bound violated, or trailing bytes                    |

`field_decode_status` per command is `layout` or `opaque`. `opaque` means the length-delimited body is framed, not decoded.

## 2. Timeline and interpretation (`wgrd_timeline.py`)

```
parse_replay output
 -> build_timeline(parsed, unit_data=None)
      - malformed block            -> ReplayFormatError (timeline export fails)
      - one event per command      -> command_order, frame, player_slot, source offsets
      - unknown tails              -> single known-boundary event, or unresolved_spans
      - _interpretation(opcode)    -> per-event interpretation
      - build_reference_catalog()  -> entity_references (wgrd_entities.py)
      - enrich_production_types()  -> production_types   (only with unit_data)
      - enrich_references()        -> catalog joined to unit data (only with unit_data)
      - attribute_supply_requests()-> 0x18 events linked to 0x07 references
 -> timeline JSON (schema wgrd_timeline/1)
```

- Unit data is opt-in: `--unit-data PATH` (with `--timeline`). `load_unit_data` in `wgrd_unit_data.py`
  dispatches to `wgrd_unit_index.load_index` for the build 59638 index file, or to the pinned public 58710 directory.
- `enrich_references` lives in `wgrd_unit_data.py` and is also called from `wgrd_production.py`.

### Interpretation status

Values produced by the code: `verified`, `partial`, `inferred`, `unknown`.
`verified` / `partial` apply only when the replay's `game_version` is `59638`; otherwise `inferred`.
Some layers add an `execution_outcome` (`unknown` throughout); this is not evidence of success in the running game.

The `opaque` label is a per-command `field_decode_status` (0x0D), not an interpretation status.
The earlier vocabulary (`verified/partial/opaque/unknown/inferred`) is kept here as the list of terms used across notes.

| opcode | layout location                 | interpretation location                          |
|--------|---------------------------------|--------------------------------------------------|
| 0x07   | `wgrd_replay._decode_command`   | `wgrd_orders.decode_standard_order`              |
| 0x08   | `wgrd_replay.decode_op08`       | inline in `wgrd_timeline._interpretation`        |
| 0x09   | `wgrd_replay._decode_command`   | inline in `wgrd_timeline._interpretation`        |
| 0x0A   | `wgrd_replay._decode_command`   | `wgrd_production.decode_production_action`       |
| 0x0C   | `wgrd_replay._decode_command`   | `wgrd_production.decode_change_production`       |
| 0x0D   | `wgrd_replay._decode_command` (opaque body) | `wgrd_production.decode_production_action` |
| 0x18   | `wgrd_replay._decode_command`   | `wgrd_entities.attribute_supply_requests` (post-pass) |
| 0x02, 0x04, 0x13, 0x17, 0x0E | `wgrd_replay._decode_command` | none (layout only; `unknown`) |

Field-level meanings and their confidence are in the per-opcode notes (section 4), not here.

## 3. Entities and unit data

- `wgrd_entities.reference_components(reference_hex)` splits 0x07 wire references.
- `build_reference_catalog(events, replay_sha256, matched)` keys entries as `sha256:reference_hex`
  and sets `lookup_key_ambiguous` when a 32-bit lookup key is shared.
- `attribute_supply_requests` resolves a 0x18 `obj_04_u32` only when exactly one catalog entry carries the key
  and the issuing slot is among its observed slots. Otherwise `resolution` is `unreferenced_key`, `ambiguous_key`,
  or `slot_mismatch`, and no reference or unit type is assigned.
- `wgrd_unit_data.py` / `wgrd_unit_index.py` join the static build 59638 NDF descriptor index through the validation GUID.
  Source: `research/unit-data/build59638-v1.json.gz` with `research/unit-data/build59638-v1.manifest.json`. The public 58710 snapshot is opt-in and not cached in this repo.

## 4. Generated files and their scripts

| output                                   | produced by                               |
|------------------------------------------|-------------------------------------------|
| `research/coverage.json`                 | `python3 -B research/coverage.py > research/coverage.json` |
| `research/timeline-coverage.json`        | `python3 -B research/timeline_coverage.py` (stdout) |
| `research/op07-coverage.json`            | `research/op07_coverage.py` (stdout)       |
| `research/production-coverage.json`      | `research/production_coverage.py` (stdout) |
| `research/entity-coverage.json`          | `research/entity_coverage.py` (stdout)     |
| `research/public-unit-coverage.json`     | `research/public_unit_coverage.py <dir>` (stdout) |
| `research/unit-data/build59638-v1.json.gz` | `research/export_unit_index59638.py` (see its header; inputs come from the git-ignored `work/` NDF extraction) |

Regenerate, then explain the diff in the commit or note. Counts are read from these files, not from docs.
Sample inputs are read from `samples/manifest.json` (external bytes, not in Git).

## 5. Canonical documents

| topic                              | canonical file                                  |
|------------------------------------|-------------------------------------------------|
| byte-level container and layouts   | `FORMAT.md`                                     |
| per-opcode command layouts         | `research/COMMAND-LAYOUTS.md` + per-opcode notes (`research/FIXED-OPCODES-02-13-18.md`, `research/CHANGEPRODUCTION-0C.md`, `research/OP07-ORDERS.md`, `research/PRODUCTION-COMMANDS.md`) |
| timeline semantics and status      | `research/TIMELINE-SEMANTICS.md`                |
| entities and reference keys        | `research/ENTITY-CONTEXT.md`, `research/OP18-REFERENCE-KEYS.md`, `research/OP18-SUPPLY-TARGETS.md` |
| executable analysis (addresses)    | `REA-NOTES-59638.md`                            |
| research provenance                | `research/INDEX.md`                             |
| current-build experiment and Phase 2 | `research/current-build/2026-10-28-controlled-experiment.md`, `research/current-build/PHASE-2-HANDOFF.md` |
| priorities                         | `NEXT-STEPS.md`                                 |
| usage                              | `README.md`                                     |

If two documents disagree, the one listed above for the topic wins; record the disagreement rather than silently editing either.
