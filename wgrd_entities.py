"""Wire-reference correlation and conditional build-59638 order-selection facts.

A catalog entry identifies repeated reference bytes within one replay. It does
not identify a named unit, prove registry acceptance, or merge shared GUIDs.
"""
from collections import defaultdict
import copy
import struct

from wgrd_replay import ReplayFormatError

REFERENCE_EVIDENCE = [
    'research/evidence/ev_b1d6856ebda0501415dfaa66a27d25166a07448ff1134b8d810adc2aff4b2c1e.json',
    'research/evidence/ev_3f7491c7d1b7ccca52ee30ed460b4b4f83a5270fe067293fee4db1435ce40ee1.json',
    'research/evidence/ev_efa16b2a312f64a0efdca81f5f34074734d019409b166b2f2f26306d567a69c3.json',
    'research/evidence/ev_f747e188b400b9f6189deda970d513c977c2a588bd6d0f42c15c5c7868772147.json',
]
CONTEXT_EVIDENCE = [
    'research/evidence/ev_3f7491c7d1b7ccca52ee30ed460b4b4f83a5270fe067293fee4db1435ce40ee1.json',
    'research/evidence/ev_efa16b2a312f64a0efdca81f5f34074734d019409b166b2f2f26306d567a69c3.json',
    'research/evidence/ev_c8b71d9cecc428d86912471c76ecddb810301871b61091688fea0ce79ebd7212.json',
]
CONTEXT_RULE_ID = '59638.c9a140.fallback'


def reference_components(reference_hex):
    try:
        raw = bytes.fromhex(reference_hex)
    except (TypeError, ValueError) as error:
        raise ReplayFormatError('invalid entity reference hex') from error
    if len(raw) != 20:
        raise ReplayFormatError('entity reference length %d != 20' % len(raw))
    key, *guid = struct.unpack('<5I', raw)
    return {'lookup_key_u32': key, 'reference_hex': raw.hex(),
            'validation_guid_hex': raw[4:].hex(), 'validation_guid_u32': guid,
            # TGUID's own four-word text format, not RFC UUID byte ordering.
            'validation_guid_text': ':'.join('%08x' % value for value in guid)}


def contextual_fallback_rules():
    """Fresh metadata only. No evaluation without live state or reachability."""
    return {
        'id': CONTEXT_RULE_ID, 'evidence_build': '59638',
        'procedure': '0x00c9a140',
        'scope': 'fallback_only_after_earlier_selection_paths',
        'complete_contextual_classifier': False,
        'entry_condition': 'Earlier selection paths did not resolve the actor; c9a140 reached with requested kind 39.',
        'inputs': {
            'module_0108_present': 'cc0210: module indexed by registry+0x108 exists for actor.',
            'module_state_28_equals_1': 'c9a210: module+0x28 == 1, only if module exists.',
            'all_members_flag10_clear': 'ca0620: every enumerated member has flag mask 0x10 clear; true for empty list.',
        },
        'branches': [
            {'when': {'module_0108_present': True, 'module_state_28_equals_1': True},
             'order_kind_u32': 32, 'order_kind': 'AirplaneTakeOff'},
            {'when': {'module_0108_present': True, 'module_state_28_equals_1': False},
             'order_kind_u32': 33, 'order_kind': 'AirplanePatrol'},
            {'when': {'module_0108_present': False, 'all_members_flag10_clear': True},
             'order_kind_u32': 4, 'order_kind': 'Move'},
            {'when': {'module_0108_present': False, 'all_members_flag10_clear': False},
             'order_kind_u32': 9, 'order_kind': 'DoNothing'},
        ],
        'missing_runtime_state': ['registry_resolution', 'module_0108_presence_and_state',
                                 'member_enumeration_and_flag_sets', 'earlier_selection_path_result'],
        'limitations': ['Module registry index is runtime data; no module class inferred from wire reference words.',
                        'Flag mask is an executable test, not a recovered named movement capability.',
                        'Earlier paths can select other order kinds; these four branches are not an exhaustive candidate set.'],
        'evidence': CONTEXT_EVIDENCE,
    }


def build_reference_catalog(events, replay_sha256, matched):
    """Attach IDs to newly built event references; never mutate parser fields.

    Full reference bytes + complete input hash form the key. Duplicated array
    entries remain duplicated occurrences. Reused lookup keys with different GUIDs
    remain separate references, flagged as ambiguous instead of silently merged.
    """
    entries, key_refs, guid_refs = {}, defaultdict(set), defaultdict(set)
    for event in events:
        if event['opcode'] != 7:
            continue
        params = event['interpretation']['parameters']
        if params is None:  # Unknown layout / unresolved boundary placeholder.
            continue
        for role in ('actor', 'target'):
            for ref in params[role + '_references']:
                reference_id = replay_sha256 + ':' + ref['reference_hex']
                ref['reference_id'] = reference_id
                mark = {'frame': event['frame'], 'command_order': event['command_order']}
                if reference_id not in entries:
                    entries[reference_id] = {
                        **ref, 'first_seen': mark, 'last_seen': mark,
                        'occurrences': {'actor': 0, 'target': 0}, 'observed_player_slots': [],
                        'identity_status': 'wire_reference_only', 'unit_identity': None,
                        'layout_status': 'matching_build_59638' if matched else 'inferred_build_59638',
                        'lookup_key_ambiguous': False, 'supply_request_occurrences': 0,
                    }
                entry = entries[reference_id]
                entry['last_seen'] = mark
                entry['occurrences'][role] += 1
                if event['player_slot'] not in entry['observed_player_slots']:
                    entry['observed_player_slots'].append(event['player_slot'])
                key_refs[ref['lookup_key_u32']].add(reference_id)
                guid_refs[ref['validation_guid_hex']].add(reference_id)
    for entry in entries.values():
        entry['observed_player_slots'].sort()
        entry['lookup_key_ambiguous'] = len(key_refs[entry['lookup_key_u32']]) > 1
    return {
        'scope_sha256': replay_sha256, 'coverage': 'opcode07_actor_target_references',
        'reference_count': len(entries), 'lookup_key_count': len(key_refs),
        'validation_guid_count': len(guid_refs),
        'shared_validation_guid_count': sum(len(refs) > 1 for refs in guid_refs.values()),
        'ambiguous_lookup_key_count': sum(len(refs) > 1 for refs in key_refs.values()),
        'entries': [entries[key] for key in sorted(entries)],
        'evidence_build': '59638', 'evidence': REFERENCE_EVIDENCE,
        'limitations': ['IDs correlate exact reference bytes within one input hash; physical unit identities remain unresolved.',
                        'Shared GUIDs do not merge registry keys; GUID component meanings and descriptor names unresolved.',
                        'Observed player slots record command provenance, not ownership or controller identity.'],
    }


OP18_EVIDENCE = ['research/OP18-REFERENCE-KEYS.md', 'research/OP18-SUPPLY-TARGETS.md',
                 'creator FUN_00b2f2e0 (WarGame3.exe build 59638)']


def attribute_supply_requests(events, reference_catalog, matched, has_unit_data):
    """Post-pass: attribute 0x18 DeactivateSupply events to 0x07 wire references.

    Rule (research/OP18-SUPPLY-TARGETS.md): a registry key resolves only when exactly
    one catalog entry carries it and the issuing slot is in its observed slots.
    Any other case assigns no reference_id, GUID or unit type.
    """
    by_key = defaultdict(list)
    for entry in reference_catalog['entries']:
        by_key[entry['lookup_key_u32']].append(entry)
    for event in events:
        if event['opcode'] != 0x18 or event['parameters'] is None:
            continue
        params = event['parameters']
        key = params['obj_04_u32']
        candidates = by_key.get(key, [])
        slot = event['player_slot']
        resolution, entry = 'unreferenced_key', None
        if len(candidates) > 1 or any(c['lookup_key_ambiguous'] for c in candidates):
            resolution = 'ambiguous_key'
        elif len(candidates) == 1:
            entry = candidates[0]
            resolution = 'unique_key' if slot in entry['observed_player_slots'] else 'slot_mismatch'
        target = {'resolution': resolution, 'reference_id': None, 'validation_guid_hex': None,
                  'issuing_slot_in_observed_slots': None, 'temporal_relation': None,
                  'candidate_reference_ids': [c['reference_id'] for c in candidates],
                  'unit_type': None}
        if entry is not None:
            target['issuing_slot_in_observed_slots'] = slot in entry['observed_player_slots']
            frame = event['frame']
            first, last = entry['first_seen']['frame'], entry['last_seen']['frame']
            if resolution == 'unique_key':
                target['temporal_relation'] = ('before_first' if frame < first else
                                               'after_last' if frame > last else 'inside')
                target['reference_id'] = entry['reference_id']
                target['validation_guid_hex'] = entry['validation_guid_hex']
                if has_unit_data and 'configured_unit_types' in entry:
                    target['unit_type'] = copy.deepcopy(entry['configured_unit_types'])
                entry['supply_request_occurrences'] += 1
        limitations = [
            'Resolution uses per-replay registry-key uniqueness among 0x07 wire references; no cross-replay identity.',
            'No consumer of the 0x18 object was traced; obj_08/obj_0c meanings and the action direction are unresolved.',
            'Unit type comes from the static NDF join on the validation GUID with its own caveats (see configured_unit_types.status).',
        ]
        if not matched:
            limitations.append('Sample build is not 59638; layout inferred.')
        event['interpretation'] = {
            'action': 'deactivate_supply_request', 'class': 'TNetworkActionDeactivateSupply',
            'status': 'partial' if matched else 'inferred', 'execution_outcome': 'unknown',
            'evidence_build': '59638', 'evidence': list(OP18_EVIDENCE),
            'parameters': {'registry_key_u32': key, 'obj_08_u32': params['obj_08_u32'],
                           'obj_0c_u8': params['obj_0c_u8'], 'target_reference': target},
            'limitations': limitations,
        }
    return reference_catalog
