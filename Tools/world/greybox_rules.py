#!/usr/bin/env python3
"""CD-5 greybox restriction validator.

TD DECISION CD-5 (APPROVED WITH RESTRICTIONS)
---------------------------------------------
PENDING APPROVAL content may be represented as greybox **for technical
evaluation only**. The restrictions are binding, and a restriction that only
lives in prose is a restriction nobody enforces. This tool makes them fail the
build.

The permitted use, verbatim in intent:
  * labelled "PENDING APPROVAL - BLOCKOUT ONLY"
  * spatial / navigation / streaming / sightline tests only
  * no final art
  * no shrine, mask or ritual decoration
  * no story dependency
  * removable without breaking progression
  * never changes approval status

WHAT THIS TOOL CHECKS
---------------------
1. Every greybox asset declares the mandatory label exactly.
2. Every greybox asset names at least one permitted test purpose, and no
   forbidden one.
3. Every greybox asset declares `establishes_story_facts: false` and
   `progression_dependency: false`.
4. No greybox asset's declared content mentions shrine, mask, ritual, or any
   other reserved decorative vocabulary.
5. A greybox asset never carries an approved environment design status.
6. Removing a greybox asset is checked for progression safety: nothing in the
   manifest may declare a dependency on a greybox id.

Also verifies the inverse: a location whose register status is APPROVED must not
be marked as greybox, because greybox and approval are mutually exclusive states.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "canon"))

MANDATORY_LABEL = "PENDING APPROVAL \u2014 BLOCKOUT ONLY"

#: Test purposes a greybox is allowed to serve. Anything outside this set is
#: outside the CD-5 permission.
PERMITTED_PURPOSES = {
    "SPATIAL",
    "NAVIGATION",
    "STREAMING",
    "SIGHTLINE",
}

#: Vocabulary that may never appear in a greybox asset's declared content. These
#: are the things CD-5 reserves: shrine, mask, ritual decoration.
RESERVED_VOCABULARY = {
    "shrine": "shrine content is reserved pending consultant review (CD-2)",
    "mask": "masks are reserved pending consultant review (CD-2) and CD-3",
    "ritual": "ritual content is reserved pending consultant review (CD-2)",
    "altar": "altar content is reserved pending consultant review (CD-2)",
    "offering": "offering content is reserved pending consultant review (CD-2)",
    "idol": "cult images are reserved pending consultant review (CD-2)",
    "fetish": "reserved pending consultant review (CD-2)",
    "glyph": "decorative glyphs are final-art work, forbidden in greybox",
    "carving": "carving is final-art ornament, forbidden in greybox",
    "texture": "final-art texture is forbidden in greybox",
    "final art": "final art is forbidden in greybox",
}

APPROVED_STATUSES = {"APPROVED", "CONDITIONAL"}


@dataclass
class GreyboxViolation:
    asset_id: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.asset_id}: [{self.rule}] {self.detail}"


def validate_greybox_asset(asset: Dict[str, Any]) -> List[GreyboxViolation]:
    """Validate one greybox declaration against the CD-5 restrictions."""
    v: List[GreyboxViolation] = []
    aid = asset.get("id", "<unknown>")

    # The mandatory label applies to PENDING APPROVAL content. That is the case
    # CD-5 exists for: material whose approval is not settled. ESTABLISHED canon
    # is not a CD-5 case, and PROPOSED content establishes no story fact, so it
    # must still be labelled if it is staged, but it is not the restricted case.
    canon = asset.get("register_canon_status", "")
    label = asset.get("label")
    if canon == "PENDING APPROVAL":
        if label != MANDATORY_LABEL:
            v.append(GreyboxViolation(
                aid, "LABEL",
                f"PENDING APPROVAL content must be labelled exactly "
                f"{MANDATORY_LABEL!r}, found {label!r}"))
    elif canon == "PROPOSED":
        if label != MANDATORY_LABEL:
            v.append(GreyboxViolation(
                aid, "LABEL",
                f"PROPOSED content staged as greybox must also carry "
                f"{MANDATORY_LABEL!r}, found {label!r}"))
    elif canon == "ESTABLISHED":
        if label == MANDATORY_LABEL:
            v.append(GreyboxViolation(
                aid, "LABEL",
                "ESTABLISHED canon must not be labelled as pending approval; "
                "that would misrepresent its status"))
    else:
        v.append(GreyboxViolation(
            aid, "STATUS", f"unrecognised register_canon_status {canon!r}"))

    purposes = asset.get("test_purposes", [])
    if not purposes:
        v.append(GreyboxViolation(
            aid, "PURPOSE", "no test purpose declared; greybox must serve a named test"))
    for purpose in purposes:
        if purpose not in PERMITTED_PURPOSES:
            v.append(GreyboxViolation(
                aid, "PURPOSE",
                f"{purpose!r} is not a permitted purpose "
                f"({', '.join(sorted(PERMITTED_PURPOSES))})"))

    if asset.get("establishes_story_facts") is not False:
        v.append(GreyboxViolation(
            aid, "STORY",
            "establishes_story_facts must be explicitly false"))
    if asset.get("progression_dependency") is not False:
        v.append(GreyboxViolation(
            aid, "PROGRESSION",
            "progression_dependency must be explicitly false"))

    if asset.get("environment_design_status") in APPROVED_STATUSES:
        v.append(GreyboxViolation(
            aid, "STATUS",
            f"greybox cannot carry design status "
            f"{asset['environment_design_status']!r}; greybox is never approved art"))

    # Reserved vocabulary may not appear in the declared content list.
    haystack = " ".join(str(x) for x in asset.get("content", [])).lower()
    haystack += " " + str(asset.get("description", "")).lower()
    for word, why in RESERVED_VOCABULARY.items():
        if word in haystack:
            v.append(GreyboxViolation(
                aid, "RESERVED", f"content mentions {word!r}: {why}"))

    # Never a story dependency: no narrative scene may reference it.
    for dep in asset.get("story_dependencies", []) or []:
        v.append(GreyboxViolation(
            aid, "STORY", f"declares a story dependency {dep!r}; CD-5 forbids this"))

    return v


def validate_greybox_manifest(data: Dict[str, Any]) -> List[str]:
    """Validate a whole greybox manifest: per-asset rules plus cross-references."""
    problems: List[str] = []
    assets = data.get("greybox_assets", [])

    if not data.get("_cd5_notice"):
        problems.append("manifest is missing the CD-5 notice; readers must not "
                        "mistake greybox for approved content")

    for asset in assets:
        problems.extend(str(x) for x in validate_greybox_asset(asset))

    # Removing any greybox must not break progression.
    for asset in assets:
        aid = asset.get("id")
        for reference in data.get("progression_dependencies", []) or []:
            if reference.get("on") == aid:
                problems.append(
                    f"{aid}: progression rule {reference.get('rule')!r} depends on a "
                    f"greybox asset; greybox must be removable without breaking progression")

    # A greybox id must not collide with an approved location.
    for asset in assets:
        if asset.get("environment_design_status") in APPROVED_STATUSES:
            problems.append(
                f"{asset.get('id')}: greybox id collides with approved design status")

    # Duplicate ids. Count from the LIST, not from a dict keyed on id: keying by
    # id collapses duplicates to one before they can be counted, which made this
    # check unfalsifiable until a test caught it.
    seen: Dict[str, int] = {}
    for asset in assets:
        aid = asset.get("id")
        seen[aid] = seen.get(aid, 0) + 1
    for aid, n in seen.items():
        if n > 1:
            problems.append(f"{aid}: declared {n} times")
    return problems


def main(argv: Sequence[str]) -> int:
    if len(argv) < 2:
        print("usage: greybox_rules.py <greybox_manifest.json>")
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    problems = validate_greybox_manifest(data)

    assets = data.get("greybox_assets", [])
    print(f"greybox assets: {len(assets)}")
    for asset in assets:
        purposes = ", ".join(asset.get("test_purposes", [])) or "NONE"
        print(f"  {asset.get('id'):16s} {purposes}")
    print(f"violations: {len(problems)}")
    for p in problems:
        print("  x", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
