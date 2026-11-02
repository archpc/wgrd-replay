# Revision 131544: guarded input and read-only state observations

Status: verified input/counter/completion milestone, not a complete replay automation cycle.

Target: original PE32 engine revision 131544, SHA-256
`5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
Preferred image base `0x400000`; VAs below are build-specific.

## Guarded Win32 actions

The existing [WgrdUi.cs](tools/WgrdUi.cs) now also exposes:

- `WindowState(expectedPid)`: checks a unique game process, HWND ownership, and client dimensions.
- `ClickClient(expectedPid, x, y, expectedWidth, expectedHeight, timeoutMs)`: checks
  coordinates, PID/HWND, client geometry and foreground, transforms client to screen
  coordinates, then issues mouse down/up through `SendInput`.
- `Key(expectedPid, virtualKey, timeoutMs)`: guarded key down/up through `SendInput`.

Foreground acquisition polls a concrete condition with a bounded timeout. No screenshot
or loading sleep is part of either new input method. Existing capture APIs remain
unchanged for calibration and diagnostics. Windows focus and geometry can still race
between checks and input. A successful `SendInput` is an attempted action, not proof
of an engine transition.

Guest PowerShell `Add-Type` compiled the maintained helper successfully. A negative
client coordinate was rejected. `ClickClient` then successfully issued the calibrated
pause/resume and speed-increase clicks on a 3008x1482 client, followed by engine reads.
The new `Key` path compiled but has not yet been exercised in-game.

Source-contract tests are separate from that guest compilation/runtime evidence.
The source of the guest-tested helper has SHA-256
`624cdc82f30ff84e0bffccadb8d4914b61820e40bf4b7f48a2c0ca2e5ea91619`.

## Read-only observer

[`state_observe.py`](../../instrumentation/state_observe.py) attaches a bounded Frida
script which only reads memory. It does not invoke game functions, install interceptors,
write target data, or infer UI state from elapsed time. The controller checks process
identity and the executable digest/revision, validates the selected loaded PE32 module,
checks the scale constant, bounds each read to one readable mapping, and detaches.
Outputs are exclusive-create JSONL with raw counter/prefix bytes, monotonic read bounds,
summary, and cleanup termination. Polling is explicitly bounded to 30 seconds.

The computation and timestamp store are documented in
[the clock finding](2026-11-02-aar-clock.md). RTTI now independently identifies the
container vtable `0x199acc0` as `.?AVTGameplayServices@IA@Eugen@@`:
COL `0x1b91f20`, type descriptor `0x1ea22c0`.

The pointer slot is `0x201d318`; the observed integer counter is container+`0xd0`.
The observer preserves unknown clock origin and does not set `simulation_time_validated`.

## Independent completion evidence

Completion is not inferred from a stationary counter.

The original engine's Lua binding table maps:

| Engine name | Binding table | Getter | Field |
|---|---|---|---|
| `GameStarted` | `0x1d97b38` | `0xa313b0` | GameplayServices+`0x20` |
| `EndGameAsked` | `0x1d97b78` | `0xa30fc0` | GameplayServices+`0x21` |
| `GameEnded` | `0x1d97b58` | `0xa31360` | GameplayServices+`0x22` |

`GameEnded`'s getter loads the global pointer at `0xa31383`, reads +`0x22`
at `0xa31388`, then returns that byte to Lua. `SetGameEnded` is bound at
`0x1d97b48` to `0xa327f0`; it calls `0xab4600`, which writes one to +`0x22`
and tail-jumps to the state publication path `0xab4800`.
The constructor initializes +`0x22` to zero at `0xaab470`.

These names are binary string/table evidence, not invented decompiler labels.
`GameStarted` is not renamed battle-start: the observed replay was still in deployment
when this flag was already true. The summary reports the named engine flags separately
from counter motion and leaves `ui_state` unknown.

## Runtime validation

Private raw files and the derived validation ledger are retained under
`$WGRD_ARTIFACTS_DIR/aar-20261102T050816Z/`; replay bytes and traces stay outside Git.
These recordings ran against authenticated replay SHA-256
`abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121`.

| Observation file | Raw counter | Counter/wall-second | GameStarted / EndGameAsked / GameEnded |
|---|---|---:|---|
| `wgrd-aar-state-paused-01.jsonl` | 2206 to 2206 | 0 over 2.993614375 s | 1 / 0 / 0 |
| `wgrd-aar-state-resumed-01.jsonl` | 2227 to 2267 | 10.008556587760044 | 1 / 0 / 0 |
| `wgrd-aar-state-faster-01.jsonl` | 2420 to 2540 | 15.009678584097424 | 1 / 0 / 0 |
| `wgrd-aar-state-end-candidate-01.jsonl` | 4165 to 4165 | 0 over 2.994888209 s | 1 / 1 / 1 |

The first three observations followed guarded pause, resume and speed-increase inputs.
The final observation was independently associated with the completed results state.
The engine flag distinguishes the final stationary observation from the earlier pause.
The flag does not by itself authenticate which replay completed.

The speed change increased the observed raw-counter rate from about 10 to about 15 per
wall-second. This is not assumed to be a doubling. Pause stopped the counter and resume
restarted it in this run. These are bounded observations, not a universal clock accuracy bound.

SHA-256 references:

- paused: `bc971f1565a46b2e86c90e6d7e8a7fd621d25cae736dbf3f35a548deaa1750e3`
- resumed: `6806edd559f33b78e55320047302c9204c7f3c9384ee7dd86bd19c6d3a323e6d`
- faster: `e728fda99d0ee0ed8881169c8c9065bca9bbee4aa35b12c5230c84c40fd6b7e1`
- ended: `e719025ba20fbd32443cfb0f6176e3e818cdba123098984f4175654581e797de`

The expanded eight-hook capture completed with guest/host SHA-256
`607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74`.
It contains 28 impact calls, 28 threshold checks and six owner/lifecycle calls;
all recorded enter/leave pairs matched, zero events were suppressed, and zero callback,
stack, stale-frame or cleanup errors were reported. Lifecycle calls are not counted as
kills: damage-triggered paths and match-end cleanup must be separated.

The updated observer was also executed in the guest against the completed state:
`engine_game_started=true`, `engine_end_game_asked=true`, `engine_game_ended=true`,
exit 0, zero cleanup errors. Raw file `wgrd-aar-state-ended-verified-01.jsonl`, SHA-256
`5b25af55f5af87164210b39f5baf849869a2e604264ddbf780568b0715fd0d9a`.
The `evidence-export-verified-01.json` manifest checks 21 new screenshots/traces/state
files against guest-generated hashes and preserves identical Mac copies. No additional
snapshot restore was performed.

## Remaining gates

- Distinguish main menu, replay browser and loading through independent engine state.
- Observe replay identity/loading failure rather than relying only on selected UI/file hashes.
- Capture a complete select/load/play/pause/resume/speed/finish cycle with state gates.
- Validate counter origin/frame mapping: final counter 4165 versus replay last frame 4173
  suggests an offset, but an endpoint fit does not establish that mapping.
- Resolve live owners against native descriptors and independently corroborate causal kills.

The working counter/flag observations are reusable steps, not completion of those gates.
