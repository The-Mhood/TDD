# TDD — Gap Register & Production Assessment

**Date:** 2026-11-23
**Branch:** `arena/553fb02d-tdd`
**Commit base:** `abb4a16` (Adanna integration + import fix)
**Source of truth:** GitHub branch `arena/553fb02d-tdd`. Owner-Mac build/PIE of new commits PENDING.

## 1. What was actually found in the repository

- A large, heavily-documented 8-chapter game design (`docs/` — story, world, character,
  combat, production plans, ADRs, defect registers, ledgers).
- A single-module UE 5.8 C++ project at `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project`
  (module `TDD_GAME`, deps Core/CoreUObject/Engine/InputCore).
- A proven **technical proxy** M1: `ATDDAdannaProxyCharacter` (cube-part blockout),
  `ATDDForbiddenForestLevel` (procedural primitive forest), `TDDForbiddenForestGameMode`,
  objective HUD, route progress, 2 interactables. **Owner-confirmed PIE-playable** on
  `PLAYABLE_FOREST_M1` (forest renders, proxy controllable, 46 obstacles / 7 waypoints /
  2 interactables).
- A Omega Valley "living world" scaffold: calendar/population/market/weather/location
  subsystems (Omega Valley, not the M1 forest) — pure logic + world subsystems, not yet
  integrated into M1 gameplay.
- Real Adanna assets on disk: `adanna_m1_technical_proxy_uv.glb` (21-joint skinned mesh,
  idle/walk/run/jump/land, 8 material slots, UV atlas) + 6 forest module GLBs. Classified
  **"rigged technical gameplay proxy — NOT final character"**, pending creative approval.
- Pure-logic gameplay math (combat, dodge distance, state machines) in `TDDWorldLogic.h`,
  covered by pure g++ tests — but **not integrated** into the live character.

## 2. Gap register

### Completed and verified
- UE 5.8 Mac compile of the Phase-1 C++ repair (commit `995caf9`, owner build exit 0 — B1).
- M1 PIE playability of the proxy world + proxy character (owner-confirmed 2026-11-23).
- Static regression suite: readiness 0/0, audit 117/117, classifier 10/10, pure g++ 937
  assertions.
- M1 map creation + config repoint + handoff import script (macOS), now with the Interchange
  skeletal-import fix.

### Implemented but not verified (owner-Mac build/PIE pending)
- **Adanna skeletal-mesh integration** (`ATDDAdannaCharacter` + `UTDDAdannaAnimInstance`)
  — code complete, static-green, **not yet compiled or PIE-verified** (commit `abb4a16`).
- **UE 5.8 skeletal GLB import** via Interchange `force_all_mesh_as_type =
  IFMT_SKELETAL_MESH` — script fixed, **not yet executed in the Editor**.
- GameMode now spawns `ATDDAdannaCharacter` (was `ATDDAdannaProxyCharacter`).

### Partially implemented
- **Animation coverage**: imported clips are idle/walk/run/jump/land. Missing from the asset:
  duck, crawl, start/stop transitions, direction changes, fall (distinct from jump), interact,
  combat, dodge. The C++ state machine covers the states but the clips for duck/crawl/
  combat/dodge/interact do not exist in the handoff asset.
- **Combat / dodge**: pure distance/state math exists (`TDDWorldLogic.h`, tested) but there is
  no health/damage component, no dodge action, no combat state integrated into the character.
- **Forest environment**: still built from Engine Basic Shapes. The 6 forest module GLBs are
  now imported by the script but **not placed** in the level. White cloth is waymarker
  cylinders + HUD text, not a world element. Great Root Mother is a trunk, not an arrival
  interactable.
- **Input**: character uses legacy input (BindKey/BindAxisKey). Enhanced Input initializes but
  is not wired to the character.
- **Omega Valley living-world subsystems**: calendar/population/market/weather exist as
  subsystems but are not integrated into the M1 forest gameplay.

### Missing
- Enemy actors / AI controller / AI behavior trees.
- Health & damage system.
- Audio (no audio assets, no audio components).
- Save / checkpoint / persistence (`USaveGame`).
- Level transitions / chapter flow.
- Final Adanna art (groom, costume, facial, PBR textures) — creative approval pending.
- Final environment art (the forest is a blockout).
- Duck / crawl / interact / combat / dodge animation clips.

### Blocked by an external dependency
- **UE 5.8 / Blender / owner Mac** are absent from the agent sandbox. All compile, PIE, cook,
  package, import and visual verification require the owner machine.
- **Final Adanna portrait/art** — `reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg`
  is a 19-byte stub; the real approved portrait is required for the W2 facial pipeline.

### Awaiting creative approval
- Adanna final turnaround, dimensions, hair/groom, costume, facial design, calibrated
  materials/textures (per `M1_ASSET_INTEGRATION_SPECIFICATION.md` §4 and the import manifest).
- The imported skeletal proxy is explicitly **not** final Adanna; it is the approved identity
  reference's technical gameplay proxy.

### Obsolete / superseded
- `ATDDAdannaProxyCharacter` is superseded as the player pawn by `ATDDAdannaCharacter`
  (retained only as the fallback visual builder and for audit history).
- `TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py` retained unchanged for audit only.

## 3. Actual Adanna status

The intended character **has been integrated in source** (commit `abb4a16`):
`ATDDAdannaCharacter` uses a `USkeletalMeshComponent` bound to the imported Adanna mesh,
with a C++ animation state machine (`UTDDAdannaAnimInstance`) playing the imported
idle/walk/run/jump/land clips. The GameMode spawns it. **Remaining:** the owner must run the
fixed import script (Interchange skeletal force) to land the mesh + animations in UE, then
verify the character renders and animates in PIE. Until then, the character falls back to the
labelled proxy visuals so PIE stays playable. **This is the technical gameplay proxy, not
final approved Adanna art.**

## 4. Playable experience status (what a player can genuinely do now)

**Before owner verification of `abb4a16`:** the proven proxy experience — launch into
`PLAYABLE_FOREST_M1`, move (WASD), run (Shift), jump (Space), look (mouse), interact (E),
follow the white-cloth route to the Great Root Mother, with the objective HUD.

**After the owner runs the import + rebuilds + PIE (pending):** the same controls with the
**actual Adanna skeletal mesh** and idle/walk/run/jump/land animation, instead of the cube
proxy. Movement, camera, interaction and objective progression are unchanged.

## 5. Outstanding blockers (genuine only)

1. **Owner-Mac UE build of `abb4a16`** — must compile both targets before any PIE claim.
2. **Owner must execute the fixed import script** in the Editor to land the Adanna skeletal
   mesh + animations + forest modules (Interchange skeletal force).
3. **Owner-Mac PIE of the integrated Adanna** — visual + animation verification.
4. **Final Adanna art / creative approval** — blocks final character visual acceptance.
5. **Final environment art** — forest is still a primitive blockout.

## 6. Verification evidence (separately)

| Check | Result | Scope |
|---|---|---|
| Static readiness (`build_readiness.py`) | 0 blockers / 0 warnings | source only |
| macOS audit (`audit_ue_macos.py`) | 117/117 | source + helper |
| Classifier regression | 10/10 PASS | diagnostic classifier |
| Pure g++ suite | 937 assertions PASS | pure logic only |
| UE 5.8 Mac build of `abb4a16` | **PENDING** | owner machine |
| PIE of integrated Adanna | **PENDING** | owner machine |
| Cook / package | **PENDING** | owner machine |

> Static checks do **not** prove compile, PIE, cook or package. No claim is made without
> owner-machine evidence.

## 7. Next implementation priorities (concrete)

1. **P1 (verify):** owner builds `abb4a16`, runs the import script, PIE-verifies Adanna
   renders + animates; feed back failures for fixing.
2. **P2 environment:** rework `ATDDForbiddenForestLevel` to instance the imported forest
   module GLBs (tree/fern/rock/great-tree/waymarker/boundary-post) instead of primitive
   shapes; make the white cloth a real world element (cloth mesh/sprite along the route);
   build the Great Root Mother as an arrival interactable.
3. **P1 gameplay:** integrate dodge into `ATDDAdannaCharacter` (consume the tested dodge
   math), add the interact animation trigger, wire Enhanced Input.
4. **P3 systems:** health/damage, enemy/AI foundations, audio, save/checkpoint, level
   transitions — in dependency order, each verified before the next.
5. **P4 pipeline:** generalise the M1 vertical-slice architecture into the chapter production
   workflow.

## 8. Owner actions (only what cannot be executed remotely)

```bash
# 1. Sync to the new commit
git fetch origin arena/553fb02d-tdd && git checkout arena/553fb02d-tdd && git pull origin arena/553fb02d-tdd

# 2. Build (UE 5.8 Mac ARM64 Development)
UE_ROOT="/Users/Shared/Epic Games/UE_5.8"
bash TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/build_phase1_diagnostic.sh

# 3. Run the FIXED import script in the Editor (Interchange skeletal force)
#    Window > Developer Tools > Output Log > Python:
exec(open(r"/ABS/PATH/TDD/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py").read())
#    Verify Content/TDD/Imports + the Adanna SkeletalMesh + Anim Sequences landed.
#    If the Interchange import names the Anim Sequences differently from idle/walk/run/jump/land,
#    assign the correct SoftObjectPaths on UTDDAdannaAnimInstance (Default Properties).

# 4. PIE PLAYABLE_FOREST_M1 and verify: actual Adanna mesh renders, idle/walk/run/jump/land
#    animate, movement/camera/interaction still work. Capture evidence.
```
