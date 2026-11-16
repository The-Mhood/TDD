#!/usr/bin/env python3
"""Tests for CD-5 greybox restriction enforcement.

A restriction that cannot fail is not a restriction. Each test here breaks one
specific clause of TD decision CD-5 and asserts the validator catches it.
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

import greybox_rules as gr  # noqa: E402

MANIFEST_PATH = REPO_ROOT / "Tools" / "world" / "data" / "greybox_ch01.json"


def setUpModule() -> None:  # noqa: N802
    global MANIFEST
    MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def pending_asset():
    """A minimal valid PENDING APPROVAL greybox asset."""
    return {
        "id": "CH01-TEST-001",
        "register_canon_status": "PENDING APPROVAL",
        "label": gr.MANDATORY_LABEL,
        "test_purposes": ["SPATIAL"],
        "establishes_story_facts": False,
        "progression_dependency": False,
        "environment_design_status": "NOT STARTED",
        "content": ["room box"],
    }


class TestShippedManifestIsClean(unittest.TestCase):
    def test_no_violations(self):
        self.assertEqual(gr.validate_greybox_manifest(MANIFEST), [])

    def test_manifest_carries_cd5_notice(self):
        self.assertIn("CD-5", MANIFEST["_cd5_notice"])

    def test_manifest_states_nothing_was_built(self):
        self.assertIn("No greybox asset in this file has been built",
                      MANIFEST["_status_note"])

    def test_no_progression_dependencies_declared(self):
        self.assertEqual(MANIFEST["progression_dependencies"], [])


class TestLabelRestriction(unittest.TestCase):
    def test_pending_approval_requires_exact_label(self):
        asset = pending_asset()
        asset["label"] = "greybox"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "LABEL" for x in v), v)

    def test_pending_approval_without_label_fails(self):
        asset = pending_asset()
        asset["label"] = None
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "LABEL" for x in v), v)

    def test_em_dash_variant_is_rejected(self):
        """A hyphen instead of an em dash is not the mandated label."""
        asset = pending_asset()
        asset["label"] = "PENDING APPROVAL - BLOCKOUT ONLY"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "LABEL" for x in v), v)

    def test_established_canon_must_not_be_labelled_pending(self):
        asset = pending_asset()
        asset["register_canon_status"] = "ESTABLISHED"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "LABEL" for x in v), v)

    def test_unknown_status_is_rejected(self):
        asset = pending_asset()
        asset["register_canon_status"] = "APPROVED"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STATUS" for x in v), v)


class TestPurposeRestriction(unittest.TestCase):
    def test_only_four_purposes_permitted(self):
        self.assertEqual(gr.PERMITTED_PURPOSES,
                         {"SPATIAL", "NAVIGATION", "STREAMING", "SIGHTLINE"})

    def test_missing_purpose_fails(self):
        asset = pending_asset()
        asset["test_purposes"] = []
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "PURPOSE" for x in v), v)

    def test_combat_test_purpose_is_rejected(self):
        """CD-5 permits technical evaluation of space, not gameplay approval."""
        asset = pending_asset()
        asset["test_purposes"] = ["SPATIAL", "COMBAT"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "PURPOSE" for x in v), v)

    def test_story_test_purpose_is_rejected(self):
        asset = pending_asset()
        asset["test_purposes"] = ["NARRATIVE"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "PURPOSE" for x in v), v)


class TestStoryAndProgressionRestrictions(unittest.TestCase):
    def test_story_facts_must_be_explicitly_false(self):
        asset = pending_asset()
        asset["establishes_story_facts"] = True
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STORY" for x in v), v)

    def test_story_facts_missing_is_not_treated_as_false(self):
        """Absence of a declaration must not silently pass."""
        asset = pending_asset()
        del asset["establishes_story_facts"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STORY" for x in v), v)

    def test_progression_dependency_must_be_false(self):
        asset = pending_asset()
        asset["progression_dependency"] = True
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "PROGRESSION" for x in v), v)

    def test_declared_story_dependency_is_rejected(self):
        asset = pending_asset()
        asset["story_dependencies"] = ["CH01-SCN-046"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STORY" for x in v), v)

    def test_removal_breaks_nothing(self):
        """Removing the greybox must not fail the manifest."""
        stripped = copy.deepcopy(MANIFEST)
        stripped["greybox_assets"] = []
        self.assertEqual(gr.validate_greybox_manifest(stripped), [])

    def test_progression_rule_on_greybox_fails(self):
        bad = copy.deepcopy(MANIFEST)
        bad["progression_dependencies"] = [
            {"rule": "gate opens", "on": "CH01-SUB-018"}]
        problems = gr.validate_greybox_manifest(bad)
        self.assertTrue(any("removable without breaking" in p for p in problems), problems)


class TestReservedVocabulary(unittest.TestCase):
    def test_shrine_content_is_rejected(self):
        asset = pending_asset()
        asset["content"] = ["shrine platform"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "RESERVED" for x in v), v)

    def test_mask_content_is_rejected(self):
        asset = pending_asset()
        asset["content"] = ["mask rack"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "RESERVED" for x in v), v)

    def test_ritual_content_is_rejected(self):
        asset = pending_asset()
        asset["description"] = "ritual space"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "RESERVED" for x in v), v)

    def test_final_art_texture_is_rejected(self):
        asset = pending_asset()
        asset["content"] = ["texture set"]
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "RESERVED" for x in v), v)

    def test_plain_geometry_passes(self):
        asset = pending_asset()
        asset["content"] = ["wall volumes", "floor plane", "doorway"]
        self.assertEqual(gr.validate_greybox_asset(asset), [])

    def test_shipped_assets_contain_no_reserved_vocabulary(self):
        for asset in MANIFEST["greybox_assets"]:
            found = [x for x in gr.validate_greybox_asset(asset) if x.rule == "RESERVED"]
            self.assertEqual(found, [], asset["id"])


class TestApprovalIsNeverChanged(unittest.TestCase):
    def test_greybox_cannot_carry_approved_status(self):
        asset = pending_asset()
        asset["environment_design_status"] = "APPROVED"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STATUS" for x in v), v)

    def test_greybox_cannot_carry_conditional_status(self):
        asset = pending_asset()
        asset["environment_design_status"] = "CONDITIONAL"
        v = gr.validate_greybox_asset(asset)
        self.assertTrue(any(x.rule == "STATUS" for x in v), v)

    def test_shipped_assets_match_register_canon_status(self):
        """Every greybox asset's declared canon status must agree with the mirror."""
        idx = json.loads(
            (REPO_ROOT / "Tools" / "canon" / "data" / "canon_index.json").read_text())
        by_id = {loc["id"]: loc for loc in idx["locations"]}
        for asset in MANIFEST["greybox_assets"]:
            loc = by_id.get(asset["id"])
            self.assertIsNotNone(loc, f"{asset['id']} not in canon mirror")
            self.assertEqual(asset["register_canon_status"], loc["canon_status"],
                             f"{asset['id']} status disagrees with register mirror")


class TestDuplicateIds(unittest.TestCase):
    def test_duplicate_asset_id_fails(self):
        bad = copy.deepcopy(MANIFEST)
        bad["greybox_assets"].append(copy.deepcopy(bad["greybox_assets"][0]))
        problems = gr.validate_greybox_manifest(bad)
        self.assertTrue(any("declared 2 times" in p for p in problems), problems)

    def test_missing_cd5_notice_fails(self):
        bad = copy.deepcopy(MANIFEST)
        del bad["_cd5_notice"]
        problems = gr.validate_greybox_manifest(bad)
        self.assertTrue(any("CD-5 notice" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main(verbosity=2)
