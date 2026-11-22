# Playable Adanna M1 — Visibility Failure Root-Cause Report

**Date:** 2026-11-22
**Branch:** `arena/553fb02d-tdd`
**Commit:** `d4f2ce0` (fix) on top of `50ef197`
**Status:** Root cause established from actual source + authoritative UE 5.8 references. **Owner-Mac build + PIE of `d4f2ce0` PENDING** — not yet verified on the target Unreal setup.

## Symptom (owner report)

PIE of the Playable Adanna M1 launches; the HUD is visible, WASD moves the character,
and Space toggles GROUNDED→NO, but the **Forbidden Forest environment and Adanna's
technical proxy are fully invisible**.

## Root cause — rendering (world + character black)

`Config/DefaultEngine.ini` set **`r.AllowStaticLighting=False`**.

`TDDForbiddenForestLevel` and `ATDDAdannaProxyCharacter` build **all** of their geometry
at runtime from Engine Basic Shapes (`/Engine/BasicShapes/{Cube,Cylinder,Sphere,Cone}.*`)
using the **lit** `ForestBasicShapeMaterial` / `ProxyBasicShapeMaterial` (tinted through a
`"Color"` parameter via `UMaterialInstanceDynamic`). With static lighting disabled, the
world's static lights do not illuminate those lit primitives, so **every instanced instance
renders black** and the world + character appear invisible.

This exactly matches the symptom: the **HUD is screen-space** (drawn regardless of
lighting) and **collision is physics** (works regardless of rendering), so both stay
functional while every lit primitive is black.

**Fix applied:** `r.AllowStaticLighting=True` in
`TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Config/DefaultEngine.ini`.

## Root cause — launch map (B3)

`GameDefaultMap` and `EditorStartupMap` still point at **`/Engine/Maps/Entry`** (the empty
engine template). The intended project-owned map `/Game/TDD/Maps/PLAYABLE_FOREST_M1` was
never created because **`Tools/TDD_M1_Unreal_Setup_macOS.py` was never executed**. That
script (verified correct) creates the map from `Template_Default`, repoints both map keys,
sets the world's default game mode, and imports the three handoff assets.

**Fix (owner action):** run the setup script before PIE (commands below).

## Ruled out — proven from source + authoritative UE 5.8 references

| Candidate | Verdict | Basis |
|---|---|---|
| GM spawn / `BeginPlay()` ordering | **Not the cause.** `GameMode::StartPlay()` spawns the level, and `Super::StartPlay()` triggers `NotifyBeginPlay()` → `DispatchBeginPlay()`, so the level's `BeginPlay()` runs and geometry builds. | Epic forums/docs (UE lifecycle) |
| `/Engine/BasicShapes/*` mesh paths | **Valid.** Confirmed canonical engine asset paths. | Web verification |
| POV camera wiring | **Correct.** Adanna's `FollowCamera` becomes the view via `bTakeCameraControlWhenPossessed` / `bFindCameraComponentWhenViewTarget` (both default true); spring arm 440 cm / 65 cm offset is correct. | Epic camera docs |
| Geometry / material / instance code | **Correct.** `CreateInstancePool` + `AddInstance` with proper scales; components registered for collision. | Source review |
| Spawn/ground math | **Consistent.** Adanna `(0,-1800,92)` sits on the ground top within bounds. | `TDDWorldData.h` + level code |

## Files changed

| File | Change |
|---|---|
| `.../ue_project/Config/DefaultEngine.ini` | `r.AllowStaticLighting=False` → `True` (+ explanatory comment) |
| `Tools/engine/build_readiness.py` | New renderer/lighting guard blocking `r.AllowStaticLighting=False` |
| `docs/06_IMPLEMENTATION/DEFECT_REGISTER.md` | D-PHASE1-030 |
| `docs/06_IMPLEMENTATION/QUALITY_LEDGER.md` | New evidence row |

## Regression guards + static test results (agent sandbox)

- `build_readiness.py` renderer/lighting guard: **positive+negative tested** (True → clean; False → blocker).
- `build_readiness.py` (M1 project): **0 blockers / 0 warnings**.
- `audit_ue_macos.py`: **114/114**.
- `test_build_diagnostic_classifier.sh`: **10/10 PASS**.
- Pure g++ suite: **GREEN** (824 assertions across 6 suites).

> These are static checks only. They do **not** prove the UE build or the PIE visual result.

## Exact Mac pull / rebuild / PIE instructions

```bash
# 1. Pull the fix
cd /home/user/TDD   # or your local clone
git fetch origin arena/553fb02d-tdd
git checkout arena/553fb02d-tdd
git pull origin arena/553fb02d-tdd      # should be at d4f2ce0

# 2. Rebuild (UE 5.8 Mac ARM64 Development)
UE_ROOT="/Users/Shared/Epic Games/UE_5.8"
bash TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/build_phase1_diagnostic.sh
# Expect: Build.sh exited 0; Binaries/Mac/TDD_GAME produced.

# 3. Run the setup script ONCE (creates PLAYABLE_FOREST_M1 + repoints config + imports handoff)
#    Recommended: open the project in Unreal Editor, Window → Developer Tools → Output Log,
#    switch dropdown to Python, then:
exec(open(r"/ABS/PATH/TO/TDD/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py").read())
#    Headless equivalent:
"$UE_ROOT/Engine/Binaries/Mac/UnrealEditor-Cmd" \
  "TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/TDD_GAME.uproject" \
  -run=pythonscript \
  -script="TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py" \
  -unattended -nosplash -nopause -stdout 2>&1 | tee Saved/TDD_M1/Evidence/02_setup.log
#    Verify: Content/TDD/Maps/PLAYABLE_FOREST_M1.umap exists on disk.

# 4. PIE
#    Open /Game/TDD/Maps/PLAYABLE_FOREST_M1, confirm World Settings → GameMode Override =
#    TDDForbiddenForestGameMode, press Play (Cmd+P).
#    Expected: lit forest + Adanna proxy visible; move/jump; follow the white cloth route.

# 5. Watch the log while PIE runs
tail -f TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Saved/Logs/TDD_GAME.log
```

## Acceptance

On PIE start the player must **visibly** see the Forbidden Forest environment and Adanna's
technical proxy, move around the world, and follow the white cloth route toward the Great
Root Mother. **Do not mark this resolved until the visual result is confirmed on the owner's
Unreal setup.**
