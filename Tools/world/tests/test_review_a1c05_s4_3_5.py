"""Tests for Docs/AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md (W-M2.16).

Locks the S4.3.5 architecture review against the exact reviewed blob a0b46f46.

DOCUMENT, ARITHMETIC and INSTRUMENT checks only. No contract behaviour is exercised:
no telegraph, producer, consumer, directory or engine exists. All 67 acceptance cases
are PROPOSED / NOT RUN and none is run here.

TestDv22AttributionEscapes asserts a defect the review reports as OPEN (MAJOR-1). If
Agent 1 fixes the predicate, those tests fail - intended, and means the review must be
reissued or its condition re-assessed.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "Docs" / "AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md"

S435_COMMIT = "baa31db3c631f0fc3e69a82b6d71207ad8061218"
S435_BLOB = "a0b46f46c81e85cea5d04b940aaf9aee46c19deb"
S435_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md"
PROV_BLOB = "0dba4a7c6eddd3ba0a3d61b408c2d3ee005a88cb"

S434_BLOB = "41df692d3d80aa967c0f80326a47582957fa8eca"
S42_BLOB = "7d03e1df837493305831962f43882a1cd3496143"
S41_BLOB = "d54e194affeaee98b1030e2b83b4c34e234fa382"
S40_BLOB = "424d2c69df62ebc1930eacd0ba67077c854ab31e"
S3_BLOB = "077232368c42b2cd910be2c9642ba05cd7faa382"

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

    def s435(self):
        t = git_show(S435_BLOB)
        if t is None:
            self.skipTest("reviewed blob unavailable")
        return t

    def blob(self, sha):
        t = git_show(sha)
        if t is None:
            self.skipTest("blob %s unavailable" % sha)
        return t

    # ---- shared parsers -------------------------------------------------
    def cells43(self, txt=None):
        s = txt if txt is not None else self.s435()
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

    def rows(self, txt=None):
        s = txt if txt is not None else self.s435()
        out = {}
        for head in ("## 7. Producer obligations", "## 8. Consumer obligations",
                     "## 9. Shared read-surface and arbitration obligations"):
            body = s.split(head)[1].split("\n## ")[0]
            for l in body.splitlines():
                if l.startswith("| **TN-"):
                    out[l.split("**")[1]] = l
        return out

    def tokmap(self, txt=None):
        s = txt if txt is not None else self.s435()
        sec = s.split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        out = {}
        for l in sec.splitlines():
            if not l.startswith("| `"):
                continue
            c = [x.strip() for x in l.strip("|").split("|")]
            rs = set()
            for a, b in re.findall(r"rows? (\d+)\s*[\u2013\u2014-]\s*(\d+)", c[2]):
                rs |= set(range(int(a), int(b) + 1))
            for x in re.findall(r"rows? (\d+)(?!\s*[\u2013\u2014-])", c[2]):
                rs.add(int(x))
            out[c[0].strip("`")] = sorted(rs)
        return out


# ---------------------------------------------------------------------------
# 1. Exact target
# ---------------------------------------------------------------------------

class TestExactTarget(Base):
    def test_reviewed_blob_resolves_from_named_commit(self):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (S435_COMMIT, S435_PATH)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), S435_BLOB)

    def test_document_is_1779_lines(self):
        self.assertEqual(len(self.s435().splitlines()), 1779)

    def test_provenance_blob_at_same_commit(self):
        r = subprocess.run(["git", "rev-parse",
                            "%s:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5_PROVENANCE.md"
                            % S435_COMMIT],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("commit unavailable")
        self.assertEqual(r.stdout.strip(), PROV_BLOB)

    def test_provenance_names_the_reviewed_blob(self):
        t = self.blob(PROV_BLOB)
        self.assertIn(S435_BLOB, t)
        self.assertIn("1,779", t)

    def test_provenance_claims_same_commit_publication(self):
        t = self.blob(PROV_BLOB)
        self.assertIn("committed in the same commit", t)
        self.assertIn("git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md", t)

    def test_register_and_document_share_a_commit(self):
        """The register must live in the same commit as the text it pins."""
        for path, sha in (
            ("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md", S435_BLOB),
            ("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5_PROVENANCE.md", PROV_BLOB),
        ):
            r = subprocess.run(
                ["git", "rev-parse", "%s:%s" % (S435_COMMIT, path)],
                capture_output=True, text=True, cwd=ROOT, check=False)
            if r.returncode != 0:
                self.skipTest("commit unavailable")
            self.assertEqual(r.stdout.strip(), sha, path)

    def test_review_records_commit_and_blob(self):
        self.assertIn(S435_BLOB, self.flat)
        self.assertIn(S435_COMMIT, self.flat)

    def test_review_states_it_is_not_a_working_tree_copy(self):
        self.assertIn("not a working-tree copy", self.flat)


# ---------------------------------------------------------------------------
# 2. S4.3.5's own three-change claim, verified against S4.3.4
# TAMPER: if a normative clause changed, these fail.
# ---------------------------------------------------------------------------

class TestThreeChangeClaim(Base):
    def test_all_43_obligation_rows_identical_to_s434(self):
        a, b = self.rows(), self.rows(self.blob(S434_BLOB))
        self.assertEqual(len(a), 43)
        self.assertEqual(a, b)

    def test_key_clauses_identical_to_s434(self):
        a, b = self.s435(), self.blob(S434_BLOB)
        for name in ("### 5.2", "### 5.4", "### 9.2", "### 4.9", "### 3.6", "### 4.2"):
            self.assertEqual(a.split(name)[1].split("\n### ")[0],
                             b.split(name)[1].split("\n### ")[0], name)

    def test_case_specifications_identical(self):
        def cases(s):
            return {m.group(1): m.group(0)
                    for m in re.finditer(r"^\| \*\*(T-C05-\d+)\*\*.*$", s, re.M)}
        self.assertEqual(cases(self.s435()), cases(self.blob(S434_BLOB)))

    def test_review_reports_the_verification(self):
        self.assertIn("all 43 obligation rows", self.flat)


# ---------------------------------------------------------------------------
# 3. Structural totals
# ---------------------------------------------------------------------------

class TestStructure(Base):
    def test_43_obligations_split(self):
        s = self.s435()
        def cnt(h, k):
            body = s.split(h)[1].split("\n## ")[0]
            return len([l for l in body.splitlines() if l.startswith("| **%s-" % k)])
        b9 = s.split("## 9. Shared read-surface and arbitration obligations")[1].split("\n## ")[0]
        got = (cnt("## 7. Producer obligations", "TN-P"),
               cnt("## 8. Consumer obligations", "TN-C"),
               cnt("## 9. Shared read-surface and arbitration obligations", "TN-R"),
               len([l for l in b9.splitlines() if l.startswith("| **TN-A-")]))
        self.assertEqual(got, (19, 15, 6, 3))

    def test_67_cases_18_suites(self):
        sec = self.s435().split("### 12.1")[1].split("### 12.2")[0]
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
        sec = self.s435().split("### 13.1")[1].split("### 13.2")[0]
        nums = [int(x.split("-")[1]) for x in re.findall(r"\| \*\*(DV-\d+)\*\*", sec)]
        self.assertEqual(nums, list(range(1, 28)))

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


# ---------------------------------------------------------------------------
# 4. D-1..D-7 and conditions -- preserved and closed
# ---------------------------------------------------------------------------

class TestCarriedFindings(Base):
    def test_clauses_identical_to_s42(self):
        a, b = self.s435(), self.blob(S42_BLOB)
        for oid in ("TN-P-18", "TN-P-19", "TN-C-10", "TN-C-11", "TN-C-14",
                    "TN-C-15", "TN-A-02", "TN-A-03"):
            ra = [l for l in a.splitlines() if l.startswith("| **%s**" % oid)]
            rb = [l for l in b.splitlines() if l.startswith("| **%s**" % oid)]
            self.assertEqual(ra, rb, oid)

    def test_d4_audio_preamble_clean(self):
        pre = [l for l in self.s435().splitlines()
               if "Each obligation is implemented by each" in l][0]
        self.assertNotIn("camera and audio", pre)
        self.assertIn("no C-05 audio responsibility", pre)

    def test_d1a_bound_still_derived_on_shared_axis(self):
        row = [l for l in self.s435().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("shared axis", row)
        self.assertIn("Minimum" if False else "one frame apart", row)

    def test_c4cn1_no_live_assertion_of_falsified_premise(self):
        flat = re.sub(r"\s+", " ", self.s435())
        for m in re.finditer(r"not observable", flat):
            ctx = flat[max(0, m.start() - 240):m.start() + 160]
            ok = ("falsified by `PO-5`" in ctx or "C4c-N1" in ctx
                  or "Active is not observable at all" in ctx)
            self.assertTrue(ok, "unaccounted 'not observable': %r" % ctx[-180:])

    def test_d3_identity_consistent(self):
        s = self.s435()
        self.assertGreaterEqual(s.count("fixed for the instance's lifetime"), 2)
        self.assertIn("T-C05-66", s)

    def test_review_reports_all_seven_closed(self):
        for d in ("D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7"):
            self.assertIn(d, self.flat)
        self.assertIn("7 defects CLOSED", self.flat)


# ---------------------------------------------------------------------------
# 5. MAJOR-1: DV-22 attribution false negatives -- STILL OPEN
# TAMPER: fix the predicate -> these fail (MAJOR-1 closed).
# ---------------------------------------------------------------------------

class TestDv22AttributionEscapes(Base):
    """Runs the REAL shipped validator on mutated copies of the reviewed blob."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        src = git_show("%s:docs/validation/dv_c05.py" % S435_COMMIT)
        doc = git_show(S435_BLOB)
        if src is None or doc is None:
            raise unittest.SkipTest("validator or document unavailable")
        cls._d = Path(tempfile.mkdtemp())
        cls._dv = cls._d / "dv.py"
        cls._dv.write_text(src)
        cls._doc = doc

    def dv22(self, text):
        p = self._d / "doc.md"
        p.write_text(text)
        r = subprocess.run([sys.executable, str(self._dv), str(p)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [l for l in r.stdout.splitlines() if l.startswith("DV-22 ")]
        self.assertTrue(line, r.stdout[-400:] + r.stderr[-400:])
        return line[0].split()[1], r.stdout

    def inject(self, sentence):
        return self._doc.replace("## 9. Shared read-surface",
                                 "| X | %s | a | b | c | d | e |\n## 9. Shared read-surface"
                                 % sentence)

    def test_baseline_passes(self):
        v, _ = self.dv22(self._doc)
        self.assertEqual(v, "PASS")

    def test_escape_1_contrastive_agent2_is_MISSED(self):
        """Agent 1, unlike Agent 2, owns the audio cues -> nearest prior ref is Agent 2."""
        v, out = self.dv22(self.inject("Agent 1, unlike Agent 2, owns the audio cues."))
        self.assertEqual(v, "PASS", "if FAIL, MAJOR-1 is closed - reissue the review")
        self.assertIn("27/27", out, "the whole document still scores clean")

    def test_escape_2_first_agent_synonym_is_MISSED(self):
        """'the first agent' carries no Agent<digit> token -> no attribution made."""
        v, out = self.dv22(self.inject("The first agent owns the audio cues."))
        self.assertEqual(v, "PASS", "if FAIL, MAJOR-1 is closed - reissue the review")
        self.assertIn("27/27", out)

    def test_plain_assignment_is_still_CAUGHT(self):
        """Control: the predicate does work on the ordinary form."""
        v, _ = self.dv22(self.inject("Agent 1 owns the audio cues."))
        self.assertEqual(v, "FAIL")

    def test_my_published_n1_attack_is_now_CAUGHT(self):
        """The keyword-prefix escape I published at S4.2 must now be caught."""
        v, _ = self.dv22(self.inject("D-4 note: Agent 1 owns the audio cues."))
        self.assertEqual(v, "FAIL")

    def test_the_document_uses_first_agent_as_a_synonym(self):
        """Escape 2 is reachable: the document itself uses the term for Agent 1."""
        s = self.s435()
        self.assertGreaterEqual(len(re.findall(r"the first agent", s, re.I)), 10)

    def test_root_cause_is_nearest_prior_reference(self):
        src = (self._d / "dv.py").read_text()
        self.assertIn("AGENT_REF = re.compile(r'agent[-\\s]?([12])\\b'", src)
        self.assertIn("before[-1].group(1) == '1'", src)

    def test_review_reports_both_escapes(self):
        self.assertIn("MAJOR-1", self.flat)
        self.assertIn("Agent 1, unlike Agent 2, owns the audio cues", self.flat)
        self.assertIn("The first agent owns the audio cues", self.flat)
        self.assertIn("22 were classified correctly", self.flat)


class TestPrescriptionIsMeasured(Base):
    """MINOR-3: the review must distinguish a fix that works from one that merely looks right.

    These encode the three-population rule: clean doc 27/27 & 0 offenders, both escapes FAIL,
    existing 67 still pass. Nothing less counts as closure for C-1.
    """

    def test_naive_synonym_add_is_ineffective(self):
        """A bare '|the first agent' alternative leaves group(1) as None -> escape survives."""
        src = git_show("%s:docs/validation/dv_c05.py" % S435_COMMIT)
        doc = git_show(S435_BLOB)
        if src is None or doc is None:
            self.skipTest("unavailable")
        patched = src.replace(
            "AGENT_REF = re.compile(r'agent[-\\s]?([12])\\b', re.I)",
            "AGENT_REF = re.compile(r'agent[-\\s]?([12])\\b|the first agent', re.I)")
        self.assertNotEqual(patched, src, "anchor moved; re-check MINOR-3")
        d = Path(tempfile.mkdtemp())
        (d / "dv.py").write_text(patched)
        (d / "doc.md").write_text(doc.replace(
            "## 9. Shared read-surface",
            "| X | The first agent owns the audio cues. | a | b | c | d | e |\n"
            "## 9. Shared read-surface"))
        r = subprocess.run([sys.executable, str(d / "dv.py"), str(d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        verdict = [l for l in r.stdout.splitlines() if l.startswith("DV-22 ")][0].split()[1]
        self.assertEqual(verdict, "PASS", "the naive fix now works - MINOR-3 needs updating")

    def test_blunt_deny_by_default_false_positives(self):
        """The 'fail on any unattributable audio mention' fix breaks the clean document."""
        src = git_show("%s:docs/validation/dv_c05.py" % S435_COMMIT)
        doc = git_show(S435_BLOB)
        if src is None or doc is None:
            self.skipTest("unavailable")
        old = ('    return [m for m in audio_mentions(ln)\n'
               '            if not negated_mention(ln, m) and attributed_to_agent_1(ln, m)]')
        new = ('    out = []\n'
               '    for m in audio_mentions(ln):\n'
               '        if negated_mention(ln, m):\n'
               '            continue\n'
               '        if attributed_to_agent_1(ln, m):\n'
               '            out.append(m)\n'
               '            continue\n'
               '        if not AGENT_REF.search(ln):\n'
               '            out.append(m)\n'
               '    return out')
        if old not in src:
            self.skipTest("audio_offences shape changed")
        d = Path(tempfile.mkdtemp())
        (d / "dv.py").write_text(src.replace(old, new))
        (d / "doc.md").write_text(doc)
        r = subprocess.run([sys.executable, str(d / "dv.py"), str(d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        verdict = [l for l in r.stdout.splitlines() if l.startswith("DV-22 ")][0].split()[1]
        self.assertEqual(verdict, "FAIL",
                         "blunt fix no longer false-positives - MINOR-3 needs updating")

    def test_review_records_the_three_population_rule(self):
        self.assertIn("three populations at once", self.flat)
        self.assertIn("MINOR-3", self.flat)

    def test_review_rejects_option_b_on_measurement(self):
        self.assertIn("REJECTED on measurement", self.flat)
        self.assertIn("Do not implement (b)", self.flat)


# ---------------------------------------------------------------------------
# 6. DV-24 deny-by-default actually works
# ---------------------------------------------------------------------------

class TestDv24(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        src = git_show("%s:docs/validation/dv_c05.py" % S435_COMMIT)
        doc = git_show(S435_BLOB)
        if src is None or doc is None:
            raise unittest.SkipTest("unavailable")
        cls._d = Path(tempfile.mkdtemp())
        (cls._d / "dv.py").write_text(src)
        cls._doc = doc

    def dv24(self, text):
        p = self._d / "doc.md"
        p.write_text(text)
        r = subprocess.run([sys.executable, str(self._d / "dv.py"), str(p)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        line = [l for l in r.stdout.splitlines() if l.startswith("DV-24 ")]
        self.assertTrue(line)
        return line[0].split()[1]

    def test_baseline_passes(self):
        self.assertEqual(self.dv24(self._doc), "PASS")

    def test_catches_number_word_contradiction(self):
        m = self._doc.replace("## 9. Shared read-surface",
                              "The suite grew from seven declared to six observed tokens.\n"
                              "## 9. Shared read-surface")
        self.assertEqual(self.dv24(m), "FAIL")

    def test_catches_mid_document_wrong_pair(self):
        m = self._doc.replace("## 9. Shared read-surface",
                              "For the record: 7 declared, 6 observed.\n"
                              "## 9. Shared read-surface")
        self.assertEqual(self.dv24(m), "FAIL")

    def test_catches_second_pair_on_anchor_line(self):
        m = self._doc.replace("## 9. Shared read-surface",
                              "| **6** | `DV-11` reports 7 declared, 5 observed. "
                              "Also 6 declared, 4 observed. | x |\n## 9. Shared read-surface")
        self.assertEqual(self.dv24(m), "FAIL")


# ---------------------------------------------------------------------------
# 7. Executed evidence the review claims
# ---------------------------------------------------------------------------

class TestExecutedEvidence(Base):
    def validator(self):
        t = git_show("%s:docs/validation/dv_c05.py" % S435_COMMIT)
        if t is None:
            self.skipTest("validator unavailable")
        return t

    def score(self, doc_text):
        d = Path(tempfile.mkdtemp())
        (d / "dv.py").write_text(self.validator())
        (d / "doc.md").write_text(doc_text)
        r = subprocess.run([sys.executable, str(d / "dv.py"), str(d / "doc.md")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        m = re.search(r"(\d+)/(\d+) checks passed", r.stdout)
        self.assertIsNotNone(m, r.stdout[-300:])
        return int(m.group(1)), int(m.group(2))

    def test_27_of_27_on_reviewed_blob(self):
        self.assertEqual(self.score(self.s435()), (27, 27))

    def test_discriminates_on_s41(self):
        got, tot = self.score(self.blob(S41_BLOB))
        self.assertEqual(tot, 27)
        self.assertLess(got, tot)

    def test_discriminates_on_s42(self):
        got, tot = self.score(self.blob(S42_BLOB))
        self.assertLess(got, tot)

    def test_discriminates_on_s3(self):
        got, tot = self.score(self.blob(S3_BLOB))
        self.assertLess(got, tot)

    def test_review_reports_the_numbers(self):
        for n in ("27/27", "26/27", "24/27", "21/27", "10/27"):
            self.assertIn(n, self.flat)


# ---------------------------------------------------------------------------
# 8. The suite-count defect S4.3.5 corrects
# ---------------------------------------------------------------------------

class TestSuiteCountCorrection(Base):
    def test_s434_said_74(self):
        s = self.blob(S434_BLOB)
        self.assertIn("from **56** to **74**", s)

    def test_s435_scope_says_67(self):
        s = self.s435()
        self.assertIn("from 56 to **67**", s)

    def test_74_appears_only_as_quotation(self):
        s = self.s435()
        for m in re.finditer(r"\b74\b", s):
            ctx = s[max(0, m.start() - 120):m.start() + 80]
            ok = ("56 to **74**" in ctx or "56 to 74" in ctx
                  or "56 \u2192 **74**" in ctx or "corrected" in ctx.lower()
                  or "S4.3.4" in ctx)
            self.assertTrue(ok, "unaccounted '74': %r" % ctx)

    def test_audit_table_has_eleven_rows(self):
        sec = self.s435().split("**Every suite-count claim in the document, audited.**")[1]
        sec = sec.split("**The two numbers that look alike")[0]
        n = len([l for l in sec.splitlines() if re.match(r"\| \d+ \|", l)])
        self.assertEqual(n, 11)

    def test_review_states_the_audit_is_unenforced(self):
        self.assertIn("recorded table, not enforced", self.flat)
        self.assertIn("MINOR-1", self.flat)


# ---------------------------------------------------------------------------
# 9. Agent 3 independence and the arbitration boundary
# ---------------------------------------------------------------------------

class TestIndependence(Base):
    def test_review_states_agent3_was_not_consulted(self):
        self.assertIn("did not read Agent 3", self.flat)
        self.assertIn("did not coordinate with Agent 3", self.flat)

    def test_review_makes_no_claim_about_agent3_conclusions(self):
        for bad in ("Agent 3 agrees", "Agent 3 concurs", "Agent 3 signed"):
            self.assertNotIn(bad, self.flat)

    def test_agent3_artifacts_still_absent_of_s42_s435(self):
        """The document's negative existence claim, checked against reality."""
        r = subprocess.run(["git", "ls-tree", "-r", "--name-only",
                            "origin/arena/c64fc525-tdd"],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            self.skipTest("other branch unavailable")
        files = [f for f in r.stdout.splitlines() if "AGENT3" in f]
        for f in files:
            body = git_show("origin/arena/c64fc525-tdd:%s" % f) or ""
            self.assertEqual(body.count(S42_BLOB) + body.count(S435_BLOB), 0, f)

    def test_arbitration_three_domains_present(self):
        s = self.s435()
        for dom in ("**Creation**", "**Selection**", "**Outcome**"):
            self.assertIn(dom, s)


# ---------------------------------------------------------------------------
# 10. Verdict and boundaries
# ---------------------------------------------------------------------------

class TestVerdict(Base):
    def test_verdict_is_pass_with_conditions(self):
        self.assertIn("`PASS WITH CONDITIONS`", self.raw)

    def test_single_condition_named(self):
        self.assertIn("**C-1 (required).**", self.flat)

    def test_no_blockers(self):
        self.assertIn("**0**", self.flat)
        self.assertIn("## 4.1 BLOCKERS — none", self.raw)

    def test_zero_acceptance_cases(self):
        self.assertIn("0 of 67 acceptance cases executed", self.flat)
        self.assertIn("`PROPOSED / NOT RUN`", self.flat)

    def test_does_not_treat_regressions_as_acceptance(self):
        self.assertIn("not", self.flat)
        self.assertIn("67 *instrument regression* cases are tests of the checker", self.flat)

    def test_no_governance_claim(self):
        """Denial context must be excluded, or 'No MEAD selected' matches 'MEAD selected'."""
        flat = self.flat
        for bad in ("C-05 is approved", "U-07 is closed", "a MEAD was selected",
                    "signature granted", "C-05 is frozen"):
            for m in re.finditer(re.escape(bad), flat):
                ctx = flat[max(0, m.start() - 70):m.start() + 30].lower()
                self.assertTrue(
                    any(n in ctx for n in ("no ", "not ", "never", "remains open",
                                           "is open", "nothing ")),
                    "affirmative governance claim: %r" % ctx)

    def test_artifact_not_modified(self):
        r = subprocess.run(["git", "diff", "--stat", "HEAD", "--", S435_PATH],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(r.stdout.strip(), "")

    def test_prior_artifacts_preserved(self):
        for p in ("AGENT2_REASSESSMENT_A1C05_S4_1_V1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_1_ADDENDUM_A1.md",
                  "AGENT2_REASSESSMENT_A1C05_S4_2_V1.md"):
            self.assertTrue((ROOT / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
