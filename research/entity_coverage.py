"""Authenticated wire-reference census. Emits counts/hashes, no replay bytes."""
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline


def census():
    samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')))
    rows = []
    for sample in json.loads((ROOT/'samples/manifest.json').read_text())['samples']:
        data = (samples/sample['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != sample['sha256']:
            raise ValueError('Sample hash mismatch: '+sample['file'])
        out = build_timeline(parse_replay(data))
        cat = out['entity_references']
        rows.append({
            'sample': sample['file'], 'sha256': sample['sha256'],
            'game_version': sample['game_version'],
            'layout_status': 'matching_build_59638' if sample['game_version']=='59638' else 'inferred_build_59638',
            **{k: cat[k] for k in ('reference_count', 'lookup_key_count', 'validation_guid_count',
                                  'shared_validation_guid_count', 'ambiguous_lookup_key_count')},
            'reference_occurrences': sum(sum(e['occurrences'].values()) for e in cat['entries']),
            'contextual_requests': sum(e['opcode']==7 and e['interpretation']['parameters']['order_kind_u32']==39
                                       for e in out['events']),
            'resolved_unit_identities': 0, 'resolved_effective_orders': 0,
        })
    return {'schema': 'wgrd_entity_census/1', 'samples': rows}


if __name__ == '__main__':
    print(json.dumps(census(), indent=1, sort_keys=True))
