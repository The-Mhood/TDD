#!/usr/bin/env python3
"""Tests for count reconciliation (TR-2).

These tests exist because the project already shipped one wrong number: the
location-entry total was recorded as 191 when the register's own columns sum to
196. The guard test at the bottom makes that specific error fail loudly.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import count_reconciliation as cr  # noqa: E402
import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"


def setUpModule() -> None:  # noqa: N802
    global COUNTS, LOCATIONS, SCENES, RECON
    COUNTS = cr.load_register_counts()
    LOCATIONS = reg.parse_location_summary(
        (FIXTURES / "location_register_ch01_excerpt.md").read_text(encoding="utf-8"))
    SCENES = reg.parse_scene_summary(
        (FIXTURES / "scene_register_ch01_full.md").read_text(encoding="utf-8"))
    RECON = cr.reconcile_chapter(LOCATIONS, SCENES, COUNTS, "CH01")


class TestRegisterArithmetic(unittest.TestCase):
    def test_published_totals_equal_sum_of_per_chapter_rows(self):
        self.assertEqual(cr.check_published_consistency(COUNTS), [])

    def test_all_eight_chapters_present(self):
        self.assertEqual(sorted(COUNTS["per_chapter"]), [f"CH0{i}" for i in range(1, 9)])

    def test_derived_totals_are_self_consistent(self):
        self.assertEqual(cr.check_derived_totals(COUNTS), [])

    def test_location_entries_are_196(self):
        t = COUNTS["published_totals"]
        self.assertEqual(t["major_environments"] + t["other_locations_not_interiors"]
                         + t["interiors_location_entries"], 196)

    def test_subset_column_never_exceeds_parent(self):
        for chapter, row in COUNTS["per_chapter"].items():
            self.assertLessEqual(row["not_main_or_secondary_story"],
                                 row["scenes_and_microlocations"], chapter)


class TestDoubleCountingIsPrevented(unittest.TestCase):
    def test_entity_kinds_state_whether_they_are_locations(self):
        self.assertTrue(cr.ENTITY_KINDS["LOCATION"]["is_location_entry"])
        self.assertTrue(cr.ENTITY_KINDS["INTERIOR"]["is_location_entry"])
        self.assertTrue(cr.ENTITY_KINDS["MAJOR_ENVIRONMENT"]["is_location_entry"])
        self.assertFalse(cr.ENTITY_KINDS["SCENE"]["is_location_entry"])
        self.assertFalse(cr.ENTITY_KINDS["ENVIRONMENT_STATE"]["is_location_entry"])

    def test_states_are_never_location_entries(self):
        """40 state refs must never be added into the location total."""
        self.assertFalse(cr.ENTITY_KINDS["ENVIRONMENT_STATE"]["is_location_entry"])
        self.assertIn(40, COUNTS["published_totals"].values())
        t = COUNTS["published_totals"]
        self.assertNotIn("environment_state_references", [
            "major_environments", "other_locations_not_interiors",
            "interiors_location_entries"])

    def test_every_entity_kind_documents_its_double_count_risk(self):
        for kind, spec in cr.ENTITY_KINDS.items():
            self.assertIn("double_count_risk", spec, kind)
            self.assertTrue(spec["double_count_risk"], kind)

    def test_interior_double_count_risk_is_called_out_as_highest(self):
        self.assertIn("HIGHEST", cr.ENTITY_KINDS["INTERIOR"]["double_count_risk"])

    def test_micro_locations_are_scenes(self):
        """EXTERIOR MICRO-LOCATION scenes are scenes, not extra locations."""
        self.assertTrue(cr.ENTITY_KINDS["SCENE"]["is_scene"])
        self.assertIn("MICRO-LOCATION", cr.ENTITY_KINDS["SCENE"]["description"])


class TestChapterOneReconciles(unittest.TestCase):
    def test_scene_count_matches_register(self):
        self.assertEqual(RECON.comparisons["scenes_and_microlocations"]["parsed"], 46)
        self.assertEqual(RECON.parsed_scenes, 46)

    def test_non_story_scene_count_independently_corroborates_register(self):
        """The location register says 45 of Chapter 1's 46 scenes are not main or
        secondary story. The scene register's own category counts say the same.
        Two registers agreeing on a number is real corroboration."""
        self.assertEqual(RECON.parsed_scenes_not_main_or_secondary, 45)
        self.assertEqual(
            RECON.comparisons["not_main_or_secondary_story"]["published"], 45)

    def test_story_scene_categories_are_exactly_two(self):
        self.assertEqual(RECON.parsed_scenes_by_category["SECONDARY STORY SCENE"], 1)
        self.assertNotIn("MAIN STORY SCENE", RECON.parsed_scenes_by_category)

    def test_major_environment_is_exactly_one(self):
        self.assertEqual(RECON.parsed_locations_by_category["ENV"], 1)

    def test_partial_location_capture_is_labelled_not_failed(self):
        cmp = RECON.comparisons["interiors_location_entries"]
        self.assertFalse(cmp["complete_capture"])
        self.assertLess(cmp["parsed"], cmp["published"])

    def test_missing_parents_are_an_ingestion_gap(self):
        """40 scenes reference parents the partial fixture does not contain. That
        is our capture gap, and it must be recorded as such, not as a register bug."""
        cmp = RECON.comparisons["scenes_with_missing_parent"]
        self.assertEqual(cmp["parsed"], 40)
        self.assertIn("INGESTION GAP", cmp["note"])

    def test_chapter_one_has_no_register_self_contradiction(self):
        self.assertEqual(RECON.problems, [])


class TestTamperDetection(unittest.TestCase):
    def test_altered_row_total_is_detected(self):
        bad = copy.deepcopy(COUNTS)
        bad["published_totals"]["scenes_and_microlocations"] = 136
        problems = cr.check_published_consistency(bad)
        self.assertTrue(any("scenes_and_microlocations" in p for p in problems), problems)

    def test_impossible_subset_is_detected(self):
        bad = copy.deepcopy(COUNTS)
        bad["per_chapter"]["CH01"]["not_main_or_secondary_story"] = 99
        problems = cr.check_derived_totals(bad)
        self.assertTrue(any("exceeds scenes" in p for p in problems), problems)

    def test_scene_count_regression_is_detected(self):
        """Dropping a scene from the capture must fail the reconciliation."""
        problems = cr.reconcile_chapter(LOCATIONS, SCENES[:-1], COUNTS, "CH01").problems
        self.assertTrue(any("REGISTER OR PARSER INCONSISTENCY" in p for p in problems),
                        problems)


_SECTION_START = "<!-- COUNT-CHECK-DISCUSSION-START -->"
_SECTION_END = "<!-- COUNT-CHECK-DISCUSSION-END -->"


def _strip_marked_sections(text: str) -> str:
    """Remove explicitly marked discussion sections before the 191 scan.

    A review that documents this very check has to be able to name the number it
    flags. Exempting by *region* keeps the scan honest for ordinary prose, which is
    the only place a stale live count could mislead a reader.
    """
    out, skipping = [], False
    for line in text.splitlines():
        if _SECTION_START in line:
            skipping = True
            continue
        if _SECTION_END in line:
            skipping = False
            continue
        if not skipping:
            out.append(line)
    return "\n".join(out)


class TestNoStaleArithmetic(unittest.TestCase):
    """Guard against the specific error that already shipped once."""

    def test_canon_index_location_total_is_196_not_191(self):
        idx = json.loads(
            (REPO_ROOT / "Tools" / "canon" / "data" / "canon_index.json").read_text())
        counts = idx["world_counts_from_register"]
        self.assertEqual(counts["per_chapter_locations_total"], 196)

    def test_canon_index_derivation_is_recorded(self):
        idx = json.loads(
            (REPO_ROOT / "Tools" / "canon" / "data" / "canon_index.json").read_text())
        derivation = idx["world_counts_from_register"]["_location_entries_derivation"]
        self.assertIn("8 major environments", derivation)
        self.assertIn("NOT location entries", derivation)

    def test_no_document_claims_191_location_entries(self):
        offenders = []
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.suffix not in {".md", ".py", ".json"}:
                continue
            # W-M2.18: a test module that *exercises* this check must contain the
            # strings it asserts on. Same convention as the two names above.
            if path.name in ("test_count_reconciliation.py", "gen_evidence.py",
                             "test_review_a1c05_s4_3_7.py"):
                continue
            # Evidence artifacts record this correction as a claim; they are
            # generated output, not prose that could mislead a reader.
            if "evidence" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            # W-M2.18: a review *of this check* must be able to quote the number it
            # discusses. A document may fence such a discussion in an explicitly
            # marked section; the markers are the same shape as the QUOTED-HISTORY
            # regions the C-05 validator uses, so exemption is by location, never by
            # which words a line happens to contain.
            text = _strip_marked_sections(text)
            # A mention of 191 is legitimate only when it is describing the
            # historical error. Flag it when it is presented as a live count.
            correction_markers = ("corrects", "correction", "191 → 196",
                                  "191 -> 196", "recorded as 191", "was 191",
                                  "191 when")
            for line_no, line in enumerate(text.splitlines(), 1):
                if "191" not in line:
                    continue
                # A git object id is a hex digest, not a count. The suite blob
                # 2a33543a8b6941262915e9a33b614411910b030b contains the digits
                # "191" at offset 31 by coincidence, which made this check flag a
                # correct citation as a stale location count (W-M2.18). Mask
                # 7-40 char hex runs before looking for the count.
                line = re.sub(r"\b[0-9a-f]{7,40}\b", "<sha>", line, flags=re.I)
                if "191" not in line:
                    continue
                lowered = line.lower()
                if any(m in lowered for m in correction_markers):
                    continue
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{line_no}: {line.strip()}")
        self.assertEqual(offenders, [], "stale 191 location count:\n" + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main(verbosity=2)
