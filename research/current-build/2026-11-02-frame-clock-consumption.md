# Revision 131544: replay frame consumption and the simulation tick

Status: static, read-only. No VM, no game run, no new capture. Builds on the
PR #24 structural timeline without changing its lossless event coverage.

Executable `WarGame3.exe`, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, VAs at
base `0x400000`. Ghidra 12.1.4 through the canonical REA CLI on the read-only
project clone; byte checks against the pinned file with GNU objdump 2.47.

## 0. Program identity check

The REA envelope's `existing_project.sha256` (`a93f2864…c196fd`) is not the
executable's digest. It is project/import metadata, not the loaded bytes. Byte
comparison against the pinned file settles identity:

| VA | Project bytes | Pinned file bytes |
|---|---|---|
| `0xb2b310` | `55` | `55` |
| `0xb2b343` | `e888dbaaff` (`call 0x5d8ed0`) | same |
| `0xb3363a` | `81f2efbeadde` (`xor edx,0xdeadbeef`) | same |
| `0xab4780` | `8b4938` (`mov ecx,[ecx+0x38]`) | same |
| `0xab4783` | `e958d0c1ff` (`jmp 0x6d17e0`) | same |

Five spans across four functions match exactly, and every decompiled body below
was cross-checked against `objdump -d` of the pinned file. Conclusion: the
project is the pinned 131544 image; the differing field is metadata.

## 1. Bulk frame loading is not frame execution

`TNetworkEventSourceFromReplay` (COL `0x1b99a10`, vtable `0x19a0540`) vtable
slot 1 is `0xb3ccb0`, which validates a replay header and calls the frame
reader `0xb3dbc0`. That reader walks an array at `+0xc`/`+0x10`, and for each
record reads three dwords (frame, slot, payload kind), then the payload through
`0xb285e0`, resolves the per-slot container with `0xb33620(slot)`, and inserts
with `0xb2b310(frame, payload)`.

`0xb2b310` is a keyed insertion into an 8-byte-entry map whose count/base live
at `+0x58`/`+0x5c`; it is not an apply call. The retained trace
(`native-v3b-replay.jsonl`, replay `abf6a5e9…`) observed 4176 calls returning to
`0xb3dcd2`, with keys `0..4173`, inside a 0.385 s burst before the first clock
sample. One pass, whole file, no simulation between keys.

Frame storage for the running match is the global map `DAT_02039d00`
(allocated `0x60` bytes in `0xb29d60`, the `TNetworkActionManager`
constructor).

## 2. The simulation tick consumes exactly one frame per 0.2 s

`FUN_00b34060` is the per-tick step of the same object (fields `+0x68`
accumulator, `+0x6c` frame index, `+0x7c`/`+0x80` slot array, `+0xa4`/`+0xa5`
mode bytes, matching the constructor `0xb29d60` and the reset `0xb2cfe0`).
Instruction-level path, decoded from the pinned bytes:

```
b34543  movss xmm0,[ebx+0x68]        ; accumulator (seconds)
b34548  addss xmm0,[ebp+8]           ; += frame delta
b3454d  movss [ebx+0x68],xmm0
b34710  mov  [ebx+0x68],0x3e4ccccd   ; forced tick: accumulator = 0.2f
b3472e  mov  [ebx+0x68],0x3e4ccccd   ; clamp: > 1.0f becomes 0.2f
b34735  movss xmm0,[ebx+0x68]
b3473a  comiss xmm0,[0x195d768]      ; 0.2f
b34741  jb   0xb34d8b                ; below quantum: no tick
b34758  subss xmm0,[0x195d768]       ; consume one 0.2 s quantum
b34760  mov  ecx,[ebx+0x6c]          ; current frame
b3478e  cmp  byte [ebx+0xa5],0
b34795  jne  0xb349b3                ; replay branch
...
b349b3  lea  eax,[ecx+1]
b349bd  mov  [ebx+0x6c],eax          ; frame index += 1
b349c0  call 0x13193f0               ; notify frame listener
```

`0x195d768` is the same constant (`0x3e4ccccd`, 0.2f) that `0xaaedf0` uses to
scale `[TGameplayServices+0xd0]` into deterministic seconds. One consumed tick
quantum advances the frame index by exactly one.

So: **frame N and frame N+1 are 0.2 s of simulation time apart, and each tick
applies exactly one frame.** This is a static relation between the replay frame
index and simulation time, not a division of frame count by a UI duration.

Origin: the frame counter is zeroed by the manager reset `0xb2cfe0`
(`+0x6c = 0`, `+0x68 = 0`, `+0x98 = 0`, `+0x9c = 5`) at load. Frame 0 is the
replay-load origin, not battle start.

## 3. Command release and ordering

`FUN_00b35650` (the manager's only vtable slot) prepares one tick's release per
slot: it scans that slot's frame map for the highest key, inserts the shared
empty payload `DAT_02039d00` for every missing key up to the current frame
`+0x6c`, and frees entries below it. A frame with no recorded command is
therefore an explicit empty tick, not a stall.

`FUN_00b34060` then dispatches, per tick:

- a loop over the slot array `+0x7c`/`+0x80` selecting entries whose pending
  frame equals the **relative** frame (`frame - [ebx+0xb0]`), calling the
  queue applier `[ebx+0xcc]` vtable `+4`/`+8`;
- a per-slot lookup `0x5d8ed0(&map, &relative_frame)` followed by
  `[ebx+0x8c]` vtable `+0x10`, which is the payload dispatch for that slot's
  commands.

Recorded orders become network action objects. `TNetworkActionGiveOrderStandard`
vtable slot 1 is `0xb2be30`, the observed `order_request_wrapper`. The vtable
reference was resolved through its MSVC COL `0x1b98f9c` (vtable base
`0x19a01b8`, slot 0 `0x5615d0`, slot 1 `0xb2be30` at `0x19a01bc`), so the
observed hook is the order-apply method, not a queue insert.

Consequences for interpretation, no stronger claim than the bytes support:

- All slots' commands for one frame are offered in one tick, in slot-array
  order; the file's pact order and the tick's slot order are the same ordering
  domain, but "same tick" does not prove a deterministic intra-tick order.
- `execution_outcome` stays `unknown`: the dispatch is a request path, and no
  trace observes its return.

## 4. Still unresolved, and the smallest experiment for each

1. **Writer of `[TGameplayServices+0xd0]`.** A scan of all 537 textual
   references to `0x201d318` and of all 497 stores to a `+0xd0` displacement in
   `.text` found exactly one writer: the Lua setter `0xa41bc0`
   (`mov [eax+0xd0],ecx` at `0xa41bf2`). The observed runtime advancement is
   therefore not accounted for statically. Until it is, `frame == deterministic
   tick` stays `tested_not_proven` and no battle-time origin is claimed.
2. **Battle start.** `0xab4780` (`[ecx+0x38]` phase store, `jmp 0x6d17e0`) was
   observed once with argument `0x2`. One sample is not a phase timeline, and
   opcode `0x13` is not battle start.
3. **Native event placement.** Retained AAR traces carry damage events with
   engine deterministic seconds (806.4, 806.6, 830.8, 831.0) and no frame
   field. `seconds / 0.2` gives 4032, 4033, 4154, 4155, all integral and inside
   `0..4173`. That is arithmetic consistency with §2, not proof that the damage
   clock and the frame clock share an origin. It is reported as a hypothesis.

   One bounded cross-check from the same replay: the retained trace's last
   standard order is the frame-4154 command (0x07), whose derived
   `t_from_replay_load_seconds` is 830.8, and the third lethal impact in the
   same trace carries deterministic seconds 830.8. Two independent fields agree
   on the same 0.2 s grid value while the order is being applied. This raises
   confidence that the damage clock runs on the frame grid; it still does not
   establish a shared origin or place the impact relative to the order.

Smallest experiment that closes all three, one authorized playback, one hook:

- Hook `0xb34758` (or its return, `0xb349bd`), read
  `[[0x201d318]+0xd0]` and `[ebx+0x6c]` on enter and leave, sample 1:1 for the
  first 400 ticks then stride 97.
- Hook `0xab4780` enter, read the phase argument and
  `[[0x201d318]+0x20..0x22]`.
- No new exporter, no new profile: the existing runtime-v3 read shapes cover
  both. The expected output is the tick-per-frame ratio and the tick value at
  the first battle-phase transition.

Do not write the capture config or profile before that run is authorized.

## 5. What this changes in the exported timeline

`wgrd_timeline_report.py` now carries `tick_basis` (0.2 s per frame, static,
origin = replay load) and `execution_model` (bulk load, one frame per tick,
empty-frame padding, slot-array dispatch). Each event gains
`time.t_from_replay_load_seconds = frame * 0.2` labelled
`derived_from_static_tick_quantum`. `deterministic_ticks`, `game_time`,
`battle_time` and `wall_clock` stay null. Native AAR events stay unplaced.

`tests/test_timeline_report.py` pins the new fields and re-pins the two
authentic-replay outputs.
