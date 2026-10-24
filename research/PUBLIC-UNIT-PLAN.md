# Public unit mapping investigation

Baseline06d1351; current tree clean. Native execution, existing checkout.

- [x] Pin ResidentMario/wargame-data and fmdostoyevskiy/wgrd-toolbox sources.
  Inspect extractor IDs, raw NDF descriptor GUIDs, deck/localization namespaces,
  versions and licenses. Public source cache stays ignored under work/.
- [x] Compare candidates with all726 authenticated full references. Numeric
  overlap alone is not identity proof. Separate Sample2/build510117427.
- [x] REA/Rizin: trace reference GUID -> saved-object pointer -> descriptor where
  reachable. Identify any required spawn/static mapping and version dependency.
- [x] If proven, enrich optional timeline only; otherwise preserve null identities
  and record a reproducible comparison/blocker. No runtime-state guesses for39.
- [x] Focused tests for new behavior, full regression once after changes,
  deterministic/default compatibility as appropriate; commit durable findings.

Stop: verified mapping milestone or explicit missing bridge/data. No installs,
global changes, full simulation, speculative best-match join or review loop.

Result: optional pinned descriptor annotation implemented;63 tests pass.
726 exact cross-version descriptor matches; company/member and per-frame
state bridge unavailable. Findings: PUBLIC-UNIT-MAPPING.md.
