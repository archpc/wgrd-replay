# Revision 131544: damage producer, credit and kill messages

Status: static, read-only. Engine SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, VAs at base
`0x400000`. Ghidra 12.1.4 via the canonical REA CLI on a disposable clone of the
existing project (no import, no analysis, no save). No VM or game run.

Evidence: REA envelopes plus the query recipe in private
`aar-causal-static-20261102/` and, for §9, `aar-ammo-static-20261102/`
(each with `SHA256SUMS`). Each address below is in the
envelope named after it, for example `decompile-0xcf97ad.json`.

## Causal path

```
0xcf8490  impact/splash resolver (impact record R; area query; per-victim loop)
  -> 0xcf95e0(R, mode 2|1, victim owner, victim damage module, ...)   x2 per victim
     -> 0xcfa120 computes the amount
     -> 0xcf7f40 -> 0xc58a70 append(amount, prefix=R, R'+0x10, mode)  queue entry
        (mode 2 also queues mode-1 suppression scaled by a global ratio)
0xc95040  per-module damage loop, for each queued entry:
  -> vtable+0x98 = 0xc9f910 apply(amount, source=lookup(entry+0x08), entry+0x10, entry, mode)
  -> vtable+0x94 = 0xc9bf20 threshold check -> 0xa75c70 owner destroy when met
  -> 0xc954f9  composition message: Killed, DamagesType, Damages, Target,
               TargetTeamNumber, ShooterTeamNumber
```

## Findings

1. **Producer.** `0xc58a70` copies the caller's prefix record into the 0x74-byte
   entry and stores amount `+0x68`, parameter 3 `+0x6c` and mode `+0x70`. Of its
   five direct callers, the combat path is `0xcf8490 -> 0xcf95e0 -> 0xcf7f40`,
   which passes the resolver's impact record `R` as the prefix. Entry `+0x08`
   is therefore `R[2]`, the handle the apply call resolves into its source
   argument. `0xcf8490` reads `R[2]` and `R[3]` before the victim loop and drops
   victims whose `0xa72ae0()` value equals `R[3]+0x3c` unless `0xd9bc70()` is
   true. That comparison is team-like; its meaning is not established.
2. **Source credit.** On a mode-2 hit with a non-null source that passes
   `0xb7aba0`, `0xc9f910` posts an `ExperienceMessage` (`Experience_GainAmount`,
   `Experience_Target`) keyed by the source owner's `+0x20` handle (`0xc9fa75`
   to `0xc9fc08`). The gain is `applied / MaxDamages × 0xa727a0()`, plus a
   lethal-hit bonus when the hit reaches `MaxDamages`. The engine thus credits
   the source argument for the damage. It does not identify weapon or projectile.
3. **Native kill event.** After every entry, `0xc95040` stores the check's AL at
   `[ebp+0x73]` (`0xc95344`) and posts a typed composition at `0xc954f9` through
   `0xaeb6b0`. `Killed` is that byte. `ShooterTeamNumber` comes from
   `[esi+0x5c]` (`0xc9534b`), or `0x17` without a source. Which object `esi`
   holds there is not yet byte-checked against a trace. This, not the
   lifecycle message below, is the per-hit kill-result boundary.
4. **`TIAKillGameplayMessage` is not a scored kill.** Builders `0xafe8c0` and
   `0xafe9f0` carry the victim reference and object, one opaque value and one
   dereferenced value. Neither carries an attacker. They are reached from owner
   destroy (`0xa75c70`, including cleanup with argument 6), reference
   reassignment (`0xd06830`) and container teardown (`0x10a0c40`). It is a
   lifecycle notification.
5. **`TIATakeDamageMessage` via `0xc4cba0`** is sent only after a killing
   mode-2 entry when module `+0x248` is non-zero. That explains the zero calls
   seen at `0xc4cba0`. It is not on the AAR path.

6. **Ownership.** `0xa72ae0` is `add ecx,0x24; call 0xb00700; mov eax,[eax+0x5c]`
   (byte-checked). So owner `+0x24` is a reference to a type-2 owning object,
   and that object's `+0x5c` is the team number used for `TargetTeamNumber`.
   `0xb7aba0` compares two such `+0x5c` values before granting experience. In
   the retained trace all six VTT-323s carry `0x00020005`; both Merkavas and
   cleanup handle 0 carry `0x00020004`.
7. **`Killed` consumers.** `0xa938f0` (`TEventInfoManagerModule`) subscribes
   with the filter `Killed == 1`, `TargetTeamNumber == own team` and `Target`
   present, with callback `0xa951a0`. `0xbfcde0` subscribes to `Killed == 0`
   with `DamagesType == 2`. These are the in-game event notifications. The
   debrief kill-stats UI is built by `0x1248620`/`0x1248b50`
   (`TUIWargame2OutGameDebriefKillStatsLine`, vtable `0x1a06e64`) and
   `0x12478f3` (`...KillStats`, vtable `0x1a06eb0`). Its data source is the `TTeam`
   statistics of section 10; the binding-to-UI path is unresolved. `0x12585b0`, the only `EG_KILLS` reference, formats career
   profile statistics alongside `EG_VICTLVL` and `EG_WINSTRK`; it is not
   per-battle scoring. The debrief corroborates the AAR but is not on the
   causal path.
8. **Actor company (H3).** The replay actor `0xC0000066`'s validation GUID
   `00000000050000000300000014040000` is exactly the descriptor of
   `Company_Merkava_IIIB_Baz` (node 51786), whose default member is
   `Unit_Merkava_IIIB_Baz` (19537). The runtime Merkava owners have keys
   `0xC0000067`/`0xC0000068`, and no owner-class object has key `0x66`. The
   company-to-unit link itself is not runtime-observed
   (`tests/test_aar_hypotheses.py`).
9. **Weapon boundary.** The resolver loop `0xcff5a0` (`TProjectileManager`,
   singleton `0x203c328`, ctor `0xcf6910`) calls `0xcf8490` for each 0x68-byte
   projectile record; `0xcf7fe0`/`0xcf81f0` append them. In `0xcf95e0`, `R[0]`
   is passed as `ecx` to `0xc2c940(mode)`, which returns `+0xa8` for mode 2 and
   `+0xb0` for mode 1 (byte-checked). `0xc2f6f0` registers the `TAmmunition`
   properties `RadiusSplashPhysicalDamages` at `+0xa8` and
   `RadiusSplashSuppressDamages` at `+0xb0`, and `0xc2c650` returns
   `PhysicalDamages` `+0xac` and `SuppressDamages` `+0xb4`. So `R[0]` is the
   firing `TAmmunition` descriptor, a `TSaveableDescriptor` (`0xb578e0`) whose
   `DescriptorId` GUID is expected at `+0x0c`, as for unit descriptors. The
   131544 NDF holds 2092 `TAmmunition` objects with 2092 unique GUIDs
   (private `aar-ammo-static-20261102/`, reproducer `ammunition_index.py`).
   The queued entry copies `R` (`0xc4b0f0`), so `entry+0x00` is the ammunition
   pointer at apply time. **Not yet observed:** neither retained trace reads
   it. `0xc9f910`'s `param_4` is the entry, and both traces show
   `arg3 - ecx = 0x10` (25 calls) or `0x84` (3 calls), so entry `+0x00` lies
   inside the damage module's inline entry storage.
10. **Kill-scoring chain.** All links are byte-checked in
   `tests/test_aar_kill_scoring.py`.
    - *Store.* For each entry, `0xc95040` loads `esi = entry+0x0c` (`0xc95121`)
      and `eax = entry+0x10` (`0xc95188`), and passes `entry+0x10` as `arg2` of
      the apply call (`0xc951e6`/`0xc951fd`, vtable `+0x98` = `0xc9f910`). After a
      nonzero result it stores `module+0x214 = entry+0x0c` and
      `module+0x210 = entry+0x10` (`0xc95292`/`0xc95298`). `ShooterTeamNumber` is
      `[esi+0x5c]` (`0xc9534b`). So `+0x214` is the shooter's team object and
      `+0x210` the shooter's unit descriptor. If entry flag `+0x50` bit 0 is set,
      `esi` is replaced by an allied team or a default. These are last-hit fields,
      overwritten by each nonzero hit.
    - *Credit.* `0xb9b680` is `sipTUniteGamePlay` vtable `+0x3c`. It reads the
      victim's damage module `+0x214`/`+0x210` (`0xb9b86c`/`0xb9b875`), computes a
      value from the victim descriptor (`+0xdc`, its `+0xe4` field), and splits it
      across the credited team (in game mode 10, also its allies). For each
      credited team it calls `0xb6a570` on `team[+0x134]` (`0xb7a4a0`). The
      victim's team gets `0xb6a630`.
    - *Statistics.* `0xb6a570` adds the value to `+0x70[shooter descriptor]`,
      increments `+0x64[victim descriptor]` and `+0x24` (the total), and
      increments `+0x1c` or `+0x20` by a victim flag. It also adds the value to
      `+0x30` and to per-category arrays `+0xcc`/`+0xe0` (category from
      descriptor `+0xa8`). `0xb6a630` increments `+0x58[victim descriptor]` and
      `+0x28` and adds the value to `+0x2c`/`+0xb8`. The Python binding
      `TTeam.GetStatsDescriptorsKilled` (`0xa4a2d0`) returns `team[+0x134]+0x64`.
    - *Invocation.* `0xa79680` (vtable `+0x48`) calls `+0x3c`. The owner-destroy
      function `0xa75c70` calls `+0x48` directly only when unit `+0x20 == -1`.
      Otherwise it posts `TIAKillGameplayMessage` (`0xafe9f0`).
    - *Kinds.* These are distinct: kill counts (`+0x64`, `+0x24`), kill value
      (`+0x70`, `+0x30`), losses (`+0x58`, `+0x28`), XP (`0xc9f910`'s
      `ExperienceMessage`, a separate path), and debrief display.
    - *Retained traces.* All 28 impact calls in both traces return to
      `0xc95200`, so `arg2` is `entry+0x10`. Every `arg2` is a
      `TUniteAuSolDescriptor`. At the three lethal checks, the last `arg2` GUID
      joins `Unit_Merkava_IIIB_Baz`. All six observed owner destroys have
      `+0x20 != -1`, so they took the message branch. The traces observe no store,
      credit or statistics call. **No scored kill is observed.**
    - *Unresolved edges.* (a) `TIAKillGameplayMessage` consumer → `0xa79680`;
      (b) whether the `0xc95292` store ran for the lethal hits (it requires a
      nonzero result); (c) `entry+0x0c` for the observed entries, which is not
      read; (d) score conditions in `0xb9b680` (mode switch, `0xb7abf0`) for this
      match; (e) Python debrief → `GetStatsDescriptorsKilled` → kill-table UI.

## Consequences for the AAR

- Exporter source roles become `engine_credited_damage_source` with confidence
  `static_xp_credit_and_producer_dataflow`. Null source arguments stay
  `unresolved_owner`.
- The retained traces already capture `Killed` (the check's AL), `Damages`,
  `DamagesType` and `Target`. The exporter emits `killed_token`, a static
  mapping of the observed AL; no captured message and no confirmed scored kill.
  It also emits a per-unit `owning_object_ref`. Team numbers are not captured,
  so no player, faction or team is assigned.
- Weapon identity needs one indirect read of `[arg3]` on the existing impact
  hook, joined by GUID to the ammunition index. Until it is captured, events
  keep `weapon` in `not_claimed`.
- Scored kills: the static chain to `TTeam` statistics is closed (section 10).
  The exporter still claims none; no trace observes `0xb9b680` or `0xb6a570`.
- Still open: section 10's edges (a)–(e), runtime weapon observation, `R`'s full
  layout, and runtime proof of the company-to-unit link.

## Reproduction

Clone the retained project (APFS clone, no extra space), then query it with the
canonical REA CLI. REA's private copy and read-only policy leave the clone's
analysis unchanged.

```sh
cp -cR ~/ghidra-projects/forensic-parent-01 "$TMPDIR/ghidra-aar"
export REA_GHIDRA_PROJECT_PATH="$TMPDIR/ghidra-aar/wgrd131544.gpr"
export REA_GHIDRA_PROGRAM_NAME=WarGame3.exe
export GHIDRA_INSTALL_DIR=~/.hermes/tools/ghidra/ghidra_12.1.4_PUBLIC
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
~/.hermes/tools/node-26.12.1-darwin-arm64/bin/node ~/.hermes/tools/rea/scripts/rea.mjs \
  decompile ~/.hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe 0xcf95e0 \
  --provider ghidra --format json
```

Use `xrefs` instead of `decompile` for callers. `JAVA_HOME` must point at a full
JDK 21 or newer; without it the provider reports `runtime_unavailable`.
