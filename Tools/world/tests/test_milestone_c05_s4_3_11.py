"""Tests for Docs/AGENT2_MILESTONE_C05_S4_3_11_V1.md (W-M2.22).

Pins the S4.3.11 implementation milestone (commit 06a4a8b) and its measured results:
27/27 document checks, 164/164 suite, 12/14 assessment probes, 26/26 required
controls, 17/17 independent edge cases, 0/67 acceptance cases executed.

ASSESSMENT / INSTRUMENT checks only. The 67 acceptance cases are PROPOSED / NOT RUN
and none is run here. The 164 suite cases are tests of a document checker, not
acceptance tests, and this module never runs them as if they were.

The milestone is a record of an instrument correction. It is NOT contract approval,
NOT MEAD completion and NOT closure of C-05; several tests here assert exactly that,
so a later editor cannot quietly upgrade the record.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "Docs" / "AGENT2_MILESTONE_C05_S4_3_11_V1.md"

TARGET = "06a4a8b"
PREDECESSOR = "7662926"
DOC_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md"
DOC_BLOB = "1929551681d6f6852076606384e22ad1424e266e"
DV_PATH = "docs/validation/dv_c05.py"
DV_BLOB = "9e88c5a44c09788646198cbd77c4259c82534efe"
SUITE_PATH = "docs/validation/test_dv_c05_regressions.py"
SUITE_BLOB = "ca0a4f902de74180fbf165013462a728130ddb07"

ACTIVE = "## 9. Shared read-surface and arbitration obligations"


def git_show(spec):
    r = subprocess.run(["git", "show", spec], capture_output=True,
                       text=True, cwd=ROOT, check=False)
    return r.stdout if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = DOC.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)


# ---------------------------------------------------------------------------
# 1. The artifact of record
# ---------------------------------------------------------------------------

class TestArtifact(Base):
    def test_identities_are_pinned(self):
        for spec, blob in ((f"{TARGET}:{DOC_PATH}", DOC_BLOB),
                           (f"{TARGET}:{DV_PATH}", DV_BLOB),
                           (f"{TARGET}:{SUITE_PATH}", SUITE_BLOB)):
            r = subprocess.run(["git", "rev-parse", spec],
                               capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), blob, spec)

    def test_predecessor_preserved(self):
        r = subprocess.run(["git", "cat-file", "-t", PREDECESSOR],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("predecessor unavailable")
        self.assertEqual(r.stdout.strip(), "commit")

    def test_record_states_measured_results(self):
        for figure in ("27/27", "164/164", "12/14", "26/26", "17/17", "0/67",
                       "0 of 67"):
            self.assertIn(figure, self.flat, figure)


# ---------------------------------------------------------------------------
# 2. Governance: the record may not overclaim
# ---------------------------------------------------------------------------

class TestNoOverclaim(Base):
    def test_disclaims_approval_mead_and_closure(self):
        self.assertIn("Not contract approval", self.flat)
        self.assertIn("Not MEAD completion", self.flat)
        self.assertIn("Not closure of C-05", self.flat)

    def test_governance_state_recorded(self):
        flat = self.flat
        for token in ("DESIGN_ONLY", "unsigned", "unfrozen", "U-07", "B-15"):
            self.assertIn(token, flat, token)

    def test_no_affirmative_closure_claim(self):
        for bad in ("C-05 is closed", "C-05 closed", "U-07 is closed",
                    "a MEAD was selected", "MEAD approved", "contract approved",
                    "C-05 is frozen", "signature granted"):
            for m in re.finditer(re.escape(bad), self.flat):
                ctx = self.flat[max(0, m.start() - 80):m.start() + 40].lower()
                self.assertTrue(any(n in ctx for n in ("not ", "no ", "never", "remain", "nothing")),
                                "affirmative claim: %r" % ctx)

    def test_zero_acceptance_cases_stated(self):
        self.assertIn("0 of 67", self.flat)


# ---------------------------------------------------------------------------
# 3. Instrument behaviour at 06a4a8b
# ---------------------------------------------------------------------------

class Instr(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dv = git_show(f"{TARGET}:{DV_PATH}")
        doc = git_show(f"{TARGET}:{DOC_PATH}")
        if dv is None or doc is None:
            raise unittest.SkipTest("artifact unavailable")
        import tempfile
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(dv)
        cls._doc = doc
        cls._src = dv

    def verdict(self, stmt):
        mut = self._doc.replace(
            ACTIVE, "| X | %s | a | b | c | d | e |\n%s" % (stmt, ACTIVE))
        self.assertNotEqual(mut, self._doc, "injection anchor missing")
        (self._d / "d.md").write_text(mut)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(self._d / "d.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [x for x in r.stdout.splitlines() if x.startswith("DV-22 ")]
        self.assertTrue(line, r.stdout[-300:])
        return line[0].split()[1]


class TestProbes(Instr):
    def test_7_closed(self):
        """D-a and D-b close seven of the nine bad probes."""
        for s in ("Agent 1 owns the camera, never the audio cues.",
                  "Agent 1 owns the camera, never any audio cues.",
                  "Agent 1 owns the camera never the audio cues."):
            self.assertEqual(self.verdict(s), "PASS", s)
        for s in ("The audio cues have been owned by Agent 1.",
                  "The audio cue, supplied by Agent 1, drives the mixer.",
                  "The audio cue supplied by Agent 1 drives the mixer.",
                  "The audio cue, provided by Agent 1, drives the mixer."):
            self.assertEqual(self.verdict(s), "FAIL", s)

    def test_2_deferred_unchanged(self):
        """D-c is deferred: these must STILL be missed. If they move, D-c was taken up."""
        for s in ("Agent 1, not Agent 2, owns the audio cues.",
                  "Agent 1, never Agent 2, owns the audio cues."):
            self.assertEqual(self.verdict(s), "PASS",
                             "D-c appears to have been implemented - update the record: %r" % s)

    def test_5_already_correct_unchanged(self):
        for s in ("Agent 1 may own the audio cues.",
                  "Agent 1 must own the audio cues.",
                  "Agent 1 has owned the audio cues.",
                  "Agent 1, unlike Agent 2, owns the audio cues.",
                  "The first agent owns the audio cues."):
            self.assertEqual(self.verdict(s), "FAIL", s)

    def test_12_of_14_tally(self):
        probes = [("PASS", "Agent 1 owns the camera, never the audio cues."),
                  ("PASS", "Agent 1 owns the camera, never any audio cues."),
                  ("PASS", "Agent 1 owns the camera never the audio cues."),
                  ("FAIL", "The audio cues have been owned by Agent 1."),
                  ("PASS", "Agent 1, not Agent 2, owns the audio cues."),
                  ("PASS", "Agent 1, never Agent 2, owns the audio cues."),
                  ("FAIL", "The audio cue, supplied by Agent 1, drives the mixer."),
                  ("FAIL", "The audio cue supplied by Agent 1 drives the mixer."),
                  ("FAIL", "The audio cue, provided by Agent 1, drives the mixer."),
                  ("FAIL", "Agent 1 may own the audio cues."),
                  ("FAIL", "Agent 1 must own the audio cues."),
                  ("FAIL", "Agent 1 has owned the audio cues."),
                  ("FAIL", "Agent 1, unlike Agent 2, owns the audio cues."),
                  ("FAIL", "The first agent owns the audio cues.")]
        # the required verdict for the two deferred probes is FAIL; they are still PASS
        deferred = {"Agent 1, not Agent 2, owns the audio cues.",
                    "Agent 1, never Agent 2, owns the audio cues."}
        correct = sum(1 for want, s in probes
                      if self.verdict(s) == want and s not in deferred)
        self.assertEqual(correct, 12, "expected 12/14")


class TestGuard(Instr):
    """The authorised deviation: D-b is hardened, not the literal optional copula."""

    def test_negated_passive_is_not_an_assignment(self):
        for s in ("Audio is not provided by Agent 1.",
                  "Audio is not owned by Agent 1.",
                  "Audio has never been owned by Agent 1.",
                  "Audio is not supplied by Agent 1.",
                  "Audio was never provided by Agent 1."):
            self.assertEqual(self.verdict(s), "PASS", s)

    def test_denial_side_reads_the_auxiliary_chain(self):
        for s in ("No audio cue has been owned by Agent 1.",
                  "None of the audio cues have been owned by Agent 1.",
                  "None of the audio cues have been provided by Agent 1.",
                  "None of the audio cues has been supplied by Agent 1."):
            self.assertEqual(self.verdict(s), "PASS", s)

    def test_positive_forms_still_caught(self):
        for s in ("The audio cues have been owned by Agent 1.",
                  "The audio cues had been owned by Agent 1.",
                  "The audio cues are owned by Agent 1."):
            self.assertEqual(self.verdict(s), "FAIL", s)

    def test_not_only_hazard_not_reopened(self):
        """This is what made C unsafe; it must still be caught."""
        for s in ("Not only does Agent 1 own the audio cues.",
                  "Not only does Agent 1 own the audio cues, but it also owns the camera."):
            self.assertEqual(self.verdict(s), "FAIL", s)


class TestExclusions(Instr):
    def test_c_unimplemented(self):
        m = re.search(r"_FOIL_ANY = re\.compile\(r'(.*?)', re\.I\)", self._src)
        self.assertIsNotNone(m)
        self.assertNotIn("never", m.group(1))
        self.assertNotIn("|not", m.group(1))

    def test_d_d_refused(self):
        m = re.search(r"_FO_PART = r'\(\?:([^)]*)\)'", self._src)
        self.assertIsNotNone(m)
        for verb in ("assigned", "managed", "controlled", "authored",
                     "approved", "commissioned", "mixed", "routed"):
            self.assertNotIn(verb, m.group(1), verb)

    def test_never_not_in_neg_after(self):
        m = re.search(r"NEG_AFTER = \((.*?)\n\)", self._src, re.S)
        self.assertIsNotNone(m)
        self.assertNotIn("never", m.group(1))


# ---------------------------------------------------------------------------
# 4. The outstanding documentation requirement
# ---------------------------------------------------------------------------

class TestL1(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        doc = git_show(f"{TARGET}:{DOC_PATH}")
        cls._doc = doc

    def test_section_13_1_row_carries_stale_tallies(self):
        if self._doc is None:
            self.skipTest("artifact unavailable")
        m = re.search(r"exempt lines (\d+) \(fenced (\d+), quoted table (\d+), "
                      r"marked block \d+\); live sections unexempted True; "
                      r"audio mentions evaluated (\d+)", self._doc)
        self.assertIsNotNone(m, "tally sentence not found")
        self.assertEqual(m.groups(), ("343", "201", "139", "146"),
                         "L-1 may have been corrected - re-measure and update the record")

    def test_record_marks_l1_open_not_closed(self):
        self.assertIn("L-1", self.flat)
        self.assertIn("recurs", self.flat)
        self.assertIn("OPEN", self.flat)

    def test_record_does_not_claim_l1_closed_by_construction(self):
        """The record must reject the claim, not repeat it as its own conclusion."""
        self.assertIn("The \"closed by construction\" argument requires the row to actually carry", self.flat)
        self.assertIn("`L-1` is NOT closed", self.flat)

    def test_record_states_l2_is_closed(self):
        self.assertIn("L-2", self.flat)


if __name__ == "__main__":
    unittest.main()
