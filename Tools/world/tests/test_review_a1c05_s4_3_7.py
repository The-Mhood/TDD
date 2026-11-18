"""Tests for Docs/AGENT2_REVIEW_A1C05_S4_3_7_V1.md (W-M2.18).

Locks the S4.3.7 instrument review against the exact reviewed commit f1beb0c.

DOCUMENT, ARITHMETIC and INSTRUMENT checks only. No contract behaviour is exercised:
no telegraph, producer, consumer or engine exists. All 67 acceptance cases are
PROPOSED / NOT RUN and none is run here. The 106 regression cases are tests of the
checker, not acceptance tests, and are not treated as such.

TestOpenConditions asserts the two defects the review reports as OPEN, plus MINOR-1.
If Agent 1 fixes them those tests fail - intended: the review must then be reissued
or the conditions reassessed. Each names the condition it guards.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_REVIEW_A1C05_S4_3_7_V1.md"

TARGET = "f1beb0c07f643d56c15297529196fb6a4118a97b"
DOC_BLOB = "0a0c36bec71f40d709878e67c19e4bca8f0b8b39"
REG_BLOB = "ef8dac0d99337195f43a8ceb6b829e36470964a4"
DV_BLOB = "06cfe2f24fb17b2540eab9e6f8fd12efdcc79a93"
SUITE_BLOB = "2a33543a8b6941262915e9a33b614411910b030b"
DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md"

PRED_COMMIT = "034d091e1abcb507fdba6df4a05318a15aa5d7a1"
PRED_BLOB = "e3a1fa85243a4749591363d4196bb5d65dad7c84"
PRED_DV_BLOB = "840fed6730a5b2e18a5f717f98c6de273b9c8721"
S435_BLOB = "a0b46f46c81e85cea5d04b940aaf9aee46c19deb"


def git_show(spec):
    r = subprocess.run(["git", "show", spec], capture_output=True,
                       text=True, cwd=ROOT, check=False)
    return r.stdout if r.returncode == 0 else None


def git_path(commit, path):
    return git_show("%s:%s" % (commit, path))


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def doc(self):
        t = git_path(TARGET, DOC_PATH)
        if t is None:
            self.skipTest("reviewed document unavailable")
        return t

    def validator(self):
        t = git_path(TARGET, "docs/validation/dv_c05.py")
        if t is None:
            self.skipTest("validator unavailable")
        return t


class Instr(Base):
    """Shared harness: run a pinned validator on a copy of the reviewed document."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_path(TARGET, "docs/validation/dv_c05.py")
        doc = git_path(TARGET, DOC_PATH)
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        old = git_show(PRED_DV_BLOB)
        if old:
            (cls._d / "old.py").write_text(old)
        cls._doc = doc

    def run_on(self, script, doc_text):
        (self._d / "doc.md").write_text(doc_text)
        return subprocess.run([sys.executable, str(self._d / script),
                               str(self._d / "doc.md")],
                              capture_output=True, text=True, cwd=ROOT, check=False)

    def dv22(self, sentence, script="dv.py", doc=None):
        base = doc if doc is not None else self._doc
        mut = base.replace("## 9. Shared read-surface",
                           "| X | %s | a | b | c | d | e |\n## 9. Shared read-surface"
                           % sentence)
        self.assertNotEqual(mut, base, "injection anchor missing")
        r = self.run_on(script, mut)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-22 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1], r.stdout

    def dv24(self, insert, script="dv.py"):
        mut = self._doc.replace("## 9. Shared read-surface",
                                "%s\n## 9. Shared read-surface" % insert)
        self.assertNotEqual(mut, self._doc)
        r = self.run_on(script, mut)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]


# ---------------------------------------------------------------------------
# 1. Exact target and provenance
# ---------------------------------------------------------------------------

class TestExactTarget(Base):
    def test_document_blob(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, DOC_PATH)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), DOC_BLOB)

    def test_register_and_instrument_blobs(self):
        for path, blob in (("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7_PROVENANCE.md", REG_BLOB),
                           ("docs/validation/dv_c05.py", DV_BLOB),
                           ("docs/validation/test_dv_c05_regressions.py", SUITE_BLOB)):
            r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, path)],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, path)

    def test_register_names_document_and_instruments(self):
        t = git_show(REG_BLOB)
        if t is None:
            self.skipTest("register unavailable")
        for blob in (DOC_BLOB, DV_BLOB, SUITE_BLOB):
            self.assertIn(blob, t)

    def test_document_is_2107_lines(self):
        self.assertEqual(len(self.doc().splitlines()), 2107)

    def test_both_predecessors_preserved(self):
        for path, blob in (
            ("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md", PRED_BLOB),
            ("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md", S435_BLOB),
        ):
            r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, path)],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, path)

    def test_s436_range_diff_is_empty(self):
        r = subprocess.run(["git", "diff", "--stat", PRED_COMMIT, TARGET, "--",
                            "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        self.assertEqual(r.stdout.strip(), "")

    def test_review_records_identities(self):
        for s in (DOC_BLOB, TARGET, DV_BLOB, SUITE_BLOB, REG_BLOB):
            self.assertIn(s, self.flat)


# ---------------------------------------------------------------------------
# 2. Reproduction
# ---------------------------------------------------------------------------

class TestReproduction(Instr):
    def test_clean_document_scores_27_of_27(self):
        r = self.run_on("dv.py", self._doc)
        self.assertIn("27/27 checks passed", r.stdout)

    def test_suite_arithmetic_is_100_literal_plus_6_generated(self):
        s = git_path(TARGET, "docs/validation/test_dv_c05_regressions.py")
        if s is None:
            self.skipTest("suite unavailable")
        literal = len(re.findall(r"^case\(\s*['\"]([^'\"]+)", s, re.M))
        pred = re.search(r"PREDECESSORS = \{(.*?)\n\}", s, re.S)
        n_pred = len(re.findall(r"^\s*['\"]", pred.group(1), re.M)) if pred else 0
        self.assertEqual((literal, n_pred), (100, 6))
        self.assertEqual(literal + n_pred, 106)

    def test_nineteen_new_cases_plus_td60_gap(self):
        r = subprocess.run(["git", "diff", PRED_COMMIT, TARGET, "--",
                            "docs/validation/test_dv_c05_regressions.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        self.assertEqual([l for l in r.stdout.splitlines()
                          if l.startswith("-") and not l.startswith("---")], [],
                         "no existing case may be edited or removed")
        ids = sorted({int(m) for m in re.findall(r"TD-(\d+)", r.stdout)})
        new = [i for i in ids if i >= 61]
        self.assertEqual(new, list(range(61, 81)))

    def test_review_states_the_numbers(self):
        for n in ("27/27", "106/106", "100", "6"):
            self.assertIn(n, self.flat)


# ---------------------------------------------------------------------------
# 3. DV-22 verified corrections
# ---------------------------------------------------------------------------

class TestDv22Corrections(Instr):
    def test_a2_major1_possessive_synonym_closed(self):
        self.assertEqual(self.dv22("The audio cues are the first agent's.")[0], "FAIL")

    def test_a2_major2_long_foil_closed(self):
        s = ("Agent 1, unlike what the wargame community might generally assume "
             "about Agent 2, owns the audio cues.")
        self.assertEqual(self.dv22(s)[0], "FAIL")

    def test_further_attachment_patterns(self):
        for s in ("The audio cues belong to the first agent.",
                  "The audio cue's owner is the first agent.",
                  "Agent 1 's audio cues.",
                  "The first agent's audio cues.",
                  "The first agent holds the audio cues.",
                  "Audio cue ownership: the first agent.",
                  "The audio cues were provided by Agent 1."):
            self.assertEqual(self.dv22(s)[0], "FAIL", s)

    def test_td66_denial_is_not_an_assignment(self):
        self.assertEqual(self.dv22("The audio cues do not belong to the first agent.")[0], "PASS")

    def test_td67_contrasted_object(self):
        self.assertEqual(
            self.dv22("The camera, rather than the audio cues, is owned by Agent 1.")[0], "PASS")

    def test_agent2_ownership_never_attributed_to_agent1(self):
        for s in ("Agent 2 owns the audio cues.",
                  "The audio cues are Agent 2's.",
                  "The audio cues belong to Agent 2.",
                  "The audio cue's owner is Agent 2.",
                  "Agent 2, unlike Agent 1, owns the audio cues.",
                  "Agent 2 rather than Agent 1 owns the audio cues.",
                  "Agent 2, but not Agent 1, owns the audio cues."):
            self.assertEqual(self.dv22(s)[0], "PASS", s)

    def test_ordinary_denials_still_pass(self):
        for s in ("Agent 1 owns no audio cues.",
                  "Agent 1 does not own the audio cues.",
                  "The audio cues are not the first agent's.",
                  "Agent 1 has no C-05 audio responsibility.",
                  "Audio is not owned by Agent 1.",
                  "Agent 1 is not responsible for audio cue selection."):
            self.assertEqual(self.dv22(s)[0], "PASS", s)

    def test_genuine_agent1_ownership_still_caught(self):
        for s in ("Agent 1 owns the audio cues.",
                  "The audio cues are owned by Agent 1.",
                  "Audio cues: Agent 1.",
                  "Agent 1 is responsible for the audio cues.",
                  "The first agent owns the audio cues."):
            self.assertEqual(self.dv22(s)[0], "FAIL", s)


# ---------------------------------------------------------------------------
# 4. DV-24 verified corrections and the regression
# ---------------------------------------------------------------------------

class TestDv24Corrections(Instr):
    def test_three_line_wrap_caught(self):
        self.assertEqual(self.dv24("Counts: 6 declared\nand then\n5 observed."), "FAIL")

    def test_three_line_wrap_with_continuation_caught(self):
        self.assertEqual(self.dv24("Counts: 6 declared\nin the audit\nand 5 observed."), "FAIL")

    def test_correct_three_line_pair_passes(self):
        self.assertEqual(self.dv24("Counts: 7 declared\nand then\n5 observed."), "PASS")

    def test_false_join_controls_pass(self):
        for s in ("- declared 6\n- observed 5",
                  "The pass declared 6 priorities.\nThe instrument observed 5 events.",
                  "# Heading declared 6\nThe row observed 5",
                  "> quote declared 6\n> quote observed 5",
                  "| a declared 6\n| a observed 5"):
            self.assertEqual(self.dv24(s), "PASS", s)

    def test_two_label_window_not_cross_paired(self):
        self.assertEqual(self.dv24("declared 6 and declared 7\nobserved 5 and observed 4"), "PASS")

    def test_genuine_contradictions_still_caught(self):
        for s in ("declared 6, observed 5",
                  "6 observed of 7 declared",
                  "Six declared\nand five observed.",
                  "| x | 6 declared and 5 observed | y |"):
            self.assertEqual(self.dv24(s), "FAIL", s)


# ---------------------------------------------------------------------------
# 5. DV-11 owner rule
# ---------------------------------------------------------------------------

class TestDv11OwnerRule(Instr):
    def dv11_detail(self, doc):
        r = self.run_on("dv.py", doc)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-11 ")]
        self.assertTrue(line, r.stdout[-300:])
        m = re.search(r"owner checks (\d+) \(map verified (\w+)\), failures (\[.*?\])", line[0])
        return line[0].split()[1], m.groups() if m else None

    def mutate(self, old, new):
        self.assertIn(old, self._doc, old)
        return self._doc.replace(old, new, 1)

    def test_td78_correct_evidence_passes(self):
        v, detail = self.dv11_detail(self._doc)
        self.assertEqual(v, "PASS")
        self.assertEqual(detail[0], "8")
        self.assertEqual(detail[1], "True", "row-owner map must be verified against §5.2")

    def test_td77_isolates_the_owner_rule(self):
        """Row 5 IS in TN-C's allowed {5,6}, so only ownership can reject it."""
        m = self.mutate("| `Agent 2, C-05 consumer` | Agent 2 | **row 6**",
                        "| `Agent 2, C-05 consumer` | Agent 2 | **row 5**")
        v, detail = self.dv11_detail(m)
        self.assertEqual(v, "FAIL")
        self.assertIn("whose owner is", detail[2], "must fail on OWNERSHIP, not allowed-row")

    def test_td77_moves_pass_to_fail_between_validators(self):
        if not (self._d / "old.py").exists():
            self.skipTest("predecessor validator unavailable")
        m = self.mutate("| `Agent 2, C-05 consumer` | Agent 2 | **row 6**",
                        "| `Agent 2, C-05 consumer` | Agent 2 | **row 5**")
        r = self.run_on("old.py", m)
        self.assertIn("DV-11 PASS", r.stdout)
        r2 = self.run_on("dv.py", m)
        self.assertIn("DV-11 FAIL", r2.stdout)

    def test_td80_allowed_row_fires_alone(self):
        m = self.mutate("| `Agent 2, C-05 consumer` | Agent 2 | **row 6**",
                        "| `Agent 2, C-05 consumer` | Agent 2 | **row 7**")
        v, detail = self.dv11_detail(m)
        self.assertEqual(v, "FAIL")
        self.assertEqual(detail[2], "[]", "owner rule must NOT be what rejects row 7")

    def test_td79_dual_owned_row_legal(self):
        self.assertEqual(self.dv11_detail(self._doc)[0], "PASS")

    def test_owner_map_is_verified_against_section_5_2(self):
        src = (self._d / "dv.py").read_text()
        self.assertIn("owner_map_ok", src)
        self.assertIn("rows52", src)


# ---------------------------------------------------------------------------
# 6. Conditions still OPEN -- guards
# ---------------------------------------------------------------------------

class TestOpenConditions(Instr):
    def test_condition1_quantified_denial_is_a_false_positive(self):
        """DV-22: 'no ... belongs to' is a denial, not an assignment."""
        for s in ("No audio cue belongs to Agent 1.",
                  "There is no audio cue that belongs to the first agent.",
                  "None of the audio cues belong to the first agent."):
            v, _ = self.dv22(s)
            self.assertEqual(v, "FAIL",
                             "if PASS, CONDITION-1 is closed - reassess: %r" % s)

    def test_condition1_predates_the_widening_in_s436(self):
        if not (self._d / "old.py").exists():
            self.skipTest("predecessor unavailable")
        v, _ = self.dv22("No audio cue belongs to Agent 1.", script="old.py")
        self.assertEqual(v, "PASS", "S4.3.6 accepted it; S4.3.7 now rejects it")

    def test_condition2_capitalised_two_line_wrap_is_missed(self):
        """DV-24: _joinable rejects a capitalised continuation."""
        for s in ("Counts: 6 declared\nThe audit shows 5 observed.",
                  "Counts: 6 declared\nThen 5 observed.",
                  "Counts: 6 declared\nAnd 5 observed."):
            self.assertEqual(self.dv24(s), "PASS",
                             "if FAIL, CONDITION-2 is closed - reassess: %r" % s)

    def test_condition2_is_a_regression_from_s436(self):
        if not (self._d / "old.py").exists():
            self.skipTest("predecessor unavailable")
        s = "Counts: 6 declared\nThe audit shows 5 observed."
        self.assertEqual(self.dv24(s, script="old.py"), "FAIL",
                         "S4.3.6 caught this; S4.3.7 must not silently lose it")
        self.assertEqual(self.dv24(s, script="dv.py"), "PASS")

    def test_lowercase_continuation_still_caught(self):
        self.assertEqual(self.dv24("Counts: 6 declared\nand 5 observed."), "FAIL")

    def test_minor1_pairs_read_is_nine_not_eight(self):
        r = self.run_on("dv.py", self._doc)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0]
        self.assertIn("pairs read 9", line, "if 8, MINOR-1 is corrected - update the review")
        self.assertIn("disagreeing pairs 0", line)

    def test_review_reports_the_conditions_and_minor1(self):
        for s in ("CONDITION-1", "CONDITION-2", "MINOR-1",
                  "No audio cue belongs to Agent 1.",
                  "The audit shows 5 observed.",
                  "pairs read"):
            self.assertIn(s, self.flat)


# ---------------------------------------------------------------------------
# 7. Normative preservation
# ---------------------------------------------------------------------------

class TestNormativePreservation(Base):
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
        a, b = self.rows(git_show(PRED_BLOB)), self.rows(self.doc())
        self.assertEqual(len(a), 43)
        self.assertEqual(a, b)

    def test_key_clauses_identical(self):
        a, b = git_show(PRED_BLOB), self.doc()
        for name in ("### 5.2", "### 5.4", "### 9.2", "### 4.9", "### 3.6", "### 4.2"):
            self.assertEqual(a.split(name)[1].split("\n### ")[0],
                             b.split(name)[1].split("\n### ")[0], name)

    def test_named_obligations_identical(self):
        a, b = git_show(PRED_BLOB), self.doc()
        for oid in ("TN-C-11", "TN-C-14", "TN-C-15", "TN-A-01", "TN-A-02", "TN-A-03"):
            ra = [l for l in a.splitlines() if l.startswith("| **%s**" % oid)]
            rb = [l for l in b.splitlines() if l.startswith("| **%s**" % oid)]
            self.assertTrue(ra and rb, oid)
            self.assertEqual(ra, rb, oid)

    def test_case_specifications_identical(self):
        def cases(s):
            return {m.group(1): m.group(0)
                    for m in re.finditer(r"^\| \*\*(T-C05-\d+)\*\*.*$", s, re.M)}
        a, b = cases(git_show(PRED_BLOB)), cases(self.doc())
        self.assertEqual((len(a), len(b)), (17, 17))
        self.assertEqual(a, b)
        self.assertEqual(a["T-C05-63"], b["T-C05-63"])
        self.assertEqual(a["T-C05-64"], b["T-C05-64"])

    def test_d1_to_d7_unchanged(self):
        a, b = git_show(PRED_BLOB), self.doc()
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
# 8. Boundaries and governance
# ---------------------------------------------------------------------------

class TestBoundaries(Base):
    def test_agent3_s436_review_still_absent(self):
        r = subprocess.run(["git", "ls-tree", "-r", "--name-only",
                            "origin/arena/c64fc525-tdd"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("Agent 3 branch unavailable")
        names = "\n".join(f for f in r.stdout.splitlines() if "AGENT3" in f)
        self.assertTrue(names, "the three pre-S4.3 Agent 3 files should exist")
        self.assertNotIn("S4_3_6", names)
        self.assertNotIn("S4_3_7", names)

    def test_review_marks_agent3_unable_to_verify(self):
        self.assertIn("UNABLE TO VERIFY", self.flat)
        self.assertIn("did not inspect it and I have not pretended to", self.flat)

    def test_verdict_is_pass_with_conditions(self):
        self.assertIn("`PASS WITH CONDITIONS`", self.raw)

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
        self.assertIn("unresolved", self.flat)

    def test_target_not_modified_by_me(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--", DOC_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_REVIEW_A1C05_S4_3_6_V1.md",
                  "AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_2_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()


class TestCountReconciliationRepair(unittest.TestCase):
    """The 191-check false positive I fixed to publish this review (section 10.5).

    Pins that the repair keeps the check's purpose: a hex digest is not a count,
    and a genuine stale '191' is still an offender.
    """

    def flagged(self, line):
        path = ROOT / "Tools/world/tests/test_count_reconciliation.py"
        src = path.read_text(encoding="utf-8")
        self.assertIn(r'[0-9a-f]{7,40}', src,
                      "SHA-masking must be present or this review's citations break the suite")
        markers = ("corrects", "correction", "191 → 196", "191 -> 196",
                   "recorded as 191", "was 191", "191 when")
        if "191" not in line:
            return False
        if any(m in line.lower() for m in markers):
            return False
        masked = re.sub(r"\b[0-9a-f]{7,40}\b", "<sha>", line, flags=re.I)
        return "191" in masked

    def test_git_sha_containing_191_is_not_flagged(self):
        self.assertFalse(self.flagged(
            "| **Suite blob** | `2a33543a8b6941262915e9a33b614411910b030b` |"))

    def test_genuine_stale_count_is_still_flagged(self):
        self.assertTrue(self.flagged("the chapter has 191 location entries"))
        self.assertTrue(self.flagged("CH01 now covers 191 locations."))

    def test_correction_marker_still_exempts(self):
        self.assertFalse(self.flagged("this corrects 191 → 196"))

    def test_review_documents_the_repair(self):
        flat = re.sub(r"\s+", " ", REVIEW.read_text(encoding="utf-8"))
        self.assertIn("test_count_reconciliation.py", flat)
        self.assertIn("offset 31", flat)
