#!/usr/bin/env python3
"""Offline CI adapter for the existing link checker; exact historical prose exceptions.

Resolve against Git-tracked paths, including directories, not a developer's work/.
Retain the legacy root-relative fallback. Exceptions cover backtick prose only;
Markdown links and reference definitions always have to resolve. No network calls.
"""
import importlib.util
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('legacy_links', ROOT / 'research/maintenance/check_links.py')
legacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(legacy)
# Also recognize angle targets, optional titles, images and reference definitions.
LINK = re.compile(r'(?<![\w\]])!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE = re.compile(r'^\s{0,3}\[[^\]]+\]:(?!:)\s*(?:<([^>]+)>|(\S+))')


def tracked_target(source, target, tracked):
    for candidate in (posixpath.join(posixpath.dirname(source), target), target):
        candidate = posixpath.normpath(candidate).rstrip('/')
        if candidate in tracked or any(p.startswith(candidate + '/') for p in tracked):
            return True
    return False


def check_line(source, line, tracked, exceptions):
    missing = []
    links = [m.group(1) or m.group(2) for m in LINK.finditer(line)]
    reference = REFERENCE.match(line)
    if reference:
        links.append(reference.group(1) or reference.group(2))
    for target in links:
        if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith(('#', '/')):
            continue
        target = unquote(target.split('#', 1)[0].split('?', 1)[0])
        if target and not tracked_target(source, target, tracked):
            missing.append(target)
    for target in legacy.tick_targets(line):
        if not tracked_target(source, target, tracked) and (source, target) not in exceptions:
            missing.append(target)
    return missing


def main():
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    tracked = set(filter(None, paths))
    records = json.loads((ROOT / 'scripts/doc-link-exceptions.json').read_text())
    exceptions = {}
    for row in records:
        key = (row['source'], row['target'])
        if not row['reason'].strip() or key in exceptions or row['source'] not in tracked:
            raise ValueError('invalid or duplicate documentation exception: ' + repr(row))
        exceptions[key] = row['reason']
    missing = []
    count = 0
    for source in sorted(p for p in tracked if p.endswith('.md')):
        count += 1
        for number, line in enumerate((ROOT / source).read_text(encoding='utf-8').splitlines(), 1):
            for target in check_line(source, line, tracked, exceptions):
                missing.append('%s:%d: missing %s' % (source, number, target))
    for finding in missing:
        print(finding)
    print('Documentation: %d tracked Markdown files; %d exact prose exceptions; %d missing references'
          % (count, len(exceptions), len(missing)))
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
