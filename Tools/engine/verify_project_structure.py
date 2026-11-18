#!/usr/bin/env python3
"""Static verification of the TDD Unreal project skeleton.

Checks the things a machine without Unreal Engine *can* check: that the descriptor
parses, that every declared module exists with its Build.cs and an implementation
translation unit, that the targets and config exist, that the automation-test
foundation is present, and that the module dependency graph obeys MEAD 3.2
(downward-only, TDDCore a leaf, nothing depends on the editor or test modules).

It does NOT compile anything and does NOT verify Unreal API correctness.
Exit 0 only if every check passes.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
UPROJECT = ROOT / "TDD.uproject"

# MEAD 3.2: modules a given module may depend on (project modules only).
ALLOWED = {
    "TDDCore": set(),
    "TDDWorld": {"TDDCore"},
    "TDDGameplay": {"TDDCore", "TDDWorld"},
    "TDDAI": {"TDDCore", "TDDWorld", "TDDGameplay"},
    "TDDNarrative": {"TDDCore", "TDDWorld"},
    "TDDUI": {"TDDCore", "TDDWorld"},
    "TDDEditor": {"TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI"},
    "TDDTests": {"TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI"},
    "TDD": {"TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI"},
}
EDITOR_ONLY = {"TDDEditor", "TDDTests"}

results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))


def project_deps(build_cs):
    text = build_cs.read_text(encoding="utf-8")
    names = set()
    for block in re.findall(r"PublicDependencyModuleNames\s*\.AddRange\s*\((.*?)\)", text, re.S):
        names |= set(re.findall(r'"([A-Za-z0-9_]+)"', block))
    for name in re.findall(r"PublicDependencyModuleNames\s*\.Add\s*\(\s*\"([A-Za-z0-9_]+)\"", text):
        names.add(name)
    return names


def main():
    if not UPROJECT.is_file():
        check("TDD.uproject exists", False, str(UPROJECT))
        return report()

    try:
        data = json.loads(UPROJECT.read_text(encoding="utf-8"))
        check("TDD.uproject is valid JSON", True)
    except json.JSONDecodeError as exc:
        check("TDD.uproject is valid JSON", False, str(exc))
        return report()

    check("EngineAssociation is the ADR-0001 pin", data.get("EngineAssociation") == "5.8",
          str(data.get("EngineAssociation")))

    modules = data.get("Modules", [])
    names = [m.get("Name") for m in modules]
    check("descriptor declares 9 modules (MEAD 3.2)", len(modules) == 9, ", ".join(names))
    check("every declared module has a unique name", len(set(names)) == len(names))

    for name in names:
        mdir = ROOT / "Source" / name
        build_cs = mdir / f"{name}.Build.cs"
        check(f"{name}: Build.cs present", build_cs.is_file())
        check(f"{name}: declares its ModuleRules class", build_cs.is_file() and
              f"public class {name} : ModuleRules" in build_cs.read_text(encoding="utf-8"))
        impls = list(mdir.rglob("*.cpp"))
        has_impl = any(("IMPLEMENT_MODULE" in p.read_text(encoding="utf-8")) or
                       ("IMPLEMENT_PRIMARY_GAME_MODULE" in p.read_text(encoding="utf-8"))
                       for p in impls)
        check(f"{name}: has a module implementation", has_impl, f"{len(impls)} .cpp file(s)")
        if build_cs.is_file():
            # policy comparison is over *project* modules only: engine/plugin modules are
            # not part of the MEAD 3.2 graph and must not read as violations
            deps = project_deps(build_cs) & set(ALLOWED)
            if name not in ALLOWED:
                # A module this verifier has no rule for: report it rather than guessing a
                # policy for it. This keeps the tool usable on a tree authored elsewhere
                # (e.g. when reconciling two foundations), where the graph may differ.
                check(f"{name}: module is in this verifier's declared graph", False,
                      "unknown module - no MEAD 3.2 rule on file for it")
            else:
                extra = deps - ALLOWED[name]
                check(f"{name}: dependencies obey MEAD 3.2", not extra,
                      f"undeclared upward edge(s): {sorted(extra)}" if extra else "")

    for target in ("TDD.Target.cs", "TDDEditor.Target.cs"):
        path = ROOT / "Source" / target
        check(f"{target} present", path.is_file())

    for cfg in ("DefaultEngine.ini", "DefaultGame.ini", "DefaultInput.ini"):
        check(f"Config/{cfg} present", (ROOT / "Config" / cfg).is_file())

    test_cpp = ROOT / "Source" / "TDDCore" / "Private" / "Tests" / "TDDEnginePinTest.cpp"
    check("automation-test foundation present", test_cpp.is_file())
    if test_cpp.is_file():
        text = test_cpp.read_text(encoding="utf-8")
        check("test is guarded by WITH_DEV_AUTOMATION_TESTS", "#if WITH_DEV_AUTOMATION_TESTS" in text)
        check("test declares an IMPLEMENT_SIMPLE_AUTOMATION_TEST", "IMPLEMENT_SIMPLE_AUTOMATION_TEST" in text)
        check("test uses the TDD-Unit.* naming (MEAD 15)", '"TDD-Unit.' in text)

    # nothing may depend on an editor-only module
    for name in names:
        build_cs = ROOT / "Source" / name / f"{name}.Build.cs"
        if build_cs.is_file():
            bad = project_deps(build_cs) & EDITOR_ONLY
            check(f"{name}: does not depend on an Editor-only module", not bad, str(sorted(bad)) if bad else "")

    return report()


def report():
    failures = [r for r in results if not r[0]]
    for ok, name, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    print()
    print(f"  {len(results) - len(failures)}/{len(results)} structural checks passed")
    print("  Scope: descriptor, module graph, targets, config, test foundation. No compile was performed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
