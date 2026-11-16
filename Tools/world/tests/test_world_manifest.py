#!/usr/bin/env python3
"""Tests for the world manifest validator (W-M1).

These tests exist to prove the canon gate has teeth. Each one constructs a
manifest that a careless pipeline would happily build, and asserts rejection.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))

import canon_index as ci  # noqa: E402
import world_manifest as wm  # noqa: E402

MANIFEST_PATH = REPO_ROOT / "Tools" / "world" / "data" / "CH01_manifest.json"


def setUpModule() -> None:  # noqa: N802
    global INDEX, BASE
    INDEX = ci.load_index()
    BASE = wm.load_manifest(MANIFEST_PATH)


def fresh():
    return copy.deepcopy(BASE)


def loc(manifest, loc_id):
    return next(l for l in manifest["locations"] if l["id"] == loc_id)


class TestShippedManifestIsValid(unittest.TestCase):
    def test_chapter_one_manifest_has_no_violations(self):
        errors = wm.validate_manifest(BASE, INDEX)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_manifest_declares_a_real_chapter(self):
        self.assertEqual(BASE["chapter"], "CH01")

    def test_all_declared_locations_are_registered(self):
        registered = {l["id"] for l in INDEX["locations"]}
        for entry in BASE["locations"]:
            self.assertIn(entry["id"], registered)


class TestCanonStatusGate(unittest.TestCase):
    def test_final_art_on_unapproved_design_is_rejected(self):
        """CH01-ENV-001 is IN REVIEW, not APPROVED."""
        m = fresh()
        loc(m, "CH01-ENV-001")["art"] = "final"
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("final art requires design status" in e for e in errors), errors)

    def test_final_art_on_approved_design_is_allowed(self):
        m = fresh()
        m["locations"].append({"id": "CH08-SUB-007", "built": True, "art": "final",
                               "presented_as_canon": False, "gameplay": []})
        # Chapter mismatch is a separate, legitimate complaint; isolate the art rule.
        errors = wm.validate_manifest(m, INDEX)
        self.assertFalse(any("final art requires" in e for e in errors), errors)

    def test_proposed_location_cannot_be_presented_as_canon(self):
        """CH01-SUB-018 The Wayside Offering Place is PROPOSED."""
        m = fresh()
        loc(m, "CH01-SUB-018")["presented_as_canon"] = True
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("presented as canon but register status is" in e for e in errors), errors)

    def test_established_location_may_be_presented_as_canon(self):
        m = fresh()
        loc(m, "CH01-ENV-001")["presented_as_canon"] = True
        self.assertEqual(wm.validate_manifest(m, INDEX), [])

    def test_gameplay_on_proposed_location_requires_blockout(self):
        m = fresh()
        loc(m, "CH01-SUB-018")["gameplay"] = [{"kind": "quest"}]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("must declare blockout" in e for e in errors), errors)

    def test_gameplay_on_proposed_location_allowed_when_blockout(self):
        m = fresh()
        loc(m, "CH01-SUB-018")["gameplay"] = [{"kind": "quest", "blockout": True}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])

    def test_gameplay_on_established_location_needs_no_blockout_flag(self):
        m = fresh()
        loc(m, "CH01-SET-001")["gameplay"] = [{"kind": "interaction"}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])

    def test_unknown_gameplay_kind_is_rejected(self):
        m = fresh()
        loc(m, "CH01-SET-001")["gameplay"] = [{"kind": "microtransaction"}]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("unknown gameplay element kind" in e for e in errors), errors)

    def test_unregistered_location_is_rejected(self):
        m = fresh()
        m["locations"].append({"id": "CH01-SUB-999", "built": True, "gameplay": []})
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("not present in the canon index" in e for e in errors), errors)

    def test_location_from_another_chapter_is_rejected(self):
        m = fresh()
        m["locations"].append({"id": "CH02-SUB-003", "built": True, "gameplay": []})
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("belongs to CH02" in e for e in errors), errors)


class TestSceneValidation(unittest.TestCase):
    def test_scene_parent_must_be_registered(self):
        m = fresh()
        m["scenes"][0]["parent"] = "CH01-SUB-777"
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("is not a registered location" in e for e in errors), errors)

    def test_scene_in_wrong_chapter_is_rejected(self):
        m = fresh()
        m["scenes"][0]["id"] = "CH02-SCN-046"
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("belongs to CH02" in e for e in errors), errors)

    def test_scene_without_built_flag_is_rejected(self):
        m = fresh()
        del m["scenes"][0]["built"]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("missing required field 'built'" in e for e in errors), errors)


class TestCanonNpcRules(unittest.TestCase):
    def test_child_as_combat_target_is_rejected(self):
        """RULE-NPC-CHILDREN-NO-COMBAT."""
        m = fresh()
        m["scenes"][1]["npcs"] = [{"role": "child", "combat_target": True}]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("RULE-NPC-CHILDREN-NO-COMBAT" in e for e in errors), errors)

    def test_child_npc_without_combat_flag_is_allowed(self):
        m = fresh()
        m["scenes"][1]["npcs"] = [{"role": "child"}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])

    def test_child_allowed_in_home_settlement(self):
        m = fresh()
        m["scenes"][1]["npcs"] = [{"role": "child", "settlement": True}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])


class TestCanonChapterRules(unittest.TestCase):
    def test_snake_enemy_in_chapter_four_is_rejected(self):
        """RULE-CH04-PYTHONS, tested against a Chapter 4 manifest."""
        m = fresh()
        m["chapter"] = "CH04"
        m["locations"] = []
        m["scenes"] = [{
            "id": "CH04-SCN-001", "parent": "CH04-SUB-002", "built": True,
            "enemies": [{"type": "python"}],
        }]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("RULE-CH04-PYTHONS" in e for e in errors), errors)

    def test_snake_enemy_is_fine_in_another_chapter(self):
        """The rule is chapter-scoped, not global."""
        m = fresh()
        m["scenes"][1]["enemies"] = [{"type": "python"}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])

    def test_ordinary_enemy_passes(self):
        m = fresh()
        m["scenes"][1]["enemies"] = [{"type": "rootwarden"}]
        self.assertEqual(wm.validate_manifest(m, INDEX), [])


class TestEnvironmentStates(unittest.TestCase):
    def test_state_id_colliding_with_location_is_rejected(self):
        m = fresh()
        m["environment_states"].append({"id": "CH01-SUB-018", "parent": "CH01-SET-001"})
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("collides with a location id" in e for e in errors), errors)

    def test_state_parent_must_be_registered(self):
        m = fresh()
        m["environment_states"].append({"id": "ES_CH01_Dusk", "parent": "CH01-SUB-888"})
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("parent is not a registered location" in e for e in errors), errors)

    def test_valid_states_pass(self):
        self.assertEqual(wm.validate_manifest(fresh(), INDEX), [])


class TestRoutines(unittest.TestCase):
    def test_routine_location_must_be_registered(self):
        m = fresh()
        m["routines"][0]["steps"][0]["location"] = "CH01-INT-999"
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("unregistered location" in e for e in errors), errors)

    def test_overlapping_routine_steps_are_rejected(self):
        m = fresh()
        m["routines"][0]["steps"] = [
            {"start_hour": 5.0, "end_hour": 10.0, "location": "CH01-INT-007"},
            {"start_hour": 8.0, "end_hour": 12.0, "location": "CH01-SUB-012"},
        ]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("overlapping steps" in e for e in errors), errors)

    def test_invalid_hour_window_is_rejected(self):
        m = fresh()
        m["routines"][0]["steps"] = [
            {"start_hour": 18.0, "end_hour": 6.0, "location": "CH01-INT-007"},
        ]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("invalid window" in e for e in errors), errors)

    def test_empty_routine_is_rejected(self):
        m = fresh()
        m["routines"] = [{"actor": "nobody", "steps": []}]
        errors = wm.validate_manifest(m, INDEX)
        self.assertTrue(any("has no steps" in e for e in errors), errors)

    def test_routine_matches_register_description(self):
        """CH01-SCN-001: cooks at dawn and dusk, farms between."""
        routine = BASE["routines"][0]
        activities = [s.get("activity", "") for s in routine["steps"]]
        self.assertIn("Activity.Cook", activities)
        self.assertIn("Activity.Farm", activities)
        hours = [(s["start_hour"], s["end_hour"], s.get("activity")) for s in routine["steps"]]
        self.assertEqual(hours[0][2], "Activity.Cook", "first step must be the dawn cook")
        self.assertEqual(hours[-1][2], "Activity.Cook", "last step must be the dusk cook")


class TestCoverage(unittest.TestCase):
    def test_covered_locations_counts_by_category(self):
        counts = wm.covered_locations(BASE)
        self.assertEqual(counts["ENV"], 1)
        self.assertEqual(counts["BOS"], 1)
        self.assertEqual(sum(counts.values()), len(BASE["locations"]))

    def test_world_counts_from_register_are_recorded(self):
        counts = INDEX["world_counts_from_register"]
        self.assertEqual(counts["major_environments"], 8)
        self.assertEqual(counts["scenes_and_microlocations"], 135)
        self.assertEqual(sum(counts["per_chapter_scenes"].values()), 135)

    def test_chapter_one_scope_is_far_larger_than_manifest(self):
        """Documents the honest gap: the vertical slice declares 6 of 68
        Chapter 1 location entries."""
        self.assertEqual(INDEX["world_counts_from_register"]["per_chapter_scenes"]["CH01"], 46)
        self.assertLess(len(BASE["locations"]), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
