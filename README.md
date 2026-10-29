# Wargame: Red Dragon Replay Decoder

A reverse-engineering project and Python toolkit for decoding, inspecting, and analyzing *Wargame: Red Dragon* replay files (`.wargamerpl2`).

The project documents the replay format and provides tools to extract recorded commands, reconstruct timelines, inspect entity references, and examine the underlying binary structures.

Decoded records retain their original byte offsets and raw data, allowing interpretations to be checked against the source. Confirmed structures are distinguished from incomplete or experimental findings.

The decoder runs offline, uses only Python's standard library, and does not require a game installation.

## Start here

- **Inspect a replay:** [find a replay and use the CLI or Python API](docs/USAGE.md).
- **Investigate the format:** [architecture and change guide](docs/ARCHITECTURE.md),
  [format reference](FORMAT.md), and [research index](research/INDEX.md).

## What comes out

The [Python example](docs/USAGE.md#read-one-useful-result) prints interpreted
requests as frame, recorded slot, action and status. One line from the historical
build-59638 Sample1 replay is:

```text
131 2 create_map_marker verified
```

This is one selected output line; other lines and the rest of the timeline fields
are omitted. The line itself is not redacted. The [sample manifest](samples/manifest.json)
identifies the input; replay bytes are not included in the repository.

This is a request to create a marker, not proof that a marker was created.
`verified` describes this interpretation on the matching evidence build, not an
execution outcome. Frame-to-seconds conversion and slot-to-player identity remain
unresolved. To reproduce the line, save and run the linked Python example with
that sample; you can also try it with your own replay.

## Run it

Use Python 3.13 or later from the repository root. The decoder has no third-party
runtime dependencies. CI tests Python 3.13, 3.14 and 3.15.

```sh
git clone https://github.com/archpc/wgrd-replay.git
cd wgrd-replay
python3 -B wgrd_replay.py --help
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --summary
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline > /path/to/private-timeline.json
```

Replace the replay path and use a fresh output filename: shell redirection
will overwrite an existing file. The summary reports structure and metadata;
the timeline adds ordered requests. Output can contain player names and chat.
The [usage guide](docs/USAGE.md#find-a-replay) covers finding a replay, and the
[Python examples](docs/USAGE.md#use-the-python-api) show how to use the API.
Sample replays and game executables are kept outside Git.

## How it works

```text
replay bytes → parser → ordered timeline
                ↑              ↑
       raw fields and     interpretation,
       source offsets     evidence and status
```

- [`wgrd_replay.py`](wgrd_replay.py) parses the container, frames and supported
  command layouts. It checks the SHA-224 digest by default; a matching digest
  establishes internal consistency, not authenticity. Unknown data is retained.
- [`wgrd_timeline.py`](wgrd_timeline.py) orders requests and attaches interpretations
  and evidence. It does not simulate the match.
- [`wgrd_orders.py`](wgrd_orders.py), [`wgrd_production.py`](wgrd_production.py)
  and [`wgrd_entities.py`](wgrd_entities.py) interpret specific command families.
  Static unit data can optionally enrich the timeline; it is not live unit identity.
  The build-59638 index is not matching data for revision 131544.
- [`wgrd_corpus.py`](wgrd_corpus.py) inventories replay collections and compares
  saved reports.

The [architecture](docs/ARCHITECTURE.md) maps behavior to code and tests. The
[usage guide](docs/USAGE.md) covers flags, output contracts and corpus checks.

## What we know, and what we don't

- The layouts and selected request interpretations are backed by executable
  research on build 59638. Other builds use inferred layouts and supported
  interpretations; unknown meanings stay unknown.
- One controlled recording on internal revision 131544 was decoded and played
  back. UI observations corroborated a fuel-toggle pair for that sample, not
  general execution outcomes. Steam content build 15652829 is a different
  identifier. See [the Oshkosh Incident](research/current-build/README.md) and
  its [experiment report](research/current-build/2026-10-28-controlled-experiment.md).
- Frame duration, coordinate axes and units, slot-to-player identity, effective
  contextual orders and combat outcomes remain unresolved.
- The parser frames `0x0D` bodies as opaque; the timeline separately interprets
  supported production interiors. CLI JSON represents non-finite floats explicitly;
  parser dictionaries can retain them.
- Coverage is limited to the recorded samples, not a promise that every replay
  works. Replay and binary redistribution is not assumed lawful.

`complete` means a block's declared commands and bytes were consumed. It does not
mean the game executed them. For the details, see [format](FORMAT.md),
[architecture](docs/ARCHITECTURE.md), [structural coverage](research/coverage.json)
and [timeline coverage](research/timeline-coverage.json).

## Work on it

Start with the [change guide](docs/ARCHITECTURE.md#change-guide) to find the code
and tests for your change. Routine fixes don't require reading the research archive.
[CONTRIBUTING.md](CONTRIBUTING.md) covers setup and checks; [next steps](NEXT-STEPS.md)
lists open investigations. For a new format claim, follow the
[evidence conventions](docs/ARCHITECTURE.md#evidence-conventions) and
[research index](research/INDEX.md). The usage guide explains what to include in
a [bug report](docs/USAGE.md#diagnose-failures).

The full test suite needs a hash-pinned public unit fixture. Fetch it first, then
run the tests from the repository root:

```sh
python3 -B scripts/fetch_public_fixture.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

Tests requiring absent private artifacts report skips; present altered artifacts
fail. See [CONTRIBUTING.md](CONTRIBUTING.md) for details and the remaining checks.

## Credits and field notes

The owner directed and reviewed the work. [Research credits](research/INDEX.md#project-credits)
cover contributors, tools and the ASCII cow, who is a maintainer.
[The ASCII Dragon Incident](research/DRAGON-INCIDENT.md) explains another
well-defended corner of the project.
