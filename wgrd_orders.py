"""Build-59638 standard-order requests. Never reconstruct runtime-selected outcomes."""
import math
import struct

from wgrd_replay import ReplayFormatError
from wgrd_entities import reference_components, CONTEXT_RULE_ID

# Name/value pairs at VA 0x1d86488..0x1d865b0; descriptor at 0x1d868b8.
# 39 is the reflected Length sentinel, explicitly handled as contextual by c972a0.
ORDER_KINDS = {
    0: 'FollowFormation', 1: 'Land', 2: 'Bombarder', 3: 'Parachuter', 4: 'Move',
    5: 'Voir', 6: 'Attack', 7: 'Replier', 8: 'Capture', 9: 'DoNothing', 10: 'Stop',
    11: 'PositionInterdite', 12: 'LoadIntoTransport', 13: 'LoadUnit',
    14: 'UnloadFromTransport', 15: 'MergeCompany', 16: 'MoveAndAttack', 17: 'GoUp',
    18: 'GoDown', 19: 'Shoot', 20: 'SplitCompany', 21: 'SupplyUnit', 22: 'AskForSupply',
    23: 'GoGetSupply', 24: 'StandBy', 25: 'GenericLoadUnit', 26: 'AskedForSupply',
    27: 'Reverse', 28: 'Spread', 29: 'EnterDistrict', 30: 'LeaveDistrict',
    31: 'AssaultDistrict', 32: 'AirplaneTakeOff', 33: 'AirplanePatrol',
    34: 'AirplaneAttack', 35: 'AirplaneEvacuate', 39: 'Length',
}
EVIDENCE = [
    'research/evidence/ev_5fb36533a0ef4930f4252665e664ba14d245fa50ba59d04a6a065d9648265830.json',
    'research/evidence/ev_4d4a3f06dacdb44f6763451408eee09ac45e8d3bff5781a5474ff7fc3dca789e.json',
    'research/evidence/ev_8126786af1d43f806f682979a267f3b6bb5e924b3148b917d12c811e73e967b5.json',
    'research/evidence/ev_88d6d3f0679457747b2762232b0604df98844a16f18f766c14b62de0b42ce7f6.json',
]


def _bytes(text, size, name):
    try:
        raw = bytes.fromhex(text)
    except (TypeError, ValueError) as error:
        raise ReplayFormatError('opcode 07 invalid %s hex' % name) from error
    if len(raw) != size:
        raise ReplayFormatError('opcode 07 %s length %d != %d' % (name, len(raw), size))
    return raw


def _references(array, name):
    # b2e070 separates first u32 from the remaining 16 bytes, performs registry
    # lookup and saved-object validation. The first word alone is not identity.
    raw = _bytes(array['items_hex'], array['count_u32'] * 20, name)
    return [reference_components(raw[i:i+20].hex()) for i in range(0, len(raw), 20)]


def decode_standard_order(fields, matched):
    options = _bytes(fields['obj_d0_hex'], 36, 'order structure')
    position = struct.unpack('<fff', _bytes(fields['obj_bc_hex'], 12, 'position'))
    _bytes(fields['obj_c8_hex'], 8, 'secondary vector')
    kind, token = struct.unpack_from('<II', options, 16)
    name = ORDER_KINDS.get(kind)
    contextual = kind == 39
    known_request = name is not None and not contextual
    if all(v == math.inf for v in position):
        usable_position, position_status = None, 'absent_sentinel'
    elif not all(math.isfinite(v) for v in position):
        usable_position, position_status = None, 'nonfinite'
    elif kind == 10:
        usable_position, position_status = None, 'not_interpreted_for_stop_request'
    else:
        usable_position, position_status = list(position), 'transmitted_argument'
    result = {
        'status': ('verified' if known_request else 'partial') if matched else 'inferred',
        'action': 'issue_standard_order', 'evidence_build': '59638',
        'execution_outcome': 'unknown', 'evidence': EVIDENCE,
        'parameters': {
            'order_kind_u32': kind, 'order_kind': name if known_request else None,
            'order_kind_enum_name': name,
            'order_selection': 'explicit_request' if known_request else ('runtime_dependent' if contextual else 'unknown'),
            'effective_order_kind': None,
            'dispatch_token_u32': token, 'dispatch_mode_u32': fields['obj_f4_u32'],
            'actor_references': _references(fields['obj_04_array'], 'actor references'),
            'target_references': _references(fields['obj_60_array'], 'target references'),
            'reference_resolution': 'runtime_required',
            'target_position_argument_f32': usable_position, 'position_status': position_status,
            'effective_target_position_f32': None,
            'position_argument_hex': fields['obj_bc_hex'],
            'secondary_vector_hex': fields['obj_c8_hex'],
            'order_structure_hex': fields['obj_d0_hex'],
            'reference_sets': {'obj_04': fields['obj_04_array'], 'obj_60': fields['obj_60_array']},
        },
        'limitations': [
            'Kind names classify requested orders; effective kinds can differ per actor at execution.',
            '39 is the Length sentinel used by contextual selection; not a move/attack discriminator.',
            'Full 20-byte entity references required; unit/group descriptors and live identities unresolved.',
            'Position is a transmitted target argument, not an observed unit position or guaranteed destination.',
            'Runtime can clamp position or replace it from target state; axes/units/map transform unresolved.',
            'Dispatch token IDs and remaining option flags have no stable semantic mapping here.',
        ],
    }
    if contextual:
        result['parameters']['contextual_resolution'] = {
            'status': 'runtime_state_required',
            'evidence_status': 'verified' if matched else 'inferred',
            'rule_id': CONTEXT_RULE_ID, 'fallback_reached': None,
            'effective_order_kind': None,
        }
    if not matched:
        result['limitation'] = 'Replay build differs from executable; semantics transferred by layout only.'
    return result
