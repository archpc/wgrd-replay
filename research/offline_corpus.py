#!/usr/bin/env python3
"""Reproduce the pinned offline census without emitting player metadata or replay bytes.

Reads whole replays through the strict parser and timeline, never a pact-only walk.
Pass --baseline FILE six times to compare production shapes with the earlier inputs.
The directory must contain every hash pinned by samples/offline-corpus-manifest.json.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline


def production_shape(p):
    return json.dumps([len(p['deployment_points']), len(p['group_quantities_u32']),
                       len(p['obj_98_nested_u32']), list(map(len, p['obj_98_nested_u32']))],
                      separators=(',', ':'))


def measure(data):
    """Validate the whole file and measure requests, not simulated outcomes."""
    parsed = parse_replay(data, include_empty=True)
    timeline = build_timeline(parsed)
    events = timeline['events']
    declared = sum(r['count'] for r in parsed['commands'])
    if len(events) != declared or timeline['unresolved_spans']:
        raise ValueError('incomplete command timeline')
    if any(e['decode_status'] not in ('layout', 'opaque') for e in events):
        raise ValueError('unsupported command layout')
    counts = defaultdict(Counter)
    actors, targets, keys = set(), set(), defaultdict(set)
    synchro = defaultdict(list)
    large_groups = []
    for e in events:
        op, f = e['opcode'], e['parameters']
        counts['opcodes'][f'0x{op:02x}'] += 1
        if op == 7:
            option = bytes.fromhex(f['obj_d0_hex'])
            kind = struct.unpack_from('<I', option, 16)[0]
            n_targets = f['obj_60_array']['count_u32']
            counts['order_kinds'][str(kind)] += 1
            counts['order_kind_target_count'][f'{kind}:{n_targets}'] += 1
            counts['dispatch_modes'][str(f['obj_f4_u32'])] += 1
            counts['queue_option'][str(option[4])] += 1
            counts['option6'][str(option[6])] += 1
            counts['padding9_11_zero'][str(option[9:12] == bytes(3))] += 1
            secondary = struct.unpack('<ff', bytes.fromhex(f['obj_c8_hex']))
            counts['secondary_vector'][
                'absent_sentinel' if all(v == math.inf for v in secondary) else
                'finite' if all(map(math.isfinite, secondary)) else 'nonfinite'] += 1
            position = struct.unpack('<fff', bytes.fromhex(f['obj_bc_hex']))
            counts['positions']['finite' if all(map(math.isfinite, position)) else 'nonfinite'] += 1
            counts['positions']['zero' if position == (0., 0., 0.) else 'nonzero'] += 1
            for name, refs in (('obj_04_array', actors), ('obj_60_array', targets)):
                raw = bytes.fromhex(f[name]['items_hex'])
                for offset in range(0, len(raw), 20):
                    ref = raw[offset:offset+20]
                    refs.add(ref)
                    keys[struct.unpack_from('<I', ref)[0]].add(ref)
        elif op == 13:
            interp = e['interpretation']
            if interp.get('payload_layout_status') != 'complete':
                raise ValueError('incomplete production interior')
            counts['production_variants'][str(f['variant_u32'])] += 1
            p = interp['parameters']
            if f['variant_u32'] in (1, 3):
                shape = production_shape(p)
                counts['production_shapes'][shape] += 1
                q, nested = p['group_quantities_u32'], p['obj_98_nested_u32']
                counts['production_parallel_counts'][str(p['parallel_group_counts_agree'])] += 1
                counts['nested_quantity_relation'][
                    'empty_outer' if not nested else
                    'equal' if list(map(len, nested)) == q else 'different'] += 1
                if len(q) >= 10:
                    large_groups.append({'frame': e['frame'], 'slot': e['player_slot'],
                                         'file_offset': e['source']['file_offset'],
                                         'shape': json.loads(shape), 'quantities': q})
        elif op == 19:
            counts['synchro_service'][str(f['obj_04_u32'])] += 1
            counts['synchro_operation'][str(f['obj_08_u32'])] += 1
            counts['synchro_member'][str(f['obj_0c_u32'])] += 1
            counts['synchro_member_matches_slot'][str(f['obj_0c_u32'] == e['player_slot'])] += 1
            synchro[e['player_slot']].append(f['obj_08_u32'])
    for values in synchro.values():
        counts['synchro_first_operation'][str(values[0])] += 1
        for before, after in zip(values, values[1:]):
            counts['synchro_transitions'][f'{before}:{after}'] += 1
    # Reference correlation is scoped to this replay. Do not publish registry keys.
    return {
        'sha256': parsed['sha256'], 'version': str(parsed['header']['game_version']),
        'size': len(data), 'frames': parsed['stats']['frames'], 'commands': declared,
        'pacts': parsed['stats']['pact'], 'digest_valid': parsed['header']['digest_valid'],
        'slots': sorted({r['slot'] for r in parsed['commands']}),
        'counts': {k: dict(v) for k, v in counts.items()},
        'references': {'actor_distinct': len(actors), 'target_distinct': len(targets),
                       'both_roles': len(actors & targets),
                       'keys_with_multiple_full_references': sum(len(v) > 1 for v in keys.values())},
        'large_groups': large_groups,
    }


def census(directory, manifest):
    wanted = {s['sha256']: s for s in manifest['samples']}
    found = {}
    for path in sorted(directory.rglob('*.wargamerpl2')):
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest not in wanted or digest in found:
            continue
        sample = wanted[digest]
        row = measure(data)
        for key in ('sha256', 'version', 'size', 'commands'):
            if row[key] != sample[key]:
                raise ValueError(f'archive {sample["archive_id"]}: {key} mismatch')
        row['archive_id'] = sample['archive_id']
        found[digest] = row
    if set(found) != set(wanted):
        missing = sorted(s['archive_id'] for h, s in wanted.items() if h not in found)
        raise ValueError(f'missing or altered pinned archives: {missing}')
    rows = sorted(found.values(), key=lambda r: r['archive_id'])
    counts = defaultdict(Counter)
    for row in rows:
        for key, values in row['counts'].items():
            counts[key].update(values)
    return {'files': len(rows), 'commands': sum(r['commands'] for r in rows),
            'counts': {k: dict(v) for k, v in counts.items()}, 'replays': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--baseline', type=Path, action='append', default=[])
    args = parser.parse_args()
    manifest = json.loads((ROOT/'samples/offline-corpus-manifest.json').read_text())
    result = census(args.directory, manifest)
    if args.baseline:
        baseline_shapes = set()
        baseline_kinds, baseline_members = set(), set()
        baseline = []
        for path in args.baseline:
            row = measure(path.read_bytes())
            baseline.append({'sha256': row['sha256'], 'commands': row['commands']})
            baseline_shapes.update(row['counts'].get('production_shapes', {}))
            baseline_kinds.update(row['counts'].get('order_kinds', {}))
            baseline_members.update(row['counts'].get('synchro_member', {}))
        novel = {k: v for k, v in result['counts']['production_shapes'].items() if k not in baseline_shapes}
        result['baseline_comparison'] = {'inputs': baseline, 'novel_shapes': novel,
                                         'novel_shape_count': len(novel), 'occurrences': sum(novel.values()),
                                         'production_shape_keys': sorted(baseline_shapes),
                                         'order_kind_values': sorted(map(int, baseline_kinds)),
                                         'synchro_member_values': sorted(map(int, baseline_members)),
                                         'novel_synchro_members': sorted(map(int,
                                             set(result['counts']['synchro_member']) - baseline_members))}
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
