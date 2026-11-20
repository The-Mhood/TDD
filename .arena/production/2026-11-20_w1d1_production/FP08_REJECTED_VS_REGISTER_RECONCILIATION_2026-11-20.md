# FP-08 — REJECTED SUBMISSIONS vs APPROVAL REGISTER — RECONCILIATION (W1 D1, read-only)
**2026-11-20 · Original VA · register `ART_BIBLE_MASTER_INDEX_POST_SYNC_2026-11-16.md` NOT edited (re-issue only on owner instruction) · nothing promoted; no status changed anywhere.**

## 1. What was enumerated (Drive, read-only, today)
- **`16_REJECTED_DESIGNS`**: query `name contains 'REJECTION_REPORT'` → **56 exact-version rejection reports** (next_page_token null). Parent folder holds ≥100 items on page 1 (unenumerated remainder); subfolder `OUR_EYES_FINAL_193_REJECTED` (`1hkC-Mt2rI3o-ne-DoMtNxjxqbarCxYoG`) holds **11 images** (see FP-09): SCN-017 V002, SCN-024 V002, CH03-EXP-001 (byte-original `1CFCPrQc…`), CH06-INT-004/005, CH05-SET-002/LMK-002/INT-002/SUB-003/EXP-002, CH04-EXP-003.
- Register: 208 rows (parsed programmatically 2026-11-20).

## 2. The reports name these subjects (union of both listings; full text IDs in Drive)
- **CH01 scene studies, V001 (never register rows):** SCN-006/007/008/009/010/012/013/014/015(FISHING_STREAM)/017/019/021/022/024/025/027/028/030/032/033/034 · EXP-003/004/005 · SUB-017 (Fishing Shelter) · SCN-015 FISHING_STREAM is additional to the earlier session's list.
- **Adanna turnaround plates (never register rows):** FRONT/BACK/LEFT_SIDE/THREE_QUARTER **V001 and V002** (8 reports, two distinct defect generations).
- **Interior & landmark corrections, V001:** CH02-INT-002/003/004/005, CH02-SET-001, CH02-SUB-004/005, CH02-TRV-006 (the CH02 rejection wave) · CH03-INT-002 (Potter's Shop).
- **Ancestral Realm successors (never register rows):** ESTABLISHING **V006, V008, V009, V010, V011, V012** (V013 was authorised-brief, not reported) · VR-008 SEALED_QUARTER **V006, V007, V008** · `WALL_OF_HOUSES_V004` · VR-010 WASHING_PLACE **V004** (V005 later recorded APPROVED-U27 by third party per sync log; outside this agent's scope).
- **Other:** REJECTION_REPORT_ENV_CH02-* set; wave images see FP-09.

## 3. Mapping against the 208-row register (the reconciliation answer)
| Rejected item class | In register? | Register disposition today | Correct treatment |
|---|---|---|---|
| SCN-* / EXP-* / SUB-017 (CH01 studies) | **NO** — scene/moodboard pool never registered | n/a | Attach as **rejection evidence annotations** to their parent location rows (VILLAGE_SQUARE, MARKET, PALACE_COURTYARD, KITCHEN…) in re-issue; do NOT add rows; keep md5s |
| Adanna turnaround V001/V002 | **NO** | n/a | Annotation on OAD-02 Adanna master row + turnaround lineage pointer |
| ESTABLISHING V006–V012 | **NO** (register holds only CH08 exploratory V001–V005) | V001–V005 stay REVIEW REQUIRED as-is | Annotate exploratory CH08 block; the rejected successors never entered review |
| VR-008 SEALED_QUARTER V006–V008 | **NO** (register: V001–V002 exploratory + **V003 APPROVED**) | **APPROVED row V003 is NOT affected** — different file lineage; design approval intact (canon still OAD-48) | Explicit guard: forbid any conflation of rejected VR-008/V006–V008 with approved V003 in re-issue notes |
| WALL_OF_HOUSES_V004, VR-010_WASHING_PLACE_V004 | **NO** | Registered WASHING_PLACE_V001 remains REVIEW REQUIRED, unaffected | Note only |
| CH02 / CH03 rejection wave | **NO** | Register CH02 `SEALED_GATE_V003` REVIEW REQUIRED unchanged; CH03 rows: none exist | Re-issue must carry a standing note: "CH02/CH03 candidate pool exists and is REJECTED; no approvals implied for later re-dos" |
| 11 wave images (FP-09) | Mostly **NO**; includes `1CFCPrQc…` = CH03-EXP-001 byte-original (earlier flagged PENDING; now observed inside the wave folder) | n/a — visibility only | Flag to owner: preservation evidence moved by external actor; restore/disposition = owner/file-owner act; do not delete |

## 4. Register-row status changes justified by written rejection evidence: **NONE**
Every written rejection concerns a **non-register-row** (moodboard/candidate pool). The 208-row register therefore stays factually intact; its defects are of a different kind:
- **Staleness:** register predates the 56 reports; rows that *should* carry "candidate rejected" notes don't (e.g., VILLAGE_SQUARE_V001 — every Batch-1/2/3 successor rejected; board itself untouched by that fact).
- **Flatness:** no linkage from scene-study rejects to location rows, so the bible understates known failure patterns (European gables SCN-017, Sahelian towers SCN-012, E/SE-Asian interior SCN-008, masonry ESTABLISHING V008–V012…).
- **Missing pool ledger:** the rejected unregistered pool (~120+ files implied by reports+wave) has no register section.

## 5. Proposed re-issue delta (owner decision; NOT executed)
1. Add §1b "Candidate-pool dispositions (2026-11-17/18 rejection wave)" enumerating the 56 reports + 11-wave images with md5s and defect-brief pointers; zero status changes.
2. Annotate ~25 location rows with "all known scene-study successors rejected <list>"; zero status changes.
3. Add CH07/CH08-adjacent note: VR-008 lineage rejected; V003 (approved design) unaffected; canon still pending OAD-48.
4. Keep the 16 APPROVED rows byte-identical; keep §0 count 9 subjects.
5. Regenerate annex counts; keep md5 of this file; version the register (v8 proposal) only on owner instruction.

## 6. What would make the register untrustworthy if skipped
Approving/rejecting any board by filename alone; folding the 11 wave files into "193" claims; treating D12/D14/D15/D16 KEEP records as approvals; treating ESTABLISHING_V012 rejection brief items as resolved (V013 still needs exact-version RR_ before verdict — see FP-10).
