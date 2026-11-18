"""Tests for Docs/AGENT2_ASSESS_C05_RESIDUAL_V1.md (W-M2.21).

Locks the C-05 residual-family assessment against Agent 1's S4.3.10, commit 7662926.

ASSESSMENT / INSTRUMENT checks only. No contract behaviour is exercised: no telegraph,
producer, consumer or engine exists. All 67 acceptance cases are PROPOSED / NOT RUN and
none is run here. The 147 regression cases are tests of the checker, not acceptance tests.

This module pins the four defects the assessment identifies, the three root sites, and
the safety result on which the recommendation rests: A+D closes seven of the nine bad
probes with zero collateral damage, while the obvious R-4 fix (adding not/never to
_FOIL_ANY) breaks TD-24 in isolation and nine required controls in combination.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_ASSESS_C05_RESIDUAL_V1.md"

TARGET = "7662926c4c3b7293daedcc393c0ec4d015cdd883"
DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md"
DOC_BLOB = "857778e18a35b35b1a5420905ec5f1482fddf868"
DV_BLOB = "353a2bff220d4daa4c176daafc941256098959ed"
SUITE_BLOB = "7ab55805c27a271706f16e9295f1f503dc5a6c94"

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


class Instr(Base):
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
        cls._src = dv

    def verdict(self, tool, stmt, src=None):
        p = self._d / "dv.py"
        if src is not None:
            (self._d / "v.py").write_text(src)
            p = self._d / "v.py"
        if tool == "DV-22":
            mut = self._doc.replace(ACTIVE,
                                    "| X | %s | a | b | c | d | e |\n%s" % (stmt, ACTIVE))
        else:
            mut = self._doc.replace(ACTIVE, "%s\n%s" % (stmt, ACTIVE))
        self.assertNotEqual(mut, self._doc, "injection anchor missing")
        (self._d / "d.md").write_text(mut)
        r = subprocess.run([sys.executable, str(p), str(self._d / "d.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith(tool + " ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]


# ---------------------------------------------------------------------------
# 1. The pinned artifact and the 14 reproduced probes
# ---------------------------------------------------------------------------

class TestPinnedAndReproduced(Instr):
    def test_identities(self):
        for spec, blob in (("%s:%s" % (TARGET, DOC_PATH), DOC_BLOB),
                           ("%s:docs/validation/dv_c05.py" % TARGET, DV_BLOB),
                           ("%s:docs/validation/test_dv_c05_regressions.py" % TARGET,
                            SUITE_BLOB)):
            r = subprocess.run(["git", "rev-parse", spec],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, spec)

    def test_six_fail_open(self):
        for s in ("The audio cues have been owned by Agent 1.",
                  "Agent 1, not Agent 2, owns the audio cues.",
                  "Agent 1, never Agent 2, owns the audio cues.",
                  "The audio cue, supplied by Agent 1, drives the mixer.",
                  "The audio cue supplied by Agent 1 drives the mixer.",
                  "The audio cue, provided by Agent 1, drives the mixer."):
            self.assertEqual(self.verdict("DV-22", s), "PASS",
                             "fail-open shape changed - reassess: %r" % s)

    def test_three_fail_closed(self):
        for s in ("Agent 1 owns the camera, never the audio cues.",
                  "Agent 1 owns the camera, never any audio cues.",
                  "Agent 1 owns the camera never the audio cues."):
            self.assertEqual(self.verdict("DV-22", s), "FAIL",
                             "fail-closed shape changed - reassess: %r" % s)

    def test_five_already_correct(self):
        for s in ("Agent 1 may own the audio cues.",
                  "Agent 1 must own the audio cues.",
                  "Agent 1 has owned the audio cues.",
                  "Agent 1, unlike Agent 2, owns the audio cues.",
                  "The first agent owns the audio cues."):
            self.assertEqual(self.verdict("DV-22", s), "FAIL", s)


# ---------------------------------------------------------------------------
# 2. The root sites the assessment names
# ---------------------------------------------------------------------------

class TestRootSites(Instr):
    def test_object_negation_takes_literal_not(self):
        self.assertIn(r"re.compile(r'\bnot\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),",
                      self._src,
                      "the object-negation negator set should still be closed at 'not'")

    def test_forward_owner_requires_a_simple_copula(self):
        self.assertIn(r"\b(?:is|are|was|were)\s+", self._src)
        self.assertIn(r"(?:owned|claimed|carried|held|supplied|provided|selected|chosen)\s+by\s+",
                      self._src)

    def test_foil_set_omits_not_and_never(self):
        m = re.search(r"_FOIL_ANY = re\.compile\(r'(.*?)', re\.I\)", self._src)
        self.assertIsNotNone(m)
        self.assertNotIn("never", m.group(1))
        self.assertIn("unlike", m.group(1))

    def test_r5b_has_no_commas(self):
        """The comma is NOT the mechanism: R-5b fails without any comma."""
        self.assertEqual("The audio cue supplied by Agent 1 drives the mixer.".count(","), 0)

    def test_copula_is_the_discriminator(self):
        """Adding only 'is' flips the same sentence from missed to caught."""
        a = self.verdict("DV-22", "The audio cue, supplied by Agent 1, drives the mixer.")
        b = self.verdict("DV-22", "The audio cue, is supplied by Agent 1, drives the mixer.")
        self.assertEqual((a, b), ("PASS", "FAIL"))


# ---------------------------------------------------------------------------
# 3. Four defects, three sites
# ---------------------------------------------------------------------------

class TestGrouping(Base):
    def test_assessment_states_four_defects(self):
        self.assertIn("four defects", self.flat.lower())

    def test_assessment_corrects_the_comma_hypothesis(self):
        """The request's hypothesis is falsified and the assessment says so."""
        self.assertIn("R-5b", self.flat)
        self.assertIn("no commas", self.flat.lower())

    def test_assessment_pairs_r3b_with_r5_not_r4(self):
        self.assertIn("R-3b` + `R-5", self.flat)

    def test_d_d_recorded_as_refused(self):
        self.assertIn("D-d", self.flat)
        self.assertIn("taxonomy expansion", self.flat.lower())


# ---------------------------------------------------------------------------
# 4. The safety result the recommendation rests on
# ---------------------------------------------------------------------------

OBJ_OLD = r"re.compile(r'\bnot\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),"
OBJ_NEW = r"re.compile(r'\b(?:not|never)\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),"
OWN_OLD = ("    re.compile(r'\\baudio\\b[^.;|]{0,40}?\\b(?:is|are|was|were)\\s+'\n"
           "               r'(?:owned|claimed|carried|held|supplied|provided|selected|chosen)\\s+by\\s+'")
OWN_NEW = ("    re.compile(r'\\baudio\\b[^.;|]{0,40}?\\b(?:(?:is|are|was|were)\\s+)?'\n"
           "           r'(?:owned|claimed|carried|held|supplied|provided|selected|chosen)\\s+by\\s+'")
FOIL_OLD = r"_FOIL_ANY = re.compile(r'\b(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\b', re.I)"
FOIL_NEW = (r"_FOIL_ANY = re.compile(r'\b(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not"
            r"|not|never)\b', re.I)")


class TestSafety(Instr):
    def test_fix_a_closes_r1_family_without_damage(self):
        src = self._src.replace(OBJ_OLD, OBJ_NEW)
        self.assertNotEqual(src, self._src, "A anchor missing")
        for s in ("Agent 1 owns the camera, never the audio cues.",
                  "Agent 1 owns the camera, never any audio cues.",
                  "Agent 1 owns the camera never the audio cues."):
            self.assertEqual(self.verdict("DV-22", s, src), "PASS", s)
        # and the legitimate object negations still hold
        for s in ("Agent 1 owns the camera, not the audio cues.",
                  "Agent 1 owns the camera, not any audio cues.",
                  "Agent 1 owns the camera, but not the audio cues."):
            self.assertEqual(self.verdict("DV-22", s, src), "PASS", s)

    def test_fix_d_closes_r3b_and_r5_without_damage(self):
        src = self._src.replace(OWN_OLD, OWN_NEW)
        self.assertNotEqual(src, self._src, "D anchor missing")
        for s in ("The audio cues have been owned by Agent 1.",
                  "The audio cue supplied by Agent 1 drives the mixer.",
                  "The audio cue, supplied by Agent 1, drives the mixer."):
            self.assertEqual(self.verdict("DV-22", s, src), "FAIL", s)
        # positive controls must keep failing, and denials keep passing
        for s in ("The audio cues are owned by Agent 1.", "Audio: Agent 1."):
            self.assertEqual(self.verdict("DV-22", s, src), "FAIL", s)
        self.assertEqual(self.verdict("DV-22", "No audio cue belongs to Agent 1.", src), "PASS")

    def test_a_plus_d_is_additive(self):
        src = self._src.replace(OBJ_OLD, OBJ_NEW).replace(OWN_OLD, OWN_NEW)
        self.assertEqual(self.verdict("DV-22", "Agent 1 owns the camera, never the audio cues.", src),
                         "PASS")
        self.assertEqual(self.verdict("DV-22", "The audio cues have been owned by Agent 1.", src),
                         "FAIL")
        # F-1b must not reopen
        self.assertEqual(self.verdict("DV-22",
                         "No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.",
                         src), "FAIL")

    def test_fix_c_alone_reopens_the_not_only_hazard(self):
        """The naive R-4 fix is refused because it buys one fail-open with another."""
        src = self._src.replace(FOIL_OLD, FOIL_NEW)
        self.assertNotEqual(src, self._src, "C anchor missing")
        probe = "Not only does Agent 1 own the audio cues."
        self.assertEqual(self.verdict("DV-22", probe), "FAIL")
        self.assertEqual(self.verdict("DV-22", probe, src), "PASS",
                         "the C fix should let a positive claim through")

    def test_fix_c_collapses_when_combined_with_d(self):
        """C alone survives; C+D breaks the denial controls. That is the trap."""
        src = self._src.replace(FOIL_OLD, FOIL_NEW).replace(OWN_OLD, OWN_NEW)
        self.assertNotEqual(src, self._src, "C+D anchor missing")
        self.assertEqual(self.verdict("DV-22", "Audio is not owned by Agent 1."), "PASS")
        self.assertEqual(self.verdict("DV-22", "Audio is not owned by Agent 1.", src), "FAIL")
        self.assertEqual(self.verdict("DV-22", "No audio cue belongs to Agent 1.", src), "FAIL")

    def test_assessment_reports_c_as_unsafe(self):
        self.assertIn("C+D", self.flat)
        self.assertIn("26/27", self.flat)
        self.assertIn("Not only", self.flat)

    def test_assessment_records_the_probe_tally(self):
        for n in ("5/14", "8/14", "9/14", "12/14"):
            self.assertIn(n, self.flat)


# ---------------------------------------------------------------------------
# 5. Recommendation and governance
# ---------------------------------------------------------------------------

class TestRecommendation(Base):
    def test_recommends_a_plus_d_now(self):
        self.assertIn("A+D", self.flat)
        self.assertIn("close now", self.flat.lower())

    def test_defers_r4(self):
        self.assertIn("defer", self.flat.lower())
        for p in ("R-4", "R-4b"):
            self.assertIn(p, self.flat)

    def test_f1b_not_reopened(self):
        self.assertIn("Does not reopen", self.flat)
        self.assertIn("CLOSED", self.flat)

    def test_no_contract_defect_claimed(self):
        self.assertIn("None is a contract defect", self.flat)

    def test_zero_acceptance_cases(self):
        self.assertIn("0 of 67", self.flat)

    def test_governance_unchanged(self):
        flat = self.flat
        for bad in ("C-05 is approved", "U-07 is closed", "a MEAD was selected",
                    "C-05 is frozen", "signature granted"):
            for m in re.finditer(re.escape(bad), flat):
                ctx = flat[max(0, m.start() - 70):m.start() + 30].lower()
                self.assertTrue(any(n in ctx for n in ("no ", "not ", "never", "open", "nothing ")),
                                "affirmative governance claim: %r" % ctx)

    def test_reviewed_files_not_modified(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--",
                            "docs/validation/dv_c05.py",
                            "docs/validation/test_dv_c05_regressions.py",
                            DOC_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
