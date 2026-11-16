#!/usr/bin/env python3
"""Canon index loader and validator for THE DISOBEDIENT DAUGHTER.

This module is dependency-free on purpose (stdlib only). It is the L0 gate in
Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md section 13: it verifies that the
engineering mirror of the Drive Art Bible registers is internally consistent and
that canonical rules are machine-enforceable before any gameplay code depends
on them.

It does NOT decide canon. The Drive registers are authoritative. If this tool
reports drift, the fix is either (a) correct the mirror, or (b) raise the
mismatch to the register owner. Never silently "fix" the mirror to make a test
pass.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

DATA_DIR = Path(__file__).resolve().parent / "data"
INDEX_PATH = DATA_DIR / "canon_index.json"
SCHEMA_PATH = DATA_DIR / "canon_index.schema.json"

CHAPTER_IDS = tuple(f"CH{i:02d}" for i in range(1, 9))
MEMORY_CHAPTER_IDS = tuple(f"CH{i:02d}" for i in range(1, 8))  # memories live in Ch 1..7 only

REQUIRED_KEYS = ("meta", "approval_states", "chapters", "source_documents",
                 "locations", "memories", "bosses", "chapter_rules")

ID_PATTERNS = {
    "chapter": re.compile(r"^CH0[1-8]$"),
    "scene": re.compile(r"^CH0[1-8]-SCN-\d{3}$"),
    "sublocation": re.compile(r"^CH0[1-8]-SUB-\d{3}$"),
    "interior": re.compile(r"^CH0[1-8]-INT-\d{3}$"),
    "boss": re.compile(r"^CH0[1-8]-BOSS-[A-Z][A-Za-z0-9]*$"),
    "rule": re.compile(r"^RULE-[A-Z0-9-]+$"),
}

APPROVAL_STATES = ("Proposed", "DesignApproved", "CanonApproved", "Shippable")


class CanonError(Exception):
    """Raised when the canon index is structurally or semantically invalid."""


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

def load_index(path: Path = INDEX_PATH) -> Dict[str, Any]:
    if not path.is_file():
        raise CanonError(f"canon index not found: {path}")
    with path.open(encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise CanonError(f"canon index is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise CanonError("canon index root must be a JSON object")
    return data


def load_schema(path: Path = SCHEMA_PATH) -> Dict[str, Any]:
    if not path.is_file():
        raise CanonError(f"canon schema not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# Minimal JSON-Schema subset validator
# --------------------------------------------------------------------------- #
# Dependency policy forbids pulling in `jsonschema` for a three-agent project,
# so we implement exactly the subset the schema uses. Anything outside the
# subset must fail loudly rather than pass silently.

_SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema", "$id", "title", "description",
    "type", "required", "properties", "additionalProperties", "items",
    "enum", "pattern", "minLength", "minItems", "maxItems",
    "minimum", "maximum", "definitions", "$ref",
}

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "integer": int,
    "number": (int, float),
    "null": type(None),
}


def _type_ok(value: Any, expected: Any) -> bool:
    expected_types = expected if isinstance(expected, list) else [expected]
    for name in expected_types:
        py = _TYPE_MAP[name]
        if name == "integer":
            if isinstance(value, int) and not isinstance(value, bool):
                return True
        elif name == "number":
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
        elif name == "boolean":
            if isinstance(value, bool):
                return True
        elif isinstance(value, py):
            # bool is a subclass of int; reject bools where int/string expected
            if name in ("string", "object", "array") and isinstance(value, bool):
                continue
            return True
    return False


def _warn_unsupported_keywords(schema: Any, path: str = "$") -> List[str]:
    problems: List[str] = []
    if not isinstance(schema, dict):
        return problems
    for key in schema:
        if key not in _SUPPORTED_SCHEMA_KEYWORDS:
            problems.append(f"{path}: unsupported schema keyword '{key}'")
    for key, sub in schema.get("properties", {}).items():
        problems.extend(_warn_unsupported_keywords(sub, f"{path}.{key}"))
    for key, sub in schema.get("definitions", {}).items():
        problems.extend(_warn_unsupported_keywords(sub, f"{path}#{key}"))
    if "items" in schema:
        problems.extend(_warn_unsupported_keywords(schema["items"], f"{path}[]"))
    return problems


def _resolve_ref(root_schema: Dict[str, Any], ref: str) -> Dict[str, Any]:
    if not ref.startswith("#/"):
        raise CanonError(f"unsupported $ref (only local refs allowed): {ref}")
    node: Any = root_schema
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def _validate(value: Any, schema: Dict[str, Any], root_schema: Dict[str, Any],
              path: str, errors: List[str]) -> None:
    if "$ref" in schema:
        schema = _resolve_ref(root_schema, schema["$ref"])

    if "type" in schema and not _type_ok(value, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")

    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match pattern {schema['pattern']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string shorter than {schema['minLength']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} above maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: {len(value)} items, minimum {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: {len(value)} items, maximum {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                _validate(item, schema["items"], root_schema, f"{path}[{i}]", errors)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property '{key}'")
        extra_allowed = schema.get("additionalProperties", True)
        for key, sub in value.items():
            if key in props:
                _validate(sub, props[key], root_schema, f"{path}.{key}", errors)
            elif extra_allowed is False:
                errors.append(f"{path}: unexpected property '{key}'")
            elif isinstance(extra_allowed, dict):
                _validate(sub, extra_allowed, root_schema, f"{path}.{key}", errors)


def validate_against_schema(index: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    problems = _warn_unsupported_keywords(schema)
    if problems:
        return problems
    errors: List[str] = []
    _validate(index, schema, schema, "$", errors)
    return errors


# --------------------------------------------------------------------------- #
# Semantic validation — the rules that actually protect the game
# --------------------------------------------------------------------------- #

def _chapter_of(location_id: str) -> str:
    return location_id[:4]


def validate_chapters(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    chapters = index.get("chapters", [])
    ids = [c.get("id") for c in chapters]
    if tuple(sorted(ids)) != tuple(sorted(CHAPTER_IDS)):
        errors.append(f"chapters must be exactly {CHAPTER_IDS}, got {tuple(ids)}")
    indexes = sorted(c.get("index") for c in chapters)
    if indexes != list(range(1, 9)):
        errors.append(f"chapter indexes must be 1..8 with no gaps, got {indexes}")
    for c in chapters:
        if not ID_PATTERNS["chapter"].match(str(c.get("id", ""))):
            errors.append(f"chapter id malformed: {c.get('id')!r}")
        expected_ch = c.get("id")
        if c.get("index") is not None and expected_ch != f"CH{c['index']:02d}":
            errors.append(f"chapter {c.get('id')} disagrees with index {c.get('index')}")
    return errors


def validate_approval_triplets(index: Dict[str, Any]) -> List[str]:
    """OAD-47/OAD-48: design approval, canon approval and shippability are separate.

    Enforcement: a location may not be Shippable unless canon-approved; and a
    location may not claim CanonApproved while its own approval.canon is false.
    This is the single most commonly violated rule in art-driven projects.
    """
    errors: List[str] = []
    for loc in index.get("locations", []):
        loc_id = loc.get("id", "<unknown>")
        approval = loc.get("approval", {})
        design = bool(approval.get("design"))
        canon = bool(approval.get("canon"))
        shippable = bool(approval.get("shippable"))
        status = loc.get("canon_status")

        if status == "CanonApproved" and not canon:
            errors.append(f"{loc_id}: canon_status=CanonApproved but approval.canon=false")
        if status == "DesignApproved" and not design:
            errors.append(f"{loc_id}: canon_status=DesignApproved but approval.design=false")
        if status == "Shippable" and not (design and canon and shippable):
            errors.append(f"{loc_id}: Shippable requires design+canon+shippable, got {approval}")
        if shippable and not canon:
            errors.append(f"{loc_id}: cannot be shippable before canon approval (OAD-47)")
        if canon and not design:
            # Legal but suspicious: recorded as a warning-only rule elsewhere.
            pass
    return errors


def validate_location_ids(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    seeen: Dict[str, int] = {}
    for loc in index.get("locations", []):
        loc_id = str(loc.get("id", ""))
        if not any(ID_PATTERNS[k].match(loc_id) for k in ("scene", "sublocation", "interior")):
            errors.append(f"location id does not match any canon pattern: {loc_id!r}")
            continue
        if _chapter_of(loc_id) != loc.get("chapter"):
            errors.append(f"{loc_id}: chapter field {loc.get('chapter')!r} disagrees with id prefix")
        seeen[loc_id] = seeen.get(loc_id, 0) + 1
    for loc_id, count in seeen.items():
        if count > 1:
            errors.append(f"duplicate location id registered {count} times: {loc_id}")
    return errors


def validate_memories(index: Dict[str, Any]) -> List[str]:
    """Hard narrative invariants from OAD-32 and the memories document."""
    errors: List[str] = []
    memories = index.get("memories", [])
    if len(memories) != 7:
        errors.append(f"exactly 7 memories are required, found {len(memories)}")

    location_ids = {loc.get("id") for loc in index.get("locations", [])}
    seen_indexes, seen_chapters, seen_scenes, seen_locations = [], [], [], []

    for mem in memories:
        idx = mem.get("index")
        ch = mem.get("chapter")
        scene = mem.get("scene_id")
        loc = mem.get("location_id")
        seen_indexes.append(idx)
        seen_chapters.append(ch)
        seen_scenes.append(scene)
        seen_locations.append(loc)

        if ch not in MEMORY_CHAPTER_IDS:
            errors.append(f"memory {idx}: chapter {ch!r} outside CH01..CH07")
        if not ID_PATTERNS["scene"].match(str(scene or "")):
            errors.append(f"memory {idx}: scene id malformed: {scene!r}")
        elif _chapter_of(str(scene)) != ch:
            errors.append(f"memory {idx}: scene {scene} is not in chapter {ch}")
        if not any(ID_PATTERNS[k].match(str(loc or "")) for k in ("sublocation", "interior", "scene")):
            errors.append(f"memory {idx}: location id malformed: {loc!r}")
        elif _chapter_of(str(loc)) != ch:
            errors.append(f"memory {idx}: location {loc} is not in chapter {ch}")
        if loc not in location_ids:
            errors.append(
                f"memory {idx}: discovery location {loc} is not registered as a location "
                f"(add it, or the memory can never be found at runtime)"
            )
        fragments = mem.get("fragments", {})
        for key in ("place", "object", "sound", "interaction"):
            if not str(fragments.get(key, "")).strip():
                errors.append(f"memory {idx}: fragment '{key}' is empty (OAD-32 requires all four)")

    if sorted(x for x in seen_indexes if isinstance(x, int)) != list(range(1, 8)):
        errors.append(f"memory indexes must be exactly 1..7, got {sorted(seen_indexes)}")
    if sorted(c for c in seen_chapters if isinstance(c, str)) != list(MEMORY_CHAPTER_IDS):
        errors.append(f"memories must occupy exactly one chapter each in CH01..CH07, got {seen_chapters}")
    if len(set(seen_scenes)) != len(seen_scenes):
        errors.append(f"duplicate memory scene ids: {seen_scenes}")
    if len(set(seen_locations)) != len(seen_locations):
        errors.append(f"duplicate memory discovery locations: {seen_locations}")
    if len(set(seen_indexes)) != len(seen_indexes):
        errors.append(f"duplicate memory indexes: {seen_indexes}")
    return errors


def validate_bosses(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    chapter_bosses = {c.get("id"): c.get("boss") for c in index.get("chapters", [])}
    bosses = index.get("bosses", [])
    seen = []
    for boss in bosses:
        boss_id = str(boss.get("id", ""))
        seen.append(boss_id)
        if not ID_PATTERNS["boss"].match(boss_id):
            errors.append(f"boss id malformed: {boss_id!r}")
            continue
        ch = boss.get("chapter")
        if _chapter_of(boss_id) != ch:
            errors.append(f"{boss_id}: chapter field {ch!r} disagrees with id prefix")
        expected_boss = chapter_bosses.get(ch)
        if expected_boss is not None and expected_boss != boss.get("name"):
            errors.append(
                f"{boss_id}: name {boss.get('name')!r} disagrees with chapter table {expected_boss!r}"
            )
        if boss.get("arena_design_status") == "CanonApproved" and boss.get("canon_status") != "CanonApproved":
            errors.append(f"{boss_id}: arena cannot be canon-approved while boss is not")
    for ch, boss_name in chapter_bosses.items():
        if not any(b.get("chapter") == ch and b.get("name") == boss_name for b in bosses):
            errors.append(f"chapter {ch} has boss {boss_name!r} but no matching boss entry")
    if len(set(seen)) != len(seen):
        errors.append(f"duplicate boss ids: {seen}")
    return errors


def validate_rules(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    rule_ids = []
    chapters = {c.get("id") for c in index.get("chapters", [])}
    for rule in index.get("chapter_rules", []):
        rid = str(rule.get("id", ""))
        rule_ids.append(rid)
        if not ID_PATTERNS["rule"].match(rid):
            errors.append(f"rule id malformed: {rid!r}")
        ch = rule.get("chapter")
        if ch is not None and ch not in chapters:
            errors.append(f"{rid}: chapter {ch!r} is not a known chapter")
        kind = rule.get("kind")
        if kind in ("spawn_exclusion", "asset_exclusion", "encounter_exclusion") and not rule.get("excludes"):
            errors.append(f"{rid}: exclusion rule of kind '{kind}' must list 'excludes'")
        if kind not in ("spawn_exclusion", "asset_exclusion", "encounter_exclusion") and rule.get("excludes"):
            errors.append(f"{rid}: 'excludes' is only meaningful on exclusion rules")
        if not str(rule.get("enforced_by", "")).strip():
            errors.append(f"{rid}: every rule must name how it is enforced")
    if len(set(rule_ids)) != len(rule_ids):
        duplicates = sorted({r for r in rule_ids if rule_ids.count(r) > 1})
        errors.append(f"duplicate rule ids: {duplicates}")
    return errors


def validate_source_documents(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for doc in index.get("source_documents", []):
        if not str(doc.get("drive_id", "")).strip():
            errors.append(f"source document {doc.get('id')!r} has no drive_id")
        if not str(doc.get("authority", "")).strip():
            errors.append(f"source document {doc.get('id')!r} has no declared authority")
    return errors


def validate_meta(index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    meta = index.get("meta", {})
    if tuple(index.get("approval_states", [])) != APPROVAL_STATES:
        errors.append(f"approval_states must be exactly {APPROVAL_STATES}")
    scheme = meta.get("id_scheme", {})
    for key, pattern in scheme.items():
        if key in ID_PATTERNS and pattern != ID_PATTERNS[key].pattern:
            errors.append(
                f"meta.id_scheme['{key}'] disagrees with code: {pattern!r} != {ID_PATTERNS[key].pattern!r}"
            )
    return errors


ALL_CHECKS = (
    validate_meta,
    validate_chapters,
    validate_approval_triplets,
    validate_location_ids,
    validate_memories,
    validate_bosses,
    validate_rules,
    validate_source_documents,
)


def validate_index(index: Dict[str, Any], schema: Dict[str, Any] | None = None) -> List[str]:
    """Return every problem found. An empty list means the index is valid."""
    errors: List[str] = []
    missing = [k for k in REQUIRED_KEYS if k not in index]
    if missing:
        errors.append(f"canon index missing required top-level keys: {missing}")
    if schema is not None:
        errors.extend(validate_against_schema(index, schema))
    for check in ALL_CHECKS:
        errors.extend(check(index))
    return errors


# --------------------------------------------------------------------------- #
# Query helpers used by engine-side mirrors and by tests
# --------------------------------------------------------------------------- #

def memory_by_index(index: Dict[str, Any], memory_index: int) -> Dict[str, Any]:
    for mem in index.get("memories", []):
        if mem.get("index") == memory_index:
            return mem
    raise CanonError(f"no memory with index {memory_index}")


def rules_for_chapter(index: Dict[str, Any], chapter: str) -> List[Dict[str, Any]]:
    return [r for r in index.get("chapter_rules", []) if r.get("chapter") == chapter]


def global_rules(index: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [r for r in index.get("chapter_rules", []) if r.get("chapter") is None]


def exclusions_for_chapter(index: Dict[str, Any], chapter: str) -> List[str]:
    excluded: List[str] = []
    for rule in rules_for_chapter(index, chapter):
        excluded.extend(rule.get("excludes", []))
    return excluded


def all_memory_tuples(index: Dict[str, Any]) -> List[Tuple[int, str, str, str]]:
    return [
        (m["index"], m["chapter"], m["scene_id"], m["location_id"])
        for m in index.get("memories", [])
    ]


def iter_locations(index: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    yield from index.get("locations", [])
