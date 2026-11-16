#!/usr/bin/env python3
"""Tests for the Agent 2 contract-submission data claims.

These are L0-data tests over register fixtures. They exist because
`Docs/CONTRACT_SUBMISSION_A2_V1.md` makes factual claims about the register's
vocabulary, and a claim in prose cannot be checked by a reviewer who does not
have the register open.

The central test is `TestTraversalIsNotAPrefix`. An earlier draft of my own C-01
proposal anchored routes on the `CH0n-TRV-nnn` ID prefix. The register's
`Category` field is multi-valued, so that would have silently excluded three
legitimate entries - one of them ESTABLISHED. The test below fails against a
prefix-only parser, which is the point.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import registers as reg  # noqa: E402
import contract_data_checks as cdc  # noqa: E402

RECORDS = cdc.load_summary()


class TestFixtureIntegrity(unittest.TestCase):
    def test_fixture_parses_all_57_rows(self):
        self.assertEqual(len(RECORDS), 57)

    def test_ids_are_unique(self):
        ids = [r.id for r in RECORDS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_family_counts_reproduce_published_split(self):
        checks = {c.name: c for c in cdc.run_all()}
        self.assertTrue(checks["ch01_family_counts"].passed,
                        checks["ch01_family_counts"].problems)

    def test_excerpt_remains_a_subset(self):
        """The older 13-row excerpt must not contradict the 57-row capture."""
        checks = {c.name: c for c in cdc.run_all()}
        self.assertTrue(checks["excerpt_is_subset_of_full_capture"].passed,
                        checks["excerpt_is_subset_of_full_capture"].problems)


class TestTraversalIsNotAPrefix(unittest.TestCase):
    """The C-01 finding: capability is a category tag, not an ID prefix."""

    def test_register_tags_eight_locations_as_traversal(self):
        traversal = [r for r in RECORDS if cdc.TRAVERSAL_TAG in r.kind]
        self.assertEqual(len(traversal), 8)

    def test_three_traversal_locations_are_outside_the_trv_prefix(self):
        traversal = [r for r in RECORDS if cdc.TRAVERSAL_TAG in r.kind]
        outside = sorted(r.id for r in traversal if r.category != "TRV")
        self.assertEqual(outside, ["CH01-EXP-003", "CH01-SUB-009", "CH01-SUB-020"])

    def test_a_prefix_only_parser_would_lose_three_locations(self):
        """This is the regression the proposal had to be corrected for.

        A prefix-only selection is not merely shorter - it drops
        `CH01-SUB-009 Streets`, which is ESTABLISHED, so the loss is content the
        project cannot withdraw.
        """
        prefix_only = {r.id for r in RECORDS if r.category == "TRV"}
        by_tag = {r.id for r in RECORDS if cdc.TRAVERSAL_TAG in r.kind}
        lost = by_tag - prefix_only
        self.assertTrue(lost, "a prefix filter must lose something; if not, "
                              "the multi-valued finding is stale")
        self.assertEqual(lost, {"CH01-SUB-009", "CH01-SUB-020", "CH01-EXP-003"})

    def test_at_least_one_traversal_location_is_established(self):
        """If every traversal location were PROPOSED, a canon review could
        withdraw all traversal content at once. Two are ESTABLISHED."""
        established = [r.id for r in RECORDS
                       if cdc.TRAVERSAL_TAG in r.kind
                       and r.canon_status == "ESTABLISHED"]
        self.assertEqual(established, ["CH01-SUB-009", "CH01-TRV-005"])

    def test_named_trv_areas_are_register_values_not_inventions(self):
        """v0.1.0 of my traversal request called these 'PROVISIONAL'. They are
        register values; the fixture now records them as such."""
        by_id = {r.id: r for r in RECORDS}
        self.assertEqual(by_id["CH01-TRV-002"].name, "The Root Way")
        self.assertEqual(by_id["CH01-TRV-003"].name, "The Stream Crossing")
        self.assertEqual(by_id["CH01-TRV-004"].name, "The Ravine and Liana Bridge")
        self.assertEqual(by_id["CH01-TRV-005"].name, "Roads")
        self.assertEqual(by_id["CH01-TRV-005"].canon_status, "ESTABLISHED")


class TestExplorationIsAlsoMultivalued(unittest.TestCase):
    def test_eight_locations_carry_the_exploration_tag(self):
        exploration = [r for r in RECORDS if cdc.EXPLORATION_TAG in r.kind]
        self.assertEqual(len(exploration), 8)

    def test_one_exploration_location_is_outside_the_exp_prefix(self):
        exploration = [r for r in RECORDS if cdc.EXPLORATION_TAG in r.kind]
        outside = [r.id for r in exploration if r.category != "EXP"]
        self.assertEqual(outside, ["CH01-SUB-003"])


class TestVocabularyIsClosed(unittest.TestCase):
    def test_canon_status_has_exactly_three_values(self):
        statuses = {r.canon_status for r in RECORDS}
        self.assertEqual(statuses,
                         {"ESTABLISHED", "PROPOSED", "PENDING APPROVAL"})

    def test_environment_design_status_is_separate_and_seven_valued(self):
        """OAD-48: approving a design does not change canon status."""
        statuses = {r.env_design_status for r in RECORDS}
        self.assertTrue(statuses.issubset({
            "NOT STARTED", "EXPLORATORY", "IN REVIEW", "REQUIRES REVISION",
            "CONDITIONAL", "APPROVED", "REJECTED"}))
        self.assertFalse(statuses & {"ESTABLISHED", "PROPOSED", "PENDING APPROVAL"},
                         "canon and design vocabularies must not be mixed")

    def test_pending_approval_locations_are_identifiable(self):
        """CD-5 blockout-only applies to these. A contract that could not
        identify them could not enforce the restriction."""
        pending = sorted(r.id for r in RECORDS
                         if r.canon_status == "PENDING APPROVAL")
        self.assertEqual(pending, ["CH01-EXP-002", "CH01-INT-016", "CH01-SUB-001"])


class TestStatedLimits(unittest.TestCase):
    """Honest scope. These assert that the checks do NOT overclaim."""

    def test_retirement_is_not_verifiable_from_a_summary_table(self):
        checks = {c.name: c for c in cdc.run_all()}
        self.assertIn("NOT verifiable", checks["location_ids_match_published_scheme"].detail)

    def test_interactable_namespace_is_recorded_as_unresolved(self):
        checks = {c.name: c for c in cdc.run_all()}
        c = checks["interactable_id_namespace_unresolved"]
        self.assertTrue(c.passed, "this check is informational, not a gate")
        self.assertIn("NO register source", c.detail)

    def test_no_check_claims_runtime_evidence(self):
        for c in cdc.run_all():
            self.assertNotIn("runtime verified", c.detail.lower())
            self.assertNotIn("measured in engine", c.detail.lower())


class TestProposalDocument(unittest.TestCase):
    DOC = REPO_ROOT / "Docs" / "CONTRACT_SUBMISSION_A2_V1.md"

    @classmethod
    def setUpClass(cls):
        cls.raw = cls.DOC.read_text(encoding="utf-8")
        cls.doc = cls.raw.replace("**", "").replace("*", "").replace("`", "")

    def test_all_seven_contracts_are_present(self):
        for n in range(1, 8):
            self.assertIn(f"C-0{n}", self.doc, f"C-0{n} missing")

    def test_nothing_claims_to_be_frozen_or_agreed(self):
        self.assertIn("PROPOSAL — NOT FROZEN", self.raw)
        self.assertIn("NOT RECEIVED", self.raw)
        for banned in ("AGREED_WITH_CONSUMERS", "FROZEN — ACCEPTED"):
            self.assertNotIn(banned, self.raw)

    def test_agreed_contract_count_is_zero(self):
        self.assertIn("0 of 7", self.doc)

    def test_document_records_the_governing_version_gap(self):
        """The request cited v1.2; only v1.1 exists. That must be stated."""
        self.assertIn("v1.2", self.raw)
        self.assertIn("v1.1", self.raw)

    def test_document_does_not_name_the_withdrawn_interactable_count(self):
        """An earlier draft said '62 world interactables'. It had no source."""
        body = self.raw
        # The withdrawal note may mention it; a live claim may not.
        live_claims = [l for l in body.splitlines()
                       if "62" in l and "withdrawn" not in l.lower()
                       and "no source" not in l.lower()]
        self.assertEqual(live_claims, [], "62 appears as a live claim")

    def test_document_names_the_three_missed_traversal_locations(self):
        for sid in ("CH01-SUB-009", "CH01-SUB-020", "CH01-EXP-003"):
            self.assertIn(sid, self.doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
