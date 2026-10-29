# Revision 131544: actor-reference data flow and targeted experiment

## Scope and identity

Question: how does the serialized 20-byte actor reference become the `0x6e`
value observed in a queue-replace call, and is a queue actually modified?

Target: x86 PE32 revision 131544, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`,
Ghidra image base `0x00400000`. The exact retained executable and the
controlled replay SHA-256 were rehashed for this analysis. Ghidra 12.1.4 used
REA's read-only existing-project private copy; original analysis completeness
and settings are unknown. Pseudocode is reconstruction, not original source.
A private REA evidence bundle contains the cited records for the pinned
subject. The subsequent review identified unresolved details in this map; the
proposed experiment is not ready to run without resolving them. The previous runtime observations and
their limitations are in [the two-trace report](2026-10-29-frida-observations.md).

**Status:** static map and experiment design only. The queue handle `0x6e`
has not yet been connected to the replay actor reference. No mutation has been
observed for this request. A third broad tracer was interrupted after the
strategy change; its owned Python process was stopped, the Parallels job ended
with exit 255, and it has no final summary. The partial private trace is not
used as complete evidence. Readback found no tracer process; the
first 16 loaded bytes at each of its nine hook entries matched the executable,
and the game remained responsive. This is not proof of every aspect of agent
cleanup. No additional replay is authorized by this note.

## Address and calling-convention map

Offsets below are REA/Ghidra file mappings, not a generic PE arithmetic rule.
`cdecl` means the listed caller removes the indicated stack bytes; `thiscall`
means the observed ECX/stack and callee-cleanup pattern. Names are descriptions,
not recovered source symbols.

| VA | RVA | File offset | Observed call shape |
|---|---|---|---|
| `0x00b2be30` | `0x0072be30` | `0x0072b230` | ECX request, two stack words, `ret 8`; thiscall-style wrapper |
| `0x00b2d210` | `0x0072d210` | `0x0072c610` | four stack words, caller cleanup; resolver |
| `0x00ae48d0` | `0x006e48d0` | `0x006e3cd0` | ECX lookup object, two stack words, `ret 8`; thiscall-style lookup |
| `0x00b30fd0` | `0x00730fd0` | `0x007303d0` | seven stack words, `ret 0x1c`; caller also loads ECX, whose role is not established here |
| `0x00b31410` | `0x00731410` | `0x00730810` | eight stack words at observed call, caller cleanup |
| `0x00b31620` | `0x00731620` | `0x00730a20` | nine stack words, caller cleanup; splits copied values |
| `0x00b31830` | `0x00731830` | `0x00730c30` | nine stack words at observed call, caller cleanup; grouping dispatcher |
| `0x00c96440` | `0x00896440` | `0x00895840` | caller releases 0x28 bytes, including an 8-byte stack allocation; exact logical prototype remains uncertain |
| `0x00b2cc30` | `0x0072cc30` | `0x0072c030` | five stack words, caller cleanup; conditional group-member extraction |
| `0x00abb3b0` | `0x006bb3b0` | `0x006ba7b0` | three stack words, caller cleanup; replacement candidate |
| `0x00abb550` | `0x006bb550` | `0x006ba950` | one stack word, caller cleanup; queue clear helper |
| `0x00ac0d70` | `0x006c0d70` | `0x006c0170` | ECX queue object, one stack word, `ret 4`; append helper |

The `0x00ae48d0` file mapping is independently derived from REA evidence
`ev_9383e69c8135cd9313330bc8485f096d1b8f90cd3c5f9d339eda8a16ffb2afdc`.
All addresses are valid only for the pinned SHA-256.

## Static data-flow map

**1. Request and resolver input.** At `0xb2be60` ECX is retained as the request
object. `0xb2bee4` calls `0xb2d210` with the container at request+0x60;
`0xb2bef1..0xb2befc` calls it with request+0x04. The corresponding return
addresses are `0xb2bee9` and `0xb2bf01`. The second is a candidate
recipient-reference container; the prior trace did not dereference it. The 36-byte request structure is copied
from request+0xd0; the copy helper skips bytes 9–11, so do not demand those
padding bytes match later copies. Evidence: REA assembly
`ev_caadc737b2e707a2e169b044ccd3375c11d5b47201dc3fca6da0e313cfe47801`
and the existing current-build report.

**2. Container and resolved-object list.** `0xb2d2a4` reads container+0x54
as a count. `0xb2d2b2..0xb2d2cf` steps 0x14 bytes per entry: the first four
entries are inline, and later entries use the pointer at container+0x50.
`0xb2d2c9` reads the entry's first u32; `0x4f6e90` copies the remaining 16
bytes. `0x4f7710` copies the first word unchanged into a temporary key.
`0xae4830` looks that key up in a hash table: on a hit it returns a pointer to
a stored mapped word; on a miss it returns the original key pointer. The
resolver dereferences that pointer, checks a sentinel, and passes the resulting
word to `0xae48d0`. It then performs additional identity/context checks. The
semantics of the remaining 16 bytes and of the remapping table are not fully
established. On an accepted result,
`0xb2d3ac..0xb2d3ba` appends a resolved object pointer to the output list:
list+0x2c points to its pointer array and list+0x30 is its count. Failed lookup
or checks can drop an input. Evidence:
`ev_15052d2ab1d7f7b2b5de438b011bf6713c70b2dd853c46d5776154537a2da040`,
`ev_f11d0373ed974ad112eeca451132bf469de872f2c3b1349d007375f308a2d57e`,
`ev_f624989d946ae502e9ae014e3d153db95fbe1765b80558168ac4b18eef7c7f7b`,
and `ev_a3bbd6a8dbc97671a4009825ad2f7c9ade1e0c2a93f6420cc975e2b452408868`.

**3. Object to intermediate value.** In `0xb30fd0`, iterator helper
`0x5142e0` sets its current object from `[list+0x2c][index]`
(`0x5142e4..0x5142fb`). The wrapper reads current-object+0x1c at
`0xb31090..0xb3109c` and appends that u32 to a temporary vector. It passes that
vector to `0xb31410` at `0xb311da`. This establishes the operation for the
observed code path, not the semantic name of the field. Evidence:
`ev_9d2b5fcc227e9549c3ad1477ecad406a3ba34c4a233d55c5c9c9b3e64744cfd4` and
`ev_f4465322fbafbfe951343d9c254dd44132ac4d998ffcf3fc73ff3a6eb1232ab8`.

**4. Intermediate value to candidate handle.** `0xb31493..0xb314a1` supplies
each temporary vector word to lookup `0xae48d0`. A null return is skipped.
At `0xb314b7..0xb314ba`, the non-null returned object's +0x20 u32 is copied to
another vector. `0xb31576..0xb3157e` passes that vector to `0xb31620`.
`0xb316d3..0xb31717` branches on a predicate and copies each value into one of
two vectors. It then calls `0xb31830` for individual entries or for the other
group (`0xb31733..0xb31794`). At lookup `0xae48d0`, the first stack word is
compared/hashed and EAX is either zero or a pointer from a table; the role of
the second stack word is not determined here. Evidence:
`ev_9d0e6b80d1bc6c11e6ca832d6bb3e8e6bb7cbf89a1896bdcdddf784a0d1107d4`,
`ev_4f2e06ab82f55abbaed93f67b2037f94941cf972007a64fd74660b8a5dfa5593`,
and `ev_23ef364ae2ffe1e1cc99b608e2a1bdc6ff3395d309c2856a4add4e307d2d2d57`.
The runtime value `0x6e` may be this representation; equality has not been
measured across these stages.

**5. Group and submission vector.** `0xb31830` builds 39 group records of
0x14 bytes, calls `0xc96440` once at `0xb31b87`, then iterates indices 0..38
with the back-edge at `0xb33357`. One grouping write site stores a member's
input word as the first u32 of a 0x14-byte member record
(`0xc970ce..0xc97127`), using group index 22 or 23. The observed nonempty
record was index 4, so that particular write site does not explain the
observation. Its writer and predicate remain unresolved. A group record's
+0x0c is a member-storage pointer and +0x10 its count. `0xb2cc30` conditionally extracts the first u32 of
such members into an output vector (`0xb2cc50..0xb2cc81`): its first stack
argument has data at +0x08 and count at +0x0c, and its third stack argument is
the group record. It can also combine another vector, and later code can filter
or regroup values. Thus group count alone does not prove which value reaches
the queue helper. Evidence:
`ev_4b9e5497a5f44beb114b00e2634524ada9d65b6f8b6c815aeea2eb6cf4523ba0`,
`ev_676930f1bcff606831ad5f77db115ad8060c0929fcbb16dd57afcaae2c4af9bf`,
and `ev_e4e37b04409aa940ebec8c1dc8db4068b54232d8f4a8efb82a6dede7f6b612f8`.

**6. Queue mutation, if its guards pass.** `0xabb3b0` takes an input vector,
a pointer to an order word, and a context word. It uses each vector member's
low 16 bits to look up a queue object (`0xabb450..0xabb480`); that lookup and
its bounds can fail. On a successful lookup it passes that object to
`0xabb550`, which writes zero to queue-object+0x20 (`0xabb687`). Back in
`0xabb3b0`, if the word pointed to by the second stack argument is not
`0xffffffff`, it stores that word through the storage pointer at
queue-object+0x1c and sets queue-object+0x20 to 1 (`0xabb48b..0xabb4e3`).
Queue-object+0x14 is consulted as capacity. These queue-object offsets have
different meanings from the +0x1c and +0x20 fields of resolved objects above.
The captured raw second stack argument was a pointer value; the pointed-to word
was not captured. `0xb31830` calls `0xabb3b0` at `0xb32f8e` or `0xb33210`;
`0xb32f48..0xb32f61` selects the former or the alternative `0xb36d10` call
using a byte derived from its stack argument at +0x18. The selected call site
and byte for the matched request have not been established in this analysis.
These instructions establish a possible mutation, not that the prior runtime
call reached it. `0xac0d70` is a separate append path and is not assumed to
occur for this specific request. Evidence:
`ev_4b1514dfb018d10854f27b89fd4f3ebcd69c7dfb5fffe1eacc219ff5727cf58e`,
`ev_a2579c728ebee7bbc44899af29b076bfd5f74371e0782ea100c5609a9739d337`,
and `ev_f08b994d5836a587e2f5308cd533c0ce0409064b5329c6285834c3157cd907e8`.

## One proposed targeted experiment, not yet run

**Hypothesis:** the unique matching frame-1352 replay request resolves one
object whose +0x1c feeds `0xb31410`; that lookup returns an object whose +0x20
value flows through dispatcher/grouping to the queue vector's `0x6e`, and the
associated queue object changes to contain the supplied raw order value.
The equality and mutation are testable; neither is assumed.

1. Reverify the running process, module, file and loaded entry bytes. Strictly
   parse and hash the same replay. Derive the exact actor-reference and
   36-byte request-structure bytes from frame 1352/slot 0/offset 112616 rather
   than embedding private replay payloads in Git.
2. On `0xb2be30` entry, check only the bounded request count, the 20-byte
   inline reference and the 36-byte structure. Arm a unique per-thread root
   only on an exact match. A failed read, more than one matching replay command,
   or repeated matching runtime invocations is reported, not silently merged.
   Do not label the invocation as an observed runtime frame without a captured
   frame counter.
3. While that root is active on the same thread, capture resolver input and
   output at `0xb2d210`, distinguish the actor call by return address
   `0xb2bf01`, and record the input key, `0xae4830`'s mapped-or-original word
   at return address `0xb2d30a`, and the nested `0xae48d0` result at return
   address `0xb2d328`. Record the resolved-list count, first object pointer, and
   readable object+0x1c/+0x20 values. Capture `0xb31410` input and the nested
   `0xae48d0` result at return address `0xb314a6`, including the returned
   object's +0x20. Record pointer chains and nulls, not guessed meanings.
4. Capture the `0xb31830` actor vector count and members, the branch flag and
   helper return address. At `0xc96440` return, inspect group counts and all
   nonempty group members under an explicit bound; identify the writer and
   predicate for observed group index 4. Also capture `0xb2cc30`'s input group
   and output vector, and the `0xabb3b0` input vector and dereferenced order word.
   Preserve every member and group; flag counts beyond the bound as incomplete.
5. Before the first nested `0xabb550` clear for each queue object, capture its
   address, capacity, storage pointer, count and bounded contents. Retain the
   address only within the active parent `0xabb3b0` invocation; recheck readable
   ranges and snapshot again at the parent's return. The clear helper's return
   brackets the clear, not the later parent insertion. If lookup and guards pass,
   expected parent-return state is count 1 and storage[0] equal to the supplied
   word, or count 0 for the `0xffffffff` path. Identical before/after values do
   not prove no write occurred. A readable address does not rule out allocation
   reuse. Report failed reads, repeated aliases and lifetime uncertainty.
6. Gate all expensive child reads and event emission to the exact root. Hooks
   still add interception overhead even when gated. Keep a per-thread stack,
   call IDs, stack pointers and return addresses; detect unwinds, reentrancy,
   thread changes, callback errors, dropped events and event limits. No inferred
   relationship survives an integrity failure. Limit each read to 128 bytes,
   bound dereference depth and list sizes, and stop on ambiguous state. Keep raw
   output private. Compare a separate uninstrumented playback if measuring
   overhead or gameplay fidelity; one hooked run cannot measure either.

**Pass for the data-flow hypothesis:** a single unambiguous matching root has
complete, same-thread correlated captures; the resolver's actor reference and
object fields connect to the actual lookup input/return; dispatcher, grouped and
queue vector members agree by captured values and ordering; and the same
queue-object's before/after bytes show the relevant change. If a check or
identity differs, report the discrepancy. If a lookup is null, a capture is
missing, a bound is exceeded, queue contents do not change, or the pointer
lifetime cannot be supported, report the affected stage as inconclusive. A
queue-state observation is not proof of movement or other gameplay outcome.

The existing generic controller does **not** yet implement this root predicate,
scoped child capture, or parent-retained queue snapshots. The broad configuration
used in the second trace is not a substitute. Implement and test that focused
module before executing the proposed experiment; do not launch a replay merely
because this design exists.
