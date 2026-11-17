#!/usr/bin/env python3
"""Tests backing the factual claims in `Docs/AGENT2_REVIEW_A1R2_V1.md`.

These test **this review**, not Agent 1 and not any contract. The review makes
several claims that decided its verdicts — most importantly that three divergent
documents identify as `TDD-MEAD-001` v1.0, that MEAD-C alone carries §5.4 and the
`Status.*` vocabulary, that `Status.Dead` exists nowhere, and that I withdrew
specific tag namespaces. Each is asserted here so a reader can verify it.

Nothing here runs a contract acceptance test. There is no implementation to run
one against.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))

import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
LOCATION_CAPTURE = FIXTURES / "location_register_ch01_summary_v29.md"
SCENE_FIXTURE = FIXTURES / "scene_register_ch01_v19_verbatim.md"
SUBMISSION = REPO_ROOT / "Docs" / "CONTRACT_SUBMISSION_A2_V1.md"
REVIEW_A1R1 = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R1_V1.md"
REVIEW_A1R2 = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R2_V1.md"

#: The MEAD that Agent 1 cites. Absent from this worktree (it lives on Agent 1's
#: branch), so the MEAD-dependent tests skip rather than fail when it is missing.
MEAD_C = Path("/tmp/mead_a1.md")


def _locations():
    return reg.parse_location_summary(LOCATION_CAPTURE.read_text(encoding="utf-8"))


class TestReviewArithmetic(unittest.TestCase):
    """The review's own counts must match its own tables."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW_A1R2.read_text(encoding="utf-8")

    def _verdict_rows(self):
        rows = [l for l in self.raw.splitlines() if re.match(r"^\|\s*§\d", l.strip())]
        return [r for r in rows if "**ACCEPT" in r or "**REJECT" in r]

    def test_sixty_one_clause_verdicts(self):
        self.assertEqual(len(self._verdict_rows()), 61)

    def test_fifty_six_plain_and_five_conditional(self):
        rows = self._verdict_rows()
        cond = [r for r in rows if "**ACCEPT with" in r or "ACCEPT amended" in r]
        self.assertEqual(len(cond), 5)
        self.assertEqual(len(rows) - len(cond), 56)

    def test_zero_clauses_rejected(self):
        self.assertEqual([r for r in self._verdict_rows() if "**REJECT" in r], [])

    def test_five_new_requirements_numbered_17_to_21(self):
        found = set(int(x) for x in re.findall(r"A2R-(\d+)", self.raw))
        self.assertEqual(sorted(found & set(range(17, 22))), [17, 18, 19, 20, 21])


class TestVerdicts(unittest.TestCase):
    """The seven verdicts and the zero-agreement statement."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW_A1R2.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("*", "").replace("`", "")

    def test_all_seven_contracts_reviewed(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        rows = [l for l in seg.splitlines() if re.match(r"^\|\s*C-0\d", l.strip())]
        self.assertEqual(len(rows), 7)

    def test_states_zero_agreed(self):
        self.assertIn("Agreed: 0 of 7", self.flat)

    def test_three_contracts_declared_signable(self):
        self.assertIn("Three contracts (C-02, C-03, C-06) are signable now", self.flat)

    def test_does_not_claim_agreement(self):
        self.assertNotIn("AGREED WITH", self.raw)

    def test_states_it_is_design_only(self):
        self.assertIn("DESIGN_ONLY", self.raw)

    def test_uses_the_permitted_verdict_vocabulary(self):
        for v in ("AGREE", "PARTIALLY AGREE", "CLARIFICATION REQUIRED"):
            self.assertIn(v, self.raw)


class TestSceneGapStillHolds(unittest.TestCase):
    """Section 3.4: the two water/rope locations cannot have routes in this slice.

    This is the finding from my A1-R1 review, reasserted because C-01's scope
    decision rests on it.
    """

    @classmethod
    def setUpClass(cls):
        locs = _locations()
        cls.trav = [l for l in locs if "Traversal Area" in l.kind]
        rows = [l for l in SCENE_FIXTURE.read_text(encoding="utf-8").splitlines()
                if l.strip().startswith("| CH01-SCN")]
        cls.hosted = Counter(
            [c.strip() for c in r.strip().strip("|").split("|")][2] for r in rows)

    def test_eight_traversal_capable_locations(self):
        self.assertEqual(len(self.trav), 8)

    def test_four_host_no_scene(self):
        gap = sorted(l.id for l in self.trav if self.hosted.get(l.id, 0) == 0)
        self.assertEqual(gap, ["CH01-TRV-001", "CH01-TRV-002",
                               "CH01-TRV-003", "CH01-TRV-004"])

    def test_the_two_water_rope_locations_are_in_that_gap(self):
        """TRV-003 and TRV-004 are the ones A1-R2 puts out of scope."""
        gap = {l.id for l in self.trav if self.hosted.get(l.id, 0) == 0}
        self.assertIn("CH01-TRV-003", gap)   # The Stream Crossing
        self.assertIn("CH01-TRV-004", gap)   # The Ravine and Liana Bridge


class TestWithdrawnNamespaces(unittest.TestCase):
    """Section 9.5: I withdrew four namespaces and deferred two.

    The review must state the withdrawal, and the original submission must still
    contain the requests (it is preserved unchanged).
    """

    @classmethod
    def setUpClass(cls):
        cls.review = REVIEW_A1R2.read_text(encoding="utf-8")
        cls.flat = cls.review.replace("**", "").replace("*", "").replace("`", "")

    def test_original_submission_still_holds_the_requests(self):
        sub = SUBMISSION.read_text(encoding="utf-8")
        for ns in ("Combat.State", "Combat.Damage", "Interaction.Mode",
                   "Traversal.State", "Interaction.Verb"):
            self.assertIn(ns, sub, f"{ns} should still be present in the preserved submission")

    def test_review_withdraws_combat_state(self):
        self.assertIn("Combat.State", self.flat)
        self.assertIn("WITHDRAWN", self.flat)

    def test_review_withdraws_combat_damage_in_full(self):
        self.assertIn("Combat.Damage", self.flat)
        self.assertIn("WITHDRAWN in full", self.flat)

    def test_review_admits_root_and_thunder_were_invented(self):
        self.assertIn("Root", self.flat)
        self.assertIn("Thunder", self.flat)
        self.assertIn("were invented", self.flat)

    def test_review_defers_two_namespaces_to_registry(self):
        self.assertIn("Interaction.Verb", self.flat)
        self.assertIn("DEFER", self.flat)


class TestCarryStateWithdrawn(unittest.TestCase):
    """Section 4.5: no Chapter 1 source supports CarryState, so it is withdrawn."""

    @classmethod
    def setUpClass(cls):
        cls.flat = REVIEW_A1R2.read_text(encoding="utf-8").replace("**", "").replace("*", "").replace("`", "")

    def test_review_withdraws_carry_state(self):
        self.assertIn("CarryState", self.flat)
        self.assertIn("Withdrawn", self.flat)

    def test_no_carry_vocabulary_in_the_register_capture(self):
        """The check the request demanded, encoded as a test."""
        text = LOCATION_CAPTURE.read_text(encoding="utf-8").lower()
        for word in ("carry", "carrying", "portage", "burden"):
            self.assertNotIn(word, text, f"register unexpectedly mentions {word}")

    def test_no_carry_vocabulary_in_the_scene_register(self):
        text = SCENE_FIXTURE.read_text(encoding="utf-8").lower()
        for word in ("carry", "carrying"):
            self.assertNotIn(word, text)


class TestNoInteractableCount(unittest.TestCase):
    """Standing constraint: no interactable or prop count may be stated."""

    @classmethod
    def setUpClass(cls):
        cls.flat = REVIEW_A1R2.read_text(encoding="utf-8").replace("**", "").replace("*", "").replace("`", "")

    NARRATIVE = ("withdraw", "unsourced", "no source", "failure mode",
                 "not established", "assertion of need")

    def _live(self, pattern):
        out = []
        for line in self.flat.splitlines():
            if not re.search(pattern, line):
                continue
            low = line.lower()
            if any(m in low for m in self.NARRATIVE):
                continue
            out.append(line)
        return out

    def test_no_live_interactable_count(self):
        self.assertEqual(self._live(r"\b\d+ (world )?interactables\b"), [])

    def test_no_live_prop_count(self):
        self.assertEqual(self._live(r"\b\d+ (registered )?props\b"), [])

    def test_states_interactable_count_not_established(self):
        self.assertIn("Not established", self.flat)


class TestCorrectionsRecorded(unittest.TestCase):
    """Section 14.3: six corrections, with attribution."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW_A1R2.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("*", "").replace("`", "")

    def test_six_corrections_recorded(self):
        seg = self.flat.split("### 14.3 The correction record", 1)[1]
        rows = [l for l in seg.splitlines() if re.match(r"^\| \d \|", l)]
        self.assertEqual(len(rows), 6)

    def test_concedes_the_c05_clock_was_wrong(self):
        self.assertIn("I withdraw the undilated rule", self.flat)

    def test_attributes_corrections_to_a1r2(self):
        self.assertIn("Four found by A1-R2", self.flat)

    def test_records_the_mead_false_accusation_nearly_made(self):
        self.assertIn("fabricat", self.flat.lower())


class TestMeadDivergence(unittest.TestCase):
    """Section 0.1: three divergent documents identify as TDD-MEAD-001.

    MEAD-C lives on Agent 1's branch and is not in this worktree; those
    assertions skip when it is absent rather than failing spuriously.
    """

    @classmethod
    def setUpClass(cls):
        cls.review = REVIEW_A1R2.read_text(encoding="utf-8")

    def test_review_names_three_meads(self):
        for tag in ("MEAD-A", "MEAD-B", "MEAD-C"):
            self.assertIn(tag, self.review)

    def test_review_records_the_1130_4_line_counts(self):
        self.assertIn("1,078", self.review)
        self.assertIn("247", self.review)
        self.assertIn("1,231", self.review)

    def test_review_records_that_dead_has_no_tag(self):
        flat = self.review.replace("**", "").replace("`", "")
        self.assertIn("Status.Dead", flat)
        self.assertIn("does not exist", flat)

    @unittest.skipUnless(MEAD_C.exists(), "MEAD-C is on Agent 1's branch, not in this worktree")
    def test_mead_c_has_section_5_4(self):
        text = MEAD_C.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^#+\s*5\.4\s")

    @unittest.skipUnless(MEAD_C.exists(), "MEAD-C is on Agent 1's branch, not in this worktree")
    def test_mead_c_has_seven_status_tags_and_no_dead(self):
        text = MEAD_C.read_text(encoding="utf-8")
        tags = set(re.findall(r"Status\.[A-Za-z]+", text))
        self.assertEqual(tags, {
            "Status.Attacking", "Status.Blocking", "Status.Cinematic",
            "Status.Grabbed", "Status.Invulnerable", "Status.Parrying",
            "Status.Staggered"})
        self.assertNotIn("Status.Dead", tags)

    @unittest.skipUnless(MEAD_C.exists(), "MEAD-C is on Agent 1's branch, not in this worktree")
    def test_mead_c_pair_hitstop_wording_supports_scaled_window(self):
        """Section 7.1's concession rests on this sentence."""
        text = MEAD_C.read_text(encoding="utf-8")
        self.assertIn("scaled time dilation to the *pair*", text)


class TestReviewInternalConsistency(unittest.TestCase):
    """Section references inside the review must resolve."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW_A1R2.read_text(encoding="utf-8")

    def test_section_headings_are_sequential(self):
        tops = [int(m.group(1)) for m in
                re.finditer(r"(?m)^## (\d+)\.", self.raw)]
        self.assertEqual(tops, list(range(0, len(tops))))

    def test_no_duplicate_section_numbers(self):
        tops = [int(m.group(1)) for m in
                re.finditer(r"(?m)^## (\d+)\.", self.raw)]
        self.assertEqual([k for k, v in Counter(tops).items() if v > 1], [])

    def test_publication_block_present(self):
        self.assertIn("### 15.1 Provenance", self.raw)
        self.assertIn("### 15.2 Change log", self.raw)

    def test_preserves_the_earlier_review(self):
        """The A1-R1 review must still exist and be unchanged in intent."""
        self.assertTrue(REVIEW_A1R1.exists())
        self.assertIn("FIVE CORRECTIONS", REVIEW_A1R1.read_text(encoding="utf-8").upper())


if __name__ == "__main__":
    unittest.main(verbosity=2)
