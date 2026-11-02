# Revision 131544: live owner/type bridge and damage lifecycle

Status: runtime owner/type attribution and three damage-to-lifecycle chains verified.
Shooter-role semantics, instance callsigns, battle-clock origin and replay-frame mapping
remain separate gates. This report does not turn six lifecycle calls into six kills.

## Provenance

- Original PE32 engine revision 131544, SHA-256
  `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
- Completed trace `wgrd-aar-combat-20261102-01.jsonl`, SHA-256
  `607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74`.
- Native index `unit-index-131544.json`, SHA-256
  `73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d`,
  generated from the authenticated [131544 archive](2026-11-02-unit-data.md).
- Parent verification: `aar-20261102T050816Z/parent-runtime-attribution-verification.json`
  outside Git. Every published chain below has exact source-line references there.

The trace has 6,188 enter/leave pairs, with no missing pair, suppressed event,
callback error, stale frame, stack mismatch, outstanding thread or cleanup error.
It detached normally. Hook addresses are preferred VAs for this build only.

## Owner bridge

`0xc52de0` adds 8 to ECX and tail-jumps to `0xb00690`, the previously recovered
handle lookup. All 365 sampled returns had a readable 128-byte header. In each,
return-object+`0x20` equalled the input handle read from module+`0x08`.
The 71 observed handles each mapped to one owner pointer and descriptor pointer
within this capture. That is bounded consistency, not a universal allocation-lifetime proof.

Observed return-object fields:

| Offset | Observation | Qualification |
|---|---|---|
| `+0x20` | local handle, equal to the lookup input | 365/365 sampled returns |
| `+0x28` | candidate descriptor pointer, subsequently joined below | exact runtime bytes available for the two relevant types |
| `+0x1c` | id-like `0xC00000xx` value | not authenticated as these members' wire registry keys |
| `+0x04` | not used for descriptor identity | the earlier experimental dereference was not a type proof |

The separate `0xae48d0` registry lookup had 243 successful header reads and
5,034 null-key returns. In those 243 readable returns, header+`0x1c` equalled
its input key. None of those returned pointers was one of the eight owners below;
therefore that observation does not authenticate their id-like fields as wire keys.
Null-source read failures are retained as such, not converted to zero-valued data.

## Native descriptor joins

The impact hook captured 128 bytes at its descriptor argument. Two runtime
pointers each produced one byte-exact GUID and name-token pair. Both fields
match one unique unit record in the native index:

| Unit type | NDF node | Runtime GUID bytes | Name token bytes |
|---|---|---|---|
| `Unit_VTT_323_NK` | 20147 | `000000000000000000000000db070000` | `15460c84e7810000` |
| `Unit_Merkava_IIIB_Baz` | 19537 | `00000000050000000000000014040000` | `bfc998bb09dfea05` |

The GUID is at descriptor+`0x0c`, token at +`0x60` in these captured headers.
The owner-header descriptor pointers match those read pointers. All six impacted
handles (31, 32, 33, 34, 39, 40) join to `Unit_VTT_323_NK`. Non-null source-candidate
owners 74 and 75 join to `Unit_Merkava_IIIB_Baz`.

These are live owner/type observations scoped to this process/capture. They do not
identify player names, callsigns, or a company-to-member registry relationship.
The wire company GUID differs from its member-unit GUID; neither is silently rewritten.

## Damage-to-lifecycle chains

All 28 impacts changed the expected accumulator: 25 suppression applications and
three physical-damage applications. The new trace reads module+`0x194` as 10.0
and +`0x198` as 800.0 without assigning their semantics. The damage descriptor's
+`0x1c`, used by the native threshold predicate, is independently captured as 10.0.

Each physical event below changes accumulated damage from 0 to the observed maximum
10, is followed by a check on the same damage object, and that check parents exactly
one owner/lifecycle call. The lifecycle operand's local handle equals the impacted
handle and its descriptor joins to VTT-323:

| Target handle | Source candidate | Engine deterministic seconds | Impact lines | Check lines | Lifecycle lines |
|---:|---:|---:|---|---|---|
| 33 | 75 | 806.4000244140625 | 10808-10809 | 10810-10813 | 10811-10812 |
| 31 | 74 | 806.6000366210938 | 10834-10835 | 10836-10839 | 10837-10838 |
| 39 | 75 | 830.7999877929688 | 12214-12215 | 12216-12219 | 12217-12218 |

All line references address the exact trace SHA-256 above. The threshold check
is `0xc9bf20`; its lifecycle call returns to `0xc9c0ce`, has argument 1, and
is nested beneath that check on the same thread. All three checks return AL=1.
The other 25 checks return AL=0 even though upper EAX bits are nonzero; full-register
truthiness would incorrectly label those calls successful.

The remaining three lifecycle calls have caller `0xb7c408`, argument 6 and no
recorded check parent, at the end of the match. They are reported separately as
end-cleanup observations. Timing alone is not used to count them as combat losses.

For the 17 non-null-source impacts, source-candidate owner+`0x28` equals the
captured descriptor argument. Eleven other impacts have a null source argument.
The pointer relationship is verified; its semantic role as shooter/weapon source
still requires the independent caller/queue provenance investigation. Source candidates
are not published as verified killers yet.

## Typed interface correction: owner+`0x60`

A bounded follow-up checked the capture's 17 non-null source headers and the
original PE. Owner+`0x60` is always vptr `0x01994500`. Its MSVC complete-object
locator is `0x01b87d40`, with **COL.offset** `0x60` and type-descriptor name
`.?AVsipTUniteGamePlay@@`. The primary vptr is `0x0199440c`. This identifies a
secondary interface subobject, not an inline callsign or per-unit name key.

At `0xc9c073..0xc9c084`, the code null-checks the resolved record+`0x08` owner,
adds `0x60` and passes that address to `0xa94b90`. The helper constructs a tagged
interface parameter (observed tag `0xc`); its parameter packing does not establish
an independently scored kill record. Earlier private "kill/name payload builder"
wording was too strong. Source-role attribution remains provisional.

`TKillablePtr` in adjacent RTTI concerns pointer/object lifetime; its name alone
is not evidence of combat death. The opaque dword at +`0x70` is not assigned a
float or pointer meaning. +`0x20` is not the only varying header field: +`0x04`
and +`0x1c` also differ across these owners. The already verified descriptor
GUID/name-token joins above are not replaced by incidental printable byte fragments.

Private receipts: `name-key-probe.md/json` and
`name-key-lead-verification.json` under `aar-20261102T050816Z/`. The lead check
matched 39 quoted instruction spans and independently decoded COL.offset; stronger
negative claims about all possible name recovery are not adopted.

## Clock and remaining uncertainty

The timestamps above are direct return-time reads of damage-module+`0x1ec`.
The [named deterministic-clock path](2026-11-02-aar-clock.md) supplies their engine
semantics. They are not inferred from wall time or obtained by dividing total frames
by match duration. Replay-frame, battle-elapsed and clock-epoch fields remain unknown.

Address-keyed histories are not global unit identities. Equal handles/pointers in
separate processes or captures are not joined. No claim is made that sampled lookups
exclude every allocation reuse between observations. Movement, ownership and weapon
attribution remain incomplete until supported by additional original-engine evidence.
