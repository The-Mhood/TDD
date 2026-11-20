# Owner-studio execution request — macOS / Unreal Engine 5.8

**Status:** **BLOCKED — OWNER-STUDIO DEPENDENCY** for compile, PIE, cook, package and a runnable build.
**Environment (supplied by owner, no longer requested):** Apple M4 Mac · 16 GB RAM · macOS 27.2.1 · ARM64 / Apple Silicon · Unreal Engine 5.8 installed.

This supersedes the earlier "tell us your engine version and hardware" request. That information
is now known. What remains is **execution access and recorded output**, and a small number of
toolchain facts that only your machine can report.

## 1. Toolchain facts only your Mac can report

Run this block in Terminal and return its output. It is one paste, no secrets.

```bash
export UE_ROOT="/Users/Shared/Epic Games/UE_5.8"   # adjust if you built from source

cat "$UE_ROOT/Engine/Build/Build.version"
xcode-select -p
xcodebuild -version
clang --version
xcrun --sdk macosx --show-sdk-version
sw_vers
sysctl -n machdep.cpu.brand_string hw.memsize hw.optional.arm64
df -h "$HOME" | tail -1
```

Decision points this answers:

| Fact | Requirement for UE 5.8 | Why it matters |
| --- | --- | --- |
| `xcodebuild -version` | 26.0 minimum, **26.1.1 recommended** | Xcode 26.4 is not compatible with Unreal Engine |
| macOS SDK | matching the selected Xcode | mismatched SDK breaks Metal shader toolchain |
| `Engine/Build/Build.version` | a 5.8 build | confirms the exact patch install the project compiles against |
| free disk | ≥ 20 GB | DerivedDataCache plus cooked data |

If Xcode is 26.4 or newer, install 26.1.1 alongside and select it:

```bash
sudo xcode-select -s /Applications/Xcode_26.1.1.app/Contents/Developer
```

## 2. Access needed — execute and record

The full command sequence, with exact paths and expected outputs, is in
`TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/README_MACOS_UE58.md`.
The ten gates that must actually pass, in order:

1. `TDD_GAME.uproject` opens in UE 5.8.
2. `TDD_GAME` module compiles for `Mac Development arm64`.
3. `/Game/TDD/Maps/PLAYABLE_FOREST_M1.umap` exists on disk under `Content/TDD/Maps/`.
4. `adanna_m1_technical_proxy_uv.glb` imports to `/Game/TDD/Imports` as a **Skeletal Mesh** with 21 bones and 5 animation sequences.
5. Meshes, materials, texture and collision are visible and functional in the editor.
6. The character is playable in the level.
7. PIE runs: walk, run, jump, land, camera collision, obstacle collision, interaction, route progress.
8. Cook completes.
9. A macOS `.app` packages for `arm64`.
10. The packaged app launches and is playable **without the editor**.

## 3. Evidence to return

Place in `ue_project/Saved/TDD_M1/Evidence/`; names are fixed so the results can be checked:

```
00_toolchain.txt      section 1 output
01_compile.log        Build.sh output, with exit code
02_setup.log          Tools/TDD_M1_Unreal_Setup_macOS.py output
tdd_m1_setup_report.json
03_cook.log
04_package.log
05_pie_video.mov      screen recording, PIE
06_package_video.mov  screen recording, packaged app
07_notes.md           anything that deviated
```

**No credentials, tokens, passwords or Apple developer account material.** Version strings,
paths, logs and recordings only.

## 4. What is already prepared, so you are not starting from zero

- `ue_project/TDD_GAME.uproject` — `EngineAssociation: 5.8`, Mac target, Python plugin enabled.
- `Source/*.Target.cs` — `BuildSettingsVersion.V7`, `EngineIncludeOrderVersion.Unreal5_8`, and
  **the same** `BuildSettingsVersion` in both files. That value is part of UBT's shared build
  environment; because this project links against the Launcher engine's precompiled
  `UnrealEditor`, a mismatch stops the build before compilation.
- `ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py` — creates and saves the project-owned map,
  repoints the map config, imports the three labelled technical files, writes a JSON report.
  Never overwrites existing assets. Has a dry-run switch.
- `ue_project/README_MACOS_UE58.md` — the full command sequence.
- `ue_project/Tools/tdd_m1_macos_audit.json` — 79/79 static compatibility checks.
- `model/adanna_m1_technical_proxy_uv.glb` — 33/33 local validation checks.

None of the above proves a compile, a PIE session, a cook, a package or a launch. Those remain
unverified until your machine produces the logs listed in section 3.
