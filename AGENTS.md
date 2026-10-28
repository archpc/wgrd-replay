# Working on wgrd-replay

A standard-library-only Python decoder for Wargame: Red Dragon `.wargamerpl2`
files. Parsing is strict; interpretation is partial and never asserts execution
success. Supported Python: 3.13–3.15.

## Start with the change

For ordinary code or documentation maintenance:

1. Use the [architecture change guide](docs/ARCHITECTURE.md#change-guide) to find
   the owning module and tests.
2. Read that code and its tests, then [CONTRIBUTING.md](CONTRIBUTING.md) for checks.
3. Read [FORMAT.md](FORMAT.md) if changing binary acceptance or output semantics.

The research archive is supporting material, not a prerequisite for editing a
function. Consult [research/INDEX.md](research/INDEX.md) when a change depends on
an uncertain field, a new layout or interpretation, or previous investigations.
[NEXT-STEPS.md](NEXT-STEPS.md) owns research priorities; historical plans are records.

## Compatibility and correctness

- Runtime and tests use Python's standard library. Do not add runtime dependencies.
- Preserve public APIs, CLI flags, output keys, ordering and raw-byte fields.
  Add semantic keys beside neutral fields rather than renaming them.
- Container violations raise `ReplayFormatError`. Malformed command blocks retain
  diagnostics; timeline export rejects them. Do not guess boundaries or truncate.
- Require exact command counts and byte consumption. A structural fit proves
  boundaries, not meaning. See [format](FORMAT.md) for accepted layouts.
- CLI JSON is strict: non-finite values use explicit `nonfinite` objects. Parser
  dictionaries may retain floats. Use the shared `wgrd_replay.json_safe` conversion.
- Preserve build qualifications and unknown outcomes. Verified layouts concern
  build 59638; other builds use inference. The controlled 131544 experiment is
  bounded evidence, not general gameplay validation.
- **Do not edit, move, reformat or delete the ASCII cow in `wgrd_orders.py`.**

## Verification

Run relevant tests while iterating, then the full suite and checks in
[CONTRIBUTING.md](CONTRIBUTING.md). Report actual results, interpreter and skips.
Missing private artifacts skip explicitly; the pinned public unit fixture is
required. A skip is unavailable coverage, not a pass. Available authenticated
samples should be checked for a parser change; compare outputs for a refactor.

CI checks code, explicit documentation links, archived source copies and the cow.
Maintained research code and notes are editable through normal review and tests.
Historical preservation manifests/verifiers are optional audit records, not
blanket immutability rules. Do not hand-edit generated coverage: regenerate using
[the owning scripts](docs/ARCHITECTURE.md#4-generated-files-and-their-scripts) and
explain material differences.

## When doing new format research

Search existing notes first; do not repeat completed analysis without a question.
State a falsifiable hypothesis. Separate observed bytes/control flow from proposed
meanings and state uncertainty where it matters. Follow the
[evidence conventions](docs/ARCHITECTURE.md#evidence-conventions).

Identify the executable build and SHA-256 before static analysis; never assume
the installed executable matches 59638. Cite addresses and excerpts or evidence
records, sample identity/hash, reproduction command and relevant tests. Hashes live
in [the binary inventory](samples/game-binaries.json) and sample manifests.
Preserve original captures and negative results; correct findings with dated notes
or explicit supersession. Update the current format/architecture reference and
index when a finding affects them. Keep bulk outputs in ignored `work/`.

## Workspace and artifacts

- Preserve existing work; use an isolated branch/workspace when requested.
  One writer per checkout. Review diffs and stage paths explicitly; no `git add .`
  or `git add -A`. Never force-push or rewrite published history. Verify remote
  SHAs after publication. Do not merge without authorization.
- Do not delete unrelated worktrees or research, reset work, or alter system
  permissions/security settings without explicit authorization.
- Never commit secrets, private player data, replay bytes, game binaries/assets
  or large dumps. External artifact paths and fixture variables are documented in
  [CONTRIBUTING.md](CONTRIBUTING.md).
- Replay bytes are untrusted: use the strict decoder; never evaluate their content.
  Executable analysis is static unless runtime work is explicitly authorized.
  A historical plan does not authorize launching the game or operating a VM.
