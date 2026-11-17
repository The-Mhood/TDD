"""Tests for Docs/AGENT2_REVIEW_A1C05_S4_V1.md (W-M2.12).

Locks the review's claims about A1-C05-S4 v4.0 at the exact reviewed blob.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised: no telegraph,
producer, consumer, directory or engine exists here. All 67 acceptance cases in the reviewed
document are PROPOSED / NOT RUN and none is run by this file.

Assertions are anchored on exact clause text or on parsed structure, never on prose alone.
Each finding has a tamper proof in the module docstring of its class.
"""

import re
import subprocess
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[3] / "Docs" / "AGENT2_REVIEW_A1C05_S4_V1.md"
REPO = REVIEW.parents[1]

S4_BLOB = "424d2c69df62ebc1930eacd0ba67077c854ab31e"
S4_COMMIT = "4692e973d04a94d7781677c704e7a0198abd2d70"
S4_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md"

S4_TIP_BLOB = "d72831e7478d084ab7c0f8841536958e2f001727"
S4_TIP_COMMIT = "a3453548c02761da37ff1a93732dab86ed0a119a"

S3_BLOB = "077232368c42b2cd910be2c9642ba05cd7faa382"

VF_FIELDS = ["Phase", "WindupEndAxis", "ActiveEndAxis", "RecoveryEndAxis",
             "ProducerRate", "WindowKey", "AttackTag"]

ALLOWED_ROWS = {"TN-P": {2}, "TN-C": {5, 6}, "TN-R": {2, 4}, "TN-A": {8}}


def git_show(spec):
    try:
        r = subprocess.run(["git", "show", spec], capture_output=True,
                           text=True, cwd=REPO, check=False)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.raw)

    def s4(self):
        t = git_show(S4_BLOB)
        if t is None:
            self.skipTest("reviewed S4 blob not available")
        return t

    def s4flat(self):
        return re.sub(r"\s+", " ", self.s4())

    def obligation_cells(self, s=None):
        s = s if s is not None else self.s4()
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
        """Parse the §5.4 token table into {token: sorted row list}."""
        s = s if s is not None else self.s4()
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
# Provenance
# ---------------------------------------------------------------------------

class TestProvenance(Base):
    def test_blob_recorded(self):
        self.assertIn(S4_BLOB, self.flat)

    def test_review_flags_the_missing_v4_1_path(self):
        self.assertIn("docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md", self.flat)
        self.assertIn("No file by that name exists on any remote branch", self.flat)

    def test_review_states_it_did_not_substitute_silently(self):
        self.assertIn("I did not silently substitute a path", self.flat)

    def test_tip_differs_by_placeholder_fill_only(self):
        a, b = git_show(S4_BLOB), git_show(S4_TIP_BLOB)
        if a is None or b is None:
            self.skipTest("both blobs required")
        import difflib
        diff = [d for d in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                                lineterm="", n=0)
                if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
        self.assertEqual(len(diff), 10, "expected 5 insertions + 5 deletions")
        for d in diff:
            if d.strip() in ("+", "-"):
                continue  # blank line added/removed by the placeholder paragraph
            self.assertTrue(
                "PUB_COMMIT" in d or "PUB_BLOB" in d
                or re.search(r"\b[0-9a-f]{40}\b", d)
                or "branch tip" in d or "Why the blob above" in d
                or "This row was filled" in d,
                "unexpected change outside placeholder fill: %r" % d)

    def test_tip_blob_hash_is_the_real_one(self):
        """Regression from W-M2.12: S3's tip hash was mis-transcribed. Assert this one resolves."""
        out = subprocess.run(["git", "rev-parse",
                              f"{S4_TIP_COMMIT}:{S4_PATH}"],
                             capture_output=True, text=True, cwd=REPO, check=False)
        if out.returncode != 0:
            self.skipTest("S4 tip commit not available")
        self.assertEqual(out.stdout.strip(), S4_TIP_BLOB)

    def test_content_commit_blob_is_the_real_one(self):
        out = subprocess.run(["git", "rev-parse", f"{S4_COMMIT}:{S4_PATH}"],
                             capture_output=True, text=True, cwd=REPO, check=False)
        if out.returncode != 0:
            self.skipTest("S4 content commit not available")
        self.assertEqual(out.stdout.strip(), S4_BLOB)

    def test_s4_line_count(self):
        self.assertEqual(len(self.s4().splitlines()), 1165)

    def test_s3_baseline_unmodified(self):
        import hashlib
        t = git_show(S3_BLOB)
        if t is None:
            self.skipTest("S3 blob not available")
        blob = hashlib.sha1(b"blob %d\x00" % len(t.encode()) + t.encode()).hexdigest()
        self.assertEqual(blob, S3_BLOB)


# ---------------------------------------------------------------------------
# D-1: the lost-retime bound
# TAMPER: change TN-C-14's "at least once per frame" -> the bound test fails.
# ---------------------------------------------------------------------------

class TestD1LostRetime(Base):
    def test_ex5_case_d_present(self):
        sec = self.s4().split("### 10.5 EX-5")[1].split("### 10.6")[0]
        self.assertIn("**(d)**", sec)
        self.assertIn("only the phase received", sec)

    def test_case_d_says_rate_stale(self):
        sec = self.s4().split("### 10.5 EX-5")[1].split("### 10.6")[0]
        flat = re.sub(r"\s+", " ", sec)
        self.assertIn("phase-correct and rate-stale", flat)
        self.assertIn("accepted and stated", flat)

    def test_tn_c_14_imposes_one_pull_per_frame(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("re-pulls every open instance it holds at least once per frame", row)

    def test_tn_c_14_states_the_bound(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-C-14**")][0]
        self.assertIn("bounded by one frame", row)

    def test_section_3_6_retracts_the_s3_claim(self):
        flat = self.s4flat()
        self.assertIn("S3's claim that it \"merely needs a resync\" was wrong", flat)

    def test_bound_depends_on_po5_being_present(self):
        """The bound only holds because PO-5 forbids live state ahead of publication."""
        flat = self.s4flat()
        self.assertIn("the producer's live state may never contain a `VF` change that no",
                      flat)

    def test_review_flags_upper_bound_wording(self):
        self.assertIn("D-1a", self.flat)
        self.assertIn("upper bound", self.flat)


# ---------------------------------------------------------------------------
# D-2 / C4c-2: PO-5 and per-message ProducerRate
# TAMPER: delete PO-5 -> both tests fail.
# ---------------------------------------------------------------------------

class TestD2Po5(Base):
    def test_po5_exists_in_section_4_9(self):
        sec = self.s4().split("### 4.9 C05-2.9")[1].split("### 4.10")[0]
        self.assertIn("**PO-5 (new).**", re.sub(r"\s+", " ", sec))

    def test_po5_states_interleaving(self):
        flat = self.s4flat()
        self.assertIn("Publication is **interleaved with application**", flat)

    def test_po5_states_the_content_rule(self):
        flat = self.s4flat()
        self.assertIn("carries the changes applied at or before", flat)

    def test_tn_p_18_exists(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-P-18**")][0]
        self.assertIn("Publish **between** applications", row)

    def test_t_c05_51_asserts_producer_rate_per_message(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **T-C05-51**")][0]
        self.assertIn("ProducerRate", row)

    def test_t_c05_65_asserts_midframe_pull(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **T-C05-65**")][0]
        self.assertIn("pull taken after each application", row)
        self.assertIn("batches both changes", row)


# ---------------------------------------------------------------------------
# D-3 / C6-1: identity fixed, close-and-reopen
# TAMPER: restore "every change to WindowKey" -> test_dead_norm_removed fails.
# ---------------------------------------------------------------------------

class TestD3Identity(Base):
    def test_tn_p_19_exists(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-P-19**")][0]
        self.assertIn("fixed for the instance's lifetime", row)
        self.assertIn("closes the instance", row)

    def test_tn_p_07_drops_the_identity_clause(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-P-07**")][0]
        self.assertNotIn("every change to `WindowKey` or `AttackTag`", row)
        self.assertIn("Identity fields cannot change mid-instance", row)

    def test_tn_p_04_names_identity_change(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-P-04**")][0]
        self.assertIn("change of attack identity", row)

    def test_rejected_phrase_never_unquoted(self):
        """DV-23's claim, verified independently: 'constant for the lifetime' only in quotes."""
        s = self.s4()
        for m in re.finditer(r"constant for the lifetime", s):
            ctx = s[max(0, m.start() - 120):m.start()]
            self.assertTrue('"' in ctx or "\u201c" in ctx or "'" in ctx,
                            "unquoted rejected phrase near: %r" % ctx[-80:])

    def test_t_c05_66_exists(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **T-C05-66**")][0]
        self.assertIn("new `AttackInstanceId` at revision 1", row)


# ---------------------------------------------------------------------------
# D-4: audio — the defect that SURVIVES
# TAMPER: delete "and audio" from the section 8 preamble -> the failing test passes,
#         which is the signal that D-4 is closed and the review must be reissued.
# ---------------------------------------------------------------------------

class TestD4Audio(Base):
    def test_row5_disclaims_audio(self):
        rows = [l for l in self.s4().splitlines()
                if re.sub(r"^\s*>\s*", "", l).lstrip().startswith("| **Consumer integration (Agent 1)")]
        self.assertTrue(rows)
        self.assertNotIn("and audio cues", rows[0])
        self.assertIn("Agent 1 owns no audio responsibility in C-05", rows[0])

    def test_row6_owns_audio(self):
        rows = [l for l in self.s4().splitlines()
                if re.sub(r"^\s*>\s*", "", l).lstrip().startswith("| **Consumer integration (Agent 2)")]
        self.assertTrue(rows)
        self.assertIn("audio cue selection", rows[0])
        self.assertIn("the only C-05 row that owns audio", rows[0])

    def test_tn_c_15_exists_and_is_agent2(self):
        cells = dict(self.obligation_cells())
        self.assertEqual(cells["TN-C-15"], "Agent 2, C-05 consumer")
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-C-15**")][0]
        self.assertIn("Agent 2 alone", row)

    def test_d4_defect_still_present_in_section_8_preamble(self):
        """This is the FAILING condition the review reports. If it passes, D-4 is closed."""
        pre = [l for l in self.s4().splitlines() if "Each obligation is implemented by each" in l]
        self.assertTrue(pre, "section 8 preamble must exist")
        self.assertIn("Agent 1 for defence, dodge, camera and audio", pre[0],
                      "if 'and audio' was removed, D-4 is CLOSED - reissue the review")

    def test_dv22_is_scoped_too_narrowly_to_catch_it(self):
        """DV-22's stated method does not mention a whole-document search."""
        row = [l for l in self.s4().splitlines() if l.startswith("| **DV-22**")][0]
        self.assertIn("row 5", row)
        self.assertNotIn("whole document", row)

    def test_review_flags_d4_as_blocking(self):
        self.assertIn("**Blocking**", self.flat)
        self.assertIn("preamble still assigns audio to Agent 1", self.flat)


# ---------------------------------------------------------------------------
# D-5 / D-6 / C9: tokens and DV-11 row-level
# TAMPER: revert TN-C-13 to the row-7 token -> row-level simulation fails.
# ---------------------------------------------------------------------------

class TestD5D6Tokens(Base):
    def test_new_token_exists_and_maps_to_row_6(self):
        tm = self.token_map()
        self.assertIn("Agent 2, C-05 consumer", tm)
        self.assertEqual(tm["Agent 2, C-05 consumer"], [6])

    def test_inside_and_outside_tokens_are_distinct(self):
        tm = self.token_map()
        self.assertEqual(tm["Agent 2, in its own systems"], [7])
        self.assertNotEqual(tm["Agent 2, C-05 consumer"], tm["Agent 2, in its own systems"])

    def test_tn_c_12_13_15_use_row6_token(self):
        cells = dict(self.obligation_cells())
        for oid in ("TN-C-12", "TN-C-13", "TN-C-15"):
            self.assertEqual(cells[oid], "Agent 2, C-05 consumer", oid)

    def test_seven_declared_five_observed(self):
        tm = self.token_map()
        obs = {t for _, t in self.obligation_cells()}
        self.assertEqual(len(tm), 7, "seven tokens declared")
        self.assertEqual(len(obs), 5, "five tokens observed in cells")
        self.assertEqual(sorted(set(tm) - obs),
                         ["Agent 2, in its own systems",
                          "contract layer, owner pending TD-12"])

    def test_row_level_rule_passes_with_zero_failures(self):
        """Re-implement DV-11's stated rule independently and run it."""
        tm = self.token_map()
        fails = []
        for oid, tok in self.obligation_cells():
            pre = "-".join(oid.split("-")[:2])
            tr = tm.get(tok)
            if tr is None:
                fails.append("%s: undeclared %r" % (oid, tok))
            elif not set(tr) & ALLOWED_ROWS[pre]:
                fails.append("%s: %r -> rows %r, allowed %r"
                             % (oid, tok, tr, sorted(ALLOWED_ROWS[pre])))
        self.assertEqual(fails, [])

    def test_row_level_rule_can_fail_on_the_s3_shape(self):
        """A TN-C obligation carrying the row-7 token must fail: this is the whole point."""
        tm = self.token_map()
        self.assertFalse(set(tm["Agent 2, in its own systems"]) & ALLOWED_ROWS["TN-C"],
                         "row-7 token must not intersect the TN-C allowed set")

    def test_43_cells(self):
        self.assertEqual(len(self.obligation_cells()), 43)

    def test_dv11_reports_7_declared_5_observed(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **DV-11**")][0]
        self.assertIn("7 declared / 5 observed", row)

    def test_section_1_row6_reports_the_wrong_count(self):
        """D-6a: the surviving arithmetic error the review reports."""
        self.assertIn("(7 declared, 6 observed)", self.s4flat(),
                      "if corrected to 5, D-6a is CLOSED - reissue the review")

    def test_all_other_count_statements_say_five(self):
        s = self.s4flat()
        self.assertIn("7 declared / 5 observed", s)
        self.assertIn("declares **seven**; **five appear", s)

    def test_section_5_4_tallies_are_imprecise(self):
        """D-6b: '19 TN-P rows' vs 23 actual cells; '11 TN-C rows' vs 12."""
        from collections import Counter
        per = Counter()
        for oid, tok in self.obligation_cells():
            if tok == "producer owner":
                per["producer"] += 1
            if tok == "each consumer":
                per["consumer"] += 1
        self.assertEqual(per["producer"], 23)
        self.assertEqual(per["consumer"], 12)
        self.assertIn("19 `TN-P` rows", self.s4flat())
        self.assertIn("11 `TN-C` rows", self.s4flat())


# ---------------------------------------------------------------------------
# D-7 / C4a-1: INV-2 precondition in the clause
# TAMPER: remove "holds only while" from INV-2 -> test fails.
# ---------------------------------------------------------------------------

class TestD7Inv2(Base):
    def test_inv2_states_precondition_in_the_clause(self):
        row = [l for l in self.s4().splitlines()
               if l.strip().startswith("> **INV-2 (corrected: precondition stated).**")]
        self.assertTrue(row)
        flat = re.sub(r"\s+", " ", row[0])
        self.assertIn("`INV-2` holds only while `ProducerRate` and `PhaseEndAxis` are fixed",
                      flat)
        self.assertIn("within a single revision", flat)

    def test_tn_c_10_echoes_it(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-C-10**")][0]
        self.assertIn("limited to the revision the consumer holds", row)

    def test_arithmetic_still_holds(self):
        """Re-derive the equivalence independently at four axes."""
        END, NOW, RATE = 4.0, 0.0, 0.05
        r0 = max(0.0, (END - NOW) * RATE)
        for axis in (0.0, 2.0, 4.0, 8.0):
            prod = max(0.0, (END - axis) * RATE)
            cons = max(0.0, r0 - (axis - NOW) * RATE)
            self.assertAlmostEqual(prod, cons, places=12, msg="axis %r" % axis)


# ---------------------------------------------------------------------------
# C4a-2 / DV-12: VF list in three homes
# TAMPER: drop a field from the struct comment -> set equality fails.
# ---------------------------------------------------------------------------

class TestC4a2VfHomes(Base):
    def _homes(self):
        s = self.s4()
        h1 = s.split("**VF — versioned fields")[1].split("\n> **OF")[0]
        # INV-1 lives in 4.6
        h2 = s.split("> **INV-1 (corrected).**")[1].split("\n\n")[0]
        # struct comment: the Timing struct's explicit VF list
        h3 = s.split("// ---- VF: versioned fields (INV-1; identical for one revision).")[1] \
              .split("double  WindupEndAxis;")[0]
        return h1, h2, h3

    def test_all_three_homes_name_all_seven(self):
        h1, h2, h3 = self._homes()
        for name, h in (("3.2", h1), ("INV-1", h2), ("struct", h3)):
            found = {f for f in VF_FIELDS if f in h}
            self.assertEqual(found, set(VF_FIELDS), "%s missing %s"
                             % (name, set(VF_FIELDS) - found))

    def test_dv12_states_set_equality(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **DV-12**")][0]
        self.assertIn("set equality", row)


# ---------------------------------------------------------------------------
# C4c-N1: PO-5 falsifies section 3.6's stated reason (b)
# TAMPER: rewrite (b) -> the "stale premise" test fails.
# ---------------------------------------------------------------------------

class TestC4cN1StalePremise(Base):
    def test_reason_b_claims_order_is_not_observable(self):
        flat = self.s4flat()
        self.assertIn("the producer's internal application order is **not observable**", flat)

    def test_po5_makes_it_observable(self):
        flat = self.s4flat()
        self.assertIn("A pull taken between two publications of the same frame returns "
                      "the earlier revision's `VF` exactly", flat)

    def test_contradiction_is_real(self):
        """Both statements are in the same section 3.6, unreconciled."""
        s = self.s4flat()
        claim = "the producer's internal application order is **not observable**" in s
        rule = "A pull taken between two publications of the same frame returns" in s
        self.assertTrue(claim and rule, "both halves must be present for C4c-N1 to stand")

    def test_review_records_c4c_n1(self):
        self.assertIn("C4c-N1", self.flat)


# ---------------------------------------------------------------------------
# Counts: every total the review verified
# ---------------------------------------------------------------------------

class TestCounts(Base):
    def test_43_obligations_correct_split(self):
        s = self.s4()
        got = {}
        for head, key in (("## 7. Producer obligations", "TN-P"),
                          ("## 8. Consumer obligations", "TN-C"),
                          ("## 9. Shared read-surface and arbitration obligations", "TN-R")):
            body = s.split(head)[1].split("\n## ")[0]
            got[key] = len([l for l in body.splitlines() if l.startswith("| **%s-" % key)])
        body9 = s.split("## 9. Shared read-surface and arbitration obligations")[1].split("\n## ")[0]
        got["TN-A"] = len([l for l in body9.splitlines() if l.startswith("| **TN-A-")])
        self.assertEqual(got, {"TN-P": 19, "TN-C": 15, "TN-R": 6, "TN-A": 3})
        self.assertEqual(sum(got.values()), 43)

    def test_67_cases_over_18_suites(self):
        s = self.s4()
        sec = s.split("### 12.1 The suites")[1].split("### 12.2")[0]
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

    def test_case_ids_01_to_67_complete(self):
        ids = sorted({int(m) for m in re.findall(r"T-C05-(\d\d)", self.s4())})
        self.assertEqual(ids, list(range(1, 68)))

    def test_23_document_checks(self):
        sec = self.s4().split("### 13.1")[1].split("### 13.2")[0]
        dvs = re.findall(r"\| \*\*(DV-\d+)\*\*", sec)
        self.assertEqual(len(dvs), 23)
        self.assertEqual(dvs[0], "DV-1")
        self.assertEqual(dvs[-1], "DV-23")

    def test_section_11_2_bidirectional(self):
        s = self.s4()
        sec = s.split("Obligation \u2192 test coverage")[1].split("\n## ")[0]
        pairs = {}
        for l in sec.splitlines():
            if not l.startswith("|"):
                continue
            c = [x.strip().strip("*") for x in l.strip("|").split("|")]
            for i in range(0, len(c) - 1, 2):
                ob, cs = c[i], c[i + 1]
                if not ob.startswith("TN-"):
                    continue
                ids = {int(x) for x in re.findall(r"T-C05-(\d\d)", cs)}
                for a, b in re.findall(r"T-C05-(\d\d)\s*\u2026\s*(?:T-C05-)?(\d\d)", cs):
                    ids |= set(range(int(a), int(b) + 1))
                pairs[ob] = ids
        self.assertEqual(len(pairs), 43)
        covered = set()
        for v in pairs.values():
            covered |= v
        self.assertEqual(covered, set(range(1, 68)))
        self.assertEqual([k for k, v in pairs.items() if not v], [])


# ---------------------------------------------------------------------------
# Arbitration boundary: C05-6.4, assessed because it is new
# ---------------------------------------------------------------------------

class TestArbitrationBoundary(Base):
    def test_three_domains_present(self):
        sec = self.s4().split("### 9.2 `C05-6.4`")[1].split("### 9.3")[0]
        for d in ("**Creation**", "**Selection**", "**Outcome**"):
            self.assertIn(d, sec)

    def test_tn_a_02_names_attack_tag(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-A-02**")][0]
        self.assertIn("`AttackTag` included", row)

    def test_tn_a_03_exists(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-A-03**")][0]
        self.assertIn("may not appear among them", row)

    def test_tn_c_11_is_selection_only(self):
        row = [l for l in self.s4().splitlines() if l.startswith("| **TN-C-11**")][0]
        self.assertIn("grants no authority over a hit's outcome", row)

    def test_review_does_not_accept_for_agent3(self):
        self.assertIn("Whether it satisfies Agent 3 is theirs to say and I do not speak for them",
                      self.flat)


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------

class TestGovernance(Base):
    def test_review_does_not_sign(self):
        self.assertIn("I am not signing v4.0", self.flat)

    def test_zero_executed_present(self):
        self.assertIn("0 executed", self.flat)

    def test_no_claim_acceptance_tests_passed(self):
        for bad in ("all 67 cases pass", "acceptance tests passed", "67/67"):
            self.assertNotIn(bad, self.flat)

    def test_u07_not_closed(self):
        self.assertIn("U-07", self.flat)
        self.assertNotIn("U-07 is closed", self.flat)
        self.assertNotIn("U-07 closed", self.flat)

    def test_no_mead_selected(self):
        self.assertIn("No MEAD is selected", self.flat)

    def test_outcome_is_one_of_the_three(self):
        vocab = re.findall(r"`(PASS|TARGETED REVISION|BLOCKED BY DEPENDENCY)`", self.raw)
        self.assertIn("TARGETED REVISION", vocab)

    def test_verdict_table_tally_is_correct(self):
        """9 AGREE + 4 AWC + 2 DISAGREE over 7 defects + 7 conditions."""
        sec = self.raw.split("## 1. Verdict summary")[1].split("## 2. D-1")[0]
        counts = {}
        n = 0
        for r in sec.splitlines():
            if not r.startswith("| **"):
                continue
            n += 1
            for cell in [x.strip() for x in r.strip("|").split("|")]:
                m = re.fullmatch(r"\*\*(AGREE WITH CONDITIONS|AGREE|DISAGREE)\*\*", cell)
                if m:
                    counts[m.group(1)] = counts.get(m.group(1), 0) + 1
                    break
        self.assertEqual(n, 14, "7 defects + 7 conditions")
        self.assertEqual(counts.get("AGREE", 0), 8, counts)
        self.assertEqual(counts.get("AGREE WITH CONDITIONS", 0), 4, counts)
        self.assertEqual(counts.get("DISAGREE", 0), 2, counts)
        self.assertIn("8 AGREE, 4 AGREE WITH CONDITIONS, 2 DISAGREE", self.flat)

    def test_records_its_own_s3_hash_correction(self):
        """W-M2.12 corrected a mis-transcribed tip hash in the published S3 review."""
        self.assertIn("mis-transcribed blob hash", self.flat)
        self.assertIn("80060dea6685f2f17cae1128ef1a4532eed4e316", self.flat)

    def test_all_prior_reviews_preserved(self):
        for p in ("AGENT2_REVIEW_A1C05_S2_V1.md", "AGENT2_REVIEW_A1C05_S3_V1.md"):
            self.assertTrue((REPO / "Docs" / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
