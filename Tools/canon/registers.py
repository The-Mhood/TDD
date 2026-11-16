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


def parse_npc_count(npcs_present: str) -> "tuple[int, bool, bool]":
    """Parse the register's 'NPCs present' prose into a person count.

    Returns (people, has_child, parsed).

    The register writes prose, not fields: "One woman, one child." /
    "None." / "Two traders." / "Goats at dusk, and one boy."

    `parsed=False` means DO NOT TRUST THE COUNT. It happens when the text
    contains no quantity this parser recognises ("a gathering of unspecified
    size", "several"). Callers must treat it as needs-manual-review, never as
    zero, because zero understates the population budget.

    Stated absence ("None.", "No one.") returns (0, False, True): that is a
    successful parse of a real answer, not a failure.

    Counting rules:
      * numeral + noun sums normally: "Three men and two women" -> 5
      * article + individual person noun adds one: "a girl" -> 1
      * article + collective noun adds nothing, because the following numeral
        already counted the people: "A family of six" -> 6, not 7
      * non-human animals are excluded: "Two old men, a girl, and a dog" -> 3
        (the dog is ambience, not a scheduled performer)

    KNOWN LIMITATION: word-list arithmetic, not language understanding. It
    cannot resolve "several", "a crowd", "many". See Docs/REGISTER_INGESTION.md.
    """
    text = (npcs_present or "").strip()
    if not text:
        return 0, False, False

    lowered = text.lower()
    has_child = any(w in lowered for w in _CHILD_WORDS)

    if any(lowered == p or lowered.startswith(p) for p in _ABSENCE_PHRASES):
        return 0, has_child, True

    total = 0
    parsed = False

    # 1. Numeral + noun pairs. Classify by the noun that the numeral counts, so
    #    "two goats" contributes nobody while "two women" contributes two.
    pair = re.compile(
        rf"\b(?P<num>{_NUMBER_WORDS_PATTERN}|\d+)\s+"
        rf"(?P<mid>(?:\w+\s+){{0,2}}?)"
        rf"(?P<noun>{_NON_HUMAN_PATTERN}|{_PERSON_PATTERN}|\w+)"
    )
    for m in pair.finditer(lowered):
        raw = m.group("num")
        value = int(raw) if raw.isdigit() else _NUMBER_WORDS[raw]
        noun = m.group("noun")
        parsed = True
        if noun in _NON_HUMAN or any(w in m.group("mid") for w in _NON_HUMAN):
            continue  # animals are ambience, not performers
        total += value

    # 2. Numerals with no noun at all ("Seven", "five"). The register only omits
    #    the noun when the meaning is obvious, so trust a bare numeral.
    if not parsed:
        for token in re.findall(r"\d+", lowered):
            total += int(token)
            parsed = True
        if not parsed:
            for token in re.findall(r"[a-z]+", lowered):
                if token in _NUMBER_WORDS:
                    total += _NUMBER_WORDS[token]
                    parsed = True
                    break

    # 3. Article-introduced individuals carrying no numeral ("a girl").
    for m in re.finditer(
            rf"\b(?:a|an)\s+(?:\w+\s+){{0,2}}?({_PERSON_PATTERN})\b", lowered):
        total += 1
        parsed = True

    return max(total, 0), has_child, parsed


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
