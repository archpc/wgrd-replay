# Contributing

[Overview](README.md) · [Documentation map](docs/README.md) · [Research index](research/INDEX.md)

WGRD is a Python standard-library-only decoder. Work from the repository root;
there is no package installation, dependency manager, documentation build, or
mandatory formatter. Supported Python: **3.13 minimum**, through **3.15**.
CI tests 3.13 and 3.15. Older historical 3.9.6 results are not a support promise.

Read [AGENTS.md](AGENTS.md) for the full evidence and preservation rules, then
[architecture](docs/ARCHITECTURE.md) for the module responsible for your change.
Current research priorities remain in [NEXT-STEPS.md](NEXT-STEPS.md).

## Choose the change boundary

- Use a focused branch for reviewable changes. Inspect existing work before editing,
  stage paths explicitly, and inspect the staged diff. Do not include unrelated
  changes or force-push over concurrent work.
- Preserve existing output keys, raw byte fields, ordering, build qualifications,
  and exact-consumption checks. A structural match does not establish semantics.
- Leave the ASCII cow in `wgrd_orders.py` exactly unchanged.
- Keep old research notes and evidence intact. Add dated corrections and links;
  do not rewrite historical findings or hand-edit generated coverage JSON.

For a decoder change, reproduce the failure with a small synthetic fixture first.
Assert the public error or output contract, then check authentic, hash-pinned
samples. Synthetic inputs test implementation behavior; they do not establish
new binary-format facts. A behavior-preserving refactor also needs before/after
output comparisons. Avoid large abstraction or formatting changes mixed with a fix.

## Contribute a research finding

Search [the provenance index](research/INDEX.md) before tracing the executable.
Use [the evidence conventions](docs/ARCHITECTURE.md#evidence-conventions) and
[AGENTS.md](AGENTS.md) to state a falsifiable hypothesis, pin artifacts, preserve
observations, and distinguish interpretation from proof. Add a reproduction
script that fails on mismatch and regression tests where code depends on the
claim. Update the current reference and index; preserve the dated investigation.

Do not launch the game or operate a VM merely because a historical plan proposes
it. Executable research is static unless runtime work is explicitly authorized.
Keep replay bytes, game binaries, large dumps and private metadata outside Git.

## Tests and external artifacts

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -q
```

Use `-v` instead of `-q` to see individual test and skip names. Do not install a
third-party test runner. Run one fixture-only file when iterating, for example:

```sh
python3 -B -m unittest discover -s tests -p 'test_corpus.py' -v
```

The full suite includes synthetic binary fixtures and authenticated external
artifacts. Only tests requiring absent private replays or the private executable
skip; verbose output identifies them. Present-but-altered evidence fails.
The public unit snapshot is required: fetch its four existing hash-pinned inputs
with `python3 -B scripts/fetch_public_fixture.py` before discovery. Fetch/checksum
failures are failures; downloaded data stays in ignored local storage.

| Variable | What it locates | Default |
|---|---|---|
| `WGRD_SAMPLES_DIR` | Original sample files listed in [the manifest](samples/manifest.json) | `~/.hermes/artifacts/wgrd-replay/samples/raw` |
| `WGRD_ARTIFACTS_DIR` | Root containing the relative artifact paths in [the cross-build manifest](samples/cross-build-manifest.json) | `~/.hermes/artifacts/wgrd-replay` |
| `WGRD_EXE_59638` | Historical executable for static byte checks | `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe` |
| `WGRD_UNIT_DATA` | Required pinned public snapshot | `work/public-units/wargame-data` |

The CLI's `--unit-data` option is separate from the test environment variable.
Use the committed build-59638 index for offline enrichment as shown in the
[usage guide](docs/USAGE.md). No test needs to launch the Windows executable.
Do not acquire or redistribute proprietary artifacts merely to hide a skip.

## Verify the change

After the suite, run summary and timeline exports against an available,
authenticated replay using the [usage examples](docs/USAGE.md). Also run:

```sh
python3 -B research/maintenance/check_links.py
python3 -B research/maintenance/preservation_manifest.py verify research/maintenance/preservation-manifest.json
python3 -B research/maintenance/work_artifacts_verify.py
git diff --check
```

The link checker examines tracked Markdown only, skips several Markdown forms,
and treats some path-like prose as files. Record its exit code and compare
findings against the pre-change run; do not claim every warning is a broken link.
Stage new Markdown explicitly before checking it, then inspect `git diff --cached`.
The preservation checks cover named historical records and local artifacts, not
every file in the repository. Use Git to check everything else.

A useful verification report includes the interpreter, commands, actual tests,
failures, skip reasons, existing warnings, authentic samples checked, and limits.
Do not copy old test totals as current results. Do not suppress warnings merely
to make the report look clean.

## Write documentation that stays useful

Put runnable tasks in [the usage guide](docs/USAGE.md), implementation context in
[architecture](docs/ARCHITECTURE.md), and wire layouts in [FORMAT.md](FORMAT.md).
Link canonical explanations instead of copying changing counts or research
claims. Keep evidence definitions in the architecture reference, not in a new
legend on every page. Clearly mark placeholders and distinguish output fields
from conclusions.
Use short sentences and concrete examples. Keep private replay output outside Git.

The [documentation research and refactoring assessment](docs/DEVELOPMENT-REVIEW.md)
records the examples behind these choices and the changes deliberately deferred.

## Continuous integration

[CI runs](https://github.com/archpc/wgrd-replay/actions/workflows/ci.yml) on PRs
into main, pushes to main, and manual dispatch. Three jobs: full unittest
discovery on Python 3.13/3.15, quality, and preservation. Runtime/tests need no
packages; Ruff is the only additional CI tool. Hosted Ubuntu runners use
SHA-pinned official actions, read-only permissions and no persisted credentials.

Run the same checks from the root on both supported endpoint interpreters:

```sh
python3 -B scripts/fetch_public_fixture.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
python3 -m pip install --no-deps ruff==0.14.2
python3 -B scripts/check_python.py
git ls-files -z '*.py' | xargs -0 python3 -m ruff check --force-exclude
python3 -B scripts/check_docs.py
python3 -B research/maintenance/preservation_manifest.py verify research/maintenance/preservation-manifest.json
git diff --exit-code HEAD -- research wgrd_orders.py
```

Syntax and lint cover every tracked Python file, including historical scripts;
ignored outputs and environments are excluded by Git's file list. Ruff enables
E9 (syntax/runtime errors) and all F (Pyflakes defect checks, including unused
imports and undefined names). No formatting or autofixes. The sole F821 exception
is the undefined Path in preserved
`research/evidence/work-archive-2026-10-26/production_rea.py` (line 23); leave that
historical probe intact. Other undefined names fail.

The offline documentation adapter reuses the existing checker's path-like prose
rules, adds titled/angle links and reference definitions, and resolves against
tracked paths. No external URLs are fetched. Its
[exception list](scripts/doc-link-exceptions.json) specifies exact source/target
pairs and reasons, only for historical/local backtick prose. Markdown links
cannot use these exceptions. Existing raw link-checker diagnostics remain
available; its filesystem-dependent totals can differ from the CI adapter.
Fragment existence and full Markdown grammar are not validated.

A failed test, syntax, lint or link check needs investigation at the logged
file/test. A preservation mismatch is an evidence-integrity failure: never
regenerate the manifest or edit protected records merely to pass CI. The final
step in each job checks that research and wgrd_orders.py were not modified.
On GitHub, open the PR Checks tab (or Actions), select the failed job, then expand
the failed step. Unittest logs distinguish passes, failures and named skips;
a green test job does not establish private-corpus validation.

**Existing preservation discrepancy (2026-10-28):** main at f67f9ad fails three
entries: research/op0c_layout.py, research/op18_reference_keys.py, and
research/op18_supply_targets.py. Comparing manifest baseline 681d8ee with main
traces all three to commit
[24a1f5c](https://github.com/archpc/wgrd-replay/commit/24a1f5c61b540ed17b4ad0b77871ec1b5760e934):
Path imports and replacements of open(...).read() with Path(...).read_bytes(),
no other changes to these files. Consistent with deliberate file-handle cleanup;
explicit preservation authorization is not established by the commit alone.
The verifier intentionally remains failing pending a separate provenance decision.
This CI change neither edits those scripts nor normalizes their manifest hashes.
