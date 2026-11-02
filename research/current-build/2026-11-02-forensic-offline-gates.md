# Forensic capture: verified offline gates — revision 131544

Status: offline structural findings, not capture readiness. No new playback.
Pinned PE SHA-256:
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
Addresses are VAs at preferred base `0x400000`.

## Structural authority and listing audit

Ghidra 12.1.4's existing `WarGame3.exe` program is the structural index for
functions, references, call relationships, types and decompilation. A retained
private project copy was opened with `-readOnly -noanalysis`; no import or
analysis seeds were used. Recorded source-project file hashes remained unchanged.
The private copy lost a runtime journal backup, so no claim of completely
write-free project opening is made.

The existing `wgrd_ansi_text.lst` contains 7,323,196 byte-bearing rows. Every
represented byte matches the pinned executable, with zero overlapping or
unmapped rows. Its 526 omitted bytes form 36 all-zero ranges:

- 436 bytes lie inside the virtual `.text` extent; 90 are file-alignment tail.
- Ghidra defines no instructions or function bodies in those ranges.
- 23 ranges intersect defined data; seven have incoming references. Zero bytes
  are therefore **not automatically harmless padding**.
- Undefined/unreferenced zero ranges remain padding candidates, not proven
  unreachable code. Byte coverage is not proof of complete disassembly.

The verified original listing, sparse address index and exact omitted-byte
supplement are sufficient for lookups. They are retained privately under
`~/REA/wgrd-131544/`. The durable original-listing path is a hard link, not another
full data copy. A zero-inclusive 369,791,265-byte listing had already been generated
before the later gap-classification correction arrived; it is preserved but is
not used to infer structure or to turn embedded data into instructions. No more
listing generation is needed.

Private records: `existing-listing-verification.json`, `existing-listing-index.json`,
`original-gap-bytes.json`, `structural-query-results.json`, `lookup-resolution.json`.

## Receiver-local input records and an append path

All 28 impacts in retained trace
`6d88cefc03e1cf6a9bc4a3ddb70318569789d124266a37ffea1e5f5121601617`
have an entry pointer at impact argument 3, relative to its receiver:
25 at `+0x10`, three at `+0x84`. This is **not** the suppression/physical-damage
25/3 partition; the three second-slot observations are different events.

The independently reviewed static appender `0xc58a70` forms queue pointer
`receiver+0x10`, selects a 0x74-byte inline/overflow slot, calls `0xc4b0f0` twice
(prefix to temporary, then temporary to slot), writes fields `+0x68/+0x6c/+0x70`,
and increments `queue+0x164`. The corresponding receiver count is `+0x174`.
The prefix copy preserves defined fields, including `+0x08`; padding
`+0x59..+0x5b` is not copied and must not be used in whole-byte equality checks.

ABI distinction: append argument 1 is the prefix pointer; append argument 3 is a
scalar. Impact argument 3 is the entry pointer. A read contract that treats
append argument 3 as that pointer is invalid.

The cleanup helper's apparent base shift is explained statically:
`0xc4d990/0xc4d9c0` pass `module+0x10` to `0xc5c270`, whose inline offsets are
relative to that queue base. Actual appender/dispatcher execution in the retained
playback remains unobserved. No unique-producer or shooter-role claim follows.

## Handle decoding and lifetime boundaries

The existing Ghidra program and checked decoder bytes support a bucket/slot
reference layout, not the earlier worker's “generation-qualified handle” label:

- `0xb00690`: low 16 bits select a slot; high 16 bits select an 0x50-stride
  bucket; object-pointer arrays/counts are at `0x02037d34/0x02037d38` plus the
  bucket stride. It checks the object tag through `0x5c6aa0`.
- Bucket base is `0x02037cf8`. `0xafd4f0` scans the free map for a reusable slot,
  marks it occupied and writes `(bucket_id << 16) | slot` to its output reference.
  No per-slot generation comparison is present in the examined decoder/path.
- `0xafe1a0` sets the supplied reference to `0xffffffff` and clears its free-map
  byte. `0xb00750` also has a registry-delisting/slot-null path.

Do not turn this into a universal claim that no generation mechanism exists
anywhere. For this handle path, raw equality is insufficient across release and
reuse. Capture must maintain observed reservation/removal epochs and validate
actual object binding; reservation alone is not proof a unit object is live.
The notification hook at `0xa75c70` is not an allocation-free witness. Its
indirect or later effects must not be ruled out from local-body inspection.

## Typed lifecycle publication, not proven kill credit

Ghidra resolves `0xaf67b0` as a queue push copying a
`Eugen::IA::TIAKillGameplayMessage` record. It copies five payload dwords into a
pool-allocated record, stores the typed vtable and appends its pointer at
`queue_array[count]`, incrementing the count. Queue array/count offsets are
`+0x14/+0x18`, with capacity `+0x0c`.

Builder `0xafe8c0` preserves a raw reference at message `+0x0c`, resolves its
object pointer into `+0x08` through the same bucket/slot table, and copies two
additional opaque values at `+0x10/+0x14`. The reference is **not authenticated
as a generation counter**, nor are the opaque fields identified as a killer.

The type name and separate publication path do not establish a persistent
postgame kill ledger, victim/killer roles or independent combat-kill credit.
This is a useful typed lifecycle-message capture point. Result-model/UI joins
remain a separate capture gate.

## Frame-consumption structure: narrowed, not finished

The provider resolves interior address `0xb34bae` to containing function
`0xb34060`. Its decompilation and xrefs show a path beyond registration:

- A `+0x68` float accumulator is tested/decremented by the known 0.2 constant.
- A key derived from receiver `+0x6c` minus `+0xb0` selects entries from player
  maps; `+0x6c` is advanced on the step path.
- The function obtains staged values, invokes sink virtual methods, constructs
  a packet reader, iterates its count and calls `0xb23720` with context from
  `TGameplayServices+0x54`. It subsequently calls `0xab1570` on the non-ended path.

This refutes promotion of the earlier claim that only an outbound whole-map
packer matters. Conversely, it does not yet prove the frame-key-to-`+0xd0`
relationship, the runtime sink identity or battle-clock origin. Non-overlap of
clock-getter callsites is not evidence that a direct counter write/read cannot
occur elsewhere. Those remaining edges need Ghidra dataflow verification before
mandatory capture hooks are selected.

## Readiness and reproduction

The parent batch used the retained private Ghidra project, explicit containing-
function resolution and decompilation, with Java temporary/cache paths confined
to approved scratch. No shared REA rebuild or protected-project mutation was
needed. Private script/log/results are in `~/REA/wgrd-131544/`; append and static
review evidence is in `forensic-prep-01/` and `ansi-live-01/`.

Capture is **not ready**. Sender sequence and receiver audit mechanics have
focused tests, but controller drain integration, throughput/read-only preflight,
complete lifetime object binding and final frame/result contracts remain open.
These unfinished implementation changes are not part of this documentation
milestone. No boot or playback is authorized by these findings alone; the user's
approved gated execution strategy still governs.
