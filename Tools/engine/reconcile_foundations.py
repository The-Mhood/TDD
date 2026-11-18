#!/usr/bin/env python3
"""Compare two Unreal project trees mechanically, for reconciliation between branches.

Usage:
    python3 Tools/engine/reconcile_foundations.py <tree-a> <tree-b> [--json out.json]

Reads each tree's .uproject, module Build.cs files, target rules, config inventory,
automation-test sources, documentation root and ADR identifiers, and prints a
section-by-section comparison. It never writes to either tree.

It does NOT compile, open or run anything, and it does not judge which side is
correct: it lists where the two differ, and which module declarations have no
implementation translation unit (a link-time failure the descriptor alone hides).
"""

import argparse
import json
import pathlib
import re
import sys

PROJECT_FILE = "TDD.uproject"


def load_tree(root):
    root = pathlib.Path(root).resolve()
    data = {"root": str(root)}
    uproject = root / PROJECT_FILE
    if not uproject.is_file():
        data["error"] = f"{PROJECT_FILE} not found"
        return data
    try:
        project = json.loads(uproject.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        data["error"] = f"invalid JSON: {exc}"
        return data

    data["engine_association"] = project.get("EngineAssociation")
    data["target_platforms"] = project.get("TargetPlatforms")
    data["plugins"] = sorted(p.get("Name", "?") for p in project.get("Plugins", []))

    modules = {}
    for entry in project.get("Modules", []):
        name = entry.get("Name")
        mdir = root / "Source" / name
        build_cs = mdir / f"{name}.Build.cs"
        deps, private = set(), set()
        if build_cs.is_file():
            text = build_cs.read_text(encoding="utf-8")
            for fn, bucket in (("PublicDependencyModuleNames", deps), ("PrivateDependencyModuleNames", private)):
                for block in re.findall(re.escape(fn) + r"\s*\.AddRange\s*\((.*?)\)", text, re.S):
                    bucket |= set(re.findall(r'"([A-Za-z0-9_]+)"', block))
        impls = [p for p in mdir.rglob("*.cpp") if "IMPLEMENT_MODULE" in p.read_text(encoding="utf-8")
                 or "IMPLEMENT_PRIMARY_GAME_MODULE" in p.read_text(encoding="utf-8")] if mdir.is_dir() else []
        modules[name] = {
            "type": entry.get("Type"),
            "loading_phase": entry.get("LoadingPhase"),
            "public_deps": sorted(deps),
            "private_deps": sorted(private),
            "has_build_cs": build_cs.is_file(),
            "has_implementation": bool(impls),
            "implementation_files": [str(p.relative_to(root)) for p in impls],
        }
    data["modules"] = modules

    targets = {}
    for tf in sorted((root / "Source").glob("*.Target.cs")) if (root / "Source").is_dir() else []:
        text = tf.read_text(encoding="utf-8")
        targets[tf.name] = {
            "build_settings": (re.search(r"DefaultBuildSettings\s*=\s*([A-Za-z0-9_.]+)", text) or [None, None])[1],
            "include_order": (re.search(r"IncludeOrderVersion\s*=\s*([A-Za-z0-9_.]+)", text) or [None, None])[1],
            "extra_modules": sorted(set(re.findall(r'ExtraModuleNames\s*\.AddRange\s*\(\s*new\s+string\[\]\s*\{(.*?)\}', text, re.S)[0].split(","))) if re.search(r"ExtraModuleNames\s*\.AddRange", text) else [],
        }
        targets[tf.name]["extra_modules"] = [m.strip().strip('"').strip() for m in targets[tf.name]["extra_modules"]]
    data["targets"] = targets

    data["config"] = sorted(p.name for p in (root / "Config").glob("*.ini")) if (root / "Config").is_dir() else []

    tests = []
    for p in root.rglob("*.cpp"):
        if ".git" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for name in re.findall(r'IMPLEMENT_(?:SIMPLE|COMPLEX|CUSTOM)_AUTOMATION_TEST\s*\(\s*[A-Za-z0-9_]+,\s*"([^"]+)"', text, re.S):
            tests.append(name)
    data["automation_tests"] = sorted(tests)

    data["doc_roots"] = sorted({p.name for p in root.iterdir() if p.is_dir() and p.name.lower() == "docs"})
    adrs = sorted(str(p.relative_to(root)) for d in root.iterdir() if d.is_dir() and d.name.lower() == "docs"
                  for p in d.rglob("*") if p.is_file() and re.search(r"ADR-\d{4}", p.name, re.I))
    data["adr_files"] = adrs
    data["verification_tools"] = sorted(str(p.relative_to(root)) for p in (root / "Tools").rglob("*")
                                        if p.is_file() and p.suffix in {".py", ".sh"}) if (root / "Tools").is_dir() else []
    return data


def show(title):
    print(f"\n{title}")
    print("=" * len(title))


def compare(a, b, name_a, name_b):
    diffs = []

    def note(field, va, vb):
        mark = "  =  " if va == vb else "  ≠  "
        print(f"{mark}{field:<28} {name_a}: {va!r}")
        if va != vb:
            print(f"     {'':<28} {name_b}: {vb!r}")
            diffs.append(field)

    for label, key in (("engine association", "engine_association"), ("target platforms", "target_platforms")):
        show(label.upper())
        note(label, a.get(key), b.get(key))

    show("MODULES")
    mods_a, mods_b = a.get("modules", {}), b.get("modules", {})
    for name in sorted(set(mods_a) | set(mods_b)):
        ina, inb = name in mods_a, name in mods_b
        print(f"  {'both' if ina and inb else (name_a if ina else name_b):<8} {name}")
        for side, mod in ((name_a, mods_a.get(name)), (name_b, mods_b.get(name))):
            if mod:
                print(f"      {side:<8} type={mod['type']:<8} phase={mod['loading_phase']:<14} impl={mod['has_implementation']}")
    if set(mods_a) != set(mods_b):
        diffs.append("module set")

    show("MODULE IMPLEMENTATIONS")
    for label, tree in ((name_a, mods_a), (name_b, mods_b)):
        missing = [m for m, v in tree.items() if not v["has_implementation"]]
        print(f"  {label}: {len(tree)} modules, {len(missing)} without an IMPLEMENT_MODULE translation unit"
              + (f" -> {missing}" if missing else ""))
        if missing:
            diffs.append(f"{label}: unimplemented modules {missing}")

    show("TARGETS")
    for tf in sorted(set(a.get("targets", {})) | set(b.get("targets", {}))):
        note(f"{tf} build settings", a.get("targets", {}).get(tf, {}).get("build_settings"),
             b.get("targets", {}).get(tf, {}).get("build_settings"))
        note(f"{tf} include order", a.get("targets", {}).get(tf, {}).get("include_order"),
             b.get("targets", {}).get(tf, {}).get("include_order"))

    show("CONFIG")
    note("config files", a.get("config"), b.get("config"))

    show("PLUGINS")
    note("plugin count", len(a.get("plugins", [])), len(b.get("plugins", [])))
    print(f"     {name_a} only: {sorted(set(a.get('plugins', [])) - set(b.get('plugins', [])))}")
    print(f"     {name_b} only: {sorted(set(b.get('plugins', [])) - set(a.get('plugins', [])))}")

    show("AUTOMATION TESTS")
    note("test count", len(a.get("automation_tests", [])), len(b.get("automation_tests", [])))
    print(f"     {name_a}: {a.get('automation_tests')}")
    print(f"     {name_b}: {b.get('automation_tests')}")

    show("DOCUMENTATION ROOT AND ADR IDENTIFIERS")
    note("doc root name", a.get("doc_roots"), b.get("doc_roots"))
    if a.get("doc_roots") != b.get("doc_roots"):
        print("     case-collision risk: a single checkout on a case-insensitive filesystem cannot hold both")
    ids_a = sorted({re.search(r"ADR-(\d{4})", p, re.I).group(1) for p in a.get("adr_files", [])})
    ids_b = sorted({re.search(r"ADR-(\d{4})", p, re.I).group(1) for p in b.get("adr_files", [])})
    note("ADR ids in use", ids_a, ids_b)
    overlap = sorted(set(ids_a) & set(ids_b))
    if overlap:
        print(f"     colliding identifiers: {overlap}")

    show("VERIFICATION TOOLS")
    print(f"  {name_a}: {a.get('verification_tools')}")
    print(f"  {name_b}: {b.get('verification_tools')}")

    show("SUMMARY")
    print(f"  differing fields: {len(diffs)}")
    for d in diffs:
        print(f"    - {d}")
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree_a")
    ap.add_argument("tree_b")
    ap.add_argument("--name-a", default=None)
    ap.add_argument("--name-b", default=None)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    a = load_tree(args.tree_a)
    b = load_tree(args.tree_b)
    for tree, side in ((a, "A"), (b, "B")):
        if "error" in tree:
            print(f"tree {side} unusable: {tree['error']} ({tree['root']})", file=sys.stderr)
            return 2

    name_a = args.name_a or pathlib.Path(args.tree_a).name
    name_b = args.name_b or pathlib.Path(args.tree_b).name
    print(f"foundation reconciliation\n  A = {name_a}  ({a['root']})\n  B = {name_b}  ({b['root']})")
    diffs = compare(a, b, name_a, name_b)

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps({"A": a, "B": b, "differences": diffs}, indent=2), encoding="utf-8")
        print(f"\n  machine-readable comparison written to {args.json}")

    print("\n  This tool compares trees; it does not build, open or run either project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
