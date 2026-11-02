# Contributing

Use Python **3.13–3.15** from the repository root. Runtime and tests use only the
standard library; there is no package installation or mandatory formatter. The
[change guide](docs/ARCHITECTURE.md#change-guide) maps changes to modules and
tests. Read [FORMAT.md](FORMAT.md) before changing binary acceptance or output
semantics. [NEXT-STEPS.md](NEXT-STEPS.md) owns priorities.

## Rules

- **Do not edit, move, reformat or delete the ASCII cow in `wgrd_orders.py`.**
- Do not add runtime dependencies. Preserve public APIs, CLI flags, output keys,
  ordering and raw-byte fields. Add semantic keys beside neutral fields rather
  than renaming them.
- Container violations raise `ReplayFormatError`. Malformed command blocks keep
  their diagnostics, and timeline export rejects them. Require exact command
  counts and byte consumption; never guess boundaries or truncate. A structural
  fit proves boundaries, not meaning.
- CLI JSON is strict: non-finite values become explicit `nonfinite` objects via
  `wgrd_replay.json_safe`.
- Preserve build qualifications and unknown outcomes. Verified layouts apply to
  build 59638; other builds use inference.
- **Git:** use a focused branch, one writer per checkout, and explicit staging
  (no `git add .` or `-A`). Review the diff. Never force-push or rewrite
  published history, and do not merge without authorization.
- **Artifacts:** never commit secrets, private player data, replay bytes, game
  binaries or bulk dumps. Replay bytes are untrusted: use the strict decoder.
- **Runtime:** executable analysis is static unless runtime work is explicitly
  authorized. Notes and plans never authorize launching the game or operating a VM.

## Research

Search [the evidence index](research/INDEX.md) first; do not repeat completed
analysis without a new question. State a falsifiable hypothesis. Identify the
executable build and SHA-256 before static analysis, and never assume an
installed executable matches 59638. Cite addresses and bytes or evidence records,
sample hashes, the reproduction command and tests. Separate observations from
proposed meanings, following the
[evidence conventions](docs/ARCHITECTURE.md#evidence-conventions). Correct
findings with dated notes, then update FORMAT/architecture and the index. Keep
bulk outputs in the ignored `work/`. Retire research only into the verified
external archive ([research/INDEX.md](research/INDEX.md#archive)).

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

- **One module:** add `-p 'test_corpus.py'` to discovery.
- **CI:** full discovery on 3.13, 3.14 and 3.15, plus a quality job for syntax,
  Ruff (E9/F only), document links and the cow. Actions are SHA-pinned with
  read-only permissions, and each job checks that the tracked tree is unchanged.
- **Docs check:** validates explicit Markdown links relative to each document.
  It ignores code, prose paths, URLs and fragments. Stage new Markdown files
  before running it.
- **Reporting:** give the interpreter, actual results and skip reasons. A skip
  is missing coverage, not a pass. For a parser change, check the available
  authenticated samples. For a refactor, compare outputs.

The public unit fixture is mandatory: the fetcher verifies four pinned files.
Missing private replay or executable inputs skip explicitly; present but altered
inputs fail. A green public CI run does not validate private samples.

| Variable | External artifact | Default |
|---|---|---|
| `WGRD_SAMPLES_DIR` | Original samples, authenticated by [manifest](samples/manifest.json) | `~/.hermes/artifacts/wgrd-replay/samples/raw` |
| `WGRD_ARTIFACTS_DIR` | Cross-build replays in [manifest](samples/cross-build-manifest.json) | `~/.hermes/artifacts/wgrd-replay` |
| `WGRD_EXE_59638` | Historical executable for static checks | `~/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe` |
| `WGRD_UNIT_DATA` | Required pinned public fixture directory | `work/public-units/wargame-data` |
| `WGRD_CORPUS_DIR` | All 71 pinned archive replays in [offline corpus manifest](samples/offline-corpus-manifest.json) | Unset: private corpus tests skip; supplied missing/altered inputs fail |

The CLI's `--unit-data` is separate: the committed build-59638 index allows
offline enrichment without the public fixture.

## Where documentation goes

Usage goes in [docs/USAGE.md](docs/USAGE.md), wire layouts in
[FORMAT.md](FORMAT.md) and implementation/status contracts in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Evidence goes in
[research/](research/INDEX.md) and status in [NEXT-STEPS.md](NEXT-STEPS.md).
Link instead of duplicating. Do not hand-edit generated outputs; regenerate them
with [their scripts](docs/ARCHITECTURE.md#4-generated-files-and-their-scripts).
