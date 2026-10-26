# Production commands, build 59638

Checkpoint: 79ff879. Scope: serialized production and cancellation requests.
The optional timeline now decodes all 514 observed 0x0d interiors, including 490
matching-build commands and 24 structurally matching Sample2 commands. Sample2's
semantics remain inferred. No Windows execution or outcome observation occurred.

## Evidence and method

Immutable PE32/x86 SHA-256:
`1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`.

`research/evidence/production59638-native.json` records native Rizin version,
commands, stdout, stderr, return codes, and unchanged input SHA-256. Reproduce:

```sh
python3 -B research/production_evidence.py > /tmp/production59638-native.json
python3 -B research/production_coverage.py > /tmp/production-coverage.json
python3 -B -m unittest discover -s tests -v
```

REA's MCP wrapper returned capability_unavailable when launching its Rizin
provider in this session. Direct installed Rizin worked; evidence is explicitly
native disassembly, not an REA envelope. Original executable and samples unchanged.
No sample-derived field guesses, game execution, installation or downloads.

## 0x0d object routing

b2fea0 installs network-action vtable19a1930. b28ef0 selects variants1/3 ->
vtable19b0180 (`TUniteWargameProductionData`), variant2 -> vtable19b01b4
(`TOutWorldUnitWargameProductionData`). Existing 18+L command framing is unchanged.

c0fad0 -> c06c20 handles variants1/3; c0f530 -> c06ba0 handles variant2.
Each enters through b580a0, which copies the complete child payload. b57f80 /
b599a0 create bounded nested views: u32 header, u32 length, then that many bytes.
The latter advances the parent past the entire section. b589a0 propagates errors.
b5abf0 reads the requested byte count from the current view and sets its error
flag on read failure. The offline decoder additionally requires exact scope/EOF
consumption. This is decoder policy, not proof of executable acceptance.

## Complete interior layout

Offsets below are object destinations, not serialized offsets. All integers are
little-endian. Counts precede their arrays; allocation/capacity branches do not
change the wire fields. Both nested header values remain raw.

| Sequence | Destination / helper | Wire fields |
|---|---|---|
| Base scope | b53df0 -> b57f80 | header, length, u32 -> obj+04 |
| Player | b074c0 | one u32 -> resolved obj+08 |
| Type-bundle scope | bd01e0 -> b57f80 | header, length, three 16-byte references, u32 -> bundle+0c |
| Variant2 only | c06ba0 | u32 -> obj+1c, u32 -> +20, u32 -> +24 |
| Variants1/3 | c061f0 | count, then 3 float32 + u32 per deployment point -> obj+1c array |
| Variants1/3 | a75940 | raw u32 token -> obj+68 |
| Variants1/3 | c06c81 / c06c8e | u32 -> obj+6c, u32 -> +70 |
| Variants1/3 | c06070 | count, then u32 per group -> obj+74 array |
| Variants1/3 | c06caf / c06cc9 / c06cd9 | u32 -> obj+90, byte -> +94, byte -> +95 |
| Variants1/3 | c069a0 | outer count, then count + u32 array for each entry -> obj+98 |
| Variants1/3 | c06cfb | byte -> obj+96 |

bd01e0 calls a66fc0 three times, each reading exactly four u32s. a66fc0 constructs
the GUID with4f71d0 without rearrangement, then b5abd0 -> b5a630 resolves it through
the saving-system registry. Offline enrichment matches these exact16 serialized
bytes to the existing original59638 NDF index. No arithmetic or GUID rewriting.
The fourth bundle word and all three reference positions remain separate.

Null references remain explicit. Nonzero unresolved references retain their GUIDs.
Some exact descriptor matches have no configured-unit candidate: in Sample1 these
are four Building_FOB_* descriptors. The decoder does not invent localized names.

## What the consumer establishes

b2d0a0 calls production-data virtual+24 (validation), virtual+20 (manager), then
ba5520. ba5520 invokes virtual+28: c09820 for variants1/3, c095d0 for variant2.
These functions check live player state, resource balance, availability, mode and
placement before dispatching production. Static decoding cannot tell which path ran.

For variants1/3, c0ce90 multiplies bundle cost (bcdcd0) by each obj+74 entry and
sums the results. bcdcd0 sums costs from the three resolved bundle type references.
c09820 also sums obj+74 entries for an availability check and iterates obj+70
production groups. c0b190 indexes obj+1c points by group, passes obj+74[group]
through c07290 into typed input field0x3e, and passes bundle references to request
construction. This supports **requested group quantities**, summed as
`requested_quantity`; it does not establish individual physical-unit counts.

The position array is a deployment argument: c0b190 copies the selected point
into a float3 and routes it through mode-specific placement logic. The point can
be replaced or rejected. Export finite transmitted points, raw bytes and the fourth
u32 control. Leave effective positions null. Axes/units remain unresolved.

obj+70, position count and quantity-array count are independently serialized.
Report their agreement; do not enforce equality or silently zip/truncate arrays.
obj+68, +6c, +90, +94/+95/+96 and the nested arrays retain neutral names. Observed
variant1 and mode1 coincide; variant3 and mode2 coincide. This observation alone
does not establish phase names or queue/append semantics.

Variant2 uses a separate scalar body. c095d0 performs a distinct out-world
production path. No quantity or deployment point is assigned to it; +1c/+20/+24
stay raw. A catalog class name alone does not establish a field as a queue ID.

## Cancellation: 0x0a

Existing layout remains unchanged. b2c410 resolves the player reference, then
passes obj+18 and obj+1c through b246b0. The first selects a player production
manager through c182a0; ba6310 compares the second with queued entries' +8 fields.
If an entry is found, b24752 calls ba5990. Export `cancel_production`, raw manager
channel and request ID, with `matched_purchase = null` and unknown outcome.

No reliable join from this queue ID to a serialized 0x0d field is established.
Do not subtract these requests from purchase totals. 0x0b has no authentic
occurrences in this corpus and remains unsupported. 0x0c ChangeProduction has
47 authentic records, including13 in Sample1; its interior is decoded structurally (see [CHANGEPRODUCTION-0C.md](CHANGEPRODUCTION-0C.md)) and exported as timeline action `change_production_request` with raw-field parameters; field meanings and consumer remain unresolved.

## Corpus results

| Sample | Build semantics | 0x0d | Variants1/2/3 | Quantity sum, variants1/3 | 0x0a |
|---|---|---:|---|---:|---:|
| 1 | matching59638 | 233 | 49 / 31 / 153 | 255 | 16 |
| 2 | inferred510117427 | 24 | 12 / 4 / 8 | 43 | 0 |
| 3 | matching59638 | 257 | 118 / 9 / 130 | 351 | 64 |

Sample1 frame1 slot0 requests the bundle **#command STAF EENHEID + DAF YA 4440**,
quantity1, with point (1131642.25,986633.375,32760.0). Frame1 slot1 requests
**#command GROUPE DE CMDT + VAB**, quantity1. These establish requested configured
types. They do not prove purchase acceptance, arrival, ownership or live position.

## Integration and verification

`wgrd_production.py` adds bounded request interpretation to `--timeline`.
`--unit-data research/unit-data/build59638-v1.json.gz` adds `production_types`:
exact GUIDs, configured-type candidates, localization and existing NDF provenance.
Events reference those entries by `type_id`. Enrichment does not mutate events.
Every request retains its original parser fields and complete raw command bytes.
Invalid interiors retain an opaque event and a malformed payload-layout diagnostic.

The default parser keeps its original opaque/framed status and byte-compatible
output. Its counters describe the original layout API. Optional production
interpretations separately report `payload_layout_status = complete`.

81 tests pass, including10 production tests. Authenticated census confirms exact
all-command byte retention, all514 interiors consumed, deterministic repeated
exports, and default parser equality with79ff879. Static index candidates remain
missing for4 distinct Sample1 GUIDs and8 Sample3 GUIDs; no guessed names.

No battle report regenerated. Contextual39 remains3318 Sample1 /5260 Sample3
(50 of54 standard orders in the declared push still contextual). No execution
outcomes became known. Next runtime milestone requires successful matching-build
playback before instrumenting position/combat/destruction paths; a Parallels guest
is a candidate environment, not yet verified.
