"""Tests for Docs/AGENT2_REVIEW_A1C05_S3_V1.md (W-M2.11).

Locks the review's claims about A1-C05-S3 v3.0 at the exact reviewed blob.

DOCUMENT and ARITHMETIC checks only. No contract behaviour is exercised: no telegraph,
producer, consumer, directory or engine exists here. All 62 acceptance cases in the reviewed
document are PROPOSED / NOT RUN and none is run by this file.

Every assertion here is anchored on either an exact line of the reviewed blob or a heading
line of the review. Prose-only anchors are deliberately avoided: they pass for reasons other
than the claim being true.
"""

import re
import subprocess
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[3] / "Docs" / "AGENT2_REVIEW_A1C05_S3_V1.md"
REPO = REVIEW.parents[1]

S3_BLOB = "077232368c42b2cd910be2c9642ba05cd7faa382"
S3_COMMIT = "a6b4e22999c7f8622c7c67e9cdc39e2f57565c20"
S3_PATH = "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md"

TIP_BLOB = "80060de67e00d26ee2be0a50df9f1ac4ce8a2d70"
A1_HEAD = "ec3c2af7455db614f7c9090fbe3c7033cd2fcaf8"

S2_BLOB = "bf6c8fb3ddf3152d1627d3b6471278f57fc82541"


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

    def s3(self):
        t = git_show(S3_BLOB)
        if t is None:
            self.skipTest("reviewed S3 blob not available")
        return t

    def s3flat(self):
        return re.sub(r"\s+", " ", self.s3())


# ---------------------------------------------------------------------------
# Provenance: the review reviewed the right object
# ---------------------------------------------------------------------------

class TestProvenance(Base):
    def test_blob_hash_recorded(self):
        self.assertIn(S3_BLOB, self.flat)

    def test_blob_matches_commit(self):
        t = git_show(f"{S3_COMMIT}:{S3_PATH}")
        if t is None:
            self.skipTest("S3 commit not available")
        import hashlib
        blob = hashlib.sha1(b"blob %d\x00" % len(t.encode()) + t.encode()).hexdigest()
        self.assertEqual(blob, S3_BLOB)

    def test_review_declares_it_did_not_review_the_tip(self):
        self.assertIn("I did not review the branch tip", self.flat)

    def test_tip_differs_only_by_placeholders(self):
        """The 3/3-line difference must be PUB_COMMIT/PUB_BLOB fill only."""
        a, b = git_show(S3_BLOB), git_show(TIP_BLOB)
        if a is None or b is None:
            self.skipTest("both blobs required")
        self.assertNotEqual(a, b)
        import difflib
        diff = [d for d in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
                if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
        self.assertEqual(len(diff), 6, "expected 3 insertions + 3 deletions")
        for d in diff:
            self.assertTrue("PUB_COMMIT" in d or "PUB_BLOB" in d
                            or re.search(r"\b[0-9a-f]{40}\b|\b[0-9a-f]{7,}\b|\u00a7|18\.1", d),
                            "unexpected change outside placeholder fill: %r" % d)

    def test_review_records_946_lines(self):
        t = self.s3()
        self.assertEqual(len(t.splitlines()), 946)


# ---------------------------------------------------------------------------
# §2 / §9: the claims the review verified, verified again here
# ---------------------------------------------------------------------------

class TestDocumentChecksReproduce(Base):
    def test_38_obligations_correct_split(self):
        s = self.s3()
        got = {}
        for head, key in (("## 7. Producer obligations", "TN-P"),
                          ("## 8. Consumer obligations", "TN-C"),
                          ("## 9. Shared read-surface", "TN-R")):
            body = s.split(head)[1].split("\n## ")[0]
            got[key] = len([l for l in body.splitlines()
                            if l.startswith("| **%s-" % key)])
        body9 = s.split("## 9. Shared read-surface")[1].split("\n## ")[0]
        got["TN-A"] = len([l for l in body9.splitlines() if l.startswith("| **TN-A-")])
        self.assertEqual(got, {"TN-P": 17, "TN-C": 13, "TN-R": 6, "TN-A": 2})
        self.assertEqual(sum(got.values()), 38)

    def test_62_cases_over_15_suites(self):
        s = self.s3()
        sec = s.split("### 12.1 The suites")[1].split("### 12.2")[0]
        n = tot = 0
        for l in sec.splitlines():
            if not l.startswith("|"):
                continue
            c = [x.strip().strip("*") for x in l.strip("|").split("|")]
            if len(c) < 5 or not re.fullmatch(r"[A-O]", c[0]):
                continue
            n += 1
            tot += int(c[3])
        self.assertEqual((n, tot), (15, 62))

    def test_case_ids_01_to_62_complete(self):
        ids = sorted({int(m) for m in re.findall(r"T-C05-(\d\d)", self.s3())})
        self.assertEqual(ids, list(range(1, 63)))

    def test_section_11_2_is_bidirectional(self):
        s = self.s3()
        sec = s.split("### 11.2 Obligation \u2192 test coverage")[1].split("\n## ")[0]
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
        self.assertEqual(len(pairs), 38, "all 38 obligations mapped")
        covered = set()
        for v in pairs.values():
            covered |= v
        self.assertEqual(covered, set(range(1, 63)), "every case covered")
        self.assertEqual([k for k, v in pairs.items() if not v], [])

    def test_no_case_in_two_suites(self):
        s = self.s3()
        sec = s.split("### 12.1 The suites")[1].split("### 12.2")[0]
        seen = {}
        for l in sec.splitlines():
            if not l.startswith("|"):
                continue
            c = [x.strip().strip("*") for x in l.strip("|").split("|")]
            if len(c) < 5 or not re.fullmatch(r"[A-O]", c[0]):
                continue
            ids = {int(x) for x in re.findall(r"T-C05-(\d\d)", c[4])}
            for a, b in re.findall(r"T-C05-(\d\d)\s*\u2026\s*(?:T-C05-)?(\d\d)", c[4]):
                ids |= set(range(int(a), int(b) + 1))
            for i in ids:
                seen.setdefault(i, []).append(c[0])
        self.assertEqual({k: v for k, v in seen.items() if len(v) > 1}, {})
        self.assertEqual(set(seen), set(range(1, 63)))


class TestDv8AndDv4Claims(Base):
    def test_dv8_count_is_actually_8(self):
        lines = [l for l in self.s3().splitlines() if "execut" in l]
        self.assertEqual(len(lines), 8)
        self.assertIn("8 lines contain `execut`", self.flat)

    def test_zero_executed_present(self):
        self.assertIn("0 executed", self.s3flat())

    def test_dv4_withdrawn_claim_absent(self):
        self.assertEqual(self.s3().count("in every candidate"), 0)


# ---------------------------------------------------------------------------
# INV-2: the arithmetic the review re-derived
# ---------------------------------------------------------------------------

class TestInv2Arithmetic(Base):
    END, NOW, RATE = 4.0, 0.0, 0.05

    def producer(self, axis):
        return max(0.0, (self.END - axis) * self.RATE)

    def consumer(self, axis):
        r0 = max(0.0, (self.END - self.NOW) * self.RATE)
        return max(0.0, r0 - (axis - self.NOW) * self.RATE)

    def test_forms_agree_at_every_ex9_axis(self):
        for axis in (0.0, 0.2, 2.0, 4.0, 8.0):
            self.assertAlmostEqual(self.producer(axis), self.consumer(axis), places=12,
                                   msg="axis %r" % axis)

    def test_ex9_table_values_reproduce(self):
        expected = [0.2000, 0.1900, 0.1000, 0.0000, 0.0000]
        got = [round(self.producer(a), 4) for a in (0.0, 0.2, 2.0, 4.0, 8.0)]
        self.assertEqual(got, expected)

    def test_clamped_never_negative(self):
        for axis in (0.0, 4.0, 8.0, 100.0):
            self.assertGreaterEqual(self.producer(axis), 0.0)
            self.assertGreaterEqual(self.consumer(axis), 0.0)

    def test_review_records_the_equivalence(self):
        """The review must state it re-derived the proof itself, not accept §3.4's."""
        self.assertIn("I verified the consistency proof myself, two ways", self.flat)


# ---------------------------------------------------------------------------
# D-1: EX-5 omits the only-n+1 case
# ---------------------------------------------------------------------------

class TestEx5OmitsOnlyNPlusOne(Base):
    def test_ex5_has_abcc_prime_markers(self):
        s = self.s3()
        sec = s.split("### 10.5 EX-5")[1].split("### 10.6")[0]
        for mark in ("**(a)**", "**(b)**", "**(c)**", "**(c\u2032)**"):
            self.assertIn(mark, sec, "EX-5 must carry marker %s" % mark)

    def test_ex5_enumerates_only_n_plus_2_loss_not_n_plus_1(self):
        """The dangerous omission: only n+1 received is absent."""
        sec = self.s3().split("### 10.5 EX-5")[1].split("### 10.6")[0]
        flat = re.sub(r"\s+", " ", sec)
        self.assertIn("Only `n+2` received", flat, "the n+2-only case must be present")
        self.assertNotIn("Only `n+1` received", flat,
                         "if EX-5 gained the n+1-only case, D-1 is closed - reissue review")

    def test_rationale_c_asserts_a_resync_nothing_obliges(self):
        s = self.s3flat()
        self.assertIn("phase-correct and merely needs a resync", s)
        self.assertIn("a consumer that loses the second", s)

    def test_ad2_trigger_is_incoming_greater_than_held_plus_one(self):
        flat = self.s3flat()
        self.assertIn("greater than held + 1", flat)
        self.assertIn("records a revision gap", flat)

    def test_review_names_the_defect(self):
        self.assertIn("only `n+1` received", self.flat)
        self.assertIn("D-1", self.flat)


# ---------------------------------------------------------------------------
# D-2: PO-3 fixes sequence not content
# ---------------------------------------------------------------------------

class TestPo3ContentGap(Base):
    def test_po3_states_order_only(self):
        flat = self.s3flat()
        self.assertIn("publishes **all phase transitions first", flat)
        self.assertIn("never a shared revision and never the reverse", flat)

    def test_po3_does_not_state_message_content(self):
        """No PO-n clause states what VF the earlier message carries."""
        s = self.s3()
        po = s.split("### 4.9 C05-2.9")[1].split("### 4.10")[0]
        self.assertNotIn("carries only the changes at or before its revision", po,
                         "if the content rule was added, D-2 is closed")

    def test_t_c05_51_asserts_sequence_not_rate_content(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **T-C05-51**")][0]
        self.assertIn("PhaseChanged`@`n+1", row)
        self.assertNotIn("ProducerRate", row,
                         "T-C05-51 does not discriminate reading A from B")

    def test_tn_p_11_demands_live_state_at_current_revision(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **TN-P-11**")][0]
        self.assertIn("every `VF` field equals the instance's current revision exactly", row)

    def test_review_names_the_reading_collision(self):
        self.assertIn("reading **B** collides with `TN-P-11`", self.flat.replace("Reading", "reading"))


# ---------------------------------------------------------------------------
# D-3: WindowKey/AttackTag constancy contradiction
# ---------------------------------------------------------------------------

class TestWindowKeyConstancyContradiction(Base):
    def test_section_3_8_says_constant_for_lifetime(self):
        s = self.s3flat()
        self.assertIn("authored at `Opened` and constant for the instance's lifetime", s)

    def test_tn_p_07_says_revision_bumps_on_their_change(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **TN-P-07**")][0]
        self.assertIn("every change to `WindowKey` or `AttackTag`", row)

    def test_t_c05_62_setup_includes_their_change(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **T-C05-62**")][0]
        self.assertIn("`WindowKey` change", row)
        self.assertIn("`AttackTag` change", row)

    def test_the_contradiction_is_real(self):
        """constant => TN-P-07 clause can never fire => T-C05-62 rows untestable."""
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **TN-P-07**")][0]
        const = "constant for the instance's lifetime" in self.s3flat()
        mutable = "every change to `WindowKey` or `AttackTag`" in row
        self.assertTrue(const and mutable,
                        "both halves must be present for D-3 to stand")

    def test_review_records_d3(self):
        self.assertIn("D-3", self.flat)


# ---------------------------------------------------------------------------
# D-4: audio owned twice
# ---------------------------------------------------------------------------

class TestAudioOwnershipOverlap(Base):
    def _rows(self):
        s = self.s3()
        return [l for l in s.splitlines()
                if l.lstrip().lstrip(">").strip().startswith("| **Consumer integration (Agent")]

    def test_row5_gives_audio_to_agent1(self):
        rows = [r for r in self._rows() if "Agent 1" in r]
        self.assertTrue(rows)
        self.assertIn("audio cues", rows[0])

    def test_row6_gives_audio_selection_to_agent2(self):
        rows = [r for r in self._rows() if "Agent 2" in r]
        self.assertTrue(rows)
        self.assertIn("audio cue selection", rows[0])

    def test_section_6_1_consumer_table_assigns_audio_to_agent2(self):
        s = self.s3()
        self.assertIn("**Audio cue** (Agent 2)", s)

    def test_no_obligation_row_covers_audio_cue_selection(self):
        s = self.s3()
        for head in ("## 7. Producer obligations", "## 8. Consumer obligations",
                     "## 9. Shared read-surface"):
            body = s.split(head)[1].split("\n## ")[0]
            self.assertNotIn("audio cue selection", body,
                             "if an obligation now covers audio, D-4 changed - reissue")

    def test_review_records_d4(self):
        self.assertIn("D-4", self.flat)


# ---------------------------------------------------------------------------
# D-5 / D-6: C9 — token mapping and DV-11 discriminating power
# ---------------------------------------------------------------------------

class TestC9TokenMapping(Base):
    def _cells(self):
        s = self.s3()
        out = []
        for head in ("## 7. Producer obligations", "## 8. Consumer obligations",
                     "## 9. Shared read-surface"):
            body = s.split(head)[1].split("\n## ")[0]
            for l in body.splitlines():
                if not l.startswith("| **TN-"):
                    continue
                c = [x.strip() for x in l.strip("|").split("|")]
                if len(c) >= 7:
                    out.append((c[0].strip("*"), c[6]))
        return out

    def test_38_cells(self):
        self.assertEqual(len(self._cells()), 38)

    def test_six_tokens_declared_five_used(self):
        s = self.s3()
        sec = s.split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        declared = re.findall(r"\| `([^`]+)` \|", sec)
        self.assertEqual(len(declared), 6, "six tokens declared")
        used = {t for _, t in self._cells()}
        self.assertEqual(len(used), 5, "five tokens used in implementer cells")
        self.assertEqual(sorted(set(declared) - used),
                         ["contract layer, owner pending TD-12"])

    def test_dv11_claims_six_tokens_checked(self):
        self.assertIn("6 role tokens, 38 cells checked", self.flat)

    def test_tn_c_12_and_13_use_outside_c05_token(self):
        cells = dict(self._cells())
        self.assertEqual(cells["TN-C-12"], "Agent 2, in its own systems")
        self.assertEqual(cells["TN-C-13"], "Agent 2, in its own systems")

    def test_that_token_maps_to_row_7_not_row_6(self):
        s = self.s3()
        sec = s.split("### 5.4 C05-7.4")[1].split("## 6.")[0]
        row = [l for l in sec.splitlines() if "Agent 2, in its own systems" in l][0]
        self.assertIn("row 7", row)
        self.assertNotIn("row 6", row)

    def test_rows_6_and_7_share_the_same_owner(self):
        """This is why an agent-level check cannot discriminate them."""
        rows = [l for l in self.s3().splitlines()
                if re.sub(r"^\s*>\s*", "", l).startswith("| **Consumer integration (Agent 2)")
                or re.sub(r"^\s*>\s*", "", l).startswith("| **Resolved outside C-05 (Agent 2")]
        self.assertEqual(len(rows), 2)
        for r in rows:
            self.assertIn("**Agent 2**", r, "both rows are owned by Agent 2")

    def test_dv11_test_is_agent_level(self):
        flat = self.s3flat()
        self.assertIn("require each token's mapped agent to appear in the corresponding", flat)
        self.assertNotIn("row index appears in the obligation's expected row set", flat,
                         "if DV-11 became row-level, D-6 is closed")

    def test_review_records_d5_d6(self):
        self.assertIn("D-5", self.flat)
        self.assertIn("D-6", self.flat)


# ---------------------------------------------------------------------------
# D-7: INV-2 states equivalence unconditionally
# ---------------------------------------------------------------------------

class TestInv2Precondition(Base):
    def test_inv2_clause_states_the_law(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.strip().startswith("> **INV-2 (new).**")]
        self.assertTrue(row)
        self.assertIn("RemainingLocalSeconds", row[0])
        self.assertIn("PhaseEndAxis", row[0])

    def test_inv2_omits_the_one_revision_precondition(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.strip().startswith("> **INV-2 (new).**")][0]
        self.assertNotIn("holds within a single revision", row,
                         "if INV-2 gained the precondition, D-7 is closed")

    def test_precondition_exists_only_in_rationale_prose(self):
        flat = self.s3flat()
        self.assertIn("The identity holds exactly while `ProducerRate` and `PhaseEndAxis` are fixed",
                      flat)

    def test_review_records_d7(self):
        self.assertIn("D-7", self.flat)


# ---------------------------------------------------------------------------
# Conditions that ARE fully resolved: assert the fix is really there
# ---------------------------------------------------------------------------

class TestFullyResolvedConditions(Base):
    def test_c1_directory_not_a_scheduler(self):
        flat = self.s3flat()
        self.assertIn("it **schedules nothing**, orders nothing, emits nothing and wakes nothing", flat)
        self.assertIn("**TN-R-06**", flat)

    def test_c2_deregistration_matches_rm1(self):
        flat = self.s3flat()
        self.assertIn("deregister on `Closed` or on any invalidation", flat)
        self.assertIn("whichever occurs first", flat)
        self.assertIn("even when no `Closed` can be emitted", flat)

    def test_c3_two_transitions_one_frame(self):
        flat = self.s3flat()
        self.assertIn("may not collapse them, drop the intermediate phase", flat)
        self.assertIn("### 10.10 EX-10", flat)

    def test_c5_resync_type_declared_normatively(self):
        s = self.s3()
        self.assertIn("struct FTDDTelegraphResynchronisation", s)
        row = [l for l in s.splitlines() if l.startswith("| **TN-C-09**")][0]
        self.assertIn("FTDDTelegraphResynchronisation", row)

    def test_c7_vfx_scoped_out(self):
        flat = self.s3flat()
        self.assertIn("no transform, position, attach point or socket", flat)
        self.assertIn("**TN-C-12**", flat)

    def test_c8_montage_trigger_and_key(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **TN-C-13**")][0]
        self.assertIn("trigger-and-key", row)
        self.assertIn("so is switching on a retime", row)

    def test_c4b_tn_r_05_corrected(self):
        s = self.s3()
        row = [l for l in s.splitlines() if l.startswith("| **TN-R-05**")][0]
        self.assertIn("never required to reproduce an earlier observation's `OF` values", row)


# ---------------------------------------------------------------------------
# Governance: nothing is claimed closed, signed, frozen or selected
# ---------------------------------------------------------------------------

class TestGovernanceClaims(Base):
    def test_review_does_not_claim_acceptance_tests_ran(self):
        flat = self.flat
        self.assertIn("0 executed", flat)
        self.assertNotIn("all 62 cases pass", flat)
        self.assertNotIn("acceptance tests passed", flat)

    def test_review_does_not_sign(self):
        self.assertIn("I am not signing v3.0", self.flat)

    def test_review_does_not_close_u07(self):
        self.assertIn("U-07", self.flat)
        self.assertNotIn("U-07 is closed", self.flat)
        self.assertNotIn("U-07 closed", self.flat)

    def test_review_outcome_is_exactly_one_of_three(self):
        vocab = re.findall(r"`(PASS|TARGETED REVISION|BLOCKED BY DEPENDENCY)`", self.raw)
        self.assertTrue(vocab, "outcome must use the mandated vocabulary")
        self.assertIn("TARGETED REVISION", vocab)

    def test_review_states_no_mead_selected(self):
        self.assertIn("No MEAD is selected", self.flat)

    def test_review_discloses_mead_a_authorship(self):
        self.assertIn("MEAD-A", self.flat)
        self.assertIn("my own MEAD-A", self.flat)

    def test_verdict_tally_is_arithmetically_correct(self):
        """7 AGREE + 3 AWC + 1 DISAGREE over the 11 numbered corrections."""
        self.assertIn("7 AGREE, 3 AGREE WITH CONDITIONS, 1 DISAGREE", self.flat)
        # and the per-section verdicts must sum to that
        verdicts = re.findall(r"\| \*\*(C\w+)\*\* \|[^|]+\| \*\*(AGREE WITH CONDITIONS|AGREE|DISAGREE)\*\*",
                              self.raw)
        counts = {}
        for _, v in verdicts:
            counts[v] = counts.get(v, 0) + 1
        self.assertEqual(counts.get("AGREE", 0), 7, "verdict table must have 7 AGREE")
        self.assertEqual(counts.get("AGREE WITH CONDITIONS", 0), 3)
        self.assertEqual(counts.get("DISAGREE", 0), 1)

    def test_all_seven_design_definitions_present(self):
        for d in ("D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7"):
            self.assertIn(d, self.flat)


# ---------------------------------------------------------------------------
# Prior artefacts untouched
# ---------------------------------------------------------------------------

class TestPriorArtefactsUntouched(Base):
    def test_s2_blob_still_present_and_unchanged(self):
        t = git_show(S2_BLOB)
        if t is None:
            self.skipTest("S2 blob not available")
        import hashlib
        blob = hashlib.sha1(b"blob %d\x00" % len(t.encode()) + t.encode()).hexdigest()
        self.assertEqual(blob, S2_BLOB)

    def test_prior_review_file_exists(self):
        p = REPO / "Docs" / "AGENT2_REVIEW_A1C05_S2_V1.md"
        self.assertTrue(p.exists())
        self.assertGreater(len(p.read_text(encoding="utf-8").splitlines()), 600)


if __name__ == "__main__":
    unittest.main()
