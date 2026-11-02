# Native hook semantics and corrected damage layout — build 131544

Status: static byte checks plus retained runtime observations. No VM operation,
game execution, binary mutation or trace rewriting in this pass.

Engine SHA-256:
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
Addresses below are VAs at image base `0x400000`.

## `frame_apply_candidate` is not a demonstrated simulation-frame apply

The existing raw hook ID is preserved for compatibility. It is a label, not a
semantic guarantee. At `0xb2b310`, the direct logic performs keyed registration
in the container at `this+0x58`:

- `arg0` (`[ebp+8]`) supplies a 32-bit key to lookup `0x5d8ed0`.
- `0xb2b34d` masks the container's count dword, not `arg0`, with
  **`0x07ffffff`**, bytes `81 e1 ff ff ff 07`.
- If lookup finds the key, `0xb2b359` branches directly to the epilogue at
  `0xb2b42f`. The function does not apply an action on this branch.
- Otherwise, `0x4e3ac0` obtains an insertion node. The routine stores a global
  value pointer when `[arg1+0x58]` is zero; the other path allocates a 0x60-byte
  object, copies that field and invokes unresolved virtual methods.
- `arg1` is dereferenced as an object pointer, not consumed as a float.
  Both exits use `ret 8` (`c2 08 00` at `0xb2b3a4` / `0xb2b440`).

This establishes the direct keyed-container role. It does not exclude effects
inside unresolved indirect callees. No simulation-clock mapping follows from
this hook's invocation count.

### Caller and observed index sequence

At `0xb3dbc0`, a loop constructs a local object at `[ebp]`, performs three
four-byte reads into `[ebp+0x74]`, `[ebp+0x60]`, `[ebp+0x58]`, then invokes
`0xb285e0` with the reader and local object. It resolves the second word via
`0xb33620`. At `0xb3dcc6..0xb3dccd`, it passes the local object's address and the
first word to `0xb2b310`; the return site is `0xb3dcd2`.

In retained trace `d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec`:

| Return site | Calls | Argument-0 sequence | Threads | Receivers |
| --- | ---: | --- | ---: | ---: |
| `0xb359b7` | 2 | 12103, 12104 | 1 | 1 |
| `0xb3dcd2` | 4174 | 0 through 4173, in order | 1 | 1 |

The second cohort occupies enter lines 10 through 8356, with no sampled clock
entries inside it. Sampling is sparse and threads differ: this recorded order
is not an atomic simulation-time observation.

The retained replay (`abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121`)
passes the existing parser's structure/digest checks. It contains 4174 `star`,
`pact` and `endt` records, with zero unknown chunks. Every stored `star` index
matches the second cohort's argument 0 in order. This is ordinal correspondence,
not proof of frame-payload equivalence, execution timing or a battle-clock origin.
The older trace's file association is not retroactively authenticated by the
later native file-open witness.

Distinct observed keys do **not** prove the receiver was initially empty, every
call took the insertion branch, or every insertion succeeded. The hook captured
no container contents or count. Duplicate-key behavior remains a static finding.

REA/Ghidra evidence records:
`ev_a9e9f708c354a0e728c81c094f7a7b8c89e5bf322b27b5c00141bf1f46d3a502`
and `ev_f49165ea8251d5fd73fc4f79032fbd7f12783ed0e705dd58ee8a2e78caab54c9`.
The parent independently checked the cited instruction spans against the pinned
PE with GNU objdump and direct byte reads.

## Damage-module loop: corrected slots and element size

All 28 impacts in the file-witnessed trace
`6d88cefc03e1cf6a9bc4a3ddb70318569789d124266a37ffea1e5f5121601617`
return to `0xc95200` and capture receiver vtable `0x19b5b08`.

- Vtable entry index 21 is `0xc95040`, therefore its byte offset is **`+0x54`**,
  not `+0xf0`. Vtable file offset: `0x15b4708`.
  PE `.rdata` RVA `0x1513000` and raw offset `0x1511c00` map that file offset
  to `0x400000 + 0x1513000 + (0x15b4708 - 0x1511c00) = 0x19b5b08`.
  A subsequent worker's linear-address alternative `0x19b4308` is rejected.
- The complete-object locator at `0x1bb56a0` has subobject offset zero and points
  to type descriptor `0x1edb610`, named
  `.?AVTModernWarfareDamageModule@IA@Eugen@@`.
- Vtable `+0x98` contains the observed apply callback `0xc9f910`.
- Inside `0xc95040`, `0xc951e9` loads that `+0x98` function, `0xc951fd` calls it
  through a stack-local pointer, and `0xc95200` is the return site. It is **not**
  an external caller of `0xc95040`.
- `0xc9582b` adds **`0x74`** to the entry offset (`83 c1 74`). The inline span
  `0x15c` is three such entries, not one entry's stride. The loop reads the count
  at container `+0x164` and the overflow pointer at `+0x160`.
  The aliases are explicit: `0xc950c1` loads the first argument into EDI,
  `0xc950c4` reads `[edi+0x164]`, and `0xc9510a` reads `[edi+0x160]`.

The apply-call argument preparation is directly visible:

| Apply argument | Origin in this loop |
| --- | --- |
| 0 | float at entry `+0x68` |
| 1 | result of `0xb00690` lookup of entry `+0x08` |
| 2 | raw value at entry `+0x10` |
| 3 | entry pointer itself (`push edi`) |
| 4 | raw dword at entry `+0x70` |

The native capture reads owner snapshots through arguments 1 and 2; it does not
capture argument 3's complete entry bytes. These flows do not name the upstream
owner as shooter, weapon owner, player or killer.

### Rejected investigation shortcuts

The earlier private worker report confused slot `+0x54` with `+0xf0`, entry
stride `0x74` with inline span `0x15c`, and the frame-container count mask with
`0x7fffffff`. Its searches/predictions based on those values are not promoted.
Absence of particular textual call/store spellings is not proof of absence of
an indirect dispatcher or writer. The actual damage-entry producer remains
unresolved; an unrelated event-copy routine does not resolve it.

Next bounded source-role work must use the corrected `+0x54` receiver dispatch
and `0x74` entry layout, or find the actual entry population path. No broad
whole-image absence claim, new runtime role, or source/killer upgrade is made.

Follow-up: the [offline forensic gates](2026-11-02-forensic-offline-gates.md)
identify a matching append/copy path and correct the handle-generation and
frame-consumer assumptions. Its execution in the captured playback and its
participant roles remain unproved.

Private reproducibility records: `frame-index-observations.json`,
`frame-hook-static-analysis.json`, and `native-hook-parent-validation.json` in
`ansi-live-01/`. Original worker reports remain unchanged alongside the parent's
explicit corrections. The VM remains shut down while this analysis is offline.
