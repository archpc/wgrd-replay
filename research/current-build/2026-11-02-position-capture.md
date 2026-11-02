# Owner-position capture — V3 experiment, build 131544

Follow-up: the original engine subsequently exercised this candidate. See the
[completed capture and reviewed exporter](2026-11-02-position-aar.md). The offline
status and "not yet sampled" statements below describe preparation of the experiment,
not its current execution status.

Status: **offline instrumentation revision**. No target process was attached, no
guest was operated, no game memory was written, and no game function was called.
The only runtime evidence in this note is the previous capture; everything new
here is static bytes plus a Node simulation of the capture helpers.

| Item | Value |
|---|---|
| Config | `instrumentation/aar-capture-131544-v3.json` |
| Capture script | `instrumentation/hooks.js` |
| Controller | `instrumentation/wgrd_frida.py` |
| Tests | `tests/test_frida_scope.py`, `tests/frida_scope_sim.js` |
| Binary | `game/win64/WarGame3.exe`, SHA-256 `5eaa6d61…9efc75d` |
| Static source | `aar-20261102T050816Z/run/combat-causality-and-position.md` |

## 1. What V3 adds

V3 is V2 plus one bounded primitive: an indirect read may clear tag bits and add
a fixed offset **before** the final read. It is configured only through
`indirect_mask` (32-bit hex string) and `indirect_offset` (integer `0..0x1000`),
and both are rejected on non-indirect reads. No other hook behavior changes.

New capture points (existing reads retained):

| Hook | Read | Phase | Sampling |
|---|---|---|---|
| `owner_lookup_candidate` `0xc52de0` | `retval+0x28` 128 B indirect (descriptor) | leave | 1/997, unscoped |
| `owner_lookup_candidate` | `retval+0xE4` 12 B indirect, mask `FFFFFFFC`, offset `0x30` | leave | 1/997, unscoped |
| `clock_sample_candidate` `0xaaedf0` | `ecx+0xD0` 4 B (existing clock word) | enter | 1/997, unscoped |
| `owner_destroy_candidate` `0xa75c70` | `ecx+0xE4` 12 B indirect, mask `FFFFFFFC`, offset `0x30` | **enter only** | every call |

Combat hooks (`impact_apply_candidate`, `destruction_check_candidate`) keep
`sample_every: 1`, so the recorded `+0x1ec` deterministic timestamp and exact
impact timing are unchanged. `order_request_wrapper`, `reference_remap`,
`reference_lookup`, `frame_apply_candidate`, `phase_change_candidate` are
carried over unchanged, including the `within` scopes that keep the reference
hooks inside the order wrapper.

## 2. Static chain, byte-verified in the pinned PE

Address translation used below: RVA = VA − `0x400000`; file offset =
`0x400` (`.text` raw start) + RVA − `0x1000`.

Getter `0xa72770` (13 bytes, `objdump -d -M intel`):

```
a72770  8b 81 e4 00 00 00   mov eax,[ecx+0xe4]
a72776  83 e0 fc            and eax,0xfffffffc
a72779  83 c0 70            add eax,0x70
a7277c  c3                  ret
```

Consumer at `0xc9bc7b` (distance from an owner to a world point):

```
c9bc7b  8b 81 e4 00 00 00   mov  eax,[ecx+0xe4]
c9bc81  83 e0 fc            and  eax,0xfffffffc
c9bc89  f3 0f 10 48 34      movss xmm1,[eax+0x34]
c9bc8e  f3 0f 10 50 30      movss xmm2,[eax+0x30]
c9bc93  f3 0f 10 40 38      movss xmm0,[eax+0x38]
```

Destroy branch at `0xc9c014` (spawn/effect at the victim position), same mask
and `+0x30` base:

```
c9c014  8b b7 e4 00 00 00   mov esi,[edi+0xe4]
c9c01e  83 e6 fc            and esi,0xfffffffc
c9c021  83 c6 30            add esi,0x30
```

So the read V3 performs is exactly:

```
tagged = *(uint32*)(owner + 0xE4)
base   = tagged & 0xFFFFFFFC
vec    = *(float32[3]*)(base + 0x30)   // x @ +0x30, y @ +0x34, z @ +0x38
```

`block+0x70` (`0xa72770`'s return, the `0xa72770`/`0xae4960` seed) is **not**
read as position: the prior static report shows it is normalised, scaled and
used to generate a point along a direction, with a `(1,0,0)` degenerate
fallback. `0xa727a0` is an integer table lookup, not a transform.

Consumer-byte verification was done before writing the labels above:

```
objdump -d -M intel --start-address=0xa72770 --stop-address=0xa7277e  WarGame3.exe
objdump -d -M intel --start-address=0xc9bc7b --stop-address=0xc9bc9a  WarGame3.exe
objdump -d -M intel --start-address=0xc9bff0 --stop-address=0xc9c030  WarGame3.exe
```

All three excerpts matched the bytes quoted here and the report's claims.

## 3. Capture semantics and audit fields

For an indirect read with a mask/offset, a reached indirection branch adds four
audit fields. An earlier source-pointer refusal retains the baseline error shape;
failed steps can leave null/default audit values. The configuration remains the
authority for requested mask/offset values:

| Field | Meaning |
|---|---|
| `raw_pointer` | pointer value read from the slot, before masking |
| `applied_mask` | canonical `0x` + 8 lowercase hex digits, or `null` if none |
| `target_offset` | integer added after masking (`0` if none) |
| `final_target` | `(raw_pointer & mask) + offset`, or `null` on failure |

`chain` still lists the pointer values read at each hop; `target` is the final
address actually sampled, and `result` is the byte read. Reads without
`indirect_mask`/`indirect_offset` emit the same record shape and values as V2.

Bounds checks, in order:

1. source pointer null and initial `address < pointer` (overflow) — unchanged;
2. the 4-byte pointer slot must be fully readable before `readPointer()`;
3. a masked (or offset) pointer that is null fails closed as
   `masked target is null` — address 0 is never read;
4. `masked + offset` must not wrap (`target offset overflow`);
5. the final span is read only through `hexBytes`, which requires the whole
   range inside one readable range and catches faults.

`second_indirect` still works, with the mask/offset applied only at the last
hop. No `NativeFunction`, no game calls, no writes, no new engine flags.

## 4. Time and lifetime caveats

* Impact events retain the recorded per-impact deterministic timestamp. A nested
  destruction can reference its parent impact; it does not independently sample
  the native clock at the moment of destruction.
* `owner_lookup_candidate` and `clock_sample_candidate` are unscoped at 1/997 to
  bracket sparse movement samples without inventing timestamps. A position time
  is a **bracket** between clock samples unless an impact witness is exact.
* `owner_destroy_candidate` samples `+0xE4` on **enter only**; the owner is
  being torn down, so a leave-phase read is lifetime-unsafe and is not done.
* A readable mapping is not proof of allocation lifetime: any sampled block can
  be recycled between the pointer read and the float read. The capture records
  addresses so such cases can be discarded later; it cannot prevent them.

## 5. Offline verification (actual run)

```
$ node tests/frida_scope_sim.js
WGRD_SCOPE_SIM_OK

$ python3 -m unittest tests.test_frida_scope -v
Ran 10 tests in 0.036s
OK
```

The fixture covers: legacy record shape for unmasked reads, `0x2003` masked to
`0x2000` plus `0x30`-style offsets (`0x2003` → `0x2004` with mask
`FFFFFFFC`/offset 4), a mask that clears the pointer failing closed, scope
filters and stack discipline unchanged. `PositionCaptureConfig` validates the V3
file with the production `validate_config`, checks all ten hook VAs are
file-backed in the pinned PE, checks the revision marker
`####SVNREVISION####0000131544####SVNREVISION####`, and checks the 997 sampling
and enter-only destroy read.

Lead integration additionally reproduced and fixed a portability defect: a missing
private PE used to skip config and Node checks as well. Only the image-byte test
may now skip; the normal config/simulation tests still run. The PE path is optional
via `WGRD_ENGINE_PE`, otherwise resolved under the current home directory. A
permanent regression checks this policy without requiring the private asset.

Final lead run: 313 full-suite tests, two existing corpus skips. The focused
no-private-PE run executed 11 tests with only its one image-byte skip. Source and
configuration checks passed; none of these is a live-engine position validation.

## 6. Not claimed

* The `owner+0xE4` chain is a **static candidate**. It has never been sampled at
  runtime; the V3 run is what tests it.
* The three floats are world-space position per four consumers, but they are not
  asserted to be metres, to be the visual centre, or to match any UI coordinate.
* The owner resolved in this path is the queued damage record's "other party".
  Nothing here identifies a player, a shooter, or a weapon.
* Sampling every 997th call can miss short-lived owners entirely; absence of a
  sample is not evidence of absence of movement.
* No claim is made about `block+0x70` or `0xa727a0` as position/transform.

## 7. Running later (not done here)

```
python instrumentation/wgrd_frida.py \
  --config instrumentation/aar-capture-131544-v3.json \
  --output /absolute/path/outside/repo/wgrd-aar-position-<ts>.jsonl \
  --seconds 90 --event-limit 20000 \
  --hook owner_lookup_candidate --hook clock_sample_candidate \
  --hook owner_destroy_candidate
```

The controller still requires the live image SHA and revision marker to match,
and it rejects output paths inside the repository. A separate AAR parsing pass
is required after a real capture; it is not part of this change.
