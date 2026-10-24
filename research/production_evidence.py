"""Capture read-only native Rizin evidence for production decoder build 59638.

No target execution or source changes. Rizin's PE loader maps virtual addresses.
Output is an inspectable native evidence record, not an REA evidence envelope.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

SHA256 = '1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46'
RANGES = [
    ('creator', 'pD 0x9e @ 0xb2fea0; pD 0x120 @ 0xb28ef0; pxw 0x68 @ 0x19b0180; pxw 0x64 @ 0x19a18e0'),
    ('serializer', 'pD 0x220 @ 0xb584e0; pD 0x80 @ 0xb57f80; pD 0x140 @ 0xb580a0; pD 0x80 @ 0xb599a0; pD 0x20 @ 0xb589a0; pD 0x230 @ 0xb5abf0'),
    ('fields', 'pD 0x70 @ 0xb53df0; pD 0x120 @ 0xc0fad0; pD 0x70 @ 0xc0f530; pD 0x180 @ 0xc06ba0; pD 0x150 @ 0xc06070; pD 0x150 @ 0xc061f0; pD 0x1c0 @ 0xc069a0'),
    ('references', 'pD 0x70 @ 0xb074c0; pD 0x90 @ 0xbd01e0; pD 0xc8 @ 0xa66fc0; pD 0x20 @ 0x4f71d0; pD 0x20 @ 0xb5abd0; pD 0x70 @ 0xb5a630'),
    ('execution', 'pD 0x30 @ 0xb2d0a0; pD 0x70 @ 0xba5520; pD 0x3d0 @ 0xc09820; pD 0x250 @ 0xc095d0; pD 0x70 @ 0xc0ce90; pD 0x1a0 @ 0xc0b190; pD 0x110 @ 0xc0b40b; pD 0x50 @ 0xbcdcd0'),
    ('cancellation', 'pD 0x50 @ 0xb2c410; pD 0xe0 @ 0xb2e870; pD 0xc0 @ 0xb246b0; pD 0x10 @ 0xc182a0; pD 0x30 @ 0xba6310; pD 0x130 @ 0xba5990; pD 0x70 @ 0xb2c390; pD 0xe8 @ 0xb245c0'),
]


def capture(binary, rizin):
    before = hashlib.sha256(binary.read_bytes()).hexdigest()
    if before != SHA256: raise ValueError('executable hash mismatch')
    version = subprocess.run([rizin, '-v'], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    records = []
    for label, command in RANGES:
        command = 'e scr.color=0; '+command
        args = [rizin, '-N', '-q', '-c', command, str(binary)]
        result = subprocess.run(args, capture_output=True, text=True, timeout=60, check=True)
        records.append({'label': label, 'arguments': args, 'stdout': result.stdout,
                        'stderr': result.stderr, 'exit_code': result.returncode})
    after = hashlib.sha256(binary.read_bytes()).hexdigest()
    if before != after: raise ValueError('executable changed')
    return {'schema': 'wgrd_native_evidence/1', 'subject': {'sha256': before, 'path': str(binary)},
            'provider': version, 'artifact_changed': False, 'records': records,
            'limitations': ['Static native disassembly only; no runtime observations.',
                            'REA MCP wrapper failed to launch provider; native Rizin used directly.',
                            'Range endpoints may end within padding or a following instruction.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, default=Path.home()/'.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe')
    parser.add_argument('--rizin', default='/opt/homebrew/bin/rizin')
    args = parser.parse_args()
    print(json.dumps(capture(args.binary, args.rizin), indent=2))
