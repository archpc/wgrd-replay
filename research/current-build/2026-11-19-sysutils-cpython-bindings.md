# Revision 131544: `_sysutils` is CPython 2.5.1, not Lua — binding table, clock fields, writer scan

Date: 2026-11-19. Status: static, read-only. No VM, no game run, no new capture.
Supersedes the "Lua binding" language in earlier notes for this table; does not
change any verified address or computation. One delegated worker claim was
refuted during parent verification (§4).

Executable `WarGame3.exe`, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, re-hashed
before analysis. VAs at image base `0x400000`. GNU objdump 2.47
(`-d -M intel`, `-s` for data). The cached `.text` listing used for the
exhaustive scan is `objdump` output, identity
`ebf338179663e635fbc5248aa03e6b48a424bec2fe1bdf449075d07dd3769275`
(7,320,958 instruction rows, 0 byte mismatches against the pinned file;
record: `~/REA/wgrd-131544/canonical-listing-verification.json`).

## 1. The table is CPython `PyMethodDef`, module `_sysutils`

**Version: CPython 2.5.1.** The original identification (PR #30) said 2.7,
inferred from the API-version gate; that inference was wrong — 1013 is shared
by Python 2.5/2.6/2.7 and never discriminated the minor version. Direct
version evidence (script-layer worker found, parent re-verified against the
pinned image, 2026-11-19):

- Build path string at file offset `0x162a3ed`: `2.5.1\Objects\cellobject.c`;
  20 `Python-2.5.1` build paths in the image.
- SVN `$HeadURL: svn+ssh://***@svn.python.org/python/tags/r251/Python/sysmodule.c $`
  at `0x1636200`; `tags/r251` is the only release tag present (r251 = 2.5.1).
- `2.5.1` occurs 21 times; `2.7.x` zero times (recomputed).
- The NDF side agrees: `initialisationnonpatchable.ndfbin` +13830 names
  `LoadPythonLib250` (decompressed blob offset `0x5a21`, §9).

The `PyMethodDef` identification, table contents and installer proof below
are unaffected by the version correction.

Entries are 16 bytes `{ml_name, ml_meth, ml_flags, ml_doc}` with `ml_flags = 1`
(`METH_VARARGS`) and `ml_doc = NULL`. Byte proof, all parent-verified:

- Installer `0xa42790` (sole caller `0x9d65d4`), one-shot guard
  `cmp ds:0x2024a4c,0` / `jne ret`:

  ```
  a4279a  68 f5 03 00 00      push 0x3f5          ; 1013 = PYTHON_API_VERSION (shared by 2.5-2.7; not a version discriminator)
  a4279f  6a 00               push 0x0            ; doc = NULL
  a427a1  6a 00               push 0x0            ; self = NULL
  a427a3  68 78 cc d9 01      push 0x1d9cc78      ; methods = table base
  a427a8  ff 35 80 c4 d9 01   push [0x1d9c480]    ; name -> 0x1988490 "_sysutils"
  a427b8  e8 73 50 af 00      call 0x1537830      ; Py_InitModule4-style helper
  ```

- The helper hard-rejects any other API version:
  `1537889: 3d f5 03 00 00  cmp eax,0x3f5` / `153788e: 74 39  je 0x15378c9`,
  otherwise formats the string at `0x1dcba88`:
  `"Python C API version mismatch for module %.100s: This Python has API
  version %d, module %.100s has version %d."` (read back verbatim).
- The method walker rejects `ml_flags & 0x30`:
  `1537960: f6 47 08 30  test BYTE PTR [edi+0x8],0x30` → string at
  `0x1a35de8`: `"module functions cannot set METH_CLASS or METH_STATIC"`
  (`METH_CLASS 0x10 | METH_STATIC 0x20`). Loop: `cmp [edi],0` → end,
  `add edi,0x10`.
- Argument format strings are CPython codes: deterministic setter
  `0x196cb98 = "i"`, realtime setter `0x196cb8c = "f"`, seconds getter
  `0x1927bdc = ""` (no args). Parser helper `0x1546430` (called by every
  binding; formerly mislabeled "Lua-arg resolver").
- After module init the installer looks up `"sip"` (`0x1988120`, read back)
  and registers the descriptor `0x1d9c478 = {0, 2, 0x1988490, 0}` — a SIP
  (Python/C++ binding layer) module definition.

Correction scope: `2026-11-02-engine-state.md` §2/§2.1,
`2026-11-02-frame-clock-consumption.md` §4, `instrumentation/state_observe.py`
comments, and the branch-only `2026-11-02-aar-clock.md` addendum called these
"Lua" bindings. That language is wrong for this table. The engine may embed
Lua elsewhere; nothing here proves or disproves that.

The lifecycle binding table (`GameStarted`/`GameEnded`/`EndGameAsked`) is now
also proven CPython: 32 entries at `0x1d97ad8..0x1d97cc8`, terminator
`0x1d97cd8`, module name `_misc` (pointer at `0x1d970f0` → `0x19883d0`, read
back). Installer `0xa32ba0` is the same pattern: one-shot guard
`ds:0x20231d8`, `push 0x3f5` at `0xa32baa`, table push at `0xa32bb3`, call to
the same version-gated helper `0x1537830` at `0xa32bc8`, then the same SIP
lookup (`push 0x1988120`). Entries include `WorldTickEnd`,
`CreateNamedActionWithTimer`, `ExecuteNamedCallbackInIAThread`/`MainThread`,
`metre`/`reverse_metre`. Any further `.data` table with this layout still
needs its own installer check before relabeling.

### Table extent and full entry list

51 entries, `0x1d9cc78..0x1d9cf98`, stride 16, null terminator at
`0x1d9cfa8` (16 zero bytes, read back). Walk-back stops at ASCII `"refcount"`
string data at `0x1d9cc68`. The region after the terminator belongs to a
neighbouring module descriptor (`{0,2,"_task",0}` at `0x1d9cfb8`).

| # | Entry VA | Name | fn |
|---|---|---|---|
| 0 | `0x1d9cc78` | `LaunchOutGame` | `0xa41380` |
| 1 | `0x1d9cc88` | `GetNbGameDesignObjectIdForAlliance` | `0xa40e30` |
| 2 | `0x1d9cc98` | `MustUseTacticalStartingPoints` | `0xa41540` |
| 3 | `0x1d9cca8` | `AddStrategicRoadInfoForZoneManager` | `0xa40240` |
| 4 | `0x1d9ccb8` | `GetAllianceNumFromGDStartingPointRoadDescription` | `0xa40a80` |
| 5 | `0x1d9ccc8` | `GetAllianceNumFromGDStartingPointAlliance` | `0xa409a0` |
| 6 | `0x1d9ccd8` | `SetGDStartingPointAllianceToAllianceNum` | `0xa41c20` |
| 7 | `0x1d9cce8` | `InitGameDesignObjectId` | `0xa41010` |
| 8 | `0x1d9ccf8` | `GetInitialStateForReplay` | `0xa40d70` |
| 9 | `0x1d9cd08` | `SetInitialStateForReplay` | `0xa420a0` |
| 10 | `0x1d9cd18` | `SetGameplayCPPStateFromSave` | `0xa41ec0` |
| 11 | `0x1d9cd28` | `GetGameplayCPPSavedState` | `0xa40c90` |
| 12 | `0x1d9cd38` | `DisplayDebugMessage` | `0xa407d0` |
| 13 | `0x1d9cd48` | `SetRootGDObject` | `0xa42350` |
| 14 | `0x1d9cd58` | `RootGDObject` | `0xa41960` |
| 15 | `0x1d9cd68` | `DeterministicCurrentTimeInSeconds` | `0xa406b0` |
| 16 | `0x1d9cd78` | `DeterministicCurrentTimeInTicks` | `0xa40780` |
| 17 | `0x1d9cd88` | `SetDeterministicCurrentTimeInTicks` | `0xa41bc0` |
| 18 | `0x1d9cd98` | `RealtimeCurrentTime` | `0xa41710` |
| 19 | `0x1d9cda8` | `SetRealtimeCurrentTime` | `0xa422e0` |
| 20 | `0x1d9cdb8` | `OnGamePhaseChanged` | `0xa41650` |
| 21 | `0x1d9cdc8` | `NeedDesynchroLogFromNow` | `0xa41600` |
| 22 | `0x1d9cdd8` | `DontNeedDesynchroLogFromNow` | `0xa408b0` |
| 23 | `0x1d9cde8` | `StartDesynchroLogNowIFN` | `0xa424b0` |
| 24 | `0x1d9cdf8` | `SetSaveLoadForTestAuto` | `0xa42460` |
| 25 | `0x1d9ce08` | `SetIsTestAuto` | `0xa421d0` |
| 26 | `0x1d9ce18` | `SetNextGamePhase` | `0xa42220` |
| 27 | `0x1d9ce28` | `TerminateGamePhaseManager` | `0xa42500` |
| 28 | `0x1d9ce38` | `BeforeStartGameGameplayServices` | `0xa403c0` |
| 29 | `0x1d9ce48` | `DestroyGameplayServices` | `0xa40600` |
| 30 | `0x1d9ce58` | `InitializeGameplayServices` | `0xa410c0` |
| 31 | `0x1d9ce68` | `KillGamesRules` | `0xa412d0` |
| 32 | `0x1d9ce78` | `SetGameRules` | `0xa41db0` |
| 33 | `0x1d9ce88` | `GetGameRules` | `0xa40bd0` |
| 34 | `0x1d9ce98` | `GameplayType` | `0xa40950` |
| 35 | `0x1d9cea8` | `SetGameplayServicesRandomSeed` | `0xa41fd0` |
| 36 | `0x1d9ceb8` | `CreateGameplayServices` | `0xa40470` |
| 37 | `0x1d9cec8` | `IsDataPackMode_DatapackOnly` | `0xa411d0` |
| 38 | `0x1d9ced8` | `IsDemoMode` | `0xa41220` |
| 39 | `0x1d9cee8` | `DontRequireDeterminismFromNowOn` | `0xa40900` |
| 40 | `0x1d9cef8` | `RequireDeterminismFromNowOn` | `0xa41770` |
| 41 | `0x1d9cf08` | `SendMail_IFP` | `0xa41b60` |
| 42 | `0x1d9cf18` | `GetOutgameChapter` | `0xa40ef0` |
| 43 | `0x1d9cf28` | `DecreaseGameSpeed` | `0xa40530` |
| 44 | `0x1d9cf38` | `IncreaseGameSpeed` | `0xa40f40` |
| 45 | `0x1d9cf48` | `ResetGameSpeed` | `0xa417c0` |
| 46 | `0x1d9cf58` | `ResetTime` | `0xa41890` |
| 47 | `0x1d9cf68` | `LoadingDone` | `0xa41470` |
| 48 | `0x1d9cf78` | `TerminateSelf` | `0xa425b0` |
| 49 | `0x1d9cf88` | `SaveData` | `0xa41a20` |
| 50 | `0x1d9cf98` | `refcount` | `0xa426d0` |

## 2. Clock fields on the GameplayServices singleton

Singleton pointer slot `0x201d318` (unchanged). Two distinct clock fields:

- **Deterministic ticks: `+0xd0`, int32.** Seconds getter path
  `0xbb04d0 → 0xaaedf0`: `movd xmm0,[ecx+0xd0]` / `cvtdq2ps` /
  `mulss [0x195d768]` (`cd cc 4c 3e` = 0.2f), x87 return. Ticks getter
  `0xa40780` pushes `[eax+0xd0]` at `0xa407a8`. Setter `0xa41bc0` parses one
  `"i"` arg and stores `mov [eax+0xd0],ecx` at `0xa41bf2`, then
  `inc ds:0x1dbf028` at `0xa41bfd`. That counter is **Py_None's refcount,
  not a setter discriminator** (verified 2026-11-19, §10): `0x1dbf028` is
  the `Py_None` object (`ob_type` at `0x1dbeea0`, `tp_name` "NoneType" read
  back); every void binding returns `Py_INCREF(Py_None); return Py_None`.
  `.text` contains 1,379 `inc ds:0x1dbf028` sites (3,514 references),
  including `DisplayDebugMessage` at `0xa4085e` and `ResetTime` at
  `0xa41907`. Its value counts None-returns across the whole binding layer;
  a nonzero value cannot attribute a call to the
  setter. Only a hook on `0xa41bc0` itself discriminates setter invocations.
  Static observation; unobserved at runtime.
- **Realtime: `+0x98`, binary32.** Getter `0xa41710`:
  `a4173b: f3 0f 10 80 98 00 00 00  movss xmm0,[eax+0x98]`; setter
  `0xa422e0`: `a42314: f3 0f 11 80 98 00 00 00  movss [eax+0x98],xmm0`,
  format `"f"`. Both load the same singleton (`a41733` / `a42309`). This is
  not the tick counter; earlier notes did not distinguish the two fields.

`BeforeStartGameGameplayServices` (`0xa403c0`) has no `+0xd0` access and no
call to the setter; its callees `0xaac910 → 0xaa2be0` do not touch `+0xd0`
(worker analysis, byte excerpts retained). `ResetTime` (`0xa41890`) loads no
singleton in its body; its callees `0x528c00` / `0x974630` are analyzed in
§8 — it posts a synchronisation-queue token, it does not write the clock. No
static reset path for `+0xd0` beyond the constructor below.

## 3. Exhaustive writer scan for `[singleton+0xd0]`

Scope: every `.text` instruction with a `+0xd0` displacement (2,546 memory
operands; `+0xd0 > 0x7f` forces disp32, so no disp8 aliasing exists).
837 modify memory:

| Form | Count |
|---|---|
| `mov` dword store | 494 |
| `mov` byte / word store | 28 / 4 |
| `fstp` dword | 3 |
| `movaps`/`movups` 16-byte store | 276 |
| `movss`/`movsd`/`movlpd`/`movq` | 22 |
| RMW (`add` 4, `inc` 3, `dec` 1, `sub` 1, `and` 1) | 10 |

The prior "497 stores" figure reproduces exactly as 494 `mov` dword + 3
`fstp`; that scan missed the other 340 modifying instructions. `lock`,
`xchg`, `xadd`, `cmpxchg`, `neg`, `not`, `adc`, `sbb`, `or`, `xor` at
`+0xd0`: zero.

Singleton-derived writers: **exactly two**, both parent-verified:

1. `0xa41bf2` `mov [eax+0xd0],ecx` — the `_sysutils` setter (base loaded at
   `0xa41be9`).
2. `0xaab588` `c7 83 d0 00 00 00 00 00 00 00` `mov [ebx+0xd0],0x0` —
   constructor zero-init; `ebx` is the fresh object installed to the slot at
   `0xaab439` (`89 1d 18 d3 01 02`). Runs once at construction, not per tick.

All 10 RMW sites were independently re-extracted and checked: three are
stack-local (`[esp+…]`), seven have zero `0x201d318` references in a
−200/+20 instruction window. The 537 singleton references include 4 slot
stores (install `0xaab439`; null-outs `0xaabc21`, `0xaabf32`, `0xaac24b`)
and 2 `cmp` reads; 356 call sites forward the singleton to 89 callees, none
of which contains a `+0xd0` writer (worker provenance pass with call-clobber
barriers; one false positive at `0xb363f2` rejected — `esi` is
`operator new(0xfc)` output, not the singleton).

**The runtime tick advance has no statically visible direct writer.** The
counter is observed advancing ~1 per replay frame
([frame/tick capture](2026-11-02-frame-tick-capture.md)). The wide-store
overlap gap is now closed (2026-11-19, second scan): a store of width W at
displacement d covers `+0xd0` iff `d <= 0xd0 <= d+W-1`; 919 instructions
qualify (837 at `d=0xd0`, address-identical to the set above, plus 82 at
`0xc0/0xc4/0xc8/0xcc`: 35 AVX `vmovdqu [esp+0xc0]`, 39 16-byte and 8 8-byte
object stores). Of the 82, 72 are stack-relative; the 10 non-stack
candidates were provenance-checked (call-clobber barriers) and none is
singleton-derived; their enclosing functions show zero `0x201d318`
references in caller lookbacks and bodies. The 89 callees that receive the
singleton pointer contain no covering store, and 14 `lea`/`add` delta paths
from `+0xc1..+0xd0` resolve to no singleton-derived store. Supporting fact:
`sizeof(TGameplayServices) = 0xf0` — the construction site pushes `0xf0`
before `operator new` (`0xaae63b push 0xf0` / `0xaae642 call 0x528c00` /
`0xaae65b mov ecx,eax` / `0xaae65d call 0xaab3e0`, parent-verified), so
offsets `>= 0xf0` are out of object and larger allocations are different
types. Remaining hypotheses: an indirect write through a copied pointer, a
write from outside `.text`, or the embedded Python calling
`SetDeterministicCurrentTimeInTicks` per tick. The runtime discriminator is
a hook on the setter `0xa41bc0` itself (the shared counter `0x1dbf028`
cannot attribute calls — §2), which needs an authorized
capture. Limitations: provenance is intra-procedural; parameter-derived
bases and cross-call indirect writes are invisible to this scan (type-level
exclusions by allocation size/vtable are not reachability proofs, and for
the six enclosing functions with no direct call site the caller lookback is
vacuous); one
worker caller-count script disagreed with the other for `0x10d0f50`
(0 vs 283; direct call sites exist), so that exclusion rests on the
283-caller singleton-reference sweep and base provenance, not the count;
absence of a textual spelling is not proof of absence.

## 4. `0xaaee10`: store-if-different, not monotonic max (worker claim refuted)

A delegated worker reported the float store in `0xaaee10` fires "only when
current ≤ new (monotonic max)". Parent flag-level analysis refutes this.
Bytes:

```
aaee87  f3 0f 10 4d 0c     movss xmm1,[ebp+0xc]    ; new (arg2)
aaee8c  f3 0f 10 41 24     movss xmm0,[ecx+0x24]   ; current
aaee91  0f 2e c1           ucomiss xmm0,xmm1
aaee94  9f                 lahf                    ; AH bit6=ZF bit2=PF bit0=CF
aaee95  f6 c4 44           test ah,0x44
aaee98  7b 10              jnp 0xaaeeaa            ; skip store
aaee9a  f3 0f 11 49 24     movss [ecx+0x24],xmm1   ; store
```

`test` recomputes PF from the parity of `AH & 0x44`; `jnp` skips the store
only when exactly one of ZF/PF is set, i.e. ordered equality:

| cur ? new | CF | ZF | PF | AH&0x44 | parity | jnp | store |
|---|---|---|---|---|---|---|---|
| cur > new | 0 | 0 | 0 | 0x00 | even | no | YES |
| cur < new | 1 | 0 | 0 | 0x00 | even | no | YES |
| cur == new | 0 | 1 | 0 | 0x40 | odd | yes | no |
| unordered | 1 | 1 | 1 | 0x44 | even | no | YES |

Verified by independent flag-level emulation of all four cases. The store
fires on increase, **decrease**, and NaN; it skips only ordered equality.
Change detection, not a max. A monotonic max would never store a decrease.

Control flow (verified, semantics not assigned): thiscall, `ret 8`;
`ecx = [esi+0xe8]` subobject; arg1 is a string key used with a container at
`subobj+0x1c` (`0x4fd050` lookup, `0x4fca90` on hit); the float field is
`subobj+0x24`; both paths call `0x58da80` (store path twice). The function
never reads or writes `+0xd0`. Sole caller in the image: `0xa40851` inside
`DisplayDebugMessage` (`0xa407d0`, entry #12), passing `3.0f`
(`0x40400000`). What the float means and what `0x58da80` do remain unknown;
"message dwell timer" is an unproven gloss. Full record with provenance:
`$WGRD_ARTIFACTS_DIR/frameclock-lua-20261119/aaee10-truth-table.md`.

## 5. Phase store / opcode-0x13 proximity (correlation, not proof)

New cross-check from retained evidence, no new capture:

- The attempt session's run 03 saw `0xab4780` fire once at deterministic tick
  **2905**, argument `0x2`, `game_started = 1`
  ([combat attempt](2026-11-03-combat-frame-capture-attempt.md)).
- run-07 (SHA-256 `acb8ecdc9f264c2784590180e1b316822a3ade6db13cd3c4969c9046f90d6f21`,
  hash re-verified) contains exactly one `phase_change_candidate` pair, also
  at tick **2905** (`+0xd0` read `590b0000` enter and leave), argument `0x2`,
  joined to frames **2915–2916**; the indirect phase-manager header read
  shows `+0x0c` transition `0 → 2` between enter and leave
  ([combat frames](2026-11-03-combat-frames-captured.md)). Two independent
  playbacks of the same replay hit the same deterministic tick: the boundary
  is reproducible for this replay.
- The same replay (`abf6a5e9…`, parsed offline) has its single opcode-0x13
  event at frame **2914** and surrender (`0x02`) at 4173.
- Distance: the phase store lands **1–2 frames after** the 0x13 frame.
- Static context: phase descriptor node 18572 (`TWargameGamePhaseDescriptor`,
  `GamePhaseType=2`) is the configured next-phase type (branch-only
  `2026-11-02-aar-clock.md`, phase-change capture target section); `0x6d17e0`
  copies the raw argument to manager `+0x0c`.

This is two independent hints converging on the same boundary region, and the
phase firing reproduces across sessions. It is still correlation: no UI
observation at that instant, and the 0x13 duration match itself assumes the
0.2 s grid. H2 (battle time starts at the 0x13 frame) stays **tested, not
proven**; opcode 0x13 remains a synchro-service membership request, not a
renamed battle-start.

## 6. Trace re-verification receipts (2026-11-19, parent recomputation)

- `frameclock-20261102/run-01.jsonl` (SHA-256 `b3a60af4…4ee0`, re-hashed):
  10,965 paired `tick_step` calls, frame deltas `{0: 8576, +1: 2389}` —
  matches the capture note exactly. 99 clock samples; 4 pre-reset
  (2586..2659), 95 post-reset spanning ticks 13..2293. Joining each sample
  to its **containing tick call** (all 95 are nested children of `tick_step`,
  frame = parent's leave frame) reproduces `frame − tick = {10: 48, 11: 47}`.
  Join-convention sensitivity: joining to the last *completed* advance
  instead gives `{9: 48, 10: 47}` — an off-by-one of convention, not of data.
  The published 48/47 split uses the containing tick's leave frame. Whether
  that equals the frame index at the sample instant depends on the
  store/getter order inside the tick, which is not directly observed; the
  static tick layout (increment at `0xb349bd` before command dispatch)
  supports it. New-epoch span: 2,311 advances, frames 1..2311,
  461.77 s between first and last advance ≈ 5.00 frames/s. (The capture
  note's 4.995 frames/s uses the full 462.65 s window; the two figures
  differ only in window endpoints, both ≈5 Hz.)
- run-07: `tick_step` frame index min 0, **max 4175**. The file holds 4174
  recorded frames (0..4173); the index reaches 4175 because the manager pads
  unrecorded frames with empty payloads (`0xb35650`, static) and keeps
  ticking after EOF. "frames 0–4175" in the capture note is the observed
  index range: 4174 recorded frames + 2 post-EOF padding ticks. Impacts
  28/28 paired, `frame_correlation.status_counts = {"inside_tick_call": 28}`,
  last impact frames 4165–4166; `tick_step` 11,780 enter / 11,779 leave (the
  documented one-unpaired-enter allowance).
- AAR traces behind the release note: both traces have exactly **459**
  `clock_sample_candidate` dword `+0xd0` reads, last counter **4164**
  (trace A `wgrd-aar-combat-20261102-01.jsonl`; trace B
  `native-v3b-replay.jsonl`, 1 pre-reset read at 12102 and 458 post-reset
  from 242). Trace B additionally reads `+0xd0` twice in its one
  `phase_change_candidate` pair (enter and leave, both 2905), so an
  all-hooks count of `+0xd0` reads gives 461 for B. The release's "459
  sampled clock reads per trace" is correct under the clock-sampler
  definition; an earlier draft of this note "corrected" it to 461 by
  silently switching definitions — that correction is withdrawn
  (independent review, 2026-11-19). "Last counter 4164" means the last
  *sampled* value, not the
  playback endpoint; it is a different quantity from 4155 (last impact's
  engine seconds 831.0 / 0.2) and 4165 (state-observer end candidate, another
  session). The three values are not in conflict once labeled.

## 7. Open questions

1. Counter writer (§3, §8, §9): direct, wide-store, ResetTime, queue-family
   and sync-item-vtable envelopes are exhausted statically; each clock field
   has one runtime writer (its Python setter) plus construction zero-init,
   and both setters have zero native call sites. Remaining candidates: the
   embedded Python layer calling the setters (offline question — shipped
   script fragments, §9), or indirect writes outside the scanned envelopes
   (the census is a proximity heuristic, not a formal proof). Runtime
   discriminator: a hook on the setter `0xa41bc0` itself, under authorization
   (`0x1dbf028` is Py_None's refcount and cannot attribute calls, §10).
2. The integer 10/11 frame lag origin: constructor zero-init is the only
   static zeroing of `+0xd0`; no static reset explains the lag. Sample-specific.
3. Battle start: §5 proximity is correlation; a UI-corroborated phase capture
   would discriminate, under authorization.
4. Binding-table inventory complete: 28 modules / 271 entries, 27 installers
   verified ([inventory note](2026-11-19-binding-inventory.md)); one table
   (`0x1d7efe0`) has no located installer. Per-function semantics beyond the
   clock bindings remain unverified.

## 8. ResetTime posts a deferred token; it is not a clock writer (2026-11-19)

Worker analysis, parent-reverified against the pinned image (re-hash before
reuse; full byte excerpts: local evidence record
`~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/resettime-callee-analysis.md`).

`ResetTime` (`0xa41890–0xa41958`, plus a dead EH funclet at `0xa41924`) takes
no Python arguments (format `""` at `0x1927bdc`). Its complete global effect:

```
a418ed  e8 0e 73 ae ff      call 0x528c00        ; array-new alloc, size 0xc
a41902  e8 29 2d f3 ff      call 0x974630        ; TResetTimeHelper ctor
a41907  ff 05 28 f0 db 01   inc ds:0x1dbf028     ; Py_INCREF(Py_None)
a4190d  b8 28 f0 db 01      mov eax,0x1dbf028    ; return Py_None
```

The earlier "return-value anomaly" is resolved (§10): `0x1dbf028` is
`Py_None`, and every void binding returns it; ResetTime is no exception.
It is not a clock write.

Class identity from RTTI: TypeDescriptor `0x1e83028` =
`.?AVTResetTimeHelper@Eugen@@`, vtable `0x1984b30`, base
`TSynchronisationItemImpl<ListForIA, TSynchronisationQueue>` vtable
`0x1942a7c`. The ctor chain enqueues the item:
`0x974630 → 0x58da80 → [vtable+0xc] = 0x58e450 → 0x58b800` (list insert under
mutex into the manager at `ds:0x2006000+0x18`):

```
58e45f  c6 41 04 01         mov byte [ecx+4],1   ; queued flag
58e464  8b 0d 00 60 00 02   mov ecx,ds:0x2006000
58e46a  8d 49 18            lea ecx,[ecx+0x18]
58e46d  e8 8e d3 ff ff      call 0x58b800
```

The object is 12 bytes with no data fields, and all five virtual slots are
accounted for: dtor `0x953030`, string getter `0x51bc20`, clear-flag
`0x58e480` (`c6 41 04 00 / c3`), enqueue `0x58e450`, no-op `0x4dc2c0`. No
virtual method of this class can store into a field of another object.

Negative scan (independently recomputed): 325 instruction rows across the 11
ranges of the ResetTime envelope contain **zero** references to `+0xd0`,
`+0xd4`, `+0xd8`, `+0xdc`, `+0x98`, `ds:0x201d318`, or `call 0xa41bc0`.
`call 0xa41890` occurs 0 times in the listing (binding-only entry);
`call 0x974630` occurs twice: `0xa41902` and `0xab3fd7`.

Consequence for the writer question (§7.1): ResetTime is eliminated as a
direct or indirect writer in this envelope. Its mechanism is a data-less
ordering token posted to the synchronisation queue — the "copied pointer,
written later" shape, but the token itself cannot write. Any ResetTime-driven
reset must live in the queue-processing code; §9 identifies that family
correctly and eliminates it too. (Topology note: `0x58e310` is a member of
`IA::Eugen::TTaskLayerMovementInterpolator`, flushing that object's own item
vector — not the manager drain; the manager-side drain is `0x58dd20`.)
Hypothesis, unproven: the token is an ordering barrier that makes the game
thread perform the reset at a synchronised frame.

Open branches: `0xab3f90`, unreferenced in text, posts both
`TResetTimeHelper` and `TLoadingDoneHelper`; §9 resolves its reachability.
The queue-family analysis is complete in §9.

Reproduction:

```sh
EXE=~/.hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe
OD=/opt/homebrew/opt/binutils/bin/objdump
$OD -d -M intel --start-address=0xa41890 --stop-address=0xa41960 "$EXE"
$OD -d -M intel --start-address=0x58e450 --stop-address=0x58e486 "$EXE"
$OD -s --start-address=0x1e83028 --stop-address=0x1e83060 "$EXE"   # RTTI name
$OD -s --start-address=0x1984b30 --stop-address=0x1984b48 "$EXE"   # vtable
grep -c 'call   0xa41890' ~/REA/wgrd-131544/wgrd_131544_full.lst   # 0
```

## 9. Queue family eliminated; one runtime writer per clock field (2026-11-19)

Worker analysis, parent-reverified (full report: local evidence record
`~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/queue-drain-analysis.md`).

Topology (RTTI read back): the manager singleton `ds:0x2006000` is
`Eugen::TSynchronisationQueue`; its drain is `0x58dd20` (called from
`0x58bc91` / `0x58bf4f`). `0x58e310` belongs to
`IA::Eugen::TTaskLayerMovementInterpolator` (COL `0x1b7ac8c` →
TypeDescriptor `0x1e876ec`, name read back) and flushes that object's own
vector; `ebp = ecx` at `58e315`, so its `[ebp+…]` operands are this-relative.
The pending array `ds:0x2005fa8/0x2005fac` holds 8-byte `{item*, handle*}`
elements, LIFO; producers `0x58d5f0` / `0x58d9a9`, poppers `0x58d1c0`
(callers `7f9a54` / `7f9bb4` in the command-playback loop `0x7f98f0`) and the
inline pop in `0x58d990`; `0x58df00` only peeks and attaches a 30 s task
handle. The playback loop writes a QWORD sim-time global `ds:0x2017270`
(`7f9adb`) and `[obj+0x24]` — not the singleton clock fields.

Negative scan (independently recomputed): the contiguous unit
`0x58d000–0x58e450` (1,860 rows inclusive; the worker's 1,859 excludes the
`0x58e450` endpoint) plus 1,695 rows of one-level callees contain zero stores
to `+0xd0/+0xd4/+0xd8/+0xdc`, zero loads of `ds:0x201d318`, zero calls to
`0xa41bc0`. The three `0x98` forms in the unit are immediates
(`58d646`, `58e269`, `58e357` — payload-variant selectors), not displacements.
Adjacent false positive pre-empted: `99f99c: mov byte [esi+0xd0],al` is in
the packet-object function `0x99f8f0` (byte width, `[esi+0x20]` buffer
context), not a singleton write.

Polymorphic channel closed: of 41 `*SynchronisationItem*` COLs, 30 resolve to
vtables; the drain's dispatch slot `vfunc[2]` (`+0x8`) is `0x58e480`
(`mov byte [ecx+4],0 ; ret`) for every concrete class (spot-verified on
`TResetTimeHelper` base `0x1942a7c` and `TLoadingDoneHelper` `0x1984b10`,
identical five-slot shape). No slot of any sync-item class writes the
`+0xd0` family. One slot-5 body (`0x13125a0`,
`TSynchronisationItemSendLaunchDirectOrder`) loads the singleton read-only.

Whole-binary writer census (proximity heuristic, limitation below):

| field | runtime writer | construction zero-init |
|---|---|---|
| `+0xd0` int ticks | `0xa41bf2` in `SetDeterministicCurrentTimeInTicks` (`0xa41bc0`) — only one | `aab588: mov [ebx+0xd0],0` |
| `+0x98` float realtime | `0xa42314` in `SetRealtimeCurrentTime` (`0xa422e0`) — only one | `aab524: mov [ebx+0x98],0` |

Both setters have **zero** textual call sites in the listing (recomputed:
`call 0xa41bc0` = 0, `call 0xa422e0` = 0); they are reachable only through
the `_sysutils` PyMethodDef dispatch. `+0xd4` has two runtime byte writers
(`0xd4e8e9` sets 1 in a restore-task step, `0xbdb254` clears 0 during
phase-2 teardown — a pending-teardown latch, §10); `+0xd8/+0xdc` none.

`0xab3f90` reachability resolved: it is virtual #0 of
`IA::Eugen::TGameplayServices` (vtable `0x199acc0`, COL `0x1b91f20` →
`.?AVTGameplayServices@IA@Eugen@@`, name read back), installed by the
constructor at `aab454: mov [ebx],0x199acc0`. Zero direct callers; a bounded
indirect search over the 537 singleton-reference rows found 7 `call [reg]`
candidates, all through other objects. Address-taken, no located caller.

Limitation, stated plainly: the writer census uses a 15-row/64-byte
"register holds the singleton" proximity heuristic. It is not a formal
whole-binary proof against indirect writes: a store in a callee that received
the pointer as an argument, or an object-copy/memcpy path outside the scanned
envelopes, would be missed. The scanned envelopes are §3 (direct + wide
stores), §8 (ResetTime), this section (queue unit + callees + all sync-item
vtables). Within them, no engine writer exists.

Consequence: the observed per-tick counter advance cannot be attributed to
any native writer found so far. The coherent remaining hypothesis is that the
Python layer calls `SetDeterministicCurrentTimeInTicks` (and
`SetRealtimeCurrentTime`) itself — the setters exist precisely for script
use, and each setter name has exactly two references in the whole image: its
`PyMethodDef` slot and its own error-path push (recomputed: one push each;
zero native lookups of the bindings).

Script-layer search (2026-11-19, worker + parent verification; full report:
local evidence record `~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/script-layer-search.md`):

- The `.rdata` "Python-like fragments" recorded in the first feasibility
  probe are CPython interpreter internals, NOT scripts: `0x1624685` cPickle
  "import of module %s failed"; `0x1631ab3/ac5/b54` compile.c diagnostics;
  `0x1624f20` cPickle error `__str__` docstring; `0x16343bc` import.c
  extension table (`.py .pyw .pyc path_importer_cache`); the `System.` hits
  are NDF filenames and C++ RTTI, not a System module.
- Exhaustive exe search: zero pyc magic, zero zipimport/frozen-module/
  `PyRun_*`/`'%s.py'` markers; 1,158 nested-zlib candidates inflated to zero
  scripts. A binding-registry string block (`0x1586c74..0x1587210`) lists
  ~75 modules (`_sysutils`, `_timeinfo`, `_misc`, `_world`,
  `_script_break_point`, sip, `_ast`/`parser`/`marshal`) — the C binding
  layer, not script code.
- `NDF_Win.dat` unpacked (edat v2): 2,664 payloads, all EUG0/CNDF flag
  `0x80`, directory and per-entry MD5 verified, 44,687,262 bytes
  decompressed, concatenated sha256
  `692379d96f2c6c030c1d45119dc1776efe7caf9f4a50935a9c65bf23fbde99c9`
  (parent recomputed). Zero hits for the setter names, `ResetTime`,
  `_sysutils`, `WorldTickEnd`, `import `, `def `, `.pyc`, pyc magic, zip or
  bzip2 markers; every entry is `pc\ndf\*.ndfbin`.
- The NDF names the script infrastructure instead:
  `initialisationnonpatchable.ndfbin` +13830 `LoadPythonLib250`;
  `TClusterAddPythonPath` and `TResourceDescriptorPythonPack` (272 instances
  across 271 clusters); `clustermap.ndfbin` +16554 mounts
  `CommonData:/Python/Eugen`, `GameData:/Python/Eugen`, `EugenPatchable`,
  `EugenSolo`, `EugenTest` plus `ResourcePythonPack::Load`. The only external
  packs named are `GladPackPatchable:/ZZ_GladPatchableWin.dat` and
  `GladPackNotPatchable:/ZZ_GladNotPatchableWin.dat` (plus `DLC_1..3.dat`).
- The script corpus is NOT retained: the DepotDownloader manifest lists 625
  paths (583 under `Data\WarGame\PC`), none containing `CommonData` or
  `Python` — the original download was filtered.

Verdict: hypothesis still open, now acquisition-gated. Next discriminating
step: obtain `ZZ_GladPatchableWin.dat` / the `CommonData:/Python` tree
(authorized acquisition or authorized guest file read) and scan for the same
markers. The runtime discriminator (authorized setter-hook capture) remains
the gold standard; nothing here manufactures a runtime observation.

## 10. Determinism stubs, Py_None, and the speed mechanism (2026-11-19)

Worker analysis, parent-reverified (full report: local evidence record
`~/.hermes/artifacts/wgrd-replay/frameclock-lua-20261119/determinism-speed-analysis.md`).
All five functions below have zero call/jmp sites in the listing
(recomputed) — binding-only entries, no arguments (format `""`).

**`0x1dbf028` is `Py_None`.** Its `ob_type` pointer reads `0x1dbeea0`, whose
`tp_name` reads back "NoneType". Every void binding ends
`inc ds:0x1dbf028 ; mov eax,0x1dbf028 ; ret` = `Py_INCREF(Py_None); return
Py_None`. The 1,379 inc sites are None-returns across the binding layer, not
a call statistic with per-binding meaning. This resolves §8's return-value
anomaly and strengthens §2: the value cannot attribute setter calls even in
principle.

**The determinism/desynchro block is inert.** `RequireDeterminismFromNowOn`
(`0xa41770`) and `DontRequireDeterminismFromNowOn` (`0xa40900`) parse no
args, perform zero game-state stores (the only write is the Py_None
refcount), and return None. Same shape for `NeedDesynchroLogFromNow`
(`0xa41600`), `DontNeedDesynchroLogFromNow` (`0xa408b0`) and
`StartDesynchroLogNowIFN` (`0xa424b0`). There is no script-controllable
determinism flag behind these names in build 131544; any determinism policy
is compile-time. Scripts calling them change nothing.

**`+0xd4` is a pending-teardown latch, not a determinism flag.** Set:
`d4e8e9: mov byte [edi+0xd4],1` inside the restore-task step `0xd4e870`
(`edi = ds:0x201d318` loaded at `d4e89d`, guarded on arg == 1). Cleared:
`bdb254: mov byte [eax+0xd4],0` inside `0xbdb110`, guarded on the TS state
enum `[TS+0x14] == 2`, during a shutdown sequence that then calls
`0xd4e6c0` and jumps to `0xab49e0`. Constructor zero-init at `aab592`.
None of the five bindings touches it. (§9's census listed only the clear
site; the set site completes it.)

**Speed control is a synchronisation-queue item, not mutable state.**
`DecreaseGameSpeed` (`0xa40530`), `IncreaseGameSpeed` (`0xa40f40`),
`ResetGameSpeed` (`0xa417c0`) each `new(0x10)` a `Eugen::TChangeGameSpeed`
(RTTI TypeDescriptor `0x1e7a4e8`, name read back; vtable `0x198121c`, base
`TSynchronisationItemImpl` `0x1942a7c`) via ctor `0x94fbe0` with opcode
2 / 1 / 0 respectively (pushes verified). The ctor posts the item into the
same queue as ResetTime's token (`0x58da80 → 0x58e450 → 0x58b800`, manager
`ds:0x2006000+0x18`); the wrapper drops the pointer because the queue owns
it. The opcode lives at item `+0xc`.

Apply is deferred to the queue drain, vtable slot 5 = `0x95e430`:
opcode 0 → `0x518560` (reset), 1 → `0x50ffe0` (increase), 2 → `0x5060d0`
(decrease), each on the speed-manager instance at `0x1fce0d0` (BSS, past
.data's virtual end; getter `0x4fc470`; no RTTI — descriptive name only).
Layout used: `+0x68` float32 current factor, `+0x6c` int32 step index,
`+0x78/+0x7c` listener vector. Setter `0x519490(idx)` computes in SSE
float32: `idx >= 0 → (float)idx + 1.0f` (`addss [0x19326e8]` = 1.0);
else `-1.0f / ((float)idx - 1.0f)` (`subss` then `divss [0x1932748]` = -1.0),
single `xchg` store into `+0x68`, then listener fan-out on change.
Increase caps at 100.0 (`0x1932738`), Decrease floors at 0.01
(`0x19326d8`), constants read back. Reset ⇒ index 0 ⇒ 1.0; Increase steps
2.0, 3.0, …; Decrease steps 0.5, 0.333…, 1/(1−i). The branches are not
symmetric inverses: from a negative index, one Increase returns to 1.0, not
to the previous slow value.

Replay consequences (static, not runtime-observed): speed changes are part
of the ordered simulation stream — a replay's speed trajectory must be
reconstructed by replaying the queue items, not by reading a load-time
field; the manager is process-global and zero-filled at load. Whether the
drain is tick-locked (a mid-tick speed item landing next tick) is unproven.
The listener fan-out reaching the tick stepper is inference, not proven —
no direct `+0x68` reader outside the manager was found in a bounded grep.
Nothing in the five functions touches `+0xd0`, `+0x98` or `+0xd4`.

## Reproduction

```sh
EXE=~/.hermes/artifacts/wgrd-replay/game/win64/WarGame3.exe
shasum -a 256 "$EXE"   # must equal 5eaa6d61...efc75d
OD=/opt/homebrew/opt/binutils/bin/objdump
$OD -d -M intel --start-address=0xa42790 --stop-address=0xa427e0 "$EXE"
$OD -d -M intel --start-address=0x1537830 --stop-address=0x15378d0 "$EXE"
$OD -s --start-address=0x1dcba88 --stop-address=0x1dcbae8 "$EXE"
$OD -s --start-address=0x1d9cc78 --stop-address=0x1d9cfb8 "$EXE"
```

Worker outputs and parent excerpts (private, outside Git):
`$WGRD_ARTIFACTS_DIR/frameclock-lua-20261119/` (worker reports, `static/`
objdump excerpts, truth table, `candidates.json`, `worker-d/` wide-store
scan outputs). Trace recomputation used the hash-pinned traces above; no new
capture was produced.