"""Authenticated 07 request census, no raw replay bytes emitted."""
from collections import Counter
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
    samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home() / '.hermes/artifacts/wgrd-replay/samples/raw')))
    rows = []
    for sample in json.loads((ROOT / 'samples/manifest.json').read_text())['samples']:
        data = (samples / sample['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != sample['sha256']:
            raise ValueError('Sample hash mismatch: ' + sample['file'])
        timeline = build_timeline(parse_replay(data))
        events = [e for e in timeline['events'] if e['opcode'] == 7]
        kinds, selections, statuses, positions = Counter(), Counter(), Counter(), Counter()
        actors, targets = set(), set()
        target_commands = 0
        for event in events:
            interpretation = event['interpretation']; p = interpretation['parameters']
            kinds['%d:%s' % (p['order_kind_u32'], p['order_kind_enum_name'] or 'unknown')] += 1
            selections[p['order_selection']] += 1
            statuses[interpretation['status']] += 1
            positions[p['position_status']] += 1
            actors.update(r['reference_hex'] for r in p['actor_references'])
            targets.update(r['reference_hex'] for r in p['target_references'])
            target_commands += bool(p['target_references'])
        rows.append({'sample': sample['file'], 'sha256': sample['sha256'],
                     'game_version': sample['game_version'], 'order_commands': len(events),
                     'requested_kinds': dict(sorted(kinds.items())), 'selection': dict(selections),
                     'interpretations': dict(statuses), 'positions': dict(positions),
                     'commands_with_target_references': target_commands,
                     'distinct_actor_references': len(actors), 'distinct_target_references': len(targets)})
    return {'schema': 'wgrd_op07_census/1', 'samples': rows}


if __name__ == '__main__':
    print(json.dumps(census(), indent=1, sort_keys=True))
