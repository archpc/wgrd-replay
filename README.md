# wgrd-replay

**Read the replay. Keep the uncertainty.**

An offline, Python standard-library-only decoder and reverse-engineering reference
for Wargame: Red Dragon `.wargamerpl2` files. It turns the game's binary recordings
into inspectable command streams and evidence-qualified timelines, with raw bytes
and source offsets available for checking the interpretation.

[Usage](docs/USAGE.md) · [Format](FORMAT.md) · [Architecture](docs/ARCHITECTURE.md) ·
[Research archive](research/INDEX.md)

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

From the repository root, this prints each interpreted request's frame, slot,
action and confidence. It needs only a replay; unit enrichment is optional.

```python
from pathlib import Path
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline

timeline = build_timeline(parse_replay(Path("match.wargamerpl2").read_bytes()))
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
