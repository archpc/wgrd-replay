# Ground-truth replay acquisition: verified prerequisites and blockers

Session 2026-10-26 (Claude Fable 5.1). Read-only inspection of the Parallels
guest via the Parallels MCP (`parallels_vm_info`, two `parallels_vm_exec`
PowerShell probes). No game launch, no installs, no configuration change.

## Why this matters

Every semantic claim in this repository rests on byte consumption, RTTI class
names, and static-data joins. None has been compared against gameplay that was
actually observed. A replay recorded alongside a written action log is the
cheapest way to test 07/08/0a/0c/0d/18 semantics, frame duration and the
coordinate frame at once.

## Verified facts (guest "Windows 11", UUID b4c9e0a8-67b7-40ff-96a5-8b7bb8a8c236)

| Item | Observed |
|---|---|
| Guest OS | Windows 11 Pro 10.0.26300, ARM64 (x86/x64 run via Windows emulation) |
| VM resources | 4 vCPU, 12 GB RAM, 256 GB disk (199.6 GB free), 3D acceleration "highest", Parallels Tools 27.0.3 installed |
| Steam | installed at `C:\Program Files (x86)\Steam`, running at probe time |
| Wargame: Red Dragon (app 251060) | `appmanifest_251060.acf` StateFlags 4 (fully installed), SizeOnDisk 22,894,585,504, buildid 15652829 |
| Game dir | `C:\Program Files (x86)\Steam\steamapps\common\Wargame Red Dragon` |
| Root `WarGame3.exe` | SHA-256 `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`, 30,032,896 B; listed in samples/game-binaries.json |
| `Data\PC\59638\WarGame3.exe` | SHA-256 `1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46`, 30,049,312 B: identical to the binary all 59638 analysis in this repo used |
| Exe builds present under `Data\PC` | 48574, 49125, 49964, 58710, 59095, 59638, 68335, 72352, 116084, 130278 |
| Data builds present under `Data\WARGAME\PC` | same set plus 131544 |
| `Data\WARGAME\PC\59638\NDF_Win.dat` | present |
| Save location | `C:\Users\sein\Saved Games\EugenSystems\WarGame3\` exists with `Option.ini` and `EugGame.lock` (the game has been started at least once); no `.wargamerpl2` files anywhere in the profile |
| Host/guest transfer | Parallels Shared Profile ON (guest Desktop/Documents/Downloads map to the host's); Shared Folders OFF |

## Blockers and open questions

1. Authorization. Launching the game and recording a match requires the
   user's go-ahead; the agent must not start it.
2. Build mismatch. A new replay will carry the current client Version, not
   59638. The repo's verified layouts are for 59638; the recording would first
   validate the structural method on the new build (its `Data\PC\<build>`
   executable is on disk for the same creator/jump-table procedure) and only
   then the semantics. Expect `inferred` labels until that is done.
3. Replay output path. Unverified. Hypothesis: the game writes
   `.wargamerpl2` under `Saved Games\EugenSystems\WarGame3\` (possibly a
   `Replays` subfolder). Confirm after the first recording with a recursive
   search of the profile.
4. Performance on ARM64 emulation. Untested; a 1v1 skirmish against AI on a
   small map is the lowest-cost trial.
5. Steam account / DRM. Steam is installed and running; whether the account is
   logged in and owns the title was not probed (would require UI).

## Proposed recording protocol (for the user to run; not executed)

1. Start Steam and the game in the guest. Note the in-game version string.
2. Skirmish vs AI, 1v1, small map, deck with at least one supply truck and one
   infantry unit. Keep a text log on the host (shared Documents) with wall-clock
   timestamps for each of these scripted actions:
   a. t0: match start (first unit visible).
   b. Buy exactly one supply truck; log the unit name and spawn point.
   c. Place one map flare (0x08) at a named landmark; log the text label.
   d. Move one unit to a second named landmark; log start/arrival times.
   e. Toggle the supply truck's supply off, then on (expected 0x18 pair).
   f. Change the production queue once (expected 0x0C), log what changed.
   g. End the match at a logged time.
3. Save the replay. Copy it to the host via the shared Documents folder.
4. In the repo: add it to samples/manifest.json with SHA-256 and the log;
   run the decoder; compare command frames with the logged timestamps to
   estimate frame duration; compare 0x08 coordinates with landmark positions.

## Confidence

All table entries are CONFIRMED by command output in this session. Items 2-5
are UNRESOLVED.
