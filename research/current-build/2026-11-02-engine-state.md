# Revision 131544: bounded multi-field engine state observer

Status: static facts re-verified against the pinned image; corrected observer integrated
in the canonical `~/Code/wgrd-replay/` checkout. The first expanded guest baseline
now disproves the earlier `GameStarted => ingame` classification; see the live
correction below. Replay identity and movement capture remain separate gates.

## Replay-watch RPC integration correction

The first real `--replay` invocation failed before hook installation:
`unable to find method 'installReplayWatch'`. Python Frida converts snake-case
export attribute access to camelCase RPC names. The JavaScript exports had been
snake_case; the local simulation had bypassed that conversion. Exports are now
`installReplayWatch` / `replayWatch`; Python call sites retain their normal
snake-case API. A runtime-export-name regression failed before this correction.

Private `replay-open-window-01.jsonl` retains that failed attempt, SHA-256
`3db760624ef8a762b9b49c98b9e7f68f9aa1b9026a28e072579d16947346f86c`.
The guard sent no UI input. Subsequent real watcher windows installed and
completed with a cleanup terminator. Windows 03, 04 and 05 did not observe the
exact target path; they do not authenticate playback identity. Three Parallels
background-exec transport failures did not start Python or create a trace;
a task-owned bounded Python subprocess worked without changing VM settings.

## Live main-menu counterexample

Fresh process 4844 (same pinned PE SHA-256 below) showed the main-menu labels
`Solo`, `Profile`, `Options`, `Quit` while `GameStarted=1`, `EndGameAsked=0` and
`GameEnded=0`. Its deterministic counter advanced at approximately five ticks per
wall second. Neither the flag nor counter motion therefore proves battle/replay
activity. A non-null replay-controller candidate and loading object were also
present at this menu; they remain presence observations only.

Evidence under private `aar-v3-20261102T082918Z/`:

- `baseline-screen.png`, SHA-256
  `3d7d9c471ba39fedabd0cb963b3e68fe668a68a107e387860cdda6bfc0c8e26b`.
  Only locally allowlisted UI-label pixels were sent for visual inspection;
  profile and chat data stayed masked.
- `baseline-state.jsonl`, SHA-256
  `c11ce6335409d822d8e2362f05e688f11e95d979c9330bafeea07d050e2431aa`,
  eight complete records including four samples and a cleanup terminator.
- `main-menu-gate-02.jsonl`, SHA-256
  `4568428b0d6c3b0f35d21485aa5f75108148f9f04bf83146e6d8b13e19f0c4fa`:
  corrected guest observer, 13 samples, `engine_state=game_started`, raw flag true,
  and `--expect ingame` exits 3 (unknown). The original 0.2-second trial produced
  only one sample because preflight consumed the budget; that trial is not counted
  as a verified predicate result.

Correction: the started lifecycle label is now `game_started`, not `ingame`.
`--expect ingame` remains accepted for CLI compatibility but fails closed as
unknown, like the uncalibrated outgame/loading predicates. Use
`--expect engine_game_started` only to wait for the named raw lifecycle flag;
it does not authenticate the current screen. This supersedes earlier classification
wording in this report without changing the preserved raw captures.

The previous process 1444 exited during preparation. The guarded input helper
refused its stale PID, and no input was sent. The replacement process was
re-hashed and rebound; the two process epochs are not merged. No snapshot was
restored. Saved VM state is an OS/tooling checkpoint, not a reusable live-game
baseline: the user confirmed Wargame must be relaunched for usable rendering.
Pause/menu/browser calibration remains unverified; the predicates below keep it explicit.

Target: `game/win64/WarGame3.exe` under the external artifact root, PE32
image base `0x400000`, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`
(re-checked in place with `shasum -a 256`). All addresses are module VAs.

Observer: [state_observe.py](../../instrumentation/state_observe.py).
Tests: [test_state_observe.py](../../tests/test_state_observe.py); the Frida read-API
simulation is embedded there so the change stays inside three files.

## 1. Correction to the earlier AAR engine-signal note

The earlier `ui-engine-signals.md` claimed `static object 0x1fce0d0 + 0x68` was
"current simulation time (s)". That is wrong. `0x519490` computes a **speed
factor** and stores it at `+0x68`:

```
519493: 8b 41 68              mov eax,[ecx+0x68]
5194a8: 66 0f 6e c8           movd xmm1,eax
5194ac: 0f 5b c9              cvtdq2ps xmm1,xmm1      ; signed step -> float
5194af: 85 c0                 test eax,eax
5194b1: 78 14                 js 0x5194c7
5194b3: f3 0f 58 0d e8 26 93 01  addss xmm1,[0x19326e8]  ; +1.0
5194c5: eb 1e                 jmp 0x5194e5
5194c7: f3 0f 5c 0d e8 26 93 01  subss xmm1,[0x19326e8]  ; step-1
5194cf: f3 0f 10 05 48 27 93 01  movss xmm0,[0x1932748]  ; -1.0
5194d7: f3 0f 5e c1           divss xmm0,xmm1          ; -1/(step-1)
5194e5: 87 03                 xchg [ebx],eax           ; ebx = ecx+0x68
```

So the durable mapping is:

| Field | Type | Meaning |
|---|---|---|
| `0x1fce0d0+0x68` | f32 | speed factor: `step >= 0 ? step+1 : -1/(step-1)` (step 0 -> 1.0, 1 -> 2.0, -1 -> 0.5, -2 -> 0.3333) |
| `0x1fce0d0+0x6c` | i32 | speed step index; **negative values are valid** (decrement stops when the factor would fall below 0.01) |

The four constants were read out of the file rather than assumed:

| VA | File offset | Bytes | Float |
|---|---|---|---|
| `0x1932738` | `0x1531338` | `0000c842` | 100.0 (upper clamp in `0x50ffe0`) |
| `0x19326d8` | `0x15312d8` | `0ad7233c` | 0.01 (lower clamp in `0x5060d0`) |
| `0x19326e8` | `0x15312e8` | `0000803f` | 1.0 (offset added/subtracted in `0x519490`) |
| `0x1932748` | `0x1531348` | `000080bf` | -1.0 (numerator in `0x519490`) |

The observer never calls `+0x68` simulation time. It reports `speed_factor` and
`speed_step`, and cross-checks the pair against the formula above at runtime; a
mismatch is reported as an uncertainty rather than silently accepted.

Reproducibility note: this PE uses the conventional RVA mapping. Its sections are
`.text` VA `0x401000` -> raw `0x400`, `.rdata` VA `0x1913000` -> raw `0x1511c00`,
`.data` VA `0x1d6b000` -> raw `0x1969000`. A VA therefore has file offset
`VA - 0x400000 - section_rva + section_raw_pointer`, e.g. `0xa42220` -> `0x641620`
and `0x1932738` -> `0x1531338`. (An earlier draft of this note claimed a shift of
`0x400000`; that was wrong and is retracted.) All instruction bytes below were
checked against the pinned file directly through this mapping.

### 1.1 Command dispatch is not a pause latch

`0x95e430` (the `TChangeGameSpeed` dispatch) selects on the *command object's*
`+0xc` and then loads `ecx = 0x1fce0d0` before calling the step functions:

```
95e433: 8b 46 0c     mov eax,[esi+0xc]
95e440: 83 e8 01     sub eax,1
95e445: b9 d0 e0 fc 01  mov ecx,0x1fce0d0
95e44a: e8 81 7c ba ff  call 0x5060d0     ; decrease
95e457: b9 d0 e0 fc 01  mov ecx,0x1fce0d0
95e45c: e8 7f 1b bb ff  call 0x50ffe0     ; increase
95e469: b9 d0 e0 fc 01  mov ecx,0x1fce0d0
95e46e: e8 ed a0 bb ff  call 0x518560     ; reset
```

`[[0x201d318]+0x3c]` is therefore a **speed-controller header whose meaning is
unresolved**; it is not proven to be the object the dispatch mutates, and its
`+0xc` dword is not a pause latch. The earlier note conflated the two because
both use offset `+0xc`. The observer reads `+0x08`/`+0x0c`/`+0x10` raw as
`speed_header_*` and makes no claim about them.

## 2. Named deterministic clock (units upgraded, origin still unknown)

The `.data` Lua binding table gives these entries (parent-confirmed, re-verified
here by disassembling the function bodies):

| Name | Table entry | fn | Reads |
|---|---|---|---|
| `DeterministicCurrentTimeInSeconds` | `0x1d9cd68` | `0xa406b0` | `[[0x201d318]+0xd0]` as int, scaled by `0.2f` in `0xaaedf0` |
| `DeterministicCurrentTimeInTicks` | `0x1d9cd78` | `0xa40780` | `[[0x201d318]+0xd0]` pushed directly |
| `SetDeterministicCurrentTimeInTicks` | `0x1d9cd88` | `0xa41bc0` | setter (never invoked by this observer) |
| `RealtimeCurrentTime` | `0x1d9cd98` | `0xa41710` | `[[0x201d318]+0x98]` as f32 |

```
a406fa: 8b 0d 18 d3 01 02  mov ecx,[0x201d318]
a40707: e8 e4 e6 06 00     call 0xaaedf0        ; cvtdq2ps [ecx+0xd0]; mulss 0.2f
a407a3: a1 18 d3 01 02     mov eax,[0x201d318]
a407a8: ff b0 d0 00 00 00  push [eax+0xd0]      ; ticks
a41733: a1 18 d3 01 02     mov eax,[0x201d318]
a4173b: f3 0f 10 80 98 00 00 00  movss xmm0,[eax+0x98]
```

And the scale constant itself:

```
aaedf1: 66 0f 6e 81 d0 00 00 00  movd xmm0,[ecx+0xd0]
aaedfc: f3 0f 59 05 68 d7 95 01  mulss xmm0,[0x195d768]   ; 0.2f (cdcc4c3e at file 0x155d368)
```

Implications, stated narrowly:

* `TS+0xd0` is the engine **deterministic clock in ticks**, not an anonymous
  counter, and `TS+0x98` is the engine realtime clock in seconds.
* `deterministic_seconds = ticks * 0.2`. A 10-tick/s observation therefore means
  the deterministic clock advances 2 s per wall second; this note draws no
  conclusion about epoch, playback rate or replay-frame mapping.
* Origin/epoch is **unresolved**. Nothing here shows the tick counter starts at
  zero on replay load or maps 1:1 to replay frames; the earlier 4165-vs-4173
  endpoint coincidence remains unfitted.

## 2.1 Lua wrapper address errata (checked against the pinned .data table)

The earlier `ui-engine-signals.md` gave the wrong `SetNextGamePhase` wrapper. The
`.data` binding table settles it, and each address below was read out of the
pinned file (conventional RVA mapping):

| Name | Table entry | String | Wrapper fn | Evidence |
|---|---|---|---|---|
| `SetNextGamePhase` | `0x1d9ce18` | `0x1d9ca7c` | `0xa42220` | entry `{0x1d9ca7c, 0xa42220, 1}`; `a42271: 8b 0d 18 d3 01 02` (`ecx = [0x201d318]`); `a4227e: e8 fd 24 07 00` -> `0xab4780` |
| `GameStarted` | `0x1d97b38` | - | `0xa313b0` | `a313d3: a1 18 d3 01 02; 8a 40 20` |
| `GameEnded` | `0x1d97b58` | - | `0xa31360` | `a31383: a1 18 d3 01 02; 8a 40 22` |
| `EndGameAsked` | `0x1d97b78` | - | `0xa30fc0` | `a30fe3: a1 18 d3 01 02; 8a 40 21` |
| `GetOutgameChapter` | `0x1d9cf18` | - | `0xa40ef0` | `a40f13: a1 40 4a 02 02; a40f18: ff 70 74` -> `[0x2024a40]+0x74` |
| `RequestEndLoadingPhase` | `0x1d99ea0` | - | `0xa3abc0` | `+0xc8` read at `a3ac19`, **inside** this function |

Retractions:

* `0xa3a0a0` is not the `SetNextGamePhase` wrapper entry (it starts mid-function,
  `ff ff ff e8 ...`), and `0xa3a0e9` is not a call site. Both claims are dropped.
  The underlying `0xab4780 -> 0x6d17e0` phase store remains correct.
* `0xa3ac19` is an instruction address inside `RequestEndLoadingPhase`, not a
  named wrapper entry; the loading read is verified as bytes, not as a binding.
* The flag getter addresses are verified through the table entries above; the
  earlier note's blanket byte-verification claim for every wrapper is still not
  accepted, so any address not listed in this table stays a **raw candidate**.

## 3. Completion flags (independent of any counter)

Three adjacent bytes on the services object, read by name-bound getters:

```
a31383: a1 18 d3 01 02  mov eax,[0x201d318]
a31388: 8a 40 22        mov al,[eax+0x22]      ; GameEnded
a313d3: a1 18 d3 01 02  mov eax,[0x201d318]
a313d8: 8a 40 20        mov al,[eax+0x20]      ; GameStarted
a30fe3: a1 18 d3 01 02  mov eax,[0x201d318]
a30fe8: 8a 40 21        mov al,[eax+0x21]      ; EndGameAsked
```

`GameEnded` is a completion signal in its own right. It is **not** a
stationary-counter inference, and the observer keeps the two separate:
`independent_completion` comes only from the byte.

Flag bytes are validated as `{0,1}`. Any other value yields
`engine_state = invalid_flags` and a non-zero exit in wait mode; the observer
does not coerce it to a boolean.

## 4. Other read fields and what they do *not* prove

| Field | Proven | Not proven |
|---|---|---|
| `[0x201d318]` | pointer slot; RTTI `.?AVTGameplayServices@IA@Eugen@@` | - |
| `TS+0x34` | pointer read by `61f570` (`8b 41 34; c3`); called from several UI paths | that it is the replay controller, or that non-null implies replay UI |
| `TS+0x38` | phase manager; `ab4780: 8b 49 38; jmp 0x6d17e0`, target writes `[ecx+0xc]` | the mapping from `+0xc` to a screen name |
| `TS+0x3c` | pointer returned by `59d220` (`8b 41 3c; c3`) | any semantics; the `+0xc` dword is **not** a pause latch |
| `TS+0x5c` | network object; `a3a688: 8b 40 5c` then `mov al,[eax+0xa4]` (dedicated-server flag) | that `+0xa5` on this object is `IsReplay` |
| `[net+0xc8]` | loading-phase object presence; `a3ac19: 8b 81 c8 00 00 00; test eax,eax`, an instruction inside `RequestEndLoadingPhase` (`0xa3abc0`) | lifecycle; the object could exist outside a load, so presence is not a loading *state* |
| `[[net+0xc8]+0xc]` | loading phase index, incremented in `RequestEndLoadingPhase` | index -> named phase |
| `[0x2024a40]+0x74` | outgame chapter id (binding `GetOutgameChapter`) | anything else about `TManagerIA` |
| `[0x2022844]` | dword passed as the **context argument** to the Lua-arg resolver `0x1546430` (`pushl 0x2022844`) | that it is a live replay-browser object, or that non-null implies the browser screen |

### 4.1 Phase id is an enum, not a descriptor-list index

The earlier note read `TGamePhaseManagerDescriptor` as supplying a descriptor
list whose *index* lands in `+0xc`. Native NDF parsed with the committed reader
shows the descriptors carry a `GamePhaseType` enum instead (`GamePhaseType=2` ->
`TWargameGamePhaseDescriptor`, type `1` -> `TDeploiementGamePhaseDescriptor`, and
the strategic manager listing types `5/3/4`). So `+0xc` is most likely a
`GamePhaseType` value, not a position in a list; the enum-to-screen binding is
still not established and no static name is claimed for any value. The observer
emits `phase_id` as a **raw integer** and `--fingerprint` matches that raw value;
a value becomes meaningful only after a runtime capture ties it to a screen.
Only selected private NDF objects were consulted, not full NDF data.

`IsReplay` caveat (this is the important one): `0xa38840` reads `+0xa5` from the
object returned by `0x1546430`, whose context is the global `0x2023674`, not
`[[0x201d318]+0x5c]`:

```
a3884f: ff 35 74 36 02 02  push [0x2023674]
a38868: e8 c3 db b0 00     call 0x1546430
a38874: 8b 44 24 04        mov eax,[esp+4]
a38878: 8a 80 a5 00 00 00  mov al,[eax+0xa5]
```

The identity of that object with the `TS+0x5c` object is a runtime property, not
a static one. `net+0xa5` is therefore reported as
`replay_net_flag_candidate`. `--replay-field` only selects a raw candidate for
reporting; it does not validate a replay state. `replay_active` remains unknown.

`0x2022844` is also unresolved: both `ReplayController_Create` (`0xa27240`) and
`ReplayController_SetVisibility` (`0xa27450`) pass its *value* to the resolver,
and the instance whose method is then called comes from a resolver out-parameter
(`mov ecx,-0x18(%ebp)` / `-0x1c(%ebp)`), not from the slot itself. A null slot is
therefore consistent with "binding will fail", but a non-null slot does not prove
a browser is open.

## 5. Observer contract

State reads use fixed bounded spans: at most `0x100` bytes per read and `0x200`
bytes per sample, with a planned total of `0x16c` (364 bytes):

* `[0x201d318]` (4) then `TS+0x00..0xff` (256), retaining the original raw prefix
* `0x1fce0d0+0x68` (8) - speed factor + step
* `0x195d768` (4), retaining the original loaded scale-byte check `cdcc4c3e`
* the four clamp/offset constants (4 x 4)
* `[TS+0x38]+0xc`, `[TS+0x3c]+0x08..0x13`, `[TS+0x5c]+0xa0..0xcb`, `[[net+0xc8]+0xc]`
* `[0x2024a40]` then `+0x74`, and `[0x2022844]`

Read-only qualification: the state observer installs **no** interceptors (the only
interceptor in the script is the optional `CreateFileW` open watch in §6, present
only when `--replay` is passed), calls no engine functions and writes no target
memory. The watch never calls a target API itself.

Each read is checked against one readable mapping before it happens; a span that
would cross a mapping edge is refused instead of truncated. Failures are recorded
per field (`reads.<name>.error`), so an unreadable sub-object still yields remaining
evidence. The retained clock-scale identity guard is intentionally fatal if the
loaded constant is unreadable or mismatched; its failure is not interpreted as time.
The original signed `counter`, `counter_hex`, `scale_hex`, 256-byte prefix and
`counter_sample` event name are preserved.

Derived values:

| Output | Source | Confidence |
|---|---|---|
| `engine_state` | named flag values + read errors | raw engine lifecycle only, not a UI screen |
| `independent_completion` | `GameEnded == 1` | high |
| `loading_object_present` | `[net+0xc8] != 0` | medium (presence only; `--expect loading` stays unknown until calibrated) |
| `speed_factor` / `speed_step` / `speed_consistent` | `0x1fce0d0` + verified formula | high for the formula, no time semantics |
| `engine_named_time` | `TS+0xd0`, `TS+0x98`, f32 scale `0.2f` | units high, origin explicitly `unknown` |
| `deterministic_seconds` | `f32(int32(TS+0xd0) * f32(0.2))` (reproduces `0xaaedf0`; 4165 -> `833.0`) | arithmetic high, origin `unknown` |
| `replay_active` | not yet authenticated | remains `null`, including with `--replay-field` |
| `pause_state` | none | always `not_determined` |
| `ui_outgame_substate` | optional caller-supplied raw fingerprint | labelled `caller_supplied_raw_fingerprint`, not engine-verified |

Fingerprint labels require all three fields to be present and correctly typed in
both the observation and configuration. Missing phase/context reads do not match
null configuration fields. A memory-range check is not an allocation-lifetime
proof, and separate reads are not an atomic engine snapshot.

Fail-closed rules:

* `[0x201d318] == 0`, **read-proven** -> `engine_state = no_gameplay_services`,
  exit 0 if that is what was expected. This is an answer, not an exception and
  **not** "menu". `ts_present` is tri-state: `false` only for a successfully read
  NULL slot, `null` for an unreadable or implausible slot.
* An unreadable/implausible slot is `unreadable`, never `no_gameplay_services`.
* `GameStarted == 0` yields `not_started`, not outgame or main menu: loading may
  also clear that flag. `--expect outgame` remains undecidable.
* unreadable services prefix / non-boolean flags / `GameEnded` with
  `GameStarted == 0` -> state is uncertain and the process exits `3`.
* Uncertainty seen in an earlier poll is recorded in
  `earlier_uncertain_states`; the **final** observation governs the exit code.
* `stable_counter` is reported as `stationary_counter` only. It never becomes
  `pause_state`, because a finished replay, a loading stall and a pause all look
  identical without a witnessed input.

CLI (superset of the previous observer, which keeps `--pid`, `--output`,
`--samples`, `--interval` and `--expect stable_counter|advancing_counter`):

```
--expect {stable_counter,advancing_counter,engine_game_ended,engine_game_started,
          no_gameplay_services,outgame,ingame,loading,replay_active}
--timeout 10          # condition-wait budget, hard-capped at 30 s
--replay-field none   # net_a5 | controller: raw candidate reporting only
--fingerprint FILE    # observed {chapter_id, phase_id, ui_binding_context_present} -> name
```

Wait mode polls until the predicate is true or the time budget expires, then
exits `0` (matched), `2` (not matched) or `3` (state could not be decided). No
screenshot or UI inference is part of the gate. `outgame`, `loading` and
`replay_active` are deliberately undecidable until supported; they cannot yet
drive a complete menu/browser/loading sequence. Polling sleeps only schedule the
bounded observations and do not establish a state by themselves.

## 6. Optional replay-open identity (native, read-only)

`--replay PATH --replay-sha256 HASH` (default pin
`abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121`) adds one
interceptor on `CreateFileW` inside the selected game process. The target file is
hashed before the run (and must equal the pin) and hashed again afterwards.

* Export discovery: `Module.getExportByName(null, "CreateFileW")`, then
  `Process.getModuleByName("kernel32.dll")`. If neither resolves, the observer
  records `watch_installed=false` plus the concrete error and leaves replay
  identity unknown. It does not fall back to a generic file-I/O subsystem.
* ABI: `CreateFileW(lpFileName, dwDesiredAccess, dwShareMode,
  lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes)`, so the
  observer reads `args[0]` (path), `args[1]` (access), `args[2]` (share) and
  `args[4]` (disposition). `args[3]` is security attributes and is not recorded.
* Path read: at most `1024` bytes, clipped to the tail of the one readable mapping
  that holds the pointer (`Process.findRangeByAddress`, then `readByteArray`), and
  rounded down to a whole UTF-16 unit. A NUL inside that span is **required** and
  decoding stops at it; an unterminated or cross-mapping path is refused
  (`path_read_errors`) rather than silently shortened.
* Matching: the path is normalized (`/` -> `\`, duplicate separators collapsed,
  lowercased) and compared with the normalized **full** target path. Only an exact
  full-path match is retained, as `match=path`; there is no basename fallback, so
  a same-named file in another folder is a non-match and its path is neither
  retained nor transmitted.
* Retention: only matching opens are stored (max 32 events). Non-matching opens
  increment `other_open_count` and their paths are never retained.
  `matching_open_attempts`, `dropped_events`, `truncated`, `path_read_errors` and
  the invalid-handle counter remain available after retention fills. The persisted
  verification includes read-error/capacity metadata and `observation_complete`;
  no retained event does not prove no matching file was opened.
* Per invocation: the pending record lives on the interceptor's per-call `this`,
  not in module state, so interleaved opens each keep their own path/access/
  share/disposition and `onLeave` consumes only its own record.
* Per event: requested path, `dwDesiredAccess`, `dwShareMode`,
  `dwCreationDisposition`, thread id, entry timestamp, return address, and
  `handle`/`valid_handle` from the `onLeave` return value. `0` and `0xffffffff`
  are invalid handles; an event with an invalid handle is a failure, not a match.
  `--backtrace` adds up to 8 fuzzy return addresses.
* Result: `replay_open.verified` requires a valid-handle open **and**
  `sha256_before == expected == sha256_after`. `--require-replay-open` turns an
  unverified result into exit `3`.
  That flag without `--replay` is rejected before attachment. A verified open
  establishes one matching file-open observation with stable before/after hashes,
  not authenticated replay playback or complete file-I/O coverage. Path reads have
  a separate per-call 1024-byte limit; the state-sample budget is not an aggregate
  limit over every file-open callback.

`CreateFileA` and `NtCreateFile` are concrete candidates but are **not**
implemented here; a replay opened through either would be missed and the result
would say `observed=false`, not "no replay was opened". UI selection, the
`0x2022844` context and the `IsReplay` byte are all weaker than this evidence and
remain unchanged in meaning.

## 7. Open items for the runtime pass

0. Phase id: observe `ab4780` and its raw phase argument, `TS+0xd0` and
   `[TS+0x38]` indirectly. Test whether a `1 -> 2` transition occurs and where it
   falls relative to the battle clock. Do not assume opcode `0x13` establishes it.
1. One capture per screen: main menu, replay browser, loading, playing, paused,
   finished. Record `{game_started, game_ended, phase_id, chapter_id,
   ui_binding_context_present, loading_object_present, speed_factor, speed_step,
   ticks}`. A caller fingerprint is a labelled observation aid, not a verified
   outgame gate; require independent screen evidence before using a UI classifier.
2. `replay_active`: capture `net+0xa5` and `TS+0x34` in browser versus playing
   states. Candidate selection does not authenticate their semantics; a validated
   replay classifier remains future work.
3. Pause: needs a witnessed input plus a repeated stationary window; the
   observer deliberately has no pause predicate yet.
4. Deterministic-clock origin: 4165 ticks vs replay last frame 4173 is still an
   unverified endpoint fit; do not present it as a frame mapping.
5. Replay identity: confirm that the engine opens the authenticated file through
   `CreateFileW` at all. If the capture shows `other_open_count` growing while
   `events` stays empty, add `CreateFileA`/`NtCreateFile` as explicitly reviewed
   candidates rather than widening the hook blindly.

## 8. Evidence hashes

Static excerpts retained under `$WGRD_ARTIFACTS_DIR/aar-20261102T050816Z/static/`
(SHA-256):

| File | SHA-256 |
|---|---|
| `clock-speed-increment.asm` | `12c3f8e2ae166ea7759f3e949cd34ccfa02e53a433f59bc65e714b9959e2b8c4` |
| `clock-speed-decrement.asm` | `6061434beeb9533b680e2630b8d3e080ae1dc7f68fd5701cc38d530ead5d8613` |
| `clock-speed-reset.asm` | `a983165fd5d9838a6e438c8862a4ff911d56e6c4d4827680b5f833434d0b554a` |
| `clock-speed-step-apply.asm` | `0c1833a2bc1d303f0384d813fe947e6d2bd68b6fc3b71cf920eaf7577d404a4c` |
| `deterministic-clock-bindings.asm` | `b0e2177f5542710a0c8273fc76c72fa04dd14c0a1f0011d54d4aafe645dfe974` |

These retained excerpts were produced with GNU objdump on the pinned file.
All 37 quoted instruction spans in this note were independently compared with
the PE section-mapped bytes; zero mismatches. No new VM execution is claimed.

## 9. Canonical integration verification

The reviewed delegate work was integrated into `~/Code/wgrd-replay/`, not the
preserved artifact worktree. Integration rejected two remaining unsupported
inferences: a clear `GameStarted` flag is not proof of outgame, and a command-line
candidate selector is not replay-state authentication. It also retained the v1
raw fields, signed counter, loaded scale guard and event name rather than silently
changing that evidence interface.

Actual canonical run, terminal Python 3.14.10:

```sh
TMPDIR="$HOME/.hermes/cache/scratch" WGRD_UNIT_DATA="$WGRD_UNIT_DATA" \
  python3.14 -B -m unittest discover -s tests -v
```

Pre-review result: 301 tests, exit 0, two private-corpus skips. The 42-test observer module
includes the production JavaScript evaluated against the bounded Frida-API fixture:
real `CreateFileW` argument positions, interleaved calls, exact-path filtering,
refused unterminated paths, null versus unreadable slots, unknown predicates,
float32/signed clock behavior and retained v1 raw keys. This is a mechanics test,
not an original-engine guest run.

Logs: `observer-integration-red.log`, `observer-compatibility-red.log`,
`observer-canonical-focused.log`, `observer-canonical-full.log` under
`aar-20261102T050816Z/`. `observer-canonical-validation.json` pins the tested source
and test files and records the 364-byte state-read budget. The existing suite was
not rerun merely for the verification-hook notice; that limitation is already
recorded in the [runtime AAR note](2026-11-02-runtime-aar.md).

Independent review identified three demonstrated required fixes: incomplete
fingerprints could match missing reads, replay-watch refusal/truncation metadata
was dropped, and non-finite legacy floats escaped strict JSON handling. Each was
reproduced before correction. An additional regression rejects required-open mode
without a replay path. Four focused regressions failed before the fixes; all 46
observer tests then passed. The final canonical full suite ran 305 tests, exit 0,
with the same two private-corpus skips (`observer-final-canonical-full.log`).

The review's 64-bit-handle concern does not apply to this pinned target:
`wgrd_frida.verify_loaded` checks `arch == ia32` and pointer size 4 before capture.
Cleanup failures may still leave an unterminated observation; such an artifact is
incomplete and must not be treated as a completed capture. No expanded observer
or live replay-open claim is made on fixture-test evidence alone.
