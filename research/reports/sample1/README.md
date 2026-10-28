# Sample1 report artifacts

BATTLE-REPORT.md: actual frame-based report, localized types and explicit orders.
measurements.json: full-population rubric, per-slot/window counts and selection bias.
events.csv: all 4162 command records, without dropping opaque or contextual events.
anchors.json:45 selected report source events; reference-labels.json resolves labels.
ReportContent.jsx/report-copy.json: authored report surface, using the installed
Data report runtime. Authoring app under ignored work/sample1-battle-report-app.
No decoder or original game-asset changes.

## Runtime dependency and preserved presentation (2026-10-26)

The authoring app is OpenAI's "data-app" report/dashboard runtime, installed by
the Codex/ChatGPT `build-report` skill (package name `data-app`,
`.openai/hosting.json`, `protected-runtime.json`, React 19 / Vite / Recharts /
Lexical / Radix). Credit: OpenAI, via the ChatGPT session archived in
`research/chatgpt-session-2026-10-23/`. Its redistribution terms have not been
confirmed, so the runtime stays local (git-ignored), hash-manifested in
`research/maintenance/work-artifacts-manifest.json` (251 files excluding dist/),
and is NOT committed. Only the WGRD-authored content is tracked, under
`app-content/` (`src/content/`, `src/data.json`; exact copies, hash-verified).

Portable presentation without the runtime (already tracked):
`research/chatgpt-session-2026-10-23/outputs/sample1-battle-report.html`
(self-contained build, 2.9 MB),
`research/chatgpt-session-2026-10-23/outputs/sample1-battle-report.md` (same text as
BATTLE-REPORT.md) and `research/chatgpt-session-2026-10-23/outputs/sample1-report-preview.png`.

## Recalculate

From repository root, with authenticated Sample1 cached:

```sh
python3 -B research/sample1_battle_report.py
```

Authenticates replay and descriptor-index hashes, builds the existing timeline,
asserts the request-level rubric and reconciles all events, phase/slot populations,
explicit subtypes, Shoot actor occurrences, opaque breakdown and unknown outcomes.
Writes deterministic measurement/audit files plus an ignored reviewed-data snapshot.
Snapshot execution timestamps change; measurement/audit contents do not depend on time.
Hand-authored prose is tied to this fixed sample; do not reuse it for another replay.

## Rebuild the report surface

Use installed Data plugin scripts and bundled Node per its authoring guide:

1. Prepare a new report app with --surface report and
   --snapshot work/sample1-report-snapshot.json; read its AGENTS.md.
2. Copy ReportContent.jsx and report-copy.json into src/content/report/.
3. Set src/data.json buildStatus to complete once authored scope/checks are done;
   preserve the app ID assigned during preparation.
4. Build through data-app.mjs build --project-dir APP --separate-data.
   Serve the complete dist/ directory locally; open its localhost preview.
5. For a portable HTML, use data-app.mjs export-offline with an output beneath
   APP/.data-app-offline/exports/. No package install, cloud publication or
   protected-runtime edits required.

Report prose/fields are source-backed through 9 reviewed queries. Chronological
sections inspect their selected anchor ranges; coverage uses all 4162 events.
Three bars measure request readability, not gameplay outcomes. Source tables retain
full values. Evidence search changes only the selected ledger, not coverage totals.

## Validation performed

- Original replay SHA256 c5f8eff1298cf38c1d9967d29f98a22dfc869c150405630f9f695bb80a521df8.
- Descriptor index SHA256 e73c0826b59c4fc6ad5940bb437fae71a8bb9b2080e91e604e2de7a9f4e15a5a.
- All 4162 CSV rows reconcile to 520 meaningful request, 3318 partial,324 opaque
  to narrative. The 324 subdivide 233 opaque interiors,42 unknown layouts,49
  known-layout/uninterpreted records. Selected 45 anchors:39/4/2 respectively.
- Push window S2 frames 6321–6999: 54 standard orders, 50 contextual and 4 explicit.
- App build and portable export passed installed protected-runtime/content checks.
- Browser inspected narrative, chart marks/hover, all summary tables and selected
  evidence ledger. T-72M1 search returned 6 selected rows; clearing restored 45.
  Render checked in the available 681px-wide viewport; separate desktop/mobile
  viewport checks not performed. No claim of a complete responsive-layout audit.
- Decoder full suite not rerun: analysis/report-only changes. No simulated
  positions, ownership, damage, effective orders or outcomes introduced.

Local preview is a report artifact, not original game playback. Prepared date is
report creation, not match date. Recorded frames have no verified seconds mapping.
