#!/usr/bin/env python3
"""Generate world data for the engine mirror from parsed register excerpts.

WHY
---
Hand-copying 191 location entries and 135 scenes from 812 KB of Googled Docs
into JSON is exactly how canon drift starts. Where a register excerpt has been
captured, the derived data is generated from it and the output is committed, so
reviewers can see the diff.

INPUT
-----
`Tools/canon/tests/fixtures/*.md` — verbatim excerpts of the real registers.
These are named `*_ch01_excerpt` because only Chapter 1 has been read so far.

OUTPUT
------
`Tools/canon/data/canon_index.json` — updated in place for the locations and
scenes captured in the excerpts. Existing entries not present in the excerpt are
left untouched (they are either verified elsewhere or marked UNVERIFIED).

IMPORTANT
---------
The fixtures are EXCERPTS. Generating from them must never overwrite a record
that was read from a different part of the register. The generator therefore
only ADDS or REFRESHES records whose id appears in the parsed excerpt, and
prints a summary of what changed.

Dependency policy: stdlib only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import registers as reg  # noqa: E402

REPO = HERE.parents[1]
INDEX = HERE / "data" / "canon_index.json"
FIXTURES = HERE / "tests" / "fixtures"
LOC_FIXTURE = FIXTURES / "location_register_ch01_excerpt.md"
SCN_FIXTURE = FIXTURES / "scene_register_ch01_excerpt.md"


def build(index: dict, loc_text: str, scn_text: str) -> tuple[dict, list[str]]:
    log: list[str] = []
    locations = reg.parse_location_summary(loc_text)
    scenes = reg.parse_scene_summary(scn_text)

    existing = {loc["id"]: loc for loc in index["locations"]}

    for rec in locations:
        design_status, annotation = reg.normalise_design_status(rec.env_design_status)
        entry = {
            "id": rec.id,
            "chapter": rec.chapter,
            "name": rec.name,
            "category": rec.category,
            "kind": rec.kind,
            "canon_status": rec.canon_status,
            "env_design_status": design_status,
            "verified_against_register": True,
            "source": f"LOCATION_MASTER_REGISTER#{rec.chapter}",
        }
        if annotation:
            entry["register_annotation"] = annotation
        if rec.id in existing:
            if existing[rec.id] != entry:
                log.append(f"refresh  {rec.id}")
                existing[rec.id].update(
                    {k: v for k, v in entry.items() if k != "notes"}
                )
        else:
            log.append(f"add      {rec.id:<20} {rec.canon_status}")
            index["locations"].append(entry)

    # Scene parents become registered locations if the excerpt referenced them
    # but the location table did not include them (they are real register entries
    # that the excerpt simply did not repeat). Mark UNVERIFIED rather than
    # guessing their status.
    known = {loc["id"] for loc in index["locations"]}
    for scn in scenes:
        parent = scn.parent_id
        if parent and parent not in known:
            index["locations"].append({
                "id": parent,
                "chapter": reg.chapter_of(parent) or "",
                "name": f"(name not in captured excerpt for {scn.id})",
                "category": reg.category_of(parent) or "SUB",
                "kind": "UNVERIFIED",
                "canon_status": "UNVERIFIED",
                "env_design_status": "UNVERIFIED",
                "verified_against_register": False,
                "source": "SCENE_AND_MICROLOCATION_MASTER_REGISTER (parent reference)",
                "notes": "Referenced as a scene parent but its own register row was "
                         "not in the captured excerpt. Status must be read before use.",
            })
            known.add(parent)
            log.append(f"add      {parent:<20} UNVERIFIED (scene parent)")

    index["meta"]["generated_from"] = {
        "from": ["location_register_ch01_excerpt.md", "scene_register_ch01_excerpt.md"],
        "note": "Only Chapter 1 has been captured. Other chapters remain UNVERIFIED.",
        "log": log,
    }
    return index, log


def main() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    if not LOC_FIXTURE.is_file() or not SCN_FIXTURE.is_file():
        print("fixtures missing; nothing to generate")
        return 1
    index, log = build(
        index,
        LOC_FIXTURE.read_text(encoding="utf-8"),
        SCN_FIXTURE.read_text(encoding="utf-8"),
    )
    INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"locations now: {len(index['locations'])}")
    for line in log:
        print(" ", line)
    if not log:
        print("  (no changes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
