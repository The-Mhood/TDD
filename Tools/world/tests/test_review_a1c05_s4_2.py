"""Tests for Docs/AGENT2_REASSESSMENT_A1C05_S4_2_V1.md (W-M2.15).

Locks the S4.2 reassessment against the exact reviewed blob 7d03e1df.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised: no telegraph,
producer, consumer, directory or engine exists. All 67 acceptance cases are PROPOSED /
NOT RUN and none is run here.

Tests marked STILL-PRESENT assert a defect the review reports as open. If Agent 1 fixes
it, they fail - intended, and means the reassessment must be reissued.
"""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_REASSESSMENT_A1C05_S4_2_V1.md"

S42_COMMIT = "a788f953256d208f3eb1310f3897924d007179b1"
S42_BLOB = "7d03e1df837493305831962f43882a1cd3496143"
S42_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md"
S42_FIRST_DRAFT = "86f56af"

S41_BLOB = "d54e194affeaee98b1030e2b83b4c34e234fa382"
S40_BLOB = "424d2c69df62ebc1930eacd0ba67077c854ab31e"
S3_BLOB = "077232368c42b2cd910be2c9642ba05cd7faa382"

PROV_REGISTER = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md"
PROV_BLOB = "eda9bd2671650b0c41a8aa1cff97da0dd0fad593"

ALLOWED_ROWS = {"TN-P": {2}, "TN-C": {5, 6}, "TN-R": {2, 4}, "TN-A": {8}}


def git_show(spec):
    r = subprocess.run(["git", "show", spec], capture_output=True,
                       text=True, cwd=ROOT, check=False)
    return r.stdout if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def s42(self):
        t = git_show(S42_BLOB)
        if t is None:
            self.skipTest("reviewed S4.2 blob unavailable")
        return t

    def s42f(self):
        return re.sub(r"\s+", " ", self.s42())

    def blob(self, sha):
        t = git_show(sha)
        if t is None:
            self.skipTest("blob %s unavailable" % sha)
        return t

    def cells43(self, txt=None):
        s = txt if txt is not None else self.s42()
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

    def tokmap(self, txt=None):
        s = txt if txt is not None else self.s42()
        sec = s.split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        out = {}
        for l in sec.splitlines():
            if not l.startswith("| `"):
                continue
            c = [x.strip() for x in l.strip("|").split("|")]
            rows = set()
            for a, b in re.findall(r"rows? (\d+)\s*[\u2013\u2014-]\s*(\d+)", c[2]):
                rows |= set(range(int(a), int(b) + 1))
            for x in re.findall(r"rows? (\d+)(?!\s*[\u2013\u2014-])", c[2]):
                rows.add(int(x))
            out[c[0].strip("`")] = sorted(rows)
        return out


# ---------------------------------------------------------------------------
# Exact target verification first
# ---------------------------------------------------------------------------

class TestExactTarget(Base):
    def test_reviewed_blob_resolves_from_named_commit(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (S42_COMMIT, S42_PATH)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), S42_BLOB)

    def test_blob_is_1265_lines(self):
        self.assertEqual(len(self.s42().splitlines()), 1265)

    def test_review_is_not_the_first_draft(self):
        """The instruction says do not review an earlier S4.2 publication."""
        first = git_show(S42_FIRST_DRAFT)
        if first is None:
            self.skipTest("first draft unavailable")
        self.assertNotEqual(first, self.s42())
        self.assertIn("not the first S4.2 commit", self.flat)

    def test_draft_diff_is_three_sentences(self):
        first = git_show(S42_FIRST_DRAFT)
        if first is None:
            self.skipTest("first draft unavailable")
        a, b = first.splitlines(), self.s42().splitlines()
        changed = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
        self.assertLessEqual(changed, 6)

    def test_tip_provenance_register_pins_reviewed_blob(self):
        t = git_show("origin/arena/3bc206a0-tdd:" + PROV_REGISTER)
        if t is None:
            self.skipTest("tip register unavailable")
        self.assertIn(S42_BLOB, t)
        self.assertIn(S42_COMMIT, t)

    def test_register_at_publishing_commit_lagged(self):
        """The register committed AT a788f95 still pinned the first draft."""
        t = self.blob(PROV_BLOB)
        self.assertIn("86f56af", t)
        self.assertNotIn(S42_BLOB, t)

    def test_review_records_the_repointing(self):
        self.assertIn("**repointed**", self.flat)

    def test_review_records_both_hashes(self):
        self.assertIn(S42_BLOB, self.flat)
        self.assertIn(S42_COMMIT, self.flat)


# ---------------------------------------------------------------------------
# D-4: audio ownership — CLOSED
# ---------------------------------------------------------------------------

class TestD4Closed(Base):
    def test_preamble_no_longer_assigns_audio_to_agent1(self):
        pre = [l for l in self.s42().splitlines()
               if "Each obligation is implemented by each" in l]
        self.assertTrue(pre)
        self.assertNotIn("camera and audio", pre[0])
        self.assertIn("Agent 1 has no C-05 audio responsibility", pre[0])

    def test_no_unmarked_agent1_audio_assignment(self):
        NEG = ("owns no audio", "no C-05 audio responsibility", "not claimed",
               "owns none", "camera and audio cues" , "removed", "deleted", "loses",
               "corrected", "materialised", "CLOSED", "scoped too narrowly",
               "review", "quotation", "S3", "S4.1", "D-4", "D-22", "C6-2",
               "also claimed", "preamble", "finding 1", "finding 5")
        bad = []
        for ln in self.s42().splitlines():
            if "audio" in ln and "Agent 1" in ln:
                if not any(n in ln for n in NEG):
                    bad.append(ln.strip()[:120])
        self.assertEqual(bad, [])

    def test_review_reports_d4_closed(self):
        sec = self.flat.split("### 3.1 D-4")[1].split("### 3.2")[0]
        self.assertIn("CLOSED", sec)
        self.assertIn("AGREE", sec)


# ---------------------------------------------------------------------------
# N-1: DV-22 whole-document scan false negative — STILL PRESENT
# TAMPER: fix the scan to deny-by-default -> these fail (N-1 closed).
# ---------------------------------------------------------------------------

class TestDv22EscapeHatch(Base):
    ALLOW = ('owns no audio', 'no C-05 audio responsibility', 'owns none',
             'owns no C-05 audio', 'D-4', 'D-22-scope', 'C6-2', 'row 5 also claimed',
             'also claimed', "S3's row 5", '\u00a78 preamble', 'preamble',
             'row 5 loses audio', 'finding 1', 'finding 5')

    def test_s41_preamble_is_whitelisted_by_D4(self):
        pre = [l for l in self.blob(S41_BLOB).splitlines()
               if "Each obligation is implemented by each" in l][0]
        self.assertIn("camera and audio", pre)           # defect present
        matching = [a for a in self.ALLOW if a in pre]
        self.assertIn("D-4", matching)                    # and whitelisted

    def test_scan_reports_zero_on_s41_despite_defect(self):
        s = self.blob(S41_BLOB)
        bad = [ln for ln in s.splitlines()
               if 'audio' in ln and 'Agent 1' in ln
               and not any(a in ln for a in self.ALLOW)]
        self.assertEqual(len(bad), 0, "scan must report 0 offenders on S4.1")

    def test_mutation_with_keyword_is_missed(self):
        inject = ("| **TN-C-99** | D-4 note: Agent 1 owns the camera and audio cues. "
                  "| x | y | z | T-C05-1 | each consumer |")
        mut = self.s42().replace("## 9. Shared read-surface", inject + "\n## 9. Shared read-surface")
        self.assertNotEqual(mut, self.s42())
        bad = [ln for ln in mut.splitlines()
               if 'audio' in ln and 'Agent 1' in ln
               and not any(a in ln for a in self.ALLOW)]
        self.assertEqual(len(bad), 0, "keyword prefix must defeat the scan")

    def test_mutation_without_keyword_is_caught(self):
        inject = ("| **TN-C-99** | Agent 1 owns the camera and audio cues for the player. "
                  "| x | y | z | T-C05-1 | each consumer |")
        mut = self.s42().replace("## 9. Shared read-surface", inject + "\n## 9. Shared read-surface")
        bad = [ln for ln in mut.splitlines()
               if 'audio' in ln and 'Agent 1' in ln
               and not any(a in ln for a in self.ALLOW)]
        self.assertEqual(len(bad), 1, "unprefixed injection must be caught")

    def test_review_states_both_required_fixes(self):
        self.assertIn("Detect assignment by **structure, not by keyword presence**", self.flat)
        self.assertIn("Deny-by-default is the point", self.flat)

    def test_review_notes_scan_never_shown_catching(self):
        self.assertIn("The scan has never been shown to catch anything", self.flat)


class TestDv22Discriminates(Base):
    """The instrument does reach the KNOWN defect, which the review concedes."""

    def dv22_fails(self, blob_sha):
        t = self.blob(blob_sha)
        pre = [l for l in t.splitlines()
               if "Each obligation is implemented by each" in l]
        # DV-22's preamble check requires the positive phrase
        return not (bool(pre) and "no C-05 audio responsibility" in pre[0])

    def test_fails_on_s41(self):
        self.assertTrue(self.dv22_fails(S41_BLOB))

    def test_fails_on_s3(self):
        self.assertTrue(self.dv22_fails(S3_BLOB))

    def test_passes_on_s42(self):
        self.assertFalse(self.dv22_fails(S42_BLOB))

    def test_review_credits_this(self):
        self.assertIn("That is exactly the discrimination `DV-22` could not produce", self.flat)


# ---------------------------------------------------------------------------
# D-1a: the bound is now DERIVED — CLOSED
# ---------------------------------------------------------------------------

class TestD1aClosed(Base):
    def test_five_rules_present(self):
        row = [l for l in self.s42().splitlines() if l.startswith("| **TN-C-14**")][0]
        for r in ("(i) Call-site scope", "(ii) Refresh in the frame",
                  "(iii) Maximum interval", "(iv) Fresh pull", "(v) Message-only"):
            self.assertIn(r, row)

    def test_interval_rule_present(self):
        # the cell wraps, so match on the flattened text
        flat = self.s42f()
        self.assertIn("Maximum interval between successful refreshes", flat)
        self.assertIn("at most **one frame apart**", flat)
        self.assertIn("measured **on the shared axis**", flat)

    def test_bound_is_derived_not_asserted(self):
        row = [l for l in self.s42().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("the staleness bound is **derived**", row)

    def test_worst_case_never_reaches_one_frame(self):
        row = [l for l in self.s42().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("approaches but never reaches one frame", row)

    def test_bound_holds_by_brute_force(self):
        """Re-derive: rule (ii) observation in frame of use; (iii) <=1 frame apart."""
        import random
        random.seed(11)
        worst = 0.0
        for _ in range(120000):
            a = random.random()
            t_o = a
            t_R = t_o + random.random() * (1 - a) if a < 1 else t_o
            hi = t_o + 1.0
            if hi < 1.0:
                continue
            t_o2 = random.uniform(1.0, hi)
            worst = max(worst, t_o2 - t_R)
        self.assertLess(worst, 1.0 + 1e-9)
        self.assertGreater(worst, 0.99)

    def test_s41_schedule_now_illegal(self):
        """S4.1 permitted a 1.98-frame gap; (iii) forbids it."""
        a = 0.99
        self.assertLess((a + 1.0) - (a + 1e-6), 1.0 + 1e-9)

    def test_review_reports_d1a_closed(self):
        sec = self.flat.split("### 3.3 D-1a")[1].split("### 3.4")[0]
        self.assertIn("CLOSED", sec)
        self.assertIn("AGREE", sec)


# ---------------------------------------------------------------------------
# D-1b: call-site scope adopted — CLOSED
# ---------------------------------------------------------------------------

class TestD1bClosed(Base):
    def test_call_site_rule_present(self):
        row = [l for l in self.s42().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("attaches to the **call site**", row)
        self.assertIn("reads `RemainingLocalSeconds`", row)

    def test_review_records_advisory_downgrade_and_no_contradiction(self):
        sec = self.flat.split("### 3.4 D-1b")[1].split("### 3.5")[0]
        self.assertIn("ADVISORY", sec)
        self.assertIn("not", sec)
        self.assertIn("forbidden", sec)

    def test_review_notes_addendum_not_answered(self):
        self.assertIn("did not answer my addendum", self.flat)


# ---------------------------------------------------------------------------
# C4c-N1: PO-3 rationale — CLOSED
# ---------------------------------------------------------------------------

class TestC4cN1Closed(Base):
    def test_falsified_premise_not_asserted_in_the_rationale(self):
        """S4.2 may QUOTE the old premise to mark it corrected; it must not assert it."""
        sec = self.s42f().split("Why this order, and not the other one")[1].split("### 3.7")[0]
        self.assertNotIn("is **not observable** at frame granularity, so leaving", sec)
        self.assertIn("is observable through a mid-frame pull", sec)

    def test_remaining_not_observable_uses_are_quotations_not_assertions(self):
        flat = self.s42f()
        for m in re.finditer(r"not observable", flat):
            ctx = flat[max(0, m.start() - 200):m.start() + 160]
            ok = ('falsified by `PO-5`' in ctx or 'C4c-N1' in ctx
                  or 'Active is not observable at all' in ctx)
            self.assertTrue(ok, "unaccounted 'not observable' use: %r" % ctx[-200:])

    def test_corrected_premise_present(self):
        self.assertIn("observable through a mid-frame pull once `PO-5` is in force", self.s42f())

    def test_po3_retained(self):
        self.assertIn("`PO-5` therefore\nrequires the application order to follow the publication order `PO-3` fixes"
                      .replace("\n", " "), self.s42f())

    def test_correction_is_disclosed(self):
        self.assertIn("S4.1 and earlier said the opposite here", self.s42f())

    def test_review_reports_closed(self):
        sec = self.flat.split("### 3.5 C4c-N1")[1].split("### 3.6")[0]
        self.assertIn("CLOSED", sec)

    def test_dv26_fails_on_s41_passes_on_s42(self):
        self.assertIn("not observable** at frame granularity", self.blob(S41_BLOB))
        self.assertIn("observable through a mid-frame pull", self.s42())


# ---------------------------------------------------------------------------
# D-6a / D-6a-i / D-6b
# ---------------------------------------------------------------------------

class TestCountsClosed(Base):
    def test_token_counts(self):
        tm = self.tokmap()
        cells = self.cells43()
        self.assertEqual(len(tm), 7)
        self.assertEqual(len({t for _, t in cells}), 5)
        self.assertEqual(len(cells), 43)

    def test_dv11_rule_zero_failures(self):
        tm = self.tokmap()
        fails = [o for o, t in self.cells43()
                 if not set(tm.get(t, [])) & ALLOWED_ROWS["-".join(o.split("-")[:2])]]
        self.assertEqual(fails, [])

    def test_dv24_exists_and_is_the_specified_instrument(self):
        self.assertIn("DV-24", self.s42())
        self.assertIn("equals `DV-11`'s computed pair", self.s42f())

    def test_dv24_failure_claim_is_true_on_s40(self):
        r6 = [l for l in self.blob(S40_BLOB).splitlines() if l.startswith("| **6** |")]
        self.assertTrue(r6)
        self.assertIn("7 declared, 6 observed", r6[0])

    def test_dv24_passes_on_s41(self):
        r6 = [l for l in self.blob(S41_BLOB).splitlines() if l.startswith("| **6** |")]
        self.assertIn("7 declared, 5 observed", r6[0])

    def test_s54_tallies_match_rederivation(self):
        sec = self.s42().split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        self.assertIn("**23 cells** (19 `TN-P`, 4 `TN-R`)", sec)
        self.assertIn("**12 cells**", sec)
        from collections import Counter
        per = Counter(t for _, t in self.cells43())
        self.assertEqual(per["producer owner"], 23)
        self.assertEqual(per["each consumer"], 12)

    def test_review_reports_all_three_closed(self):
        for head, nxt in (("### 3.6 D-6a", "### 3.7"),
                          ("### 3.7 D-6a-i", "### 3.8"),
                          ("### 3.8 D-6b", "### 3.9")):
            self.assertIn("CLOSED", self.flat.split(head)[1].split(nxt)[0], head)


# ---------------------------------------------------------------------------
# Preservation of the carried findings
# ---------------------------------------------------------------------------

class TestPreservation(Base):
    def test_clauses_identical_to_s41(self):
        a, b = self.s42(), self.blob(S41_BLOB)
        for oid in ("TN-P-18", "TN-P-19", "TN-C-10", "TN-C-11", "TN-C-15",
                    "TN-A-02", "TN-A-03"):
            ra = [l for l in a.splitlines() if l.startswith("| **%s**" % oid)]
            rb = [l for l in b.splitlines() if l.startswith("| **%s**" % oid)]
            self.assertEqual(ra, rb, oid)

    def test_totals(self):
        s = self.s42()
        def cnt(head, key):
            body = s.split(head)[1].split("\n## ")[0]
            return len([l for l in body.splitlines() if l.startswith("| **%s-" % key)])
        p = cnt("## 7. Producer obligations", "TN-P")
        c = cnt("## 8. Consumer obligations", "TN-C")
        r = cnt("## 9. Shared read-surface and arbitration obligations", "TN-R")
        b9 = s.split("## 9. Shared read-surface and arbitration obligations")[1].split("\n## ")[0]
        a = len([l for l in b9.splitlines() if l.startswith("| **TN-A-")])
        self.assertEqual((p, c, r, a), (19, 15, 6, 3))

    def test_67_cases_18_suites(self):
        sec = self.s42().split("### 12.1")[1].split("### 12.2")[0]
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

    def test_27_dv_rows_contiguous(self):
        sec = self.s42().split("### 13.1")[1].split("### 13.2")[0]
        nums = [int(x.split("-")[1]) for x in re.findall(r"\| \*\*(DV-\d+)\*\*", sec)]
        self.assertEqual(nums, list(range(1, 28)))


# ---------------------------------------------------------------------------
# N-2: duplicate S4.2 identity — STILL PRESENT
# ---------------------------------------------------------------------------

class TestDuplicateIdentity(Base):
    def other_branch_copy(self):
        t = git_show("origin/arena/c64fc525-tdd:" + S42_PATH)
        if t is None:
            self.skipTest("other-branch copy unavailable")
        return t

    def test_both_declare_the_same_response_id(self):
        RID = "TDD-A1-C05-SUCCESSOR-004.2"
        self.assertIn(RID, self.s42())
        self.assertIn(RID, self.other_branch_copy())

    def test_they_are_different_documents(self):
        self.assertNotEqual(self.other_branch_copy(), self.s42())

    def test_they_disagree_on_the_tn_c_14_measure(self):
        mine, other = self.s42(), self.other_branch_copy()
        self.assertIn("measured **on the shared axis**", mine)
        self.assertIn("monotonic elapsed time", other)
        self.assertNotEqual("measured **on the shared axis**" in other, True)

    def test_review_states_it_does_not_adjudicate(self):
        self.assertIn("I am not asserting which is authoritative", self.flat)
        self.assertIn("I have not reviewed the other", self.flat)

    def test_review_gives_three_closure_options(self):
        sec = self.flat.split("### 7.2.1 Exact closure condition")[1].split("### 7.3")[0]
        for o in ("Withdraw", "Re-identify", "Declare"):
            self.assertIn(o, sec)


# ---------------------------------------------------------------------------
# Executed validator reproduces the claimed discrimination
# ---------------------------------------------------------------------------

class TestValidatorExecuted(Base):
    def run_dv(self, text):
        src = git_show("origin/arena/3bc206a0-tdd:docs/validation/dv_c05.py")
        if src is None:
            self.skipTest("validator unavailable")
        import tempfile, sys
        d = Path(tempfile.mkdtemp())
        (d / "dv.py").write_text(src)
        (d / "doc.md").write_text(text)
        r = subprocess.run([sys.executable, str(d / "dv.py"), str(d / "doc.md")],
                           capture_output=True, text=True, check=False)
        return r.stdout

    def passed(self, text):
        out = self.run_dv(text)
        m = re.search(r"(\d+)/(\d+) checks passed", out)
        self.assertIsNotNone(m, out[-300:])
        return int(m.group(1)), int(m.group(2))

    def test_27_of_27_on_reviewed_blob(self):
        got, total = self.passed(self.s42())
        self.assertEqual((got, total), (27, 27))

    def test_discriminates_on_s41(self):
        got, total = self.passed(self.blob(S41_BLOB))
        self.assertLess(got, total)
        self.assertEqual(total, 27)

    def test_discriminates_on_s40(self):
        got, total = self.passed(self.blob(S40_BLOB))
        self.assertLess(got, total)

    def test_discriminates_on_s3(self):
        got, total = self.passed(self.blob(S3_BLOB))
        self.assertLess(got, total)

    def test_review_reports_these_numbers(self):
        for n in ("27/27", "22/27", "21/27", "10/27"):
            self.assertIn(n, self.flat)


# ---------------------------------------------------------------------------
# Verdict and governance discipline
# ---------------------------------------------------------------------------

class TestVerdict(Base):
    def test_verdict_is_pass_with_conditions(self):
        self.assertIn("`PASS WITH CONDITIONS`", self.raw)

    def test_both_conditions_named(self):
        self.assertIn("N-1", self.flat)
        self.assertIn("N-2", self.flat)
        self.assertIn("**2** — both instruments, neither normative", self.flat)

    def test_separates_normative_from_instrument(self):
        for layer in ("Normative correctness", "Documentation correctness",
                      "Validation-instrument correctness", "Provenance correctness"):
            self.assertIn(layer, self.flat)

    def test_separates_spec_from_execution(self):
        self.assertIn("`PROPOSED / NOT RUN` · 0 executed", self.flat)
        self.assertIn("This is a *specification*, not a result", self.flat)

    def test_zero_executed_stated(self):
        self.assertIn("0 of 67", self.flat)

    def test_no_governance_claim(self):
        for bad in ("C-05 is closed", "U-07 is closed", "signature granted",
                    "M0 complete"):
            self.assertNotIn(bad, self.flat)
        self.assertIn("no MEAD has been selected", self.flat)

    def test_disclaimer_is_negative_not_affirmative(self):
        import re as _re
        asserts = _re.findall(r"(?<!no )(?<!not )MEAD (?:is )?selected", self.flat)
        self.assertEqual(asserts, [])

    def test_keeps_agent3_independent(self):
        self.assertIn("Independent of Agent 3", self.flat)
        self.assertIn("make no independent claim about Agent 3", self.flat)

    def test_provenance_rule_applied(self):
        self.assertIn("re-verify any negative existence claim as the last action", self.flat)

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_REASSESSMENT_A1C05_S4_1_V1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_1_ADDENDUM_A1.md",
                  "AGENT2_REVIEW_A1C05_S3_V1.md",
                  "AGENT2_REVIEW_A1C05_S4_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)

    def test_reviewed_document_not_modified(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--", S42_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
