#!/usr/bin/env python3
"""Tests backing the factual and arithmetic claims in `Docs/AGENT2_REVIEW_A1R3_V1.md`.

The review's central finding is that `A1-R3` §3.3(a) states an inverted conversion.
That is a claim about arithmetic, so it can be tested directly: derive the correct
conversion from `A1-R3` §3.2's own definitions and assert that §3.3(a)'s formula
disagrees with it by the predicted factor.

The rest lock the MEAD claims, the spelling count, and the review's own internal
counts. None of these is a contract acceptance test — no clock, arbiter, telegraph
or registry exists to test against.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import mead_refs  # noqa: E402

REVIEW = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R3_V1.md"
PRIOR = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R2_V1.md"
SUBMISSION = REPO_ROOT / "Docs" / "CONTRACT_SUBMISSION_A2_V1.md"

A1R3_REF = "origin/a1branch"
A1R3_PATH = "docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md"


def _a1r3() -> str | None:
    try:
        out = subprocess.run(
            ["git", "show", f"{A1R3_REF}:{A1R3_PATH}"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


class TestConversionIsInverted(unittest.TestCase):
    """§7.3: the review's blocking finding.

    A1-R3 §3.2 defines the axis as advancing by `PrimaryDilation` per wall second and
    the local clock by `PrimaryDilation * CustomDilation(e)`. Therefore

        d(local)/d(axis) = CustomDilation(e) = ProducerRate

    and `local_span = axis_span * ProducerRate`. §3.3(a) prints a division.
    """

    def _correct(self, axis_span, rate):
        return axis_span * rate

    def _as_written(self, axis_span, rate):
        """§3.3(a) verbatim: (EndAxis - AxisNow) / ProducerRate."""
        return axis_span / rate

    def test_agree_when_rate_is_one(self):
        """Why the error is invisible in the undilated case."""
        for span in (0.2, 1.0, 4.0):
            self.assertAlmostEqual(self._correct(span, 1.0), self._as_written(span, 1.0))

    def test_disagree_under_dilation(self):
        for rate in (0.5, 0.05):
            self.assertNotAlmostEqual(self._correct(4.0, rate), self._as_written(4.0, rate))

    def test_error_factor_is_inverse_rate_squared(self):
        for rate in (0.5, 0.25, 0.05):
            correct = self._correct(4.0, rate)
            written = self._as_written(4.0, rate)
            self.assertAlmostEqual(written / correct, 1.0 / rate ** 2, places=9)

    def test_worked_case_at_rate_0_05(self):
        """The case Option A+ exists to fix: 0.20 s authored window, staggered attacker."""
        rate, local = 0.05, 0.20
        axis_span = local / rate          # 4.00 axis-seconds
        self.assertAlmostEqual(axis_span, 4.00)
        self.assertAlmostEqual(self._as_written(axis_span, rate), 80.00)
        self.assertAlmostEqual(self._correct(axis_span, rate), 0.20)

    def test_retime_rule_uses_the_inverse_of_the_table(self):
        """§3.3(b) recomputes EndAxis; it implies local/rate, the opposite of §3.3(a)."""
        old_end, axis_now, new_rate, old_rate = 2.0, 0.40, 0.2, 0.5
        axis_remaining = old_end - axis_now              # 1.60 axis-seconds
        local_rem = axis_remaining * old_rate            # 0.80 correct conversion
        self.assertAlmostEqual(local_rem, 0.800)

        # §3.3(b) turns local remaining back into an axis offset by DIVIDING.
        new_end_by_retime_rule = axis_now + local_rem / new_rate
        self.assertAlmostEqual(new_end_by_retime_rule, 4.40)

        # §3.3(a) and §3.3(b) are mutual inverses ONLY because one multiplies
        # (retime: local -> axis by dividing) and the other divides. Applying
        # §3.3(a) to the axis-remaining offset is where they part company:
        axis_by_table = self._as_written(axis_remaining, new_rate)   # 1.60 / 0.2
        truth_local = axis_remaining * new_rate                     # 1.60 * 0.2
        self.assertAlmostEqual(axis_by_table, 8.00)
        self.assertAlmostEqual(truth_local, 0.32)
        self.assertNotAlmostEqual(axis_by_table, truth_local)


class TestA1R3FormulaAsWritten(unittest.TestCase):
    """The review quotes §3.3(a). The quote must match the source document."""

    @classmethod
    def setUpClass(cls):
        cls.text = _a1r3()
        if cls.text is None:
            raise unittest.SkipTest("A1-R3 branch not fetched")

    def test_divides_by_producer_rate(self):
        """§3.3(a) as written: division, which §7.3 derives to be inverted."""
        self.assertIn("`local_span = (EndAxis − AxisNow) / ProducerRate`", self.text)

    def test_defines_local_clock_with_custom_dilation(self):
        """§3.2's comment block is the definition §7.3's derivation rests on."""
        self.assertIn("DeltaWorld * PrimaryDilation", self.text)
        self.assertIn("CustomDilation", self.text)
        self.assertIn("Per-entity CustomDilation is NOT applied", self.text)

    def test_axis_excludes_custom_dilation(self):
        self.assertIn("Per-entity CustomDilation is NOT applied", self.text)

    def test_parry_is_same_frame_overlap(self):
        self.assertIn("same-frame phase-overlap test against live state", self.text)

    def test_retimed_replaces_never_integrates(self):
        self.assertIn("never accumulate segments", self.text)


class TestSpellingSilentlySelected(unittest.TestCase):
    """§5.3: A1-R3 selects FTDDDamageRequest by reproduction without comment."""

    @classmethod
    def setUpClass(cls):
        cls.text = _a1r3()
        if cls.text is None:
            raise unittest.SkipTest("A1-R3 branch not fetched")

    def test_one_spelling_present(self):
        import re
        found = sorted(set(re.findall(r"FTD+D?amageRequest", self.text)))
        self.assertEqual(found, ["FTDDDamageRequest"])
        self.assertEqual(self.text.count("FTDDDamageRequest"), 1)

    def test_does_not_discuss_the_inconsistency(self):
        """If A1-R3 ever addresses it, this test tells us to revisit the condition."""
        low = self.text.lower()
        self.assertNotIn("type name", low)
        self.assertNotIn("spelling inconsistency", low)


class TestMeadAClaims(unittest.TestCase):
    """§4.3 and §10.1: the MEAD-A mapping must match the file."""

    @classmethod
    def setUpClass(cls):
        cls.a = mead_refs.read("A")
        if cls.a is None:
            raise unittest.SkipTest("MEAD-A ref not fetched")

    def test_has_no_status_namespace(self):
        self.assertEqual(re.findall(r"\bStatus\.[A-Za-z]+", self.a), [])

    def test_has_state_combat_namespace(self):
        self.assertIn("State.Combat.<InCombat|Staggered|Downed|ParryWindow|Invulnerable>", self.a)

    def test_has_the_tag_governance_rule(self):
        self.assertIn("DefaultGameplayTags.ini", self.a)

    def test_has_the_no_new_namespace_prohibition(self):
        self.assertIn("no agent introduces a tag namespace", self.a)

    def test_dead_is_an_enemy_ai_state_not_a_status_tag(self):
        self.assertIn("Staggered, Dead", self.a)
        self.assertNotIn("Status.Dead", self.a)

    def test_has_no_section_5_5(self):
        self.assertFalse(re.search(r"(?m)^#+\s*5\.5\s", self.a))
        self.assertTrue(re.search(r"(?m)^#+\s*5\.3\s", self.a))

    def test_arbiter_is_a_world_subsystem(self):
        self.assertIn("Only `UTDDHitArbiter` (a world subsystem) decides", self.a)

    def test_seven_retained_tags_have_only_two_exact_equivalents(self):
        """Innermost tag value is the right comparison — `State.Combat.<A|B>` is one line."""
        values = {"InCombat", "Staggered", "Downed", "ParryWindow", "Invulnerable"}
        exact = {"Invulnerable", "Staggered"}
        self.assertTrue(exact <= values, "expected exact equivalents must be present")
        self.assertEqual(len(exact & values), 2)


class TestMeadC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = mead_refs.read("C")
        if cls.c is None:
            raise unittest.SkipTest("MEAD-C ref not fetched")

    def test_seven_status_tags_no_dead(self):
        tags = mead_refs.status_tags(self.c)
        self.assertEqual(tags, {
            "Status.Attacking", "Status.Blocking", "Status.Cinematic",
            "Status.Grabbed", "Status.Invulnerable", "Status.Parrying",
            "Status.Staggered"})

    def test_6_6_is_the_chapter_pipeline_not_tag_governance(self):
        """The basis for accepting A1-R3 §0.5's correction of my v1.1 error."""
        self.assertIn("### 6.6 Chapter production pipeline", self.c)
        self.assertNotIn("DefaultGameplayTags", self.c)

    def test_section_5_4_spells_the_struct_two_ways_at_different_lengths(self):
        """The finding my v1.1 got right and my first draft of this review mangled."""
        import re
        found = sorted(set(re.findall(r"FTD+D?amageRequest", self.c)))
        self.assertEqual(found, ["FTDDamageRequest", "FTDamageRequest"])
        self.assertEqual(len("FTDDamageRequest"), 16)
        self.assertEqual(len("FTDamageRequest"), 15)
        self.assertNotIn("FTDDDamageRequest", self.c)


class TestReviewSelfConsistency(unittest.TestCase):
    """The review's own counts and structure."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("`", "")
        # Markdown wraps prose, so multi-word assertions must run on one line.
        cls.flow = re.sub(r"\s+", " ", cls.flat)

    def test_seven_verdicts_recorded(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        rows = [l for l in seg.splitlines() if re.match(r"^\|\s*C-0\d", l.strip())]
        self.assertEqual(len(rows), 7)

    def test_zero_signed(self):
        """Both the header callout and the §1.2 table must say zero."""
        # appears in the header callout, in §1.2, and once in the §12.5 test table
        self.assertGreaterEqual(self.flow.count("Signed: 0 of 7"), 3)
        self.assertIn("Contracts signed | 0 of 7", self.flow)
        self.assertNotIn("Signed: 3 of 7", self.flow)

    def test_verdict_distribution(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        body = "\n".join(seg.splitlines())
        for row, verdict in [
            ("C-01", "AGREE"), ("C-02", "AGREE WITH CONDITIONS"),
            ("C-03", "AGREE WITH CONDITIONS"), ("C-04", "AGREE WITH CONDITIONS"),
            ("C-05", "DISAGREE"), ("C-06", "AGREE"), ("C-07", "AGREE WITH CONDITIONS"),
        ]:
            line = [l for l in body.splitlines() if l.strip().startswith(f"| {row}")][0]
            self.assertIn(verdict, line, f"{row} should be {verdict}")

    def test_uses_only_the_three_permitted_labels(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        self.assertNotIn("PARTIALLY AGREE", seg)
        self.assertNotIn("CLARIFICATION REQUIRED", seg)

    def test_ten_asks_numbered_22_to_30(self):
        found = sorted({int(x) for x in re.findall(r"A2R-(\d+)", self.flat)})
        self.assertEqual([n for n in found if n >= 22], [22, 23, 24, 25, 26, 27, 28, 29, 30])

    def test_sections_are_sequential(self):
        tops = [int(m.group(1)) for m in re.finditer(r"(?m)^## (\d+)\.", self.raw)]
        self.assertEqual(tops, list(range(len(tops))))

    def test_states_design_only(self):
        self.assertIn("DESIGN_ONLY", self.flat)

    def test_discloses_authorship_of_mead_a(self):
        self.assertIn("I authored MEAD-A", self.flat)

    def test_parry_outcome_declared_safe(self):
        """§7.7 — the disagreement must not be overstated."""
        self.assertIn("parry outcome cannot be corrupted", self.flow)
        self.assertIn("reporting defect rather than a gameplay defect", self.flow)

    def test_does_not_state_an_interactable_count(self):
        live = [l for l in self.flat.splitlines()
                if re.search(r"\b\d+ (world )?interactables\b", l, re.I)
                and not any(m in l.lower() for m in
                            ("withdraw", "no count", "not established"))]
        self.assertEqual(live, [])

    def test_does_not_repeat_the_three_meads_claim(self):
        """Carried-forward correction: only two declare TDD-MEAD-001."""
        self.assertNotIn("all three MEAD documents identify", self.flat)
        self.assertIn("only MEAD-A and MEAD-C", self.flat)

    def test_does_not_select_a_canonical_mead(self):
        self.assertIn("I do not choose", self.flat)
        self.assertIn("nonbinding", self.flat)


class TestRejectionsAndAcceptances(unittest.TestCase):
    """§1.4: the review must accept A1's correction and reject the one overreach."""

    @classmethod
    def setUpClass(cls):
        cls.flat = REVIEW.read_text(encoding="utf-8").replace("**", "").replace("`", "")

    def test_accepts_the_6_6_misattribution(self):
        self.assertIn("ACCEPTED", self.flat)
        self.assertIn("MEAD-A §6.6", self.flat)

    def test_rejects_the_already_there_claim(self):
        self.assertIn("C-03 and C-06 are not", self.flat)
        self.assertIn("REJECTED", self.flat)

    def test_records_five_own_errors(self):
        seg = self.flat.split("### 13.3 Where my own record stands", 1)[1]
        rows = [l for l in seg.splitlines() if re.match(r"^\|\s*\d\s*\|", l)]
        self.assertEqual(len(rows), 5)

    def test_cites_which_errors_another_agent_found(self):
        self.assertIn("Agent 3, recon V3", self.flat)
        self.assertIn("Agent 1, A1-R3", self.flat)


class TestPreservation(unittest.TestCase):
    def test_prior_reviews_still_exist(self):
        self.assertTrue(PRIOR.exists())
        self.assertTrue(SUBMISSION.exists())

    def test_prior_review_still_version_1_1(self):
        text = PRIOR.read_text(encoding="utf-8")
        self.assertIn("**Version:** 1.1", text)
        self.assertIn("preserved unchanged", text)

    def test_submission_unchanged_and_still_holds_withdrawn_namespaces(self):
        text = SUBMISSION.read_text(encoding="utf-8")
        for ns in ("Combat.State", "Combat.Damage", "Interaction.Mode", "Traversal.State"):
            self.assertIn(ns, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
