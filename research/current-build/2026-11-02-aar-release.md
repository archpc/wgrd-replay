# Revision-131544 AAR: evidence-bounded release

Date: 2026-11-02. Build: internal revision 131544, `WarGame3.exe` SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.

Status: **final for the retained evidence.** Built only from existing
authenticated captures and static analysis. No VM, gameplay, new hook or new
investigation was used for this release. A fully runtime-verified AAR is a
separate future task and needs explicit VM authorization.

Evidence levels used below: **observed** (read in a hash-pinned trace),
**static** (pinned executable bytes or the build-matched NDF index),
**hypothesis** (tested against evidence, not proven), **unknown** (not
observed; no value is asserted).

## 1. Inputs (pinned)

| Input | SHA-256 |
|---|---|
| Executable `WarGame3.exe` (rev 131544) | `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d` |
| Replay `replay_2026-11-01_19-10-26.wargamerpl2` | `abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121` |
| Trace A `wgrd-aar-combat-20261102-01.jsonl` (12,382 records) | `607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74` |
| Trace B `native-v3b-replay.jsonl` (10,182 records) | `d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec` |
| Unit index `unit-index-131544.json` | `73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d` |
| NDF source archive (via index) | `172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b` |
| Capture config A `aar-capture-131544.json` | `f904c7ed526129148fc41857ee3e981f5531cc26c3c3b684f85c2ebfe7e25ba0` |
| Capture config B `aar-capture-131544-v3.json` | `e02901924b5465b0ab58a29cce1c537d45139d2054333d950aeed265e3a3eefd` |

Capture-era `hooks.js`/`wgrd_frida.py` copies for both traces are retained in
each capture's private `capture-sources/`. The exporter verified every one
against the trace's start record ("all capture-era source/config hashes
matched retained copies").

Replay binding: trace B's experiment manifest records the replay hash above.
Trace A has no playback log naming its replay. It is bound to the same replay
by content: all 28 impact events agree on every compared value with trace B
(section 7) and with the earlier 2026-11-01 capture of that replay. The native
file-open of the replay was **not observed** in either capture.

## 2. Reproduction

From a checkout of this commit, Python 3.14 or 3.15:

```sh
A="$HOME/.hermes/artifacts/wgrd-replay"
IDX="$A/aar-20261102T050816Z/units/unit-index-131544.json"
python3.14 -B instrumentation/aar_events.py \
  "$A/aar-20261102T050816Z/wgrd-aar-combat-20261102-01.jsonl" \
  --profile runtime --unit-index "$IDX" --out "$TMPDIR/aar-A"
python3.14 -B instrumentation/aar_events.py \
  "$A/aar-v3-20261102T082918Z/native-v3b-replay.jsonl" \
  --profile runtime-v3 --unit-index "$IDX" --out "$TMPDIR/aar-B"
(cd "$TMPDIR/aar-A" && shasum -a 256 *); (cd "$TMPDIR/aar-B" && shasum -a 256 *)
```

Expected stdout:

```text
wrote 28 runtime impacts, 9 units, 3 lifecycle destructions to <out>/aar-A
wrote 28 runtime impacts, 9 units, 3 lifecycle destructions, 371 position observations, 153 anchor changes to <out>/aar-B
```

Expected output SHA-256 (identical under 3.14 and 3.15):

| Trace | File | SHA-256 |
|---|---|---|
| A | `chronology.md` | `a2e401b311ed27201287fb41bac487a7e511fddea628598e5d9b7d6e9e696e0a` |
| A | `events.json` | `d8f26e83f725f1b3f19f750ddb22b6efaf269e6f0378c22a780a2c6bf2c0b706` |
| A | `summary.json` | `8d3d1e7afb45a3397e38e18d1c3ac53bdf245378c2f316f1b0d8d664b4f357c8` |
| A | `units.json` | `ebe43d9e34ca87d0a0f7aef533f3766c8a989fa0d0051756017a7698a4cf0baa` |
| B | `chronology.md` | `c744d2760834ae594725637d74b70c569057f54f957fe90225bf5e385b805b3e` |
| B | `events.json` | `ae3752078b482753b862253a01568cb6a11ae49eb4cdcff01c019129646f58ac` |
| B | `positions.json` | `6645cb4b3a7d361968fd19d9a8c8c46adaf2f6b969cf973d19907f896c2c396b` |
| B | `summary.json` | `c9b20e8bab79890143b877f080af0a50c71dcead9b22db24bf9e308b7f9bb487` |
| B | `units.json` | `ce19f1732b4d06729c1fd0916b738446650972a40b5bf13ee156b409a61a725e` |

`tests/test_aar_release.py` re-runs both exports and checks these hashes,
cross-trace agreement and the unknowns below. Outputs are exclusively created
and contain no host paths. The older private `existing-evidence-aar-repro/`
and `runtime-aar-v3-reviewed/` directories predate the source-role and
`killed_token` changes (PRs #16, #18) and are superseded by these outputs; they
are kept unchanged as provenance.

## 3. Observed damage

Both traces: 28 impact calls (`0xc9f910`), each paired with its destruction
check (`0xc9bf20`); 0 unpaired, duplicate, stale-frame, stack-mismatch or
callback-error records.

- 25 suppression increases (field `+0x190`) and 3 physical-damage increases
  (field `+0x19c`, 0 → 10 each) on 6 target handles (31, 32, 33, 34, 39, 40).
- Per-event before/after float32 values and raw hex are in `events.json` and
  `chronology.md`, with trace line references.
- Physical-damage hits: ordinals 3 (handle 33), 7 (handle 31), 21 (handle 39).

## 4. Source and target identities

| Role | Handles | Unit type (static 2-of-2 GUID + name-token join) | Level |
|---|---|---|---|
| Target | 31, 32, 33, 34, 39, 40 | `Unit_VTT_323_NK` (node 20147) | observed handle and descriptor pointer; static type join |
| Reported source | 74 (7 hits), 75 (10 hits) | `Unit_Merkava_IIIB_Baz` (node 19537) | observed `arg1` owner; static engine-credited role |
| Source unresolved | — | — | 11 hits with null `arg1`: **unknown**, not "no source" |
| Cleanup operand | 0 | unresolved | observed |

Source role `engine_credited_damage_source` is static: `0xc9f910` credits
`arg1` with an `ExperienceMessage` (lethal-hit bonus at `0xc9fa75`–`0xc9fc08`),
and `arg1` comes from the queued entry's copied impact record. It is not a
weapon or projectile identity. Type joins do not authenticate live entities,
players or deployments. The debrief kill-table screenshot (separate evidence,
SHA-256 `62334686…59f1d`) shows three `VTT-323` victim rows and `MERKAVA IIID
BAZ` attacker labels; its row-to-handle mapping and IIID/IIIB label mapping are
**not established**.

## 5. Destruction events

| Impact ord | Victim handle | Reported source | Check AL | Destroy call (`0xa75c70`) | Level |
|---:|---:|---|---:|---|---|
| 3 | 33 | 75 `Unit_Merkava_IIIB_Baz` | 1 | parented by the check, retval 1 | observed chain |
| 7 | 31 | 74 `Unit_Merkava_IIIB_Baz` | 1 | parented by the check, retval 1 | observed chain |
| 21 | 39 | 75 `Unit_Merkava_IIIB_Baz` | 1 | parented by the check, retval 1 | observed chain |

The check's AL is the entry's `Killed` token by static mapping (`0xc95344` →
`0xc954f9`); the message itself is not captured. All three destroys took the
`TIAKillGameplayMessage` branch (unit `+0x20 != -1`). Three further destroy
calls (handles 0, 74, 75; argument 6; no parent) are end-of-match cleanup and
are excluded from combat losses. These are **destruction invocations, not
scored kills**.

## 6. Timing evidence

- **Observed:** the damage object's `+0x1ec` (engine-named deterministic
  seconds) at each impact. Lethal hits: 806.4 (ord 3), 806.6 (ord 7), 830.8
  (ord 21). All 28 values are 0.2 multiples (quantization check only).
- **Static:** `DeterministicCurrentTimeInSeconds` (`0x1d9cd68` → `0xa406b0`)
  loads global `0x201d318`, calls `0xaaedf0`, which scales `[ecx+0xd0]` by
  0.2 (`0x195d768` = `0x3e4ccccd`). The ticks accessor reads the same counter.
- **Observed counters:** 459 sampled clock reads per trace; one receiver change
  each (A: 2195 → 195; B: 12102 → 242), last counter 4164 in both. Receiver
  changes are not interpreted as epochs.
- **Hypotheses (tested, not proven; `tests/test_aar_hypotheses.py`):** H1 one
  replay frame = one 0.2 s tick; H2 battle time starts at the opcode-0x13
  frame.
- **Unknown:** clock origin, replay frame, simulation/battle time of any
  event. Guest wall-clock timestamps are UTC observations, not game time.

## 7. Cross-trace verification

The two traces are independent playbacks with different hook sets. On all 28
impacts they agree on ordinal, kind, target handle, every field's before/after
raw bytes, target type, reported-source handle and type, check AL and destroy
operand (`test_both_traces_agree_on_every_combat_observation`). Only process
addresses, line numbers and call IDs differ.

## 8. Static scoring model (verified)

Byte-checked against the pinned executable by `tests/test_aar_kill_scoring.py`
(17 instruction sites, 2 vtable slots, both trace boundaries). Full detail:
[causal chain §10](2026-11-02-causal-chain.md).

1. **Store (`0xc95040`).** After a nonzero apply result, `module+0x214 =
   entry+0x0c` (shooter's team object; `ShooterTeamNumber` = `[esi+0x5c]`) and
   `module+0x210 = entry+0x10` (shooter's unit descriptor). Last-hit fields.
   Entry flag `+0x50` bit 0 substitutes an allied or default team.
2. **Credit (`0xb9b680`, `sipTUniteGamePlay` vtable `+0x3c`).** Reads the
   victim's `+0x214`/`+0x210`, computes a value from the victim descriptor
   (`+0xdc` → `+0xe4`), splits it across the credited team (game mode 10: also
   allies) and calls `0xb6a570` on each `team[+0x134]`. The victim's team gets
   `0xb6a630`.
3. **Statistics (`0xb6a570`).** Kill value by shooter descriptor (`+0x70`),
   kill count by victim descriptor (`+0x64`), kill total (`+0x24`), `+0x1c`/
   `+0x20` by victim flag, value into `+0x30` and category arrays `+0xcc`/
   `+0xe0`. Losses (`0xb6a630`): `+0x58`, `+0x28`, `+0x2c`/`+0xb8`.
   `TTeam.GetStatsDescriptorsKilled` (`0xa4a2d0`) returns `+0x64`.
4. **Invocation.** `0xa79680` (vtable `+0x48`) calls `+0x3c`. `0xa75c70` calls
   `+0x48` directly only when unit `+0x20 == -1`; otherwise it posts
   `TIAKillGameplayMessage`.

Kill counts, kill value, losses, XP and debrief display are distinct
quantities. The chain is static; no retained trace observes `0xb9b680` or
`0xb6a570`.

## 9. Unknown (not observed; no value asserted)

| Item | Why unknown |
|---|---|
| Weapon / ammunition ID | Entry `+0x00` is the firing `TAmmunition` descriptor (static); neither trace reads it |
| Credited team | `entry+0x0c` / `module+0x214` not read; team number `+0x5c` not captured |
| Scored kills | Store, credit and statistics calls not observed; message consumer not traced |
| Player, faction, team per unit | Only raw owning-object ref `owner+0x24` observed |
| Company → unit links | H3 is a static/adjacency hypothesis; parent-child link not observed |
| Clock origin, frame, battle time | Not captured; H1/H2 untested at runtime |
| Replay file-open identity | Native open not observed in either capture |
| Movement, tactical outcome | Position anchors are raw, uncalibrated float triples |

## 10. Remaining runtime-only gaps

Each needs an authorized playback; none is part of this release.

1. Read `[arg3]` at the impact hook → ammunition GUID → weapon ID.
2. Read `entry+0x0c` / victim `+0x214` and team `+0x5c` → credited team.
3. Observe `0xb9b680` and `0xb6a570` (args, victim `+0x210`/`+0x214`) →
   scored kills and kill value.
4. Trace the `TIAKillGameplayMessage` consumer → `0xa79680`.
5. Confirm the `0xc95292` store ran for each lethal hit.
6. Score conditions in `0xb9b680` (mode switch, `0xb7abf0`) for this match.
7. Debrief binding: Python → `GetStatsDescriptorsKilled` → kill-table UI.
8. Clock origin and frame mapping (H1/H2); company-to-unit link (H3).
9. Native replay file-open identity for each capture.
