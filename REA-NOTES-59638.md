# REA notes: WarGame3.exe build 59638 (work in progress)

Target: ~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe
SHA-256 1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46, PE32 i386,
compiled 2021-10-12, ImageBase 0x400000, PDB path WarGame.Final.Win32.pdb (PDB not loaded).
Tools: REA 6.7.0 / Ghidra 12.1.4 (decompile), rizin (independent disassembly), Python (byte scans).

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
- SHA-224 digest: the executable verifies it; the parser does not.
NOT ADDRESSED by the executable evidence: little-endian layout inside pact payloads
(the decoding happens in the downstream consumer).

## Open
- Consumer of the queued pact payloads (opcode dispatch, LE field decoding).
- this[5] origin; whether a digest mismatch aborts loading.
- FUN_004e6d80, FUN_004fcc00, FUN_004f94a0, FUN_00522ec0 semantics.
- Hopper not used (demo install; Ghidra + rizin were sufficient).
