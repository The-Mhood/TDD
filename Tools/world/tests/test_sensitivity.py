#!/usr/bin/env python3
"""Tests for the population sensitivity report.

The report's value is that it tells the truth about its own uncertainty. These
tests assert the properties that make that true: facts and assumptions are
separated, the structural finding holds, and the model responds monotonically
where it should.
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
import sensitivity as sens  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
EVIDENCE = REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_sensitivity.json"


def setUpModule() -> None:  # noqa: N802
    global SCENES, DETAILS, POLICY, REPORT
    text = (FIXTURES / "scene_register_ch01_full.md").read_text(encoding="utf-8")
    SCENES = reg.parse_scene_summary(text)
    DETAILS = reg.parse_scene_details(text)
    POLICY = pb.load_policy()
    REPORT = sens.build_report(SCENES, DETAILS, POLICY)


class TestFactsAreSeparatedFromAssumptions(unittest.TestCase):
    def test_report_has_explicit_facts_and_assumptions_sections(self):
        self.assertIn("facts", REPORT)
        self.assertIn("assumptions", REPORT)
        self.assertIn("assumption_dependence", REPORT)

    def test_facts_record_register_coverage(self):
        facts = REPORT["facts"]
        self.assertEqual(facts["scenes_with_register_npc_data"], 5)
        self.assertEqual(facts["scenes_total"], 46)

    def test_coverage_is_low_and_reported_as_low(self):
        """The headline honesty check: most of the estimate is not register data."""
        self.assertLess(REPORT["facts"]["coverage_ratio"], 0.2)
        self.assertGreater(
            REPORT["assumption_dependence"]["share_of_cost_from_policy_defaults"], 0.5)

    def test_every_fact_row_names_a_scene(self):
        for row in REPORT["facts"]["detail"]:
            self.assertRegex(row["scene_id"], r"^CH01-SCN-\d{3}$")

    def test_assumptions_section_admits_no_register_basis(self):
        self.assertIn("no register basis", REPORT["assumptions"]["_note"].lower())

    def test_meta_states_not_measured(self):
        self.assertIn("not a measurement", REPORT["meta"]["status"].lower())


class TestStructuralFinding(unittest.TestCase):
    def test_scripted_sweep_is_inert(self):
        """Scripted scenes are flat per-scene cost. If this ever moves, the cost
        model changed and needs review."""
        block = REPORT["sensitivity"]["expected_npcs_for_scripted"]
        self.assertEqual(block["elasticity"], 0.0)
        costs = {p["total_cost_units"] for p in block["points"]}
        self.assertEqual(len(costs), 1, costs)

    def test_only_crowd_scenes_are_sensitive(self):
        crowd = REPORT["sensitivity"]["expected_npcs_for_policy_defaults"]
        self.assertGreater(abs(crowd["elasticity"]), 0.1)

    def test_crowd_scene_count_is_14(self):
        baseline = sens._rebuild(POLICY, SCENES, DETAILS)
        self.assertEqual(baseline.by_tier["CROWD"], 14)

    def test_twelve_of_fourteen_crowd_scenes_are_policy_defaults(self):
        baseline = sens._rebuild(POLICY, SCENES, DETAILS)
        crowd_default = [s for s in baseline.scenes
                         if s.tier == "CROWD" and s.npcs_source == "policy_default"]
        self.assertEqual(len(crowd_default), 12)


class TestElasticity(unittest.TestCase):
    def test_elasticity_uses_neighbours_not_extremes(self):
        """A previous version used the closest and farthest points, which made a
        quantized sweep report a meaningless slope. With points at 1,2,3,10 the
        neighbours of baseline 3 are 2 and 10, NOT 1 and 10.

        Neighbour central difference: (cost(10)-cost(2))/cost(2) divided by
        (10-2)/3 = (100-20)/20 / 2.6667 = 4.0/2.6667 = 1.5
        Extreme difference would give (100-10)/10 / ((10-1)/3) = 9/3 = 3.0
        """
        points = [
            sens.SensitivityPoint("p", 1, 10.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 2, 20.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 3, 20.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 10, 100.0, 0, 0, 0.0, 0.0),
        ]
        self.assertAlmostEqual(sens.elasticity(points, 3.0), 1.5, places=3)

    def test_returns_zero_when_no_point_above_baseline(self):
        points = [
            sens.SensitivityPoint("p", 1, 10.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 2, 20.0, 0, 0, 0.0, 0.0),
        ]
        self.assertEqual(sens.elasticity(points, 2.0), 0.0)

    def test_central_difference_between_immediate_neighbours(self):
        points = [
            sens.SensitivityPoint("p", 1, 10.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 2, 20.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 3, 30.0, 0, 0, 0.0, 0.0),
        ]
        # (30-10)/10 = 2.0 ; (3-1)/2 = 1.0 -> 2.0
        self.assertAlmostEqual(sens.elasticity(points, 2.0), 2.0, places=3)

    def test_zero_elasticity_when_costs_identical(self):
        points = [
            sens.SensitivityPoint("p", 1, 5.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 2, 5.0, 0, 0, 0.0, 0.0),
            sens.SensitivityPoint("p", 3, 5.0, 0, 0, 0.0, 0.0),
        ]
        self.assertEqual(sens.elasticity(points, 2.0), 0.0)


class TestQuantizationIsReported(unittest.TestCase):
    def test_quantization_detected_and_explained(self):
        block = REPORT["sensitivity"]["expected_npcs_for_policy_defaults"]
        q = block["quantization"]
        self.assertTrue(q["is_quantized"])
        self.assertTrue(q["flat_intervals"])
        self.assertIn("rounded to whole numbers", q["cause"])

    def test_plateau_is_physically_justified_not_hidden(self):
        """ceil(2*0.75) == ceil(2*1.0) == 2. You cannot simulate 2.25 actors."""
        import math
        self.assertEqual(math.ceil(2 * 0.75), math.ceil(2 * 1.0))


class TestRoundingIsConservative(unittest.TestCase):
    def test_crowd_estimation_rounds_up(self):
        """Banker's rounding made 2 and 3 depicted people cost the same, and could
        round cost downward. Budgets must round up."""
        policy = copy.deepcopy(POLICY)
        policy["crowd_concurrency_ratio"]["AMBIENT NPC SCENE"] = 0.75
        self.assertEqual(pb._estimate_crowd(2, policy, "AMBIENT NPC SCENE"), 2)
        self.assertEqual(pb._estimate_crowd(3, policy, "AMBIENT NPC SCENE"), 3)

    def test_three_people_costs_more_than_two(self):
        policy = copy.deepcopy(POLICY)
        self.assertGreater(pb._estimate_crowd(3, policy, "AMBIENT NPC SCENE"),
                           pb._estimate_crowd(2, policy, "AMBIENT NPC SCENE"))

    def test_zero_stays_zero(self):
        self.assertEqual(pb._estimate_crowd(0, POLICY, "AMBIENT NPC SCENE"), 0)


class TestScenarios(unittest.TestCase):
    def test_five_scenarios_present(self):
        self.assertEqual(len(REPORT["scenarios"]), 5)

    def test_baseline_scenario_matches_baseline(self):
        base = next(s for s in REPORT["scenarios"] if s["scenario"] == "BASELINE")
        self.assertEqual(base["total_cost_units"], REPORT["baseline"]["total_cost_units"])

    def test_cost_increases_monotonically_with_density(self):
        ordered = [s for s in REPORT["scenarios"]]
        costs = [s["total_cost_units"] for s in ordered]
        self.assertEqual(costs, sorted(costs), costs)

    def test_spread_is_reported(self):
        costs = [s["total_cost_units"] for s in REPORT["scenarios"]]
        self.assertGreater(max(costs) / min(costs), 2.0)

    def test_ceiling_headroom_computed(self):
        c = REPORT["ceiling"]
        self.assertEqual(c["chapter_ceiling"], 60.0)
        self.assertTrue(c["all_scenarios_within_ceiling"])


class TestCaptureStatusIsDistinguished(unittest.TestCase):
    def test_scenes_complete_locations_partial(self):
        cap = REPORT["capture_status"]
        self.assertIn("COMPLETE", cap["scenes"])
        self.assertIn("PARTIAL", cap["locations"])

    def test_report_warns_it_covers_scenes_only(self):
        self.assertIn("scenes only", REPORT["capture_status"]["warning"])

    def test_budget_artifact_carries_same_distinction(self):
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json")
            .read_text())
        cap = data["meta"]["capture_status"]
        self.assertIn("COMPLETE", cap["scenes"])
        self.assertIn("PARTIAL", cap["locations"])


class TestEvidenceArtifactMatchesCode(unittest.TestCase):
    def test_artifact_exists(self):
        self.assertTrue(EVIDENCE.is_file(), "run Tools/world/sensitivity.py --out ...")

    def test_artifact_states_provisional(self):
        data = json.loads(EVIDENCE.read_text())
        self.assertIn("PROVISIONAL", data["meta"]["status"])

    def test_artifact_baseline_matches_live_computation(self):
        data = json.loads(EVIDENCE.read_text())
        self.assertEqual(data["baseline"]["total_cost_units"],
                         REPORT["baseline"]["total_cost_units"])

    def test_artifact_facts_match_live_computation(self):
        data = json.loads(EVIDENCE.read_text())
        self.assertEqual(data["facts"]["scenes_with_register_npc_data"],
                         REPORT["facts"]["scenes_with_register_npc_data"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
