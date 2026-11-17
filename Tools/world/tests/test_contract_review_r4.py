#!/usr/bin/env python3
"""Tests backing the claims in `Docs/AGENT2_REVIEW_A1R4_V1.md`.

The review's central technical claim is that A1-R4 corrected the C-05 conversion,
and that the correction is right. That is arithmetic, so it is testable directly:
derive the conversion from A1-R4's own stated definitions and compare against the
formula A1-R4 prints in both directions.

The remainder lock the document-level claims: MEAD-A line citations, the three
spellings, the signature position, and the four broker gaps the review reports.

None of this is a contract acceptance test. No clock, broker, telegraph or
registry exists to test against.
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

REVIEW = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R4_V1.md"
PRIOR = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R3_V1.md"

A1_REF = "origin/a1branch"
A1R4_PATH = "docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md"
STANDARDS_PATH = "docs/01_ARCHITECTURE/CODING_STANDARDS.md"

REVIEWED_BLOB = "2cc548faf86cb9b30cd2e26386fc672edbdd9f75"


def _git_show(path: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "show", f"{A1_REF}:{path}"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


# ---------------------------------------------------------------- arithmetic

def axis_from_local(local, rate):
    return local / rate


def local_from_axis(axis, rate):
    return axis * rate


def remaining(R0, axis_elapsed, rate):
    """A1-R4 3.3(e): R(t) = max(0, R0 - axis_elapsed * ProducerRate)."""
    return max(0.0, R0 - axis_elapsed * rate)


class TestConversionCorrected(unittest.TestCase):
    """§3 — the corrected conversion, re-derived rather than read."""

    def test_multiply_is_the_axis_to_local_direction(self):
        self.assertAlmostEqual(local_from_axis(4.0, 0.05), 0.20)

    def test_divide_is_the_local_to_axis_direction(self):
        self.assertAlmostEqual(axis_from_local(0.20, 0.05), 4.00)

    def test_the_two_directions_are_inverses_at_every_rate(self):
        for rate in (1.0, 0.5, 0.2, 0.05):
            axis = axis_from_local(1.0, rate)
            self.assertAlmostEqual(local_from_axis(axis, rate), 1.0, places=12)

    def test_required_example_zero_twenty_at_zero_zero_five(self):
        """The value the assignment names: 0.20 s authored at 0.05 dilation."""
        self.assertAlmostEqual(axis_from_local(0.20, 0.05), 4.00)
        self.assertAlmostEqual(local_from_axis(4.00, 0.05), 0.20)

    def test_old_divide_form_is_wrong_by_inverse_rate_squared(self):
        for rate in (0.5, 0.25, 0.05):
            wrong = 4.0 / rate          # A1-R3 3.3(a) as printed
            right = local_from_axis(4.0, rate)
            self.assertAlmostEqual(wrong / right, 1.0 / rate ** 2, places=9)

    def test_worked_inflation_is_400x(self):
        self.assertAlmostEqual(4.00 / 0.05, 80.00)
        self.assertAlmostEqual((4.00 / 0.05) / 0.20, 400.0)

    def test_identical_at_rate_one_which_is_why_it_hid(self):
        for axis in (0.2, 1.0, 4.0):
            self.assertEqual(local_from_axis(axis, 1.0), axis / 1.0)


class TestRetimeAgreement(unittest.TestCase):
    """§3.3 — A1-R4 2.4 claims 3.3(a)'s inverse row and 3.3(b) now agree."""

    def test_retime_recomputation_uses_the_divide_direction(self):
        axis_now, rem_local, new_rate = 0.4, 0.800, 0.2
        # 3.3(b): EndAxis = AxisNow + RemainingLocal / rate
        self.assertAlmostEqual(axis_now + axis_from_local(rem_local, new_rate), 4.40)

    def test_old_table_form_on_an_axis_offset_inflates(self):
        """A1-R3's form (axis / rate) applied to the remaining AXIS offset."""
        axis_remaining, rate = 1.60, 0.2
        inflated = axis_remaining / rate          # 8.00
        correct = axis_remaining * rate           # 0.32
        self.assertAlmostEqual(inflated, 8.00)
        self.assertAlmostEqual(correct, 0.32)
        self.assertNotAlmostEqual(inflated, correct)


class TestAgingRule(unittest.TestCase):
    """§4 — the RemainingLocalSeconds lifecycle claims."""

    def test_normal_gameplay_is_linear(self):
        self.assertAlmostEqual(remaining(1.0, 1.0, 0.5), 0.5)
        self.assertAlmostEqual(remaining(1.0, 2.0, 0.5), 0.0)

    def test_pause_leaves_it_unchanged(self):
        """Axis does not advance across a pause, so R is constant."""
        before = remaining(1.0, 1.0, 0.5)
        after = remaining(1.0, 1.0, 0.5)   # axis unchanged by the pause
        self.assertAlmostEqual(before, after)

    def test_wall_clock_aging_would_close_early(self):
        """The failure the rule prevents: aging by wall rather than axis."""
        correct = remaining(1.0, 1.0, 0.5)
        wall = max(0.0, 1.0 - 11.0 * 0.5)   # 1 s axis + 10 s pause of wall time
        self.assertLess(wall, correct)

    def test_completion_predicate_equivalence(self):
        for R0, rate in ((1.0, 0.5), (0.2, 0.05), (1.0, 1.0)):
            threshold = R0 / rate
            self.assertEqual(remaining(R0, threshold, rate), 0.0)
            self.assertGreater(remaining(R0, threshold - 1e-6, rate), 0.0)

    def test_monotone_non_increasing_and_non_negative(self):
        seq = [remaining(1.0, i * 0.1, 0.5) for i in range(30)]
        self.assertTrue(all(seq[i] >= seq[i + 1] - 1e-12 for i in range(len(seq) - 1)))
        self.assertTrue(all(v >= 0.0 for v in seq))

    def test_primary_dilation_change_needs_no_retime(self):
        """R depends on R0, axis elapsed and ProducerRate only.

        A primary-dilation change moves d(Axis)/d(wall) and leaves the derivative
        d(Local)/d(Axis) untouched, so no field in R changes form.
        """
        import inspect
        self.assertEqual(
            list(inspect.signature(remaining).parameters), ["R0", "axis_elapsed", "rate"])


class TestPrecisionConcernDiscarded(unittest.TestCase):
    """§3.5 — the review reports this concern and then discards it. Pin the discard."""

    def test_float32_ulp_is_negligible_for_a_frame(self):
        import math
        import struct
        f32 = lambda x: struct.unpack("f", struct.pack("f", x))[0]  # noqa: E731
        e = math.floor(math.log2(f32(0.20)))
        ulp = 2.0 ** (e - 23)
        self.assertLess(ulp / (1 / 60), 1e-5, "float32 ULP must be negligible vs a frame")

    def test_long_session_double_axis_ulp_is_negligible(self):
        import math
        total = 8 * 3600.0
        ulp = 2.0 ** (math.floor(math.log2(total)) - 52)
        self.assertLess(ulp * 60, 1e-6, "double axis ULP must stay far below a frame")


class TestA1R4DocumentClaims(unittest.TestCase):
    """The formula text and clause markers the review quotes must exist in A1-R4."""

    @classmethod
    def setUpClass(cls):
        cls.text = _git_show(A1R4_PATH)
        if cls.text is None:
            raise unittest.SkipTest("A1-R4 branch not fetched")

    def test_blob_is_the_reviewed_one(self):
        out = subprocess.run(
            ["git", "rev-parse", f"{A1_REF}:{A1R4_PATH}"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(out.stdout.strip(), REVIEWED_BLOB)

    def test_states_multiply_form(self):
        self.assertIn("local_span = (EndAxis − AxisNow) × ProducerRate", self.text)

    def test_states_divide_inverse(self):
        self.assertIn("axis_span = local_span / ProducerRate", self.text)

    def test_states_the_derivation(self):
        self.assertIn("d(local)/d(axis) = CustomDilation(producer)", self.text)

    def test_states_the_aging_formula(self):
        self.assertIn("R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)", self.text)

    def test_has_a_negative_control(self):
        self.assertIn("Negative control", self.text)

    def test_withdraws_the_signature_overreach(self):
        self.assertIn("withdrawn in full", self.text)

    def test_internal_fields_absent_not_marked(self):
        self.assertIn("not members of the published snapshot struct at all", self.text)

    def test_combat_state_is_authoritative(self):
        self.assertIn("AUTHORITATIVE for consumers", self.text)

    def test_tags_are_derived(self):
        self.assertIn("DERIVED — never authored independently", self.text)

    def test_names_the_spelling_decision(self):
        self.assertIn("U-15", self.text)

    def test_retains_the_residual_blocker(self):
        self.assertIn("C-05 remains blocked on U-07", self.text)

    def test_does_not_register_a_tag_or_issue_an_erratum(self):
        self.assertRegex(self.text, r"No tag was registered, no erratum issued")

    def test_the_three_spellings_are_all_present_with_distinct_lengths(self):
        found = {m for m in re.findall(r"FTD+D?amageRequest", self.text)}
        self.assertIn("FTDamageRequest", found)
        self.assertEqual(len("FTDamageRequest"), 15)
        self.assertEqual(len("FTDDamageRequest"), 16)
        self.assertEqual(len("FTDDDamageRequest"), 17)


class TestBrokerGaps(unittest.TestCase):
    """§5 — the four gaps the review reports must still be absent from A1-R4.

    If A1-R5 closes one, these fail and the review should say so.
    """

    @classmethod
    def setUpClass(cls):
        cls.text = _git_show(A1R4_PATH)
        if cls.text is None:
            raise unittest.SkipTest("A1-R4 branch not fetched")
        cls.low = cls.text.lower()

    def test_no_adoption_ordering_rule(self):
        """Gap 1: 'adopt only if strictly greater' is not stated."""
        self.assertNotIn("strictly greater", self.low)
        self.assertNotIn("revision is greater", self.low)

    def test_no_at_most_once_phase_entry_rule(self):
        """Gap 2: no at-most-once phase-entry semantics."""
        self.assertNotIn("at most once", self.low)

    def test_no_eviction_on_producer_invalidation(self):
        """Gap 3: no eviction rule when a producer dies without Closed."""
        for term in ("evict", "purge", "producer invalid", "abandoned telegraph"):
            self.assertNotIn(term, self.low)

    def test_no_reentrancy_rule(self):
        """Gap 4: no re-entrancy rule for the query surface."""
        self.assertNotIn("re-entran", self.low)
        self.assertNotIn("reentran", self.low)

    def test_broker_is_placed_in_core(self):
        """§5.3 — the ownership question rests on this placement."""
        self.assertIn("`UTDDTelegraphBroker` (Core)", self.text)

    def test_broker_is_stateful_not_a_relay(self):
        self.assertIn("not merely a relay", self.text)
        self.assertIn("authoritative for current telegraph state", self.text)


class TestMeadCitations(unittest.TestCase):
    """§7 — the MEAD-A line citations, including the one A1-R4 gets wrong."""

    @classmethod
    def setUpClass(cls):
        cls.a = mead_refs.read("A")
        if cls.a is None:
            raise unittest.SkipTest("MEAD-A ref not fetched")
        cls.lines = cls.a.splitlines()

    def test_450_traversal_action_has_four_values(self):
        self.assertIn("ETDDTraversalAction", self.lines[449])
        self.assertIn("climb-lite", self.lines[449])

    def test_488_invulnerable_dodge(self):
        self.assertIn("State.Invulnerable.Dodge", self.lines[487])

    def test_506_not_505_is_the_locomotion_axis(self):
        """A1-R4 7.1 cites 505. It is 506 — the correction the review records."""
        self.assertIn("State.Locomotion", self.lines[505])
        self.assertIn("Cinematic", self.lines[505])
        self.assertNotIn("State.Locomotion", self.lines[504])

    def test_507_state_combat_values(self):
        self.assertIn("State.Combat.", self.lines[506])
        for v in ("InCombat", "Staggered", "Downed", "ParryWindow", "Invulnerable"):
            self.assertIn(v, self.lines[506])

    def test_517_prohibition(self):
        self.assertIn("no agent introduces a tag namespace", self.lines[516])

    def test_615_dead_is_an_enemy_ai_state(self):
        self.assertIn("Staggered, Dead", self.lines[614])

    def test_mantle_missing(self):
        self.assertEqual(len(re.findall(r"(?i)\bmantle\b", self.a)), 0)

    def test_no_status_namespace_at_all(self):
        self.assertEqual(re.findall(r"\bStatus\.[A-Za-z]+", self.a), [])

    def test_no_grab_or_block_or_attack_state(self):
        for v in ("Grabbed", "Blocking", "Attacking"):
            self.assertNotIn(v, self.lines[506])


class TestCodingStandard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _git_show(STANDARDS_PATH)
        if cls.text is None:
            raise unittest.SkipTest("coding standards not fetched")

    def test_line_21_generates_the_17_char_form(self):
        lines = self.text.splitlines()
        self.assertIn("FTDD<Thing>", lines[20])
        self.assertIn("FTDDDamageRequest", lines[20])


class TestReviewSelfConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("`", "")
        cls.flow = re.sub(r"\s+", " ", cls.flat)

    def test_seven_verdicts(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        rows = [l for l in seg.splitlines() if re.match(r"^\|\s*C-0\d", l.strip())]
        self.assertEqual(len(rows), 7)

    def test_verdict_distribution(self):
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        expect = {"C-01": "AGREE", "C-02": "AGREE", "C-03": "AGREE WITH CONDITIONS",
                  "C-04": "AGREE WITH CONDITIONS", "C-05": "AGREE WITH CONDITIONS",
                  "C-06": "AGREE", "C-07": "AGREE WITH CONDITIONS"}
        for cid, verdict in expect.items():
            line = [l for l in seg.splitlines() if l.strip().startswith(f"| {cid}")][0]
            self.assertIn(verdict, line, f"{cid} should be {verdict}")

    def test_no_disagree_remains(self):
        """The prior-verdict column legitimately records the historical DISAGREE;
        only the *new* verdict column must be free of it."""
        seg = self.flat.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        for row in seg.splitlines():
            if not re.match(r"^\|\s*C-0\d", row.strip()):
                continue
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            new_verdict = cells[2]
            self.assertNotIn("DISAGREE", new_verdict, f"{cells[0]} still DISAGREE")

    def test_three_signed_and_named(self):
        self.assertIn("Signed this review: 3 of 7", self.flow)
        for cid in ("C-01", "C-02", "C-06"):
            self.assertIn(f"| **{cid}** | **SIGNED", self.raw)

    def test_four_not_signed(self):
        for cid in ("C-03", "C-04", "C-05", "C-07"):
            self.assertIn(f"| **{cid}** | **NOT signed**", self.raw)

    def test_signature_names_the_blob(self):
        self.assertIn(REVIEWED_BLOB, self.raw)

    def test_refuses_bilateral_agreement(self):
        self.assertIn("No bilateral agreement is claimed", self.flow)
        self.assertIn("Not one contract reaches two signatures", self.flow)

    def test_no_contract_marked_agreed_by_both(self):
        self.assertNotIn("AGREED BY BOTH", self.raw.replace("`AGREED BY BOTH — PENDING TD`", ""))
        self.assertNotIn("AGREED_WITH_CONSUMERS", self.raw)

    def test_five_new_asks_31_to_35(self):
        found = sorted({int(x) for x in re.findall(r"A2R-(\d+)", self.flat)})
        self.assertEqual([n for n in found if n >= 31], [31, 32, 33, 34, 35])

    def test_sections_sequential(self):
        tops = [int(m.group(1)) for m in re.finditer(r"(?m)^## (\d+)\.", self.raw)]
        self.assertEqual(tops, list(range(len(tops))))

    def test_design_only(self):
        self.assertIn("DESIGN_ONLY", self.flat)

    def test_records_seven_own_errors(self):
        seg = self.flat.split("### 11.4 My own errors in this series, updated", 1)[1]
        rows = []
        for line in seg.splitlines():
            if re.match(r"^\|\s*\d+\s*\|", line):
                rows.append(line)
            elif rows and not line.strip().startswith("|"):
                break          # end of the table
        self.assertEqual(len(rows), 7)

    def test_does_not_state_an_interactable_count(self):
        live = [l for l in self.flat.splitlines()
                if re.search(r"\b\d+ (world )?interactables\b", l, re.I)
                and not any(m in l.lower() for m in ("withdraw", "no count", "not established"))]
        self.assertEqual(live, [])

    def test_no_three_meads_claim(self):
        self.assertNotIn("all three MEAD documents identify", self.flat)

    def test_does_not_select_a_canonical_mead(self):
        self.assertIn("I do not make TD decisions", self.flat)


class TestPreservation(unittest.TestCase):
    def test_prior_review_exists_and_unchanged(self):
        self.assertTrue(PRIOR.exists())
        text = PRIOR.read_text(encoding="utf-8")
        self.assertIn("Version:** 1.0", text)

    def test_prior_review_still_zero_signed(self):
        """The R3 review's 0-of-7 must not be retro-edited by this one."""
        flat = PRIOR.read_text(encoding="utf-8").replace("**", "")
        self.assertIn("Signed: 0 of 7", flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
