"""Tests for Docs/AGENT2_FINAL_VERIFY_C05_S4_3_10_V1.md (W-M2.20).

Locks the final verification of Agent 1's S4.3.10 (commit 7662926), the targeted
F-1b correction cycle.

DOCUMENT, ARITHMETIC and INSTRUMENT checks only. No contract behaviour is exercised:
no telegraph, producer, consumer or engine exists. All 67 acceptance cases are
PROPOSED / NOT RUN and none is run here. The 147 regression cases are tests of the
checker, not acceptance tests, and are not treated as such.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_FINAL_VERIFY_C05_S4_3_10_V1.md"

TARGET = "7662926c4c3b7293daedcc393c0ec4d015cdd883"
BASELINE = "83c24f9ce974c8194d5788d62c28043cc7511974"

DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md"
DOC_BLOB = "857778e18a35b35b1a5420905ec5f1482fddf868"
REG_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10_PROVENANCE.md"
REG_BLOB = "675014ec84852d92ffe37769802ae97ac86796e3"
DV_BLOB = "353a2bff220d4daa4c176daafc941256098959ed"
SUITE_BLOB = "7ab55805c27a271706f16e9295f1f503dc5a6c94"

BASE_DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md"
BASE_DOC_BLOB = "72d218a865b6713f78cb22308fa3dea81c74ac39"

ACTIVE = "## 9. Shared read-surface and arbitration obligations"


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

    def base_doc(self):
        return git_show(BASE_DOC_BLOB)


class Instr(Base):
    """Runs the shipped validator against injected text, in a scratch copy."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_show("%s:docs/validation/dv_c05.py" % TARGET)
        doc = git_show("%s:%s" % (TARGET, DOC_PATH))
        bdv = git_show("%s:docs/validation/dv_c05.py" % BASELINE)
        bdoc = git_show("%s:%s" % (BASELINE, BASE_DOC_PATH))
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc
        if bdv is not None and bdoc is not None:
            (cls._d / "bdv.py").write_text(bdv)
            cls._bdoc = bdoc
        else:
            cls._bdoc = None

    def verdict(self, tool, insert, doc=None, dv="dv.py"):
        base = self._doc if doc is None else doc
        if tool == "DV-22":
            mut = base.replace(ACTIVE,
                               "| X | %s | a | b | c | d | e |\n%s" % (insert, ACTIVE))
        else:
            mut = base.replace(ACTIVE, "%s\n%s" % (insert, ACTIVE))
        self.assertNotEqual(mut, base, "injection anchor missing")
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / dv), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith(tool + " ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]

    def both(self, tool, insert):
        """Verdict at S4.3.9 and at S4.3.10 for the same injected text."""
        a = self.verdict(tool, insert, doc=self._bdoc, dv="bdv.py")
        b = self.verdict(tool, insert)
        return a, b


# ---------------------------------------------------------------------------
# 1. The exact published commit
# ---------------------------------------------------------------------------

class TestPublishedCommit(Base):
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

    def test_baseline_document_is_unmodified(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, BASE_DOC_PATH)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("unavailable")
        self.assertEqual(r.stdout.strip(), BASE_DOC_BLOB)

    def test_document_is_2441_lines(self):
        self.assertEqual(len(self.doc().splitlines()), 2441)

    def test_only_one_alternation_changed_in_the_validator(self):
        r = subprocess.run(["git", "diff", "--numstat", BASELINE, TARGET, "--",
                            "docs/validation/dv_c05.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        added, removed = r.stdout.split()[0], r.stdout.split()[1]
        self.assertEqual((added, removed), ("11", "3"))

    def test_suite_gained_no_deletions(self):
        r = subprocess.run(["git", "diff", "--numstat", BASELINE, TARGET, "--",
                            "docs/validation/test_dv_c05_regressions.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        self.assertEqual(r.stdout.split()[1], "0", "a carried case may not be edited")


# ---------------------------------------------------------------------------
# 2. F-1b is closed, and closed by the intended rule
# ---------------------------------------------------------------------------

class TestF1bClosed(Instr):
    F1B = ("No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.")

    def test_original_statement_moved_pass_to_fail(self):
        a, b = self.both("DV-22", self.F1B)
        self.assertEqual(a, "PASS", "the S4.3.9 defect should reproduce")
        self.assertEqual(b, "FAIL", "F-1b should be closed")

    def test_equivalent_constructions_all_move(self):
        for s in ("No audio cue is assigned to Agent 2, the audio cue is owned by Agent 1.",
                  "No audio cue is provided for Agent 2, the audio cue is Agent 1's.",
                  "No audio cue is provided for Agent 2, the audio cue belongs to the first agent.",
                  "Agent 1 owns the camera, the audio cues."):
            a, b = self.both("DV-22", s)
            self.assertEqual((a, b), ("PASS", "FAIL"), s)

    def test_the_comma_alternative_is_gone(self):
        src = (self._d / "dv.py").read_text()
        # the old construction: a negator OR a bare comma
        self.assertNotIn("(?:\\bnot|,)\\s+(?:the\\s+|any\\s+)", src,
                         "the bare comma alternative should be removed")
        # the new construction: a stated negator only
        self.assertIn("\\bnot\\s+(?:the\\s+|any\\s+)", src)
        # and the negator is required, not optional
        self.assertNotIn("\\bnot?\\s+(?:the\\s+|any\\s+)", src)

    def test_review_traces_the_mechanism(self):
        self.assertIn("', the audio'", self.flat)
        self.assertIn("negated_mention", self.flat)


# ---------------------------------------------------------------------------
# 3. Legitimate statements protected
# ---------------------------------------------------------------------------

class TestLegitimateProtected(Instr):
    def test_object_negations_still_pass_at_both(self):
        for s in ("Agent 1 owns the camera, not the audio cues.",
                  "Agent 1 owns the camera, not any audio cues.",
                  "Agent 1 owns the camera, but not the audio cues.",
                  "Agent 1 owns the camera,not the audio cues.",
                  "Agent 1 owns the camera, the lighting rig, the montage track, "
                  "and not the audio cues.",
                  "Agent 1 owns the camera, not the C-05 audio cues."):
            a, b = self.both("DV-22", s)
            self.assertEqual((a, b), ("PASS", "PASS"), s)

    def test_positive_ownership_still_caught_at_both(self):
        for s in ("The audio cues belong to Agent 1.",
                  "Agent 1 owns the audio cues.",
                  "Audio: Agent 1.",
                  "The audio cues are the first agent's.",
                  "The audio cues are owned by Agent 1."):
            a, b = self.both("DV-22", s)
            self.assertEqual((a, b), ("FAIL", "FAIL"), s)


# ---------------------------------------------------------------------------
# 4. Preserved corrections
# ---------------------------------------------------------------------------

class TestPreserved(Instr):
    def test_f1_conjunction_boundary_holds(self):
        for s in ("No audio cue is assigned to Agent 2 and the audio cue belongs to Agent 1.",
                  "No audio cue is provided for Agent 2, but the audio cue belongs to Agent 1.",
                  "No audio cue is assigned to Agent 2; the audio cue belongs to Agent 1."):
            a, b = self.both("DV-22", s)
            self.assertEqual((a, b), ("FAIL", "FAIL"), s)

    def test_condition1_holds(self):
        for s in ("No audio cue belongs to Agent 1.",
                  "There is no audio cue that belongs to the first agent.",
                  "None of the audio cues belong to the first agent.",
                  "No audio cue is owned by Agent 1."):
            a, b = self.both("DV-22", s)
            self.assertEqual((a, b), ("PASS", "PASS"), s)

    def test_condition2_and_wraps_hold(self):
        for s in ("Counts: 6 declared\nThe audit shows 5 observed.",
                  "Counts: 6 declared\nThen 5 observed.",
                  "Counts: 6 declared\nAnd 5 observed.",
                  "Counts: 6 declared\nand then\n5 observed."):
            a, b = self.both("DV-24", s)
            self.assertEqual((a, b), ("FAIL", "FAIL"), s)

    def test_seven_joinable_boundaries_hold(self):
        for s in ("- declared 6\n- observed 5",
                  "The pass declared 6 priorities.\nThe instrument observed 5 events.",
                  "# Heading declared 6\nThe row observed 5",
                  "> quote declared 6\n> quote observed 5",
                  "| declared 6 |\n| observed 5 |",
                  "declared 6\n\nobserved 5"):
            a, b = self.both("DV-24", s)
            self.assertEqual((a, b), ("PASS", "PASS"), s)

    def test_minor1_pair_count_matches_runner(self):
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        # run on the clean document
        (self._d / "clean.md").write_text(self._doc)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"),
                            str(self._d / "clean.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0]
        self.assertIn("pairs read 10", line)


# ---------------------------------------------------------------------------
# 5. Suite, counts and the five verdict movements
# ---------------------------------------------------------------------------

class TestSuiteAndCounts(Base):
    def test_suite_total_is_147(self):
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        literal = len(re.findall(r"^case\(", s, re.M))
        pred = re.search(r"PREDECESSORS = \{(.*?)\n\}", s, re.S)
        n_pred = len(re.findall(r"^\s*['\"]", pred.group(1), re.M)) if pred else 0
        self.assertEqual(literal + n_pred, 147)

    def test_new_cases_are_contiguous_104_to_121(self):
        s = git_show("%s:docs/validation/test_dv_c05_regressions.py" % TARGET)
        if s is None:
            self.skipTest("suite unavailable")
        ids = sorted({int(m) for m in re.findall(r"TD-(\d+)", s)})
        new = [i for i in ids if i >= 104]
        self.assertEqual(new, list(range(104, 122)))

    def test_review_reports_five_moves_only(self):
        self.assertIn("Exactly five verdicts move", self.flat)
        for cid in ("TD-104", "TD-105", "TD-106", "TD-107", "TD-108"):
            self.assertIn(cid, self.flat)

    def test_review_reports_129_carried(self):
        self.assertIn("129 carried", self.flat)
        self.assertIn("147", self.flat)

    def test_normative_boundaries_identical(self):
        a, b = self.base_doc(), self.doc()
        if a is None:
            self.skipTest("baseline unavailable")

        def rows(s):
            out = {}
            for h in ("## 7. Producer obligations", "## 8. Consumer obligations",
                      "## 9. Shared read-surface and arbitration obligations"):
                body = s.split(h)[1].split("\n## ")[0]
                for l in body.splitlines():
                    if l.startswith("| **TN-"):
                        out[l.split("**")[1]] = l
            return out

        ra, rb = rows(a), rows(b)
        self.assertEqual(len(ra), 43)
        self.assertEqual(ra, rb)

        def cases(s):
            return {m.group(1): m.group(0)
                    for m in re.finditer(r"^\| \*\*(T-C05-\d+)\*\*.*$", s, re.M)}
        self.assertEqual(cases(a), cases(b))

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
# 6. Verdict and governance
# ---------------------------------------------------------------------------

class TestVerdict(Base):
    def test_verdict_is_pass_with_unrelated_limitations(self):
        self.assertIn("PASS WITH UNRELATED LIMITATIONS", self.raw)

    def test_review_requests_no_further_revision(self):
        self.assertIn("I request no further revision", self.flat)

    def test_limitations_are_classified_unrelated(self):
        flat = self.flat
        self.assertIn("L-1", flat)
        self.assertIn("pre-existing", flat)
        self.assertIn("unrelated to F-1/F-1b", flat)

    def test_zero_acceptance_cases_and_regressions_not_acceptance(self):
        self.assertIn("0 of 67 acceptance cases executed", self.flat)
        self.assertIn("tests of the checker, not acceptance evidence", self.flat)

    def test_no_governance_overreach(self):
        flat = self.flat
        for bad in ("C-05 is approved", "U-07 is closed", "a MEAD was selected",
                    "C-05 is frozen", "signature granted"):
            for m in re.finditer(re.escape(bad), flat):
                ctx = flat[max(0, m.start() - 70):m.start() + 30].lower()
                self.assertTrue(any(n in ctx for n in ("no ", "not ", "never", "open", "nothing ")),
                                "affirmative governance claim: %r" % ctx)

    def test_reviewed_files_not_modified_by_me(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--",
                            "docs/validation/dv_c05.py",
                            "docs/validation/test_dv_c05_regressions.py",
                            DOC_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_FINAL_VERIFY_C05_V1.md",
                  "AGENT2_FINAL_VERIFY_C05_V2.md",
                  "AGENT2_REVIEW_A1C05_S4_3_7_V1.md",
                  "AGENT2_REVIEW_A1C05_S4_3_6_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
