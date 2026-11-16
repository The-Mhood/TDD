#!/usr/bin/env python3
"""L0 canon validation tests (stdlib unittest only).

Run:  python3 -m unittest discover -s Tools/canon/tests -v
   or python3 Tools/canon/tests/test_canon.py

Design principle: a validator that only ever sees correct data is untested.
Most tests here mutate a *copy* of the real index into a known-invalid state and
assert that the specific expected error is produced. That is how we prove the
gate would actually stop bad canon data from reaching the game.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "Tools" / "canon"))

import canon_index as ci  # noqa: E402
import registers as reg  # noqa: E402


def setUpModule() -> None:  # noqa: N802 - unittest naming
    global BASE_INDEX, BASE_SCHEMA
    BASE_INDEX = ci.load_index()
    BASE_SCHEMA = ci.load_schema()


def fresh():
    return copy.deepcopy(BASE_INDEX)


class TestIndexIsValid(unittest.TestCase):
    """The real shipped index must be clean."""

    def test_index_passes_all_checks(self):
        errors = ci.validate_index(BASE_INDEX, BASE_SCHEMA)
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_schema_uses_only_supported_keywords(self):
        # Guards the hand-rolled validator: if the schema grows a keyword the
        # validator ignores, validation would silently pass. Fail loudly instead.
        problems = ci._warn_unsupported_keywords(BASE_SCHEMA)
        self.assertEqual(problems, [])

    def test_schema_is_valid_json_and_declares_draft07(self):
        self.assertIn("$schema", BASE_SCHEMA)
        self.assertIn("draft-07", BASE_SCHEMA["$schema"])

    def test_index_is_valid_json_with_expected_top_level_keys(self):
        for key in ci.REQUIRED_KEYS:
            self.assertIn(key, BASE_INDEX)


class TestChapters(unittest.TestCase):
    def test_eight_chapters_in_order(self):
        chapters = BASE_INDEX["chapters"]
        self.assertEqual(len(chapters), 8)
        self.assertEqual([c["index"] for c in chapters], list(range(1, 9)))
        self.assertEqual([c["id"] for c in chapters], list(ci.CHAPTER_IDS))

    def test_chapter_names_match_directive(self):
        expected = {
            "CH01": "Forbidden Forest",
            "CH02": "Kingdom Beneath the Earth",
            "CH03": "City of the Living Dead",
            "CH04": "River of Idemili",
            "CH05": "Mountain of Thunder",
            "CH06": "Kingdom of Masks",
            "CH07": "Gates of the Dead",
        }
        by_id = {c["id"]: c["name"] for c in BASE_INDEX["chapters"]}
        for ch, name in expected.items():
            self.assertEqual(by_id[ch], name)
        self.assertIn("Last Daughter", by_id["CH08"])

    def test_chapter_boss_names_match_directive(self):
        by_id = {c["id"]: c["boss"] for c in BASE_INDEX["chapters"]}
        self.assertEqual(by_id["CH01"], "Great Root Mother")
        self.assertEqual(by_id["CH02"], "Iron Elephant")
        self.assertEqual(by_id["CH03"], "King Without a Face")
        self.assertEqual(by_id["CH04"], "Daughter of the Deep")
        self.assertEqual(by_id["CH08"], "Ezeani")

    def test_missing_chapter_is_rejected(self):
        idx = fresh()
        idx["chapters"].pop()
        errors = ci.validate_chapters(idx)
        self.assertTrue(errors, "a 7-chapter index must not validate")

    def test_duplicate_chapter_index_is_rejected(self):
        idx = fresh()
        idx["chapters"][1]["index"] = 1
        self.assertTrue(ci.validate_chapters(idx))


class TestStatusSeparation(unittest.TestCase):
    """OAD-47 / OAD-48: design approval is not canon approval.

    v1.0.0 of this index modelled approval as a {design, canon, shippable}
    triplet. Reading LOCATION_MASTER_REGISTER v2.9 showed the registers use
    THREE canon statuses (ESTABLISHED / PROPOSED / PENDING APPROVAL) plus a
    SEPARATE seven-value environment design status. v2.0.0 follows the register.
    These tests pin that model so it cannot silently drift back.
    """

    def test_canon_status_vocabulary_matches_register(self):
        self.assertEqual(
            tuple(BASE_INDEX["canon_statuses"]),
            ("ESTABLISHED", "PROPOSED", "PENDING APPROVAL"),
        )

    def test_design_and_canon_axes_are_disjoint(self):
        for value in BASE_INDEX["environment_design_statuses"]:
            self.assertNotIn(value, BASE_INDEX["canon_statuses"],
                             f"{value!r} must not appear in both axes")

    def test_environment_design_status_vocabulary_matches_register(self):
        self.assertEqual(
            tuple(BASE_INDEX["environment_design_statuses"]),
            ("NOT STARTED", "EXPLORATORY", "IN REVIEW", "REQUIRES REVISION",
             "CONDITIONAL", "APPROVED", "REJECTED"),
        )

    def test_invented_canon_status_is_rejected(self):
        idx = fresh()
        idx["locations"][0]["canon_status"] = "CanonApproved"
        errors = ci.validate_status_separation(idx)
        self.assertTrue(any("not a register value" in e for e in errors), errors)

    def test_unverified_status_requires_unverified_flag(self):
        idx = fresh()
        unverified = next(l for l in idx["locations"] if l["canon_status"] == "UNVERIFIED")
        unverified["verified_against_register"] = True
        errors = ci.validate_status_separation(idx)
        self.assertTrue(any("inconsistent" in e for e in errors), errors)

    def test_verified_status_cannot_be_unverified_marker(self):
        idx = fresh()
        verified = next(l for l in idx["locations"] if l["verified_against_register"])
        verified["canon_status"] = "UNVERIFIED"
        errors = ci.validate_status_separation(idx)
        self.assertTrue(any("inconsistent" in e for e in errors), errors)

    def test_memory_one_location_is_proposed_not_established_dup_head(self):
        """The Wayside Offering Place must never be presented as canon."""
        loc = next(l for l in BASE_INDEX["locations"] if l["id"] == "CH01-SUB-018")
        self.assertEqual(loc["canon_status"], "PROPOSED")
        self.assertEqual(loc["env_design_status"], "NOT STARTED")

    def test_chapter1_boss_arena_is_established_canon_but_design_in_review(self):
        """OAD-21: encounter established, arena design not approved."""
        loc = next(l for l in BASE_INDEX["locations"] if l["id"] == "CH01-BOS-001")
        self.assertEqual(loc["canon_status"], "ESTABLISHED")
        self.assertEqual(loc["env_design_status"], "IN REVIEW")

    def test_chapter8_approved_designs_are_still_not_canon(self):
        """OAD-45 approved four Chapter 8 designs for composition work; OAD-47/48
        confirmed that does not make the places canon."""
        ch8 = [l for l in BASE_INDEX["locations"] if l["chapter"] == "CH08"]
        self.assertTrue(ch8)
        approved = [l for l in ch8 if l["env_design_status"] == "APPROVED"]
        self.assertTrue(approved, "expected the OAD-45 approved designs to be recorded")
        for loc in ch8:
            self.assertNotEqual(loc["canon_status"], "ESTABLISHED", loc["id"])


class TestMemories(unittest.TestCase):
    def test_seven_memories_one_per_chapter_1_to_7(self):
        memories = BASE_INDEX["memories"]
        self.assertEqual(len(memories), 7)
        self.assertEqual(sorted(m["chapter"] for m in memories), list(ci.MEMORY_CHAPTER_IDS))

    def test_memory_scene_and_location_ids_match_published_table(self):
        """These IDs come from NNEKA_MEMORIES_AND_TIMELINE.md section 1."""
        expected = {
            1: ("CH01-SCN-046", "CH01-SUB-018"),
            2: ("CH02-SCN-011", "CH02-SUB-003"),
            3: ("CH03-SCN-012", "CH03-INT-001"),
            4: ("CH04-SCN-012", "CH04-SUB-002"),
            5: ("CH05-SCN-011", "CH05-SUB-002"),
            6: ("CH06-SCN-010", "CH06-INT-003"),
            7: ("CH07-SCN-015", "CH07-INT-005"),
        }
        got = {m["index"]: (m["scene_id"], m["location_id"]) for m in BASE_INDEX["memories"]}
        self.assertEqual(got, expected)

    def test_every_memory_has_all_four_fragments(self):
        for mem in BASE_INDEX["memories"]:
            for key in ("place", "object", "sound", "interaction"):
                self.assertTrue(mem["fragments"][key].strip(), f"memory {mem['index']} {key}")

    def test_duplicate_memory_index_is_rejected(self):
        idx = fresh()
        idx["memories"][1]["index"] = 1
        self.assertTrue(ci.validate_memories(idx))

    def test_memory_in_chapter_eight_is_rejected(self):
        """OAD-32 places memories in Chapters 1-7 only. A memory in Ch08 would
        silently change the pacing and break the ending gate."""
        idx = fresh()
        mem = idx["memories"][6]
        mem["chapter"] = "CH08"
        mem["scene_id"] = "CH08-SCN-015"
        errors = ci.validate_memories(idx)
        self.assertTrue(any("outside CH01..CH07" in e for e in errors), errors)

    def test_memory_whose_location_is_unregistered_is_rejected(self):
        """If the discovery location is absent, the memory can never be found."""
        idx = fresh()
        idx["locations"] = [l for l in idx["locations"] if l["id"] != "CH04-SUB-002"]
        errors = ci.validate_memories(idx)
        self.assertTrue(any("not registered as a location" in e for e in errors), errors)

    def test_memory_with_empty_fragment_is_rejected(self):
        idx = fresh()
        idx["memories"][0]["fragments"]["sound"] = "   "
        errors = ci.validate_memories(idx)
        self.assertTrue(any("fragment 'sound'" in e for e in errors), errors)

    def test_two_memories_sharing_a_location_are_rejected(self):
        idx = fresh()
        idx["memories"][1]["location_id"] = idx["memories"][0]["location_id"]
        idx["memories"][1]["chapter"] = "CH01"
        idx["memories"][1]["scene_id"] = "CH01-SCN-047"
        self.assertTrue(ci.validate_memories(idx))

    def test_memory_chapter_must_match_scene_prefix(self):
        idx = fresh()
        idx["memories"][2]["scene_id"] = "CH04-SCN-012"  # wrong chapter
        errors = ci.validate_memories(idx)
        self.assertTrue(any("is not in chapter" in e for e in errors), errors)

    def test_only_six_memories_is_rejected(self):
        idx = fresh()
        idx["memories"].pop()
        self.assertTrue(ci.validate_memories(idx))


class TestBosses(unittest.TestCase):
    def test_all_eight_bosses_present(self):
        bosses = BASE_INDEX["bosses"]
        self.assertEqual(len(bosses), 8)
        self.assertEqual({b["chapter"] for b in bosses}, set(ci.CHAPTER_IDS))

    def test_no_arena_design_is_approved(self):
        """OAD-21: encounters are established; arena designs are not approved."""
        allowed = {"IN REVIEW", "NOT STARTED", "UNVERIFIED", "EXPLORATORY", "CONDITIONAL"}
        for boss in BASE_INDEX["bosses"]:
            self.assertIn(boss["arena_design_status"], allowed, boss["id"])

    def test_encounters_are_established(self):
        for boss in BASE_INDEX["bosses"]:
            self.assertEqual(boss["encounter_canon_status"], "ESTABLISHED", boss["id"])

    def test_arena_location_must_be_registered(self):
        idx = fresh()
        idx["bosses"][0]["arena_location_id"] = "CH01-BOS-999"
        errors = ci.validate_bosses(idx)
        self.assertTrue(any("is not registered" in e for e in errors), errors)

    def test_boss_name_mismatch_with_chapter_table_is_rejected(self):
        idx = fresh()
        idx["bosses"][0]["name"] = "Root Mother"
        errors = ci.validate_bosses(idx)
        self.assertTrue(any("disagrees with chapter table" in e for e in errors), errors)

    def test_boss_in_wrong_chapter_prefix_is_rejected(self):
        idx = fresh()
        idx["bosses"][0]["id"] = "CH02-BOS-001"
        self.assertTrue(ci.validate_bosses(idx))

    def test_chapter_without_boss_entry_is_rejected(self):
        idx = fresh()
        idx["bosses"] = [b for b in idx["bosses"] if b["chapter"] != "CH06"]
        errors = ci.validate_bosses(idx)
        self.assertTrue(any("no matching boss entry" in e for e in errors), errors)


class TestChapterRules(unittest.TestCase):
    def test_python_rule_is_present_and_enforced(self):
        rule = next(r for r in BASE_INDEX["chapter_rules"] if r["id"] == "RULE-CH04-PYTHONS")
        self.assertEqual(rule["chapter"], "CH04")
        self.assertIn("enemy:snake", rule["excludes"])
        self.assertIn("loot:snake", rule["excludes"])
        self.assertIn("enemy:python", rule["excludes"])

    def test_ch04_exclusions_cover_snakes_and_lightning(self):
        excluded = ci.exclusions_for_chapter(BASE_INDEX, "CH04")
        self.assertIn("enemy:snake", excluded)
        self.assertIn("lightning_vfx", excluded)
        self.assertIn("stilt_house", excluded)

    def test_ch02_no_flame_rule_excludes_fire(self):
        excluded = ci.exclusions_for_chapter(BASE_INDEX, "CH02")
        self.assertIn("fire_vfx", excluded)

    def test_ch07_ember_rule_excludes_flame_and_stone_castle(self):
        excluded = ci.exclusions_for_chapter(BASE_INDEX, "CH07")
        self.assertIn("fire_vfx", excluded)
        self.assertIn("stone_castle_kit", excluded)

    def test_exclusion_rule_without_excludes_list_is_rejected(self):
        idx = fresh()
        rule = next(r for r in idx["chapter_rules"] if r["id"] == "RULE-CH04-PYTHONS")
        rule.pop("excludes")
        errors = ci.validate_rules(idx)
        self.assertTrue(any("must list 'excludes'" in e for e in errors), errors)

    def test_rule_without_enforcement_is_rejected(self):
        idx = fresh()
        idx["chapter_rules"][0]["enforced_by"] = ""
        errors = ci.validate_rules(idx)
        self.assertTrue(any("must name how it is enforced" in e for e in errors), errors)

    def test_duplicate_rule_id_is_rejected(self):
        idx = fresh()
        idx["chapter_rules"].append(copy.deepcopy(idx["chapter_rules"][0]))
        errors = ci.validate_rules(idx)
        self.assertTrue(any("duplicate rule ids" in e for e in errors), errors)

    def test_global_rules_are_distinguished_from_chapter_rules(self):
        globals_ = ci.global_rules(BASE_INDEX)
        self.assertTrue(globals_)
        ids = {r["id"] for r in globals_}
        self.assertIn("RULE-OKWU-HOOD", ids)
        self.assertIn("RULE-ADANNA-NO-MIRROR", ids)
        self.assertIn("RULE-ADANNA-ONE-WEAPON", ids)
        self.assertIn("RULE-CULTURAL-FICTIONALITY", ids)

    def test_cultural_fictionality_rule_exists(self):
        """The directive forbids presenting invented mythology as Igbo tradition."""
        rule = next(r for r in BASE_INDEX["chapter_rules"] if r["id"] == "RULE-CULTURAL-FICTIONALITY")
        self.assertEqual(rule["kind"], "cultural")
        self.assertIn("never be presented as authentic", rule["statement"])


class TestIdsAndScheme(unittest.TestCase):
    def test_id_scheme_in_meta_matches_code(self):
        self.assertEqual(ci.validate_meta(BASE_INDEX), [])

    def test_malformed_ids_are_rejected(self):
        bad_ids = [
            "CH1-SUB-018",       # unpadded chapter
            "CH09-SUB-001",      # nonexistent chapter
            "CH01-SUB-18",       # short number
            "CH01-XXX-001",      # unknown type
            "ch01-sub-018",      # lowercase
            "CH01-SUB-018 ",     # trailing space
            "CH01-BOSS-001",     # the register uses BOS, never BOSS
        ]
        for bad in bad_ids:
            self.assertFalse(
                any(ci.ID_PATTERNS[k].match(bad) for k in ("scene", "location", "boss")),
                f"{bad!r} should not match any canon id pattern",
            )

    def test_all_register_location_categories_are_recognised(self):
        for category in ci.LOCATION_CATEGORIES:
            self.assertTrue(ci.ID_PATTERNS["location"].match(f"CH03-{category}-001"), category)

    def test_location_category_must_match_prefix(self):
        idx = fresh()
        idx["locations"][0]["category"] = "INT"
        errors = ci.validate_location_ids(idx)
        self.assertTrue(any("disagrees with category field" in e for e in errors), errors)

    def test_duplicate_location_id_is_rejected(self):
        idx = fresh()
        idx["locations"].append(copy.deepcopy(idx["locations"][0]))
        errors = ci.validate_location_ids(idx)
        self.assertTrue(any("duplicate location id" in e for e in errors), errors)

    def test_location_chapter_field_must_match_prefix(self):
        idx = fresh()
        idx["locations"][0]["chapter"] = "CH02"
        errors = ci.validate_location_ids(idx)
        self.assertTrue(any("disagrees with id prefix" in e for e in errors), errors)

    def test_boss_id_pattern(self):
        self.assertTrue(ci.ID_PATTERNS["boss"].match("CH01-BOS-001"))
        self.assertFalse(ci.ID_PATTERNS["boss"].match("CH01-BOSS-001"))
        self.assertFalse(ci.ID_PATTERNS["boss"].match("CH01-BOS-1"))


class TestSourceDocuments(unittest.TestCase):
    def test_six_authority_documents_registered(self):
        ids = {d["id"] for d in BASE_INDEX["source_documents"]}
        for expected in ("CHARACTER_DESIGN_REGISTER", "ENVIRONMENT_DESIGN_REGISTER",
                         "OPEN_ART_DECISIONS", "NNEKA_MEMORIES_AND_TIMELINE",
                         "LOCATION_MASTER_REGISTER",
                         "SCENE_AND_MICROLOCATION_MASTER_REGISTER"):
            self.assertIn(expected, ids)

    def test_each_document_declares_authority_and_drive_id(self):
        self.assertEqual(ci.validate_source_documents(BASE_INDEX), [])

    def test_document_without_drive_id_is_rejected(self):
        idx = fresh()
        idx["source_documents"][0]["drive_id"] = ""
        self.assertTrue(ci.validate_source_documents(idx))


class TestSchemaValidation(unittest.TestCase):
    def test_schema_accepts_real_index(self):
        self.assertEqual(ci.validate_against_schema(BASE_INDEX, BASE_SCHEMA), [])

    def test_schema_rejects_wrong_type(self):
        idx = fresh()
        idx["memories"] = "not-a-list"
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(errors)

    def test_schema_rejects_extra_property(self):
        idx = fresh()
        idx["memories"][0]["invented_field"] = True
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(any("unexpected property" in e for e in errors), errors)

    def test_schema_rejects_missing_required_property(self):
        idx = fresh()
        del idx["memories"][0]["fragments"]
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(any("missing required property 'fragments'" in e for e in errors), errors)

    def test_schema_rejects_bad_enum(self):
        idx = fresh()
        idx["chapters"][0]["canon_status"] = "Approved"
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(any("not in enum" in e for e in errors), errors)

    def test_schema_enforces_exactly_seven_memories(self):
        idx = fresh()
        idx["memories"].pop()
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(any("minimum 7" in e for e in errors), errors)

    def test_boolean_is_not_accepted_as_integer(self):
        idx = fresh()
        idx["memories"][0]["index"] = True
        errors = ci.validate_against_schema(idx, BASE_SCHEMA)
        self.assertTrue(errors, "True must not validate as an integer index")


class TestQueryHelpers(unittest.TestCase):
    def test_memory_by_index(self):
        mem = ci.memory_by_index(BASE_INDEX, 4)
        self.assertEqual(mem["title"], "Do Not Answer")
        self.assertEqual(mem["location_id"], "CH04-SUB-002")

    def test_memory_by_missing_index_raises(self):
        with self.assertRaises(ci.CanonError):
            ci.memory_by_index(BASE_INDEX, 99)

    def test_rules_for_chapter(self):
        rules = ci.rules_for_chapter(BASE_INDEX, "CH04")
        self.assertTrue(any(r["id"] == "RULE-CH04-PYTHONS" for r in rules))
        self.assertFalse(any(r["chapter"] == "CH05" for r in rules))

    def test_all_memory_tuples(self):
        tuples = ci.all_memory_tuples(BASE_INDEX)
        self.assertEqual(len(tuples), 7)
        self.assertEqual(tuples[0], (1, "CH01", "CH01-SCN-046", "CH01-SUB-018"))

    def test_load_missing_file_raises(self):
        with self.assertRaises(ci.CanonError):
            ci.load_index(Path("/nonexistent/canon_index.json"))


class TestEvidenceArtifact(unittest.TestCase):
    """The L0 run must emit machine-readable evidence (see architecture doc 11.3)."""

    def test_write_evidence(self):
        errors = ci.validate_index(BASE_INDEX, BASE_SCHEMA)
        result = {
            "test": "L0.Canon.Index.Valid",
            "suite": "Tools/canon/tests",
            "engine": "n/a (L0 host-side)",
            "canon_index_version": BASE_INDEX["meta"]["version"],
            "canon_documents": [d["id"] for d in BASE_INDEX["source_documents"]],
            "result": "PASS" if not errors else "FAIL",
            "errors": errors,
            "assertions": {
                "chapters": len(BASE_INDEX["chapters"]),
                "locations": len(BASE_INDEX["locations"]),
                "memories": len(BASE_INDEX["memories"]),
                "bosses": len(BASE_INDEX["bosses"]),
                "chapter_rules": len(BASE_INDEX["chapter_rules"]),
            },
        }
        out_dir = REPO_ROOT / "Docs" / "evidence" / "stage0"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "L0_canon_index_validation.json"
        out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        self.assertTrue(out_path.is_file())
        self.assertEqual(result["result"], "PASS", result["errors"])



class TestNpcCountParsing(unittest.TestCase):
    """The budget depends on this, and it has already been wrong twice: 'no one'
    parsed as 1, and an article-introduced person was dropped entirely."""

    def test_stated_absence_is_zero_and_parsed(self):
        for text in ("None.", "No one.", "Nobody", "Empty"):
            self.assertEqual(reg.parse_npc_count(text)[:2], (0, False), text)
            self.assertTrue(reg.parse_npc_count(text)[2], f"{text!r} must count as parsed")

    def test_absence_is_not_confused_with_unparseable(self):
        self.assertTrue(reg.parse_npc_count("None.")[2])
        self.assertFalse(reg.parse_npc_count("A gathering of unspecified size.")[2])

    def test_single_child(self):
        self.assertEqual(reg.parse_npc_count("One boy")[:2], (1, True))

    def test_numeral_plus_noun(self):
        self.assertEqual(reg.parse_npc_count("Three men and two women")[:2], (5, False))

    def test_collective_does_not_double_count(self):
        """"A family of six" is six people, not seven."""
        self.assertEqual(reg.parse_npc_count("A family of six")[:2], (6, False))

    def test_article_introduced_person_is_counted(self):
        """The bug: 'a girl' carried no numeral, so she vanished from the count."""
        self.assertEqual(reg.parse_npc_count("Two old men, a girl, and a dog")[:2],
                         (3, True))

    def test_animals_are_not_performers(self):
        self.assertEqual(reg.parse_npc_count("Two goats")[:2], (0, False))
        self.assertEqual(reg.parse_npc_count("six chickens")[:2], (0, False))

    def test_mixed_people_and_animals(self):
        self.assertEqual(reg.parse_npc_count("One woman, two goats and a child")[:2],
                         (2, True))

    def test_animal_does_not_hide_the_person(self):
        self.assertEqual(reg.parse_npc_count("Goats at dusk, and one boy.")[:2],
                         (1, True))

    def test_bare_numeral_is_trusted(self):
        self.assertEqual(reg.parse_npc_count("Seven")[:2], (7, False))

    def test_unknown_quantity_is_flagged_not_silently_zero(self):
        count, _, parsed = reg.parse_npc_count("A crowd")
        self.assertEqual(count, 0)
        self.assertFalse(parsed, "unparseable prose must never look like a valid zero")

    def test_empty_is_unparsed(self):
        self.assertFalse(reg.parse_npc_count("")[2])

    def test_numbers_above_ten(self):
        self.assertEqual(reg.parse_npc_count("twelve dancers")[:2], (12, False))


if __name__ == "__main__":
    unittest.main(verbosity=2)
