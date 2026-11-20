"""Build a native UE editor greybox map from the committed M1 world.json.

Run from Unreal Editor's Python console or with -ExecutePythonScript. This
creates a real UMAP only when run in the owner UE 5.8 environment; the agent
sandbox cannot execute Unreal editor Python.
"""
import json
import math
import os
from pathlib import Path
import unreal

REPO = Path(unreal.Paths.project_dir())
WORLD_JSON = REPO / "TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/world.json"
MAP_PACKAGE = "/Game/Maps/Ch01_Greybox"
CUBE_PATH = "/Engine/BasicShapes/Cube.Cube"
CYLINDER_PATH = "/Engine/BasicShapes/Cylinder.Cylinder"
SPHERE_PATH = "/Engine/BasicShapes/Sphere.Sphere"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def spawn_mesh(mesh, label, location_m, scale, rotation=None):
    loc = unreal.Vector(location_m[0] * 100.0, location_m[1] * 100.0, location_m[2] * 100.0)
    rot = rotation or unreal.Rotator(0.0, 0.0, 0.0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    require(actor is not None, "Failed to spawn " + label)
    actor.set_actor_label(label, mark_dirty=True)
    component = actor.static_mesh_component
    component.set_static_mesh(mesh)
    actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
    return actor


def main():
    data = json.loads(WORLD_JSON.read_text(encoding="utf-8"))
    bounds, route = data["bounds"], data["route"]
    points = route["waypoints"]
    require(len(points) >= 2, "Route must have at least two waypoints")
    require(route["pathWidth"] > 0, "Path width must be positive")
    for p in points:
        require(bounds["minX"] <= p["x"] <= bounds["maxX"] and
                bounds["minY"] <= p["y"] <= bounds["maxY"],
                "Waypoint outside layout bounds: " + p["label"])

    # Create a fresh, explicitly named map; refuse to overwrite an existing asset.
    require(not unreal.EditorAssetLibrary.does_asset_exist(MAP_PACKAGE),
            "Refusing to replace existing map: " + MAP_PACKAGE)
    require(unreal.EditorLevelLibrary.new_level(MAP_PACKAGE), "Could not create " + MAP_PACKAGE)
    cube = unreal.EditorAssetLibrary.load_asset(CUBE_PATH)
    cylinder = unreal.EditorAssetLibrary.load_asset(CYLINDER_PATH)
    sphere = unreal.EditorAssetLibrary.load_asset(SPHERE_PATH)
    require(cube and cylinder and sphere, "Engine BasicShapes assets are unavailable")

    center_x = (bounds["minX"] + bounds["maxX"]) * 0.5
    center_y = (bounds["minY"] + bounds["maxY"]) * 0.5
    half_x = (bounds["maxX"] - bounds["minX"]) * 0.5
    half_y = (bounds["maxY"] - bounds["minY"]) * 0.5
    spawn_mesh(cube, "GBX_Ground", (center_x, center_y, -0.25), (half_x, half_y, 0.25))

    # Greybox route strips are flat, connected, and follow the authored route.
    width = route["pathWidth"]
    for index, (a, b) in enumerate(zip(points, points[1:])):
        dx, dy = b["x"] - a["x"], b["y"] - a["y"]
        length = math.hypot(dx, dy)
        yaw = math.degrees(math.atan2(dy, dx))
        spawn_mesh(cube, "GBX_Route_%02d_%s" % (index + 1, b["label"].replace(" ", "_")),
                   ((a["x"] + b["x"]) * 0.5, (a["y"] + b["y"]) * 0.5, 0.02),
                   (length * 0.5, width * 0.5, 0.02), unreal.Rotator(0.0, yaw, 0.0))

    # Authored obstacle data converted to neutral, collision-enabled primitives.
    for obstacle in data.get("obstacles", []):
        kind = obstacle.get("type", "BLOCK")
        x, y = obstacle.get("x", 0.0), obstacle.get("y", 0.0)
        radius = max(0.08, obstacle.get("trunkRadius", obstacle.get("radius", 0.5)))
        height = max(0.2, obstacle.get("height", 1.0))
        ident = obstacle.get("id", "Obstacle")
        if kind in ("TREE", "GREAT_TREE", "ROOTS", "POST", "CAMERA_PROBE"):
            mesh = cylinder
            actor = spawn_mesh(mesh, "GBX_" + ident, (x, y, height * 0.5),
                               (radius * 2.0, radius * 2.0, height))
            actor.tags = ["TDD_Greybox", "TDD_Obstacle", kind]
            canopy = obstacle.get("canopyRadius", 0.0)
            if canopy > 0 and kind in ("TREE", "GREAT_TREE"):
                crown = spawn_mesh(sphere, "GBX_Canopy_" + ident,
                                   (x, y, height + canopy * 0.35),
                                   (canopy * 2.0, canopy * 2.0, canopy * 1.3))
                crown.tags = ["TDD_Greybox", "TDD_Canopy", kind]
        else:
            actor = spawn_mesh(cube, "GBX_" + ident, (x, y, height * 0.5),
                               (radius, radius, height))
            actor.tags = ["TDD_Greybox", "TDD_Obstacle", kind]

    for marker in data.get("interactables", []):
        marker_actor = spawn_mesh(sphere, "GBX_Marker_" + marker["id"],
                                  (marker["x"], marker["y"], 0.5),
                                  (marker["radius"] * 2.0, marker["radius"] * 2.0, marker["radius"] * 2.0))
        marker_actor.tags = ["TDD_Greybox", "TDD_Interactable"]

    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart, unreal.Vector(data["spawn"]["position"]["x"] * 100,
        data["spawn"]["position"]["y"] * 100, 100), unreal.Rotator(0, data["spawn"]["yaw"], 0))
    require(player_start is not None, "Could not create PlayerStart")
    player_start.set_actor_label("GBX_PlayerStart", mark_dirty=True)

    enemy_class = unreal.load_class(None, "/Script/TheDisobedientDaughter.TDDTrainingEnemy")
    if enemy_class:
        enemy = unreal.EditorLevelLibrary.spawn_actor_from_class(
            enemy_class, unreal.Vector(0, 1200, 100), unreal.Rotator(0, 180, 0))
        require(enemy is not None, "Could not spawn training enemy")
        enemy.set_actor_label("GBX_TrainingEnemy", mark_dirty=True)
    else:
        unreal.log_warning("TDDTrainingEnemy class unavailable; build the project module and rerun.")

    game_mode_bp = unreal.EditorAssetLibrary.load_asset(
        "/Game/Characters/Adanna/TechnicalProxy/BP_TDDGameMode_TechnicalProxy")
    if game_mode_bp and game_mode_bp.generated_class:
        world = unreal.EditorLevelLibrary.get_editor_world()
        world.get_world_settings().set_editor_property("default_game_mode", game_mode_bp.generated_class)

    require(unreal.EditorLevelLibrary.save_current_level(), "Could not save greybox map")
    engine_ini = REPO / "Config/DefaultEngine.ini"
    text = engine_ini.read_text(encoding="utf-8")
    for key in ("EditorStartupMap", "GameDefaultMap"):
        import re
        pattern = r"(?m)^" + key + r"=.*$"
        text, count = re.subn(pattern, key + "=" + MAP_PACKAGE, text, count=1)
        require(count == 1, "Could not update " + key + " in DefaultEngine.ini")
    engine_ini.write_text(text, encoding="utf-8")

    report = {
        "status": "EDITOR_MAP_CREATED",
        "map": MAP_PACKAGE,
        "route_waypoints": len(points),
        "obstacles": len(data.get("obstacles", [])),
        "interactables": len(data.get("interactables", [])),
        "player_start": True,
        "training_enemy_spawned": bool(enemy_class),
        "classification": "neutral greybox, not final art or approved level design",
    }
    out = REPO / "Saved/BuildEvidence/W1D2/greybox-build-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W1D2 greybox build: " + json.dumps(report))


main()
