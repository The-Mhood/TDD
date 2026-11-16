#!/usr/bin/env python3
"""Tests for the Drive register parser.

Fixtures are verbatim Chapter 1 excerpts of the real registers as read from
Google Drive on 2026-11-16, including their irregularities (annotated design
statuses, "(Name)" suffixes, backticked board references). A parser only tested
on tidy synthetic input would fail on the real documents.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))

import registers as reg  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def location_text() -> str:
    return (FIXTURES / "location_register_ch01_excerpt.md").read_text(encoding="utf-8")


def scene_text() -> str:
    return (FIXTURES / "scene_register_ch01_excerpt.md").read_text(encoding="utf-8")


class TestIdPattern(unittest.TestCase):
    def test_all_location_categories_recognised(self):
        for category in reg.LOCATION_CATEGORIES:
            candidate = f"CH01-{category}-001"
            self.assertTrue(reg.split_id(candidate), candidate)

    def test_scene_ids_recognised(self):
        self.assertTrue(reg.split_id("CH01-SCN-046"))

    def test_boss_arena_uses_bos_not_boss(self):
        """The register uses BOS. An earlier engineering proposal used BOSS."""
        self.assertTrue(reg.split_id("CH01-BOS-001"))
        self.assertFalse(reg.split_id("CH01-BOSS-001"))

    def test_malformed_ids_rejected(self):
        for bad in ("CH1-SUB-001", "CH09-SUB-001", "CH01-SUB-1", "CH01-XXX-001",
                    "CH01-SUB-001-P", "ch01-sub-001", ""):
            self.assertFalse(reg.split_id(bad), bad)

    def test_chapter_and_category_helpers(self):
        self.assertEqual(reg.chapter_of("CH04-SUB-002"), "CH04")
        self.assertEqual(reg.category_of("CH04-SUB-002"), "SUB")
        self.assertIsNone(reg.chapter_of("garbage"))


class TestCanonVocabularies(unittest.TestCase):
    def test_canon_status_has_exactly_three_values(self):
        """Register v2.9: ESTABLISHED / PROPOSED / PENDING APPROVAL."""
        self.assertEqual(reg.CANON_STATUSES, ("ESTABLISHED", "PROPOSED", "PENDING APPROVAL"))

    def test_design_status_is_a_separate_axis(self):
        """OAD-48: environment design status is not canon status."""
        self.assertIn("EXPLORATORY", reg.ENV_DESIGN_STATUSES)
        self.assertIn("IN REVIEW", reg.ENV_DESIGN_STATUSES)
        for value in reg.ENV_DESIGN_STATUSES:
            self.assertNotIn(value, reg.CANON_STATUSES)

    def test_access_levels(self):
        self.assertEqual(len(reg.ACCESS_LEVELS), 5)
        self.assertIn("OPEN EXTERIOR", reg.ACCESS_LEVELS)


class TestMarkdownTableParsing(unittest.TestCase):
    def test_parses_every_table(self):
        tables = reg.parse_markdown_tables(location_text())
        self.assertGreaterEqual(len(tables), 1)

    def test_ignores_lines_that_only_start_with_pipe(self):
        text = "| not a table\n| still not\n\nplain text\n"
        self.assertEqual(reg.parse_markdown_tables(text), [])

    def test_ragged_row_does_not_crash(self):
        text = "| A | B |\n|---|---|\n| 1 |\n"
        tables = reg.parse_markdown_tables(text)
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0][0]["B"], "")


class TestLocationRegister(unittest.TestCase):
    def setUp(self):
        self.records = reg.parse_location_summary(location_text())
        self.by_id = {r.id: r for r in self.records}

    def test_parses_expected_locations(self):
        self.assertEqual(len(self.records), 13)

    def test_categories_captured(self):
        self.assertEqual(self.by_id["CH01-SUB-018"].category, "SUB")
        self.assertEqual(self.by_id["CH01-BOS-001"].category, "BOS")
        self.assertEqual(self.by_id["CH01-SET-001"].category, "SET")

    def test_canon_statuses_captured(self):
        self.assertEqual(self.by_id["CH01-ENV-001"].canon_status, "ESTABLISHED")
        self.assertEqual(self.by_id["CH01-SUB-018"].canon_status, "PROPOSED")
        self.assertEqual(self.by_id["CH01-SUB-001"].canon_status, "PENDING APPROVAL")

    def test_annotated_design_status_is_tolerated_by_validator(self):
        """The register writes e.g. 'IN REVIEW (revised; V002 submitted)'."""
        wells = self.by_id["CH01-SUB-014"]
        self.assertTrue(wells.env_design_status.startswith("IN REVIEW"))
        problems = reg.validate_locations(self.records)
        self.assertEqual(problems, [], problems)

    def test_boss_arena_is_established_canon(self):
        """OAD-21: the encounter is established even though the arena design is not."""
        arena = self.by_id["CH01-BOS-001"]
        self.assertEqual(arena.canon_status, "ESTABLISHED")
        self.assertEqual(arena.env_design_status, "IN REVIEW")

    def test_wayside_offering_place_is_only_proposed(self):
        """Memory 1's discovery location is NOT canon-approved. Engineering must
        never present it as established."""
        self.assertEqual(self.by_id["CH01-SUB-018"].canon_status, "PROPOSED")

    def test_design_approval_does_not_imply_canon(self):
        for rec in self.records:
            if rec.env_design_status.startswith("APPROVED"):
                # Legal in principle, but the canon axis stays independent.
                self.assertIn(rec.canon_status, reg.CANON_STATUSES)

    def test_invalid_canon_status_is_rejected(self):
        records = [reg.LocationRecord(
            id="CH01-SUB-019", name="X", category="SUB", kind="Sub-location",
            canon_status="APPROVED", env_design_status="IN REVIEW")]
        problems = reg.validate_locations(records)
        self.assertTrue(any("canon status" in p for p in problems), problems)

    def test_duplicate_location_is_rejected(self):
        duplicate = list(self.records) + [self.records[0]]
        problems = reg.validate_locations(duplicate)
        self.assertTrue(any("appears 2 times" in p for p in problems), problems)


class TestHierarchy(unittest.TestCase):
    def test_children_attached_to_major_environment(self):
        hierarchy = reg.parse_location_hierarchy(location_text())
        self.assertIn("CH01-ENV-001", hierarchy)
        children = hierarchy["CH01-ENV-001"]
        self.assertIn("CH01-SUB-001", children)
        self.assertIn("CH01-SUB-018", children)

    def test_landmark_header_does_not_become_a_parent_id(self):
        hierarchy = reg.parse_location_hierarchy(location_text())
        self.assertNotIn("Landmarks", hierarchy)
        self.assertIn("CH01-LMK-001", hierarchy["CH01-ENV-001"])


class TestSceneRegister(unittest.TestCase):
    def setUp(self):
        self.locations = reg.parse_location_summary(location_text())
        self.scenes = reg.parse_scene_summary(scene_text())
        self.by_id = {s.id: s for s in self.scenes}

    def test_parses_scenes(self):
        self.assertEqual(len(self.scenes), 4)

    def test_parent_location_extracted(self):
        self.assertEqual(self.by_id["CH01-SCN-046"].parent_id, "CH01-SUB-018")
        self.assertEqual(self.by_id["CH01-SCN-035"].parent_id, "CH01-ENV-001")

    def test_memory_scene_is_pending_approval(self):
        """CH01-SCN-046 (Memory 1) is PENDING APPROVAL in the register."""
        mem = self.by_id["CH01-SCN-046"]
        self.assertEqual(mem.canon_status, "PENDING APPROVAL")
        self.assertEqual(mem.scene_kind, "SECONDARY STORY SCENE")

    def test_ambient_scene_kind_and_access(self):
        scene = self.by_id["CH01-SCN-001"]
        self.assertEqual(scene.scene_kind, "AMBIENT NPC SCENE")
        self.assertEqual(scene.access, "OPEN EXTERIOR")

    def test_parent_missing_from_location_register_is_rejected(self):
        """CH01-INT-007 is referenced as a parent but was not in our excerpt,
        so it must be reported: a scene cannot hang off an unknown location."""
        problems = reg.validate_scenes(self.scenes, self.locations)
        self.assertTrue(
            any("CH01-SCN-001" in p and "not in the location register" in p for p in problems),
            problems,
        )

    def test_validation_clean_when_parents_present(self):
        locations = list(self.locations) + [reg.LocationRecord(
            id="CH01-INT-007", name="A Small Family House", category="INT",
            kind="Interior", canon_status="PROPOSED", env_design_status="IN REVIEW")]
        self.assertEqual(reg.validate_scenes(self.scenes, locations), [])

    def test_unknown_scene_kind_is_rejected(self):
        scene = reg.SceneRecord(id="CH01-SCN-050", name="X", parent_id="CH01-ENV-001",
                                scene_kind="MUSICAL NUMBER", access="OPEN EXTERIOR",
                                canon_status="PROPOSED", chapter="CH01")
        problems = reg.validate_scenes([scene], self.locations)
        self.assertTrue(any("scene kind" in p for p in problems), problems)

    def test_unknown_access_level_is_rejected(self):
        scene = reg.SceneRecord(id="CH01-SCN-050", name="X", parent_id="CH01-ENV-001",
                                scene_kind="ATMOSPHERIC SCENE", access="FLYABLE",
                                canon_status="PROPOSED", chapter="CH01")
        problems = reg.validate_scenes([scene], self.locations)
        self.assertTrue(any("access" in p for p in problems), problems)


class TestExtract(unittest.TestCase):
    def test_extract_shape(self):
        data = reg.extract(location_text(), scene_text())
        self.assertIn("meta", data)
        self.assertIn("locations", data)
        self.assertIn("scenes", data)
        self.assertIn("hierarchy", data)
        self.assertIn("validation", data)

    def test_counts_by_chapter(self):
        data = reg.extract(location_text(), scene_text())
        ch01 = data["counts_by_chapter"]["CH01"]
        self.assertEqual(ch01["_total"], 13)
        self.assertEqual(ch01["SCN"], 4)
        self.assertEqual(ch01["BOS"], 1)

    def test_extract_reports_the_missing_parent(self):
        data = reg.extract(location_text(), scene_text())
        problems = data["validation"]["scene_problems"]
        self.assertTrue(any("CH01-INT-007" in p for p in problems), problems)

    def test_register_count_table_columns_sum_to_scene_total(self):
        """Within the register's own count table, the category columns must sum
        to the 'Scenes' column for every row, including the Total row.

        This is a single-row invariant, so it is checkable on a one-chapter
        excerpt. Cross-chapter grand totals cannot be verified without all eight
        chapters and are therefore a full-register task (Stage 6).
        """
        tables = reg.parse_markdown_tables(scene_text())
        count_table = next(t for t in tables if "Main Story Scene" in t[0])

        def as_int(cell: str) -> int:
            # The register bolds its totals, e.g. "**135**".
            return int(cell.replace("*", "").strip())

        category_columns = [k for k in count_table[0]
                            if k not in ("Chapter", "Scenes")]
        self.assertGreaterEqual(len(category_columns), 5)

        checked = 0
        for row in count_table:
            if not row.get("Scenes"):
                continue
            declared_scenes = as_int(row["Scenes"])
            summed = sum(as_int(row[c]) for c in category_columns)
            self.assertEqual(
                declared_scenes, summed,
                f"row {row.get('Chapter')!r}: categories sum to {summed} "
                f"but the row declares {declared_scenes} scenes",
            )
            checked += 1
        self.assertGreaterEqual(checked, 2, "expected a chapter row and a total row")


if __name__ == "__main__":
    unittest.main(verbosity=2)
