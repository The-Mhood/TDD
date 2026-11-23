#!/usr/bin/env python3
"""Offline tests for Tools/TDD_M1_Unreal_Setup_macOS.py.

Runs WITHOUT Unreal: a fake `unreal` module is injected into sys.modules before the
setup script is imported, so the full import/verification/idempotency flow can be
exercised deterministically.

Coverage:
  - path resolution (resolve_paths against a fake unreal.Paths)
  - deterministic naming + collision handling (prefixed_asset_path, folders)
  - canonical plan + import-result validation (verify_expected_assets)
  - idempotency (manifest_entry_complete, rerun skip)
  - failure reporting (missing source, no-op import, source changed)
  - runtime API-failure regressions (UE 5.8.4): Asset Registry discovery instead
    of EditorAssetLibrary.find_assets; in-memory pipeline lifecycle (no
    save_loaded_asset on a transient pipeline); partial-rename reconciliation
    (FOREST_TREE_MODULE1-style); pre-existing staging leftover handling;
    wrong-type canonical-path conflict; discovery capability in the report
  - end-to-end main() run against the fake editor

Run:  python3 TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/tests/test_tdd_m1_setup_offline.py
"""

from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import sys
import tempfile
import types
from pathlib import Path

SETUP_PATH = Path(__file__).resolve().parents[1] / "TDD_M1_Unreal_Setup_macOS.py"


def _called_attr_names(source: str) -> set:
    """Attribute names that are actually CALLLED in the source (AST, ignores prose)."""
    names = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            names.add(node.func.attr)
    return names


# ----------------------------------------------------------------------------------
# Fake unreal module
# ----------------------------------------------------------------------------------
class FakeAssetData:
    def __init__(self, path: str, asset_class: str):
        self._path = path
        self._class = asset_class

    def get_asset_path(self) -> str:
        return self._path

    def get_asset_class(self) -> str:
        return self._class

    def get_name(self) -> str:
        return self._path.rsplit("/", 1)[-1]


class FakeAssetRegistry:
    """path -> asset_class, plus simulated Interchange import behaviour."""

    def __init__(self):
        self.assets = {}
        self.pipeline_saved = []
        self.renames = []
        self.import_calls = []
        self.no_op_import = False
        self.import_return = True

    def add(self, path: str, asset_class: str):
        self.assets[path] = asset_class

    # Verified UE 5.8.4 Asset Registry discovery API (the script uses this; the
    # old EditorAssetLibrary.find_assets does NOT exist in UE 5.8.4).
    def get_assets_by_path(self, folder: str, recursive: bool = False):
        if folder in self.assets:
            return [FakeAssetData(folder, self.assets[folder])]
        prefix = folder.rstrip("/") + "/"
        return [FakeAssetData(p, c) for p, c in sorted(self.assets.items())
                if p.startswith(prefix)]

    def get_asset_by_object_path(self, path: str):
        if path in self.assets:
            return FakeAssetData(path, self.assets[path])
        return None

    def enumerate_assets(self, folder: str = ""):
        return self.get_assets_by_path(folder, recursive=True)

    def find_assets(self, folder: str):
        # Backward-compatible alias; the script must NOT use this (UE 5.8.4 has
        # no EditorAssetLibrary.find_assets).
        return self.get_assets_by_path(folder, recursive=True)

    def does_asset_exist(self, path: str) -> bool:
        return path in self.assets

    def make_directory(self, path: str) -> bool:
        return True

    def save_asset(self, path: str, only_if_is_dirty: bool = True) -> bool:
        return True

    def save_loaded_asset(self, asset, only_if_is_dirty: bool = True) -> bool:
        # Model the exact owner-side runtime failure: a transient UObject (the
        # Interchange pipeline) is not a registered content asset, so saving it
        # raises "Asset is not registered" (returned here as a False/failure so
        # the test can assert the script never attempts it).
        self.pipeline_saved.append(asset)
        if isinstance(asset, FakePipeline):
            return False
        return True

    def rename_asset(self, old_path: str, new_path: str) -> bool:
        if old_path not in self.assets:
            return False
        if new_path in self.assets:
            return False  # never overwrite
        self.assets[new_path] = self.assets.pop(old_path)
        self.renames.append((old_path, new_path))
        return True

    # Simulated Interchange import: creates deterministic assets per source file.
    def _simulate_import(self, source: str, destination: str):
        stem = Path(source).stem
        if "adanna_m1_technical_proxy_uv" in source:
            self.add(destination + "/adanna_proxy", "SkeletalMesh")
            self.add(destination + "/adanna_proxy_Skeleton", "Skeleton")
            for clip in ("idle", "walk", "run", "jump", "land"):  # fall/interact absent
                self.add(destination + "/" + clip, "AnimSequence")
            self.add(destination + "/M_adanna_proxy", "Material")
        elif "forbidden_forest_m1" in source:
            for name in ("FOREST_GROUND", "TREE_TRUNKS", "CANOPY"):
                self.add(destination + "/" + name, "StaticMesh")
            self.add(destination + "/M_FOREST_GROUND", "Material")
        elif "collision_proxy" in source:
            self.add(destination + "/adanna_collision", "StaticMesh")
        elif "MODULE" in stem.upper():
            self.add(destination + "/" + stem, "StaticMesh")
            self.add(destination + "/M_" + stem, "Material")


class FakePipeline:
    def __init__(self):
        self.common_meshes_properties = types.SimpleNamespace(force_all_mesh_as_type=None)
        # In-memory object path (transient UObject; never a saved content asset).
        self._path = "/Script/TDD_GAME/_RuntimePipelines/InterchangeGenericAssetsPipeline"

    def get_path_name(self) -> str:
        return self._path


class FakeInterchangeManager:
    def __init__(self, registry: FakeAssetRegistry):
        self.registry = registry

    @staticmethod
    def get_interchange_manager_scripted():
        return _FAKE_STATE["manager"]

    def create_source_data(self, file_name: str):
        return types.SimpleNamespace(get_filename=lambda: file_name)

    def import_asset(self, content_path: str, source_data, import_asset_parameters) -> bool:
        self.registry.import_calls.append({
            "content_path": content_path,
            "source": source_data.get_filename(),
            "is_automated": import_asset_parameters.is_automated,
            "replace_existing": import_asset_parameters.replace_existing,
            "override_pipelines": list(import_asset_parameters.override_pipelines),
        })
        if self.registry.no_op_import:
            return self.registry.import_return
        self.registry._simulate_import(source_data.get_filename(), content_path)
        return self.registry.import_return


class FakeLevelEditorSubsystem:
    def new_level_from_template(self, path: str, template: str) -> bool:
        return True

    def save_current_level(self) -> bool:
        return True


class FakePaths:
    def __init__(self, project_dir: Path):
        self.project_dir_path = project_dir

    def project_dir(self) -> str:
        return str(self.project_dir_path)

    def get_project_file_path(self) -> str:
        return str(self.project_dir_path / "TDD_GAME.uproject")

    def project_saved_dir(self) -> str:
        return str(self.project_dir_path / "Saved")

    def engine_dir(self) -> str:
        return "/Engine"

    def convert_relative_path_to_full(self, path: str) -> str:
        if path.startswith("/"):
            return path
        return str(self.project_dir_path / path)


_FAKE_STATE = {}


def _install_fake_unreal(project_dir: Path, registry: FakeAssetRegistry) -> types.ModuleType:
    fake = types.ModuleType("unreal")
    fake.Paths = FakePaths(project_dir)
    fake.SystemLibrary = types.SimpleNamespace(
        get_engine_version=lambda: "5.8.4",
        get_console_variable=lambda name: "1" if name == "Interchange.FeatureFlags.Import.GLTF" else "0",
    )
    fake.EditorAssetLibrary = registry
    # Verified UE 5.8.4 Asset Registry entry point used by the script's discovery.
    fake.AssetRegistryHelpers = types.SimpleNamespace(
        get_asset_registry=lambda: registry,
        get_asset=lambda asset_data: asset_data,
    )
    fake.InterchangeManager = FakeInterchangeManager
    fake.InterchangeGenericAssetsPipeline = FakePipeline
    fake.InterchangeForceMeshType = types.SimpleNamespace(IFMT_SKELETAL_MESH="SKELETAL")
    fake.ImportAssetParameters = lambda: types.SimpleNamespace(
        is_automated=False, replace_existing=False, override_pipelines=[])
    fake.SoftObjectPath = lambda path: path
    fake.LevelEditorSubsystem = FakeLevelEditorSubsystem

    class _FakeUnrealEditorSubsystem:
        def get_editor_world(self):
            return types.SimpleNamespace(
                get_world_settings=lambda: types.SimpleNamespace(
                    set_editor_property=lambda *a, **k: None))

    fake.UnrealEditorSubsystem = _FakeUnrealEditorSubsystem
    fake.get_editor_subsystem = (
        lambda cls: _FakeUnrealEditorSubsystem()
        if cls is _FakeUnrealEditorSubsystem else FakeLevelEditorSubsystem())
    fake.load_class = lambda outer, path: types.SimpleNamespace() if path else None
    fake.log = lambda msg: None
    fake.log_warning = lambda msg: None
    _FAKE_STATE["manager"] = FakeInterchangeManager(registry)
    sys.modules["unreal"] = fake
    return fake


def load_setup_module():
    spec = importlib.util.spec_from_file_location("tdd_m1_setup", SETUP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ----------------------------------------------------------------------------------
# Tiny test harness
# ----------------------------------------------------------------------------------
PASSED = 0
FAILED = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print("  PASS  " + name)
    else:
        FAILED += 1
        print("  FAIL  " + name + (("  -> " + detail) if detail else ""))


def make_project(tmp: Path):
    """Create a fake project tree: uproject, Config, model handoff files."""
    project = tmp / "ue_project"
    (project / "Config").mkdir(parents=True)
    (project / "Config" / "DefaultEngine.ini").write_text(
        "[/Script/Engine.Engine]\nGameDefaultMap=/Game/Old/Map\nEditorStartupMap=/Game/Old/Map\n",
        encoding="utf-8")
    (project / "TDD_GAME.uproject").write_text("{}", encoding="utf-8")
    model = tmp / "model"
    (model / "modules").mkdir(parents=True)
    (model / "adanna_m1_technical_proxy_uv.glb").write_bytes(b"glb")
    (model / "forbidden_forest_m1.glb").write_bytes(b"glb")
    (model / "adanna_m1_collision_proxy.obj").write_bytes(b"obj")
    for name in ("FOREST_TREE_MODULE", "FOREST_FERN_MODULE", "FOREST_ROCK_MODULE",
                 "FOREST_GREAT_TREE_MODULE", "FOREST_WAYMARKER_MODULE",
                 "FOREST_BOUNDARY_POST_MODULE"):
        (model / "modules" / (name + ".glb")).write_bytes(b"glb")
    return project, model


def new_env(setup, tmp: Path):
    """Fresh fake project + registry + fake unreal bound to the setup module."""
    project, model = make_project(tmp)
    registry = FakeAssetRegistry()
    fake = _install_fake_unreal(project, registry)
    setup.unreal = fake
    return project, model, registry, fake


# ----------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------
def test_pure_naming_and_collision(setup):
    print("[test] pure naming + collision handling")
    a = setup.prefixed_asset_path("forbidden_forest_m1", "FOREST_GROUND")
    b = setup.prefixed_asset_path("forbidden_forest_m1", "TREE_TRUNKS")
    # Same internal name from two different sources must never collide.
    c = setup.prefixed_asset_path("other_source", "FOREST_GROUND")
    check("prefixed path is deterministic",
          a == "/Game/TDD/Imports/forbidden_forest_m1_assets/forbidden_forest_m1_FOREST_GROUND", a)
    check("distinct internal names map to distinct paths", a != b)
    check("cross-source same name does not collide", a != c, "%s vs %s" % (a, c))
    check("staging folder is per-source",
          setup.staging_folder("X") == "/Game/TDD/Imports/_staging/X")
    check("assets folder is per-source",
          setup.assets_folder("X") == "/Game/TDD/Imports/X_assets")


def test_canonical_plan(setup):
    print("[test] canonical plan")
    skeletal = {"path": "/model/adanna_m1_technical_proxy_uv.glb", "kind": "skeletal"}
    plan = setup.canonical_plan_for(skeletal)
    paths = [p["path"] for p in plan]
    check("skeletal plan has mesh + skeleton + 7 animations", len(plan) == 9, str(len(plan)))
    check("skeletal mesh canonical path", "/Game/TDD/Characters/Adanna/Adanna_M1" in paths)
    check("skeleton canonical path", "/Game/TDD/Characters/Adanna/Adanna_M1_Skeleton" in paths)
    check("all 7 animation paths",
          all(("/Game/TDD/Animations/" + n) in paths for n in
              ("idle", "walk", "run", "jump", "fall", "land", "interact")))
    module = {"path": "/model/modules/FOREST_TREE_MODULE.glb", "kind": "module"}
    mplan = setup.canonical_plan_for(module)
    check("module plan is one static mesh at the exact C++ path",
          mplan == [{"path": "/Game/TDD/Imports/FOREST_TREE_MODULE", "class": "StaticMesh"}],
          str(mplan))
    forest = {"path": "/model/forbidden_forest_m1.glb", "kind": "forest"}
    check("forest plan has no canonical assets", setup.canonical_plan_for(forest) == [])


def test_verification_logic(setup):
    print("[test] import-result validation")
    expected = [
        {"path": "/Game/A", "class": "SkeletalMesh"},
        {"path": "/Game/B", "class": "AnimSequence"},
    ]
    result = setup.verify_expected_assets(expected, {"/Game/A": "SkeletalMesh"})
    check("missing asset detected", result["missing"] == ["/Game/B"], str(result))
    check("not ok when missing", not result["ok"])
    result = setup.verify_expected_assets(expected, {
        "/Game/A": "StaticMesh", "/Game/B": "AnimSequence"})
    check("wrong type detected", result["wrong_type"] == [
        {"path": "/Game/A", "expected": "SkeletalMesh", "actual": "StaticMesh"}], str(result))
    result = setup.verify_expected_assets(expected, {
        "/Game/A": "SkeletalMesh", "/Game/B": "AnimSequence"})
    check("all-ok verification", result["ok"] and not result["missing"] and not result["wrong_type"])


def test_diff_and_manifest(setup):
    print("[test] diff + idempotency")
    check("diff_new_assets", setup.diff_new_assets({"a", "b"}, {"b", "c"}) == {"c"})
    entry = {"status": "ok", "final_asset_paths": ["/Game/X", "/Game/Y"]}
    check("complete entry with all assets", setup.manifest_entry_complete(entry, lambda p: True))
    check("complete entry with missing asset",
          not setup.manifest_entry_complete(entry, lambda p: p != "/Game/Y"))
    check("non-ok entry is not complete",
          not setup.manifest_entry_complete(
              {"status": "failed", "final_asset_paths": ["/Game/X"]}, lambda p: True))


def test_path_resolution(setup):
    print("[test] path resolution")
    paths = setup.resolve_paths()
    check("project_dir resolved from unreal.Paths",
          paths["project_dir"].endswith("ue_project"), paths["project_dir"])
    check("model_dir is project_dir parent /model",
          paths["model_dir"].endswith("model"), paths["model_dir"])
    check("config_file points at Config/DefaultEngine.ini",
          paths["config_file"].endswith("Config/DefaultEngine.ini"))


def test_import_flow(setup, tmp):
    print("[test] import flow + per-file verification")
    project, model, registry, fake = new_env(setup, tmp)
    paths = setup.resolve_paths()
    report = {"imports": [], "warnings": []}
    setup.import_assets(report, paths)
    entries = {Path(e["source"]).name: e for e in report["imports"]}

    adaanna = entries["adanna_m1_technical_proxy_uv.glb"]
    check("adanna skeletal mesh at canonical path",
          registry.does_asset_exist("/Game/TDD/Characters/Adanna/Adanna_M1"))
    check("adanna skeleton at canonical path",
          registry.does_asset_exist("/Game/TDD/Characters/Adanna/Adanna_M1_Skeleton"))
    check("adanna animations at canonical paths",
          all(registry.does_asset_exist("/Game/TDD/Animations/" + n)
              for n in ("idle", "walk", "run", "jump", "land")))
    check("missing fall/interact reported explicitly",
          set(adaanna["verification"]["missing"]) == {
              "/Game/TDD/Animations/fall", "/Game/TDD/Animations/interact"},
          str(adaanna["verification"]["missing"]))
    check("adanna status reflects missing clips as a content gap",
          adaanna["status"] == "COMPLETED WITH MISSING", adaanna["status"])

    module = entries["FOREST_TREE_MODULE.glb"]
    check("module import completed", module["status"] == "COMPLETED AND VERIFIED", module.get("status", ""))
    check("module static mesh at exact C++ path",
          registry.does_asset_exist("/Game/TDD/Imports/FOREST_TREE_MODULE"))

    forest = entries["forbidden_forest_m1.glb"]
    check("forest import completed", forest["status"] == "COMPLETED AND VERIFIED", forest.get("status", ""))
    check("forest assets source-prefixed (no flat collision)",
          registry.does_asset_exist(
              "/Game/TDD/Imports/forbidden_forest_m1_assets/forbidden_forest_m1_FOREST_GROUND"))
    check("forest material source-prefixed",
          registry.does_asset_exist(
              "/Game/TDD/Imports/forbidden_forest_m1_assets/forbidden_forest_m1_M_FOREST_GROUND"))
    check("no asset left in staging after rename",
          not registry.get_assets_by_path("/Game/TDD/Imports/_staging/forbidden_forest_m1"))

    # Pipeline lifecycle: the transient pipeline must NOT be saved (UE 5.8.4
    # raises "Asset is not registered" on save_loaded_asset of a transient
    # UObject). It is kept in-memory and referenced via SoftObjectPath.
    check("pipeline NOT saved (transient UObject, in-memory only)",
          len(registry.pipeline_saved) == 0, "saved=%s" % registry.pipeline_saved)
    check("pipeline kept alive in _PIPELINE_KEEPALIVE",
          len(setup._PIPELINE_KEEPALIVE) > 0, str(len(setup._PIPELINE_KEEPALIVE)))
    check("pipeline referenced via SoftObjectPath in override_pipelines",
          all(c["override_pipelines"] for c in registry.import_calls),
          str([c["override_pipelines"] for c in registry.import_calls]))
    check("import called with automated parameters",
          all(c["is_automated"] for c in registry.import_calls))
    check("import called with replace_existing=False",
          all(c["replace_existing"] is False for c in registry.import_calls))


def test_idempotent_rerun(setup, tmp):
    print("[test] idempotent rerun")
    project, model, registry, fake = new_env(setup, tmp)
    paths = setup.resolve_paths()
    report1 = {"imports": [], "warnings": []}
    setup.import_assets(report1, paths)
    calls_after_first = len(registry.import_calls)

    report2 = {"imports": [], "warnings": []}
    setup.import_assets(report2, paths)
    entries = {Path(e["source"]).name: e for e in report2["imports"]}
    check("rerun performs no new imports", len(registry.import_calls) == calls_after_first,
          "%d -> %d" % (calls_after_first, len(registry.import_calls)))
    check("rerun skips completed sources",
          entries["FOREST_TREE_MODULE.glb"]["status"] == "SKIPPED - ALREADY COMPLETE",
          entries["FOREST_TREE_MODULE.glb"]["status"])
    check("rerun still verifies canonical assets exist",
          registry.does_asset_exist("/Game/TDD/Imports/FOREST_TREE_MODULE"))


def test_failure_reporting(setup, tmp):
    print("[test] failure reporting")

    # Missing source file.
    project, model, registry, fake = new_env(setup, tmp / "missing")
    (model / "forbidden_forest_m1.glb").unlink()
    paths = setup.resolve_paths()
    report = {"imports": [], "warnings": []}
    setup.import_assets(report, paths)
    entries = {Path(e["source"]).name: e for e in report["imports"]}
    check("missing source reported as blocked",
          entries["forbidden_forest_m1.glb"]["status"] == "BLOCKED - OWNER-STUDIO DEPENDENCY",
          entries["forbidden_forest_m1.glb"]["status"])

    # No-op import (returns True, creates nothing) must NOT be treated as success.
    project2, model2, registry2, fake2 = new_env(setup, tmp / "noop")
    registry2.no_op_import = True
    setup.TDD_IMPORT_TIMEOUT_S = 0.5
    paths = setup.resolve_paths()
    report = {"imports": [], "warnings": []}
    setup.import_assets(report, paths)
    entries = {Path(e["source"]).name: e for e in report["imports"]}
    check("no-op import reported as failed (not success)",
          entries["adanna_m1_technical_proxy_uv.glb"]["status"].startswith("FAILED"),
          entries["adanna_m1_technical_proxy_uv.glb"]["status"])
    check("no-op import records the timeout",
          entries["adanna_m1_technical_proxy_uv.glb"]["import_timed_out"] is True)
    registry2.no_op_import = False
    setup.TDD_IMPORT_TIMEOUT_S = 180.0

    # Source changed on disk -> skipped, never overwritten.
    project3, model3, registry3, fake3 = new_env(setup, tmp / "changed")
    paths = setup.resolve_paths()
    report = {"imports": [], "warnings": []}
    setup.import_assets(report, paths)
    (model3 / "adanna_m1_technical_proxy_uv.glb").write_bytes(b"glb-modified")
    report = {"imports": [], "warnings": []}
    setup.import_assets(report, paths)
    entries = {Path(e["source"]).name: e for e in report["imports"]}
    check("changed source skipped with explicit status",
          entries["adanna_m1_technical_proxy_uv.glb"]["status"] == "SKIPPED - SOURCE CHANGED",
          entries["adanna_m1_technical_proxy_uv.glb"]["status"])
    check("changed source records both fingerprints",
          "previous_fingerprint" in entries["adanna_m1_technical_proxy_uv.glb"])


def test_runtime_api_regressions(setup, tmp):
    """Regression tests for the owner's exact UE 5.8.4 runtime failures."""
    print("[test] runtime API-failure regressions")

    # --- (1) EditorAssetLibrary.find_assets must NOT be used. ---
    src = SETUP_PATH.read_text(encoding="utf-8")
    called = _called_attr_names(src)
    check("script never calls EditorAssetLibrary.find_assets",
          "find_assets" not in called, "find_assets called: %s" % sorted(called))
    check("script uses verified Asset Registry get_assets_by_path",
          "get_assets_by_path" in called)
    check("script keeps pipeline in-memory via _PIPELINE_KEEPALIVE",
          "_PIPELINE_KEEPALIVE" in src)
    check("script never calls save_loaded_asset on the pipeline",
          "save_loaded_asset" not in called, "save_loaded_asset called")

    # --- (2) Transient pipeline save is rejected; script must not attempt it. ---
    project, model, registry, fake = new_env(setup, tmp / "api_fail")
    # The fake save_loaded_asset returns False for a FakePipeline (models the
    # owner's "Asset is not registered" failure). The script must never call it.
    pipeline = setup._make_interchange_pipeline(force_skeletal=True)
    check("pipeline creation returns (pipeline, path_used) tuple",
          isinstance(pipeline, tuple) and len(pipeline) == 2, str(pipeline))
    check("pipeline is kept alive in-memory",
          pipeline[0] in setup._PIPELINE_KEEPALIVE)
    check("pipeline path_used is its in-memory object path",
          bool(pipeline[1]), str(pipeline[1]))
    check("no save_loaded_asset attempted on the pipeline",
          len(registry.pipeline_saved) == 0, str(registry.pipeline_saved))

    # --- (3) Partial rename reconciliation (FOREST_TREE_MODULE1 from failed run). ---
    project2, model2, registry2, fake2 = new_env(setup, tmp / "reconcile_rename")
    # Simulate the failed run's Interchange collision rename: the module landed at
    # FOREST_TREE_MODULE1 (StaticMesh) instead of the canonical path.
    registry2.add("/Game/TDD/Imports/FOREST_TREE_MODULE1", "StaticMesh")
    item = {"path": model2 / "modules" / "FOREST_TREE_MODULE.glb",
            "kind": "module", "note": "regression"}
    entry = setup._import_one(item)
    check("partial FOREST_TREE_MODULE1 reconciled to canonical path",
          registry2.does_asset_exist("/Game/TDD/Imports/FOREST_TREE_MODULE"),
          entry.get("status", ""))
    check("reconciliation renamed the partial (not copied/overwritten)",
          any(r["to"] == "/Game/TDD/Imports/FOREST_TREE_MODULE"
              for r in entry.get("reconciled_assets", [])),
          str(entry.get("reconciled_assets")))
    check("partial rename source no longer present (renamed, not duplicated)",
          not registry2.does_asset_exist("/Game/TDD/Imports/FOREST_TREE_MODULE1"))
    check("reconciled source verified without re-importing",
          entry["status"] == "COMPLETED AND VERIFIED" and
          entry.get("action") == "completed_via_reconciliation",
          entry.get("status", ""))
    check("no import attempted for reconciled source",
          len(registry2.import_calls) == 0, str(len(registry2.import_calls)))

    # --- (4) Pre-existing staging leftover moved, never overwritten/deleted. ---
    project3, model3, registry3, fake3 = new_env(setup, tmp / "reconcile_staging")
    staging = "/Game/TDD/Imports/_staging/FOREST_TREE_MODULE"
    registry3.add(staging + "/M_leftover", "Material")  # non-canonical leftover
    item3 = {"path": model3 / "modules" / "FOREST_TREE_MODULE.glb",
             "kind": "module", "note": "regression"}
    entry3 = setup._import_one(item3)
    check("staging leftover moved to prefixed collision-safe path",
          registry3.does_asset_exist(
              "/Game/TDD/Imports/FOREST_TREE_MODULE_assets/FOREST_TREE_MODULE_M_leftover"),
          str(entry3.get("prefixed_from_reconciliation")))
    check("staging leftover NOT deleted",
          not registry3.does_asset_exist(staging + "/M_leftover"))
    check("staging cleared before fresh import",
          not registry3.get_assets_by_path(staging))
    check("source still imported after leftover cleanup",
          entry3["status"] == "COMPLETED AND VERIFIED", entry3.get("status", ""))

    # --- (5) Wrong type at a canonical path -> conflict, never overwritten. ---
    project4, model4, registry4, fake4 = new_env(setup, tmp / "reconcile_conflict")
    registry4.add("/Game/TDD/Imports/FOREST_TREE_MODULE", "Material")  # wrong type
    item4 = {"path": model4 / "modules" / "FOREST_TREE_MODULE.glb",
             "kind": "module", "note": "regression"}
    entry4 = setup._import_one(item4)
    check("wrong-type canonical path reported as conflict",
          entry4["status"] == "CONFLICT - NOT OVERWRITTEN", entry4.get("status", ""))
    check("wrong-type canonical path left untouched (not overwritten)",
          registry4.assets.get("/Game/TDD/Imports/FOREST_TREE_MODULE") == "Material")
    check("conflict recorded with expected vs actual type",
          entry4.get("reconciliation", {}).get("conflicts"),
          str(entry4.get("reconciliation")))

    # --- (6) Discovery API capability recorded in the report. ---
    project5, model5, registry5, fake5 = new_env(setup, tmp / "discovery")
    setup.TDD_IMPORT_TIMEOUT_S = 5.0
    setup.main()
    report = json.loads(
        (project5 / "Saved" / "TDD_M1" / "tdd_m1_setup_report.json")
        .read_text(encoding="utf-8"))
    check("report records Asset Registry discovery API",
          report["asset_discovery"]["api"] ==
          "AssetRegistryHelpers.get_asset_registry().get_assets_by_path",
          str(report["asset_discovery"]))
    check("report marks discovery API supported",
          report["asset_discovery"]["supported"] is True,
          str(report["asset_discovery"]))
    check("report discovery detail is the get_assets_by_path variant",
          report["asset_discovery"]["support_detail"] ==
          "asset_registry_get_assets_by_path",
          str(report["asset_discovery"]["support_detail"]))


def test_main_end_to_end(setup, tmp):
    print("[test] main() end-to-end")
    project, model, registry, fake = new_env(setup, tmp)
    setup.TDD_IMPORT_TIMEOUT_S = 5.0
    setup.main()
    report_path = project / "Saved" / "TDD_M1" / "tdd_m1_setup_report.json"
    manifest_path = project / "Saved" / "TDD_M1" / "tdd_m1_setup_manifest.json"
    check("report written", report_path.is_file())
    check("manifest written", manifest_path.is_file())
    report = json.loads(report_path.read_text(encoding="utf-8"))
    check("map section completed", report["map"].get("status") == "COMPLETED AND VERIFIED",
          str(report["map"]))
    check("config repointed", report["config"].get("changed") is True, str(report["config"]))
    check("config backed up",
          (project / "Config" / "DefaultEngine.ini.tdd_backup").is_file())
    check("manifest records all sources",
          len(json.loads(manifest_path.read_text(encoding="utf-8"))["sources"]) == 9)


def main():
    tmp_root = Path(tempfile.mkdtemp(prefix="tdd_m1_setup_test_"))
    try:
        # Boot env for the pure tests and path resolution.
        project, model = make_project(tmp_root / "boot")
        registry = FakeAssetRegistry()
        fake = _install_fake_unreal(project, registry)
        setup = load_setup_module()
        setup.unreal = fake

        test_pure_naming_and_collision(setup)
        test_canonical_plan(setup)
        test_verification_logic(setup)
        test_diff_and_manifest(setup)
        test_path_resolution(setup)
        test_import_flow(setup, tmp_root / "flow")
        test_idempotent_rerun(setup, tmp_root / "rerun")
        test_failure_reporting(setup, tmp_root / "fail")
        test_runtime_api_regressions(setup, tmp_root / "regress")
        test_main_end_to_end(setup, tmp_root / "e2e")
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    print()
    print("RESULT: %d passed, %d failed" % (PASSED, FAILED))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
