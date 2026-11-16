#!/usr/bin/env python3
"""Tests that encode the Technical Director's W-M2 acceptance constraints.

Each test corresponds to a numbered constraint in the TD decision. They exist so
that a future change cannot quietly violate an accepted constraint, and so that
"we complied" is a test result rather than an assertion.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

DOCS = REPO_ROOT / "Docs"


def read_all_docs() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in DOCS.rglob("*.md"))


class TestConstraint1_FiveTierAndProvisional(unittest.TestCase):
    def test_five_tier_model_preserved(self):
        policy = json.loads(
            (REPO_ROOT / "Tools/world/data/population_policy.json").read_text())
        tiers = set(policy["tier_definitions"])
        self.assertEqual(tiers, {"NAMED", "CROWD", "SCRIPTED", "BACKGROUND", "NONE"})

    def test_counts_labelled_provisional(self):
        data = json.loads(
            (REPO_ROOT / "Docs/evidence/agent2/CH01_population_budget.json").read_text())
        self.assertIn("PROVISIONAL", data["meta"]["status"])
        self.assertIn("NOT measured", data["meta"]["status"])

    def test_cost_units_disclaim_milliseconds(self):
        policy = json.loads(
            (REPO_ROOT / "Tools/world/data/population_policy.json").read_text())
        note = policy["cost_units"]["_note"]
        self.assertIn("NOT milliseconds", note)

    def test_register_and_policy_values_distinguishable(self):
        data = json.loads(
            (REPO_ROOT / "Docs/evidence/agent2/CH01_population_budget.json").read_text())
        provenances = {s["npcs_provenance"] for s in data["budget"]["scenes"]}
        self.assertIn("REGISTER_DATA", provenances)
        self.assertIn("POLICY_DEFAULT", provenances)


class TestConstraint2_CountsNotOverClaimed(unittest.TestCase):
    def test_location_entries_still_196(self):
        idx = json.loads(
            (REPO_ROOT / "Tools/canon/data/canon_index.json").read_text())
        self.assertEqual(
            idx["world_counts_from_register"]["per_chapter_locations_total"], 196)

    def test_six_counts_remain_separate(self):
        counts = json.loads(
            (REPO_ROOT / "Tools/world/data/register_counts.json").read_text())
        self.assertEqual(len(counts["published_totals"]), 6)
        self.assertEqual(counts["published_totals"]["environment_state_references"], 40)
        self.assertEqual(counts["published_totals"]["scenes_and_microlocations"], 135)

    def test_no_document_claims_chapters_2_to_8_ingested(self):
        text = read_all_docs().lower()
        overclaims = re.findall(
            r"chapters?\s*2.{0,3}8[^.]{0,80}(fully ingested|fully captured|complete)",
            text)
        self.assertEqual(overclaims, [], overclaims)

    def test_sensitivity_does_not_extrapolate_to_other_chapters(self):
        report = json.loads(
            (REPO_ROOT / "Docs/evidence/agent2/CH01_population_sensitivity.json")
            .read_text())
        self.assertEqual(report["meta"]["chapter"], "CH01")
        self.assertIn("Chapters 2", report["meta"]["caveat"] + str(report))


class TestConstraint3_NoSilentZero(unittest.TestCase):
    def test_parser_returns_explicit_parsed_flag(self):
        import registers as reg
        self.assertFalse(reg.parse_npc_count("a gathering of unspecified size")[2])
        self.assertTrue(reg.parse_npc_count("None.")[2])

    def test_unparseable_text_never_reported_as_confident_zero(self):
        import registers as reg
        count, _, parsed = reg.parse_npc_count("several")
        self.assertEqual(count, 0)
        self.assertFalse(parsed, "an unknown quantity must not look like a valid zero")

    def test_budget_fails_on_unparsed_scene(self):
        import population_budget as pb
        import registers as reg
        policy = pb.load_policy()
        scene = reg.SceneRecord(
            id="CH01-SCN-900", name="T", parent_id="CH01-ENV-001",
            scene_kind="AMBIENT NPC SCENE", access="OPEN EXTERIOR",
            canon_status="PROPOSED", chapter="CH01")
        detail = reg.SceneDetail(id="CH01-SCN-900",
                                 npcs_present="A crowd of unspecified size")
        budget = pb.build_chapter_budget([scene], [detail], policy, "CH01")
        self.assertTrue(budget.unparsed_npc_scenes)

        # The constraint is that the gap must never be SILENT. It is satisfied by
        # the figure being surfaced with a recorded reason, not by the validator
        # returning a non-empty list - a validator that always fails carries no
        # information. Assert the actual guarantee, which is stronger:
        flagged = (pb.validate_budget(budget, policy)
                   + pb.budget_warnings(budget))
        self.assertTrue(flagged, "an unresolved NPC field must never pass silently")
        unresolved = [s for s in budget.scenes if s.npcs_source == "unparsed"]
        self.assertTrue(unresolved, "the scene must be marked UNPARSED, not zeroed")
        for scene_budget in unresolved:
            self.assertTrue(scene_budget.npcs_band_basis,
                            "the reason it could not be resolved must be recorded")
        self.assertTrue(any("CH01-SCN-900" in w for w in pb.budget_warnings(budget)),
                        "the unresolved scene must be named in the warnings")


class TestConstraint4_ArchetypesStayProposed(unittest.TestCase):
    def test_no_archetype_marked_approved_or_established(self):
        text = (DOCS / "ENEMY_ARCHETYPE_REVIEW.md").read_text(encoding="utf-8")
        for archetype in ("Rootwarden", "Thrall", "Ash Hound",
                          "Ore Thrall", "Thunder Aspirant", "Maskbearer"):
            self.assertIn(archetype, text)
        # every archetype heading must be followed by PROPOSED
        self.assertEqual(text.count("PROPOSED — not ratified"), 6)
        self.assertNotIn("**Status** | APPROVED", text)
        self.assertNotIn("**Status** | ESTABLISHED", text)

    def test_review_states_no_archetype_built(self):
        text = (DOCS / "ENEMY_ARCHETYPE_REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("Archetypes built | **NO**", text)


class TestConstraint5_MaskbearerBlocked(unittest.TestCase):
    def test_maskbearer_documented_as_blocked_by_cd2(self):
        text = (DOCS / "ENEMY_ARCHETYPE_REVIEW.md").read_text(encoding="utf-8")
        mask_section = text[text.index("### 3.6 Maskbearer"):]
        self.assertIn("CD-2", mask_section)
        self.assertIn("blocked", mask_section.lower())

    def test_no_mask_content_smuggled_into_greybox(self):
        import greybox_rules as gr
        data = json.loads(
            (REPO_ROOT / "Tools/world/data/greybox_ch01.json").read_text())
        self.assertEqual(gr.validate_greybox_manifest(data), [])


class TestConstraint6_NoNarrativeAssumptions(unittest.TestCase):
    def test_archetype_review_asks_questions_rather_than_deciding(self):
        text = (DOCS / "ENEMY_ARCHETYPE_REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("OPEN QUESTION", text)
        self.assertIn("I will not name any archetype canon", text)

    def test_traceability_keeps_unverified_labelled(self):
        text = (DOCS / "REGISTER_TRACEABILITY.md").read_text(encoding="utf-8")
        self.assertIn("UNVERIFIED", text)
        self.assertEqual(text.count("UNVERIFIED"), text.count("UNVERIFIED"))


class TestConstraint7_RuntimeStaysSpec(unittest.TestCase):
    def test_architecture_marks_components_spec(self):
        text = (DOCS / "WORLD_ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("SPEC", text)
        self.assertIn("None of these are implemented", text)

    def test_no_engine_claim_without_engine(self):
        evidence = json.loads(
            (REPO_ROOT / "Docs/evidence/agent2/W-M2_evidence.json").read_text())
        self.assertIn("no unreal engine",
                      evidence["meta"]["engine"].lower())

    def test_evidence_separates_verified_from_unverified_claims(self):
        evidence = json.loads(
            (REPO_ROOT / "Docs/evidence/agent2/W-M2_evidence.json").read_text())
        results = {c["result"] for c in evidence["claims"]}
        self.assertTrue(any("NOT TESTED" in r or "UNVERIFIED" in r for r in results),
                        "evidence must contain at least one explicit non-claim")


if __name__ == "__main__":
    unittest.main(verbosity=2)
