"""Authenticated production request census; no replay bytes emitted.

Run: python3 -B research/production_coverage.py > research/production-coverage.json
Default parser remains byte-compatible with checkpoint 79ff879.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import load_unit_data


def census():
    data = load_unit_data(ROOT/'research/unit-data/build59638-v1.json.gz')
    source = subprocess.run(['git','show','79ff879:wgrd_replay.py'], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout
    baseline = {'__name__': 'wgrd_checkpoint'}
    exec(compile(source, '79ff879:wgrd_replay.py', 'exec'), baseline)
    result = {'schema': 'wgrd_production_coverage/1', 'checkpoint': '79ff879',
              'evidence_build': '59638', 'samples': [], 'limitations': [
                  'All totals describe serialized requests, not accepted purchases or units on the map.',
                  'All samples share one acquisition source; Sample2 has an unmatched executable build.',
                  'Contextual39 and all execution outcomes remain unresolved.']}
    for sample in json.loads((ROOT/'samples/manifest.json').read_text())['samples']:
        blob = Path(sample['stored_at']).expanduser().read_bytes()
        if len(blob) != sample['size'] or hashlib.sha256(blob).hexdigest() != sample['sha256']:
            raise ValueError('sample authentication failed')
        parsed = parse_replay(blob)
        original = baseline['parse_replay'](blob)
        if parsed != original: raise ValueError('default parser compatibility failure')
        one = build_timeline(parsed, data)
        encoded = json.dumps(one,sort_keys=True,ensure_ascii=False,allow_nan=False)
        repeated = json.dumps(build_timeline(parsed, data),sort_keys=True,ensure_ascii=False,allow_nan=False)
        if encoded != repeated: raise ValueError('nondeterministic timeline')
        production = [e for e in one['events'] if e['opcode']==13]
        cancellation = [e for e in one['events'] if e['opcode']==10]
        types = {e['validation_guid_hex']:e for e in one['production_types']['entries']}
        variants, quantities, modes, nulls = Counter(), Counter(), Counter(), Counter()
        names, missing, examples, slot_totals = Counter(), Counter(), [], {}
        for event in production:
            interpretation = event['interpretation']
            if interpretation.get('payload_layout_status') != 'complete': raise ValueError('opaque production remains')
            p = interpretation['parameters']; variants[p['variant_u32']] += 1
            slot = slot_totals.setdefault(str(event['player_slot']), {'commands':0,'quantity_variants_1_3':0,'variant2_commands':0})
            slot['commands'] += 1
            if p['requested_quantity'] is not None:
                quantities[p['requested_quantity']] += 1
                slot['quantity_variants_1_3'] += p['requested_quantity']
                modes[p['obj_90_u32']] += 1
            else: slot['variant2_commands'] += 1
            declared = []
            for ref in p['type_references']:
                if ref['reference_status']=='null': nulls[ref['bundle_index']] += 1;continue
                match = types[ref['type_id']]['configured_unit_types']
                if match['status']=='unique':
                    name = match['candidates'][0]['localized_name']
                    if name is not None: names[name] += 1
                    else: missing['localization'] += 1
                else:
                    name = None; missing[match['status']] += 1
                declared.append({'bundle_index':ref['bundle_index'],'name':name,'configured_type_status':match['status']})
            if len(examples)<3:
                examples.append({'frame':event['frame'],'slot':event['player_slot'],
                    'file_offset':event['source']['file_offset'],'variant':p['variant_u32'],
                    'declared_types':declared,'quantity':p['requested_quantity'],
                    'deployment_points':[p['position_argument_f32'] for p in p['deployment_points']]})
        # Every output event still points at its exact original command bytes.
        for event in one['events']:
            s=event['source']
            if bytes.fromhex(event['raw_hex']) != blob[s['file_offset']:s['file_offset']+s['length']]:
                raise ValueError('event byte retention failed')
        if len(one['events']) != sum(r['count'] for r in parsed['commands']): raise ValueError('command retention failed')
        result['samples'].append({'file':sample['file'],'sha256':sample['sha256'],
            'game_version':sample['game_version'],'semantics':'matching59638' if sample['game_version']=='59638' else 'inferred59638',
            'events':len(one['events']),'production_commands':len(production),'variants':dict(variants),
            'quantity_histogram_variants_1_3':dict(quantities),'mode_obj90_histogram':dict(modes),
            'quantity_sum_variants_1_3':sum(q*n for q,n in quantities.items()),
            'production_type_mapping':one['production_types']['descriptor_data']['mapping_counts'],
            'named_reference_occurrences':sum(names.values()),'unresolved_reference_occurrences':dict(missing),
            'unique_localized_names':len(names),'null_reference_occurrences_by_bundle_index':dict(nulls),
            'cancellation_requests':len(cancellation),'cancellation_channels':dict(Counter(e['interpretation']['parameters']['production_channel_u32'] for e in cancellation)),
            'opaque_change_production_commands':sum(e['opcode']==12 for e in one['events']),
            'contextual39_orders':sum(e['opcode']==7 and e['interpretation']['parameters']['order_kind_u32']==39 for e in one['events']),
            'per_recorded_slot':slot_totals,'examples':examples,
            'verification':{'default_parser_matches_checkpoint':True,'two_timeline_exports_identical':True,
                            'all_commands_and_bytes_retained':True,'timeline_sha256':hashlib.sha256(encoded.encode()).hexdigest()}})
    return result


if __name__ == '__main__': print(json.dumps(census(),indent=2,sort_keys=True,ensure_ascii=False))
