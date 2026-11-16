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
    # Must use the SAME source the artifact is generated from, or the test
    # compares a live computation against a stale fixture and fails for the
    # wrong reason. The abridged fixture is preserved and still exercised by
    # Tools/world/tests/test_scene_capture.py.
    text = (FIXTURES / sens.FIXTURE_VERBATIM.name).read_text(encoding="utf-8")
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
        # Post-capture: 28 scenes resolve to an exact head-count and 7 more
        # carry register prose that states only a bound. Both are register data;
        # only the first is a point value, and the report keeps them apart.
        self.assertEqual(facts["scenes_with_register_npc_data"], 29)
        self.assertEqual(facts["scenes_with_register_prose_unresolved"], 6)
        self.assertEqual(facts["scenes_total"], 46)

    def test_coverage_is_reported_honestly(self):
        """Coverage rose, so the old 'under 20%' assertion must change.

        The honesty requirement is that the report STATES its coverage and its
        remaining assumption dependence, not that the number stays low. Asserting
        a specific low number would make the test fire when the data improves,
        which is the opposite of what it is for.
        """
        facts = REPORT["facts"]
        dependence = REPORT["assumption_dependence"]

        # Prose coverage is now a majority of the chapter...
        self.assertGreater(facts["prose_capture_ratio"], 0.5)
        self.assertGreater(facts["coverage_ratio"], 0.5)

        # ...and the cost attributable to UNCAPPED scenes collapsed, because all
        # of them are flat-cost tiers. What survives as assumption is the policy
        # parameter values themselves (cost unit, concurrency ratio), not the
        # per-scene NPC defaults. Both facts must be reported, and neither may be
        # allowed to masquerade as the other.
        self.assertLess(dependence["share_of_cost_from_policy_defaults"], 0.1,
                        "flat-tier scenes should carry almost no cost")
        self.assertGreater(dependence["share_of_cost_from_unresolved_register"], 0.0,
                           "the unresolved register bounds must still be visible")
        self.assertIn("not a measurement", REPORT["meta"]["status"].lower())
        # The model is still assumption-driven - just through different parameters.
        self.assertFalse(REPORT["conclusion"]["estimate_is_mostly_assumption"])

    def test_uncaptured_scenes_are_count_independent(self):
        """Undercutting the coverage figure honestly: the 11 remaining scenes
        cannot move the total, because their tiers are flat or zero cost."""
        uncaptured = REPORT["facts"]["uncaptured_detail"]
        self.assertEqual(len(uncaptured), 11)
        for row in uncaptured:
            self.assertTrue(row["count_independent"],
                            f"{row['scene_id']} is {row['tier']} and must be "
                            f"count-independent, or the coverage gap matters")

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

    def test_crowd_default_sweep_is_now_inert(self):
        """The capture's whole point: the ambient NPC default no longer matters.

        Before capture this elasticity was +0.88, because 12 of 14 crowd scenes
        were billed at the default. Every crowd scene now has register prose, so
        the sweep must be flat. If this ever becomes non-zero again, a scene has
        silently regressed to a policy default.
        """
        crowd = REPORT["sensitivity"]["expected_npcs_for_policy_defaults"]
        self.assertEqual(crowd["elasticity"], 0.0)
        costs = {p["total_cost_units"] for p in crowd["points"]}
        self.assertEqual(len(costs), 1, costs)

    def test_crowd_scene_count_is_14(self):
        baseline = sens._rebuild(POLICY, SCENES, DETAILS)
        self.assertEqual(baseline.by_tier["CROWD"], 14)

    def test_no_crowd_scene_is_on_a_policy_default(self):
        """Was 12 of 14 before the capture; must now be zero."""
        baseline = sens._rebuild(POLICY, SCENES, DETAILS)
        crowd_default = [s for s in baseline.scenes
                         if s.tier == "CROWD" and s.npcs_source == "policy_default"]
        self.assertEqual(crowd_default, [],
                         "every CROWD scene must rest on register prose")


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

    def test_spread_is_reported_and_narrowed(self):
        """Spread fell from 2.5x to ~1.4x because the capture removed the
        dominant assumption. A spread still exists, so the model is still
        assumption-sensitive - it is just much less so."""
        costs = [s["total_cost_units"] for s in REPORT["scenarios"]]
        spread = max(costs) / min(costs)
        self.assertGreater(spread, 1.2, "assumptions must still visibly matter")
        self.assertLess(spread, 2.0, "the capture was supposed to narrow this")

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


class TestReportDocMatchesArtifact(unittest.TestCase):
    """Doc/code drift has been caught twice in this project. The report is prose,
    so nothing stops it describing a world that no longer exists. These checks
    tie every headline number in the report to the generated artifact.
    """

    @classmethod
    def setUpClass(cls):
        raw = (REPO_ROOT / "Docs" / "POPULATION_SENSITIVITY_REPORT.md"
               ).read_text(encoding="utf-8")
        # Strip emphasis so wording checks test the prose, not the markup. A
        # test that breaks when an editor adds italics is testing markdown.
        cls.doc = raw.replace("**", "").replace("*", "").replace("`", "")
        cls.data = json.loads(EVIDENCE.read_text())

    def test_baseline_figures_appear(self):
        baseline = self.data["baseline"]
        for key in ("total_cost_units", "simulated_npcs", "crowd_peak"):
            self.assertIn(str(baseline[key]), self.doc,
                          f"baseline {key}={baseline[key]} missing from the report")

    def test_band_figures_appear(self):
        dep = self.data["assumption_dependence"]
        self.assertIn(f"{dep['band_cost_units_low']}", self.doc)
        self.assertIn(f"{dep['band_cost_units_high']}", self.doc)

    def test_scenario_costs_appear(self):
        for row in self.data["scenarios"]:
            self.assertIn(str(row["total_cost_units"]), self.doc,
                          f"{row['scenario']} cost missing from the report")

    def test_coverage_figures_appear(self):
        facts = self.data["facts"]
        self.assertIn(str(facts["prose_capture_ratio"] * 100)[:2], self.doc)
        self.assertIn(str(facts["scenes_with_register_prose_unresolved"]), self.doc)
        self.assertIn(str(facts["scenes_without_any_capture"]), self.doc)

    def test_report_does_not_claim_measurement(self):
        self.assertIn("PROVISIONAL", self.doc)
        self.assertIn("not a measurement", self.doc)
        self.assertNotIn("measured budget", self.doc.lower())

    def test_report_keeps_the_open_band_warning(self):
        """A reader of the report must learn the band is open BEFORE they read
        the ceiling headroom, not after."""
        self.assertIn("OPEN", self.doc)
        self.assertIn("CH01-SCN-014", self.doc)
        self.assertIn("lower bound on the true cost", self.doc)

    def test_headroom_is_reported_against_the_upper_endpoint(self):
        """TD range-budgeting rule: capacity planning uses the upper endpoint.

        A report that quotes only the point headroom is quoting the one figure
        that is neither endpoint, and the most flattering.
        """
        ceiling = self.data["ceiling"]
        self.assertEqual(ceiling["headroom_at_worst_case"],
                         round(ceiling["chapter_ceiling"]
                               - ceiling["highest_scenario_cost"], 4))
        self.assertIn("upper endpoint", ceiling["headroom_basis"].lower())
        self.assertIn("understates", ceiling["point_headroom_basis"].lower())
        self.assertIn("11.63", self.doc)
        self.assertIn("upper", self.doc.lower())

    def test_report_never_presents_point_cost_as_measured_runtime(self):
        for banned in ("measured runtime", "measured performance",
                       "observed frame time", "measured cost"):
            self.assertNotIn(banned, self.doc.lower())

    def test_report_states_the_dead_parameter(self):
        """The single most important change, and the one most likely to be
        quietly dropped by an editor who finds it confusing."""
        self.assertIn("0.000", self.doc)
        self.assertIn("inert", self.doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
