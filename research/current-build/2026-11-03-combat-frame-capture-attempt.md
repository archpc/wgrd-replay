# Revision 131544: attempted frame-indexed combat capture (bounded session)

Status: **incomplete experiment**. The instrumentation and offline join are
implemented and tested, but **no combat event was captured with a frame index**.
This note records what the session actually produced, why it stopped short, and
the smallest next step. It does not claim a battle timeline.

## Scope

One authorized read-only session: existing runtime-v3 hooks plus the validated
`tick_step` hook (`0xb34060`), same replay, no binary patching, no new UI code.
UI navigation used the maintained `WgrdUi.cs` with the client rect verified at
`3008x1482`.

## What was built

- `instrumentation/aar-capture-131544-v4.json`: the ten v3 hooks plus
  `tick_step`; eleven hooks, config SHA-256 `ab7810a2…5752de1`.
- `aar_events.py` profile `runtime-v4`: same extraction as v3, plus a tick-frame
  join. Each event gets `time.frame_correlation` with `frame_low`, `frame_high`,
  `bracket_before_seconds`, `bracket_after_seconds`, `status`, and
  `estimated_deterministic_seconds_bounds`. Statuses are
  `inside_tick_call`, `bracketed`, `wide_bracket`, `unbracketed`,
  `no_line_reference`, `line_out_of_range`.
- A join is called exact only inside a tick call or between two calls closer
  than 1.0 s; anything wider stays a bracket. No nearest-timestamp substitution.
- The naive `replay_frame_hypothesis` is marked
  `superseded_by_tick_frame_correlation` when a tick hook is present.
- `combat_frames.json` is written beside the usual four outputs.
- Five focused tests for the join mechanics; the AAR module now runs 43 tests.

## What the session captured

| run | replay frames observed | tick calls | impacts | phase calls | outcome |
|---|---|---|---|---|---|
| 01 | 0 – 1486 | 5554 | 0 | 0 | complete, window ended early |
| 03 | 0 – 3297 | 4007 | 0 | 2 (enter+leave) | complete |
| 05 | 4175 idle, then 16 – 73 | 2654 | 0 | 0 | complete; attached to a finished replay |
| 06 | 262 – 317 | 203 | 0 | 0 | failed: target detached before completion |

Hashes are in `SHA256SUMS` and `manifest.json` beside this note's artifact
directory. Run 02 was a failed attach (`loaded entry mismatch`) after an
interrupted run left patched bytes; the process was restarted and re-verified
before further capture.

### Why combat was not reached

The retained AAR trace places its 28 impacts at engine deterministic seconds
806.4–831.0. On the observed 0.2 s grid with the measured 10–11 frame lag, that
is replay frames ≈ 4042–4165 of 4174. A capture window that starts at frame 0
must therefore run to the end of a 13:53 replay.

Requesting 5x–7x playback produced an effective ~2.75x (wall rate), so a 240 s
window covered only 3297 frames. No seek to the end of the timeline was
performed, and run 05 attached after the replay had already finished. That is
the whole reason there are zero combat callbacks: **the combat frames were never
executed inside a capture window**, not a hook that failed to fire.

### One new positive observation

`0xab4780` did fire once, during run 03 at `23:07:50.221Z`, with argument `0x2`,
`[TS+0xd0] = 2905`, and `[TS+0x20] = 1` (`game_started`). The leave record shows
the same tick. This contradicts the earlier "never called" statement, which was
true only for that earlier window: the phase hook is reachable during replay.
One event is not a phase timeline, and the deployment→battle boundary is still
unidentified.

## What this does not establish

- No combat event has an observed frame. The join implementation is tested on
  synthetic rows only; it has not yet been exercised on a real impact.
- Whether the tick-frame join holds at high playback speed. Run 03 shows the
  engine advancing 5 frames/s of simulation while wall time ran ~2.75x faster;
  the frame index per tick stayed `+1`, but a speed where the engine skips
  frames was not observed or ruled out.
- Anything about battle start. The single phase event has no named meaning.

## Smallest next experiment

Seek the replay to ~96% of its timeline before attaching, then capture 120 s at
1x: that window covers frames ≈ 4000–4174, which is where every retained impact
sits. If seeking is unavailable, leave the replay running and attach only after
`tick_step` reports frame > 3950 (a cheap read of the same hook). Either path
needs no new hook, no new profile and no UI work beyond one drag on the existing
progress bar.

A capture that spans the end must also record whether the frame index parks at
4175 after the last frame; run 05 observed that idle value and it is unexplained.

## Evidence

Artifact: `~/.hermes/artifacts/wgrd-replay/combat-frames-20261103/` with
`run0*.jsonl`, `SHA256SUMS`, `manifest.json`. Guest and host trace hashes were
compared per run. VM stopped gracefully afterwards; `prlctl` reported `stopped`
and no `prl_vm_app` process remained.
