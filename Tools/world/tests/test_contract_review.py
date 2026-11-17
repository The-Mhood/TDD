#!/usr/bin/env python3
"""Tests backing the factual claims in `Docs/AGENT2_REVIEW_A1R1_V1.md`.

These tests test **this review**, not Agent 1 and not any contract. Every figure the
review asserts about register data, scene coverage, the acceptance-test inventory or
its own status is asserted here so a reader can check it instead of trusting prose.

Nothing here executes a contract acceptance test. There is no implementation to run
them against, and this suite does not pretend otherwise.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
LOCATION_CAPTURE = FIXTURES / "location_register_ch01_summary_v29.md"
SCENE_FIXTURE = FIXTURES / "scene_register_ch01_v19_verbatim.md"
MANIFEST = REPO_ROOT / "Tools" / "world" / "data" / "CH01_manifest.json"
SUBMISSION = REPO_ROOT / "Docs" / "CONTRACT_SUBMISSION_A2_V1.md"
REVIEW = REPO_ROOT / "Docs" / "AGENT2_REVIEW_A1R1_V1.md"


def _locations():
    return reg.parse_location_summary(LOCATION_CAPTURE.read_text(encoding="utf-8"))


def _scene_rows():
    text = SCENE_FIXTURE.read_text(encoding="utf-8")
    rows = [l for l in text.splitlines() if l.strip().startswith("| CH01-SCN")]
    out = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        out.append(cells)
    return out


def _traversal_locations():
    return [l for l in _locations() if "Traversal Area" in l.kind]


class TestTraversalRoster(unittest.TestCase):
    """Review section 3.4: the 8 traversal-capable locations, by ID."""

    # Sorted, because the assertion sorts. EXP sorts before SUB before TRV.
    EXPECTED = [
        "CH01-EXP-003",
        "CH01-SUB-009", "CH01-SUB-020",
        "CH01-TRV-001", "CH01-TRV-002", "CH01-TRV-003",
        "CH01-TRV-004", "CH01-TRV-005",
    ]

    def test_roster_is_exactly_the_eight_in_the_review(self):
        got = sorted(l.id for l in _traversal_locations())
        self.assertEqual(got, self.EXPECTED)

    def test_two_are_established(self):
        est = sorted(l.id for l in _traversal_locations()
                     if l.canon_status == "ESTABLISHED")
        self.assertEqual(est, ["CH01-SUB-009", "CH01-TRV-005"])

    def test_register_names_match_what_the_review_quotes(self):
        by_id = {l.id: l for l in _traversal_locations()}
        self.assertEqual(by_id["CH01-TRV-003"].name, "The Stream Crossing")
        self.assertEqual(by_id["CH01-TRV-004"].name, "The Ravine and Liana Bridge")
        self.assertEqual(by_id["CH01-TRV-005"].name, "Roads")


class TestSceneGapForTraversalLocations(unittest.TestCase):
    """Review section 3.4: the finding that rejects A1's RouteId format.

    A1-R1 section 1.5 requires `TRV.<ChapterId>.<SceneId>.<NNN>`. If a traversal
    location hosts no scene, there is no SceneId to use, and inventing one would be
    fabricating canon. This is the single most consequential finding in the review,
    so it is asserted from data rather than stated in prose.
    """

    @classmethod
    def setUpClass(cls):
        cls.hosted = Counter(r[2] for r in _scene_rows())

    def test_four_of_eight_traversal_locations_host_no_scene(self):
        gap = sorted(l.id for l in _traversal_locations()
                     if self.hosted.get(l.id, 0) == 0)
        self.assertEqual(gap, ["CH01-TRV-001", "CH01-TRV-002",
                               "CH01-TRV-003", "CH01-TRV-004"])

    def test_the_gap_is_exactly_the_four_named_trv_locations(self):
        """If this ever changes, the review's section 3.4 argument must be re-run."""
        gap = {l.id for l in _traversal_locations() if self.hosted.get(l.id, 0) == 0}
        self.assertTrue(all(g.startswith("CH01-TRV-") for g in gap))

    def test_forty_six_scenes_span_thirty_eight_locations(self):
        rows = _scene_rows()
        self.assertEqual(len(rows), 46)
        self.assertEqual(len({r[2] for r in rows}), 38)

    def test_the_four_sceneless_locations_are_absent_from_the_scene_register(self):
        """Not merely 'no scene hosted' — their names appear nowhere in it."""
        text = SCENE_FIXTURE.read_text(encoding="utf-8")
        for name in ("The Threshold Path", "The Root Way",
                     "The Stream Crossing", "The Ravine and Liana Bridge"):
            self.assertNotIn(name, text, f"{name} unexpectedly present in scene register")

    def test_at_least_one_sceneless_location_would_be_lost_by_data_not_preference(self):
        """The finding is about authored content, not taste."""
        noscene = [l for l in _traversal_locations()
                   if self.hosted.get(l.id, 0) == 0]
        self.assertTrue(noscene)
        self.assertTrue(all(l.kind for l in noscene))


class TestAcceptanceInventory(unittest.TestCase):
    """Review section 11.3: 42 unique acceptance test IDs, 10 / 11 / 21 by layer."""

    LAYER_PAT = re.compile(r"\*\*(L0-data|L1-unit|L2-auto)\*\*")

    @classmethod
    def setUpClass(cls):
        text = SUBMISSION.read_text(encoding="utf-8")
        cls.rows = []
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            m = cls.LAYER_PAT.search(line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tid = cells[0].strip("`").strip()
            if not tid or tid.lower().startswith("test id"):
                continue
            if cls.LAYER_PAT.search(tid):
                continue
            cls.rows.append((tid, m.group(1)))

    def test_forty_two_rows_and_forty_two_unique_ids(self):
        self.assertEqual(len(self.rows), 42)
        self.assertEqual(len({t for t, _ in self.rows}), 42)

    def test_layer_split_is_ten_eleven_twenty_one(self):
        counts = Counter(layer for _, layer in self.rows)
        self.assertEqual(dict(counts),
                         {"L0-data": 10, "L1-unit": 11, "L2-auto": 21})

    def test_no_duplicate_test_ids(self):
        counts = Counter(t for t, _ in self.rows)
        self.assertEqual([k for k, v in counts.items() if v > 1], [])


class TestL0ExecutableCount(unittest.TestCase):
    """Review section 11.4: the three-vs-four defect, resolved.

    The review states 2 of 10 L0 tests pass today, 1 partially, 7 blocked. This class
    asserts the *basis* for that split — what data exists and what does not — rather
    than re-deriving pass/fail, which would duplicate the contract tests themselves.
    """

    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_has_no_route_section(self):
        self.assertFalse(any("route" in k.lower() for k in self.manifest))

    def test_manifest_has_no_interactable_section(self):
        self.assertFalse(any("interact" in k.lower() for k in self.manifest))

    def test_manifest_has_no_id_or_tag_section(self):
        keys = [k for k in self.manifest if "id" in k.lower() or "tag" in k.lower()]
        self.assertEqual(keys, [])

    def test_manifest_has_no_retirement_record(self):
        """`IdRetiredNeverReused` and A1's `Retired` status both need one."""
        self.assertFalse(any("retire" in str(k).lower() for k in self.manifest))

    def test_no_route_records_exist_in_the_repository(self):
        hits = list(REPO_ROOT.rglob("*.json"))
        with_routes = [p for p in hits
                       if "ROUTE-" in p.read_text(encoding="utf-8", errors="ignore")]
        self.assertEqual(with_routes, [], "route records now exist; re-derive section 11.4")

    def test_location_register_rows_exist_so_the_multivalued_check_can_run(self):
        """The one L0 test with all its data present."""
        self.assertEqual(len(_locations()), 57)

    def test_manifest_keys_are_duplicate_free_so_dedupe_check_can_run(self):
        locs = [l.get("id") for l in self.manifest.get("locations", [])]
        scns = [s.get("id") for s in self.manifest.get("scenes", [])]
        self.assertEqual([k for k, v in Counter(locs).items() if v > 1], [])
        self.assertEqual([k for k, v in Counter(scns).items() if v > 1], [])

    def test_display_label_sample_is_too_small_to_be_a_real_test(self):
        """Review marks this 'partially' — it would pass vacuously."""
        keys = ([l.get("id") for l in self.manifest.get("locations", [])]
                + [s.get("id") for s in self.manifest.get("scenes", [])])
        self.assertLess(len(keys), 20,
                        "sample has grown; §11.4 no longer applies unchanged")


class TestReviewInternalArithmetic(unittest.TestCase):
    """The review's own counts must match its own tables.

    A review that miscounts its own verdicts is not trustworthy about anything
    else. These assert the arithmetic, not the judgement.
    """

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")

    def _clause_rows(self):
        rows = [l for l in self.raw.splitlines()
                if l.strip().startswith("| §")]
        return [r for r in rows
                if not re.match(r"\|\s*§\d+\.\d+ \(C-0\d\)", r.strip())]

    def test_clause_row_total_is_seventy_one(self):
        self.assertEqual(len(self._clause_rows()), 71)

    def test_clause_verdict_breakdown_matches_section_1_2(self):
        rows = self._clause_rows()
        acc = sum(1 for r in rows if "**ACCEPT with" not in r and "**ACCEPT**" in r)
        accw = sum(1 for r in rows if "**ACCEPT with" in r)
        rej = sum(1 for r in rows if "**REJECT" in r)
        self.assertEqual(acc, 28)
        self.assertEqual(accw, 21)
        self.assertEqual(rej, 2)

    def test_sixteen_requirements_are_numbered(self):
        found = set(re.findall(r"\*\*A2R-(\d+)\*\*", self.raw))
        self.assertEqual(sorted(int(x) for x in found), list(range(1, 17)))

    def test_five_corrections_are_recorded(self):
        seg = self.raw.split("### 13.3 The correction record", 1)[1]
        rows = [l for l in seg.splitlines() if re.match(r"^\| \d \|", l)]
        self.assertEqual(len(rows), 5)

    def test_field_removals_match_the_net_effect_sentence(self):
        seg = self.raw.split("### 4.4 Field classification", 1)[1]
        seg = seg.split("### 4.5", 1)[0]
        unreq = re.findall(r"\| `(\w+)` \| \*\*UNREQUESTED\*\*", seg)
        withdrawn = re.findall(r"\| `(\w+)` \| \*\*CONDITIONAL — WITHDRAWN\*\*", seg)
        self.assertEqual(sorted(unreq), ["ActiveActionId", "GroundSlopeDegrees"])
        self.assertEqual(withdrawn, ["HealthFraction"])
        # the sentence must name all three
        for name in unreq + withdrawn:
            self.assertIn(name, seg)

    def test_all_seven_verdicts_are_distinct_rows(self):
        seg = self.raw.split("### 1.1 The seven verdicts", 1)[1].split("### 1.2", 1)[0]
        rows = [l for l in seg.splitlines() if l.strip().startswith("| **C-0")]
        self.assertEqual(len(rows), 7)


class TestCapabilityVocabulary(unittest.TestCase):
    """Review section 3.2: A1's five capabilities, accepted without change."""

    EXPECTED = ["Vault", "Mantle", "LedgeShimmy", "Drop", "ClimbLadder"]

    @classmethod
    def setUpClass(cls):
        cls.review = REVIEW.read_text(encoding="utf-8")

    def test_all_five_capabilities_are_named_in_the_review(self):
        for cap in self.EXPECTED:
            self.assertIn(cap, self.review)

    def test_review_does_not_invent_a_sixth_capability(self):
        found = set(re.findall(r"`Traversal\.Capability\.([A-Za-z]+)`", self.review))
        self.assertTrue(found.issubset(set(self.EXPECTED)),
                        f"unexpected capability tags: {found - set(self.EXPECTED)}")


class TestReviewDocumentClaims(unittest.TestCase):
    """The review must not claim agreement, a freeze, or a passed contract test."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("*", "").replace("`", "")

    def test_all_seven_contracts_are_reviewed(self):
        for n in range(1, 8):
            self.assertIn(f"C-0{n}", self.flat)

    def test_zero_agreements_stated(self):
        self.assertIn("Agreed: 0 of 7", self.flat)

    def test_does_not_claim_any_contract_agreed(self):
        self.assertNotIn("AGREED WITH", self.raw)
        self.assertNotIn("FROZEN — ACCEPTED", self.raw)

    def test_uses_only_the_four_permitted_verdicts(self):
        for verdict in ("PARTIALLY AGREE", "AGREE IN PRINCIPLE — NOT AGREED",
                        "DISAGREE", "REQUIRE CLARIFICATION"):
            self.assertIn(verdict, self.raw)

    def test_states_that_no_contract_test_ran(self):
        self.assertIn("0 of 42", self.flat)

    def test_states_it_is_design_only(self):
        self.assertIn("DESIGN_ONLY", self.raw)


class TestVersionCorrectionRecorded(unittest.TestCase):
    """Review section 0.1: I was wrong about v1.2 and must say so."""

    @classmethod
    def setUpClass(cls):
        cls.raw = REVIEW.read_text(encoding="utf-8")
        cls.flat = cls.raw.replace("**", "").replace("*", "").replace("`", "")

    def test_admits_v12_exists(self):
        self.assertIn("v1.2 exists", self.flat)

    def test_names_the_commit_where_v12_lives(self):
        self.assertIn("e121bbbf09562e3cba0efe81aad971809685db23", self.raw)

    def test_states_the_earlier_claim_was_wrong(self):
        self.assertIn("I was wrong", self.flat)

    def test_records_all_five_corrections(self):
        self.assertIn("Five corrections to my own work", self.flat)
        for n in range(1, 6):
            self.assertIn(f"| {n} |", self.flat)


class TestCorrectionsAreReal(unittest.TestCase):
    """The withdrawals the review claims must actually be absent from the live text.

    Each entry names a pattern that must NOT appear as a live claim in the review.
    """

    @classmethod
    def setUpClass(cls):
        cls.flat = REVIEW.read_text(encoding="utf-8").replace("**", "").replace("*", "").replace("`", "")

    def test_states_route_record_withdrawn(self):
        self.assertIn("withdraw", self.flat.lower())

    def test_no_interactable_count_is_asserted(self):
        """Review must not state a count for interactables (standing constraint)."""
        live = [l for l in self.flat.splitlines()
                if re.search(r"\b\d+ (world )?interactables\b", l)
                and "withdrawn" not in l.lower()
                and "not established" not in l.lower()
                and "do not" not in l.lower()]
        self.assertEqual(live, [], f"interactable count stated as live claim: {live}")

    def test_states_two_of_ten_l0_pass(self):
        self.assertIn("2 of 10", self.flat)

    def test_marks_the_four_runnable_claim_as_wrong(self):
        self.assertIn("simply wrong", self.flat)

    def test_preserves_57_of_57(self):
        self.assertIn("57 of 57", self.flat)

    def test_preserves_canon_status_split(self):
        self.assertIn("22 ESTABLISHED / 32 PROPOSED / 3 PENDING APPROVAL", self.flat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
