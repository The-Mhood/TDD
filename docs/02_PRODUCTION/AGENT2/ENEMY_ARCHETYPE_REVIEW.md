# ENEMY ARCHETYPE REVIEW — FOR CD-3 DECISION

**Document ID:** TDD-CREAT-001
**Version:** 1.0.0
**Date:** 2026-11-16
**Author:** Agent 2 (world structure / level architecture)
**Status:** **PROPOSED — CD-3 NOT RATIFIED.** Every archetype in this document is PROPOSED. None is canon. None is approved. None has been built.

---

## 1. What this document is, and what it is not

TD decision **CD-3 was not ratified.** The direction was explicit: submit a proper review document covering role, chapter, behaviour, capabilities, narrative relationship and cultural-visual dependencies — and **invent no mythology**.

So this document does that and stops there. It is a decision-support document for the Creative Director, not a design bible.

**What this is not:** a canon proposal. Nothing here asserts what the world *is*. The register is silent on enemy creatures — there is no canon source for any of these — and silence is not permission.

| Field | Meaning in this document |
|---|---|
| **Role** | Combat function. A mechanical description only. |
| **Chapter fit** | Where the encounter would sit. Chapter canon still constrains it. |
| **Behaviour** | What it does. Expressed as AI capability, not lore. |
| **Capabilities** | What systems it needs. Drives engineering cost. |
| **Narrative relationship** | **What the story would have to say about it, if approved.** This is a question for the CD, not an answer. |
| **Cultural-visual dependencies** | Whether it invents visual or cultural material, and therefore needs review. |

The `Narrative relationship` column is deliberately written as an open question. Choosing a creature is choosing a claim about the world; that claim belongs to the Creative Director and the consultant, not to me.

---

## 2. Standing constraints that apply to every archetype

These are canon, not proposals. Any archetype violating one is dead on arrival.

| Constraint | Source | Effect on archetypes |
|---|---|---|
| No python or snake enemies, ever | `RULE-CH04-PYTHONS` | Chapter 4 has no serpentine enemy. The pythons are never enemies and never loot. |
| Children are never combat targets | `RULE-NPC-CHILDREN-NO-COMBAT` | No child-model enemy, no child-adjacent threat framing |
| Chapter 2 has no flame | Chapter 2 rules | Fire-based enemy visuals impossible in Ch02 |
| Chapter 3 shows no remains | Chapter 3 rules | No bone, corpse or skeletal reads. Ash, not snow. |
| Chapter 5 lightning is white only | Chapter 5 rules | No coloured lightning variants |
| Chapter 7 is earth/timber/cloth, ember not flame, starless | Chapter 7 rules | Constrains armour, materials, light |
| Chapter 6 masks are invented and featureless | Chapter 6 rules + `RULE-CH06-MASKS` | Any mask needs consultant review |
| Adanna is never mirrored; right side plain | Character canon | Applies to her, but also: do not mirror enemy silhouettes from her design |

Additionally, **shrine, mask and ritual content is blocked by CD-2** (consultant gate). An archetype that leans on any of those cannot proceed past blockout regardless of CD-3.

---

## 3. The six proposed archetypes

All rows: **status PROPOSED**, `canon_source: NONE EXISTS`, `built: NO`.

### 3.1 Rootwarden

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 1 (The Forbidden Forest) |
| **Role** | Slow heavy bruiser. Teaches spacing and punish windows. |
| **Behaviour** | Patrols a fixed route; slow turn rate; telegraphs a wide sweep; does not pursue beyond a leash radius. No ranged attack. |
| **Capabilities** | StateTree base, ground nav, single attack, damage receive, stagger. Lowest-cost archetype. |
| **Narrative relationship** | **OPEN QUESTION for CD.** If the forest is ESTABLISHED but no creature is, does a guardian creature imply a belief about the forest that the story has not established? Does it need to be a creature at all, or could the forest's threat be environmental? |
| **Cultural-visual dependencies** | **Invented creature.** Must not read as a known figure from Igbo tradition. Bark/root material avoids metal entirely. Needs visual review for accidental resemblance to masquerade or shrine-guardian imagery. |
| **Canon risk** | Medium. Introduces a creature into an ESTABLISHED environment. |

### 3.2 Thrall

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 3 (City of the Living Dead), 7 (Gates of the Dead) |
| **Role** | Weak swarm. Teaches group management and crowd control. |
| **Behaviour** | Spawns in small groups; slow individual pursuit; no flanking; loses interest at a boundary. Individually trivial, collectively pressure. |
| **Capabilities** | Cheap; benefits most from the CROWD tier rather than full per-actor AI. Good candidate for Mass. |
| **Narrative relationship** | **OPEN QUESTION for CD, and the most sensitive one here.** Chapters 3 and 7 are the lands of the dead. A humanoid "thrall" makes a claim about the dead that could read as a statement about ancestors. That is a cultural and narrative decision of the highest order and I will not take it by naming an archetype. |
| **Cultural-visual dependencies** | **High.** Humanoid + death + Igbo-inspired setting is precisely the combination that can invent mythology about the dead. Requires consultant review (CD-2) *before* CD-3, not after. |
| **Canon risk** | **High.** Recommend the CD consider a non-humanoid or environmental expression of the same combat pressure. |

### 3.3 Ash Hound

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 3 |
| **Role** | Fast flanker. Forces the player to reposition. |
| **Behaviour** | Circles at range, commits in bursts, retreats after a hit. Highest mobility archetype. |
| **Capabilities** | Faster nav, flanking logic, burst movement. More expensive than Thrall. |
| **Narrative relationship** | **OPEN QUESTION.** A dog-like creature invites a reading about hunting, domesticity or rites involving animals. Must not imply a real animal rite. |
| **Cultural-visual dependencies** | Ash-dulled surface must obey "no remains" — ash is not bone, and must not be modelled to read as bone. |
| **Canon risk** | Medium. |

### 3.4 Ore Thrall

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 2 (Kingdom Beneath the Earth) |
| **Role** | Slow, cold, armoured. Teaches armour-breaking or positioning around a hard target. |
| **Behaviour** | Very slow; high poise; cannot be staggered by light attacks; turns poorly. |
| **Capabilities** | Same base as Thrall with higher poise values. Cheap to add **if** Thrall exists. |
| **Narrative relationship** | **OPEN QUESTION.** Does a "thrall" concept in Chapter 2 make a claim about labour, binding or servitude in the underground kingdom? That is a story question. |
| **Cultural-visual dependencies** | **No flame anywhere in Chapter 2.** Cannot carry ember, torch or forge visuals. Metal reads must be cold and lightless. |
| **Canon risk** | Low-medium, but blocked by its dependency on Thrall's unresolved narrative question. |

### 3.5 Thunder Aspirant

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 5 (Mountain of Thunder) |
| **Role** | Elite. Human-scale, disciplined, duel-like. |
| **Behaviour** | Single opponent; holds distance; counter-attacks; does not chain-stun. Deliberately the most "fair" archetype. |
| **Capabilities** | Highest per-actor cost; needs defensive logic and timing windows. |
| **Narrative relationship** | **OPEN QUESTION, and a canon constraint.** "Aspirant" implies a relationship to Amadioha's champion — a claim about the chapter's central religious figure. Electrical effects must be **white only**. |
| **Cultural-visual dependencies** | Lightning is white, always. No coloured variants. Any regalia needs review: this archetype sits closest to a religious figure and is the easiest place to invent doctrine by accident. |
| **Canon risk** | **High.** Recommend the CD decide whether this archetype can exist at all before its behaviour is specified. |

### 3.6 Maskbearer

| | |
|---|---|
| **Status** | PROPOSED — not ratified |
| **Chapter fit** | 6 (Kingdom of Masks) — this chapter only |
| **Role** | Area-denial. Presence changes where the player can stand. |
| **Behaviour** | Largely stationary; projects a zone; turns slowly toward the player. Low chase, high control. |
| **Capabilities** | Zone/aura system; cheapest AI, most expensive VFX and visual review. |
| **Narrative relationship** | **OPEN QUESTION, and blocked by CD-2.** Chapter 6 is the masks chapter. Any mask content is under consultant gate. Whether a *wearer* exists is a story claim. |
| **Cultural-visual dependencies** | **Highest in this list.** Featureless invented masks are canon for Chapter 6. This archetype requires consultant review (CD-2) and must not resolve until that gate does. |
| **Canon risk** | **High, and currently blocked.** |

---

## 4. Risk summary

Ordered by how much they could damage the project if approved carelessly.

| Rank | Archetype | Risk | Why | Recommendation |
|---|---|---|---|---|
| 1 | Maskbearer | High, blocked | CD-2 consultant gate is open | Do not proceed. Cannot resolve before CD-2. |
| 2 | Thrall | High | Humanoid dead — can invent mythology about ancestors | CD should consider non-humanoid alternative |
| 3 | Thunder Aspirant | High | Closest to a religious figure | Decide existence before behaviour |
| 4 | Rootwarden | Medium | Creature in an ESTABLISHED environment | Safest of the six; still needs visual review |
| 5 | Ash Hound | Medium | Animal-rite implication | Manageable with material discipline |
| 6 | Ore Thrall | Low-medium | Dependent on Thrall's question | Resolve via Thrall |

**A note on this ranking.** It is ordered by cultural and narrative risk, not by engineering cost. The cheapest archetype to build (Maskbearer) is the most dangerous to approve, and the most expensive (Thunder Aspirant) is not the riskiest. Engineering convenience must not drive this decision — which is exactly why I am not making it.

---

## 5. Engineering reality

| Claim | Status |
|---|---|
| Archetypes designed | **NO** — described only |
| Archetypes built | **NO** |
| Any AI behaviour implemented | **NO** |
| StateTree assets created | **NO** |
| Any archetype tested | **NO** |

There is no Unreal project. Nothing in this document can be compiled or run. The six entries are descriptions of intended capability sets for the CD's decision, and they are the *minimum* needed to decide whether an enemy interface can accommodate the eventual answer.

**Dependency, stated plainly:** enemies cannot be built before the combat foundation and enemy interface exist. Per the directive, bosses come after enemy interfaces. Any archetype approval now is approval to *design against*, not to build.

What engineering can offer the CD regardless of which archetypes survive: an AI base that supports patrol, leash, telegraph, stagger and zone behaviours covers all six. The interface does not need to be decided before the creatures are.

---

## 6. Questions for the Creative Director

1. Does Chapter 1 need a creature at all, or can the forest's threat be environmental?
2. May a humanoid enemy exist in the lands of the dead? If not, what expresses the same combat pressure?
3. Can any archetype sit as close to Amadioha as "Thunder Aspirant" implies?
4. Should Maskbearer be withdrawn until CD-2 closes?
5. Is a six-archetype roster the right size for a 135-scene game, or should it be smaller and deeper?
6. Does "thrall" carry an unwanted implication about servitude or binding?

---

## 7. What I will not do

- I will not name any archetype canon.
- I will not invent a mythological origin for any of them.
- I will not present invented creatures as Igbo tradition.
- I will not build any of them before the combat foundation and enemy interface exist.
- I will not treat silence in the register as approval.

---

## 8. Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-11-16 | First issue. Six archetypes documented against CD-3's requested fields; all remain PROPOSED; risk ranked by cultural exposure rather than build cost; Maskbearer marked blocked by CD-2. |
