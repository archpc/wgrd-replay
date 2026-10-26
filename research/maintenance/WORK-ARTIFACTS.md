# Local-only research artifacts under `work/` (git-ignored)

Audit date 2026-10-26, baseline commit in
`research/maintenance/work-artifacts-manifest.json` (450 files, 611 MB, SHA-256
per file). Policy for this audit: nothing under `work/` was deleted, moved,
overwritten, cleaned or committed. `referenced_by_tracked_files` in the manifest
counts tracked text files mentioning the path or a parent directory of it
(prefix match), so it is an upper bound.

## Categories

| Category | Files | Size | Identical tracked copy | Regenerability | Preservation status |
|---|---:|---:|---:|---|---|
| rizin-disassembly-excerpt (`work/*.asm`: production-*, entity-trace*, op07-finaltrace, b32690, c972a0) | 21 | 1.2 MB | 0 (now copied, see below) | In principle via rizin on the 59638 binary; exact commands not recorded per file | **ARCHIVAL RISK**: original evidence behind OP07-ORDERS, PRODUCTION-COMMANDS, ENTITY-CONTEXT addresses exists only here |
| rea-mcp-raw-response (`work/rea-mcp-3..21.json`) | 19 | 1.8 MB | 0 (the 7 same-named files under `research/chatgpt-session-2026-10-23/work/` differ by hash) | Not regenerable as-is (REA session state) | **ARCHIVAL RISK** |
| validation-log (`*.log`) | 6 | 16 KB | 0 | Historical output | risk, low value |
| probe-or-validation-script (`rea_mcp.py`, `production_rea.py`, `production_probe.py`, `validate_*_cli.py`, `read_ndf_manifest.py`, `inspect_localization_manifests.py`, `*baseline_wgrd_replay.py`) | 11 | 53 KB | 0 | Original scripts | **ARCHIVAL RISK** (baseline decoder copies are also in git history) |
| report-app-source (`work/sample1-battle-report-app/`, Vite app incl. `dist/`, no node_modules) | 254 | 7.8 MB | 3 | Not regenerable: original work | **ARCHIVAL RISK**; only `ReportContent.jsx`, data JSON and README are tracked under `research/reports/sample1/` |
| decoder-output-snapshot (`*.wargamerpl2.*.json`, `baseline-*`, `default-*`, `blocks.json`, `op07-fields.json`, `production-*.json`, ...) | 47 | 439 MB | 0 | Regenerable from the external samples with the current decoder; `baseline-*` need the historical decoder commit (in git history) | low risk; do not commit (size, derived from non-redistributable replays) |
| ndf-extraction (`work/ndf59638/`, `work/ndf-recovery/`) | 31 | 109 MB | 1 | `work/ndf59638/` via `research/ndf59638_unpack.py` from the original archive (external, proprietary); `ndf-recovery` regeneration not demonstrated | proprietary-derived; do not commit; document only |
| localization-extraction (`work/localization59638/`) | 21 | 4.7 MB | 0 | Not demonstrated | proprietary-derived; do not commit |
| public-dataset-snapshot (`work/public-units/`) | 21 | 40.8 MB | 0 | Re-downloadable; pinned sources and hashes in `research/public-unit-sources.json` | low risk |
| runtime-feasibility-data (`work/runtime59638/`, `work/compat59638/`) | 18 | 3.9 MB | 2 | Partly outputs of `research/runtime59638_prerequisites.py` | medium |
| tool-schema-capture (`work/rea-tool-schemas.json`) | 1 | 3.4 MB | 1 | Re-capturable | preserved (tracked copy identical) |

## Findings

1. Eight REA evidence IDs cited in `REA-NOTES-59638.md` Sessions 1-3
   (ev_b44efd7d, ev_7841a093, ev_4ea358ce, ev_1e924a6e, ev_37b97e85,
   ev_d3d3f966, ev_0ea526f5, ev_06018019) are not present under
   `research/evidence/`, `work/`, or `~/.hermes/artifacts/wgrd-replay/` at audit
   time. They were subsequently recovered verbatim from 2026-10-23 Hermes
   session transcripts and added to `research/evidence/`
   (`research/evidence/RECOVERED-2026-10-26.md`). Time Machine could not be
   read from this session (no Full Disk Access; snapshot mount refused).
2. The small text evidence above (about 3 MB: `.asm`, `rea-mcp-*.json`, logs,
   probe scripts) and the report app source (7.8 MB) exist only in the ignored
   directory. Loss of `work/` would lose the original evidence trail for the
   0x07, production and entity investigations.

## Preservation actions taken (2026-10-26 follow-up, user-authorized)

- Copied (hash-verified, `copied_to` in the manifest; `work/` untouched): 57
  text evidence files (21 `.asm`, 19 `rea-mcp-*.json`, 6 `.log`, 11 `.py`) to
  `research/evidence/work-archive-2026-10-26/`; authored report content
  (`src/content/`, `src/data.json`, 14 files) to
  `research/reports/sample1/app-content/`.
- Not copied: the rest of `work/sample1-battle-report-app/` (a copied
  third-party data-app plugin runtime with `protected-runtime.json`;
  redistribution unclear), decoder output snapshots, and proprietary-derived
  NDF/localization extractions.
- Secret/PII scan of the copied text: only false positives (the binary string
  `"Token"` inside disassembly; sanitization code in the app).

## Original recommended strategy (for reference)

1. Review the `.asm`, `rea-mcp-*.json`, `.log` and `.py` files for
   redistribution concerns. Precedent: `research/evidence/` already tracks REA
   raw results and a rizin excerpt of the same binary. If acceptable, add them
   under `research/evidence/work-archive-2026-10-26/` preserving relative paths,
   and record the mapping in this manifest (`moved_to`), leaving `work/` intact.
3. Review `work/sample1-battle-report-app/` (excluding `dist/`) for third-party
   or personal content, then track it under `research/reports/sample1/app/`.
3. Keep `work/ndf59638/`, `work/localization59638/`, `work/ndf-recovery/`
   and decoder output snapshots local; they are proprietary-derived or
   regenerable. Record the regeneration command for `ndf59638` (present) and
   mark the others as not demonstrated.
4. Until then, keep an off-repository copy of `work/` with this manifest for
   hash verification: `python3 -B research/maintenance/work_artifacts_verify.py`
   (see below) reports changed or missing files.
