#!/usr/bin/env python3
"""Report broken relative references in tracked Markdown files.

Checks two forms in every `git ls-files '*.md'` file:
  * relative markdown links: [text](path) (URL schemes, pure anchors, and
    absolute paths are skipped; #fragments and ?queries are stripped);
  * backtick spans that look like repo paths: contain '/' or end in
    .py/.md/.json/.txt/.gz, with no whitespace, and no glob/placeholder/home
    or variable syntax.

A target resolves if it exists relative to the referencing file OR relative
to the repository root. Missing targets are printed as file:line: target.
Exit status: 0 if none missing, 1 otherwise. A failed `git ls-files` also exits 1
(sys.exit with a message on stderr), not 2 as older text claimed.
Read-only; stdlib only. Run from any directory:
    python3 -B research/maintenance/check_links.py

Known limits (false negatives, not checked):
  * markdown links with a title, e.g. [t](path "title"), and angle-bracket targets
    [t](<path with spaces>) are not matched by LINK;
  * backtick spans containing whitespace are skipped entirely;
  * backtick spans with an anchor (`file.md#section`) are NOT stripped and are
    reported as missing;
  * only single-line link text is matched.
Reported findings can also be false positives: prose such as `verified/partial`
and paths that exist only in an uncommitted or external tree are reported as missing.

Baseline on 2026-10-28 at e01ac84: 31 "missing" lines (AGENTS.md cites 32).
A clean run is not proof of no broken links; classify each finding.

2026-10-28 checkout audit: 30 reports, all from backtick spans, not Markdown
links. Eight are repeated basenames of an external session dump in RECOVERED;
17 describe historical or local-only paths in WORK-ARTIFACTS; four describe
excluded runtime paths in the Sample1 README; one names the unavailable runtime
import in app-content/content/shared/README.md. The last is a real dependency
of that preserved source, not a self-contained module. The portable report build
is tracked separately. Counts depend on tracked files and local filesystem state.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?<![\w\]])\[[^\]]*\]\(([^)\s]+)\)")
SCHEMA = re.compile(r"^[a-z_]+/\d+$")  # e.g. wgrd_timeline/1: a version tag, not a path
TICK = re.compile(r"`([^`\n]+)`")
PATH_SUFFIXES = (".py", ".md", ".json", ".txt", ".gz")
SKIP_CHARS = set("*<>{}$~|")


def tracked_markdown():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True,
                         text=True, check=False)
    if out.returncode != 0:
        sys.exit("git ls-files failed: %s" % out.stderr.strip())
    return [ROOT / line for line in out.stdout.splitlines() if line]


def link_targets(line):
    for match in LINK.finditer(line):
        target = match.group(1)
        if "://" in target or target.startswith(("mailto:", "#", "/")):
            continue
        yield target.split("#", 1)[0].split("?", 1)[0]


def tick_targets(line):
    # ASCII WARNING: exit 0 covers only recognized forms, not the docstring's excluded cases.
    #      ____
    #     / ..  \  "0 missing" != "0 broken"
    #    |  --  |
    #     \____/
    for match in TICK.finditer(line):
        text = match.group(1)
        # Anchors are not stripped here (unlike link targets): `x.md#y` is checked as a file name.
        if any(c.isspace() for c in text) or SKIP_CHARS & set(text):
            continue
        if "://" in text or text.startswith("/") or SCHEMA.match(text):
            continue
        if "/" in text or text.endswith(PATH_SUFFIXES):
            yield text.rstrip("/")


def resolves(source, target):
    if not target:
        return True
    return (source.parent / target).exists() or (ROOT / target).exists()


def main():
    missing = []
    for md in tracked_markdown():
        lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
        for number, line in enumerate(lines, 1):
            for target in list(link_targets(line)) + list(tick_targets(line)):
                if target and not resolves(md, target):
                    missing.append((md.relative_to(ROOT).as_posix(), number, target))
    for path, number, target in missing:
        print("%s:%d: missing %s" % (path, number, target))
    print("checked markdown files; missing references: %d" % len(missing))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
