"""Production requests: bounded layouts and conservative request semantics."""
import copy
import json
import struct
import unittest

from wgrd_replay import ReplayFormatError, decode_command_block
from wgrd_timeline import build_timeline


def u(*values):
    return struct.pack('<'+'I'*len(values), *values)


def scope(body, version=32):
    return u(version, len(body))+body


def fields(variant=1, positions=None, counts=None, nested=None, guid=None):
    if positions is None: positions = [(100., 200., 300., 2)]
    if counts is None: counts = [2]
    if nested is None: nested = [[7, 9], []]
    if guid is None: guid = u(11, 22, 33, 44)
    body = scope(u(variant))+u(0xc000001e)+scope(guid+bytes(32)+u(5))
    if variant == 2:
        body += u(6, 2, 77)
    else:
        body += u(len(positions))+b''.join(struct.pack('<3fI', *p) for p in positions)
        body += u(42, 8, len(positions), len(counts), *counts, 2)+b'\x01\x00'
        body += u(len(nested))+b''.join(u(len(row), *row) for row in nested)+b'\x01'
    return {'variant_u32': variant, 'serializer_header_u32': 32,
            'serializer_header_u8': 0, 'serializer_section_u32': 32,
            'serializer_length_u32': len(body), 'serializer_payload_hex': body.hex()}


def wire(f):
    return b'\x0d'+u(f['variant_u32'], f['serializer_header_u32'])+bytes([f['serializer_header_u8']])+u(f['serializer_section_u32'], f['serializer_length_u32'])+bytes.fromhex(f['serializer_payload_hex'])


class ProductionTests(unittest.TestCase):
    def decode(self, f=None, matched=True):
        from wgrd_production import decode_production
        return decode_production(fields() if f is None else f, matched)

    def test_timeline_recovers_production_without_mutating_parser(self):
        f = fields(); raw = wire(f); decoded = decode_command_block(raw, 1, 0)
        parsed = {'header': {'game_version': '59638'}, 'sha256': 'a'*64, 'size': len(raw),
                  'metadata': {}, 'stats': {}, 'unknown_chunks': [],
                  'commands': [{'frame': 8, 'slot': 0, 'offset': 100, 'count': 1,
                                'command_decode': decoded}]}
        old = copy.deepcopy(parsed)
        result = build_timeline(parsed)
        event = result['events'][0]
        self.assertEqual(event['interpretation']['action'], 'request_unit_production')
        self.assertEqual(event['interpretation']['parameters']['requested_quantity'], 2)
        self.assertEqual(event['raw_hex'], raw.hex())
        self.assertEqual(parsed, old)
        self.assertEqual(decoded['status'], 'framed')

    def test_distinct_guid_words_and_all_control_fields_survive(self):
        r = self.decode(); p = r['parameters']
        self.assertEqual(r['status'], 'verified')
        self.assertEqual(r['execution_outcome'], 'unknown')
        self.assertEqual(p['type_references'][0]['descriptor_guid_hex'], u(11,22,33,44).hex())
        self.assertEqual(p['type_references'][1]['descriptor_guid_hex'], bytes(16).hex())
        self.assertEqual(p['deployment_points'][0]['position_argument_f32'], [100.,200.,300.])
        self.assertEqual(p['deployment_points'][0]['obj_0c_u32'], 2)
        self.assertEqual(p['group_quantities_u32'], [2])
        self.assertEqual(p['obj_98_nested_u32'], [[7,9],[]])
        self.assertEqual(p['obj_68_u32'], 42)
        self.assertEqual(p['obj_6c_u32'], 8)
        self.assertEqual(p['obj_90_u32'], 2)
        self.assertEqual(p['obj_94_u8'], 1)
        self.assertEqual(p['obj_95_u8'], 0)
        self.assertEqual(p['obj_96_u8'], 1)
        self.assertIsNone(p['effective_deployment_positions'])

    def test_zero_four_five_entries_and_mismatched_group_count(self):
        for n in (0,4,5):
            r = self.decode(fields(3, positions=[(1.,2.,3.,4)]*n, counts=[1]*n, nested=[[]]*n))
            self.assertEqual(r['parameters']['requested_quantity'], n)
            self.assertEqual(len(r['parameters']['deployment_points']), n)
        r=self.decode(fields(positions=[],counts=[3,4]))
        self.assertEqual(r['parameters']['requested_quantity'],7)
        self.assertEqual(r['parameters']['obj_70_u32'],0)
        self.assertFalse(r['parameters']['parallel_group_counts_agree'])

    def test_variant2_keeps_separate_scalar_semantics(self):
        p=self.decode(fields(2))['parameters']
        self.assertEqual(p['obj_1c_u32'],6)
        self.assertEqual(p['obj_20_u32'],2)
        self.assertEqual(p['obj_24_u32'],77)
        self.assertIsNone(p['requested_quantity'])
        self.assertEqual(p['deployment_points'],[])

    def test_nonfinite_points_remain_safe_json(self):
        r=self.decode(fields(positions=[(float('inf'),float('nan'),3.,2)]))
        self.assertIsNone(r['parameters']['deployment_points'][0]['position_argument_f32'])
        json.dumps(r,allow_nan=False)

    def test_every_truncation_and_extra_byte_rejected(self):
        f=fields();body=bytes.fromhex(f['serializer_payload_hex'])
        for i in range(len(body)):
            cut={**f,'serializer_length_u32':i,'serializer_payload_hex':body[:i].hex()}
            with self.subTest(size=i),self.assertRaises(ReplayFormatError):self.decode(cut)
        with self.assertRaises(ReplayFormatError):self.decode({**f,'serializer_length_u32':len(body)+1,'serializer_payload_hex':(body+b'\0').hex()})

    def test_hostile_counts_and_nested_lengths_rejected(self):
        f=fields();body=bytearray.fromhex(f['serializer_payload_hex'])
        for offset in (4,20,76,108):
            bad=bytearray(body);struct.pack_into('<I',bad,offset,0xffffffff)
            with self.subTest(offset=offset),self.assertRaises(ReplayFormatError):
                self.decode({**f,'serializer_payload_hex':bad.hex()})
        bad=bytearray(body);struct.pack_into('<I',bad,4,8)
        with self.assertRaises(ReplayFormatError):self.decode({**f,'serializer_payload_hex':bad.hex()})

    def test_different_build_is_inferred(self):
        self.assertEqual(self.decode(matched=False)['status'],'inferred')

    def test_static_type_enrichment_preserves_events_and_missing_guids(self):
        from test_unit_index import fixture, UNIT
        from wgrd_production import enrich_production_types
        events = [{'interpretation': self.decode(fields(guid=bytes.fromhex(UNIT)))},
                  {'interpretation': self.decode(fields(guid=bytes.fromhex('ff'*16)))}]
        before = copy.deepcopy(events)
        data = {'index': fixture(), 'source': {}}
        catalog = enrich_production_types(events, data, '510117427')
        self.assertEqual(events, before)
        self.assertEqual(len(catalog['entries']), 2)
        first, missing = [e['configured_unit_types'] for e in catalog['entries']]
        self.assertEqual(first['candidates'][0]['localized_name'], 'PLAYER NAME #reco2')
        self.assertEqual(first['evidence_status'], 'inferred_build_59638')
        self.assertEqual(missing['status'], 'missing')
        self.assertEqual(missing['candidates'], [])

    def test_cancellation_has_request_id_without_purchase_correlation(self):
        from wgrd_production import decode_production_action
        r=decode_production_action(10,{'obj_04_u32':123,'obj_08_hex':bytes(16).hex(),
                                     'obj_18_u32':4,'obj_1c_u32':99},None,True)
        self.assertEqual(r['action'],'cancel_production')
        self.assertEqual(r['parameters']['production_channel_u32'],4)
        self.assertEqual(r['parameters']['production_request_id_u32'],99)
        self.assertIsNone(r['parameters']['matched_purchase'])
        self.assertEqual(r['execution_outcome'],'unknown')


if __name__ == '__main__': unittest.main()
