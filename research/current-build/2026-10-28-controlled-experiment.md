# The Oshkosh Incident: current-build controlled replay experiment, 2026-10-28

**2026-10-28 Phase 2 maintenance note:** The helper used in this experiment is preserved byte-for-byte as [WgrdUi-v2.cs](history/WgrdUi-v2.cs). The evidence ledger's historical `WgrdUi.cs` filename and hash identify that version. The [current helper](tools/WgrdUi.cs) adds input-only and capture-only entry points; those changes have not been exercised in the VM. See the [Phase 2 handoff](PHASE-2-HANDOFF.md).

## 1. Executive summary

This session crossed the project's previous boundary between static analysis of historical executable build 59638 and observation of a running, current Windows release. A short, network-isolated skirmish was recorded with internal game revision **131544**, copied without changing the original, parsed by the existing decoder, and played back in the same game installation through the post-match results screen.

The principal results are:

- Steam app 251060 was installed at **Steam build ID 15652829**. The launched root executable identifies internal revision **131544**; the UI displayed **v.24.09.10.131544**. These are separate identifiers.
- The apparent black-screen failure was not a total game-rendering failure. Parallels MCP framebuffer captures were black while a foreground-verified, Windows-native GDI capture showed the rendered game. A small C# helper enabled capture and coordinate-based interaction without modifying game assets or graphics settings.
- The controlled replay has a valid ESAV container and SHA-224, **1,784 frames and 12 commands**. All command boundaries fit the existing decoder. Timeline export retained all 12 events without unresolved spans or errors.
- In the live recording, the selected Oshkosh's **Fuel** supply control was visibly changed from ON to OFF and then back to ON. The replay contains exactly two 0x18 commands, with the same registry key, raw channel value 2, and final-byte values 0 then 1. This is sample-specific UI/command corroboration, not a general proof of every 0x18 field or of actual fuel delivery.
- Playback showed a separate replay clock, including pre-battle deployment, and reached the same Death Row results: **2 min. 24 sec.** The replay UI displayed a total of **5 min. 55 sec.** Total replay frames must not be divided by battle duration as though both start at the same instant.
- Two independently sourced historical archive recordings were acquired and hash-verified. Their embedded versions are **510061340** and **510064564**, not 131544. Both parse and export timelines with no unresolved spans. They improve historical cross-build coverage, not current-build coverage.
- A small, read-only corpus CLI, provenance manifests, and regression tests were added. The seven existing parser/interpretation modules were preserved byte-for-byte against starting commit `a2728fc82d1b5a17e037a57d7af4ba57c8e3206e`.

**No decoder layout change was justified by the observed samples.** No new opcode, first incompatible block, or changed serializer layout was demonstrated. This is positive evidence for these files, not blanket compatibility with all revision-131544 replays. General decoder interpretations remain inferred for non-59638 versions, and execution outcomes remain unknown.

### Evidence and confidence convention

- **Observed:** recorded file bytes, hashes, process paths, tool output, or visible UI state.
- **Corroborated for this recording:** a controlled action plus matching replay evidence, with stated attribution limits.
- **Inferred:** a historical layout or meaning carried across versions without a current executable consumer trace.
- **Unresolved:** not established by the experiment.

The machine-readable evidence ledger is [2026-10-28-evidence.json](2026-10-28-evidence.json). It records screenshot hashes, acquisition mtimes, all 12 command locations, and helper-version identities. Replay provenance and structural expectations are in [cross-build-manifest.json](../../samples/cross-build-manifest.json). The [visual archive page](README.md) presents seven original PNGs and twelve lightweight thumbnails in Git. All 43 original captures are preserved separately in a versioned release archive with checksums; see [the archive manifest](screenshot-archive-manifest.json). Raw replays, downloaded executables, and private transcripts remain outside Git.

## 2. Environment and executable identification

### Host and guest

| Component | Measured value | Evidence route |
|---|---|---|
| Host | MacBook Pro, Mac17,9; Apple M5 Pro; 48 GB memory | Filtered `system_profiler SPHardwareDataType -json` |
| Host CPU configuration | 15 cores; profiler reports `proc 15:5:10:0` | Same profiler output; no serial number published |
| Host OS | macOS 27.2, build 26B123; arm64 | `sw_vers`, `uname -m` |
| Parallels Desktop CLI | 27.0.3 (58680) | `prlctl --version` |
| Guest | Microsoft Windows 11 Pro, ARM 64-bit Processor; version 10.0.26300 | Win32_OperatingSystem CIM query |
| Guest servicing fields | DisplayVersion 26H2, CurrentBuild 26300, UBR 9711 | Windows CurrentVersion registry |
| Guest resources | 4 vCPUs; configured memory 12288 MB; virtual disk configured size 262144 MB | Parallels VM inventory |
| Guest tools | Parallels Tools 27.0.3-58680, installed | Parallels VM inventory |
| Display | 3024 × 1648 physical capture; Parallels capture downscaled to 1568 × 855 | MCP capture metadata and GDI helper return |
| Sharing | Shared Profile on; general host shared folders off; Documents/Desktop/Downloads mapped to host; shared cloud drive present | VM inventory and Windows shell-folder queries |
| Network | Bridged adapter; disconnected explicitly for the experiment, restored afterward | Device-set readback and Get-NetAdapter |

The Windows registry's ProductName string still read "Windows 10 Pro", while CIM identified Windows 11 Pro. The report uses the CIM identity and retains the registry discrepancy rather than treating that stale string as a second operating system.

WGRD is an **x86 PE32** program on an ARM64 Windows guest. Native host architecture, guest architecture, and game architecture are not interchangeable. Windows emulation and the virtual graphics stack are relevant constraints, but this experiment did not isolate an emulator defect or graphics-driver defect.

### Three different build identifiers

| Identifier | Value | Meaning |
|---|---|---|
| Steam application ID | 251060 | Product identity |
| Steam build ID | 15652829 | Installed Steam content build |
| Internal game revision | 131544 | Revision embedded in launched executable and new replay |
| Game-reported UI version | v.24.09.10.131544 | Displayed release/revision string |
| Historical analysis reference | 59638 | Older executable retained for prior reverse engineering |

Steam was found under the standard Windows installation directory. Its library configuration identified the game installation at:

```text
C:\Program Files (x86)\Steam\steamapps\common\Wargame Red Dragon
```

The process actually launched by Steam used:

```text
C:\Program Files (x86)\Steam\steamapps\common\Wargame Red Dragon\wargame3.exe
SHA-256: 5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d
Size: 30,032,896 bytes
```

It did **not** run the retained executable under `Data\PC\59638`. That older executable still hashes to `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46` and remains the basis of the historical layout analysis.

The root executable's embedded string, at file offset **0x151ea00**, is:

```text
####SVNREVISION####0000131544####SVNREVISION####
```

Windows FileVersionInfo initially returned null FileVersion and ProductVersion strings. Targeted REA PE-resource inspection located the version resource at file offset **30031824**, length **624**, SHA-256 `0c364371d1cb4156c54fc451bd0c2088ce3425f5f3799cbe68eb487740b86802`. Reading its fixed version fields yielded **1.0.0.1** for both file and product version. That generic resource version is not the game revision.

REA evidence: `ev_5ccbb4fde44b7ed628a26ef4ec074f5887c1da7f8f4230ce956b7de09b235c3f`. The native binary was not executed on the Mac.

### Update check and its limit

The Steam app manifest reported StateFlags 4, installed build 15652829, TargetBuildID 15652829, and no scheduled update. The fetched app-info service's public branch also reported 15652829. Launching through Steam succeeded without an update workflow.

The public-branch corroboration came from [api.steamcmd.net](https://api.steamcmd.net/v1/info/251060), a third-party Steam metadata service, not a direct authenticated Steam backend query. Therefore the precise claim is **installed build equals the public build returned by the retrieved metadata**, not a timeless guarantee that no newer release can exist. No beta branch was selected and no game content was modified.

### Tools actually used or installed

| Tool | Verified identity/use | What was not done |
|---|---|---|
| Hermes | CLI v0.22.5, local revision bf0203a794a0; CLI reports Python 3.14.9 | No model/configuration rebalance |
| Repository Python | Python 3.9.6 for the executed test commands | No dependency installation; decoder remains stdlib-only |
| Parallels MCP | VM discovery, start, exec, captures/OCR, key input, network hot-disconnect/reconnect | No VM reset, disk modification, or guest security change |
| REA | Live server rea-agents 6.8.0; PE resource provider version 1 | No new Ghidra import or repeated 59638 function analysis |
| Windows PowerShell | CIM, process/registry/hash queries; Add-Type and GDI capture | No execution-policy change |
| Process Monitor | ARM64 4.12; valid Microsoft signature | Installed, not used to capture a trace |
| Process Explorer | ARM64 17.2; valid Microsoft signature | Installed, not used to diagnose a live stack |
| WinDbg | ARM64 package 1.2610.1001.0; x86 CDB present with valid signature | No debugger attach or debugger-derived claim |
| Computer-use backend | Attempted, unavailable due to daemon/SDK mismatch | Not repaired as an adjacent infrastructure task |

Sysinternals came from the official ProcessMonitor.zip and ProcessExplorer.zip downloads. Their ARM64 executable PE machine value was AA64. WinDbg was installed with Add-AppxPackage using Microsoft's appinstaller returned by its official download link. Microsoft documents x86 WinDbg for x86 user-mode programs running on ARM64; ARM64 debugger context switching is also documented. A combined CDB version probe failed at the Parallels transport layer; a narrower signature query succeeded. Installation and signature verification do not constitute debugger execution validation.

Tool hashes:

```text
ProcessMonitor.zip  477754bf299c9e5b311c5666f7a4a48dfdb21265eaa8f0cca70ef9d9552e3a10
Procmon64a.exe     b1c6beaec539f0ffdf714746c161bf9d78f44cb3715d634f36cdb2683f4d6f5b
ProcessExplorer.zip dab147316264b89ae46ae2ad7d8a94116848ef0b703bcac8de9ff22689ce9d51
procexp64a.exe     48db5c371054e53eaefc97eed1e8e6debb57652b2ffbac233d1bb5791cb6da26
```

## 3. Computer-use investigation and WgrdUi.cs

### The black capture was not proof of a black game

The first Parallels MCP capture was a uniform black image. OCR found no text. A later capture of the **Windows guest desktop** worked, establishing that the MCP route was not universally unable to capture the VM. It was not a successful Mac computer-use capture: that separate backend failed.

Guest process inspection showed WGRD, Explorer, and the diagnostic PowerShell in Windows session 1. WGRD reported a DirectX 9 window and was responsive to window messages. This ruled out a simple assumption that the game had been launched solely into an inaccessible session-0 desktop, but did not alone establish rendering.

Several bounded activation attempts failed or proved insufficient:

1. A Shift tap did not expose game content in MCP capture.
2. WScript AppActivate returned false.
3. UI Automation reported a minimized game window. Restore was attempted, but SetFocus raised **Target element cannot receive focus**.
4. Alt-Tab and Alt-Enter did not make MCP game captures usable.
5. Normal CloseMainWindow destroyed the first window, but the process remained CPU-active. Only the experiment-owned process was then stopped; the VM and Steam were not killed.
6. A fresh launch through the Windows Run dialog and the Steam game URI still produced a black MCP framebuffer.

The separate computer-use tool returned a backend setup failure. Its diagnostic command reported:

```text
incompatible daemon: contract version 0.8.0 does not match SDK 0.7.0
```

That backend was left unchanged. Repairing it was no longer required once an alternate capture route worked.

### Successful differential observation

A Windows-native GDI CopyFromScreen capture after **ShowWindow, SetForegroundWindow, and a GetForegroundWindow equality check** showed the rendered WGRD menu. The returned game and foreground HWNDs matched. A Parallels capture near that observation still returned black.

This is the decisive distinction: **rendered game content was accessible through guest GDI while the tested Parallels framebuffer route did not expose it**. The experiment did not establish the internal reason for the Parallels discrepancy. Exclusive-surface handling, focus behavior, display presentation, and capture implementation remain mechanisms to investigate only if needed. It would be incorrect to diagnose a DirectX failure, a hung renderer, or unsupported ARM emulation from the earlier black PNG alone.

The user independently changed window mode to W. Full Screen. Readback showed WindowFormStyle 2; GraphicAPI remained 0, corresponding to the already-used DirectX 9 mode. The agent did not change graphics settings. MCP capture was still black after this change, so no claim is made that windowed fullscreen fixed capture.

### DPI and coordinates

The first guest capture used non-DPI-aware Screen.Bounds and produced a **1512 × 824** bitmap representing a cropped part of the **3024 × 1648** native display. This was not a correct full-screen downscale. The corrected route called SetProcessDPIAware before choosing dimensions. The final helper reads physical dimensions through GetSystemMetrics.

Coordinates supplied to the helper are **physical guest-screen pixels**, with origin at the primary display's top-left. They are not Mac window coordinates and not the downscaled MCP coordinates. When visual analysis used a crop, its origin had to be added; when it used a half-resolution view, coordinates had to be scaled. Arithmetic was checked separately. Some visual-model replies mislabeled the game, mistook static spawn arrows for movement orders, or called scaled coordinates "original". Those descriptions were not adopted as semantic evidence. Cropped UI text and independent process/file evidence were used for consequential claims.

### Development history preserved

| Version/attempt | Preserved result |
|---|---|
| Encoded inline GDI probes | Established foreground-verified rendering, then corrected DPI geometry |
| capture-active-game.ps1 | Execution denied because scripts were disabled; policy was not changed |
| guest_ui.py using direct host prlctl | Returned an unable-to-open-guest-session error; not the working route |
| [WgrdUi-v1.cs](history/WgrdUi-v1.cs) | Exact initial left-click/capture helper recovered from the session's original write, message 31140 |
| [WgrdUi-v2.cs](history/WgrdUi-v2.cs) | Original `WgrdUi.cs` from this experiment: added CaptureRight and a shared CaptureAction implementation; compiled and exercised during the controlled right-click order |

Initial helper SHA-256: `64e36d7eadf7d7ded45421028e6ead70ff22de7a012106cdd098b2d866465ea7`.
Experiment helper SHA-256: `27d754195dc6f7ad701ede32b240e91f8e4fa35a5ff3768b71f5034c58f124df`.

The failed PowerShell-file and direct-prlctl probes remain in the private artifact directory. They contain machine-specific paths and are not presented as portable working recipes. The two C# versions are committed, without personal paths or VM identifiers. Loading the authored C# with Add-Type worked; no ExecutionPolicy bypass was used.

### Capabilities and safety boundaries

The helper restores and foregrounds the sole WarGame3 process, optionally left- or right-clicks, then saves a PNG. With both coordinates negative it performs no click, but **it still changes foreground/window state**. It is not a wholly read-only tool.

It refuses an existing output filename, requires exactly one matching process, rejects a zero main-window handle, and checks that the foreground handle matches the game before input. It returns process ID, game HWND, foreground HWND at completion, and image dimensions. The recording's right-click operation was actually executed through the final version, not merely compiled in theory.

Limits:

- Fixed waits of 600 ms and 1500 ms are not render-completion guarantees. Loading transitions required later captures.
- It does not identify controls, enforce semantic button identity, or validate input coordinates against window bounds.
- There is a focus race after the pre-input check. Completion foreground is reported, not enforced by a second guard.
- It captures the primary screen; multiple monitors and non-primary game placement were not tested.
- It uses legacy mouse_event and SetCursorPos. It moves the **guest** cursor and can interfere with a human controlling that guest.
- Add-Type compiles diagnostic code and may create temporary artifacts. This is not a zero-write probe.
- It reads no game memory, injects no DLL into WGRD, and changes no game assets or settings.
- Screenshots can contain account names or chat. The owner subsequently authorized publication of the screenshot record. A curated set is committed; the complete archive includes three incidental desktop diagnostics. No credentials or private session transcript are included. Future users must perform their own privacy review before publication.

### Reproduction from a Mac using Parallels MCP

1. Discover the VM ID and state with the configured Parallels MCP. Start only the intended guest. Discover actual shared-profile mappings; do not assume that a host path is guest-accessible.
2. Stage the committed helper into a verified shared directory. Use the actual shared path as a parameter, not a hardcoded account path.
3. Launch WGRD normally through Steam. Do not use unknown binaries, authentication workarounds, or an online match.
4. Run the following **inside the guest through parallels_vm_exec**, using its current-user context. Substitute paths before sending the command. Use a fresh output name each time.

```powershell
# These variables are examples to be filled from the inspected environment.
$source = '<GUEST_SHARED_DIRECTORY>\WgrdUi.cs'
$output = '<GUEST_SHARED_DIRECTORY>\capture-unique.png'
Add-Type -Path $source -ReferencedAssemblies System.Drawing
[WgrdUi]::Capture($output, -1, -1)
```

5. Copy/read the PNG through the shared mapping. Inspect it before any input. For an observed target, use the same loading command followed by one of:

```powershell
[WgrdUi]::Capture('<NEW_OUTPUT_PNG>', <PHYSICAL_X>, <PHYSICAL_Y>)
[WgrdUi]::CaptureRight('<NEW_OUTPUT_PNG>', <PHYSICAL_X>, <PHYSICAL_Y>)
```

6. Inspect the returned image and foreground handle. A successfully delivered click is not proof that the intended control changed.
7. Do not bypass execution-policy or permission prompts if a different installation rejects this route. Some long or quoted MCP exec commands returned **PrlJob_GetRetCode: Invalid argument** here; shorter commands or correctly encoded inline commands worked. A transport failure was not counted as a game-state change.

The final working invocation used PowerShell with NoProfile and WindowStyle Hidden through MCP, not the failed direct host Python/prlctl wrapper. No new framework or persistent service was installed for this helper.

## 4. Chronological experiment log

Times below are UTC. Original screenshot mtimes and command-message timestamps are preserved in the evidence ledger/private session record. They bound observations; they are not precise original input-event timestamps. Local Windows filenames use the guest's local clock.

| Time/phase | Action and observation | Evidence |
|---|---|---|
| 05:23 | VM initially stopped; started through Parallels MCP. First exec was too early and failed opening a guest session; subsequent exec worked. | VM list/start/exec receipts |
| 05:23–05:25 | Steam, manifests, candidate executables, known replay locations, shared-profile and cloud mappings inspected. | Manifest/process/hash output |
| Initial search | Checked Saved Games, Eugen application-data candidates, Steam userdata/cloud cache, game directory, local/shared Documents and Downloads, Public profile and relevant cloud gaming storage. No original personal corpus found in those bounded checks. | Discovery receipts; no speculative full-disk crawl |
| User correction | User confirmed the personal recordings were gone; broad search stopped. Earlier claims about missing files were not generalized into a permanent acquisition blocker. | User steering in private session record |
| 05:24 onward | Steam launched the root x86 executable; repeated MCP captures black. Windows desktop capture worked. | Process path and capture hashes |
| 05:32 | Clean UI launch through Steam URI reproduced black MCP capture. | parallels-ui-launch-black.png |
| 05:35–05:38 | Foreground-verified GDI exposed the menu; DPI-corrected capture exposed full settings screen and UI version. | wgrd-active-game.png, wgrd-full-menu.png |
| 05:38–05:40 | User's W. Full Screen setting read back; C# helper established menu interaction. | Option.ini readback; helper v1 |
| 05:40:48 | After explicit approval, VM adapter hot-disconnected. Guest Get-NetAdapter reported Disconnected. | Network action/readback |
| 05:41 onward | Solo → Skirmish. Death Row, 1v1, Destruction, 1500 initial points, no time limit, medium income; one player versus Medium AI. Existing decks retained. | wgrd-skirmish.png |
| Deployment | Match loaded into deployment. Two early production commands later found at frame 1; no claim that these were manually purchased in this session. | wgrd-deployment.png; command ledger |
| Purchase UI | HQ was initially mistaken for purchase navigation; it opened the pause/menu screen. Continue returned to deployment. Clicking the points counter opened the deployment menu. | wgrd-hq.png, wgrd-purchase.png |
| By 05:45:17 | Selected Oshkosh; tooltip showed Supply 2400 L. This selection observation precedes the placement window below. | wgrd-truck-select.png |
| 05:45:49–05:45:52 | Clicked ground inside Charlie. Solid OSHKOSH label appeared. | wgrd-truck-placed.png |
| 05:46:24–05:46:27 | Clicked Launch Battle. Subsequent image showed battle timer 00:00:01. | wgrd-battle-start.png |
| 05:47:20–05:47:25 | Selected the truck and right-clicked another ground point. A single 0x07 appears in the resulting replay. Arrival was not demonstrated. | wgrd-truck-selected-live.png, wgrd-move-issued.png |
| 05:48:19–05:48:22 | Clicked Fuel ON. Screenshot explicitly showed Fuel OFF, with Ammunition and Spare Parts still ON. | wgrd-fuel-off.png |
| 05:48:46–05:48:49 | Clicked Fuel OFF. Screenshot explicitly showed Fuel ON again. | wgrd-fuel-on.png |
| 05:48:49–05:49:18 | Opened menu, selected Surrender, confirmed. An immediate screenshot still showed the battlefield; later capture and file listing established completion. | wgrd-surrender-prompt.png, wgrd-postmatch.png |
| 05:49:58 | Results showed Defeat, Death Row, Destruction, 2 min. 24 sec.; no kills/losses displayed. | wgrd-postmatch.png |
| 05:50 | New replay copied to shared staging and host artifact storage; guest source and copies had identical SHA-256. Decoder/timeline succeeded immediately. | Hash receipts; current inventory |
| 05:55:40 | Profile → Replay browser contained the newly recorded file. Selected row and Play. | wgrd-replay-browser.png, playback-launch capture |
| 05:56:15 | Playback transport visible; replay 00:00:28 / 00:05:55, battle clock 00:00:00. | wgrd-playback-loaded.png |
| Later playback | Replay 00:01:17 and 00:02:26 still had battle clock zero. | Playback progress/later captures |
| 06:00:16 | Replay 00:04:29, battle 00:00:58; Oshkosh selected, Fuel ON. | wgrd-playback-observation-final.png |
| 06:01:21 | Replay 00:05:34 / 00:05:55; supply panel not visible. This image did not independently confirm the replayed OFF transition. | wgrd-playback-fuel-window.png |
| Playback completion | Results again showed Defeat, Death Row, 2 min. 24 sec. | wgrd-playback-exit-menu.png, full results crop |
| Cleanup | Original replay hash rechecked unchanged. Normal game-window close left a windowless process; only the experiment-owned process was stopped. Adapter reconnected; guest reported Up and no WGRD process. VM remains running. | Close/integrity and restore receipts |

The saved profile automatically joined online chat before isolation was established. No multiplayer match was initiated. Once discovered, this was reported; explicit adapter-disconnect approval was obtained before the controlled match. Persistent old chat text remained visible after disconnection; it was not taken as evidence of live network connectivity. The new replay metadata independently reports IsNetworkMode 0.

## 5. Replay provenance and corpus census

### Controlled recording

The original guest file remains under the user's Saved Games EugenSystems/WarGame3 directory, named:

```text
replay_2026-10-28_01-49-18.wargamerpl2
148,119 bytes
SHA-256 1b060d2ab2e5501c6c8731fcb87ac0c7ac6dc4598387dcdb261ab8bb06bc8d70
```

Its exact absolute guest source path is retained in the private provenance record. Public instructions use the user-profile convention rather than publishing an account-specific path. The host copy resides beneath `$WGRD_ARTIFACTS_DIR/current-build-20261028/raw/`. The original was not renamed, moved, overwritten, or deleted. Source/copy hashes were compared after acquisition and the original was rehashed after playback.

### Historical archive acquisition

Source: [Wargame replay uploader](https://ux.getuploader.com/wargame_ee/index), whose links resolve to the uu.getuploader.com host. The site explicitly announced shutdown and deletion on 2026-11-25 and requested restrained automated access.

The user's separate Cloud acquisition jobs could not be inspected: local cron list was empty, no Cloud peer/access route was configured, and the Portal browser was at sign-in without saved credentials. No claim was made that remote jobs did not exist. After the user explicitly authorized a small redownload, a Haiku worker acquired only IDs **219** and **218**. It used sequential requests with at least six-second gaps and encountered no password or CAPTCHA. No protection was bypassed.

The worker reported that ID 219 was fetched twice because the first script attempt did not persist its bytes. This duplicate fetch is recorded, not hidden. The bounded acquisition is not a mirror of the archive, not proof of its full count/size, and not verification of Cloud-job completion. Both saved files were independently rehashed by the lead and their MD5 values matched the site's listed checksums.

| ID | File | Posted timestamp, timezone unknown | Bytes | SHA-256 |
|---|---|---|---:|---|
| [218](https://uu.getuploader.com/wargame_ee/download/218) | komachi.wargamerpl2 | 2017/01/14 18:50:58 | 1,358,077 | 93953b293e65a69434b2a70d4edbd6e1ca7daf6f0683c196542411615ccdd2fd |
| [219](https://uu.getuploader.com/wargame_ee/download/219) | replay_2017-10-14_23-19-39.wargamerpl2 | 2017/10/15 10:43:11 | 10,642,223 | 7406065c11258bcc0e82663d229e4d4529c6da13e91ee5511673a580af389583 |

Private acquisition manifests retain actual tokenized download URLs, retrieval UTC times, landing pages, fetch logs, hashes, and decoder output. Public manifests retain durable landing URLs and checksums rather than presenting ephemeral token URLs as permanent acquisition endpoints. Archive dates and replay version fields are distinct measurements.

### Measured structural results

| Sample | Replay Version | Map identifier | Frames | Slots/frame | Commands | Complete/framed blocks |
|---|---|---|---:|---:|---:|---|
| Controlled | 131544 | Destruction_2x3_Montagne_1 | 1,784 | 1 | 12 | 7 / 2 |
| Archive 218 | 510061340 | Conquete_2x3_Gangjin | 9,727 | 2 | 2,711 | 2,389 / 110 |
| Archive 219 | 510064564 | Destruction_5x3_Asgard_10v10 | 14,207 | 20 | 12,126 | 10,492 / 1,092 |

These three new files total **12,148,419 bytes and 14,849 commands**. All three have valid digests, zero unknown chunks, zero failed command blocks, and zero unresolved timeline spans. The original three reference samples remain separate and passed their existing regressions.

The metadata game-mode values are raw: 0 for the controlled file, 1 for each historical file. Do not repair or reinterpret the archive-219 mode solely because its map name starts with Destruction. Player metadata is retained in private inventories, but slot-to-identity mapping remains null; the single recorded slot in the AI skirmish is not evidence that both human and AI actions are serialized as two pact slots.

| Opcode | Controlled 131544 | Archive 218 | Archive 219 |
|---|---:|---:|---:|
| 0x02 | 1 | 0 | 2 |
| 0x04 | 2 | 4 | 40 |
| 0x07 | 1 | 2,491 | 10,555 |
| 0x08 | 0 | 11 | 55 |
| 0x09 | 0 | 0 | 3 |
| 0x0A | 0 | 28 | 52 |
| 0x0C | 0 | 19 | 83 |
| 0x0D | 3 | 111 | 1,114 |
| 0x0E | 2 | 4 | 20 |
| 0x13 | 1 | 2 | 4 |
| 0x17 | 0 | 37 | 109 |
| 0x18 | 2 | 4 | 89 |

A framed block is not the same thing as a layout-decoded command. The core parser retains 0x0D bodies as opaque, length-framed content; the timeline's existing production interpreter separately consumes known interiors. Counts of opaque 0x0D commands are 3, 111, and 1,114, respectively. Successful timeline export is not a claim that every field or runtime effect is understood.

## 6. Command-level interpretation and ground truth

### Complete controlled sequence

| Frame | Commands | Observation/limit |
|---:|---|---|
| 0 | two 0x04 | Initial setup; semantic meaning not newly verified |
| 1 | two 0x0D, one 0x0E | Initial production/setup; not two observed manual purchases |
| 7 | one 0x0E | Structural decode only |
| 885 | one 0x0D | Candidate corresponding to the observed Oshkosh placement |
| 1060 | one 0x13 | Near the battle-start phase; **not** proven to be a battle-start opcode |
| 1352 | one 0x07 | Correlates with the controlled selected-truck ground order |
| 1638 | one 0x18 | Correlates with visible Fuel ON → OFF |
| 1771 | one 0x18 | Correlates with visible Fuel OFF → ON |
| 1783 | one 0x02 | Correlates with the surrender action and resulting match end |

### Fuel toggles: what is established

Both 0x18 records contain:

- obj_04_u32 = **3221225609**;
- obj_08_u32 = **2**;
- obj_0c_u8 = **0**, then **1**.

The 0x07 actor reference carries the same registry key. Existing per-replay attribution resolves it uniquely in this file. The live UI observations explicitly show Fuel OFF and then Fuel ON for the selected Oshkosh while Ammunition and Spare Parts remain ON.

This supports the **sample-specific association** of raw channel 2 with the observed Fuel control and values 0/1 with those observed states. It does not establish all channel values, every unit's behavior, actual fuel transfer, ownership outside this scenario, or cross-replay entity identity. The inherited decoder label remains deactivate_supply_request; it is not renamed to a universally verified fuel command.

During playback the truck was selected and Fuel ON was seen at replay 4:29. The later 5:34 capture did not show the supply panel, so a second visual OFF/ON confirmation during playback was **not** obtained. Live recording evidence and playback evidence are deliberately separated.

### Production and movement

The Oshkosh purchase/placement UI and the visible deployed label are observed. The frame-885 production request is consistent with that action and has a known, exactly consumed production layout. The earlier frame-1 records are setup, not evidence of two additional player clicks. Unit type naming from a 59638 NDF index was not promoted to current-build authority.

The 0x07 request at frame 1352 has one actor reference and contextual kind value **39**. The existing decoder correctly keeps its effective order runtime-dependent. A right-click on ground was issued, but the experiment did not establish arrival, a complete trajectory, coordinate axes/units, or a world-to-screen transform. Static spawn arrows labeled Land/Air are not evidence that this particular unit executed a movement order.

No controlled 0x08 marker, 0x0A cancellation, or 0x0C production-change action was recorded. Their occurrences in the historical files are structural evidence only. No current-build consumer trace was needed to fix an actual incompatibility because none was observed.

## 7. Time bases and playback

The match results and playback results both show **2:24**. Replay transport shows **5:55** total, with an extended initial interval during which the battle clock is zero. At replay **4:29**, the battle clock is **0:58**.

These observations demonstrate distinct replay/deployment and battle-time origins. They do not by themselves prove a constant tick rate, the exact mapping of every frame to either clock, or how paused menus/loading affect serialization. No frame-to-seconds conversion was added. The runner keeps duration_seconds null and records TimeLimit only as raw configuration, not elapsed duration.

Playback compatibility was actually exercised: the newly saved recording appeared in Profile → Replay, loaded into replay mode with transport controls, progressed, and reached the same post-match result. This is stronger than merely detecting a saved file or accepting its header. It is still only one current-build recording, not a broad gameplay simulation validation.

## 8. Implementation and regression preservation

Added components:

- [wgrd_corpus.py](../../wgrd_corpus.py): explicit files or recursively discovered replay files; stable absolute provenance paths, size/SHA-256, version census, raw map/mode/player metadata, frame/slot counts, decoded opcode counts, block failures with byte offsets, timeline status, header-only mode, and exact JSON baseline comparison.
- [tests/test_corpus.py](../../tests/test_corpus.py): seven synthetic runner-behavior tests, including unknown tails, malformed blocks, bad digests, empty/missing paths, deduplication, baseline mismatch, and non-finite metadata isolation.
- [tests/test_cross_build_corpus.py](../../tests/test_cross_build_corpus.py): three hash-pinned authentic regressions, including the observed current-file fuel pair. External samples skip explicitly if absent and fail if altered.
- Cross-build sample manifest and this report/evidence ledger.
- The portable C# helper and its exact initial version.

The runner is not a new parser, downloader, database, or simulation layer. It calls the existing decoder and timeline. It reports failed files without scanning undecoded tails for plausible opcode bytes. Header-only mode still reads and hashes whole files but skips the expensive frame/command walk; it reports compatibility as not checked, not compatible.

A Haiku review demonstrated one required defect: non-finite metadata accepted by Python's JSON reader could reach the final strict JSON dump and truncate the entire report. A CLI regression reproduced that failure. The runner now validates metadata for strict JSON before adding it to a row, so NaN, Infinity, negative Infinity, and exponent overflow become per-file header errors. Tests cover full and header-only modes. The core parser was not modified for this adjacent input-policy issue.

No existing output keys or APIs were changed. The seven original Python decoder/interpretation modules were compared byte-for-byte with starting commit a2728fc82d1b5a17e037a57d7af4ba57c8e3206e and were unchanged. All non-59638 interpretation statuses remain inferred or unknown, and execution_outcome remains unknown.

## 9. Reproduction and validation

Set the external artifact root as needed. Raw bytes must be obtained separately; the repository does not redistribute them.

```sh
export WGRD_ARTIFACTS_DIR="$HOME/.hermes/artifacts/wgrd-replay"
python3 -B wgrd_corpus.py \
  "$WGRD_ARTIFACTS_DIR/current-build-20261028/raw" \
  "$WGRD_ARTIFACTS_DIR/historical-getuploader-20261028" > /path/to/private-inventory.json
python3 -B wgrd_corpus.py \
  "$WGRD_ARTIFACTS_DIR/current-build-20261028/raw" \
  "$WGRD_ARTIFACTS_DIR/historical-getuploader-20261028" \
  --expect /path/to/private-inventory.json
python3 -B wgrd_corpus.py /path/to/replays --headers-only
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
python3 -B research/maintenance/preservation_manifest.py verify research/maintenance/preservation-manifest.json
python3 -B research/maintenance/work_artifacts_verify.py
python3 -B research/maintenance/check_links.py
git diff --check
```

Do not redirect a report onto a replay or an existing valuable manifest. The CLI itself writes only stdout; shell redirection is the caller's responsibility. Inventories contain private player metadata and source paths and should not be committed. Exact --expect comparison includes paths, so its baseline is location-specific.

Executed verification:

- Canonical suite: **139 tests, OK, no skips** with all local external artifacts available.
- Focused new authentic suite: **3 tests, OK**.
- Runner behavior suite after the NaN correction: **7 tests, OK**.
- Separate temporary ad-hoc CLI script: inventory, unchanged baseline, mismatch rejection, and strict-JSON per-file isolation in both modes passed. Its first attempt had a harness import-path error, corrected without changing production code. Temporary files were cleaned up. This was not counted as the canonical suite.
- Research preservation: **182 entries, 182 OK, 0 problems**.
- Work-artifact preservation: **450 entries, 0 missing, 0 changed**.
- git diff --check: passed.
- The existing link checker reported **32 pre-existing missing-reference warnings** before this work's documentation changes. The final check reproduced exactly those 32 warnings, with no findings under the new current-build documentation. They include false-positive path-like prose and historical references. They were classified adjacent, not silently repaired.

Existing ResourceWarnings from unclosed files in older tests/research scripts were present in the baseline and final suite. They were not fixed as unrelated cleanup. A passing test count does not erase warnings or convert a skipped external test into a pass.

## 10. Preservation, final state, and remaining limits

Private artifact directories:

```text
$WGRD_ARTIFACTS_DIR/current-build-20261028/
  raw/                         current replay copy
  evidence/                    retained screenshots
  current-corpus.json          private full inventory
  reference-corpus.json        original-sample inventory
  session-evidence-private.json tool inputs/results and visible session text
  WgrdUi-v1.cs, WgrdUi.cs       exact helper source snapshots
$WGRD_ARTIFACTS_DIR/historical-getuploader-20261028/
  replay files, manifest, landing pages, fetch logs, decoder/inventory outputs
```

The private session export excludes hidden reasoning fields but can contain personal paths, account data, and retrieved conversation text. It is not suitable for public redistribution. The public evidence ledger provides checksums and bounded claim anchors, not the private transcript itself. Shared Downloads contained task-created staging copies; authoritative preserved copies are under the artifact root. Original replays and game assets were not altered.

The final publication layout follows the owner's storage preference: seven representative original PNGs (52,471,638 bytes) and twelve JPEG thumbnails (1,427,934 bytes) in Git, plus a separate versioned ZIP containing all 43 originals (312,109,052 uncompressed bytes). The archive was reopened and every image's length and SHA-256 verified. Its ZIP size is 311,677,181 bytes and SHA-256 is `b2f7b5e417fe48786372db1badd054c64c6bf04ae7c6e86203aeb804d42a1da8`. See [the gallery and release link](README.md) and [complete archive manifest](screenshot-archive-manifest.json). No full-collection Git commit was made; only verified, untracked staging copies were removed when curating the repository set. Originals remain intact in the archive and local evidence directory.

Final VM state was verified: WGRD stopped, network adapter Up, VM still running. The user's window-mode setting was retained. Diagnostic tools remain installed. No Procmon capture or debugger attachment was performed after rendered game content became accessible. The unrelated computer-use backend version mismatch remains unresolved.

Remaining limits are specific, not a replacement roadmap: only one current-build skirmish was tested; movement outcomes and coordinates remain unresolved; marker/cancellation/change-production controls were not exercised; all-opcode semantics were not revalidated against the current executable; the Cloud archive-job state remains unknown. A next recording targeting one of those relationships should isolate that action and capture a before/after UI state rather than infer it from opcode presence.

## 11. Model attribution and cost accounting

The lead route was OpenAI GPT-6 Astra Flex through Nous. Bounded delegated tasks ran on Claude Haiku 5.5: runner review, diagnostic-tool documentation research, historical acquisition, computer-use report drafting, and independent corpus analysis. The lead retained VM control, consequential interpretations, file integration, and final verification. Drafts were reviewed rather than copied as authoritative: several inaccurate wording claims were corrected against actual tool output.

Usage is measured from the local session_model_usage ledger, not estimated from prose length. The [usage snapshot](2026-10-28-usage.json) covers the parent and six completed direct children through its recorded cutoff: 298 API calls, 119,545 input tokens, 189,531 output tokens, 38,720,453 cache-read tokens, and 951,267 cache-write tokens. It records an estimated total of **$25.137584275**, comprising **$25.0252565** for the lead model and **$0.112327775** across Haiku delegation and auxiliary rows. Reasoning tokens are reported separately and must not be added to output tokens.

These are **ledger estimates, not Nous Portal-reconciled charges**, and exclude later publication calls/turns. Auxiliary cost rows have incomplete pricing-status metadata; their stored estimates have not been independently repriced. An actual_cost_usd field of zero in an unreconciled row does not mean the work was free. The snapshot distinguishes child task scopes and auxiliary tasks. The main session cannot be precisely apportioned into investigation, implementation, and documentation from its aggregate row; no such split is invented.

**Accounting clarification:** The 298 API calls are model-inference requests recorded in that ledger, not counts of tool calls, guest-control invocations, input actions, screenshots or vision analyses. Separate definitions for future work are in the [Phase 2 handoff](PHASE-2-HANDOFF.md#accounting-vocabulary); the missing historical interaction counts are not reconstructed.

## 12. Sources

- [Steam app metadata service](https://api.steamcmd.net/v1/info/251060), retrieved during the experiment; third-party public-branch corroboration.
- [Microsoft Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon).
- [Microsoft Process Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer).
- [Microsoft WinDbg installation](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/).
- [Microsoft debugging on ARM64](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/debugging-arm64).
- [Archive index and closure notice](https://ux.getuploader.com/wargame_ee/index).
- [Machine-readable evidence](2026-10-28-evidence.json), [sample manifest](../../samples/cross-build-manifest.json), [prior architecture](../../docs/ARCHITECTURE.md), and [research index](../INDEX.md).
