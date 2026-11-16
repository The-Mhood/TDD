#!/usr/bin/env python3
"""Parser for the Drive Art Bible registers (LOCATION_MASTER_REGISTER.md and
SCENE_AND_MICROLOCATION_MASTER_REGISTER.md).

WHY THIS EXISTS
---------------
The registers are the authority for world structure (ADR-0006). They are large
prose documents (534 KB and 278 KB) that contain dense, machine-readable tables.
Hand-copying them into engine data is both error-prone and guaranteed to drift.

This module turns those tables into structured records so that:
  - world structure can be generated rather than retyped,
  - the ID scheme and status vocabulary can be validated in CI,
  - engineering can detect when a register changes under it.

HONEST LIMITATION (see Docs/evidence/stage0/REPORT.md and ADR-0005)
-------------------------------------------------------------------
This parser has been validated against **Chapter 1 excerpts** of both registers
as read on 2026-11-16, not against the full 812 KB of text. Full-register
ingestion is a per-chapter task as chapters enter production (Stage 6 onward).
Do not report it as "fully validated" until a full-register run exists.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

# --------------------------------------------------------------------------- #
# Canonic vocabularies, read from the registers on 2026-11-16.
# These are CONSTANTS OF THE ART BIBLE, not engineering choices.
# If a register introduces a new value, the parser must fail loudly rather than
# silently accept it, so that the engine mirror is never out of step.
# --------------------------------------------------------------------------- #

#: Canon status has EXACTLY THREE values (LOCATION_MASTER_REGISTER v2.9).
CANON_STATUSES = ("ESTABLISHED", "PROPOSED", "PENDING APPROVAL")

#: Environment design status is a SEPARATE axis (client, OAD-48).
#: Approving a design does not change canon status and establishes no story fact.
ENV_DESIGN_STATUSES = (
    "NOT STARTED",
    "EXPLORATORY",
    "IN REVIEW",
    "REQUIRES REVISION",
    "CONDITIONAL",
    "APPROVED",
    "REJECTED",
)

#: Access level vocabulary.
ACCESS_LEVELS = (
    "FULLY ENTERABLE",
    "PARTIALLY ENTERABLE",
    "VISUALLY ACCESSIBLE",
    "BACKGROUND ENVIRONMENT",
    "OPEN EXTERIOR",
)

#: Location ID categories actually used in the registers.
LOCATION_CATEGORIES = {
    "ENV": "major environment",
    "SUB": "sub-location",
    "SET": "settlement",
    "INT": "interior",
    "LMK": "landmark",
    "TRV": "traversal area",
    "EXP": "exploration area",
    "BOS": "boss arena",
}

#: Scene ID categories (scene register).
SCENE_CATEGORIES = {
    "SCN": "scene",
}

#: Scene categories used in the scene register's Category column.
SCENE_KINDS = (
    "MAIN STORY SCENE",
    "SECONDARY STORY SCENE",
    "INCIDENTAL SCENE",
    "AMBIENT NPC SCENE",
    "ENTERABLE INTERIOR",
    "EXTERIOR MICRO-LOCATION",
    "ENVIRONMENTAL STORYTELLING",
    "EXPLORATION SCENE",
    "WORLD ACTIVITY SCENE",
    "ATMOSPHERIC SCENE",
)

#: CH01-SCN-001 / CH01-SUB-018 / CH08-BOS-001 / etc.
#: NOTE: boss arenas use BOS, not BOSS. This was established by reading the
#: location register; an earlier engineering proposal used "BOSS" and was wrong.
ID_PATTERN = re.compile(r"^(CH0[1-8])-(ENV|SUB|SET|INT|LMK|TRV|EXP|BOS|SCN)-(\d{3})$")


@dataclass
class LocationRecord:
    id: str
    name: str
    category: str          # ENV/SUB/SET/INT/LMK/TRV/EXP/BOS
    kind: str              # the Category column text, e.g. "Sub-location, Exterior"
    canon_status: str
    env_design_status: str
    added_in: str = ""
    chapter: str = ""
    notes: List[str] = field(default_factory=list)


@dataclass
class SceneDetail:
    """Per-scene detail block from the scene register's "Entries" section.

    The register writes each scene as an '### <ID> · <Name>' heading followed by
    a two-column '| Field | Value |' table. The fields that matter to world
    simulation are extracted here; everything else is left in the document.
    """
    id: str
    name: str = ""
    parent_id: str = ""
    scene_kind: str = ""
    canon_status: str = ""
    physical_description: str = ""
    what_player_sees: str = ""
    interaction: str = ""
    access_text: str = ""
    npcs_present: str = ""
    routines: str = ""
    time_variations: str = ""
    weather_variations: str = ""
    gameplay_relevance: str = ""
    production_notes: str = ""


@dataclass
class SceneRecord:
    id: str
    name: str
    parent_id: str
    scene_kind: str
    access: str
    canon_status: str
    chapter: str = ""


# --------------------------------------------------------------------------- #
# Markdown table parsing
# --------------------------------------------------------------------------- #

_TABLE_ROW = re.compile(r"^\|(.+)\|$")
_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def parse_markdown_tables(text: str) -> List[List[Dict[str, str]]]:
    """Return every markdown table in `text` as a list of row dicts.

    Each table becomes its own list. Header names are stripped. A table ends at
    the first non-pipe line.
    """
    tables: List[List[Dict[str, str]]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        row = _TABLE_ROW.match(lines[i].strip())
        if not row:
            i += 1
            continue
        # Need a separator on the next non-empty line to confirm a real table.
        j = i + 1
        if j >= len(lines) or not _SEPARATOR.match(lines[j].strip()):
            i += 1
            continue

        headers = [h.strip() for h in row.group(1).split("|")]
        rows: List[Dict[str, str]] = []
        j += 1
        while j < len(lines):
            candidate = _TABLE_ROW.match(lines[j].strip())
            if not candidate:
                break
            cells = [c.strip() for c in candidate.group(1).split("|")]
            # Pad/truncate defensively: a malformed row must not crash the build.
            if len(cells) < len(headers):
                cells += [""] * (len(headers) - len(cells))
            rows.append(dict(zip(headers, cells)))
            j += 1
        if rows:
            tables.append(rows)
        i = j
    return tables


def normalise_design_status(raw: str) -> "tuple[str, str]":
    """Split a register design-status cell into (status, annotation).

    The register writes annotations in parentheses, e.g.
        "IN REVIEW (revised; V002 submitted)"
        "REQUIRES REVISION (patient in modern clothing)"
    The status must be a closed vocabulary value; the annotation is preserved
    verbatim because it is often the instruction the art team must follow.
    """
    text = (raw or "").strip()
    if "(" in text:
        status, _, rest = text.partition("(")
        return status.strip(), rest.rstrip(")").strip()
    return text, ""


def split_id(id_text: str) -> Optional[re.Match]:
    return ID_PATTERN.match(id_text.strip())


def category_of(id_text: str) -> Optional[str]:
    m = split_id(id_text)
    return m.group(2) if m else None


def chapter_of(id_text: str) -> Optional[str]:
    m = split_id(id_text)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# Location register
# --------------------------------------------------------------------------- #

def parse_location_summary(text: str) -> List[LocationRecord]:
    """Parse every 'Location ID | Location Name | Category | Canon Status |
    Environment Design Status | Added in' table in the location register.

    The register repeats this table once per chapter, so we accept many.
    """
    records: List[LocationRecord] = []
    seen: set = set()
    for table in parse_markdown_tables(text):
        if not table:
            continue
        header = table[0]
        if "Location ID" not in header or "Canon Status" not in header:
            continue
        for row in table:
            raw_id = row.get("Location ID", "").strip()
            if not split_id(raw_id):
                continue
            if raw_id in seen:
                continue
            seen.add(raw_id)
            records.append(
                LocationRecord(
                    id=raw_id,
                    name=row.get("Location Name", "").strip(),
                    category=category_of(raw_id) or "",
                    kind=row.get("Category", "").strip(),
                    canon_status=row.get("Canon Status", "").strip(),
                    env_design_status=row.get("Environment Design Status", "").strip(),
                    added_in=row.get("Added in", "").strip(),
                    chapter=chapter_of(raw_id) or "",
                )
            )
    return records


def parse_location_hierarchy(text: str) -> Dict[str, List[str]]:
    """Parse the per-chapter '## Hierarchy' bullet lists into parent->children.

    Observed format in LOCATION_MASTER_REGISTER v2.9 (Chapter 1):

        ## Hierarchy

        - **Major Environment**
          - CH01-ENV-001 The Forbidden Forest (ESTABLISHED)
        - **Sub-locations**
          - CH01-SUB-001 The Abandoned Shrine (PENDING APPROVAL)

    So: only category headers are bold, entries are plain, and nesting is by
    indentation. The first entry at each nesting level after a bold header is
    the parent (the chapter's major environment); subsequent entries are its
    children. A bold header is never itself an id.

    Kept deliberately tolerant: an unparseable line is skipped rather than
    aborting the whole chapter's hierarchy.
    """
    out: Dict[str, List[str]] = {}
    bullet = re.compile(r"^(\s*)-\s+(.*\S)\s*$")
    entry = re.compile(r"^CH0[1-8]-[A-Z]{3}-\d{3}")
    bold_header = re.compile(r"^\*\*(.+?)\*\*$")

    chapter_root: Optional[str] = None
    current_section: str = ""

    for line in text.splitlines():
        if line.startswith("# CHAPTER"):
            chapter_root = None
            current_section = ""
            continue
        m = bullet.match(line)
        if not m:
            continue
        body = m.group(2).strip()

        header = bold_header.match(body)
        if header:
            # "Major Environment", "Sub-locations", "Landmarks", ...
            current_section = header.group(1).strip().lower()
            continue

        if not entry.match(body):
            continue

        loc_id = body[: len("CHnn-XXX-nnn")]
        is_major_environment = "major environment" in current_section

        if chapter_root is None or is_major_environment:
            chapter_root = loc_id
            out.setdefault(loc_id, [])
        else:
            out.setdefault(chapter_root, []).append(loc_id)

    return out


# --------------------------------------------------------------------------- #
# Scene register
# --------------------------------------------------------------------------- #

def parse_scene_summary(text: str) -> List[SceneRecord]:
    """Parse the per-chapter scene summary tables.

    Columns: Scene ID | Scene name | Parent location | Category | Access |
             Canon status | Level 1 | Level 2 | Level 3
    """
    records: List[SceneRecord] = []
    seen: set = set()
    for table in parse_markdown_tables(text):
        if not table:
            continue
        if "Scene ID" not in table[0] or "Parent location" not in table[0]:
            continue
        for row in table:
            raw_id = row.get("Scene ID", "").strip()
            if not split_id(raw_id) or raw_id in seen:
                continue
            seen.add(raw_id)
            parent = row.get("Parent location", "").strip()
            # Parent may be rendered as "CH01-INT-007" or "CH01-INT-007 (Name)".
            pm = re.match(r"^(CH0[1-8]-[A-Z]{3}-\d{3})", parent)
            records.append(
                SceneRecord(
                    id=raw_id,
                    name=row.get("Scene name", "").strip(),
                    parent_id=pm.group(1) if pm else parent,
                    scene_kind=row.get("Category", "").strip(),
                    access=row.get("Access", "").strip(),
                    canon_status=row.get("Canon status", "").strip().strip("*"),
                    chapter=chapter_of(raw_id) or "",
                )
            )
    return records


# --------------------------------------------------------------------------- #
# Scene detail blocks
# --------------------------------------------------------------------------- #

_SCENE_HEADING = re.compile(r"^###\s+(CH0[1-8]-SCN-\d{3})\s*(?:[\u00b7\-]\s*(.*))?$")

#: Register field labels -> SceneDetail attribute. Exact strings as published.
_FIELD_MAP = {
    "Scene ID": None,                      # the id; already captured from heading
    "Scene name": "name",
    "Parent location ID": "parent_id",
    "Scene category": "scene_kind",
    "Canon status": "canon_status",
    "Physical description.": "physical_description",
    "What the player sees.": "what_player_sees",
    "What the player can interact with.": "interaction",
    "Can the player enter the space?": "access_text",
    "NPCs present.": "npcs_present",
    "NPC activities and routines.": "routines",
    "Time-of-day variations.": "time_variations",
    "Weather variations.": "weather_variations",
    "Gameplay relevance.": "gameplay_relevance",
    "Production notes.": "production_notes",
}


def parse_scene_details(text: str) -> List[SceneDetail]:
    """Parse the register's per-scene detail blocks ('### ID · Name' + table)."""
    details: List[SceneDetail] = []
    current: Optional[SceneDetail] = None
    in_table = False

    for line in text.splitlines():
        heading = _SCENE_HEADING.match(line.strip())
        if heading:
            if current is not None:
                details.append(current)
            current = SceneDetail(id=heading.group(1), name=(heading.group(2) or "").strip())
            in_table = False
            continue

        if current is None:
            continue

        stripped = line.strip()
        if stripped.startswith("| Field | Value |") or stripped.startswith("|---|---|"):
            in_table = True
            continue
        if in_table:
            if not stripped:
                # A blank line terminates the field table. This is the boundary
                # between the '| Field | Value |' block and the bulleted fields
                # that follow it. Getting this wrong silently drops every
                # bulleted field, which is exactly what happened on first run.
                in_table = False
                continue
            row = _TABLE_ROW.match(stripped)
            if not row:
                in_table = False
                # fall through so a bullet on this line is still parsed
            else:
                cells = [c.strip() for c in row.group(1).split("|")]
                if len(cells) >= 2:
                    label, value = cells[0], cells[1]
                    target = _FIELD_MAP.get(label)
                    if target:
                        setattr(current, target, _strip_emphasis(value))
                continue
            cells = [c.strip() for c in row.group(1).split("|")]
            if len(cells) < 2:
                continue
            label, value = cells[0], cells[1]
            target = _FIELD_MAP.get(label)
            if target:
                setattr(current, target, _strip_emphasis(value))
            continue

        # Bulleted fields outside a table, e.g. "- **Physical description.** ..."
        bullet = re.match(r"^-\s+\*\*(.+?)\*\*\s*(.*)$", stripped)
        if bullet:
            label = bullet.group(1).strip()
            value = bullet.group(2).strip()
            target = _FIELD_MAP.get(label)
            if target:
                setattr(current, target, _strip_emphasis(value))

    if current is not None:
        details.append(current)
    return details


def _strip_emphasis(value: str) -> str:
    """Remove markdown emphasis and backticks from a register cell."""
    return value.replace("**", "").replace("`", "").strip()


_NUMBER_WORDS = {
    "no": 0, "zero": 0, "none": 0,
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12,
}
_NUMBER_WORDS_PATTERN = "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True))

#: Creatures present in a scene that are NOT people needing a performer.
#: Reported as ambience by the population budget, never billed as an NPC.
_NON_HUMAN = ("dog", "dogs", "goat", "goats", "chicken", "chickens", "fowl",
              "bird", "birds", "hornbill", "hornbills", "duiker", "duikers",
              "cat", "cats", "sheep", "cow", "cows", "monkey", "monkeys")
_NON_HUMAN_PATTERN = "|".join(sorted(_NON_HUMAN, key=len, reverse=True))

#: Individual people nouns. Used to count article-introduced people ("a girl")
#: that carry no numeral.
_PERSON_NOUNS = (
    "woman", "women", "man", "men", "child", "children", "boy", "boys",
    "girl", "girls", "elder", "elders", "trader", "traders", "smith",
    "smiths", "farmer", "farmers", "hunter", "hunters", "guard", "guards",
    "weaver", "weavers", "potter", "potters", "drummer", "drummers",
    "dancer", "dancers", "singer", "singers", "mother", "father",
    "grandmother", "grandfather", "baby", "person", "people", "youth",
    "youths", "widow", "widows", "bride", "priest", "priestess",
)
_PERSON_PATTERN = "|".join(sorted(_PERSON_NOUNS, key=len, reverse=True))

#: Collective nouns. "A family of six" is six people, already counted by the
#: numeral, so the article must not add one more.
_COLLECTIVE = ("family", "families", "group", "groups", "gathering", "crowd",
               "party", "household", "procession")

_ABSENCE_PHRASES = ("none", "no one", "nobody", "not present", "empty",
                    "unpopulated", "deserted")

_CHILD_WORDS = ("child", "children", "boy", "boys", "girl", "girls")


#: ("six to ten"), an alternative ("four or five") and a vagueness marker
#: ("several", "occasional") all describe a population the register has NOT
#: pinned down. Reducing any of them to one integer would invent precision the
#: source does not have.
#:
#: "a dozen" is NOT in this list. It is a definite quantity: exactly twelve.
#: "dozens" is indefinite and remains listed. The two differ by one letter and
#: by an order of magnitude of precision, so they are matched separately.
_VAGUE_WORDS = (
    "several", "some", "few", "many", "various", "occasional", "occasionally",
    "sometimes", "usually", "often", "rare", "rarely", "dozens",
    "handful", "couple", "line", "bunch", "crowd",
)
#: Range connectors: "six to ten", "four or five", "between three and five".
_RANGE_CONNECTORS = (" to ", " or ", "through", "between")

#: Nouns that count PEOPLE and therefore carry a head-count when numbered.
_PERSON_EXTRA = (
    "apprentice", "apprentices", "patient", "patients", "servant", "servants",
    "visitor", "visitors", "traveller", "travellers", "adult", "adults",
    "inhabitant", "inhabitants", "occupant", "occupants", "attendant",
    "attendants", "messenger", "messengers", "student", "students",
    "worker", "workers", "seller", "sellers", "buyer", "buyers",
    "storyteller", "storytellers", "elder", "elders",
    "passer-by", "passers-by", "passerby", "passer",
)

#: The register's documented naming convention for a single named NPC is
#: "Name (role)" - "Mgbafo (village elder)", "Okorie (royal guard)". One such
#: entry is one person. This is a documented convention, not an inference.
_NAMED_PERSON = re.compile(r"\b[A-Z][a-z\u00c0-\u024f]+\s*\(([a-z][a-z \-/]*)\)")


def _person_nouns() -> tuple:
    return tuple(set(_PERSON_NOUNS) | set(_PERSON_EXTRA))


def parse_npc_count(npcs_present: str) -> "tuple[int, bool, bool]":
    """Parse the register's 'NPCs present' prose into a person count.

    Returns (people, has_child, parsed).

    The register writes prose, not fields: "One woman, one child." /
    "None." / "Two traders." / "Goats at dusk, and one boy."

    `parsed=False` means DO NOT TRUST THE COUNT. The caller must treat it as
    needs-manual-review and must NOT substitute zero, because zero understates
    the population budget.

    WHY THIS IS NOT A NUMBER-SCRAPER
    --------------------------------
    An earlier version summed every numeral it could find. Two real Chapter 1
    strings broke it:

        "Six to ten adults; Unoka (storyteller) some days."  -> 16   (6 + 10)
        "Family of eight across three generations."          -> 11   (8 + 3)

    Both are confidently wrong. 16 invents a crowd twice the register's own
    upper bound; 11 counts a generation as a person. A plausible wrong number
    is far more dangerous than an admitted gap, because downstream budget
    arithmetic cannot tell it apart from a real one.

    The corrected rule is that every number must be classified by the noun it
    counts. A number attached to a person noun or a collective of people is a
    head-count. A number attached to anything else - animals, generations,
    pots, stools - describes something that is not a performer and contributes
    nothing. When no quantity can be classified with confidence, the function
    refuses and reports UNPARSED upstream.

    Counting rules:
      * numeral + person noun sums: "Three men and two women" -> 5
      * numeral + non-person noun contributes nobody: "Two goats" -> 0
        (animals are ambience, not scheduled performers)
      * numeral + collective of people is a head-count: "A family of six" -> 6
      * a number counting an abstract noun is not a head-count:
        "across three generations" contributes 0
      * a named NPC in the register's "Name (role)" convention is 1 person:
        "Okorie (royal guard)." -> 1
      * article + person noun adds one: "a girl" -> 1
      * ranges, alternatives and vague quantities are REFUSED, not summed:
        "Six to ten adults" -> UNPARSED, "Four or five men" -> UNPARSED
      * a bare numeral with no noun is trusted when it is the only number:
        "Two." -> 2

    KNOWN LIMITATION: word-list arithmetic, not language understanding. See
    Docs/REGISTER_INGESTION.md for the documented ingestion rules.
    """
    text = (npcs_present or "").strip()
    if not text:
        return 0, False, False

    lowered = text.lower()
    has_child = any(re.search(rf"\b{w}\b", lowered) for w in _CHILD_WORDS)

    if any(lowered == p or lowered.startswith(p) for p in _ABSENCE_PHRASES):
        return 0, has_child, True

    # --- Exact dozen. ------------------------------------------------------
    # "A dozen people." is twelve people. This is a definite quantity, not a
    # vague one, and refusing it would be a false negative of the same kind as
    # the old "six to ten -> 16" error, only in the opposite direction: it
    # understates a scene the register actually pins down.
    #
    # The variants below are NOT all twelve, and each is handled explicitly
    # rather than by a loose regex:
    #   "two dozen"      -> 24
    #   "half a dozen"   -> 6
    #   "a dozen or so"  -> NOT exact; an approximation, refused
    #   "dozens"         -> indefinite, refused by the vague-word gate
    m = re.search(r"\b([a-z]+|\d+)?\s*dozen\b", lowered)
    if m:
        if re.search(r"\bdozen\s+(?:or|and)\s+so\b", lowered):
            return 0, has_child, False      # approximation, not a count
        prefix = (m.group(1) or "").strip()
        if prefix == "half" or "half a dozen" in lowered:
            return 6, has_child, True
        if prefix in ("a", "one", ""):
            return 12, has_child, True
        multiplier = int(prefix) if prefix.isdigit() else _NUMBER_WORDS.get(prefix)
        if multiplier:
            return 12 * multiplier, has_child, True
        # "several dozen", "many dozen" - the vague-word gate will refuse these.

    # --- Refusal gate 1: an explicit range or alternative. ----------------
    padded = f" {' '.join(lowered.split())} "
    if any(conn in padded for conn in _RANGE_CONNECTORS):
        return 0, has_child, False

    # --- Refusal gate 2: a vague quantity word. ---------------------------
    for word in _VAGUE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            return 0, has_child, False

    person_nouns = _person_nouns()
    non_person = set(_NON_HUMAN)
    # A numeral binds to a HEAD-COUNT noun. Collectives of people ("a family of
    # eight") belong here, but they must stay out of the article rule below,
    # which would otherwise add a spurious +1 to "a family of six".
    headcount_nouns = person_nouns + tuple(_COLLECTIVE)
    total = 0
    recognized_any = False

    # --- Named NPCs: "Name (role)" is one person. -------------------------
    named = list(_NAMED_PERSON.finditer(text))
    total += len(named)
    if named:
        recognized_any = True

    # Strip the named entries so their role parenthetical cannot be re-counted.
    stripped = _NAMED_PERSON.sub(" ", text)
    stripped_l = stripped.lower()

    # --- Every remaining number, classified by the noun it counts. --------
    # A number can bind FORWARD ("four farmers") or BACKWARD through 'of'
    # ("a family of eight").
    number_re = re.compile(rf"\b(?P<num>{_NUMBER_WORDS_PATTERN}|\d+)\b")
    for m in number_re.finditer(stripped_l):
        raw = m.group("num")
        value = int(raw) if raw.isdigit() else _NUMBER_WORDS[raw]

        after = stripped_l[m.end():m.end() + 48]
        before = stripped_l[max(0, m.start() - 40):m.start()]

        noun_after = re.match(r"\s+(?:[a-z][a-z\-]*\s+){0,2}?([a-z][a-z\-]*)", after)
        forward = noun_after.group(1) if noun_after else ""

        backward = ""
        of_match = re.search(r"\b([a-z][a-z\-]*)\s+of\s*$", before)
        if of_match:
            backward = of_match.group(1)

        candidate_forward = forward in headcount_nouns or forward in non_person
        candidate_backward = backward in headcount_nouns or backward in non_person

        if candidate_forward:
            noun, is_person = forward, (forward in headcount_nouns)
        elif candidate_backward:
            noun, is_person = backward, (backward in headcount_nouns)
        else:
            # The noun is unknown (abstract, or omitted). It MAY still be a
            # head-count, but we cannot prove it, so it is not counted here and
            # the bare-numeral fallback below decides.
            continue

        recognized_any = True
        if is_person:
            total += value
        # non-person nouns contribute nobody, by design

    # --- Bare numerals: trusted only when the string holds exactly one. ---
    if total == 0 and not recognized_any:
        numeric_tokens = re.findall(
            rf"\b(?:\d+|{_NUMBER_WORDS_PATTERN})\b", stripped_l)
        if len(numeric_tokens) == 1:
            token = numeric_tokens[0]
            total = int(token) if token.isdigit() else _NUMBER_WORDS[token]
            recognized_any = True
        elif len(numeric_tokens) > 1:
            # Several numbers and no noun to bind them to: refuse.
            return 0, has_child, False

    # --- Article-introduced individuals with no numeral ("a girl"). -------
    if not named:
        for _ in re.finditer(
                rf"\b(?:a|an)\s+(?:[a-z]+\s+){{0,2}}?({'|'.join(person_nouns)})\b",
                stripped_l):
            total += 1
            recognized_any = True

    return max(total, 0), has_child, (recognized_any and total >= 0)


#: A quantity the register states as a CONDITION rather than a constant:
#: "Sometimes one cook.", "Occasional passer-by.", "Unoka ... some days."
_CONDITION_MARKERS = (
    "sometimes", "occasional", "occasionally", "some days", "at times",
    "now and then", "when ", "if ",
)


def parse_npc_band(npcs_present: str) -> "tuple[Optional[int], Optional[int], str]":
    """Derive the register's OWN numeric BOUNDS for an 'NPCs present' string.

    Returns (low, high, basis). `basis` explains where the bounds came from so
    the provenance table can quote it. (None, None, ...) means the register
    states no bound at all and the field must stay unresolved.

    WHY THIS EXISTS
    ---------------
    When parse_npc_count refuses a string, the scene must not silently become
    zero. But it also must not be given an invented point value. What the
    register DOES often provide is a bound:

        "Six to ten adults; ..."   -> (6, 10, "stated range")
        "Four or five men."        -> (4, 5,  "stated alternative")
        "Sometimes one cook."      -> (0, 1,  "conditional presence")
        "A line of women ..."      -> (None, None, "collective without a number")

    A bound is register data: the range is written in the source. Reporting it
    as a band is therefore faithful, while reporting it as a single integer
    (or as 0) would not be.

    These bounds feed an explicitly LABELLED banded estimate. They are never
    merged into the point estimate silently.
    """
    text = (npcs_present or "").strip()
    if not text:
        return None, None, "no text"
    lowered = " ".join(text.lower().split())

    if any(lowered == p or lowered.startswith(p) for p in _ABSENCE_PHRASES):
        return 0, 0, "stated absence"

    def num(token: str) -> Optional[int]:
        if token.isdigit():
            return int(token)
        return _NUMBER_WORDS.get(token)

    word = rf"(?:{_NUMBER_WORDS_PATTERN}|\d+)"

    # "between three and five"
    m = re.search(rf"between\s+({word})\s+and\s+({word})", lowered)
    if m:
        lo, hi = num(m.group(1)), num(m.group(2))
        if lo is not None and hi is not None:
            return min(lo, hi), max(lo, hi), "stated range (between X and Y)"

    # "six to ten", "eight through twelve"
    m = re.search(rf"({word})\s+(?:to|through)\s+({word})", lowered)
    if m:
        lo, hi = num(m.group(1)), num(m.group(2))
        if lo is not None and hi is not None:
            return min(lo, hi), max(lo, hi), "stated range (X to Y)"

    # "four or five"
    m = re.search(rf"({word})\s+or\s+({word})", lowered)
    if m:
        lo, hi = num(m.group(1)), num(m.group(2))
        if lo is not None and hi is not None:
            return min(lo, hi), max(lo, hi), "stated alternative (X or Y)"

    # "a dozen people" is exactly twelve. The same variants the point parser
    # distinguishes must be distinguished here, or the band and the point
    # estimate disagree about the same sentence:
    #   "half a dozen" -> 6, "two dozen" -> 24
    #   "a dozen or so" -> an approximation, so NO exact bound is claimed
    #   "dozens"        -> indefinite, falls through to "no bound stated"
    m_doz = re.search(r"\b([a-z]+|\d+)?\s*dozen\b", lowered)
    if m_doz and "dozens" not in lowered:
        if re.search(r"\bdozen\s+(?:or|and)\s+so\b", lowered):
            return None, None, "approximate collective (a dozen or so); no exact bound"
        prefix = (m_doz.group(1) or "").strip()
        if prefix == "half" or "half a dozen" in lowered:
            return 6, 6, "stated collective equal to six (half a dozen)"
        if prefix in ("a", "one", ""):
            return 12, 12, "stated collective equal to twelve (a dozen)"
        multiplier = int(prefix) if prefix.isdigit() else _NUMBER_WORDS.get(prefix)
        if multiplier:
            return (12 * multiplier, 12 * multiplier,
                    f"stated collective equal to {12 * multiplier} ({multiplier} dozen)")

    # Exact count wins when the parser can read one.
    exact, _has_child, parsed = parse_npc_count(text)
    if parsed:
        if any(marker in lowered for marker in _CONDITION_MARKERS):
            return 0, exact, "conditional presence (0 when absent)"
        return exact, exact, "stated count"

    # Conditional phrasing with a single readable numeral inside it.
    if any(marker in lowered for marker in _CONDITION_MARKERS):
        numerals = re.findall(rf"\b{word}\b", lowered)
        if len(numerals) == 1:
            value = num(numerals[0])
            if value is not None:
                return 0, value, "conditional presence (0 when absent)"

        # Conditional phrasing that names a SINGULAR person ("Sometimes a
        # traveller.", "Occasional passer-by."). The register's own wording is
        # singular, so at most one person is depicted at a time. This is a bound
        # read from the grammar of the source, not an assumption about density.
        plural_hits = [n for n in _person_nouns() + tuple(_COLLECTIVE)
                       if n.endswith("s") and re.search(rf"\b{re.escape(n)}\b", lowered)]
        singular_hits = [n for n in _person_nouns()
                         if not n.endswith("s") and re.search(rf"\b{re.escape(n)}\b", lowered)]
        if singular_hits and not plural_hits:
            return 0, 1, "conditional presence, singular person named (0 to 1)"

    # No numeral at all, and the prose is a collective ("a line of women").
    return None, None, "collective without a number; no bound stated"


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_scene_details(details: Sequence[SceneDetail]) -> List[str]:
    problems: List[str] = []
    seen: Dict[str, int] = {}
    for detail in details:
        seen[detail.id] = seen.get(detail.id, 0) + 1
        if detail.canon_status and detail.canon_status not in CANON_STATUSES:
            problems.append(f"{detail.id}: canon status {detail.canon_status!r} not recognised")
        if detail.scene_kind and detail.scene_kind not in SCENE_KINDS:
            problems.append(f"{detail.id}: scene kind {detail.scene_kind!r} not recognised")
        if not detail.npcs_present:
            problems.append(f"{detail.id}: no 'NPCs present' field parsed")
    for scene_id, count in seen.items():
        if count > 1:
            problems.append(f"{scene_id}: detail block appears {count} times")
    return problems


def validate_locations(records: Sequence[LocationRecord]) -> List[str]:
    """Return problems. An empty list means the records are self-consistent."""
    problems: List[str] = []
    seen: Dict[str, int] = {}
    for rec in records:
        seen[rec.id] = seen.get(rec.id, 0) + 1
        if category_of(rec.id) != rec.category:
            problems.append(f"{rec.id}: category field {rec.category!r} disagrees with id")
        if rec.canon_status not in CANON_STATUSES:
            problems.append(
                f"{rec.id}: canon status {rec.canon_status!r} is not one of {CANON_STATUSES}"
            )
        if rec.env_design_status and rec.env_design_status not in ENV_DESIGN_STATUSES:
            # The register sometimes annotates, e.g.
            # "IN REVIEW (V002 accepted for visual review)".
            base = rec.env_design_status.split("(")[0].strip()
            if base not in ENV_DESIGN_STATUSES:
                problems.append(
                    f"{rec.id}: environment design status {rec.env_design_status!r} "
                    f"does not start with a known value"
                )
        if not rec.name:
            problems.append(f"{rec.id}: missing name")
    for loc_id, count in seen.items():
        if count > 1:
            problems.append(f"{loc_id}: appears {count} times in the summary tables")
    return problems


def validate_scenes(records: Sequence[SceneRecord],
                    locations: Sequence[LocationRecord]) -> List[str]:
    problems: List[str] = []
    known_locations = {loc.id for loc in locations}
    seen: Dict[str, int] = {}
    for rec in records:
        seen[rec.id] = seen.get(rec.id, 0) + 1
        if category_of(rec.id) != "SCN":
            problems.append(f"{rec.id}: not a scene id")
        if rec.canon_status not in CANON_STATUSES:
            problems.append(f"{rec.id}: canon status {rec.canon_status!r} not recognised")
        if rec.scene_kind and rec.scene_kind not in SCENE_KINDS:
            problems.append(f"{rec.id}: scene kind {rec.scene_kind!r} not recognised")
        if rec.access and rec.access not in ACCESS_LEVELS:
            problems.append(f"{rec.id}: access {rec.access!r} not recognised")
        if rec.parent_id not in known_locations:
            problems.append(
                f"{rec.id}: parent location {rec.parent_id!r} is not in the location register"
            )
        if chapter_of(rec.id) != chapter_of(rec.parent_id):
            problems.append(f"{rec.id}: parent {rec.parent_id} is in a different chapter")
    for scene_id, count in seen.items():
        if count > 1:
            problems.append(f"{scene_id}: appears {count} times")
    return problems


# --------------------------------------------------------------------------- #
# Extraction (compact derived data for the engine mirror)
# --------------------------------------------------------------------------- #

def extract(text_location: str, text_scene: str) -> Dict[str, object]:
    locations = parse_location_summary(text_location)
    scenes = parse_scene_summary(text_scene)
    hierarchy = parse_location_hierarchy(text_location)

    chapters: Dict[str, Dict[str, int]] = {}
    for loc in locations:
        bucket = chapters.setdefault(loc.chapter, {})
        bucket[loc.category] = bucket.get(loc.category, 0) + 1
        bucket["_total"] = bucket.get("_total", 0) + 1
    for scn in scenes:
        bucket = chapters.setdefault(scn.chapter, {})
        bucket["SCN"] = bucket.get("SCN", 0) + 1

    return {
        "meta": {
            "source": "LOCATION_MASTER_REGISTER.md v2.9 + SCENE_AND_MICROLOCATION_MASTER_REGISTER.md v1.9",
            "canon_statuses": list(CANON_STATUSES),
            "env_design_statuses": list(ENV_DESIGN_STATUSES),
            "access_levels": list(ACCESS_LEVELS),
            "location_categories": LOCATION_CATEGORIES,
        },
        "counts_by_chapter": chapters,
        "locations": [asdict(loc) for loc in locations],
        "scenes": [asdict(scn) for scn in scenes],
        "hierarchy": hierarchy,
        "validation": {
            "location_problems": validate_locations(locations),
            "scene_problems": validate_scenes(scenes, locations),
        },
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) < 3:
        print("usage: registers.py <LOCATION_MASTER_REGISTER.md> "
              "<SCENE_AND_MICROLOCATION_MASTER_REGISTER.md> [--out out.json]")
        return 2
    loc_path, scn_path = Path(argv[1]), Path(argv[2])
    out_path = None
    if "--out" in argv:
        out_path = Path(argv[argv.index("--out") + 1])

    data = extract(loc_path.read_text(encoding="utf-8"),
                   scn_path.read_text(encoding="utf-8"))
    problems = (data["validation"]["location_problems"]      # type: ignore[index]
                + data["validation"]["scene_problems"])      # type: ignore[index]
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"written {out_path}")
    print(f"locations={len(data['locations'])} scenes={len(data['scenes'])} "
          f"problems={len(problems)}")
    for problem in problems[:40]:
        print("  ", problem)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
