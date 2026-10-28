#!/usr/bin/env python3
"""Fetch only existing hash-pinned public test inputs. Never execute downloaded code."""
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_unit_data import FILES  # noqa: E402


def main():
    destination = ROOT / 'work/public-units/wargame-data'
    manifest = json.loads((ROOT / 'research/public-unit-sources.json').read_text())
    records = {r['path']: r for r in manifest['files'] if r['repo'] == 'ResidentMario/wargame-data'}
    for name in FILES:
        record = records[name]
        target = destination / name
        if target.exists():
            data = target.read_bytes()
        else:
            print('Fetching pinned public fixture: ' + name, flush=True)
            with urllib.request.urlopen(record['url'], timeout=60) as response:
                data = response.read(record['size'] + 1)
        if len(data) != record['size'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('public fixture integrity mismatch: ' + name)
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        print('Verified: ' + name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
