#!/usr/bin/env python3
"""Contract-submission validators for the Agent 2 world-side proposals.

This module validates **authored data**, not runtime behaviour. There is no
Unreal project and no engine. Everything here is L0-data: it reads register
fixtures, parses them, and asserts relationships. It establishes nothing about
how anything behaves when running.

Its purpose is narrow and deliberate: the C-01…C-07 submission
(`Docs/CONTRACT_SUBMISSION_A2_V1.md`) makes claims about the register's
vocabulary. Those claims are testable without an engine, so they are tested
here rather than asserted in prose.

Usage:
    python3 Tools/world/contract_data_checks.py [--verbose]
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))

import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
LOCATION_SUMMARY_V29 = FIXTURES / "location_register_ch01_summary_v29.md"
LOCATION_EXCERPT = FIXTURES / "location_register_ch01_excerpt.md"

#: The register's own published Chapter 1 counts, from the "Counts (kept separate,
#: never mixed)" table in LOCATION_MASTER_REGISTER v2.9. These are transcribed,
#: not derived - if they disagree with the parsed rows, one of the two is wrong
#: and the disagreement is the finding.
PUBLISHED_CH01 = {
    "major_environments": 1,
    "other_locations_not_interiors": 40,
    "interiors_location_entries": 16,
    "total_location_entries": 57,
}

#: Category tags must be multi-valued aware. "Traversal Area" appears on SUB and
#: EXP entries as well as on TRV ones; a validator keyed on the ID prefix alone
#: silently loses three legitimate register entries.
TRAVERSAL_TAG = "Traversal Area"
EXPLORATION_TAG = "Exploration Area"


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    problems: List[str] = field(default_factory=list)


def load_summary() -> List[reg.LocationRecord]:
    text = LOCATION_SUMMARY_V29.read_text(encoding="utf-8")
    return reg.parse_location_summary(text)


def check_row_count(records: Sequence[reg.LocationRecord]) -> Check:
    """57 rows, matching the register's own published total."""
    problems: List[str] = []
    if len(records) != PUBLISHED_CH01["total_location_entries"]:
        problems.append(
            f"parsed {len(records)} location rows, register publishes "
            f"{PUBLISHED_CH01['total_location_entries']}")
    ids = [r.id for r in records]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append(f"duplicate location IDs: {dupes}")
    return Check("ch01_location_row_count", not problems,
                 f"{len(records)} rows, {len(set(ids))} unique", problems)


def check_family_counts(records: Sequence[reg.LocationRecord]) -> Check:
    """Per-family counts must reproduce the register's published split."""
    problems: List[str] = []
    by_prefix: Dict[str, int] = {}
    for r in records:
        by_prefix[r.category] = by_prefix.get(r.category, 0) + 1

    interiors = by_prefix.get("INT", 0)
    envs = by_prefix.get("ENV", 0)
    others = sum(v for k, v in by_prefix.items() if k not in {"ENV", "INT"})

    if envs != PUBLISHED_CH01["major_environments"]:
        problems.append(f"ENV {envs} != published "
                        f"{PUBLISHED_CH01['major_environments']}")
    if interiors != PUBLISHED_CH01["interiors_location_entries"]:
        problems.append(f"INT {interiors} != published "
                        f"{PUBLISHED_CH01['interiors_location_entries']}")
    if others != PUBLISHED_CH01["other_locations_not_interiors"]:
        problems.append(f"non-interior others {others} != published "
                        f"{PUBLISHED_CH01['other_locations_not_interiors']}")
    return Check("ch01_family_counts", not problems,
                 f"ENV {envs} + others {others} + INT {interiors} = "
                 f"{envs + others + interiors}", problems)


def check_traversal_is_multivalued(
        records: Sequence[reg.LocationRecord]) -> Check:
    """THE FINDING. Traversal capability is a category TAG, not an ID prefix.

    A contract that anchors routes on `CH0n-TRV-nnn` only would exclude
    `SUB-009 Streets`, `SUB-020 The Back Lanes` and `EXP-003 The Forgotten Path`
    - all three marked "Traversal Area" by the register itself. Two of the
    three are legitimate register entries regardless of their prefix, and
    `SUB-009` is ESTABLISHED, so it cannot be dismissed as a proposal.
    """
    problems: List[str] = []
    traversal = [r for r in records if TRAVERSAL_TAG in r.kind]
    prefix_only = [r for r in records if r.category == "TRV"]
    missed = [r.id for r in traversal if r.category != "TRV"]

    if not traversal:
        problems.append("no Traversal Area rows found - fixture or parser broken")
    if len(traversal) <= len(prefix_only):
        problems.append(
            f"traversal-capable ({len(traversal)}) must exceed TRV-prefixed "
            f"({len(prefix_only)}); the register tags SUB and EXP entries too")
    for expected in ("CH01-SUB-009", "CH01-SUB-020", "CH01-EXP-003"):
        if expected not in [r.id for r in traversal]:
            problems.append(f"{expected} carries 'Traversal Area' but was not parsed")
    if expected_established := [
            r.id for r in traversal if r.canon_status == "ESTABLISHED"]:
        pass  # presence recorded in detail
    else:
        problems.append("no ESTABLISHED traversal-capable location; "
                        "every traversal route would rest on a PROPOSED entry")

    detail = (f"{len(traversal)} traversal-capable of {len(records)}; "
              f"TRV-prefix-only would find {len(prefix_only)} and miss {missed}")
    return Check("traversal_category_is_multivalued", not problems, detail, problems)


def check_exploration_is_multivalued(
        records: Sequence[reg.LocationRecord]) -> Check:
    """Same shape of defect for 'Exploration Area'."""
    problems: List[str] = []
    exploration = [r for r in records if EXPLORATION_TAG in r.kind]
    missed = [r.id for r in exploration if r.category != "EXP"]
    if not exploration:
        problems.append("no Exploration Area rows found")
    if missed != ["CH01-SUB-003"]:
        problems.append(
            f"expected exactly SUB-003 outside the EXP prefix, got "
            f"{missed} - if this changed, re-check the register")
    return Check("exploration_category_is_multivalued", not problems,
                 f"{len(exploration)} exploration-capable; non-EXP: {missed}",
                 problems)


def check_canon_status_vocabulary(
        records: Sequence[reg.LocationRecord]) -> Check:
    """Exactly three canon statuses, per the register's own rule."""
    allowed = {"ESTABLISHED", "PROPOSED", "PENDING APPROVAL"}
    problems: List[str] = []
    for r in records:
        if r.canon_status not in allowed:
            problems.append(f"{r.id}: canon status {r.canon_status!r} not in "
                            f"{sorted(allowed)}")
    counts: Dict[str, int] = {}
    for r in records:
        counts[r.canon_status] = counts.get(r.canon_status, 0) + 1
    return Check("canon_status_has_three_values", not problems,
                 f"{dict(sorted(counts.items()))}", problems)


def check_environment_design_vocabulary(
        records: Sequence[reg.LocationRecord]) -> Check:
    """Seven environment-design statuses, separate from canon status (OAD-48)."""
    allowed = {"NOT STARTED", "EXPLORATORY", "IN REVIEW", "REQUIRES REVISION",
               "CONDITIONAL", "APPROVED", "REJECTED"}
    problems: List[str] = []
    for r in records:
        if r.env_design_status not in allowed:
            problems.append(
                f"{r.id}: env design status {r.env_design_status!r} not in "
                f"{sorted(allowed)}")
    return Check("env_design_status_has_seven_values", not problems,
                 f"{len(records)} rows checked against {len(allowed)} allowed values",
                 problems)


def check_no_retired_or_reused_ids(
        records: Sequence[reg.LocationRecord]) -> Check:
    """IDs must match the published scheme and not be reused.

    The register states: 'IDs are permanent. Retired IDs stay in the register
    and are never reused.' We cannot detect a *retired* ID from a summary table
    alone (that information lives in the register's retirement notes), so this
    check is explicit about its own limit rather than implying more.
    """
    import re
    pattern = re.compile(
        r"^CH0[1-8]-(ENV|SUB|SET|INT|LMK|TRV|EXP|BOS)-\d{3}$")
    problems: List[str] = []
    for r in records:
        if not pattern.match(r.id):
            problems.append(f"{r.id}: does not match the published ID scheme")
        if r.category != r.id.split("-")[1]:
            problems.append(
                f"{r.id}: parsed category {r.category!r} disagrees with the ID "
                f"prefix - category_of() and the register disagree")
    return Check("location_ids_match_published_scheme", not problems,
                 f"{len(records)} IDs checked; retirement NOT verifiable from a "
                 f"summary table (stated limit)", problems)


def check_excerpt_is_subset(records: Sequence[reg.LocationRecord]) -> Check:
    """The older 13-row excerpt must remain a strict subset of this capture."""
    problems: List[str] = []
    excerpt_text = LOCATION_EXCERPT.read_text(encoding="utf-8")
    excerpt = reg.parse_location_summary(excerpt_text)
    full_ids = {r.id for r in records}
    missing = [r.id for r in excerpt if r.id not in full_ids]
    if missing:
        problems.append(
            f"excerpt rows absent from the full capture: {missing} - the two "
            f"fixtures disagree, which means one of them was mis-transcribed")
    return Check("excerpt_is_subset_of_full_capture", not problems,
                 f"excerpt {len(excerpt)} rows, all present in the {len(records)}-row "
                 f"capture", problems)


def check_interactable_id_unresolved() -> Check:
    """C-07 §9.2: interactables have NO register source. This is a stated gap.

    This check does not fail - it records a known absence so that nobody later
    assumes an interactable ID scheme was decided. A check that passed silently
    here would be the thing to worry about.
    """
    return Check(
        "interactable_id_namespace_unresolved",
        True,
        "NO register source exists for interactable IDs. Options A (scene-derived), "
        "B (new CH0n-ACT-nnn family) and C (actor name only) are all unresolved; "
        "see Docs/CONTRACT_SUBMISSION_A2_V1.md section 9.2 and TD-3.",
        [])


def run_all() -> List[Check]:
    records = load_summary()
    return [
        check_row_count(records),
        check_family_counts(records),
        check_traversal_is_multivalued(records),
        check_exploration_is_multivalued(records),
        check_canon_status_vocabulary(records),
        check_environment_design_vocabulary(records),
        check_no_retired_or_reused_ids(records),
        check_excerpt_is_subset(records),
        check_interactable_id_unresolved(),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    checks = run_all()
    failed = [c for c in checks if not c.passed]
    for c in checks:
        mark = "PASS" if c.passed else "FAIL"
        print(f"[{mark}] {c.name}")
        if args.verbose or not c.passed:
            print(f"        {c.detail}")
            for p in c.problems:
                print(f"        ! {p}")
    print()
    print("NOTE: L0-data validation only. No engine, no runtime evidence.")
    print(f"checks: {len(checks) - len(failed)}/{len(checks)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
