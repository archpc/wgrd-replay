"""Versioned original59638 static configuration index. Never runtime identities.

Nodes retain mapping/name properties, original object IDs and expanded-file offsets.
Paths run unit -> CompanyUnit selector/default -> module -> company; replay joins
the final descriptor GUID exactly. Selector conditions are data, never executed.
"""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

from wgrd_replay import ReplayFormatError

SCHEMA = 'wgrd_unit_index/1'
UNIT_CLASSES = ('TUniteAuSolDescriptor', 'TUniteDescriptor')


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                       allow_nan=False)+'\n').encode('utf-8')


def parse_dictionary(blob):
    """TRAD: raw 8-byte token, absolute byte offset, UTF16 code-unit count.

    Retain duplicate records; do not silently choose a translation or trim markup.
    """
    if len(blob) < 8 or blob[:4] != b'TRAD':
        raise ReplayFormatError('invalid localization dictionary header')
    count = struct.unpack_from('<I', blob, 4)[0]
    start = 8+16*count
    if start > len(blob): raise ReplayFormatError('truncated localization record table')
    result = {}
    for i in range(count):
        p = 8+i*16
        token = blob[p:p+8].hex()
        offset, length = struct.unpack_from('<II', blob, p+8)
        end = offset+2*length
        if offset < start or offset % 2 or end > len(blob):
            raise ReplayFormatError('localization string outside data region')
        try: text = blob[offset:end].decode('utf-16-le', errors='strict')
        except UnicodeError as error:
            raise ReplayFormatError('invalid localization UTF16') from error
        result.setdefault(token, []).append({'text': text, 'record_index': i,
                                             'offset': offset, 'length': length})
    return result


def _hex(value, length):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{'+str(length)+'}', value):
        raise ValueError('invalid serialized hex value')
    return value


def _refs(value):
    if isinstance(value, dict):
        if 'ref_index' in value:
            if value['ref_index'] == value['ref_class_id'] == 0xffffffff: return
            yield value
        else:
            for v in value.values(): yield from _refs(v)
    elif isinstance(value, list):
        for v in value: yield from _refs(v)


def _derive(nodes):
    def resolve(ref):
        node = nodes[str(ref['ref_index'])]
        if node['class_id'] != ref['ref_class_id']: raise ValueError('reference class mismatch')
        return str(ref['ref_index']), node
    descriptors, units = {}, {}
    for key, node in nodes.items():
        if not re.fullmatch(r'0|[1-9][0-9]*', key): raise ValueError('invalid object index')
        if type(node['class_id']) is not int or type(node['file_offset']) is not int or node['file_offset'] < 40:
            raise ValueError('invalid object metadata')
        for ref in _refs(node['properties']): resolve(ref)
        if node['class'] not in UNIT_CLASSES: continue
        guid = _hex(node['properties']['DescriptorId']['raw_hex'], 32)
        if node['properties']['DescriptorId']['ndf_type'] != 26: raise ValueError('invalid GUID type')
        descriptors.setdefault(guid, {'source_nodes': [], 'candidates': []})['source_nodes'].append(key)
    def add_unit(key):
        node = nodes[key]; p = node['properties']; token = p.get('NameInMenuToken')
        if token is not None:
            _hex(token['raw_hex'], 16)
            if token['ndf_type'] != 29: raise ValueError('invalid localization token type')
        units[key] = {'descriptor_guid_hex': p['DescriptorId']['raw_hex'], 'ndf_class': node['class'],
                      'debug_name': p.get('ClassNameForDebug'), 'alias_name': p.get('AliasName'),
                      'name_token': token['raw_hex'] if token else None, 'source_node': key}
    for key, node in nodes.items():
        if node['class'] not in UNIT_CLASSES: continue
        p = node['properties']; guid = p['DescriptorId']['raw_hex']
        if node['class'] == 'TUniteAuSolDescriptor':
            add_unit(key)
            descriptors[guid]['candidates'].append({'unit_type_id': key, 'relation': 'direct',
                'path': [key], 'selector_filters': [], 'conditions_evaluated': False})
        for slot in p.get('Modules', []):
            if slot['key'] != 'CompanyUnit': raise ValueError('unexpected projected module slot')
            path = [key]; mid, module = resolve(slot['value']); path.append(mid); filters = []
            if module['class'] == 'TModuleSelector':
                for ref in module['properties'].get('Selection', []):
                    fid, filt = resolve(ref)
                    if filt['class'] != 'TModuleSelectorFilter': raise ValueError('unexpected selector filter')
                    resolve(filt['properties']['Condition']); filters.append(fid)
                default = module['properties'].get('Default')
                if default is None or default.get('ref_index') == 0xffffffff: continue
                mid, module = resolve(default); path.append(mid)
            if module['class'] != 'TCompanyUnitModuleDescriptor': raise ValueError('unexpected CompanyUnit module')
            ref = module['properties'].get('CompanyDescriptor')
            if ref is None or ref.get('ref_index') == 0xffffffff: continue
            cid, company = resolve(ref); path.append(cid)
            if company['class'] != 'TUniteDescriptor': raise ValueError('unexpected company descriptor')
            add_unit(key)
            descriptors[company['properties']['DescriptorId']['raw_hex']]['candidates'].append({
                'unit_type_id': key, 'relation': 'company_default', 'path': path,
                'selector_filters': filters, 'conditions_evaluated': False})
    for desc in descriptors.values():
        desc['source_nodes'].sort(key=int)
        desc['candidates'].sort(key=lambda c: (int(c['unit_type_id']), c['path']))
    return units, descriptors


def export_index(objects, source, names=None, localization=None):
    """Project already authenticated research objects; no guessed GUID rewrites."""
    by_id = {str(o['index']): o for o in objects}
    if len(by_id) != len(objects): raise ReplayFormatError('duplicate NDF object index')
    nodes = {}
    def include(key):
        if key in nodes: return
        obj = by_id[key]; props = copy.deepcopy(obj['properties'])
        if obj['class'] in UNIT_CLASSES:
            props = {k: v for k, v in props.items() if k in
                     ('DescriptorId', 'ClassNameForDebug', 'AliasName', 'NameInMenuToken')}
            props['Modules'] = [copy.deepcopy(s) for s in obj['properties'].get('Modules', []) if s['key'] == 'CompanyUnit']
        nodes[key] = {'class': obj['class'], 'class_id': obj['class_id'],
                      'file_offset': obj['offset']+40, 'properties': props}
        for ref in _refs(props): include(str(ref['ref_index']))
    for key, obj in by_id.items():
        if obj['class'] in UNIT_CLASSES: include(key)
    units, descriptors = _derive(nodes)
    tokens = {u['name_token'] for u in units.values()}
    return {'schema': SCHEMA, 'game_build': '59638', 'source': copy.deepcopy(source),
            'localization': copy.deepcopy(localization), 'nodes': nodes, 'unit_types': units,
            'descriptors': descriptors,
            'names': {t: copy.deepcopy(v) for t, v in (names or {}).items() if t in tokens}}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError('duplicate JSON key: '+key)
        result[key] = value
    return result


def load_index(path):
    try:
        raw = Path(path).read_bytes()
        payload = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
        index = json.loads(payload, object_pairs_hook=_unique_object,
                           parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
        if index['schema'] != SCHEMA or index['game_build'] != '59638':
            raise ValueError('unsupported schema or game build')
        if not isinstance(index['source']['ndf'], dict): raise ValueError('missing NDF provenance')
        units, descriptors = _derive(index['nodes'])
        if units != index['unit_types'] or descriptors != index['descriptors']:
            raise ValueError('index paths disagree with source graph')
        for token, records in index['names'].items():
            _hex(token, 16)
            if not isinstance(records, list) or not records: raise ValueError('invalid name candidates')
            for record in records:
                if not isinstance(record['text'], str): raise ValueError('invalid localized name')
                for field in ('record_index', 'offset', 'length'):
                    if type(record[field]) is not int or record[field] < 0: raise ValueError('invalid name provenance')
                if len(record['text'].encode('utf-16-le')) != record['length']*2:
                    raise ValueError('localized text length mismatch')
        if index['names'] and not isinstance(index['localization'], dict):
            raise ValueError('missing dictionary provenance')
        return {'index': index, 'source': {'index_sha256': hashlib.sha256(raw).hexdigest()}}
    except (OSError, EOFError, zlib.error, ValueError, KeyError, TypeError, AttributeError, RecursionError) as error:
        raise ReplayFormatError('invalid unit index: '+str(error)) from error


def enrich_index(catalog, data, replay_version):
    index = data['index']; used_nodes = {}; counts = {'unique': 0, 'ambiguous': 0, 'missing': 0}
    def include(key):
        if key in used_nodes: return
        used_nodes[key] = copy.deepcopy(index['nodes'][key])
        for ref in _refs(used_nodes[key]['properties']): include(str(ref['ref_index']))
    evidence = 'matching_build_static_configuration' if replay_version == '59638' else 'inferred_build_59638'
    for entry in catalog['entries']:
        desc = index['descriptors'].get(entry['validation_guid_hex'])
        candidates = []
        if desc:
            for key in desc['source_nodes']: include(key)
            for path in desc['candidates']:
                unit = copy.deepcopy(index['unit_types'][path['unit_type_id']])
                names = copy.deepcopy(index['names'].get(unit['name_token'], []))
                unit.update(localized_name=names[0]['text'] if len(names) == 1 else None,
                            name_status='localized' if len(names) == 1 else 'ambiguous' if names else 'missing',
                            name_candidates=names, provenance=copy.deepcopy(path))
                candidates.append(unit)
                for key in path['path']+path['selector_filters']: include(key)
        status = 'missing' if not candidates else 'unique' if len(candidates) == 1 else 'ambiguous'
        counts[status] += 1
        entry['configured_unit_types'] = {'status': status, 'evidence_status': evidence,
            'source_descriptors': copy.deepcopy(desc['source_nodes']) if desc else [], 'candidates': candidates}
    catalog['descriptor_data'] = {**copy.deepcopy(data['source']), 'schema': SCHEMA,
        'dataset_version': '59638', 'replay_version': replay_version, 'evidence_status': evidence,
        'source': copy.deepcopy(index['source']), 'localization': copy.deepcopy(index['localization']),
        'mapping_counts': counts, 'nodes': used_nodes,
        'scope': 'wire_validation_descriptor_to_configured_static_unit_type',
        'limitations': ['Configured static type is not an accepted runtime entity identity or company membership.',
            'Selector conditions are retained unevaluated; default paths do not establish active modules.',
            'Localized strings retain dictionary markup verbatim; aliases/debug names are separate raw fields.',
            'Build mismatch remains inferred. Effective contextual order39 outcomes remain unknown.']}
