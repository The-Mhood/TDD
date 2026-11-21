# DESIGN PRODUCTION INVENTORY — all chapters (2026-12-06)
Method: repo file audit (counts in JSON sibling) + 2026-11-20 gap-analysis denominators + production since. **Exists != approved; produced != qualified; qualified != integrated.** Accountable: Design Lead (this agent) for all Design rows; qualification = Owner-Mac/TA; integration = PM/Engineering.

| Category | Total required | Produced | Accepted | Awaiting review | Rejected/rework | Awaiting qualification | Awaiting Unreal integration | Not started | Next deliverable / target |
|---|---|---|---|---|---|---|---|---|---|
| Adanna (identity, model, costume) | Concept set + 3D + facial milestone | Concept set, V5 3D, presentation | Concept APPROVED; V5 production-approved | Facial tier (owner) | V001 turnarounds superseded | V5 (Mac) | V5 after qual. | Facial sculpt | Owner tier decision -> PoC (W4, see schedule) |
| Guard class | Model + poses + clips | V3, board, 5 clips | Production-approved | — | V1/V2 superseded (fallback retained) | V3 (Mac) | After qual. | — | Mac run |
| Supporting/named cast 3D | Per register roster (identities unapproved) | 0 3D | 0 | Register identities await Story/CD verdicts | — | — | — | All | **Missing decision: Story/CD identity approvals** -> PM |
| Civilian NPCs | Clothing ref + family | 6 assets + clips + boards | Production-approved | — | 3 board attempts (logged) | NPC FBX (later Mac batch) | 6 GLBs | — | PM density pick |
| Enemies beyond Guard | Undefined | 0 | 0 | — | — | — | — | All | **Missing: PM/story class list** |
| CH01 environment | Kit + compound + states ST01-07 | Kits, compound, populated x3, dressing, ST01-04 keys, ST05-07 PENDING keys | ST01-04 provisional | ST05 Rain/ST06 Market/ST07 Gathering (PENDING, this batch) | ST06 attempt1 (modern shirts) | n/a (OBJ) | All OBJs | Final locked layout (PM greybox) | PM confirms ST mapping + density |
| CH02-CH07 environments | Per chapter registers (gap analysis: ~74 L2 studies + approvals backlog) | Candidate scene art only (CH02 16, CH03 17, CH04 10, CH05 6, CH06 2 files) | 0 approved | All candidates await CD/owner verdicts | Known defect boards flagged in gap analysis | — | — | Production kits per chapter | **Missing: chapter approval verdicts (CD/owner)** - Design cannot self-approve canon environments |
| CH08 environments | 5 designs | 5 (pre-existing) | Design-approved (NOT canon, OAD-48) | Canon/location register pending | — | — | — | Kits | Owner canon decision |
| Animation | Adanna/Guard/civilian sets | 6+5+2 clips, 3 boards | Production-approved | — | — | FBX via Mac | All clip JSONs | Enemy anims (no classes), traversal/combat beyond unarmed sets (gameplay undefined) | PM gameplay anim list |
| VFX | Physical set | 8 sprites + spec + sheet | Approved | — | — | — | Niagara assembly (TD) | Ability/supernatural (undefined) | TD assembly |
| Lighting/weather | CH01 states | ST01-07 keys (4 accepted prov. + 3 pending) | 4 | 3 | — | — | TD lighting impl. | Other chapters' states | PM ST mapping confirm |
| Cinematics/UI | Boards + specs | 2 cine boards, UI board+spec, HUD + menu refs | Concept-approved | — | — | — | UX/TD impl. | Storyboard frames (cinematics unscoped by Story) | Story cinematic list |

## Definition conflict raised to PM (exact decision needed)
Repo spec (2026-11-17) maps ST05=market, ST06=ritual, ST07=festival with ST06/ST07 culturally excluded; the W3 directive renames ST05=Rain, ST06=Market day, ST07=Gathering as approved. Design produced PENDING keys under the new names with everyday-only content (no ritual/regalia/ceremony) and needs **PM to confirm the authoritative ST05-ST07 mapping** before any of the three is promoted beyond PENDING.
