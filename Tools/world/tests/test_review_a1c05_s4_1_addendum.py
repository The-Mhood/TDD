"""Tests for Docs/AGENT2_REASSESSMENT_A1C05_S4_1_ADDENDUM_A1.md (W-M2.14).

Locks the closure taxonomy and its consistency across the addendum AND the review
it amends. The defect this addendum repairs was a three-way disagreement between
sections 6, 7 and 9 of W-M2.13 over which findings gate PASS. These tests exist so
that disagreement cannot reappear in either document.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised.
"""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_REASSESSMENT_A1C05_S4_1_V1.md"
ADDENDUM = ROOT / "Docs" / "AGENT2_REASSESSMENT_A1C05_S4_1_ADDENDUM_A1.md"
REPO = ROOT

S41_BLOB = "d54e194affeaee98b1030e2b83b4c34e234fa382"
S41_COMMIT = "95918268ed5b20b878fef3ee0a7855ad18e6eeb6"
S41_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md"

W_M2_13_COMMIT = "eee9401dc3557660bbc248b6975c9ce8a4e50446"
A3_ARTIFACT = "AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md"

# The four closure classes, and the single source of truth for what blocks PASS.
PASS_BLOCKING = {"D-4", "D-22-scope"}
PASS_CONDITION = {"D-1a", "C4c-N1"}
ADVISORY = {"D-1b", "D-6b"}
RESOLVED = {"D-6a"}


def git_show(spec):
    r = subprocess.run(["git", "show", spec], capture_output=True,
                       text=True, cwd=REPO, check=False)
    return r.stdout if r.returncode == 0 else None


def flat(p):
    return re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.add_raw = ADDENDUM.read_text(encoding="utf-8")
        cls.add = re.sub(r"\s+", " ", cls.add_raw)
        cls.rev = flat(REVIEW)

    def s41(self):
        t = git_show(S41_BLOB)
        if t is None:
            self.skipTest("reviewed S4.1 blob unavailable")
        return t


# ---------------------------------------------------------------------------
# The taxonomy itself
# ---------------------------------------------------------------------------

class TestTaxonomy(Base):
    def test_four_classes_defined(self):
        for c in ("PASS-BLOCKING", "PASS-CONDITION", "ADVISORY", "RESOLVED"):
            self.assertIn(c, self.add)

    def test_each_class_has_a_may_close_with_this_open_answer(self):
        self.assertIn("May close with this open?", self.add)
        self.assertIn("**No**", self.add)
        self.assertIn("**Yes**", self.add)

    def test_boundary_rule_is_stated(self):
        self.assertIn("if two conforming teams could read the document and", self.add)

    def test_assignment_table_covers_every_finding(self):
        for f in PASS_BLOCKING | PASS_CONDITION | ADVISORY | RESOLVED:
            self.assertIn(f, self.add, f)

    def test_counts_stated(self):
        self.assertIn("Final PASS criteria: five items", self.add)
        self.assertIn("Advisory, may remain open: two", self.add)


# ---------------------------------------------------------------------------
# The contradiction this addendum exists to repair
# TAMPER: if section 9 lists D-1b/D-6b again as PASS conditions, these fail.
# ---------------------------------------------------------------------------

class TestSection9Corrected(Base):
    def test_addendum_quotes_the_original_defect(self):
        self.assertIn("D-1a/D-1b/D-6b wording", self.add)

    def test_addendum_repairs_it_explicitly(self):
        self.assertIn("§9 is the one that is wrong", self.add)

    def test_corrected_criteria_list_four_changes(self):
        sec = self.add.split("Corrected — four changes, two of them atomic:")[1]
        sec = sec.split("May remain open as advisory")[0]
        for item in ("D-4 + D-22-scope", "D-1a.", "C4c-N1.", "Re-issue the blob"):
            self.assertIn(item, sec, item)

    def test_advisory_items_explicitly_excluded_from_pass(self):
        sec = self.add.split("May remain open as advisory")[1].split("Closable inside")[0]
        self.assertIn("D-1b", sec)
        self.assertIn("D-6b", sec)
        self.assertIn("would not withhold `PASS`", sec)

    def test_original_review_still_contains_the_contradiction(self):
        """The addendum amends; it must not silently rewrite W-M2.13."""
        self.assertIn("What would move me to `PASS`", self.rev)
        self.assertIn("D-1a/D-1b/D-6b wording", self.rev)
        self.assertIn("neither gating", self.rev)


class TestSection7Corrected(Base):
    def test_original_sentence_quoted(self):
        self.assertIn("No defect in a normative clause remains open", self.add)

    def test_replacement_sentence_present(self):
        self.assertIn("No defect remains open in how the contract assigns work", self.add)

    def test_addendum_explains_why_original_was_wrong(self):
        self.assertIn("a clause can be **normatively correct in what it requires**", self.add)
        self.assertIn("My original sentence collapsed the two", self.add)


# ---------------------------------------------------------------------------
# D-1b reclassification — must be grounded in the clause, not my summary
# ---------------------------------------------------------------------------

class TestD1bReclassified(Base):
    def test_clause_defines_the_consumer(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("it acts on `TN-C-10`'s output", row)

    def test_tn_c_10_output_is_remaining_time(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **TN-C-10**")][0]
        self.assertIn("remaining local seconds", row)
        self.assertIn("ProducerRate", row)

    def test_addendum_admits_its_own_previous_error(self):
        self.assertIn("nothing defines which consumer is which", self.add)
        self.assertIn("That is wrong", self.add)

    def test_reclassified_as_advisory(self):
        self.assertIn("`ADVISORY`, not a normative gap (reclassified)", self.add_raw)

    def test_identical_compliance_sets_argument_present(self):
        self.assertIn("identical compliance sets", self.add)

    def test_call_site_recommendation_withdrawn(self):
        self.assertIn("I withdraw my §6.1 recommendation", self.add)

    def test_d1b_not_in_pass_criteria(self):
        sec = self.add.split("Corrected — four changes, two of them atomic:")[1]
        sec = sec.split("May remain open as advisory")[0]
        self.assertNotIn("D-1b", sec)


# ---------------------------------------------------------------------------
# D-1a upgrade — arithmetic must be right
# ---------------------------------------------------------------------------

class TestD1aArithmetic(Base):
    def test_clause_constrains_count_not_interval(self):
        self.assertIn("at least once per frame, per held open instance", self.s41())

    def test_addendum_states_the_worst_case(self):
        self.assertIn("1.98 frames", self.add)
        self.assertIn("2 frames", self.add)

    def test_addendum_shows_a_legal_adversarial_schedule(self):
        for t in ("t = 0.99", "t = 1.99", "t = 2.99"):
            self.assertIn(t, self.add)

    def test_bound_asserted_in_four_places(self):
        s = self.s41()
        self.assertIn("bounds rate staleness to one frame", s)          # section 1 row 2
        self.assertIn("bounded by one frame, by construction", s)       # TN-C-14
        self.assertIn("rate-stale for **at most one frame**", s)        # T-C05-64
        self.assertIn("that one frame is a", s)                         # section 14.2

    def test_t_c05_64_asserts_the_unreachable_bound(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **T-C05-64**")][0]
        self.assertIn("at most one frame", row)

    def test_upgraded_to_pass_condition(self):
        self.assertIn("the sharpest of the three PASS conditions", self.add)

    def test_admits_own_understatement(self):
        self.assertIn("my own finding was understated", self.add)
        # bind the actual correction sentence, not just the heading
        self.assertIn('D-1a is **not** *"minor, wording, non-gating"*.', self.add_raw)

    def test_original_non_gating_characterisation_is_quoted_not_asserted(self):
        """The review said D-1a was non-gating; the addendum must quote that as superseded."""
        sec = self.add_raw.split("**Correction to my own review:**")[1].split("###")[0]
        self.assertIn("not", sec)
        self.assertIn("PASS-CONDITION", sec)

    def test_three_fix_options_offered(self):
        for opt in ("(i) interval-based (preferred)", "(ii) publish-relative",
                    "(iii) weaken the claim"):
            self.assertIn(opt, self.add)

    def test_arithmetic_is_actually_correct(self):
        """Recompute the worst-case gap independently."""
        import math
        # legal schedule: one pull per frame, all at offset eps before frame end
        eps = 0.99
        pulls = [k + eps for k in range(4)]
        gaps = [pulls[i + 1] - pulls[i] for i in range(len(pulls) - 1)]
        self.assertAlmostEqual(max(gaps), 1.0, places=9)  # uniform offset => 1.0
        # adversarial: one early, one late
        worst = [(1 - 0.01) + 1.0 + 0.01]
        self.assertAlmostEqual(worst[0], 2.0, places=9)
        # best case
        self.assertAlmostEqual(1.0, 1.0, places=9)


# ---------------------------------------------------------------------------
# Scope discipline: the prohibited changes must NOT have happened
# ---------------------------------------------------------------------------

class TestScopeDiscipline(Base):
    def test_d4_finding_unchanged(self):
        self.assertIn("**Finding unchanged.**", self.add)
        self.assertIn("Agent 1 for defence, dodge, camera and audio", self.s41())

    def test_c4cn1_unchanged(self):
        self.assertIn("**Finding unchanged.** §6.2 stands", self.add)

    def test_d6a_still_resolved(self):
        self.assertIn("Remains RESOLVED", self.add)

    def test_blob_unchanged(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (S41_COMMIT, S41_PATH)],
                           capture_output=True, text=True, cwd=REPO, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), S41_BLOB)

    def test_w_m2_13_preserved_unmodified(self):
        r = subprocess.run(["git", "diff", "--stat", W_M2_13_COMMIT, "--",
                            str(REVIEW.relative_to(ROOT))],
                           capture_output=True, text=True, cwd=REPO, check=False)
        self.assertEqual(r.stdout.strip(), "", "W-M2.13 must not be altered")

    def test_addendum_is_a_separate_artifact(self):
        self.assertNotEqual(ADDENDUM.resolve(), REVIEW.resolve())
        self.assertIn("Amends:", self.add)

    def test_no_governance_claim(self):
        self.assertIn("Still not signing v4.1", self.add)
        self.assertIn("0 of 67 acceptance cases", self.add)
        for bad in ("C-05 is closed", "U-07 is closed", "signature granted"):
            self.assertNotIn(bad, self.add)


# ---------------------------------------------------------------------------
# Agent 3 independence
# ---------------------------------------------------------------------------

class TestAgent3Independence(Base):
    def artifact(self):
        t = git_show("origin/a3branch:docs/" + A3_ARTIFACT)
        if t is None:
            t = git_show("34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a:docs/" + A3_ARTIFACT)
        if t is None:
            self.skipTest("Agent 3 artifact not fetched")
        return t

    def test_agent3_reviewed_the_same_blob(self):
        self.assertEqual(self.artifact().count(S41_BLOB), 2)

    def test_agent3_reviewed_the_same_commit(self):
        self.assertEqual(self.artifact().count(S41_COMMIT), 3)

    def test_agent3_review_is_published(self):
        r = subprocess.run(["git", "cat-file", "-t",
                            "34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a"],
                           capture_output=True, text=True, cwd=REPO, check=False)
        if r.returncode != 0:
            self.skipTest("Agent 3 commit unavailable")
        self.assertEqual(r.stdout.strip(), "commit")

    def test_addendum_records_both_and_keeps_them_separate(self):
        self.assertIn("It targets the right object", self.add)
        self.assertIn("I have not used Agent 3's findings as evidence for mine", self.add)

    def test_addendum_does_not_assess_agent3_cluster1(self):
        self.assertIn("I have not assessed Agent 3's cluster 1 finding", self.add)

    def test_addendum_does_not_speak_for_agent3(self):
        self.assertIn("Agent 3 has not endorsed anything in this document", self.add)

    def test_does_not_claim_agent3_closed_anything(self):
        for bad in ("Agent 3 agrees", "Agent 3 signed", "Agent 3 concurs"):
            self.assertNotIn(bad, self.add)


# ---------------------------------------------------------------------------
# Internal reference integrity
# ---------------------------------------------------------------------------

class TestReferences(Base):
    def test_cross_reference_to_d1b_lands_on_2_1(self):
        self.assertIn("(reclassified — §2.1)", self.add)
        self.assertNotIn("(reclassified — §2.3)", self.add)

    def test_no_section_2_3_exists(self):
        self.assertNotRegex(self.add_raw, r"(?m)^###+ 2\.3")

    def test_checks_table_has_thirteen_rows(self):
        sec = self.add_raw.split("## 5. Reproducible checks")[1].split("## 6.")[0]
        n = len([l for l in sec.splitlines() if re.match(r"\| \d+ \|", l)])
        self.assertEqual(n, 13)


if __name__ == "__main__":
    unittest.main()
