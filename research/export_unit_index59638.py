"""Export original59638 static mappings + matching US unit dictionary, offline.

Inputs opened read-only. Output is a compact local index, not a repacked game file.
Objects come from ndf59638_parse.py after ndf59638_unpack.py; hashes recorded.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_unit_index import export_index, canonical_bytes, parse_dictionary, load_index

LOCALE_SHA1 = '743a93ec96fc3f90caab466cd9ebe60b8c7b24b2'
LOCALE_MEMBER = 'pc\\localisation\\us\\localisation\\unites.dic'


def authenticate_objects(objects, expanded, record):
    if hashlib.sha256(objects).hexdigest() != record['objects_sha256']:
        raise ValueError('parsed objects hash mismatch')
    if hashlib.sha256(expanded).hexdigest() != record['expanded_sha256']:
        raise ValueError('parsed objects expanded-source hash mismatch')


def read_dictionary_archive(path):
    blob = Path(path).read_bytes()
    if len(blob) != 1875968 or hashlib.sha1(blob).hexdigest() != LOCALE_SHA1:
        raise ValueError('localization archive differs from pinned59638 depot manifest')
    if blob[:8] != b'edat\x02\0\0\0': raise ValueError('invalid EDAT header')
    doff, dsize, boff, bsize = struct.unpack_from('<4I', blob, 25)
    if doff+dsize > len(blob) or boff+bsize > len(blob): raise ValueError('EDAT bounds')
    if hashlib.md5(blob[doff:doff+dsize]).digest() != blob[49:65]: raise ValueError('EDAT dictionary checksum')
    if blob[doff:doff+10] != b'\x0a\0\0\0'+b'\0'*6: raise ValueError('EDAT root')
    entries = {}
    def walk(p, end, prefix):
        while p < end:
            start = p
            if p+8 > end: raise ValueError('truncated EDAT node')
            span, total = struct.unpack_from('<2I', blob, p); p += 8
            stop = start+total if total else end
            if not p <= stop <= end: raise ValueError('EDAT node bounds')
            if span:
                z = blob.index(b'\0', p, stop); part = blob[p:z].decode('utf-8'); p = z+1+(z+1-p)%2
                if p != start+span: raise ValueError('EDAT directory span')
                walk(p, stop, prefix+part); p = stop
            else:
                if p+32 > stop: raise ValueError('truncated EDAT file')
                off, pad, size, pad2 = struct.unpack_from('<4I', blob, p)
                md5 = blob[p+16:p+32].hex(); p += 32
                z = blob.index(b'\0', p, stop); part = blob[p:z].decode('utf-8'); p = z+1+(z+1-p)%2
                name = prefix+part
                if p != stop or pad or pad2 or off+size > bsize or name in entries:
                    raise ValueError('invalid EDAT file')
                entries[name] = {'offset': boff+off, 'size': size, 'md5': md5}
        if p != end: raise ValueError('EDAT consumption')
    walk(doff+10, doff+dsize, '')
    entry = entries[LOCALE_MEMBER]
    raw = blob[entry['offset']:entry['offset']+entry['size']]
    if hashlib.md5(raw).hexdigest() != entry['md5']: raise ValueError('dictionary member checksum')
    source = {'locale': 'us', 'archive_path': 'Data/WarGame/PC/59095/59638/ZZ_Win.dat',
              'archive_size': len(blob), 'archive_sha1': LOCALE_SHA1,
              'archive_sha256': hashlib.sha256(blob).hexdigest(),
              'depot_id': '251062', 'manifest_id': '7569342467126442184',
              'member': {'path': LOCALE_MEMBER, **entry}, 'dictionary_sha256': hashlib.sha256(raw).hexdigest(),
              'format': 'TRAD/raw8-token/u32-byte-offset/u32-UTF16-code-unit-count',
              'lookup': 'exact_raw_token_bytes', 'overlay': '59638 member only; all exported tokens present; no older/newer dictionary merge',
              'format_sources': ['research/ndf59638-format-sources.json',
                                'https://github.com/fmdostoyevskiy/wgrd-toolbox/blob/69b0b662fd6aa799474432d2391e7ececcf8a44f/scripts/extract.py'],
              'format_source_manifest': 'research/public-unit-sources.json'}
    return parse_dictionary(raw), source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--objects', type=Path, default=ROOT/'work/ndf59638/objects.json')
    parser.add_argument('--expanded', type=Path, default=ROOT/'work/ndf59638/everything.expanded.ndfbin')
    parser.add_argument('--ndf-archive', type=Path, default=Path.home()/'.hermes/artifacts/wgrd-replay/game/win64/Data/WarGame/PC/59638/NDF_Win.dat')
    parser.add_argument('--localization-archive', type=Path, default=ROOT/'work/localization59638/download/Data/WarGame/PC/59095/59638/ZZ_Win.dat')
    parser.add_argument('--output', type=Path, default=ROOT/'research/unit-data/build59638-v1.json.gz')
    parser.add_argument('--manifest', type=Path, default=ROOT/'research/unit-data/build59638-v1.manifest.json')
    args = parser.parse_args()
    extraction = json.loads((ROOT/'research/ndf59638-extraction.json').read_text())['unpack']
    archive = args.ndf_archive.read_bytes(); expanded = args.expanded.read_bytes(); objects = args.objects.read_bytes()
    if hashlib.sha256(archive).hexdigest() != extraction['archive_sha256']:
        raise ValueError('NDF archive hash mismatch')
    if hashlib.sha256(expanded).hexdigest() != extraction['expanded_sha256']:
        raise ValueError('expanded NDF hash mismatch')
    artifacts = json.loads((ROOT/'research/unit-data/source-artifacts.json').read_text())
    authenticate_objects(objects, expanded, artifacts)
    source = {'ndf': extraction, 'parsed_objects_sha256': hashlib.sha256(objects).hexdigest(),
              'parsed_artifact_provenance': artifacts,
              'research': ['research/NDF59638-BRIDGE.md', 'research/ndf59638-extraction.json',
                           'research/ndf59638-bridge-coverage.json', 'research/ndf59638_parse.py',
                           'research/export_unit_index59638.py'],
              'node_properties': 'mapping and naming projection only; offsets absolute in authenticated expanded NDF',
              'bridge': 'explicit CompanyUnit slot -> selector Default -> CompanyDescriptor; inverse retained as candidate arrays',
              'direct': 'TUniteAuSolDescriptor exact GUID only; no GUID edits or debug-name joins'}
    names, localization = read_dictionary_archive(args.localization_archive)
    index = export_index(json.loads(objects), source, names, localization)
    payload = canonical_bytes(index)
    raw = gzip.compress(payload, mtime=0) if args.output.suffix == '.gz' else payload
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_bytes(raw)
    load_index(args.output)
    manifest = {'schema': 'wgrd_unit_index_export/1', 'game_build': '59638', 'index_schema': index['schema'],
                'index_sha256': hashlib.sha256(raw).hexdigest(), 'index_size': len(raw),
                'canonical_json_sha256': hashlib.sha256(payload).hexdigest(), 'canonical_json_size': len(payload),
                'source': source, 'localization': localization,
                'counts': {'source_descriptors': len(index['descriptors']), 'configured_unit_types': len(index['unit_types']),
                           'projected_nodes': len(index['nodes']), 'name_tokens': len(index['names']),
                           'unit_types_with_unique_localized_name': sum(len(index['names'].get(u['name_token'], [])) == 1 for u in index['unit_types'].values())}}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: manifest[k] for k in ('index_sha256', 'index_size', 'counts')}, sort_keys=True))


if __name__ == '__main__': main()
