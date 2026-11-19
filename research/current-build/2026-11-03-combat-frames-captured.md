# Revision 131544: frame-indexed combat events (bounded capture)

Status: **captured and validated offline**. Every retained combat callback now
carries a bounded replay frame from an observed tick call. This is the combat
placement that the earlier attempt could not reach; it is still not a complete
battle timeline (see "Not established").

## Session

One authorized read-only playback: the ten runtime-v3 hooks plus `tick_step`
(`0xb34060`), replay `abf6a5e9…9da121`, no binary patches, no new UI code.
Existing capture-era controller pair reused unchanged; UI via the maintained
`WgrdUi.cs` after confirming the client rect at `3008x1482`.

| item | value |
|---|---|
| trace | `run-07.jsonl`, 32,029,839 B, SHA-256 `acb8ecdc9f264c2784590180e1b316822a3ade6db13cd3c4969c9046f90d6f21` |
| config | `aar-capture-131544-v4.json`, `ab7810a2…5752de1` (11 hooks) |
| window | 600 s, playback raised to 5.00x; whole replay executed (frames 0–4175) |
| termination | `summary`, `detached` `application-requested`, `end` `cleanup_errors: 0` |
| hashes | guest and host trace SHA-256 equal |

The one caveat in `summary` is `outstanding_threads: 1`. It is exactly one
`tick_step` enter (11780 vs 11779) whose leave never arrived at detach. Every
event hook is fully paired: impacts 28/28, checks 28/28, destroys 6/6, orders
5/5, phase 1/1. The exporter checks that pairing per hook and refuses any
unpaired call outside the tick hook, so the allowance cannot hide an event loss.

## Result: all 28 impacts landed inside a tick call

`frame_correlation.status_counts` is `{"inside_tick_call": 28}`: every event
line falls between a tick hook's entry and its leave, so `bracket_before` and
`bracket_after` are both `0.0` and no nearest-timestamp matching was used. The
frame span inside such a call is one frame, which is reported as
`frame_low` / `frame_high` rather than collapsed.

| measure | value |
|---|---|
| first impacts | frames 4042–4043, engine seconds 806.4 |
| last impacts | frames 4165–4166, engine seconds 831.0 |
| destruction checks | 28, same frames as their impacts |
| lifecycle destroys | handles 33, 31, 39 at frames 4042, 4043, 4164 |
| order requests | 5 |
| phase store | 1, frames 2915–2916 |

Cross-check that the join is not an artefact: each event keeps its independently
captured engine deterministic seconds, and those values sit inside the bounds
derived from the frame (`(frame−11)…(frame−10) × 0.2`). For example 806.4 lies in
[806.2, 806.6] and 831.0 in [830.8, 831.2]. The frame join and the engine clock
agree for all 28 events without being fitted to each other.

The lifecycle destroys also reproduce the retained AAR: same three handles in the
same order (33, 31, 39), return address `0xc9c0ce`, argument `0x1`.

## Instrumentation changes

- `runtime-v4` profile = v3 + `tick_step`, schema `wgrd-aar-runtime-v4/1`.
- Tick-frame join per event: `status`, `frame_low`, `frame_high`,
  `bracket_before_seconds`, `bracket_after_seconds`, `tick_call_id`,
  `estimated_deterministic_seconds_bounds`. Exact only inside a tick call or
  between calls under 1.0 s; otherwise `wide_bracket` / `unbracketed`.
- `combat_frames.json` written beside the usual outputs.
- The naive `replay_frame_hypothesis` is marked superseded in v4 output.
- Pairing policy: one unpaired tick enter is allowed and reported; any unpaired
  event hook still fails the export.
- Anchor reads that succeed without a raw pointer now record
  `position_read_failed`/`no_raw_pointer` instead of raising. The retained v3
  trace never hit that branch, so v3 output is unchanged (its digests still pass).

## Not established

- A single frame per event. The callback lies inside a tick that advances the
  frame, so the honest answer is the pair (`4042–4043`), not one integer.
- Which combat step inside the tick ran first. Tick entry precedes the callback,
  but intra-tick ordering is not observed.
- Battle start, phase meaning, unit lifetimes or movement. The phase event has
  one sample and no named meaning; positions were captured but produced zero
  anchor changes at this playback rate.
- Whether the join survives a playback speed where the engine skips frames. This
  run advanced +1 frame per tick at an effective ~2.75x wall rate; a skipping
  regime was not observed or ruled out.

## Reproduction

```sh
python3.14 -B instrumentation/aar_events.py <run-07.jsonl> --profile runtime-v4 \
  --unit-index <unit-index-131544.json> \
  --expect-sha256 acb8ecdc9f264c2784590180e1b316822a3ade6db13cd3c4969c9046f90d6f21 \
  --out <dir>
```

`tests/test_aar_events.py::CombatFrameCaptureTests` pins the same trace when it
is present locally (skipped otherwise): 28 impacts all `inside_tick_call`, first
frame 4042, last 4165, engine seconds inside the derived bounds, three lifecycle
destroys at 4042/4043/4164.

Artifact: `~/.hermes/artifacts/wgrd-replay/combat-frames-20261103/run07/` with
the trace, `capture-sources/`, the export and `SHA256SUMS`. VM stopped
gracefully; `prlctl` reported `stopped`.
