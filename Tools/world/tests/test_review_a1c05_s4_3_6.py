"""Tests for Docs/AGENT2_REVIEW_A1C05_S4_3_6_V1.md (W-M2.17).

Locks the S4.3.6 instrument review against the exact reviewed commit 034d091.

DOCUMENT, ARITHMETIC and INSTRUMENT checks only. No contract behaviour is exercised:
no telegraph, producer, consumer or engine exists. All 67 acceptance cases are
PROPOSED / NOT RUN and none is run here. The 86 regression cases are tests of the
checker, not acceptance tests, and are not treated as such.

TestDvEscapes asserts three defects the review reports as OPEN (C-1). If Agent 1 fixes
them, those tests fail - intended: the review must then be reissued or C-1 reassessed.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_REVIEW_A1C05_S4_3_6_V1.md"

TARGET = "034d091e1abcb507fdba6df4a05318a15aa5d7a1"
DOC_BLOB = "e3a1fa85243a4749591363d4196bb5d65dad7c84"
REG_BLOB = "ce1ebc8d079f83aa594ef222ff71a108def1e8a6"
DV_BLOB = "840fed6730a5b2e18a5f717f98c6de273b9c8721"
SUITE_BLOB = "ee69f549a5c684c211a3dc15878c69c6dc32afe8"
DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md"

PRED_COMMIT = "baa31db3c631f0fc3e69a82b6d71207ad8061218"
PRED_BLOB = "a0b46f46c81e85cea5d04b940aaf9aee46c19deb"
PRED_DV_BLOB = "6927644fb2a684024b3acc722ede0f0b610fc7d9"

S42_BLOB = "7d03e1df837493305831962f43882a1cd3496143"
S42_DV_BLOB = "381be714954415ba2ef62c32888ed8597b6688f3"


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


# ---------------------------------------------------------------------------
# 1. Exact target and provenance
# ---------------------------------------------------------------------------

class TestExactTarget(Base):
    def test_document_blob_matches_stated(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, DOC_PATH)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), DOC_BLOB)

    def test_register_blob(self):
        r = subprocess.run(["git", "rev-parse",
                            "%s:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6_PROVENANCE.md" % TARGET],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), REG_BLOB)

    def test_instrument_blobs_match_register(self):
        for path, blob in (("docs/validation/dv_c05.py", DV_BLOB),
                           ("docs/validation/test_dv_c05_regressions.py", SUITE_BLOB)):
            r = subprocess.run(["git", "rev-parse", "%s:%s" % (TARGET, path)],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, path)

    def test_register_names_the_document_blob(self):
        t = git_show(REG_BLOB)
        if t is None:
            self.skipTest("register unavailable")
        self.assertIn(DOC_BLOB, t)
        self.assertIn(DV_BLOB, t)
        self.assertIn(SUITE_BLOB, t)

    def test_document_is_1931_lines(self):
        self.assertEqual(len(self.doc().splitlines()), 1931)

    def test_predecessor_unmodified_at_successor_commit(self):
        r = subprocess.run(["git", "rev-parse",
                            "%s:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md" % TARGET],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), PRED_BLOB)

    def test_predecessor_diff_across_range_is_empty(self):
        r = subprocess.run(["git", "diff", "--stat", PRED_COMMIT, TARGET, "--",
                            "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        self.assertEqual(r.stdout.strip(), "")

    def test_review_records_commit_and_blob(self):
        self.assertIn(DOC_BLOB, self.flat)
        self.assertIn(TARGET, self.flat)


# ---------------------------------------------------------------------------
# 2. Reproduction of reported results
# ---------------------------------------------------------------------------

class TestReproduction(Base):
    def run_dv(self, script_text, doc_text):
        d = Path(tempfile.mkdtemp())
        (d / "dv.py").write_text(script_text)
        (d / "doc.md").write_text(doc_text)
        r = subprocess.run([sys.executable, str(d / "dv.py"), str(d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        m = re.search(r"(\d+)/(\d+) checks passed", r.stdout)
        if not m:
            self.skipTest("validator produced no tally")
        fails = [l.split()[0] for l in r.stdout.splitlines()
                 if l.startswith("DV-") and " FAIL " in l]
        return int(m.group(1)), int(m.group(2)), fails

    def test_successor_scores_27_of_27(self):
        self.assertEqual(self.run_dv(self.validator(), self.doc())[:2], (27, 27))

    def test_s435_under_s436_checker_is_26_of_27_dv27_only(self):
        got, tot, fails = self.run_dv(self.validator(), git_show(PRED_BLOB))
        self.assertEqual((got, tot), (26, 27))
        self.assertEqual(fails, ["DV-27"])

    def test_s42_under_s436_checker_fails_dv22_dv24_dv27(self):
        got, tot, fails = self.run_dv(self.validator(), git_show(S42_BLOB))
        self.assertEqual((got, tot), (24, 27))
        self.assertEqual(fails, ["DV-22", "DV-24", "DV-27"])

    def test_s42_scored_27_of_27_under_its_own_validator(self):
        """The 24/27 is checker growth, not a defect in S4.2."""
        own = git_show(S42_DV_BLOB)
        if own is None:
            self.skipTest("S4.2 validator unavailable")
        self.assertEqual(self.run_dv(own, git_show(S42_BLOB))[:2], (27, 27))

    def test_s435_scored_27_of_27_under_its_own_validator(self):
        own = git_show(PRED_DV_BLOB)
        if own is None:
            self.skipTest("S4.3.5 validator unavailable")
        self.assertEqual(self.run_dv(own, git_show(PRED_BLOB))[:2], (27, 27))

    def test_suite_diff_removes_nothing(self):
        r = subprocess.run(["git", "diff", PRED_COMMIT, TARGET, "--",
                            "docs/validation/test_dv_c05_regressions.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        removed = [l for l in r.stdout.splitlines()
                   if l.startswith("-") and not l.startswith("---")]
        self.assertEqual(removed, [], "no existing case may be edited or removed")

    def test_nineteen_new_cases_contiguous(self):
        r = subprocess.run(["git", "diff", PRED_COMMIT, TARGET, "--",
                            "docs/validation/test_dv_c05_regressions.py"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commits unavailable")
        added = r.stdout
        ids = sorted({int(m) for m in re.findall(r"TD-(\d+)", added)})
        new = [i for i in ids if i >= 42]
        self.assertEqual(new, list(range(42, 61)))

    def test_review_states_the_numbers(self):
        for n in ("27/27", "86/86", "24/27", "26/27", "10/27"):
            self.assertIn(n, self.flat)


# ---------------------------------------------------------------------------
# 3. DV-22 published cases TD-42..TD-51
# ---------------------------------------------------------------------------

class TestDv22Published(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_path(TARGET, "docs/validation/dv_c05.py")
        doc = git_path(TARGET, DOC_PATH)
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc

    def dv22(self, sentence):
        mut = self._doc.replace(
            "## 9. Shared read-surface",
            "| X | %s | a | b | c | d | e |\n## 9. Shared read-surface" % sentence)
        self.assertNotEqual(mut, self._doc, "injection anchor missing")
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-22 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1], r.stdout

    def test_td42_contrastive_agent2_is_caught(self):
        self.assertEqual(self.dv22("Agent 1, unlike Agent 2, owns the audio cues.")[0], "FAIL")

    def test_td43_first_agent_synonym_is_caught(self):
        self.assertEqual(self.dv22("The first agent owns the audio cues.")[0], "FAIL")

    def test_td44_as_opposed_to(self):
        self.assertEqual(self.dv22("Agent 1, as opposed to Agent 2, owns the audio cues.")[0], "FAIL")

    def test_td45_rather_than(self):
        self.assertEqual(self.dv22("Agent 1 rather than Agent 2 owns the audio cues.")[0], "FAIL")

    def test_td46_but_not(self):
        self.assertEqual(self.dv22("Agent 1, but not Agent 2, owns the audio cues.")[0], "FAIL")

    def test_td47_foil_naming_agent1_leaves_agent2_subject(self):
        """The false positive the correction removes."""
        self.assertEqual(self.dv22("Agent 2, unlike Agent 1, owns the audio cues.")[0], "PASS")

    def test_td48_denial_with_foil(self):
        self.assertEqual(self.dv22("Agent 1, unlike Agent 2, owns no audio cues.")[0], "PASS")

    def test_td49_synonym_denial(self):
        self.assertEqual(self.dv22("The first agent has no C-05 audio responsibility.")[0], "PASS")

    def test_td50_object_negation(self):
        self.assertEqual(self.dv22("Agent 1 owns the camera, not the audio cues.")[0], "PASS")

    def test_td51_whereas_is_not_a_foil(self):
        self.assertEqual(
            self.dv22("Agent 2 selects the camera, whereas Agent 1 owns the audio cues.")[0], "FAIL")

    def test_whereas_departure_does_not_hide_a_denial(self):
        self.assertEqual(self.dv22("Agent 1 owns no audio cues, whereas Agent 2 owns the camera.")[0],
                         "PASS")

    def test_object_negation_does_not_hide_an_assignment(self):
        self.assertEqual(self.dv22("Agent 1 owns the audio cues, not the camera.")[0], "FAIL")


# ---------------------------------------------------------------------------
# 4. DV-22 escapes -- STILL OPEN (C-1)
# TAMPER: fix them -> these fail, and C-1 can be reassessed.
# ---------------------------------------------------------------------------

class TestDvEscapes(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_path(TARGET, "docs/validation/dv_c05.py")
        doc = git_path(TARGET, DOC_PATH)
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc

    def run_check(self, name, sentence, whole):
        mut = self._doc.replace(
            "## 9. Shared read-surface",
            "%s\n## 9. Shared read-surface" % whole.replace("{S}", sentence))
        self.assertNotEqual(mut, self._doc)
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith(name + " ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1], r.stdout

    def test_escape_A_synonym_possessive_is_MISSED(self):
        """FORWARD_OWNER's possessive pattern is still the literal 'agent 1's'."""
        v, out = self.run_check("DV-22", "The audio cues are the first agent's.",
                                "| X | {S} | a | b | c | d | e |")
        self.assertEqual(v, "PASS", "if FAIL, C-1 item 1 is closed - reassess")
        self.assertIn("27/27", out, "the whole document still scores clean")

    def test_escape_A_literal_form_IS_caught(self):
        """Control proving it is the synonym, not the possessive path, that fails."""
        v, _ = self.run_check("DV-22", "The audio cues are Agent 1's.",
                              "| X | {S} | a | b | c | d | e |")
        self.assertEqual(v, "FAIL")

    def test_escape_B_long_foil_window_is_MISSED(self):
        """FOIL_BEFORE is anchored within 32 chars, so a long foil is not seen."""
        s = ("Agent 1, unlike what the wargame community might generally assume "
             "about Agent 2, owns the audio cues.")
        v, out = self.run_check("DV-22", s, "| X | {S} | a | b | c | d | e |")
        self.assertEqual(v, "PASS", "if FAIL, C-1 item 2 is closed - reassess")
        self.assertIn("27/27", out)

    def test_escape_B_short_foil_IS_caught(self):
        v, _ = self.run_check("DV-22", "Agent 1, unlike Agent 2, owns the audio cues.",
                              "| X | {S} | a | b | c | d | e |")
        self.assertEqual(v, "FAIL")

    def test_escape_C_three_line_wrap_is_MISSED(self):
        """DV-24 joins only adjacent line pairs."""
        v, _ = self.run_check("DV-24", "", "6 declared\\nand then\\n5 observed")
        # injected as literal backslash-n so the mutation keeps physical lines
        mut = self._doc.replace("## 9. Shared read-surface",
                                "The tally reads 6 declared\nand then\n5 observed.\n"
                                "## 9. Shared read-surface")
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0]
        self.assertEqual(line.split()[1], "PASS", "if FAIL, C-1 item 3 is closed - reassess")

    def test_two_line_wrap_IS_caught(self):
        v, _ = self.run_check("DV-24", "", "6 declared\\n5 observed")
        mut = self._doc.replace("## 9. Shared read-surface",
                                "The tally reads 6 declared\n5 observed.\n"
                                "## 9. Shared read-surface")
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0]
        self.assertEqual(line.split()[1], "FAIL")

    def test_root_causes_are_the_lines_the_review_names(self):
        src = (self._d / "dv.py").read_text()
        # (a) the possessive branch of FORWARD_OWNER is still hard-coded to the literal
        self.assertIn("(?:is|are)\\s+agent[-\\s]?1", src)
        self.assertIn("FOIL_BEFORE = re.compile", src)
        # (b) the foil anchoring is a fixed-window match, not a structural one
        self.assertIn("FOIL_BEFORE.search(ln[max(0, m.start() - 32):m.start()])", src)
        # (c) DV-24 joins adjacent lines only
        self.assertIn("for i in range(len(lines) - 1):", src)

    def test_review_reports_all_three_escapes(self):
        self.assertIn("MAJOR-1", self.flat)
        self.assertIn("MAJOR-2", self.flat)
        self.assertIn("The audio cues are the first agent's.", self.flat)
        self.assertIn("The tally reads 6 declared", self.flat)


# ---------------------------------------------------------------------------
# 5. DV-24 published cases TD-52..TD-55
# ---------------------------------------------------------------------------

class TestDv24Published(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_path(TARGET, "docs/validation/dv_c05.py")
        doc = git_path(TARGET, DOC_PATH)
        if dv is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc

    def dv24(self, insert):
        mut = self._doc.replace("## 9. Shared read-surface",
                                "%s\n## 9. Shared read-surface" % insert)
        (self._d / "doc.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        return [x for x in r.stdout.splitlines() if x.startswith("DV-24 ")][0].split()[1]

    def test_td52_label_first_with_punctuation(self):
        self.assertEqual(self.dv24("For the record: declared: 6, observed: 5."), "FAIL")

    def test_td53_line_break(self):
        self.assertEqual(self.dv24("The tally reads 6 declared and\n5 observed."), "FAIL")

    def test_td54_sentence_split(self):
        self.assertEqual(self.dv24("The tally reads 6 declared. Then 5 observed."), "FAIL")

    def test_td55_correct_pairs_in_all_forms_pass(self):
        for s in ("If it helps: 7 declared and 5 observed.",
                  "If it helps: declared: 7, observed: 5.",
                  "If it helps: 7 declared. Then 5 observed.",
                  "If it helps: The tally reads 7 declared and\n5 observed."):
            self.assertEqual(self.dv24(s), "PASS", s)

    def test_number_words_and_reverse_order(self):
        self.assertEqual(self.dv24("declared: six, observed: five"), "FAIL")
        self.assertEqual(self.dv24("6 observed of 7 declared"), "FAIL")


# ---------------------------------------------------------------------------
# 6. DV-11 published cases TD-56..TD-60
# ---------------------------------------------------------------------------

class TestDv11Published(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_path(TARGET, "docs/validation/dv_c05.py")
        old = git_show(PRED_DV_BLOB)
        doc = git_path(TARGET, DOC_PATH)
        if dv is None or old is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        (cls._d / "old.py").write_text(old)
        cls._doc = doc

    def dv11(self, script, doc):
        (self._d / "doc.md").write_text(doc)
        r = subprocess.run([sys.executable, str(self._d / script), str(self._d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-11 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]

    def mutate(self, old, new):
        self.assertIn(old, self._doc)
        return self._doc.replace(old, new, 1)

    def test_td56_extra_row_pass_before_fail_after(self):
        m = self.mutate("| **row 2** (inside C-05: producer implementation) |",
                        "| **rows 2 and 3** |")
        self.assertEqual(self.dv11("old.py", m), "PASS")
        self.assertEqual(self.dv11("dv.py", m), "FAIL")

    def test_td57_disallowed_range_pass_before_fail_after(self):
        m = self.mutate("| **rows 5–6** | **12 cells**", "| **rows 5–8** | **12 cells**")
        self.assertEqual(self.dv11("old.py", m), "PASS")
        self.assertEqual(self.dv11("dv.py", m), "FAIL")

    def test_td58_falsified_cell_count_pass_before_fail_after(self):
        m = self.mutate("**23 cells** (19 `TN-P`, 4 `TN-R`)",
                        "**99 cells** (19 `TN-P`, 4 `TN-R`)")
        self.assertEqual(self.dv11("old.py", m), "PASS")
        self.assertEqual(self.dv11("dv.py", m), "FAIL")

    def test_td59_unchanged_table_passes(self):
        self.assertEqual(self.dv11("dv.py", self._doc), "PASS")

    def test_td60_wrong_owner_fails_before_and_after(self):
        m = self.mutate("| **row 6** (inside C-05: consumer integration) | **3 cells**",
                        "| **row 7** (outside C-05) | **3 cells**")
        self.assertEqual(self.dv11("old.py", m), "FAIL")
        self.assertEqual(self.dv11("dv.py", m), "FAIL")

    def test_subset_rule_present(self):
        self.assertIn("decl[tok] <= allowed[pref]", (self._d / "dv.py").read_text())

    def test_review_notes_td60_under_discriminates(self):
        self.assertIn("MINOR-2", self.flat)
        self.assertIn("does not isolate the subset rule", self.flat)


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
        self.assertEqual(len(a), 17)
        self.assertEqual(a, b)
        self.assertEqual(a["T-C05-63"], b["T-C05-63"])
        self.assertEqual(a["T-C05-64"], b["T-C05-64"])

    def test_section_8_preamble_clean(self):
        pre = [l for l in self.doc().splitlines()
               if "Each obligation is implemented by each" in l][0]
        self.assertNotIn("camera and audio", pre)
        self.assertIn("no C-05 audio responsibility", pre)

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
# 8. UNABLE TO VERIFY + governance boundaries
# ---------------------------------------------------------------------------

class TestBoundaries(Base):
    def test_agent3_named_qa_review_is_absent(self):
        """The one claim I must not accept on trust."""
        r = subprocess.run(["git", "ls-tree", "-r", "--name-only",
                            "origin/arena/c64fc525-tdd"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("Agent 3 branch unavailable")
        names = [f for f in r.stdout.splitlines() if "AGENT3" in f]
        self.assertTrue(names, "expected the three pre-S4.3 Agent 3 files to exist")
        joined = "\n".join(names)
        self.assertNotIn("S4_3_5", joined)
        self.assertNotIn("INTEGRATION_QA", joined)

    def test_agent3_s4_1_review_has_no_dv24(self):
        r = subprocess.run(["git", "show",
                            "origin/arena/c64fc525-tdd:docs/"
                            "AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("artifact unavailable")
        self.assertEqual(r.stdout.count("DV-24"), 0)

    def test_review_marks_agent3_items_unable_to_verify(self):
        self.assertIn("UNABLE TO VERIFY", self.flat)
        self.assertIn("does not exist in this repository", self.flat)

    def test_review_attributes_nothing_to_agent3(self):
        for bad in ("Agent 3's counterexample is", "Agent 3 demonstrated that",
                    "Agent 3 found that DV-24 misses"):
            self.assertNotIn(bad, self.flat)

    def test_verdict_is_pass_with_conditions(self):
        self.assertIn("`PASS WITH CONDITIONS`", self.raw)

    def test_condition_c1_names_three_items(self):
        self.assertIn("**C-1 (required) — `DV-22`.**", self.flat)
        self.assertIn("The audio cues are the first agent's.", self.flat)
        self.assertIn("The tally reads 6 declared", self.flat)

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
        self.assertIn("remains unresolved", self.flat)

    def test_target_not_modified_by_me(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--", DOC_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_2_V1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_1_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
