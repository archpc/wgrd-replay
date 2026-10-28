# Documentation and developer-experience audit — 2026-10-28

Starting commit: `7daa1c4bd7ad4a71ae12a254a49bb8d1ec77347c`, clean `main`.
Task: research exemplary Python and technical documentation, improve WGRD's docs
and developer experience, and evaluate conservative refactoring. Documentation
may go to `main`; executable changes and associated documentation must remain
on a separate review branch. The ASCII cow is protected: no edits anywhere in
`wgrd_orders.py`.

## Changes and research

The [development assessment](../../docs/DEVELOPMENT-REVIEW.md) records primary
sources, inspected functions, adopted practices and refactoring tradeoffs.
The README gains a quick start and task-based navigation. New
[usage](../../docs/USAGE.md) and [contributor](../../CONTRIBUTING.md) guides cover
API calls, options, errors, output contracts, artifact prerequisites and checks.
Existing research notes, generated JSON and format evidence remain intact.

Two misleading generalizations are corrected in active documentation: default
parser output can permit non-standard JSON numbers, and not all sample-backed
tests skip when artifacts are missing. Neither behavior is changed on `main`.

The known metadata-shape defect merits a narrow review-branch bug fix, not a
dispatcher rewrite. Larger refactors remain evaluated and deferred; see the
assessment. This `main` report does not claim the proposed bug fix is merged.

## Baseline and documentation verification

Interpreter: Python 3.15.0. Command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

Baseline: 148 tests, OK, no skips. Existing `ResourceWarning` diagnostics identify
unclosed reads in the 0x0C layout test and the 0x0C/reference-key/supply-target
research scripts. They are reported, not suppressed or folded into a documentation
commit. This is a dated run, not a standing test count.

Before editing executable code, captured SHA-256 values of full parser, summary,
timeline and enriched timeline CLI output on all original authenticated samples.
Also captured the full protected-file hash. Local logs and hashes are under
`work/dx-audit/`; private decoded outputs were not committed.

The link checker baseline is exit 1 with 31 findings: one status-vocabulary false
positive in architecture, eight recovered-evidence transcript references, seventeen
references in the historical work-artifact note, four external report-build paths,
and one absent report-runtime JSX link. Those diagnostics concern retained history
or the external report build, rather than the newly added guides. The old dated
32-warning record is retained; the historical difference is not reconstructed.

Preservation baseline: tracked manifest reports 182 entries OK, zero problems,
with five permitted active-document exceptions. Local artifact verification reports
450 entries, none missing or changed; audit scratch files are newly untracked.
These manifests are scoped checks, not a guarantee about unlisted files.

Final documentation suite: 148 tests, OK, no skips (9.699 seconds). Full inventory
accepted all six authenticated original/cross-build samples as structurally
compatible; header-only inventory reported all six as not checked. Executed the
usage guide's Python example with an authenticated sample substituted for the
placeholder, including strict JSON serialization. Both CLI help commands and
the documented unit-data usage error behaved as described. All twelve captured
original-sample CLI outputs remained byte-identical. The complete protected-file
SHA-256 remained unchanged.

## Integration limitation

Staging failed because the session cannot write Git metadata: creating the Git
index lock returned Operation not permitted. No commit, review branch, push or
executable edit was made. The documentation changes remain unstaged on `main`.
The proposed metadata-shape fix remains an assessment, not an implemented fix.
This avoids placing executable changes or fix-specific documentation on `main`.
New guides require a separate explicit link scan because the repository checker
only examines tracked files and staging is unavailable.

Final link checks: the tracked-file checker still exits 1 with exactly the same
31 findings (the before/after outputs compare identically). An explicit scan of
all five edited/new Markdown files using the checker's target/resolution rules
reports zero unresolved references. This shares the documented checker limits;
it does not validate web availability or every Markdown form. `git diff --check`
passes. No executable files changed.

At the user's request, checked execution location directly: terminal commands
report Darwin 27.2.0 arm64, macOS 27.2 build 26B123, computer name Honk and a
Homebrew Python interpreter. These commands use the Mac's environment even
though the conversation interface reports cloud hosting. Attempted to create a
separate ChatGPT Work cloud task carrying the complete drafts and instructions;
the app service returned an error. No cloud transfer was confirmed. Local edits
remain available in this checkout and no background job was left running.

## Deliberate limits

No game launch, VM access, executable analysis, dependency installation, artifact
acquisition, coverage regeneration or publication. No changes to opcode layouts,
semantic confidence or output keys on `main`. Test-version observations are not a
new minimum-Python guarantee. This work is local; remote publication is outside
the task's explicit instructions.
