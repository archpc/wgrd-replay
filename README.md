# wgrd-replay

Offline, stdlib-only decoder for Wargame: Red Dragon replay files (`.wargamerpl2`).

The decoder reads Wargame: Red Dragon replays strictly. It checks the container, verifies the SHA-224 digest by default, walks the `star` / `pact` / `endt` frame stream, and splits command blocks. Whatever it cannot place stays as raw hex. Nothing is guessed or silently skipped.

Malformed input generally raises `ReplayFormatError`. A known defect in `parse_header()` can instead propagate `AttributeError` for non-object JSON metadata. See [Known limitations](#known-limitations).

## Quick start

Run from the repository root with Python 3; no dependency installation or game
installation is needed to decode a replay you already have. Replay files are
external and are not included in this repository.

```sh
python3 -B wgrd_replay.py --help
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --summary
python3 -B wgrd_replay.py /path/to/match.wargamerpl2 --timeline > /path/to/private-timeline.json
```

Replace the example paths with your replay and a fresh output filename. Output
can contain player names and chat; keep it private. A summary reports structure;
a timeline adds evidence-qualified action requests. Neither establishes gameplay
outcomes or a frame-to-seconds conversion.

| I want to… | Read |
|---|---|
| Decode files, use the Python API, or diagnose an error | [Usage guide](docs/USAGE.md) |
| Change code or docs and run the right checks | [Contributing guide](CONTRIBUTING.md) |
| Understand the pipeline and status labels | [Architecture](docs/ARCHITECTURE.md) |
| Inspect byte layouts and their evidence | [Format reference](FORMAT.md) and [research index](research/INDEX.md) |
| Find current research priorities | [Next steps](NEXT-STEPS.md) |

## Current-build milestone (2026-10-28)

A controlled offline replay from internal revision **131544** (Steam build **15652829**) was recorded, decoded, and played back to completion. Two newly acquired historical recordings (Versions 510061340 and 510064564) also passed structural and timeline checks. This is sample-specific compatibility, not a guarantee for every current-build replay.

The investigation, including the Windows GDI capture workaround, chronology, hashes, limits, and reproduction commands, is in [the controlled experiment report](research/current-build/2026-10-28-controlled-experiment.md). Browse the [Oshkosh Incident visual archive](research/current-build/README.md), the controlled-experiment archive, for curated screenshots and the complete versioned screenshot release. Replay bytes and private session data remain outside Git. General non-59638 semantics remain inferred and execution outcomes remain unknown.

Read-only corpus inventory and regression checks:

    python3 -B wgrd_corpus.py /path/to/replays > /path/to/private-inventory.json
    python3 -B wgrd_corpus.py /path/to/replays --expect /path/to/private-inventory.json
    python3 -B wgrd_corpus.py /path/to/replays --headers-only

Reports can contain player metadata and absolute source paths. Keep them private. Exit 1 means a failed/unsupported file or baseline mismatch; exit 2 means invalid invocation or no files found. Header-only mode does not claim command compatibility.

## Original three-sample baseline (historical checkpoint)

The following counts and source limits describe the original corpus, not the expanded milestone above.

- Container, digest, and frame framing: verified on all 3 samples.
- Command splitting: 594/594 multi-command blocks split with exact count and EOF.
- Command layouts: every non-empty block in the corpus is either `complete` (creator-backed layout) or `framed` (explicitly opaque 0x0D serializer envelope). Zero unresolved blocks. Layouts exist for opcodes 02, 04, 07, 08, 09, 0A, 0C, 0D (boundary only), 0E, 13, 17, 18; each is traced to its creator function in WarGame3.exe build 59638 (`REA-NOTES-59638.md`, `research/COMMAND-LAYOUTS.md`).
- Command semantics: verified only for build 59638. Other builds are marked `inferred`. Field meanings for 0x0C, 0x13 and 0x18 are structural only; the timeline reports them with raw fields and explicit limitations.
- Outcomes (kills, hits, scores, positions over time): not decoded. Not observed in the three available samples; whether other replays encode them is untested.
- Source limit: all 3 samples come from one independent source (KoppelTAR, commit 9f77fa9). The two-source requirement is not met. See REPLAY-RESEARCH.md.

## Usage

    python3 wgrd_replay.py REPLAY.wargamerpl2 [--summary] [--include-empty] [--no-verify-digest]
    python3 wgrd_replay.py REPLAY.wargamerpl2 --timeline [--summary] [--unit-data research/unit-data/build59638-v1.json.gz]

Default output contains the header, metadata, and per-pact command decode. `--timeline` emits the ordered `wgrd_timeline/1` event list with source byte offsets. `--unit-data` adds offline unit-type names from the build 59638 index. Timeline output is strict JSON; non-finite float32 values are emitted as `{"nonfinite": "+Infinity"}` style markers. **2026-10-28 correction:** the default parser CLI still permits Python's non-standard NaN/Infinity JSON tokens. Use timeline output when strict JSON is required; see the [usage guide](docs/USAGE.md).

## Tests

    python3 -m unittest discover -s tests -q

The 2026-10-28 local run executed 139 tests with no skips with its external artifacts available; this is a historical result, not the current test count. A later run at commit 2bde168 (2026-10-28) executed 148 tests, OK, with no skips. Cross-build tests use `WGRD_ARTIFACTS_DIR` and skip explicitly when external files are absent; altered files fail. **2026-10-28 clarification:** some older sample-backed tests fail with missing-file errors rather than skipping. See [test prerequisites](CONTRIBUTING.md#tests-and-external-artifacts) before interpreting a fresh-checkout run. Report actual results and skips.

## Reproducing research findings

The 2026-10-26 research notes under `research/` name their artifacts (build, SHA-256, addresses) and ship a standalone read-only script that re-derives the result and exits non-zero on mismatch:

    python3 -B research/op0c_layout.py WarGame3.exe 'samples/raw/koppeltar-Sample*'
    python3 -B research/op_fixed_layout.py WarGame3.exe 'samples/raw/koppeltar-Sample*'
    python3 -B research/op18_reference_keys.py 'samples/raw/koppeltar-Sample*'
    python3 -B research/coverage.py > research/coverage.json

## Documentation map

- `AGENTS.md`: operating guide for AI coding and reverse-engineering agents (reading order, evidence standards, verified commands, preservation rules).
- `docs/ARCHITECTURE.md`: data flow, status vocabularies, canonical document per subsystem.
- `FORMAT.md`: byte-level format spec. Each field is tagged VERIFIED, INFERRED, or UNKNOWN with evidence. Start here for the format.
- `research/INDEX.md`: provenance index. Every current claim mapped to its original note, evidence record, reproduction script and tests, with a reproducibility status code.
- [The ASCII Dragon Incident](research/DRAGON-INCIDENT.md): a cautionary tale about agent overengineering, uncertain dragons, and one victorious cow.
- `NEXT-STEPS.md`: current priorities and detailed open items.
- `REA-NOTES-59638.md`: executable analysis notes for build 59638 (addresses, evidence IDs). `REPLAY-RESEARCH.md`: investigation log.
- `research/`: per-topic research notes, historical plans, reproduction scripts, generated coverage JSON, `research/evidence/` (REA records, disassembly excerpts), `research/chatgpt-session-2026-10-23/` (archived session), `research/maintenance/` (preservation manifests and verifiers, link checker), `research/session-records/`.
- `samples/`: manifest and binary inventory. Replay files are not in Git (see `.gitignore`).

## Layout

- `wgrd_replay.py`: container, frame, and command decoder. Opcode table `OPCODE_CLASSES`.
- `wgrd_entities.py`, `wgrd_orders.py`, `wgrd_production.py`, `wgrd_timeline.py`, `wgrd_unit_data.py`, `wgrd_unit_index.py`: entity, order, production, timeline, and unit-name layers.
- `tests/`: unittest suite; corpus and executable tests skip when external artifacts are absent.

## Next milestone

The first controlled current-build recording and playback are complete. The next timing and movement work is described in [the Phase 2 handoff](research/current-build/PHASE-2-HANDOFF.md); it does not authorize VM operation. The controlled experiment report holds current evidence and limits; `research/GROUND-TRUTH-PREREQUISITES.md` remains a historical prerequisite record.

## Known limitations

- `parse_header()` raises `AttributeError` instead of `ReplayFormatError` when the metadata JSON root, or its `game` value, is not an object. Reproduced on 2026-10-28 with a metadata root of `[]`. Not fixed. The fix belongs in a separate, tested change; the comment above the return in `parse_header` records the same defect.

## Not included

- Replay files and game binaries. They are kept outside Git because redistribution is unclear.
- Any claim about gameplay outcomes. The decoder reads inputs and command structure only.

## Format spec

Read [FORMAT.md](FORMAT.md) for the container, chunk, frame, and `pact` layouts, opcode 0x08 detail, and the timeline output schema.

## Credits

AI models produced the research and code in this repository, running on [Hermes Agent](https://hermes-agent.nousresearch.com) via the Nous Portal. The repository owner directed and reviewed the work.

- Reverse engineering of build 59638 in the 2026-10-26 sessions (opcode 0x0C creator and helper readers, fixed-size creators for 0x02/0x13/0x18, the 0x18 registry-key cross-reference), assessment and roadmap, review and integration of delegated work: Claude Fable 5.1 (Anthropic), technical lead.
- Decoder implementation, regression tests, coverage regeneration and implementation docs for opcodes 0x0C, 0x02, 0x13, 0x18 and the 0x0C timeline interpretation: Claude Haiku 5.5 (Anthropic), working in isolated git worktrees under the lead's review.
- Earlier sessions (container, digest, framing, dispatcher, opcodes 04/07/08/09/0A/0D/0E/17, NDF bridge, timeline) are recorded in `REPLAY-RESEARCH.md`, `REA-NOTES-59638.md` and `research/chatgpt-session-2026-10-23/`.
- Tooling: rizin, Ghidra, REA MCP, Python 3 standard library. The Sample1 battle-report surface (`research/reports/sample1/`) was authored on OpenAI's `data-app` report runtime (Codex/ChatGPT `build-report` skill); the runtime itself is not redistributed here, only the authored content and a self-contained HTML build.

The 2026-10-26 findings (`research/CHANGEPRODUCTION-0C.md`, `research/FIXED-OPCODES-02-13-18.md`, `research/OP18-REFERENCE-KEYS.md`, `research/OP18-SUPPLY-TARGETS.md`) are each backed by a reproduction script and regression tests that exercise the claim against the artifacts named in the note. Earlier research is documented with evidence IDs and notes in `research/evidence/` and `REA-NOTES-59638.md`; not all of it has a standalone script.
