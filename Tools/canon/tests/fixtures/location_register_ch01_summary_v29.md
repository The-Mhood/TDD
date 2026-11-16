# LOCATION MASTER REGISTER - Chapter 1 SUMMARY ROWS (complete, verbatim category field)

Captured from `LOCATION_MASTER_REGISTER.md` **v2.9** (2026-11-15), Drive file id
`1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5` (534,140 bytes), read 2026-11-16 with
`read_file_text` at `max_chars` 12000.

WHY THIS FILE EXISTS
--------------------
The existing excerpt fixture `location_register_ch01_excerpt.md` captures 13 of these
rows. That is enough for scene-parenting checks but NOT enough to reason about the
register's `Category` field, which is **multi-valued** ('Sub-location, Exterior,
Traversal Area'). A traversal contract that assumed the ID prefix determined the
category would silently drop three legitimate entries.

So this file captures the **complete** Chapter 1 summary table - all 57 location
entries - with the category field verbatim.

WHAT THIS FILE DOES AND DOES NOT REPLACE
-----------------------------------------
* It does NOT replace `location_register_ch01_excerpt.md`, which stays as the
  scene-parenting fixture with its own hierarchy section.
* It captures ONLY the summary table. The per-location detail sections,
  hierarchy bullets and environment-state tables are NOT here.
* `Canon Status` is transcribed verbatim. `REQUIRES REVISION` carries its parenthetical
  in the register ('patient in modern clothing'); the parenthetical is dropped here
  because it is art-review commentary, not a status value. The status word is exact.

## Counts check

Register publishes, for Chapter 1: 1 major environment, 40 other locations (not
interiors), 16 interiors = **57 location entries**.

| Family | rows below | expected |
|---|---|---|
| ENV | 1 | 1 |
| SUB | 23 | part of 40 |
| SET | 1 | part of 40 |
| LMK | 3 | part of 40 |
| TRV | 5 | part of 40 |
| EXP | 7 | part of 40 |
| BOS | 1 | part of 40 |
| INT | 16 | 16 |

SUB+SET+LMK+TRV+EXP+BOS = 23+1+3+5+7+1 = **40**. Plus ENV 1 + INT 16 = **57**. Matches.

## Summary

| Location ID | Location Name | Category | Canon Status | Environment Design Status |
|---|---|---|---|---|
| CH01-ENV-001 | The Forbidden Forest | Major Environment, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-001 | The Abandoned Shrine | Sub-location, Exterior, Story Location | PENDING APPROVAL | IN REVIEW |
| CH01-SUB-002 | The Abandoned Compound | Sub-location, Exterior | PROPOSED | IN REVIEW |
| CH01-SUB-003 | The Raffia Swamp | Sub-location, Exterior, Exploration Area | PROPOSED | IN REVIEW |
| CH01-SUB-004 | The Hunter's Camp | Sub-location, Exterior | PROPOSED | IN REVIEW |
| CH01-SUB-005 | The Waterfall Escarpment | Sub-location, Exterior, Landmark | PROPOSED | IN REVIEW |
| CH01-SUB-006 | Village Square | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-007 | Market | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-008 | Market Stalls | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-009 | Streets | Sub-location, Exterior, Traversal Area | ESTABLISHED | IN REVIEW |
| CH01-SUB-010 | Palace Courtyard | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-011 | Gathering Areas | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-012 | Farms | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-013 | Home Settlement - Local Fishing Stream | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-014 | Wells | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-015 | Water Collection Point | Sub-location, Exterior | ESTABLISHED | IN REVIEW |
| CH01-SUB-016 | The Old Campsite | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SUB-017 | The Overgrown Wall | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SUB-018 | The Wayside Offering Place | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SUB-019 | A Large Family Compound | Sub-location, Exterior, Interior | PROPOSED | IN REVIEW |
| CH01-SUB-020 | The Back Lanes | Sub-location, Exterior, Traversal Area | PROPOSED | NOT STARTED |
| CH01-SUB-021 | Compound Gardens | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SUB-022 | Animal Pens | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SUB-023 | The Washing Place | Sub-location, Exterior | PROPOSED | NOT STARTED |
| CH01-SET-001 | Home Settlement | Settlement, Exterior | ESTABLISHED | IN REVIEW |
| CH01-INT-001 | Throne Room | Interior, Story Location | ESTABLISHED | IN REVIEW |
| CH01-INT-002 | Kitchen | Interior | ESTABLISHED | IN REVIEW |
| CH01-INT-003 | Bedroom | Interior | ESTABLISHED | IN REVIEW |
| CH01-INT-004 | Stores | Interior | ESTABLISHED | IN REVIEW |
| CH01-INT-005 | Smithy | Interior | ESTABLISHED | IN REVIEW |
| CH01-INT-006 | The Leaning Shelter | Interior, Hidden Area | PROPOSED | NOT STARTED |
| CH01-INT-007 | A Small Family House | Interior | PROPOSED | IN REVIEW |
| CH01-INT-008 | The Healer's House | Interior | PROPOSED | REQUIRES REVISION |
| CH01-INT-009 | The Elder's House | Interior | PROPOSED | NOT STARTED |
| CH01-INT-010 | The Weaver's House | Interior | PROPOSED | IN REVIEW |
| CH01-INT-011 | The Potter's Yard | Interior, Exterior | PROPOSED | IN REVIEW |
| CH01-INT-012 | The Palm-Wine Shelter | Interior, Exterior | PROPOSED | NOT STARTED |
| CH01-INT-013 | The Gate Guard Shelter | Interior | PROPOSED | NOT STARTED |
| CH01-INT-014 | The Market Backrooms | Interior | PROPOSED | NOT STARTED |
| CH01-INT-015 | An Empty House | Interior | PROPOSED | NOT STARTED |
| CH01-INT-016 | A Household Ancestral Corner | Interior | PENDING APPROVAL | NOT STARTED |
| CH01-LMK-001 | The Great Tree | Landmark, Exterior | ESTABLISHED | IN REVIEW |
| CH01-LMK-002 | Palace | Landmark, Exterior | ESTABLISHED | IN REVIEW |
| CH01-LMK-003 | Gates | Landmark, Exterior | ESTABLISHED | IN REVIEW |
| CH01-TRV-001 | The Threshold Path | Traversal Area, Exterior, Story Location | PROPOSED | IN REVIEW |
| CH01-TRV-002 | The Root Way | Traversal Area, Exterior | PROPOSED | IN REVIEW |
| CH01-TRV-003 | The Stream Crossing | Traversal Area, Exterior | PROPOSED | IN REVIEW |
| CH01-TRV-004 | The Ravine and Liana Bridge | Traversal Area, Exterior | PROPOSED | IN REVIEW |
| CH01-TRV-005 | Roads | Traversal Area, Exterior | ESTABLISHED | IN REVIEW |
| CH01-EXP-001 | The Canopy Overlook | Exploration Area, Exterior | PROPOSED | IN REVIEW |
| CH01-EXP-002 | The Whispering Hollow | Exploration Area, Hidden Area, Exterior, Story Location | PENDING APPROVAL | IN REVIEW |
| CH01-EXP-003 | The Forgotten Path | Exploration Area, Exterior, Traversal Area | PROPOSED | NOT STARTED |
| CH01-EXP-004 | The Small Clearing | Exploration Area, Exterior | PROPOSED | NOT STARTED |
| CH01-EXP-005 | The Still Pool | Exploration Area, Exterior | PROPOSED | NOT STARTED |
| CH01-EXP-006 | The Hornbill Tree | Exploration Area, Exterior | PROPOSED | NOT STARTED |
| CH01-EXP-007 | The Duiker Run | Exploration Area, Exterior | PROPOSED | NOT STARTED |
| CH01-BOS-001 | Great Root Mother Arena | Boss Arena, Exterior | ESTABLISHED | IN REVIEW |
