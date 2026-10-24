"""Read-only playback prerequisites census. No download, installation or execution.

Prints JSON to stdout. Cached Steam manifest supplies expectations, not proof of
the actual runtime file-open set. Candidate assets are a conservative selection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import struct

BINARY_SHA256 = '1c7533eb5387a3e82db66595c782f23c20f5871250d6b6a24d630b9d074bda46'
MANIFEST_SHA256 = '09747c171db5743e2ad8b5bcd52d0369ae2ff91f5856960ea56676e749c5510c'


def varint(blob, offset):
    value = shift = 0
    while offset < len(blob) and shift <= 63:
        byte = blob[offset]; offset += 1; value |= (byte & 127) << shift
        if byte < 128: return value, offset
        shift += 7
    raise ValueError('invalid protobuf varint')


def fields(blob):
    p = 0
    while p < len(blob):
        tag, p = varint(blob, p); number, kind = tag >> 3, tag & 7
        if kind == 0: value, p = varint(blob, p)
        elif kind in (1, 2, 5):
            if kind == 2: size, p = varint(blob, p)
            else: size = 8 if kind == 1 else 4
            value = blob[p:p+size]
            if len(value) != size: raise ValueError('truncated protobuf field')
            p += size
        else: raise ValueError('unsupported protobuf field')
        yield number, value


def manifest_entries(blob):
    if hashlib.sha256(blob).hexdigest() != MANIFEST_SHA256: raise ValueError('manifest hash mismatch')
    magic, size = struct.unpack_from('<II', blob)
    if magic != 0x71f617d0: raise ValueError('manifest payload header')
    payload = blob[8:8+size]
    magic, size2 = struct.unpack_from('<II', blob, 8+size)
    if magic != 0x1f4812be: raise ValueError('manifest metadata header')
    meta = dict(fields(blob[16+size:16+size+size2]))
    if (meta[1], meta[2], meta[4]) != (251062, 7569342467126442184, 0):
        raise ValueError('unexpected depot/manifest/encryption')
    entries = []
    for number, value in fields(payload):
        if number != 1: continue
        entry = {k: v for k, v in fields(value) if k != 6}
        if entry.get(3, 0) & 64: continue
        entries.append({'path': entry[1].decode('utf-8').rstrip('\0').replace('\\', '/'),
                        'size': entry[2], 'content_sha1': entry[5].hex()})
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root', type=Path, default=Path.home()/'.hermes/artifacts/wgrd-replay/game/win64')
    args = parser.parse_args(); root = args.game_root
    binary = root/'Data/PC/59638/WarGame3.exe'; raw = binary.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BINARY_SHA256: raise ValueError('matching executable hash mismatch')
    manifest = root/'.DepotDownloader/251062_7569342467126442184.manifest'
    entries = manifest_entries(manifest.read_bytes())
    names = {'Data.dat', 'DataMap.dat', 'ZZ_1.dat', 'ZZ_2.dat', 'ZZ_3a.dat',
             'ZZ_3b.dat', 'ZZ_4.dat', 'ZZ_Win.dat', '_2x3_Tohoku_v11.dat'}
    versions = {'48574', '49125', '49964', '58710', '59095', '59638'}
    selected = []
    for entry in entries:
        parts = entry['path'].split('/'); take = False
        if parts[:4] == ['Data', 'WarGame', 'PC', '48574'] and len(parts) == 5:
            take = parts[-1] in names
        if parts[:3] == ['Data', 'WarGame', 'PC'] and len(parts) == 6:
            take = parts[3] in versions and parts[4] in versions and parts[-1] in names
        if entry['path'] in {'Data/WarGame/PC/59638/NDF_Win.dat',
                             'Maps/WarGame/PC/_2x3_Tohoku_v11.dat',
                             'Data/PC/59638/WarGame3.exe', 'Data/PC/59638/steam_api.dll',
                             'Data/PC/59638/atimgpud.dll'}: take = True
        if take:
            path = root/entry['path']; record = {**entry, 'present_in_game_tree': path.is_file()}
            if path.is_file():
                actual = path.read_bytes()
                record['local_size'] = len(actual)
                record['content_sha1_matches'] = hashlib.sha1(actual).hexdigest() == entry['content_sha1']
            selected.append(record)
    applications = []
    for directory in (Path('/Applications'), Path.home()/'Applications'):
        if directory.is_dir():
            applications += [str(p) for p in directory.iterdir()
                             if any(n in p.name.lower() for n in ('steam', 'wine', 'cross', 'whisky', 'parallels', 'vmware', 'utm', 'wargame'))]
    report = {'schema': 'wgrd_runtime59638_prerequisites/1',
        'host': {'os': platform.system(), 'architecture': platform.machine()},
        'binary': {'path': str(binary), 'size': len(raw), 'sha256': BINARY_SHA256,
                   'format': 'PE32/i386; Windows GUI; original bytes only'},
        'manifest': {'path': str(manifest), 'sha256': MANIFEST_SHA256, 'depot': 251062,
                     'id': '7569342467126442184', 'files': len(entries), 'logical_bytes': sum(e['size'] for e in entries),
                     'signature_revalidated': False},
        'runtime_tools_on_path': {n: shutil.which(n) for n in ('wine', 'wine64', 'wine32', 'qemu-system-x86_64', 'prlctl', 'vmrun', 'VBoxManage', 'lldb', 'rizin')},
        'matching_app_names_in_checked_roots': applications,
        'checked_steamapps_path': str(Path.home()/'Library/Application Support/Steam/steamapps'),
        'checked_steamapps_exists': (Path.home()/'Library/Application Support/Steam/steamapps').exists(),
        'sample1_asset_candidates': sorted(selected, key=lambda e: e['path']),
        'candidate_count': len(selected), 'candidate_logical_bytes': sum(e['size'] for e in selected),
        'candidate_missing_from_game_tree': sum(not e['present_in_game_tree'] for e in selected),
        'limitations': ['Candidate asset set is not a proven minimum or sufficient install; runtime file opens and patch selection not observed.',
                        'Full cached depot also contains later builds; whole-depot size is not a59638 minimum.',
                        'Localization archive exists separately in project work/; not staged into original game tree.',
                        'PATH/application-root checks do not exclude unindexed tools, external installs or remote Windows hosts.'],
        'game_execution_attempted': False, 'downloads_or_installs_attempted': False}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__': main()
