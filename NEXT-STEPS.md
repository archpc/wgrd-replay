# Current status and next steps

Target: a complete, reproducible after-action report (AAR) for revision 131544
(SHA-256 `5eaa6d61…f09efc75d`), produced by the original engine replaying a
recording.

The replay file contains only inputs. The decoder (`wgrd_replay.py`) recovers
the player's commands. Combat outcomes exist only when the engine re-executes
them. Playback is deterministic at the observed boundary: two captures with
different hook sets produced the same 28 impacts.

Repository cleanup is frozen as of 2026-11-02 (PRs #19–#21). Work now returns to
understanding the game; change structure only when a game question requires it.

## Release status

The evidence-bounded AAR is **complete**:
[AAR release](research/current-build/2026-11-02-aar-release.md) pins inputs,
commands, output hashes, the static scoring model and every unknown. A fully
runtime-verified AAR is a separate task that needs explicit VM authorization;
its gaps are listed in that note's section 10.

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
| Threshold → `Killed` token and owner destroy | observed AL and nested destroy; Killed = AL by static mapping. The message itself is not captured. Exported as `killed_token` | causal chain §3 |
| Owning object per unit | observed owner `+0x24` ref, static meaning; exported as `owning_object_ref`. No player, faction or team assigned | causal chain §6 |
| Scored kill | static chain closed to `TTeam` stats (`0xc95040`→`+0x210/+0x214`→`0xb9b680`→`0xb6a570`). **Not observed** | causal chain §10 |
| `TIAKillGameplayMessage` | lifecycle only, not kill credit | causal chain §4 |
| Kill table / kill points (debrief) | source = `TTeam` stats `+0x64`/`+0x70` (static); UI binding unresolved | causal chain §10 |
| Weapon identity | static: entry `+0x00` is the firing `TAmmunition` descriptor; 2092 unique GUIDs indexed. **Not yet observed** | causal chain §9 |
| Movement / tactical events | **open**: position anchors are raw, uncalibrated; this capture produced 0 anchor changes | [position AAR](research/current-build/2026-11-02-position-aar.md) |
| Frame → simulation time | static: one frame per 0.2 s tick; origin = replay load | [frame consumption](research/current-build/2026-11-02-frame-clock-consumption.md) |
| Recorded order apply path | static: `TNetworkActionGiveOrderStandard` slot 1 `0xb2be30`; outcome unknown | frame consumption §3 |
| Frame/tick clock | observed: 5.00 frames/s, ticks 1:1 with frames, integer difference 10 or 11 (boundary unresolved) | [frame/tick capture](research/current-build/2026-11-02-frame-tick-capture.md) |
| Battle start / phase boundary | **unknown**: `0xab4780` fired once during replay (arg `0x2`, tick 2905); one sample is not a timeline | [combat attempt](research/current-build/2026-11-03-combat-frame-capture-attempt.md) |

## Hypotheses (tested, not proven)

`tests/test_aar_hypotheses.py` checks these against pinned evidence. Any
new replay with known UI times should be added to its `DISPLAYED` table.

- **H1:** one replay frame is a 0.2 s deterministic tick. Observed in the
  authorized playback: 2311 frames in 462.65 s (5.00 Hz), every tick advance
  `+1`, and the deterministic counter one tick per frame. The counters do *not*
  share an origin: `frame - tick` is 10 (48 samples) or 11 (47), stable over
  462 s, with no sample where both advance together. The exact boundary is
  unresolved; 10.5 frames is a statistic used only for a bounded per-event
  estimate. Verified battle time stays null.
- **H2:** battle time starts at the opcode-0x13 frame. It matches two displayed
  battle durations (4:11 and 2:24) and one mid-battle UI point (replay 4:29 =
  battle 0:58).
- **H3:** the replay actor `0xC0000066` is the company owning runtime units
  `0xC0000067`/`0xC0000068`. Its GUID is exactly `Company_Merkava_IIIB_Baz`,
  whose member type matches both runtime owners, and the keys are adjacent.
  The parent-child link is not runtime-observed.

## Next authorized capture (delta from v3)

Add one indirect read `("arg3", 0, 128, "enter", indirect)` to
`impact_apply_candidate`: the descriptor GUID at `+0x0c` joins the private
ammunition index (causal chain §9). No new hook is needed. Add `0xc52de0` only
`within` the apply hook, replacing the 1-in-997 sample. Hook `0xa72ae0` (or read owning object `+0x5c`) to
capture team numbers. Drop
`frame_apply_candidate`, the order/reference hooks and the clock sampler.
For scored kills: hook `0xb6a570` (args: victim descriptor, victim owner,
shooter descriptor, value) and `0xb9b680` enter (read victim module
`+0x210`/`+0x214`). Read impact `arg3` `+0x0c` for the credited team object.
Do not write the config or exporter profile before the run is authorized.

## AI decision model (static thread, no VM authorization)

Mechanisms are mapped, shipped values are not. Next milestone: recover effective
NDF values (`NDF_Win.dat` encoding unresolved) and trace influence-map output
into AI order generation. Keep economy and information as separate questions.
See the [AI decision model](research/current-build/2026-11-08-ai-decision-model.md).

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

Generated outputs and scripts: [architecture](docs/ARCHITECTURE.md#4-generated-files-and-their-scripts).
Earlier priorities and narratives: [research archive](research/INDEX.md#archive).
