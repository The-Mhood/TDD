#!/usr/bin/env python3
"""Tests for the W-M2.2 ambient-scene NPC data capture.

WHAT THIS FILE GUARDS
---------------------
The capture replaced twelve policy-default NPC counts with register data. Three
things about that work are easy to get silently wrong later, so each has a
regression test here:

1.  The previous fixture (`scene_register_ch01_full.md`) is PRESERVED and still
    produces the W-M2.1 baseline exactly. Superseding a source must not destroy
    the ability to reproduce the earlier report.
2.  The abridged fixture's NPC prose diverges from the register. Its
    CH01-SCN-017 reads "Three adults." where the register reads "Six to ten
    adults; Unoka (storyteller) some days." That divergence is asserted, not
    merely documented, so it cannot quietly disappear.
3.  The parser must REFUSE prose it cannot resolve rather than inventing a
    number. The old parser turned "Six to ten adults" into 16 and
    "Family of eight across three generations" into 11. Both are asserted as
    bugs that must never come back.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))
sys.path.insert(0, str(REPO_ROOT / "Tools" / "world"))

import population_budget as pb  # noqa: E402
import registers as reg  # noqa: E402

FIXTURES = REPO_ROOT / "Tools" / "canon" / "tests" / "fixtures"
VERBATIM = FIXTURES / "scene_register_ch01_v19_verbatim.md"
ABRIDGED = FIXTURES / "scene_register_ch01_full.md"


def setUpModule() -> None:  # noqa: N802
    global POLICY, OLD_BUDGET, NEW_BUDGET, NEW_TEXT, OLD_TEXT
    POLICY = pb.load_policy()
    OLD_TEXT = ABRIDGED.read_text(encoding="utf-8")
    NEW_TEXT = VERBATIM.read_text(encoding="utf-8")
    OLD_BUDGET = pb.build_chapter_budget(
        reg.parse_scene_summary(OLD_TEXT), reg.parse_scene_details(OLD_TEXT),
        POLICY, "CH01")
    NEW_BUDGET = pb.build_chapter_budget(
        reg.parse_scene_summary(NEW_TEXT), reg.parse_scene_details(NEW_TEXT),
        POLICY, "CH01")


def _by_id(budget):
    return {s.scene_id: s for s in budget.scenes}


class TestSourcesArePreserved(unittest.TestCase):
    """Requirement 8: no destructive overwrites."""

    def test_both_fixtures_exist(self):
        self.assertTrue(ABRIDGED.is_file(), "the previous fixture must be preserved")
        self.assertTrue(VERBATIM.is_file(), "the verbatim capture must exist")

    def test_both_fixtures_cover_the_same_46_scenes(self):
        old = {s.id for s in reg.parse_scene_summary(OLD_TEXT)}
        new = {s.id for s in reg.parse_scene_summary(NEW_TEXT)}
        self.assertEqual(len(old), 46)
        self.assertEqual(old, new)

    def test_previous_baseline_is_still_reproducible(self):
        """The W-M2.1 headline must remain derivable from the file it came from."""
        self.assertEqual(OLD_BUDGET.total_cost_units, 36.58)
        self.assertEqual(OLD_BUDGET.simulated_npcs_lower, 30)
        self.assertEqual(OLD_BUDGET.simulated_npcs_upper, 49)
        self.assertEqual(OLD_BUDGET.npcs_provenance_summary,
                         {"POLICY_DEFAULT": 41, "REGISTER_DATA": 5})

    def test_every_verbatim_block_matches_the_harvest_record(self):
        """The fixture and the harvest record are the same data in two places.

        If they disagree, one of them was edited by hand and the capture lost
        its provenance. Checking both directions also catches an orphan block
        that no harvest window ever produced.
        """
        import json
        import re
        harvest = json.loads(
            (REPO_ROOT / "Tools" / "world" / "data" / "_harvest_progress.json")
            .read_text(encoding="utf-8"))["verbatim_npcs_present"]
        assert harvest, "the harvest record is empty"

        text = VERBATIM.read_text(encoding="utf-8")
        blocks, current = {}, None
        for line in text.splitlines():
            m = re.match(r"^### (CH01-SCN-\d{3})", line)
            if m:
                current = m.group(1)
                continue
            m = re.match(r"^- \*\*NPCs present\.\*\*\s*(.+)$", line)
            if m and current:
                blocks[current] = m.group(1).strip()

        self.assertEqual(len(blocks), len(harvest),
                         "fixture and harvest hold a different number of blocks")
        self.assertEqual(sorted(blocks), sorted(harvest),
                         "a block exists in one record but not the other")
        for scene_id, expected in harvest.items():
            self.assertEqual(blocks[scene_id], expected,
                             f"{scene_id}: fixture text diverges from the harvest")

    def test_abridged_fixture_is_byte_for_byte_the_committed_version(self):
        """A hash pin, not a promise.

        The capture's whole claim to trustworthiness is that it did not destroy
        the evidence the previous milestone rested on. Recording the digest means
        an accidental in-place edit fails the suite instead of silently making
        W-M2.1 unreproducible. If this fixture ever legitimately changes, the
        digest must be updated deliberately and the reproduction test re-run.
        """
        import hashlib
        digest = hashlib.sha256(ABRIDGED.read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            "4c3f9a45bd75d5b261237bb2b8ce0d4bf9622fea08c8db17203517ebe3b570f7",
            "the abridged fixture changed - W-M2.1 reproduction is now in doubt")

    def test_abridged_fixture_is_the_smaller_capture(self):
        old = reg.parse_scene_details(OLD_TEXT)
        new = reg.parse_scene_details(NEW_TEXT)
        self.assertEqual(len(old), 5)
        self.assertEqual(len(new), 35)


class TestFixtureDivergesFromRegister(unittest.TestCase):
    """The finding: the old fixture is abridged, and wrong about SCN-017."""

    def test_scn017_abridged_text_says_three_adults(self):
        old = {d.id: d for d in reg.parse_scene_details(OLD_TEXT)}
        self.assertEqual(old["CH01-SCN-017"].npcs_present, "Three adults.")

    def test_scn017_verbatim_text_is_a_range_with_a_conditional(self):
        new = {d.id: d for d in reg.parse_scene_details(NEW_TEXT)}
        self.assertEqual(new["CH01-SCN-017"].npcs_present,
                         "Six to ten adults; Unoka (storyteller) some days.")

    def test_the_two_sources_disagree_for_scn017(self):
        old = {d.id: d for d in reg.parse_scene_details(OLD_TEXT)}
        new = {d.id: d for d in reg.parse_scene_details(NEW_TEXT)}
        self.assertNotEqual(old["CH01-SCN-017"].npcs_present,
                            new["CH01-SCN-017"].npcs_present,
                            "the divergence between abridged and verbatim must be visible")

    def test_the_divergence_moves_the_derived_count(self):
        old = _by_id(OLD_BUDGET)["CH01-SCN-017"]
        new = _by_id(NEW_BUDGET)["CH01-SCN-017"]
        self.assertEqual(old.npcs_provenance, "REGISTER_DATA")
        self.assertEqual(old.npcs_from_register, 3)
        # The verbatim prose is unresolved, so the count must NOT be a point value.
        self.assertEqual(new.npcs_provenance, "UNPARSED")
        self.assertEqual(new.npcs_from_register, 0)


class TestParserRefusesRatherThanInvents(unittest.TestCase):
    """The two silent-corruption bugs found during the capture."""

    def test_range_is_not_summed(self):
        """"Six to ten adults" must never become 16."""
        count, _child, parsed = reg.parse_npc_count(
            "Six to ten adults; Unoka (storyteller) some days.")
        self.assertFalse(parsed, "a range is not a point count")
        self.assertNotEqual(count, 16, "6 + 10 was the old, wrong behaviour")

    def test_alternative_is_not_summed(self):
        """"Four or five men" must never become 9."""
        count, _child, parsed = reg.parse_npc_count("Four or five men.")
        self.assertFalse(parsed)
        self.assertNotEqual(count, 9)

    def test_abstract_number_is_not_a_person(self):
        """"eight across three generations" must never become 11."""
        count, _child, parsed = reg.parse_npc_count(
            "Family of eight across three generations.")
        self.assertNotEqual(count, 11, "counting a generation as a person was the old bug")
        self.assertTrue(parsed, "eight family members IS a readable head-count")
        self.assertEqual(count, 8)

    def test_vague_quantities_are_refused(self):
        # "A dozen people." was moved OUT of this list by TD correction 1: it is
        # a definite quantity (12), not a vague one. It is asserted as an exact
        # count in TestDozenIsExact below. "Dozens" remains indefinite and stays.
        for text in ("Sometimes one cook.", "Occasional passer-by.",
                     "Dozens of people.", "A dozen or so.",
                     "A line of women and girls filling pots and lifting "
                     "them onto head-pads, talking."):
            with self.subTest(text=text):
                self.assertFalse(reg.parse_npc_count(text)[2],
                                 f"{text!r} states no exact head-count")

    def test_refusal_never_becomes_a_measured_zero(self):
        """Requirement: never silently convert missing data to zero."""
        for text in ("Six to ten adults.", "Sometimes a traveller."):
            with self.subTest(text=text):
                _count, _child, parsed = reg.parse_npc_count(text)
                self.assertFalse(parsed)


class TestNamedNpcConvention(unittest.TestCase):
    """The register names single NPCs as "Name (role)". That is one person."""

    def test_named_role_is_one_person(self):
        for text in ("Mgbafo (village elder).", "Okorie (royal guard).",
                     "Akuebue (merchant).", "Ogbuagu (hunter)."):
            with self.subTest(text=text):
                self.assertEqual(reg.parse_npc_count(text)[:2], (1, False))

    def test_named_plus_numeral_sums(self):
        self.assertEqual(reg.parse_npc_count("Omenka (blacksmith), one apprentice.")[:2],
                         (2, False))
        self.assertEqual(reg.parse_npc_count("Ojiugo (healer), one patient.")[:2],
                         (2, False))
        self.assertEqual(reg.parse_npc_count("Mgborie (palace servant), two guards.")[:2],
                         (3, False))


class TestBandsComeFromTheRegister(unittest.TestCase):
    """A bound the register states is register data, not an assumption."""

    def test_stated_range(self):
        self.assertEqual(reg.parse_npc_band("Six to ten adults.")[:2], (6, 10))

    def test_stated_alternative(self):
        self.assertEqual(reg.parse_npc_band("Four or five men.")[:2], (4, 5))

    def test_conditional_presence(self):
        self.assertEqual(reg.parse_npc_band("Sometimes one cook.")[:2], (0, 1))

    def test_conditional_singular_person(self):
        self.assertEqual(reg.parse_npc_band("Occasional passer-by.")[:2], (0, 1))
        self.assertEqual(reg.parse_npc_band("Sometimes a traveller.")[:2], (0, 1))

    def test_a_dozen_is_twelve(self):
        self.assertEqual(reg.parse_npc_band("A dozen people.")[:2], (12, 12))

    def test_collective_without_a_number_has_no_bound(self):
        low, high, basis = reg.parse_npc_band(
            "A line of women and girls filling pots and lifting them onto "
            "head-pads, talking.")
        self.assertIsNone(low)
        self.assertIsNone(high)
        self.assertIn("no bound", basis)

    def test_settled_scene_band_is_a_point(self):
        self.assertEqual(reg.parse_npc_band("One woman, one child.")[:2], (2, 2))


class TestCaptureOutcomes(unittest.TestCase):
    """What the capture actually changed, stated exactly."""

    def test_all_fourteen_crowd_scenes_now_have_register_prose(self):
        crowd = [s for s in NEW_BUDGET.scenes if s.tier == "CROWD"]
        self.assertEqual(len(crowd), 14)
        for scene in crowd:
            with self.subTest(scene=scene.scene_id):
                self.assertNotEqual(scene.npcs_source, "policy_default",
                                    "no CROWD scene may still rest on a policy default")

    def test_provenance_moved_substantially(self):
        before = OLD_BUDGET.npcs_provenance_summary
        after = NEW_BUDGET.npcs_provenance_summary
        self.assertEqual(before["REGISTER_DATA"], 5)
        self.assertEqual(after["REGISTER_DATA"], 29)
        self.assertEqual(before["POLICY_DEFAULT"], 41)
        self.assertEqual(after["POLICY_DEFAULT"], 11)

    def test_unresolved_scenes_are_named_not_zeroed(self):
        # CH01-SCN-018 "A dozen people." left this set in W-M2.3: it resolves to
        # exactly 12 (TD correction 1), so it is no longer unresolved.
        expected = {"CH01-SCN-005", "CH01-SCN-014", "CH01-SCN-017",
                    "CH01-SCN-020", "CH01-SCN-021", "CH01-SCN-034"}
        self.assertEqual(set(NEW_BUDGET.unparsed_npc_scenes), expected)

    def test_the_band_is_open_where_no_bound_is_stated(self):
        """CH01-SCN-014 is a collective with no number: the band cannot close."""
        self.assertFalse(NEW_BUDGET.band_is_complete)
        self.assertEqual(NEW_BUDGET.npcs_band_summary["scenes_without_any_bound"],
                         ["CH01-SCN-014"])

    def test_point_estimate_understates_the_banded_estimate(self):
        """The headline is a FLOOR, not a best guess."""
        self.assertLess(NEW_BUDGET.total_cost_units, NEW_BUDGET.band_cost_units_high)
        self.assertAlmostEqual(NEW_BUDGET.band_cost_units_low, 38.38, places=2)

    def test_scn002_raises_the_count_to_eight(self):
        scene = _by_id(NEW_BUDGET)["CH01-SCN-002"]
        self.assertEqual(scene.npcs_from_register, 8)
        self.assertEqual(scene.npcs_provenance, "REGISTER_DATA")

    def test_scn030_is_three_people(self):
        scene = _by_id(NEW_BUDGET)["CH01-SCN-030"]
        self.assertEqual(scene.npcs_from_register, 3)


class TestTdConstraintsHold(unittest.TestCase):
    """The standing W-M2 constraints survive the capture."""

    def test_no_chapter_2_to_8_data_is_used(self):
        ids = {s.scene_id for s in NEW_BUDGET.scenes}
        self.assertTrue(all(i.startswith("CH01-SCN-") for i in ids))
        self.assertFalse(any(i.startswith(("CH02", "CH03", "CH04", "CH05",
                                           "CH06", "CH07", "CH08")) for i in ids))

    def test_the_model_is_still_provisional(self):
        self.assertEqual(OLD_BUDGET.by_tier, NEW_BUDGET.by_tier,
                         "the capture must not change the tier model itself")

    def test_the_tier_partition_is_unchanged(self):
        self.assertEqual(NEW_BUDGET.by_tier,
                         {"CROWD": 14, "NAMED": 1, "NONE": 12, "SCRIPTED": 19})

    def test_children_are_never_combat_targets(self):
        for scene in NEW_BUDGET.scenes:
            if scene.has_child:
                with self.subTest(scene=scene.scene_id):
                    self.assertTrue(any("CHILDREN-NO-COMBAT" in n for n in scene.notes))

    def test_it_is_not_described_as_a_measurement(self):
        self.assertEqual(NEW_BUDGET.scenes_total, 46)
        # Nothing in this module may claim to be measured.
        for scene in NEW_BUDGET.scenes:
            self.assertFalse(getattr(scene, "is_measured", False))


class TestDozenIsExact(unittest.TestCase):
    """TD correction 1: "A dozen people." is twelve, not an unresolved range.

    The W-M2.2 parser refused it because "dozen" sat in the vague-word list,
    which conflated "a dozen" (definite) with "dozens" (indefinite). The two
    differ by one letter and by whether the register has pinned the number down.
    """

    def test_dozen_is_twelve(self):
        for text in ("A dozen people.", "A dozen.", "a dozen", "One dozen people."):
            with self.subTest(text=text):
                count, _has_child, parsed = reg.parse_npc_count(text)
                self.assertTrue(parsed, f"{text!r} must parse")
                self.assertEqual(count, 12)

    def test_scn018_is_an_exact_register_count(self):
        row = {s.scene_id: s for s in NEW_BUDGET.scenes}["CH01-SCN-018"]
        self.assertEqual(row.npcs_source, "register")
        self.assertEqual(row.npcs_provenance, "REGISTER_DATA")
        self.assertEqual(row.npcs_from_register, 12)
        self.assertNotIn("CH01-SCN-018", NEW_BUDGET.unparsed_npc_scenes)

    def test_dozen_variants_are_not_all_twelve(self):
        """A loose regex here would silently misprice two of these."""
        cases = {
            "Half a dozen women.": 6,
            "Two dozen men.": 24,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(reg.parse_npc_count(text)[0], expected)
                self.assertEqual(reg.parse_npc_band(text)[:2], (expected, expected))

    def test_indefinite_quantities_are_still_refused(self):
        """The correction must not become a licence to guess."""
        for text in ("Dozens of people.", "A dozen or so.", "Several dozen farmers."):
            with self.subTest(text=text):
                self.assertFalse(reg.parse_npc_count(text)[2],
                                 f"{text!r} is indefinite and must not parse")

    def test_point_count_and_band_never_disagree(self):
        """If these two disagree, one screen says 12 and another says 6."""
        texts = ("A dozen people.", "Half a dozen women.", "Two dozen men.",
                 "A dozen or so.", "Dozens of people.",
                 "Six to ten adults.", "Four or five men.",
                 "Sometimes one cook.", "Family of eight across three generations.",
                 "One woman, one child.", "None.")
        for text in texts:
            with self.subTest(text=text):
                count, _h, parsed = reg.parse_npc_count(text)
                low, high, _b = reg.parse_npc_band(text)
                if parsed:
                    # An exact count must agree with its own band exactly.
                    self.assertEqual((low, high), (count, count),
                                     f"{text!r}: point={count} band=({low},{high})")
                elif low is not None:
                    # A refused field MAY carry a bound - that is what the band
                    # is for. But the bound must be a real interval, and the
                    # exact count must not sit outside it.
                    self.assertLessEqual(low, high,
                                         f"{text!r}: inverted band ({low},{high})")
                    self.assertNotEqual(low, high,
                                        f"{text!r}: refused an exact count it could "
                                        f"have read as {low}")
                else:
                    # No bound at all is also valid: the register stated a
                    # collective with no number ("a line of women and girls").
                    self.assertIsNone(high, f"{text!r}: half-open bound")


class TestRangeBudgetingRule(unittest.TestCase):
    """The TD's modelling decision, encoded where it can be checked.

    Endpoints have distinct jobs. If a midpoint ever appears, or if a derived
    cost is ever described as runtime performance, the rule has been broken.
    """

    @staticmethod
    def _band_rows():
        import json
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2"
             / "CH01_population_budget.json").read_text(encoding="utf-8"))
        return data["budget"]["npcs_band_summary"]["detail"]

    def test_both_endpoints_are_preserved(self):
        for row in self._band_rows():
            low, high = row["npcs_band"]
            self.assertIsNotNone(low, row["scene_id"])
            self.assertIsNotNone(high, row["scene_id"])
            self.assertLessEqual(low, high, row["scene_id"])

    def test_original_register_wording_is_preserved(self):
        """A reader must be able to check an endpoint against the source."""
        import json
        harvest = json.loads(
            (REPO_ROOT / "Tools" / "world" / "data" / "_harvest_progress.json")
            .read_text(encoding="utf-8"))["verbatim_npcs_present"]
        for row in self._band_rows():
            self.assertEqual(row["register_wording"],
                             harvest[row["scene_id"]],
                             f"{row['scene_id']}: band row must quote the register "
                             f"verbatim, not a paraphrase")

    def test_no_midpoint_is_used(self):
        for row in self._band_rows():
            self.assertIs(row["midpoint_used"], False, row["scene_id"])

    def test_endpoint_roles_are_stated(self):
        for row in self._band_rows():
            self.assertIn("lower", row["endpoint_use"]["low"].lower())
            self.assertIn("capacity", row["endpoint_use"]["high"].lower())

    def test_no_source_file_computes_a_midpoint(self):
        """A guard against a future 'helpful' simplification."""
        import re
        for path in (REPO_ROOT / "Tools").rglob("*.py"):
            if "test" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in (r"midpoint\s*=", r"\(\s*lo\w*\s*\+\s*hi",
                            r"\(\s*low\s*\+\s*high"):
                self.assertIsNone(re.search(pattern, text),
                                  f"{path.name} appears to compute a midpoint of the "
                                  f"band, which the TD's rule forbids")


class TestMeasurementIsNotProvenance(unittest.TestCase):
    """TD correction 2.

    A count authored in the register is DATA transcribed from a design
    document. A measurement is an observation of a running build. Nothing in
    this repository has been observed, so no row may claim to be measured -
    including a row that is faithfully REGISTER_DATA.
    """

    def test_no_scene_claims_to_be_measured(self):
        offenders = [s.scene_id for s in NEW_BUDGET.scenes if s.npcs_is_measured]
        self.assertEqual(offenders, [],
                         "no engine has run; nothing may be marked measured")

    def test_register_rows_are_still_marked_as_register_provenance(self):
        """is_measured=False must NOT be implemented by weakening provenance."""
        rows = [s for s in NEW_BUDGET.scenes if s.npcs_source == "register"]
        self.assertEqual(len(rows), 29)
        for row in rows:
            self.assertEqual(row.npcs_provenance, "REGISTER_DATA", row.scene_id)
            self.assertFalse(row.npcs_is_measured, row.scene_id)

    def test_generated_json_carries_false_not_null(self):
        """A missing key reads as 'unknown', which is also wrong. It must be a
        literal false so a consumer can assert on it directly."""
        import json
        data = json.loads(
            (REPO_ROOT / "Docs" / "evidence" / "agent2"
             / "CH01_population_budget.json").read_text(encoding="utf-8"))
        for scene in data["budget"]["scenes"]:
            self.assertIn("npcs_is_measured", scene, scene.get("scene_id"))
            self.assertIs(scene["npcs_is_measured"], False, scene.get("scene_id"))

    def test_gate_rejects_a_row_claiming_to_be_measured(self):
        """The gate must FAIL on an injected true, not merely omit it.

        Without this the field could rot to True and every test would still
        pass, because none of them reads the field the gate checks.
        """
        import json
        import subprocess
        import sys
        artifact = (REPO_ROOT / "Docs" / "evidence" / "agent2"
                    / "CH01_population_budget.json")
        original = artifact.read_text(encoding="utf-8")
        self.addCleanup(artifact.write_text, original, encoding="utf-8")

        data = json.loads(original)
        target = next(s for s in data["budget"]["scenes"]
                      if s["npcs_provenance"] == "REGISTER_DATA")
        target["npcs_is_measured"] = True
        artifact.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "Tools" / "ci" / "l0_checks.py"),
             "--verbose"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertNotEqual(proc.returncode, 0,
                            "the provenance gate accepted a measured=True row")
        self.assertIn(target["scene_id"], proc.stdout + proc.stderr)


class TestDocsAgreeWithCorrection(unittest.TestCase):
    """Doc/code drift has been caught three times in this project. The capture
    classification is quoted in prose in several documents, so it is pinned."""

    DOCS = ("REGISTER_INGESTION.md", "DEPENDENCY_AND_BLOCKER_REGISTER.md")

    def test_docs_quote_the_corrected_classification(self):
        summary = NEW_BUDGET.npcs_provenance_summary
        self.assertEqual(summary["REGISTER_DATA"], 29)
        self.assertEqual(summary["UNPARSED"], 6)
        for name in self.DOCS:
            text = (REPO_ROOT / "Docs" / name).read_text(encoding="utf-8")
            self.assertIn("29", text, f"{name} must state 29 exact")
            self.assertNotIn("28 reduce to an exact head-count", text,
                             f"{name} still quotes the superseded W-M2.2 figure")

    def test_no_doc_says_seven_unresolved(self):
        for name in self.DOCS:
            text = (REPO_ROOT / "Docs" / name).read_text(encoding="utf-8")
            self.assertNotIn("7 state a range", text, name)
            self.assertNotIn("A further 7 scenes", text, name)


if __name__ == "__main__":
    unittest.main()
