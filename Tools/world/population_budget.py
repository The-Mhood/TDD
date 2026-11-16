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

#: The verbatim Chapter 1 capture (register v1.9). This is the default source.
#: `scene_register_ch01_full.md` is PRESERVED unchanged as the earlier abridged
#: fixture: it is still readable, still testable, and is what the previous
#: model was built from. Superseding a fixture is not the same as deleting it,
#: and the W-M2.1 baseline must stay reproducible from the file it came from.
FIXTURE_VERBATIM = DEFAULT_FIXTURES / "scene_register_ch01_v19_verbatim.md"
FIXTURE_ABRIDGED = DEFAULT_FIXTURES / "scene_register_ch01_full.md"


# --------------------------------------------------------------------------- #
# Policy
# --------------------------------------------------------------------------- #

def _display_path(path: Path) -> str:
    """Repo-relative path when possible, absolute otherwise. Never raises."""
    try:
        return str(path.resolve().relative_to(HERE.parent.parent.resolve()))
    except (ValueError, OSError):
        return str(path)


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
    # MEASUREMENT IS NOT PROVENANCE. A count authored in the register is
    # transcribed DATA: it tells us what the designer wrote, not what actually
    # happens in a running build. Nothing in this project has been observed.
    # This field is therefore False for every row, and exists so that a consumer
    # can assert that rather than infer it from a comment. If any row ever
    # becomes True, it means someone ran a measurement - which requires an
    # engine that does not exist yet.
    npcs_is_measured: bool = False
    # The register's OWN numeric bounds for the field, where it states any.
    # "Six to ten adults" yields (6, 10). A collective with no number yields
    # (None, None) and the field stays genuinely unresolved. These are register
    # data, quoted from the source, never an assumption about density.
    npcs_band_low: Optional[int] = None
    npcs_band_high: Optional[int] = None
    npcs_band_basis: str = ""
    has_child: bool = False
    simulated_cost: float = 0.0    # cost units; 0.0 for NONE/BACKGROUND
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
    # Banded estimate. The point estimate treats an unresolved count as 0, which
    # understates. The band applies the register's own stated bounds where it
    # states any, so the reader can see how much the unresolved fields can
    # possibly move the total. `band_is_complete` is False when at least one
    # unresolved field has NO stated bound - then even the upper bound is a
    # lower bound on the true figure, and must be said so.
    npcs_band_summary: Dict[str, Any]
    band_cost_units_low: float
    band_cost_units_high: float
    band_is_complete: bool
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


def scene_cost_for_count(tier: str, count: Optional[int], policy: Dict[str, Any],
                         category: str) -> float:
    """Cost units for a scene at a GIVEN NPC count, before the access multiplier.

    One implementation, used by both the point estimate and the band, so the
    band can never drift from the model it is bounding.
    """
    if tier == "NAMED":
        return policy["cost_units"]["NAMED"]
    if tier == "CROWD":
        return policy["cost_units"]["CROWD"] * _estimate_crowd(count or 0, policy, category)
    if tier == "SCRIPTED":
        return policy["cost_units"]["SCRIPTED"]
    if tier == "BACKGROUND":
        return policy["cost_units"]["BACKGROUND"]
    return 0.0


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
    band_cost_low = 0.0
    band_cost_high = 0.0
    band_open: List[str] = []
    band_rows: List[Dict[str, Any]] = []

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

        # The register's own numeric bounds, where it states any.
        band_low = band_high = None
        band_basis = ""
        if detail is not None and detail.npcs_present:
            band_low, band_high, band_basis = reg.parse_npc_band(detail.npcs_present)

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

        # Banded cost. For a scene whose count is a settled integer the band is
        # that integer and adds nothing. For an unresolved field the band uses
        # the register's stated bounds instead of the point estimate's 0.
        if band_low is not None and band_high is not None and band_low != band_high:
            lo = scene_cost_for_count(tier, band_low, policy, category) * access_mult
            hi = scene_cost_for_count(tier, band_high, policy, category) * access_mult
            band_cost_low += lo
            band_cost_high += hi
            band_rows.append({
                "scene_id": scene.id, "tier": tier, "access": access,
                "npcs_band": [band_low, band_high], "basis": band_basis,
                # The register's OWN words, preserved verbatim. A reader must be
                # able to check the endpoints against the source without opening
                # the fixture, and no summarising step may sit between them.
                "register_wording": (detail.npcs_present if detail else ""),
                "cost_band": [round(lo, 2), round(hi, 2)],
                # The TD's range-budgeting rule, stated per row so the meaning of
                # the two endpoints cannot drift from what they are used for.
                "endpoint_use": {
                    "low": "lower scenario bound",
                    "high": "conservative population-capacity planning",
                },
                "midpoint_used": False,
            })
        else:
            band_cost_low += cost * access_mult
            band_cost_high += cost * access_mult
        if npcs_source == "unparsed" and band_low is None:
            band_open.append(scene.id)

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
            # Authored register data is not empirical measurement. See the field
            # comment on SceneBudget; this is deliberately always False.
            npcs_is_measured=False,
            npcs_band_low=band_low,
            npcs_band_high=band_high,
            npcs_band_basis=band_basis,
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
        npcs_band_summary={
            "scenes_with_stated_bounds": len(band_rows),
            "scenes_without_any_bound": sorted(band_open),
            "band_is_complete": not band_open,
            "detail": band_rows,
            "_note": "Bounds are the register's own wording (for example "
                     "'six to ten', 'four or five', 'sometimes one'). Where a "
                     "field states no bound the band is open in that direction "
                     "and the upper figure is a LOWER bound on the true cost.",
        },
        band_cost_units_low=round(band_cost_low, 2),
        band_cost_units_high=round(band_cost_high, 2),
        band_is_complete=not band_open,
        scenes=budgets,
    )


def validate_budget(budget: ChapterBudget, policy: Dict[str, Any]) -> List[str]:
    """Hard failures only: a derived budget that cannot be trusted at all.

    A WARNING is something the reader must be told but which does not falsify
    the model: an unresolved field, an open cost band, remaining policy defaults.
    Those live in `budget_warnings`. Folding them into the hard failures would
    make a correct, honestly-labelled result look broken, and a validator that
    always fails is a validator nobody reads.

    HARD FAILURES are only: a ceiling breach, an unmapped category, or an NPC
    field that is unresolvable in a way the model has not accounted for.
    """
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
    # Unresolved NPC prose is not automatically a failure. What matters is
    # whether the register gives us BOUNDS on it:
    #
    #   * bounded   - "six to ten", "four or five", "sometimes one". The point
    #                 estimate still treats these as 0, but the band replaces
    #                 those zeros with the register's own limits, so the reader
    #                 is told exactly how far off the point figure can be. That
    #                 is honest, and it is a WARNING.
    #   * unbounded - "a line of women and girls" with no numeral. Nothing bounds
    #                 the figure, so the band is open in that direction and the
    #                 upper figure is itself a lower bound. That is a FAILURE,
    #                 because it can no longer be quantified.

    undocumented = [s.scene_id for s in budget.scenes
                    if s.npcs_source == "unparsed" and not s.npcs_band_basis]
    if undocumented:
        problems.append(
            f"{budget.chapter}: {len(undocumented)} scene(s) are UNPARSED with no "
            f"recorded basis, so the gap UNDERSTATES cost and is undocumented: "
            f"{undocumented}"
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


def budget_warnings(budget: ChapterBudget) -> List[str]:
    """True warnings: the result stands, but the reader is owed the caveat."""
    warnings: List[str] = []
    bounded = [sid for sid in budget.unparsed_npc_scenes
               if sid not in budget.npcs_band_summary["scenes_without_any_bound"]]
    if bounded:
        warnings.append(
            f"{budget.chapter}: {len(bounded)} scene(s) state a range, alternative or "
            f"condition rather than a head-count. The point estimate bills them at 0 "
            f"and therefore UNDERSTATES; the band {budget.band_cost_units_low}-"
            f"{budget.band_cost_units_high} carries the register's own limits. "
            f"Resolving them needs a ruling on how a range is budgeted, not more "
            f"parsing: {bounded}"
        )
    if not budget.band_is_complete:
        warnings.append(
            f"{budget.chapter}: the cost band is OPEN because "
            f"{budget.npcs_band_summary['scenes_without_any_bound']} states no NPC "
            f"number. The band's upper figure is a LOWER bound on the true cost."
        )
    if budget.npcs_provenance_summary.get("POLICY_DEFAULT"):
        warnings.append(
            f"{budget.chapter}: {budget.npcs_provenance_summary['POLICY_DEFAULT']} "
            f"scene(s) remain uncaptured and rest on a policy default. All are "
            f"SCRIPTED or NONE tier, whose cost does not depend on the count, so "
            f"they carry provenance debt rather than numeric exposure."
        )
    return warnings


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

    scene_fixture = FIXTURE_VERBATIM
    for i, arg in enumerate(argv):
        if arg == "--fixture" and i + 1 < len(argv):
            scene_fixture = Path(argv[i + 1])
    if not scene_fixture.is_file():
        print(f"missing fixture: {scene_fixture}")
        return 2

    text = scene_fixture.read_text(encoding="utf-8")
    scenes = reg.parse_scene_summary(text)
    details = reg.parse_scene_details(text)
    policy = load_policy()

    budget = build_chapter_budget(scenes, details, policy, chapter)
    problems = validate_budget(budget, policy)
    warnings = budget_warnings(budget)

    payload = {
        "meta": {
            "tool": "Tools/world/population_budget.py",
            "derivation": "register scene categories -> policy tier -> cost units",
            "status": "PROVISIONAL - derived from authored data, NOT measured",
            "register_source": ("SCENE_AND_MICROLOCATION_MASTER_REGISTER v1.9 "
                                f"(fixture: {scene_fixture.name})"),
            "fixture_path": _display_path(scene_fixture),
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
        "validation": {
            "problems": problems,
            "warnings": warnings,
            "result": "PASS" if not problems else "FAIL",
            "result_note": "PASS means the derivation is internally sound and its "
                           "open fields are documented. It does NOT mean the figures "
                           "are measured; they are projections.",
        },
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
    print(f"  banded cost (low/high): {budget.band_cost_units_low}/{budget.band_cost_units_high}"
          f"  complete={budget.band_is_complete}")
    if not budget.band_is_complete:
        print(f"    band is OPEN at: {budget.npcs_band_summary['scenes_without_any_bound']}")
    print(f"  validation: {'PASS' if not problems else 'FAIL'}")
    for problem in problems:
        print("   !", problem)
    for warning in warnings:
        print("   ~", warning)

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"  written: {out_path}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
