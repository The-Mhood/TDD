"""Tests for Docs/AGENT2_REVIEW_A1C05_S2_V1.md (W-M2.10).

Locks the review's claims about A1-C05-S2 v2.0 at the exact reviewed blob.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised: no telegraph,
producer, consumer, directory or engine exists here. All acceptance cases in the reviewed
document are PROPOSED / NOT RUN and none is run by this file.

TestBlockerPersistence asserts phrases are ABSENT or present in specific clauses. If a
successor closes a finding, those tests FAIL. That is intended: the review's claims are
about blob bf6c8fb3, not about whatever the branch later becomes.
"""

import re
import subprocess
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[3] / "Docs" / "AGENT2_REVIEW_A1C05_S2_V1.md"
REPO = REVIEW.parents[1]

S2_BLOB = "bf6c8fb3ddf3152d1627d3b6471278f57fc82541"
S2_COMMIT = "e5ddad6965e06b179061d8cebb6ffecf59829224"
S2_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V2.md"

TIP_BLOB = "30a98b88f7d1f4e30cd50068f3cfe207522c7d1a"
A1_HEAD = "5103a451d452d7c7ef85863aa889421861b9603d"

A2_C05_COMMIT = "3ac438b32fcd73ceb22dcd81385356f7b8b39644"
A2_C05_PATH = "Docs/CONTRACT_SUBMISSION_A2_V1.md"

S1_COMMIT = "2bb729f2cbd525e3cd7f5f5d46b3b9cc72c803d0"
S1_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V1.md"

A1R4_COMMIT = "142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6"
A1R4_PATH = "docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md"


def git_show(spec):
    try:
        r = subprocess.run(["git", "show", spec], capture_output=True,
                           text=True, cwd=REPO, check=False)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def git_run(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True,
                       cwd=REPO, check=False)
    return r.stdout if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def s2(self):
        t = git_show(S2_BLOB)
        if t is None:
            self.skipTest("reviewed S2 blob not available")
        return t

    def s2flat(self):
        return re.sub(r"\s+", " ", self.s2())

    def a2c05(self):
        t = git_show(f"{A2_C05_COMMIT}:{A2_C05_PATH}")
        if t is None:
            self.skipTest("A2-C05 submission not available")
        return t


class TestProvenance(Base):
    """§0: the exact blob, and proof the excluded correction is provenance-only."""

    def test_reviewed_blob_named(self):
        self.assertIn(S2_BLOB, self.raw)

    def test_publishing_commit_named(self):
        self.assertIn(S2_COMMIT, self.raw)

    def test_blob_resolves_at_publishing_commit(self):
        actual = git_run("rev-parse", f"{S2_COMMIT}:{S2_PATH}")
        if actual is None:
            self.skipTest("cannot resolve")
        self.assertEqual(actual.strip(), S2_BLOB)

    def test_tip_diff_is_provenance_only(self):
        """§0.2's load-bearing claim: only 6 insertions / 3 deletions."""
        d = git_run("diff", "--numstat", S2_BLOB, TIP_BLOB)
        if d is None:
            self.skipTest("cannot diff")
        adds, dels = d.split()[:2]
        self.assertEqual((int(adds), int(dels)), (6, 3),
                         "tip diff changed size; review §0.2 must be revisited")

    def test_tip_diff_hunks_are_s0_and_s16(self):
        """Every changed line must sit in the provenance/publication rows."""
        d = git_run("diff", S2_BLOB, TIP_BLOB)
        if d is None:
            self.skipTest("cannot diff")
        changed = [l for l in d.splitlines()
                   if (l.startswith("+") or l.startswith("-"))
                   and not l.startswith(("+++", "---"))]
        # 9 changed lines, all provenance/publication material
        self.assertEqual(len(changed), 9, f"unexpected changed-line count: {changed}")
        for l in changed:
            body = l[1:].strip()
            ok = ("MEAD" in body or "PUB_" in body or "Publishing commit" in body
                  or "Blob at that commit" in body or "Provenance correction" in body
                  or "Superseded" in body)
            self.assertTrue(ok, f"a non-provenance line changed: {body[:100]}")

    def test_review_states_it_did_not_review_tip(self):
        self.assertIn("I did not review the branch tip", self.flat)


class TestFiveVerdicts(Base):
    """§1: two DISAGREE on Q2/Q4, three AWC on Q1/Q3/Q5."""

    HEADINGS = [
        "## 2. Q1", "## 3. Q2", "## 4. Q3", "## 5. Q4", "## 6. Q5",
    ]

    def test_all_five_sections_present(self):
        for h in self.HEADINGS:
            self.assertIn(h, self.raw, f"missing {h}")

    def test_verdict_tokens_exact(self):
        for v in ("### Verdict: AGREE WITH CONDITIONS",
                  "### Verdict: DISAGREE"):
            self.assertIn(v, self.raw)

    def test_verdict_distribution_matches_table(self):
        """§1's table must agree with each section's own verdict line."""
        qs = re.findall(r"### Verdict: (AGREE WITH CONDITIONS|DISAGREE|AGREE)\n", self.raw)
        self.assertEqual(len(qs), 5, f"expected 5 verdict lines, got {qs}")
        self.assertEqual(qs.count("DISAGREE"), 2, f"distribution changed: {qs}")
        self.assertEqual(qs.count("AGREE WITH CONDITIONS"), 3, f"distribution changed: {qs}")

    def test_no_bare_agree(self):
        self.assertNotIn("### Verdict: AGREE\n", self.raw)

    def test_nine_corrections_claimed_and_counted(self):
        self.assertIn("9 narrowly necessary corrections", self.flat)
        self.assertIn("0 architectural changes", self.flat)
        self.assertIn("0 reopened findings", self.flat)


class TestInv1Contradiction(Base):
    """§3: INV-1 includes an aging field -> false under passage of time."""

    def test_inv1_is_in_s2_and_lists_the_aging_field(self):
        """The whole finding rests on INV-1 naming RemainingLocalSeconds."""
        t = self.s2flat()
        self.assertIn("C05-2.6 INV-1 (new invariant)", t)
        self.assertIn("identical in every pull-visible field", t)
        # locate the INV-1 sentence and check the aging field is inside it
        start = t.index("C05-2.6 INV-1 (new invariant)")
        sent = t[start:start + 700]
        self.assertIn("RemainingLocalSeconds", sent,
                      "if INV-1 no longer lists RemainingLocalSeconds, §3.2 is obsolete")
        self.assertIn("phase, all timing endpoints", sent)

    def test_tn_r_05_is_in_s2(self):
        self.assertIn("TN-R-05", self.s2())

    def test_aging_formula_exists_in_a1r4(self):
        """§3.2's formula source must be real, not invented."""
        t = git_show(f"{A1R4_COMMIT}:{A1R4_PATH}")
        if t is None:
            self.skipTest("A1-R4 not available")
        flat = re.sub(r"\s+", " ", t)
        self.assertIn("max(0, R0", flat)
        self.assertIn("ProducerRate", flat)

    def test_s2_does_not_restate_the_aging_rule(self):
        """§3.2 claim: S2 does not restate R(t). If it now does, revisit §3."""
        t = self.s2()
        self.assertNotIn("max(0, R0", t,
                         "S2 now restates the aging formula; re-read §3.2")

    def test_arithmetic_demonstrates_the_violation(self):
        """Compute, don't assert: same revision, two different R values."""
        rate, r0 = 0.05, 0.20
        r_frame0 = max(0.0, r0 - 0.0 * rate)
        r_frame2 = max(0.0, r0 - 0.4 * rate)
        self.assertEqual(round(r_frame0, 4), 0.2)
        self.assertEqual(round(r_frame2, 4), 0.18)
        self.assertNotEqual(r_frame0, r_frame2,
                            "the two same-revision observations must differ")

    def test_tn_p_11_live_state_conflicts(self):
        self.assertIn("live state at call time", self.s2flat())

    def test_review_proposes_option_a_and_b(self):
        self.assertIn("Option A (recommended)", self.raw)
        self.assertIn("Option B", self.raw)

    def test_review_requires_tc05_46_fix(self):
        self.assertIn("T-C05-46", self.raw)


class TestEx5Ambiguity(Base):
    """§3.6: EX-5 does not unambiguously enumerate revisions for case (c)."""

    def test_ex5_exists_in_s2(self):
        self.assertIn("EX-5", self.s2())

    def test_ex5_text_still_ambiguous(self):
        """The 'then' construction plus 'if the dilation changes again' is the ambiguity."""
        t = self.s2flat()
        self.assertIn("phase change and retime in the same frame", t)
        self.assertIn("if the dilation changes again", t,
                      "EX-5 reworded; re-read §3.6")

    def test_tn_p_13_two_revision_rule_exists(self):
        self.assertIn("two revisions", self.s2flat())

    def test_no_published_ordering_rule_for_case_c(self):
        """§3.6 claim: S2 states two revisions but not which comes first."""
        t = self.s2()
        # there must be no clause naming PhaseChanged-before-Retimed ordering
        self.assertNotIn("PhaseChanged, then Retimed", t)
        self.assertNotIn("PhaseChanged` at `n+1`, `Retimed` at `n+2`", t)

    def test_review_requires_ordering_sentence(self):
        self.assertIn("published in that order", self.flat)


class TestResynchronised(Base):
    """§4: signal named and never declared."""

    def test_signal_named_in_s2(self):
        self.assertIn("Resynchronised", self.s2())

    def test_signal_has_no_declaration_in_s2(self):
        """If a type is declared, §4.2's condition is satisfied and this must fail."""
        t = self.s2()
        self.assertIsNone(
            re.search(r"struct\s+\w*Resynchron", t),
            "Resynchronised now declared; §4.2 condition 5 is closed, update the review")
        self.assertIsNone(re.search(r"enum class \w*Resync", t))

    def test_s2_says_no_new_transport(self):
        self.assertIn("needs no new transport", self.s2flat())

    def test_review_notes_two_suites_assert_on_it(self):
        for c in ("T-C05-45", "T-C05-50"):
            self.assertIn(c, self.raw)


class TestMissingConsumerFields(Base):
    """§4.3/§5: WindowKey and AttackTag absent from a snapshot whose consumers need them."""

    def test_absent_from_s2(self):
        t = self.s2()
        self.assertNotIn("WindowKey", t,
                         "WindowKey now present; §4.3/§5.3 conditions are closed")
        self.assertNotIn("AttackTag", t,
                         "AttackTag now present; §4.3/§5.3 conditions are closed")

    def test_snapshot_carries_exactly_four_fields(self):
        t = self.s2()
        m = re.search(r"struct FTDDTelegraphSnapshot.*?\{(.*?)\};", t, re.S)
        self.assertIsNotNone(m, "FTDDTelegraphSnapshot not found")
        fields = re.findall(r"^\s+\w[\w:<>]*\s+(\w+);", m.group(1), re.M)
        self.assertEqual(fields,
                         ["AttackInstanceId", "SourceEntityId", "Phase", "Timing"],
                         f"snapshot fields changed: {fields}")

    def test_my_submission_marks_them_required(self):
        """The finding rests on my own §7.6, so check it rather than assert it."""
        t = self.a2c05()
        sec = t.split("### 7.6 Required vs optional")[1].split("### 7.7")[0]
        self.assertIn("`WindowKey` | **Required**", sec)
        self.assertIn("`AttackTag` | **Required**", sec)

    def test_my_submission_names_four_consumers(self):
        """The C-05 row specifically: `Consumers (named)` appears 7x in the file."""
        t = self.a2c05()
        c05 = t.split("## 8. C-05")[1].split("## 9. C-06")[0]
        sec = c05.split("| **Consumers (named)** |")[1].split("\n")[0]
        # compare case-insensitively on BOTH sides: "VFX marker" vs sec.lower()
        low = sec.lower()
        for c in ("audio cue", "vfx marker", "montage selection"):
            self.assertIn(c, low, f"{c} not in my C-05 consumer list")

    def test_review_quotes_montage_trigger_distinction(self):
        self.assertIn("trigger", self.raw)


class TestDirectoryAndOwnership(Base):
    """§2.2/§6: the directory is a reversal of my §7.1, narrowly scoped."""

    def test_my_s71_objection_is_real(self):
        t = self.a2c05()
        flat = re.sub(r"\s+", " ", t)
        self.assertIn("No central telegraph director", flat)
        self.assertIn("second scheduler competing with StateTree", flat)

    def test_s2_scopes_directory_to_no_timing(self):
        flat = self.s2flat()
        self.assertIn("no timing, no phase, no revision", flat)

    def test_s2_scopes_vfx_assignment_to_agent2(self):
        self.assertIn("VFX marker", self.s2flat())

    def test_withdrawn_sentence_absent_from_normative_clause(self):
        """DV-4: the sentence appears exactly once, inside §3.1's quotation.

        My first version of this test asserted 0 occurrences and was wrong: the
        quotations legitimately reproduce the withdrawn words. The claim is
        "once, in the correction ledger, never in a normative clause".
        """
        t = self.s2()
        self.assertEqual(
            t.count("is Agent 1's in every candidate"), 1,
            "if this is 0 or >1, re-read review §7 / DV-4")
        line = [l for l in t.splitlines()
                if "is Agent 1's in every candidate" in l][0]
        self.assertIn("C05-7.1` then said", line,
                      "the single occurrence must be the §3.1 problem statement")

    def test_withdrawn_sentence_not_in_c05_7_1_clause(self):
        """The normative C05-7.1 clause must not contain it."""
        t = self.s2()
        sec = t.split("### 4.9 Referenced clauses")[1].split("## 5.")[0]
        self.assertNotIn("in every candidate", sec)

    def test_c05_7_3_excludes_agent2_producers(self):
        self.assertIn(
            "Agent 1 does not implement the `TN-P` obligations on Agent 2's enemy producers",
            self.s2flat())

    def test_no_conflict_verdict_stated(self):
        self.assertIn("**none — identical**", self.raw)

    def test_review_withdraws_own_dilation_error(self):
        """§2.5: I withdraw my A2-C05 §7.3 statement — check it existed."""
        t = re.sub(r"\s+", " ", self.a2c05())
        self.assertIn("a dilated window still ends at the same gameplay time", t)
        self.assertIn("I withdraw", self.raw)


class TestDocumentChecksReRun(Base):
    """§7: I re-ran DV-1, DV-2, DV-4, DV-6, DV-8."""

    def test_dv2_case_ids_complete(self):
        t = self.s2()
        found = {int(m) for m in re.findall(r"T-C05-(\d\d)", t)}
        self.assertEqual(found, set(range(1, 51)))

    def test_dv6_suite_rows_sum_to_50(self):
        t = self.s2()
        sec = t.split("### 13.1")[1].split("### 13.2")[0]
        tot = 0
        n = 0
        for line in sec.splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip().strip("*") for c in line.strip("|").split("|")]
            if len(cells) < 5 or not re.fullmatch(r"[A-K]", cells[0]):
                continue
            n += 1
            tot += int(cells[3])
        self.assertEqual(n, 11)
        self.assertEqual(tot, 50)

    def test_dv1_obligation_counts(self):
        t = self.s2()
        counts = {}
        for sec_name in ("## 6. Producer obligations",
                         "## 7. Consumer obligations",
                         "## 8. Shared read-surface"):
            body = t.split(sec_name)[1].split("\n## ")[0]
            rows = [l for l in body.splitlines() if l.startswith("| **TN-")]
            counts[sec_name] = len(rows)
        self.assertEqual(counts["## 6. Producer obligations"], 14)
        self.assertEqual(counts["## 7. Consumer obligations"], 9)
        # §8 holds TN-R-01..05 and TN-A-01..02 = 7 rows
        self.assertEqual(counts["## 8. Shared read-surface"], 7)

    def test_dv8_count_is_inaccurate(self):
        """The review says 12 'executed', DV-8 claims 10 'execut'. Both must hold."""
        t = self.s2()
        self.assertEqual(len(re.findall(r"[Ee]xecuted", t)), 12)
        self.assertIn("the stated count of 10 is wrong", self.flat)

    def test_d32660f_is_a_valid_commit_and_review_says_so(self):
        """§7 corrected finding: d32660f resolves; my earlier 'invalid' claim was mine.

        The commit is on origin/a3branch and carries the same MEAD-B blob the
        correction cites at 1eb613f. A short SHA failing to resolve locally is
        not evidence of a bad citation.
        """
        kind = git_run("cat-file", "-t", "d32660f")
        if kind is None:
            self.skipTest("d32660f not fetched in this clone")
        self.assertEqual(kind.strip(), "commit")
        blob = git_run("rev-parse", "d32660f:docs/MASTER_ENGINEERING_ARCHITECTURE.md")
        if blob is not None:
            self.assertEqual(blob.strip(),
                             "1e8d1bd1b223c364c02464f6036e3f9ee9a9b0a7")
        self.assertIn("was my error, not the document's", self.flat)

    def test_review_withdraws_the_invalid_object_claim(self):
        self.assertIn("A short SHA that does not resolve locally is not evidence",
                      self.flat)

    def test_placeholders_present_in_reviewed_blob(self):
        self.assertIn("PUB_COMMIT", self.s2())
        self.assertIn("already remediated", self.flat)


class TestRestrictions(Base):
    """§9: the restrictions, each with a checkable statement."""

    def test_zero_contract_tests_executed(self):
        self.assertIn("Tests executed by me on contract behaviour: 0", self.flat)

    def test_no_false_pass_claim(self):
        for bad in ("all tests pass", "tests passed successfully", "verified by execution"):
            self.assertNotIn(bad, self.raw.lower())

    def test_c05_and_u07_not_claimed_closed(self):
        self.assertIn("remain open", self.flat)
        self.assertIn("I do not claim otherwise", self.flat)

    def test_no_signature_claimed(self):
        self.assertIn("no signature given", self.flat)

    def test_mead_authorship_disclosed(self):
        self.assertIn("I authored MEAD-A", self.raw)

    def test_did_not_review_tip_but_reviewed_blob(self):
        self.assertIn(S2_BLOB, self.raw)
        self.assertIn("branch tip", self.flat)

    def test_restriction_table_present(self):
        for phrase in ("No C++ implementation", "No canonical MEAD selection",
                       "Preserve all earlier reviews"):
            self.assertIn(phrase, self.raw)

    def test_states_what_would_change_verdict(self):
        self.assertIn("what would change my verdict", self.flat)


class TestAlignmentWithS2Sections(unittest.TestCase):
    """The review must answer the five §17.2 questions, in order, once each."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def test_cites_17_2(self):
        self.assertIn("§17.2", self.raw)

    def test_each_question_section_names_its_clause_anchors(self):
        anchors = {
            "## 2. Q1": ["C05-7.2", "TN-P-14", "TN-P-13", "TN-P-08"],
            "## 3. Q2": ["INV-1", "EX-5", "TN-P-13"],
            "## 4. Q3": ["EN-3", "TN-C-09", "RS-1"],
            "## 5. Q4": ["C05-7.2", "TN-C-01", "TN-C-07"],
            "## 6. Q5": ["C05-7.3", "C05-7.2"],
        }
        for sec, needles in anchors.items():
            body = self.raw.split(sec)[1].split("\n## ")[0]
            for n in needles:
                self.assertIn(n, body, f"{sec} does not cite {n}")

    def test_review_section_count(self):
        for n in range(1, 11):
            self.assertRegex(self.raw, rf"(?m)^## {n}\. ")


if __name__ == "__main__":
    unittest.main()
