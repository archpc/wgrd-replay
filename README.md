# wgrd-replay

**Read the replay. Keep the uncertainty.**

An offline, Python standard-library-only decoder and reverse-engineering reference
for Wargame: Red Dragon `.wargamerpl2` files. It turns the game's binary recordings
into inspectable command streams and evidence-qualified timelines, with raw bytes
and source offsets available for checking the interpretation.

## See a result

After saving the [example script below](#read-one-useful-result) as `inspect_replay.py`
and setting its replay path, run it from the repository root:

```sh
python3 inspect_replay.py
```

One line from a build-59638 sample looks like this:

```text
131 2 create_map_marker verified
```

The columns are replay frame, recorded player slot, interpreted action and
confidence. This is one selected line from the script's output; other lines and
all other timeline fields are omitted. The line itself has not been redacted.
Sample identity is in the [manifest](samples/manifest.json); the replay bytes are
not included.

This records a requested action; it does not establish that the game executed it.
Frames are not seconds, and slots are not established player identities.

## Start here

- [Inspect a replay](docs/USAGE.md): find a replay, run the decoder and read its output.
- Research the format: start with the [architecture](docs/ARCHITECTURE.md),
  [evidence conventions](docs/ARCHITECTURE.md#evidence-conventions) and
  [research index](research/INDEX.md).

## What it can do

| Layer | Implemented behavior | What it establishes |
|---|---|---|
| Container | Check ESAV framing, declared size and SHA-224; retain unknown chunks | Internal consistency, not authenticity |
| Commands | Split supported layouts with exact byte consumption; retain raw blocks and unresolved tails | Boundaries and fields, not gameplay meaning |
| Timeline | Export ordered requests with source offsets, evidence and interpretation status | Recorded intent, not execution success |
| Unit data | Optionally join a bundled build-59638 index or pinned public snapshot | Static type associations, not live unit identity |
| Corpus | Inventory local replay collections and compare saved baselines | Sample-specific structural compatibility |

## What is known

| Evidence boundary | Current position |
|---|---|
| **Build 59638** | Executable-backed layouts and selected request interpretations; many field meanings remain unknown |
| **Other builds** | Layouts and supported interpretations transfer by inference; unsupported meanings remain unknown |
| **Controlled revision 131544** | Recording and completed playback, plus bounded UI corroboration of a fuel-toggle pair; no general semantic promotion |
| **Still unresolved** | Frame duration, coordinate axes/units, slot-to-player identity, effective orders and combat outcomes |

The controlled experiment used internal revision **131544** and Steam content build
**15652829**. These are different identifiers. Read [the Oshkosh Incident](research/current-build/README.md)
for the visual investigation, or [the experiment report](research/current-build/2026-10-28-controlled-experiment.md)
for hashes, observations, reproduction and limits.

> **A request is not a result.** `complete` describes byte consumption;
> `verified` qualifies a particular interpretation. Neither means the truck arrived.

Current coverage lives in [structural coverage](research/coverage.json) and
[timeline coverage](research/timeline-coverage.json). The [provenance index](research/INDEX.md)
separates the original three-sample baseline from later experiments.

## Run it

Clone the repository and run from its root with Python 3.13 or later (CI: 3.13, 3.14 and 3.15).
No dependency installation or game installation is required to decode a replay you already have. Sample replay
bytes and game executables are kept outside Git.

```sh
git clone https://github.com/archpc/wgrd-replay.git
cd wgrd-replay
python3 -B wgrd_replay.py --help
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --summary
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline > /path/to/private-timeline.json
```

Replace the paths with your replay and a fresh output filename. Output can contain
player names and chat. `--summary` reports structure and metadata; `--timeline`
adds ordered requests. Digest verification is on by default.

### Read one useful result

Save this as `inspect_replay.py` in the repository root. Replace
`/path/to/match.wargamerpl2` with the path to your replay, then run
`python3 inspect_replay.py` from the repository root. It prints each interpreted
request's frame, slot, action and confidence. Unit enrichment is optional.

```python
from pathlib import Path
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline

timeline = build_timeline(parse_replay(Path("/path/to/match.wargamerpl2").read_bytes()))
for event in timeline["events"]:
    meaning = event["interpretation"]
    if meaning["action"] is not None:
        print(event["frame"], event["player_slot"],
              meaning["action"], meaning["status"])
```

A `create_map_marker` row describes a marker request, not a unit location.
Frame numbers are not seconds; slots are not established player identities.
See [usage](docs/USAGE.md) for flags, JSON contracts, enrichment and corpus checks.

## Documentation

- [Usage](docs/USAGE.md): CLI flags, Python API, enrichment and corpus checks.
- [Format reference](FORMAT.md): byte maps, layouts, semantics and uncertainties.
- [Architecture](docs/ARCHITECTURE.md): implementation boundaries and output statuses.
- [Research archive](research/INDEX.md): evidence, investigations and reproduction.
- [Next steps](NEXT-STEPS.md): current priorities.

## Contribute

Start with the [change guide](docs/ARCHITECTURE.md#change-guide) to find the owning
module and tests, then [CONTRIBUTING.md](CONTRIBUTING.md) for setup and checks. Research contributions need a
falsifiable claim, identified builds and samples, evidence, and a reproduction
command. Exact consumption is necessary. It is not a theory of warfare.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

Fetch the hash-pinned public unit fixture first with
`python3 -B scripts/fetch_public_fixture.py`. Tests needing absent private artifacts
report skips; present altered artifacts fail. Report actual results and skip reasons.
[AGENTS.md](AGENTS.md) specifies repository operating and evidence standards.
[The ASCII Dragon Incident](research/DRAGON-INCIDENT.md) explains one unusually
well-defended contribution boundary.

## Known limitations

- Most field semantics remain unconfirmed. Contextual orders require runtime
  state, and execution outcomes remain unknown in exported interpretations.
- Opcode `0x0D` bodies are opaque in the parser. The timeline separately decodes
  supported production interiors; inspect its payload status and limitations.
- CLI JSON normalizes non-finite floats to explicit objects. Parser dictionaries
  can still contain non-finite floats.
- Corpus coverage is bounded. Passing the recorded samples is not universal
  replay compatibility. Replay and binary redistribution is not assumed lawful.

## Credits

The owner directed and reviewed the work. [Research credits](research/INDEX.md#project-credits)
retain contributor roles, tools and historical session attribution.
