#!/usr/bin/env python3
"""Static pre-UBT readiness check for a canonical Unreal project tree.

Runs BEFORE UnrealBuildTool, on any layout (it does not assume a module graph).
It reports the failures that UBT or the linker would hit, with the exact file to
fix, so the first build on the owner's Mac is not wasted on avoidable errors.

Usage:  python3 Tools/engine/build_readiness.py [project-dir] [--platform mac|win]

Exit 0 = no blocking finding.   1 = at least one blocking finding.
It never builds anything and never claims a build.
"""

import argparse
import json
import pathlib
import re
import sys

EDITOR_ONLY_DEP_PREFIXES = ("UnrealEd", "UnrealEd", "EditorStyle", "ToolMenus", "DetailCustomizations",
                            "EditorFramework", "PropertyEditor", "AssetTools", "DataValidation",
                            "EditorScriptingUtilities", "PlacementMode", "ClassViewer", "GraphEditor")

# IWYU guard: a .cpp that uses a UE component (by type name or by calling an
# accessor that returns a component pointer) must include that component's
# header directly. A missing include yields an incomplete-type compile error
# (e.g. SetupAttachment(GetCapsuleComponent()) with only a forward declaration).
# This static check catches it before UBT so the owner's Mac build is not wasted.
# Each rule: (regex matching usage in a .cpp, required include header).
COMPONENT_INCLUDE_RULES = [
    (r"\bUCapsuleComponent\b", "Components/CapsuleComponent.h"),
    (r"GetCapsuleComponent\s*\(", "Components/CapsuleComponent.h"),
    (r"\bUStaticMeshComponent\b", "Components/StaticMeshComponent.h"),
    (r"\bUSceneComponent\b", "Components/SceneComponent.h"),
    (r"\bUSpringArmComponent\b", "GameFramework/SpringArmComponent.h"),
    (r"\bUCameraComponent\b", "Camera/CameraComponent.h"),
    (r"\bUCharacterMovementComponent\b", "GameFramework/CharacterMovementComponent.h"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--platform", default="mac", choices=["mac", "win"])
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    blockers, warnings, notes = [], [], []

    def block(msg, fix=""):
        blockers.append((msg, fix))

    def warn(msg, fix=""):
        warnings.append((msg, fix))

    # ---- descriptor
    descriptors = sorted(root.glob("*.uproject"))
    if not descriptors:
        print(f"BLOCKER  no .uproject in {root}")
        print("FIX      the canonical descriptor must exist at the repository root before any build")
        return 1
    if len(descriptors) > 1:
        block(f"{len(descriptors)} descriptors at the root: {[d.name for d in descriptors]}",
              "exactly one .uproject may exist; delete or move the others")
    uproject = descriptors[0]
    try:
        project = json.loads(uproject.read_text(encoding="utf-8"))
        notes.append(f"descriptor {uproject.name} parses")
    except json.JSONDecodeError as exc:
        block(f"{uproject.name} is not valid JSON: {exc}", "fix the JSON before running UBT")
        return report(blockers, warnings, notes)

    assoc = project.get("EngineAssociation")
    if assoc != "5.8":
        block(f"EngineAssociation is {assoc!r}, expected '5.8'",
              "set it to the installed engine; a mismatch makes the launcher open the wrong engine")

    platforms = [p.lower() for p in project.get("TargetPlatforms", [])]
    if args.platform == "mac" and "mac" not in platforms:
        warn(f"TargetPlatforms {project.get('TargetPlatforms')} does not list Mac",
             'add "Mac" to TargetPlatforms (macOS is the initial development platform)')

    # ---- modules
    modules = project.get("Modules", [])
    if not modules:
        block("descriptor declares no modules", "add at least the primary game module")
    src = root / "Source"
    module_names = {m.get("Name") for m in modules}
    module_deps = {}  # module -> project modules it names in its Build.cs
    for entry in modules:
        name = entry.get("Name")
        mtype = entry.get("Type")
        phase = entry.get("LoadingPhase")
        mdir = src / name
        build_cs = mdir / f"{name}.Build.cs"
        if not mdir.is_dir():
            block(f"module {name}: directory Source/{name} missing",
                  f"create Source/{name}/{name}.Build.cs and an implementation .cpp")
            continue
        if not build_cs.is_file():
            block(f"module {name}: Build.cs missing", f"create Source/{name}/{name}.Build.cs")
            continue
        tusp = [p for p in mdir.rglob("*.cpp")
                if re.search(r"IMPLEMENT_(PRIMARY_GAME_MODULE|MODULE)\s*\(", p.read_text(encoding="utf-8", errors="ignore"))]
        if not tusp:
            block(f"module {name}: declared in {uproject.name} but has no IMPLEMENT_MODULE translation unit",
                  f"create Source/{name}/Private/{name}Module.cpp containing "
                  f"IMPLEMENT_MODULE(FDefaultModuleImpl, {name}); without it the link fails")

        text = build_cs.read_text(encoding="utf-8")
        pub = set(re.findall(r'"([A-Za-z0-9_]+)"', " ".join(
            re.findall(r"PublicDependencyModuleNames\s*\.AddRange\s*\((.*?)\)", text, re.S))))
        prv = set(re.findall(r'"([A-Za-z0-9_]+)"', " ".join(
            re.findall(r"PrivateDependencyModuleNames\s*\.AddRange\s*\((.*?)\)", text, re.S))))
        module_deps[name] = {d for d in pub | prv if d in module_names}
        editor_deps = {d for d in pub | prv if d.startswith(EDITOR_ONLY_DEP_PREFIXES)}
        if mtype == "Runtime" and editor_deps:
            block(f"module {name}: Type Runtime but depends on editor-only {sorted(editor_deps)}",
                  "either change the module to Type Editor (and Editor target) or remove those dependencies; "
                  "a Runtime module cannot link into a Game target with UnrealEd in it")
        if name.endswith("Tests") and mtype == "Runtime" and phase == "PostEngineInit":
            warn(f"module {name}: Type Runtime, LoadingPhase PostEngineInit — it will load in a packaged game",
                 "test modules are normally Type Editor so they exist only in the editor target")

    # ---- IWYU component-include guard -------------------------------------
    # Scan every .cpp in the project for UE component usage (type name or
    # accessor call) and verify the matching header is included directly.
    # Catches incomplete-type compile errors before UBT runs on the owner's Mac.
    if src.is_dir():
        for cpp in sorted(src.rglob("*.cpp")):
            try:
                text = cpp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = cpp.relative_to(root)
            for pattern, header in COMPONENT_INCLUDE_RULES:
                if re.search(pattern, text) and f'"{header}"' not in text:
                    block(
                        f"{rel}: uses a UE component (pattern {pattern}) without "
                        f'#include \"{header}\"',
                        f"add #include \"{header}\" to {rel}; a missing include "
                        f"causes an incomplete-type compile error")

    # ---- targets
    target_files = sorted(src.glob("*.Target.cs")) if src.is_dir() else []
    if not target_files:
        block("no *.Target.cs under Source/", "add <Project>.Target.cs and <Project>Editor.Target.cs")
    names = [t.name.replace(".Target.cs", "") for t in target_files]
    for want in ("", "Editor"):
        pass
    targets_text = {t.name: t.read_text(encoding="utf-8") for t in target_files}
    for tname, text in targets_text.items():
        inc = re.search(r"IncludeOrderVersion\s*=\s*([A-Za-z0-9_.]+)", text)
        bs = re.search(r"DefaultBuildSettings\s*=\s*([A-Za-z0-9_.]+)", text)
        # both ExtraModuleNames.Add("X") and ExtraModuleNames.AddRange(new string[] { "X", ... })
        extra = []
        for call in re.finditer(r"ExtraModuleNames\s*\.\s*Add(?:Range)?\s*\(([^;]*?)\)\s*;", text, re.S):
            extra += re.findall(r'"([A-Za-z0-9_]+)"', call.group(1))
        notes.append(f"{tname}: build settings {bs.group(1) if bs else 'unset'}, "
                     f"include order {inc.group(1) if inc else 'unset'}, modules {extra}")
        if inc and re.search(r"Unreal5_(\d+)", inc.group(1)):
            pinned = int(re.search(r"Unreal5_(\d+)", inc.group(1)).group(1))
            if assoc and assoc.startswith("5.") and pinned != int(assoc.split(".")[1]):
                block(f"{tname}: IncludeOrderVersion pins 5.{pinned} while the project targets {assoc}",
                      "use EngineIncludeOrderVersion.Latest until a verified build pins an explicit value")
        # A module satisfies the target if it is listed, or if it is reachable
        # through Build.cs dependencies from a listed module (UBT links that closure);
        # only modules with no such route must be added explicitly.
        reachable, frontier = set(extra), list(extra)
        while frontier:
            cur = frontier.pop()
            for dep in module_deps.get(cur) or ():
                if dep not in reachable:
                    reachable.add(dep)
                    frontier.append(dep)
        missing = [m.get("Name") for m in modules
                   if m.get("Type") == ("Editor" if "Editor" in tname else "Runtime")
                   and m.get("Name") not in reachable]
        if missing:
            block(f"{tname}: ExtraModuleNames omits {missing}",
                  "add every module of that type to the matching target's ExtraModuleNames")

    # ---- config and ignores
    if not (root / "Config" / "DefaultEngine.ini").is_file():
        warn("Config/DefaultEngine.ini missing", "the project will boot with engine defaults; add the ini baseline")
    gi = root / ".gitignore"
    if gi.is_file():
        text = gi.read_text(encoding="utf-8")
        for pattern in ("Binaries/", "Intermediate/", "Saved/", "DerivedDataCache/"):
            if pattern not in text:
                warn(f".gitignore does not exclude {pattern}", "build output must never be committed")
    else:
        warn(".gitignore missing", "Binaries/, Intermediate/, Saved/, DerivedDataCache/ must be ignored")

    return report(blockers, warnings, notes)


def report(blockers, warnings, notes):
    for msg, fix in blockers:
        print(f"BLOCKER  {msg}")
        if fix:
            print(f"FIX      {fix}")
    for msg, fix in warnings:
        print(f"WARNING  {msg}")
        if fix:
            print(f"FIX      {fix}")
    for note in notes:
        print(f"note     {note}")
    print()
    print(f"  {len(blockers)} blocker(s), {len(warnings)} warning(s). Static check only: nothing was built.")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
