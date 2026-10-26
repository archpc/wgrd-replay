# wgrd-replay

Offline, stdlib-only decoder for Wargame: Red Dragon replay files (`.wargamerpl2`).

It parses the `ESAV` container, verifies the SHA-224 digest, walks the `star` / `pact` / `endt` frame stream, and splits command blocks into opcode-level commands. Unknown or unsupported data is kept as raw hex. Nothing is guessed or silently skipped. Malformed input raises `ReplayFormatError`.

## Status

- Container, digest, and frame framing: verified on all 3 samples.
- Command splitting: 594/594 multi-command blocks split with exact count and EOF. 571 complete layouts, 23 opaque-framed blocks.
- Command semantics: verified only for build 59638. Other builds are marked `inferred`.
- Outcomes (kills, hits, scores, positions): not decoded. Likely need simulation reconstruction. Not proven.
- Source limit: all 3 samples come from one independent source (KoppelTAR, commit 9f77fa9). The two-source requirement is not met. See REPLAY-RESEARCH.md.

## Usage

    python3 wgrd_replay.py REPLAY.wargamerpl2 [--summary] [--include-empty] [--no-verify-digest]
    python3 wgrd_replay.py REPLAY.wargamerpl2 --timeline [--summary] [--unit-data research/unit-data/build59638-v1.json.gz]

Default output is JSON with the header, metadata, and per-pact command decode. `--timeline` emits the ordered `wgrd_timeline/1` event list with source byte offsets. `--unit-data` adds offline unit-type names from the build 59638 index.

## Tests

    python3 -m unittest discover -s tests -q

98 tests pass.

## Layout

- `wgrd_replay.py`: container, frame, and command decoder. Opcode table `OPCODE_CLASSES`.
- `wgrd_entities.py`, `wgrd_orders.py`, `wgrd_production.py`, `wgrd_timeline.py`, `wgrd_unit_data.py`, `wgrd_unit_index.py`: entity, order, production, timeline, and unit-name layers.
- `FORMAT.md`: byte-level format spec. Each field is tagged VERIFIED, INFERRED, or UNKNOWN with evidence. Start here.
- `REA-NOTES-59638.md`: reverse-engineering notes on game build 59638 (addresses, evidence IDs).
- `REPLAY-RESEARCH.md`: investigation log and method.
- `NEXT-STEPS.md`: open work, prioritized.
- `research/`: coverage JSON, command layouts, timeline semantics, NDF bridge.
- `samples/`: manifest and binary inventory. Replay files are not in Git (see `.gitignore`).

## Not included

- Replay files and game binaries. They are kept outside Git because redistribution is unclear.
- Any claim about gameplay outcomes. The decoder reads inputs and command structure only.

## Format spec

Read [FORMAT.md](FORMAT.md) for the container, chunk, frame, and `pact` layouts, opcode 0x08 detail, and the timeline output schema.
