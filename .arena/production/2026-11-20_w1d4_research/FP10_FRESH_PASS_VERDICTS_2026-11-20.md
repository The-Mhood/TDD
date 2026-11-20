# FP-10 — FRESH EXACT-VERSION PASS — VERDICTS (2026-11-20, executed)
Scope = `FP10_FRESH_PASS_SCOPE_TABLE_2026-11-20.md` (51 files). Method: live download of EVERY candidate from the PENDING tree (Drive), sha256/dimension forensics, visual inspection at native resolution by this review pass, verdict per file with evidence. **Verdict semantics:** PASS = acceptable as direction reference (EXPLORATORY boards; not canon, not production, not approval) · REVISE = fix the listed defects before CD ruling · REJECT = same design@version previously rejected; do not re-submit without a version bump and a new direction · DEFER = cannot rule honestly without missing research/subject authority. **No file is cleared for production. CD records binding verdicts; these are reviewer recommendations with evidence.**

## Reconciliation results (RECONCILE-FIRST rows — CLOSED)
- `SCN-017` PENDING `SCENE_CH01-SCN-017_VILLAGE_SQUARE_V002.jpg` 1536×1024 sha256 `d3ca6889…` ≠ rejected wave `B2_CAND_…_1672x941.jpg` 1672×941 sha256 `736a0c61…`. **Different files, different crops (close-up square vs wide establishing view, no shared chrome). Same design, same version V002.** The wave rejection covers this design@V002; re-rendering does not create a new design. → **REJECT (lineage)**. CD may commission V003 only as a new direction.
- `SCN-024` PENDING `SCENE_CH01-SCN-024_AN_EMPTY_HOUSE_V002.jpg` 1536×1024 sha256 `b34f2ed2…` ≠ rejected wave interior plate `…1672x941` sha256 `5e1ba6a8…`. Different files (exterior-with-mat vs interior-sunshaft — same subject, same version). → **REJECT (lineage)**, same basis.

## Per-file verdicts (29/29 processed)
| # | File | Dims | sha256[:12] | Verdict | Evidence / reason |
|---|---|---|---|---|---|
| 1 | ENV_CH01-EXP-003_THE_FORGOTTEN_PATH_V002 | 1536×1024 | 20fe29c3e220 | **PASS (ref)** | Forest path, ruined laterite rubble wall; no cultural claim needed; mood usable; not production geometry |
| 2 | ENV_CH01-EXP-004_THE_SMALL_CLEARING_V002 | 1672×941 | 8a9886bb5ddd | **PASS (ref)** | Dense forest clearing; coherent at a glance; ⚠️ 1672×941 = rejected-wave dimension class (check lineage before any later promotion); reference only, biome verification deferred |
| 3 | ENV_CH01-EXP-005_THE_STILL_POOL_V002 | 1536×1024 | 083c1d47ddda | **REVISE** | Pool + vegetation read SE-Asian/S-American tropical (broad buttress leaves); mismatch with recorded CH01 biome (savanna/forest edge, W-African palette); re-tag biome or regenerate flora |
| 4 | SCENE_CH01-SCN-006_A_LARGE_FAMILY_COMPOUND_V002 | 1536×1024 | cf0d3b2d3d88 | **PASS (ref)** | Compound wall + gate beam + hipped thatch + baskets/pots; coherent; fiction-appropriate; reference only |
| 5 | SCENE_CH01-SCN-007_A_SMALL_FAMILY_HOUSE_V002 | 1536×1024 | 237d1a866d87 | **PASS (ref)** | Mud-brick courses, thatch gable, firewood/pot, indigo curtain; coherent; reference only |
| 6 | SCENE_CH01-SCN-008_A_SMALL_FAMILY_HOUSE_V002 | 1536×1024 | a4002122eee1 | **PASS (ref)** | Interior: mat/platform/thatch underside; coherent; reference only |
| 7 | SCENE_CH01-SCN-011_MARKET_STALLS_V002 | 1536×1024 | 58773a003af9 | **PASS (ref)** | Strong goods density (yam/plantain/fish/indigo bolts); zero figures; excellent dressing reference; reference only |
| 8 | SCENE_CH01-SCN-012_MARKET_STALLS_V002 | 1536×1024 | 4ec8cb553410 | **REVISE** | **Sudano-Sahelian grammar:** tall banco tower with toron (protruding beams) + rounded buttresses — NOT Igbo vernacular (SUB-007 lesson). Goods plausible; rebuild backdrop to thatch/timber or re-skin; reject if uncorrected |
| 9 | SCENE_CH01-SCN-014_WATER_COLLECTION_POINT_V002 | 1536×1024 | f8d1cb989411 | **PASS (ref)** | Laterite-rimmed spring pool + pots/walls; Igbo-plausible fiction; reference only |
| 10 | SCENE_CH01-SCN-017_VILLAGE_SQUARE_V002 | 1536×1024 | d3ca68891d60 | **REJECT (lineage)** | See reconciliation above; same design@V002 as rejected wave item |
| 11 | SCENE_CH01-SCN-019_GATE_GUARD_SHELTER_V002 | 1536×1024 | b69d0cfbc8dc | **PASS (ref)** | Timber gate frame + laterite wall + thatch guard shelter; coherent; PROPOSED subject — subject ruling still owner's before build |
| 12 | SCENE_CH01-SCN-020_PALM_WINE_SHELTER_V002 | 1536×1024 | 02462e9e2a2c | **PASS (ref)** | Tapped palm with hanging bucket + rope + pot; subject-accurate fiction; note dry-stone rubble at right should become laterite masonry in build |
| 13 | SCENE_CH01-SCN-021_BACK_LANES_V002 | 1536×1024 | 833c415f2db4 | **PASS (ref)** | Laterite walls + bamboo palisade + paved gutter; coherent; reference only |
| 14 | SCENE_CH01-SCN-022_STREETS_V002 | 1536×1024 | bd12db37b048 | **PASS (ref)** | Laterite lane, indigo curtain doorway, paver gutter; coherent; reference only |
| 15 | SCENE_CH01-SCN-024_AN_EMPTY_HOUSE_V002 | 1536×1024 | b34f2ed20313 | **REJECT (lineage)** | See reconciliation above; same design@V002 as rejected wave item |
| 16 | SCENE_CH01-SCN-030_PALACE_COURTYARD_V002 | 1536×1024 | 1c491f5fc130 | **REVISE** | Portal block + walls too smooth/uniform (modern-render feel); NO distinct palace grammar (no scale hierarchy, no verandah rhythm); re-grade or rebuild after palace-grammar research; reject if presented as palace final |
| 17 | ENV_CH01-SUB-017_THE_OVERGROWN_WALL_V002 | 1536×1024 | b56bb0b1201b | **PASS (ref)** | Laterite rubble ruin + cracked pot; atmospheric; reference only |
| 18 | ENV_CH03-TRV-003_THE_NARROW_PASSAGES_V003 | 1536×1024 | adfdf250682d | **DEFER** | Mud-brick canyon coherent for "City of the Living Dead" fiction, BUT (a) CH03 grammar unresearched in this pass; (b) conical tower reads Sudano-Sahelian; needs CH03-specific exact-version research + CD subject ruling; do not clear |
| 19 | ENV_CH03-SUB-006_THE_BACK_PLOTS_V003 | 1536×1024 | e5391b2fe09a | **DEFER** | Yam-mound accuracy ✓ (real Igbo ridge farming) but same CH03 grammar + tower issue; needs CH03 research + ruling; do not clear |
| 20 | ENV_CH03-INT-002_THE_POTTERS_SHOP_V002 | 1536×1024 | dc5e032590e8 | **PASS (ref)** | Rock-hewn potter's cave interior; coherent with CH03 fiction; reference only |
| 21 | ENV_CH03-INT-003_THE_CLOTH_SELLERS_SHOP_V002 | 1536×1024 | e98005896c17 | **PASS (ref)** | Rock-hewn cloth store, indigo/natural bolts; coherent; reference only |
| 22 | ENV_CH02-SET-001_THE_LOWER_MARKET_V002 | 1536×1024 | 146f01fd26c2 | **PASS (ref)** | Subterranean market, indigo awnings, torch; coherent with "Kingdom Beneath Earth"; reference only |
| 23 | ENV_CH02-SUB-004_THE_DRIP_BASINS_V002 | 1536×1024 | 5a29e25f417a | **PASS (ref)** | Cave drip pools + ladles; coherent; reference only |
| 24 | ENV_CH02-SUB-005_THE_FORGOTTEN_QUARTER_V002 | 1536×1024 | 03f01ee577a7 | **PASS (ref)** | Mud-plaster colonnaded corridor; coherent; reference only |
| 25 | ENV_CH02-TRV-006_THE_SIDE_TUNNELS_V002 | 1536×1024 | 8ee0c2d24495 | **PASS (ref)** | Rock-hewn shoring corridor + torch; coherent; reference only |
| 26 | ENV_CH02-INT-002_A_DWELLING_CHAMBER_V002 | 1536×1024 | d4bab1c92afe | **PASS (ref)** | Rock-hewn dwelling, fire/mat/pots; coherent; reference only |
| 27 | ENV_CH02-INT-003_THE_SMITHS_WORKSHOP_V002 | 1536×1024 | efd2a86b7ba1 | **PASS (ref)** | Forge/anvil/tongs/charcoal; strong tooling accuracy; reference only |
| 28 | ENV_CH02-INT-004_THE_ORE_STORE_V002 | 1536×1024 | 8c57bd43a66b | **PASS (ref)** | Ore/charcoal piles, baskets; coherent; reference only |
| 29 | ENV_CH02-INT-005_THE_OVERSEERS_ROOM_V002 | 1536×1024 | 9bd0447df52d | **PASS (ref)** | Desk/stools/mat + ledger-like pots; coherent; reference only |

## TALLY
**PASS 22 · REVISE 3 · REJECT 2 · DEFER 2 · cleared for production: 0.** Manifest docs (22) untouched — context only. All files preserved in place; nothing overwritten; full hashes filed separately (`FP10_FRESH_PASS_MANIFEST.csv`). SCN-017/024 disposition for CD: commission V003 only as NEW directions. The 3 REVISE items are correctable by the submitting artist; CH03 DEFERs wait on CH03 research.

## Direct consequences
- No PENDING file graduates. C-01 greybox continues unaffected (it never depended on these boards).
- SCN-012 REVISE flags a recurring failure mode (Sahelian grammar leak) — recorded for all future CH01 generation prompts: forbid toron/banco/beehive-tower motifs; Igbo = mud-plaster + thatch + timber only.
- Next action (Research org/CD): ratify tally → CD records verdicts → register v8 delta prepared **after** ratification (FP-08 authorization).
