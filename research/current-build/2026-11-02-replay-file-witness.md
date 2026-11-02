# Native replay-file witness — revision 131544

Status: **file identity witnessed for the new playback**. This does not
retroactively authenticate earlier combat captures or prove complete simulation
coverage.

## Target and evidence

- Engine SHA-256: `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
- Replay SHA-256 before and after: `abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121`.
- Replay size: 344438 bytes.
- Task-private probe: the maintained wide-string observer with only its export
  lookup changed to `KERNELBASE.dll!CreateFileW`. Probe file SHA-256:
  `95024380e713312acf6a4c06bfcbdbe2cf57f79d2115fcbfdf12faaa2935d7f6`.
- Private evidence root: `ansi-live-01/`. Closed witness trace:
  `guest-export-03/ansi-open-window-04.jsonl`. Parent validation:
  `file-open-witness-validation.json`.
- The closed-evidence export contains 52 files, all independently hash-verified
  against the guest manifest. The active native collector and its two output
  streams were explicitly excluded until they finish; no snapshot was restored.

## Observations

Three bounded `KERNEL32!CreateFileA` windows covered Profile/Replay opening,
selection and Play. They installed successfully but observed no calls or matching
opens. These are inconclusive windows, not proof that the file was not opened.

A read-only IAT/export comparison in the same process established:

| Item | Address in this process |
| --- | --- |
| Main image | `0x400000` |
| CreateFileA IAT slot | `0x19131a8` |
| Resolved CreateFileA / KERNEL32 export | `0x76dc1c00` |
| KERNEL32 CreateFileW export | `0x76dc1c70` |
| KERNELBASE CreateFileW export | `0x77141ce0` |

The ASLR-dependent export addresses are evidence for this process only, not
production constants. The matching A import/export rules out that particular
address-selection mismatch; it does not establish which I/O route the replay
reader uses. The IAT comparison artifact SHA-256 is
`22355aaf1b6f059299b1fb705ce9921b8cf6806f839417f81d774ca024b57844`.

The follow-up W watch checked its installed target against the independently
read KERNELBASE export before any input. A calibrated target-row selection and
Play then produced two exact normalized-path matches with valid returned
handles. Both calls used `GENERIC_READ` (`0x80000000`), share flags 3 and
`OPEN_EXISTING` (3). Their handles were `0xfa4` and `0xf10`. There were 14 other
opens, zero path-read errors, zero dropped records, no invalid matching handles,
and an `end` record with zero cleanup errors. Before/after replay digests matched.

Both recorded return addresses were `0x759f4840`. Backtraces were requested with
Frida's fuzzy unwinder; they are leads, not authenticated full call chains.
This demonstrates coverage of the KERNELBASE entry point for these opens. It
does not prove that the KERNEL32 wrapper is never used elsewhere.

## Same-playback native collection

After the successful file witness, a bounded V3 collector was started in the
same game process, with hooks-ready confirmation and a 600-second limit.
The initial interval before collector readiness is uncovered. The completed
native trace SHA-256 is
`6d88cefc03e1cf6a9bc4a3ddb70318569789d124266a37ffea1e5f5121601617`.
Its 1796 records include clean summary/end records, zero callback/cleanup errors,
zero suppressed events and no outstanding threads or scope mismatches. The final
57-file guest export was independently hash-verified on the Mac.

File witness, native capture and a separate completion observation have matching
PID, process-creation FILETIME and executable digest. The GameEnded byte was
observed true at deterministic counter 4165 / engine-named seconds 833.0; the
stable counter alone was not used as completion evidence. No manual exit was
requested for this second playback.

The existing strict V3 exporter accepted the new trace and retained source pins:
28 impacts (25 suppression increases, three physical-damage increases), nine
event-involved unit histories, three threshold-parented lifecycle destructions,
356 position observations across 71 tracks and 146 raw anchor changes. All 356
position observations are bracketed; 349 have exact GUID+token joins and seven
remain ambiguous. Source roles and individual killer credit remain provisional.

The 28-event mode/arg0/six-field before-after projection matches the earlier
capture exactly. Clock sampling begins at observed counter 453 and ends at 4164;
no frame-application callbacks were captured after the delayed collector start.
Neither fact establishes a battle origin or zero replay-frame processing.
The private `file-witnessed-aar-v1/` export contains the structured results,
chronology, a short readable report and a separate `replay-provenance.json`
sidecar with the file/epoch links and coverage limitations.

A replay speed input produced a raw factor of 2.0 and approximately ten observed
counter ticks per wall second, but the step-index field stayed zero. The old
step-derived model therefore reported inconsistency. The strict 2x consistency
check failed; no further speed input was issued and no model was repaired merely
to make the check pass. This is an adjacent timing-model uncertainty, separate
from the successful file witness.

## Validation and integration status

The canonical resolver change prefers KERNELBASE, then kernel32, then the
legacy module-search fallback. Its bounded UTF-16 reads, exact-path matching,
Win32 ABI, invalid-handle handling and per-invocation records remain unchanged.
Resolver provenance is retained in install/watch metadata.

A new regression first failed against the old resolver. The final canonical
suite passed 329 tests with two existing skips; Ruff, syntax, documentation and
preservation gates passed. An earlier full run failed because a source-contract
test rejected the word CreateFileA in an explanatory comment. The corrected
assertion rejects implemented API string literals, not prose; the failed log is
retained. No production behavior was changed merely to satisfy that assertion.
Independent reconstruction of the new dataset passed with its declared coverage
gaps: all 356 raw position observations, 146 transition intervals, 28 impacts,
three threshold-parented lifecycle calls, same-process file/completion links and
57 exported files were checked without running project code. The independent
review digest is
`117507e005b6f2b8f5adc069357e40af7627ad0db1efcd2e5c815bf1d8b7384e`.
The source roles, distance units, battle origin and initial uncovered interval
remain unknown. The watcher review approved the resolver implementation; its
stale test failure was closed by a read-only follow-up against the corrected
assertion and passing-run evidence. Current source and test hashes matched the
approved snapshot before commit. Follow-up review digest:
`6aed42004139f981225bd59271a033147c04832e735156ae452e4976f5001115`.
The lexical guard remains a source-contract check, not a formal JavaScript
read-only proof; template-literal and quoted-comment edge cases are documented
non-blocking coverage limits. The final unnamed-search fallback is also not
separately exercised by the new factory. No test rerun was needed for review.

## Controls and preservation

Replay exit used the actual HQ button in the lower-left game panel, then Exit
and its confirmation. A prior Escape input left the captured frame unchanged;
it was not treated as a successful menu transition. The first playback was
manually exited, not declared naturally complete.

No credentials were entered, multiplayer used, game functions called, game
memory directly written, settings restored or snapshots reverted. Interceptors
were limited to the authorized OS file-open API and native observation hooks.
Private screenshots, traces, paths and large research files remain outside Git.
