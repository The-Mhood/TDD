# Enemy Taxonomy & Scene Briefs — PM/Story Deliverable

**Document ID:** TDD-IMPL-ENEMYSCENE-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM + Story, jointly. Coordinated by the Takeover Lead.
**Status:** PROPOSED — **CD-3 (enemy ratification) is NOT ratified.** Every enemy class below is a candidate for CD-3 ratification by the owner/Creative Director. None is canon, none is approved, none is built. Cultural holds (CD-2) remain active until formally cleared.
**Basis:** `ENEMY_ARCHETYPE_REVIEW.md` (Agent 2, TDD-CREAT-001 v1.0.0), `WORLD_ARCHITECTURE.md` (TDD-WARCH-001), the chapter rules, and the standing cultural constraints. **No mythology is invented.**

---

## Part 1 — Enemy taxonomy (proposed, for CD-3 ratification)

### Standing cultural / narrative constraints (canon — apply to every archetype)

| Constraint | Source | Effect |
|---|---|---|
| No python or snake enemies, ever | `RULE-CH04-PYTHONS` | Ch.4 has no serpentine enemy; pythons are never enemies or loot |
| Children are never combat targets | `RULE-NPC-CHILDREN-NO-COMBAT` | No child-model enemy; no child-adjacent threat framing |
| Ch.2 has no flame | Ch.2 rules | No fire-based enemy visuals in Ch.2 |
| Ch.3 shows no remains | Ch.3 rules | No bone/corpse/skeletal reads; ash, not snow |
| Ch.5 lightning is white only | Ch.5 rules | No coloured lightning variants |
| Ch.7 is earth/timber/cloth, ember not flame, starless | Ch.7 rules | Constrains armour, materials, light |
| Ch.6 masks are invented and featureless | `RULE-CH06-MASKS` | Any mask needs consultant review (CD-2) |
| Adanna is never mirrored; right side plain | Character canon | Do not mirror enemy silhouettes from her design |
| **Shrine / mask / ritual content is blocked by CD-2** | Consultant gate | Any archetype leaning on these cannot proceed past blockout until CD-2 closes |

### The six proposed archetypes

> **Status of each: PROPOSED — not ratified.** `canon_source: NONE EXISTS`; `built: NO`. Roles/behaviours are mechanical descriptions. Narrative relationships are **open questions for the CD**, not answers.

#### 1. Rootwarden — *proposed*
- **Role:** Slow heavy bruiser. Teaches spacing and punish windows.
- **Threat level:** Moderate (high damage, low mobility, leash-bound).
- **Behaviour:** Patrols a fixed route; slow turn rate; telegraphs a wide sweep; does not pursue beyond a leash radius; no ranged attack.
- **Distinguishing characteristics:** Bark/root material; reads as a forest guardian; no metal.
- **Capabilities (engineering):** StateTree base, ground nav, single attack, damage receive, stagger. Lowest-cost archetype.
- **Narrative constraint (OPEN for CD):** If the forest is ESTABLISHED but no creature is, does a guardian creature imply a belief about the forest the story has not established? Could the threat be environmental instead?
- **Visual identity / cultural:** Invented creature. Must not read as a known figure from Igbo tradition. Bark/root avoids metal. Needs visual review for accidental resemblance to masquerade or shrine-guardian imagery. **Canon risk: Medium.**

#### 2. Thrall — *proposed*
- **Role:** Weak swarm. Teaches group management and crowd control.
- **Threat level:** Low individually, collectively pressuring.
- **Behaviour:** Spawns in small groups; slow individual pursuit; no flanking; loses interest at a boundary.
- **Distinguishing characteristics:** Swarm presence; individually trivial.
- **Capabilities:** Cheap; benefits most from the CROWD tier rather than full per-actor AI. Good candidate for Mass.
- **Narrative constraint (OPEN for CD — most sensitive):** Ch.3 and Ch.7 are the lands of the dead. A humanoid "thrall" makes a claim about the dead that could read as a statement about ancestors — a cultural and narrative decision of the highest order.
- **Visual identity / cultural:** **High dependency.** Humanoid + death + Igbo-inspired setting is the precise combination that can invent mythology about the dead. Requires consultant review (CD-2) **before** CD-3. **Recommendation: consider a non-humanoid or environmental expression of the same combat pressure. Canon risk: High.**

#### 3. Ash Hound — *proposed*
- **Role:** Fast flanker. Forces the player to reposition.
- **Threat level:** Moderate (high mobility, burst damage).
- **Behaviour:** Circles at range, commits in bursts, retreats after a hit. Highest mobility archetype.
- **Distinguishing characteristics:** Ash-dulled surface; fast, skittering movement.
- **Capabilities:** Faster nav, flanking logic, burst movement. More expensive than Thrall.
- **Narrative constraint (OPEN for CD):** A dog-like creature invites a reading about hunting, domesticity or animal rites. Must not imply a real animal rite.
- **Visual identity / cultural:** Ash surface must obey "no remains" — ash is not bone and must not read as bone. **Canon risk: Medium.**

#### 4. Ore Thrall — *proposed*
- **Role:** Slow, cold, armoured. Teaches armour-breaking / positioning around a hard target.
- **Threat level:** High defence, low mobility.
- **Behaviour:** Very slow; high poise; cannot be staggered by light attacks; turns poorly.
- **Distinguishing characteristics:** Cold, lightless metal armour.
- **Capabilities:** Same base as Thrall with higher poise values. Cheap to add **if** Thrall exists.
- **Narrative constraint (OPEN for CD):** Does a "thrall" concept in Ch.2 make a claim about labour, binding or servitude in the underground kingdom?
- **Visual identity / cultural:** **No flame anywhere in Ch.2.** Cannot carry ember/torch/forge visuals. Metal reads must be cold and lightless. **Canon risk: Low-medium, but blocked by its dependency on Thrall's unresolved question.**

#### 5. Thunder Aspirant — *proposed*
- **Role:** Elite. Human-scale, disciplined, duel-like.
- **Threat level:** High (disciplined counter-attacker).
- **Behaviour:** Single opponent; holds distance; counter-attacks; does not chain-stun. Deliberately the most "fair" archetype.
- **Distinguishing characteristics:** Disciplined, regal; white electrical effects.
- **Capabilities:** Highest per-actor cost; needs defensive logic and timing windows.
- **Narrative constraint (OPEN for CD — canon constraint):** "Aspirant" implies a relationship to Amadioha's champion — a claim about the chapter's central religious figure. Electrical effects must be **white only**.
- **Visual identity / cultural:** Lightning is white, always. Any regalia needs review — this archetype sits closest to a religious figure and is the easiest place to invent doctrine by accident. **Recommendation: CD decides whether this archetype can exist at all before its behaviour is specified. Canon risk: High.**

#### 6. Maskbearer — *proposed — BLOCKED by CD-2*
- **Role:** Area-denial. Presence changes where the player can stand.
- **Threat level:** Control-oriented (zone denial, low chase).
- **Behaviour:** Largely stationary; projects a zone; turns slowly toward the player. Low chase, high control.
- **Distinguishing characteristics:** Featureless invented mask (canon for Ch.6).
- **Capabilities:** Zone/aura system; cheapest AI, most expensive VFX and visual review.
- **Narrative constraint (OPEN for CD — blocked by CD-2):** Ch.6 is the masks chapter. Any mask content is under consultant gate. Whether a *wearer* exists is a story claim.
- **Visual identity / cultural:** **Highest in the list.** Featureless invented masks are canon for Ch.6. Requires consultant review (CD-2) and **must not resolve until that gate does.** **Canon risk: High, and currently blocked. Recommendation: withdraw until CD-2 closes.**

### Risk summary (by cultural/narrative exposure, not build cost)

| Rank | Archetype | Risk | Recommendation |
|---|---|---|---|
| 1 | Maskbearer | High, blocked | Do not proceed; blocked by CD-2 |
| 2 | Thrall | High | CD to consider non-humanoid alternative |
| 3 | Thunder Aspirant | High | Decide existence before behaviour |
| 4 | Rootwarden | Medium | Safest; still needs visual review |
| 5 | Ash Hound | Medium | Manageable with material discipline |
| 6 | Ore Thrall | Low-medium | Resolve via Thrall |

**PM position:** the taxonomy is delivered as the CD-3 decision package. **Ratification is the owner/CD's decision, not PM's.** Engineering can build an AI base supporting patrol, leash, telegraph, stagger and zone behaviours that covers all six regardless of which survive — the interface does not need to be decided before the creatures are. Enemies cannot be built before the combat foundation and enemy interface exist; any approval now is approval to **design against**, not to build.

---

## Part 2 — Scene briefs (PM/Story)

> **Basis:** `WORLD_ARCHITECTURE.md` — 8 chapters, 1 major environment per chapter, locations `CHxx-{SUB,SET,INT,LMK,TRV,EXP,BOS}-nnn`, **135 scenes** total, environment states `ES_<Chapter>_<Time|Weather|Supernatural>`. Scene IDs are permanent. Scene briefs below cover the W1/W2 production-relevant scenes; the full 135-scene register is the source of truth for population and IDs. Cultural review is mandatory where applicable; existing cultural holds remain active.

### Scene brief template (applied to each)
- **Narrative purpose** · **Gameplay purpose** · **Location & environment** · **Architecture / props / population** · **Cultural references & restrictions**

### SB-1 — CH01 Forbidden Forest (opening traversal + first encounter)
- **Narrative purpose:** Establish the forest, Adanna's world, and the first threat; introduce traversal and the encounter beat.
- **Gameplay purpose:** Movement/traversal lab (AC-01…13, E1–E7) + first combat encounter vs a dummy or pilot archetype.
- **Location & environment:** CH01-ENV-001; dense forest, dappled light; environment state ES_CH01_Time (dawn/dusk).
- **Architecture/props/population:** Greybox zones (Z_Flat, Z_Steps, Z_Corridor1/2, Z_Dodge per M1 spec §7); trees, rocks, ruins; PlayerStart per zone; 0–1 pilot encounter actor; NPCs minimal.
- **Cultural references & restrictions:** Forest is ESTABLISHED. **No creature is canon until CD-3 ratifies an archetype.** If a Rootwarden-style encounter is used, it is labelled `PENDING_CONTENT` pending CD-3 + visual review. No shrine/mask/ritual content (CD-2 hold).

### SB-2 — CH01 settlement / compound (interaction + memory anchor)
- **Narrative purpose:** Introduce interaction, a memory anchor, and the world's human presence.
- **Gameplay purpose:** Interaction volumes (T36), checkpoint marker, metrics overlay (M1-P5); save/load smoke point.
- **Location & environment:** CH01-SUB/SET; family compound; indigo/clay/plaster (smoother-maintained-clay-plaster correction — the compound view is the plaster authority).
- **Architecture/props/population:** Huts/interiors/palace shells (W1 D4 source patch); doorway shells; NPC population per the 29-scene register; no combat population.
- **Cultural references & restrictions:** Settlement identity per the M1 art spec; no sacred vocabulary without CD-2 sign-off. Environment Kit V1 stays provisional, never canon.

### SB-3 — CH03 City of the Living Dead (the dead lands)
- **Narrative purpose:** The dead lands; ash, not snow; the register's constraints.
- **Gameplay purpose:** Swarm/crowd encounter (Thrall-class pressure, if ratified); group management.
- **Location & environment:** CH03-ENV-001; ash-covered, no remains; ES_CH03_Time.
- **Architecture/props/population:** Ruined structures; ash ground; swarm population.
- **Cultural references & restrictions:** **No bone/corpse/skeletal reads** (ash, not snow). **A humanoid dead-enemy is the most sensitive cultural question** — CD-2/CD-3 must clear before any humanoid enemy here. Thrall is PROPOSED only.

### SB-4 — CH06 Kingdom of Masks (mask chapter)
- **Narrative purpose:** The masks chapter; featureless masks are canon.
- **Gameplay purpose:** Area-denial encounter (Maskbearer-class, if ever ratified).
- **Location & environment:** CH06-ENV-001; mask-themed architecture.
- **Architecture/props/population:** Featureless mask props; zone-denial actor.
- **Cultural references & restrictions:** **Fully blocked by CD-2.** Featureless invented masks are canon for Ch.6, but any mask content requires consultant review. Maskbearer is withdrawn until CD-2 closes.

### SB-5 — CH05 Mountain of Thunder (elite duel)
- **Narrative purpose:** The thunder/mountain chapter; Amadioha's domain.
- **Gameplay purpose:** Elite duel encounter (Thunder Aspirant-class, if ratified).
- **Location & environment:** CH05-ENV-001; mountain; white lightning.
- **Architecture/props/population:** Elevated terrain; duel arena.
- **Cultural references & restrictions:** **Lightning is white, always** — no coloured variants. Any regalia needs review; the archetype sits closest to a religious figure. Thunder Aspirant is PROPOSED; CD must decide existence before behaviour.

### SB-6 — CH02 Kingdom Beneath the Earth (subterranean)
- **Narrative purpose:** The underground kingdom.
- **Gameplay purpose:** Armoured-target encounter (Ore Thrall-class, if ratified).
- **Location & environment:** CH02-ENV-001; cold, lightless underground.
- **Architecture/props/population:** Caverns, forge-shells (no flame).
- **Cultural references & restrictions:** **No flame anywhere in Ch.2.** Metal reads cold and lightless. Ore Thrall depends on the unresolved Thrall question.

**Scene-brief rule:** every scene brief carries its cultural clearance status. No scene is promoted to production without its cultural hold cleared (CD-2 where applicable) and its CD-3 enemy decision (where an enemy is involved). Population is reconciled against the 29-scene register (TR-4); no double-counts (TR-2).
