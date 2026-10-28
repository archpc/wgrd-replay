#!/usr/bin/env python3
"""Portable evidence checks; historical manifests remain unchanged.

Three exact script revisions from 24a1f5c replace their historical hashes.
Review rationale and original hashes: docs/DEVELOPMENT-REVIEW.md.
This checks records, archived copies and the cow, not arbitrary implementation
bytes or the existence of private, regenerable work/ outputs.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_HASHES = {
    'research/maintenance/preservation-manifest.json': '3b3d95a97e9bbecb189aaec6eb28ece6372e3f04d8d33fe6534b85b2e89adc31',
    'research/maintenance/work-artifacts-manifest.json': 'eb81b09c4db840b02594b5fb4501fb46e966208e042e28173e3f303d7f2d9cc6',
}
# Exact accepted revisions, not path-wide exemptions.
REVISIONS = {
    'research/op0c_layout.py': 'c23f4163d451b33dbd4579530b8a9402ed113d0df39183a4aac43f0d38cbbce0',
    'research/op18_reference_keys.py': '8150fa93f9b1da6b53cfd690bbb7faea98d3059cf51dd5cf402c6c47c94899ee',
    'research/op18_supply_targets.py': 'ec73dc092b2478752738e2957859715b83d3b537a8a431a3e0b5000cac390ee7',
}
COW_SHA256 = '0a13b78075453d2bc36bc9895e2a860138ddd5a5ce710ddc89f8966904cc7dc4'


def problems():
    bad = []
    manifests = []
    for path, expected in MANIFEST_HASHES.items():
        try:
            raw = (ROOT / path).read_bytes()
        except OSError as error:
            bad.append('%s: %s' % (path, error))
            continue
        if hashlib.sha256(raw).hexdigest() != expected:
            bad.append('historical manifest changed: ' + path)
        else:
            manifests.append(json.loads(raw))
    if len(manifests) != 2:
        return bad
    historical, work = manifests
    records = [(e.get('moved_to') or e['path'], REVISIONS.get(e['path'], e['sha256']),
                e['path'] in historical['allowed_changes']) for e in historical['entries']]
    records += [(e['copied_to'], e['sha256'], False) for e in work['entries'] if e.get('copied_to')]
    for path, expected, mutable in records:
        try:
            raw = (ROOT / path).read_bytes()
        except OSError as error:
            bad.append('%s: %s' % (path, error))
            continue
        if not mutable and hashlib.sha256(raw).hexdigest() != expected:
            bad.append('preserved file changed: ' + path)
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
    print('Preservation: historical records, archived copies, exact script revisions and cow; '
          + ('FAILED' if bad else 'OK'))
    return bool(bad)


if __name__ == '__main__':
    sys.exit(main())
