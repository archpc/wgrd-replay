"""Reproduce public ID comparisons. Inputs are pinned caches, no network writes."""
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import load_unit_data, ndf_guid_hex, TABLE_ROOT


def census(cache):
    manifest=json.loads((ROOT/'research/public-unit-sources.json').read_text())
    for source in manifest['files']:
        path=cache/source['repo'].split('/')[-1]/source['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=source['sha256']:
            raise ValueError('Public source hash mismatch: '+str(path))
    mario=cache/'wargame-data'; data=load_unit_data(mario)
    raw_units=list(csv.DictReader((mario/(TABLE_ROOT+'TUniteAuSolDescriptor.csv')).open()))
    raw_other=list(csv.DictReader((mario/(TABLE_ROOT+'TUniteDescriptor.csv')).open()))
    unit_guids={ndf_guid_hex(r['DescriptorId']) for r in raw_units}
    other_guids={ndf_guid_hex(r['DescriptorId']) for r in raw_other}
    assert unit_guids|other_guids==set(data['descriptors'])
    toolbox_bytes=(cache/'wgrd-toolbox/data/master.json').read_bytes()
    toolbox=json.loads(toolbox_bytes.decode('utf-16' if toolbox_bytes[:2]==b'\xff\xfe' else 'utf-8-sig'))
    tb_guids={r['id'] for r in toolbox}
    instance_ids={int(r['[ID]']) for r in raw_units+raw_other}
    rows=[]
    samples=Path(os.environ.get('WGRD_SAMPLES_DIR',str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')))
    for sample in json.loads((ROOT/'samples/manifest.json').read_text())['samples']:
        raw=(samples/sample['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==sample['sha256']
        timeline=build_timeline(parse_replay(raw),unit_data=data)
        refs=timeline['entity_references']['entries']
        rows.append({
            'sample':sample['file'],'sha256':sample['sha256'],'game_version':sample['game_version'],
            'reference_mapping_status':timeline['entity_references']['descriptor_data']['reference_mapping_status'],
            'references':len(refs),'exact_guid_matches':sum(e['static_descriptor'] is not None for e in refs),
            'ndf_classes':dict(Counter(e['static_descriptor']['ndf_class'] for e in refs)),
            'direct_unit_card_references':sum(e['static_descriptor']['unit_card'] is not None for e in refs),
            'company_debug_references':sum((e['static_descriptor']['debug_name'] or '').startswith('Company_') for e in refs),
            'direct_unit_card_occurrences':{role:sum(e['occurrences'][role] for e in refs if e['static_descriptor']['unit_card']) for role in ('actor','target')},
            'direct_unit_card_names':sorted({e['static_descriptor']['unit_card']['name'] for e in refs if e['static_descriptor']['unit_card']}),
            'toolbox_direct_guid_matches':sum(e['validation_guid_hex'] in tb_guids for e in refs),
            'runtime_key_equal_to_ndf_instance_id':sum(e['lookup_key_u32'] in instance_ids for e in refs),
            'snapshot_version_matches_replay':sample['game_version']=='58710',
            'contextual_requests':sum(e['opcode']==7 and e['interpretation']['parameters']['order_kind_u32']==39 for e in timeline['events']),
            'resolved_effective_orders':0,'resolved_live_unit_identities':0,
        })
    return {'schema':'wgrd_public_unit_comparison/1','snapshot_version':'58710',
            'ndf_unit_rows':len(raw_units),'ndf_other_descriptor_rows':len(raw_other),
            'toolbox_rows':len(toolbox),'toolbox_dataset_version':None,
            'toolbox_shared_exact_unit_guids':len(tb_guids&unit_guids),
            'toolbox_shared_exact_other_descriptor_guids':len(tb_guids&other_guids),
            'verified_matching_version_unit_names':0,'samples':rows}


if __name__=='__main__':
    print(json.dumps(census(Path(sys.argv[1])),indent=1,sort_keys=True))
