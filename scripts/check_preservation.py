#!/usr/bin/env python3
"""Check archived source copies and the cow; research code/docs stay editable.

Use the existing work-artifact inventory for archived-copy hashes. Git history
and regression tests cover maintained code and documents. Intentional inventory
updates receive ordinary diff review, without a separate approval mechanism.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COW_SHA256 = '0a13b78075453d2bc36bc9895e2a860138ddd5a5ce710ddc89f8966904cc7dc4'


def problems():
    bad = []
    inventory = ROOT / 'research/maintenance/work-artifacts-manifest.json'
    try:
        work = json.loads(inventory.read_text())
        records = [(e['copied_to'], e['sha256']) for e in work['entries'] if e.get('copied_to')]
        if not records:
            raise ValueError('no archived copies listed')
    except (OSError, ValueError, KeyError, TypeError) as error:
        return ['cannot read archive inventory: ' + str(error)]
    for path, expected in records:
        try:
            raw = (ROOT / path).read_bytes()
        except OSError as error:
            bad.append('%s: %s' % (path, error))
            continue
        if hashlib.sha256(raw).hexdigest() != expected:
            bad.append('archived source changed: ' + path)
    try:
        raw = (ROOT / 'wgrd_orders.py').read_bytes()
        cow = raw.split(b'    #   _____', 1)[1].split(b'    contextual =', 1)[0]
        if hashlib.sha256(cow).hexdigest() != COW_SHA256:
            bad.append('cow changed: wgrd_orders.py')
    except (OSError, IndexError):
        bad.append('cow missing: wgrd_orders.py')
    return bad


def main():
    bad = problems()
    for problem in bad:
        print(problem, file=sys.stderr)
    print('Archived copies and cow: '
          + ('FAILED' if bad else 'OK'))
    return bool(bad)


if __name__ == '__main__':
    sys.exit(main())
