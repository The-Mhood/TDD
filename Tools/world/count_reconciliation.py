#!/usr/bin/env python3
"""World entity relationship and count reconciliation (technical requirement TR-2).

THE PROBLEM
-----------
The location register publishes SIX quantities in one table headed "Counts (kept
separate, never mixed)". They are different kinds of thing and they overlap in
ways that punish casual arithmetic:

    8    major environments       one per chapter - these ARE location entries
    142  other locations          SUB/SET/LMK/TRV/EXP/BOS - location entries
    46   interiors                INT - location entries, but only when they exist
                                  as separate locations at all
    135  scenes and micro-locs    SCN - NOT locations
    122  of which not main or secondary story
    40   environment-state refs   ES_* - explicitly NOT locations

So "how many places are there" has no single answer. It depends which question:

    Location entries .................. 196   (8 + 142 + 46)
    Playable content units ............ 135   (scenes)  -- or 331 if you add them
    State variants ....................  40   (multipliers on locations, not places)

The register explains the trap itself: "Interiors that appear only as scenes (for
example a sleeping corner inside a house) are counted as scenes, not as
locations." The same physical room can therefore be a location, a scene, or
both, and adding the two columns double-counts it.

WHAT THIS TOOL DOES
-------------------
1. Verifies the register's own totals equal the sum of its own per-chapter rows.
2. Verifies the derived totals are consistent with each other and with the scene
   register's independent category counts.
3. Reconciles a parsed chapter against the published row for that chapter, and
   classifies any difference as INGESTION GAP (our capture is incomplete) or
   REGISTER INCONSISTENCY (the register contradicts itself).
4. Defines the entity kinds and containment rules in machine-readable form so
   other tools do not have to re-derive them.

WHAT IT DOES NOT DO
-------------------
Only Chapter 1 has been parsed. For Chapters 2-8 this checks arithmetic on the
published numbers, not the register's prose. Full per-chapter parsing is a task
per chapter (Docs/REGISTER_INGESTION.md).

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "canon"))
import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
COUNTS_FILE = HERE / "data" / "register_counts.json"

COUNT_KEYS = [
    "major_environments",
    "other_locations_not_interiors",
    "interiors_location_entries",
    "scenes_and_microlocations",
    "not_main_or_secondary_story",
    "environment_state_references",
]

# --------------------------------------------------------------------------- #
# Entity kinds — the things that exist, and whether they are locations
# --------------------------------------------------------------------------- #

ENTITY_KINDS: Dict[str, Dict[str, Any]] = {
    "MAJOR_ENVIRONMENT": {
        "id_pattern": "CHxx-ENV-001",
        "is_location_entry": True,
        "is_scene": False,
        "is_state": False,
        "description": "One per chapter. The chapter's exterior world.",
        "contains": "every other location in the chapter",
        "double_count_risk": "none: unique per chapter",
    },
    "LOCATION": {
        "id_pattern": "CHxx-(SUB|SET|LMK|TRV|EXP|BOS)-nnn",
        "is_location_entry": True,
        "is_scene": False,
        "is_state": False,
        "description": "A named place the player can be at: sub-location, settlement, "
                       "landmark, traversal area, exploration area, boss arena.",
        "contains": "scenes (optional), environment states (optional)",
        "double_count_risk": "An interior listed as a location AND described by a scene with "
                             "the same name is one place. The register counts the scene, not the "
                             "location, when the interior exists only as a scene.",
    },
    "INTERIOR": {
        "id_pattern": "CHxx-INT-nnn",
        "is_location_entry": True,
        "is_scene": False,
        "is_state": False,
        "description": "An interior that has its own location entry.",
        "contains": "scenes (optional), environment states (optional)",
        "double_count_risk": "HIGHEST. The register states that interiors appearing only as "
                             "scenes are counted as scenes. Never add INT count to SCN count and "
                             "call the result 'places'.",
    },
    "SCENE": {
        "id_pattern": "CHxx-SCN-nnn",
        "is_location_entry": False,
        "is_scene": True,
        "is_state": False,
        "description": "A staged moment or micro-location with its own board, category, access "
                       "level and NPC content. Includes EXTERIOR MICRO-LOCATION scenes.",
        "contains": "nothing; belongs to exactly one parent location",
        "double_count_risk": "Micro-locations are scenes. Do not add them again.",
    },
    "ENVIRONMENT_STATE": {
        "id_pattern": "CHxx-<LOC>-STnn",
        "is_location_entry": False,
        "is_scene": False,
        "is_state": True,
        "description": "A time, weather or supernatural variant of one location (night, rain, "
                       "market day, supernatural). Belongs to a location.",
        "contains": "nothing",
        "double_count_risk": "A state is a multiplier on one place, not a place. 40 state refs "
                             "do not mean 40 more locations.",
    },
}

CONTAINMENT_RULES = [
    "A scene has exactly one parent location.",
    "A location has zero or more scenes.",
    "An environment state has exactly one parent location and is not a location.",
    "Environment state ids never collide with location ids.",
    "A location entry's chapter prefix matches its major environment's chapter.",
    "Location entries = major_environments + other_locations + interiors. Scenes and "
    "states are excluded from that sum by definition.",
]


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

def load_register_counts(path: Path = COUNTS_FILE) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Register self-consistency
# --------------------------------------------------------------------------- #

def check_published_consistency(counts: Dict[str, Any]) -> List[str]:
    """The register's totals must equal the sum of its own per-chapter rows."""
    problems: List[str] = []
    per_chapter = counts["per_chapter"]
    for key in COUNT_KEYS:
        row_sum = sum(ch[key] for ch in per_chapter.values())
        published = counts["published_totals"][key]
        if row_sum != published:
            problems.append(
                f"published total '{key}' is {published} but its per-chapter rows sum to "
                f"{row_sum} (difference {published - row_sum:+d})"
            )
    return problems


def check_derived_totals(counts: Dict[str, Any]) -> List[str]:
    """The derived quantities must agree with the register and with each other."""
    problems: List[str] = []
    totals = counts["published_totals"]

    derived_locations = (totals["major_environments"]
                         + totals["other_locations_not_interiors"]
                         + totals["interiors_location_entries"])
    stated = counts["derived_totals"]["location_entries"]["value"]
    if derived_locations != stated:
        problems.append(
            f"location_entries derived as {derived_locations} but register_counts.json states "
            f"{stated}"
        )

    derived_story = (totals["scenes_and_microlocations"]
                     - totals["not_main_or_secondary_story"])
    stated_story = counts["derived_totals"]["main_or_secondary_story_scenes"]["value"]
    if derived_story != stated_story:
        problems.append(
            f"main_or_secondary_story_scenes derived as {derived_story} but "
            f"register_counts.json states {stated_story}"
        )

    # A subset column must not exceed its parent column, per chapter.
    for chapter, row in counts["per_chapter"].items():
        if row["not_main_or_secondary_story"] > row["scenes_and_microlocations"]:
            problems.append(
                f"{chapter}: not_main_or_secondary_story "
                f"{row['not_main_or_secondary_story']} exceeds scenes "
                f"{row['scenes_and_microlocations']}"
            )
    return problems


# --------------------------------------------------------------------------- #
# Per-chapter reconciliation against parsed fixtures
# --------------------------------------------------------------------------- #

@dataclass
class Reconciliation:
    chapter: str
    parsed_locations: int
    parsed_locations_by_category: Dict[str, int]
    parsed_scenes: int
    parsed_scenes_by_category: Dict[str, int]
    parsed_scenes_not_main_or_secondary: Optional[int]
    published: Dict[str, int]
    comparisons: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    problems: List[str] = field(default_factory=list)


def reconcile_chapter(locations: Sequence[reg.LocationRecord],
                      scenes: Sequence[reg.SceneRecord],
                      counts: Dict[str, Any],
                      chapter: str) -> Reconciliation:
    problems: List[str] = []

    base = chapter[:4]
    chapter_locations = [l for l in locations if l.chapter == base]
    chapter_scenes = [s for s in scenes if s.chapter == base]

    loc_cat: Dict[str, int] = {}
    for loc in chapter_locations:
        loc_cat[loc.category] = loc_cat.get(loc.category, 0) + 1

    scn_cat: Dict[str, int] = {}
    for scn in chapter_scenes:
        scn_cat[scn.scene_kind] = scn_cat.get(scn.scene_kind, 0) + 1

    story_categories = {"MAIN STORY SCENE", "SECONDARY STORY SCENE"}
    not_story = sum(n for c, n in scn_cat.items() if c not in story_categories)

    published = counts["per_chapter"][chapter]
    comparisons: Dict[str, Dict[str, Any]] = {}

    # ---- scenes: the scene fixture is complete for CH01, so this must match.
    comparisons["scenes_and_microlocations"] = {
        "parsed": len(chapter_scenes),
        "published": published["scenes_and_microlocations"],
        "complete_capture": True,
    }
    if len(chapter_scenes) != published["scenes_and_microlocations"]:
        problems.append(
            f"{chapter}: parsed {len(chapter_scenes)} scenes, register publishes "
            f"{published['scenes_and_microlocations']} - scene capture is supposedly complete, "
            f"so this is a REGISTER OR PARSER INCONSISTENCY"
        )

    # ---- not main/secondary: independent corroboration of the category mapping.
    comparisons["not_main_or_secondary_story"] = {
        "parsed": not_story,
        "published": published["not_main_or_secondary_story"],
        "complete_capture": True,
    }
    if not_story != published["not_main_or_secondary_story"]:
        problems.append(
            f"{chapter}: parsed {not_story} non-story scenes, register publishes "
            f"{published['not_main_or_secondary_story']} - category mapping or parser disagrees"
        )

    # ---- location entries: the location fixture is a PARTIAL capture.
    #      category + SUB/INT counts are derived from the register summary table.
    parsed_int = loc_cat.get("INT", 0)
    comparisons["interiors_location_entries"] = {
        "parsed": parsed_int,
        "published": published["interiors_location_entries"],
        "complete_capture": False,
    }
    comparisons["other_locations_not_interiors"] = {
        "parsed": len([l for l in chapter_locations if l.category != "INT"
                       and l.category != "ENV"]),
        "published": published["other_locations_not_interiors"],
        "complete_capture": False,
    }
    comparisons["major_environments"] = {
        "parsed": loc_cat.get("ENV", 0),
        "published": published["major_environments"],
        "complete_capture": True,
    }
    if loc_cat.get("ENV", 0) != published["major_environments"]:
        problems.append(
            f"{chapter}: parsed {loc_cat.get('ENV', 0)} major environments, register publishes "
            f"{published['major_environments']}"
        )

    # ---- containment: every scene needs a parent that exists.
    missing = sorted({s.id for s in chapter_scenes
                      if s.parent_id not in {l.id for l in chapter_locations}})
    comparisons["scenes_with_missing_parent"] = {
        "parsed": len(missing),
        "complete_capture": False,
        "ids": missing,
        "note": "Expected non-zero while the location fixture is a partial capture. "
                "Classified as INGESTION GAP, not a register defect."
                if missing else "none",
    }

    return Reconciliation(
        chapter=chapter,
        parsed_locations=len(chapter_locations),
        parsed_locations_by_category=dict(sorted(loc_cat.items())),
        parsed_scenes=len(chapter_scenes),
        parsed_scenes_by_category=dict(sorted(scn_cat.items())),
        parsed_scenes_not_main_or_secondary=not_story,
        published=published,
        comparisons=comparisons,
        problems=problems,
    )


def main(argv: Sequence[str]) -> int:
    out_path: Optional[Path] = None
    if "--out" in argv:
        out_path = Path(argv[argv.index("--out") + 1])

    counts = load_register_counts()
    loc_text = (FIXTURES / "location_register_ch01_excerpt.md").read_text(encoding="utf-8")
    scn_text = (FIXTURES / "scene_register_ch01_full.md").read_text(encoding="utf-8")
    locations = reg.parse_location_summary(loc_text)
    scenes = reg.parse_scene_summary(scn_text)

    consistency = check_published_consistency(counts)
    derived = check_derived_totals(counts)
    recon = reconcile_chapter(locations, scenes, counts, "CH01")

    all_problems = consistency + derived + recon.problems
    payload = {
        "meta": {
            "tool": "Tools/world/count_reconciliation.py",
            "purpose": "Prove the register's six counts are distinct quantities and reconcile.",
            "register_source": counts["register_source"],
            "companion_source": counts["companion_source"],
            "column_semantics": counts["column_semantics"],
            "entity_kinds": ENTITY_KINDS,
            "containment_rules": CONTAINMENT_RULES,
            "ingestion_status": "Chapter 1 parsed for locations (partial) and scenes (complete). "
                                "Chapters 2-8 arithmetic-checked on published numbers only.",
        },
        "published_totals": counts["published_totals"],
        "derived_totals": counts["derived_totals"],
        "register_self_consistency": {"problems": consistency},
        "derived_consistency": {"problems": derived},
        "chapter": asdict(recon),
        "result": "PASS" if not all_problems else "FAIL",
        "problems": all_problems,
    }

    print(f"register v{counts['register_source']['version']} - published totals")
    for key in COUNT_KEYS:
        print(f"  {key:34s} {counts['published_totals'][key]:4d}")
    print(f"  {'DERIVED location entries':34s} "
          f"{counts['derived_totals']['location_entries']['value']:4d}"
          f"   ({counts['derived_totals']['location_entries']['derivation']})")
    print()
    print(f"CH01 parsed: {recon.parsed_locations} location rows "
          f"{recon.parsed_locations_by_category}")
    print(f"CH01 parsed: {recon.parsed_scenes} scenes {recon.parsed_scenes_by_category}")
    print()
    for name, cmp in recon.comparisons.items():
        if isinstance(cmp, dict) and "parsed" in cmp:
            flag = "" if cmp["parsed"] == cmp.get("published") else "  <-- differs"
            if not cmp.get("complete_capture"):
                flag += " (partial capture, expected)"
            print(f"  {name:34s} parsed {cmp['parsed']:4d}  published "
                  f"{cmp.get('published', '-')}{flag}")
    print()
    print(f"self-consistency: {'PASS' if not consistency else 'FAIL'}")
    print(f"derived consistency: {'PASS' if not derived else 'FAIL'}")
    for p in all_problems:
        print("  -", p)
    print(f"RESULT: {payload['result']}")

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"written: {out_path}")
    return 0 if payload["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
