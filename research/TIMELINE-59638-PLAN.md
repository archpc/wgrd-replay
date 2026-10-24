# Player-readable59638 timeline enrichment

Baseline02b4081. Existing checkout. User-authorized implementation; no simulation.

- Export a versioned compact index from authenticated original NDF artifacts.
  Full GUID keys, candidate arrays, source descriptor/type records, exact paths,
  source archive/entry/object hashes and offsets, raw selector conditions.
- Recover original unit-name dictionary from game patch layers loaded by59638.
  Preserve locale/asset hashes and explicit localization status. No spreadsheet
  or debug-name substitution presented as localized names.
- --timeline --unit-data accepts index file; existing58710 directory stays compatible.
  Annotate catalog only. Unique/ambiguous/missing states explicit; source/request
  build mismatch inferred; unit runtime identity and effective kinds remain null.
- Focused tests first: unique and ambiguous paths, missing records, malformed index,
  locale hashes, mismatch, no parser/event mutation, CLI compatibility/determinism.
- Commit tested index support, then verified localization improvement if separable.
  Full source game/replay data stays local; compact versioned export bundled in Git
  as deterministic gzip with input/export manifests.

Completed: original59638 US dictionary recovered; all2121 types localized. Index
and localization shipped together. 685 matching-build references +41 inferred
Sample2 references enriched; 71 tests pass. Default/plain timeline byte-identical
to02b4081. One bounded review; two concrete gaps fixed. See TIMELINE-59638.md.
