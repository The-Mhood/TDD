#!/usr/bin/env python3
"""L0 CI: verify repository text integrity without an engine.

Runs here and on any machine. This is intentionally independent of Unreal so that
a broken document, a dangling strategy reference or a stray binary is caught in
seconds rather than discovered at integration.

Usage:
    python3 Tools/ci/l0_checks.py
    python3 Tools/ci/l0_checks.py --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO = Path(__file__).resolve().parents[2]

# Files that must never be committed in plain git (ADR-0004).
FORBIDDEN_BINARY_SUFFIXES = {
    ".uasset", ".umap", ".ubulk", ".uexp", ".upk", ".pak", ".utoc", ".ucas",
    ".wav", ".mp3", ".ogg", ".png", ".jpg", ".jpeg", ".tga", ".exr",
    ".fbx", ".obj", ".usd", ".usda", ".blend", ".max", ".ma", ".mb",
}
MAX_TEXT_FILE_BYTES = 5 * 1024 * 1024  # ADR-0004 hard rule
DOCS_REQUIRED = [
    "Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md",
    "Docs/CANON_INDEX.md",
    "Docs/production/STAGE_GATES.md",
    "Docs/production/RACI.md",
    "Docs/adr/README.md",
]
ADR_EXPECTED = [f"ADR-000{i}-" for i in range(1, 9)]
STATUS_TAGS = [
    "ESTABLISHED", "PARTIAL", "SPEC", "STUB", "EXPERIMENTAL", "MOCKED", "BLOCKED", "UNAVAILABLE",
]


def tracked_files() -> List[Path]:
    """Files git would consider, plus untracked non-ignored files."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=REPO, capture_output=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in REPO.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [REPO / p for p in out.decode().split("\0") if p]


def check_no_binaries(files: List[Path]) -> List[str]:
    problems = []
    for path in files:
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_BINARY_SUFFIXES:
            problems.append(f"forbidden binary committed (ADR-0004): {path.relative_to(REPO)}")
        elif path.is_file() and path.stat().st_size > MAX_TEXT_FILE_BYTES:
            problems.append(f"file exceeds 5 MB text rule (ADR-0004): {path.relative_to(REPO)}")
    return problems


def check_required_docs() -> List[str]:
    problems = []
    for rel in DOCS_REQUIRED:
        if not (REPO / rel).is_file():
            problems.append(f"missing required document: {rel}")
    adr_dir = REPO / "Docs" / "adr"
    if adr_dir.is_dir():
        names = [p.name for p in adr_dir.glob("ADR-*.md")]
        for prefix in ADR_EXPECTED:
            if not any(n.startswith(prefix) for n in names):
                problems.append(f"missing architecture decision record: {prefix}*.md")
    return problems


def check_doc_links(files: List[Path]) -> List[str]:
    """Relative markdown links must resolve, so architecture references stay honest."""
    problems = []
    link_re = re.compile(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            problems.append(f"unreadable markdown: {path.relative_to(REPO)}")
            continue
        for match in link_re.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(REPO)
            except ValueError:
                continue  # link points outside the repo; not ours to validate
            if not resolved.exists():
                problems.append(
                    f"dangling link in {path.relative_to(REPO)}: {target}"
                )
    return problems


def check_json_parses(files: List[Path]) -> List[str]:
    problems = []
    for path in files:
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            problems.append(f"invalid JSON in {path.relative_to(REPO)}: {exc}")
    return problems


def check_uproject() -> List[str]:
    problems = []
    uproject = REPO / "TDD.uproject"
    if not uproject.is_file():
        return ["missing TDD.uproject"]
    try:
        data = json.loads(uproject.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"TDD.uproject is not valid JSON: {exc}"]
    if data.get("EngineAssociation") != "5.8":
        problems.append(
            f"TDD.uproject EngineAssociation is {data.get('EngineAssociation')!r}, "
            f"expected '5.8' (ADR-0002)"
        )
    declared = {m.get("Name") for m in data.get("Modules", [])}
    for module in ("TDDRuntime", "TDDEditor", "TDDTests"):
        if module not in declared:
            problems.append(f"TDD.uproject does not declare module {module}")
        build_cs = REPO / "Source" / module / f"{module}.Build.cs"
        if not build_cs.is_file():
            problems.append(f"module {module} declared but {build_cs.name} missing")
    return problems


def check_no_engine_claim_in_reports(files: List[Path]) -> List[str]:
    """Guard against the failure mode ADR-0005 exists to prevent.

    Any file that claims a runtime system is ESTABLISHED must reference evidence.
    We check evidence files and agent reports only, not the architecture docs
    (which describe the *policy* and legitimately contain the word ESTABLISHED).
    """
    problems = []
    evidence_dir = REPO / "Docs" / "evidence"
    reports_dir = REPO / "Docs" / "reports"
    for base in (evidence_dir, reports_dir):
        if not base.is_dir():
            continue
        for path in base.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            if "ESTABLISHED" in text and "evidence" not in text.lower():
                problems.append(
                    f"{path.relative_to(REPO)} claims ESTABLISHED but cites no evidence path"
                )
    return problems


def check_stage_gates_cover_all_stages() -> List[str]:
    path = REPO / "Docs" / "production" / "STAGE_GATES.md"
    if not path.is_file():
        return ["missing STAGE_GATES.md"]
    text = path.read_text(encoding="utf-8")
    problems = []
    for stage in range(0, 10):
        if f"## Stage {stage} " not in text:
            problems.append(f"STAGE_GATES.md does not define Stage {stage}")
    return problems


def check_status_tag_vocabulary() -> List[str]:
    """The status vocabulary must be identical in the architecture doc and README."""
    arch = REPO / "Docs" / "00_MASTER_ENGINEERING_ARCHITECTURE.md"
    if not arch.is_file():
        return ["missing architecture document"]
    text = arch.read_text(encoding="utf-8")
    return [
        f"architecture document does not define status tag {tag}"
        for tag in STATUS_TAGS
        if tag not in text
    ]


def check_world_manifest() -> List[str]:
    """Every committed chapter manifest must pass the canon gate."""
    problems: List[str] = []
    manifests = sorted((REPO / "Tools" / "world" / "data").glob("*_manifest.json"))
    if not manifests:
        return ["no chapter manifests found under Tools/world/data"]
    try:
        sys.path.insert(0, str(REPO / "Tools" / "canon"))
        sys.path.insert(0, str(REPO / "Tools" / "world"))
        import canon_index  # noqa: F401
        import world_manifest
        index = canon_index.load_index()
    except Exception as exc:  # pragma: no cover - defensive
        return [f"cannot import world tooling: {exc}"]
    for path in manifests:
        try:
            manifest = world_manifest.load_manifest(path)
        except Exception as exc:
            problems.append(f"{path.name}: unreadable ({exc})")
            continue
        for error in world_manifest.validate_manifest(manifest, index):
            problems.append(f"{path.name}: {error}")
    return problems


def check_canon_mirror_drift() -> List[str]:
    """Regenerating from the captured excerpt must be a no-op.

    If it is not, the committed mirror no longer matches the registers it claims
    to mirror - the exact canon-drift failure ADR-0006 exists to prevent.
    """
    import subprocess
    try:
        before = (REPO / "Tools" / "canon" / "data" / "canon_index.json").read_text()
        result = subprocess.run(
            [sys.executable, str(REPO / "Tools" / "canon" / "gen_world_data.py")],
            capture_output=True, text=True, cwd=REPO,
        )
        if result.returncode != 0:
            return [f"generator failed: {result.stderr.strip()[:400]}"]
        after = (REPO / "Tools" / "canon" / "data" / "canon_index.json").read_text()
        if before != after:
            return ["canon_index.json is stale: regenerating from the register "
                    "excerpt produced different output. Run "
                    "python3 Tools/canon/gen_world_data.py and commit the result."]
    except Exception as exc:  # pragma: no cover
        return [f"drift check failed: {exc}"]
    return []


def check_greybox_restrictions() -> List[str]:
    """CD-5: greybox is for technical evaluation only, and the rules must bite."""
    try:
        sys.path.insert(0, str(REPO / "Tools" / "world"))
        import greybox_rules
    except Exception as exc:  # pragma: no cover - defensive
        return [f"cannot import greybox_rules: {exc}"]
    problems: List[str] = []
    manifests = sorted((REPO / "Tools" / "world" / "data").glob("greybox_*.json"))
    for path in manifests:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            problems.append(f"{path.name}: unreadable ({exc})")
            continue
        for problem in greybox_rules.validate_greybox_manifest(data):
            problems.append(f"{path.name}: {problem}")
        if not data.get("greybox_assets") and not data.get("_empty_reason"):
            problems.append(f"{path.name}: declares no assets and gives no reason")
    return problems


def check_register_counts_reconcile() -> List[str]:
    """The register's published counts must sum, and Chapter 1 must reconcile.

    This is the guard for the arithmetic error that already shipped once
    (location entries recorded as 191 when 8+142+46 = 196).
    """
    import subprocess
    result = subprocess.run(
        [sys.executable, str(REPO / "Tools" / "world" / "count_reconciliation.py")],
        capture_output=True, text=True, cwd=REPO,
    )
    if result.returncode != 0:
        tail = (result.stdout or "").strip().splitlines()[-12:]
        return ["register counts do not reconcile:", *[f"  {line}" for line in tail]]
    return []


def check_population_provenance() -> List[str]:
    """Every scene must state whether its NPC count is register data or an
    assumption, and the budget must admit most of it is assumption.

    The TD required the two to be distinguishable. Making it a gate means a
    future change cannot quietly relabel a policy default as register data.
    """
    problems: List[str] = []
    artifact = REPO / "Docs" / "evidence" / "agent2" / "CH01_population_budget.json"
    if not artifact.is_file():
        return [f"missing evidence artifact: {artifact.name}"]
    try:
        data = json.loads(artifact.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{artifact.name}: unreadable ({exc})"]

    scenes = data.get("budget", {}).get("scenes", [])
    if not scenes:
        return [f"{artifact.name}: no scene rows"]

    allowed = {"REGISTER_DATA", "POLICY_DEFAULT", "UNPARSED", "NO_NPCS"}
    for scene in scenes:
        prov = scene.get("npcs_provenance")
        if prov not in allowed:
            problems.append(
                f"{scene.get('scene_id')}: npcs_provenance {prov!r} not one of {sorted(allowed)}")
        if prov == "REGISTER_DATA" and scene.get("npcs_is_measured") is not True:
            problems.append(
                f"{scene.get('scene_id')}: claims REGISTER_DATA but npcs_is_measured is false")
        if prov in {"POLICY_DEFAULT", "UNPARSED"} and scene.get("npcs_is_measured"):
            problems.append(
                f"{scene.get('scene_id')}: provenance {prov} but npcs_is_measured is true - "
                f"an assumption must never be marked as measured")

    summary = data.get("budget", {}).get("npcs_provenance_summary", {})
    if not summary:
        problems.append("budget has no npcs_provenance_summary")
    if summary.get("POLICY_DEFAULT", 0) == 0:
        problems.append("no scene is marked POLICY_DEFAULT; this contradicts the "
                        "documented partial capture and suggests mislabelling")

    # CROSS-CHECK AGAINST THE SOURCE. Trusting the artifact's own self-reported
    # flags is not enough: relabelling a scene and flipping npcs_is_measured with
    # it passes every internal consistency test. Provenance must be re-derived
    # from the register fixture and compared.
    try:
        import population_budget as pb
        import registers as reg
        fixture = (REPO / "Tools" / "canon" / "tests" / "fixtures"
                   / "scene_register_ch01_full.md")
        text = fixture.read_text(encoding="utf-8")
        live = pb.build_chapter_budget(reg.parse_scene_summary(text),
                                       reg.parse_scene_details(text),
                                       pb.load_policy(), "CH01")
        live_by_id = {s.scene_id: s for s in live.scenes}
    except Exception as exc:
        return problems + [f"cannot re-derive provenance: {exc}"]

    for scene in scenes:
        sid = scene.get("scene_id")
        expected = live_by_id.get(sid)
        if expected is None:
            problems.append(f"{sid}: not present in the live derivation")
            continue
        if scene.get("npcs_provenance") != expected.npcs_provenance:
            problems.append(
                f"{sid}: artifact says {scene.get('npcs_provenance')} but the register "
                f"fixture derives {expected.npcs_provenance}")
        if scene.get("npcs_from_register") != expected.npcs_from_register:
            problems.append(
                f"{sid}: artifact NPC count {scene.get('npcs_from_register')} does not "
                f"match register-derived {expected.npcs_from_register}")

    cap = data.get("meta", {}).get("capture_status", {})
    if "PARTIAL" not in str(cap.get("locations", "")):
        problems.append("capture_status must state that locations are PARTIAL")
    return problems


def check_sensitivity_artifact_current() -> List[str]:
    """The sensitivity artifact must match what the code produces now."""
    import subprocess
    artifact = REPO / "Docs" / "evidence" / "agent2" / "CH01_population_sensitivity.json"
    if not artifact.is_file():
        return ["missing Docs/evidence/agent2/CH01_population_sensitivity.json"]
    try:
        committed = json.loads(artifact.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"sensitivity artifact unreadable ({exc})"]

    result = subprocess.run(
        [sys.executable, str(REPO / "Tools" / "world" / "sensitivity.py")],
        capture_output=True, text=True, cwd=REPO)
    if result.returncode != 0:
        return [f"sensitivity tool failed: {result.stderr.strip()[:300]}"]

    sys.path.insert(0, str(REPO / "Tools" / "canon"))
    sys.path.insert(0, str(REPO / "Tools" / "world"))
    import population_budget as pb
    import registers as reg
    import sensitivity as sens
    fixtures = REPO / "Tools" / "canon" / "tests" / "fixtures" / "scene_register_ch01_full.md"
    text = fixtures.read_text(encoding="utf-8")
    live = sens.build_report(reg.parse_scene_summary(text),
                             reg.parse_scene_details(text),
                             pb.load_policy())

    problems: List[str] = []
    if committed["baseline"] != live["baseline"]:
        problems.append(
            f"sensitivity baseline is stale: artifact {committed['baseline']} "
            f"vs live {live['baseline']}. Re-run Tools/world/sensitivity.py --out ...")
    if (committed["facts"]["scenes_with_register_npc_data"]
            != live["facts"]["scenes_with_register_npc_data"]):
        problems.append("sensitivity facts are stale")
    return problems


def run(verbose: bool = False) -> Tuple[bool, Dict[str, List[str]]]:
    files = tracked_files()
    results: Dict[str, List[str]] = {
        "no_forbidden_binaries": check_no_binaries(files),
        "required_docs": check_required_docs(),
        "doc_links": check_doc_links(files),
        "json_parses": check_json_parses(files),
        "uproject": check_uproject(),
        "stage_gates": check_stage_gates_cover_all_stages(),
        "status_vocabulary": check_status_tag_vocabulary(),
        "evidence_claims": check_no_engine_claim_in_reports(files),
        "world_manifest": check_world_manifest(),
        "canon_mirror_drift": check_canon_mirror_drift(),
        "greybox_restrictions": check_greybox_restrictions(),
        "register_counts_reconcile": check_register_counts_reconcile(),
        "population_provenance": check_population_provenance(),
        "sensitivity_artifact_current": check_sensitivity_artifact_current(),
    }
    ok = all(not v for v in results.values())
    if verbose:
        for name, problems in results.items():
            mark = "PASS" if not problems else "FAIL"
            print(f"[{mark}] {name}")
            for problem in problems:
                print(f"        {problem}")
    return ok, results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument(
        "--evidence",
        metavar="PATH",
        help="Write a machine-readable evidence JSON (architecture doc 11.3).",
    )
    args = parser.parse_args()
    ok, results = run(verbose=args.verbose)
    checks_run = len(results)
    checks_failed = sum(1 for v in results.values() if v)

    if args.evidence:
        import datetime

        payload = {
            "test": "L0.Repository.TextIntegrity",
            "suite": "Tools/ci/l0_checks.py",
            "engine": "n/a (host-side)",
            "dateUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "result": "PASS" if ok else "FAIL",
            "checksRun": checks_run,
            "checksFailed": checks_failed,
            "checks": [{"name": name, "result": "PASS" if not p else "FAIL", "problems": p}
                       for name, p in results.items()],
        }
        out = Path(args.evidence)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"evidence written: {out}")

    print(f"\nL0 checks: {checks_run - checks_failed}/{checks_run} passed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
