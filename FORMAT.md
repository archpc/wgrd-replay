# Replay format reference

[Overview](README.md) · [Architecture & evidence conventions](docs/ARCHITECTURE.md) · [Research provenance](research/INDEX.md)

Wire layouts implemented by `wgrd_replay.py`, with the timeline export described
separately below. Executable-backed layouts concern **WarGame3.exe build 59638**,
SHA-256 `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`.
Other replay builds use those layouts by inference.

The original observations use the hash-pinned KoppelTAR Sample1/2/3 recordings
(builds 59638 / 510117427 / 59638) in [the sample manifest](samples/manifest.json).
Later cross-build observations are recorded in [the controlled experiment](research/current-build/2026-10-28-controlled-experiment.md)
and [its manifest](samples/cross-build-manifest.json). Structural fit does not
verify another executable's behavior.

**Read in order:** [header](#1-file-header-big-endian) → [chunks](#2-chunk-stream) →
[frames](#3-frames) → [pact](#4-pact-payload-little-endian) →
[commands](#6-implemented-command-splitting-decoder-04).
For a worked field layout, see [opcode 0x08](#5-opcode-0x08-map-marker-request).
For exported events, see [timeline](#8-optional-timeline-export).

## Notation

| Notation | Meaning |
|---|---|
| `0x28` | Hexadecimal byte offset or value; sizes are decimal bytes unless stated |
| Absolute offset | From file byte zero |
| `+0x04` | Relative to the structure named above the table |
| `u16`, `u32`, `f32` | Unsigned 16-bit, unsigned 32-bit, IEEE-754 binary32 |
| BE / LE | Big-endian / little-endian; raw byte strings have no implied integer order |
| `raw16`, `T bytes` | Exactly 16 bytes, or exactly the declared `T` bytes; no implied padding |
| Counted array | `u32 LE` element count, followed by that many elements of the stated width |
| `obj+0x18` / `obj_18_u32` | Creator object destination / exported key; **not** a wire offset |

Confidence labels follow [the authoritative evidence conventions](docs/ARCHITECTURE.md#evidence-conventions).
Tables distinguish **layout**, **observation**, and **interpretation** rather than
assign one confidence label to an entire structure. Parser requirements below
describe this decoder's acceptance policy, which can be stricter than the game.

## 1. File header (big-endian)

Absolute offsets. All words here are BE; command payloads switch to LE.

| Offset | Bytes | Wire field | Observation / parser behavior |
|---|---:|---|---|
| `0x00` | 4 | Magic `ESAV` | Require `45534156` |
| `0x04` | 4 | `u32` container version | Observed 1; parser requires 1; the 59638 executable accepts values ≤ 1 |
| `0x08` | 4 | `u32` declared file size | Parser requires equality with actual size; no equivalent equality check found in the executable |
| `0x0C` | 28 | SHA-224 digest | Covers bytes `[0x28, EOF)`; checked by `parse_replay` after the structural walk, unless disabled |
| `0x28` | 16 | First chunk header, tag `rply` | Same chunk layout as section 2; both reserved words must be zero in the parser |
| `0x38` | `N` | UTF-8 JSON metadata | `N` is the `rply` payload length; next chunk starts at `0x38 + N` |

Metadata is a **nested object**: `game` holds fields such as `Version`, `Map`,
`Seed`, `InitMoney`, `TimeLimit`, `ScoreLimit` and `VictoryCond`; `player_<id>`
objects hold fields such as `PlayerName`, `PlayerDeckContent` and
`PlayerAlliance`. Sample values are commonly strings. Configured `TimeLimit` is
not observed match duration. The first post-metadata chunk starts at `0x9A4`,
`0x96B` and `0x2826` in Sample1, Sample2 and Sample3 respectively.

> **Metadata validation:** the JSON root and any present `game` value must be
> objects; otherwise `parse_header` raises `ReplayFormatError`. Missing `game`
> or `Version` remains accepted, with `game_version` set to null. The parser
> still accepts Python's non-standard NaN/Infinity tokens; that is not a format
> guarantee.

**2026-10-28 correction:** explicit object checks replace the former
`AttributeError` leak. Regression coverage: `tests/test_header_metadata.py`.

`parse_header` validates only the header and metadata. It does not verify the
digest or walk the remaining chunks. See [usage and error boundaries](docs/USAGE.md).

Evidence: [REA findings and parser comparison](REA-NOTES-59638.md), including
`FUN_010b9300`, `FUN_010b9790` and SHA-224 initialization at `FUN_016fd070`;
[container provenance](research/INDEX.md#1-esav-container-and-integrity-validation).

## 2. Chunk stream

Offsets relative to each chunk header. Chunks are contiguous, with no padding.

| Relative offset | Bytes | Wire field | Parser behavior |
|---|---:|---|---|
| `+0x00` | 4 | Tag bytes | Dispatch `star`, `pact`, `endt`; retain other tags and payloads in `unknown_chunks` |
| `+0x04` | 4 | `u32 BE` field A | Require zero; meaning unresolved |
| `+0x08` | 4 | `u32 BE` payload length `L` | Require payload to fit within remaining file bytes |
| `+0x0C` | 4 | `u32 BE` field B | Require zero |
| `+0x10` | `L` | Payload | LE fields where decoded; next header is at current offset + 16 + `L` |

The executable reader `FUN_010b9500` passes field A to its visitor and discards
field B; requiring zero is decoder policy. The executable also handles `cmpg`,
which has not been observed in the original samples and is retained as unknown
by this parser. The chunk walk must finish exactly at EOF.

### Hex example: a chunk boundary

Sample2, absolute offset `0x96B`:

```text
73 74 61 72  00 00 00 00  00 00 00 08  00 00 00 00
```

| Byte group | Read as | Value |
|---|---|---|
| `73 74 61 72` | Raw tag | `star` |
| `00 00 00 00` | BE field A | 0 |
| `00 00 00 08` | BE payload length | 8 |
| `00 00 00 00` | BE field B | 0 |

The next header is at `0x96B + 0x10 + 8 = 0x983`. Evidence:
[REA framing analysis](REA-NOTES-59638.md), records `ev_fbeb6905…` and
`ev_0d8a7293…`; regression: `tests/test_wgrd_replay.py`.

## 3. Frames

One frame is `star`, followed by the ordered slot `pact` chunks, then `endt`.
Unknown chunks are retained without being treated as commands.

| Tag | Parser requirement | Original sample observation |
|---|---|---|
| `star` | At least 8 payload bytes; first `u32 LE` equals the next frame index; no already-open frame | L=8 in Samples1–2; Sample3 also has L=34/60; extra content unresolved |
| `pact` | Inside an open frame; matching frame index; slots begin at 0 and appear consecutively | Slots per frame match `game.NbMaxPlayer` in the original samples; parser does not enforce that metadata equality |
| `endt` | At least 4 payload bytes; first `u32 LE` equals the open frame index | L=12 with eight trailing zero bytes; parser does not require this exact length or zero tail |

Frame indices start at zero with no gaps. The number of slots must stay constant
across frames, and EOF cannot leave a frame open. `star` and `endt` trailing bytes
are not exposed in the parser result; the original file remains their source.

**Frame duration is unresolved.** Recorded frame order is not wall-clock time,
and the controlled experiment distinguishes replay and battle clocks. See
[timing evidence](research/current-build/2026-10-28-controlled-experiment.md#7-time-bases-and-playback).

## 4. `pact` payload (little-endian)

Offsets relative to the payload, after its 16-byte chunk header.

| Relative offset | Bytes | Wire field | Parser requirement |
|---|---:|---|---|
| `+0x00` | 4 | `u32` frame index | Match the enclosing `star` |
| `+0x04` | 4 | `u32` slot | Equal the number of slots already encountered in this frame |
| `+0x08` | 4 | `u32` command count | Zero exactly when the block length is zero |
| `+0x0C` | 2 | `u16` block length `B` | `14 + B` equals the payload length |
| `+0x0E` | `B` | Command block | Decode the declared command count; retain original `block_hex` |

Commands are concatenated. Each starts with an opcode byte, but there is **no
universal per-command length prefix**. Creator-backed reads establish boundaries;
the decoder never scans forward for a plausible opcode.

For a chunk header at file offset `C` and a command at block offset `K`:

```text
command file offset = C + 16 + 14 + K
```

An empty pact has a 14-byte payload, count 0 and length 0. Empty records contribute
to statistics but are omitted from parser `commands` unless `--include-empty` is
set. See [count-loop evidence](research/count-loop.md) and
[command-layout recovery](research/COMMAND-LAYOUTS.md).

## 5. Opcode 0x08: map marker request

Class `TNetworkActionLaunchFumigene`; creator `FUN_00b2fbc0`, selected by dispatcher
`FUN_00b24050`, jump table `0xB241F4` in build 59638. RTTI names identify classes;
consumer traces establish the marker interpretation. This is not smoke-weapon
execution evidence.

Offsets relative to the **command's opcode byte**, not the creator object.

| Wire offset | Bytes | Read → object destination | Exported field | Meaning / limit |
|---|---:|---|---|---|
| `+0x00` | 1 | Opcode | `opcode` | `0x08` |
| `+0x01` | 4 | `u32 LE` → `obj+0x04` | `player_handle` | Observed `0xC000001E + slot`; equality reported, not enforced |
| `+0x05` | 16 | Raw → `obj+0x08` | `unknown16_hex` | Observed 12 zero bytes then `32000000`; retained without guessed semantics |
| `+0x15` | 12 | `3 × f32 LE` → `obj+0x18` | `position_f32` | Transmitted marker position argument; axes and units unresolved |
| `+0x21` | 4 | `u32 LE` → `obj+0x24` | `type_u32` | Values 0–3 observed; type 3 with nonempty text displays a label; 0/1/2 meanings unresolved |
| `+0x25` | 2 | String helper reads `u16 LE T` | `text_length` | Byte count, not character count |
| `+0x27` | `T` | Narrow string bytes | `text`, or `text_hex` with error flag | UTF-8 presentation attempted; original command bytes retained |

Total size is `39 + T` bytes, with no terminator or padding. `decode_op08` returns
`None` if the supplied bytes do not fit exactly. The block decoder converts a
failed supported layout into a `malformed` diagnostic.

Worked sample: Sample1 frame 131, slot 2, command at `0x69A7`. First five bytes
`08 20 00 00 c0` encode opcode `0x08` and LE handle `0xC0000020`; string length
bytes `15 00` encode 21 bytes, `leave your cv at base`.
See `tests/test_wgrd_replay.py` and [marker consumer evidence](research/TIMELINE-SEMANTICS.md#08--create-graphical-map-marker).

**2026-10-28 correction:** the former “map flare (INFERRED)” description predates
consumer analysis. The current matching-build timeline classifies a marker
creation request as `verified`; actual creation and position are not observed.

## 6. Implemented command splitting (decoder 0.4)

All sizes include the opcode. Fields after it are LE unless raw. Object-offset
names describe storage, not gameplay roles. The class-name table `OPCODE_CLASSES`
is larger than the set of implemented layouts.

| Opcode | Total bytes | Reads after opcode |
|---|---|---|
| `0x02` | 22 | `u32`, `raw16`, `u8` |
| `0x04`, `0x09` | 25 | `u32`, `raw16`, `u32` |
| `0x07` | `71 + 20×(N1+N2) + T` | Two counted raw20 arrays; `raw12`, `raw8`, `raw36`, `u32 ≤ 3`; `u16 T`, `T` bytes |
| `0x08` | `39 + T` | Section 5 |
| `0x0A` | 29 | `u32`, `raw16`, `u32 ≤ 14`, `u32` |
| `0x0C` | `61 + 4×(n1+n2+n3) + 16×(m1+m2)` | See the ordered sequence below |
| `0x0D` | `18 + L` | `u32` variant 1–3; `raw4`, `raw1`, `raw4`; `u32 L`, opaque `L` bytes |
| `0x0E` | 25 | `u32`, `u32`, `raw16` |
| `0x13` | 13 | Three `u32` values |
| `0x17` | `10 + 8×N` | `u32`, `u32 N`, `N × raw8`, `raw1` |
| `0x18` | 10 | `u32`, `u32`, `u8` |

For `0x0C`, read in order: `u32`, `raw16`; counted `u32` arrays `n1`, `n2`
(elements of `n2` ≤ `0x0E`); two counted point arrays `m1`, `m2` (each point is
`raw12` + `u32 ≤ 6`); counted `u32` array `n3`; `u32`, `raw16`.
Its field meanings remain open; [the creator note](research/CHANGEPRODUCTION-0C.md)
records the enum and float hypotheses separately from the proven reads.

Creator addresses, evidence records, authentic sample identities and reproduction:
[layout recovery](research/COMMAND-LAYOUTS.md), [fixed opcodes](research/FIXED-OPCODES-02-13-18.md),
[0x07 orders](research/OP07-ORDERS.md) and [0x0C](research/CHANGEPRODUCTION-0C.md).
Current per-sample counts: [generated structural coverage](research/coverage.json).

### Block result and failure boundaries

Each pact's `command_decode` contains `commands`, `consumed_bytes`,
`remaining_hex`, `layout_build`, `status` and an optional `reason`.

| `status` | Meaning | Counts as fully split / fully decoded |
|---|---|---|
| `complete` | All declared commands have supported field layouts; exact EOF | Yes / yes |
| `framed` | All boundaries known; at least one `0x0D` body opaque in the parser | Yes / no |
| `unresolved` | Unsupported opcode stops decoding; verified prefix retained | No / no |
| `malformed` | Read/count/enum constraint or exact-EOF violation | No / no |

A command stores `offset` (block-relative), `length`, `raw_hex`, `fields` and
`field_decode_status` (`layout` or `opaque`). On a failed read, consumption rolls
back to the start of that command; its entire span stays in `remaining_hex`.
Exact EOF is decoder policy, not a promise of executable parity.

`parse_replay` retains block diagnostics instead of raising for every malformed
block. Container/frame errors do raise. **Exit 0 is not complete command coverage.**

## 7. Inputs vs. outcomes

The stream resembles lockstep input recording: one packet per slot per frame,
mostly empty. No kill/hit/score/position-snapshot records have been identified in
the original sample corpus. That is a bounded observation, not proof that the
format cannot contain them. RTTI entries such as `TNetworkActionKill` do not
establish a decoded outcome feature.

The [controlled experiment](research/current-build/2026-10-28-controlled-experiment.md)
adds sample-specific UI and playback evidence. It does not supply a universal
simulation model or establish all field meanings.

## 8. Optional timeline export

```sh
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline
```

`build_timeline` produces schema `wgrd_timeline/1`. `--timeline --summary` omits
`events` but keeps statistics, metadata, catalogs and unresolved spans.
[Usage](docs/USAGE.md) covers the API, flags and JSON contracts.

| Event field | Contract |
|---|---|
| `command_order` | Zero-based global export order |
| `frame`, `frame_command_order` | Raw replay frame and order across slots within that frame |
| `player_slot`, `slot_command_order` | Recorded slot and command index within its pact; `player_identity` remains null |
| `opcode`, `class`, `class_status` | Opcode and build-59638 RTTI class where known |
| `parameters`, `raw_hex`, `decode_status` | Original parser fields, bytes and structural status |
| `layout_status` | `matching_build` or `inferred_build_59638` |
| `source` | Chunk offset, block-relative offset, absolute file offset, byte length and `boundary_known` |
| `interpretation` | Separate action, semantic parameters, evidence, status and limitations |

Known malformed parser blocks fail timeline export. Unknown single-command tails
have known boundaries; multi-command tails produce placeholders linked to one
shared `unresolved_spans` entry, without invented per-command offsets.

Parser-level `opaque` does not forbid a later interpretation. For `0x0D`,
`wgrd_production.py` separately decodes supported nested production layouts and
reports `interpretation.payload_layout_status`. An invalid interior becomes a
`malformed` payload interpretation with unknown action; the parser's framed
boundary remains valid. Evidence: [production commands](research/PRODUCTION-COMMANDS.md).

Timeline output recursively normalizes non-finite numbers to objects such as
`{"nonfinite": "+Infinity"}`; semantic positions become null where unusable.
Parser CLI output uses the same markers. Original command
bytes survive either representation. Unknown chunks are retained; undecoded
`star`/`endt` tails are not included in the exported structure.

### 8.1 Opcode07 requested order subtypes

`interpretation.parameters.order_kind_u32` comes from creator object `+0xE0`,
order-structure `+0x10`. `order_kind` names an explicit request where established;
contextual kind 39 and unnamed values remain null. `order_selection` is
`explicit_request`, `runtime_dependent` or `unknown`. `effective_order_kind`
remains null: runtime state may select a different order per actor.

The `actor_references` array comes from `obj+0x04`, `target_references` from `obj+0x60`. Each raw20 entry
contains a registry key plus validation GUID. The finite positional argument from
`obj+0xBC` is not an observed destination; all-positive-infinity is an absent
sentinel, and other non-finite values have no usable position. Stop omits the
positional interpretation. `secondary_vector_hex`, dispatch token/mode and
`order_structure_hex` retain their neutral names and raw values.

Classification, conditional fallback branches, addresses and limitations:
[0x07 orders](research/OP07-ORDERS.md), [entity context](research/ENTITY-CONTEXT.md).

### 8.2 Replay-scoped reference catalog and conditional context rules

`entity_references` keys catalog entries by full replay SHA-256 plus full20-byte
`reference_hex`, separated by `:`. The catalog covers decoded opcode-0x07 arrays.
Each entry records first/last frame and command order,
actor/target occurrences (including duplicates) and observed commanding slots.
A shared lookup key is flagged as ambiguous; shared GUIDs do not merge keys.
The GUID exposes raw trailing16 bytes, four LE words and colon text, not RFC UUID
ordering. `unit_identity` stays null.

`contextual_order_rules` describes conditional build-59638 branches, not a complete
classifier. Kind39 `contextual_resolution` leaves `fallback_reached` and effective
kind null. Static type association does not supply missing runtime flags.

The `0x18` post-pass attributes supply requests only with a unique catalog key
and compatible observed slot; it cannot establish ownership or cross-replay
identity. See [reference-key evidence](research/OP18-REFERENCE-KEYS.md) and
[supply-target evidence](research/OP18-SUPPLY-TARGETS.md).

### 8.3 Optional public descriptor snapshot

`--timeline --unit-data ROOT` loads four pinned public build-58710 files offline.
No download occurs. [Source hashes](research/public-unit-sources.json) identify
them. Matching is by exact validation GUID bytes; .NET XML GUID strings use
`UUID.bytes_le`, while runtime keys, NDF instance IDs and deck indices remain
separate namespaces.

The catalog gains `static_descriptor`, `descriptor_match_status`, and top-level
`descriptor_data` provenance. These are cross-version static associations for the
original samples, not verified matching-build capabilities or names. Descriptor records retain NDF class/instance ID/debug name, module and selector
Default references, and direct `TUniteAuSolDescriptor` card values where available.
Card flags describe the snapshot. No company GUID rewriting or runtime membership
is inferred. Events remain unchanged.
See [public descriptor mapping](research/PUBLIC-UNIT-MAPPING.md).

### 8.4 Original 59638 configured-type index and localized names

`--timeline --unit-data research/unit-data/build59638-v1.json.gz` loads the bundled
`wgrd_unit_index/1` index; plain JSON index files are also supported.

References gain `configured_unit_types` with unique/ambiguous/missing status,
evidence qualification and candidate paths. Candidates retain GUID/class, debug
name, alias, localized-name candidates and provenance. A localized name requires
exactly one dictionary record; there is no alias/debug-name fallback, and original
markup remains. Duplicate translations and inverse mappings remain candidate
arrays. Missing and ambiguous mappings stay explicit. Inverse paths retain the
unit → CompanyUnit selector Default → module → CompanyDescriptor object IDs;
direct AuSol GUID matches stay separate.

Shared `descriptor_data.nodes` retains source object IDs, expanded-NDF offsets,
projected properties and unevaluated selector conditions. Index/archive/member/
expanded/object/dictionary hashes and locale identify the source. It is a static
projection, not a live world model. Non-59638 mappings remain inferred.

With unit data, production requests also gain static type associations. Neither
reference nor production enrichment proves membership, ownership, active modules,
accepted placement or execution. See [matching-build enrichment](research/TIMELINE-59638.md),
[NDF bridge](research/NDF59638-BRIDGE.md) and [production commands](research/PRODUCTION-COMMANDS.md).
