#!/usr/bin/env python3
"""Compile every tracked Python file without importing it or writing bytecode."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def check_files(paths):
    ok = True
    for path in paths:
        try:
            compile(path.read_bytes(), str(path), 'exec')
        except (SyntaxError, ValueError) as error:
            print(str(error), file=sys.stderr)
            ok = False
    return ok


def main():
    paths = subprocess.check_output(['git', 'ls-files', '-z', '*.py'], cwd=ROOT).split(b'\0')
    files = [ROOT / path.decode() for path in paths if path]
    ok = check_files(files)
    print('Python syntax: %d tracked files; %s' % (len(files), 'OK' if ok else 'FAILED'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
