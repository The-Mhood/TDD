# PM ← Design controlled integration record — W1 D4

**Integration target:** `arena/553fb02d-tdd` (PM production branch)
**PM HEAD before integration:** `e208cb19d832388a9e9fbdffbc7876601b7811c4`
**Design source:** `arena/6e649a9b-tdd`, commit `d50658a346a9cda4ba851aa24979f1b9d9cddc70`
**Design parent:** `57b81bd52ce153ed7a6c54643677629db927fa8f`
**Method:** selective file-level import from the named Design commit and its parent spec. No branch switch, reset, rebase, wholesale merge, or overwrite of PM code/content was performed. Design's additions live in `.arena/production/...`, separate from the PM gameplay sources and existing `Tools/unreal/build_chapter1_greybox.py`.

The Design branch is based on the common `main` root and contains a separate production-document tree; merging its full tree into PM would bring unrelated branch-level additions/deletions. This scoped transfer preserves the PM branch ancestry and the Design commit's exact source hash for provenance. The source branch/ref was fetched for read-only inspection; it was not changed. The PM W1 D3 gameplay source was then recorded in its own commit `8721a97cbb0f85a2a7b952a29e515276725730e9`; it is separate from the Design file import.

## Imported deliverables

The following are exact snapshots from Design `d50658a` unless noted; the source commit is unchanged:

1. `.arena/production/2026-11-20_w1d3_ch01_greybox/ADANNA_CONTROLLED_BATCH_BRIEF_2026-11-20.md`
2. `.arena/production/2026-11-20_w1d3_ch01_greybox/CH01_GREYBOX_PLAN.png` (the top-down schematic; a layout aid only)
3. `.arena/production/2026-11-20_w1d3_ch01_greybox/CH01_GREYBOX_REPORT_2026-11-20.md`
4. `.arena/production/2026-11-20_w1d3_ch01_greybox/CH01_RESEARCH_NOTES_2026-11-20.md`
5. `.arena/production/2026-11-20_w1d3_ch01_greybox/FP10_FRESH_PASS_SCOPE_TABLE_2026-11-20.md`
6. `.arena/production/2026-11-20_w1d3_ch01_greybox/OWNER_DECISION_RECORD_2026-11-20_W1D3.md`
7. `.arena/production/2026-11-20_w1d3_ch01_greybox/W1D3_REPORT_2026-11-20.md`
8. `.arena/production/2026-11-20_w1d3_ch01_greybox/build_ch01_greybox.py` — imported byte-identically, then updated by the D4 PM-controlled gate/interior-shell patch documented in `PM_CONTROLLED_BUILDER_PATCH_D4.md`.
9. `.arena/production/2026-11-20_w1d3_ch01_greybox/render_plan.py` — imported byte-identically, then updated with the D4 open-gate annotation; the original Design schematic is retained as `CH01_GREYBOX_PLAN_DESIGN_D506.png`.
10. `.arena/production/2026-11-20_w1d1_production/ADANNA_PRODUCTION_WORKBOOK_2026-11-20.md` — current Design snapshot, including §11 owner decisions (AD-01..04 and identity locks).
11. `.arena/production/2026-11-20_w1d1_production/FP07_TD_SPEC_001_DRAFT_2026-11-20.md` — current Design snapshot, including Addendum A baseline UE 5.8.4 / Blender / FBX centimetre conversion and still-open TD ratifications.
12. `.arena/production/2026-11-20_w1d2_production/DRIVE_FOLDER_AUDIT_2026-11-20.md` — current Design snapshot including owner closure.
13. `.arena/production/2026-11-20_w1d1_production/CH01_ENVIRONMENT_PRODUCTION_BREAKDOWN_2026-11-20.md` — imported from Design parent `57b81bd` because it is the builder's referenced §9 specification; it is a greybox/layout spec, not approval of final design. One trailing Markdown space was normalized; both source and working blob hashes are recorded.

## Review findings / non-overwrite decisions

- The schematic is an engineering plan, not an actual environment or screenshot from Blender/Unreal. It depicts the settlement, gate, roads, square, palace axis, market, farms, stream, structures and anchors. The separate PIL renderer was executed in this host to `/tmp`; output was 1350×1350 and byte-identical to the imported PNG (`evidence/SCHEMATIC_RENDER_VERIFICATION.txt`). This verifies only the schematic generator, not Blender geometry.
- The builder is distinct from PM's existing forest/route generator; both remain available. Design's builder constructs the larger Chapter 1 settlement in metres and intends to save a Blender `.blend`, export FBX and write a manifest. It had no generated `.blend`, `.fbx`, or manifest at source commit time.
- Static review found the original Design builder's leaves blocked the gate opening and its registered building/interior blockouts were solid masses. A PM-controlled D4 patch now swings the gate leaves clear and builds enterable shell geometry with door gaps; the original Design PNG and source commit remain preserved. This patch is source-only and unexecuted. The stream remains a flat strip with wading anchors rather than measured water/terrain; collision, doorway clearances, and imported FBX orientation/scale still need validation in Blender/UE.
- Adanna workbook §11 preserves the approved identity locks and explicitly defers blade/scabbard geometry; V003/V004 identity selection remains Our Eyes/Research evidence followed by delegated CD selection. It does not add an approved production mesh. Therefore the PM technical proxy remains a technical proxy and is not promoted or replaced.
- The FP-10 table is a fresh-pass scope work order, not Research clearance. Design's report says the 29 artwork candidates and the V003/V004 review are still pending; no visual approval or production image generation is inferred.

## Execution evidence and exact blocker

A supported Blender binary is not installed in this sandbox. As a practical execution attempt, installed the PyPI Blender Python module `bpy==4.5.16` into `/tmp/tdd-bpy` (not the repository) and attempted `import bpy`. It fails before script execution. `ldd /tmp/tdd-bpy/bpy/__init__.so` confirms these unavailable shared libraries:

```text
libGL.so.1
libICE.so.6
libSM.so.6
libXfixes.so.3
libXi.so.6
libXrender.so.1
libxkbcommon.so.0
```

No `.blend`, FBX or manifest was generated. The repo host also has no UE Editor/UBT installation (`UnrealEditor` and `UnrealEditor-Cmd` absent), and is Linux x86_64 rather than the owner Mac/reference Windows environment. Thus UE 5.8.4 build/import/PIE and Windows x64 Shipping are **not run**. This is execution evidence, not a claim that the scripts passed. The exact import failure and dependency scan are captured in `evidence/EXECUTION_BLOCKER_LINUX.txt`; imported source file hashes are checked against Git objects in `evidence/IMPORT_HASH_VERIFICATION.txt`. D4 host-gated Mac/Windows command outputs and rerun tests are in `docs/06_IMPLEMENTATION/evidence/20261120T-W1D4/`.

## Exact owner-platform handoff

On a workstation with Blender 4.2+ (preferably Blender 4.5 LTS, after TD confirms the workstation's production pin), from the imported Design directory:

```sh
# macOS example
"/Applications/Blender.app/Contents/MacOS/Blender" --background --python build_ch01_greybox.py

# Windows PowerShell example
& "$env:ProgramFiles\Blender Foundation\Blender 4.5\blender.exe" --background --python build_ch01_greybox.py
```

Expected outputs beside the script: `CH01_GREYBOX.blend`, `CH01_GREYBOX.fbx`, `CH01_GREYBOX_MANIFEST.json`; save Blender stdout/stderr and confirm the object count and each file exists/non-zero. Open the `.blend` in GUI Blender and inspect the gate opening, interior access, terrain/stream, collisions, scale, anchor positions, and proposed-subject flags before exporting to UE.

In the UE 5.8.4 project, run the project's Mac build/automation command `Tools/engine/run_daily_train.sh` from the project root first. Then import the FBX into a new technical-only content folder (do not overwrite existing production assets), explicitly verify centimetres, forward/up axes, normals, collisions and navigation, open the generated map and run PIE traversal, gate, interior, movement and encounter checks. Preserve full import/build/automation logs, screenshots and PIE recording. On the reference Windows PC, run `Tools/engine/windows_ci.sh arena/553fb02d-tdd` from a clean checkout at the pushed commit. This D4 change adds `TheDisobedientDaughter Win64 Shipping` as a separate UBT build gate and records it at `Saved/BuildEvidence/<UTC>/02b-build-win64-shipping.log`; expected target output is `Binaries/Win64/TheDisobedientDaughter-Win64-Shipping.exe`. This validates Shipping compilation only, not cooking or packaging. Preserve that log and the existing Editor-development/automation logs; the Linux static safety test does not establish a successful Shipping build.

## Separate / not integrated

- No cherry-pick or merge of Design's branch history was performed; only the enumerated production deliverables were imported. The `arena/6e649a9b-tdd` branch and its commit graph remain separate and untouched.
- The rest of Design's W1 D1/D2 production tree, Royal Guard review assets, external Drive contents, and any source not listed above remain separate. They can be integrated later as specifically needed; none was silently substituted for an approval.
- No generated `.blend`, FBX, manifest, Unreal map, native Adanna asset, screenshots or gameplay recording exists from this sandbox run.
