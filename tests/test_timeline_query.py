"""Tests for wgrd_timeline_query: pure read-only views over timeline events.

Synthetic events test mechanics; authentic pinned-sample tests (skipped when
the private sample is absent) test integration against real interpretations.
"""
import copy
import os
from pathlib import Path
import unittest

from wgrd_timeline_query import filter_events, reference_history, request_summary


def event(order, frame=0, slot=0, opcode=0x07, action="issue_standard_order",
          status="partial", kind=None, actors=(), targets=(), outcome="unknown"):
    params = {}
    if kind is not None:
        params["order_kind_u32"] = kind
    if actors:
        params["actor_references"] = [{"reference_id": r} for r in actors]
    if targets:
        params["target_references"] = [{"reference_id": r} for r in targets]
    return {
        "command_order": order, "frame": frame, "player_slot": slot,
        "opcode": opcode,
        "interpretation": {"action": action, "status": status,
                           "execution_outcome": outcome, "parameters": params},
    }


class FilterMechanics(unittest.TestCase):
    def test_opcode_filter_selects_matching_events_in_order(self):
        events = [event(0, opcode=0x07), event(1, opcode=0x0C),
                  event(2, opcode=0x07), event(3, opcode=0x08)]
        out = filter_events(events, opcode=0x07)
        self.assertEqual([e["command_order"] for e in out], [0, 2])

    def test_filters_compose_with_and(self):
        events = [event(0, frame=10, slot=0, opcode=0x07),
                  event(1, frame=20, slot=1, opcode=0x07),
                  event(2, frame=20, slot=1, opcode=0x0C),
                  event(3, frame=30, slot=1, opcode=0x07)]
        out = filter_events(events, opcode=0x07, slot=1,
                            frame_min=15, frame_max=25)
        self.assertEqual([e["command_order"] for e in out], [1])

    def test_no_criteria_returns_all_events(self):
        events = [event(0), event(1)]
        self.assertEqual(filter_events(events), events)

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(filter_events([], opcode=0x07), [])

    def test_frame_bounds_are_inclusive(self):
        events = [event(0, frame=5), event(1, frame=10), event(2, frame=15)]
        out = filter_events(events, frame_min=5, frame_max=10)
        self.assertEqual([e["command_order"] for e in out], [0, 1])

    def test_action_filter_excludes_none_action_events(self):
        events = [event(0, action=None), event(1, action="request_unit_production")]
        out = filter_events(events, action="request_unit_production")
        self.assertEqual([e["command_order"] for e in out], [1])
        self.assertEqual(filter_events(events, status="partial"), events)

    def test_action_none_string_selects_none_action_events(self):
        # A3: the summary counts None actions under "None"; the filter must
        # be able to enumerate that bucket, not silently return [].
        events = [event(0, action=None), event(1, action="issue_standard_order")]
        out = filter_events(events, action="None")
        self.assertEqual([e["command_order"] for e in out], [0])


class FilterValidation(unittest.TestCase):
    def test_invalid_opcode_rejected(self):
        for bad in (-1, 256, "0x07", 7.0, True):
            with self.assertRaises(ValueError):
                filter_events([], opcode=bad)

    def test_negative_bounds_rejected(self):
        for kw in ({"slot": -1}, {"frame_min": -1}, {"frame_max": -1}):
            with self.assertRaises(ValueError):
                filter_events([], **kw)

    def test_inverted_frame_range_rejected(self):
        with self.assertRaises(ValueError):
            filter_events([], frame_min=10, frame_max=5)

    def test_non_string_action_status_rejected(self):
        with self.assertRaises(ValueError):
            filter_events([], action=7)
        with self.assertRaises(ValueError):
            filter_events([], status=[])

    def test_inputs_are_not_mutated(self):
        events = [event(0, opcode=0x07, actors=("a"*64+":r11",)), event(1, opcode=0x0C)]
        before = copy.deepcopy(events)
        filter_events(events, opcode=0x07)
        reference_history(events, "a"*64+":r11")
        request_summary(events)
        self.assertEqual(events, before)


class ReferenceHistoryMechanics(unittest.TestCase):
    def test_history_matches_actor_and_target_roles_in_command_order(self):
        events = [event(2, actors=("a"*64+":r11",)), event(0, targets=("a"*64+":r11",)),
                  event(1, actors=("a"*64+":r22",)), event(3, actors=("a"*64+":r11",), targets=("a"*64+":r22",))]
        out = reference_history(events, "a"*64+":r11")
        self.assertEqual([e["command_order"] for e in out], [0, 2, 3])

    def test_unknown_reference_id_returns_empty(self):
        self.assertEqual(reference_history([event(0, actors=("a"*64+":r11",))], "a"*64+":r99"), [])

    def test_events_without_references_are_skipped(self):
        events = [event(0), event(1, actors=("a"*64+":r11",))]
        self.assertEqual([e["command_order"] for e in reference_history(events, "a"*64+":r11")], [1])

    def test_invalid_reference_id_rejected(self):
        for bad in (11, 11.0, None, True, ""):
            with self.assertRaises(ValueError):
                reference_history([], bad)

    def test_unscoped_reference_id_rejected_not_silently_empty(self):
        # A4: a bare reference_hex (no sha256 scope) is a caller error, not
        # "this reference was never used".
        for bad in ("0e0600c000000000", "a"*63+":r1", "a"*64+":", "xyz:r1"):
            with self.assertRaises(ValueError):
                reference_history([], bad)

    def test_singular_target_reference_is_included(self):
        # A2: 0x18 DeactivateSupply carries parameters.target_reference (a
        # single dict), which the catalog attributes to the same id.
        e = event(0, opcode=0x18, action="deactivate_supply_request")
        e["interpretation"]["parameters"]["target_reference"] = {"reference_id": "a"*64+":r11"}
        out = reference_history([e], "a"*64+":r11")
        self.assertEqual([x["command_order"] for x in out], [0])


class RequestSummaryMechanics(unittest.TestCase):
    def test_counts_match_manual_recomputation(self):
        events = [event(0, opcode=0x07, slot=0, action="issue_standard_order",
                        status="partial", kind=39, outcome="unknown"),
                  event(1, opcode=0x07, slot=1, action="issue_standard_order",
                        status="partial", kind=4, outcome="unknown"),
                  event(2, opcode=0x0C, slot=0, action="change_production_request",
                        status="verified", outcome=None),
                  event(3, opcode=0x08, slot=2, action=None, status="unknown", outcome=None)]
        s = request_summary(events)
        self.assertEqual(s["total"], 4)
        self.assertEqual(s["by_action"], {"issue_standard_order": 2,
                                          "change_production_request": 1, "None": 1})
        self.assertEqual(s["by_status"], {"partial": 2, "verified": 1, "unknown": 1})
        self.assertEqual(s["by_slot"], {0: 2, 1: 1, 2: 1})
        self.assertEqual(s["by_opcode"], {"0x07": 2, "0x0c": 1, "0x08": 1})
        self.assertEqual(s["contextual_kind39"], 1)
        self.assertEqual(s["execution_outcomes"], {"unknown": 2, "None": 2})

    def test_empty_input_gives_zero_counts(self):
        s = request_summary([])
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["by_action"], {})
        self.assertEqual(s["contextual_kind39"], 0)

    def test_kind39_count_is_independent_of_action_counts(self):
        events = [event(0, kind=39), event(1, kind=39), event(2, kind=4)]
        s = request_summary(events)
        self.assertEqual(s["contextual_kind39"], 2)
        self.assertEqual(s["by_action"]["issue_standard_order"], 3)

    def test_unresolved_tail_events_with_none_opcode_are_counted(self):
        # build_timeline emits opcode=None events for unresolved multi-command
        # tails; the summary must count them, not crash on "0x%02x" % None.
        # Use the PRODUCER shape: _interpretation(None, ...) gives parameters
        # None and no execution_outcome key (A6).
        from wgrd_timeline import _interpretation
        tail = event(1, opcode=0x07)
        tail["opcode"] = None
        tail["interpretation"] = _interpretation(None, None, True, 0, "59638")
        s = request_summary([event(0, opcode=0x07), tail])
        self.assertEqual(s["total"], 2)
        self.assertEqual(s["by_opcode"], {"0x07": 1, "None": 1})
        self.assertEqual(s["execution_outcomes"], {"unknown": 1, "None": 1})
        self.assertEqual(filter_events([tail], opcode=0x07), [])
        self.assertEqual([e["command_order"] for e in filter_events([tail], action="None")], [1])


class AuthenticSampleIntegration(unittest.TestCase):
    """Pinned private sample; skips when absent (never fetches)."""

    @classmethod
    def setUpClass(cls):
        samples = Path(os.environ.get(
            "WGRD_SAMPLES_DIR",
            str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))
        path = samples / "koppeltar-Sample1.wargamerpl2"
        if not path.exists():
            raise unittest.SkipTest("private replay fixture unavailable: " + path.name)
        import hashlib
        from wgrd_replay import parse_replay
        from wgrd_timeline import build_timeline
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != \
                "c5f8eff1298cf38c1d9967d29f98a22dfc869c150405630f9f695bb80a521df8":
            raise AssertionError("sample integrity mismatch")
        timeline = build_timeline(parse_replay(data))
        cls.events = timeline["events"]
        cls.catalog = timeline["entity_references"]

    def test_summary_totals_match_event_list(self):
        s = request_summary(self.events)
        self.assertEqual(s["total"], len(self.events))
        self.assertEqual(sum(s["by_action"].values()), len(self.events))
        self.assertEqual(sum(s["by_status"].values()), len(self.events))
        self.assertEqual(sum(s["by_opcode"].values()), len(self.events))
        self.assertEqual(s["contextual_kind39"], 3318)

    def test_filter_and_history_compose_on_real_events(self):
        orders = filter_events(self.events, opcode=0x07, status="partial")
        self.assertTrue(orders)
        self.assertTrue(all(e["opcode"] == 0x07 for e in orders))
        params = orders[0]["interpretation"].get("parameters") or {}
        refs = params.get("actor_references") or []
        if refs:
            rid = refs[0]["reference_id"]
            history = reference_history(self.events, rid)
            self.assertIn(orders[0]["command_order"],
                          [e["command_order"] for e in history])
            self.assertEqual([e["command_order"] for e in history],
                             sorted(e["command_order"] for e in history))

    def test_supply_reference_history_includes_deactivate_event(self):
        # A2: catalog entries with supply_request_occurrences > 0 must have
        # their 0x18 event in reference_history.
        from wgrd_timeline import build_timeline  # noqa: F401 (events already built)
        supply_entries = [e for e in self.catalog["entries"]
                          if e.get("supply_request_occurrences", 0) > 0]
        self.assertTrue(supply_entries, "Sample1 should have supply references")
        entry = supply_entries[0]
        history = reference_history(self.events, entry["reference_id"])
        orders = {e["command_order"] for e in history}
        supply_events = [e for e in self.events if e["opcode"] == 0x18
                         and (e["interpretation"].get("parameters") or {})
                         .get("target_reference", {}).get("reference_id") == entry["reference_id"]]
        self.assertTrue(supply_events)
        for e in supply_events:
            self.assertIn(e["command_order"], orders)


if __name__ == "__main__":
    unittest.main()