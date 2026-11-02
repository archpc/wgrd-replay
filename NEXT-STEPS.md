# Current status and next steps

Target: a complete, reproducible after-action report (AAR) for revision 131544
(SHA-256 `5eaa6d61…f09efc75d`), produced by the original engine replaying a
recording.

The replay file contains only inputs. The decoder (`wgrd_replay.py`) recovers
the player's commands. Combat outcomes exist only when the engine re-executes
them. Playback is deterministic at the observed boundary: two captures with
different hook sets produced the same 28 impacts.

## Canonical AAR workflow

1. Run an authorized playback with `instrumentation/wgrd_frida.py`,
   `hooks.js` and `aar-capture-131544-v3.json` (see
   [instrumentation](instrumentation/README.md)).
2. Run `instrumentation/aar_events.py` (one exporter) on the hash-pinned trace
   to get events, units, destruction chains and chronology.
3. Use `wgrd_replay.py --timeline` on the same replay for the player's commands.

Ghidra 12.1.4, through the canonical REA CLI on a disposable project copy, is
the structural authority. The recipe is in the
[causal chain note](research/current-build/2026-11-02-causal-chain.md).

## Causal chain coverage

| Link | Status | Evidence |
|---|---|---|
| Impact record → queued damage entry (producer) | static | [causal chain](research/current-build/2026-11-02-causal-chain.md) |
| Entry → apply: source, target, amount, mode | observed + static | [runtime AAR](research/current-build/2026-11-02-runtime-aar.md) |
| Source owner = engine-credited attacker (XP credit) | static | causal chain §2 |
| Target/source unit types | observed + static index join | [unit data](research/current-build/2026-11-02-unit-data.md) |
| Threshold → `Killed` composition and owner destroy | observed (AL, nested destroy) + static | causal chain §3 |
| `TIAKillGameplayMessage` | lifecycle only, not kill credit | causal chain §4 |
| Kill table / kill points (debrief) | **open**: data source not located | type/count corroboration only |
| Weapon identity | **open**: impact record layout not captured | — |
| Team numbers in `Killed` message | **open**: not captured | — |
| Movement / tactical events | **open**: position anchors are raw, uncalibrated | [position AAR](research/current-build/2026-11-02-position-aar.md) |

## Clock hypotheses (tested, not proven)

`tests/test_aar_clock_hypotheses.py` checks these against pinned evidence. Any
new replay with known UI times should be added to its `DISPLAYED` table.

- **H1:** one replay frame is a 0.2 s deterministic tick. The impact clock equals
  0.2 × the engine counter, and the counter stays within the file's frame range.
  The controlled replay's 1784 frames give 356.8 s against a UI total of 5:55.
  The exporter emits `replay_frame_hypothesis` with this status.
- **H2:** battle time starts at the opcode-0x13 frame. It matches two displayed
  battle durations (4:11 and 2:24) and one mid-battle UI point (replay 4:29 =
  battle 0:58).
- **H3:** the replay actor `0xC0000066` is the parent group of runtime owners
  `0xC0000067` and `0xC0000068`. This rests on key adjacency and shared GUID
  parts only. Untested.

## Next authorized capture (delta from v3)

Add `0xcf8490` entry (impact record, 128 bytes at arg 0). Add `0xc52de0` only
`within` the apply hook, replacing the 1-in-997 sample. Add reads of the
`0xc954f9` composition inputs (`[ebp+0x73]`, `[ebp-0x38]`). Drop
`frame_apply_candidate`, the order/reference hooks and the clock sampler.
Locate the debrief kill-stats provider statically first. Do not write the
config or exporter profile before the run is authorized.

## Other priorities

1. Request usefulness: filters, reference history and request summaries on the
   existing timeline. Keep contextual kind 39 and unknown execution outcomes.
2. Targeted format questions: the `0x0C` consumer, `0x0A`/`0x0B` and marker
   fields. Check the [research index](research/INDEX.md) first.
3. Independent validation: more authenticated samples, and the Sample2
   executable.

## Constraints

- Strict container acceptance stays until evidence justifies a change.
- Unknown: digest origin, slot-to-player identity and extended `star` payloads.
- Static NDF types do not establish ownership or outcomes.
- This file grants no VM authorization.

Current counts and scripts: [architecture](docs/ARCHITECTURE.md#4-generated-files-and-their-scripts).
Earlier narratives: Git history and the
[2026-10-28 archive](research/NEXT-STEPS-2026-10-28.md).
