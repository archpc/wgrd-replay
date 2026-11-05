# Revision 131544: frame, tick and battle-clock capture (bounded runtime)

Status: one authorized bounded playback, read-only instrumentation, no binary
patches. Evidence is private; no trace bytes in Git.

## Authorization and scope

User-authorized single bounded session: hooks at `0xb34060` (containing the
requested `0xb34758`/`0xb349bd` frame advance), `0xaaedf0` (clock reader) and
`0xab4780` (phase store); existing replay and tooling; graceful VM shutdown
verified afterwards. No gameplay modification, no unrelated RE.

Instruction-level hooks at `0xb34758`/`0xb349bd` cannot read the frame index:
the manager is in `EBX` there and the read model exposes only `ECX`/`EDX`/args.
The containing step `0xb34060` is `__thiscall` with the manager in `ECX`, so the
three sites requested are covered by one entry hook plus a leave read of the
saved entry pointer (the controller re-reads through the entry-time `ECX`, not
the clobbered register).

## Inputs and identity

| item | value |
|---|---|
| executable | `WarGame3.exe` `5eaa6d61…f09efc75d`, revision 131544 |
| replay | `replay_2026-11-01_19-10-26.wargamerpl2`, `abf6a5e9…9da121` |
| trace | `run-01.jsonl`, 22,467,374 B, SHA-256 `b3a60af42665bb15936befa720a5719121323b6fc63ef61ffd185ee3c2934ee0` |
| capture sources | `hooks.js` `f398ffa3…`, `wgrd_frida.py` `3d3cb502…`, `frameclock-131544.json` `c9bc952d…`, `WgrdUi.cs` `624cdc82…` |
| window | start `22:38:23.720Z`, end `22:46:25.564Z` (481.8 s), `--seconds 480 --event-limit 60000` |
| guest | Windows 10.0.26300, Frida 17.24.3 in the existing user venv |

Termination is clean: `summary` (10966 tick_step calls, 9539 clock invocations,
0 phase_store), `detached` reason `application-requested`, `end`
`cleanup_errors: 0`. Limitations recorded by the trace: one `enter` without a
matching `leave` at the cut, and `outstanding_threads: 1`.

UI navigation used the maintained `WgrdUi.cs` (`WindowState`, `ClickClient`,
`CaptureOnly`) after confirming the client rect is `3008x1482`. The older guest
helper was replaced with the maintained copy, hash-verified before use.

## Result 1: the frame counter resets to 0 when the replay starts

At `22:38:42.856Z` the manager's `+0x6c` goes `2664 -> 0` and the
replay-mode byte `+0xa5` goes `0 -> 1`. Before that instant the same object
serves the outgame session and carries a non-zero frame counter; a non-zero
frame index therefore does not imply an active replay.

## Result 2: one frame per 0.2 s tick, no skips

Over the replay segment (frame 0 at `22:38:42.856Z` to frame 2311 at
`22:46:25.504Z`, 462.65 s):

- 2389 tick advances; every enter→leave delta is `0` (8576 calls that ran
  without advancing) or `+1` (2389 advances). No frame was skipped, repeated or
  advanced by more than one.
- 2311 frames in 462.65 s = **4.995 frames/s**, i.e. 5 Hz at 0.2 s per frame,
  matching the static `0x195d768` quantum.

## Result 3: deterministic ticks advance 1:1 with frames, integer difference 10 or 11

95 clock samples after the reset, spanning ticks 13 to 2293, each joined to the
most recent frame advance (samples land 0.002–0.005 s after it):

- `frame - tick` is **10** for 48 samples and **11** for 47 samples, with no
  drift over 462 s. Only these two integers occur; nothing observed both
  counters advancing at the same instant, so the exact synchronization boundary
  is unresolved.
- The 10.5-frame midpoint (2.1 s) is a sample statistic, not an observed
  boundary. It is carried only as a labelled estimate with per-event bounds
  `(frame - 11) .. (frame - 10)`.
- The clock value is `[TGameplayServices+0xd0]`; `0xaaedf0` scales it by 0.2.
  So the deterministic clock is not the frame index, and frame 0 is not
  deterministic time 0.

## Result 4: total-duration agreement, not clock identity

The replay HUD showed `00:00:00 - 00:13:53` at speed 1.00x. The file has 4174
frames (0..4173): `4174 × 0.2 = 834.8 s`, and `(4174 − 11..10) × 0.2` =
832.6..832.8 s, which also displays as 13:53.

That is a consistency check on the same 0.2 s grid, not proof that the HUD
timeline and `[TGameplayServices+0xd0]` are the same clock: the HUD value was
read from a screenshot, not from the engine, and no sample pairs a HUD tick with
a counter value. Two clocks on the same grid with a fixed offset produce the
same total.

Verified battle time therefore stays **null**. The export carries only

```
estimated_deterministic_time_seconds = (frame - 10.5) * 0.2
bounds                              = [(frame - 11) * 0.2, (frame - 10) * 0.2]
```

with provenance `single_capture_statistic`. No universal offset is applied to
other replays; each replay would need its own observation.

## Result 5: the phase hook did not fire in this window

`0xab4780` produced **0** calls in 481.8 s, including the whole load sequence
and 462 s of playback. A later session saw it fire once during replay
(`0x2`, tick 2905); see the
[combat frame attempt](2026-11-03-combat-frame-capture-attempt.md). "Never
called" was too strong. It is not the deployment→battle transition path for a
replay, or it is not reached in this window. The previously retained single
observation with argument `0x2` remains a single sample; battle start is still
unresolved and no phase timeline is claimed.

## Corrections to earlier notes

- **H4 corrected.** The earlier arithmetic check that put the 830.8 s impact on
  frame 4154 assumed `t = frame × 0.2`. With the measured offset the impact at
  830.8 s is frame ≈ 4165, not 4154. The "same grid value" note in the frame
  consumption document is withdrawn as a coincidence of the naive formula.
- **H1 restated.** The rate claim (one frame per 0.2 s tick) is observed. The
  frame→tick difference is observed only as the integers 10 and 11; the exact
  boundary is unresolved and no midpoint is promoted to a mapping.
- **H2 unchanged.** Opcode `0x13` is still not battle start; nothing in this
  capture tests it.

## What this does not establish

- Battle start, deployment length or any phase boundary (no phase observation).
- AAR event placement: no damage hook ran in this window. Placing impact
  seconds on frames needs a capture that carries both hooks; the estimated
  offset alone is insufficient and its bounds must be carried.
- Whether the 2.1 s offset is constant across replays, speeds or machines. One
  replay, one speed.
- Unit lifetimes or movement: not instrumented here.

## Smallest next experiment

One playback with the existing runtime-v3 hook set plus this `tick_step` hook,
so impact/destroy records carry a frame index directly instead of a derived
one. That closes AAR placement and unit-lifetime timing without new tooling.

## Reproduction

Capture config: `instrumentation/frameclock-131544.json`. Command (guest):

```text
python.exe wgrd_frida.py --config frameclock-131544.json \
  --output frameclock-01.jsonl --pid PID --seconds 480 --event-limit 60000
```

Analysis is a read-only join of `tick_step` enter/leave reads
(`ecx+0x68`, `ecx+0x6c`, `ecx+0xa0`, `ecx+0xa4`, `ecx+0xa5`) with
`clock_tick_sample` (`ecx+0xd0`). Private artifact:
`~/.hermes/artifacts/wgrd-replay/frameclock-20261102/` with `SHA256SUMS`.
