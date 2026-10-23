"""Opt-in, pinned public descriptor snapshot. No runtime entity-ID joins.

Matches describe the GUID transmitted for validation, not proof of live registry
acceptance or company members. Dataset58710 differs from all current samples.
"""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import uuid
import xml.etree.ElementTree as ET

from wgrd_replay import ReplayFormatError

VERSION = '58710'
TABLE_ROOT = 'raws/58710/pc/ndf/patchable/gfx/everything/'
FILES = [TABLE_ROOT+n+'.xml' for n in
         ('TUniteAuSolDescriptor', 'TUniteDescriptor', 'TModuleSelector')] + ['data/58710/final_data.csv']
EVIDENCE = [
    'research/evidence/ev_b1d6856ebda0501415dfaa66a27d25166a07448ff1134b8d810adc2aff4b2c1e.json',
    'research/evidence/ev_a170f55ff1a58539dbe916244814a1e6b32f5aa2cf7b1848c1644f796c734fc7.json',
    'research/evidence/ev_2679b34d671a32b1859b7ce2fb2a507b8e521666b9b57568d54f10c63d983f4e.json',
    'research/evidence/ev_091f83c9e2a410860f6ca602cc51c34335ffe3dc1b7f9c6418445e24e9429e41.json',
]


def ndf_guid_hex(text):
    """.NET XML/CSV GUID text -> exact serialized16 bytes, mixed-endian fields."""
    if not isinstance(text, str) or not re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', text):
        raise ReplayFormatError('invalid NDF GUID text')
    return uuid.UUID(text).bytes_le.hex()


def _text(text):
    return None if text in (None, '', 'null') else text


def _boolean(text):
    if text in (None, '', 'null'): return None
    if text in ('True', 'False'): return text == 'True'
    raise ReplayFormatError('invalid static card boolean: '+text)


def _reference(text):
    if _text(text) is None: return None
    m = re.fullmatch(r'\d+ : (\d+) \((?:True|False)\) - (\w+)', text)
    if not m: raise ReplayFormatError('invalid NDF object reference: '+text)
    return {'ndf_instance_id': m[1], 'class': m[2]}


def descriptor_index(unit_xml, descriptor_xml, selector_xml, card_csv):
    """Join snapshot tables only by explicit object references or exact GUIDs."""
    try:
        roots = [ET.fromstring(blob) for blob in (unit_xml, descriptor_xml, selector_xml)]
        cards = {}
        for row in csv.DictReader(io.StringIO(card_csv.decode('utf-8-sig'))):
            key = row['ID']
            if key in cards: raise ReplayFormatError('duplicate unit card ID: '+key)
            cards[key] = row
        selectors = {x.attrib['id']: x for x in roots[2]}
        index = {}
        for root, kind in zip(roots[:2], ('TUniteAuSolDescriptor', 'TUniteDescriptor')):
            for obj in root:
                if obj.tag != kind: raise ReplayFormatError('unexpected descriptor class')
                guid = ndf_guid_hex(obj.findtext('DescriptorId'))
                if guid in index: raise ReplayFormatError('duplicate descriptor GUID: '+guid)
                modules = []
                for elem in obj.find('Modules'):
                    m = re.fullmatch(r'Map: ([^:]+) : (.+)', elem.text or '')
                    if not m: raise ReplayFormatError('invalid module map entry')
                    ref = _reference(m[2]); default = None
                    if ref['class'] == 'TModuleSelector' and ref['ndf_instance_id'] in selectors:
                        default = _reference(selectors[ref['ndf_instance_id']].findtext('Default'))
                    modules.append({'slot': m[1].strip(), 'reference_class': ref['class'],
                                    'ndf_instance_id': ref['ndf_instance_id'], 'default': default})
                card = None
                # Only this table has the same ID namespace as final_data.csv.
                # Never remove "Company_" or change a GUID word to find a unit.
                if kind == 'TUniteAuSolDescriptor' and obj.attrib['id'] in cards:
                    row = cards[obj.attrib['id']]
                    if row.get('ClassNameForDebug') and row['ClassNameForDebug'] != obj.findtext('ClassNameForDebug'):
                        raise ReplayFormatError('unit card/descriptor debug name mismatch')
                    card = {'name': _text(row.get('Name')), 'movement_type': _text(row.get('MovementType')),
                            'nation': _text(row.get('MotherCountry')), 'tab': _text(row.get('Tab')),
                            **{field: _boolean(row.get(column)) for field,column in
                               [('is_command_unit','IsCommandUnit'), ('is_transporter','IsTransporter'),
                                ('is_ship','IsShip'), ('amphibious','Amphibious')]}}
                index[guid] = {'descriptor_guid_hex': guid, 'ndf_class': kind,
                               'ndf_instance_id': obj.attrib['id'],
                               'debug_name': _text(obj.findtext('ClassNameForDebug')),
                               'modules': modules, 'unit_card': card}
        return index
    except (ET.ParseError, UnicodeError, KeyError, TypeError, ValueError) as error:
        raise ReplayFormatError('invalid descriptor snapshot: '+str(error)) from error


def load_unit_data(directory):
    """Load four hash-pinned files from a ResidentMario/wargame-data root. Offline."""
    manifest = json.loads((Path(__file__).resolve().parent/'research/public-unit-sources.json').read_text())
    records = {r['path']:r for r in manifest['files'] if r['repo']=='ResidentMario/wargame-data'}
    blobs = []
    for name in FILES:
        try: data = (Path(directory)/name).read_bytes()
        except OSError as error:
            raise ReplayFormatError('cannot read pinned unit data '+name+': '+str(error)) from error
        if hashlib.sha256(data).hexdigest() != records[name]['sha256']:
            raise ReplayFormatError('unit data hash mismatch: '+name)
        blobs.append(data)
    return {'descriptors': descriptor_index(*blobs),
            'source': {'dataset_version': VERSION, 'repo':'https://github.com/ResidentMario/wargame-data',
                       'commit': records[FILES[0]]['commit'],
                       'files': [{k: records[name][k] for k in ('path','sha256')} for name in FILES]}}


def enrich_references(catalog, unit_data, replay_version):
    """Annotate newly built reference catalog only. No event/outcome changes."""
    source = unit_data['source']; matched = 0
    for entry in catalog['entries']:
        desc = unit_data['descriptors'].get(entry['validation_guid_hex'])
        entry['static_descriptor'] = copy.deepcopy(desc)
        entry['descriptor_match_status'] = 'unmatched'
        if desc is not None:
            matched += 1
            entry['descriptor_match_status'] = ('exact_guid_snapshot_build' if replay_version==source['dataset_version']
                                                 else 'exact_guid_cross_version')
    catalog['descriptor_data'] = {
        **copy.deepcopy(source), 'replay_version': replay_version,
        'reference_mapping_status': 'verified_build_59638' if replay_version=='59638' else 'inferred_build_59638',
        'matched_references': matched, 'unmatched_references': len(catalog['entries'])-matched,
        'scope': 'wire_declared_validation_descriptor', 'evidence': EVIDENCE,
        'limitations': ['Cross-version descriptor matches do not verify names, capabilities or module values for this replay build.',
                        'Company descriptors are not individual units; no GUID transformation or debug-name substitution used.',
                        'Module defaults describe the static snapshot, not live module presence, flags, state or group members.',
                        'Runtime registry translation can bypass descriptor validation; actual accepted entity identity remains unknown.'],
    }
