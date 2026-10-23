# WGRD counted command loop — read-only evidence report

Date: 2026-10-23. Repository: /Users/sein/Code/wgrd-replay.
Baseline HEAD: 3122ba7ded32ae1fcb8c97a215c02d5d138ddbca.
Target: /Users/sein/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe.
SHA-256: 1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46.

Method: actual REA 6.7.0 MCP stdio connection through the installed launcher;
execute_rizin_command with /opt/homebrew/bin/rizin. No Work MCP registration
change, download, target execution, new Ghidra import, or existing provider-session
modification. Ghidra availability was reported by binary_session, but Ghidra
analysis was not exercised. Rizin version is unprobed in these Evidence records.

## Verified count linkage

1. FUN_00b3ea20 constructs a block stream at local base EBP (constructor call
   0xb3eaa7). Reads three consecutive raw four-byte fields:
   - 0xb3eab9..0xb3eac6: destination EBP+0x74 (frame, sample-correlated).
   - 0xb3ead6..0xb3eadf: destination EBP+0x60 (slot, sample-correlated).
   - 0xb3eaef..0xb3eaf8: destination EBP+0x58, i.e. block+0x58 (count).
   Each read's false result branches to 0xb3eb8e.
2. 0xb3eb09 calls FUN_00b29440 for the u16 length plus block bytes. A failed read
   takes the same failure branch. 0xb3eb1d looks up the slot; 0xb3eb2d passes
   (frame, &block) to FUN_00b2c170 when that lookup returns non-NULL.
3. FUN_00b2c170's insertion path allocates a 0x60-byte stored object. The count
   copy is explicit: 0xb2c26c loads [source+0x58], and 0xb2c26f stores it at
   [destination+0x58]. 0xb2c275..0xb2c28d copies source stream bytes via virtual
   size/data/write calls. If the frame lookup already finds an entry, 0xb2c1b9
   branches directly to the function epilogue; the observed copy path is insertion.
4. In the caller region attributed by the prior notes to FUN_00b34ec0,
   0xb35a00..0xb35a28 uses the same map lookup helper FUN_005d9fb0 with the frame
   key and selects the stored pointer. Function ownership/extents were not
   independently re-derived in this pass; the instruction addresses are direct evidence.
5. 0xb35ad7 loads [stored_block+0x58]; zero skips the loop. 0xb35ae4 moves the
   non-zero value into EDI. 0xb35aea calls FUN_00b24050; 0xb35b23 decrements EDI;
   0xb35b26 jumps back while non-zero.

Conclusion: for this selected stored replay block and ordinary returning control
flow, the loop attempts exactly pact.count dispatcher calls. This is count-driven,
not an EOF-driven loop. It does not establish successful creation/application of
that many commands, runtime reachability on a particular replay, or action semantics.

## Reader and failure behavior

- Block constructor FUN_004f76b0 installs stream vtable 0x1929128 (0x4f7731).
  Its slot +0x10 resolves to FUN_00519210, which sets cursor field +0x40 to its
  argument. 0xb35ab9..0xb35ac0 passes zero: reset to byte zero before dispatch.
- FUN_010b3cd0 wraps that stream, stores its pointer at wrapper+4, and installs
  packet-reader vtable 0x19ea164. Slot +4 is FUN_010b94c0.
- FUN_010b94c0 obtains stream position and size and compares size-position with
  requested bytes (0x10b94dc..0x10b94e0). Insufficient remaining bytes returns
  false before calling the stream read. The underlying stream read
  FUN_00517710 copies bytes and advances +0x40 by n (0x51771c..0x517730).
  This describes the observed normal stream state; no broad malformed-state or
  integer-underflow safety claim is made.
- FUN_00b24050 requests one byte. Failed read or opcode outside 0x02..0x22
  reaches 0xb241f0 (xor eax,eax; return). An invalid opcode byte has already
  been read; the dispatcher has no rollback there.
- After NULL, 0xb35af9 skips processing and reaches the same decrement at
  0xb35b23. NULL does not break this loop. For a non-NULL result the loop calls
  FUN_00b24580 and then virtual slot +8; their behavior is outside this scope.
- On loop exhaustion, 0xb35b2e..0xb35b35 performs wrapper cleanup, then advances
  the outer iterator. No cursor==size comparison is present in this inspected
  loop exit. This is a local observation, not proof that no other layer checks
  consumption. Creator-specific partial-read/rollback behavior remains untraced
  except for previously documented opcode 0x08 behavior.

## Phase gate and next task

Count linkage is now supported by executable instruction evidence. No parser
changes authorized or made. Next: recover ONE creator's exact read layout, using
an observed fixed-size opcode such as 0x09 (current table maps to FUN_00b2edc0),
including branches, failure paths, and complete read dependencies. Then compare
against authenticated count==1 sample blocks. Only after all needed layouts are
proven should multi-command splitting be implemented, with exact count and exact
byte consumption as explicit strict-parser policy; the latter is not established
as an executable requirement by this loop.

Existing caveats remain: three samples from one independent source; Sample2's
game version lacks a matching analyzed executable. Older parser-comparison text
in REA-NOTES-59638.md and REPLAY-RESEARCH.md says SHA-224 validation is absent;
current committed code already validates it. No documentation edits in this pass.

## Evidence

Canonical inline REA Evidence retained in wgrd-count-loop-evidence.json. Each call
reports exit_code=0, completion_status=complete, artifact_changed=false and the
same post-call target SHA-256. Commands and provider limitations are retained.

- ev_4829a75998332e8123ed3e49d64fa0397b1b28efd1b8cda4968a9169e64a262b
  Command: `e scr.color=0; pD 0xb0 @ 0xb35ab7; pD 0x120 @ 0xb3ea20; pD 0x100 @ 0x10b3cd0; pD 0xa0 @ 0x10b94c0`

- ev_3c6567305e6b2ef33156e0f43996a572c9d326b227472bdc21334ec4ba72f8cd
  Command: `e scr.color=0; pD 0x240 @ 0xb2c207; pD 0x6c @ 0x4f76b0; pD 0xa0 @ 0xb359e0; pD 0x20 @ 0xb241e5`

- ev_a99a6fbf78964c346c6e0e6b50694cb3a0f3ed2f34fcf601ead1f972b036ea7d
  Command: `e scr.color=0; pD 0x130 @ 0x4f771c; pxw 12 @ 0x19ea164; pD 0x35 @ 0xb24050; pD 0x52 @ 0xb3eb4e`

- ev_5143920b98311e02bd3502d7690944be454e9abcfc5c11c3f940f363d9ddbed8
  Command: `e scr.color=0; pxw 44 @ 0x1929128`

- ev_57931860547e35a8a5aa3ccc7c11b0763a8b7ceb314542619cfe424518568b0d
  Command: `e scr.color=0; pD 0x22 @ 0x51a7b0; pD 0x10 @ 0x5167c0; pD 0x4a @ 0x519210; pD 0xe0 @ 0x517710; pD 0x55 @ 0xb2c170`
