# Approach assessment: replay decoding, consumer modeling, or engine re-execution (2026-10-29)

**Assessment only.** Nothing was executed, no VM or game was operated, and no
decoder code changed. This note does not change [NEXT-STEPS.md](../../NEXT-STEPS.md)
until the owner adopts it. Inputs were the repository at `102b1b9` and the notes
linked below. Every figure is as recorded in those notes, not re-measured here.

## Question

Is replay-only decoding approaching diminishing returns? Would one of these give
better leverage:

1. continued interpretation of serialized commands;
2. reverse-engineered models of command consumers, entity resolution and world-state
   transitions;
3. emulation or reimplementation of enough engine behavior to reconstruct outcomes?

## Findings that decide it

- **Framing is closed.** 594/594 multi-command blocks are split, and every
  non-empty block is complete or framed ([archived priorities](../NEXT-STEPS-2026-10-28.md)).
  Three new cross-build files parsed with zero unresolved spans and needed no layout
  change ([controlled experiment](2026-10-28-controlled-experiment.md)).
- **The dominant semantic gap is runtime-bound.** In the matching-59638 samples,
  8,578 of 10,375 `0x07` orders use contextual kind 39 ([OP07-ORDERS](../OP07-ORDERS.md)).
  Inside the `c9a140` fallback, the effective kind depends on the module at registry
  `+108`, that module's `+28` state, per-member `0x10` flags, and earlier `c972a0`
  path results. `0x07` serializes none of them ([ENTITY-CONTEXT](../ENTITY-CONTEXT.md)).
- **Replays are input streams.** `TNetworkEventSourceFromReplay` RTTI and the
  command-only framing are consistent with lockstep re-execution
  ([REA notes](../../REA-NOTES-59638.md)). Positions, damage, destruction and resolved
  orders cannot be decoded from the file. They can only be observed while a
  matching engine re-executes it.
- **Execution is no longer the blocker.** Revision 131544 records and plays back in
  the ARM64 Parallels guest, and guest GDI capture works. x86 CDB is installed but
  has not been attached ([controlled experiment](2026-10-28-controlled-experiment.md)).
- **The guest may also run 59638.** The 2026-10-26 probe found
  `Data\PC\59638\WarGame3.exe` with SHA-256 `1c7533eb…bda46`, which is the executable
  behind all static analysis here. It also found data builds 48574 through 131544,
  including `Data\WARGAME\PC\59638\NDF_Win.dat`
  ([prerequisites](../GROUND-TRUTH-PREREQUISITES.md)). The asset shortfall in
  [RUNTIME59638-FEASIBILITY](../RUNTIME59638-FEASIBILITY.md) describes the Mac cache,
  not this guest. Launching that executable directly was not attempted on 2026-10-28.
  Whether it starts, which data it loads, and whether it plays Samples 1 and 3 are
  all **untested**.

## Assessment

| | 1. Serialized commands | 2. Static consumer models | 3. Emulate / reimplement |
|---|---|---|---|
| Feasibility | High | Medium per function; low for the whole order chain | Reimplementation: none. Selective emulation (e.g. Unicorn on extracted functions): possible, but no live state to feed it |
| Executable evidence | Framing complete; 59638 traces for `07/08/0d/18` | `c972a0` → `b32690` → `abd410` → `af9f60`; `c9a140` fallback table; `da4d20` getter; `TPositionModule`/`TWorldUpdater`/`TDamageModule` RTTI | Same leads; tick, position writer, damage and lifecycle untraced |
| Dependencies | None new | 59638 only; assembly-level (Ghidra import timed out); no oracle | Bit-exact lockstep: pathing, LOS, ballistics, RNG, terrain, NDF, maps |
| Research value | Low for outcomes; moderate for tooling and residual fields (`0x0C`, `0x0A` correlation, `0x0B`, marker types) | Conditional kind-39 labels at best; never effective kinds | Highest in principle; unlikely to be realized |
| Cost | Days | Weeks per subsystem; risk of confident, unvalidated models | Person-years; divergence compounds across thousands of frames |

**Ceiling of approach 2.** Combining a static model with NDF capabilities could rule
out branches by unit type (for example, actors with no airplane-type module never
reaching 32/33). It cannot select a branch, because module state and member flags
change during play. The registry `+108` → `TAirplaneModule` link also remains
unproven.

**Ceiling of approach 3's selective variant.** It needs the world state the replay
omits. A live, re-executing game process already holds that state.

## Recommendation: engine as oracle

Treat original playback as the re-executor. Use passive logging breakpoints to
record engine-resolved values. Restrict static analysis to locating hook points.
Logging breakpoints add delay but, under the lockstep inference above, should not
change results. That remains a **hypothesis**, which the second gate below tests.

Each gate needs separate authorization. Stop at the first failed gate.

0. **59638 launch probe (cheapest, decides porting).** Launch the pinned
   `Data\PC\59638\WarGame3.exe` in the guest offline. Record the process image hash
   and loaded modules, and attempt Sample 1. Pass: Sample 1 plays and reaches its
   known anchors (frame-131 marker text, frame-1050 explicit Move). Fail: record the
   concrete error. No DRM, renderer or loader workaround.
1. **Debugger probe.** Attach x86 CDB to replay-mode playback under ARM64
   emulation and hit one software logging breakpoint. Run it twice and compare
   results. Hardware data breakpoints under emulation are unverified, so treat them
   as optional. If attach fails, move to native x86 Windows rather than expanding
   static RE.
2. **Effective-order capture (highest value per cost).** At the post-grouping
   submission (`b33c5f` → `abd410`, concrete kind into typed-input field `0x48`), log
   the concrete kind, actor handle and frame. Pass: identical logs across two
   playbacks, with explicit requests reproducing their decoded kinds. Output becomes
   a new **engine-observed** tier in the timeline, kept separate from verified
   request decoding and from inference. Use it also as a live differential test of
   decoder command order.
3. **Position observation (time-boxed, about one week).** Use the `c7e3c8`/`da4d26`
   accessor described in [RUNTIME59638-FEASIBILITY](../RUNTIME59638-FEASIBILITY.md).
   Exit if no stored vector tracks at least three known Move targets, and do not
   start damage or destruction work.

If gate 0 fails but 131544 playback still works, port gates 2 and 3 to 131544
through rebuild-stable anchors: the `OrderType` reflection table, `TPositionModule`
RTTI and constructor, and the `abd410` field shape. Label the results 131544-only
until a controlled recording corroborates them. Controlled 131544 recordings are
unlimited, which offsets the smaller historical corpus.

Separately, test whether 131544 plays a 510061340 or 510064564 archive replay.
Finish any remaining archive acquisition before the source's announced 2026-11-25
shutdown.

**Continue from approach 1:** request filters, reference history and summaries
(NEXT-STEPS item 2), plus the small residual field traces.

**Continue from Phase 2, reduced:** one visual timing and movement recording as
independent validation of hook output. Hooked tick and clock reads should replace
screenshot timing for calibration, but they should not be the only check on
themselves.

**Do not:** reimplement or emulate the simulation; start static world-loop, damage
or destruction RE before gate 2 passes; or extend 59638-only static modeling of
kind 39.

## Principal risks

- Debugger behavior for x86 processes under ARM64 emulation. Gate 1 settles this
  cheaply.
- Old-executable data precedence or Steam-launch requirements. Gate 0 settles this.
- Cross-build porting errors if gate 0 fails. Mitigate with stable anchors and a
  controlled recording.
- Instrumentation changing timing-sensitive behavior. Gate 2 compares two playbacks
  to catch it.
