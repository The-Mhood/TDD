# PM HANDOFF ADDENDUM — W1 D5 (2026-11-21) — WHAT PM CAN PULL NOW
**Branch:** `arena/6e649a9b-tdd` (pushed; PM fetches this branch) · **Drive:** shared store, IDs in the manifests · **Contact:** Design via this branch's documents.
**Rule of access:** everything listed here is either ON the branch (git paths) or IN Drive (IDs). Nothing lives only in a private workspace.

## Package A — ADANNA (Design status: CD decision pending)
| Item | Where | Tier | PM use |
|---|---|---|---|
| AD-02 complete exact-version review + contact sheet + reference packet | branch: `.arena/production/2026-11-21_w1d5_adanna/` (review, brief, contact sheet, checksums, `reference_packet/` with all 8 plates + master) | C→RC boundary | Understand candidate state; do NOT build from it yet |
| CD decision brief (A/B/C) | branch: same folder `CD_AD02_DECISION_BRIEF_2026-11-21.md` | — | CD ruling; PM informed on signature |
| AD-03 v1 base texture set (cloth/leather/bronze, 2048, deterministic) | branch `…2026-11-20_w1d4_research/textures/` | C+ | TD ratifies on import; engine-material authoring start point |
| **ADANNA_BLOCKOUT_PLACEHOLDER_m.obj** (+ .mtl, 856 tris, height 1.80 m, origin ground centre, +Z up) | branch `…2026-11-21_w1d5_adanna/blockout/` | PLACEHOLDER only | PM/TD: import smoke-test, capsule sizing, pivot/silhouette check vs master; budget_checker PASS filed |
| Full plates (FRONT V004 / TQ V004 / BACK V003 / LS V003; master) — committed this turn for PM access under explicit no-promotion rule: they remain UNAPPROVED and cannot be used until CD signs A/B | branch `…2026-11-21_w1d5_adanna/reference_packet/` + Drive IDs/sha256 in `ADANNA_REFERENCE_CHECKSUMS_2026-11-21.txt` | unapproved | reference only; no approvals implied |
**PM actions when CD signs A:** create `Content/Adanna/` scaffolding; capsule per TD; import blockout as silhouette sanity check (replace with LOD0 when AD-03 lands); keep FP-07 cm discipline; **do not** import any Adanna plate as a texture without CD/TD sign-off.

## Package B — CH01 ENVIRONMENT
| Item | Where | Tier | PM use |
|---|---|---|---|
| Greybox builder + PLAN.png | branch `…2026-11-20_w1d3_ch01_greybox/` | C | run on workstation per W1 D3 report (blocked in Design sandbox) |
| **CH01-SUBJ-001 family-house production-target sheet (VERIFIED)** | branch `…2026-11-21_w1d5_ch01/CH01-SUBJ-001_FAMILY_HOUSE_TARGET_SHEET.jpg` + `RESEARCH_RECORD_…_FAMILY_HOUSE_2026-11-21.md` + `VERIFIED_…_2026-11-21.md` | C→RC | target direction for KIT-HUT module; dimensions/pivots after CD kit approval |
| CH01 PM/integration pack (runbook, assumptions-not-canon, asset gates) | branch `…2026-11-20_w1d4_research/CH01_PM_AND_ASSET_PREP_2026-11-20.md` | C | build order + integration checks |
**Framing caution (repeated, binding):** the family-house sheet is a verified TARGET, not an approval; kit build precedes any import; greybox assumptions never become canon.

## Package C — RG / ENEMY (unnamed guard-class, unarmed)
Findings + A–G + coordination + PM questions: branch `…2026-11-20_w1d3_rg_v002/RG_V002_REVIEW_FINDINGS_2026-11-20.md` + `…2026-11-20_w1d4_research/RG_V002_COORDINATION_2026-11-20.md`. **PM actions:** answer the 5 coordination questions (Section 5) at next sync; rig proposal (shared HUMAN_BASE) awaits TD; animation authoring waits on PM minimum-set ruling. No assets until CD REVISE ruling.

## Package D — FP-10 / research disposition (W1 D4 output, unchanged)
29/29 artwork verdicts + reconciliation + manifest: branch `…2026-11-20_w1d4_research/`. **No action for PM**; CD ratifies tally → register v8.

## What PM should NOT expect today
No Adanna FBX/uasset · no CH01 modulars · no rig/animation · no Unreal-verified assets. Blockers: CD AD-02 signature; capable-Blender runner for greybox/kit builds; TD rulings (skeleton family, texel density, cm checks); PM rulings (anim minimums, guard mechanic). Everything else is in flight.
