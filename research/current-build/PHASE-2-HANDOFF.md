# Phase 2 handoff: replay timing and movement

**Plan only. This document does not authorize VM access, game launch, network changes, recording, playback, publication, or cleanup. Obtain explicit authorization for each applicable action before proceeding.** The 2026-10-28 maintenance pass did not operate the VM or run an experiment.

## Baseline and evidence

The [Oshkosh report](2026-10-28-controlled-experiment.md), [evidence ledger](2026-10-28-evidence.json), [gallery](README.md), and [cross-build manifest](../../samples/cross-build-manifest.json) are the sources of record. Historical executable build **59638**, controlled internal revision **131544**, and Steam content build **15652829** are distinct. The recorded root executable `wargame3.exe` SHA-256 is `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`; verify the actual launched executable and revision again before a future run.

The authenticated controlled replay is `$WGRD_ARTIFACTS_DIR/current-build-20261028/raw/replay_2026-10-28_01-49-18.wargamerpl2` (`WGRD_ARTIFACTS_DIR` defaults to `~/.hermes/artifacts/wgrd-replay`). SHA-256: `1b060d2ab2e5501c6c8731fcb87ac0c7ac6dc4598387dcdb261ab8bb06bc8d70`. It contains 1,784 frames and 12 commands. The live fuel-control pair is sample-specific corroboration; the contextual 0x07 request does not prove movement or arrival. Playback finished, but did not independently establish the fuel transition or movement. Raw replays and full-size captures remain external; do not publish private metadata, proprietary files or session transcripts.

The [evidence ledger](2026-10-28-evidence.json) records frames 1352, 1638 and 1771 and the screenshot mtimes; the [report](2026-10-28-controlled-experiment.md#6-command-level-interpretation-and-ground-truth) provides the action correlations. The gaps are 286 frames over about 57.148 seconds and 133 frames over about 26.622 seconds. Both suggest roughly **5 frames/second**, but screenshot mtimes are acquisition times, not exact inputs. This is a hypothesis, not a conversion or error bound. Clock origins, serialization latency and simulation-pause behavior remain unresolved. Do not call 0x13 a battle-start opcode or reuse the 59638 unit index as matching 131544 data.

## Clock and pause distinctions

- A live in-game menu opening is an interface event, not proof that simulation paused. Verify game-clock and frame behavior across a bounded interval before classifying a simulation pause.
- A simulation pause concerns advancement of the recorded match. A replay-playback pause concerns the playback transport; test it separately. Neither implies the other.
- Playback speed changes the rate at which playback is observed; it does not establish the relationship of original frames to the simulation clock. Record the actual setting. Other speeds are untested.
- Deployment precedes the displayed battle clock; replay transport time, battle time, host/guest wall-clock timestamps and recorded frame indices are separate measurements. Do not assume equal origins or constant progression. A monotonic stopwatch measures elapsed time in its own process/clock domain; do not subtract guest ticks from host ticks.

## Helper and bounded batching

The [current helper](tools/WgrdUi.cs) uses physical primary-display pixels, restores/foregrounds the unique game process and checks its window before input. It exposes:

- `Click(x,y)` and `ClickRight(x,y)`: input only; return an `_attempted` label, not game acceptance.
- `CaptureOnly(file)`: capture without a click. It still restores and foregrounds the game.
- `Capture(file,x,y)` and `CaptureRight(file,x,y)`: original left/right input followed by capture; either negative coordinate retains the old no-click behavior. Blank or existing output paths are rejected.

The 2026-10-28 experiment exercised [v2](history/WgrdUi-v2.cs); the added entry points and later safety changes have **not** been compiled or exercised in the Windows VM. The ledger's historical `WgrdUi.cs` name and hash refer to v2, not the modified current helper. The helper checks primary-display bounds, cursor placement and foreground before a click; these do not prove the point is inside the game window or eliminate a focus/geometry race. It does not return the window rectangle or DPI state; establish those independently and stop if they cannot be verified. It cannot confirm that the game accepted input. A failed combined input/capture call may already have attempted input. `mouse_event` supplies no acceptance result. Captures use exclusive file creation, but a failed write can leave a partial new file; preserve and identify it, never overwrite it.

Use the documented current-user Parallels guest-exec route and `Add-Type -Path` with `System.Drawing`, not the failed host `prlctl` wrapper. Record process identity, HWND, window rectangle, DPI and primary-display dimensions. Restore can change geometry. Compare foreground and rectangle around consequential calls; abort on mismatch or ambiguous state. The tested Parallels game framebuffer was black while guest GDI worked, so do not rely on a black framebuffer or its image-change signal as proof of game state. Fixed helper waits are not loading or rendering guarantees.

For an authorized action, the caller can bracket the whole helper invocation; this example uses **guest** UTC and stopwatch ticks. Set `$source` to the verified guest-visible helper path and `$x`/`$y` to inspected integer pixels before running. PowerShell can coerce `$null` to integer zero, so never pass unvalidated coordinates to the helper. The host should separately log its own monotonic and UTC start/end around the guest invocation. Record both time domains and do not label either as the exact click or serialization time:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($null -eq $x -or $null -eq $y -or $x -isnot [int] -or $y -isnot [int]) {
    throw 'Set x and y to inspected integer pixels before input'
}
Add-Type -Path $source -ReferencedAssemblies System.Drawing  # once per PowerShell process
$beginUtc = [DateTime]::UtcNow.ToString('o')
$beginTicks = [Diagnostics.Stopwatch]::GetTimestamp()
try {
    Write-Output 'action=left status=calling'
    $result = [WgrdUi]::Click($x, $y)  # x/y: previously inspected physical pixels
    Write-Output "result=$result"
} catch {
    Write-Output ("status=error input_may_have_been_attempted=true error=" + $_.Exception.Message)
    throw
} finally {
    $endTicks = [Diagnostics.Stopwatch]::GetTimestamp()
    $endUtc = [DateTime]::UtcNow.ToString('o')
    Write-Output "begin_utc=$beginUtc end_utc=$endUtc begin_ticks=$beginTicks end_ticks=$endTicks frequency=$([Diagnostics.Stopwatch]::Frequency)"
}
Write-Output 'HERMES_PHASE2_DONE'
```

Check stdout, stderr, exit status and the final marker; some guest PowerShell failures have returned exit 0. A result says only that input was attempted. Log exceptions as potentially attempted and stop; never retry blindly. Batch only actions whose state and coordinates have already been established, in a short sequential guest invocation that stops on any exception or failed check. Put explicit capture/inspection checkpoints at loading transitions, selection, battle start, each meaningful movement state, surrender and playback observations. Fewer invocations reduce overhead but reduce opportunities to inspect intermediate states. Use selected captures or offline crops for vision, not a separate vision call for every screenshot. Each existing capture call still writes a full-resolution PNG.

## Proposed recordings

One lead controls the VM exclusively. Before running, predeclare action labels, clock precision/tolerances, evidence requirements, failure rules and the point at which the evidence would count as inconclusive. Determine the timestamp-bracket precision without using the holdout to choose a favorable threshold.

1. **Timing calibration.** On a short offline skirmish, capture deployment and the battle-start transition. If distinguishable serialized deployment actions are available, make two with deliberate spacing. At normal speed, make at least three uniquely identifiable battle actions at uneven intervals, plus a within-recording check action. Record before/after clock images, input/capture brackets, helper results, process/geometry state, and action order. A fuel toggle is a candidate only when selection and state are visible. Observe a short pause/resume only if actual pause can be established; bracket it with distinguishable actions and clock readings. Otherwise classify pause as untested. Surrender, record the result, preserve and hash the original and its copy.
2. **Independent holdout and movement.** Relaunch the game with authorization, change the action spacing and record a second short skirmish. Select one visually identifiable truck. Keep a stationary camera and visible fixed landmarks. Right-click two separated reachable destinations A then B. For each, capture the selected unit and intended ground location before input, an intermediate position, and at least three stable observations separated by a predeclared interval and tolerance. A starting proposal is five seconds between stable captures and a tolerance no larger than one visible marker radius; approve the actual values before recording. If the ground position, target, selection or camera cannot be distinguished, mark arrival inconclusive. An optional observed fuel-control pair can bridge the unit to a replay-scoped key; require a unique full 20-byte actor reference and matching issuing slot. Preserve source offsets and raw values. Extra commands are acceptable only if attribution stays unique.
3. **Playback and offline analysis.** Inspect playback at 1× around recognizable transitions. Record replay and battle clocks together where possible, then observe the same truck relative to landmarks at A and B. Do not assume a visible frame cursor or equate a matching results screen with movement. Decode each authenticated replay with the existing corpus/timeline tooling. Separate attempted input, recorded request, actor attribution, transmitted target argument, observed displacement, arrival and playback reproduction. Contextual kind 39 remains runtime-dependent.

Fit candidate frame-to-clock relationships using bounded observations, testing deployment/battle offsets and possible changes in rate. Include display rounding, invocation/capture delay, observed transition windows and unknown action-to-serialization latency. Frame-to-time estimates are conditional on the demonstrated event associations; do not promote a fitted value to an authoritative universal rate. Pass a bounded candidate only if uniquely associated anchors span both phases and an independently checked holdout overlaps its prediction within the predeclared tolerance. Validate on the second recording after the fresh launch, with a Haiku analyst independently checking raw anchors and criteria. Shared hardware, game and operator can still produce correlated systematic errors. A sufficiently precise contradiction fails the candidate; insufficient precision or ambiguous attribution is inconclusive. Pause remains a separate untested result unless directly verified.

## Budget, stop conditions and ownership

Planning estimates, not measurements: one VM session, two game launches, two recordings and up to two playback runs; roughly 25–40 inputs, 25–45 captures, 40–100 guest invocations and 8–16 vision analyses. The modified helper has not been VM-tested, and actual counts depend on evidence and recovery. Optimize cost per defensible finding, not minimum clicks. Stop on unexpected UI, unreadable clocks, failed foreground/geometry checks, unapproved network state, changed camera, unidentifiable actor/target, or about two failed attempts at the same control. Do not modify settings, bypass policy, or kill an unrelated process to continue. Restore any separately authorized temporary network change and verify it; do not assume a disconnected adapter from stale chat text.

The lead model (Terra in the planning session, or its successor) owns consequential interpretation, sole VM control, repository integration and verification. Haiku receives bounded read-only offline analysis or independent review; do not give multiple agents guest control. Preserve replay originals, source paths, hashes, UTC/monotonic bounds, raw screenshots, helper version, action log, observed clocks, decoded offsets and uncertainty. Publish only after separate approval and privacy review. Keep large or private artifacts outside Git; place a dated report and a small public evidence ledger in this existing directory, update the appropriate manifest and tests only from authenticated observations, and retain old records unchanged.

## Accounting vocabulary

Measure and report separately:

1. Lead-model inference calls: Terra/Astra API requests.
2. Delegated-model inference calls: Haiku subagent API requests.
3. Auxiliary-model calls: vision, approval or other model-backed requests.
4. Tool invocations: terminal, Python, skill, Parallels MCP or other tool executions.
5. Guest-control invocations: tool operations that actually reach the VM.
6. Physical input actions: injected clicks, keys or other input events.
7. Screenshot captures: images captured, whether or not analyzed by a model.
8. Vision analyses: model-backed image interpretations, distinct from capture.

One inference can initiate multiple tool calls; a guest invocation may perform multiple inputs; a capture need not cause a vision analysis. The previous report's 298 API calls and estimated $25.137584275 are a measured ledger snapshot and unreconciled cost estimate, not a count of guest interactions or clicks. Do not invent unavailable historical counts. Use `session_model_usage` for model calls/tokens and label estimated dollars until reconciled; log guest calls, inputs, captures and vision analyses separately for future runs.

## Verification before publication

Run the complete available suite from the repository root and report skips:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
python3 -B research/maintenance/preservation_manifest.py verify research/maintenance/preservation-manifest.json
python3 -B research/maintenance/work_artifacts_verify.py
python3 -B research/maintenance/check_links.py
git diff --check
```

The link checker historically reported 32 warnings, including path-like prose and external references; compare and classify new findings. Verify original and copied replay hashes before and after playback. Review the full diff, evidence privacy, external artifact paths and actual test/skip results. Commit or publish only if explicitly authorized. The 2026-10-26 preservation manifest allows changes to five named active documents; an OK result is not byte-identity proof for those exceptions. It does not cover later files or unlisted paths such as `AGENTS.md`, `docs/ARCHITECTURE.md`, and `research/INDEX.md`; check those separately with Git.
