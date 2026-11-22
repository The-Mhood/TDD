# Character Identity Records — Integration Foundation

**Document ID:** TDD-IMPL-CHARID-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM (with Story, Design, Character Art). **Status:** ESTABLISHED for the main cast; supporting cast in progress.
**Purpose:** One consistent identity record per character, connecting name/aliases, role, relationships, chapter appearances, visual references, model/animation status, gameplay function, and dialogue/story dependencies. This is the foundation that keeps the whole game consistent — one storyline, one cast, one visual world.
**Source:** Google Drive `CHARACTER_DESIGN_REGISTER.md` (authoritative), `OPEN_ART_DECISIONS.md`, and the project narrative facts.

---

## Record template (applied to each character)
1. **Name & aliases** · 2. **Role & narrative purpose** · 3. **Family & relationships** · 4. **Chapter appearances** · 5. **Existing image folder & visual references** · 6. **Model & animation status** · 7. **Gameplay function** · 8. **Dialogue & story dependencies**

---

## Main cast

### 1. Adanna
1. **Name & aliases:** Adanna (protagonist). No aliases.
2. **Role & narrative purpose:** 25-year-old warrior, daughter of Ezeani; the player character. Guarded/defiant default; her arc drives the story and the three endings (OAD-27).
3. **Family & relationships:** Daughter of **Ezeani** (father) and **Nneka** (mother, deceased). Was **six** when Nneka died (OAD-35); 19 years separate Nneka's death from the game's start.
4. **Chapter appearances:** All chapters (player character). Ch.1–Ch.8.
5. **Existing image folder & visual references:** `Reference_Control/adanna_master_portrait.png` (master APPROVED — the identity anchor, OAD-02). Turnaround V004/V005, expressions V002/V003, exploration outfit V002/V003, upgraded armour V002 (single LEFT shoulder guard). Right side plain; never mirrored (OAD-51).
6. **Model & animation status:** **Adanna AD-03 V3** modelled in Blender 4.2.23 (13,680 tris, 10 material slots, `HUMAN_BASE_PROPOSED` skeleton) — integration-verified headless (W1D7). **Facial likeness PoC v2 pipeline authored** (repaired); **not yet owner-built/reviewed** (DP-02). Animation: movement clips V1 (validation done).
7. **Gameplay function:** Player character — movement/combat, encounters, camera. Blade (short leaf-bladed iron sword) on LEFT hip (OAD-09).
8. **Dialogue & story dependencies:** Central to all dialogue; three endings; the hidden Ending 3 earned through seven Nneka memories (OAD-32).

### 2. Ezeani
1. **Name & aliases:** Ezeani.
2. **Role & narrative purpose:** Father, former warrior-king, **final boss**. Killed Nneka; morally complicated, not absolved (OAD-34).
3. **Family & relationships:** Father of **Adanna**; husband/partner of **Nneka** (killed her). Early sixties now; ~43 when he killed Nneka.
4. **Chapter appearances:** Ch.1 (memory/backstory), Ch.8 (confrontation/endings); final boss encounter.
5. **Existing image folder & visual references:** 2 boards REVIEW REQUIRED. Turnaround V002 (staff in right hand, wrapper on left shoulder, ivory bracelet on right wrist). Identity locks: short grey-white beard, heavy brow, massive ageing frame, old blade scars. Costume: indigo + oxblood wrapper, coral strands, red cap with eagle feather, ivory bracelet, carved staff, no crown.
6. **Model & animation status:** Not yet modelled in the Blender pipeline (design boards only).
7. **Gameplay function:** Final boss; boss phases outstanding (Q-14 PENDING_CONTENT).
8. **Dialogue & story dependencies:** Central to the Nneka truth; three endings (killed / spared / hidden). **Cultural review of regalia required (OAD-03, CD-2)** — red cap, eagle feather, coral, ivory are real markers of title.

### 3. Nneka
1. **Name & aliases:** Nneka ("mother is supreme").
2. **Role & narrative purpose:** Adanna's mother, killed by Ezeani. Appears in ancestral memories and manifestations; her voice calls Adanna at 25 (OAD-39); her story drives Ending 3.
3. **Family & relationships:** Mother of **Adanna**; partner of **Ezeani** (who killed her at her request, concealing the truth). ~45 at death; ~39 when Adanna born.
4. **Chapter appearances:** Memory scenes across Ch.1–Ch.7 (seven hidden memories, OAD-32); Ch.8 (voice/manifestation).
5. **Existing image folder & visual references:** `Reference_Control/nneka_master_portrait.png`. Turnaround V002. Living-memory version (striped everyday cloth, solid, no mist). Identity locks: ~45, softer rounder face with Adanna's cheekbones/eyes, upswept braided crest with ivory-white beads, white/pale-blue bead strand, plain white wrapper over left shoulder, curved chalk lines at left temple/collarbones. Manifestation: soft edges, cool moonlit skin, drifting chalk dust; never glows.
6. **Model & animation status:** Not yet modelled (design boards only). One adult model (~39–45) serves all memory scenes.
7. **Gameplay function:** Narrative/memory driver; not a player-controlled character.
8. **Dialogue & story dependencies:** Central to the boundary truth (OAD-34) and Ending 3; the seven memories.

### 4. Okwu
1. **Name & aliases:** Okwu ("word/speech").
2. **Role & narrative purpose:** Spirit companion and guide. Entirely fictional; kept distinct from real masquerade forms (OAD-04).
3. **Family & relationships:** Companion to Adanna; no known family.
4. **Chapter appearances:** All chapters (alongside Adanna).
5. **Existing image folder & visual references:** `Reference_Control/okwu_master_portrait.png`. Identity locks: ~2.4 m, thin, stooped; charcoal hood with face withheld (darkness only, always — OAD-12); layered charcoal + indigo cloth; floor-length raffia mantle; forked staff with iron bells and a gourd; chalk-pale hands; no visible feet.
6. **Model & animation status:** Not yet modelled (design boards only). **Cultural sensitivity:** raffia/masquerade imagery — confirm comfort (OAD-04).
7. **Gameplay function:** Guide/companion; narrative guidance.
8. **Dialogue & story dependencies:** Companion dialogue; guides Adanna. **Cultural review (CD-2)** for masquerade-adjacent imagery.

### 5. Amadioha
1. **Name & aliases:** Amadioha (documented thunder/judgment deity).
2. **Role & narrative purpose:** Ancient divine force of thunder, judgment and destruction. Ch.5 figure; human form chosen and consultant-approved (OAD-05).
3. **Family & relationships:** A deity; no family. Symbol: white ram (ordinary livestock, no special rule — OAD-19).
4. **Chapter appearances:** Ch.5 (Mountain of Thunder).
5. **Existing image folder & visual references:** Master sheet APPROVED (in 14_APPROVED_DESIGNS); turnaround V001; details sheet. Identity locks: ~5 m; slate-dark skin with pale lightning-figure scars; cloud-white hair/beard; blank white eyes; white wrapper with red band; fulgurite staff. No armour, crown or weapon. Lightning **white, always**.
6. **Model & animation status:** Not yet modelled (design boards only).
7. **Gameplay function:** Ch.5 presence/lore; not a combat target (deity figure).
8. **Dialogue & story dependencies:** Ch.5 lore. **Documented deity — fictionalised treatment; cultural review sensitive (CD-2).**

### 6. Idemili
1. **Name & aliases:** Idemili (documented river deity).
2. **Role & narrative purpose:** Ancient water deity of the river domain. Ch.4 figure. Python is her sacred animal (never an enemy/loot — OAD-14).
3. **Family & relationships:** A deity; no family.
4. **Chapter appearances:** Ch.4 (river domain).
5. **Existing image folder & visual references:** 2 boards REVIEW REQUIRED; details sheet. Identity locks: ~2.2 m+, ageless; always wet; chalked brow/eyelids; heavy coiled hair with cowries trailing into river weed; white + indigo cloth turning to water at the hem; living python across shoulders. No tail, crown or armour.
6. **Model & animation status:** Not yet modelled (design boards only).
7. **Gameplay function:** Ch.4 presence/lore; river domain.
8. **Dialogue & story dependencies:** Ch.4 lore. **Documented deity — fictionalised; cultural review sensitive (CD-2).**

### 7. The Hollow King
1. **Name & aliases:** The Hollow King (fictional title).
2. **Role & narrative purpose:** Primary antagonist. Ch.7. A "broken vessel"; began his work on the boundary ~1 year before the game opens (OAD-41).
3. **Family & relationships:** Antagonist; employer/commander of **Onwuka** (lieutenant). No family.
4. **Chapter appearances:** Ch.7 (primary); his boundary-work leaks Nneka's memories (OAD-39/41).
5. **Existing image folder & visual references:** 2 boards REVIEW REQUIRED; details V002/V003 (West African features, empty sockets). Identity locks: ~2.6 m with headdress; cracked fired-clay skin; open dark cavity through the torso shedding ash; burial-cloth headdress with corroded bronze rings; ash + faded indigo funerary cloth; bone beads; eyes closed.
6. **Model & animation status:** Not yet modelled (design boards only).
7. **Gameplay function:** Primary antagonist; boss encounter (Q-14 PENDING_CONTENT).
8. **Dialogue & story dependencies:** Central antagonist; boundary/memory leaks. **Ensure "king of the dead" framing does not read as a claim about real Igbo funerary/ancestral practice (CD-2).**

---

## Supporting cast (compact records)

| # | Character | Role | Chapters | Visual ref | Model status | Gameplay | Story dependency |
|---|---|---|---|---|---|---|---|
| 8 | **Mgbafo** | Village elder, 78; knows the truth about Nneka | Ch.1 (home settlement) | Supporting board | Not modelled | Info/lore | Knows Nneka truth |
| 9 | **Obika** | Warrior companion, 32; spear, cane-and-hide shield | Ch.1+ | Supporting board | Not modelled | Companion/combat ally | Ally |
| 10 | **Ojiugo** | Healer, 52; gourds/herbs belt | Ch.1+ | Supporting board | Not modelled | Healer/lore | Healing/herbs |
| 11 | **Akuebue** | Merchant, 46; sells to both sides | Ch.1+ | Supporting board | Not modelled | Trader | Faction-bridging |
| 12 | **Omenka** | Blacksmith, 41; blind left eye; made Adanna's blade | Ch.1+ | Supporting board | Not modelled | Smith/lore | Made Adanna's blade |
| 13 | **Ogbuagu** | Hunter, 57; claw scars, hide cape, short bow | Ch.1+ | Supporting board | Not modelled | Hunter/ally | Ally |
| 14 | **Okorie** | Royal guard, 28; oxblood wrapper, iron disc harness | Ch.1+ (palace) | `sup_royal_guard_v002.jpg` | Not modelled | Guard | Palace faction |
| 15 | **Mgborie** | Palace servant, ~24; shaved head, oxblood waist strip | Ch.1+ | `sup_palace_servant.jpg` | **BLOCKED** (not generated) | Servant/lore | Palace faction |
| 16 | **Uchendu** | Spiritual specialist, 66; chalk ring, iron staff | Ch.1+ | Supporting board | Not modelled | Spiritual/lore | Spiritual matters |
| 17 | **Mgbokwo** | Rogue, 27; half-shaved twists, two knives | Ch.1+ | Supporting board | Not modelled | Rogue/ally | Ally |
| 18 | **Nwanyibuife** | Rebel leader, 44; shaved head, burn scar, pry-out disc harness | Ch.1+ (rebels) | Supporting board | Not modelled | Rebel leader | Rebel faction |
| 19 | **Onwuka** | Hollow King's lieutenant, ~50; turning to cracked clay, hooked polearm | Ch.7 | `sup_lieutenant_v002.jpg` | Not modelled | Lieutenant/combat | Hollow King's commander |
| 20 | **Unoka** | Travelling storyteller, 61; cloak, pole, thumb piano, flute | Ch.1+ | Supporting board | Not modelled | Storyteller/lore | Lore/narrative |

**Faction badge (fictional):** palace guards wear a hammered iron disc on the chest harness; rebels wear the same harness with the disc removed.

---

## Integration status
- **Named-character count:** 20 (7 main + 13 supporting) — matches the PM naming target (no inflation).
- **Model/animation:** Only **Adanna** has a modelled asset (AD-03 V3, integration-verified); **Adanna's facial PoC v2** is the active production item (DP-02, repaired, awaiting owner build). All other characters are at design-board stage.
- **Cultural gates:** Amadioha, Idemili (deities), Okwu (masquerade-adjacent), Ezeani (regalia), Hollow King (funerary framing) carry CD-2 sensitivity — see each record.
- **Enemy characters** (Ore Sentinel, White-Arc Duelist, etc.) are tracked in `ENEMY_DECISION_PACKAGE.md`, not in this character-identity record (they are enemies, not named characters, until ratified).

**This record is the single consistency anchor per character.** New characters are added here first; all departments reference it so name, story, visual, model and gameplay stay connected.
