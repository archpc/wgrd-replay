# WGRD Frida tracing

## Experimental Gate 1/2 capture, not ready for playback

`wgrd_frida.py --gate-replay REPLAY --output OUTPUT` selects a fixed revision-131544
hook set and verifies the exact controlled replay SHA-256 before attaching. It
uses the existing repository parser and timeline modules, which must be present
beside the instrumentation directory. It refuses `--hook` subsets. This mode is
fixture-tested only: **do not use it for a playback yet**. The complete actor
identity-chain validator and queue allocation-lifetime witness are missing.
An identical address or readable memory does not prove the same allocation.
The emitted queue snapshot explicitly says `lifetime: unverified`.

Root matching is scoped to the exact reference, request bytes and runtime actor
count, with per-thread correlation. Other threads and unmatched roots do not
emit events. Queue snapshots are retained on the parent replace call and read
before the clear and at parent return; each read is bounded, counts over 32 fail
closed, and storage is re-read after possible reallocation. Snapshot content
comparison is conditional, not a Gate 1/2 result. The inspector can report
content `pass`/`fail`/`inconclusive` only for that comparison; both complete gate
results remain inconclusive without identity and lifetime validation. A completed
trace is not evidence that the target process loaded the supplied replay.

Run offline fixtures without game execution or Frida attachment:

```text
python3.14 -B -m unittest discover -s tests -p 'test_gate_request.py' -v
python3.14 -B -m unittest discover -s tests -p 'test_frida_inspect.py' -v
```

Do not copy runtime data, raw traces or replay bytes into Git. Any future guest
execution, Frida attachment or replay requires separate authorization.

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

## Scoped AAR capture candidate (2026-11-02)

`aar-capture-131544-v2.json` is an offline-validated experiment configuration,
not yet an engine-validated capture. It retains the pinned image and impact,
threshold and lifecycle targets, captures owner lookup return headers and the
candidate descriptor at return-object+0x28, and captures clock getter calls only
inside selected roots. `frame_apply_candidate` at `0xb2b310` records two raw
arguments; the caller at `0xb3dccd` passes the decoded frame and command object.
The relationship between a runtime counter and replay frame remains unresolved.

The first expanded capture had 28 impact calls, 28 threshold checks and six
owner/lifecycle calls, with no suppressed events or callback/stack errors. It did
not capture the target descriptor bytes. V2 adds the missing read without tracing
hundreds of thousands of unrelated owner/clock calls. An owner header's +0x04 is
not treated as a descriptor pointer; that experimental read is replaced by the
+0x28 candidate, still requiring runtime/type validation.

`test_frida_scope.py` and its Node callback simulation validate admission,
thread/stack scoping, filtered counts and bounded return-value reads. The staged
controller/hooks were separately exported and tested without the pre-existing
uncommitted request-gate work, so this capture support does not depend on that
unfinished work. Simulated hooks are mechanics tests, not live engine evidence.

## Damage-event publish capture (2026-11-01)

`damage-publish-131544.json` selects two hooks against the same pinned executable
(SHA-256 `5eaa6d61...f09efc75d`, Ghidra base `0x400000`). Evidence: REA/Ghidra
12.1.4 read-only existing-project session on the hash-pinned image; addresses are
Ghidra VAs valid only for that revision.

- `take_damage_publish` `0x00c4cba0` — IA message publish helper. Thiscall: ECX is
  a queue/container object; arg0 points to a caller-constructed message. It copies
  seven words from arg0 (+4, +8, +0xc, +0x10, +0x14, +0x18, +0x1c) into a new
  heap `TIAMessage` and appends it. The 32-byte read at arg0+0 is bounded raw
  message data, INCLUDING the base `TIAMessage` vftable word; no field beyond the
  vftables is claimed as decoded.
- `damage_dispatch_entry` `0x00c95040` — damage-application loop. ECX-relative
  owner object; iterates damage entries at owner+0x15c, stride 0x74, count at
  owner+0x164. On damage and on kill it builds messages on its stack and calls
  `0xc4cba0`. No reads are configured; the hook records call timing and nesting
  only.

Message identity, byte-aligned to observed constructor stores in `0xc95040`
(evidence `ev_b4c8b9d2`, `ev_97203167`):

- Base `Eugen::IA::TIAMessage` vftable at message+0 (`0x1998940` in .rdata).
- `Eugen::IA::TIATakeDamageMessage` vftable at message+8 (`0x199bcc0`; RTTI COL
  `0x1b93e54`, type descriptor `0x1ea4368`).
- Publisher copies arg0+4 to the heap object's singleton-word slot and arg0+8,
  +0xc, +0x10, +0x14, +0x18, +0x1c to consecutive heap fields. In the sender's
  stack message, the observed stores are: +0x0c amount (float, written only when
  the pre-computed value passes a >0 guard), +0x10 damage type (observed stores
  1, 2, 3; meaning unverified), +0x14 target unit id, +0x18 shooter-side id
  (defaults 0x17 when a lookup fails), +0x1c unverified. These are candidate
  field positions from one call site; treat every field except the vftable words
  as unknown until a runtime capture correlates values with visible game state.
- Kill composition (separate message, not `TIATakeDamageMessage`) carries typed
  tokens `Killed`, `DamagesType`, `Damages`, `Target`, `TargetTeamNumber`,
  `ShooterTeamNumber`; token-constructor vftables `0x19998d4` (Killed),
  `0x19998bc` (Target), `0x19998c8` (TargetTeamNumber), `0x19b5bb4`
  (ShooterTeamNumber), `0x19b5bc0` (Damages), `0x19ae374` (DamagesType), built
  at `0xc9535d`..`0xc954f9` and published through the same `0xc4cba0` chokepoint.
  Its heap layout is NOT captured by the arg0+0..32 read and is unverified.

Interpretation limits: ECX (the queue/container) is not dereferenced. Amount,
type, and id fields are inferred from instruction-level stores at one call site
in `0xc95040`; other publishers of `0xc4cba0` may write different message types
(`TIAKillGameplayMessage` singleton accessor `0xad5320`, `TIATakeDamageMessage`
accessor `0xad5940`). The vftable word at arg0+0 is the only reliable
message-type discriminator in this capture; classify every event by that word
before quoting any field.

Run the same controller with `--config instrumentation/damage-publish-131544.json`
instead of `--gate-replay`; no gate root is used. Expect sparse events in menus
and bursts during combat. Unknown fields stay null; do not apply the
`TIATakeDamageMessage` offsets to messages whose vftable word differs.
