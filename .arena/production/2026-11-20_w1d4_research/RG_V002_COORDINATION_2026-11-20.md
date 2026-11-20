# RG-V002 — RIG / ANIMATION / AI COORDINATION PACKAGE (2026-11-20, W1 D4)
**Authority:** E-01 (owner 2026-11-20): first playable enemy = **unnamed guard-class**, **unarmed lane**, no variants, no invented weapons/names/cultural details. Parent ruling context: Adanna workbook §11 · ROYAL_GUARD_V002_PRODUCTION_PATH_2026-11-20.md (16-clip proposal, §9) · findings doc `../2026-11-20_w1d3_rg_v002/RG_V002_REVIEW_FINDINGS_2026-11-20.md` (recommendation: REVISE/V003 class-generic face).

## 1. RIG COORDINATION (Research→TD)
- **Skeleton family:** propose shared HUMAN_BASE with Adanna (spine 3, neck+head, clavicles, 2-seg arms, full hands, 2-seg legs, feet) — TD ratifies. If TD keeps separate skeletons, anim set must be authored twice; flag now so PM can budget.
- **Proportion delta (vs Adanna):** shoulder mass ≈1.2× (not 1.3×), same leg length class, heavier torso slab. Pelvis width same. Head same topology (face NOT FACS-gated for the guard unless PM wants challenge barks animated — default: NO facial set, saves ≈18 shapes).
- **Sockets:** `Socket_Hand_R` / `Socket_Hand_L` only (no weapon sockets in unarmed lane; `Socket_Weapon*` must NOT exist on the slice-1 guard rig). `Socket_GuardTab` NOT created (no heraldry ratified).
- **QC:** bind pose = neutral A-pose; mirror until asymmetry (none authored — class has no left/right asymmetry by design); ≤4 influences/vertex.
- **Scale:** same cm pipeline (FP-07); capsule TBD by PM/TD (proposal r 0.36 m / h 1.85 m — assumption, not canon).

## 2. ANIMATION MINIMUM SET — PROPOSAL FOR PM (PM DEFINES, WE PROVIDE OPTIONS)
**Slice-1 minimum (unarmed, guard-class):** idle (2, alert-weight + relaxed) · walk_patrol · turn_in_place L/R · stop · investigate_step ×2 · alert_look (head/torso raise) · challenge_gesture (open-palm presentation — unarmed) · shove/restraint_push (only if PM confirms guard mechanic exists — otherwise omit) · hit_react ×2 · knockdown · get_up · death ×1 (non-violent-looking placeholder acceptable for slice).
**Explicitly NOT in slice 1:** weapon draw/attack/block/parry/dodge-combat variants · shield work · formation moves · class variants · named guard uniques.
**Count:** 11–13 clips (vs 16 in the 2026-11 path §9 once weapon clips are struck per E-01). Non-combat subset may be authored PROVISIONAL; challenge/restraint gate on PM ruling.

## 3. AI COORDINATION (with PM's behaviour design — we do NOT invent behaviour)
- Lane: **Patrol → Suspicion → Challenge → Engage (unarmed restraint) → Alarm/Report**. Design provides silhouette + readability requirements only; state graph, radii, timers, and fail logic belong to PM/TD gameplay.
- Readability requirements (Design → PM): guard must read "authority/watchful, not hostile-by-default" at 20–30 m (indigo-under-harness at distance, upright gait); challenge must be visually legible (arm raise, halt) before any restraint action — no unreadable leaps to violence.
- **No AI facts may be encoded in art assets** (no glow states, no rage textures, no alert decals).

## 4. BLOCKED / NOT BLOCKED
- V003 re-render (this pipeline) — blocked on CD accepting REVISE recommendation.
- Rig spec sign-off — blocked on TD (skeleton family) — can proceed as proposal now.
- Animation authoring — blocked on PM's minimum-set ruling (§2). Provisional non-combat authoring may start with PROVISIONAL labels.
- Disc/coral "palace service mark" — blocked on Research exact-version or removal (see findings §F). No stop-work for unrelated items.
- Adanna build — NOT blocked by RG track. Greybox — NOT blocked. FP-10 tally ratification — NOT blocked.

## 5. QUESTIONS FOR PM (W1 D5 check-in)
1. Is the slice-1 guard mechanic "challenge → restrain" or purely "block the gate" (non-interactive)? Determines clips #8 and #13.
2. Face presentation: class-generic (recommended) vs named-cast allowance for slice 2?
3. Audio bark involvement in slice 1 (affects whether facial/lip subset is needed)?
4. Patrol route anchors (already in greybox manifest plan) — PM confirms count/positions acceptable?
