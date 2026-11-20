# macOS / UE 5.8 execution runbook — TDD_GAME

**Owner environment:** Apple M4 Mac, 16 GB RAM, macOS 27.2.1 (26B131), ARM64,
Unreal Engine 5.8.4 (CL 58902052), Xcode 27.2 (27B52).
**Status of every step below: not yet executed.** Nothing here has been run on the owner's
machine. This file is the procedure, not evidence. Status stays
**BLOCKED — OWNER-STUDIO DEPENDENCY** until each command's real output is recorded.

Set these once per terminal session. Adjust only if your install path differs.

```bash
export UE_ROOT="/Users/Shared/Epic Games/UE_5.8"
export TDD_REPO="/ABS/PATH/TO/TDD"
export TDD_UE="$TDD_REPO/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project"
export UE_EDITOR="$UE_ROOT/Engine/Binaries/Mac/UnrealEditor"
export UE_CMD="$UE_ROOT/Engine/Binaries/Mac/UnrealEditor-Cmd"
export UE_UAT="$UE_ROOT/Engine/Build/BatchFiles/RunUAT.sh"
mkdir -p "$TDD_UE/Saved/TDD_M1/Evidence"
```

> If the engine came from the Epic Games Launcher it lives under `/Users/Shared/Epic Games/UE_5.8`.
> If you built from source it lives wherever you cloned it. `EngineAssociation` in the
> `.uproject` is `5.8`; a launcher install resolves that automatically.

---

## 0. Verify the engine and the toolchain (do this first, always)

Run the gate. It is read-only: it installs nothing, downloads nothing, downgrades nothing.

```bash
./Tools/verify_toolchain.sh            # verdicts for CAP-1..CAP-4
./Tools/verify_toolchain.sh --build    # then: the real editor compile (only proof of CAP-1)
```

Status: **PRODUCED — NOT YET VERIFIED**. It has been exercised against stubbed hosts in the
sandbox (all five verdict branches) but has never run on macOS.

### The owner's toolchain, and what is actually confirmed

Target: UE **5.8.4** (CL 58902052), Xcode **27.2** (27B52), macOS **27.2.1** (26B131), M4, 16 GB.

| Capability | Verdict | Basis |
|---|---|---|
| CAP-1 native C++ editor compile | **GO** | Xcode 27 compiles and links UE 5.8 game binaries; only the final `.app` step broke. Our module is four engine modules, no lambdas, no shadowing-prone captures. |
| CAP-2 open project, launch editor, generate M1 map | **GO** | UE 5.8's `Apple_SDK.json` `MaxVersion` accepts Xcode 27 (5.7 was capped at 26.9 and is not affected here). |
| CAP-3 PIE | **GO** | No engine/runtime bound in any report of the failure class. |
| CAP-4 cook + package + launch | **GO on 5.8.4** | Epic closed UE-396802 as Fixed for 5.8.4 and confirmed the Mac fix in the Mac bug thread. |

**Do not downgrade Xcode.** The old "avoid Xcode 27" advice applied to 5.8.0–5.8.3, where the
`.app` finalize step failed on any C++ project. On 5.8.4 that defect is fixed.

**Prerequisite that is easy to miss:** install the Metal toolchain, or shaders will not compile.

```bash
xcodebuild -downloadComponent MetalToolchain
```

### What is not confirmed, stated plainly

- Epic's *published* 5.8.4 release-note line names only **iOS** `.app` finalize ("Bad file
  descriptor" with macOS 27). The **Mac** game target is covered by Epic staff statements in the
  Mac bug thread, not by that release-note text. The gate checks the shipped binary for the fix
  marker and reports CONDITIONAL if it is absent.
- No public report yet shows a **5.8.4 + Xcode 27.2 + macOS 27.2.1** Mac package end to end.
  Every measurement in that failure class predates 5.8.4 or used Xcode 26.6.
- Engine still publishes Xcode **26.1.1** as recommended and lists no macOS 27 in its matrix.
  Accepted by the SDK gate is not the same as tested by Epic.

### Fallbacks, in order, if CAP-4 fails

1. Confirm the engine really is 5.8.4 (`Build.version` `PatchVersion`), not 5.8.3.
2. Check for iCloud/Finder xattrs. A checkout under `~/Documents` fails codesign **even on 5.8.4**.
3. If the log says `Failed to finalize the .app with Xcode` with a `Touch UBT generated tiles`
   pre-action failure, the stdin defect is present in that build:
   `./Tools/verify_toolchain.sh --emit-workaround ~/xcode27-stdin-shim`, then re-run the package
   command it prints. Keep `-package`; `-archive` alone copies the bare `Binaries/Mac/*.app`.

---

## 1. Confirm the project version requirement

```bash
python3 - <<'PY'
import json, os
p = os.path.join(os.environ["TDD_UE"], "TDD_GAME.uproject")
d = json.load(open(p))
print("EngineAssociation:", d["EngineAssociation"])
print("Modules:", [m["Name"] for m in d["Modules"]])
print("Plugins:", d.get("Plugins"))
print("TargetPlatforms:", d.get("TargetPlatforms"))
PY
# UBT loads ONLY files named *.Target.cs. There must be exactly two, and nothing else
# in Source/ may declare TargetRules - a differently-named copy is never read.
ls -1 "$TDD_UE/Source/"*.Target.cs
grep -rn "TargetRules" "$TDD_UE/Source/" --include=*.cs | grep -v "\.Target\.cs:"
grep -n "BuildSettingsVersion\|IncludeOrderVersion" \
  "$TDD_UE/Source/TDD_GAME.Target.cs" "$TDD_UE/Source/TDD_GAMEEditor.Target.cs"
```

Expect exactly `TDD_GAME.Target.cs` and `TDD_GAMEEditor.Target.cs`, the second grep empty,
`EngineAssociation: 5.8`, and **the same** `BuildSettingsVersion.V7` /
`EngineIncludeOrderVersion.Unreal5_8` in both targets.

`DefaultBuildSettings` is part of the shared build environment. This project is built
against the Launcher engine, so its modules link against the engine's precompiled
`UnrealEditor`. If a target asks for a different `BuildSettingsVersion`, UBT stops before
compiling anything:

```
TDD_GAMEEditor modifies the values of properties: [ UndefinedIdentifierWarningLevel: Off != Error,
UnreachableCodeWarningLevel: Off != Error, ReturnTypeWarningLevel: Off != Error,
DanglingWarningLevel: Off != Error ]. This is not allowed, as TDD_GAMEEditor has build
products in common with UnrealEditor.
```

Do not reach for `BuildEnvironment = TargetBuildEnvironment.Unique` to silence that: an
installed engine rejects it ("Targets with a unique build environment cannot be built with
an installed engine"). Do not set `bOverrideBuildEnvironment` either - it only forces a
divergence through. The correct fix is that both targets agree.

---

## 2. Compile

```bash
"$UE_ROOT/Engine/Build/BatchFiles/Mac/Build.sh" \
  TDD_GAMEEditor Mac Development \
  -project="$TDD_UE/TDD_GAME.uproject" \
  -architecture=arm64 \
  -waitmutex 2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/01_compile.log"
echo "exit=${PIPESTATUS[0]}"
```

Success criterion: `exit=0` and `Total execution time` in the log, with no `error:` lines.

```bash
grep -Ei "error:|warning: .*deprecat|Result: Failed" \
  "$TDD_UE/Saved/TDD_M1/Evidence/01_compile.log" | head -40
```

If a target-rule file changed since the last attempt, clear the cached makefile so UBT
does not reuse the old environment check. Delete only build artefacts, never `Content/`
or `Source/`:

```bash
rm -rf "$TDD_UE/Binaries" "$TDD_UE/Intermediate"
```

---

## 3. Open the correct project

```bash
open -a "$UE_EDITOR" --args "$TDD_UE/TDD_GAME.uproject"
```

In the editor: **Edit → Plugins**, confirm enabled — `Python Editor Script Plugin`,
`Editor Scripting Utilities`, `Interchange Framework`. Restart if you changed any of them.

Check the Content Browser: `/Game/TDD/Maps` may not exist yet. That is expected at this point.

---

## 4. Run the setup helper (creates the project-owned map + imports the handoff)

Recommended path — editor is already open and compiled:

1. **Window → Developer Tools → Output Log**
2. Change the entry dropdown from `Cmd` to `Python`
3. Paste (single line):

```python
exec(open(r"/ABS/PATH/TO/TDD/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py").read())
```

Headless equivalent:

```bash
"$UE_CMD" "$TDD_UE/TDD_GAME.uproject" -run=pythonscript \
  -script="$TDD_UE/Tools/TDD_M1_Unreal_Setup_macOS.py" \
  -unattended -nosplash -nopause -stdout 2>&1 \
  | tee "$TDD_UE/Saved/TDD_M1/Evidence/02_setup.log"
```

What it does, in order: records engine/host facts → creates `/Game/TDD/Maps/PLAYABLE_FOREST_M1`
from the default template and saves it → repoints `GameDefaultMap`/`EditorStartupMap` in
`Config/DefaultEngine.ini` (after writing `DefaultEngine.ini.tdd_backup`) →
imports the three labelled technical files into `/Game/TDD/Imports` → writes
`Saved/TDD_M1/tdd_m1_setup_report.json`.

Safety: it never overwrites an existing map or asset (`replace_existing=False`,
`pre_existing` short-circuit). Set `TDD_DRY_RUN = True` at the top to inspect only.

Verify:

```bash
python3 -m json.tool "$TDD_UE/Saved/TDD_M1/tdd_m1_setup_report.json" | head -60
ls -la "$TDD_UE/Content/TDD/Maps/" "$TDD_UE/Content/TDD/Imports/" 2>&1
```

`PLAYABLE_FOREST_M1.umap` must exist on disk. If `Content/TDD/Maps` is empty, the map was not
saved — do not proceed to PIE claiming it exists.

---

## 5. Verify the imports in the Content Browser

`/Game/TDD/Imports/` should contain:

| File | Expected asset type | Check |
| --- | --- | --- |
| `adanna_m1_technical_proxy_uv.glb` | Skeletal Mesh + Skeleton + 5 Anim Sequences + Material + Texture | bone count **21**, clips `idle/walk/run/jump/land`, texture = `adanna_m1_uv_atlas` |
| `forbidden_forest_m1.glb` | Static Mesh (12 named parts) | bounds roughly 3600 × 8800 × ~2000 cm |
| `adanna_m1_collision_proxy.obj` | Static Mesh | height ≈ 176 cm, radius ≈ 34 cm |

```bash
# quick disk-level proof the imported uassets landed
find "$TDD_UE/Content/TDD/Imports" -name "*.uasset" -maxdepth 1 | sort
```

If the GLB arrives as a single Static Mesh instead of a Skeletal Mesh, re-import it with
**Skeletal Mesh** selected in the import dialog and `Import Animations` on. The helper requests
these options but Interchange behaviour must be confirmed on your engine build.

---

## 6. Play In Editor

1. Open `/Game/TDD/Maps/PLAYABLE_FOREST_M1`
2. Confirm **World Settings → GameMode Override** = `TDDForbiddenForestGameMode`
3. Press **Play** (`Cmd+P`), click the viewport once to capture the mouse

Controls: `W A S D` move · mouse look · `Shift` run · `Space` jump · `E` interact · `Esc` release cursor.

Expected: a rigged blockout proxy with a third-person spring-arm camera, a forest of trees,
roots and rocks, a laterite path to follow, white cloth waymarkers, two interaction points,
and an on-screen HUD showing state/speed/grounded/camera/route/jump/land/interact counters.

Record:

```bash
# while PIE is running, the log is live:
tail -f "$TDD_UE/Saved/Logs/TDD_GAME.log"
```

Capture a screen recording (`Cmd+Shift+5`) of at least: idle → walk → run → jump → land →
interact at the first waymarker → reach the Great Root Mother marker.

---

## 7. Cook

```bash
"$UE_UAT" BuildCookRun -project="$TDD_UE/TDD_GAME.uproject" \
  -noP4 -platform=Mac -clientconfig=Development \
  -cook -allmaps -utf8output -unattended \
  2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/03_cook.log"
echo "exit=${PIPESTATUS[0]}"
```

Success: `exit=0` and `Cook commandlet` completes without `Error:`.

---

## 8. Package a runnable macOS build

```bash
"$UE_UAT" BuildCookRun -project="$TDD_UE/TDD_GAME.uproject" \
  -noP4 -platform=Mac -clientconfig=Development \
  -build -cook -stage -pak -package -prereqs \
  -architecture=arm64 -specifiedarchitecture=arm64 \
  -archive -archivedirectory="$TDD_UE/Saved/TDD_M1/Build" \
  -utf8output -unattended \
  2>&1 | tee "$TDD_UE/Saved/TDD_M1/Evidence/04_package.log"
echo "exit=${PIPESTATUS[0]}"

find "$TDD_UE/Saved/TDD_M1/Build" -maxdepth 4 -name "*.app"
```

Codesigning is required for macOS. If signing fails, the usual causes are a missing
development certificate or a wrong team ID under **Project Settings → Platforms → Mac**.
For internal testing only, an unsigned/ad-hoc build can be forced with `-nocodesign`, but
the result is not distributable — record that limitation if you use it.

---

## 9. Launch the packaged build

```bash
APP="$(find "$TDD_UE/Saved/TDD_M1/Build" -maxdepth 4 -name "TDD_GAME.app" | head -1)"
open "$APP"
```

Confirm the packaged app starts on its own (no editor), shows the forest and the proxy, and
is playable. Record a short video of the packaged build; that is the only acceptable evidence
for "packaged build launches".

---

## 10. Evidence to return

Put everything in `ue_project/Saved/TDD_M1/Evidence/` and keep the names:

```
00_toolchain.txt      xcodebuild -version, clang, sdk, sw_vers, sysctl, Build.version
01_compile.log        Build.sh output
02_setup.log          setup helper output
tdd_m1_setup_report.json
03_cook.log
04_package.log
05_pie_video.mov      PIE recording
06_package_video.mov  packaged build recording
07_notes.md           anything that deviated from this runbook
```

---

## Known macOS / M4 / 16 GB constraints

| Step | Expectation | Risk |
| --- | --- | --- |
| Open project | Works | First open compiles shaders for the default template; expect 5–15 min with fan noise |
| Compile TDD_GAME | Works, fast | ~1–2 min incremental; full engine shaders only if you modify engine modules |
| Import Adanna GLB (500 KB) | Works | Trivial; no memory pressure |
| Create `.umap` | Works | Template map is light |
| PIE, forest blockout | Works, may be slow at first | ~46 trees + roots + 64 understory instances; first PIE triggers shader compilation |
| Cook | Works, slowest step | Expect 10–30+ min cold; Metal shader cooking dominates. DerivedDataCache grows several GB |
| Package | Works | Final `.app` copy + codesign; needs free disk |

Practical limits on this machine: keep **Lumen, Nanite and Virtual Shadow Maps off** for the
first pass (already set in `Config/DefaultEngine.ini`), close other apps before cook, and keep
at least 20 GB free for `DerivedDataCache`. The current blockout is far below what 16 GB can
handle; the risk is shader-compilation time, not memory. Real limits appear only once final
production assets, grooms and a dense forest kit are introduced — that is when an asset
budget and LOD pass become mandatory, not now.

---

## What this runbook does not prove

Compile, PIE, cook, package and launch are unverified until you run the commands above and
record the outputs. Final Adanna appearance, dimensions, groom, costume and facial design
remain subject to Creative Director approval, and Forbidden Forest canon, botanical and
landmark approvals remain outstanding, regardless of a successful build.
