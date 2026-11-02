#!/usr/bin/env python3
"""Check that the protected ASCII cow in wgrd_orders.py is byte-identical.

Retired research copies are verified in the external archive
(research/INDEX.md#archive), not in this repository.
"""
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COW_SHA256 = '0a13b78075453d2bc36bc9895e2a860138ddd5a5ce710ddc89f8966904cc7dc4'


def problems():
    try:
        raw = (ROOT / 'wgrd_orders.py').read_bytes()
        cow = raw.split(b'    #   _____', 1)[1].split(b'    contextual =', 1)[0]
    except (OSError, IndexError):
        return ['cow missing: wgrd_orders.py']
    if hashlib.sha256(cow).hexdigest() != COW_SHA256:
        return ['cow changed: wgrd_orders.py']
    return []


def main():
    bad = problems()
    for problem in bad:
        print(problem, file=sys.stderr)
    print('Cow: ' + ('FAILED' if bad else 'OK'))
    return bool(bad)


if __name__ == '__main__':
    sys.exit(main())
