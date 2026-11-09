# Next milestone: tracing the 500-point bonus and the pinned/death multipliers

Date: 2026-11-08. Static, read-only. No game launch.
Follows [`2026-11-08-ndf-effective-values.md`](2026-11-08-ndf-effective-values.md),
which recovered the shipped values. This note records the anchors found while
starting the two traces, and the negative results so the next pass does not
repeat them.

Two objectives, deliberately separate:

* **A. `BonusIAMoneyForSkirmish = 500` → skirmish initialisation.**
* **B. `MultiplicateurSeuilPinnedEtMort*` → suppression and destruction math.**

## Anchors established

### The tunables loader is a virtual method

`0x00b914c0` (the function that copies NDF fields into fixed globals) carries
Rizin's own flag `method.Eugen::IA::TTunableConstante.virtual_28`, which matches
the class actually present in the shipped blob (`TTunableConstante`, 144
properties) and the 144 globals we recovered. It has **no direct `call rel32`
caller** anywhere in the image, consistent with virtual dispatch from the
descriptor vtable rather than a named call site. Any consumer trace has to go
through the object, not through a call graph edge.

### The difficulty initialiser belongs to the gameplay-services singleton

`0x00babf40` is the constructor: it installs vtable `0x19ab14c` at `[ebx]`,
`0x19ab1c8` at `[ebx+4]`, `0x19ab1d8` at `[ebx+8]`, and stores the object in the
global `0x0201d31c`. `0x00bb2740` — the difficulty switch that writes
`+0x270..+0x27c` — is called from `0x00bae820`, which is vtable slot 2 of that
same object.

So the multipliers live at `+0x274` (player pinned/death), `+0x278` (player
damage), `+0x27c` (IA pinned/death) of the object at `0x0201d31c`, not in a
standalone structure.

### Negative results (do not redo)

* Scanning the **654** code references to `0x0201d31c` for a nearby
  `[reg+0x274]` / `[reg+0x278]` / `[reg+0x27c]` operand found **zero** real
  reads. The two byte-level matches (`0xb1365b`, `0xb1d74e`) both turn out to
  read `+0x2bc`, not a multiplier.
* Searching the whole image for the displacement `0x274` alone yields 133
  functions; the offset is too common to identify the struct. Anchor on the
  object pointer, never on the offset.
* `0x02026390` (`BonusIAMoneyForSkirmish`) has exactly one code reference, the
  loader store at `0x00b92035`. No absolute reader exists.

## A. The 500-point bonus

Question: does the shipped 500 reach starting funds, income, or nothing at all?

Hypotheses, in order of likelihood:

1. **Script-side consumption.** The value is written to a global for a script
   layer (Lua or the NDF-driven skirmish setup) that this installation does not
   ship. Testable by checking the install for script payloads and by looking
   for the descriptor being handed to a scripting bridge.
2. **Read through the descriptor, not the global.** Skirmish code may fetch the
   live `TTunableConstante` instance and read `+0x264` directly. The loader
   global would then be a cache for other subsystems.
3. **Vestigial.** The property ships, nothing reads it.

Method:

* Locate the global that holds the live `TTunableConstante` instance. Start from
  the vtable resolution (`scripts/ai_rtti.py --class '.?AVTTunableConstante@Eugen@@'`)
  and scan `.data` for objects pointing at that vtable; cross-check against the
  singleton pattern used at `0x0201d31c`.
* Once the instance pointer is known, xref it and look for `+0x264` reads in
  skirmish-initialisation functions (the skirmish descriptor classes are
  `TIASkirmishDescriptor`, `TIASkirmishList`, `TModernWarfareTacticalGameRules*`).
* Confirm any candidate with `scripts/ai_field_xrefs.py --validate`, which
  requires a real instruction boundary and a bracketed operand.

Falsifier: no read of `+0x264` and no script payload that ships the value →
hypothesis 3, and the 500 is inert.

## B. The pinned/death multipliers

Question: where do `1.5 / 1.0 / 0.75` (player) and `0.75 / 1.0 / 1.25` (IA)
enter suppression and destruction math, and which direction favours the AI?

Method:

* Walk the singleton's real member functions rather than guessing by offset:
  enumerate functions whose `ecx` is loaded from `0x0201d31c`, then read each
  one's displacements once (`pdfj`), instead of scanning the image for `0x274`.
* In parallel, search the unit-side modules for reads of a threshold multiplier
  passed as an argument: `TModernWarfareDamageModule`, `TMoralModule`, the
  pinned/suppression state classes (`TStateFire`, `TQueryOnStress`,
  `TCriticalEffect_AddDamages`), and `TModernWarfareTestMoralRollRule`.
* Determine direction from the comparison, not from the name: the multiplier is
  presumably applied to a threshold, so "higher" may mean *more* resilient or
  *easier to break* depending on which side of the comparison it lands.

Falsifier: the multipliers are read only by UI or debug code, or one side's
value is never loaded at all, which would make the asymmetry inert.

## Deliverables for the milestone

1. A call/data-flow path for each objective, ending in a named function and a
   comparison or arithmetic operation, with addresses.
2. A direction statement for B backed by the comparison operand order.
3. An explicit "inert" verdict when a value ships but nothing reads it.
4. Regression tests for any new reader helper; the existing
   `tests/test_ndf_read.py` and `tests/test_ai_rtti.py` pins stay authoritative.
5. No promotion of any claim past *suspected* without a shipped value **and** a
   consumer.

## Constraints

Static only; no game launch, no VM operation, no multiplayer. PR #26 remains
frozen. Cow untouched.

## Progress, 2026-11-08 (parent-verified)

Two bounded read-only traces were run in parallel and every address below was
re-disassembled by the parent before integration.

### A. The 500-point bonus

| finding | address | status |
|---|---|---|
| property registration: offset `0x264`, i32, name `0x19a808c` | `0x00b9448d` | verified |
| class registry (schema + creator) | global `0x0203b350` | verified |
| instance creator: loads registry, allocates `0x2c8` | `0x00b92680` | verified |
| constructor installs vtable `0x19a6fe4`, zero-fills `+0x0c..+0x2bf` | `0x00b8de50` | verified |
| loader is vtable **byte offset `0x1c` (slot index 7)**, not slot 28 | `0x19a7000` → `0x00b914c0` | verified |
| field copy `[edi+0x264]` → global `0x02026390` | `0x00b9202f` / `0x00b92035` | verified |

Correction to the earlier briefing: Rizin's `virtual_28` label is a **byte
offset**, matching slot index 7. Both descriptions name the same method.

Negative results, each method-scoped:

* No reader of `0x02026390` by exact-address reference anywhere in the image
  (whole-file dword scan; one hit, the store).
* `BonusIAMoneyForSkirmish` occurs exactly once as a string (`0x19a808c`) and is
  referenced only by the registration push at `0x00b94495`; there is no second
  name table or binding entry.
* No `.lua`, `.luac`, `.py`, or `.pyc` payload exists anywhere under `Data/`
  (enumeration count 0), so this installation ships no script that could read it.
* No `[reg+0x264]` operand inside 43 vtable methods of the skirmish/game-rules
  classes (12600 instructions disassembled).

Unresolved: the instance pointer is returned in `eax` only and stored nowhere,
so the NDF parse-tree node that owns it was not identified; and aliased access
through a base register other than the instance cannot be excluded.

### B. Singleton and multipliers

| finding | address | status |
|---|---|---|
| singleton is an **object base**, one dereference: `mov eax,[0x0201d31c]; mov eax,[eax+0x60]; ret` | `0x00bb2a10` | verified |
| only non-zero store is `mov [0x0201d31c], ebx` (ebx == this) | `0x00babfa5` | verified |
| three clear sites (`mov [global],0`): `0x00bacd61`, `0x00bad11b`, `0x00badb1b` | same | verified |
| factory allocates `0x428`, runs ctor, then **replaces** the three vtable pointers with `0x1994cac` / `0x1994d28` / `0x1994d38` | `0x00a5d424`–`0x00a5d49c` | verified |
| difficulty initialiser called from base slot 2 and again during construction | `0x00bae8a1`, `0x00bac469` | verified |
| static difficulty table at `0x1da3f0c` is **nine × `0x3f800000`**; shipped 1.5/0.75/1.25 arrive only from the loader | `0x1da3f0c` | verified |

That last row matters: the multipliers are not compiled-in constants. The image
ships 1.0 everywhere and the NDF loader overwrites those nine globals at
runtime, so the difficulty asymmetry is entirely data-driven.

The runtime object is a **derived** class (vtable `0x1994cac`, factory
`0x00a5d424`), not the base whose vtable the constructor installs. Field offsets
`+0x270..+0x27c` therefore belong to the derived layout.

Semantics check, run by the parent after the traces: of the 654 literal uses of
`0x0201d31c`, 644 are plain `mov reg,[global]` loads, 3 are `mov [global],0`
clears, 1 is the init store at `0x00babfa5`, and 1 is a compare. Seven sites
look like a second dereference; disassembly shows they are vtable loads
(`mov reg,[global]; mov vt,[reg]; call [vt+off]`, e.g. `0x00a95530` →
`call dword [eax+0x38]`). So the global is an object base, not a
pointer-to-pointer, and the earlier single-clear description was incomplete.

Negative results, method-scoped: no read of `+0x274`/`+0x278`/`+0x27c` was found
by (a) full-function disassembly of all 448 functions referencing the singleton,
(b) enumeration of 24 base-vtable methods and 22 runtime-vtable methods,
(c) an ECX-anchored scan of 11 callees receiving the singleton, or (d) 47
methods of the damage/morale/stress/fire classes. Direction of the multipliers
is therefore **unresolved**; nothing found compares them to a unit-side value.

### What this does and does not settle

Settled: the bonus has a proven data value and a proven loader path but no
located consumer; the multipliers are data-driven, live on a derived
gameplay-services object, and still have no located comparison.

Not settled: any effect on skirmish outcomes. Both remain *suspected*, not
proven, and neither is evidence of cheating.
