"""Build-59638 production request fields. Runtime acceptance remains unknown.

This optional timeline layer never changes the strict parser's opaque framing.
Object-offset names preserve controls whose gameplay meaning is not established.
"""
import math
import struct

from wgrd_replay import ReplayFormatError

EVIDENCE = ['research/evidence/production59638-native.json']


class _Payload:
    def __init__(self, raw):
        self.raw, self.offset = raw, 0

    def take(self, size):
        if size < 0 or size > len(self.raw)-self.offset:
            raise ReplayFormatError('production payload truncated at 0x%x (need %d bytes)' % (self.offset, size))
        start = self.offset
        self.offset += size
        return self.raw[start:self.offset]

    def uint(self):
        return int.from_bytes(self.take(4), 'little')

    def count(self, width):
        count = self.uint()
        if count > (len(self.raw)-self.offset)//width:
            raise ReplayFormatError('production array count exceeds bounded payload')
        return count

    def section(self):
        # Give each length-delimited scope its own cursor: a short child cannot
        # borrow bytes from its sibling. Callers must finish each scope separately.
        header, size = self.uint(), self.uint()
        return header, _Payload(self.take(size))

    def finish(self):
        if self.offset != len(self.raw):
            raise ReplayFormatError('production payload has trailing bytes at 0x%x' % self.offset)


def _result(action, parameters, matched):
    result = {'status': 'verified' if matched else 'inferred', 'action': action,
              'parameters': parameters, 'evidence_build': '59638', 'evidence': EVIDENCE,
              'execution_outcome': 'unknown', 'limitations': [
                  'Serialized request only; funds, availability, placement and execution were not observed.',
                  'Type references declare a static production bundle, not accepted runtime unit identities.',
              ]}
    if not matched:
        result['limitation'] = 'Replay build differs from executable; semantics transferred by layout only.'
    return result


def decode_production(fields, matched):
    """Consume both nested scopes and every variant-specific wire field exactly.

    Exact scope/EOF checks are decoder policy, not executable acceptance claims.
    No parallel-array equality or reference-resolution success is assumed.

    !! TRAP: requested_quantity sums group quantities for variants 1/3. It is a
    !! request, not a physical-unit count. Variant 2 gets no quantity at all.
    !! Deployment points are arguments that the runtime may clamp or reject.
    """
    try:
        raw = bytes.fromhex(fields['serializer_payload_hex'])
    except (TypeError, ValueError) as error:
        raise ReplayFormatError('invalid production payload hex') from error
    if len(raw) != fields['serializer_length_u32']:
        raise ReplayFormatError('production envelope length mismatch')
    variant = fields['variant_u32']
    if variant not in (1, 2, 3):
        raise ReplayFormatError('unsupported production variant')
    cursor = _Payload(raw)
    base_header, base = cursor.section()
    base_kind = base.uint()
    base.finish()
    player_handle = cursor.uint()
    bundle_header, bundle = cursor.section()
    references = []
    for i in range(3):
        # Declared descriptor GUID, not a configured type ID or runtime identity.
        guid = bundle.take(16).hex()
        references.append({'bundle_index': i, 'descriptor_guid_hex': guid,
                           'reference_status': 'null' if guid == '0'*32 else 'declared',
                           'runtime_identity': None,
                           'type_id': None if guid == '0'*32 else guid})
    bundle_extra = bundle.uint()
    bundle.finish()
    params = {'variant_u32': variant, 'production_data_class':
              'TOutWorldUnitWargameProductionData' if variant == 2 else 'TUniteWargameProductionData',
              'base_section_u32': base_header, 'base_obj_04_u32': base_kind,
              'player_handle_u32': player_handle, 'type_bundle_section_u32': bundle_header,
              'type_references': references, 'type_bundle_obj_0c_u32': bundle_extra,
              'requested_quantity': None, 'deployment_points': [],
              'effective_deployment_positions': None}
    if variant == 2:
        params.update(obj_1c_u32=cursor.uint(), obj_20_u32=cursor.uint(), obj_24_u32=cursor.uint())
    else:
        for _ in range(cursor.count(16)):
            point = cursor.take(16)
            values = list(struct.unpack('<3f', point[:12]))
            finite = all(math.isfinite(v) for v in values)
            params['deployment_points'].append({
                'position_argument_f32': values if finite else None,
                'position_status': 'finite_argument' if finite else 'nonfinite',
                'obj_0c_u32': int.from_bytes(point[12:], 'little'), 'raw_hex': point.hex()})
        params.update(obj_68_u32=cursor.uint(), obj_6c_u32=cursor.uint(), obj_70_u32=cursor.uint())
        params['group_quantities_u32'] = [cursor.uint() for _ in range(cursor.count(4))]
        params['requested_quantity'] = sum(params['group_quantities_u32'])
        params['parallel_group_counts_agree'] = (params['obj_70_u32'] ==
            len(params['deployment_points']) == len(params['group_quantities_u32']))
        params.update(obj_90_u32=cursor.uint(), obj_94_u8=cursor.take(1)[0], obj_95_u8=cursor.take(1)[0])
        params['obj_98_nested_u32'] = [
            [cursor.uint() for _ in range(cursor.count(4))] for _ in range(cursor.count(4))]
        params['obj_96_u8'] = cursor.take(1)[0]
    cursor.finish()
    result = _result('request_unit_production', params, matched)
    result['payload_layout_status'] = 'complete'
    result['limitations'] += [
        'Quantity sums the serialized group quantities for variants 1/3; it is not a physical-unit count.',
        'Variant 2 has a separate scalar layout; no requested quantity is assigned.',
        'Deployment points are arguments. Axes, units, accepted positions and travel are unverified.',
        'Variant, base kind, modes, flags, token and nested controls retain neutral field names.',
        'Complete means exact known wire layout; runtime reference resolution is not validated.',
    ]
    return result


def decode_production_action(opcode, fields, raw_hex, matched):
    """Interpret supported production actions without guessing queue correlations."""
    if opcode == 0x0d and fields is not None:
        return decode_production(fields, matched)
    if opcode == 0x0a and fields is not None:
        # Request ID is compared with queued entries at runtime. No purchase join
        # is established, so do not subtract cancellations from purchase totals.
        result = _result('cancel_production', {
            'player_reference': {'lookup_key_u32': fields['obj_04_u32'],
                                 'validation_guid_hex': fields['obj_08_hex']},
            'production_channel_u32': fields['obj_18_u32'],
            'production_request_id_u32': fields['obj_1c_u32'], 'matched_purchase': None,
        }, matched)
        result['limitations'] += [
            'Channel selects a player production manager; channel names remain unresolved.',
            'Request ID is compared with queued entry+8. No reliable purchase-to-cancellation join established.',
        ]
        return result
    return None


CHANGE_PRODUCTION_EVIDENCE = [
    'creator FUN_00b2eeb0 (WarGame3.exe build 59638, read sequence and sizes)',
    'research/CHANGEPRODUCTION-0C.md',
]


def decode_change_production(fields, matched, slot):
    """Raw-field interpretation of opcode 0x0C. Field meanings are not established.

    Status mirrors the timeline convention for layout-verified, semantics-open
    actions: 'partial' on the matching build, 'inferred' on other builds.
    """
    # Observed handle = 0xC000001E + slot (research/TIMELINE-SEMANTICS.md, 08).
    # slot_consistent checks that convention; it does not identify the player.
    player_id = fields['obj_04_u32']
    result = {'status': 'partial' if matched else 'inferred',
              'action': 'change_production_request',
              'parameters': {
                  'player_id_u32': player_id,
                  'slot_consistent': player_id == 0xC000001E + slot,
                  'obj_08_hex': fields['obj_08_hex'],
                  'obj_18_u32_items': fields['obj_18_array']['items_u32'],
                  'obj_34_u32_items': fields['obj_34_array']['items_u32'],
                  'obj_50_points': fields['obj_50_points']['items'],
                  'obj_9c_points': fields['obj_9c_points']['items'],
                  'obj_e8_u32_items': fields['obj_e8_array']['items_u32'],
                  'obj_104_u32': fields['obj_104_u32'],
                  'obj_108_hex': fields['obj_108_hex'],
              },
              'evidence_build': '59638', 'evidence': list(CHANGE_PRODUCTION_EVIDENCE),
              'execution_outcome': 'unknown',
              'payload_layout_status': 'complete',
              'limitations': [
                  'Field meanings are unconfirmed; all parameters are raw wire fields.',
                  'No consumer of this request was traced; effect on production state is unknown.',
                  'Point kinds, obj_18/obj_34 enums and obj_e8 values have no established meaning.',
                  'Sentinel or nonfinite points are emitted as decoded; no location is asserted.',
              ]}
    if not matched:
        result['limitation'] = 'Replay build differs from executable; semantics transferred by layout only.'
        result['limitations'].append('Sample build is not 59638; field layout inferred, not verified.')
    return result


def enrich_production_types(events, unit_data, replay_version):
    """Resolve exact declared GUIDs with existing static index provenance."""
    entries = {}
    for event in events:
        interpretation = event['interpretation']
        if interpretation['action'] != 'request_unit_production':
            continue
        for reference in interpretation['parameters']['type_references']:
            guid = reference['descriptor_guid_hex']
            if reference['reference_status'] == 'null':
                continue
            entries.setdefault(guid, {'validation_guid_hex': guid})
    catalog = {'scope': 'declared_production_type_guids', 'entries': list(entries.values())}
    from wgrd_unit_data import enrich_references
    enrich_references(catalog, unit_data, replay_version)
    if 'descriptor_data' in catalog:
        catalog['descriptor_data']['scope'] = 'declared_production_descriptor_to_configured_static_unit_type'
    return catalog
