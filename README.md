# wgrd-replay

**Read the replay. Keep the uncertainty.**

An offline, Python standard-library-only decoder and reverse-engineering reference
for Wargame: Red Dragon `.wargamerpl2` files. It turns the game's binary recordings
into inspectable command streams and evidence-qualified timelines, with raw bytes
and source offsets available for checking the interpretation.

The interesting part is the boundary between what the bytes say and what the game
does. This project documents that boundary rather than quietly stepping over it.

[Research & evidence](research/INDEX.md) · [Binary format](FORMAT.md) ·
[Usage](docs/USAGE.md) · [Documentation map](docs/README.md)

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

Clone the repository and run from its root with Python 3. No dependency installation
or game installation is required to decode a replay you already have. Sample replay
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

## Follow the investigation

| Question | Start here |
|---|---|
| How are bytes framed and commands split? | [Binary format](FORMAT.md) → [creator traces](research/COMMAND-LAYOUTS.md) |
| Why does an opcode get an action name? | [Evidence conventions](docs/ARCHITECTURE.md#evidence-conventions) → [research index](research/INDEX.md) |
| How do parsing, timelines and unit data fit together? | [Architecture](docs/ARCHITECTURE.md) |
| What did recorded gameplay actually corroborate? | [Controlled experiment](research/current-build/2026-10-28-controlled-experiment.md) |
| What should be investigated next? | [Current priorities](NEXT-STEPS.md) and [Phase 2 handoff](research/current-build/PHASE-2-HANDOFF.md) |

The research trail includes executable addresses, hash-pinned artifacts, archived
REA responses and reproduction scripts. [REA notes](REA-NOTES-59638.md) retain the
static-analysis record; [the investigation log](REPLAY-RESEARCH.md) retains its
chronology. Historical plans describe the work as it stood then, not today's API.

## Contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, artifact
requirements, testing and preservation rules. Research contributions need a
falsifiable claim, identified builds and samples, evidence, and a reproduction
command. Exact consumption is necessary. It is not a theory of warfare.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

The full suite needs external artifacts: some tests skip when they are absent,
while older sample tests fail. Report the actual results and skip reasons.
[AGENTS.md](AGENTS.md) specifies repository operating and evidence standards.
[The ASCII Dragon Incident](research/DRAGON-INCIDENT.md) explains one unusually
well-defended contribution boundary.

## Known limitations

- Most field semantics remain unconfirmed. Contextual orders require runtime
  state, and execution outcomes remain unknown in exported interpretations.
- Opcode `0x0D` bodies are opaque in the parser. The timeline separately decodes
  supported production interiors; inspect its payload status and limitations.
- `parse_header()` can raise `AttributeError` for non-object metadata roots or
  non-object `game` values. This known defect needs a separate tested fix.
- Timeline JSON normalizes non-finite floats to explicit objects. Default parser
  JSON can still contain non-standard NaN/Infinity tokens.
- Corpus coverage is bounded. Passing the recorded samples is not universal
  replay compatibility. Replay and binary redistribution is not assumed lawful.

## Credits

- Maintainer: the ASCII cow in `wgrd_orders.py`.

AI models produced the research and code in this repository, running on [Hermes Agent](https://hermes-agent.nousresearch.com) via the Nous Portal. The repository owner directed and reviewed the work.

- Reverse engineering of build 59638 in the 2026-10-26 sessions (opcode 0x0C creator and helper readers, fixed-size creators for 0x02/0x13/0x18, the 0x18 registry-key cross-reference), assessment and roadmap, review and integration of delegated work: Claude Fable 5.1 (Anthropic), technical lead.
- Decoder implementation, regression tests, coverage regeneration and implementation docs for opcodes 0x0C, 0x02, 0x13, 0x18 and the 0x0C timeline interpretation: Claude Haiku 5.5 (Anthropic), working in isolated git worktrees under the lead's review.
- Earlier sessions (container, digest, framing, dispatcher, opcodes 04/07/08/09/0A/0D/0E/17, NDF bridge, timeline) are recorded in `REPLAY-RESEARCH.md`, `REA-NOTES-59638.md` and `research/chatgpt-session-2026-10-23/`.
- Tooling: rizin, Ghidra, REA MCP, Python 3 standard library. The Sample1 battle-report surface (`research/reports/sample1/`) was authored on OpenAI's `data-app` report runtime (Codex/ChatGPT `build-report` skill); the runtime itself is not redistributed here, only the authored content and a self-contained HTML build.

The 2026-10-26 findings (`research/CHANGEPRODUCTION-0C.md`, `research/FIXED-OPCODES-02-13-18.md`, `research/OP18-REFERENCE-KEYS.md`, `research/OP18-SUPPLY-TARGETS.md`) are each backed by a reproduction script and regression tests that exercise the claim against the artifacts named in the note. Earlier research is documented with evidence IDs and notes in `research/evidence/` and `REA-NOTES-59638.md`; not all of it has a standalone script.
