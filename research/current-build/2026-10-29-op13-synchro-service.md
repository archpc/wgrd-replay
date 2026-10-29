# Opcode 0x13 native trace: player synchronization service, 2026-10-29

## Scope and evidence

Static follow-up to the [offline corpus report](2026-10-29-offline-corpus.md).
Target: the retained current executable, revision **131544**, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, PE i386
(the `win64/` directory name is misleading; the image is 32-bit, base
`0x400000`). Tooling: REA 6.8.0 with Ghidra 12.1.4 default auto-analysis,
read-only; no VM, Windows process, game launch, or network research. Original
bytes were never written. An independent reviewer spot-checked the core
disassembly claims in a separate session; two initial claims were corrected
and are marked below.

Claims are labeled **confirmed** (read from disassembly or decompilation this
pass), **inferred** (a supported but unproven interpretation), or **unresolved**.
Addresses are Ghidra/REA addresses on the 0x400000 base.

## Command identity (confirmed)

`b2ef70` allocates a 16-byte object, assigns the RTTI-named vtable
`Eugen::IA::TNetworkActionPlayerSynchroServiceAction`, and reads three u32
command fields through the stream vtable (+4) into object offsets +4, +8, +0xC.
The execute wrapper `b2c220` (vtable `0x19a02a8`) forwards those three fields to
`b79760`, which loads singleton `[0x203b0d0]` into ECX and tail-jumps `b7b8a0`.
This confirms the corpus interpretation: +4 service index, +8 operation, +0xC
member value.

Provenance correction: class names come from MSVC RTTI, not surviving
RTTI-less symbols. A type descriptor
`.?AVTPlayerSynchronizationService@IA@Eugen@@` exists at `0x1eb3d44`; Ghidra
applies RTTI naming automatically. The identities are unaffected.

## Service manager and service 0 (confirmed + inferred)

- **Confirmed.** Singleton `0x203b0d0` is
  `Eugen::Meta::TSingleton<Eugen::IA::TPlayerSynchronizationService,0>`
  (names observed in the singleton and service destructors `b772f0`, `b77570`).
  The class embeds a `Eugen::TSynchronisationQueue` whose template evidence
  names `ListForIA()` and `ListFor3D()` lists.
- **Confirmed.** "Services" are synchronization items registered by the item
  base constructor `b75680`: appended to the table at manager+0x28 (count
  +0x2C, capacity +0x20), with the registration index stored at item+4. The
  +4 field is therefore registration order, matching the corpus's bounded
  service-table read.
- `b75680` has three call sites: `bcb800`, `d478c0`, `d61240`. One is
  **confirmed**: `bcb800` is the `Eugen::IA::TDeploiementGamePhase`
  constructor, which embeds an `Eugen::IA::TPlayersSynchronizationListener`
  sub-object and registers its item.
- **Inferred, order unproven:** service 0 is the deployment-phase item. The
  other two creation sites are unresolved, so registration order is not
  established and this inference must not enter parser semantics.
- **Confirmed.** Lifecycle: the destructor chain tears down items and nulls
  `0x203b0d0` (`b77570`, `b772f0`). The mechanism is scoped to a game phase,
  consistent with the corpus's rejection of a battle-start interpretation.

## Membership mechanics (confirmed, from `b7b8a0`)

Item layout resolved from assembly:

| Offset | Meaning |
|---|---|
| +0x00 | listener object pointer; its vtable: +0 member-joined(member), +4 first-member, +0xC reached-full, +0x10 dropped-to-empty |
| +0x48 | member array capacity |
| +0x50 | member array pointer |
| +0x54 | member count |
| +0x58 | "full" threshold |
| +0x5C | "empty/low" threshold |
| +0x60 | enabled byte |
| +0x61 | self-member latch |

- Operation 0 appends +0xC if absent (duplicate members are ignored);
  operation 1 removes if present via swap-with-last. Both are gated on the
  enabled byte at +0x60. Other operations have no traced branch — the corpus
  caveat stands.
- **Resolved (was open):** `68e990` is a vector-growth helper invoked with
  ECX = item+0x24 (embedded header: capacity +0x48, data +0x50, count +0x54).
  New capacity is `FUN_504910(max(capacity, 8), 4)`; it reallocates, copies
  the count elements, and frees the old block. Hitting capacity is a growth
  path, not an error or drop.
- Listener callbacks fire after append: vtable+0 per member; vtable+0xC when
  count reaches +0x58; vtable+4 when count−(+0x5C) == 1. The remove path
  fires vtable+0x10 when count == +0x5C. Callback gameplay effects remain
  unresolved.

## `ab1260`, the +0x61 latch, and `58da80` (resolved with one caveat)

- `ab1260` is a thiscall thunk calling `b7a4d0(this+0x24)`, which calls
  `b006d0` and returns `result+0x3C`. `b006d0` resolves a packed handle:
  0xFFFFFFFF is invalid; high 16 bits select a table (0x50-byte stride,
  registry at `0x2037d34`/`0x2037d38`), low 16 bits index the entry array.
  **Confirmed caller:** `b7b8a0` loads ECX from `[0x201d318]` at `0xb7b982`
  before the call. `ab1260` has 12 callers; the ECX source of the other 11
  was not checked, so "the canonical local-player-id accessor" is an
  **inference**, not an established fact. **Inferred:** the returned +0x3C
  value is the local player's synchronization token.
- Add path: when the incoming member equals `ab1260()`'s result, the item
  sets `+0x61 = 1` and calls `58da80` on `[0x203b0d0]+0x10` (the
  `TSynchronisationQueue`). The remove path never writes +0x61, verified
  line-by-line: the latch is one-way per item.
- `58da80`: if the queue's byte +8 is zero, calls queue vtable+0xC with
  argument 0. It is also invoked at item registration (`b78ae0`) and by the
  enabled-join path `b7ed60`. **Inferred:** it marks the queue dirty/ready.
- `b7ed60` (enabled-join): calls `b7ef70(item+4, 0)`, sets +0x61, calls
  `58da80`. `b7ef70` builds a network action via `b2a0b0(item+4, 0,
  ab1260())` and submits it through `b35840`: the item broadcasts a
  PlayerSynchro action carrying the local id when enabled.

## Membership-dependent control flow (partially confirmed)

- **Confirmed.** `b7bbb0`, registered per item at creation as a
  `Eugen::IA::Message::TTokenTypeFilterConstructor` callback with token type
  `DAT_0203b16c`, scans an incoming network action's token list
  (action+0x7C array, +0x80 count), finds the matching token type, and
  appends the token value (+8) to the item's member list with the same
  append/callback logic as `b7b8a0`. Membership is therefore fed both by
  opcode 0x13 executes and by synchronization tokens attached to other
  network actions.
- **Unresolved.** Whether membership gates replay dispatch, synchronization
  barriers, or simulation advancement. The `ListForIA`/`ListFor3D` structure
  suggests a per-phase wait-for-players barrier whose released items are
  consumed by IA and 3D systems, but the queue's vtable+0xC handler was not
  traced.

## Strongest slot evidence

Confirmed chain: the corpus member value equals the enclosing pact slot; the
add path compares that same value against the handle-resolved +0x3C field to
set the self-latch. Member values therefore live in the same value space as
player synchronization tokens. This supports "membership = players
participating in a synchronization phase, keyed by the same IDs recorded as
pact slots" without equating slots with player identities. No decoder change
is proposed by this document.

## Falsification conditions

- Service 0 = deployment-phase item: false if `d478c0`/`d61240` register
  before the deployment phase in game-phase construction order.
- `ab1260` = local synchronization token: false if resolved+0x3C is a
  coincidental session index.
- Queue-not-dispatch: false if the queue vtable+0xC handler reaches
  frame-advance or replay-dispatch code.

## Limits

- Static paths do not establish runtime acceptance, historical playback, or
  simulation outcomes.
- Listener callback implementations, the queue dirty-handler consumer, the
  two untraced creation sites, `FUN_504910`'s exact growth policy, and 11 of
  12 `ab1260` caller contexts remain open.
- All findings qualify only the literal Version `131544` executable; the
  corpus exporter's build-qualification approach remains the correct pattern.

## Next experiment

Trace `d478c0` and `d61240` to pin service-0 registration order, then follow
the `TPlayersSynchronizationListener` vtable implementations and the queue's
vtable+0xC handler to the consumer of released synchronization items. That
single thread resolves whether membership controls replay dispatch, a
synchronization barrier, or simulation advancement.
