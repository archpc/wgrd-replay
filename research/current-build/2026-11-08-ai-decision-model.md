# AI decision model and difficulty parameters (build 131544)

Date: 2026-11-08. Target: `WarGame3.exe`, internal revision 131544,
SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
Method: static, read-only. No game launch, no VM interaction, no network, no
execution of the target. The Cow is untouched.

Scope was deliberately split into two independent questions, because they have
different evidence and different remedies:

* **Economy axis** — does the AI receive resources, income, or cost advantages?
* **Information axis** — does the AI act on state a human player cannot see?

Neither axis may be answered by the other. A finding on one is not evidence for
the other.

## 1. Symbol situation (record this before any address)

* The image is **PE32, i386**, `machine i386`, `lang msvc`, despite living in a
  `win64` directory. Address math therefore uses 4-byte pointers and
  `ImageBase + section RVA`, with ImageBase `0x00400000`.
* A **PDB is referenced but absent**. Debug directory: CodeView `RSDS` at file
  offset `0x18625c8`, GUID `db6b159c652c9342b1950b30b1b8c179`, age 1, path
  `C:\Data\GitlabBuild\Nu8Q8jzE\0\eugen\Slayer\Bin\WarGame.Final.Win32.pdb`.
  No `.pdb` exists in the artifact tree, the Steam data directory, or the
  local analysis directories. **The binary is not symbol-rich**: the COFF
  symbol table holds 1128 entries, almost all `TPoolAllocation::_sPoolStorage`
  template statics. Do not describe this build as having symbols.
* Names therefore come from **MSVC RTTI**, which is complete: 2962
  IA-namespace type names, 2311 resolving through TypeDescriptor → COL →
  vftable to 5378 virtual slots. `IA` is Eugen's *intelligence artificielle*
  namespace (the studio is French); `IAStrat` is the strategic AI layer.

Reproduce the name recovery:

```
python3 scripts/ai_rtti.py --exe <WarGame3.exe> --slot-map --json slotmap.json
python3 scripts/ai_rtti.py --exe <WarGame3.exe> \
    --class '.?AVTWargameCheatLogic_Impl@Wargame@Eugen@@' --slots 4
```

Verified chain example (bytes checked in Rizin, not inferred):
`TWargameCheatLogic_Impl` TD `0x01f98690` → COL `0x01c32ffc` → vftable
`0x01a130ac`, where `vftable[-1]` holds `0x01c32ffc` and slot 0 is
`0x01326670`.

## 2. Gameplay tunables: the field table

A descriptor-registration block at `0x00b94011`–`0x00b94909` pushes
`(offset, name)` pairs for the gameplay-constant class. 76 pairs were
recovered mechanically (`scripts/ai_field_xrefs.py` plus the registration
listing). Fields that matter to this investigation:

| offset | name | axis |
|---|---|---|
| `0x1ec` | `DefaultDifficulty` | difficulty |
| `0x1f0` / `0x1fc` / `0x208` | `StockDeviseSupplementaireFacile` / `…Moyen` / `…Difficile` | economy |
| `0x1f4` / `0x200` / `0x20c` | `MultiplicateurSeuilPinnedEtMortJoueur{Facile,Moyen,Difficile}` | difficulty |
| `0x1f8` / `0x204` / `0x210` | `MultiplicateurSeuilPinnedEtMortIA{…}` | difficulty |
| `0x214` / `0x218` / `0x21c` | `MultiplicateurDegatInfligeParLeJoueur_{Facile,Moyen,Difficile}` | difficulty |
| `0x224` | `QteDeviseParCamion` | economy |
| `0x250` | `SeedForIAStrat` | AI |
| `0x264` | `BonusIAMoneyForSkirmish` | economy (AI) |
| `0x268` | `VisibilityMemoTimer` | information |
| `0x270` | `IgnoreInvisibleUnit` | information |
| `0x271` | `InfluenceMapAlwaysKnowAllUnits` | information |
| `0x272` | `DeplacementPionsIAGroupes` | AI |
| `0x274`–`0x288` | `PlaneSuperiority`, `InterceptorFactor…`, `MultiroleFactor…`, `NbAvionMaxParCibleAvantEquilibrage`, `RepartitionAvionAntiship`, `GroundAttackFactor…` | AI |
| `0x28c` / `0x290` | `MaxDelayBeforeEvacuation` / `MinDelayBeforeEvacuation` | AI timing |
| `0x294` / `0x298` | `OneRecoForXCaptures` / `OneRecoForXAttacks` | AI composition |
| `0x2b8` | `BonusDissimulationDesUnitesIntervientPourLeurEtatDeStealth` | information |
| `0x2c0` | `SimulatedSecondsInOneFrame` | clock |
| `0x2c4` | `StrategicAttackCanAffectAttacker` | rules |

French names are the shipped identifiers and are quoted verbatim; do not
translate them in code or tests.

Meaning of each, where established: `StockDeviseSupplementaire` is an extra
*currency stock* granted per difficulty. `MultiplicateurSeuilPinnedEtMort*` are
multiplicative thresholds for the pinned/death state, kept separately for the
**player** and the **IA** — the split itself is evidence that difficulty is
allowed to treat the two sides differently, without yet proving which side
benefits.

## 3. Loader: fields become fixed Globals

One function, `0x00b914c0`–`0x00b921c1` (prologue and epilogue verified in
Rizin), copies 65 of those fields from the descriptor into fixed global
addresses. Selected mappings (`scripts/ai_field_xrefs.py` cannot see these;
they were extracted from the store listing and are reproduced in the ledger):

| field | source offset | global |
|---|---|---|
| `StockDeviseSupplementaireFacile` | `0x1f0` | `0x02026360` |
| `StockDeviseSupplementaireMoyen` | `0x1fc` | `0x02026364` |
| `StockDeviseSupplementaireDifficile` | `0x208` | `0x02026368` |
| `BonusIAMoneyForSkirmish` | `0x264` | `0x02026390` |
| `VisibilityMemoTimer` | `0x268` | `0x020263a4` |
| `IgnoreInvisibleUnit` | `0x270` | `0x020263a1` |
| `InfluenceMapAlwaysKnowAllUnits` | `0x271` | `0x020263a2` |
| `BonusDissimulation…Stealth` | `0x2b8` | `0x020263cf` |
| `SimulatedSecondsInOneFrame` | `0x2c0` | `0x02026374` |

This is the useful structural result: these are **plain globals**, so their
consumers can be found by absolute-address xref with no type information and no
PDB. The full 65-entry table is in `ai-findings-ledger.json`.

## 4. Economy axis

### 4.1 Difficulty selects an economy block

Function at `0x00bb2740` (frame-pointer-less; `sub esp,0x20`; returns at
`0x00bb27c4`, `0x00bb2862`) reads the difficulty byte returned by
`0x00e68460` and branches:

```
movzx eax, byte [esp+0x1e]   ; 0x00bb2775
sub   eax, 1
jz    0x00bb282f             ; value 1 -> Facile block
sub   eax, 1
jz    0x00bb27fa             ; value 2 -> Moyen block
sub   eax, 1
jz    0x00bb27c5             ; value 3 -> Difficile block
; anything else: neutral
mov   dword [esi+0x270], 0x00
mov   dword [esi+0x274], 0x3f800000   ; 1.0f
mov   dword [esi+0x278], 0x3f800000
mov   dword [esi+0x27c], 0x3f800000
```

Each difficulty branch writes the same four slots from globals:

```
[esi+0x270] <- StockDeviseSupplementaire<Difficulty>
[esi+0x274] <- MultiplicateurSeuilPinnedEtMortJoueur<Difficulty>
[esi+0x278] <- MultiplicateurDegatInfligeParLeJoueur_<Difficulty>
[esi+0x27c] <- MultiplicateurSeuilPinnedEtMortIA<Difficulty>
```

Consequences that are proven by bytes:

1. Difficulty is a **closed enum 1/2/3** here; `AI_VHARD` exists as an enum
   string elsewhere but is **not a case** in this selector. Vertical scaling to
   Very Hard is therefore not implemented by this block.
2. The **neutral default is an explicit cheat-free baseline**: stock bonus 0,
   all three multipliers 1.0. Any nonzero economy effect must come from data.
3. The block is a mixed bag: it bundles an economy term with difficulty-scaled
   damage and pinned state terms. An economy finding here does not imply a
   targeting finding, and vice versa.

Not established: what object `esi` is, which team reads `+0x270`, and whether
the stock bonus is paid to the AI, the player, or both. The caller set is
small — `0x00babf40` and `TWorld` vtable slot 2 at `0x00bae820` — so this is a
short, well-defined next trace.

**Status: a difficulty-selected parameter, not a proven AI-only bonus.** The
table groups `StockDeviseSupplementaire` with player/IA threshold multipliers;
it does not say who receives the stock. Treating "difficulty affects economy"
as "the AI gets extra money" would be exactly the conflation this split
forbids.

### 4.2 `BonusIAMoneyForSkirmish`

The name states a skirmish-scoped AI money bonus. Its global `0x02026390` has
exactly one code reference, the loader store at `0x00b92036`. No absolute
reader exists. That is not proof of absence: a reader may use a base pointer
plus displacement (for example a `0x02026340`-based block that reads `+0x50`).
No such base reference was found for the surrounding block either, so the
current honest statement is **field exists, is shipped, consumer not located**.

## 5. Information axis

### 5.1 Influence-map visibility gate (strongest finding)

In the influence-map update loop (Rizin function `0x01082680`, instruction
`0x010828a5`):

```
0x010828a5  cmp byte [0x020263a2], 0x00      ; InfluenceMapAlwaysKnowAllUnits
0x010828ac  jnz 0x010828be                   ; flag set -> treat unit as known
0x010828ae  mov eax, dword [edi+0x140]
0x010828b4  cmp byte [edx+eax*1], 0x00       ; otherwise require visibility
0x010828b8  jz  0x01082838                   ; not visible -> skip unit
0x010828be  ...                              ; accumulate influence for the unit
```

Semantics: with the flag at 0, a unit enters the influence map only when its
visibility byte is set. With the flag at 1, the visibility test is bypassed and
every unit in the iteration contributes influence. That is a **fog-of-war
bypass for the AI's influence map**, gated by a data field rather than
hard-coded.

This does not make it a cheat. Whether it is an advantage depends entirely on
the shipped value of `InfluenceMapAlwaysKnowAllUnits`, which is not readable
from the binary by this pass (see §7). Read it as "a designed, data-controlled
omniscience lever", not as "the AI cheats". Status: **code path proven,
shipped enablement unresolved.**

### 5.2 Per-unit visibility bookkeeping

At `0x01037775` inside the visibility/identification loop:

```
0x01037775  cmp byte [0x020263a1], 0x00      ; IgnoreInvisibleUnit
0x0103777c  jz  0x01037833
0x0103779b  cmp dword [eax+edi*4], 0x01
0x010377a2  jl  0x01037836
0x010377b8  cmp ecx, dword [0x020263a4]      ; VisibilityMemoTimer
0x010377be  cmovl ecx, dword [0x020263a4]
0x010377c5  mov dword [edx+eax*4], ecx
```

Read: when the flag is set and a per-unit counter is at least 1, a stored
timestamp is clamped to at least `VisibilityMemoTimer`. The direction of the
flag (ignore invisible units vs. include them) is **not** settled by this
snippet; `IgnoreInvisibleUnit` could mean "the AI ignores units it cannot see",
which would be the opposite of a cheat. **Status: unresolved semantics;
recorded because the flag is real, consulted, and controls a memoised
visibility value.**

### 5.3 What was not found

No hard-coded omniscient targeting was observed. `TInfluenceMap` has one
virtual slot (`0x01029750`); the visibility bypass lives in a non-virtual
routine reached from higher-level AI updates, and every path found so far is
flag-gated. This leaves **omniscient targeting unresolved, not refuted**: the
absence of an unconditional bypass in the regions examined is weak evidence,
because a 30 MB image was not exhaustively swept. Do not cite this section as a
negative result.

## 6. Cheat-logic surface

`TWargameCheatLogic_Impl` (vftable `0x01a130ac`, 3 slots: `0x01326670`,
`0x01344000`, `0x004d7b40`) and its interface `ICommonCheatLogic` exist as
developer cheat plumbing. Global name strings `DevCheats`, `FullyRevealed`,
`NoDifficulty` live in `.data` (`0x01d840c0`, `0x01d8430c`, `0x01d84004`) as
registered option names. None of these are referenced by the AI paths above.
`FullyRevealed` is a renderer/material-pack name (`ForceRevealed`,
`MultiRenderTypeMaterialPack_ForceRevealed`) as well as an option name; do not
conflate the two without a call trace.

## 7. Why defaults are missing, and what that costs

`Data/WarGame/PC/131544/NDF_Win.dat` (24 MB, SHA-256
`172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b`)
should carry the tunables values, but none of `StockDeviseSupplementaire`,
`InfluenceMapAlwaysKnowAllUnits`, `IgnoreInvisibleUnit`,
`BonusIAMoneyForSkirmish`, or `GameplayConstantes` appears in its 90 753
string-extraction hits. The strings that do appear are paths (`edat`,
`pc\ndf\`, `nonpatchable`, `luster`, `bootstrap`).

**The NDF encoding is unknown to this pass.** Absence from naive string
extraction is consistent with compression, with tokenisation by hash, with
encryption, or with a text encoding this extractor does not read. No
assumption is made, and "compressed" is not asserted anywhere. Recovering the
effective values is the next research milestone (§9, E1) and is a prerequisite
for any default-value claim. No default is asserted here.

This is the single largest limitation of this report. Every economy and
information finding is a **mechanism** finding. None is yet a **shipped-value**
finding.

## 8. Findings ledger

`research/current-build/ai-findings-ledger.json` is machine-readable and is the
authority for status. Summary:

| id | claim | axis | status |
|---|---|---|---|
| P1 | Build is PE32 i386, SHA-256 pinned; PDB absent; RTTI complete | meta | proven |
| P2 | 76 gameplay-tunable fields registered with offsets | meta | proven |
| P3 | 65 fields copied to fixed globals by `0x00b914c0` | meta | proven |
| P4 | Difficulty 1/2/3 selects stock + threshold + damage blocks; neutral = 0/1.0 | economy | proven |
| P5 | `InfluenceMapAlwaysKnowAllUnits` gates the influence-map visibility test | information | proven (path); enablement unresolved |
| P6 | `IgnoreInvisibleUnit` is consulted in visibility bookkeeping | information | proven (read only) |
| S1 | `StockDeviseSupplementaire*` is a difficulty-selected currency parameter; AI-only receipt not shown | economy | suspected |
| S2 | `BonusIAMoneyForSkirmish` is named as a skirmish AI money term; receipt not shown | economy | suspected |
| S3 | `IgnoreInvisibleUnit` direction favours the AI | information | unresolved |
| U1 | Omniscient targeting: AI acting on units the player cannot see | information | unresolved (not refuted) |
| U2 | Reaction latency, ammo/fuel exemptions, deployment restrictions, `TCostComputer*` valuation | mechanics | not examined |

Shipped values are not a claim but an open item (§7, §9 E1): without them, no
row above can move from *suspected* to *proven cheat*.

"proven" here means a direct read, write or branch at a cited address. It never
means "the AI cheats". No cheating claim is promoted past *suspected* in this
report, because no shipped value and no per-team consumer was established.

## 9. Controlled experiments (design only, none run)

Each experiment states a numeric prediction and its falsifier. None is
authorised yet; E3 and E4 require explicit VM authorisation, and no experiment
may touch multiplayer.

**E1 — Decode the NDF tunables table (offline).**
Parse `NDF_Win.dat` for the gameplay-constant class. Prediction: the 76
registered names appear with values; `StockDeviseSupplementaireFacile > 0` and
`InfluenceMapAlwaysKnowAllUnits ∈ {0,1}`. Falsifier: fields absent, or a value
outside the domain implied by the code (e.g. a float where the code reads a
byte).

**E2 — Replay-corpus order/vision join (offline, corpus only).**
For AI-issued order records in the retained 131544 replay, join each target to
observed vision events. Prediction: if no information advantage is active, no
AI order targets a unit with zero prior vision; if any do, quantify the rate.
Falsifier: order events resolve to units with no vision record at all in the
same replay, which would indicate incomplete vision logging rather than a
cheat — record which.

**E3 — Global read at runtime (needs authorisation).**
Read the 65 globals and `+0x270..+0x27c` after world init on each difficulty.
Prediction table (Hard as shipped): stock > 0, player damage multiplier < 1.0,
IA threshold != 1.0, all others 1.0. Falsifier: all globals equal to the
neutral defaults on every difficulty, which would mean the table is inert in
skirmish.

**E4 — Latency and exemption probe (needs authorisation).**
Measure AI order issuance delay and ammo/fuel consumption for AI units across
difficulties. Prediction under "no exemption": identical consumption per shot
and per distance across difficulties; latency differs only by difficulty
constant. Falsifier: AI unit consumes less ammo/fuel than an identical player
unit under identical orders.

## 10. Reproduction

All commands read the pinned binary only.

```
python3 scripts/ai_rtti.py     --exe <exe> --slot-map --json slotmap.json
python3 scripts/ai_rtti.py     --exe <exe> --class '.<name>' --slots 8
python3 scripts/ai_field_xrefs.py --exe <exe> --disp 0x271 --disp 0x270 --validate --afl afl.txt
python3 scripts/ai_attrib.py   --exe <exe> --afl afl.txt --slotmap slotmap.json --va 0x010828a5 --validate
rizin -q -e scr.color=0 -c 'afl' <exe>          # save once for --afl
rizin -q -e scr.color=0 -c 'pd 40 @ 0x01082870' <exe>
rizin -q -e scr.color=0 -c 'pd 26 @ 0x00b92110' <exe>
```

Disp-xref hits are candidates. `--validate` keeps only sites that Rizin decodes
as instruction starts whose operand text shows the displacement, and caller
scanning applies the same boundary test to `call` instructions. Two decoder
defects were found and fixed while adding it: the SIB form had ModRM and SIB
swapped, and `[ebp+disp32]` (ModRM mod=10, rm=5) was rejected as an absolute
address. Both are pinned by tests. The `0x270`/`0x271` globals cited above are
read through *absolute* addresses (`0x020263a1`, `0x020263a2`), so those
findings never depended on the displacement decoder.

`tests/test_ai_rtti.py` pins the chain on a synthetic fixture and on the real
binary when the artifact is present (skipped, not failed, when absent).
