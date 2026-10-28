# Documentation research and conservative refactoring assessment

Dated 2026-10-28. Scope: improve navigation, runnable examples and contributor
feedback without changing verified layouts or rewriting historical evidence.
Repository observations refer to starting commit `7daa1c4` unless stated otherwise.
This assessment is not a replacement research roadmap; use
[NEXT-STEPS.md](../NEXT-STEPS.md) for investigation priorities.

## Exemplars and application

These primary sources were read on 2026-10-28. The CPython links below track
`main` and can change; the observations name the specific functions inspected.
They are examples of local design choices, not claims that every part of those
projects should be copied. No third-party code was imported.

| Source | Concrete observation | Application to WGRD |
|---|---|---|
| [CPython wave](https://github.com/python/cpython/blob/main/Lib/wave.py) | `_Chunk.read` bounds a read to the chunk; constructor/read helpers translate short binary reads into explicit exceptions | Retain bounded cursors and explicit failures; do not substitute permissive skipping for exact consumption |
| [CPython tomllib parser](https://github.com/python/cpython/blob/main/Lib/tomllib/_parser.py) | Parsing rules such as `create_dict_rule` translate internal conflicts into `TOMLDecodeError` | Validate metadata shape at the parser boundary rather than catch all exceptions in consumers |
| [Python argparse tutorial](https://docs.python.org/3.13/howto/argparse.html) | Small commands are paired with expected results; positional arguments and flags are explained separately | Add runnable quick-start tasks, option effects and exit-code troubleshooting |
| [Python documentation style](https://devguide.python.org/documentation/style-guide/) | Prefers simple language and explains unfamiliar abbreviations | Keep instructions short and name what a result actually proves |
| [Diataxis incremental guidance](https://diataxis.fr/how-to-use-diataxis/) | Improve an existing small section rather than impose an empty documentation hierarchy | Add the missing task and contributor guides; keep canonical reference and research paths intact |
| [PEP 8](https://peps.python.org/pep-0008/) | Project consistency and compatibility can outweigh mechanical style compliance | Avoid a formatter migration or broad renaming; preserve the protected cow and existing output keys |

## Audit findings

- The original README led with milestones before a runnable first task. Added
  a quick start and a task-to-document map without deleting the historical record.
- API entry points, CLI error boundaries, corpus comparison semantics and
  artifact-dependent testing were scattered across code and notes. Added
  [usage](USAGE.md) and [contributor](../CONTRIBUTING.md) guides linked from the README.
- The README's strict-JSON statement was broader than the implementation:
  `main` uses `allow_nan=not a.timeline`, while the timeline normalizes numbers.
  Added a dated correction; did not change serialization policy on `main`.
- Some older tests load samples directly, while newer tests skip absent
  artifacts. Documented the distinction rather than promise an artifact-free suite.
- The link checker is a heuristic over tracked Markdown. Its baseline reports
  path-like vocabulary and external/archived build references as well as a missing
  report-runtime link. Documented its limits instead of deleting provenance or
  treating all diagnostics as actionable broken links.

## Refactoring decisions

| Candidate and code location | Benefit | Risk and required verification | Decision |
|---|---|---|---|
| Explicit object checks in `wgrd_replay.parse_header` | Prevent malformed metadata leaking `AttributeError`; honor the documented format-error boundary | Changes failure behavior, so requires synthetic root/game shape cases, CLI and corpus checks, and authentic-output identity | Narrow bug fix for a separate review branch; not a behavior-preserving refactor |
| Name the pact prefix size shared by parser, timeline and corpus | Removes repeated 14/30-byte offset arithmetic | Must keep every source offset and output key identical; authenticate all sample outputs and test truncated prefixes | Worth a future small review change; unnecessary for the documentation task |
| Context-managed reads in research reproduction scripts and tests | Removes observed unclosed-file warnings | Historical source preservation and manifests require a deliberate follow-up; no format semantics change justified | Defer; report existing warnings rather than alter archived tools opportunistically |
| Extract the command dispatcher into handlers or classes | Might shorten one long function | Adds indirection between creator evidence and exact byte reads; can change rollback/count behavior | Defer until a real opcode addition demonstrates a simpler boundary |
| Extract a shared JSON normalization module | Could align parser and timeline output handling | Default parser currently permits non-finite tokens; normalization is an output-contract decision, not mere cleanup | Defer pending an explicit policy and compatibility tests |
| Packaging, new dependencies, formatter or typing migration | Could help a larger distribution workflow | Adds installation and maintenance cost without solving current decoding tasks | Do not introduce for this assignment |

No broad executable refactor is justified by line count or another project's
popularity. The existing flat stdlib modules and evidence-oriented field names
are useful constraints. Documentation changes are independently reviewable and
must not claim an unmerged executable fix is already available on `main`.

## Verification record

Actual commands, results, known warnings and preservation limits are recorded in
[the dated session report](../research/session-records/2026-10-28-documentation-dx.md).

## Repository-wide redesign — 2026-10-28

This is a later review of local starting commit `ad5dda0`, including the existing
README cow credit and source-comment edits. It supplements the earlier assessment;
it does not replace its dated verification record. Remote `main` had advanced to
`6b1ea34` during the session; its Python files and README matched the local starting
material exactly. Publication can therefore preserve those concurrent commits.

### Principal weaknesses and implemented structure

The audit inventoried all 51 existing Markdown files, including topic notes,
plans, session records, report assets and the controlled experiment. Current
references were checked against the Python parser, timeline, orders, entities,
production, unit-data and corpus modules and their tests. Historical material was
examined for scope, navigation and contradictions, rather than rewritten as if it
had been authored today.

The principal problems were competing current/historical narratives in the
README, weak links between current reference and evidence, dense mixed-purpose
layout tables, and confidence language that collapsed structure, semantics and
build transfer. The existing usage and contributor guides were worth keeping.

The resulting hierarchy is deliberately small: README for orientation; a short
[documentation map](README.md); [usage](USAGE.md) for tasks;
[architecture](ARCHITECTURE.md) for implementation and the single evidence-reading
guide; [FORMAT.md](../FORMAT.md) for wire/reference contracts; the existing
[research index](../research/INDEX.md) for findings, scripts and source evidence.
No research files were moved. No second research guide or roadmap was added.

| File | Substantive change |
|---|---|
| [README](../README.md) | Capabilities → evidence boundaries → run → inspect → investigate → contribute → limitations; research links at the top; credits retained verbatim |
| [Format](../FORMAT.md) | Consistent byte notation, layout tables, annotated hex example, parser/observation boundaries, event field table and current production-layer explanation |
| [Architecture](ARCHITECTURE.md) | Pipeline diagram, authoritative evidence conventions, build/status distinction and clickable canonical references |
| [Usage](USAGE.md) | Authenticated event projection, precise provenance language and stable error descriptions |
| [Contributing](../CONTRIBUTING.md) | Replace prior-assignment branch instructions with reusable guidance; connect research workflow to evidence conventions |
| [Documentation map](README.md) | One short question-to-reference index, with research treated as a primary destination |
| [Research index](../research/INDEX.md) | Dated current-behavior clarification above intact milestone tables; preserve original-corpus source limits |
| This review | Audit decisions, before/after examples, verification and deferred issues |

### Before → after: technical corrections

| Earlier wording or structure | Current reference and reason |
|---|---|
| Metadata described as a “flat-string-valued object” | Nested `game` and player objects; sample field values are commonly strings; parser shape defect remains explicit |
| Frame heading “VERIFIED” followed by L=12 `endt` | Observed L=12 is separate from implemented minimum L=4; the parser does not require a zero tail or equality with metadata `NbMaxPlayer` |
| Unknown frame content “preserved” without an output boundary | Original file retains those bytes; parser/timeline results omit undecoded `star`/`endt` tails |
| `0x08` described as an inferred map flare | Consumer-backed matching-build marker **request**, linked to later research; actual creation remains unobserved |
| `0x0D` interiors described simply as opaque | Parser framing remains opaque; timeline production decoding has a separate complete/malformed payload result |
| Other-build statuses described as always inferred | Supported interpretations transfer as inferred; unsupported meanings remain unknown |
| Canonical usage destination was README | Usage/API tasks belong to the existing usage guide; README provides orientation |
| One confidence label applied to an entire structure | Identify layout, sample observation and interpretation separately; definitions live in architecture |

Older findings and evidence remain available in their original files. Changing
coverage totals were replaced with links to generated source data; source limits,
raw-field cautions, static-type constraints and credits were retained or linked
from their relevant reference. This is an editorial redesign, not a new binary
investigation or a claim to have fixed parser defects.

### Validation of this redesign

- Python 3.15.0: the prescribed unittest command ran **148 tests, OK, no skips**.
  Existing unclosed-file `ResourceWarning` messages remain in research/test code.
- Six authenticated original/cross-build replays: default, summary, timeline,
  timeline-summary and enriched-timeline CLI exports succeeded. API enrichment
  serialized with `allow_nan=False`; the README request loop and the usage
  projection matched actual output. Both help commands, the unit-data usage
  error, full inventory and header-only inventory behaved as documented.
- Synthetic boundary probes reproduced the metadata-shape defect, minimum
  four-byte `endt` acceptance, lack of metadata slot-count enforcement, and
  unknown semantics on a mismatched build. These verify current behavior, not
  new format facts.
- The existing link checker changed from 31 to 30 findings, exit 1: removal of
  the slash-separated status phrase eliminated one false positive. Remaining
  findings concern recovered transcript paths, historical/external work/report
  paths and one unavailable report-runtime JSX target. They were retained and
  classified rather than hidden by modifying history or the checker.
- An additional scan includes the new index and validates local Markdown targets
  and heading fragments. No new broken links or fragments were found; the sole
  regex finding in REA notes is disassembly syntax containing a bracketed vtable
  offset followed by a call argument, not a Markdown link.
- Independent read-only review checked the five acceptance criteria. Its one
  finding, the missing event-only `unresolved_boundary` status, was corrected in
  the authoritative table before publication.
- Markdown parsed into temporary table-enabled HTML for structural inspection.
  Local browser preview was unavailable: serving a local port was denied and
  browser policy disallowed file URLs. This is not claimed as screenshot QA.
- Preservation checks: **182 entries OK**, zero problems; **450 local artifact
  entries**, none missing or changed. Neither manifest was edited. File hashes
  confirm every tracked non-Markdown file, including `wgrd_orders.py`, remained
  byte-identical to the start. Existing README credits remained verbatim.

### Remaining weaknesses that need separate work

The external report runtime link is unavailable in a standalone checkout; a
future report-maintenance change should provide a valid distribution destination
without rewriting archived provenance. The heuristic link checker still does not
validate all Markdown forms or heading fragments. Historical notes necessarily
contain superseded claims; the current-reference routes now explain how to read
them, but a future evidence audit could annotate more individual contradictions.
Minimum supported Python versions have not been established by a version matrix.
Frame timing, coordinates and general execution semantics still require research;
polished documentation does not resolve them. The known metadata defect and JSON
policy differences remain separate implementation work.

## Repository rationalization (2026-10-28)

Based on remote main `460a3ab8c18c7ac188abb0b4deae8defb0f0699e`, source tree
`4d4df498d47246522bf93c5317be189e1c6af74d`. A separate scratch checkout was used;
the primary checkout was not edited. The user authorized GitHub branch/commit/PR
publication and broad maintenance discretion, preserving APIs, evidence and the cow.

### Decisions

- Retain the existing module boundaries: parsing, interpretation, attribution and
  static enrichment already have different invariants. A package rewrite adds risk
  without a demonstrated benefit. Consolidate only duplicate non-finite JSON
  conversion in `wgrd_replay.json_safe`; retain the former private helper names.
- Put the module/test change guide before evidence taxonomy. Routine maintenance
  starts with the owning code and tests; research reading is conditional on needing
  new format knowledge. Replace the long agent checklist with the same practical
  path. Keep the byte maps and research evidence. Shorten the normal reading path:
  README for entry points, FORMAT for wire layouts, architecture for invariants,
  CONTRIBUTING for checks. Move the previous full roadmap into
  [a dated archive](../research/NEXT-STEPS-2026-10-28.md), with source identity;
  move contributor attribution into the [research index](../research/INDEX.md#project-credits).
- Use confirmed/inferred/unknown in new prose. Keep historical confidence nuances
  and all parser/timeline statuses; they answer different questions.
- Check explicit Markdown links in CI, relative to their document. Drop the
  37-entry prose-path exception list: inline code is not a hyperlink. Keep the old
  diagnostic for historical reproduction. External URLs, fragment existence and
  full Markdown grammar remain outside this offline check.
- Merge preservation into quality rather than provisioning a separate runner.
  Test every supported minor (3.13/3.14/3.15). Retain read-only permissions,
  SHA-pinned official Actions, timeouts, full discovery, mandatory hash-pinned
  public data, and explicit absent-private-artifact skips. Detect tracked writes
  across the whole repository after each job, instead of only two path scopes.

### Preservation policy: preserve sources, allow maintenance

The first version of this PR retained the historical hash freeze and added exact
exceptions. The owner asked to loosen preservation because it obstructed useful
work. That machinery is now removed: no manifest hash pins, script-revision
allowlist or blanket freeze on research notes and code.

CI checks archived source copies against the existing work-artifact inventory,
and protects the cow. Maintained scripts and documentation rely on ordinary diff
review, regression tests and Git history. Intentional inventory updates use the
same review process; there is no separate preservation approval flow. Original
observations should remain recoverable when a finding is corrected.

Both historical manifests and verifiers remain unchanged as optional audit
records. Their three script mismatches trace to
[24a1f5c](https://github.com/archpc/wgrd-replay/commit/24a1f5c61b540ed17b4ad0b77871ec1b5760e934):
`Path` imports and `read_bytes()` replaced unclosed file reads in
`research/op0c_layout.py`, `research/op18_reference_keys.py` and
`research/op18_supply_targets.py`. Diff review and historical/current result
comparisons found no analysis changes. This is an example of legitimate
maintenance the old blanket freeze should not block. Reproduce with
`git diff 681d8ee 24a1f5c --` followed by those paths.

No evidence, byte maps, coverage or sample manifests were removed. The full
previous roadmap is archived with provenance. The deleted prose exceptions were
CI false-positive handling, not binary findings.

### Validation of this change

- Baseline: 161 tests, no skips on Python 3.15. After rationalization: 164 tests,
  no skips on Python 3.13.15, 3.14.7 and 3.15.0. Tests used the authenticated
  original three replays, three cross-build replays, the 59638 executable and
  the hash-pinned public fixture. Private artifacts were read locally, not copied
  into Git.
- With all private fixture locations redirected to absent paths, discovery ran
  164 tests and reported 51 skip records (including sample subtests). Synthetic
  and mandatory public-fixture checks ran. This is unavailable private coverage,
  not 164 passing cases.
- All six replay hashes were checked before comparing 48 before/after results:
  parser dictionaries, timeline/enriched dictionaries, and five CLI modes per
  replay (default, summary, timeline, timeline summary, enriched timeline).
  Canonical API JSON hashes and CLI byte hashes were identical.
- The three historically changed research scripts were loaded alongside their
  `681d8ee` sources and compared on all original authenticated samples. Analysis
  results matched; `op0c_layout.main` stdout/return status also matched using the
  SHA-256-verified 59638 executable. No executable was run.
- Syntax (65 tracked Python files), Ruff 0.14.2, explicit Markdown links (53 files),
  portable preservation and actionlint 1.7.12 passed. ShellCheck was unavailable;
  actionlint ran with its ShellCheck integration disabled. The historical link
  diagnostic reported 46 findings before and after, with identical source/target
  pairs; these depend on external/local paths and are not 46 broken hyperlinks.
- Historical preservation still reports exactly three script mismatches, by
  the retired snapshot policy. The local-only work inventory reports 439 missing entries in scratch;
  these were not copied merely to satisfy an audit. Its 71 committed archive
  copies are authenticated by the portable gate. Both historical manifests and
  verifiers, all evidence bytes and the entire orders module remain unchanged.

The active README/CONTRIBUTING/NEXT-STEPS path is shorter; archival text remains
accessible through explicit links. No package rewrite, third-party runtime
requirement, new evidence taxonomy or generated coverage baseline was introduced.
The archive check detects accidental loss or edits; Git review evaluates intentional
changes. It is not an immutable-history or security mechanism.
