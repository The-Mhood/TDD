#!/usr/bin/env python3
"""Import the W1 D13 CH01 Compound Assembled V2 OBJ and assemble it with the
CH01 greybox. Run from Unreal Editor's Python console or -ExecutePythonScript.

Creates a real Unreal asset + level actor only in the owner UE 5.8 environment.
Individual modular assets are preserved (the OBJ is a single-import assembly of
Env Kit V2 + W1 D7 modules; the module OBJs remain untouched).
"""
import hashlib
import json
import os
from pathlib import Path

import unreal

REPO = Path(unreal.Paths.project_dir())
SOURCE_OBJ = REPO / ".arena/production/2026-11-29_w1d13_production/ch01_assembly/out/CH01_COMPOUND_ASSEMBLED_V2.obj"
MANIFEST = REPO / ".arena/production/2026-11-29_w1d13_production/ch01_assembly/out/ASSEMBLY_V2_MANIFEST.json"
DESTINATION = "/Game/Environment/CH01/CompoundV2"
ASSET_NAME = "SM_CH01_Compound_Assembled_V2"
GREYBOX_MAP = "/Game/Maps/Ch01_Greybox"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    require(SOURCE_OBJ.is_file(), "Compound OBJ not found at " + str(SOURCE_OBJ))
    actual_hash = hashlib.sha256(SOURCE_OBJ.read_bytes()).hexdigest()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest.get("asset") == "CH01_COMPOUND_ASSEMBLED_V2",
            "Manifest asset name mismatch: " + manifest.get("asset", "?"))
    require(manifest.get("status", "").startswith("PROVISIONAL"),
            "Manifest is not flagged provisional — refusing to import")

    asset_path = DESTINATION + "/" + ASSET_NAME
    require(not unreal.EditorAssetLibrary.does_asset_exist(asset_path),
            "Refusing to replace existing asset: " + asset_path)

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(SOURCE_OBJ))
    task.set_editor_property("destination_path", DESTINATION)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", False)
    task.set_editor_property("save", True)
    task.set_editor_property("scale", 1.0)  # OBJ is metres; UE imports at 1.0
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    imported = [unreal.EditorAssetLibrary.load_asset(path)
                for path in task.get_editor_property("imported_object_paths")]
    imported = [asset for asset in imported if asset is not None]
    classes = sorted(set(asset.get_class().get_name() for asset in imported))
    require("StaticMesh" in classes, "OBJ import did not produce a StaticMesh: " + str(classes))
    mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    require(mesh is not None, "Imported mesh not loadable at " + asset_path)

    # Assemble with the greybox: place the compound in the current level.
    # Collision uses the mesh (module bounds proxies are the TD confirmation
    # step per the manifest).
    world = unreal.EditorLevelLibrary.get_editor_world()
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(0.0, 0.0, 0.0), unreal.Rotator(0.0, 0.0, 0.0))
    require(actor is not None, "Could not spawn compound actor")
    actor.set_actor_label("GBX_CH01_Compound_V2", mark_dirty=True)
    actor.static_mesh_component.set_static_mesh(mesh)
    actor.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    actor.tags = ["TDD_Greybox", "TDD_Compound"]

    report = {
        "status": "IMPORTED_AND_ASSEMBLED",
        "source_obj": str(SOURCE_OBJ),
        "source_sha256": actual_hash,
        "manifest_status": manifest.get("status"),
        "asset_path": asset_path,
        "imported_classes": classes,
        "assembled_actor_label": "GBX_CH01_Compound_V2",
        "collision": "mesh (module bounds proxies pending TD confirmation)",
        "classification": "provisional assembly, not canon; modular assets preserved",
    }
    out = REPO / "Saved/BuildEvidence/W2/compound-v2-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W2 compound V2 import: " + json.dumps(report))


main()
