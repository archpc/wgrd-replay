# Contributing

Use Python **3.13–3.15** from the repository root. Runtime and tests use only the
standard library; there is no package installation or mandatory formatter.
[The change guide](docs/ARCHITECTURE.md#change-guide) maps changes to modules and tests;
[AGENTS.md](AGENTS.md) records repository operating rules.

## Change boundaries

- Use a focused branch, preserve unrelated work, stage paths explicitly, review
  the diff, and never force-push over concurrent work.
- Preserve public APIs, CLI flags, JSON keys, raw bytes, ordering, exact consumption
  and build qualifications. Reproduce decoder bugs with synthetic fixtures; compare
  outputs on authenticated samples for a refactor.
- Leave the ASCII cow in `wgrd_orders.py` byte-for-byte unchanged.
- Preserve historical evidence and negative results. Add dated corrections and
  update the current reference; do not hand-edit generated coverage JSON.

For research, search [the index](research/INDEX.md) first. State a falsifiable
claim, identify executable and sample hashes, cite addresses/bytes, add a failing
reproducer and tests, then update [FORMAT.md](FORMAT.md) or
[architecture](docs/ARCHITECTURE.md). Follow its
[evidence conventions](docs/ARCHITECTURE.md#evidence-conventions).
Keep game binaries, replay bytes, private metadata and bulk dumps outside Git.
VM/game operation requires explicit authorization; historical plans do not grant it.

## Test and verify

```sh
python3 -B scripts/fetch_public_fixture.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_python.py
python3 -m pip install --no-deps ruff==0.14.2
git ls-files -z '*.py' | xargs -0 python3 -m ruff check --force-exclude
python3 -B scripts/check_docs.py
python3 -B scripts/check_preservation.py
git diff --check
```

Use `-p 'test_corpus.py'` with discovery for one test module. CI runs full discovery
on 3.13, 3.14 and 3.15, plus one quality job for syntax, Ruff, links and preservation.
Actions are SHA-pinned, permissions read-only, credentials not persisted, and
jobs bounded by timeouts. Each job checks that it left the tracked tree unchanged.
Ruff checks E9/F defects without formatting; one archived probe has a documented
F821 exception in [ruff.toml](ruff.toml).

The public unit test fixture is mandatory: the fetcher verifies four pinned
files and fails on download/checksum errors. Cached inputs are rechecked.
Missing private replay/executable tests skip explicitly; present altered evidence
fails. A green public CI run does not validate private samples.

| Variable | External artifact | Default |
|---|---|---|
| `WGRD_SAMPLES_DIR` | Original samples, authenticated by [manifest](samples/manifest.json) | `~/.hermes/artifacts/wgrd-replay/samples/raw` |
| `WGRD_ARTIFACTS_DIR` | Cross-build replays in [manifest](samples/cross-build-manifest.json) | `~/.hermes/artifacts/wgrd-replay` |
| `WGRD_EXE_59638` | Historical executable for static checks | `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe` |
| `WGRD_UNIT_DATA` | Required pinned public fixture directory | `work/public-units/wargame-data` |

The CLI's `--unit-data` is separate: the committed build-59638 index allows offline
enrichment without the public fixture. Run summary/timeline exports on an available
authenticated replay using [usage examples](docs/USAGE.md). Report the interpreter,
actual test results, skip reasons, available corpus, and validation limits.

## Documentation and preservation

Keep usage in [the usage guide](docs/USAGE.md), wire layouts in
[FORMAT.md](FORMAT.md), implementation/status contracts in
[architecture](docs/ARCHITECTURE.md), and historical investigations in
[research](research/INDEX.md). Link explanations instead of duplicating them.

The offline link check validates explicit Markdown links against tracked paths,
relative to each document. It ignores code examples, prose paths, external URLs
and fragments; it is not a full Markdown parser. Stage new Markdown paths
explicitly before running it. The old prose-path diagnostic remains available at
`research/maintenance/check_links.py`; its warnings are not CI failures.

The portable preservation check covers archived source copies and the cow.
Maintained research scripts and notes are editable: use normal review and
regression tests, with Git history retaining earlier versions. Intentional archive
or inventory changes receive ordinary diff review. Preserve original observations
when adding corrections; no special hash-waiver process is required.

Historical manifests/verifiers remain available as optional audit records, not
CI requirements. They can report old script mismatches or absent private `work/`
outputs. The [maintenance review](docs/DEVELOPMENT-REVIEW.md#repository-rationalization-2026-10-28)
records why the old blanket freeze was retired.
