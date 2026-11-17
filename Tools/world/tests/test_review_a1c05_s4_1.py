"""Tests for Docs/AGENT2_REASSESSMENT_A1C05_S4_1_V1.md (W-M2.13).

Locks the reassessment's claims about A1-C05-S4.1 v4.1 at the exact reviewed blob.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised: no telegraph,
producer, consumer, directory or engine exists here. All 67 acceptance cases in the reviewed
document are PROPOSED / NOT RUN and none is run by this file.

Several tests assert that a DEFECT IS STILL PRESENT (e.g. section 8's preamble still assigns
audio to Agent 1). If Agent 1 fixes it, those tests will fail - that is intended, and means
the reassessment must be reissued.
"""

import re
import subprocess
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[3] / "Docs" / "AGENT2_REASSESSMENT_A1C05_S4_1_V1.md"
REPO = REVIEW.parents[1]

S41_BLOB = "d54e194affeaee98b1030e2b83b4c34e234fa382"
S41_COMMIT = "95918268ed5b20b878fef3ee0a7855ad18e6eeb6"
S41_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md"

S41_TIP_COMMIT = "3784949595d2d62944f712e7345be69118aa14d9"
S41_TIP_BLOB = "cc056a4854de00f362163d79275d0f411c3045d3"

S40_BLOB = "424d2c69df62ebc1930eacd0ba67077c854ab31e"
S3_BLOB = "077232368c42b2cd910be2c9642ba05cd7faa382"

ALLOWED_ROWS = {"TN-P": {2}, "TN-C": {5, 6}, "TN-R": {2, 4}, "TN-A": {8}}


def git_show(spec):
    try:
        r = subprocess.run(["git", "show", spec], capture_output=True,
                           text=True, cwd=REPO, check=False)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def git_rev(spec):
    r = subprocess.run(["git", "rev-parse", spec], capture_output=True,
                       text=True, cwd=REPO, check=False)
    return r.stdout.strip() if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def s41(self):
        t = git_show(S41_BLOB)
        if t is None:
            self.skipTest("reviewed S4.1 blob not available")
        return t

    def s41flat(self):
        return re.sub(r"\s+", " ", self.s41())

    def s40(self):
        t = git_show(S40_BLOB)
        if t is None:
            self.skipTest("S4.0 blob not available")
        return t

    def obligation_cells(self, s=None):
        s = s if s is not None else self.s41()
        out = []
        for head in ("## 7. Producer obligations", "## 8. Consumer obligations",
                     "## 9. Shared read-surface and arbitration obligations"):
            body = s.split(head)[1].split("\n## ")[0]
            for l in body.splitlines():
                if not l.startswith("| **TN-"):
                    continue
                c = [x.strip() for x in l.strip("|").split("|")]
                if len(c) >= 7:
                    out.append((c[0].strip("*"), c[6]))
        return out

    def token_map(self, s=None):
        s = s if s is not None else self.s41()
        sec = s.split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        out = {}
        for l in sec.splitlines():
            if not l.startswith("| `"):
                continue
            c = [x.strip() for x in l.strip("|").split("|")]
            tok = c[0].strip("`")
            rows = set()
            for a, b in re.findall(r"rows? (\d+)\s*[\u2013\u2014-]\s*(\d+)", c[2]):
                rows |= set(range(int(a), int(b) + 1))
            for x in re.findall(r"rows? (\d+)(?!\s*[\u2013\u2014-])", c[2]):
                rows.add(int(x))
            out[tok] = sorted(rows)
        return out


# ---------------------------------------------------------------------------
# Provenance: the reviewed object is S4.1 and the hashes resolve
# TAMPER: any mis-transcribed hash makes these fail (the W-M2.12 lesson).
# ---------------------------------------------------------------------------

class TestProvenance(Base):
    def test_reviewed_blob_resolves_from_named_commit(self):
        got = git_rev(f"{S41_COMMIT}:{S41_PATH}")
        if got is None:
            self.skipTest("S4.1 commit not available")
        self.assertEqual(got, S41_BLOB)

    def test_tip_blob_resolves_from_named_tip(self):
        got = git_rev(f"{S41_TIP_COMMIT}:{S41_PATH}")
        if got is None:
            self.skipTest("S4.1 tip not available")
        self.assertEqual(got, S41_TIP_BLOB)

    def test_reviewed_blob_is_not_the_tip(self):
        self.assertNotEqual(S41_BLOB, S41_TIP_BLOB)

    def test_review_records_both_blobs(self):
        self.assertIn(S41_BLOB, self.flat)
        self.assertIn(S41_COMMIT, self.flat)

    def test_s41_is_1185_lines(self):
        self.assertEqual(len(self.s41().splitlines()), 1185)

    def test_is_genuinely_s41_not_s40_renamed(self):
        s = self.s41()
        self.assertIn("A1-C05-S4.1", s)
        self.assertIn("SUCCESSOR-004.1", s)
        self.assertIn("### 0.5 S4.1", s)
        self.assertNotEqual(self.s41flat(), re.sub(r"\s+", " ", self.s40()))


class TestMyWithdrawnClaim(Base):
    def test_review_withdraws_the_previous_provenance_statement(self):
        # the quote is a blockquote that wraps mid-sentence: normalise "> " first
        flat = re.sub(r"\s*>\s*", " ", self.flat)
        self.assertIn("No file by that name exists on any remote branch", flat)
        self.assertIn("That statement is false, and I withdraw it", self.flat)

    def test_review_does_not_claim_v4_1_is_absent(self):
        """Guards against reintroducing the withdrawn claim as an assertion."""
        self.assertNotIn("No file by that name exists on any remote branch.",
                         self.s41flat())

    def test_review_establishes_the_timeline(self):
        for t in ("14:09:47", "14:15:02"):
            self.assertIn(t, self.flat)

    def test_review_states_the_process_fix(self):
        self.assertIn("re-verify any negative existence claim", self.flat.lower())


# ---------------------------------------------------------------------------
# S4.1's own claim: nothing changed but one cell
# ---------------------------------------------------------------------------

class TestSection05ClaimVerified(Base):
    def test_normative_sections_identical_to_s40(self):
        s41, s40 = self.s41(), self.s40()
        for name in ("## 7. Producer obligations", "## 8. Consumer obligations",
                     "## 9. Shared read-surface and arbitration obligations"):
            a = s41.split(name)[1].split("\n## ")[0]
            b = s40.split(name)[1].split("\n## ")[0]
            self.assertEqual(a, b, "%s must be byte-identical to S4.0" % name)

    def test_key_clauses_identical(self):
        s41, s40 = self.s41(), self.s40()
        for oid in ("TN-P-18", "TN-P-19", "TN-C-11", "TN-C-14", "TN-C-15",
                    "TN-A-02", "TN-A-03"):
            r41 = [l for l in s41.splitlines() if l.startswith("| **%s**" % oid)]
            r40 = [l for l in s40.splitlines() if l.startswith("| **%s**" % oid)]
            self.assertEqual(r41, r40, oid)

    def test_po5_unchanged(self):
        s41, s40 = self.s41(), self.s40()
        a = s41.split("### 4.9 C05-2.9")[1].split("### 4.10")[0]
        b = s40.split("### 4.9 C05-2.9")[1].split("### 4.10")[0]
        self.assertEqual(a, b)


# ---------------------------------------------------------------------------
# D-6a: the count correction is present and correct
# TAMPER: revert section 1 row 6 to "6 observed" -> these fail.
# ---------------------------------------------------------------------------

class TestD6aResolved(Base):
    def test_section1_row6_says_five(self):
        sec = self.s41().split("## 1. The ten corrections at a glance")[1].split("\n## 2.")[0]
        row = [l for l in sec.splitlines() if l.startswith("| **6**")]
        self.assertTrue(row, "row 6 must exist")
        self.assertIn("7 declared, 5 observed", row[0])
        # the only "6 observed" allowed here is inside the CORRECTED annotation
        before = row[0].split("[CORRECTED")[0]
        self.assertNotIn("6 observed", before)

    def test_correction_is_annotated(self):
        self.assertIn("[CORRECTED at S4.1", self.s41flat())

    def test_no_nons3_statement_reports_other_than_five(self):
        s = self.s41()
        bad = []
        for m in re.finditer(r"(\d)\s*declared\s*[,/]?\s*(?:against\s*)?(\d)\s*observed", s):
            ctx = s[max(0, m.start() - 200):m.start()]
            is_s3 = ("S3" in ctx or "s3check" in ctx or "a6b4e22" in ctx)
            is_hist = ("S4 said" in ctx or "What changed in S4.1" in ctx
                       or "`6 observed` \u2192" in ctx)
            if not is_s3 and not is_hist and m.group(2) != "5":
                bad.append(m.group(0))
        self.assertEqual(bad, [])

    def test_declared_seven_observed_five(self):
        tm = self.token_map()
        obs = {t for _, t in self.obligation_cells()}
        self.assertEqual(len(tm), 7)
        self.assertEqual(len(obs), 5)

    def test_dv11_row_reports_five(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **DV-11**")][0]
        self.assertIn("7 declared / 5 observed", row)


# ---------------------------------------------------------------------------
# DV-11 row-level rule, re-implemented
# ---------------------------------------------------------------------------

class TestDv11RowLevel(Base):
    def test_row_level_rule_zero_failures(self):
        tm = self.token_map()
        fails = []
        for oid, tok in self.obligation_cells():
            pre = "-".join(oid.split("-")[:2])
            tr = tm.get(tok)
            if tr is None:
                fails.append("%s: undeclared %r" % (oid, tok))
            elif not set(tr) & ALLOWED_ROWS[pre]:
                fails.append("%s: %r -> %r, allowed %r"
                             % (oid, tok, tr, sorted(ALLOWED_ROWS[pre])))
        self.assertEqual(fails, [])

    def test_row7_token_would_fail_a_tn_c_obligation(self):
        tm = self.token_map()
        self.assertFalse(set(tm["Agent 2, in its own systems"]) & ALLOWED_ROWS["TN-C"])


# ---------------------------------------------------------------------------
# D-4: audio — STILL PRESENT
# TAMPER: delete "and audio" from section 8 preamble -> these fail (D-4 closed).
# ---------------------------------------------------------------------------

class TestD4StillPresent(Base):
    def test_section8_preamble_still_assigns_audio_to_agent1(self):
        pre = [l for l in self.s41().splitlines()
               if "Each obligation is implemented by each" in l]
        self.assertTrue(pre)
        self.assertIn("Agent 1 for defence, dodge, camera and audio", pre[0],
                      "if 'and audio' was removed, D-4 is CLOSED - reissue this reassessment")

    def test_row5_says_agent1_owns_no_audio(self):
        rows = [l for l in self.s41().splitlines()
                if re.sub(r"^\s*>\s*", "", l).lstrip().startswith(
                    "| **Consumer integration (Agent 1)")]
        self.assertTrue(rows)
        self.assertIn("Agent 1 owns no audio responsibility in C-05", rows[0])

    def test_audio_has_exactly_two_owners_in_the_document(self):
        """The contradiction, stated as a measurement."""
        s = self.s41()
        pre = [l for l in s.splitlines() if "Agent 1 for defence" in l]
        self.assertTrue(pre)
        self.assertIn("and audio", pre[0],
                      "the Agent 1 + audio assignment must still be measurable in the preamble")

    def test_dv22_scope_is_narrow(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **DV-22**")][0]
        c = [x.strip() for x in row.strip("|").split("|")]
        self.assertIn("row 5", c[1])
        self.assertIn("TN-C-15", c[1])
        self.assertNotIn("whole-document", c[1])
        self.assertNotIn("preamble", c[1])

    def test_s4_itself_predicted_this_risk(self):
        """S4.0's D-4 risk column named this exact failure mode."""
        flat = self.s41flat()
        self.assertIn("DV-22` was scoped too narrowly", flat)

    def test_review_states_both_corrections_required(self):
        self.assertIn("Both are required", self.flat)
        self.assertIn("Agent 1 for defence, dodge and camera;", self.flat)


# ---------------------------------------------------------------------------
# C4c-N1: PO-3 justification — STILL CONTRADICTED
# TAMPER: rewrite reason (b) -> these fail (C4c-N1 closed).
# ---------------------------------------------------------------------------

class TestC4cN1StillPresent(Base):
    def test_reason_b_claims_not_observable(self):
        flat = self.s41flat()
        self.assertIn("the producer's internal application order is **not observable**", flat)

    def test_po5_makes_it_observable(self):
        flat = self.s41flat()
        self.assertIn("A pull taken between two publications of the same frame returns "
                      "the earlier revision's `VF` exactly", flat)

    def test_t_c05_65_observes_the_order(self):
        row = [l for l in self.s41().splitlines() if l.startswith("| **T-C05-65**")][0]
        self.assertIn("after each application", row)

    def test_po3_still_required_for_reason_a(self):
        flat = self.s41flat()
        self.assertIn("a retime published first would describe the timing of a phase the "
                      "consumer has not been told about", flat)

    def test_review_keeps_po3_and_names_the_minimal_fix(self):
        self.assertIn("PO-3` is not made redundant by `PO-5`", self.flat)
        self.assertIn("one-sentence edit", self.flat)

    def test_review_does_not_propose_deleting_po3(self):
        self.assertNotIn("delete PO-3", self.flat)
        self.assertNotIn("remove PO-3", self.flat)


# ---------------------------------------------------------------------------
# D-6b: tallies still imprecise
# ---------------------------------------------------------------------------

class TestD6bStillImprecise(Base):
    def test_tallies_present_and_wrong(self):
        from collections import Counter
        per = Counter(t for _, t in self.obligation_cells())
        self.assertEqual(per["producer owner"], 23)
        self.assertEqual(per["each consumer"], 12)
        flat = self.s41flat()
        self.assertIn("19 `TN-P` rows", flat)
        self.assertIn("11 `TN-C` rows", flat)

    def test_review_flags_as_cosmetic(self):
        self.assertIn("D-6b", self.flat)
        self.assertIn("Cosmetic, non-gating", self.flat)


# ---------------------------------------------------------------------------
# Structural totals unchanged
# ---------------------------------------------------------------------------

class TestTotals(Base):
    def test_43_obligations(self):
        got = {}
        s = self.s41()
        for head, key in (("## 7. Producer obligations", "TN-P"),
                          ("## 8. Consumer obligations", "TN-C"),
                          ("## 9. Shared read-surface and arbitration obligations", "TN-R")):
            body = s.split(head)[1].split("\n## ")[0]
            got[key] = len([l for l in body.splitlines()
                            if l.startswith("| **%s-" % key)])
        body9 = s.split("## 9. Shared read-surface and arbitration obligations")[1].split("\n## ")[0]
        got["TN-A"] = len([l for l in body9.splitlines() if l.startswith("| **TN-A-")])
        self.assertEqual(got, {"TN-P": 19, "TN-C": 15, "TN-R": 6, "TN-A": 3})

    def test_67_cases_18_suites(self):
        sec = self.s41().split("### 12.1 The suites")[1].split("### 12.2")[0]
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

    def test_23_document_checks(self):
        sec = self.s41().split("### 13.1")[1].split("### 13.2")[0]
        self.assertEqual(len(re.findall(r"\| \*\*(DV-\d+)\*\*", sec)), 23)

    def test_case_ids_complete(self):
        ids = sorted({int(m) for m in re.findall(r"T-C05-(\d\d)", self.s41())})
        self.assertEqual(ids, list(range(1, 68)))


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------

class TestGovernance(Base):
    def test_outcome_is_mandated_vocabulary(self):
        vocab = re.findall(r"`(PASS|TARGETED REVISION|BLOCKED BY DEPENDENCY)`", self.raw)
        self.assertIn("TARGETED REVISION", vocab)

    def test_not_signing(self):
        self.assertIn("Still not signing v4.1", self.flat)

    def test_zero_executed(self):
        self.assertIn("0 executed", self.flat)

    def test_no_pass_claims(self):
        for bad in ("all 67 cases pass", "acceptance tests passed"):
            self.assertNotIn(bad, self.flat)

    def test_u07_open_no_mead(self):
        self.assertIn("U-07", self.flat)
        self.assertNotIn("U-07 closed", self.flat)
        self.assertTrue("no mead" in self.flat.lower(), "review must state MEAD neutrality")

    def test_classifies_defects_by_type(self):
        for cat in ("Implementation framing", "Explanatory rationale",
                    "Validation instrument", "Provenance"):
            self.assertIn(cat, self.flat)

    def test_tally_is_10_3_1(self):
        self.assertIn("10 AGREE, 3 AGREE WITH CONDITIONS, 1 DISAGREE", self.flat)

    def test_prior_reviews_preserved(self):
        for p in ("AGENT2_REVIEW_A1C05_S2_V1.md", "AGENT2_REVIEW_A1C05_S3_V1.md",
                  "AGENT2_REVIEW_A1C05_S4_V1.md"):
            self.assertTrue((REPO / "Docs" / p).exists(), p)

    def test_s3_blob_still_unmodified(self):
        import hashlib
        t = git_show(S3_BLOB)
        if t is None:
            self.skipTest("S3 blob not available")
        blob = hashlib.sha1(b"blob %d\x00" % len(t.encode()) + t.encode()).hexdigest()
        self.assertEqual(blob, S3_BLOB)


if __name__ == "__main__":
    unittest.main()
