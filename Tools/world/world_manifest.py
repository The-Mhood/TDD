#!/usr/bin/env python3
"""World manifest schema and validator (W-M1).

PURPOSE
-------
Canon status must constrain what engineering is allowed to build. This tool takes
a *content manifest* — a declaration of what has actually been built or authored
for a chapter — and validates it against the canon index and the world rules.

It is the mechanism behind the promise in Docs/WORLD_ARCHITECTURE.md section 5.1:

    "A scene manifest declaring a gameplay element on a PROPOSED location fails
     the build unless the element is tagged BlockoutContent."

WHAT IT CANNOT DO
-----------------
It validates declarations, not Unreal content. A manifest is only as honest as the
person who wrote it. When an engine exists, the same rules are re-checked from the
asset registry (L2) so the manifest cannot lie. Recorded in ADR-0005.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "canon"))
import canon_index as ci  # noqa: E402

# Design statuses that permit final (non-blockout) production art.
ART_READY_DESIGN_STATUSES = {"APPROVED", "CONDITIONAL"}

# Canon statuses that permit story-bearing content.
CANON_BEARING_STATUSES = {"ESTABLISHED"}

# Elements that constitute "gameplay content" and therefore require canon cover
# unless explicitly declared blockout.
GAMEPLAY_ELEMENT_KINDS = {
    "quest",
    "reward",
    "collectible",
    "encounter",
    "boss",
    "memory",
    "dialogue",
    "cinematic",
    "interaction",
}


# --------------------------------------------------------------------------- #
# Manifest loading
# --------------------------------------------------------------------------- #

REQUIRED_TOP_LEVEL = ("chapter", "manifest_version", "locations", "scenes")


def load_manifest(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: manifest root must be an object")
    return data


def _require_keys(obj: Dict[str, Any], keys: Sequence[str], where: str,
                  errors: List[str]) -> bool:
    ok = True
    for key in keys:
        if key not in obj:
            errors.append(f"{where}: missing required field '{key}'")
            ok = False
    return ok


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_manifest(manifest: Dict[str, Any], index: Dict[str, Any]) -> List[str]:
    """Return every canon violation in the manifest. Empty list means valid."""
    errors: List[str] = []
    if not _require_keys(manifest, REQUIRED_TOP_LEVEL, "manifest", errors):
        return errors

    chapter = manifest["chapter"]
    chapter_ids = {c["id"] for c in index.get("chapters", [])}
    if chapter not in chapter_ids:
        errors.append(f"manifest.chapter {chapter!r} is not a known chapter")
        return errors

    canon_locations = {loc["id"]: loc for loc in index.get("locations", [])}
    rules = index.get("chapter_rules", [])

    # --- locations -------------------------------------------------------- #
    manifest_locations: Dict[str, Dict[str, Any]] = {}
    for loc in manifest.get("locations", []):
        if not _require_keys(loc, ("id", "built"), f"location {loc.get('id', '?')}", errors):
            continue
        loc_id = loc["id"]
        manifest_locations[loc_id] = loc

        canon = canon_locations.get(loc_id)
        if canon is None:
            errors.append(
                f"location {loc_id}: not present in the canon index. An unregistered "
                f"location cannot be built (ADR-0006)."
            )
            continue
        if ci.chapter_of(loc_id) != chapter:
            errors.append(f"location {loc_id}: belongs to {ci.chapter_of(loc_id)}, not {chapter}")
        if not isinstance(loc.get("built"), bool):
            errors.append(f"location {loc_id}: 'built' must be a boolean")

        canon_status = canon.get("canon_status")
        design_status = canon.get("env_design_status")

        # Final art may only be produced for art-ready designs.
        if loc.get("art") == "final" and design_status not in ART_READY_DESIGN_STATUSES:
            errors.append(
                f"location {loc_id}: final art requires design status in "
                f"{sorted(ART_READY_DESIGN_STATUSES)}; register says {design_status!r}"
            )

        # A location may not be presented as canon in-game unless it is canon.
        if loc.get("presented_as_canon") and canon_status not in CANON_BEARING_STATUSES:
            errors.append(
                f"location {loc_id}: presented as canon but register status is {canon_status!r} "
                f"(must be ESTABLISHED)"
            )

        # Gameplay elements on non-canon locations require blockout declaration.
        for element in loc.get("gameplay", []):
            if not _require_keys(element, ("kind",), f"location {loc_id} gameplay", errors):
                continue
            kind = element.get("kind")
            if kind not in GAMEPLAY_ELEMENT_KINDS:
                errors.append(
                    f"location {loc_id}: unknown gameplay element kind {kind!r}; "
                    f"expected one of {sorted(GAMEPLAY_ELEMENT_KINDS)}"
                )
                continue
            if canon_status not in CANON_BEARING_STATUSES and not element.get("blockout", False):
                errors.append(
                    f"location {loc_id}: '{kind}' content on a {canon_status} location must "
                    f"declare blockout: true. Non-canon locations may not carry shipped gameplay."
                )

    # --- scenes ----------------------------------------------------------- #
    for scene in manifest.get("scenes", []):
        if not _require_keys(scene, ("id", "parent", "built"),
                             f"scene {scene.get('id', '?')}", errors):
            continue
        scene_id = scene["id"]
        parent = scene["parent"]
        if ci.chapter_of(scene_id) != chapter:
            errors.append(f"scene {scene_id}: belongs to {ci.chapter_of(scene_id)}, not {chapter}")
        if parent not in canon_locations:
            errors.append(f"scene {scene_id}: parent {parent} is not a registered location")
        elif ci.chapter_of(parent) != chapter:
            errors.append(f"scene {scene_id}: parent {parent} is in a different chapter")

        # NPC and actor declarations are validated by reference to canon rules.
        for npc in scene.get("npcs", []):
            role = (npc.get("role") or "").lower()
            if role == "child" and npc.get("combat_target"):
                errors.append(
                    f"scene {scene_id}: child declared as a combat target. "
                    f"Violates RULE-NPC-CHILDREN-NO-COMBAT."
                )
            if role == "child" and npc.get("settlement") not in (None, True, chapter):
                errors.append(
                    f"scene {scene_id}: child outside the home settlement, which the register forbids"
                )

        for enemy in scene.get("enemies", []):
            enemy_type = (enemy.get("type") or "").lower()
            for rule in rules:
                if rule.get("chapter") != chapter:
                    continue
                for excluded in rule.get("excludes", []):
                    if not excluded.startswith("enemy:"):
                        continue
                    forbidden = excluded.split(":", 1)[1].lower()
                    if forbidden in enemy_type:
                        errors.append(
                            f"scene {scene_id}: enemy '{enemy_type}' violates {rule['id']}"
                        )

    # --- environment states ---------------------------------------------- #
    for state in manifest.get("environment_states", []):
        if not _require_keys(state, ("id", "parent"), f"environment state {state.get('id', '?')}",
                             errors):
            continue
        state_id = state["id"]
        if ci.chapter_of(state["parent"]) != chapter:
            errors.append(f"environment state {state_id}: parent is in a different chapter")
        if state["parent"] not in canon_locations:
            errors.append(f"environment state {state_id}: parent is not a registered location")
        if state_id in canon_locations:
            errors.append(
                f"environment state {state_id}: collides with a location id. "
                f"The registers state that environment states are not locations."
            )

    # --- routines --------------------------------------------------------- #
    for routine in manifest.get("routines", []):
        actor = routine.get("actor", "?")
        steps = routine.get("steps", [])
        if not steps:
            errors.append(f"routine for {actor}: has no steps")
            continue
        for step in steps:
            loc = step.get("location")
            if loc not in canon_locations and loc not in manifest_locations:
                errors.append(
                    f"routine for {actor}: step references unregistered location {loc!r}"
                )
            start, end = step.get("start_hour"), step.get("end_hour")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                errors.append(f"routine for {actor}: step hours must be numeric")
            elif not (0.0 <= start < 24.0 and 0.0 < end <= 24.0 and end > start):
                errors.append(
                    f"routine for {actor}: invalid window {start}..{end} "
                    f"(must be within 0..24 and end > start)"
                )
        ordered = sorted((s.get("start_hour", 0), s.get("end_hour", 0)) for s in steps)
        for (s1, e1), (s2, e2) in zip(ordered, ordered[1:]):
            if s2 < e1:
                errors.append(
                    f"routine for {actor}: overlapping steps {s1}..{e1} and {s2}..{e2}"
                )

    return errors


def covered_locations(manifest: Dict[str, Any]) -> Dict[str, int]:
    """Report coverage: how many locations the manifest declares, by category."""
    counts: Dict[str, int] = {}
    for loc in manifest.get("locations", []):
        category = ci.chapter_of(loc.get("id", "")) and str(loc.get("id", ""))[5:8]
        if not category:
            continue
        counts[category] = counts.get(category, 0) + 1
    return counts


def main(argv: Sequence[str]) -> int:
    if len(argv) < 2:
        print("usage: world_manifest.py <manifest.json> [--index path] [--verbose]")
        return 2
    manifest_path = Path(argv[1])
    index_path = Path(argv[argv.index("--index") + 1]) if "--index" in argv else ci.INDEX_PATH

    index = ci.load_index(index_path)
    manifest = load_manifest(manifest_path)
    errors = validate_manifest(manifest, index)

    print(f"manifest: {manifest_path}")
    print(f"chapter:  {manifest.get('chapter')}")
    print(f"locations declared: {len(manifest.get('locations', []))}  {covered_locations(manifest)}")
    print(f"scenes declared:    {len(manifest.get('scenes', []))}")
    print(f"violations: {len(errors)}")
    for error in errors:
        print("  ✗", error)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
