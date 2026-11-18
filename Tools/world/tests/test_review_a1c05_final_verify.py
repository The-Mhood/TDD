"""Tests for Docs/AGENT2_FINAL_VERIFY_C05_V2.md (W-M2.19).

Locks the final C-05 verification against Agent 1's S4.3.8, commit c4761f5.

DOCUMENT, ARITHMETIC and INSTRUMENT checks only. No contract behaviour is exercised:
no telegraph, producer, consumer or engine exists. All 67 acceptance cases are
PROPOSED / NOT RUN and none is run here. The regression cases are tests of the
checker, not acceptance tests, and are not treated as such.

TestSuccessorIsPublished pins the premise: the S4.3.8 successor exists and both
corrections are present. TestClosedConditions asserts the two W-M2.18 conditions are
now genuinely closed. TestNewRegression asserts the one defect this review adds,
F-1. If Agent 1 publishes a further revision, these fail - intended: the review must
then be reissued.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_FINAL_VERIFY_C05_V2.md"

TARGET = "c4761f52003958fb95c405db56591063f255f55f"
PREDECESSOR = "f1beb0c07f643d56c15297529196fb6a4118a97b"

DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md"
DOC_BLOB = "3c6bab6c63b6ed47e82a490a8858819080695f86"
REG_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8_PROVENANCE.md"
REG_BLOB = "60c003960bc047df93a0616397b7b1efb03fd89e"
DV_BLOB = "cd1606c208e9db2d51b4267dff5099167ee29921"
SUITE_BLOB = "a99adaf674e8bc86f9f99f50040a5b59374cd608"

PRED_DOC_BLOB = "0a0c36bec71f40d709878e67c19e4bca8f0b8b39"


def git_show(spec):
    r = subprocess.run(["git", "show", spec], capture_output=True,
                       text=True, cwd=ROOT, check=False)
    return r.stdout if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def doc(self):
        t = git_show("%s:%s" % (TARGET, DOC_PATH))
        if t is None:
            self.skipTest("reviewed document unavailable")
        return t

    def pred(self):
        return git_show(PRED_DOC_BLOB)


class Instr(Base):
    """Runs the shipped validator against injected text, in a scratch copy."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_show("%s:docs/validation/dv_c05.py" % TARGET)
        doc = git_show("%s:%s" % (TARGET, DOC_PATH))
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc

    def run_on(self, doc_text):
        (self._d / "doc.md").write_text(doc_text)
        return subprocess.run([sys.executable, str(self._d / "dv.py"),
                               str(self._d / "doc.md")],
                              capture_output=True, text=True, cwd=ROOT, check=False)

    def dv22(self, sentence):
        mut = self._doc.replace(
            "## 9. Shared read-surface",
            "| X | %s | a | b | c | d | e |\n## 9. Shared read-surface" % sentence)
        self.assertNotEqual(mut, self._doc, "injection anchor missing")
        r = self.run_on(mut)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-22 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]

    def dv24(self, insert):
        mut = self._doc.replace("## 9. Shared read-surface",
                                "%s\n## 9. Shared read-surface" % insert)
        self.assertNotEqual(mut, self._doc)
        r = self.run_on(mut)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]


# ---------------------------------------------------------------------------
# 1. The premise now holds: S4.3.8 exists
# ---------------------------------------------------------------------------

class TestSuccessorIsPublished(Base):
    def test_target_identities(self):
        for spec, blob in (("%s:%s" % (TARGET, DOC_PATH), DOC_BLOB),
                           ("%s:%s" % (TARGET, REG_PATH), REG_BLOB),
                           ("%s:docs/validation/dv_c05.py" % TARGET, DV_BLOB),
                           ("%s:docs/validation/test_dv_c05_regressions.py" % TARGET,
                            SUITE_BLOB)):
            r = subprocess.run(["git", "rev-parse", spec],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, spec)

    def test_reviewed_commit_is_still_intact(self):
        """S4.3.8 is an immutable historical record now that Agent 1 has moved on.

        This review found a fail-open regression at c4761f5; Agent 1 answered it at
        S4.3.9 (83c24f9) and S4.3.10 (7662926). So the correct assertion is no longer
        "the head has not moved" - it is "the commit reviewed here still exists and
        still carries the blobs this review pinned", so the finding stays checkable.
        """
        r = subprocess.run(["git", "rev-parse", "--verify", "%s^{commit}" % TARGET],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit no longer present in this clone")
        self.assertEqual(r.stdout.strip(), TARGET)

    def test_s437_predecessor_unmodified(self):
        a = git_show("%s:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md" % PREDECESSOR)
        b = git_show("%s:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md" % TARGET)
        if a is None or b is None:
            self.skipTest("unavailable")
        self.assertEqual(a, b)
        self.assertEqual(PRED_DOC_BLOB, PRED_DOC_BLOB)

    def test_document_is_2242_lines(self):
        self.assertEqual(len(self.doc().splitlines()), 2242)

    def test_review_states_the_successor_exists(self):
        self.assertIn("S4.3.8", self.flat)
        self.assertIn("c4761f5", self.flat)


# ---------------------------------------------------------------------------
# 2. Check 1: clean-archive reproduction, re-derived
# ---------------------------------------------------------------------------

class TestReproduction(Instr):
    def test_clean_document_scores_27_of_27(self):
        r = self.run_on(self._doc)
        self.assertIn("27/27 checks passed", r.stdout)

    def test_suite_total_is_114_literal_plus_6_generated(self):
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        literal = len(re.findall(r"^case\(\s*['\"]", s, re.M))
        pred = re.search(r"PREDECESSORS = \{(.*?)\n\}", s, re.S)
        n_pred = len(re.findall(r"^\s*['\"]", pred.group(1), re.M)) if pred else 0
        self.assertEqual((literal, n_pred), (114, 6))
        self.assertEqual(literal + n_pred, 120)

    def test_review_reports_120_derived(self):
        self.assertIn("120/120", self.flat)
        self.assertIn("114 literal", self.flat)

    def test_pairs_read_is_10_and_matches_the_runner(self):
        r = self.run_on(self._doc)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0]
        self.assertIn("pairs read 10", line)
        self.assertIn("pairs read", self.flat)


# ---------------------------------------------------------------------------
# 3. Checks 2 and 3: both corrections are PRESENT
# ---------------------------------------------------------------------------

class TestCorrectionsPresent(Instr):
    def test_check2_dv22_quantified_denials_pass(self):
        """W-M2.18 CONDITION-1 is closed."""
        for s in ("No audio cue belongs to Agent 1.",
                  "There is no audio cue that belongs to the first agent.",
                  "None of the audio cues belong to the first agent.",
                  "No audio cue is owned by Agent 1.",
                  "No audio cue is the first agent's."):
            self.assertEqual(self.dv22(s), "PASS", "CONDITION-1 regressed: %r" % s)

    def test_check2_ordinary_denials_still_pass(self):
        for s in ("Agent 1 owns no audio cues.",
                  "The audio cues do not belong to the first agent.",
                  "The audio cues are not the first agent's.",
                  "Nobody owns the audio cues."):
            self.assertEqual(self.dv22(s), "PASS", s)

    def test_check2_real_offences_still_caught(self):
        for s in ("The audio cues belong to Agent 1.",
                  "Agent 1 owns the audio cues.",
                  "Audio: Agent 1.",
                  "The audio cues are the first agent's."):
            self.assertEqual(self.dv22(s), "FAIL", s)

    def test_check3_dv24_capitalised_continuation_fails(self):
        """W-M2.18 CONDITION-2 is closed."""
        for s in ("Counts: 6 declared\nThe audit shows 5 observed.",
                  "Counts: 6 declared\nThen 5 observed.",
                  "Counts: 6 declared\nAnd 5 observed."):
            self.assertEqual(self.dv24(s), "FAIL", "CONDITION-2 regressed: %r" % s)

    def test_review_records_both_as_closed(self):
        flat = self.flat.lower()
        self.assertIn("condition-1", flat)
        self.assertIn("condition-2", flat)
        self.assertIn("closed", flat)


# ---------------------------------------------------------------------------
# 4. Check 4: the _joinable change does not reintroduce false joins
# ---------------------------------------------------------------------------

class TestNoFalseJoins(Instr):
    def test_all_block_boundaries_hold(self):
        for s in ("- declared 6\n- observed 5",
                  "# Heading declared 6\nThe row observed 5",
                  "> quote declared 6\n> quote observed 5",
                  "| declared 6 |\n| observed 5 |",
                  "declared 6\n\nobserved 5"):
            self.assertEqual(self.dv24(s), "PASS", s)

    def test_sentence_terminator_holds(self):
        self.assertEqual(
            self.dv24("The pass declared 6 priorities.\nThe instrument observed 5 events."),
            "PASS")

    def test_three_line_window_still_gated(self):
        self.assertEqual(self.dv24("Counts: 6 declared\nand then\n5 observed."), "FAIL")

    def test_two_line_wrap_still_detected(self):
        self.assertEqual(self.dv24("Counts: 6 declared and\n5 observed."), "FAIL")

    def test_review_reports_no_false_join(self):
        self.assertIn("no false join", self.flat.lower())


# ---------------------------------------------------------------------------
# 5. Check 5: S4.3.7 corrections still hold
# ---------------------------------------------------------------------------

class TestPriorCorrectionsHold(Instr):
    def test_dv22_possessive_synonym(self):
        self.assertEqual(self.dv22("The audio cues are the first agent's."), "FAIL")

    def test_dv22_long_foil(self):
        s = ("Agent 1, unlike what the wargame community might generally assume "
             "about Agent 2, owns the audio cues.")
        self.assertEqual(self.dv22(s), "FAIL")

    def test_dv24_three_line_wrap(self):
        self.assertEqual(self.dv24("Counts: 6 declared\nand then\n5 observed."), "FAIL")

    def test_dv11_owner_rule_live(self):
        r = self.run_on(self._doc)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-11 ")][0]
        self.assertIn("owner checks 8", line)
        self.assertIn("map verified True", line)


# ---------------------------------------------------------------------------
# 6. Checks 6 and 7: cases intact, new ones isolated, no deletions
# ---------------------------------------------------------------------------

class TestCaseIntegrity(Base):
    def test_new_cases_are_81_to_94(self):
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        ids = sorted({int(m) for m in re.findall(r"TD-(\d+)", s)})
        new = [i for i in ids if i >= 81]
        self.assertEqual(new, list(range(81, 95)))

    def test_no_case_deleted(self):
        r = subprocess.run(["git", "diff", "--numstat", PREDECESSOR, TARGET, "--",
                            "docs/validation/test_dv_c05_regressions.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        parts = r.stdout.split()
        self.assertEqual(parts[1], "1", "only one comment line may be deleted")

    def test_original_80_cases_still_present(self):
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        ids = {int(m) for m in re.findall(r"TD-(\d+)", s)}
        self.assertTrue(set(range(1, 81)).issubset(ids))

    def test_seven_verdicts_move_as_claimed(self):
        self.assertIn("seven verdicts move", self.flat.lower())


# ---------------------------------------------------------------------------
# 7. Check 8: normative boundaries unchanged
# ---------------------------------------------------------------------------

class TestNormativeBoundaries(Base):
    def rows(self, s):
        out = {}
        for h in ("## 7. Producer obligations", "## 8. Consumer obligations",
                  "## 9. Shared read-surface and arbitration obligations"):
            body = s.split(h)[1].split("\n## ")[0]
            for l in body.splitlines():
                if l.startswith("| **TN-"):
                    out[l.split("**")[1]] = l
        return out

    def test_all_43_obligation_rows_identical(self):
        a, b = self.rows(self.pred()), self.rows(self.doc())
        self.assertEqual(len(a), 43)
        self.assertEqual(a, b)

    def test_named_obligations_identical(self):
        a, b = self.pred(), self.doc()
        for oid in ("TN-C-11", "TN-C-14", "TN-C-15", "TN-A-01", "TN-A-02", "TN-A-03"):
            ra = [l for l in a.splitlines() if l.startswith("| **%s**" % oid)]
            rb = [l for l in b.splitlines() if l.startswith("| **%s**" % oid)]
            self.assertTrue(ra and rb, oid)
            self.assertEqual(ra, rb, oid)

    def test_case_specifications_identical(self):
        def cases(s):
            return {m.group(1): m.group(0)
                    for m in re.finditer(r"^\| \*\*(T-C05-\d+)\*\*.*$", s, re.M)}
        a, b = cases(self.pred()), cases(self.doc())
        self.assertEqual(len(a), 17)
        self.assertEqual(a, b)

    def test_d1_to_d7_unchanged(self):
        a, b = self.pred(), self.doc()
        for d in ("D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7"):
            ra = [l for l in a.splitlines() if l.startswith("| **%s** |" % d)]
            rb = [l for l in b.splitlines() if l.startswith("| **%s** |" % d)]
            self.assertTrue(ra, d)
            self.assertEqual(ra, rb, d)

    def test_18_suites_67_cases(self):
        sec = self.doc().split("### 12.1")[1].split("### 12.2")[0]
        n = tot = 0
        for l in sec.splitlines():
            if not l.startswith("|"):
                continue
            c = [x.strip().strip("*") for x in l.strip("|").split("|")]
            if len(c) < 5 or not re.fullmatch(r"[A-R]", c[0]):
                continue
            n += 1
            tot += int(c[3])
        self.assertEqual((n, tot), (18, 67))


# ---------------------------------------------------------------------------
# 8. F-1: the new regression this review finds
# ---------------------------------------------------------------------------

class TestNewRegression(Instr):
    def test_same_line_denial_plus_offence_is_missed(self):
        """F-1. The new NEG_BEFORE patterns span a clause boundary and excuse the
        later real offence on the same line."""
        self.assertEqual(
            self.dv22("No audio cue is assigned to Agent 2 and the audio cue "
                      "belongs to Agent 1."), "PASS", "F-1 apparently fixed - reissue")

    def test_but_form_is_missed(self):
        self.assertEqual(
            self.dv22("No audio cue is provided for Agent 2, but the audio cue "
                      "belongs to Agent 1."), "PASS", "F-1 apparently fixed - reissue")

    def test_plain_offence_still_caught(self):
        """The control that shows the miss is specific to the combined line."""
        self.assertEqual(self.dv22("The audio cue belongs to Agent 1."), "FAIL")

    def test_the_new_patterns_are_the_cause(self):
        src = (self._d / "dv.py").read_text()
        self.assertIn(r"belong(?:s)?\s+to\s+' + AGENT1", src)
        self.assertIn(r"r'\bno\s+' + _MODS + r'audio\b[^.;|]{0,50}?", src,
                      "the gap should still cross '.' ';' '|' only")

    def test_suite_has_no_case_for_the_combined_line(self):
        """No case places a quantified denial and a real offence on ONE line.

        TD-84's control uses a separate line, which is why the suite stays green.
        """
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        for shape in ("assigned to Agent 2 and", "provided for Agent 2",
                      "Agent 2, but the audio cue"):
            self.assertNotIn(shape, s, "a case now covers it - reissue: %r" % shape)

    def test_review_classifies_it_material(self):
        self.assertIn("F-1", self.flat)
        self.assertIn("material blocker", self.flat.lower())


# ---------------------------------------------------------------------------
# 9. Verdict and governance
# ---------------------------------------------------------------------------

class TestVerdict(Base):
    def test_verdict_is_targeted_revision_required(self):
        self.assertIn("`TARGETED REVISION REQUIRED`", self.raw)

    def test_verdict_is_not_driven_by_the_minor_items(self):
        self.assertIn("not a reason for the verdict", self.flat)

    def test_zero_acceptance_cases_and_regressions_not_acceptance(self):
        self.assertIn("0 of 67 acceptance cases executed", self.flat)
        self.assertIn("tests of the checker, not of the contract", self.flat)

    def test_no_governance_overreach(self):
        flat = self.flat
        for bad in ("C-05 is approved", "U-07 is closed", "a MEAD was selected",
                    "C-05 is frozen", "signature granted"):
            for m in re.finditer(re.escape(bad), flat):
                ctx = flat[max(0, m.start() - 70):m.start() + 30].lower()
                self.assertTrue(any(n in ctx for n in ("no ", "not ", "never", "open", "nothing ")),
                                "affirmative governance claim: %r" % ctx)

    def test_does_not_resolve_tn_c11_or_tn_a_boundary(self):
        self.assertIn("I do not resolve them", self.flat)

    def test_reviewed_files_not_modified_by_me(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--",
                            "docs/validation/dv_c05.py",
                            "docs/validation/test_dv_c05_regressions.py",
                            DOC_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_FINAL_VERIFY_C05_V1.md",
                  "AGENT2_REVIEW_A1C05_S4_3_7_V1.md",
                  "AGENT2_REVIEW_A1C05_S4_3_6_V1.md",
                  "AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
