# Decode and inspect a replay

[Overview](../README.md) · [Documentation map](README.md) · [Format reference](../FORMAT.md)

Run these commands from the repository root with Python 3. Substitute real paths;
the examples do not download sample bytes. Use a fresh private output filename:
shell redirection overwrites an existing destination before Python starts.

## Start with the summary

```sh
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --summary
```

The summary retains header, metadata, statistics and unknown chunks, omitting the
command list. SHA-224 is verified by default. A matching digest establishes
internal integrity, not authenticity or a trusted source. File hashes in
[the sample manifest](../samples/manifest.json) pin research input identity and
provenance; they do not independently prove the recording genuine.

## Export requests in recorded order

```sh
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline > /path/to/private-timeline.json
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline --unit-data research/unit-data/build59638-v1.json.gz > /path/to/private-enriched-timeline.json
```

Timeline output follows schema `wgrd_timeline/1`. Events retain source offsets,
raw bytes and interpretation status. Enrichment adds static unit-type evidence;
it does not identify a live unit, prove ownership, or establish execution success.
Build-59638 unit data is not matching data for revision 131544.

Ordering is by replay frame, recorded pact slot order and serialized command
order. Frames are not seconds; slots are not established player identities.
The [architecture](ARCHITECTURE.md) defines the status vocabularies, while
[FORMAT.md](../FORMAT.md) describes fields and offsets.

### Inspect one event without mistaking it for an outcome

This projection selects fields from Sample1's marker request (frame 131, slot 2);
it is not a complete event object. Reproduce it with the Python API below, then
select that frame and slot from `timeline["events"]`. Sample identity and hash:
[original sample manifest](../samples/manifest.json); regression:
`tests/test_wgrd_replay.py`.

```json
{
  "frame": 131,
  "player_slot": 2,
  "opcode": 8,
  "decode_status": "layout",
  "layout_status": "matching_build",
  "interpretation": {
    "action": "create_map_marker",
    "status": "verified",
    "execution_outcome": "unknown"
  }
}
```

The layout is decoded and the marker-request interpretation is supported. No
marker ID or successful creation follows from that status. For other builds,
this supported interpretation becomes `inferred`.

### Command-line options

| Option | Effect |
|---|---|
| `--summary` | Omit `commands`, or `events` with `--timeline`; parsing still runs |
| `--include-empty` | Retain empty pact records in parser output; they add no timeline events |
| `--timeline` | Build the ordered interpretation layer; malformed command blocks fail export |
| `--unit-data INDEX_OR_ROOT` | Enrich a timeline using a versioned index file or pinned public-data directory; requires `--timeline` |
| `--no-verify-digest` | Permit a digest mismatch while retaining `header.digest_valid`; all other structural checks still apply |

Without `--timeline`, the parser retains unresolved or malformed command-block
diagnostics in its result. Exit 0 alone therefore does not establish that every
command decoded. Inspect each block's `command_decode.status` or use the full
corpus inventory for a compatibility verdict.

## Use the Python API

This example assumes `match.wargamerpl2` is in the current directory:

```python
import json
from pathlib import Path

from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import load_unit_data

parsed = parse_replay(Path("match.wargamerpl2").read_bytes())
unit_data = load_unit_data("research/unit-data/build59638-v1.json.gz")
timeline = build_timeline(parsed, unit_data=unit_data)
print(json.dumps(timeline, ensure_ascii=False, allow_nan=False))
```

| Function | Input and return | Important boundary |
|---|---|---|
| `parse_header(b)` | Bytes → `(header, metadata)` | Header and metadata only; no digest verification or frame walk |
| `parse_replay(b, include_empty=False, verify_digest=True)` | Bytes → parser result dictionary | Reads the complete file in memory; block decode problems can be returned as diagnostics |
| `decode_command_block(block, count, slot)` | Block bytes and declared count/slot → split result dictionary | Check `status`, `commands`, `consumed_bytes`, and `remaining_hex` |
| `build_timeline(parsed, unit_data=None)` | Parser result → timeline dictionary | Rejects malformed known command layouts; retains unresolved boundaries explicitly |
| `load_unit_data(path)` | Index-file or pinned-directory path → unit data dictionary | Offline; does not fetch or update a dataset |

These describe current entry points, not a new versioning or API-stability promise.
Catch `ReplayFormatError` from `wgrd_replay` for recognized format failures and
`OSError` around your own file access. Non-object metadata roots and present
non-object `game` values raise `ReplayFormatError`; missing `game` or `Version`
remains accepted.

Timeline export replaces non-finite numbers recursively with explicit markers
such as `{"nonfinite": "NaN"}`. Parser dictionaries can contain raw non-finite
floats and the default parser CLI permits non-standard JSON number tokens.
`json.dumps(parsed, allow_nan=False)` detects them but does not normalize them.
Corpus inventory rejects non-finite metadata. These are distinct output contracts.

## Check a collection

```sh
python3 -B wgrd_corpus.py /path/to/replays > /path/to/private-inventory.json
python3 -B wgrd_corpus.py /path/to/replays --expect /path/to/private-inventory.json
python3 -B wgrd_corpus.py /path/to/replays --headers-only
```

Directories are recursive, matching replay extensions case-insensitively without
following symlinked directories. Explicit files are also accepted. Resolved paths
are deduplicated; byte-identical copies at different paths remain separate rows.
The baseline comparison is whole-report equality, including absolute paths and
mode. Recreate or compare baselines intentionally when relocating inputs.

Full inventory checks structural compatibility and timeline export. Header-only
mode reads the entire file for hashes, but skips the frame/command stream:
`not_checked` and exit 0 are not command validation. Reports contain player
metadata and source paths; do not publish them without review.

## Diagnose failures

| Observation | Meaning and next step |
|---|---|
| Decoder exit 2 with `ReplayFormatError` | Recognized format or timeline failure; inspect the message and preserve the original input |
| Decoder usage error, exit 2 | Check `--help`; `--unit-data` requires `--timeline` |
| Missing-file traceback | Decoder file access is outside its format-error handler; check the path and permissions |
| Non-object metadata root or `game` value | Recognized format error; CLI exits 2 without a traceback |
| SHA-224 mismatch | Input integrity check failed; investigate provenance before using the diagnostic override |
| Corpus exit 1 | A file is unsupported/failed, or the baseline differs; inspect JSON rows and stderr |
| Corpus exit 2 | Invalid invocation, empty directory walk, unreadable directory, or invalid/unreadable baseline |
| Parser block `framed` | Boundary known; at least one serializer body remains opaque at the parser layer |

For a bug report, include the command, interpreter version, exception or status,
replay version and SHA-256, and a shareable synthetic reproducer if possible.
Exclude player metadata, replay bytes, game assets and credentials from public issues.
