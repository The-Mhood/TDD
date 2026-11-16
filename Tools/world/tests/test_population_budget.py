#!/usr/bin/env python3
"""Tests for the traceable population budget (TR-1).

The point of these tests is that the budget must be *derivable* and *auditable*:
every tier assignment must trace to either a register row or a named policy rule,
and a policy gap must surface as a validation failure rather than a silent zero.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import population_budget as pb  # noqa: E402
import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"


def setUpModule() -> None:  # noqa: N802
    global SCENES, DETAILS, POLICY, BUDGET
    # The default source must match the one the evidence artifact is built from,
    # or the doc-consistency tests compare against a different world. The abridged
    # fixture is preserved and pinned separately by test_scene_capture.py.
    text = pb.FIXTURE_VERBATIM.read_text(encoding="utf-8")
    SCENES = reg.parse_scene_summary(text)
    DETAILS = reg.parse_scene_details(text)
    POLICY = pb.load_policy()
    BUDGET = pb.build_chapter_budget(SCENES, DETAILS, POLICY, "CH01")


def fresh_policy():
    return copy.deepcopy(POLICY)


class TestPolicyIsWellFormed(unittest.TestCase):
    def test_policy_declares_itself_provisional(self):
        self.assertIn("PROVISIONAL", POLICY["meta"]["status"])

    def test_policy_states_the_separation_rule(self):
        """Register data and engineering assumptions must never mix silently."""
        rule = POLICY["meta"]["separation_rule"]
        self.assertIn("ONLY engineering assumptions", rule)
        self.assertIn("may be presented as coming from the register", rule)

    def test_every_tier_mapped_has_a_definition(self):
        tiers = {rule["tier"] for rule in POLICY["scene_category_tiers"].values()}
        tiers.add(POLICY["unmapped_category_fallback"]["tier"])
        for tier in tiers:
            self.assertIn(tier, POLICY["tier_definitions"], f"tier {tier} undefined")

    def test_every_mapping_states_rationale_and_confidence(self):
        for category, rule in POLICY["scene_category_tiers"].items():
            self.assertTrue(rule.get("rationale"), category)
            self.assertTrue(rule.get("confidence"), category)

    def test_fallback_is_not_free(self):
        """An unmapped category must not be silently treated as zero cost."""
        self.assertNotEqual(POLICY["unmapped_category_fallback"]["tier"], "NONE")

    def test_cost_units_are_explicitly_not_a_frame_time_claim(self):
        note = POLICY["cost_units"]["_note"]
        self.assertIn("NOT milliseconds", note)
        self.assertIn("replaced by measured cost", note.lower())


class TestChapterOneBudget(unittest.TestCase):
    def test_all_46_scenes_budgeted(self):
        self.assertEqual(BUDGET.scenes_total, 46)
        self.assertEqual(len(BUDGET.scenes), 46)

    def test_category_counts_match_the_register_count_table(self):
        """The register's own Chapter 1 totals: 14 ambient, 4 enterable, 6 micro,
        4 environmental, 2 exploration, 8 world activity, 7 atmospheric, 1 secondary."""
        self.assertEqual(BUDGET.by_category["AMBIENT NPC SCENE"], 14)
        self.assertEqual(BUDGET.by_category["WORLD ACTIVITY SCENE"], 8)
        self.assertEqual(BUDGET.by_category["ATMOSPHERIC SCENE"], 7)
        self.assertEqual(BUDGET.by_category["EXTERIOR MICRO-LOCATION"], 6)
        self.assertEqual(BUDGET.by_category["ENVIRONMENTAL STORYTELLING"], 4)
        self.assertEqual(BUDGET.by_category["ENTERABLE INTERIOR"], 4)
        self.assertEqual(BUDGET.by_category["EXPLORATION SCENE"], 2)
        self.assertEqual(BUDGET.by_category["SECONDARY STORY SCENE"], 1)
        self.assertEqual(sum(BUDGET.by_category.values()), 46)

    def test_most_scenes_do_not_get_a_simulated_npc(self):
        """The Technical Director's core concern: do not assume every ambient
        activity needs an individually simulated NPC."""
        no_simulation = BUDGET.by_tier.get("NONE", 0) + BUDGET.by_tier.get("SCRIPTED", 0)
        self.assertGreater(no_simulation, 30,
                           "expected the large majority of scenes to need no full NPC simulation")
        self.assertLessEqual(BUDGET.by_tier.get("CROWD", 0), 16)

    def test_environmental_storytelling_gets_no_npcs(self):
        """These scenes are about absence; adding a person contradicts them."""
        for scene in BUDGET.scenes:
            if scene.category == "ENVIRONMENTAL STORYTELLING":
                self.assertEqual(scene.tier, "NONE", scene.scene_id)

    def test_world_activity_uses_scripted_not_crowd(self):
        for scene in BUDGET.scenes:
            if scene.category == "WORLD ACTIVITY SCENE":
                self.assertEqual(scene.tier, "SCRIPTED", scene.scene_id)

    def test_ambient_npc_scenes_use_crowd(self):
        for scene in BUDGET.scenes:
            if scene.category == "AMBIENT NPC SCENE":
                self.assertEqual(scene.tier, "CROWD", scene.scene_id)

    def test_memory_scene_is_named_tier(self):
        memory = next(s for s in BUDGET.scenes if s.scene_id == "CH01-SCN-046")
        self.assertEqual(memory.tier, "NAMED")
        self.assertEqual(memory.canon_status, "PENDING APPROVAL")

    def test_every_scene_records_its_tier_source(self):
        for scene in BUDGET.scenes:
            self.assertTrue(scene.tier_source.startswith(("policy:", "fallback")))

    def test_budget_is_valid_against_chapter_limits(self):
        self.assertEqual(pb.validate_budget(BUDGET, POLICY), [])

    def test_total_cost_within_ceiling(self):
        self.assertLessEqual(BUDGET.total_cost_units, POLICY["chapter_limits"]["max_total_cost_units"])


class TestRegisterTraceability(unittest.TestCase):
    def test_register_npc_count_used_where_available(self):
        """CH01-SCN-001 depicts 'One woman, one child.' -> 2."""
        scene = next(s for s in BUDGET.scenes if s.scene_id == "CH01-SCN-001")
        self.assertEqual(scene.npcs_from_register, 2)
        self.assertEqual(scene.npcs_source, "register")

    def test_child_detected_from_register_prose(self):
        scene = next(s for s in BUDGET.scenes if s.scene_id == "CH01-SCN-001")
        self.assertTrue(scene.has_child)

    def test_atmospheric_scene_with_a_child_is_detected(self):
        """CH01-SCN-025 'Goats at Dusk' depicts 'One boy' — atmospheric does not
        mean empty. This is the case that proves the category default alone is
        insufficient."""
        scene = next(s for s in BUDGET.scenes if s.scene_id == "CH01-SCN-025")
        self.assertEqual(scene.npcs_from_register, 1)
        self.assertTrue(scene.has_child)

    def test_scene_without_detail_block_is_marked_policy_default(self):
        """A scene with no captured prose must fall back to the category default
        and SAY SO, rather than quietly looking like register data.

        Named a specific scene until the W-M2.2 capture, which resolved it. The
        test now discovers any scene that genuinely has no prose, so it keeps
        testing the fallback path instead of a fixed ID that may later be
        captured.
        """
        captured = {d.id for d in DETAILS if d.npcs_present}
        uncaptured = [s for s in BUDGET.scenes if s.scene_id not in captured]
        self.assertTrue(uncaptured,
                        "expected some Chapter 1 scene to remain uncaptured")
        for scene in uncaptured:
            self.assertEqual(scene.npcs_source, "policy_default", scene.scene_id)
            self.assertTrue(any("policy default" in n for n in scene.notes),
                            f"{scene.scene_id} must state that its count is a default")
        # And the converse: a captured scene must NOT be on a default.
        for scene in BUDGET.scenes:
            if scene.scene_id in captured:
                self.assertIn(scene.npcs_source, {"register", "unparsed"},
                              f"{scene.scene_id} has prose but is on a default")

    def test_unparseable_npc_prose_is_flagged_not_zeroed(self):
        policy = fresh_policy()
        scene = reg.SceneRecord(
            id="CH01-SCN-999", name="Test", parent_id="CH01-ENV-001",
            scene_kind="AMBIENT NPC SCENE", access="OPEN EXTERIOR",
            canon_status="PROPOSED", chapter="CH01")
        detail = reg.SceneDetail(
            id="CH01-SCN-999", scene_kind="AMBIENT NPC SCENE",
            npcs_present="A gathering of unspecified size.")
        budget = pb.build_chapter_budget([scene], [detail], policy, "CH01")
        self.assertIn("CH01-SCN-999", budget.unparsed_npc_scenes)

        # Never silently zero, and never silently pass. The scene must be named,
        # and the reason it could not be resolved must be recorded on the row.
        self.assertTrue(pb.validate_budget(budget, policy)
                        + pb.budget_warnings(budget),
                        "an unparseable NPC field must never pass silently")
        row = {s.scene_id: s for s in budget.scenes}["CH01-SCN-999"]
        self.assertEqual(row.npcs_source, "unparsed")
        self.assertTrue(row.npcs_band_basis,
                        "the resolution basis must be recorded, even when it resolves "
                        "to 'no bound stated'")


class TestPolicyGapsSurface(unittest.TestCase):
    def test_fallback_use_is_reported(self):
        policy = fresh_policy()
        scene = reg.SceneRecord(
            id="CH01-SCN-998", name="Test", parent_id="CH01-ENV-001",
            scene_kind="SOME NEW CATEGORY", access="OPEN EXTERIOR",
            canon_status="PROPOSED", chapter="CH01")
        budget = pb.build_chapter_budget([scene], [], policy, "CH01")
        self.assertEqual(budget.scenes[0].tier, policy["unmapped_category_fallback"]["tier"])
        problems = pb.validate_budget(budget, policy)
        self.assertTrue(any("no tier mapping" in p for p in problems), problems)

    def test_crowd_scene_ceiling_is_enforced(self):
        policy = fresh_policy()
        policy["chapter_limits"]["max_crowd_scenes"] = 2
        problems = pb.validate_budget(BUDGET, policy)
        self.assertTrue(any("crowd scenes exceeds ceiling" in p for p in problems), problems)

    def test_cost_ceiling_is_enforced(self):
        policy = fresh_policy()
        policy["chapter_limits"]["max_total_cost_units"] = 1.0
        problems = pb.validate_budget(BUDGET, policy)
        self.assertTrue(any("total cost" in p and "exceeds" in p for p in problems), problems)


class TestAccessMultiplier(unittest.TestCase):
    def test_background_access_reduces_cost(self):
        policy = fresh_policy()
        self.assertLess(pb.tier_for_access(policy, "BACKGROUND ENVIRONMENT"),
                        pb.tier_for_access(policy, "FULLY ENTERABLE"))

    def test_unknown_access_falls_back_to_one(self):
        policy = fresh_policy()
        self.assertEqual(pb.tier_for_access(policy, "TELEPORTING"), 1.0)

    def test_hornbills_background_scene_is_cheap(self):
        """CH01-SCN-042 is BACKGROUND ENVIRONMENT."""
        scene = next(s for s in BUDGET.scenes if s.scene_id == "CH01-SCN-042")
        self.assertEqual(scene.access, "BACKGROUND ENVIRONMENT")
        self.assertLess(scene.simulated_cost, 1.0)


class TestBudgetIsLabelledProvisional(unittest.TestCase):
    def test_evidence_output_says_provisional_and_unmeasured(self):
        path = REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json"
        self.assertTrue(path.is_file(), "run Tools/world/population_budget.py --out ...")
        data = json.loads(path.read_text())
        self.assertIn("PROVISIONAL", data["meta"]["status"])
        self.assertIn("No simulation has run", data["meta"]["caveat"])
        self.assertIn("NOT measured", data["meta"]["status"])

    def test_evidence_records_register_and_policy_sources(self):
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json")
            .read_text())
        self.assertIn("SCENE_AND_MICROLOCATION", data["meta"]["register_source"])
        self.assertIn("population_policy.json", data["meta"]["policy_source"])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestDocsAgreeWithPolicyData(unittest.TestCase):
    """Documentation drift is real: this milestone produced an architecture table
    with invented cost units (6.0/0.45/1.0/0.15) that contradicted the policy file
    (4.0/1.0/0.3/0.05). These tests keep prose honest against the data it cites."""

    def setUp(self):
        self.doc = (REPO_ROOT / "Docs" / "WORLD_ARCHITECTURE.md").read_text(encoding="utf-8")
        self.policy = POLICY

    def test_cost_units_in_doc_match_policy(self):
        for tier, value in self.policy["cost_units"].items():
            if tier.startswith("_"):
                continue
            if value == 0:
                continue
            self.assertIn(str(value), self.doc,
                          f"cost unit {value} for {tier} not found in architecture doc")

    def test_doc_does_not_claim_three_tiers(self):
        self.assertNotIn("three-tier NPC model", self.doc)
        self.assertNotIn("Three-tier population", self.doc)

    def test_doc_names_all_five_tiers(self):
        for tier in ("NAMED", "CROWD", "SCRIPTED", "BACKGROUND", "NONE"):
            self.assertIn(tier, self.doc, f"tier {tier} not documented")

    def test_doc_derived_budget_matches_evidence(self):
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json")
            .read_text())
        budget = data["budget"]
        for key, doc_fragment in [
            ("scenes_total", str(budget["scenes_total"])),
            ("crowd_peak_estimate", str(budget["crowd_peak_estimate"])),
        ]:
            self.assertIn(doc_fragment, self.doc,
                          f"{key}={doc_fragment} from evidence is not reflected in "
                          f"Docs/WORLD_ARCHITECTURE.md")

    def test_doc_states_no_simulation_majority(self):
        """The headline finding: most scenes need no simulated agent."""
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json")
            .read_text())
        tiers = data["budget"]["by_tier"]
        no_sim = tiers.get("NONE", 0) + tiers.get("SCRIPTED", 0)
        self.assertIn(f"{no_sim} of {data['budget']['scenes_total']}", self.doc)
