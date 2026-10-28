"""Replay-scoped wire identities and strictly conditional contextual-order facts."""
import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wgrd_replay as w
import wgrd_timeline as timeline
from wgrd_entities import build_reference_catalog, reference_components, contextual_fallback_rules

A = struct.pack('<5I', 0xc00000ba, 0, 0, 3, 2143).hex()
B = struct.pack('<5I', 0xc00000bb, 0, 0, 3, 2143).hex()
C = struct.pack('<5I', 0xc00000ba, 0, 7, 3, 2143).hex()


def event(order, frame, slot, actors=(), targets=()):
    return {'command_order': order, 'frame': frame, 'player_slot': slot, 'opcode': 7,
            'interpretation': {'parameters': {
                'actor_references': [reference_components(r) for r in actors],
                'target_references': [reference_components(r) for r in targets]}}}


class EntityReferences(unittest.TestCase):
    def test_reference_words_and_guid_are_separate(self):
        r = reference_components(A)
        self.assertEqual(r['lookup_key_u32'], 0xc00000ba)
        self.assertEqual(r['validation_guid_u32'], [0, 0, 3, 2143])
        self.assertEqual(r['validation_guid_text'], '00000000:00000000:00000003:0000085f')
        self.assertEqual(r['validation_guid_hex'], bytes.fromhex(A)[4:].hex())
        self.assertEqual(r['reference_hex'], A)
        for bad in ('', A[:-2], A+'00', 'zz'*20):
            with self.assertRaises(w.ReplayFormatError): reference_components(bad)

    def test_catalog_roles_chronology_and_scope(self):
        events = [event(0, 3, 1, [A, A, B]), event(1, 4, 0, [A], [B]), event(2, 8, 2, [], [A])]
        cat = build_reference_catalog(events, 'a'*64, True)
        a, b = sorted(cat['entries'], key=lambda r: r['lookup_key_u32'])
        self.assertEqual(cat['reference_count'], 2)
        self.assertEqual(cat['validation_guid_count'], 1)
        self.assertEqual(a['occurrences'], {'actor': 3, 'target': 1})
        self.assertEqual(a['first_seen'], {'frame': 3, 'command_order': 0})
        self.assertEqual(a['last_seen'], {'frame': 8, 'command_order': 2})
        self.assertEqual(a['observed_player_slots'], [0, 1, 2])
        self.assertIsNone(a['unit_identity'])
        self.assertEqual(a['reference_id'], 'a'*64+':'+A)
        self.assertEqual(events[1]['interpretation']['parameters']['actor_references'][0]['reference_id'], a['reference_id'])
        self.assertNotEqual(a['reference_id'], b['reference_id'])
        other = build_reference_catalog([event(0, 3, 1, [A])], 'b'*64, True)
        self.assertNotEqual(other['entries'][0]['reference_id'], a['reference_id'])

    def test_same_key_different_guid_never_merges(self):
        cat = build_reference_catalog([event(0, 0, 0, [A, C])], 'a'*64, True)
        self.assertEqual(cat['reference_count'], 2)
        self.assertEqual(cat['ambiguous_lookup_key_count'], 1)
        self.assertTrue(all(e['lookup_key_ambiguous'] for e in cat['entries']))
        self.assertEqual(cat['validation_guid_count'], 2)

    def test_build_mismatch_is_inferred_and_empty_catalog_valid(self):
        cat = build_reference_catalog([event(0, 0, 0, [A])], 'a'*64, False)
        self.assertEqual(cat['entries'][0]['layout_status'], 'inferred_build_59638')
        self.assertIsNone(cat['entries'][0]['unit_identity'])
        self.assertEqual(build_reference_catalog([], 'a'*64, True)['entries'], [])

    def test_rules_are_fallback_only_and_not_evaluated_from_wire(self):
        rules = contextual_fallback_rules()
        self.assertEqual(rules['scope'], 'fallback_only_after_earlier_selection_paths')
        self.assertEqual(rules['procedure'], '0x00c9a140')
        self.assertEqual([b['order_kind_u32'] for b in rules['branches']], [32, 33, 4, 9])
        self.assertEqual(rules['branches'][0]['when'], {'module_0108_present': True, 'module_state_28_equals_1': True})
        self.assertFalse(rules['complete_contextual_classifier'])
        # Metadata is independent per export; no shared mutable state.
        rules['branches'].clear()
        self.assertEqual(len(contextual_fallback_rules()['branches']), 4)


class AuthenticEntityCatalog(unittest.TestCase):
    def test_all_samples_reference_counts_and_links(self):
        root = Path(__file__).resolve().parents[1]
        # NOTE: no skip guard. Absent samples raise FileNotFoundError (error, not skip); see AGENTS.md section 9.
        samples = Path(os.environ.get('WGRD_SAMPLES_DIR', str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')))
        manifest = json.loads((root/'samples/manifest.json').read_text())
        for sample, count, guids, occurrences in zip(manifest['samples'], [285,41,400], [103,29,181], [4552,136,8968]):
            b = (samples/sample['file']).read_bytes()
            self.assertEqual(hashlib.sha256(b).hexdigest(), sample['sha256'])
            parsed = w.parse_replay(b); before = copy.deepcopy(parsed)
            out = timeline.build_timeline(parsed); cat = out['entity_references']
            self.assertEqual(parsed, before)
            self.assertEqual((cat['reference_count'], cat['validation_guid_count']), (count, guids))
            self.assertEqual(cat['ambiguous_lookup_key_count'], 0)
            entries = {e['reference_id']: e for e in cat['entries']}
            seen = 0
            for e in out['events']:
                if e['opcode'] != 7: continue
                p = e['interpretation']['parameters']
                if p['order_kind_u32'] == 39:
                    self.assertIsNone(p['effective_order_kind'])
                    self.assertIsNone(p['contextual_resolution']['fallback_reached'])
                    self.assertEqual(p['contextual_resolution']['status'], 'runtime_state_required')
                    self.assertEqual(p['contextual_resolution']['evidence_status'], 'verified' if sample['game_version']=='59638' else 'inferred')
                for role in ['actor','target']:
                    for ref in p[role+'_references']:
                        self.assertEqual(entries[ref['reference_id']]['reference_hex'], ref['reference_hex'])
                        self.assertEqual(ref['reference_id'], sample['sha256']+':'+ref['reference_hex'])
                        seen += 1
            self.assertEqual(seen, occurrences)
            self.assertEqual(sum(sum(e['occurrences'].values()) for e in entries.values()), occurrences)
            json.dumps(out, allow_nan=False)


if __name__ == '__main__': unittest.main()
