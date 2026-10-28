# REA notes: WarGame3.exe build 59638 (work in progress)

Target: ~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe
SHA-256 1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46, PE32 i386,
compiled 2021-10-12, ImageBase 0x400000, PDB path WarGame.Final.Win32.pdb (PDB not loaded).
Tools: REA 6.7.0 / Ghidra 12.1.4 (decompile), rizin (independent disassembly), Python (byte scans).

Original-playback feasibility follow-up: research/RUNTIME59638-FEASIBILITY.md.
Fresh REA/Rizin candidate c7e350 -> da4d20 returns a stored-vector pointer;
not yet validated as an individual-unit position. No game execution. Runtime/
asset prerequisites block local playback; tick/health/spawn/destruction untraced.

Address conversion (VERIFIED from section table):
- RVA = VA - 0x400000
- .text:  file = VA - 0x401000 + 0x400
- .rdata: file = VA - 0x1914000 + 0x1513000

## Findings

| # | Item | VA | RVA | File off | Evidence | Status |
|---|---|---|---|---|---|---|
| 1 | ESAV header reader FUN_010b9300 | 0x010b9300 | 0xcb9300 | 0xcb8700 | Ghidra decompile ev_b44efd7d… | VERIFIED |
| 1a | cmp ebx,'ESAV' | 0x010b9366 | 0xcb9366 | 0xcb8766 | rizin pd: cmp ebx, 0x45534156 | VERIFIED |
| 2 | u32 BE reader FUN_010b9790 | 0x010b9790 | 0xcb9790 | 0xcb8b90 | rizin pdf: read 4 -> ntohl -> store | VERIFIED |
| 3 | tag handler FUN_00b3c5d0 (vtbl slot +8) | 0x00b3c5d0 | 0x73c5d0 | 0x73b9d0 | Ghidra decompile ev_7841a093… | VERIFIED |
| 4 | vtable TReplayActionVisitor | 0x019a1c4c | 0x15a1c4c | 0x15a0c4c | RTTI COL 0x1b9b34c | VERIFIED |
| 5 | cmp eax,'rply' | 0x0093c699 | 0x53c699 | 0x53ba99 | rizin pd: cmp eax, 0x72706c79 | location VERIFIED |
| 6 | writer push imm32 sites (VA) | ESAV 0x10bb177, rply 0xb39139, star 0xb3fd38, pact 0xb3fb38, endt 0xb3fa67 | | | rizin pd | location VERIFIED |

FUN_010b9300 behaviour (Ghidra, one decompiler; error paths shown as unrecovered jumptables):
read 4 -> ntohl -> must == 0x45534156 ('ESAV'); read 4 -> ntohl -> reject if > 1
(=> versions 0 and 1 accepted; parser accepts only 1: discrepancy); tell();
FUN_010b9790 (read u32 BE = file-size field 0x08); alloc 0x1c, read exactly 0x1c bytes
(= unknown 28-byte field 0x0C..0x27; short read -> error); visitor->slot+4(version, ...);
store tell() (inferred = 0x28).
Ordinal_14 = WS2_32 ntohl (rizin import table, IAT 0x191481c). Explicit endian conversion CONFIRMED.

FUN_00b3c5d0 behaviour: compares a u32 tag with integer constants 'pact' 0x70616374,
'endt' 0x656e6474, 'star' 0x73746172 (no string compare). Each calls
FUN_004e6d80(param_3,param_4) (likely payload ptr/len, INFERRED). pact: increments
counter at this+0x1c. star/endt: FUN_004fcc00. All: set byte this+0x24 = 1.

RTTI classes (names are evidence of intent, not proof of behaviour):
- Eugen::IA::TReplayActionVisitor : Eugen::ISaveFileReaderVisitor (vtable 0x19a1c4c)
- Eugen::IA::TNetworkEventSourceFromReplay : Eugen::IA::TNetworkEventSource (COL 0x1b9b300)
  -> suggests replay data is fed back as network input (consistent with lockstep inference).

## Session 2 findings

| # | Item | VA | RVA | File off | Evidence | Status |
|---|---|---|---|---|---|---|
| 7 | chunk reader FUN_010b9500 | 0x010b9500 | 0xcb9500 | 0xcb8900 | Ghidra ev_1b96c300…; rizin shows ntohl load at 0x10b9569 | VERIFIED |
| 8 | SHA-224 init FUN_016fd070 | 0x016fd070 | 0x12fd070 | 0x12fc470 | rizin: IV c1059ed8 367cd507 3070dd17 f70e5939 ffc00b31 68581511 64f98fa7 befa4fa4, digest len 0x1c | VERIFIED |
| 9 | 'rply'/'cmpg' handler FUN_0093c670 | 0x0093c670 | 0x53c670 | 0x53ba70 | Ghidra ev_8d92ebc1… | VERIFIED |
| 10 | callers of FUN_010b9300 (call rel32) | 0x93e238, 0x93e50c, 0xe6be5b, 0xe6d0d8 | | | Python E8 scan | VERIFIED (direct calls only) |

FUN_010b9500 (reads one chunk; Ghidra pseudocode, one decompiler):
1. start = tell(); seek(this[2]).
2. Four reads of 4 bytes, each passed through ntohl (WS2_32 ordinal 14):
   #1 tag, #2 field A, #3 length, #4 field B (converted, then DISCARDED).
   Short read on any -> failure path.
3. Length check: length <= size() - tell(); else seek-end + failure. Bounds check CONFIRMED.
4. A substream from start of (16 + length) bytes is fed to the SHA-224 context this[6]
   (thunk_FUN_016fd440). The header is hashed along with the payload.
5. visitor->vtbl[+8](tag, fieldA, base+tell(), length): payload passed raw, no decoding here.
6. seek(+length, relative).
7. If this[5] != 0 and tell() >= this[5]: finalize SHA-224 and compare 28 bytes with the
   0x1c block read in the header (this[3]); visitor->vtbl[+0xc](match). Whether a mismatch
   is fatal is UNKNOWN. What this[5] holds (end offset? declared size?) is UNKNOWN.

Byte-level confirmation (Python, all 3 samples): file[0x0C:0x28] == SHA-224(file[0x28:EOF]).
'rply' at 0x28 is a normal chunk (A=0, length = JSON length, B=0), so the JSON is
that chunk's payload.

FUN_0093c670: handles tag 'rply' 0x72706c79 (gated on FUN_00522ec0) and tag 'cmpg'
0x636d7067 (not seen in samples). Both: FUN_004e6d80(ptr,len) -> FUN_004fcc00 -> FUN_004f94a0.
Other tags: returns without action.

FUN_00b3c5d0 'pact': payload is wrapped by FUN_004e6d80 and appended to a container
(grow via FUN_0068fc80 when full; count at this+0x1c). Raw command bytes are QUEUED;
opcode deserialization happens downstream (consumer not yet located). Unknown tags,
including 'rply', fall through to the flag store at +0x24.

## Parser comparison
CONFIRMED: magic; BE header and chunk-header integers via explicit ntohl; 16-byte chunk
header; tag recognized as an integer; length = third u32; length bounds check; payload
handed raw to the visitor.
DIFFERS (parser stricter or narrower than the executable):
- Version: the executable accepts <= 1 (0 and 1). The parser accepts 1 only.
- Field A is passed to the visitor (meaning UNKNOWN); field B is ignored. The parser rejects
  non-zero values in both.
- The parser treats 'rply' + JSON as special header fields; the executable treats them as chunk 0.
- File-size equality: the parser requires it. No equality check found in the reader yet.
- Frame order star->pact->endt: the parser enforces it. No order enforcement found in the
  visitor (it only dispatches on tag).
- SHA-224 digest: both executable and current parser verify it (older parser comparison superseded).
NOT ADDRESSED by the executable evidence: little-endian layout inside pact payloads
(the decoding happens in the downstream consumer).

## Open
- Remaining command fields: opcode 0d nested serializer content.
- this[5] origin; whether a digest mismatch aborts loading.
- FUN_004e6d80, FUN_004fcc00, FUN_004f94a0, FUN_00522ec0 semantics.
- Hopper not used (demo install; Ghidra + rizin were sufficient).

## Session 3: pact consumer -> dispatcher -> opcode 0x08 (build 59638)

Address conversion: as above (.text file = VA - 0x401000 + 0x400).

| # | Item | VA | RVA | File off | Evidence | Status |
|---|---|---|---|---|---|---|
| 11 | replay frame loop FUN_00b3db10 (TNetworkEventSourceFromReplay vtbl) | 0x00b3db10 | 0x73db10 | 0x73cf10 | Ghidra ev_4ea358ce… | VERIFIED |
| 12 | pact list consumer FUN_00b3ea20 | 0x00b3ea20 | 0x73ea20 | 0x73de20 | Ghidra ev_1e924a6e… | VERIFIED |
| 13 | block reader FUN_00b29440 (u16 len + bytes) | 0x00b29440 | 0x729440 | 0x728840 | Ghidra ev_37b97e85… | VERIFIED |
| 14 | per-frame block store FUN_00b2c170 | 0x00b2c170 | 0x72c170 | 0x72b570 | Ghidra ev_d3d3f966… | VERIFIED |
| 15 | opcode dispatcher FUN_00b24050 | 0x00b24050 | 0x724050 | 0x723450 | rizin pd: movzx byte; add -2; cmp 0x20; jmp [eax*4+0xb241f4] | VERIFIED |
| 16 | jump table (33 dwords) | 0x00b241f4 | 0x7241f4 | 0x7235f4 | Python read; each case = push esi; call creator | VERIFIED |
| 17 | op 0x08 creator FUN_00b2fbc0 | 0x00b2fbc0 | 0x72fbc0 | 0x72efc0 | Ghidra ev_0ea526f5…; installs TNetworkActionLaunchFumigene vtbl 0x19a18cc | VERIFIED |
| 18 | length-prefixed string reader FUN_008fb4a0 | 0x008fb4a0 | 0x4fb4a0 | 0x4fa8a0 | Ghidra ev_06018019… | VERIFIED |
| 19 | TNetworkPacketReaderFromStream::Read (vtbl 0x19ea164 slot 1) | 0x010b94c0 | 0xcb94c0 | 0xcb88c0 | rizin pd: remaining>=n check, then raw stream read, no swap | VERIFIED |

Data path: FUN_00b3db10 builds TReplayActionVisitor, calls FUN_010b9500 per chunk until
a frame completes, then FUN_00b3ea20(pact list). For each pact payload FUN_00b3ea20 reads
u32 frame, u32 slot, u32 count (raw, native LE), then FUN_00b29440 reads u16 length +
block bytes; FUN_00b34480(slot) looks up the player; FUN_00b2c170(frame, block) stores the
block per frame. Opcode dispatch happens later via FUN_00b24050 (caller of the dispatcher
region and count linkage now traced; see research/count-loop.md and Session 4 below).

Endianness: packet reads are raw memory copies on x86 -> little-endian. CONFIRMED.
No per-command length field exists; each creator consumes exactly its own fields.

Opcode table (dispatcher case -> creator -> vtable installed in creator body):
0x02 Surrender, 0x03 Retreat, 0x04 CommitOptionPlayer, 0x05 Stop, 0x06 CreateGroup,
0x07 GiveOrderStandard, 0x08 LaunchFumigene, 0x09 CancelFumigene, 0x0a AnnuleProduction,
0x0b AnnuleLastProductionOfType, 0x0c ChangeProduction, 0x0d ProductionUnite,
0x0e ItemFinished, 0x0f Kill, 0x10 AddMaterial, 0x11 SpawnUnit, 0x12 SpawnUnitV2,
0x13 PlayerSynchroServiceAction, 0x14 SetTechnoResearch, 0x15 StopTechnoResearch,
0x16 DynamicCampaignEndTurn, 0x17 DeactivateWeapon, 0x18 DeactivateSupply,
0x19 GiveOrderBattleGroup, 0x1a AutoBattleResolution, 0x1b AvoidBattle, 0x1c CancelBattle,
0x1d LaunchStrategicAction, 0x1e BuyBattleGroup, 0x1f CancelBattleGroup, 0x20 EventPopup,
0x21 RetreatFromBattle, 0x22 ResolveConflictInZone (all prefixed TNetworkAction).
Opcodes 0x00, 0x01 and > 0x22 -> default path (0xb241f0). Class names are RTTI; behaviour
of each class is not analysed beyond 0x08.

Opcode 0x08 TNetworkActionLaunchFumigene, object size 0x2c, creator reads in order:
  read(obj+0x04, 4)    block[1:5]    u32   (data: 0xC000001E+slot, 226/226)
  read(obj+0x08, 16)   block[5:21]   raw   (data: 00*12 32000000, 226/226)
  read(obj+0x18, 12)   block[21:33]  raw   (data: plausible f32 x,y,z map coordinates)
  read(obj+0x24, 4)    block[33:37]  u32   (data: 0,1,2,3; text non-empty iff 3)
  FUN_008fb4a0(obj+0x28): read u16 T, read T bytes -> narrow string
Total 39+T bytes: matches all 226 sample instances. Any short read -> object destroyed,
creator returns NULL.
Semantics: class name LaunchFumigene (French "fumigene" = smoke/signal flare), with a
position and optional text label -> map flare/marker. Executable: VERIFIED class and layout.
Meaning of each field: INFERRED (no consumer/Execute analysis yet).

## Session 4: implemented counted-block decoding

The caller region around 0xb35aea loads the counter from stored block+0x58,
which is copied unchanged from the third pact u32. It attempts count dispatches;
NULL results continue the loop. Reader bounds checks are present; no exact-EOF
check was found in this loop exit. Exact-EOF enforcement is decoder policy.

All 594 multi blocks are now split with exact count and EOF. 571 have complete
supported layouts; 23 require explicitly opaque 0d envelopes and report framed.
New layouts 04/07/09/0a/0e/17 plus existing08; 0d boundary support only.
Complete instruction traces, failure exits, limitations and evidence IDs:
[Command layouts](research/COMMAND-LAYOUTS.md).
Canonical REA 6.7.0 MCP/Rizin Evidence: research/evidence/. No new Ghidra import,
target execution, global config change, or sample/binary redistribution.
[Census](research/coverage.json) is reproduced by research/coverage.py.

## Timeline milestone: execution handlers

REA MCP / Rizin execution traces extend RTTI-only labels:
- vtable+4 dispatch b24580 -> 07 b2cc90, 08 b2ced0, 09 b2c680.
- 08 -> player-context+124 manager aa3d00 -> graphical marker/position/type/text;
  graphics a9d730, label aa6a50. Type3 nonempty text shown.
- 09 -> same manager aa0620; compares manager-local ID, removes matching marker.
- 07 -> reference resolution -> b31e30 -> b32270 -> b32480 -> b32690 -> c972a0;
  order subtype and reference roles unresolved.

Complete chains, failure/no-op conditions, evidence IDs and confidence limits:
research/TIMELINE-SEMANTICS.md. All canonical records committed under research/evidence/.
No frame-to-seconds or metadata-to-slot identity mapping established. No Windows
execution, source mutation or inferred gameplay outcomes. Sample2 semantics remain
inferred because the available executable is build59638, not 510117427.

## 07 requested-order milestone

Recovered object+e0 requested kind; reflected OrderType table1d86488 and descriptor
1d868b8; kind-group dispatch c972a0 -> b32690 -> abd410 -> af9f60. Distinct from
object+e4 runtime token and object+f4 mode. Full20-byte actor/target reference roles
established; target-position argument from object+bc, effective destination unknown.

Matched samples:1797 explicit requests now classified (including Move481,
Attack399);8578 contextual39 requests remain partial. Sample2:31 explicit +55
contextual, all inferred. See research/OP07-ORDERS.md for precise claims/limits,
canonical evidence IDs, aligned instruction ranges and Ghidra startup limitation.
## Entity/context follow-up (2026-10-23)

REA MCP / Rizin. b2e070 separates20-byte references into u32 registry key and
16-byte validation GUID. ae5690 translates key; ae5730 resolves live pointer.
b5abd0/b5a630 map full GUID to saved-object pointer; conditional comparison with
live object+28 rejects stale/mismatched references. No unique unit/descriptor
meaning inferred for GUID words. Exact raw references retained and cataloged
within replay hash, never merged by shared tail or key alone.

c9a140 kind39 fallback: module registry+108 exists -> state+28 equals1 selects32,
otherwise33. No module -> ca0620 all member flag0x10 clear selects4, else9.
Earlier paths can select other kinds. Module class/flag name unproven. Runtime
values and reachability unavailable from decoded07. effective kinds remain null.
See research/ENTITY-CONTEXT.md for canonical evidence IDs, tests and state blocker.

## Public descriptor mapping follow-up (2026-10-23)

DescriptorId reflected at+0c (b5bf60); TSaveableDescriptor destructor b58aa0
removes that GUID from manager203b890+10. b5a630 reads same map; b2d263 resolves
GUID and b2d288..29b casts TModularUnitDescriptor -> TUniteDescriptor. RTTI base
chain: TUniteDescriptor -> TModularUnitDescriptor -> TSaveableDescriptor. This
establishes descriptor role for transmitted trailing16-byte validation material;
firstu32 remains runtime registry key. Translation can bypass validation, so wire
match does not prove accepted live entity descriptor.

Public58710 snapshot:726/726 exact GUID matches,722 Company_* +4 individual
units. No data-build match to 59638 or Sample2. --timeline --unit-data ROOT adds
opt-in cross-version descriptor/card/module annotations; actual unit_identity
and effective order39 remain unknown. Company/member bridge table missing.
See research/PUBLIC-UNIT-MAPPING.md, public-unit-coverage.json and canonical
REA ev_a170f55f / ev_2679b34d / ev_31396b02 / ev_091f83c9.

## Static company bridge / simulation boundary (2026-10-23)

c55fb0 registers TCompanyUnitModuleDescriptor.CompanyDescriptor at+18;
c1f730 property vtable19b2344 RTTI confirms refptr<TUniteDescriptor>.
Static reverse path: individual descriptor.Modules[CompanyUnit] -> selector
Default -> CompanyDescriptor. Invert actual matching-data references, retaining
missing/multiple matches. No live entity-key or GUID-word substitution.

dad680's TUnitListCompanyModuleDescriptor.PorteurDescriptor+18 uses helpera6a5d0,
vtable1998104 RTTI refptr<TGfxDescriptorPorteur>. Graphics reference, not a unit.
Other fields: CompanyMergeRadius+1c, spawn count+20, max count+24, spacing+28,
CanBeSupplied+2c. Static type association is not current live membership.

Original Data/WarGame/PC/59638/NDF_Win.dat identified in cached data-depot
manifest251062/7569342467126442184;24,199,168 bytes, expected content SHA1
bfd6c3e8affaad83a08ccff3271f6e4a5447e590. NDF not cached. Values extraction
blocked by missing original file, not proven transient-only reconstruction.
See research/COMPANY-BRIDGE.md and matching-ndf-target.json; canonical
REA ev_5a0ebdad / ev_c4c3078f / ev_01688e53. No decoder change or test rerun.

## Matching original NDF values recovered (2026-10-23)

Original 59638 NDF_Win.dat verified:24,199,168 bytes, manifest SHA1
bfd6c3e8affaad83a08ccff3271f6e4a5447e590; independent SHA25697d7442eecff5d0f836d5caee4d01cdf93bd7fe262ff12fef75f59fbc84638c0.
EDAT dictionary and everything.ndfbin entry MD5s pass. Read-only extraction,
expanded lengths/footer spans/120516-object count checked;367499 non-null
object refs match exact class IDs. No separator scanning/resynchronization.

Actual values:2121 CompanyUnit selector Default -> CompanyDescriptor paths,
all distinct inverse company GUIDs with one configured unit candidate. All 685
matching-build replay references resolve (681 company paths +4 direct unit GUIDs).
Sample2's 41 remain inferred. All selectors include an unevaluated shared filter:
ParamEquals_Integer ParamId11,ParamValue1. No claim that module is active.
Source debug names available; localized display-name dictionary absent.

Current REA ev_c71bc22a reconfirms typed CompanyDescriptor property; ev_1de49c5f
and ev_5c5c9e64 capture expanded NDF bytes/header/illustrative link endpoints.
Full durable result research/NDF59638-BRIDGE.md, extraction/coverage JSON and
research-only reproduction scripts. Decoder untouched; no simulation behavior.

## Opcode 0x0C creator (2026-10-26)

Jump table 0xb241f4[0x0c-2] -> case 0xb240f3 -> creator FUN_00b2eeb0 (file
0x72e2b0), object 0x118, vtbl 0x19a191c. Reads u32, raw16, then helper arrays
FUN_00b35cd0 (u32 array), FUN_00b35fc0 (u32 array, each <= 0x0e), FUN_00b290c0
x2 (16-byte points, kind <= 6), FUN_00b35cd0, FUN_00b29080 (u32 + raw16).
rizin `af; pdf` only, no Ghidra import. 47/47 authentic blocks fit exactly.
Layout CONFIRMED; field meaning TENTATIVE. Detail: research/CHANGEPRODUCTION-0C.md.
Implemented 2026-10-26 (wgrd_replay.py, tests/test_op0c_decoder.py); 02/13/18 followed the same day (research/FIXED-OPCODES-02-13-18.md).
