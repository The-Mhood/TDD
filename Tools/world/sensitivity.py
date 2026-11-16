#!/usr/bin/env python3
"""Sensitivity analysis of the Chapter 1 population estimate.

PURPOSE
-------
The population estimate is derived, not measured. Part of it comes from the
register (5 scenes have captured NPC prose) and the overwhelming majority comes
from policy defaults (41 scenes have none). A single headline number hides that
asymmetry and invites false confidence.

This tool answers the question the Technical Director actually asked:

    "How does the Chapter 1 population estimate change when policy-default NPC
     counts and crowd-concurrency assumptions are varied?"

and it answers it by separating, in the output structure itself:

    FACTS          what the register says (traceable to a scene id)
    ASSUMPTIONS    what the policy assumes (traceable to a named parameter)
    RESULT         what the combination produces, with its range

STRUCTURAL FINDING
------------------
Only CROWD-tier scenes carry a per-NPC cost. NAMED and SCRIPTED are flat
per-scene costs, so their NPC counts cannot move the total at all. Chapter 1 has
14 CROWD scenes, of which 12 are policy defaults. The estimate therefore
collapses to a question about two knobs:

    expected_npcs  for AMBIENT NPC SCENE (policy default, currently 2)
    crowd_concurrency_ratio for AMBIENT NPC SCENE (policy, currently 0.75)

Everything else in the chapter is insensitive to these variations. That is the
most useful thing this report can say, and it is more useful than a range.

WHAT THIS IS NOT
----------------
Not a measurement. Not a prediction of runtime cost. The variation ranges below
are engineering hypotheses about plausible policy error, not observed values.
No simulation has run.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canon"))
sys.path.insert(0, str(HERE))

import population_budget as pb  # noqa: E402
import registers as reg  # noqa: E402

FIXTURES = HERE.parent / "canon" / "tests" / "fixtures"

CROWD_CATEGORY = "AMBIENT NPC SCENE"


# --------------------------------------------------------------------------- #
# Fact / assumption separation
# --------------------------------------------------------------------------- #

def register_facts(budget: pb.ChapterBudget) -> Dict[str, Any]:
    """What the register actually tells us. Traceable to scene ids."""
    from_register = [s for s in budget.scenes if s.npcs_source == "register"]
    return {
        "scenes_with_register_npc_data": len(from_register),
        "scenes_total": budget.scenes_total,
        "coverage_ratio": round(len(from_register) / budget.scenes_total, 3)
        if budget.scenes_total else 0.0,
        "detail": [
            {
                "scene_id": s.scene_id,
                "name": s.name,
                "category": s.category,
                "npcs_from_register": s.npcs_from_register,
                "tier": s.tier,
            }
            for s in from_register
        ],
    }


def policy_assumptions(policy: Dict[str, Any]) -> Dict[str, Any]:
    """What the policy assumes, and which parameter each number traces to."""
    return {
        "cost_units": {k: v for k, v in policy["cost_units"].items()
                       if not k.startswith("_")},
        "crowd_concurrency_ratio": {k: v for k, v in
                                    policy["crowd_concurrency_ratio"].items()
                                    if not k.startswith("_")},
        "expected_npcs_defaults": {
            cat: rule.get("expected_npcs")
            for cat, rule in policy["scene_category_tiers"].items()
        },
        "access_multipliers": policy.get("access_multipliers", {}),
        "_note": "Every value here is an engineering assumption with no register "
                 "basis. None of it is measured.",
    }


def assumption_driven(budget: pb.ChapterBudget) -> Dict[str, Any]:
    """How much of the estimate rests on assumption rather than data."""
    default_scenes = [s for s in budget.scenes if s.npcs_source == "policy_default"]
    register_scenes = [s for s in budget.scenes if s.npcs_source == "register"]

    def cost(scenes: Sequence[pb.SceneBudget]) -> float:
        return round(sum(s.simulated_cost for s in scenes), 4)

    total = cost(budget.scenes) or 1.0
    return {
        "cost_from_register_scenes": cost(register_scenes),
        "cost_from_policy_default_scenes": cost(default_scenes),
        "share_of_cost_from_policy_defaults": round(cost(default_scenes) / total, 3),
        "scenes_on_policy_default": len(default_scenes),
        "scenes_with_register_data": len(register_scenes),
    }


# --------------------------------------------------------------------------- #
# Sensitivity
# --------------------------------------------------------------------------- #

@dataclass
class SensitivityPoint:
    parameter: str
    value: Any
    total_cost_units: float
    simulated_npcs: int
    crowd_peak: int
    delta_vs_baseline: float
    pct_vs_baseline: float


def _rebuild(policy: Dict[str, Any], scenes, details) -> pb.ChapterBudget:
    return pb.build_chapter_budget(scenes, details, policy, "CH01")


def sweep(policy: Dict[str, Any], scenes, details,
          parameter: str, values: Sequence[Any]) -> List[SensitivityPoint]:
    """Vary one policy parameter, holding everything else at baseline."""
    baseline = _rebuild(policy, scenes, details)
    base_cost = baseline.total_cost_units
    points: List[SensitivityPoint] = []

    for value in values:
        p = copy.deepcopy(policy)
        if parameter == "crowd_concurrency_ratio":
            p["crowd_concurrency_ratio"][CROWD_CATEGORY] = value
        elif parameter == "expected_npcs_crowd":
            p["scene_category_tiers"][CROWD_CATEGORY]["expected_npcs"] = value
        elif parameter == "expected_npcs_scripted":
            # SCRIPTED is a flat per-scene cost, so this SHOULD be inert.
            # Swept deliberately to demonstrate that, not to change the result.
            p["scene_category_tiers"]["WORLD ACTIVITY SCENE"]["expected_npcs"] = value
        elif parameter == "cost_unit_crowd":
            p["cost_units"]["CROWD"] = value
        else:
            raise ValueError(f"unknown parameter {parameter}")

        b = _rebuild(p, scenes, details)
        delta = round(b.total_cost_units - base_cost, 4)
        points.append(SensitivityPoint(
            parameter=parameter, value=value,
            total_cost_units=b.total_cost_units,
            simulated_npcs=b.simulated_npcs_upper,
            crowd_peak=b.crowd_peak_estimate,
            delta_vs_baseline=delta,
            pct_vs_baseline=round(100.0 * delta / base_cost, 2) if base_cost else 0.0,
        ))
    return points


def elasticity(points: Sequence[SensitivityPoint], param_value_baseline: float) -> float:
    """Percent change in cost per percent change in the parameter.

    Computed by central finite difference using the sweep points IMMEDIATELY
    below and above the baseline. An earlier version selected the closest and
    farthest points, which happened to give a plausible number on the ratio
    sweep and a meaningless one on the quantized NPC sweep. Use neighbours.

    A value of 0 means the total does not depend on that parameter.
    """
    below = [p for p in points if float(p.value) < param_value_baseline]
    above = [p for p in points if float(p.value) > param_value_baseline]
    if not below or not above:
        return 0.0
    lo = max(below, key=lambda p: float(p.value))
    hi = min(above, key=lambda p: float(p.value))
    try:
        d_param = (float(hi.value) - float(lo.value)) / param_value_baseline
        d_cost = (hi.total_cost_units - lo.total_cost_units) / (
            lo.total_cost_units or 1.0)
    except (ZeroDivisionError, TypeError):
        return 0.0
    if d_param == 0:
        return 0.0
    return round(d_cost / d_param, 3)


def detect_quantization(points: Sequence[SensitivityPoint]) -> Dict[str, Any]:
    """Report where the sweep flattens.

    `_estimate_crowd` rounds to whole actors, so a change in the depicted count
    does not necessarily change the simulated count. The model is therefore a
    step function, not a smooth surface. Saying so is more honest than reporting
    a single elasticity that implies continuous response.
    """
    flat_pairs = []
    for a, b in zip(points, points[1:]):
        if a.total_cost_units == b.total_cost_units:
            flat_pairs.append([a.value, b.value])
    return {
        "is_quantized": bool(flat_pairs),
        "flat_intervals": flat_pairs,
        "cause": "crowd actors are rounded to whole numbers per scene, so small "
                 "changes in the depicted count can leave the simulated count "
                 "unchanged",
        "consequence": "the reported elasticity is a local slope and does not "
                       "describe the whole sweep",
    }


def combined_scenarios(policy: Dict[str, Any], scenes, details) -> List[Dict[str, Any]]:
    """Named joint scenarios: what the chapter costs under coherent assumption sets."""
    baseline = _rebuild(policy, scenes, details)
    out: List[Dict[str, Any]] = []

    combos = [
        ("LOW-DENSITY", 1, 0.5,
         "Every ambient scene depicts one person; half are simulated at once."),
        ("LOW-COUNT", 1, 0.75,
         "One person per ambient scene, baseline concurrency."),
        ("BASELINE", 2, 0.75,
         "Current policy defaults."),
        ("HIGH-COUNT", 3, 0.75,
         "Ambient scenes depict three people."),
        ("HIGH-DENSITY", 4, 1.0,
         "Four people per ambient scene, all simulated simultaneously."),
    ]
    for name, npcs, ratio, note in combos:
        p = copy.deepcopy(policy)
        p["scene_category_tiers"][CROWD_CATEGORY]["expected_npcs"] = npcs
        p["crowd_concurrency_ratio"][CROWD_CATEGORY] = ratio
        b = _rebuild(p, scenes, details)
        delta = round(b.total_cost_units - baseline.total_cost_units, 4)
        out.append({
            "scenario": name,
            "expected_npcs_default": npcs,
            "crowd_concurrency_ratio": ratio,
            "total_cost_units": b.total_cost_units,
            "simulated_npcs": b.simulated_npcs_upper,
            "crowd_peak": b.crowd_peak_estimate,
            "delta_vs_baseline": delta,
            "pct_vs_baseline": round(
                100.0 * delta / baseline.total_cost_units, 2)
            if baseline.total_cost_units else 0.0,
            "still_within_chapter_ceiling":
                b.total_cost_units <= policy["chapter_limits"]["max_total_cost_units"],
            "note": note,
        })
    return out


def ceiling_headroom(scenarios: Sequence[Dict[str, Any]],
                     ceiling: float) -> Dict[str, Any]:
    worst = max(scenarios, key=lambda s: s["total_cost_units"])
    best = min(scenarios, key=lambda s: s["total_cost_units"])
    return {
        "chapter_ceiling": ceiling,
        "lowest_scenario_cost": best["total_cost_units"],
        "highest_scenario_cost": worst["total_cost_units"],
        "highest_scenario_name": worst["scenario"],
        "headroom_at_worst_case": round(ceiling - worst["total_cost_units"], 4),
        "all_scenarios_within_ceiling": worst["total_cost_units"] <= ceiling,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def build_report(scenes, details, policy) -> Dict[str, Any]:
    baseline = _rebuild(policy, scenes, details)

    ratio_base = policy["crowd_concurrency_ratio"][CROWD_CATEGORY]
    npc_base = policy["scene_category_tiers"][CROWD_CATEGORY]["expected_npcs"]

    ratio_points = sweep(policy, scenes, details, "crowd_concurrency_ratio",
                         [0.25, 0.5, 0.75, 1.0])
    npc_points = sweep(policy, scenes, details, "expected_npcs_crowd", [1, 2, 3, 4, 5])
    scripted_points = sweep(policy, scenes, details, "expected_npcs_scripted",
                            [0, 1, 2, 4])
    unit_points = sweep(policy, scenes, details, "cost_unit_crowd",
                        [0.5, 1.0, 1.5, 2.0])

    scenarios = combined_scenarios(policy, scenes, details)

    return {
        "meta": {
            "tool": "Tools/world/sensitivity.py",
            "chapter": "CH01",
            "status": "PROVISIONAL - sensitivity of a derived estimate, not a measurement",
            "register_source": "SCENE_AND_MICROLOCATION_MASTER_REGISTER v1.9",
            "policy_source": "Tools/world/data/population_policy.json",
            "caveat": "Variation ranges are engineering hypotheses about plausible "
                      "policy error. They are NOT observed values. No simulation has run. "
                      "This report covers Chapter 1 only and does NOT extrapolate to "
                      "Chapters 2-8, whose categories are not ingested.",
            "reading_guide": {
                "facts": "Values read from the register. Traceable to a scene id.",
                "assumptions": "Values invented by the policy. No register basis.",
                "elasticity": "Percent change in total cost per percent change in the "
                              "parameter. 0 means the total does not depend on it.",
            },
        },
        "capture_status": {
            "scenes": "COMPLETE - 46 of 46 Chapter 1 scenes captured",
            "locations": "PARTIAL - 13 of 57 Chapter 1 location entries captured",
            "warning": "This report covers scenes only. It says nothing about the "
                       "41 uncaptured location entries, and it must not be read as "
                       "covering the full chapter's world content.",
        },
        "facts": register_facts(baseline),
        "assumptions": policy_assumptions(policy),
        "assumption_dependence": assumption_driven(baseline),
        "baseline": {
            "total_cost_units": baseline.total_cost_units,
            "simulated_npcs": baseline.simulated_npcs_upper,
            "crowd_peak": baseline.crowd_peak_estimate,
        },
        "sensitivity": {
            "crowd_concurrency_ratio": {
                "baseline": ratio_base,
                "points": [asdict(p) for p in ratio_points],
                "elasticity": elasticity(ratio_points, float(ratio_base)),
                "quantization": detect_quantization(ratio_points),
                "interpretation": "How many of the depicted crowd must be "
                                  "simulated at the same time.",
            },
            "expected_npcs_for_policy_defaults": {
                "baseline": npc_base,
                "points": [asdict(p) for p in npc_points],
                "elasticity": elasticity(npc_points, float(npc_base)),
                "quantization": detect_quantization(npc_points),
                "interpretation": "How many people an ambient scene depicts, for "
                                  "the 12 crowd scenes with no captured detail block.",
            },
            "expected_npcs_for_scripted": {
                "baseline": policy["scene_category_tiers"]["WORLD ACTIVITY SCENE"]
                .get("expected_npcs"),
                "points": [asdict(p) for p in scripted_points],
                "elasticity": elasticity(scripted_points, 1.0),
                "interpretation": "EXPECTED TO BE INERT. Scripted scenes are billed "
                                  "as a flat per-scene cost, so their NPC count "
                                  "cannot move the total. Included to demonstrate "
                                  "the model's structure, not to vary the result.",
            },
            "crowd_cost_unit": {
                "baseline": policy["cost_units"]["CROWD"],
                "points": [asdict(p) for p in unit_points],
                "elasticity": elasticity(unit_points, 1.0),
                "interpretation": "The cost assigned to one simulated crowd actor. "
                                  "Pure assumption: no capture exists.",
            },
        },
        "scenarios": scenarios,
        "ceiling": ceiling_headroom(scenarios, policy["chapter_limits"]["max_total_cost_units"]),
        "conclusion": {
            "estimate_is_mostly_assumption": True,
            "register_coverage_of_scenes": round(
                len([s for s in baseline.scenes if s.npcs_source == "register"])
                / baseline.scenes_total, 3),
            "only_crowd_scenes_are_sensitive": True,
            "summary": "The estimate is driven almost entirely by two policy "
                       "parameters applied to 12 uncaptured ambient scenes. "
                       "Capturing those 12 detail blocks would convert most of the "
                       "estimate from assumption to fact, and is worth more than "
                       "any refinement of the policy numbers.",
        },
    }


def main(argv: Sequence[str]) -> int:
    out_path = None
    if "--out" in argv:
        out_path = Path(argv[argv.index("--out") + 1])

    text = (FIXTURES / "scene_register_ch01_full.md").read_text(encoding="utf-8")
    scenes = reg.parse_scene_summary(text)
    details = reg.parse_scene_details(text)
    policy = pb.load_policy()

    report = build_report(scenes, details, policy)

    print("CHAPTER 1 POPULATION SENSITIVITY")
    print("=" * 62)
    f = report["facts"]
    print(f"register-derived NPC data: {f['scenes_with_register_npc_data']} of "
          f"{f['scenes_total']} scenes ({f['coverage_ratio']:.0%})")
    a = report["assumption_dependence"]
    print(f"share of cost from policy defaults: "
          f"{a['share_of_cost_from_policy_defaults']:.0%}")
    print(f"baseline: {report['baseline']['total_cost_units']} cost units, "
          f"{report['baseline']['simulated_npcs']} simulated NPCs")
    print()
    print(f"{'parameter':34s} {'value':>7s} {'cost':>8s} {'delta':>8s} {'elast':>7s}")
    for name, block in report["sensitivity"].items():
        for pt in block["points"]:
            print(f"{name:34s} {str(pt['value']):>7s} {pt['total_cost_units']:8.2f} "
                  f"{pt['delta_vs_baseline']:+8.2f} {block['elasticity']:+7.2f}")
        print()
    print("SCENARIOS")
    for s in report["scenarios"]:
        flag = "" if s["still_within_chapter_ceiling"] else "  CEILING EXCEEDED"
        print(f"  {s['scenario']:14s} npcs={s['expected_npcs_default']} "
              f"ratio={s['crowd_concurrency_ratio']:.2f}  "
              f"cost={s['total_cost_units']:6.2f}  sim={s['simulated_npcs']:3d}  "
              f"({s['pct_vs_baseline']:+.0f}%){flag}")
    c = report["ceiling"]
    print()
    print(f"headroom at worst case: {c['headroom_at_worst_case']} of "
          f"{c['chapter_ceiling']} ({c['highest_scenario_name']})")

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
