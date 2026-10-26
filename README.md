# wgrd-replay

Offline, stdlib-only decoder for Wargame: Red Dragon replay files (`.wargamerpl2`).

It parses the `ESAV` container, verifies the SHA-224 digest, walks the `star` / `pact` / `endt` frame stream, and splits command blocks into opcode-level commands. Unknown or unsupported data is kept as raw hex. Nothing is guessed or silently skipped. Malformed input raises `ReplayFormatError`.

## Status

- Container, digest, and frame framing: verified on all 3 samples.
- Command splitting: 594/594 multi-command blocks split with exact count and EOF.
- Command layouts: every non-empty block in the corpus is either `complete` (creator-backed layout) or `framed` (explicitly opaque 0x0D serializer envelope). Zero unresolved blocks. Layouts exist for opcodes 02, 04, 07, 08, 09, 0A, 0C, 0D (boundary only), 0E, 13, 17, 18; each is traced to its creator function in WarGame3.exe build 59638 (`REA-NOTES-59638.md`, `research/COMMAND-LAYOUTS.md`).
- Command semantics: verified only for build 59638. Other builds are marked `inferred`. Field meanings for 0x0C, 0x13 and 0x18 are structural only; the timeline reports them with raw fields and explicit limitations.
- Outcomes (kills, hits, scores, positions over time): not decoded. Not observed in the three available samples; whether other replays encode them is untested.
- Source limit: all 3 samples come from one independent source (KoppelTAR, commit 9f77fa9). The two-source requirement is not met. See REPLAY-RESEARCH.md.

## Usage

    python3 wgrd_replay.py REPLAY.wargamerpl2 [--summary] [--include-empty] [--no-verify-digest]
    python3 wgrd_replay.py REPLAY.wargamerpl2 --timeline [--summary] [--unit-data research/unit-data/build59638-v1.json.gz]

Default output is JSON with the header, metadata, and per-pact command decode. `--timeline` emits the ordered `wgrd_timeline/1` event list with source byte offsets. `--unit-data` adds offline unit-type names from the build 59638 index. Output is strict JSON; non-finite float32 values are emitted as `{"nonfinite": "+Infinity"}` style markers.

## Tests

    python3 -m unittest discover -s tests -q

129 tests pass (1 skipped without the cached public unit snapshot). Corpus and executable-backed tests skip when the replay samples or WarGame3.exe are not present locally; `WGRD_SAMPLES_DIR` and `WGRD_EXE_59638` override the default paths.

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
- `NEXT-STEPS.md`: current priorities and detailed open items.
- `REA-NOTES-59638.md`: executable analysis notes for build 59638 (addresses, evidence IDs). `REPLAY-RESEARCH.md`: investigation log.
- `research/`: per-topic research notes, historical plans, reproduction scripts, generated coverage JSON, `research/evidence/` (REA records, disassembly excerpts), `research/chatgpt-session-2026-10-23/` (archived session), `research/maintenance/` (preservation manifests and verifiers, link checker), `research/session-records/`.
- `samples/`: manifest and binary inventory. Replay files are not in Git (see `.gitignore`).

## Layout

- `wgrd_replay.py`: container, frame, and command decoder. Opcode table `OPCODE_CLASSES`.
- `wgrd_entities.py`, `wgrd_orders.py`, `wgrd_production.py`, `wgrd_timeline.py`, `wgrd_unit_data.py`, `wgrd_unit_index.py`: entity, order, production, timeline, and unit-name layers.
- `tests/`: unittest suite; corpus and executable tests skip when external artifacts are absent.

## Next milestone

Ground-truth validation: record a scripted match on the Parallels Windows guest (game build 59638 binary and NDF verified present) and compare decoded commands against the action log. Prerequisites, blockers and protocol: `research/GROUND-TRUTH-PREREQUISITES.md`. Until then no semantic claim in this repository has been checked against observed gameplay.

## Not included

- Replay files and game binaries. They are kept outside Git because redistribution is unclear.
- Any claim about gameplay outcomes. The decoder reads inputs and command structure only.

## Format spec

Read [FORMAT.md](FORMAT.md) for the container, chunk, frame, and `pact` layouts, opcode 0x08 detail, and the timeline output schema.

## Credits

Research and development in this repository were carried out by AI models directed and reviewed by the repository owner, running on [Hermes Agent](https://hermes-agent.nousresearch.com) via the Nous Portal.

- Reverse engineering of build 59638 in the 2026-10-26 sessions (opcode 0x0C creator and helper readers, fixed-size creators for 0x02/0x13/0x18, the 0x18 registry-key cross-reference), assessment and roadmap, review and integration of delegated work: Claude Fable 5.1 (Anthropic), technical lead.
- Decoder implementation, regression tests, coverage regeneration and implementation docs for opcodes 0x0C, 0x02, 0x13, 0x18 and the 0x0C timeline interpretation: Claude Haiku 5.5 (Anthropic), working in isolated git worktrees under the lead's review.
- Earlier sessions (container, digest, framing, dispatcher, opcodes 04/07/08/09/0A/0D/0E/17, NDF bridge, timeline) are recorded in `REPLAY-RESEARCH.md`, `REA-NOTES-59638.md` and `research/chatgpt-session-2026-10-23/`.
- Tooling: rizin, Ghidra, REA MCP, Python 3 standard library.

The 2026-10-26 findings (`research/CHANGEPRODUCTION-0C.md`, `research/FIXED-OPCODES-02-13-18.md`, `research/OP18-REFERENCE-KEYS.md`, `research/OP18-SUPPLY-TARGETS.md`) are each backed by a reproduction script and regression tests that exercise the claim against the artifacts named in the note. Earlier research is documented with evidence IDs and notes in `research/evidence/` and `REA-NOTES-59638.md`; not all of it has a standalone script.
