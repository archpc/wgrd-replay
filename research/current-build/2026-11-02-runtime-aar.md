# Runtime AAR export — type attribution and witnessed destruction chains

Date: 2026-11-02. Build 131544. Status: one capture reanalysed read-only; the
export is additive and keeps the legacy 28-event exporter byte-compatible.

> **Superseded in part (2026-11-02, [causal chain](2026-11-02-causal-chain.md)).**
> The exporter now labels source owners `engine_credited_damage_source` on
> static XP-credit and producer evidence. The legacy profile is retired from
> the maintained exporter and reproducible from commit `71c4f8e`. The
> observations below are unchanged.

## Sources and pins

| Input | Identity |
|---|---|
| `wgrd-aar-combat-20261102-01.jsonl` | SHA-256 `607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74`, 12,382 records, 4,497,537 B |
| `units/unit-index-131544.json` | SHA-256 `73d5912746ae5b278dfd77c29bc84dc96b0e8d28cc9a79b765bf91c0851a411d`, 4,563,368 B |
| Source archive `NDF_Win.dat` (via index `source`) | SHA-256 `172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b`, build 131544 |
| Executable `WarGame3.exe` | SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d` |
| Clock binding excerpt `deterministic-clock-bindings.asm` | SHA-256 `b0e2177f5542710a0c8273fc76c72fa04dd14c0a1f0011d54d4aafe645dfe974` |
| Capture config `aar-capture-131544.json` | SHA-256 `f904c7ed526129148fc41857ee3e981f5531cc26c3c3b684f85c2ebfe7e25ba0` |

The earlier delegate reported missing capture-era sources after comparing them
with the changed working copies. Integration recovered the exact files from Git
base `6c9df99` plus the preserved `prior-work.patch`: `hooks.js` hashes
`f398ffa3febc93dfd5ea733866a5464eec9e277f9613f58bd17602e72fbc158e`, and
`wgrd_frida.py` hashes `3d3cb50212f0731367203cfbb6eb62d7ada9a37f2e5130002ff842987164c0bc`.
Both match the original capture manifest. They and the matching config are retained
privately in `aar-20261102T050816Z/capture-sources/`, with a reconstruction receipt.
File-based extraction verifies those exact copies; current code is not substituted.

## What was verified from the raw trace

* 6,188 enter/leave pairs, 12,376 emitted records, 0 duplicates, 0 unpaired,
  0 stale frames, 0 stack mismatches, 0 callback errors. Per-hook counts:
  28 impacts, 28 checks, 6 owner destroys, 459 sampled clock reads,
  365 sampled owner lookups, 5 order wrappers, 20 remaps, 5,277 reference
  lookups.
* The stride rule holds: `emitted = floor((invocations-1)/997)+1` for the
  clock (459 of 456,902) and owner lookup (365 of 363,897); every sampled
  ordinal is `1 mod 997`.
* Every impact's 96-byte `+0x190..+0x1ec` block on leave equals the following
  destruction check's enter block (28/28), and the check's `ecx` and `+0x08`
  handle equal the impact's (28/28).
* 25 impacts change `+0x190` (mode 1); 3 change `+0x19c` 0 -> 10.0 (mode 2,
  ordinals 3, 7, 21). `+0x194` is 10.0 and `+0x198` is 800.0 for all 28;
  their semantics are **not** asserted. Unit 34 reaches `+0x190 = 800.0`
  (ordinal 26) without a destruction call.
* Check return is a low-byte boolean: 25 checks return `0x3c221900` (AL=0,
  no nested destroy) and 3 return `0x1` (AL=1). Upper EAX bits are never
  treated as truthy.
* The three AL=1 checks each parent exactly one `owner_destroy_candidate`
  with return address `0xc9c0ce` and argument `1`:
  ordinal 3 / handle 33 / check 737948 / destroy 737953 (L10810-L10813),
  ordinal 7 / handle 31 / check 738698 / destroy 738703 (L10836-L10839),
  ordinal 21 / handle 39 / check 818611 / destroy 818616 (L12216-L12219).
* Three further destroys use return address `0xb7c408`, argument `6`, no
  recorded parent, retvals 1/2/3, on handles 0/74/75 (L12364-L12369). These
  are end-of-match cleanup calls, exported separately and never counted as
  damage lifecycle or kills.
* Owner bridge: 365 sampled `owner_lookup_candidate` returns; input handle
  equals returned `+0x20` 365/365; 71 distinct handles map to one
  `(object, descriptor)` pair each; every destroy operand's `+0x20`/`+0x28`
  equals the sampled lookup for that handle. All six destroy headers are
  byte-identical on enter and leave.
* Descriptors captured as 128 bytes on `arg2`: 17 source-bearing impacts
  carry `0x50f15bb0` and 11 null-source impacts carry `0x50fa72e0`; GUID is
  at `+0x0c`, token at `+0x60`, repeated reads are byte-consistent.
* The generic reference registry does **not** authenticate these owners:
  5,277 `reference_lookup` calls, 243 readable headers, 5,034 null-key
  unreadable returns, `+0x1c == arg0` 243/243, but 0 of the 8 damaged/source
  owner objects appear among the 26 distinct returned objects. `+0x1c` is
  not promoted to a wire key for them.

## Unit type attribution (2-of-2 static join)

| Runtime descriptor | GUID | Token | Node | Type | Status |
|---|---|---|---:|---|---|
| `0x50f15bb0` | `00000000050000000000000014040000` | `bfc998bb09dfea05` | 19537 | `Unit_Merkava_IIIB_Baz` | `2_of_2_exact_guid_and_token` |
| `0x50fa72e0` | `000000000000000000000000db070000` | `15460c84e7810000` | 20147 | `Unit_VTT_323_NK` | `2_of_2_exact_guid_and_token` |

Both the GUID and the token are unique among the 2,227 indexed unit types,
the descriptor entry has exactly one candidate, and the candidate's GUID and
token both match the captured bytes. This names types for the observed owner
objects; it does not establish player identity, callsigns, deployment ownership
or allocation lifetimes between unsampled observations.

## Frozen observations and unknowns

| Field | Value | Confidence |
|---|---|---|
| Damaged handles | 31, 32, 33, 34, 39, 40 | observed `+0x08` |
| Victim type | `Unit_VTT_323_NK` (20147) | high static 2-of-2 join |
| Reported source owners | 74 and 75, `Unit_Merkava_IIIB_Baz` (19537) | object observed; role inferred |
| Source role (`arg1`) | first impact argument; `+0x28 == arg2` 17/17 | inferred, not statically proven |
| Destruction calls | 3 nested (`0xc9c0ce`, arg 1) + 3 cleanup (`0xb7c408`, arg 6) | observed |
| Kill / score outcome | unknown | no death, removal, score or kill record |
| Player / instance identity | unknown | not captured |
| Position / movement | unsupported | not captured; not inferred |
| Frame / epoch / replay / battle time | unknown | not captured |

`+0x1ec` is exported as `deterministic_time_seconds` with proof level
`engine_named_clock_static_path_and_observed_module_store`: the
`DeterministicCurrentTimeInSeconds` binding at `0x1d9cd68` loads global
`0x201d318` and calls `0xaaedf0`, which converts `[ecx+0xd0]` and multiplies
by `0x3e4ccccd` (0.2f, verified from the executable at `0x195d768`). Values
are 806.400024, 806.600037, 807.400024, 807.600037, 830.799988 and
831.000000 by ordinal group. The enter-side `+0x1ec` is `-1.0` on early
impacts (guarded-store sentinel). Equality with a 0.2 multiple is a
quantization test only; no counter value, epoch or frame mapping is claimed.
The counter change 2195 -> 195 crosses receivers: one sample at `0x3f7f6bc0`,
then 458 samples at `0x3f802ea0`. It is **not** evidence of resetting one clock.
The latter pointer matches all retained direct-global state observations from
the same process creation identity. `clock-receiver-segmentation.json` preserves
the independent check. The exporter records receiver pointers and discontinuities.

The earlier `+0x68` "clock time" reading is rejected: the deterministic path
uses `+0xd0`, and `+0x68` belongs to a different static object (speed
factor).

## Corrections to the prior self-report

* The three AL=1 checks are **not** three kills. They are three observed
  destruction invocations; no kill outcome exists in the trace.
* `arg1` is not the shooter. It is a non-null owner whose `+0x28` equals
  `arg2`; static data flow from a firing unit, weapon or projectile is not
  proven. Kill attribution "75 -> 33/39, 74 -> 31" stays inferred.
* Handle 0's descriptor is partly resolved: the lookup maps handle 0 to
  owner `0x66ed8e50` and descriptor `0x50af1d80`, but descriptor bytes were
  not captured, so its type is unresolved rather than simply "never
  dereferenced".
* `arg2` is the source descriptor on source-bearing impacts and the victim's
  own descriptor on null-source impacts. Victim types are therefore taken
  from the sampled owner lookup, not from `arg2` alone.

## Integration corrections and failed reads

Null `arg1` is an unresolved owner, not evidence that no damage source existed.
Owner+`0x24` is exported as `owner_field_0x24_raw`, not an invented descriptor tag.
Confidence labels distinguish sampled owner lookups, nested destruction operands
and cleanup calls; all lookup references for the nine event-involved histories
are retained rather than silently truncated.

There are 5,049 failed memory reads, distinct from zero callback errors:
5,034 generic registry null returns, 11 null owner arguments, and four old
`owner_destroy_candidate` indirect reads through owner+`0x04`. The latter are
not used for descriptor identity. Failures are missing evidence, never zeros.
The current output and `read-failure-observations.json` retain these limitations.

## Outputs

The original delegate outputs remain unchanged in `run/runtime-aar/`. The reviewed,
integrated exporter generated a separate current bundle from the same pinned inputs:
`aar-20261102T050816Z/existing-evidence-aar-v1/` (outside Git):

| File | SHA-256 |
|---|---|
| `events.json` | `302199fa1f4e37bfca1ced65c8d26b13fbb2f3aa9dc305c4802d1c542cee2447` |
| `units.json` | `01a1ad0bebaf0af958ef7e5eff627f5c7590bfabc20bbacb562edfc0bc7e4c5a` |
| `summary.json` | `c2c1427d5d6c6407517f4aa77488673da59604778b0bcdab3a96bd594ad9a3af` |
| `chronology.md` | `42adc755faa9d1d35e458eeaeeecdd4d5a5784066473b48f9772d0f88b217e2e` |

`events.json` keeps every impact with enter/leave/check/destroy line refs,
field bytes and values, target and reported-source joins, the AL boolean,
per-field confidence and the deterministic time. `units.json` contains nine
unit histories (six damaged, two reported sources, one cleanup-only handle 0)
with lookup refs and destruction observations. `summary.json` adds integrity,
clock, descriptor joins, the reference-registry probe and corrections. These are
event-involved histories, not a complete roster of all 71 sampled lookup handles.

`results-observation.json` separately transcribes the retained calibration screen:
DEFEAT / MINOR DEFEAT, 4 min. 11 sec., Death Row, Destruction. Its SHA-256 is
`045b7cc095f1a26963a10bebe91945eb3d6590a4193550da2dbeeed5129b68e4`.
The displayed Kills/Losses values are 30/0; their numeric units are not established
by the screenshot. No individual kill table is visible. This is a same-session
UI observation, not a replay-open or per-kill binding, and does not corroborate
named killers or turn 30 into a unit count.

## Bounded cross-capture update

The [original kill-table corroboration](2026-11-02-kill-corroboration.md) now
independently checks the repeated 28-event sequence and three visible VTT-323
rows. All 252 selected values match across captures. Same-input execution is
strongly supported but not a logged file-open fact. The agreement is cohort-level;
per-row native handles and killer identities remain unknown, so the existing
structured per-event kill fields are unchanged.

## Code and tests

`instrumentation/aar_events.py` gains an additive runtime profile:
`extract_runtime`, `extract_runtime_file`, `render_runtime_chronology`,
`write_runtime_outputs` and `--profile runtime` / `--runtime` with
`--unit-index`. The legacy path, default pinned trace, output keys and
28-event chronology are unchanged. Runtime selection is explicit; a runtime
trace without `--runtime` still fails the legacy hash check rather than
falling through.

The integration retains the 19 legacy tests and 16 initial runtime tests, then
adds three targeted regressions for unresolved-owner/raw-field claims and exact
capture-source verification. The complete current module has 38 tests.

Actual runs (Python 3.14.10 unless noted):

```sh
TMPDIR="$HOME/.hermes/cache/scratch" \
  python3.14 -B -m unittest discover -s tests -p test_aar_events.py -v
# RED: 38 tests, 1 failure + 2 errors before the integration fixes.
# GREEN: 38 tests, OK after the fixes.
TMPDIR="$HOME/.hermes/cache/scratch" WGRD_UNIT_DATA="$WGRD_UNIT_DATA" \
  python3.14 -B -m unittest discover -s tests -v
# 278 tests, OK, 2 private-corpus skips. Includes the final 38-test AAR module.
uvx --from ruff==0.14.2 ruff check instrumentation/aar_events.py tests/test_aar_events.py
# All checks passed.
```

Executed with terminal Python 3.14.10. Full results are retained in
`runtime-aar-integrated-tests.log`; earlier red/green logs are retained separately.
The two skips require `WGRD_CORPUS_DIR`. The real CLI generated all four outputs;
an independent check matched all 28 original event payloads, source-line pairs,
nine unit histories, three capture-source/config hashes and unknown kill outcomes.
`validation.json` records the command and output hashes. The documented runtime
CLI also ran from a clean staged-source export and reproduced all four core output
files byte-for-byte; `clean-export-reproduction.json` retains the receipt.
No new live capture or VM resume was performed; `prlctl` confirmed the VM remains suspended.

Verification-hook limitation, recorded once: Hermes detects no recipe for this
repository and does not recognize the versioned Python command. The maintained
suite above is the actual repository gate; no passing check is repeated merely
to silence that bookkeeping defect.
