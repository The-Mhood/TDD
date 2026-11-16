#!/usr/bin/env python3
"""Population budget derivation (technical requirement TR-1).

PURPOSE
-------
Produce a TRACEABLE mapping from the register's own scene categories to a concrete
simulation tier, so the population cost of the world is an arithmetic consequence
of authored design data rather than an engineering guess.

The Technical Director's instruction was explicit:

    "Map actual register scene categories to named actors, Mass crowd simulation,
     lightweight scripted activity and background-only representation. Do not
     assume every ambient activity needs an individually simulated NPC."

This tool implements exactly that, and it deliberately does NOT assume. Every
number in its output is either (a) read from the register, or (b) an ENGINEERING
ASSUMPTION carried in `data/population_policy.json` with a stated rationale and a
`confidence` field. The two are never mixed silently: each output row records
which register row it came from and which policy rule assigned its tier.

WHAT THIS IS NOT
----------------
It is not a measurement. No simulation has run. These are *derived budgets*: what
the world is projected to cost, from authored data. The moment an engine exists,
every figure here must be replaced by a measurement from a capture (see
Docs/evidence and stage gates). Until then the numbers are PROVISIONAL and are
labelled as such in the output.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "canon"))
import registers as reg  # noqa: E402

POLICY_PATH = HERE / "data" / "population_policy.json"
DEFAULT_FIXTURES = HERE.parent / "canon" / "tests" / "fixtures"


# --------------------------------------------------------------------------- #
# Policy
# --------------------------------------------------------------------------- #

def load_policy(path: Path = POLICY_PATH) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tier_for_scene_category(policy: Dict[str, Any], category: str) -> Dict[str, Any]:
    """Return the policy rule governing a scene category, or a safe default."""
    rule = policy["scene_category_tiers"].get(category)
    if rule is not None:
        return rule
    return policy["unmapped_category_fallback"]


def tier_for_access(policy: Dict[str, Any], access: str) -> str:
    """Access level is an independent cost multiplier, not a tier selector."""
    return policy["access_multipliers"].get(access, policy["access_multipliers"]["_default"])


# --------------------------------------------------------------------------- #
# Budget model
# --------------------------------------------------------------------------- #

@dataclass
class SceneBudget:
    scene_id: str
    name: str
    category: str
    access: str
    canon_status: str
    parent_id: str

    tier: str                      # NAMED | CROWD | SCRIPTED | BACKGROUND | NONE
    tier_source: str               # "policy:<category>" or "fallback"
    npcs_from_register: Optional[int]
    npcs_source: str               # "register" | "policy_default" | "unparsed" | "none"
    # Explicit, machine-readable provenance so no reader has to infer whether a
    # number is data or assumption. These are derived from npcs_source and are
    # duplicated deliberately: a field a human can read at a glance is worth more
    # than a rule they must remember.
    npcs_provenance: str           # REGISTER_DATA | POLICY_DEFAULT | UNPARSED | NO_NPCS
    npcs_is_measured: bool         # True only when read from the register
    has_child: bool
    simulated_cost: float          # cost units; 0.0 for NONE/BACKGROUND
    notes: List[str] = field(default_factory=list)


@dataclass
class ChapterBudget:
    chapter: str
    scenes_total: int
    by_category: Dict[str, int]
    by_tier: Dict[str, int]
    by_status: Dict[str, int]
    simulated_npcs_lower: int
    simulated_npcs_upper: int
    crowd_peak_estimate: int
    background_estimate: int
    total_cost_units: float
    unparsed_npc_scenes: List[str]
    npcs_provenance_summary: Dict[str, int]
    scenes: List[SceneBudget]


def _estimate_crowd(count: int, policy: Dict[str, Any], category: str) -> int:
    """Crowd NPCs are simulated, but not all at once.

    Register NPC totals are the number of people the scene *depicts*, not the
    number that must be simulated simultaneously. The policy supplies a
    concurrency ratio per category, with a stated basis.

    ROUNDING IS DELIBERATELY UPWARD (ceiling).

    An earlier version used round(), which applies banker's rounding: round(1.5)
    and round(2.5) both return 2. That made a scene depicting two people and a
    scene depicting three people cost exactly the same, so the model silently
    flattened under variation. Worse, rounding to nearest can round a cost
    DOWNWARD, and a population budget that understates cost is worse than
    useless - it is the direction that produces a frame-rate failure nobody
    planned for.

    Ceiling is asymmetric on purpose: overestimating a budget costs margin,
    underestimating costs the project. Scenes are still individually small, so
    the aggregate bias is bounded and visible in the sensitivity report.
    """
    ratio = policy["crowd_concurrency_ratio"].get(category,
                                                 policy["crowd_concurrency_ratio"]["_default"])
    if not count:
        return 0
    return max(1, math.ceil(count * ratio))


def build_chapter_budget(scenes: Sequence[reg.SceneRecord],
                         details: Sequence[reg.SceneDetail],
                         policy: Dict[str, Any],
                         chapter: str) -> ChapterBudget:
    detail_by_id = {d.id: d for d in details}
    budgets: List[SceneBudget] = []
    by_category: Counter = Counter()
    by_tier: Counter = Counter()
    by_status: Counter = Counter()
    unparsed: List[str] = []

    sim_lower = sim_upper = crowd_peak = background = 0
    total_cost = 0.0

    for scene in scenes:
        if scene.chapter != chapter:
            continue
        detail = detail_by_id.get(scene.id)
        category = scene.scene_kind or (detail.scene_kind if detail else "")
        access = scene.access or (detail.access_text if detail else "")
        canon = scene.canon_status or (detail.canon_status if detail else "")

        by_category[category] += 1
        by_status[canon] += 1

        rule = tier_for_scene_category(policy, category)
        tier = rule["tier"]
        access_mult = tier_for_access(policy, access)

        npcs: Optional[int] = None
        npcs_source = "policy_default"
        has_child = False
        notes: List[str] = []

        if detail is not None and detail.npcs_present:
            npcs, has_child, npcs_parsed = reg.parse_npc_count(detail.npcs_present)
            npcs_source = "register"
            if not npcs_parsed:
                # Prose we could not parse numerically. Do not silently budget 0.
                unparsed.append(scene.id)
                npcs_source = "unparsed"
                notes.append(
                    f"NPC description not machine-parseable: {detail.npcs_present!r}; "
                    f"counted as 0 which UNDERSTATES cost. Manual review required."
                )
        elif rule.get("expected_npcs") is not None:
            npcs = int(rule["expected_npcs"])
            notes.append("No detail block captured; NPC count is a policy default, not register data.")
        else:
            npcs = 0
            npcs_source = "none"

        if has_child:
            notes.append("Child present: RULE-NPC-CHILDREN-NO-COMBAT applies; never a combat target.")

        # Cost accounting by tier.
        cost = 0.0
        if tier == "NAMED":
            sim_lower += 1
            sim_upper += 1
            cost = policy["cost_units"]["NAMED"]
        elif tier == "CROWD":
            simulated = _estimate_crowd(npcs or 0, policy, category)
            crowd_peak += simulated
            sim_lower += simulated
            sim_upper += simulated
            cost = policy["cost_units"]["CROWD"] * simulated
        elif tier == "SCRIPTED":
            # One lightweight scripted performer, no AI, no perception.
            sim_upper += 1
            cost = policy["cost_units"]["SCRIPTED"]
            notes.append("Scripted activity: animates on a loop, has no AI or perception.")
        elif tier == "BACKGROUND":
            background += max(npcs or 0, 1)
            cost = policy["cost_units"]["BACKGROUND"]
        elif tier == "NONE":
            cost = 0.0

        total_cost += cost * access_mult

        by_tier[tier] += 1
        provenance = {
            "register": "REGISTER_DATA",
            "policy_default": "POLICY_DEFAULT",
            "unparsed": "UNPARSED",
            "none": "NO_NPCS",
        }[npcs_source]
        budgets.append(SceneBudget(
            scene_id=scene.id, name=scene.name, category=category, access=access,
            canon_status=canon, parent_id=scene.parent_id,
            tier=tier, tier_source=f"policy:{category}" if category in
            policy["scene_category_tiers"] else "fallback",
            npcs_from_register=npcs, npcs_source=npcs_source,
            npcs_provenance=provenance,
            npcs_is_measured=(npcs_source == "register"),
            has_child=has_child,
            simulated_cost=round(cost * access_mult, 2), notes=notes,
        ))

    return ChapterBudget(
        chapter=chapter,
        scenes_total=len(budgets),
        by_category=dict(sorted(by_category.items())),
        by_tier=dict(sorted(by_tier.items())),
        by_status=dict(sorted(by_status.items())),
        simulated_npcs_lower=sim_lower,
        simulated_npcs_upper=sim_upper,
        crowd_peak_estimate=crowd_peak,
        background_estimate=background,
        total_cost_units=round(total_cost, 2),
        unparsed_npc_scenes=sorted(set(unparsed)),
        npcs_provenance_summary=dict(sorted(
            Counter(b.npcs_provenance for b in budgets).items())),
        scenes=budgets,
    )


def validate_budget(budget: ChapterBudget, policy: Dict[str, Any]) -> List[str]:
    """Check a derived budget against the chapter ceilings in the policy."""
    problems: List[str] = []
    limits = policy["chapter_limits"]

    if budget.by_tier.get("CROWD", 0) > limits["max_crowd_scenes"]:
        problems.append(
            f"{budget.chapter}: {budget.by_tier['CROWD']} crowd scenes exceeds "
            f"ceiling {limits['max_crowd_scenes']}"
        )
    if budget.total_cost_units > limits["max_total_cost_units"]:
        problems.append(
            f"{budget.chapter}: total cost {budget.total_cost_units} exceeds "
            f"chapter ceiling {limits['max_total_cost_units']}"
        )
    if budget.unparsed_npc_scenes:
        problems.append(
            f"{budget.chapter}: {len(budget.unparsed_npc_scenes)} scene(s) have "
            f"unparseable NPC counts and UNDERSTATE cost: {budget.unparsed_npc_scenes}"
        )
    unknown_categories = [
        c for c in budget.by_category if c not in policy["scene_category_tiers"]
    ]
    if unknown_categories:
        problems.append(
            f"{budget.chapter}: scene categories with no tier mapping "
            f"(fell back to default): {unknown_categories}"
        )
    return problems


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: Sequence[str]) -> int:
    chapter = "CH01"
    out_path: Optional[Path] = None
    for i, arg in enumerate(argv):
        if arg == "--chapter" and i + 1 < len(argv):
            chapter = argv[i + 1]
        if arg == "--out" and i + 1 < len(argv):
            out_path = Path(argv[i + 1])

    scene_fixture = DEFAULT_FIXTURES / "scene_register_ch01_full.md"
    if not scene_fixture.is_file():
        print(f"missing fixture: {scene_fixture}")
        return 2

    text = scene_fixture.read_text(encoding="utf-8")
    scenes = reg.parse_scene_summary(text)
    details = reg.parse_scene_details(text)
    policy = load_policy()

    budget = build_chapter_budget(scenes, details, policy, chapter)
    problems = validate_budget(budget, policy)

    payload = {
        "meta": {
            "tool": "Tools/world/population_budget.py",
            "derivation": "register scene categories -> policy tier -> cost units",
            "status": "PROVISIONAL - derived from authored data, NOT measured",
            "register_source": "SCENE_AND_MICROLOCATION_MASTER_REGISTER v1.9 (Chapter 1 fixture)",
            "policy_source": "Tools/world/data/population_policy.json",
            "caveat": "No simulation has run. Every figure is a projection. "
                      "Replace with capture data when an engine exists.",
            "capture_status": {
                "scenes": "COMPLETE - all Chapter 1 scenes captured",
                "locations": "PARTIAL - location entries are NOT fully captured",
                "note": "This tool consumes the scene fixture only. A complete "
                        "scene capture does not imply a complete location capture.",
            },
            "provenance_legend": {
                "REGISTER_DATA": "NPC count read from the register's detail block",
                "POLICY_DEFAULT": "NPC count is a policy assumption; NEEDS SOURCE CAPTURE",
                "UNPARSED": "register prose found but not machine-parseable; "
                            "counted as 0 and UNDERSTATES cost",
                "NO_NPCS": "scene has no NPC field and none is expected",
            },
        },
        "budget": asdict(budget),
        "validation": {"problems": problems, "result": "PASS" if not problems else "FAIL"},
    }

    print(f"chapter {chapter}: {budget.scenes_total} scenes")
    print(f"  by category: {budget.by_category}")
    print(f"  by tier:     {budget.by_tier}")
    print(f"  by status:   {budget.by_status}")
    print(f"  simulated NPCs (lower/upper): {budget.simulated_npcs_lower}/{budget.simulated_npcs_upper}")
    print(f"  crowd peak estimate: {budget.crowd_peak_estimate}")
    print(f"  background: {budget.background_estimate}")
    print(f"  total cost units: {budget.total_cost_units}")
    print(f"  NPC count provenance: {budget.npcs_provenance_summary}")
    print(f"  validation: {'PASS' if not problems else 'FAIL'}")
    for problem in problems:
        print("   -", problem)

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"  written: {out_path}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
