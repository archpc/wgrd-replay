# WGRD Frida tracing

Maintained workflow: capture with `wgrd_frida.py` and a hook configuration
(current AAR: `aar-capture-131544-v3.json`), then export with `aar_events.py`
([Retained-capture AAR export](#retained-capture-aar-export)).

The unfinished Gate 1/2 queue-capture mode (`--gate-replay`) and its tests were
never merged. They are preserved as WIP from the retired `frida-worktree`, in
the private `retired-worktrees-20261102` artifact archive, and are not part of
this tool.

Do not copy runtime data, raw traces or replay bytes into Git. Any future guest
execution, Frida attachment or replay requires separate authorization.

This optional research tool uses the Windows Frida Python API. It is separate
from the standard-library replay decoder and does not add a decoder dependency.
It attaches to an already-running process; it never launches the game. Frida
must already be installed in the guest Python environment. Do not change
security settings, game files, or network configuration to make it work.

## Safety and identity

Use only on an authorized, trusted local process. Select the guest and running
process explicitly. The hook configurations apply only to the executable with
SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
The controller checks the Windows process path and creation time before and
following attachment, hashes the process image, checks its embedded revision,
and checks the explicit `wargame3.exe` module's path, x86 PE32 headers, loaded
address ranges, and 16 bytes at every selected hook against the hashed file.
It rehashes the file before installing hooks. This compares specific loaded
bytes, not a hash of all loaded memory. It never relies on `Process.mainModule`.

An injection changes the target process temporarily. Detachment and script
unload are attempted on normal completion, callback errors, and Python
exceptions. Forced termination, Windows failure, an external process exit, or a
broken transport can interrupt cleanup; inspect the JSONL and the process state.
The controller does not kill the target or modify game assets. A bounded
runtime and event limit reduce, but do not eliminate, overhead or perturbation.

Keep executable binaries, replays, screenshots, full traces, and player data
outside Git. The controller exclusively creates its output file and rejects
paths inside a discoverable checkout. Protect guest and host copies. A hash of
the executable on disk does not establish that its loaded image is entirely
unmodified.

## Run through Parallels MCP

Discover the running VM and use its UUID. Copy the three files in this directory
(`wgrd_frida.py`, `hooks.js`, and the hook configuration JSON) to a guest-readable
staging directory, verify their hashes, and choose a new private output path.
Use the existing guest Python containing Frida. For example, invoke
`mcp__parallels__parallels_vm_exec_start` with the UUID, a bounded timeout,
`elevated: false` or omitted, and a Windows command equivalent to:

```text
C:\Users\USER\frida-wgrd\Scripts\python.exe C:\STAGING\wgrd_frida.py --config C:\STAGING\aar-capture-131544-v3.json --output C:\PRIVATE\run-01.jsonl --pid PID --seconds 480 --event-limit 20000
```

Replace every placeholder with the verified local path or PID. Omit `--pid` to
require exactly one process named `wargame3.exe`. Repeat `--hook NAME` to select
a subset. `--seconds` is 1–600; `--event-limit` is 1–100000. The limit covers
enter/leave events, not administrative or callback-error records. Hooks remain
installed until the bounded interval ends even after the limit is reached;
summary reports suppressed events. Poll `parallels_vm_exec_result` until its
terminal state. Require exit 0, empty stderr, `HERMES_DONE_WGRD_TRACE`, and a
JSONL `summary`, `detached` reason `application-requested`, and `end` with zero
cleanup errors. Inspect any `failure`, `script_error`, or `callback_error`.
Do not infer success from a running job, a filename, or an exit code alone.

## Configuration

Each revision file fixes a SHA-256, explicit module, Ghidra preferred base, and
hook entries. Each entry names a unique Ghidra VA, number of stack arguments,
`sample_every` (first call, then every Nth), optional `backtrace`, and optional
bounded reads. Each read names `ecx`, `edx`, or `arg0`…`arg11`, a nonnegative
offset up to 4096, and a size from 1 to 128 bytes. Optional `phase` is `enter`
(the default), `leave`, or `both`; a leave read uses the entry-time pointer and
reads current memory just before return. Optional `indirect: true` reads one
pointer from the selected source plus offset, then reads the requested size at
that pointer. Optional `second_indirect: true` follows one further pointer;
`indirect: true` is required. Every pointer slot and destination is checked
independently, and the recorded `chain` retains the values read. A leave-time
pointer may have been freed or reused even if it is readable.
A read is attempted only if
the whole requested span lies in a single readable mapped range. A range check
can race an unmapping; read exceptions are recorded as failed reads. Registers
and arguments are raw values. For x86 `thiscall`, ECX is commonly the object;
verify the calling convention per function, not by configuration alone.

Only use function entries and offsets supported by evidence from the exact
executable revision. Optional `within: ["parent_hook"]` admits a hook only while
one of those instrumented hooks is active on the same OS thread and its saved
ESP is above the callee's ESP. Other invocations increment `summary.filtered`
without emitting entry/return records. In standard (non-gate) capture mode,
`summary.counts` counts admitted callbacks; `counts + filtered` recovers observed
entries for scoped hooks. This is a
bounded nesting filter, not proof of unit identity, lifetime or causality.

A read may use `source: "retval"` only with `phase: "leave"`. It treats the raw
return register as a pointer, records each bounded dereference, and retains failed
reads explicitly. It does not validate the pointed-to type or a success boolean;
for a byte-returning x86 function, unrelated upper EAX bits can remain nonzero.

Python converts VA to RVA relative to `ghidra_base`; the
script adds the RVA to the observed module base. It rejects an address outside
the loaded image or mismatched entry bytes. Configuring a new function does not
establish its calling convention, parameters, return meaning, or success.

### Loss accounting (opt-in)

`loss_accounting: true` makes the script assign a contiguous integer
`sequence` (from 1) to every record it sends, including `callback_error`, and
report `loss_accounting: {last_sequence, send_failures}` in the stop summary.
The controller audits the stream: missing, duplicate, out-of-order or
non-integer sequences fail the capture, and the final summary must reconcile
with the receiver's last sequence. All sender loss counters (`send_failures`,
`suppressed`, `callback_errors`, `stale_frames`, `stack_mismatches`,
`outstanding_threads`) must be zero, with one explicit exception:
`loss_allow_outstanding_threads: true` (the key requires `loss_accounting:
true`) tolerates exactly one outstanding thread — the unpaired tick enter a
v4-style capture leaves at detach. The allowance never stretches to 2 and
never relaxes another counter. Because `suppressed` must be zero, size
`event_limit` for the expected record count of the whole window; the default
limit will fail a busy accounting capture by design. A record arriving after
drain completion fails the capture; the controller drains in-flight
deliveries for up to 0.5 s before the exit decision (legacy captures exit
immediately). A capture that already failed for another reason records
`loss_accounting_skipped` instead of a vacuous "complete" audit. On success
the trace gains a `loss_accounting` record with `received_records`,
`last_sequence`, `complete: true`; on any violation it gains
`loss_accounting_failure` records and the run exits nonzero.

With accounting disabled (the default) the trace and summary keep their legacy
shape exactly: no `sequence` fields, no `loss_accounting` keys. The mechanics
are exercised offline by `tests/frida_loss_sim.js` (simulated Frida API,
including a failed-send scenario), the receiver audit by
`tests/test_frida_controller.py`, and the controller wiring end-to-end by
`tests/test_frida_loss_integration.py` (fake Frida device: transport loss,
late delivery, install/stop failures; no game, no live attach). A live attach
still requires an authorized Windows capture. A clean audit proves record
transport integrity, not engine semantics or coverage completeness.

## Event schema and interpretation

Each line is JSON. Administrative records include `start`, `identity_verified`,
`hooks_installed`, `summary`, `detached`, `end`, and failures. `enter` includes
hook, UTC timestamp, per-hook ordinal, thread ID, raw ECX/EDX, stack arguments,
return address, optional bounded reads and backtrace, call ID, nearest active
hooked parent ID, and whether that parent was recorded. `leave` includes the
same call ID and thread, raw return value, and stack-match result. A return value
is not necessarily a success indicator. `summary.counts` counts all callbacks,
including unsampled calls; `emitted` and `suppressed` count enter/leave events.
UTC timestamps are wall-clock timestamps, not a monotonic or simulation clock.

Parent IDs represent observed nesting among instrumented functions on one OS
thread, not necessarily direct calls or command causality. Sampling can leave a
parent unrecorded. Event limits can truncate a pair. Exceptions/nonlocal unwinds,
thread-ID reuse, fibers and stack switching can invalidate the stack heuristic.
The script reports discarded stale frames, mismatches, callback errors and
outstanding threads. Do not treat even clean nesting as proof of a particular
request, actor, order, or successful gameplay outcome. Pointer values are scoped
to a process lifetime and may be reused for different allocations.

The order/queue tooling (`revision-131544.json` order hooks, the
`trace_inspect.py` inspector and its tests) had no active consumer and was
archived on 2026-11-02 to the private `order-tools-archive-20261102`. Restore it
with `git show 47f0ae2:<path>`. Its hook-target evidence remains in
`research/current-build/2026-10-29-native-excerpts.json` and
`research/current-build/2026-10-29-offline-corpus.md`.

## Retained-capture AAR export

`aar_events.py` is the single maintained AAR exporter, with revision-131544
`runtime` (default), `runtime-v3` and `runtime-v4` profiles. It verifies trace/index pins, pairs calls, joins captured descriptor
GUID and token bytes, and emits `events.json`, `units.json`, `summary.json` and
`chronology.md`. Existing outputs are never overwritten. Details and coverage:
[runtime AAR evidence](../research/current-build/2026-11-02-runtime-aar.md).

`runtime-v4` (schema `wgrd-aar-runtime-v4/1`) is v3 plus the `tick_step` hook
(`0xb34060`, reads `+0x68` accumulator, `+0x6c` frame index, `+0xa0`/`+0xa4`/
`+0xa5` mode bytes at enter and leave). It joins every event to the tick call
it fell inside: `frame_correlation` carries `status`, `frame_low`/`frame_high`,
`bracket_before_seconds`/`bracket_after_seconds`, `tick_call_id` and
`estimated_deterministic_seconds_bounds`. An exact frame is assigned only
inside a tick call or between two calls closer than the 1.0 s tolerance;
otherwise the frame stays a bracket. One unpaired `tick_step` enter at detach
is allowed; any unpaired event hook fails the export. v4 additionally emits
`combat_frames.json`. The frame/tick difference is carried as the observed
integers 10 or 11; no midpoint mapping or battle start is derived. Capture and
results: [frame-indexed combat events](../research/current-build/2026-11-03-combat-frames-captured.md).

Example executed from an isolated staged-source export against the retained data:

```sh
EVIDENCE="$HOME/.hermes/artifacts/wgrd-replay/aar-20261102T050816Z"
python3.14 -B instrumentation/aar_events.py \
  "$EVIDENCE/wgrd-aar-combat-20261102-01.jsonl" --runtime \
  --unit-index "$EVIDENCE/units/unit-index-131544.json" \
  --out "$EVIDENCE/existing-evidence-aar-repro"
```

The retired legacy profile (sampled `damage-state-combat-02.jsonl`) is archived
in Git. This reproduces `aar-20261102T050816Z/events-reviewed/` byte-for-byte:

```sh
git show 71c4f8e:instrumentation/aar_events.py > "$TMPDIR/aar_events_legacy.py"
C="$HOME/.hermes/artifacts/wgrd-replay/combat-20261101"
python3 -B "$TMPDIR/aar_events_legacy.py" "$C/damage-state-combat-02.jsonl" \
  --classified "$C/battle-timeline-classified.json" \
  --expect-classified-sha256 e19e83dd23c3baae5afadb89403676ac0b0fa68b73fdfb803f3edaceae1ebb4a \
  --out "$TMPDIR/legacy-aar"
```

Put matching capture-era source/config copies in `capture-sources/` beside the
trace for independent source-hash verification. Missing copies remain explicit;
mismatched copies fail. The current working scripts are not substituted. Source
roles, kill credit, movement and battle-clock mapping remain unproven where the
retained evidence does not establish them.

## Retired capture configurations

`aar-capture-131544-v2.json` (never used for a retained capture; superseded by
`aar-capture-131544-v3.json`) and `damage-publish-131544.json` (its
`0xc4cba0` publisher is gated off the AAR path; see
[causal chain](../research/current-build/2026-11-02-causal-chain.md)) were
removed. No retained trace's start record matches v2. Every trace records its
hook configuration in its `start` record, and Git history keeps the files.
