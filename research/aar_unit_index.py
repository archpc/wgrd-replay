"""Build-131544 native NDF descriptor index and static replay GUID joins.

Read-only research tool. It authenticates one exact NDF archive, extracts the
single ``everything.ndfbin`` member, decodes the CNDF object/property tables with
the same minimal reader used for build 59638, and projects a descriptor index.
A replay join compares the 16-byte validation GUID from a 0x07 wire reference
against ``DescriptorId`` bytes only.

!! TRAP: a GUID-type match is not live entity identity. It does not prove the
!! server accepted an object, that a company was deployed, that a module was
!! active, or that a member is present at any frame. Selector conditions are
!! retained as data and are never evaluated.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wgrd_replay import ReplayFormatError, parse_replay
# Reuse the 59638 chain projection rather than re-writing its graph walk.
from wgrd_unit_index import UNIT_CLASSES, _derive, _refs

BUILD = '131544'
SCHEMA = 'aar_unit_index/1'
ARCHIVE_SHA256 = '172e481d80b4e07c057b43b758191e389e5f79b34d0e566357f768a1e2be151b'
ARCHIVE_SIZE = 24281088
EVERYTHING_SUFFIX = 'everything.ndfbin'
ENTRY_MD5 = '0f653347ca8b414c48162e294360810a'

# Value type table observed across the 131544 everything.ndfbin; unknown types
# raise instead of guessing a length. Types 0x1f/0x21 are EugInt2/EugFloat2.
_RAW_WIDTHS = {12: 16, 26: 16, 29: 8}
_SCALARS = {0: '<?', 1: '<B', 2: '<i', 3: '<I', 5: '<f', 6: '<d', 24: '<h', 25: '<H'}
_NULL_TYPES = (0xffffffff, 0xeeeeeeee)


class _Reader:
    def __init__(self, data):
        self.b = data
        self.p = 0

    def take(self, size):
        if not 0 <= size <= len(self.b)-self.p:
            raise ReplayFormatError('truncated NDF block at 0x%x (want %d)' % (self.p, size))
        out = self.b[self.p:self.p+size]
        self.p += size
        return out

    def num(self, fmt):
        return struct.unpack(fmt, self.take(struct.calcsize(fmt)))[0]

    def u32(self):
        return self.num('<I')

    def string(self):
        raw = self.take(self.u32())
        try:
            return raw.decode('latin1')
        except UnicodeError as error:
            raise ReplayFormatError('invalid NDF table string') from error


def _sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def authenticate_archive(blob, expected_sha256=ARCHIVE_SHA256, expected_size=ARCHIVE_SIZE):
    """Fail closed unless the exact 131544 archive bytes are supplied."""
    digest = _sha256(blob)
    if len(blob) != expected_size or digest != expected_sha256:
        raise ReplayFormatError(
            'NDF archive is not the pinned 131544 source: size %d (want %d), sha256 %s (want %s)'
            % (len(blob), expected_size, digest, expected_sha256))
    return {'sha256': digest, 'size': len(blob)}


def read_edat(blob):
    """Walk the EDAT dictionary used by Data/WarGame/PC/<build>/NDF_Win.dat."""
    if len(blob) < 65 or blob[:8] != b'edat\x02\0\0\0':
        raise ReplayFormatError('invalid EDAT header')
    doff, dsize, boff, bsize = struct.unpack_from('<4I', blob, 25)
    if doff+dsize > len(blob) or boff+bsize > len(blob) or doff < 65:
        raise ReplayFormatError('EDAT dictionary outside file')
    if hashlib.md5(blob[doff:doff+dsize]).digest() != blob[49:65]:
        raise ReplayFormatError('EDAT dictionary checksum mismatch')
    if blob[doff:doff+10] != b'\x0a\0\0\0'+b'\0'*6:
        raise ReplayFormatError('unexpected EDAT root record')
    entries = {}

    def walk(p, end, prefix, depth):
        if depth > 64:
            raise ReplayFormatError('EDAT directory nesting too deep')
        while p < end:
            start = p
            if p+8 > end:
                raise ReplayFormatError('truncated EDAT node')
            span, total = struct.unpack_from('<2I', blob, p)
            p += 8
            stop = start+total if total else end
            if not p <= stop <= end:
                raise ReplayFormatError('EDAT node bounds')
            if span:
                zero = blob.find(b'\0', p, stop)
                if zero < 0:
                    raise ReplayFormatError('unterminated EDAT directory name')
                part = blob[p:zero].decode('utf-8')
                p = zero+1+(zero+1-p) % 2
                if p != start+span:
                    raise ReplayFormatError('EDAT directory span mismatch')
                walk(p, stop, prefix+part, depth+1)
                p = stop
            else:
                if p+32 > stop:
                    raise ReplayFormatError('truncated EDAT file record')
                offset, pad, size, pad2 = struct.unpack_from('<4I', blob, p)
                md5 = blob[p+16:p+32].hex()
                p += 32
                zero = blob.find(b'\0', p, stop)
                if zero < 0:
                    raise ReplayFormatError('unterminated EDAT file name')
                part = blob[p:zero].decode('utf-8')
                p = zero+1+(zero+1-p) % 2
                name = prefix+part
                if p != stop or pad or pad2 or boff+offset+size > len(blob):
                    raise ReplayFormatError('invalid EDAT file record')
                if name in entries:
                    raise ReplayFormatError('duplicate EDAT member '+name)
                entries[name] = {'offset': boff+offset, 'size': size, 'md5': md5}
        if p != end:
            raise ReplayFormatError('EDAT node consumption mismatch')

    walk(doff+10, doff+dsize, '', 0)
    return entries


def extract_everything(blob):
    """Return the single expanded everything.ndfbin payload plus provenance."""
    entries = read_edat(blob)
    hits = [name for name in entries if name.lower().endswith(EVERYTHING_SUFFIX)]
    if len(hits) != 1:
        raise ReplayFormatError('expected exactly one everything.ndfbin member, found %d' % len(hits))
    name = hits[0]
    entry = entries[name]
    raw = blob[entry['offset']:entry['offset']+entry['size']]
    if hashlib.md5(raw).hexdigest() != entry['md5']:
        raise ReplayFormatError('everything.ndfbin member checksum mismatch')
    if raw[:4] != b'EUG0' or raw[8:12] != b'CNDF':
        raise ReplayFormatError('unexpected ndfbin container magic')
    flag = struct.unpack_from('<I', raw, 12)[0]
    declared_total = struct.unpack_from('<I', raw, 32)[0]
    declared_body = struct.unpack_from('<I', raw, 40)[0]
    if flag not in (0, 128):
        raise ReplayFormatError('unsupported ndfbin compression flag %d' % flag)
    if flag == 128:
        decoder = zlib.decompressobj()
        body = decoder.decompress(raw[44:])+decoder.flush()
        if decoder.unused_data or decoder.unconsumed_tail:
            raise ReplayFormatError('compressed ndfbin has trailing/unconsumed input')
        zlib_eof = decoder.eof
    else:
        body = raw[40:]
        zlib_eof = None
    if len(body) != declared_body:
        raise ReplayFormatError('expanded body length %d != declared %d' % (len(body), declared_body))
    expanded = raw[:40]+body
    if len(expanded) != declared_total:
        raise ReplayFormatError('expanded file length %d != declared %d' % (len(expanded), declared_total))
    source = {'member': name, 'entry_offset': entry['offset'], 'entry_size': entry['size'],
              'entry_md5': entry['md5'], 'entry_sha256': _sha256(raw),
              'expanded_size': len(expanded), 'expanded_sha256': _sha256(expanded),
              'compression_flag': flag, 'zlib_eof_marker': zlib_eof,
              'declared_total_size': declared_total, 'declared_body_size': declared_body}
    return expanded, source


def _strings(reader):
    values = []
    while reader.p < len(reader.b):
        values.append(reader.string())
    return values


def _all_refs(value):
    """Yield object-reference dicts including explicit null references."""
    if isinstance(value, dict):
        if 'ref_index' in value:
            yield value
        else:
            for item in value.values():
                yield from _all_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from _all_refs(item)


def _blocks(expanded):
    if expanded[:4] != b'EUG0' or expanded[8:12] != b'CNDF':
        raise ReplayFormatError('expanded payload is not CNDF')
    if len(expanded) < 40:
        raise ReplayFormatError('truncated CNDF header')
    toc = struct.unpack_from('<I', expanded, 16)[0]
    if not 40 <= toc <= len(expanded)-8 or expanded[toc:toc+4] != b'TOC0':
        raise ReplayFormatError('invalid CNDF TOC')
    count = struct.unpack_from('<I', expanded, toc+4)[0]
    if toc+8+24*count != len(expanded):
        raise ReplayFormatError('CNDF TOC length mismatch')
    blocks = {}
    for index in range(count):
        p = toc+8+24*index
        name = expanded[p:p+4].decode('latin1')
        offset, size = struct.unpack_from('<QQ', expanded, p+8)
        if name in blocks:
            raise ReplayFormatError('duplicate CNDF block '+name)
        if offset < 40 or offset+size > toc:
            raise ReplayFormatError('CNDF block outside body: '+name)
        blocks[name] = (offset, size)
    ordered = sorted(blocks.values())
    end = 40
    for offset, size in ordered:
        if offset != end:
            raise ReplayFormatError('CNDF blocks are not contiguous')
        end = offset+size
    if end != toc:
        raise ReplayFormatError('CNDF blocks do not cover body')
    return blocks


def _block_reader(expanded, blocks, name):
    if name not in blocks:
        raise ReplayFormatError('missing CNDF block '+name)
    offset, size = blocks[name]
    return _Reader(expanded[offset:offset+size])


def _value(reader, strings, imports, depth=0):
    if depth > 64:
        raise ReplayFormatError('NDF value nesting too deep')
    kind = reader.u32()
    if kind == 9:
        return _value(reader, strings, imports, depth+1)
    if kind in _NULL_TYPES:
        return {'null_kind': hex(kind)}
    if kind == 0xbbbbbbbb:
        return {'ref_index': reader.u32(), 'ref_class_id': reader.u32()}
    if kind == 0xaaaaaaaa:
        index = reader.u32()
        if index >= len(imports):
            raise ReplayFormatError('import path index out of range')
        return {'import_path_index': index}
    if kind == 17:
        return [_value(reader, strings, imports, depth+1) for _ in range(reader.u32())]
    if kind == 18:
        return [{'key': _value(reader, strings, imports, depth+1),
                 'value': _value(reader, strings, imports, depth+1)} for _ in range(reader.u32())]
    if kind == 34:
        return {'key': _value(reader, strings, imports, depth+1),
                'value': _value(reader, strings, imports, depth+1)}
    if kind == 8:
        length = reader.u32()
        try:
            return reader.take(length).decode('utf-16-le')
        except UnicodeError as error:
            raise ReplayFormatError('invalid UTF-16 NDF string') from error
    if kind in (7, 28):
        index = reader.u32()
        if index >= len(strings):
            raise ReplayFormatError('table string index out of range')
        return strings[index]
    if kind in _RAW_WIDTHS:
        return {'raw_hex': reader.take(_RAW_WIDTHS[kind]).hex(), 'ndf_type': kind}
    if kind in (11, 33):
        return list(struct.unpack('<'+'f'*(3 if kind == 11 else 2),
                                  reader.take(12 if kind == 11 else 8)))
    if kind == 31:
        return list(struct.unpack('<ii', reader.take(8)))
    if kind == 13:
        return {'raw_hex': reader.take(4).hex(), 'ndf_type': kind}
    if kind in _SCALARS:
        return reader.num(_SCALARS[kind])
    raise ReplayFormatError('unknown NDF value type 0x%x at block offset 0x%x' % (kind, reader.p-4))


def parse_ndf(expanded):
    """Decode the CNDF tables; returns (objects, report). Fails closed."""
    blocks = _blocks(expanded)
    classes = _strings(_block_reader(expanded, blocks, 'CLAS'))
    strings = _strings(_block_reader(expanded, blocks, 'STRG'))
    imports = _strings(_block_reader(expanded, blocks, 'TRAN'))
    props = []
    reader = _block_reader(expanded, blocks, 'PROP')
    while reader.p < len(reader.b):
        props.append((reader.string(), reader.u32()))
    objects, refs, types = [], [], {}
    reader = _block_reader(expanded, blocks, 'OBJE')
    while reader.p < len(reader.b):
        start = reader.p
        class_id = reader.u32()
        if class_id >= len(classes):
            raise ReplayFormatError('object class id out of range')
        obj = {'index': len(objects), 'class_id': class_id, 'class': classes[class_id],
               'offset': start, 'properties': {}}
        while True:
            pid = reader.u32()
            if pid == 0xabababab:
                break
            if pid >= len(props):
                raise ReplayFormatError('property id out of range in object %d' % len(objects))
            name, _owner = props[pid]
            if name in obj['properties']:
                raise ReplayFormatError('duplicate property %s in object %d' % (name, len(objects)))
            kind = struct.unpack_from('<I', reader.b, reader.p)[0] if reader.p+4 <= len(reader.b) else None
            value = _value(reader, strings, imports)
            types[kind] = types.get(kind, 0)+1
            obj['properties'][name] = value
            refs.extend(_all_refs(value))
        objects.append(obj)
    chunk = _block_reader(expanded, blocks, 'CHNK')
    if len(chunk.b) != 8 or chunk.u32() != 0 or chunk.u32() != len(objects):
        raise ReplayFormatError('CHNK object count mismatch')
    null_refs = 0
    for ref in refs:
        if ref['ref_index'] == ref['ref_class_id'] == 0xffffffff:
            null_refs += 1
            continue
        if ref['ref_index'] >= len(objects):
            raise ReplayFormatError('object reference index out of range')
        if objects[ref['ref_index']]['class_id'] != ref['ref_class_id']:
            raise ReplayFormatError('object reference class mismatch')
    report = {'blocks': {k: list(v) for k, v in blocks.items()}, 'classes': len(classes),
              'properties': len(props), 'strings': len(strings), 'imports': len(imports),
              'objects': len(objects), 'object_bytes': reader.p,
              'non_null_references': len(refs)-null_refs, 'null_references': null_refs,
              'value_types': {'0x%x' % k: v for k, v in sorted(types.items())}}
    return objects, report


def _project_nodes(objects):
    """Project unit-class objects plus the nodes their projected refs reach."""
    by_id = {obj['index']: obj for obj in objects}
    nodes = {}

    def include(key):
        key = str(key)
        if key in nodes:
            return
        obj = by_id[int(key)]
        props = obj['properties']
        if obj['class'] in UNIT_CLASSES:
            keep = ('DescriptorId', 'ClassNameForDebug', 'AliasName', 'NameInMenuToken')
            props = {name: copy.deepcopy(props[name]) for name in keep if name in props}
            props['Modules'] = [copy.deepcopy(slot) for slot in obj['properties'].get('Modules', [])
                                if isinstance(slot, dict) and slot.get('key') == 'CompanyUnit']
        else:
            props = copy.deepcopy(props)
        # +40: object offsets are relative to OBJE, which starts at file offset 40.
        nodes[str(key)] = {'class': obj['class'], 'class_id': obj['class_id'],
                           'file_offset': obj['offset']+40, 'properties': props}
        for ref in _refs(props):
            include(ref['ref_index'])

    for obj in objects:
        if obj['class'] in UNIT_CLASSES:
            include(obj['index'])
    if None in nodes:
        raise ReplayFormatError('invalid object index')
    return nodes


def _company_modules(objects):
    """Static company descriptor -> UnitListCompany module -> gfx porteur chain."""
    result = {}
    for obj in objects:
        if obj['class'] != 'TUniteDescriptor':
            continue
        guid = obj['properties'].get('DescriptorId')
        if not isinstance(guid, dict) or 'raw_hex' not in guid:
            continue
        chains = []
        for slot in obj['properties'].get('Modules', []):
            if slot.get('key') != 'UnitListCompany':
                continue
            ref = slot.get('value')
            if not isinstance(ref, dict) or 'ref_index' not in ref:
                raise ReplayFormatError('invalid UnitListCompany module reference')
            module = objects[ref['ref_index']]
            if module['class'] != 'TUnitListCompanyModuleDescriptor':
                raise ReplayFormatError('unexpected UnitListCompany module class')
            props = module['properties']
            porteur = props.get('PorteurDescriptor')
            porteur_info = None
            if isinstance(porteur, dict) and 'ref_index' in porteur:
                target = objects[porteur['ref_index']]
                porteur_info = {'node': porteur['ref_index'], 'ndf_class': target['class'],
                                'debug_name': target['properties'].get('ClassNameForDebug'),
                                'short_name': target['properties'].get('_ShortDatabaseName')}
            chains.append({'slot': 'UnitListCompany', 'module_node': ref['ref_index'],
                           'module_class': module['class'],
                           'controller_name': props.get('ControllerName'),
                           'porteur_descriptor': porteur_info,
                           'units_to_spawn': props.get('NbUniteInCompagnieToSpawn'),
                           'units_max': props.get('NbUniteInCompagnieMax')})
        if chains:
            result[guid['raw_hex']] = chains
    return result


def _member_chain(index, candidate):
    """company -> CompanyUnit module -> member unit, the inverse of derivation."""
    chain = []
    path = candidate['path']
    unit = index['unit_types'][candidate['unit_type_id']]
    if len(path) == 1:
        return [{'role': 'unit_descriptor', 'node': path[0], 'ndf_class': unit['ndf_class'],
                 'debug_name': unit.get('debug_name'), 'alias_name': unit.get('alias_name')}]
    chain.append({'role': 'member_unit_type', 'node': candidate['unit_type_id'],
                  'ndf_class': unit['ndf_class'], 'debug_name': unit.get('debug_name'),
                  'alias_name': unit.get('alias_name')})
    for node in path[1:-1]:
        cls = index['nodes'][node]['class']
        chain.append({'role': 'company_unit_module' if cls == 'TCompanyUnitModuleDescriptor'
                      else 'module_selector', 'node': node, 'ndf_class': cls})
    chain.append({'role': 'company_descriptor', 'node': path[-1],
                  'ndf_class': index['nodes'][path[-1]]['class'],
                  'debug_name': index['nodes'][path[-1]]['properties'].get('ClassNameForDebug')})
    return list(reversed(chain))


def build_index(archive_bytes, source_path=None):
    """Authenticate + extract + project. Never writes or executes game code."""
    provenance = authenticate_archive(archive_bytes)
    expanded, entry = extract_everything(archive_bytes)
    source = {'build': BUILD, 'archive_path': str(source_path) if source_path else None,
              **provenance, 'member': entry}
    return index_from_expanded(expanded, source)


def index_from_expanded(expanded, source):
    """Project an already extracted CNDF payload; used by tests and build_index."""
    objects, report = parse_ndf(expanded)
    nodes = _project_nodes(objects)
    units, descriptors = _derive(nodes)
    company_modules = _company_modules(objects)
    return {'schema': SCHEMA, 'game_build': BUILD, 'source': source,
            'scope': 'static_ndf_descriptor_index_and_exact_validation_guid_join',
            'parse': report, 'nodes': nodes, 'unit_types': units,
            'descriptors': descriptors, 'company_modules': company_modules,
            'limitations': [
                'Static configuration only; no runtime registry, acceptance, deployment or timing evidence.',
                'Selector conditions are retained unevaluated; candidate paths are configured, not active modules.',
                'A GUID-type join compares 16 configured bytes to 16 wire bytes; it does not authenticate live entity identity.',
                'UnitListCompany.PorteurDescriptor resolves to a TGfxDescriptorPorteur, not a member unit type; member units are the inverse CompanyUnit paths.',
                'No localized names are read or claimed; only debug names, aliases and raw tokens appear.']}


def _join_one(index, guid):
    descriptor = index['descriptors'].get(guid)
    if descriptor is None:
        return {'validation_guid_hex': guid, 'join_status': 'missing',
                'source_descriptors': [], 'configured_member_units': [],
                'company_modules': []}
    ambiguous = len(descriptor['source_nodes']) != 1
    candidates = []
    for candidate in descriptor['candidates']:
        unit = index['unit_types'][candidate['unit_type_id']]
        candidates.append({
            'unit_type_id': candidate['unit_type_id'], 'relation': candidate['relation'],
            'ndf_class': unit['ndf_class'], 'debug_name': unit.get('debug_name'),
            'alias_name': unit.get('alias_name'),
            'selector_filters': copy.deepcopy(candidate['selector_filters']),
            'conditions_evaluated': False,
            'member_chain': _member_chain(index, candidate)})
    return {'validation_guid_hex': guid,
            'join_status': 'ambiguous_descriptor' if ambiguous else 'exact_guid',
            'source_descriptors': copy.deepcopy(descriptor['source_nodes']),
            'descriptor_classes': sorted({index['nodes'][node]['class']
                                          for node in descriptor['source_nodes']}),
            'configured_member_units': candidates,
            'company_modules': copy.deepcopy(index['company_modules'].get(guid, [])),
            'runtime_identity': None, 'identity_status': 'static_guid_join_only'}


def join_replay(index, replay_bytes, replay_path=None, expected_sha256=None):
    """Join one replay's 0x07 validation GUIDs independently. No cross-replay merge."""
    import wgrd_timeline as timeline  # Local import keeps static extraction replay-free.
    digest = _sha256(replay_bytes)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ReplayFormatError('replay hash mismatch: %s != %s' % (digest, expected_sha256))
    parsed = parse_replay(replay_bytes)
    catalog = timeline.build_timeline(parsed)['entity_references']
    version = parsed['header'].get('game_version')
    guids = sorted({entry['validation_guid_hex'] for entry in catalog['entries']})
    joins = [_join_one(index, guid) for guid in guids]
    return {'replay': {'path': str(replay_path) if replay_path else None,
                       'sha256': digest, 'game_version': version,
                       'version_matches_index': version == BUILD},
            'scope': 'opcode07_validation_guid',
            'reference_count': catalog['reference_count'],
            'validation_guid_count': catalog['validation_guid_count'],
            'joins': joins,
            'counts': {status: sum(1 for item in joins if item['join_status'] == status)
                       for status in ('exact_guid', 'ambiguous_descriptor', 'missing')},
            'limitations': [
                'Replay joins are computed per input hash; GUIDs are never merged across replays.',
                'Exact GUID equality does not authenticate live entity identity, ownership or deployment.',
                'Member chains are configured static paths; selector conditions were not evaluated.']}


def _write_exclusive(path, payload):
    try:
        with path.open('xb') as handle:
            handle.write(payload)
    except FileExistsError as error:
        raise ReplayFormatError('refusing to overwrite existing output '+str(path)) from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--archive', type=Path, required=True,
                        help='exact build-131544 Data/WarGame/PC/131544/NDF_Win.dat')
    parser.add_argument('--output', type=Path, required=True,
                        help='directory for generated index/join artifacts (must not exist as files)')
    parser.add_argument('--replay', type=Path, action='append', default=[],
                        help='replay to join independently; may be repeated')
    args = parser.parse_args(argv)
    try:
        blob = args.archive.read_bytes()
        index = build_index(blob, args.archive)
        index_payload = (json.dumps(index, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8')
        joins = [join_replay(index, path.read_bytes(), path) for path in args.replay]
        join_doc = {'schema': 'aar_unit_join/1', 'game_build': BUILD,
                    'index_sha256': _sha256(index_payload), 'replays': joins}
        join_payload = (json.dumps(join_doc, sort_keys=True, separators=(',', ':'),
                                   ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8')
        manifest = {'schema': 'aar_unit_index_manifest/1', 'game_build': BUILD,
                    'archive': index['source'], 'index_sha256': _sha256(index_payload),
                    'index_size': len(index_payload),
                    'join_sha256': _sha256(join_payload) if joins else None,
                    'join_size': len(join_payload) if joins else None,
                    'counts': {'descriptors': len(index['descriptors']),
                               'unit_types': len(index['unit_types']),
                               'projected_nodes': len(index['nodes']),
                               'company_module_chains': len(index['company_modules'])},
                    'joins': [{'replay': item['replay'], 'counts': item['counts']} for item in joins]}
        args.output.mkdir(parents=True, exist_ok=True)
        targets = [args.output/('unit-index-%s.json' % BUILD)]
        if joins:
            targets.append(args.output/('unit-join-%s.json' % BUILD))
        targets.append(args.output/('unit-index-%s.manifest.json' % BUILD))
        existing = [str(path) for path in targets if path.exists()]
        if existing:
            raise ReplayFormatError('refusing to overwrite existing output: '+', '.join(existing))
        _write_exclusive(args.output/('unit-index-%s.json' % BUILD), index_payload)
        if joins:
            _write_exclusive(args.output/('unit-join-%s.json' % BUILD), join_payload)
        _write_exclusive(args.output/('unit-index-%s.manifest.json' % BUILD),
                         (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode('utf-8'))
        print(json.dumps({'manifest': manifest, 'join_status': [
            {'replay': item['replay'], 'joins': [{'guid': j['validation_guid_hex'],
             'status': j['join_status'], 'member_debug_names': [c['debug_name'] for c in
             j['configured_member_units']]} for j in item['joins']]} for item in joins]},
            indent=2, sort_keys=True))
    except (OSError, ReplayFormatError, ValueError, KeyError, TypeError) as error:
        print('error: '+str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
