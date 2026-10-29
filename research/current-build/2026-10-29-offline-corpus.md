# Offline corpus research, 2026-10-29

## Scope and evidence

Based on remote `main` at `102b1b90371c339df18969e0de551c40364c61d0`.
This investigation used Python, REA 6.8.0, Ghidra 12.1.4 and a bounded Rizin
cross-check. No VM, Windows process, game launch or Cloud research was used.
Original replay and executable bytes were read-only. No player metadata is
published here; the cow is unchanged.

The native findings below concern the retained current executable, revision
**131544**, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`,
30,032,896 bytes. The embedded SVN revision was checked again. This was the
current installed executable identified in the preceding controlled experiment;
no online update check was performed today. None of the archive recordings is
claimed to have a matching executable. Initial historical triage was superseded
by current-executable traces; historical results are not authority for these new
interpretations.

Ghidra completed auto-analysis and returned decompiled functions and assembly
from this exact hash. The Java headless and native decompiler processes were
also observed. A running process alone would not establish useful analysis.
[Native excerpts](2026-10-29-native-excerpts.json) retain relevant current-build
addresses, pseudocode, assembly and source evidence IDs. These are curated
projections, not full canonical REA records. Original types/names are not recovered
source. The large `b31830` value-flow dossier is truncated; the conclusions below
use explicit assembly and bounded helpers, not an exhaustive value-flow claim.

[The manifest](../../samples/offline-corpus-manifest.json) pins all 71 selected
archive recordings by SHA-256, size, literal Version and command count. Product
attribution follows the earlier census's Red Dragon version-family/map evidence;
a digest establishes identity, not publisher authenticity. The other 28 recovered
older-title recordings are outside this task. Six earlier reference inputs are
identified by hash in the [measured summary](2026-10-29-corpus-summary.json).

## Archive 119: recorded slots are IDs, not dense indices

SHA-256 `ae30734792126a0a94a2de363e9d68ff1b33265ed9534b12f87a69ccb6be94c9`,
Version `430000244`, size 343,309 bytes. Baseline parser failure:
`pact slot 1 out of order at 0x463`.

The initial independent pact walker was research-only: command extraction did
**not** validate the whole replay. After the parser correction, the normal
`parse_replay(..., include_empty=True)` and `build_timeline()` paths independently
established:

- 3,979 consecutive frames, indices 0 through 3,978;
- 3,979 pacts, recorded slot 1 in every frame;
- 126 commands retained, including 103 standard orders and 15 production requests;
- valid embedded SHA-224, exact chunk bounds and command consumption;
- no unresolved timeline spans or malformed production interiors.

Current executable `b3dbc0` reads frame, slot and count, then the bounded command
block. At `b3dcbd` it calls `b33620` with the recorded slot; a lookup miss branches
at `b3dcc4` past dispatch. `b33620` hashes the supplied ID into a table at `this+7c`.
It does not compare it with the number of pacts already read. This trace does not
prove whether slot 1 resolves in archive 119's historical runtime.

The decoder now permits non-zero and sparse IDs, but still requires a strictly
increasing roster repeated in every frame. Duplicate IDs, descending IDs,
changed IDs/counts, bad frame boundaries, block-length errors and digest failures
remain rejected. Increasing/stable rosters are conservative **decoder policy**,
not alleged restrictions of the executable's lookup. `slots_per_frame` remains
a count, never maximum slot plus one. Slot IDs are not linked to metadata players.

All 71 pinned files now whole-parse and export **208,666 commands**. The earlier
70-file total was 208,540; the difference is archive 119's 126 commands. This is
structural compatibility, not playback validation.

## Standard orders: corpus constraints

There are **181,888** opcode `0x07` requests. The kind set is unchanged from the
six reference files. Kind 39 accounts for **131,759** requests: 107,542 have no
target reference and 24,217 have one. Explicit kind 6 has 17,897 requests without
a target reference and 991 with one. Consequently, target presence cannot be
used to label contextual requests Move or Attack, nor to reject explicit Attack.

Actor and target arrays retain all full 20-byte references and their ordering.
Summing distinct references **within each replay**, not deduplicating across
recordings, gives 22,024 actor references, 8,981 target references and 8,171 in
both roles. No per-replay lookup key was associated with multiple full reference
values in this corpus. That observation does not justify replacing the complete
reference with its leading key or treating references as global identities.
Current wrapper `b2be30` resolves `obj+60` and `obj+04` through `b2d210`, then passes
the `obj+04` result first and `obj+60` second to `b30fd0`. No ownership, registry
acceptance, unit-name mapping or resulting target state is reconstructed.

All transmitted position triples are finite; 13,899 are exactly zero. These are
arguments, not measured unit positions. The secondary float2 is finite in
167,903 requests and the all-positive-infinity sentinel in 13,985. Current
`bb0b50`, called from `b31830`, clamps the first two position components against
runtime bounds plus/minus a margin. The third component is not written by that
helper. Units, axes, map transforms, target-derived replacement and movement
outcomes remain unresolved. Zero is not promoted to an absent-position sentinel.

Current `c992e0` explicitly branches on kind 39 and consults runtime capabilities
and modules. The corpus does not supply that state. Existing contextual behavior,
null effective kind/position and unknown execution outcomes remain intact.

### Order queue option

The 36-byte structure begins at `obj+d0`. Current `aba270` copies byte fields
0..8, words at 0c/10/14/18/1c, and bytes20..23. It skips bytes9..11.
Those skipped bytes are nonzero in 72,449 corpus requests. They are padding in
this copy operation, not a proven flag or stable semantic signature. Their raw
bytes remain preserved; no blanket claim that every consumer ignores them.

A new request-side interpretation is justified for **structure byte +4**:

1. `b2be30` copies `obj+d0` through `aba270` and forwards the structure.
2. `b31881` reads byte+4; `b3189d` saves it in stack local `ebp-3e0`.
3. `b32f48..b32f61` tests that byte. Nonzero calls `b36d10`; zero reaches
   `b32f8e`, calling `abb3b0`.
4. `b36d10` loops over actors. For each actor it appends inline when that actor's
   list is empty, or calls `ac0d70` for a nonempty list. `ac0d70` writes at the old
   count and increments it: both branches append.
5. `abb3b0` clears the prior list before inserting the new request: replacement.

Corpus values: 0 in 178,342 requests; 1 in 3,546. The native branch tests nonzero,
not equality with one. Dispatch mode `obj+f4` is 1 in every corpus request and is
**not** this queue selector. Option byte+6 is 1 in 196 requests; its meaning is
still unresolved, and it receives no new semantic name.

`parameters.queue_request` adds `raw_u8`, `policy`, separate evidence status/build
and null `effective_queue_policy`. Its status is verified only for literal replay
Version `131544`, inferred for every other version. This does not upgrade the
existing build-59638 kind interpretation. The specialized group-kind-10 branch
is gated by `CMP ECX,0xa` at `b33091`, with a separate replacement call at
`b33210` (Stop under the existing kind classification). The published excerpts
include this gate and its surrounding branch chain. Other specialized paths can
bypass the ordinary branch. Thus
`policy` describes the transmitted option, not a guaranteed effective queue,
physical Shift-key input, or successful action.

## Production shapes

All **18,556** framed `0x0D` interiors consume exactly through the existing
production interpreter. This is 18,541 previously measured plus archive 119's 15.
Variants 1/2/3 occur 4,746/2,136/11,674 times. No serializer format or decoder
change is established by larger arrays.

The six-reference comparison finds the same **33 novel shapes**, now **133
occurrences** rather than 131: archive 119 adds two occurrences of the existing
novel six-group shape. Shapes count deployment points, quantity entries, nested
outer entries and inner lengths. They are not new opcodes or formats.

For variants 1/3, all 16,420 rows satisfy the existing points/quantity/obj+70 count
comparison. In 15,646 rows with nonempty nested arrays, each inner length equals
the corresponding requested quantity. The other 774 rows have an empty nested
outer array and shape `[1,1,0,[]]`. This is a measured relationship, **not** a new
acceptance rule. Nested values remain unnamed. Equality does not prove successful
unit creation, and empty or unequal nested arrays must not be rejected based on
this corpus correlation.

Archive 194, Version `430000610`, SHA-256
`b6831b8d0d8e9788580a4f9cfef39b9b3fcebe7f91a9bf3db05a8d824b8a22b1`,
has two 12-group variant-3 requests:

| Frame | Recorded slot | Command file offset | Shape |
|---:|---:|---:|---|
| 1816 | 19 | 1285317 | 12 points, 12 quantities of 1, 12 inner lists of length 1 |
| 20963 | 6 | 14847550 | Same shape |

The complete large-group locator list is in the summary. No current-executable
trace of the production nested-element consumer was completed in this pass;
its semantics remain explicitly open. Synthetic regressions exercise 12-group
payloads and nonmatching nested lengths without imposing the observed equality.

## Synchronization membership

Current creator `b2ef70` reads three u32 fields; vtable `19a02a8` points to execute
wrapper `b2c220`. That wrapper forwards fields+4/+8/+c through `b79760` to
`b7b8a0`. Rizin confirms `b79760` is a singleton load followed by a tail jump;
Ghidra's terminal-flow warning here is not evidence of an omitted continuation.

`b7b8a0` establishes bounded request semantics:

- +4 indexes the service table at manager+28, bounded by manager+2c.
- +8 == 0 adds +c to an enabled service's member list if absent.
- +8 == 1 removes +c if present, using a swap-with-last removal.
- Other operations have no traced add/remove branch. No new parser bound is imposed.
- Service presence, enabled state, existing membership and count thresholds gate
  changes and callbacks. Callback gameplay effects and service 0's purpose remain
  unresolved. This is **not** a battle-start event.

The add path has another unresolved side branch: when the member equals the
result of `ab1260`, it writes service byte `+0x61=1` and calls `58da80`. Neither
that value source nor the flag/helper effect is named here. At full list capacity
the code calls `68e990` before insertion; its growth/failure behavior was not
traced. The demonstrated bound is on the service-table index, not a proven bound
on membership-list capacity or a claim that these are all runtime effects.

All **222** corpus events have +4 == 0 and +c == enclosing pact slot, including
the nine newly observed values 4,7,8,9,11,12,15,17,19. Value 6 is absent; the corpus
does **not** cover every value 0..19. +8 is 0 in 181 events and 1 in 41. The 147
per-recording/per-slot sequences start at 0; transitions are 41 add→remove and
34 remove→add, with no consecutive equal operations. Archive 119 contributes
one of these events.

The exporter adds `player_synchro_service_request`, raw-preserving service index,
operation, member value, and a nullable `member_matches_recorded_slot` comparison.
The member value is not renamed player identity. Effective membership remains
null and outcome unknown. Status is partial for literal Version `131544`, inferred
elsewhere. Existing neutral parser fields are unchanged.

## Reproduction and regression coverage

Use Python 3.13–3.15. Set paths to existing private inputs; do not download or
publish recordings as part of this procedure.

```sh
export WGRD_CORPUS_DIR=/path/to/getuploader-20261029
export WGRD_UNIT_DATA=/path/to/pinned/wargame-data
python3 -B research/offline_corpus.py "$WGRD_CORPUS_DIR" > /path/to/census.json
# Optional shape comparison: append --baseline FILE for each of the six
# hash-identified inputs in 2026-10-29-corpus-summary.json.
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
python3 -B scripts/check_python.py
python3 -B scripts/check_docs.py
python3 -B scripts/check_preservation.py
git diff --check
```

The research script rehashes source files, requires every pinned recording,
whole-parses with empty pacts included, exports the timeline, checks declared
counts/known boundaries and exact production interiors, and emits counters and
source locators without metadata, player names or command payloads. It never
substitutes the independent pact walk for parser validation.

`test_sparse_slots.py` covers acceptance and whole-container rejection controls;
`test_order_queue.py` covers byte+4, mode independence, padding, build qualification
and Stop limitations; `test_synchro_requests.py` covers operations, unknown values
and build qualification; `test_offline_corpus.py` checks all 71 pinned files and
the two 12-group examples. The existing controlled-recording test allows only the
newly traced 0x13 partial interpretation; other top-level statuses remain guarded.
Without `WGRD_CORPUS_DIR`, private corpus coverage skips explicitly. A supplied
missing/altered corpus fails. Public CI cannot prove private-corpus compatibility.

Initial baseline: 164 tests passed on Python 3.14. After implementation: 182 tests
passed with the complete private corpus and existing fixtures available, no skips.
Final verification and independent review outcomes are recorded in the PR.

## Limits and unresolved questions

- Structural success and static code paths do not establish historical playback,
  accepted commands or simulation outcomes.
- Slot order/roster stability remain deliberately stricter decoder policies than
  the traced current consumer. Unknown-slot resolution and metadata mapping remain open.
- Queue semantics are bounded to the ordinary dispatch path, not all order handlers.
- Contextual effective kinds, coordinate transforms, secondary-vector semantics,
  other option bytes and live reference resolution remain unresolved.
- Production nested element meanings and matching historical consumers remain open.
- Synchronization service purpose and callback effects remain unresolved.
- The corpus comes from one archive source, not independent controlled experiments.
