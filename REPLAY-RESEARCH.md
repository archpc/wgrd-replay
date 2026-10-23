# REPLAY-RESEARCH.md

Investigation date: 2026-10-23. Analyst: Hermes (claude-opus-5.5). All findings
re-derived from sample bytes; prior community claims treated as hypotheses.

## Phase 0 — Recon
- No prior Wargame project, notes, samples, or game binaries on Honk (searched ~/Code,
  ~/.hermes, Steam dir; only two unrelated value-manual PDFs in iCloud).
- Tooling: REA 6.7.0 MCP (Ghidra 12.1.4, Kuna; rizin via execute_rizin_command only),
  rizin (brew), Python 3.9.6 stdlib. Hopper 6.6.0-demo installed via brew cask on user
  request (2026-10-23); not exercised (no executable to analyze; Hopper rejects raw-binary).
- New repo ~/Code/wgrd-replay; no baseline existed.

## Phase 1 — Samples
See samples/manifest.json. 3 samples, 1 independent source (KoppelTAR GitHub repo,
commit 9f77fa9, 2022-01-24). Second-source attempts all failed (manifest lists them).
Requirement of ≥2 independent sources NOT met.

## Phase 2 — Container (summary; full map in FORMAT.md)
- `ESAV` header: VERIFIED. JSON metadata: VERIFIED (length-prefixed at 0x30, starts 0x38).
- `star`/`pact`/`endt` markers: VERIFIED as 16-byte-header chunks; full-file walk lands exactly at EOF in all 3.
- Compression: none observed in container (JSON and command text are plaintext).
- Checksum: 28 bytes at 0x0C UNKNOWN; not plain MD5/SHA1/SHA256 over tested ranges.
- Alignment: none (chunks packed, odd offsets occur, e.g. 0xc89).

Comparison: qReplay (replay.cpp) and the 3Mydlo3 PowerShell gist only text-scan for
`{"game` … `}}` JSON; neither parses binary framing. wgrd-cons-parsers has no replay parser.
Our JSON boundaries agree with that scan.

## Phase 3 — REA
- No legitimate game executable available; none downloaded. Replay-loader analysis BLOCKED.
- REA used for independent byte verification only: Ghidra 12.1.4 raw-binary import of
  Sample2 (sha256 132a1a1b…, x86, entry 0x0 ⇒ address = file offset).
  read_bytes 0x0/64 and 0x963/48 matched Python; search_bytes `star…0008` → 0x96b, 0xa3f, 0xc94…
  matches the Python walk.
- First attempt with provider_id=rizin failed (capability_unavailable: open_binary accepts
  ghidra/hopper/ida/kuna). Skill reverse-engineering patched with this pitfall.

## Phase 4 — Command recovery
Opcode 0x08 (layout VERIFIED, meaning INFERRED map marker with optional text). Evidence:
1. Exact length rule 39+T on 226/226 instances across 3 files.
2. Embedded handle equals 0xC000001E+slot on 226/226 — ties command to the issuing slot.
3. Text present iff type==3 (226/226); texts are coherent player chat with map context.
4. Floats fall in the same coordinate range as op 0x0c floats.
Not validated against game execution (no game). Timing: frame index only; seconds UNKNOWN.

## Inputs vs outcomes
One pact per slot per frame, ~96.5% empty ⇒ lockstep input log. No explicit
kill/score/position records found. Treat outcomes as requiring simulation.

## Reproduction
```
cd ~/Code/wgrd-replay
python3 -m unittest -v tests/test_wgrd_replay.py
python3 wgrd_replay.py --summary ~/.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample1.wargamerpl2
```

## Open questions
See NEXT-STEPS.md.
