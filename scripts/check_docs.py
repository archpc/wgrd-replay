#!/usr/bin/env python3
"""Check explicit Markdown links against tracked paths, offline.

Document-relative links, images and reference definitions are checked, including
angle targets and titles. Fenced/inline code, backtick prose, external URLs,
absolute paths and fragments are excluded. This is not a full Markdown parser.
The historical prose-path diagnostic remains in research/maintenance/check_links.py.
"""
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
# Also recognize angle targets, optional titles, images and reference definitions.
LINK = re.compile(r'(?<![\w\]])!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE = re.compile(r'^\s{0,3}\[[^\]]+\]:(?!:)\s*(?:<([^>]+)>|(\S+))')


def tracked_target(source, target, tracked):
    candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), target)).rstrip('/')
    return candidate in tracked or any(p.startswith(candidate + '/') for p in tracked)


def check_line(source, line, tracked, exceptions=None):
    # Backtick prose is not a link. Retain the optional fourth argument for callers.
    line = re.sub(r"(`+).*?\1", "", line)
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
    return missing


def main():
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    tracked = set(filter(None, paths))
    missing = []
    count = 0
    for source in sorted(p for p in tracked if p.endswith('.md')):
        count += 1
        fence = None
        for number, line in enumerate((ROOT / source).read_text(encoding='utf-8').splitlines(), 1):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if marker:
                token = marker.group(1)
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence):
                    fence = None
                continue
            if fence is not None:
                continue
            for target in check_line(source, line, tracked):
                missing.append('%s:%d: missing %s' % (source, number, target))
    for finding in missing:
        print(finding)
    print('Documentation: %d tracked Markdown files; %d missing links' % (count, len(missing)))
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
