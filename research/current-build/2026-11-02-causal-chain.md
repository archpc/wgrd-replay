# Revision 131544: damage producer, credit and kill messages

Status: static, read-only. Engine SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, VAs at base
`0x400000`. Ghidra 12.1.4 via the canonical REA CLI on a disposable clone of the
existing project (no import, no analysis, no save). No VM or game run.

Evidence: 22 REA envelopes plus the query recipe in private
`aar-causal-static-20261102/` (`SHA256SUMS`). Each address below is in the
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
   `0x12478f3` (`...KillStats`, vtable `0x1a06eb0`). Its data provider is still
   unlocated. `0x12585b0`, the only `EG_KILLS` reference, formats career
   profile statistics alongside `EG_VICTLVL` and `EG_WINSTRK`; it is not
   per-battle scoring. The debrief corroborates the AAR but is not on the
   causal path. A scored kill stays unconfirmed until its provider is found
   or captured.
8. **Actor company (H3).** The replay actor `0xC0000066`'s validation GUID
   `00000000050000000300000014040000` is exactly the descriptor of
   `Company_Merkava_IIIB_Baz` (node 51786), whose default member is
   `Unit_Merkava_IIIB_Baz` (19537). The runtime Merkava owners have keys
   `0xC0000067`/`0xC0000068`, and no owner-class object has key `0x66`. The
   company-to-unit link itself is not runtime-observed
   (`tests/test_aar_hypotheses.py`).

## Consequences for the AAR

- Exporter source roles become `engine_credited_damage_source` with confidence
  `static_xp_credit_and_producer_dataflow`. Null source arguments stay
  `unresolved_owner`.
- The retained traces already capture `Killed` (the check's AL), `Damages`,
  `DamagesType` and `Target`. The exporter emits `killed_token`, a static
  mapping of the observed AL; no captured message and no confirmed scored kill.
  It also emits a per-unit `owning_object_ref`. Team numbers are not captured,
  so no player, faction or team is assigned.
- Still open: the debrief data provider, exact weapon identity, `R`'s full
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
