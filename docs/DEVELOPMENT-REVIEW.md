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
