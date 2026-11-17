"""Tests for Docs/AGENT2_REVIEW_A1_C05_3_V1.md (W-M2.9).

These lock the review's claims about Agent 1's C-05-3 response. They are DOCUMENT and
ARITHMETIC checks, not implementation acceptance tests: no telegraph, custodian, arbiter or
registry exists, and no test here exercises contract behaviour.

Two classes are deliberately fragile in one direction:

  TestBlockerPersistence asserts a phrase is ABSENT from the reviewed response. If a
  successor closes a gap, these FAIL. That is correct: the review's claim is about this
  blob, and a suite that kept passing against a later document would hide the closure.

Remote documents are fetched through git; if the ref is unavailable the test skips rather
than fails.
"""

import re
import subprocess
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[3] / "Docs" / "AGENT2_REVIEW_A1_C05_3_V1.md"

A1_HEAD = "22c29daddc3b7a9285ceb4709113d9657ddbe0bd"
A1_RESPONSE = "docs/AGENT1_C05_3_TELEGRAPH_AUTHORITY_RESPONSE_V1.md"
A1_RESPONSE_BLOB = "a94b49efb65c671c6c9fc8bb56436778aeb7030b"

A3_HEAD = "58ec7fd4bacbaaddf55f64e3e784de5c3fc8b0e6"
A3_REC = "docs/AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md"

A1R4_HEAD = "142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6"
A1R4_BLOB = "2cc548faf86cb9b30cd2e26386fc672edbdd9f75"
A1R4 = "docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md"

A1R3_HEAD = "70db9665b67723a526a6d40fa71ec832f1a95498"
A1R3 = "docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md"

MEADC_HEAD = "169a8d8f4f95dca526239dfbf744e97590504a70"
MEADC = "docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md"


def git_show(rev, path):
    """Return file text at rev:path, or None if unavailable."""
    try:
        r = subprocess.run(
            ["git", "show", f"{rev}:{path}"],
            capture_output=True, text=True, cwd=REVIEW.parents[1], check=False,
        )
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def git_rev(path_or_spec):
    r = subprocess.run(
        ["git", "rev-parse", path_or_spec],
        capture_output=True, text=True, cwd=REVIEW.parents[1], check=False,
    )
    return r.stdout.strip() if r.returncode == 0 else None


class ReviewText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        # flow: whitespace-normalised, for prose assertions spanning wrapped lines
        cls.flow = re.sub(r"\s+", " ", cls.raw)

    def response(self):
        t = git_show(A1_HEAD, A1_RESPONSE)
        if t is None:
            self.skipTest(f"{A1_RESPONSE} not available at {A1_HEAD[:8]}")
        return t

    def rec(self):
        t = git_show(A3_HEAD, A3_REC)
        if t is None:
            self.skipTest(f"{A3_REC} not available at {A3_HEAD[:8]}")
        return t

    def a1r4(self):
        t = git_show(A1R4_HEAD, A1R4)
        if t is None:
            self.skipTest("A1-R4 not available")
        return t

    def meadc(self):
        t = git_show(MEADC_HEAD, MEADC)
        if t is None:
            self.skipTest("MEAD-C not available")
        return t


class TestProvenance(ReviewText):
    """The review names exact commits and blobs; those must be real and correct."""

    def test_names_reviewed_response_commit(self):
        self.assertIn(A1_HEAD, self.raw)

    def test_names_reviewed_response_blob(self):
        self.assertIn(A1_RESPONSE_BLOB, self.raw)

    def test_a3_commit_named(self):
        self.assertIn(A3_HEAD, self.raw)

    def test_a1r4_blob_named(self):
        self.assertIn(A1R4_BLOB, self.raw)

    def test_response_blob_matches_actual(self):
        actual = git_rev(f"{A1_HEAD}:{A1_RESPONSE}")
        if actual is None:
            self.skipTest("cannot resolve response blob")
        self.assertEqual(actual, A1_RESPONSE_BLOB)
        self.assertIn(actual, self.raw)

    def test_a3_blob_is_real(self):
        actual = git_rev(f"{A3_HEAD}:{A3_REC}")
        if actual is None:
            self.skipTest("cannot resolve A3 blob")
        self.assertIn(actual, self.raw, "review must name A3's blob")

    def test_a1r4_blob_unchanged_on_branch(self):
        """A1 claims A1-R4 is unmodified; the review relies on it."""
        actual = git_rev(f"{A1_HEAD}:{A1R4}")
        if actual is None:
            self.skipTest("cannot resolve")
        self.assertEqual(actual, A1R4_BLOB)

    def test_meadc_blob_identity_claim(self):
        """Review §2.2: MEAD-C at the commit A1 cites equals the file on A1's branch.

        The claim is about A1's cited commit, not about A3's tree (MEAD-C is not present
        in A3's tree at all, so comparing against A3_HEAD was a bug in this test).
        """
        cited = git_rev(f"{MEADC_HEAD}:{MEADC}")
        onbranch = git_rev(f"{A1_HEAD}:{MEADC}")
        if cited is None or onbranch is None:
            self.skipTest("MEAD-C not resolvable")
        self.assertEqual(cited, onbranch)
        self.assertIn(cited, self.raw)

    def test_meadc_absent_from_a3_tree(self):
        """Records why the comparison above cannot use A3's head."""
        self.assertIsNone(git_rev(f"{A3_HEAD}:{MEADC}"),
                          "MEAD-C is expected to be absent from A3's tree")


class TestMyOwnErrorWithdrawn(ReviewText):
    """§0.3: the review withdraws its prior claim that A1-R4 miscited line 505."""

    def test_review_admits_the_error(self):
        self.assertIn("I was wrong", self.raw)
        self.assertIn("My review attributed to", self.flow)
        self.assertIn("Agent 1 a citation error Agent 1 did not make", self.flow)

    def test_a1r4_contains_no_505(self):
        """The load-bearing fact: A1-R4 says 506, not 505."""
        t = self.a1r4()
        self.assertEqual(t.count("505"), 0, "A1-R4 must contain no occurrence of 505")
        # build the needle so this file is not itself a counterexample
        self.assertIn("Locomotion.Cinematic` (506)", t)

    def test_root_cause_recorded(self):
        # the review states the failure class explicitly, not just the fact
        self.assertIn("Root cause, stated because the countermeasure should have prevented it",
                      self.flow)
        self.assertIn("a true fact about a source, mistaken for a fact about a document", self.flow)

    def test_prior_review_not_edited_claim(self):
        self.assertIn("not by rewriting it", self.flow)


class TestNecessityVerdict(ReviewText):
    """§1.1 and §3: NOT ESTABLISHED, with the reasoning present."""

    def test_verdict_present_at_the_verdict_heading(self):
        """The verdict must appear as the §1.1 heading form, not merely in prose.

        A bare `assertIn("NOT ESTABLISHED", raw)` is satisfied by any of the seven
        occurrences in this document, so it cannot detect the verdict being flipped.
        Anchor on the heading line.
        """
        self.assertIn("> ## NOT ESTABLISHED", self.raw)
        lines = [l for l in self.raw.splitlines() if l.startswith("> ## ")]
        self.assertIn("> ## NOT ESTABLISHED", lines)
        self.assertNotIn("> ## ESTABLISHED", lines)

    def test_all_three_verdict_headings(self):
        headings = [l.strip() for l in self.raw.splitlines() if l.startswith("> ## ")]
        self.assertEqual(headings,
                         ["> ## NOT ESTABLISHED",
                          "> ## AGREE WITH CONDITIONS",
                          "> ## NOT SUFFICIENT"])

    def test_r1_and_r2_distinguished(self):
        self.assertIn("**R1**", self.raw)
        self.assertIn("**R2**", self.raw)

    def test_m1_precedent_verified_against_m1(self):
        """Review §3.2 quotes M1 v1.4 796-797; check the lines exist as quoted."""
        m1 = git_show(A1_HEAD, "docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md")
        if m1 is None:
            self.skipTest("M1 not available")
        lines = m1.splitlines()
        self.assertIn("IsTelegraphingAttack", lines[795])       # line 796
        self.assertIn("GetAttackTelegraphRemaining", lines[796])  # line 797
        self.assertIn("IsTelegraphingAttack", self.raw)

    def test_no_acceptance_test_for_enumeration_claim(self):
        """Review §3.3 says 0 of A1's 8 suites exercises enumeration."""
        t = self.response()
        sec = t.split("### 10.2")[1].split("## 11")[0]
        names = re.findall(r"`TDD-Contract\.Combat\.(\w+)`", sec)
        self.assertEqual(len(names), 8)
        self.assertFalse(
            [n for n in names if "Enum" in n or "Aggregate" in n],
            "if an enumeration suite now exists, review §3.3 must be revisited",
        )


class TestConditionAudit(ReviewText):
    """§4: twelve conditions, six with no suite."""

    def test_twelve_conditions_exist_in_response(self):
        t = self.response()
        found = sorted(set(re.findall(r"\*\*C(\d+)\*\*", t)), key=int)
        self.assertEqual(found, [str(i) for i in range(1, 13)])

    def test_ten_accepted_claim(self):
        self.assertIn("Ten accepted", self.raw)

    def test_six_conditions_uncovered(self):
        """Verified in §4.4: C1, C2, C8, C10, C11, C12 have no suite row."""
        t = self.response()
        sec = t.split("### 10.2")[1].split("## 11")[0]
        rows = [l for l in sec.splitlines() if l.strip().startswith("| `TDD-Contract.Combat.")]
        covered = " ".join(rows)
        missing = [f"C{i}" for i in range(1, 13)
                   if not re.search(r"\bC%d\b" % i, covered)]
        self.assertEqual(missing, ["C1", "C2", "C8", "C10", "C11", "C12"])
        for c in missing:
            self.assertIn(c, self.raw)

    def test_four_p_obligations_covered(self):
        t = self.response()
        sec = t.split("### 10.2")[1].split("## 11")[0]
        covered = " ".join(l for l in sec.splitlines()
                           if l.strip().startswith("| `TDD-Contract.Combat."))
        named = [f"P{i}" for i in range(1, 13) if re.search(r"\bP%d\b" % i, covered)]
        self.assertEqual(named, ["P4", "P5", "P6", "P8"])

    def test_twelve_p_obligations_exist(self):
        t = self.response()
        found = sorted(set(re.findall(r"\*\*P(\d+)\*\*", t)), key=int)
        self.assertEqual(found, [str(i) for i in range(1, 13)])

    def test_thirty_cases_sum(self):
        t = self.response()
        sec = t.split("### 10.2")[1].split("## 11")[0]
        rows = [l for l in sec.splitlines() if l.strip().startswith("| `TDD-Contract.Combat.")]
        counts = [int(m.group(1)) for r in rows
                  if (m := re.search(r"\|\s*(\d+)\s*\|", r))]
        self.assertEqual(sum(counts), 30)
        self.assertEqual(len(counts), 8)


class TestBlockerPersistence(ReviewText):
    """§8's six blockers assert ABSENCE. Closing one must fail these tests."""

    def test_no_coalescing_prohibition_in_normative_clause(self):
        """§7.2: coalescing appears only in commentary and a test description."""
        t = self.response()
        hits = [l for l in t.splitlines()
                if re.search(r"coalesc", l, re.I)]
        # every hit must be commentary (§5.7) or a test-description row (§10.2)
        for h in hits:
            self.assertTrue(
                h.lstrip().startswith("-") or "TDD-Contract.Combat" in h or "§5.7" in h
                or "coalescing them would create" in h.lower(),
                "a normative clause now forbids coalescing -> update review §7.2: " + h[:120],
            )

    def test_named_ordering_point_never_named(self):
        """C8 requires a name; grep must find only the requirement."""
        t = self.response()
        for probe in ("TickGroup", "PrePhysics", "PostPhysics", "ETickingGroup"):
            self.assertNotIn(probe, t,
                             f"C8 may now name {probe} -> update review §8.5")

    def test_no_producer_resolution_rule(self):
        """§2.5: the per-instance query has no id->producer resolution."""
        t = self.response()
        self.assertIn("implemented by each producer", t)
        # the review's finding is that nothing resolves id -> producer object
        self.assertNotIn("ITDDTelegraphResolver", t)

    def test_dangling_section_reference_exists(self):
        """§8.2: 12 bare §3.4 references, and A1-R4 has no §3.4."""
        t = self.response()
        self.assertGreaterEqual(t.count("§3.4"), 8)
        a1r4 = self.a1r4()
        headings = [l for l in a1r4.splitlines() if l.startswith("###")]
        self.assertFalse([h for h in headings if h.startswith("### 3.4")],
                         "A1-R4 gained a §3.4 -> review §8.2 must be revisited")

    def test_a1r3_has_the_normative_parry_text(self):
        t = git_show(A1R3_HEAD, A1R3)
        if t is None:
            self.skipTest("A1-R3 not available")
        self.assertIn("### 3.4 Parry is same-frame phase overlap", t)

    def test_silent_eviction_still_claimed(self):
        t = self.response()
        self.assertIn("eviction emits no message", t)
        self.assertIn("aggregate query is the only way", re.sub(r"\s+", " ", t))

    def test_late_subscriber_collision_persists(self):
        """§8.1: P11 says a snapshot can report an unannounced phase; C5 says
        'without re-firing entry for a phase already held'. Both must still be present."""
        t = self.response()
        flat = re.sub(r"\s+", " ", t)
        self.assertIn("a snapshot never reports a phase that was never announced", flat)
        # the source bolds "**without**", so assert the two halves, not the bolded span
        self.assertIn("A snapshot establishes the consumer's current phase", flat)
        self.assertIn("firing entry for a phase already held", flat)

    def test_status_cinematic_provenance_conflict(self):
        """§8.6: A1-R4 routes Cinematic to the control state machine, not CombatState."""
        a1r4 = self.a1r4()
        flat = re.sub(r"\s+", " ", a1r4)
        self.assertIn("derive from the control state machine directly and never from", flat)
        t = self.response()
        self.assertIn("Status.Cinematic", t)


class TestMeadCNeutrality(ReviewText):
    """§2.1: C2 is MEAD-C-only because only MEAD-C has a TDDCore module."""

    def test_meadc_has_tddcore(self):
        m = self.meadc()
        self.assertIn("TDDCore", m)

    def test_meadc_citations_seven_exact(self):
        """§2.2: the seven MEAD-C lines A1 cites must read as A1 says."""
        m = self.meadc().splitlines()
        checks = {
            303: "UTDDEventBus",
            310: "UTDDCombatDirectorSubsystem",
            315: "UTDDPerformanceBudgetSubsystem",
            317: "State that dies with the world goes in a `WorldSubsystem`",
            321: "cannot accidentally hold a stale actor",
            599: "telegraph fairness",
            600: "FTDDAttackTokenPolicy",
        }
        for lineno, needle in checks.items():
            self.assertIn(needle, m[lineno - 1],
                          f"MEAD-C line {lineno} does not contain {needle!r}")

    def test_meadc_has_no_section_3_4_confusion(self):
        """Line 310 is the Director, 303 the bus, 315 the dev subsystem."""
        m = self.meadc().splitlines()
        self.assertIn("UGameInstanceSubsystem", m[302])
        self.assertIn("UWorldSubsystem", m[309])
        self.assertIn("(dev)", m[314])

    def test_review_states_no_mead_selected(self):
        self.assertIn("Not choosing a MEAD", self.raw)
        self.assertIn("I authored MEAD-A", self.raw)

    def test_mead_a_absent_from_repo_claim(self):
        """§2.1 claims MEAD-A has no TDDCore module. Check the local MEAD-A."""
        mead_a = REVIEW.parents[1] / "Docs" / "00_MASTER_ENGINEERING_ARCHITECTURE.md"
        if not mead_a.exists():
            self.skipTest("MEAD-A not present")
        t = mead_a.read_text(encoding="utf-8")
        self.assertNotIn("TDDCore", t)
        self.assertIn("TDDRuntime", t)


class TestSignatureDiscipline(ReviewText):
    """§1.4: no signature given or withdrawn."""

    def test_no_signature_added(self):
        self.assertIn("NOT SIGNED", self.raw)

    def test_no_bilateral_claim(self):
        flat = self.flow
        self.assertIn("None claimed", flat)
        self.assertNotIn("bilaterally agreed by both agents", flat)

    def test_u07_not_claimed_closed(self):
        self.assertIn("I do not claim either is closed", self.flow)
        self.assertIn("U-07", self.raw)
        self.assertIn("C-05", self.raw)

    def test_still_signed_only_on_a1r4_blob(self):
        """C-01/C-02/C-06 signatures were on 2cc548fa; this review must keep that scope."""
        self.assertIn("2cc548faf86cb9b30cd2e26386fc672edbdd9f75", self.raw)
        self.assertIn("Still signed on", self.raw)


class TestNoTestsClaimedRun(ReviewText):
    """§11.3: zero contract tests executed. The review must say so."""

    def test_zero_executed_stated(self):
        """Scope to the §11.3 row: a bare '**0**' also appears for MEAD grep counts."""
        row = [l for l in self.raw.splitlines()
               if l.startswith("| Contract acceptance tests")]
        self.assertEqual(len(row), 1, "the executed-count row must exist exactly once")
        self.assertIn("**0**", row[0])
        self.assertIn("executed** by me", row[0])

    def test_executed_count_not_inflated(self):
        """No row may claim a non-zero executed count."""
        for l in self.raw.splitlines():
            if l.startswith("| Contract acceptance tests") or \
               l.startswith("| Contract tests **written"):
                self.assertIn("**0**", l, "executed/written count must stay 0")

    def test_no_false_pass_claim(self):
        for bad in ("all tests pass", "tests passed successfully", "verified by execution"):
            self.assertNotIn(bad, self.raw.lower())

    def test_six_proposed_tests(self):
        for t in ("T1", "T2", "T3", "T4", "T5", "T6"):
            self.assertIn(f"**{t}**", self.raw)

    def test_proposed_tests_marked_not_run(self):
        self.assertIn("NOT RUN", self.raw)


class TestDeliverablesComplete(unittest.TestCase):
    """The task asked for three verdicts; all three must be present and distinct."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")

    def test_three_verdicts(self):
        self.assertIn("Is central custody necessary?", self.raw)
        self.assertIn("Is the proposed ownership boundary appropriate", self.raw)
        self.assertIn("Is the revised contract model sufficient", self.raw)

    def test_verdict_values(self):
        self.assertIn("NOT ESTABLISHED", self.raw)
        self.assertIn("AGREE WITH CONDITIONS", self.raw)
        self.assertIn("NOT SUFFICIENT", self.raw)

    def test_all_mandatory_sections_present(self):
        for n in range(1, 14):
            self.assertRegex(self.raw, rf"(?m)^## {n}\. ",
                             f"missing section {n}")

    def test_a2r_reassessment_table(self):
        for a in ("A2R-32", "A2R-33", "A2R-34", "A2R-35"):
            self.assertIn(a, self.raw)

    def test_restrictions_respected_statements(self):
        for phrase in ("Not editing Agent 1's documents",
                       "Not choosing a MEAD",
                       "Not claiming tests passed"):
            self.assertIn(phrase, self.raw)

    def test_root_cause_and_countermeasure(self):
        self.assertIn("0.4 The countermeasure, extended", self.raw)
        self.assertIn("git show", self.raw)


if __name__ == "__main__":
    unittest.main()
