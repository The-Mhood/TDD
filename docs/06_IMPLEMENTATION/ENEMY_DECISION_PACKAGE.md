# Enemy Taxonomy Decision Package — Reconciled with Story Dispositions

**Document ID:** TDD-IMPL-ENEMYDEC-001 · **Version:** 2.0 · **Date:** 2026-11-21
**Author:** PM/Story. **Status:** RECONCILED — Story narrative dispositions merged in; **awaiting owner/CD ratification.**
**Purpose:** Reconcile the six PROPOSED archetypes with Story's narrative dispositions. **No archetype is approved, canon, or built.** CD-3 is NOT ratified; CD-2 cultural holds remain active.

## Story narrative dispositions (merged in)
Story has supplied narrative dispositions for the six archetypes. These are **Story recommendations, not final owner/CD ratification.** PM reconciles them below rather than restarting from zero.

| # | Archetype (proposed) | Story disposition | PM reconciliation | Cultural/canon exposure | Status |
|---|---|---|---|---|---|
| 1 | **Rootwarden** | Retain as a fictional slow bruiser | Accepted. Fictional creature; teaches spacing/punish. Bark/root material, no metal. | Medium — must not read as a known Igbo figure | **Story: RETAIN** — owner ratification pending |
| 2 | **Thrall** | Revise as a **non-humanoid hostile swarm** | Accepted. The non-humanoid revision resolves the highest cultural risk (no humanoid-dead mythology). Swarm pressure retained; reads as a hostile natural/swarm phenomenon, not the dead. | **Reduced by revision** — but confirm the swarm is not a ritual/shrine image | **Story: REVISE (non-humanoid swarm)** — owner ratification pending |
| 3 | **Ash Hound** | Retain as a fictional ash-based fast flanker | Accepted. Fictional ash-surface flanker. **No remains** — ash must not read as bone. | Medium — material discipline | **Story: RETAIN** — owner ratification pending |
| 4 | **Ore Thrall** | Revise to **Ore Sentinel** | Accepted. Renamed **Ore Sentinel**. Cold, lightless, armoured hard target. **No flame in Ch.2.** | Low-medium — resolves via the Thrall revision | **Story: REVISE → Ore Sentinel** — owner ratification pending |
| 5 | **Thunder Aspirant** | Revise to **White-Arc Duelist** | Accepted. Renamed **White-Arc Duelist**. Disciplined elite duelist. **Lightning is white, always.** Renaming reduces the direct "aspirant/champion of Amadioha" doctrinal claim, but it still sits in Ch.5 (Amadioha's domain) — confirm no doctrinal invention. | High — Ch.5 religious context; white lightning only | **Story: REVISE → White-Arc Duelist** — owner ratification pending |
| 6 | **Maskbearer** | **Reject the mask-based identity**; preserve the gameplay role through an **ordinary physical enemy** | Accepted. Mask identity rejected (CD-2 blocked). The area-denial gameplay role is preserved via an ordinary physical enemy — no mask, no masquerade imagery. | **Resolved by rejection** — removes the CD-2 block on this archetype | **Story: REJECT mask identity → ordinary physical enemy** — owner ratification pending |

## Reconciled proposed roster (for owner ratification)
After applying Story's dispositions, the proposed roster is:

1. **Rootwarden** — fictional slow bruiser (Ch.1).
2. **Thrall** — non-humanoid hostile swarm (Ch.3/7). *(revised)*
3. **Ash Hound** — fictional ash-based fast flanker (Ch.3).
4. **Ore Sentinel** — cold armoured hard target (Ch.2). *(renamed from Ore Thrall)*
5. **White-Arc Duelist** — disciplined elite duelist (Ch.5). *(renamed from Thunder Aspirant)*
6. **[unnamed ordinary physical enemy]** — area-denial role, no mask (Ch.6). *(Maskbearer identity rejected; name TBD)*

## Remaining decision points for the owner
PM identifies the actual decision points — these are what the owner/CD must resolve:

1. **Ratify the reconciled roster** (KEEP/REVISE/REJECT each of the six above). Story dispositions are recommendations, not ratification.
2. **Thrall swarm form** — confirm the non-humanoid swarm expression is acceptable and does not read as a ritual/shrine image (cultural confirmation).
3. **White-Arc Duelist** — confirm the renamed elite duelist in Ch.5 does not invent doctrine about Amadioha; white lightning only.
4. **Maskbearer replacement name** — the mask identity is rejected; the ordinary physical enemy needs a name (Story/PM to propose; owner to approve).
5. **Ore Sentinel / White-Arc Duelist names** — confirm the renames are accepted (they replace Ore Thrall / Thunder Aspirant).
6. **Cultural review (CD-2)** — remains necessary for any sensitive cultural/religious representation; the Thrall and White-Arc Duelist revisions reduce but do not eliminate the need for specialist confirmation on Ch.3/Ch.5 content.

## Standing constraints (apply to every ratified archetype)
- No python/snake enemies, ever (`RULE-CH04-PYTHONS`).
- Children are never combat targets.
- Ch.2: no flame. Ch.3: no remains. Ch.5: lightning white only. Ch.7: earth/timber/cloth, ember not flame, starless.
- Ch.6: **no masks** (the Maskbearer mask identity is rejected).
- Adanna never mirrored; right side plain.
- **Shrine/mask/ritual content blocked by CD-2.**

## Engineering note (does not block decisions)
Engineering can build an AI base (StateTree, patrol, leash, telegraph, stagger, zone, swarm) that covers all six behaviours regardless of which survive. **The AI interface does not need to be decided before the creatures are.** Enemies are not built before the combat foundation + enemy interface exists (`WORLD_ARCHITECTURE.md`). Any approval now is approval to **design against**, not to build.

## Required owner action
Ratify the reconciled roster (per-archetype KEEP/REVISE/REJECT/APPROVE), confirm the cultural points above, and approve the Maskbearer-replacement name. PM records the ratified subset, the canon source, and cultural-clearance status in `PM_DEPENDENCY_REGISTER.md` (DP-03) and `VISUAL_PRODUCTION_REGISTER.md`, then proceeds only on ratified archetypes. **Until a decision is recorded, no enemy is promoted to approved production status.**
