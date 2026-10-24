# Original playback / position observation — bounded feasibility

Baseline790572d. Localized integration already committed f5e41cc; Sample1
validation790572d. No pending decoder work in this pass. No game execution,
download, installation, simulation replacement or original-asset modification.
REA6.7.0 MCP stdio, execute_rizin_command through installed Rizin. Original
PE32/i386 Windows GUI image SHA256
1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.

## Decision / first milestone

**Local playback blocked before launch.** Checked host is Darwin/arm64. No
Steam/Wine/CrossOver/Whisky/Parallels/VMware/UTM app name in /Applications or
~/Applications; standard Steam steamapps absent. No wine/wine64/wine32,
qemu-system-x86_64, prlctl, vmrun or VBoxManage on PATH. LLDB exists but is not a
Windows execution environment. Bounded checks do not exclude external/remote
hosts or tools outside these locations. No native-Mac replay compatibility claim.

Game cache has executables, root DLLs, redistributables and NDF archives. Base
data/graphics packs and Tohoku map absent. Localization archive exists separately
in project work/ and has not been staged into the original game tree.

Pinned data depot251062 / manifest7569342467126442184 contains640 files,
22,894,585,504 logical bytes, including later builds. This is not the59638 minimum
or a compressed download estimate. A conservative Sample1 prerequisite candidate
set contains58 files /11,103,890,752 logical bytes;56 absent from game tree.
Only target executable and59638 NDF present at their selected paths and both
content SHA1s match. Selected version-specific DLLs absent even though root DLLs
exist. Full per-file expectations: runtime59638-prerequisites.json.

Important missing examples:

| Manifest path | Bytes |
|---|---:|
| Data/WarGame/PC/48574/Data.dat | 1090150400 |
| Data/WarGame/PC/48574/DataMap.dat | 89399296 |
| Data/WarGame/PC/48574/ZZ_3a.dat | 4165189632 |
| Data/WarGame/PC/48574/ZZ_3b.dat | 3068952576 |
| Maps/WarGame/PC/_2x3_Tohoku_v11.dat | 165871616 |

Candidate selection includes base resource packs and relevant patch paths through
59638, matching NDF/executable/DLLs and Sample1 map. It is **not** a validated
minimal or sufficient install. Actual file opens, working directory, launch route
and asset patch precedence remain unobserved. Cached manifest signature not
independently revalidated; original NDF/executable content authenticated separately.

## Runtime dependencies from executable

REA evidence ev_fab8ee36… records PE architecture/image base/PDB path and import
libraries. Imports include steam_api.dll, MSVCP140.dll, VCRUNTIME140.dll, UCRT
api-ms-win-crt-* DLLs, D3D11, D3D9, DXGI, OpenGL32, XInput9_1_0, WMVCore and
ordinary Windows system libraries. Require a Windows-compatible32-bit process
environment with those imports satisfied. Cached2019 VC++/DirectX installers exist;
none run here. Import presence does not establish which renderer initializes,
Steam authentication/DRM policy, or that all listed API paths run during replay.

Renderer behavior on this ARM Mac, Steam launch requirements, command-line replay
switches, old-build selection and playback synchronization are untested. Do not
invent flags, bypass Steam checks, or mistake a later root WarGame3.exe for59638.

## Executable references / observation candidates

All VAs assume preferred ImageBase00400000. For another loaded base use
loaded_base + (VA -00400000); validate process image hash first.

| Area | Reference | Established scope |
|---|---|---|
| Replay block count/dispatch | b3ea20 -> b2c170; b35ad7..b35b26 -> b24050 | Existing counted-block evidence; dispatch attempts driven by count |
| Opcode07 order path | b2cc90 -> b31e30 -> b32690 -> c972a0; b33c5f -> abd410 -> af9f60 | Existing request grouping/submission; not final world effect |
| Submission wrapper | af9f60 -> af9fa0; af9fa0 -> af8840 | Fresh aligned instructions; no claim this is the simulation tick |
| Wire-to-live lookup | ae5690/ae5730; b5abd0 -> b5a630 | Existing translation/validation evidence; ae5730 is a keyed lookup |
| Internal handle lookup | b014f0 | low16 indexes a table selected by high16; table stride50h; pointer checked through5c7b80 ==1 |
| Company member array | 6e2140 | Copies module+30 pointer and+34 count; no ownership or member identity assigned |
| Stored-position access | c7e350 -> da4d20 | Runtime table lookup, then three stored values copied; detailed limit below |
| Position-module RTTI | vtable19a2884 -> COL1b9d888 -> TypeDescriptor1eb06ec | TPositionModule; constructor b4fcd0, object allocation100h |
| World updater RTTI lead | vtable19ace58 / TypeDescriptor1ec2114 | TWorldUpdater@WorldUpdater@IA; name only, no tick function established |
| Damage RTTI lead | vtable19b3ac8 / TypeDescriptor1ed6f40 | TDamageModule; no health field, damage application or death path established |
| Spawn command classes | opcode11 SpawnUnit,12 SpawnUnitV2 | Existing RTTI/dispatcher mapping; not proof of live spawn implementation |
| Destruction | Unresolved | No verified destruction/lifetime hook in this pass |

Tick, final position writer, health/damage writer and spawn/destruction lifecycle
remain untraced. Do not expand these searches before establishing playback.
RTTI leads are navigation aids, not recovered behavior.

### Concrete stored-vector candidate

Fresh REA evidence ev_fab8ee36…:

- c7e376 loads global201f660; c7e37f selects registry slot+1f8; c7e38b loads
  table provider from2027ed0 indexed by that slot ID.
- Virtual call+3c obtains table pointer/count. c7e3b7..c7e3c1 uses the low16
  of the supplied internal handle to select a pointer, with a count check.
- c7e3c8 calls da4d20 with that pointer in ECX. c7e3cd..c7e3e6 copies three
  dwords to an output buffer, then calls bb1a20. The latter's exact behavior is
  untraced here; the earlier bb19b0 clamp finding is not transferred to this callee.

Fresh ev_6c822034… contains the entire getter:

```text
00da4d20  mov eax, [ecx+3c]
00da4d23  add eax, 30
00da4d26  ret
```

Thus a passive breakpoint at da4d26 could read12 bytes at EAX, or compute
`*(ECX+0x3c)+0x30` at entry, without invoking a function or changing game memory.
This observes a stored vector before the caller's bb1a20 processing. Read it as
three raw words plus float interpretations; reject null/unreadable/nonfinite data.

**Not yet an individual-unit position hook.** The caller uses the registry family
previously associated with company modules. A company center, member position or
other aggregate has not been distinguished. Pointer field+3c -> TPositionModule
is not proven by this accessor alone. TPositionModule constructor b4fcd0 installs
its RTTI-backed vtable and initializes+30/+34/+38 to +Infinity (ev_aa4439a7…);
matching offsets support investigation but do not establish the pointer's class
or live field meaning. No direct ECX/runtime-reference correspondence assumed.

Do not substitute a735d0: it returns `([ECX+e4] & ~3)+70`, with another object
layout whose world/graphics role is not established here. No float-memory scan
or guessed address treated as a successful observation.

## Smallest next experiment

**Stage0: original playback, no instrumentation.** Needs an owned, complete
Windows installation/compatible host supplied or separately prepared. Prefer
using an existing setup; no cloud, VM or compatibility installation selected here.

1. Open Sample1 through the original replay UI/known installation launch route.
   Record actual process image path, SHA256, loaded module base and renderer.
   Continue only if executing the pinned59638 image. Do not assume root launcher
   or a guessed replay switch selects it. Record missing-file/loader errors.
2. Confirm the frame131 marker text `leave your cv at base`, then the known
   frame1050 explicit Move request. These are decoder anchors, not an assumed
   frame-to-seconds formula. A screenshot alone cannot prove exact frame alignment.
3. Record whether replay advances without visible desync. A second playback is
   useful for repeatability only after first success. Do not demand end-screen
   equality as a substitute for an actual state comparison.
4. Stop on launch/build mismatch, missing assets or replay failure. Capture the
   concrete failure; no renderer/DRM bypass or speculative repair loop.

**Stage1: one passive observation, only after Stage0 succeeds.**

- Prefer a debugger logging/hardware breakpoint without replacing original files.
  At c7e3c8/da4d26 record caller, ECX, internal handle at caller's EBP+0c,
  returned pointer/raw12 bytes and loaded image base. No injected getter calls.
- Correlate to one validated runtime reference through the existing resolver;
  expanding a company to a member needs an observed live member array. A memory
  match to packet reference bytes is not an entity-pointer proof.
- First success criterion: same validated entity/module across two playback
  observations, finite stored vector consistent with visible movement. Coordinate
  axes/scale and whether it is an aggregate remain explicit until validated.
  Instruction/command sequence and sample frame are not a verified simulation tick.
- Once pointer and lifetime checks hold, a hardware write watchpoint on the vector
  can identify its actual writer. Do not infer the writer from requested Move
  targets. Stop before health/spawn/destruction analysis if this basic link fails.
- If observing order resolution later, inspect final grouped dispatch, not only
  c9a140 fallback. Earlier c972a0 paths matter. Dispatcher b24050 itself does not
  provide established tick/slot arguments.

No Stage0 or Stage1 execution attempted: prerequisites fail locally. No unit
trajectory, live tick, effective order39, health value or destruction observed.

## Reference/ownership review checks

runtime59638-reference-census.json authenticates each sample and counts actual
opcode07 actor arrays separately from targets:

| Sample | Full20 references | Validation GUIDs | Actors appearing under multiple slots |
|---|---:|---:|---:|
|1 matching59638|285|103|0|
|2 inferred510117427|41|29|0|
|3 matching59638|400|181|30|

Multiple full references share a descriptor; same type does not merge references.
Sample3 falsifies the proposed global commanding-slot ownership shortcut.
Shared control, reference reuse and other explanations remain unverified. No
friendly/enemy labels derived. Static labels685 matching +41 inferred preserved.

## Reproduction / evidence limits

```sh
python3 -B research/runtime59638_prerequisites.py > work/runtime59638/prerequisites.json
rizin -N -q -c 'e scr.color=0; pD 7 @ 0xda4d20' \
  /Users/sein/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe
```

Actual REA MCP launcher: ~/.hermes/tools/rea/node_modules/.bin/rea mcp; tool
execute_rizin_command(path,command). Canonical records retain command arguments,
provider, target digest and limitations. All five report completion_status complete,
exit_code0, artifact_changed false. No Ghidra import or game/debug session opened.

- ev_fab8ee36…: imports, c7e350, af9f60/af9fa0 prefix, ae5730.
- ev_6c822034…: complete da4d20, a735d0, b5abd0, b014f0.
- ev_6917c61e…: module serialization wrappers and6e2140. da4c80 is an exploratory
  interior/misaligned range; excluded from semantic claims.
- ev_158a9562…: partial constructor range and position-module vtable; superseded
  for constructor entry by the next record. Trailing truncated instructions excluded.
- ev_aa4439a7…: aligned b4fcd0, d9f6c0 constructor, RTTI COL/type bytes.

RTTI candidates recovered from raw PE typed-descriptor/COL/vtable pointers in
scratch; only TPositionModule linkage independently captured in the REA bytes above.
World/damage names remain low-confidence navigation leads. No exhaustive xref or
simulation-loop claim. Original image hash unchanged after this pass.

Verification: prerequisite script executed; present candidates matched pinned
SHA1s; reference census reproduced; evidence completion/digests checked. Decoder
code unchanged; prior71-test implementation result not rerun for research-only work.
