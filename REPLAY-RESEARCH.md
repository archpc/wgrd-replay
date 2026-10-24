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
- Checksum: 28 bytes at 0x0C = SHA-224(file[0x28:EOF]), VERIFIED on all 3 samples
  and confirmed from the executable (see Phase 3).
- Alignment: none (chunks packed, odd offsets occur, e.g. 0xc89).

Comparison: qReplay (replay.cpp) and the 3Mydlo3 PowerShell gist only text-scan for
`{"game` … `}}` JSON; neither parses binary framing. wgrd-cons-parsers has no replay parser.
Our JSON boundaries agree with that scan.

## Phase 3 — REA
Executables: user-owned Steam copy (app 251060) fetched with DepotDownloader 3.4.0
(`-os windows -qr`, .exe/.dll file list only). Inventory with SHA-256 for every file:
samples/game-binaries.json. Binaries are kept outside Git in ~/.hermes/artifacts/wgrd-replay/game/.
Target analyzed: Data/PC/59638/WarGame3.exe (sha256 1c7533eb…4bda46), the same build as
Samples 1 and 3. Full findings, addresses, and evidence IDs: REA-NOTES-59638.md.

Summary:
- FUN_010b9300 (VA 0x010b9300, file 0xcb8700): ntohl magic == 'ESAV', version <= 1,
  reads the file-size field (FUN_010b9790), then the 28-byte digest.
- FUN_010b9500 (VA 0x010b9500, file 0xcb8900): per-chunk reader. 4 × ntohl header words,
  L <= remaining check, SHA-224 over chunk bytes, visitor vtbl[+8](tag, A, ptr, L).
- FUN_00b3c5d0 (TReplayActionVisitor vtbl[+8]): integer compares 'pact'/'endt'/'star';
  pact payloads are queued raw.
- FUN_0093c670: handles 'rply' (JSON chunk) and 'cmpg'.
- FUN_016fd070: SHA-224 IV constants, digest length 0x1c.
- Parser comparison: structure CONFIRMED. The parser is stricter than the executable on
  version, fields A/B, file-size equality, and frame order. Current code verifies the SHA-224 digest; the older comparison was stale.

Earlier (pre-executable) REA use: Ghidra raw-binary import of Sample2 for byte
cross-checks (read_bytes/search_bytes matched Python). provider_id=rizin is rejected by
open_binary (accepts ghidra/hopper/ida/kuna); reverse-engineering skill patched.
Hopper 6.6.0-demo installed on user request; not used.

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

## Counted-block implementation milestone (2026-10-23)

REA 6.7.0 MCP/Rizin findings and immutable-artifact evidence now retained in
research/COMMAND-LAYOUTS.md and research/evidence/. Shared-cursor implementation
splits 594/594 multi-command blocks exactly: 571 complete field layouts, 23
framed with opaque 0d serializer content. Raw blocks, prefix boundaries and
unresolved tails are retained. No speculative names for new fields.

Across all nonempty blocks: 10,830/10,942 split; 112 unresolved singles remain.
Build provenance, opaque interiors and one-source limitation stay explicit.
31 tests pass; authentic coverage/reassembly census in research/coverage.json.
