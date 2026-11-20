# ROYAL GUARD (CHAR_SUPPORTING_ROYAL_GUARD_V002) — FIRST-ENEMY PRODUCTION PATH (W1 D1)
**2026-11-20 · Original VA · status: PRE-PRODUCTION ONLY — final production is CONDITIONAL on design approval (CD/owner) of the sheet and on the gates below. No selection executed; no approval claimed; no variants; no models.**
Existing prep: `ENEMY_SELECTION_BRIEF_ROYAL_GUARD_V002_2026-11-17.md` (selection brief) · `ROYAL_GUARD_V002_REVIEW_SCOPE_AND_CRITERIA_2026-11-17.md` (review criteria A–G) — this file extends them into the production path; **read those first**. Selection itself remains CD's act. This document assumes a "SELECT (direction)" outcome for planning purposes only; if CD instead defers/rejects, its §§3–7 lapse harmlessly.

---

## 1. WHAT HE IS / IS NOT (design guardrails)
- **Is:** the slice's recommended representative-enemy design direction — palace/gates-class guard (CH01-SCN-019 gate approach; palace courtyard lineage); indigo torso cloth under harness per **OAD-18** (the only locked constraint); COMPLIANT sync/integrity class (audit 2026-11-16); md5 `267262040a35737f20c267a02ca4dfd0`, 525,656 B, Drive `1NCNGakEKbiRtg0B14jlcH7S48gieN898` (`01_CHARACTERS/Supporting_Characters`).
- **Is not:** approved; a named canon character ("Okorie" is an unverified working name — identity lock does not exist); boss-grade; license to reuse Adanna/Amadioha likeness; licence to invent palace regalia/militaria (OAD-03 open; Research clearance required before any variant propagation); a weapon authority (see §5).
- **V001 is superseded** (retained as history; bare-chested, pre-OAD-18) — never use as reference.

## 2. KNOWN DEFECTS TO ADJUDICATE (from brief/scope; Our Eyes pass owns the ruling)
1. Arms read heavy vs Adanna-humanoid mass — quantify vs torso/leg in the review pass.
2. Cloth reads sewn in rear view — construction logic of indigo wrap + harness overlap.
3. No identity lock (face, marks, build, name) — CD must order an identity-lock doc **or** ratify him as unnamed class (recommended for slice: class, not person).
4. Sheet is painterly single-image 2560×? (not measured this session — record on review) — insufficient for model build without ortho pass **after** direction sign-off.
5. Uniform compliance vs OAD-18 panel-by-panel unverified by Our Eyes.

## 3. PRODUCTION SEQUENCE (conditional)
**Step 0 (now, no approvals):** this doc; criteria pack for review pass (done); dependency map (here); no art, no variants.
**Step 1 — CD design-direction selection** (E-01 ruling in queue). Output: SELECT/REVISE/REJECT/DEFER recorded.
**Step 2 — Our Eyes + Research review pass** (criteria A–G, one sitting): verdict KEEP (direction) · REVISE (defects list → Assistant VA V003) · REJECT · DEFER. Research must also clear palace-militaria specifics before any propagation. KEEP ≠ approval — it is direction sign-off only.
**Step 3 — Approval of the sheet itself** (CD signs the accepted version; register row updated by authorised agent). Until this lands, nothing below Step 4 may start.
**Step 4 — Ortho/model-sheet development** (Assistant VA; commissioned work, tied to this production requirement): turnarounds (front/3-4/back/side), head-turn, 2 expressions (neutral/threat), scale block vs 1.80 m Adanna (≈1.88 m proposal ⟦DECIDE⟧), hand-scale; SAME bar as Adanna set (no painterly-to-mesh direct path).
**Step 5 — Production package build** = §4; conditional on Step 3 + TD-SPEC-001 ratification (FP-07) + AD-03-equivalent sign-off for enemy (lighter lane: no cutscene face rig, no pendant/cloth subtleties).
**Step 6 — Integration & evidence** per §6; identical harness to Adanna (FP-07 #7).

## 4. PRODUCTION REQUIREMENTS (proposals; TD ratifies; lighter than Adanna)
- **Model LODs:** LOD0 ≤ 30k tris (no fine facial set unless CD demands cutscene use) · LOD1 ≤ 15k · LOD2 ≤ 7k · LOD3 ≤ 3k. Texel density one band below Adanna (2K body).
- **Topology:** same discipline as Adanna workbook §3; simpler hands (mitten-adjacent grip loops for haft weapons); indigo torso cloth + harness as layered materials (cloth over skin, harness leather); no scars/jewellery inventions; bare arms per OAD-18.
- **Proportions:** ≈1.86–1.90 m proposal; shoulder/mass heavier — target 1.25–1.35 × Adanna shoulder mass; hips narrower; calves heavier (guard stance). All ratified in TD-SPEC-001 §9.
- **Rig:** humanoid standard (reuse Adanna skeleton with scale + mass adjustments if engine skeleton allows; else cloned skeleton `SKEL_GUARD_RHV002`); no facial rig by default; 2 expression shapes optional for death/pain read (jaw open/squint) — CD call.
- **Animation set (≈16 clips proposal):** idle_guard ×2 (scan/relaxed) · walk · jog · alert_raise (weapon to ready) · attack_melee ×2 (spear/staff, see §5) · attack_throw? (only if weapon assigned) · block/parry (if combat design includes) · pain ×2 · death ×2 · shove/guard_break (if PM wants non-lethal) — **sized by PM/design input**; locomotion blend quality matters more than attack count; loop-safe for patrol state machine (AI: patrol→alert→engage→return; needs PM/AI alignment).
- **Collision:** capsule controller (r 0.36/h 1.78 proposal); hit boxes head/torso/pelvis/arms/legs; damage scalars per TD table; guard is combatant — hit boxes mandatory.
- **Materials:** poorer-leather harness, indigo torso cloth (faded, sun-worn — palette within FP-01), skin same family as Adanna pipeline (reuse SSS profile), no bronze jewellery (reserved cultural motifs: none without Research).
- **Integration evidence:** turntable, in-engine shots at LOD0–3, collision debug, anim montage incl. patrol loop, budget sheet actual-vs-ratified, md5 manifest, deviations log.

## 5. WEAPON — UNRESOLVED (do not paper over)
No weapon is assigned to Royal Guard V002 anywhere; defaulting to Adanna's blade is forbidden by CQ-9 adjacency and by OAD-03 (regalia open). Candidate lanes (owner ruling required): (a) **none** — empty-hand/grappling class (simplest, honest); (b) simple staff/haft — Research-cleared generic object; (c) ekwe/staff percussion weapon — thematically wrong for combat; (d) spear — Research-cleared generic militaria. Until ruling, model ships with **no weapon mesh; sockets `Socket_Weapon_R` placeholder only**, anims cover unarmed + alert states; combat numbers stay PM-open. Any Igbo-specific regalia item = consultant/Research gate.

## 6. COORDINATION WITH COMBAT & AI IMPLEMENTATION (for PM/design; requests, not decisions)
- **Combat design:** guard role in CH01 encounter (patrol/intercept/gate-hold); damage model vs Adanna; telegraphs (audio-visual tells); non-lethal resolution allowed?; respawn/reset rules.
- **AI:** state machine scope (patrol waypoints — gate approach ↔ courtyard; alert radii; engage/acquire; leash return); nav-mesh cost (court clearing vs market stalls); animation-driven movement sync (in-place required); group behaviour (2 guards? max NPCs) — V001 sheet shows single figure; group staging = separate direction decision.
- **Performance:** NPC skinning budget; concurrent guards cap (proposal ≤3 in cell); LOD distances for gate-view silhouette.
- **Save/checkpoint:** gate threshold trigger — PM.
- **Evidence hand-off:** integration report expected from whoever wires gameplay; design dept defines "verified in-game" pass criteria for the enemy specifically.

## 7. WHAT I NEED (owner/CD), IN ORDER
1. **E-01 selection ruling** (SELECT/REVISE/REJECT/DEFER as per brief) — without it nothing moves.
2. **Identity ruling:** unnamed class vs identity-lock document (latter = separate task; I recommend class for slice).
3. **Weapon lane ruling (§5 a–d)** + any Research instruction.
4. **Review-pass authorisation** (Our Eyes + Research; I draft the order; no execution without it).
5. **Combat/AI slot intent from PM** (§6) — arrival format negotiable (brief or meeting notes).
6. TD-SPEC-001 ratification covering §9 enemy substitutions (FP-07).

## 8. CRITICAL PATH EFFECT
Enemy = first asset through FP-07 pipeline; if RG-V002 slips, the pipeline shake-out shifts to Adanna-only scope; slip risk lives in **Step 1–3 approvals**, not in modelling capacity. The package is deliberately small; it exists to prove the lane, not to populate the roster. **Variants/roster: explicitly out of scope** (Research clearance required before any second guard figure is generated — also paused under the no-speculative-generation rule).

## 9. RIG/ANIM READINESS & AI COORDINATION DETAIL (2026-11-20 W1 D2)
Advances §4/§6 into build-ready checklists. Still conditional on Steps 1–3; no gameplay commitment is made here.

### 9.1 Skeleton & retarget policy (proposal for TD)
- If project skeleton family = Adanna humanoid (recommended): reuse `SKEL_ADANNA` retargeted via Unreal IK-Retargeter / equivalent; scale 1.044× Adanna (1.88/1.80); mass deltas are material/skin only, not joint-count changes.
- Else clone as `SKEL_GUARD_RHV002` with identical joint names + one extra `spine_clavicle_pad` dummy for harness strap deformation if AD-03 equivalent requires it (default NO — harness rides layered materials, not bones).
- Root motion: OFF. All clips in-place; velocity from AI movement. Mount/socket attach points: `Socket_Weapon_R` only (§5); no helmet/head attach until regalia ruling.

### 9.2 Animation readiness matrix (what must exist before AI can integrate)
| Clip | AI state it feeds | Minimum bar |
|---|---|---|
| idle_guard_scan / relaxed | Patrol idle | loop-safe ≥4 s, no foot drift |
| walk / jog | Patrol locomotion | 8-dir blend; foot-lock ≤5 mm @30fps |
| alert_raise | Alert (sight/sound) | 0.6–0.9 s telegraph; readable at 15 m |
| attack_melee_a/b | Engage | 2 distinct verbs (haft thrust / sweep) once weapon lane assigned |
| block_parry | Engage (optional) | only if combat design includes; else omit, don't stub |
| pain_light / pain_heavy | Hit react | cancel windows defined by combat |
| death_front / death_back | Death | montage ≥1.2 s; no ragdoll dependency |
| shove_guard_break | Optional non-lethal | only if PM non-lethal ruling lands |

### 9.3 AI contract (request to PM/AI — format negotiable)
- States: `PATROL → ALERT → ENGAGE → RETURN` (+ `DEAD`); transitions by sight/sound stimuli with hysteresis (alert linger ≥3 s).
- Anchors: gate approach 2 waypoints, courtyard 2 waypoints, market edge 1 waypoint (proposed; PM owns).
- Concurrency cap: ≤3 concurrent guards per cell (proposal); LOD beyond 35 m swaps to impostor-less simple LODs (no billboards in slice).
- Perception: sight cone 60°/12 m (proposal), sound 6 m; no omniscience — stealth viability is a PM design call, noted here so the anim set supports sneak-vs-guard fairness (idle scan ≠ idle loop).
- Animation events: `OnAlertRaised`, `OnAttackHit`, `OnDeath` — names proposed; PM/AI owns final.
- Nav: dirt single surface; court/market blockers per CH01 greybox §9; stall collision = low blocker (guard vaults? NO — pathing around, per PM).

### 9.4 Evidence contract for "verified in-game" (enemy-specific; PM/design to ratify)
1. Patrol loop demo (walk waypoints, alert trigger by scripted stimulus) — capture ≥20 s video.
2. Engage demo with assigned weapon lane (or unarmed if lane (a)) — telegraphs visible at gameplay camera distance.
3. Death + despawn/reset behaviour per PM respawn ruling.
4. Perf capture: ≤3 guards, LOD transitions, frame cost on target hardware (FP-07 #7 names the platform — outstanding).
5. Deviations log vs this path; any deviation is owner/CD visibility, not silent acceptance.

### 9.5 Still deliberately unstarted (correctly)
No mesh, no ortho sheet, no weapon, no variants, no promotion, no canon claims. The moment CD selects direction, Step 2 (Our Eyes + Research) is the next executed work; Step 4 commission drafts are pre-staged in the evidence scaffold but not issued.
