# Revision 131544: direct-fire damage calculation (Phase 1, static)

Status: static, read-only, milestone 1. No game launch, VM or instrumentation.
Engine SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`
(re-hashed 2026-11-09), image base `0x400000`. Rizin 0.9.1, `af` + `pdfj` per
function; raw `pd` used only for byte checks of stack-offset operands. Private
evidence: `~/.hermes/artifacts/wgrd-replay/combat-damage-static-20261109/`
(`pdfj/<addr>.json`, `mw-offsets.txt`, `hp-delta-check.txt`).

Labels: OBS = read from analysed instructions. INF = inference from OBS plus
names. HYP = untested hypothesis. NOT = not established.

## Call graph (all edges OBS)

```
0xcff5a0 TProjectileManager loop (prior doc; not re-read)
 -> 0xcf8490 impact resolver
     0xcf8c72  call 0xcf95e0(R, mode=2, victim, dmgModule, ctx, d, pos)
     0xcf8ca2  call 0xcf95e0(R, mode=1, ...)        same victim
     0xcf92ee  call 0xcf95e0(R, mode=1, ...)        second (splash) loop
     d = 0xcfcea0(...) or 0.0 when the direct-hit test at 0xcf8bae passes
 -> 0xcf95e0 per-victim, per-mode
     0xcf9653  0xc2c940(ammo, mode) radius; radius <= 0 -> return
     0xcf9693  facing = 0xc842c0(ctx, R, mode)
     0xcf96d0  0xcfa120(out, ammo, victim, R, facing, mode, d, pos)   AMOUNT
     0xcf96dd  amount > 0.0 (0x193d3a0) else return
     0xcf96fc  0xcf7f40(dmgModule, amount, mode) -> 0xcf7f64 0xc58a70
     0xcf97ad  mode 2 only: 0xc58a70(amount * S, mode 1)   suppression from physical
 -> 0xc58a70 queue append: entry +0x68 amount, +0x6c arg, +0x70 mode
 -> 0xc95040 per-entry loop -> vtable+0x98 = 0xc9f910 apply (prior doc)
```

The four supplied anchors are confirmed by direct `call rel32` edges:
`0xcf8490 -> 0xcf95e0` (3 sites), `0xcf95e0 -> 0xcf7f40` (`0xcf96fc`),
`0xcf7f40 -> 0xc58a70` (`0xcf7f64`). `0xcf95e0` also calls `0xc58a70` directly
(`0xcf97ad`), which the earlier chain did not list.

## Amount: `0xcfa120` (OBS)

```
amount = H * P * T[family][armor] * K * C * F            (0xcfa2ae..0xcfa2e6)
```

| term | source | evidence |
|---|---|---|
| P | `0xc2c650(ammo, mode)`: mode 0 `+0x54 Puissance`, 1 `+0xb4 SuppressDamages`, 2 `+0xac PhysicalDamages`, 3 `+0xb4` | jump table `0xc2c6a4`; names from registrar `0xc2f6f0` |
| H | `R+0x48` (float) | `0xcfa183` |
| T | `0xa9e380(table=[0x2026e70], family, armor)` = `data[family*35 + armor]`, `data = table+0x18` | `0xa9e388`; `0x56b020` returns 35 |
| K | crit multiplier, default 1.0, see below | `0xcfa203`, `0xcfa294` |
| C | `0xc52d90(ammo, victim)`: 1.0 unless victim `0xa73ea0` and module `victim+0x104`; then `0xab0130` picks module `+0x14/+0x18/+0x1c/+0x20` by state (1 or 3/4) and ammo class | `0xab0130` |
| F | splash falloff `0xc4fd10(d, mode, radius)` | below |

Output record: `+0x0` pos (copy), `+0xc` amount, `+0x10` facing,
`+0x14` family, `+0x18` armor.

**family** (`ebx`): mode 1 -> 4. Otherwise `ammo+0xe8 Arme`. If
`0xc2ce00(ammo)` (`ProjectileType +0xec == 0` and `Arme` in 5..64) and
`ammo+0xf0 EfficaciteSelonPortee`, family = `0xda3410` (KE range AP).

**KE range AP** `0xda3410` (OBS):
```
rmax = ammo range for target class 0xda5b90(victim):
       1 +0x8c Bateaux, 2 +0x6c Maximale, 3/4 +0x74 TBA, 5 +0x7c HA, 6 +0x84 Projectile
ap   = Arme + trunc(max(0, rmax - R+0x44) / [0x203dd00])
cap  = 34 if Arme < 34 else 64
family = max(5, min(ap, cap))
```

**armor** (`edi`): `0xda3a20(victim+0x20, facing)` = armor module
`[+0x21c + 4*facing]` (`0xc9b800`); 0 when the looked-up object's flag `0x100`
is set.

**crit** (`R+0x54 = margin`): only when `R+4 == victim handle` and margin >= 0.
If family in 5..64: `armor = max(3, armor - trunc(margin / [0x203dd0c] + 1))`
when armor > 3 (divisor 0 -> reduction 0). Otherwise `K = [0x203dd10]`.

**falloff** `0xc4fd10` (byte-checked return at `0xc4fd49`, `c7442408 00000000`):
```
x = d / radius
F = 0                                   if x > 1
F = m + (1-m) * (1-x) / (1-t)           if t < x <= 1
F = 1                                   otherwise
t = [[0x2026688]][mode], m = [[0x20264d8]][mode]
```
Direct hit passes `d = 0.0` (`0xcf8bd3`), so F = 1 for the struck target.

**facing** `0xc83fd0` via `0xc842c0`: 4 for sub-ammunition (`+0xf9`) or a
flagged R; 1 for invalid geometry or indirect fire paths; else the normalised
local impact direction picks 1/2/3 against `[0x1da7c50]`/`[0x1da7c54]`.

## Constants (OBS writers, INF names)

Loader `0xcba1c0` (vtable `0x19b7b84`, COL at `-4`, slot 7 at `0x19b7ba0`;
the type-name string `TModernWarfareTunable...` follows at `0x19b7bac`) copies tunables. Offsets match the
`TModernWarfareTunableConstante` property registrar in `0xcc17..` (INF: class
binding by offset and name set, not by COL walk).

| global | from | NDF name | shipped value |
|---|---|---|---|
| `0x203dd00` | `+0x94` | DistanceStepToGain1APLevel | 13000.0 |
| `0x203dd04` | `+0x98` | DistanceMinOfAPFiringAuthorization | 26000.0 |
| `0x203dd0c` | `+0xa8` | CritMarginForArmorReduction | 0.1 |
| `0x203dd10` | `+0xac` | CritDefaulDamagetMultiplier | 1.5 |
| `0x1da7c50` | `sincos(+0xb0 * 0.5 * pi/180)[1]` | FrontSideAngleInDeg | 90 -> 45 deg -> 0.7071 (file pre-load value 0.5) |
| `0x1da7c54` | same, `+0xb4` | RearSideAngleInDeg | 90 -> 0.7071 |
| `0x20262ac` -> `0x203e7cc` (S) | `+0xbc` | AdditionalSuppressDamagePerLostPhysicalDamage | 50.0 |

Blob `gdconstanteoriginal.ndfbin`, decompressed SHA-256 `4d928518…08d2`
(byte-identical copy from 130278; per the 2026-11-08 report identical in 131544).

## Application (OBS static, OBS runtime)

`0xc9f910` mode 2: `applied = min(amount, max(+0x194) - cur(+0x19c))`,
`cur = max(cur + applied, 0)` (`0xc9fa4f`..`0xc9fc37`). Retained trace
`run-07.jsonl` (`acb8ecdc…`): all 28 enter/leave pairs match that rule on the
captured `+0x190..` window. The 3 mode-2 hits (28.0, 28.0, 14.5) each moved
`+0x19c` 0 -> 10 = MaxDamages, so all were lethal and clamped. Mode-1 hits add to
`+0x190`; one sample saturates at 800.0 (634.281 + 171 -> 800).

## Milestone 1b: damage table T (OBS, parent-verified)

Found by delegate A; every claim below was re-run by the parent.

- `[0x2026e70]` is written live only at `0xaa3719` (`mov [0x2026e70], edi`)
  in creator `0xaa3690` (0x30-byte object; final vtable `0x1999e50`). The
  stores at `0xa9e76b`/`0xa9efe0` are destructor clears to 0.
- RTTI: vtable[-1] `0x1b90dfc` -> TypeDescriptor `0x1ea0940` ->
  `.?AVTGameplayArmeArmureContainer@IA@Eugen@@`.
- The NDF registry entry at `0xaa0f40` binds the name
  `"TGameplayArmeArmureContainer"`, size 0x30 and creator `0xaa3690`. Bounded
  negative: no `E8` caller of `0xaa3690` in `.text`; one pointer ref.
- The `Values` reader is `0xaa64b0`. Rows come from `0xa86170` (= 65 = 0x41),
  the stride from `0x56b020` (= 35). It zero-fills `rows*35` floats, then
  copies each maplist row to `[obj+0x18] + key*35*4`.
- Shipped data: `pc/ndf/patchable/gfx/everything.ndfbin` (packed SHA-256
  `6b829a65…dc2c8`; decompressed with a tolerant inflate, SHA-256
  `640c66c2…d032`). The object record at offset `0x104f2f7` has class id 236,
  property 1419, MAPLIST of 65 entries. Keys 0..64 (UINT32), values are
  LIST of FLOAT32. 64 rows have 30 values, key 2 has 25. Columns 30..34 stay 0.0.
- Parent decode with an independent parser: all 65 rows equal delegate A's
  table. Private copy: `arme-armure-table.json` (SHA-256
  `9004d776…d12834`), which also pins `packed_sha256`/`decompressed_sha256`
  and the record offset.
- Samples, `T[family][armor]`: `T[8]` = `0,0,0,8,8,4,2,1.5,1,0…`;
  `T[24]` = `0,0,0,40,40,20,10,9.5,9…`; `T[64]` = `0,0,0,60,60,30,24,23,22…`.
- INF only: the column index is armor level and the row is the damage family.
  Mapping the rows to weapon kinds (KE, HEAT, HE, ...) is not established.

## Milestone 1c: hit roll, margin and H (OBS)

R-record layout, from appender `0xcf7fe0` (11 stack args, `ret 0x2c`;
record at `var_7ch`, copied by `0xc4b0f0`):

| R offset | value | site |
|---|---|---|
| +0x44 | 2-D distance (sqrtss of dx²+dy²) | `0xcf8132` |
| +0x48 | arg_20h = **H** | `0xcf813b` |
| +0x54 | arg_28h = **margin** | `0xcf8145` |

Producer at `0xce1b50` (reached from `0xcdf11c` <- `0xd88219`; INF: the
direct-fire path, since `0xce1830` requires `ProjectileType == 5`):

- **H** = `0xc52b10(handle, ...)`. It is the product of the resolved object's
  `+0xa0`, a vtable `+0x64` factor and an optional `+0x50` multiplier, times
  `[0x1da3ef8]` when the condition holds. Object roles are not established.
- **margin** = `e[8] - e[0]` when `e[8] >= e[0]`, else `-1.0` (`0xce1ae5`).

The shot record `e` (0x48 bytes) is built by `0xc9a980`. For a non-missile
`ProjectileType` it calls the ammo's `HitRollRule` (`ammo+0xcc`) vtable
`+0x28`. RTTI: vtable `0x19b4808` = `TModernWarfareHitRollRule`; slot +0x28 =
`0xc889e0`, slot +0x2c = `0xc8f700`.

- `0xc889e0`: `e[0] = 0xbb19b0(gameplay services)`, the **uniform roll** in
  [0,1). Then tail-calls `+0x2c`.
- `0xc8f700` writes `e[4]` (`0xc8fb52`), `e[8] = max(e4 * k, base) * [obj+0xb0]`
  with `obj = 0xb00690(arg 2)` (`0xc8fb65`; object not identified), and
  `e[0xc]`. `e[8] = -1.0` when a flag at `[+0x3c]+0x3f`
  is set (`0xc8fb84`). The interpolation table at `0x19b43b0` and threshold
  3.5 (`0x199fb64`) feed `e4`.
- **RNG** `0xbb19b0`: on the owning thread it calls `0xab1840` (`ecx+0x28`) ->
  `0x517030`. That is **Wichmann-Hill**: three state words, multipliers
  171/172/170, moduli 30269/30307/30323 (`0x763d/0x7663/0x7673`), result =
  frac(s1/30269 + s2/30307 + s3/30323). Off-thread it uses a different
  generator via `0x50f080`.

INF: `e[8]` is the hit probability and the margin is `p_hit - roll`, so a hit
means roll <= p_hit, and crits scale with the margin. HYP: the `e[4]` / `k`
names (accuracy x modifiers). Not verified at runtime.

## Milestone 1d: HP-clamp fixtures (OBS, parent-verified)

Delegate B's `extract.py`, rerun by the parent, reproduces
`hp_clamp_fixtures.json` byte for byte (SHA-256 `e4eaaad0…5654`, private
`delegates/B/`). The parent's own parse agrees on all 28 pairs: mode, amount,
`+0x190/+0x194/+0x19c` before and after.

- 56 events = 28 enter + 28 leave, paired by `(thread_id, call_id)`, 0 unpaired.
  11 failed reads, all the `arg1` source-handle read at address 0. All 28
  windows were read.
- Mode 2: 3/3 bit-exact under float32 rounding per operation. Only the clamped
  branch (`amount > room`) occurs; the unclamped and floor branches are not
  covered by any capture.
- Mode 1, empirical only: `after == f32(before + amount)` in 24/25; one
  saturates at 800.0. No mode-1 formula is claimed.
- No frame field on these events; frames are `not_captured`.

## FP operation order (OBS, `0xcfa2ae`..`0xcfa2e6`)

Scalar SSE single precision, left to right:
`((((H * P) * T) * K) * C) * F`. T arrives through x87 (`fld` in `0xa9e380`,
`fstp dword` at `0xcfa2be`), so it is rounded to float32 before the multiply.
P, C and F are also returned on x87 and stored as float32 (`0xcfa180`,
`0xcfa1a2`, `0xcfa170`). A predictor must round after every step.

## Not established

- t, m falloff arrays.
- `0xcde829` H = `edi+0x48` and `0xcf81f0` callers (`0xc71ad5`, `0xc821d8`,
  `0xcde8b4`): producers not traced.
- Full `0xc8f700` accuracy formula (`e4`, `k`) and the identity of `obj`
  whose `+0xb0` scales `e[8]`.
- Facing index -> front/side/rear/top naming (local axis sign unverified).
- C: state meaning of module `+0x104`.
- Mode-2-derived suppression entry (28 * 50) is absent from the trace after
  lethal hits. HYP: dead-module entries are dropped.
- Kill publication (`0xc9bf20`, `0xc954f9`) is from the 2026-11-02 doc and was
  not re-read in this pass.
- No weapon identity in either trace, so no amount is predicted yet.
