# Design Production Assignment — Measurable Output & Handoffs

**Document ID:** TDD-IMPL-DESIGN-PROD-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM (for Design). **Purpose:** Convert the visual production inventory into **measurable production quantities and asset handoffs** — not another weekly plan. Design continues producing while W2 engineering runs (parallel, non-blocking).
**Status definitions:** NOT STARTED → IN PROGRESS → DELIVERED / AWAITING REVIEW → ACCEPTED. Plus BLOCKED, REWORK REQUIRED, AWAITING INTEGRATION, UNTOUCHED.
**Rule:** a delivered asset is not automatically accepted; an accepted asset is not automatically integrated. Do not invent quantities — flag missing scope definitions.

---

## 1. Measurable inventory (required / produced / accepted / provisional / rework / awaiting-integration / untouched)

| Category | Required | Produced | Accepted | Provisional/Awaiting review | Rejected/Rework | Awaiting integration | Untouched |
|---|---|---|---|---|---|---|---|
| **Main characters (7)** | 7 | 7 (boards) | 1 (Adanna master APPROVED) | 6 (REVIEW REQUIRED) | 0 | 0 | 0 (models not built except Adanna) |
| **Supporting characters (13)** | 13 | 13 (boards) | 0 (names approved) | 13 | 0 (Mgborie BLOCKED) | 0 | 0 (models not built) |
| **Character models/likeness** | 20 | 1 (Adanna V3 modelled) | 0 (in-engine) | 1 (FBX prepared) | 0 | 1 (W2-R4) | 19 |
| **Facial likeness (Adanna)** | 1 | 0 (face not built) | 0 | 0 | 0 | 0 | 1 (pipeline v2.1 ready) |
| **Clothing/accessories/variations** | TBD | Several | 0 | Several | 0 | 0 | TBD |
| **Enemy archetypes (6)** | 6 | 0 | 0 | 0 | 0 (Maskbearer mask rejected) | 0 | 6 (CD-3 unratified) |
| **Environments/kits (8 chapters)** | 8 | CH01 compound V2 + kits | 0 (provisional) | CH01 kits | 3 rejected attempts | 0 | Ch.2–8 kits |
| **Props/interactive objects** | TBD | Some | 0 | Some | 0 | 0 | TBD |
| **Character movement/combat anims** | 6+ | 6 (Adanna movement clips) | 0 | 6 | 0 | 0 | Combat anims |
| **Deformation checks** | 46 | 46 | 46 (PASS) | 0 | 0 | 0 | 0 |
| **Enemy anims/combat behaviours** | TBD | 0 | 0 | 0 | 0 | 0 | TBD (CD-3) |
| **VFX/environmental effects** | TBD | Some (white lightning direction) | 0 | Some | 0 | 0 | TBD |
| **Lighting/atmosphere** | CH01 3 keys | 3 (dawn/dusk/night) | 0 | 3 (REVIEW) | 0 | 0 | Ch.2–8 |
| **Cinematic/narrative assets** | TBD | 0 | 0 | 0 | 0 | 0 | TBD |
| **UI/gameplay visuals** | TBD | 0 | 0 | 0 | 0 | 0 | TBD |

**Missing scope definitions (PM + Design to establish, not invent):** clothing/accessory variation count, props count, enemy animation count, VFX count, cinematic count, UI count.

## 2. Prioritised production (actual work, in order)

Design proceeds on this priority while W2 engineering runs. Every deliverable is handed to PM for reconciliation against the roadmap + register.

| Priority | Deliverable | Quantity target | Status | Handoff | Needs from |
|---|---|---|---|---|---|
| **P1** | **Adanna facial likeness** (run v2.1 on Mac → renders/QC) | 1 face PoC | IN PROGRESS (pipeline ready; owner-Mac run required) | Facial FBX → Eng (UE import) | Owner (Mac run), Tech Art (QC) |
| **P2** | **CH01 greybox + environment completion** | 1 playable greybox + CH01 kit finalisation | IN PROGRESS (plan exists; in-engine build is W2-R5) | CH01 level → Eng | Eng (W2-R5) |
| **P3** | **ST05–ST07 production** (Rain / Market day / Gathering) | 3 approved scene states | NOT STARTED (approved; production pending) | Scene assets → Eng | — |
| **P4** | **Character animation integration** (6 movement clips) | 6 clips integrated | PRODUCED, awaiting integration | Anim sequences → Eng | Eng |
| **P5** | **Remaining character production** (supporting cast) | batch (scope-defined) | NOT STARTED (boards REVIEW REQUIRED) | Models → Eng | Character Art capacity, naming approval |
| **P6** | **Environment kits (Ch.2+)** | Ch.2–8 kits | NOT STARTED | → Eng | — |
| **P7** | **Enemy visual production** | 6 archetypes | NOT STARTED (CD-3 unratified) | → Eng | Owner (CD-3), Story |
| **P8** | **VFX, lighting, props, chapter-specific assets** | TBD | NOT STARTED | → Eng | Scope definition |

## 3. Design-to-PM reporting
- Design reports execution to PM at the agreed production checkpoints (this assignment is the baseline).
- **Each report must state:** produced quantity, accepted quantity, rework, integration status, untouched quantity, and the **exact asset location / repository path** for every deliverable.
- PM reconciles Design's report against: the original game requirements, the visual production register, the chapter asset requirements, the actual Drive/repository outputs, and Technical Art/Engineering integration status.
- **Design owns** visual production + internal visual review. **PM owns** production coordination, scope reconciliation, schedule, dependencies, acceptance tracking and handoffs.

## 4. Independent-work rule
A blocked character (e.g. waiting on naming approval) must **not** prevent unrelated environment, animation or scene production. Design continues P2–P4 and environment work regardless of W2 integration status or CD-3 delays.

## 5. Immediate next deliverable (this cycle)
**P1 + P2:** (a) the owner runs the facial PoC v2.1 → face + QC (see `FACIAL_POC_OWNER_EXECUTION_PROCEDURE.md`); (b) Design finalises the CH01 greybox layout for W2-R5 in-engine build. Both hands off to PM for register reconciliation.
