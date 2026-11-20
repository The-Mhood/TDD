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

# Engine-subsystem header guard: UE subsystem headers live under Subsystems/*.h.
# In UE 5.8 both UWorldSubsystem and UTickableWorldSubsystem are defined in
# Subsystems/WorldSubsystem.h; the separate Subsystems/TickableWorldSubsystem.h
# header of the UE 5.0-5.6 era no longer exists, so including it is a fatal
# 'file not found' compile error (the UE 5.8.4 API docs list both classes under
# Subsystems/WorldSubsystem.h). This guard catches removed/invalid engine
# header paths before UBT so the owner's Mac build is not wasted.
# Maps a header that no longer exists in UE 5.8.4 to its replacement.
REMOVED_ENGINE_HEADERS = {
    "Subsystems/TickableWorldSubsystem.h": "Subsystems/WorldSubsystem.h",
}

# Subsystem headers verified to exist in UE 5.8.4 under
# Engine/Source/Runtime/Engine/Public/Subsystems/ (per the official UE 5.8 API
# documentation). Headers outside this set are flagged for verification
# rather than assumed valid or invalid.
KNOWN_ENGINE_SUBSYSTEM_HEADERS = (
    "Subsystems/EngineSubsystem.h",
    "Subsystems/GameInstanceSubsystem.h",
    "Subsystems/WorldSubsystem.h",
    "Subsystems/LocalPlayerSubsystem.h",
)

# Subsystem base class -> the header that defines it in UE 5.8.4. A file using
# the base class (as a base, or in code) must include that header.
SUBSYSTEM_BASE_INCLUDE_RULES = [
    (r"\bUTickableWorldSubsystem\b", "Subsystems/WorldSubsystem.h"),
    (r"\bUWorldSubsystem\b", "Subsystems/WorldSubsystem.h"),
    (r"\bUEngineSubsystem\b", "Subsystems/EngineSubsystem.h"),
    (r"\bUGameInstanceSubsystem\b", "Subsystems/GameInstanceSubsystem.h"),
    (r"\bULocalPlayerSubsystem\b", "Subsystems/LocalPlayerSubsystem.h"),
]

# UHT private Blueprint-access guard: UHT rejects Blueprint visibility
# specifiers on private members unless meta=(AllowPrivateAccess="true") is
# present (e.g. "BlueprintReadOnly should not be used on private members").
# C++ default access applies: a `class` body defaults to private, a `struct`
# body to public. Catches this UHT error class before the Mac build.
BLUEPRINT_SPECIFIERS = (
    "BlueprintReadOnly",
    "BlueprintCallable",
    "BlueprintPure",
    "BlueprintImplementableEvent",
    "BlueprintNativeEvent",
    "BlueprintEditable",
    "BlueprintGetProperty",
    "BlueprintSetProperty",
)


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

    # ---- engine subsystem header guard ------------------------------------
    # Scan every .h and .cpp in the project for UE engine subsystem header
    # includes. (1) A header that no longer exists in UE 5.8.4 is a hard
    # blocker with its replacement. (2) A subsystem base class used in a file
    # requires that file to include the header defining the class. (3) A
    # Subsystems/*.h include outside the verified set is flagged for
    # verification against the installed engine source.
    if src.is_dir():
        for header_file in sorted(list(src.rglob("*.h")) + list(src.rglob("*.cpp"))):
            try:
                text = header_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = header_file.relative_to(root)
            for inc in re.findall(r'#include\s+"((?:[^"\\]|\\.)*Subsystems/[^"\\]+\.h)"', text):
                if inc in REMOVED_ENGINE_HEADERS:
                    block(f"{rel}: #include \"{inc}\" no longer exists in UE 5.8.4",
                          f"use #include \"{REMOVED_ENGINE_HEADERS[inc]}\" instead; "
                          f"in UE 5.8 UTickableWorldSubsystem is defined in WorldSubsystem.h")
                elif inc not in KNOWN_ENGINE_SUBSYSTEM_HEADERS:
                    warn(f"{rel}: #include \"{inc}\" is not a verified UE 5.8.4 subsystem header",
                         "confirm the header exists under Engine/Source/Runtime/Engine/Public/Subsystems/ "
                         "in the installed engine before building")
            for pattern, header in SUBSYSTEM_BASE_INCLUDE_RULES:
                if re.search(pattern, text) and f'"{header}"' not in text:
                    block(
                        f"{rel}: uses {re.search(pattern, text).group(0)} but does not include \"{header}\"",
                        f"add #include \"{header}\" to {rel}; the class is defined there in UE 5.8.4")

    # ---- UHT-generated-constructor member guard ---------------------------
    # UHT emits a default constructor for every UCLASS in the .gen.cpp (with
    # only `: Super()` in its mem-init list). A data member whose type has NO
    # usable default constructor must therefore be initialized by a default
    # member initializer (NSDMI) at its declaration. A mem-init list in the
    # user constructor is NOT sufficient: the UHT-generated constructor has no
    # such entry and fails to compile. "Usable default constructor" = a ctor
    # callable with zero arguments (empty parameter list, or every parameter
    # defaulted); a deleted ctor does not count.
    def _class_bodies(text):
        """Yield (class_name, body) for each class/struct definition in text."""
        for m in re.finditer(r"\b(?:class|struct)\s+(?:\w+\s+)?(\w+)\s*(?::[^;{]*)?\{", text):
            name = m.group(1)
            i = m.end() - 1
            depth = 0
            for j in range(i, len(text)):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
            yield name, text[i:j]

    # Map of project-defined types -> has a usable default constructor.
    type_default_ctor = {}
    if src.is_dir():
        for hdr in sorted(src.rglob("*.h")):
            try:
                htext = hdr.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for name, body in _class_bodies(htext):
                has_user_ctor = False
                zero_callable = False
                for cm in re.finditer(r"\b" + re.escape(name) + r"\s*\(([^)]*)\)([^;{]*)", body):
                    params = cm.group(1).strip()
                    tail = cm.group(2)
                    if "= delete" in tail:
                        continue
                    has_user_ctor = True
                    if params == "" or all("=" in p for p in params.split(",")):
                        zero_callable = True
                # A type with no user-declared ctor has an implicit default ctor.
                type_default_ctor[name] = (not has_user_ctor) or zero_callable

    if src.is_dir():
        for hdr in sorted(src.rglob("*.h")):
            try:
                htext = hdr.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = hdr.relative_to(root)
            for cname, body in _class_bodies(htext):
                if "GENERATED_BODY" not in body:
                    continue
                for m in re.finditer(
                        r"^\s*(?:UPROPERTY(?:\([^)]*\))?\s*)?"
                        r"([A-Za-z_][\w:<>,*&\s]*?)\s+([A-Za-z_]\w*)\s*(\[[^\]]*\])?\s*(=[^;]*)?;",
                        body, re.M):
                    member_type, member_name, _arr, init = (m.group(1), m.group(2), m.group(3), m.group(4))
                    if init or "(" in body[m.start():m.end()]:
                        continue
                    base = member_type.split("::")[-1].split("<")[0].strip().strip("*&")
                    if base in type_default_ctor and not type_default_ctor[base]:
                        block(
                            f"{rel}: UCLASS {cname} member '{member_name}' of type {base} has no "
                            f"usable default constructor and no default member initializer",
                            f"initialize it at the declaration, e.g. '{base} {member_name} = {base}(...)'; "
                            f"a mem-init list in the user constructor is not enough because UHT "
                            f"also generates a default constructor")

    # ---- UHT private Blueprint-access guard -----------------------------
    # Scan every header: track the current access section (public:/private:/
    # protected:, with C++ default access per class/struct body) and block any
    # UPROPERTY/UFUNCTION carrying a Blueprint visibility specifier while in a
    # private section without AllowPrivateAccess metadata.
    if src.is_dir():
        for hdr in sorted(src.rglob("*.h")):
            try:
                htext = hdr.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = hdr.relative_to(root)
            events = []
            for m in re.finditer(r"(?m)^\s*(public|private|protected)\s*:", htext):
                events.append((m.start(), "access", m.group(1)))
            for m in re.finditer(r"\b(class|struct)\s+[^;{]*\{", htext):
                # Skip `enum class`/`enum struct` declarations: the keyword is
                # not opening a type body, so it must not flip access tracking.
                if re.search(r"enum\s*$", htext[:m.start()]):
                    continue
                events.append((m.start(), "open", m.group(1)))
            for m in re.finditer(r"\b(UPROPERTY|UFUNCTION)\s*\(", htext):
                end = htext.find(";", m.end())
                if end == -1:
                    continue
                events.append((m.start(), "member", htext[m.start():end]))
            events.sort(key=lambda e: e[0])
            current_access = "public"
            for _pos, kind, payload in events:
                if kind == "open":
                    current_access = "private" if payload == "class" else "public"
                elif kind == "access":
                    current_access = payload
                elif kind == "member" and current_access == "private":
                    if any(s in payload for s in BLUEPRINT_SPECIFIERS) and "AllowPrivateAccess" not in payload:
                        block(
                            f"{rel}: UHT error class — private member with a Blueprint visibility "
                            f"specifier and no AllowPrivateAccess metadata",
                            f"add meta=(AllowPrivateAccess=\"true\") to the member's "
                            f"UPROPERTY/UFUNCTION in {rel} (keep the member private), or move it "
                            f"to a public section; UHT rejects Blueprint specifiers on private members")

    # ---- UHT enum reflection guard ---------------------------------------
    # UHT can only reflect enums declared with UENUM. A UPROPERTY or UFUNCTION
    # signature that uses a plain C++ enum (no UENUM) fails with "Unable to
    # find 'class', 'delegate', 'enum', or 'struct' with name '<Enum>'".
    # Scan every header: collect plain (non-UENUM) enum names, then block any
    # UPROPERTY/UFUNCTION whose declaration text (type, return type or
    # parameters) uses such an enum.
    if src.is_dir():
        header_texts = {}
        for hdr in sorted(src.rglob("*.h")):
            try:
                header_texts[hdr.relative_to(root)] = hdr.read_text(
                    encoding="utf-8", errors="replace")
            except OSError:
                continue
        plain_enums = set()
        for rel, htext in header_texts.items():
            for m in re.finditer(r"(?m)^\s*enum(?:\s+class)?\s+(\w+)", htext):
                prefix = htext[:m.start()]
                last = max(prefix.rfind(";"), prefix.rfind("}"))
                window = prefix[last:] if last != -1 else prefix
                if not re.search(r"UENUM\s*\(", window):
                    plain_enums.add(m.group(1))
        for rel, htext in header_texts.items():
            for m in re.finditer(r"\b(?:UPROPERTY|UFUNCTION)\s*\(", htext):
                open_idx = htext.find("(", m.start())
                # Find the closing paren of the specifier list, depth-aware.
                depth = 0
                close_idx = open_idx
                while close_idx < len(htext):
                    if htext[close_idx] == "(":
                        depth += 1
                    elif htext[close_idx] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    close_idx += 1
                if depth != 0:
                    continue
                after = htext[close_idx + 1:]
                ends = [i for i in (after.find(";"), after.find("{")) if i != -1]
                sig = after[:min(ends) if ends else len(after)]
                for name in sorted(plain_enums):
                    if re.search(r"\b" + re.escape(name) + r"\b", sig):
                        line = htext[:m.start()].count("\n") + 1
                        block(
                            f"{rel}:{line}: UHT error class — UPROPERTY/UFUNCTION uses plain "
                            f"enum '{name}' which UHT cannot reflect",
                            f"add UENUM(BlueprintType) to the '{name}' enum declaration in "
                            f"{rel} before its reflected use (keep the underlying type and "
                            f"existing behaviour; do not remove reflection)")

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
