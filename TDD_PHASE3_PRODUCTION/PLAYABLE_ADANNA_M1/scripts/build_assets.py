#!/usr/bin/env python3
"""Build TDD Playable Adanna M1 reusable assets, world data and CPU replay geometry.

This is a production-stage M1 gameplay integration proxy, not a final commercial
character or final Forbidden Forest art pass. It does not overwrite Hall of Posts M1.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE.parents[0]
WEB = BASE / "web_build"
MODEL = BASE / "model"
INTERNAL = WEB / "internal"
sys.path.insert(0, str(ROOT / "TDD_PHASE3_PRODUCTION" / "HALL_OF_POSTS_M1" / "scripts"))
sys.path.insert(0, str(HERE))
import build_hall_of_posts_m1 as m1  # noqa: E402
from gltf_skin import build_adanna_proxy  # noqa: E402

for d in (MODEL, MODEL / "modules", WEB / "assets", WEB / "captures" / "frames", INTERNAL, BASE / "references"):
    d.mkdir(parents=True, exist_ok=True)

SOURCE_FILES = {
    "adanna_master": {
        "name": "CHAR_ADANNA_MASTER_REFERENCE_V001.jpg",
        "drive_id": "1FY3hw3602iB-1405RgUIO3ih2USmck_Y",
        "status": "APPROVED 2026-11-15; master identity reference",
        "role": "approved Adanna identity locks and palette",
    },
    "game_art_bible_moodboard": {
        "name": "REF_ORIGINAL_MOODBOARD_GAME_ART_BIBLE_V001.jpg",
        "drive_id": "1YU_5PoER-i6MxLiUno6G2Qh7-sD6ayiQ",
        "status": "reference moodboard; not standalone production approval",
        "role": "game art-bible visual direction and palette context",
    },
    "forest_establishing": {
        "name": "forest_establishing.jpg",
        "drive_id": "154fUiArdD9lhQeRA3VjQCTOg0xH01lvp",
        "status": "reference; not standalone production approval",
        "role": "Forbidden Forest establishing reference",
    },
    "horn_bill_tree": {
        "name": "ENV_CH01-EXP-006_THE_HORNBILL_TREE_V001.jpg",
        "drive_id": "1zRTQ0olcgTo2Z_aBD6X3YdKUQCjUB-ip",
        "status": "EXPLORATORY; not production approval",
        "role": "buttress-root / canopy reference",
    },
    "duiker_run": {
        "name": "ENV_CH01-EXP-007_THE_DUIKER_RUN_V001.jpg",
        "drive_id": "1Pm7nXmSKgoukgY5qMXPMqzlyc_5ZHtRy",
        "status": "EXPLORATORY; not production approval",
        "role": "laterite path and enclosed route reference",
    },
}

MASTER_PALETTE_HEX = {
    "ABYSS": "#06080D", "GRAPHITE": "#121215", "BROWN_BLACK": "#241916",
    "COOL_CHARCOAL": "#283338", "WARM_GREY": "#403D3E", "MIST_BLUE": "#44525C",
    "PALE_STEEL": "#677A85",
}

# Lifted, source-derived real-time palette. Raw sampled medians are also recorded.
PALETTE_HEX = {
    "FOREST_DARK": "#1D2A21",
    "CANOPY": "#3B432F",
    "CANOPY_LIT": "#596443",
    "LATERITE": "#76523A",
    "LATERITE_PATH": "#8A5A38",
    "BARK": "#5E4930",
    "BARK_DARK": "#35291F",
    "ROCK": "#4B4A42",
    "VEGETATION": "#435A3A",
    "MIST": "#767156",
    "CLOTH": "#DCD6C5",
    "BRONZE": "#9A7039",
    "CORAL": "#B04A33",
    "INDIGO": "#252D50",
    "SKIN": "#433027",
    "LEATHER": "#402A1F",
}


def hexrgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


PALETTE = {k: hexrgb(v) for k, v in PALETTE_HEX.items()}

m1.MATERIALS.update({
    "FOREST_GROUND": {"base": "FOREST_DARK", "roughness": 0.94, "metallic": 0.0, "spec": 0.03},
    "LATERITE_PATH": {"base": "LATERITE_PATH", "roughness": 0.88, "metallic": 0.0, "spec": 0.05},
    "TREE_BARK": {"base": "BARK", "roughness": 0.90, "metallic": 0.0, "spec": 0.04},
    "TREE_ROOT": {"base": "BARK_DARK", "roughness": 0.94, "metallic": 0.0, "spec": 0.02},
    "CANOPY": {"base": "CANOPY", "roughness": 0.96, "metallic": 0.0, "spec": 0.02},
    "BRANCH": {"base": "BARK_DARK", "roughness": 0.92, "metallic": 0.0, "spec": 0.02},
    "ROCK": {"base": "ROCK", "roughness": 0.92, "metallic": 0.0, "spec": 0.05},
    "VEGETATION": {"base": "VEGETATION", "roughness": 0.95, "metallic": 0.0, "spec": 0.02},
    "CLOTH": {"base": "CLOTH", "roughness": 0.92, "metallic": 0.0, "spec": 0.02},
    "WAYMARKER": {"base": "CLOTH", "roughness": 0.80, "metallic": 0.0, "spec": 0.10, "emission": 0.12},
    "GREAT_ROOT": {"base": "BARK", "roughness": 0.90, "metallic": 0.0, "spec": 0.04},
    "INTERACTABLE": {"base": "BRONZE", "roughness": 0.55, "metallic": 0.15, "spec": 0.20, "emission": 0.18},
})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_sources() -> dict:
    out = {}
    for key, meta in SOURCE_FILES.items():
        src = ROOT / "google_drive" / meta["name"]
        dst = BASE / "references" / meta["name"]
        if not src.exists():
            raise FileNotFoundError(f"missing downloaded source: {src}")
        if not dst.exists() or sha256(src) != sha256(dst):
            shutil.copy2(src, dst)
        out[key] = {**meta, "path": str(dst.relative_to(ROOT)), "sha256": sha256(dst), "bytes": dst.stat().st_size}
    return out


def sample_median(image_path: Path, box: tuple[int, int, int, int]) -> list[int]:
    arr = np.asarray(Image.open(image_path).convert("RGB").crop(box)).reshape(-1, 3)
    return [int(v) for v in np.median(arr, axis=0)]


def sample_palette_sources(sources: dict) -> dict:
    f = BASE / "references" / SOURCE_FILES["forest_establishing"]["name"]
    d = BASE / "references" / SOURCE_FILES["duiker_run"]["name"]
    h = BASE / "references" / SOURCE_FILES["horn_bill_tree"]["name"]
    return {
        "forest_establishing": {
            "laterite_median": sample_median(f, (650, 650, 1050, 930)),
            "canopy_median": sample_median(f, (1100, 30, 1650, 350)),
            "mist_median": sample_median(f, (350, 250, 900, 560)),
        },
        "duiker_run": {
            "laterite_median": sample_median(d, (600, 450, 1050, 930)),
            "canopy_median": sample_median(d, (100, 50, 700, 450)),
            "trunk_median": sample_median(d, (700, 150, 1100, 800)),
        },
        "horn_bill_tree": {
            "ivory_light_median": sample_median(h, (100, 50, 700, 450)),
            "bark_median": sample_median(h, (700, 150, 1100, 800)),
        },
        "note": "Medians are source samples, not approved colour specifications; render values are lifted for real-time readability.",
    }


def jitter_colors(rng: np.random.Generator, base: tuple[int, int, int], n: int, amount: int = 7) -> np.ndarray:
    delta = rng.integers(-amount, amount + 1, size=(n, 1))
    warm = np.asarray([1.0, 0.88, 0.76], dtype=float)[None, :]
    arr = np.asarray(base, dtype=float)[None, :] + delta * warm
    return np.uint8(np.clip(arr, 0, 255))


def make_tapered_cylinder(p1, p2, r0: float, r1: float, sections: int = 8, levels: int = 3):
    p1 = np.asarray(p1, dtype=float)
    p2 = np.asarray(p2, dtype=float)
    direction = p2 - p1
    length = float(np.linalg.norm(direction))
    if length < 1e-6:
        raise ValueError("zero-length cylinder")
    axis = direction / length
    ref = np.array([0.0, 1.0, 0.0]) if abs(axis[1]) < 0.88 else np.array([1.0, 0.0, 0.0])
    x = np.cross(ref, axis)
    x /= np.linalg.norm(x)
    y = np.cross(axis, x)
    verts, faces = [], []
    ts = np.linspace(0.0, 1.0, levels)
    for t in ts:
        r = r0 + (r1 - r0) * t
        center = p1 + direction * t
        for i in range(sections):
            theta = 2 * math.pi * i / sections
            verts.append(center + r * (math.cos(theta) * x + math.sin(theta) * y))
    for j in range(levels - 1):
        for i in range(sections):
            a = j * sections + i
            b = j * sections + (i + 1) % sections
            c = (j + 1) * sections + i
            d = (j + 1) * sections + (i + 1) % sections
            faces.extend([[a, b, d], [a, d, c]])
    bottom = len(verts)
    verts.append(p1)
    top = len(verts)
    verts.append(p2)
    last = (levels - 1) * sections
    for i in range(sections):
        faces.append([bottom, (i + 1) % sections, i])
        faces.append([top, last + i, last + (i + 1) % sections])
    return trimesh.Trimesh(vertices=np.asarray(verts), faces=np.asarray(faces), process=False)


def make_icosphere(center, scale, subdivisions: int = 1) -> trimesh.Trimesh:
    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=1.0)
    mesh.apply_scale(np.asarray(scale, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return mesh


def distance_to_route(x: float, y: float, route: list[dict]) -> float:
    best = math.inf
    for a, b in zip(route[:-1], route[1:]):
        vx, vy = b["x"] - a["x"], b["y"] - a["y"]
        l2 = vx * vx + vy * vy or 1.0
        t = max(0.0, min(1.0, ((x - a["x"]) * vx + (y - a["y"]) * vy) / l2))
        qx, qy = a["x"] + vx * t, a["y"] + vy * t
        best = min(best, math.hypot(x - qx, y - qy))
    return best


def generate_world() -> dict:
    rng = np.random.default_rng(20261119)
    route = [
        {"x": 0.0, "y": -18.0, "label": "Threshold"},
        {"x": 0.0, "y": -8.0, "label": "White-cloth boundary"},
        {"x": -2.0, "y": 2.0, "label": "Root way"},
        {"x": 1.0, "y": 12.0, "label": "Stream crossing"},
        {"x": -1.0, "y": 24.0, "label": "Abandoned shrine"},
        {"x": 2.0, "y": 36.0, "label": "Duiker run"},
        {"x": 0.0, "y": 50.0, "label": "Great Root Mother approach"},
    ]
    obstacles = []
    # Camera-collision probe deliberately behind spawn so the shared boom test is deterministic.
    obstacles.append({"id": "CAMERA_PROBE_TREE", "type": "CAMERA_PROBE", "x": 0.0, "y": -21.0,
                      "radius": 1.0, "height": 8.5, "trunkRadius": 0.78, "canopyRadius": 2.2, "seed": 10})
    # Boundary posts and waymarkers are collision obstacles.
    for i, (x, y) in enumerate([(-2.0, -16.0), (2.0, -16.0), (-1.6, 49.0), (1.6, 49.0)]):
        obstacles.append({"id": f"BOUNDARY_POST_{i+1:02d}", "type": "POST", "x": x, "y": y,
                          "radius": 0.16, "height": 2.2, "trunkRadius": 0.11, "canopyRadius": 0.0, "seed": 100 + i})
    obstacles.append({"id": "GREAT_ROOT_MOTHER", "type": "GREAT_TREE", "x": 0.0, "y": 58.0,
                      "radius": 3.2, "height": 18.0, "trunkRadius": 2.55, "canopyRadius": 7.0, "seed": 999})
    # Trees set back from the playable corridor.
    tries, made = 0, 0
    while made < 28 and tries < 800:
        tries += 1
        side = -1 if rng.random() < 0.5 else 1
        x = side * float(rng.uniform(4.6, 16.2))
        y = float(rng.uniform(-14.0, 54.0))
        radius = float(rng.uniform(0.55, 0.95))
        if distance_to_route(x, y, route) < 2.6 + radius:
            continue
        if any(math.hypot(x - o["x"], y - o["y"]) < radius + o["radius"] + 1.2 for o in obstacles):
            continue
        obstacles.append({
            "id": f"FOREST_TREE_{made+1:02d}", "type": "TREE", "x": x, "y": y,
            "radius": radius, "height": float(rng.uniform(8.0, 14.5)),
            "trunkRadius": radius * float(rng.uniform(0.70, 0.92)),
            "canopyRadius": float(rng.uniform(1.8, 3.2)), "seed": int(rng.integers(1000, 900000)),
        })
        made += 1
    # Low rocks can be jumped over; they still exercise ground/obstacle collision.
    made = 0
    tries = 0
    while made < 12 and tries < 400:
        tries += 1
        x = float(rng.uniform(-15.0, 15.0))
        y = float(rng.uniform(-12.0, 52.0))
        radius = float(rng.uniform(0.42, 0.85))
        if distance_to_route(x, y, route) < 2.0 + radius:
            continue
        if any(math.hypot(x - o["x"], y - o["y"]) < radius + o["radius"] + 0.7 for o in obstacles):
            continue
        obstacles.append({
            "id": f"FOREST_ROCK_{made+1:02d}", "type": "ROCK", "x": x, "y": y,
            "radius": radius, "height": float(rng.uniform(0.45, 0.95)),
            "trunkRadius": 0.0, "canopyRadius": 0.0, "seed": int(rng.integers(1000, 900000)),
        })
        made += 1
    return {
        "worldVersion": "PLAYABLE_ADANNA_FOREST_M1_2026-11-19",
        "classification": "neutral gameplay/collision proxy; not approved story dimensions or final level art",
        "source": "Art Bible Forbidden Forest rules, approved Adanna master identity, and source/reference boards listed in source_authority.json",
        "bounds": {"minX": -18.0, "maxX": 18.0, "minY": -26.0, "maxY": 62.0},
        "spawn": {"position": {"x": 0.0, "y": -18.0, "z": 0.0}, "yaw": 0.0},
        "terrain": {"amplitude": 0.04, "frequency": 0.13, "phase": 0.0},
        "character": {
            "radius": 0.34, "eyeHeight": 1.55, "walkSpeed": 2.8, "runSpeed": 5.6,
            "groundAcceleration": 9.0, "airAcceleration": 2.5, "gravity": 18.0,
            "jumpVelocity": 6.4, "turnSpeed": 9.0,
        },
        "camera": {
            "distance": 4.4, "lookSpeed": 2.2, "minPitch": 0.08, "maxPitch": 0.62,
            "collisionPadding": 0.35,
        },
        "route": {"waypoints": route, "pathWidth": 3.4},
        "interactables": [
            {"id": "boundary_waymarker", "label": "White-cloth boundary waymarker", "x": 0.0, "y": -14.5,
             "radius": 1.6, "final": False, "message": "Boundary acknowledged. Follow the white cloth and laterite path."},
            {"id": "great_root_waymarker", "label": "Great Root Mother waymarker", "x": 0.0, "y": 49.0,
             "radius": 2.2, "final": True, "message": "Route complete: Great Root Mother approach acknowledged."},
        ],
        "obstacles": obstacles,
        "decorSeed": 7719,
        "notes": [
            "Great Root Mother is the Chapter 1 navigation landmark and must remain visible from major clearings.",
            "White cloth marks the way; boundary posts are tied with white cloth.",
            "Lowland rainforest: colossal buttress roots, lianas, red laterite soil, constant mist, cool green shade, warm canopy light only.",
            "No tree ferns; exploratory boards are not final production approval.",
        ],
    }


def build_forest_scene(world: dict):
    rng = np.random.default_rng(world["decorSeed"])
    b = m1.SceneBuilder()
    cats = {
        "FOREST_GROUND": m1.Category("FOREST_GROUND", "FOREST_GROUND"),
        "LATERITE_PATH": m1.Category("LATERITE_PATH", "LATERITE_PATH"),
        "TREE_TRUNKS": m1.Category("TREE_TRUNKS", "TREE_BARK"),
        "BUTTRESS_ROOTS": m1.Category("BUTTRESS_ROOTS", "TREE_ROOT"),
        "CANOPY": m1.Category("CANOPY", "CANOPY"),
        "TREE_BRANCHES": m1.Category("TREE_BRANCHES", "BRANCH"),
        "ROCKS": m1.Category("ROCKS", "ROCK"),
        "VEGETATION": m1.Category("VEGETATION", "VEGETATION"),
        "BOUNDARY_POSTS": m1.Category("BOUNDARY_POSTS", "TREE_BARK"),
        "WHITE_CLOTH": m1.Category("WHITE_CLOTH", "CLOTH"),
        "WAYMARKERS": m1.Category("WAYMARKERS", "WAYMARKER"),
        "INTERACTION_RINGS": m1.Category("INTERACTION_RINGS", "INTERACTABLE"),
        "GREAT_ROOT_MOTHER": m1.Category("GREAT_ROOT_MOTHER", "GREAT_ROOT"),
    }

    def add(cat_name: str, mesh, base, amount=6, emission=None, specular=None):
        colors = jitter_colors(rng, base, len(mesh.faces), amount)
        cats[cat_name].add(mesh, colors, emission=emission, specular=specular)

    # Ground grid.
    bx = world["bounds"]
    cell = 4.0
    xs = np.arange(bx["minX"], bx["maxX"], cell)
    ys = np.arange(bx["minY"], bx["maxY"], cell)
    for x0 in xs:
        for y0 in ys:
            q = m1.make_quad((x0, y0, 0.0), (x0 + cell, y0, 0.0),
                             (x0 + cell, y0 + cell, 0.0), (x0, y0 + cell, 0.0))
            base = PALETTE["FOREST_DARK"] if rng.random() < 0.72 else PALETTE["CANOPY"]
            add("FOREST_GROUND", q, base, 4)

    # Laterite route ribbon and darker shoulders.
    route = world["route"]["waypoints"]
    half = world["route"]["pathWidth"] * 0.5
    for a, c in zip(route[:-1], route[1:]):
        vx, vy = c["x"] - a["x"], c["y"] - a["y"]
        length = math.hypot(vx, vy) or 1.0
        nx, ny = -vy / length, vx / length
        for offset, width, key in [(0.0, 1.22, "LATERITE_PATH"), (-1.0, 0.55, "FOREST_GROUND"), (1.0, 0.55, "FOREST_GROUND")]:
            left = half * width
            right = half * width
            p0 = (a["x"] + nx * (offset - left), a["y"] + ny * (offset - left), 0.025)
            p1 = (c["x"] + nx * (offset - left), c["y"] + ny * (offset - left), 0.025)
            p2 = (c["x"] + nx * (offset + right), c["y"] + ny * (offset + right), 0.025)
            p3 = (a["x"] + nx * (offset + right), a["y"] + ny * (offset + right), 0.025)
            q = m1.make_quad(p0, p1, p2, p3)
            if key == "LATERITE_PATH":
                add("LATERITE_PATH", q, PALETTE["LATERITE_PATH"], 7)
            else:
                add("FOREST_GROUND", q, PALETTE["BARK_DARK"], 3)

    # Trees, roots, canopies, rocks and posts from the same gameplay obstacle data.
    for o in world["obstacles"]:
        ox, oy = o["x"], o["y"]
        if o["type"] in ("TREE", "CAMERA_PROBE", "GREAT_TREE"):
            tr = o["trunkRadius"]
            h = o["height"]
            trunk_h = h * (0.74 if o["type"] != "ROCK" else 1.0)
            trunk = make_tapered_cylinder((ox, oy, 0.0), (ox, oy, trunk_h), tr * 1.28, tr * 0.68, 10, 4)
            if o["type"] == "GREAT_TREE":
                add("GREAT_ROOT_MOTHER", trunk, PALETTE["BARK"], 5)
            else:
                add("TREE_TRUNKS", trunk, PALETTE["BARK"], 7)
            root_count = 6 if o["type"] == "GREAT_TREE" else 3
            for k in range(root_count):
                theta = 2 * math.pi * k / root_count + rng.random() * 0.35
                rad = tr * (2.7 if o["type"] == "GREAT_TREE" else 2.1)
                p2 = (ox + math.cos(theta) * rad, oy + math.sin(theta) * rad, 0.03)
                root = make_tapered_cylinder((ox, oy, trunk_h * 0.10), p2, tr * 0.55, 0.045, 6, 3)
                add("BUTTRESS_ROOTS" if o["type"] != "GREAT_TREE" else "GREAT_ROOT_MOTHER", root, PALETTE["BARK_DARK"], 5)
            clusters = 3 if o["type"] == "GREAT_TREE" else 2
            for k in range(clusters):
                cr = o["canopyRadius"] * float(rng.uniform(0.68, 1.05))
                cx = ox + float(rng.uniform(-0.9, 0.9)) * cr * 0.22
                cy = oy + float(rng.uniform(-0.9, 0.9)) * cr * 0.22
                cz = trunk_h + cr * float(rng.uniform(0.35, 0.65))
                canopy = make_icosphere((cx, cy, cz), (cr, cr * 0.82, cr * 0.55), subdivisions=0)
                add("CANOPY", canopy, PALETTE["CANOPY_LIT"] if k == 0 else PALETTE["CANOPY"], 8)
                branch = make_tapered_cylinder((ox, oy, trunk_h * 0.82), (cx, cy, cz - cr * 0.35), tr * 0.13, 0.045, 5, 2)
                add("TREE_BRANCHES", branch, PALETTE["BARK_DARK"], 4)
        elif o["type"] == "ROCK":
            rock = make_icosphere((ox, oy, o["height"] * 0.42),
                                  (o["radius"], o["radius"] * 0.78, o["height"] * 0.55), subdivisions=1)
            add("ROCKS", rock, PALETTE["ROCK"], 8)
        elif o["type"] == "POST":
            post = make_tapered_cylinder((ox, oy, 0.0), (ox, oy, o["height"]), 0.14, 0.10, 7, 3)
            add("BOUNDARY_POSTS", post, PALETTE["BARK_DARK"], 4)
            # White cloth strip tied near the top; no flags or invented bunting.
            side = -1 if ox < 0 else 1
            cloth = m1.make_quad((ox, oy - 0.05, o["height"] * 0.72),
                                  (ox, oy + 0.05, o["height"] * 0.72),
                                  (ox + side * 0.16, oy + 0.02, o["height"] * 0.50),
                                  (ox + side * 0.16, oy - 0.02, o["height"] * 0.50))
            add("WHITE_CLOTH", cloth, PALETTE["CLOTH"], 3)
            band = m1.make_torus(0.145, 0.025, o["height"] * 0.70)
            band.apply_translation((ox, oy, 0.0))
            add("WHITE_CLOTH", band, PALETTE["CLOTH"], 2)

    # Boundary cloth between the two threshold posts.
    cloth_bridge = m1.make_quad((-1.9, -16.0, 1.55), (1.9, -16.0, 1.55),
                                (1.9, -15.94, 1.35), (-1.9, -15.94, 1.35))
    add("WHITE_CLOTH", cloth_bridge, PALETTE["CLOTH"], 3)

    # Interaction rings, visible but restrained.
    for it in world["interactables"]:
        ring = m1.make_torus(it["radius"] * 0.62, 0.035, 0.055)
        ring.apply_translation((it["x"], it["y"], 0.0))
        add("INTERACTION_RINGS", ring, PALETTE["BRONZE"], 3, emission=0.18, specular=0.25)

    # Low vegetation clumps outside the path.
    for i in range(34):
        for _ in range(12):
            x = float(rng.uniform(-16.0, 16.0))
            y = float(rng.uniform(-22.0, 58.0))
            if distance_to_route(x, y, route) > 2.3:
                break
        h = float(rng.uniform(0.45, 1.15))
        for k in range(3):
            theta = rng.random() * 2 * math.pi
            tip = (x + math.cos(theta) * 0.35, y + math.sin(theta) * 0.35, h)
            frond = make_tapered_cylinder((x, y, 0.02), tip, 0.035, 0.006, 5, 2)
            add("VEGETATION", frond, PALETTE["VEGETATION"], 7)

    for cat in cats.values():
        if len(cat.f):
            b.add_category(cat)
    return b, cats


def build_module_pack(cats: dict) -> dict:
    out = MODEL / "modules"
    made = {}
    # Each module is a small named category with one representative instance.
    def export(name: str, cat: m1.Category):
        path = out / f"{name}.glb"
        m1.export_module(cat, name, path)
        made[name] = {"path": str(path.relative_to(ROOT)), "triangles": int(sum(len(f) for f in cat.f))}

    # Tree module: one trunk, two roots, one canopy, one branch from source category slices.
    tree = m1.Category("FOREST_TREE_MODULE", "TREE_BARK")
    # Rebuild a representative compact tree rather than slicing the assembled category.
    trunk = make_tapered_cylinder((0, 0, 0), (0, 0, 8.0), 0.72, 0.42, 9, 3)
    tree.add(trunk, PALETTE["BARK"])
    for k in range(3):
        theta = 2 * math.pi * k / 3
        tree.add(make_tapered_cylinder((0, 0, 0.8), (math.cos(theta) * 1.6, math.sin(theta) * 1.6, 0.03), 0.32, 0.04, 6, 2), PALETTE["BARK_DARK"])
    tree.add(make_icosphere((0, 0, 8.8), (2.2, 1.8, 1.2), 0), PALETTE["CANOPY"])
    export("FOREST_TREE_MODULE", tree)

    rock = m1.Category("FOREST_ROCK_MODULE", "ROCK")
    rock.add(make_icosphere((0, 0, 0.35), (0.8, 0.62, 0.42), 1), PALETTE["ROCK"])
    export("FOREST_ROCK_MODULE", rock)

    post = m1.Category("FOREST_BOUNDARY_POST_MODULE", "TREE_BARK")
    post.add(make_tapered_cylinder((0, 0, 0), (0, 0, 2.2), 0.14, 0.10, 7, 3), PALETTE["BARK_DARK"])
    band = m1.make_torus(0.145, 0.025, 1.55)
    post.add(band, PALETTE["CLOTH"])
    export("FOREST_BOUNDARY_POST_MODULE", post)

    fern = m1.Category("FOREST_FERN_MODULE", "VEGETATION")
    for k in range(3):
        theta = 2 * math.pi * k / 3
        fern.add(make_tapered_cylinder((0, 0, 0.02), (math.cos(theta) * 0.35, math.sin(theta) * 0.35, 0.9), 0.035, 0.006, 5, 2), PALETTE["VEGETATION"])
    export("FOREST_FERN_MODULE", fern)

    marker = m1.Category("FOREST_WAYMARKER_MODULE", "WAYMARKER")
    marker.add(m1.make_torus(0.8, 0.035, 0.055), PALETTE["CLOTH"])
    export("FOREST_WAYMARKER_MODULE", marker)

    great = m1.Category("FOREST_GREAT_TREE_MODULE", "GREAT_ROOT")
    great.add(make_tapered_cylinder((0, 0, 0), (0, 0, 13.5), 3.2, 1.7, 12, 4), PALETTE["BARK"])
    for k in range(6):
        theta = 2 * math.pi * k / 6
        great.add(make_tapered_cylinder((0, 0, 1.4), (math.cos(theta) * 6.5, math.sin(theta) * 6.5, 0.03), 1.3, 0.12, 7, 3), PALETTE["BARK_DARK"])
    great.add(make_icosphere((0, 0, 15.0), (6.5, 5.3, 3.4), 0), PALETTE["CANOPY"])
    export("FOREST_GREAT_TREE_MODULE", great)
    return made


def parse_glb_json(path: Path) -> dict:
    data = path.read_bytes()
    if data[:4] != b"glTF":
        raise ValueError("not GLB")
    json_len = int.from_bytes(data[12:16], "little")
    return json.loads(data[20 : 20 + json_len].decode("utf-8"))


def main() -> int:
    started = time.time()
    print("[M1] copying and hashing sources", flush=True)
    sources = copy_sources()
    palette_samples = sample_palette_sources(sources)
    (BASE / "source_authority.json").write_text(json.dumps({
        "classification": "targeted game-production state recovery; not a Phase 2 re-audit",
        "sources": sources,
        "phase1_restrictions": [
            "Adanna V003 BACK/LEFT_SIDE are PRESERVE/UNAPPROVED; no new version, mirror, armlet move, blade insertion, pose/geometry/likeness/costume/baldric change.",
            "V013 item-5 NOT DONE; waiver is internal exploratory only.",
            "H3/VR-011 Landing and Field of Cloth retain D9/RQ-01 no visual release.",
            "Six visual-release-only passes are not production-authoritative designs.",
            "Rejected/superseded artwork, failed corrections, and limited internal studies are not production authority.",
        ],
        "recovered_engine_state": {
            "uproject_found": False, "uasset_found": False, "umap_found": False,
            "unreal_engine_binary_found": False, "unreal_version_found": False,
            "playable_project_found": False, "packaged_build_found": False,
            "native_character_model_found": False, "native_animation_found": False,
            "native_rig_found": False, "gameplay_system_found": False,
        },
        "precise_blocker": "Unreal Engine installation/version and owner-studio hardware profile are absent from this sandbox; UE import/compile/package cannot be verified here.",
    }, indent=2), encoding="utf-8")

    print("[M1] generating world and forest geometry", flush=True)
    world = generate_world()
    (WEB / "world.json").write_text(json.dumps(world, indent=2), encoding="utf-8")
    (BASE / "world.json").write_text(json.dumps(world, indent=2), encoding="utf-8")
    builder, cats = build_forest_scene(world)
    V, F, C, E, S = builder.arrays()
    np.savez_compressed(INTERNAL / "render_scene.npz", V=V, F=F, C=C, E=E, S=S)
    m1.write_glb(builder.scene, MODEL / "forbidden_forest_m1.glb")
    builder.combined_mesh().export(MODEL / "forbidden_forest_m1.obj")
    modules = build_module_pack(cats)

    print("[M1] generating skinned Adanna technical proxy", flush=True)
    adanna_meta = {
        "drive_id": sources["adanna_master"]["drive_id"],
        "sha256": sources["adanna_master"]["sha256"],
        "status": sources["adanna_master"]["status"],
        "art_bible_register": "CHARACTER_DESIGN_REGISTER.md: master reference APPROVED; 7.5 heads, athletic fighter, identity locks retained",
    }
    character = build_adanna_proxy(
        MODEL / "adanna_m1_technical_proxy.glb",
        MODEL / "adanna_m1_technical_proxy.obj",
        MODEL / "adanna_m1_character_rig.json",
        INTERNAL / "character_parts.json",
        BASE / "references" / SOURCE_FILES["adanna_master"]["name"],
        adanna_meta,
    )
    # Browser assets are copies, keeping model/ as the canonical asset folder.
    shutil.copy2(MODEL / "forbidden_forest_m1.glb", WEB / "assets" / "forbidden_forest_m1.glb")
    shutil.copy2(MODEL / "adanna_m1_technical_proxy.glb", WEB / "assets" / "adanna_m1_technical_proxy.glb")

    print("[M1] reopening and validating assets", flush=True)
    forest_scene = trimesh.load(MODEL / "forbidden_forest_m1.glb", force="scene")
    forest_geom = forest_scene.to_geometry()
    forest_obj = trimesh.load(MODEL / "forbidden_forest_m1.obj", force="mesh")
    adanna_obj = trimesh.load(MODEL / "adanna_m1_technical_proxy.obj", force="mesh")
    char_gltf = parse_glb_json(MODEL / "adanna_m1_technical_proxy.glb")
    asset_report = {
        "forest_glb_nodes": list(forest_scene.geometry),
        "forest_glb_vertices": int(len(forest_geom.vertices)),
        "forest_glb_triangles": int(len(forest_geom.faces)),
        "forest_obj_vertices": int(len(forest_obj.vertices)),
        "forest_obj_triangles": int(len(forest_obj.faces)),
        "adanna_glb_skins": len(char_gltf.get("skins", [])),
        "adanna_glb_joints": len(char_gltf.get("skins", [{}])[0].get("joints", [])),
        "adanna_glb_animations": [a.get("name") for a in char_gltf.get("animations", [])],
        "adanna_glb_nodes": len(char_gltf.get("nodes", [])),
        "adanna_obj_vertices": int(len(adanna_obj.vertices)),
        "adanna_obj_triangles": int(len(adanna_obj.faces)),
        "modules": modules,
    }
    (BASE / "ASSET_REOPEN_REPORT.json").write_text(json.dumps(asset_report, indent=2), encoding="utf-8")

    materials = {
        "approved_master_palette": MASTER_PALETTE_HEX,
        "realtime_palette": PALETTE_HEX,
        "source_samples": palette_samples,
        "material_intent": {k: {kk: vv for kk, vv in v.items()} for k, v in m1.MATERIALS.items() if k.startswith(("FOREST_", "LATERITE_", "TREE_", "CANOPY", "BRANCH", "ROCK", "VEGETATION", "CLOTH", "WAYMARKER", "GREAT_ROOT", "INTERACTABLE"))},
        "note": "Palette-derived PBR intent only; no calibrated texture maps, final groom, facial rig or production topology is claimed.",
    }
    (BASE / "materials.json").write_text(json.dumps(materials, indent=2), encoding="utf-8")
    shutil.copy2(BASE / "materials.json", WEB / "assets" / "materials.json")

    # Manifest state is derived from files actually present; do not claim a UE project,
    # package, browser render or live build merely because the scaffold was planned.
    ue_source_files = [
        BASE / "ue_project" / "TDD_GAME.uproject",
        BASE / "ue_project" / "Config" / "DefaultEngine.ini",
        BASE / "ue_project" / "Config" / "DefaultInput.ini",
        BASE / "ue_project" / "Source" / "TDD_GAME.Target.cs",
        BASE / "ue_project" / "Source" / "TDD_GAMEEditor.Target.cs",
        BASE / "ue_project" / "Source" / "TDD_GAME" / "TDD_GAME.Build.cs",
        BASE / "ue_project" / "Source" / "TDD_GAME" / "Private" / "TDDForbiddenForestGameMode.cpp",
        BASE / "ue_project" / "Source" / "TDD_GAME" / "Private" / "TDDForbiddenForestLevel.cpp",
        BASE / "ue_project" / "Source" / "TDD_GAME" / "Private" / "TDDAdannaProxyCharacter.cpp",
        BASE / "ue_project" / "Source" / "TDD_GAME" / "Public" / "TDDWorldData.h",
    ]
    ue_source_created = all(p.is_file() and p.stat().st_size > 0 for p in ue_source_files)
    live_report_path = WEB / "test" / "live_build_report.json"
    live_report = json.loads(live_report_path.read_text(encoding="utf-8")) if live_report_path.is_file() else None
    live_checks = len(live_report.get("checks", [])) if live_report else 0
    live_pass = bool(live_report and live_report.get("overallPass") and all(c.get("ok") for c in live_report.get("checks", [])))
    capture_manifest_path = WEB / "captures" / "capture_manifest.json"
    capture_manifest = json.loads(capture_manifest_path.read_text(encoding="utf-8")) if capture_manifest_path.is_file() else None
    captures_verified = bool(
        capture_manifest
        and capture_manifest.get("mp4_status") == "written"
        and (WEB / "captures" / "frames").is_dir()
        and len(list((WEB / "captures" / "frames").glob("frame_*.png"))) >= int(capture_manifest.get("frame_count", 0))
    )
    directly_launchable = bool(
        ue_source_created
        and (WEB / "index.html").is_file()
        and (WEB / "server.mjs").is_file()
        and (WEB / "test" / "integration_report.json").is_file()
        and live_pass
        and captures_verified
    )
    live_verification = (
        f"{live_checks}/{live_checks} static/live HTTP, local ES-module, asset, capture, UE source-file and durable-record checks passed; WebGL rendering not automated"
        if live_pass
        else "live build verification pending; do not claim directly launchable browser build"
    )

    uv_validation_path = MODEL / "adanna_m1_uv_validation.json"
    uv_validation = json.loads(uv_validation_path.read_text(encoding="utf-8")) if uv_validation_path.is_file() else None
    uv_handoff_files = [
        MODEL / "adanna_m1_technical_proxy_uv.glb",
        MODEL / "adanna_m1_uv_atlas.png",
        MODEL / "adanna_m1_uv_layout.png",
        MODEL / "adanna_m1_collision_proxy.obj",
        MODEL / "adanna_m1_ue_import_manifest.json",
        uv_validation_path,
        WEB / "captures" / "adanna_m1_uv_atlas.png",
        WEB / "captures" / "adanna_m1_uv_layout.png",
        BASE.parents[1] / "OWNER_STUDIO_UNREAL_REQUEST.md",
        BASE / "ue_project" / "Tools" / "TDD_M1_Unreal_Setup_macOS.py",
        BASE / "ue_project" / "README_MACOS_UE58.md",
        BASE / "ue_project" / "Tools" / "tdd_m1_macos_audit.json",
    ]
    uv_handoff_verified = bool(
        uv_validation
        and uv_validation.get("overallPass")
        and all(p.is_file() and p.stat().st_size > 0 for p in uv_handoff_files)
    )
    uv_handoff_status = "COMPLETED AND VERIFIED" if uv_handoff_verified else "PRODUCED — NOT YET VERIFIED"
    uv_checks = (
        f"{uv_validation.get('checksPassed', 0)}/{uv_validation.get('checksTotal', 0)} local UV/material/collision checks passed"
        if uv_validation
        else "local UV/material/collision validation pending"
    )

    manifest = {
        "milestone": "M1 — First playable character: Adanna gameplay proxy in Forbidden Forest blockout",
        "date": "2026-11-19",
        "classification": "real-time gameplay integration milestone; NOT final commercial character, final environment, canon approval, or verified UE package",
        "preserved": {
            "hall_of_posts_m1": "TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/ unchanged",
            "phase1_authority": "retained; see source_authority.json",
        },
        "recovered_state": {
            "existing_unreal_project": False,
            "existing_engine_version": None,
            "existing_playable_build": False,
            "existing_native_character_assets": False,
            "existing_native_animations_rigs_gameplay": False,
            "usable_authority": "approved Adanna master reference, Art Bible forest rules, scene/location registers, exploratory/reference boards, Hall of Posts M1 pipeline",
        },
        "geometry": {
            "forest_vertices": int(len(V)), "forest_triangles": int(len(F)),
            "forest_nodes": [n["node"] for n in builder.nodes],
            "character": character,
            "obstacles": len(world["obstacles"]), "interactables": len(world["interactables"]),
            "route_waypoints": len(world["route"]["waypoints"]),
        },
        "outputs": {
            "ue_source_scaffold": "ue_project/",
            "ue_source_state_readme": "ue_project/UE_SOURCE_STATE.md",
            "web_playable_build": "web_build/index.html",
            "web_server": "web_build/server.mjs",
            "world": "web_build/world.json",
            "forest_glb": "model/forbidden_forest_m1.glb",
            "forest_obj": "model/forbidden_forest_m1.obj",
            "character_glb": "model/adanna_m1_technical_proxy.glb",
            "character_obj": "model/adanna_m1_technical_proxy.obj",
            "character_rig": "model/adanna_m1_character_rig.json",
            "modules": "model/modules/",
            "integration_report": "web_build/test/integration_report.json",
            "live_build_report": "web_build/test/live_build_report.json",
            "captures": "web_build/captures/",
            "capture_manifest": "web_build/captures/capture_manifest.json",
            "milestone_tracker": "../../PLAYABLE_MILESTONE_TRACKER.md",
            "owner_request": "../../OWNER_STUDIO_UNREAL_REQUEST.md",
            "ue_setup_helper_macos": "ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py",
            "ue_setup_helper_superseded": "ue_project/Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py",
            "macos_runbook": "ue_project/README_MACOS_UE58.md",
            "macos_static_audit": "ue_project/Tools/tdd_m1_macos_audit.json",
            "adanna_uv_glb": "model/adanna_m1_technical_proxy_uv.glb",
            "adanna_uv_atlas": "model/adanna_m1_uv_atlas.png",
            "adanna_uv_layout": "model/adanna_m1_uv_layout.png",
            "adanna_collision_proxy": "model/adanna_m1_collision_proxy.obj",
            "adanna_ue_import_manifest": "model/adanna_m1_ue_import_manifest.json",
            "adanna_uv_validation": "model/adanna_m1_uv_validation.json",
        },
        "unreal": {
            "project_source_state_created": ue_source_created,
            "source_state_classification": "new provisional runtime-procedural source scaffold; NO recovered existing Unreal project or version",
            "engine_association": "5.8 (owner-verified installed engine); BuildSettingsVersion.V7; EngineIncludeOrderVersion.Unreal5_8",
            "owner_target_environment": {
                "machine": "Apple M4 Mac",
                "memory": "16 GB",
                "os": "macOS 27.2.1",
                "architecture": "ARM64 / Apple Silicon",
                "engine": "Unreal Engine 5.8",
                "status": "supplied by owner; no Windows target assumed",
            },
            "toolchain_requirement": "Xcode 26.0 minimum, 26.1.1 recommended; Xcode 26.4 incompatible with UE 5.8; macOS SDK via xcrun; Metal 1.2 class GPU",
            "macos_runbook": "ue_project/README_MACOS_UE58.md",
            "static_compatibility_audit": "ue_project/Tools/tdd_m1_macos_audit.json",
            "owner_setup_helper_macos": "ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py",
            "superseded_helper_preserved": "ue_project/Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py",
            "source_files_verified": ue_source_created,
            "native_uasset_umap_import_verified": False,
            "compile_verified": False,
            "real_time_ue_test_verified": False,
            "package_verified": False,
            "precise_blocker": "Owner macOS/UE 5.8 environment is known, but this sandbox has no Unreal binary and no access to the Mac. Compile/PIE/cook/package must be executed and recorded by the owner.",
        },
        "web_build": {
            "directly_launchable": directly_launchable,
            "engine": "Three.js 0.187.0 vendored locally, including three.core.js; no external CDN dependency",
            "shared_simulation": "web_build/game.js used by browser, Node integration test and CPU replay captures",
            "live_server": "node server.mjs, bound to 0.0.0.0 for Arena live preview",
            "verification": live_verification,
            "automated_webgl_render_verified": False,
            "captures_verified": captures_verified,
        },
        "adanna_uv_material_collision_handoff": {
            "status": uv_handoff_status,
            "classification": "PROVISIONAL — AWAITING CREATIVE APPROVAL; UE import remains BLOCKED — OWNER-STUDIO DEPENDENCY",
            "local_validation": uv_checks,
            "scope": "technical UV0/material-atlas/collision import preparation; NOT final character, final textures, final dimensions, native UE asset, compile, PIE, cook or package",
            "source_glb_preserved": "model/adanna_m1_technical_proxy.glb",
            "owner_request": "../../OWNER_STUDIO_UNREAL_REQUEST.md",
            "ue_setup_helper_macos": "ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py",
            "ue_setup_helper_superseded": "ue_project/Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py",
            "macos_runbook": "ue_project/README_MACOS_UE58.md",
            "macos_static_audit": "ue_project/Tools/tdd_m1_macos_audit.json",
        },
        "status_classification": {
            "targeted_production_state_recovery": "COMPLETED AND VERIFIED",
            "hall_of_posts_m1_preserved": "COMPLETED AND VERIFIED",
            "shared_simulation_and_replay_captures": "COMPLETED AND VERIFIED" if captures_verified else "PRODUCED — NOT YET VERIFIED",
            "browser_static_live_delivery": "COMPLETED AND VERIFIED" if directly_launchable else "PRODUCED — NOT YET VERIFIED",
            "browser_gameplay_implementation": "TECHNICALLY DEMONSTRATED — NOT INTEGRATED",
            "adanna_uv_material_collision_handoff": uv_handoff_status,
            "ue_source_scaffold": "PRODUCED — NOT YET VERIFIED" if ue_source_created else "NOT STARTED",
            "ue_project_owned_umap": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "ue_compile_pie_cook_package": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "final_adanna_and_forbidden_forest": "BLOCKED — CREATIVE APPROVAL",
            "m3_m4_gameplay": "NOT STARTED",
        },
        "approval_dependencies": [
            "CD/Research authority for final Adanna turnaround, dimensions, hair/groom, costume technical interpretation and facial rig.",
            "CD film/game canon and consultant review for final Forbidden Forest geography, cultural details and landmark use.",
            "Unreal Engine version/installation and owner-studio hardware profile for verified UE import, compile, cook and package.",
        ],
        "next_milestone": "M2: replace proxy with approved game-ready Adanna and production forest kit; then UE compile/cook/package on owner hardware.",
    }
    (BASE / "production_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.copy2(BASE / "production_manifest.json", WEB / "assets" / "production_manifest.json")
    print(f"[M1] assets complete in {time.time() - started:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
