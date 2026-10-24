"""Reproduce Sample1 battle-report measurements from authenticated replay bytes.

No simulation or decoder changes. Request-level readability is an explicit rubric,
not an estimate of correct battle outcomes. All commands remain in the audit CSV.
"""
import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline
from wgrd_unit_data import load_unit_data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sample', type=Path, default=Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw/koppeltar-Sample1.wargamerpl2')
    ap.add_argument('--output', type=Path, default=ROOT/'research/reports/sample1')
    ap.add_argument('--snapshot', type=Path, default=ROOT/'work/sample1-report-snapshot.json')
    args = ap.parse_args(); raw = args.sample.read_bytes()
    sample = json.loads((ROOT/'samples/manifest.json').read_text())['samples'][0]
    assert hashlib.sha256(raw).hexdigest() == sample['sha256']
    index_path = ROOT/'research/unit-data/build59638-v1.json.gz'
    index_manifest = json.loads(index_path.with_name('build59638-v1.manifest.json').read_text())
    assert hashlib.sha256(index_path.read_bytes()).hexdigest() == index_manifest['index_sha256']
    timeline = build_timeline(parse_replay(raw), unit_data=load_unit_data(index_path))
    refs = sorted(timeline['entity_references']['entries'], key=lambda r: (r['first_seen']['command_order'], r['reference_id']))
    catalog = {r['reference_id']: r for r in refs}
    labels = {r['reference_id']: f'R{i+1:03d}' for i, r in enumerate(refs)}
    def named(items):
        names, ids = [], []
        for item in items:
            match = catalog[item['reference_id']]['configured_unit_types']
            assert match['status'] == 'unique' and match['evidence_status'] == 'matching_build_static_configuration'
            candidate = match['candidates'][0]; assert candidate['name_status'] == 'localized'
            names.append(candidate['localized_name']); ids.append(labels[item['reference_id']])
        return names, ids
    events = []; subtype = collections.Counter(); shoots = collections.Counter()
    for event in timeline['events']:
        interp = event['interpretation']; params = interp.get('parameters') or {}
        actors, actor_ids = named(params.get('actor_references', []))
        targets, target_ids = named(params.get('target_references', []))
        if event['opcode'] == 7:
            kind = params['order_kind']
            if kind is not None:
                assert actors and interp['status'] == 'verified'
                tier, reason = 'meaningful_request', 'named actor references and explicit requested order kind'
                subtype[kind] += 1
                if kind == 'Shoot': shoots.update(actors)
            else:
                assert params['order_kind_u32'] == 39
                tier, reason = 'partial', 'named actor/target references; effective contextual verb unresolved'
            action = kind or 'Contextual39'
        elif event['opcode'] in (8, 9):
            assert interp['status'] == 'verified'
            tier, reason = 'meaningful_request', 'known marker create/remove request; outcome unresolved'
            action = interp['action']
        else:
            tier, reason = 'opaque_to_narrative', 'no supported gameplay interpretation'
            action = None
        events.append({'command_order': event['command_order'], 'frame': event['frame'], 'slot': event['player_slot'],
            'opcode_hex': f"0x{event['opcode']:02x}", 'class': event['class'], 'decode_status': event['decode_status'],
            'tier': tier, 'tier_reason': reason, 'requested_action': action, 'actors': actors,
            'actor_refs': actor_ids, 'targets': targets, 'target_refs': target_ids,
            'position_argument': params.get('target_position_argument_f32', params.get('position_f32')),
            'marker_text': params.get('text_utf8'), 'file_offset': event['source']['file_offset'],
            'byte_length': event['source']['length'], 'execution_outcome': 'unknown'})
    count = collections.Counter(e['tier'] for e in events)
    assert count == {'meaningful_request': 520, 'partial': 3318, 'opaque_to_narrative': 324}
    assert len(events) == 4162 and sum(subtype.values()) == 476
    def measure(rows):
        counts = collections.Counter(e['tier'] for e in rows)
        return {'events': len(rows), **{k: counts[k] for k in ('meaningful_request', 'partial', 'opaque_to_narrative')}}
    coverage = [{'tier': k, 'commands': n, 'percent': round(100*n/len(events), 4)} for k, n in count.items()]
    phases = [{'frame_range': f'{lo}–{hi}', 'first_frame': lo, 'last_frame': hi,
               **measure([e for e in events if lo <= e['frame'] <= hi])}
              for lo, hi in ((0,1499),(1500,4999),(5000,9999),(10000,14999),(15000,19032))]
    slots = []
    for slot in range(4):
        orders = [e for e in events if e['slot'] == slot and e['opcode_hex'] == '0x07']
        explicit = sum(e['tier'] == 'meaningful_request' for e in orders)
        slots.append({'slot': slot, 'standard_orders': len(orders), 'explicit_orders': explicit,
                      'contextual_orders': len(orders)-explicit, 'explicit_percent': round(100*explicit/len(orders),4)})
    push = [e for e in events if e['slot'] == 2 and e['opcode_hex'] == '0x07' and 6321 <= e['frame'] <= 6999]
    anchors = [8,26,29,105,107,109,111,117,127,130,139,153,157,286,383,412,447,766,938,1426,1501,1518,1544,1554,1556,1570,1573,1615,1699,1727,1733,1820,1744,2043,2282,2466,2514,2599,2670,2857,2994,3136,3871,4160,4161]
    story = [e for e in events if e['command_order'] in anchors]
    assert len(story) == len(anchors)
    metrics = {'schema': 'wgrd_battle_report_measurements/1', 'sample_sha256': sample['sha256'],
        'descriptor_index_sha256': index_manifest['index_sha256'], 'game_build': '59638',
        'rubric': {'meaningful_request': 'Explicit order with named actor references, or verified marker action. Request-level readability only.',
                   'partial': 'Contextual39: configured actor/target labels known, effective verb/outcome unknown.',
                   'opaque_to_narrative': 'No gameplay interpretation: separate known-layout, opaque-interior and unsupported-layout breakdown below.'},
        'coverage': coverage, 'phases': phases, 'slots': slots,
        'standard_orders': 3794, 'explicit_order_commands': sum(subtype.values()),
        'explicit_order_counts': dict(sorted(subtype.items())),
        'marker_requests': sum(e['opcode_hex'] in ('0x08','0x09') for e in events),
        'marker_messages': sum(bool(e['marker_text']) for e in events),
        'opaque_breakdown': dict(collections.Counter(e['decode_status'] for e in events if e['tier']=='opaque_to_narrative')),
        'shoot_actor_occurrences_by_type': dict(shoots.most_common()),
        'push_window': {'slot': 2, 'first_frame':6321, 'last_frame':6999,
                        'standard_orders':len(push), 'actions':dict(collections.Counter(e['requested_action'] for e in push))},
        'named_references':len(refs), 'distinct_configured_types':len({r['configured_unit_types']['candidates'][0]['descriptor_guid_hex'] for r in refs}),
        'events_with_verified_execution_outcome':0,
        'selected_report_anchors':len(story), 'selected_anchor_tiers':dict(collections.Counter(e['tier'] for e in story)),
        'selection_policy':'Hand-selected chronological examples, explicitly not an unbiased coverage sample. All4162 events used for coverage.',
        'limits':['Frames, not seconds. Slots, not identified players/teams/owners.',
                  'Configured static types, not accepted physical-unit identities or verified deployment.',
                  'Shoot requests are not shots/hits/kills; marker text is player assertion.',
                  'Positions are transmitted arguments in uncalibrated coordinates, not trajectories.']}
    assert sum(p['events'] for p in phases) == len(events)
    assert sum(s['standard_orders'] for s in slots) == 3794
    assert metrics['opaque_breakdown'] == {'opaque':233,'layout':49,'unknown':42}
    assert sum(shoots.values()) == subtype['Shoot']
    assert all(e['interpretation'].get('execution_outcome', 'unknown') == 'unknown' for e in timeline['events'])
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'measurements.json').write_text(json.dumps(metrics,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
    (args.output/'anchors.json').write_text(json.dumps(story,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
    ref_rows = [{'label':labels[r['reference_id']], 'reference_id':r['reference_id'],
                 'localized_name':r['configured_unit_types']['candidates'][0]['localized_name']} for r in refs]
    (args.output/'reference-labels.json').write_text(json.dumps(ref_rows,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
    with (args.output/'events.csv').open('w',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=list(events[0]));writer.writeheader()
        for row in events:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
    now = datetime.now(timezone.utc).isoformat()
    queries = {}
    for key, rows in {'coverage':coverage,'phases':phases,'slots':slots,'anchors':story,
                      'summary':[{'events':len(events),'named_references':len(refs),'configured_types':metrics['distinct_configured_types'],
                                  'explicit_standard_orders':476,'standard_orders':3794,'markers':44,'marker_messages':12,
                                  'outcomes_verified':0}],
                      'push_window':[{'slot':2,'first_frame':6321,'last_frame':6999,'orders':54,'contextual':50,'Move':2,'UnloadFromTransport':1,'Reverse':1}],
                      'opaque_breakdown':[{'decode_status':k,'commands':n} for k,n in metrics['opaque_breakdown'].items()],
                      'order_counts':[{'requested_order':k,'commands':n} for k,n in subtype.items()],
                      'shoot_types':[{'localized_type':k,'actor_occurrences':n} for k,n in shoots.most_common()]}.items():
        queries[key] = {'rows':rows,'source':{'type':'local-files','name':'Authenticated Sample1 replay and original59638 descriptor index',
            'files':[sample['file'],'build59638-v1.json.gz'],'executedAt':now,
            'evidenceFlow':[{'title':'Authenticate','detail':'Replay SHA256 '+sample['sha256']+'; index SHA256 '+index_manifest['index_sha256']},
                            {'title':'Decode and classify','detail':'Existing parser and optional enrichment; rubric in research/sample1_battle_report.py; all4162 commands retained.'}],
            'caveats':metrics['limits'], 'metricDefinitions':[{'label':'Commands','definition':'Command records, not actors, physical units, successful actions or outcomes.'}]}}
    snapshot = {'surface':'report','title':'Sample1: named orders reveal intent; most tactical verbs remain unknown',
                'generatedAt':now,'status':'verified','buildStatus':'creating','filters':[],
                'queries':queries}
    args.snapshot.parent.mkdir(parents=True,exist_ok=True);args.snapshot.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'coverage':coverage,'push_window':metrics['push_window'],'selected_anchor_tiers':metrics['selected_anchor_tiers']},ensure_ascii=False))


if __name__ == '__main__': main()
