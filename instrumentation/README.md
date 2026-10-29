# WGRD Frida tracing

This optional research tool uses the Windows Frida Python API. It is separate
from the standard-library replay decoder and does not add a decoder dependency.
It attaches to an already-running process; it never launches the game. Frida
must already be installed in the guest Python environment. Do not change
security settings, game files, or network configuration to make it work.

## Safety and identity

Use only on an authorized, trusted local process. Select the guest and running
process explicitly. `revision-131544.json` applies only to the executable with
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
(`wgrd_frida.py`, `hooks.js`, and the matching revision JSON) to a guest-readable
staging directory, verify their hashes, and choose a new private output path.
Use the existing guest Python containing Frida. For example, invoke
`mcp__parallels__parallels_vm_exec_start` with the UUID, a bounded timeout,
`elevated: false` or omitted, and a Windows command equivalent to:

```text
C:\Users\USER\frida-wgrd\Scripts\python.exe C:\STAGING\wgrd_frida.py --config C:\STAGING\revision-131544.json --output C:\PRIVATE\run-01.jsonl --pid PID --seconds 480 --event-limit 20000
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
executable revision. Python converts VA to RVA relative to `ghidra_base`; the
script adds the RVA to the observed module base. It rejects an address outside
the loaded image or mismatched entry bytes. Configuring a new function does not
establish its calling convention, parameters, return meaning, or success.

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

Inspect a private trace using Python on the host:

```text
python3 -B instrumentation/trace_inspect.py /absolute/private/run-01.jsonl
python3 -B instrumentation/trace_inspect.py /absolute/private/run-01.jsonl --relations
python3 -B instrumentation/trace_inspect.py /absolute/private/run-01.jsonl --replay /absolute/private/recording.wargamerpl2
```

Relations preserve each observed parent/child pair, including one-to-many
relationships. They do not join by pointer or assert semantics. The inspector
flags missing or malformed correlations, missing summaries, limits, callback
errors, and unmatched calls. `--replay` strictly parses and hashes the replay,
then compares captured reference prefixes and 36-byte structures against
opcode-0x07 candidates with one to four actor references. It skips larger
actor arrays. A candidate needs enough captured bytes; a missing candidate
can mean insufficient capture, not a mismatch. The utility does not verify the
runtime actor count, so a matching prefix is not proof of identity. Multiple
candidates remain ambiguous. It only accepts the pinned executable and literal
131544 replay version. It does not establish a runtime frame counter or prove
execution.

## Initial revision-131544 targets

These are narrow Ghidra candidates, not recovered source names. Evidence is in
`research/current-build/2026-10-29-native-excerpts.json` and
`research/current-build/2026-10-29-offline-corpus.md`.

| Hook | Ghidra VA | RVA | Current evidence and limits |
|---|---|---|---|
| `network_packet_dispatch` | `0x00b3dbc0` | `0x0073dbc0` | Reads frame, slot and command block; indirect calls and path coverage are incomplete. Two stack arguments in Ghidra. Frequency depends on replay loading and playback. |
| `order_request_wrapper` | `0x00b2be30` | `0x0072be30` | ECX-relative request object; two stack arguments; resolves object+4 and +0x60 and forwards them. Inferred x86 thiscall. Runs for this request path, not necessarily all orders. |
| `reference_resolution` | `0x00b2d210` | `0x0072d210` | Four stack arguments, caller cleanup; resolves references into a list. The fourth argument points to the input reference container; the first is the output list. |
| `handle_conversion` | `0x00b31410` | `0x00731410` | Eight stack arguments in the listed call, caller cleanup; it resolves values and copies object `+0x20` into a new list. Meaning and failure cases remain bounded to the static trace. |
| `order_group_dispatcher` | `0x00b31830` | `0x00731830` | Current-build group dispatcher; stack arguments include the copied 36-byte option structure. Ordinary and specialized paths differ. Exact parameter types remain incomplete. |
| `actor_order_grouping` | `0x00c96440` | `0x00896440` | Called by the dispatcher and other functions; grouping semantics are inferred from current-build control flow. Eight captured stack slots are raw; Ghidra prototype and nested structures need further checking. |
| `order_prepare_candidate` | `0x00abc100` | `0x006bc100` | Ghidra shows a thiscall-like ECX object and two stack parameters. It updates fields under some conditions; captured before/after values alone do not establish purpose or gameplay effect. |
| `queue_replace_candidate` | `0x00abb3b0` | `0x006bb3b0` | Three stack arguments; current-build static analysis shows a gated list-clear-and-insert path. A call does not prove every actor passed the gates. |
| `queue_append_candidate` | `0x00b36d10` | `0x00736d10` | Three stack arguments; current-build static analysis shows gated actor-list append paths. Capture is optional; zero calls do not prove a path is impossible. |
| `queue_clear_candidate` | `0x00abb550` | `0x006bb550` | One stack parameter points to an object whose `+0x20` count is cleared in Ghidra. Entry/exit snapshots can measure that field, subject to pointer lifetime. |
| `queue_append_inner_candidate` | `0x00ac0d70` | `0x006c0d70` | ECX-relative object, one stack argument; Ghidra reads `+0x20`, appends a value and increments the count. Other callers exist. |

The functions are expected to be sparse in a menu; replay ingestion can be bursty.
For each run, preserve the actual runtime addresses from `identity_verified`,
configuration, replay hash and source offset, timing, and limitations. Only map
replay frame/slot/offset to a runtime request after a reproducible identity or
content match. An order can resolve to multiple actors and each actor can receive
a different order. A post-grouping call is not proof of execution or state change.
