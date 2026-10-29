# Frida replay traces: revision 131544, 2026-10-29

## Scope and identity

Two user-operated playbacks of the same controlled Death Row recording were
observed in the existing Windows 11 ARM Parallels guest. No new recording, game
launch, security change or network change was performed. The game was already
running. The interpreter was the existing Frida 17.24.3 Python environment.

- Executable: PE32/x86, embedded revision 131544, SHA-256
  `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
- Explicit loaded module: `wargame3.exe`, observed base `0x00400000` in both
  runs. Controller compared the selected entry bytes with the hashed on-disk
  image. This is not a hash of all loaded memory.
- The guest replay hash matched before the first run and after the second.
- Original JSONL traces and their hashes are private. Guest-to-host copy hashes
  matched. The files contain process addresses and raw data and are not in Git.

Both scripts reported successful programmatic detachment. The first trace ended
at 15:21:19 UTC; the second ended at 15:37:01 UTC. Their absolute hook windows and
captured auxiliary activity differ. The first had 170 dispatcher entries versus
172 in the second. This alone does not establish a replay divergence or its cause.
Second-run summary:
4,870 enter/leave events; zero suppressed events, callback errors, stale frames,
stack mismatches, outstanding threads or cleanup errors. The offline inspector
found no unmatched calls or correlation issues. This checks the instrumented
call-stack bookkeeping, not completeness of unhooked functions or gameplay
semantics. The game process remained responsive after detachment.

## Bounded observations

The first trace recorded 1,784 calls to `0x00b3dbc0`. They occurred within
approximately 0.219 seconds at replay load. The number equals this replay's
1,784 frames, but neither equality nor temporal proximity proves a particular
call-to-frame mapping. The second run also recorded 1,784 calls.

In both runs, a single `0x00b2be30` invocation contained the exact 20-byte
single-actor reference and exact 36-byte request structure of the decoded
opcode-0x07 command at frame 1352, recorded slot 0, file offset 112616. This is
one exact match among the opcode-0x07 candidates in the supplied recording.
The trace did not capture the wrapper's original actor count; matching the
reference prefix cannot establish that its entire runtime actor array had one
entry. It is a sample-specific content correlation, not a captured runtime frame
counter or proof of an executed order. The matching utility preserves multiple
candidate locations if bytes recur. The matching dispatcher and grouping calls
were ordinal 156 in each run. The first-ingest-to-wrapper wall-clock intervals
were 271.128 and 273.247 seconds; these are not simulation-clock measurements.

In the second run, the wrapper invocation had one observed same-thread nested
`0x00b31830` dispatcher, which nested `0x00c96440` grouping, `0x00abc100`, and
`0x00abb3b0` in that order. The grouping function's return-time snapshot had one
nonempty 20-byte group record at index 4, with count 1. The nested `0x00abb3b0`
entry had an input vector count 1, first captured handle `0x0000006e`, and a
raw second-argument pointer value `0x00010000`. The pointed-to word was not
captured, so this is not an observed gameplay order. No state mutation or
movement outcome was captured for this request.

**Actor identity gap:** the trace did not dereference the dispatcher's input
actor vector or the group record's member storage. Therefore the queue handle
`0x6e` is not directly connected to the replay's 20-byte actor reference. One
input and one group member do not prove identity. Pointers are process-lifetime
observations and may be reused. Nearest-hook nesting is not proof of data flow.

Static Ghidra analysis of this exact executable provides a follow-up route:
`0x00b2be30` calls `0x00b2d210` for object+0x60 and object+4; `0x00b30fd0`
passes converted lists to `0x00b31410`, which looks up input values and copies
resolved object+0x20 into a list passed through `0x00b31620` to `0x00b31830`.
These observations are not a runtime capture of the missing values. Relevant
REA evidence: `ev_caadc737b2e707a2e169b044ccd3375c11d5b47201dc3fca6da0e313cfe47801`,
`ev_3cd748e1924e6fab6a77abef5094709454778a38515ddb13772245ab1731b6fa`,
`ev_7eee5383132281630636c6419c98b94d753225fa54b08f590ad932f11eaa27ff`,
`ev_91049cd4a41605049dc8435c148298ad3dd26e1df34d95922c60088da9947940`,
and `ev_a67685d84d8766027b8a6d969e9a3c1ed2c75752656d8f061af13d5cdbe21460`.
Ghidra used an existing-project private copy whose original analysis
completeness is unknown.

## Submission-coverage question

Among 172 second-run `0x00b31830` dispatcher entries, all had a nested observed
`0x00c96440` entry. Their observed descendants classified as follows:

| Nested hooks under dispatcher | Calls |
|---|---:|
| grouping, `0x00abc100`, `0x00abb3b0` | 96 |
| grouping, `0x00abc100`, `0x00b36d10` | 38 |
| grouping, `0x00abb3b0` | 34 |
| grouping, `0x00b36d10` | 4 |

All these hooks used sample rate 1; the trace reports no dropped events or stack
mismatches. Thus, within this recording and trace interval, the replace helper
`0x00abb3b0` alone did not observe the 42 dispatcher calls whose observed nested
queue helper was `0x00b36d10`. Similarly, `0x00abc100` was not nested in 38
observed dispatcher calls. This does **not** identify a different proposed
submission point as universal, prove queue mutations, or establish coverage of
all order types. The single matched replay request followed the replace path.
Other dispatcher invocations are not automatically attributed to the replay
command or player.

## Reproduction and limits

Run the focused inspector against the preserved trace and original replay:

```sh
python3 -B instrumentation/trace_inspect.py \
  "$HOME/.hermes/artifacts/wgrd-replay/frida-traces/replay-02.private.jsonl" \
  --replay "$HOME/.hermes/artifacts/wgrd-replay/current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2"
```

The inspector strictly parses the supplied replay and checks its embedded digest.
The private `analyze_order_run.py` beside the traces computes the descendant
pattern table and grouping snapshot; it does not assert actor identity.

A targeted follow-up would capture the single-actor reference as it enters
`0x00b2d210`, the resolved object and its relevant fields, the first element of
the dispatcher's input vector, the member of group index 4, and the first value
of the replace vector in one correlated invocation. Every dereference must be
bounded and checked; an address match across separate runs is not enough.
Recording queue-object fields at entry and return would separately test a
specific state change. No follow-up playback was started during this analysis.

The 99-file archived corpus census contains no literal replay Version `131544`.
Historical recordings can supply varied hypotheses, but playback on this
executable and cross-version semantic equivalence are not established.

Measured menu CPU samples, five seconds each, were approximately 0.374 and
0.586 CPU seconds per wall second before and with hooks. They were single,
unmatched observations, not a controlled overhead measurement. Replay timing,
frame fidelity and game outcomes were not compared against an uninstrumented
control.
