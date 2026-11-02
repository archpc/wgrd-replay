# Revision 131544: verified Ghidra project reuse

Status: task-owned canonical CLI query completed. Live MCP servers and their
registration were not changed or restarted. No VM was operated by this check.

## Actual result

- Canonical Git HEAD: `d54a4661da20382ad8456564a08569fdd24131c5`.
  The helper does not self-report a build commit (`build_commit:null`); Git HEAD
  is not a cryptographic attestation of compiled chunks.
- Target PE SHA-256:
  `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d`.
- Ghidra provider: 12.1.4, procedure `0xaaedf0`.
- Evidence ID:
  `ev_65ed27c8318d4ed355740c4c41a1c545d5b555309acb362317896b97191a98e5`.
- Reported command time: 6153 ms, exit 0.
- Import mode: `existing-project-private-copy-v1`.
- Annotation policy: `read-only-existing-project-v1`.
- Project name `wgrd131544`; imported **program name `WarGame3.exe`**.
- Selected project fingerprint:
  `8861d185713b01edcf2ca0905826b0e95499897f062321ca847204ffd74108fb`.

The query selected the previously hash-verified disposable project, not the
original project. REA then made its own session-private copy and performed no
import, auto-analysis or repair. Original analysis completeness/settings remain
unknown. Ghidra returned the expected signed counter conversion and scale:

```c
return (float10)((float)*(int *)(in_ECX + 0xd0) * 0.2);
```

This is decompiler interpretation, corroborating the already checked
[clock instructions](2026-11-02-aar-clock.md), not original source or runtime
observation. It does not establish the battle-clock origin or replay-frame offset.

## Preservation and MCP

The complete file sets and hashes of both the original and the selected disposable
`.gpr`/`.rep` pairs matched before and after the query. No source-project lock
remained. MCP subsequently reported `open:false`, `cleanup_pending:false` and
`alignment:aligned` for the canonical launcher path.

`expected_server_path` takes the launcher file (`scripts/rea.mjs`), not its parent
installation directory. An initial comparison using the directory produced a false
registration mismatch; correcting the input resolved it without a restart.

## Version boundary

The canonical checkout describes itself as 852 commits after tag
`rea-agents-6.8.0`. That tag lacks the existing-project configuration module.
Replacing this source build with the published 6.8.0 package would lose reuse.
The upstream branch advanced again while the audit ran; those newer commits have
not been adopted or declared compatible by this smoke test. A coordinated rebuild
and restart window is still required before replacing the shared lazy-loaded build.

The smoke verifies the current canonical commit only. It is not a claim that
upstream-current code, every provider, or the old imported project's analysis
completeness has been validated.

## Reproduction evidence

Private `aar-20261102T050816Z/` artifacts:

- `ghidra-reuse-smoke.json`: complete REA evidence envelope and profile.
- `ghidra-reuse-smoke.stderr`: actual command timing.
- `ghidra-reuse-smoke-before.json`: both source-project file/hash snapshots.
- `ghidra-reuse-smoke-verification.json`: post-check assertions and limitations.

The invocation used the canonical Node/REA launcher, explicit Ghidra and Java
paths, `REA_GHIDRA_PROJECT_PATH` selecting the disposable `.gpr`,
`REA_GHIDRA_PROGRAM_NAME=WarGame3.exe`, `--provider ghidra --format json --full-output`,
and approved scratch for Node/Java temporary work. No install, configuration edit,
shared-server cutover or original-project save was needed.
