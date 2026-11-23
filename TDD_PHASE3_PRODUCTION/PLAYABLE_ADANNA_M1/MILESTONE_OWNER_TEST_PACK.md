# Consolidated Owner Test Pack — Integrated Adanna Gameplay Milestone (M1)

**Scope:** One comprehensive owner-side qualification session for the **integrated Adanna gameplay milestone**. This pack consolidates all owner-side testing for the milestone into ONE run. It covers the actual Adanna character, the integrated Forbidden Forest asset modules, dodge/traversal, interaction, the white-cloth world objective, the Great Root Mother arrival, and objective progression + HUD.

**Status:** Source implementation complete and committed (Queue A). **Not yet compiled, imported, or PIE-verified on the owner Mac.** Everything in this pack is owner-side qualification (Queue B). Static checks are green but are **not** Unreal verification.

**Owner environment (from `README_MACOS_UE58.md`):** Apple M4 Mac, 16 GB RAM, macOS 27.2.1, Unreal Engine 5.8.4, Xcode 27.2, ARM64. Blender (version per the asset pipeline; confirm the version used for the GLBs).

> Commands, environment variables and deeper detail are in `ue_project/README_MACOS_UE58.md`.
> This pack is the qualification checklist; it does not repeat every command verbatim. Run the
> items in order. Do not restart the editor between items unless an item says to.

---

## 1. Exact commit / release ref

- **Branch:** `arena/553fb02d-tdd`
- **Milestone tip commit:** `0860725` (chain: `c24d683` → `1f0619d` forest modules + dodge → `0860725` objective progression)
- **Prior milestone commits:** `abb4a16` (Adanna integration + Interchange import fix), `d4f2ce0`/`53ead92` (visibility fix).
- **Confirm before testing:** `git fetch origin arena/553fb02d-tdd && git reset --hard origin/arena/553fb02d-tdd && git rev-parse HEAD` → must equal `0860725…`.
- **Milestone content under test:** `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/` (module `TDD_GAME`).

## 2. Sync instructions

```bash
git fetch origin arena/553fb02d-tdd
git checkout arena/553fb02d-tdd
git reset --hard origin/arena/553fb02d-tdd
git rev-parse HEAD          # expect 0860725…
git status                  # expect clean
```
Set the runbook env vars once (`UE_ROOT`, `TDD_REPO`, `TDD_UE`, `UE_EDITOR`, `UE_CMD`, `UE_UAT`) and create `$TDD_UE/Saved/TDD_M1/Evidence/`.

## 3. UE / Blender versions

- **Unreal Engine:** 5.8.4 (CL 58902052). `EngineAssociation` in `TDD_GAME.uproject` = `5.8`.
- **Xcode:** 27.2 (27B52). **Do not downgrade** — 5.8.4 fixed the Xcode-27 `.app` finalize defect.
- **Prerequisite:** `xcodebuild -downloadComponent MetalToolchain` (shaders will not compile without it).
- **Editor plugins (Edit → Plugins):** `Python Editor Script Plugin`, `Editor Scripting Utilities`, `Interchange Framework` — all enabled.
- **Blender:** the version that produced `model/adanna_m1_technical_proxy_uv.glb` and `model/modules/*.glb`. Record the exact version if the GLBs were regenerated; otherwise use the GLBs as committed (no Blender needed unless item 7 applies).

## 4. Asset / import prep

Assets are committed under `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/model/`:
- `adanna_m1_technical_proxy_uv.glb` — **PROVISIONAL** Adanna skeletal mesh (21 joints, 5 anim clips, 8 material slots), awaiting creative approval. Not final.
- `forbidden_forest_m1.glb` + `model/modules/*.glb` (6 forest modules) — forest kit, **provisional**.
- `adanna_m1_collision_proxy.obj` — collision proxy.

**Do not hand-patch any source or asset.** The import is fully scripted (item 8). If a GLB must be regenerated in Blender (only if the committed GLBs are rejected), record the Blender version and re-run the import script.

## 5. One-time setup

Run once, before build/PIE:
1. `./Tools/verify_toolchain.sh` (read-only gate; CAP-1..CAP-4 verdicts).
2. Compile the module (item 6) so the editor loads the new `ATDDAdannaCharacter` / `UTDDAdannaAnimInstance` / level code.
3. Open the project (`open -a "$UE_EDITOR" --args "$TDD_UE/TDD_GAME.uproject"`), confirm the three plugins are enabled, restart if changed.
4. Run the setup helper (item 8) to create the map and import assets.

## 6. Build commands

```bash
"$UE_ROOT/Engine/Build/BatchFiles/Mac/Build.sh" \
  TDD_GAMEEditor Mac Development \
  -project="$TDD_UE/TDD_GAME.uproject" -architecture=arm64 -waitmutex \
  2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/01_compile.log"
echo "exit=${PIPESTATUS[0]}"
grep -Ei "error:|warning: .*deprecat|Result: Failed" "$TDD_UE/Saved/TDD_M1/Evidence/01_compile.log" | head -40
```
Success: `exit=0`, no `error:` lines. If a target-rule changed, `rm -rf "$TDD_UE/Binaries" "$TDD_UE/Intermediate"` and rebuild (never delete `Content/` or `Source/`).

## 7. Blender qualification steps

**Mandatory only if** the committed GLBs are rejected or a source asset changed. Otherwise **optional / skip** — the committed GLBs are the assets under test.
- Open each GLB in Blender; confirm: skeleton present (Adanna = 21 joints), animations present (`idle/walk/run/jump/land`), UV atlas texture intact, forest modules are static meshes with sensible scale (100 = cm).
- Re-export only if correcting a defect; record Blender version + export settings; re-run the import script (item 8).
- Record results in `07_notes.md`. **Blender inspection is not Unreal verification** — it only validates the source asset.

## 8. UE Editor / import steps

Run the setup helper (creates the project-owned map + imports all assets via the Interchange pipeline):
```bash
# Editor already open + compiled: paste in the Python Output Log:
exec(open(r"/ABS/PATH/TO/TDD/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py").read())
# or headless:
"$UE_CMD" "$TDD_UE/TDD_GAME.uproject" -run=pythonscript \
  -script="$TDD_UE/Tools/TDD_M1_Unreal_Setup_macOS.py" \
  -unattended -nosplash -nopause -stdout 2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/02_setup.log"
```
Verify in the Content Browser that `/Game/TDD/Imports/` contains the Adanna **Skeletal Mesh + Skeleton + 5 Anim Sequences + Material + Texture** and the forest module static meshes. Confirm `PLAYABLE_FOREST_M1.umap` exists. Set `TDD_DRY_RUN = True` at the top of the script to inspect only, if desired.

## 9. PIE scenarios

Open `/Game/TDD/Maps/PLAYABLE_FOREST_M1`, confirm **World Settings → GameMode Override = `TDDForbiddenForestGameMode`**, press **Play** (`Cmd+P`), capture the viewport. Controls: `WASD` move · mouse look · `Shift` run · `Space` jump · `E` interact · **`Ctrl` dodge** · `Esc` cursor.

Record a screen capture covering, in order:
1. **Spawn / idle** — Adanna present (skeletal mesh, not the cube proxy), third-person spring-arm camera, forest + laterite path visible.
2. **Walk** — Adanna walks along the path; `STATE WALK`.
3. **Run** (hold Shift) — `STATE RUN`, speed rises.
4. **Jump + land** (Space) — leaves ground, `GROUNDED NO`, lands, `GROUNDED YES`, `J/L` counters increment.
5. **Dodge** (Ctrl) — burst in the input/facing direction; HUD shows `DODGE` then `DODGE CD` then `DODGE READY`.
6. **Interact at the first waymarker** (E near Y≈-1450 cm) — on-screen interaction message appears, `INT` counter increments.
7. **Follow white cloth waymarkers** — module waymarker meshes are present at route waypoints.
8. **Reach Great Root Mother approach** (Y≈4900 cm) — interact; objective stages to `ROUTE COMPLETE`.
9. **Objective progression** — HUD objective text advances through stages as route progress climbs; `STAGE` value increments.

## 10. Expected visual / functional results

**Visual:** actual Adanna skeletal mesh renders and animates (idle/walk/run/jump/fall/land); forest shows the imported asset modules (trees, ferns, rocks, great tree, boundary posts, white-cloth waymarkers) layered over the blockout; ground/path/interaction rings remain visible; no black/invisible geometry; camera follows at ~4.4 m, clear (not occluded).

**Functional:** WASD/run/jump/land/dodge/interact all respond; dodge grants a burst + brief invulnerability and returns to walk/run; interaction messages fire at both waymarkers; route progress and objective stage update; the two interaction counters and J/L counters increment; HUD shows state/speed/grounded/camera/route/stage/objective.

**Known provisional (not failures):** Adanna GLB and forest modules are **provisional production assets pending creative approval** — visual fidelity/approval is a separate creative sign-off, not this gameplay qualification.

## 11. Cook / package steps

```bash
# Cook
"$UE_UAT" BuildCookRun -project="$TDD_UE/TDD_GAME.uproject" -noP4 -platform=Mac \
  -clientconfig=Development -cook -allmaps -utf8output -unattended \
  2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/03_cook.log"
echo "exit=${PIPESTATUS[0]}"

# Package
"$UE_UAT" BuildCookRun -project="$TDD_UE/TDD_GAME.uproject" -noP4 -platform=Mac \
  -clientconfig=Development -build -cook -stage -pak -package -prereqs \
  -architecture=arm64 -specifiedarchitecture=arm64 -archive \
  -archivedirectory="$TDD_UE/Saved/TDD_M1/Build" -utf8output -unattended \
  2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/04_package.log"
echo "exit=${PIPESTATUS[0]}"
find "$TDD_UE/Saved/TDD_M1/Build" -maxdepth 4 -name "*.app"
```
Success: both `exit=0`, no `Error:`. Codesigning required for macOS; internal-only unsigned build possible with `-nocodesign` (record the limitation). Launch the `.app` and confirm it starts and is playable without the editor (record a short video).

## 12. Failure / log reporting

Save all evidence under `ue_project/Saved/TDD_M1/Evidence/` with these names:
`00_toolchain.txt` · `01_compile.log` · `02_setup.log` · `tdd_m1_setup_report.json` · `03_cook.log` · `04_package.log` · `05_pie_video.mov` · `06_package_video.mov` · `07_notes.md`.

On any failure, return: the exact command, the commit hash, the relevant log tail (compile/setup/cook), the PIE console output, and a short description of the observed vs expected behavior. **Do not patch source files to work around a failure** — report it; the agent will fix and re-commit.

## 13. Pass / fail checklist

| # | Check | Pass criterion |
|---|---|---|
| 1 | Commit ref | `HEAD` = `0860725…`, clean tree |
| 2 | Compile | `exit=0`, no `error:` |
| 3 | Adanna import | Skeletal Mesh + Skeleton + 5 anims in `/Game/TDD/Imports` |
| 4 | Forest import | 6 forest module static meshes + forest GLB in `/Game/TDD/Imports` |
| 5 | Map created | `PLAYABLE_FOREST_M1.umap` exists; GameMode override set |
| 6 | Idle/visual | Adanna skeletal mesh renders; forest modules visible; not black |
| 7 | Movement | WASD walk/run; speed + state update |
| 8 | Jump/land | Leaves/lands ground; J/L counters increment |
| 9 | Dodge | Ctrl triggers burst; DODGE/CD/READY states cycle |
| 10 | Interaction | Both waymarkers fire messages; INT counter increments |
| 11 | White cloth / waymarkers | Module waymarker meshes present along route |
| 12 | Great Root Mother | Arrival interaction fires; objective → ROUTE COMPLETE |
| 13 | Objective/HUD | Route %, stage, objective text advance correctly |
| 14 | Cook + package | Both `exit=0`; `.app` launches and is playable |

## 14. Optional vs mandatory tests

**Mandatory (milestone gate):** items 1–6, 8–13 above (commit, compile, import, map, visual, movement, jump/land, dodge, interaction, white cloth, Great Root Mother, objective/HUD). Cook + package (item 14) is mandatory for release-readiness claims but not for the gameplay milestone gate — mark cook/package as **mandatory for release, optional for this milestone gate**.

**Optional / conditional:**
- **Blender qualification (item 7):** optional unless the committed GLBs are rejected or a source asset changed.
- **Packaged-build launch video:** required only when a release-readiness claim is being made.
- **Facial-likeness / creative visual approval:** separate creative sign-off, not part of this gameplay qualification (provisional assets).

**Not in this pack (automated / non-owner):** static readiness, audit, classifier and pure-core g++ suites are run agent-side and are green at `0860725`; they are not owner tests and are not repeated here.

---

**Traceability:** D-PHASE1-031 (import fix), D-PHASE1-032 (Adanna integration), D-PHASE1-033 (forest modules), D-PHASE1-034 (dodge/traversal) — see `docs/06_IMPLEMENTATION/DEFECT_REGISTER.md`. This pack is the owner-side evidence gate for those; **no owner-side test is marked complete without the returned evidence above.**
