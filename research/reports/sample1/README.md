# Sample1 report artifacts

BATTLE-REPORT.md: actual frame-based report, localized types and explicit orders.
measurements.json: full-population rubric, per-slot/window counts and selection bias.
events.csv: all4162 command records, without dropping opaque or contextual events.
anchors.json:45 selected report source events; reference-labels.json resolves labels.
ReportContent.jsx/report-copy.json: authored report surface, using the installed
Data report runtime. Authoring app under ignored work/sample1-battle-report-app.
No decoder or original game-asset changes.

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

Report prose/fields are source-backed through9 reviewed queries. Chronological
sections inspect their selected anchor ranges; coverage uses all4162 events.
Three bars measure request readability, not gameplay outcomes. Source tables retain
full values. Evidence search changes only the selected ledger, not coverage totals.

## Validation performed

- Original replay SHA256 c5f8eff1298cf38c1d9967d29f98a22dfc869c150405630f9f695bb80a521df8.
- Descriptor index SHA256 e73c0826b59c4fc6ad5940bb437fae71a8bb9b2080e91e604e2de7a9f4e15a5a.
- All4162 CSV rows reconcile to520 meaningful request,3318 partial,324 opaque
  to narrative. The324 subdivide233 opaque interiors,42 unknown layouts,49
  known-layout/uninterpreted records. Selected45 anchors:39/4/2 respectively.
- Push window S2 frames6321–6999:54 standard orders,50 contextual and4 explicit.
- App build and portable export passed installed protected-runtime/content checks.
- Browser inspected narrative, chart marks/hover, all summary tables and selected
  evidence ledger. T-72M1 search returned6 selected rows; clearing restored45.
  Render checked in the available681px-wide viewport; separate desktop/mobile
  viewport checks not performed. No claim of a complete responsive-layout audit.
- Decoder full suite not rerun: analysis/report-only changes. No simulated
  positions, ownership, damage, effective orders or outcomes introduced.

Local preview is a report artifact, not original game playback. Prepared date is
report creation, not match date. Recorded frames have no verified seconds mapping.
