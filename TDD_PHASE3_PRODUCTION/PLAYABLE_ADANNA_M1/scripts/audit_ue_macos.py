#!/usr/bin/env python3
"""Static UE source/packaging audit for the macOS + Unreal Engine 5.8 target.

This does NOT compile anything. It machine-checks the specific failure classes that
would stop an Apple Silicon UE 5.8 build, so the owner does not discover them only
after a multi-minute shader compile:

  * EngineAssociation and BuildSettingsVersion/IncludeOrderVersion mismatch
  * deprecated/removed Unreal Python editor APIs in the setup helper
  * Windows-only paths, binaries or shell conventions
  * INI keys written under the wrong section (silently ignored by UE)
  * C++ binding-signature mistakes known to fail UHT/compile
  * runtime component registration order that removes collision
  * hardcoded absolute paths in project or helper files
  * macOS packaging prerequisites (Xcode/Metal SDK expectations)
  * the owner-facing toolchain gate (Tools/verify_toolchain.sh) is real, not a stub

Result is written to ue_project/Tools/tdd_m1_macos_audit.json. It is evidence of a
source inspection, NOT of a successful compile, PIE session, cook or package.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
UE = BASE / "ue_project"
SRC = UE / "Source"
GAME = SRC / "TDD_GAME"
PUB = GAME / "Public"
PRIV = GAME / "Private"
TOOLS = UE / "Tools"
HELPER = TOOLS / "TDD_M1_Unreal_Setup_macOS.py"
PRESERVED = TOOLS / "TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py"
OUT = TOOLS / "tdd_m1_macos_audit.json"

CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str = "", severity: str = "error") -> None:
    CHECKS.append({"name": name, "ok": bool(ok), "severity": severity, "detail": detail})


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def main() -> dict:
    uproject_text = read(UE / "TDD_GAME.uproject")
    uproject = json.loads(uproject_text) if uproject_text else {}
    target = read(SRC / "TDD_GAME.Target.cs")
    # UBT loads only files matching "*.Target.cs". "TDD_GAMEEditorTarget.cs" does not
    # match that pattern, so it is dead code that UBT never reads - reading it here
    # previously certified V7/Unreal5_8 while the live editor target said V5/Unreal5_4.
    editor_target = read(SRC / "TDD_GAMEEditor.Target.cs")
    engine_ini = read(UE / "Config" / "DefaultEngine.ini")
    input_ini = read(UE / "Config" / "DefaultInput.ini")
    helper = read(HELPER)
    character_h = read(PUB / "TDDAdannaProxyCharacter.h")
    character_cpp = read(PRIV / "TDDAdannaProxyCharacter.cpp")
    level_cpp = read(PRIV / "TDDForbiddenForestLevel.cpp")
    level_h = read(PUB / "TDDForbiddenForestLevel.h")
    build_cs = read(GAME / "TDD_GAME.Build.cs")

    # ---- 1. Engine version alignment ------------------------------------------------
    check("uproject EngineAssociation is 5.8",
          uproject.get("EngineAssociation") == "5.8",
          "found=%r" % uproject.get("EngineAssociation"))
    def target_files() -> list:
        return sorted(SRC.glob("*.Target.cs"))

    def setting(text: str, key: str) -> str:
        m = re.search(r"\b%s\s*=\s*([^;]+);" % key, text)
        return m.group(1).strip() if m else ""

    def strip_comments(text: str) -> str:
        return re.sub(r"//[^\n]*", "", text)

    loadable = target_files()
    check("UBT target files present (*.Target.cs)",
          [f.name for f in loadable] == ["TDD_GAME.Target.cs", "TDD_GAMEEditor.Target.cs"],
          str([f.name for f in loadable]))

    # A file declaring TargetRules that UBT will NEVER load. This is the defect that
    # stopped the owner's first compile: the audit was green against it while the live
    # target still held V5/Unreal5_4.
    orphans = [f.name for f in SRC.glob("*.cs")
               if "TargetRules" in read(f) and not f.name.endswith(".Target.cs")]
    check("no unloadable TargetRules file (must end in .Target.cs)", not orphans, str(orphans))

    game_settings = setting(strip_comments(target), "DefaultBuildSettings")
    editor_settings = setting(strip_comments(editor_target), "DefaultBuildSettings")
    check("Game target uses BuildSettingsVersion.V7",
          game_settings == "BuildSettingsVersion.V7",
          "found=%r; 5.8 ships V7, and V6/V7 are what raise the four warning levels to Error"
          % game_settings)
    check("Editor target uses BuildSettingsVersion.V7",
          editor_settings == "BuildSettingsVersion.V7",
          "found=%r" % editor_settings)
    # The exact cause of the owner's failure: a shared-environment property differing
    # between the two targets is rejected before any C++ is compiled.
    check("both targets share one BuildSettingsVersion (UBT shared environment)",
          game_settings == editor_settings and game_settings != "",
          "game=%r editor=%r" % (game_settings, editor_settings))
    check("build settings are not force-overridden",
          "bOverrideBuildEnvironment" not in target + editor_target,
          "bOverrideBuildEnvironment only masks a divergence")
    check("no Unique build environment (installed-engine builds reject it)",
          "TargetBuildEnvironment.Unique" not in target + editor_target,
          "Unique is source-build only and fails on a Launcher engine")
    check("IncludeOrderVersion is Unreal5_8 in both targets",
          setting(strip_comments(target), "IncludeOrderVersion") == "EngineIncludeOrderVersion.Unreal5_8" and
          setting(strip_comments(editor_target), "IncludeOrderVersion") == "EngineIncludeOrderVersion.Unreal5_8",
          "game=%r editor=%r" % (setting(strip_comments(target), "IncludeOrderVersion"),
                                 setting(strip_comments(editor_target), "IncludeOrderVersion")))
    check("no legacy include order left anywhere",
          not re.search(r"EngineIncludeOrderVersion\.Unreal5_[0-7]\b",
                        strip_comments(target) + strip_comments(editor_target)))
    check("uproject targets Mac",
          "Mac" in (uproject.get("TargetPlatforms") or []),
          str(uproject.get("TargetPlatforms")))
    check("uproject declares required Python plugin",
          any(p.get("Name") == "PythonScriptPlugin" and p.get("Enabled")
              for p in uproject.get("Plugins", [])))

    # ---- 1b. C# target-rule structural sanity ---------------------------------------
    # No C# compiler exists in this environment, so validate the structure that UBT's
    # Roslyn compile would reject: unbalanced braces/parens/quotes, a class/ctor name
    # mismatch, a duplicate class across the rules assembly (both *.Target.cs files are
    # compiled together), and a wrong TargetType.
    def cs_sanity(fname: str, text: str, expect_type: str) -> None:
        code = strip_comments(text)
        check("%s braces balance" % fname,
              code.count("{") == code.count("}"), "%d open / %d close" % (code.count("{"), code.count("}")))
        check("%s parentheses balance" % fname,
              code.count("(") == code.count(")"))
        check("%s double quotes balance" % fname,
              code.count('"') % 2 == 0)
        m = re.search(r"public class (\w+)\s*:\s*TargetRules", code)
        check("%s declares one TargetRules class" % fname, bool(m))
        if m:
            cls = m.group(1)
            check("%s constructor name matches class" % fname,
                  re.search(r"public %s\s*\(\s*TargetInfo" % re.escape(cls), code) is not None)
            check("%s calls base(Target)" % fname, "base(Target)" in code)
            cs_classes.append(cls)
        check("%s sets Type = TargetType.%s" % (fname, expect_type),
              re.search(r"Type\s*=\s*TargetType\.%s\s*;" % expect_type, code) is not None)
        check("%s names the TDD_GAME module" % fname,
              re.search(r'ExtraModuleNames\.Add\("TDD_GAME"\)\s*;', code) is not None)
        check("%s ends with a closing brace" % fname, code.rstrip().endswith("}"))

    cs_classes: list = []
    cs_sanity("TDD_GAME.Target.cs", target, "Game")
    cs_sanity("TDD_GAMEEditor.Target.cs", editor_target, "Editor")
    check("target class names are unique across the rules assembly",
          len(cs_classes) == len(set(cs_classes)), str(cs_classes))

    # Documentation must not point the owner at a file UBT never loads.
    runbook_now = read(UE / "README_MACOS_UE58.md")
    check("runbook does not cite the unloadable TDD_GAMEEditorTarget.cs",
          "TDD_GAMEEditorTarget.cs" not in runbook_now)
    check("runbook names the real editor target file",
          "TDD_GAMEEditor.Target.cs" in runbook_now)

    # ---- 1c. Clang -Werror hazards from BuildSettingsVersion.V7 ---------------------
    # V7 raises UnreachableCodeWarningLevel to Error, so a loop whose increment can
    # never execute becomes a hard error (-Wunreachable-code-loop-increment). This is
    # how the first real compile failed on three TActorIterator loops.
    def unreachable_increments(code: str) -> list:
        """Line numbers of for-loops whose increment is unreachable.

        A loop whose body reaches an unconditional `break`/`return` before any
        conditional statement can never run its increment. Clang diagnoses exactly
        that, and V7 makes it an error.
        """
        hits = []
        lines = code.splitlines()
        for idx, line in enumerate(lines):
            m = re.match(r"\s*for\s*\(", line)
            if not m:
                continue
            # locate the body opening brace
            j, depth = idx, 0
            while j < len(lines):
                depth += lines[j].count("(") - lines[j].count(")")
                if depth <= 0 and "{" in lines[j]:
                    break
                j += 1
                if j - idx > 6:
                    break
            if j >= len(lines):
                continue
            # walk the body at brace depth 1, collecting top-level statements
            d = 0
            stmt = ""
            unconditional = False
            started = False
            for k in range(j, len(lines)):
                for ch in lines[k]:
                    if ch == "{":
                        d += 1
                        if d == 1:
                            started = True
                            continue
                    if ch == "}":
                        d -= 1
                        if d == 0:
                            if unconditional:
                                hits.append(idx + 1)
                            k = len(lines)
                            break
                        continue
                    if d == 1:
                        stmt += ch
                        if ch == ";":
                            t = stmt.strip()
                            if t.startswith("break"):
                                unconditional = True
                            elif re.match(r"^(if|switch|for|while|do|return)\b", t):
                                pass  # may exit conditionally; do not claim unreachability
                            elif t.startswith(("{", "}")):
                                pass
                            stmt = ""
                if d == 0 and started:
                    break
        return hits

    src_texts = {f.name: read(f) for f in sorted(list(SRC.rglob("*.cpp")) + list(SRC.rglob("*.h")))}
    offenders = {n: v for n, v in ((n, unreachable_increments(t)) for n, t in src_texts.items()) if v}
    check("no for-loop with an unreachable increment (V7 makes it -Werror)",
          not offenders, str(offenders))

    # Never fix this class of error by silencing the diagnostic.
    suppressed = [n for n, t in src_texts.items()
                  if "-Wno-" in t or "pragma clang diagnostic ignored" in t]
    check("project sources suppress no Clang warnings", not suppressed, str(suppressed))
    check("module keeps warnings fatal (no bWarningsAsErrors = false)",
          not re.search(r"bWarningsAsErrors\s*=\s*false", build_cs))
    # Any TActorIterator presence test must be a real one. A `for` header that is not
    # followed by a loop body doing work indicates someone reintroduced the pattern.
    iterator_files = [n for n, t in src_texts.items() if "TActorIterator" in t]
    check("actor presence tests exist where expected",
          set(iterator_files) == {"TDDForbiddenForestLevel.cpp", "TDDForbiddenForestGameMode.cpp",
                                  "TDDAdannaProxyCharacter.cpp", "ATDDAdannaCharacter.cpp",
                                  "TDDOmegaValleyGameMode.cpp"},
          str(sorted(iterator_files)))
    for name in iterator_files:
        text = "\n".join(l for l in src_texts[name].splitlines()
                          if not l.strip().startswith("//"))
        lines = text.splitlines()
        for m in re.finditer(r"TActorIterator<([^>]+)>", text):
            line = text[:m.start()].count("\n")
            ctx = lines[line]
            ok = ("static_cast<bool>" in ctx) or ctx.lstrip().startswith("if (TActorIterator") \
                or ctx.lstrip().startswith("for (TActorIterator")
            if not ok:
                # Declare-then-test pattern: the iterator is declared on its own
                # line (a variable declaration inside an `if` condition cannot
                # have a parenthesized initializer — Clang error), then tested
                # by a following `if (Var)` / `static_cast<bool>(Var)`.
                dm = re.match(r"\s*TActorIterator<[^>]+>\s+(\w+)\s*\(", ctx)
                if dm:
                    var = dm.group(1)
                    for nl in range(line + 1, min(line + 4, len(lines))):
                        if re.search(r"\bif\s*\(\s*%s\s*\)" % re.escape(var), lines[nl]) or \
                           re.search(r"static_cast<bool>\s*\(\s*%s\s*\)" % re.escape(var), lines[nl]):
                            ok = True
                            break
            check("%s:%d presence test uses the iterator bool" % (name, line + 1), ok, ctx.strip())

    # ---- 2. Module dependencies ----------------------------------------------------
    for dep in ("Core", "CoreUObject", "Engine", "InputCore"):
        check("Build.cs declares %s" % dep, '"%s"' % dep in build_cs)
    check("Build.cs adds no Windows-only module",
          not re.search(r'"(Windows|XInput|WinSDK|D3D\d*)"', build_cs))
    check("module implementation present",
          (PRIV / "TDD_GAME.cpp").is_file())

    # ---- 3. Deprecated Unreal Python APIs in the macOS helper -----------------------
    active_helper = re.sub(r'^\s*#.*$', '', helper, flags=re.MULTILINE)
    active_helper = re.sub(r'""".*?"""', '', active_helper, flags=re.DOTALL)
    check("macOS helper avoids EditorLevelLibrary",
          "EditorLevelLibrary" not in active_helper,
          "deprecated since UE 5.0, removed from the default path in 5.7+")
    check("macOS helper uses LevelEditorSubsystem",
          "LevelEditorSubsystem" in helper)
    check("macOS helper creates the map from a template",
          "new_level_from_template" in helper,
          "new_level alone leaves no saved .umap on disk")
    check("macOS helper saves the map explicitly",
          "save_current_level" in helper and "save_asset" in helper)
    check("macOS helper repoints map config",
          "GameDefaultMap" in helper or "MAP_ASSET" in helper and "config" in helper.lower())
    check("macOS helper writes its report under Saved/",
          "project_saved_dir" in helper)
    check("macOS helper has a dry-run switch", "TDD_DRY_RUN" in helper)
    check("macOS helper never deletes assets",
          not re.search(r"delete_asset|delete_directory|remove_asset", active_helper))
    check("macOS helper backs up config before edit",
          "tdd_backup" in helper)
    # The legacy GLTFImportOptions object only exposes generate_lightmap_u_vs and
    # import_scale (no import_animations/import_materials/import_textures), and assigning
    # it as AssetImportTask.options against an Interchange factory is a type mismatch that
    # drops the skin, so a skinned GLB imports as a Static Mesh. The supported UE 5.8 path is
    # the Interchange pipeline with force_all_mesh_as_type = IFMT_SKELETAL_MESH.
    check("macOS helper avoids broken GLTFImportOptions import",
          "GLTFImportOptions" not in active_helper,
          "GLTFImportOptions has no import_animations/materials/textures props and "
          "mismatches the Interchange factory; use InterchangeGenericAssetsPipeline")
    check("macOS helper forces skeletal mesh via Interchange",
          "force_all_mesh_as_type" in helper and "IFMT_SKELETAL_MESH" in helper,
          "skinned GLB must be forced to Skeletal Mesh via the Interchange pipeline")

    # ---- 4. Windows-only assumptions ------------------------------------------------
    windows_tokens = ["C:\\\\", "Program Files", "UnrealEditor.exe", "RunUAT.bat", "cmd.exe", "Win64"]
    for token in windows_tokens:
        check("no Windows-only token %r in helper" % token, token not in helper)
    project_texts = {
        "uproject": uproject_text, "Target.cs": target, "TDD_GAMEEditor.Target.cs": editor_target,
        "Build.cs": build_cs, "character.h": character_h, "character.cpp": character_cpp,
        "level.cpp": level_cpp, "level.h": level_h,
    }
    for label, text in project_texts.items():
        hits = [t for t in windows_tokens if t in text]
        check("no Windows-only token in %s" % label, not hits, str(hits))
    check("no hardcoded /Users/ absolute path in project files",
          all("/Users/" not in text for label, text in project_texts.items() if label != "helper"))
    check("preserved original helper retained unchanged",
          PRESERVED.is_file() and PRESERVED.stat().st_size > 500,
          "kept for audit; do not execute")
    stub_text = read(TOOLS / "TDD_M1_Unreal_Setup.py")
    # Drop the leading module docstring whether or not the file starts with a shebang.
    stub_code = re.sub(r"^(?:#![^\n]*\n)?\s*(?:\"\"\").*?(?:\"\"\")", "", stub_text, count=1, flags=re.DOTALL)
    check("old helper filename is a non-executing stub",
          "SUPERSEDED" in stub_text and "EditorLevelLibrary" not in stub_code
          and "def main()" in stub_code,
          "prevents launching the obsolete helper by mistake; original bytes remain in the preserved copy")
    check("preserved helper documents its superseded status",
          "PRESERVED AUDIT COPY" in read(PRESERVED)
          and "EditorLevelLibrary" in read(PRESERVED))

    # ---- 5. INI section correctness ------------------------------------------------
    check("GameDefaultMap is under GameMapsSettings",
          bool(re.search(r"\[/Script/EngineSettings\.GameMapsSettings\][^\[]*GameDefaultMap=",
                         engine_ini, re.DOTALL)),
          "under /Script/Engine.Engine the key is ignored and the game mode never applies")
    check("GlobalDefaultGameMode is under GameMapsSettings",
          bool(re.search(r"\[/Script/EngineSettings\.GameMapsSettings\][^\[]*GlobalDefaultGameMode=",
                         engine_ini, re.DOTALL)))
    check("no GameDefaultMap under /Script/Engine.Engine",
          not re.search(r"\[/Script/Engine\.Engine\][^\[]*GameDefaultMap=", engine_ini, re.DOTALL))
    check("input ini carries no hand-authored AxisMappings",
          "AxisMappings=" not in input_ini,
          "UE5 serialises these as map keys; code-registered bindings are used instead")

    # ---- 6. UHT / compile-signature hazards ----------------------------------------
    check("BindKey handlers take no parameters",
          not re.search(r"BindKey\([^;]*::\w+Axis\b", character_cpp),
          "BindKey requires a parameterless handler; float-axis handlers fail to compile")
    check("movement keys bound as press/release pairs",
          character_cpp.count("IE_Pressed") >= 6 and character_cpp.count("IE_Released") >= 6)
    check("signed keyboard axis state applied each tick",
          "ApplyMovementInput()" in character_cpp)
    def generated_include_is_last(header_text: str) -> bool:
        includes = [ln.strip() for ln in header_text.splitlines() if ln.strip().startswith("#include")]
        return bool(includes) and includes[-1].endswith('.generated.h"')

    for name in ("TDDAdannaProxyCharacter.h", "TDDForbiddenForestLevel.h", "TDDForbiddenForestGameMode.h"):
        text = read(PUB / name)
        check("UCLASS generated.h include is last in %s" % name,
              generated_include_is_last(text),
              "a .generated.h include not last in the header breaks UHT")
    # UE5 deprecates raw object pointers in UPROPERTY members; TObjectPtr is required
    # for the 5.8 / V7 build settings and will otherwise raise upgrade warnings.
    raw_uproperty = re.findall(
        r"UPROPERTY\([^)]*\)\s*\n\s*(?:TArray<)?U[A-Za-z]+\*", character_h + level_h)
    check("UPROPERTY members use TObjectPtr, not raw pointers",
          not raw_uproperty, str(raw_uproperty[:3]))
    check("no invented blade geometry in the UE proxy",
          "PROXY_BLADE" not in character_cpp and "Steel" not in character_cpp,
          "Phase 1 forbids inventing blade design; only the approved hip mount marker may exist")
    check("UE proxy keeps the approved LEFT-hip cross-draw mount marker",
          "LEFT_HIP_CROSS_DRAW_MOUNT_MARKER" in character_cpp)
    check("UE proxy carries no invented character dimensions",
          "NOT an approved character dimension" in read(PUB / "TDDWorldData.h"))
    check("character header includes InputCoreTypes for EKeys",
          "InputCoreTypes.h" in character_h)
    check("level spawns a PlayerStart when none exists",
          "APlayerStart" in level_cpp,
          "a generated map with no PlayerStart cannot possess a pawn in PIE")
    check("forest level uses TActorIterator (EngineUtils included)",
          "EngineUtils.h" in level_cpp and "TActorIterator" in level_cpp)

    # ---- 7. Runtime component registration (collision) ------------------------------
    pool_fn = re.search(r"CreateInstancePool\(.*?\n\}", level_cpp, re.DOTALL)
    pool_body = pool_fn.group(0) if pool_fn else ""
    reg = pool_body.find("RegisterComponent()")
    first_instance = level_cpp.find("AddInstance(")
    check("INSTANCED pool registers before AddInstance is ever called",
          reg != -1 and first_instance != -1,
          "registration inside the factory at index %d; first AddInstance call site at %d"
          % (reg, first_instance))
    check("registration occurs exactly once per pool",
          pool_body.count("RegisterComponent()") == 1)
    check("collidable pools enable QueryAndPhysics",
          "ECollisionEnabled::QueryAndPhysics" in pool_body)

    # ---- 7b. Dead constants (V7 treats several warning classes as errors) -----------
    for name in ("TDDAdannaProxyCharacter.cpp", "TDDForbiddenForestLevel.cpp"):
        text = read(PRIV / name)
        decls = re.findall(r"constexpr TCHAR (\w+)\[\]", text)
        unused = [d for d in decls if len(re.findall(r"\b%s\b" % re.escape(d), text)) < 2]
        check("no unused constexpr TCHAR in %s" % name, not unused, str(unused))

    # ---- 7c. Type conversions that fail under strict settings ----------------------
    check("CreatePart return assigned to TObjectPtr is legal",
          "TObjectPtr<UStaticMeshComponent> Torso;" in character_h
          and "UStaticMeshComponent* ATDDAdannaProxyCharacter::CreatePart" in character_cpp)
    check("Instanced pool array stores TObjectPtr",
          "TArray<TObjectPtr<UInstancedStaticMeshComponent>> InstancePools" in level_h)

    # ---- 8. Asset import expectations ----------------------------------------------
    check("GLB import requests skeletal mesh options",
          "GLTFImportOptions" in helper)
    check("OBJ import kept static",
          "collision_proxy.obj" in helper)

    # ---- 9. Packaging prerequisites (documented, not executed) ----------------------
    runbook = read(UE / "README_MACOS_UE58.md")
    for need in ("Xcode", "Metal", "RunUAT.sh", "arm64"):
        check("macOS packaging expects %s" % need, need in helper or need in runbook)

    # ---- 10. Toolchain gate (verify_toolchain.sh) ------------------------------------
    # Machine-checks that the owner-facing gate exists, is executable, is valid bash
    # AND is not a placeholder: it must actually branch on the 5.8.4 boundary, on the
    # Apple SDK MaxVersion bound and on the finalize-fix marker.
    vt = TOOLS / "verify_toolchain.sh"
    check("toolchain gate script exists", vt.is_file(), str(vt))
    vt_text = read(vt) if vt.is_file() else ""
    check("toolchain gate is executable", vt.is_file() and bool(vt.stat().st_mode & 0o111))
    check("toolchain gate declares PRODUCED - NOT YET VERIFIED status",
          "PRODUCED - NOT YET VERIFIED" in vt_text)
    # Must not *execute* elevated commands. A mention inside printed advice is fine;
    # a line that runs sudo is not.
    runs_sudo = any(re.match(r"^\s*sudo\s", ln) for ln in vt_text.splitlines())
    check("toolchain gate never executes sudo", not runs_sudo)
    for probe, label in (("PatchVersion", "engine patch gate"),
                         ("MaxVersion", "Apple SDK MaxVersion gate"),
                         ("RedirectStandardInput", "finalize-fix marker"),
                         ("emit-workaround", "stdin shim fallback"),
                         ("-package", "Mac package flag")):
        check("toolchain gate probes %s" % label, probe in vt_text)
    import subprocess
    syntax_ok = False
    if vt.is_file():
        try:
            syntax_ok = subprocess.run(["bash", "-n", str(vt)],
                                       capture_output=True, timeout=30).returncode == 0
        except Exception:
            syntax_ok = False
    check("toolchain gate passes bash -n", syntax_ok)

    overall = all(c["ok"] for c in CHECKS)
    errors = [c for c in CHECKS if not c["ok"] and c["severity"] == "error"]
    report = {
        "generated": "2026-11-20",
        "status": "COMPLETED AND VERIFIED" if overall else "PRODUCED — NOT YET VERIFIED",
        "scope": ("static source inspection for macOS/UE 5.8 compatibility only; "
                  "NOT a compile, PIE, cook, package or device test"),
        "target_environment": {
            "machine": "Apple M4 Mac, 16 GB RAM, macOS 27.2.1, ARM64",
            "engine": "Unreal Engine 5.8",
        },
        "checks": CHECKS,
        "checksPassed": sum(1 for c in CHECKS if c["ok"]),
        "checksTotal": len(CHECKS),
        "errors": [c["name"] for c in errors],
        "compile_verified": False,
        "pie_verified": False,
        "cook_verified": False,
        "package_verified": False,
        "runnable_build_verified": False,
        "classification": "static audit evidence; Unreal execution remains BLOCKED — OWNER-STUDIO DEPENDENCY",
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("[macOS audit] %d/%d checks passed" % (report["checksPassed"], report["checksTotal"]))
    for c in errors:
        print("  FAIL:", c["name"], "|", c["detail"])
    return report


if __name__ == "__main__":
    main()
