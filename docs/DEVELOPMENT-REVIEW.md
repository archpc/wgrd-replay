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
