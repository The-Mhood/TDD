#!/usr/bin/env python3
"""Build the TDD Hall of Posts M1 H2/H3 modular blockout and CPU render proof.

Source authority: ENV_LAST_DAUGHTER_ANCESTRAL_REALM_HALL_OF_POSTS_V004.jpg
(Drive ID 1MHCd25z3x-cfBUf-eoCJvDLqwvYj9Ins, approved environment design,
canon pending). All geometry is a neutral technical proxy, not approved canon,
cultural evidence, or measured production dimensions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial

ROOT = Path(__file__).resolve().parents[3]
M1 = Path(__file__).resolve().parents[1]
SOURCE_NAME = "ENV_LAST_DAUGHTER_ANCESTRAL_REALM_HALL_OF_POSTS_V004.jpg"
DOWNLOADED_SOURCE = ROOT / "google_drive" / SOURCE_NAME
REFERENCE = M1 / "references" / SOURCE_NAME

for d in ("model", "model/modules", "renders", "renders/turntable_frames", "references", "docs"):
    (M1 / d).mkdir(parents=True, exist_ok=True)

PALETTE_HEX = {
    "P0_DEEP": "#0F0B0A",
    "P1_CHAR": "#19100D",
    "P2_WOOD": "#1E1512",
    "P3_EARTH_DARK": "#201A18",
    "P4_LATERITE": "#2C1C17",
    "P5_WORN_EARTH": "#332622",
    "P6_PALE": "#645956",
}


def hexrgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


PALETTE = {k: hexrgb(v) for k, v in PALETTE_HEX.items()}

MATERIALS = {
    "EARTH_FLOOR": {"base": "P5_WORN_EARTH", "roughness": 0.88, "metallic": 0.0, "spec": 0.10},
    "WET_EARTH_AISLE": {"base": "P3_EARTH_DARK", "roughness": 0.43, "metallic": 0.0, "spec": 0.55},
    "EARTHEN_WALL": {"base": "P4_LATERITE", "roughness": 0.90, "metallic": 0.0, "spec": 0.04},
    "EARTHEN_BENCH": {"base": "P5_WORN_EARTH", "roughness": 0.86, "metallic": 0.0, "spec": 0.08},
    "HARDWOOD_POST": {"base": "P2_WOOD", "roughness": 0.82, "metallic": 0.0, "spec": 0.10},
    "CARVED_BAND": {"base": "P5_WORN_EARTH", "roughness": 0.76, "metallic": 0.0, "spec": 0.12},
    "ROOF_BEAM": {"base": "P1_CHAR", "roughness": 0.86, "metallic": 0.0, "spec": 0.06},
    "THATCH": {"base": "P1_CHAR", "roughness": 0.94, "metallic": 0.0, "spec": 0.02},
    "FIBRE_LASHING": {"base": "P6_PALE", "roughness": 0.92, "metallic": 0.0, "spec": 0.02},
    "STOOL_WOOD": {"base": "P3_EARTH_DARK", "roughness": 0.78, "metallic": 0.0, "spec": 0.10},
    "EXPOSURE_CARD": {"base": "P6_PALE", "roughness": 1.0, "metallic": 0.0, "spec": 0.0, "emission": 0.45},
}


def jitter(rng: np.random.Generator, base: tuple[int, int, int], amount: int = 7) -> np.ndarray:
    # Luminance-preserving variation: dark earth/wood must not drift into rainbow hues.
    delta = float(rng.integers(-amount, amount + 1))
    warm = np.asarray([1.0, 0.88, 0.78], dtype=float)
    arr = np.asarray(base, dtype=float) + delta * warm
    return np.clip(arr, 0, 255).astype(np.uint8)


def uniform_face_colors(n: int, color: tuple[int, int, int]) -> np.ndarray:
    return np.tile(np.asarray(color, dtype=np.uint8), (n, 1))


class Category:
    """Named production category with render-facing per-face colour/emission/spec arrays."""

    def __init__(self, name: str, material_key: str):
        self.name = name
        self.material_key = material_key
        self.material = MATERIALS[material_key]
        self.v: list[np.ndarray] = []
        self.f: list[np.ndarray] = []
        self.c: list[np.ndarray] = []
        self.e: list[np.ndarray] = []
        self.s: list[np.ndarray] = []

    @staticmethod
    def _param(value, n: int, default: float) -> np.ndarray:
        if value is None:
            return np.full(n, default, dtype=float)
        arr = np.asarray(value, dtype=float)
        if arr.ndim == 0:
            return np.full(n, float(arr), dtype=float)
        return np.broadcast_to(arr.reshape(-1), (n,)).astype(float).copy()

    def add(self, mesh: trimesh.Trimesh, color, emission=None, specular=None) -> None:
        vertices = np.asarray(mesh.vertices, dtype=float)
        faces = np.asarray(mesh.faces, dtype=np.int64)
        if faces.ndim != 2 or faces.shape[1] != 3:
            raise ValueError(f"{self.name}: expected triangular faces, got {faces.shape}")
        offset = sum(len(v) for v in self.v)
        colors = np.asarray(color, dtype=np.uint8)
        if colors.ndim == 1:
            colors = np.tile(colors, (len(faces), 1))
        colors = colors.reshape(-1, colors.shape[-1])[:, :3]
        if len(colors) != len(faces):
            raise ValueError(f"{self.name}: {len(colors)} colours for {len(faces)} faces")
        self.v.append(vertices)
        self.f.append(faces + offset)
        self.c.append(colors.astype(np.uint8))
        self.e.append(self._param(emission, len(faces), self.material.get("emission", 0.0)))
        self.s.append(self._param(specular, len(faces), self.material.get("spec", 0.0)))

    def arrays(self):
        if not self.v:
            raise ValueError(f"Category {self.name} is empty")
        return (
            np.vstack(self.v),
            np.vstack(self.f),
            np.vstack(self.c),
            np.concatenate(self.e),
            np.concatenate(self.s),
        )

    def to_trimesh(self) -> trimesh.Trimesh:
        v, f, _, _, _ = self.arrays()
        return trimesh.Trimesh(vertices=v, faces=f, process=False)


class SceneBuilder:
    def __init__(self):
        self.scene = trimesh.Scene()
        self.categories: list[Category] = []
        self.v: list[np.ndarray] = []
        self.f: list[np.ndarray] = []
        self.c: list[np.ndarray] = []
        self.e: list[np.ndarray] = []
        self.s: list[np.ndarray] = []
        self.nodes: list[dict] = []

    def add_category(self, cat: Category) -> None:
        v, f, c, e, s = cat.arrays()
        mesh = trimesh.Trimesh(vertices=v, faces=f, process=False)
        base = np.round(c.mean(axis=0)).astype(int).tolist()
        emission = float(np.clip(e.mean(), 0.0, 1.0))
        emissive_factor = [min(1.0, emission * x / 255.0) for x in base] if emission > 0 else None
        pbr = PBRMaterial(
            name=cat.name,
            baseColorFactor=[*base, 255],
            metallicFactor=float(cat.material.get("metallic", 0.0)),
            roughnessFactor=float(cat.material.get("roughness", 0.9)),
            emissiveFactor=emissive_factor,
            doubleSided=True,
        )
        mesh.visual = TextureVisuals(material=pbr)
        self.scene.add_geometry(mesh, node_name=cat.name, geom_name=cat.name)
        offset = sum(len(x) for x in self.v)
        self.v.append(v)
        self.f.append(f + offset)
        self.c.append(c)
        self.e.append(e)
        self.s.append(s)
        self.categories.append(cat)
        self.nodes.append(
            {
                "node": cat.name,
                "material_key": cat.material_key,
                "vertices": int(len(v)),
                "triangles": int(len(f)),
                "baseColorRGB": base,
                "pbr_roughness": pbr.roughnessFactor,
                "pbr_metallic": pbr.metallicFactor,
                "render_only": cat.name == "RENDER_EXPOSURE_CARDS",
            }
        )

    def arrays(self):
        return (
            np.vstack(self.v),
            np.vstack(self.f),
            np.vstack(self.c),
            np.concatenate(self.e),
            np.concatenate(self.s),
        )

    def combined_mesh(self) -> trimesh.Trimesh:
        v, f, _, _, _ = self.arrays()
        return trimesh.Trimesh(vertices=v, faces=f, process=False)


def make_box(center, extents) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return mesh


def make_quad(v0, v1, v2, v3) -> trimesh.Trimesh:
    vertices = np.asarray([v0, v1, v2, v3], dtype=float)
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)


def make_beam(p1, p2, radius: float, sections: int = 8) -> trimesh.Trimesh:
    p1 = np.asarray(p1, dtype=float)
    p2 = np.asarray(p2, dtype=float)
    direction = p2 - p1
    length = float(np.linalg.norm(direction))
    z = direction / length
    ref = np.array([0.0, 1.0, 0.0]) if abs(z[1]) < 0.88 else np.array([1.0, 0.0, 0.0])
    x = np.cross(ref, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    transform = np.eye(4)
    transform[:3, 0] = x
    transform[:3, 1] = y
    transform[:3, 2] = z
    transform[:3, 3] = (p1 + p2) * 0.5
    mesh = trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    mesh.apply_transform(transform)
    return mesh


def make_torus(major_radius: float, minor_radius: float, z: float) -> trimesh.Trimesh:
    mesh = trimesh.creation.torus(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_sections=20,
        minor_sections=6,
    )
    mesh.apply_translation([0.0, 0.0, z])
    return mesh


def make_tapered_post(height: float = 7.55, r0: float = 0.86, r1: float = 0.67,
                      sections: int = 20, levels: int = 16):
    rng = np.random.default_rng(20261119)
    wood = np.asarray(PALETTE["P2_WOOD"], dtype=float)
    dark = np.asarray(PALETTE["P1_CHAR"], dtype=float)
    band_light = np.asarray(PALETTE["P5_WORN_EARTH"], dtype=float) * 0.78
    vertices: list[list[float]] = []
    faces: list[list[int]] = []
    colors: list[np.ndarray] = []
    z_values = np.linspace(0.0, height, levels)
    for j, z in enumerate(z_values):
        for i in range(sections):
            theta = 2.0 * math.pi * i / sections
            base_r = r0 + (r1 - r0) * (z / height)
            gnarl = 1.0 + 0.026 * math.sin(3 * theta + j * 0.63) + 0.018 * math.cos(7 * theta - j * 0.31)
            r = base_r * gnarl
            vertices.append([r * math.cos(theta), r * math.sin(theta), float(z)])
    band_rows = {3, 4, 5}
    for j in range(levels - 1):
        for i in range(sections):
            a = j * sections + i
            b = j * sections + (i + 1) % sections
            c = (j + 1) * sections + i
            d = (j + 1) * sections + (i + 1) % sections
            faces.extend([[a, b, d], [a, d, c]])
            if j in band_rows:
                # Non-iconographic chevron-like alternation: mass only, not a final motif.
                tone = band_light if (i + j) % 3 else dark
                shade = tone * (0.93 + 0.06 * ((i + j) % 2))
            else:
                delta = float(rng.integers(-3, 4))
                shade = wood + delta * np.asarray([1.0, 0.86, 0.74])
            shade = np.clip(shade, 0, 255).astype(np.uint8)
            colors.extend([shade, shade])
    bottom_center = len(vertices)
    vertices.append([0.0, 0.0, 0.0])
    top_center = len(vertices)
    vertices.append([0.0, 0.0, height])
    cap_color = np.asarray(PALETTE["P0_DEEP"], dtype=np.uint8)
    last = (levels - 1) * sections
    for i in range(sections):
        faces.append([bottom_center, (i + 1) % sections, i])
        colors.append(cap_color)
        faces.append([top_center, last + i, last + (i + 1) % sections])
        colors.append(cap_color)
    mesh = trimesh.Trimesh(vertices=np.asarray(vertices), faces=np.asarray(faces), process=False)
    return mesh, np.asarray(colors, dtype=np.uint8)


def build_post_master() -> Category:
    cat = Category("HALL_POST_MODULE", "HARDWOOD_POST")
    trunk, trunk_colors = make_tapered_post()
    cat.add(trunk, trunk_colors)
    wood = PALETTE["P1_CHAR"]
    fibre = PALETTE["P1_CHAR"]
    # Forked hardwood head: two branches, no stone or metal column language.
    cat.add(make_beam((0, 0, 6.65), (-0.62, 0, 7.85), 0.24, 10), wood)
    cat.add(make_beam((0, 0, 6.65), (0.62, 0, 7.85), 0.24, 10), wood)
    # Horizontal lashings at the fork and carved-band boundaries.
    for z, major in ((6.62, 0.76), (6.86, 0.73), (2.05, 0.79), (2.42, 0.78)):
        cat.add(make_torus(major, 0.045, z), fibre, specular=0.02)
    return cat


def transform_mesh(mesh: trimesh.Trimesh, translate, rotation_z: float = 0.0) -> trimesh.Trimesh:
    out = mesh.copy()
    angle = float(rotation_z)
    transform = np.eye(4)
    c, s = math.cos(angle), math.sin(angle)
    transform[:3, 0] = [c, s, 0]
    transform[:3, 1] = [-s, c, 0]
    transform[:3, 2] = [0, 0, 1]
    transform[:3, 3] = np.asarray(translate, dtype=float)
    out.apply_transform(transform)
    return out


def wall_bay_pieces(side: float, y0: float, length: float = 6.0):
    x = side * 10.25
    return [
        make_box((x, y0 + length / 2, 0.40), (0.38, length, 0.80)),
        make_box((x, y0 + length / 2, 3.08), (0.38, length, 0.64)),
        make_box((x, y0 + 0.62, 1.78), (0.38, 1.24, 2.20)),
        make_box((x, y0 + length - 0.62, 1.78), (0.38, 1.24, 2.20)),
    ]


def bench_bay_pieces(side: float, y0: float, length: float = 6.0):
    return [
        make_box((side * 6.65, y0 + length / 2, 0.25), (4.55, length - 0.35, 0.50)),
        make_box((side * 7.00, y0 + length / 2, 0.66), (3.80, length - 0.55, 0.32)),
        make_box((side * 7.35, y0 + length / 2, 0.92), (3.00, length - 0.75, 0.20)),
    ]


def roof_bay_pieces(y0: float, length: float = 6.0):
    quads = []
    beams = []
    eave_x = 10.5
    ridge_z = 9.45
    eave_z = 6.25
    # Thatch strips on both slopes.
    for side in (-1, 1):
        strips = 8
        for k in range(strips):
            t0, t1 = k / strips, (k + 1) / strips
            x0, x1 = side * eave_x * (1 - t0), side * eave_x * (1 - t1)
            z0, z1 = eave_z + (ridge_z - eave_z) * t0 + 0.06, eave_z + (ridge_z - eave_z) * t1 + 0.06
            quads.append(make_quad((x0, y0, z0), (x0, y0 + length, z0),
                                   (x1, y0 + length, z1), (x1, y0, z1)))
    for side in (-1, 1):
        beams.append(make_beam((side * eave_x, y0, eave_z), (0, y0, ridge_z), 0.115, 6))
        beams.append(make_beam((side * eave_x * 0.66, y0, eave_z + (ridge_z - eave_z) * 0.34),
                               (0, y0 + length, ridge_z), 0.075, 6))
    return quads, beams


def stool_pieces(center=(0.0, -7.0, 0.0)):
    x, y, z = center
    pieces = [make_box((x, y, z + 0.56), (0.92, 0.62, 0.13))]
    for dx, dy in ((-0.34, -0.21), (0.34, -0.21), (0.0, 0.24)):
        pieces.append(make_beam((x + dx, y + dy, z + 0.03),
                                (x + dx * 0.86, y + dy * 0.86, z + 0.51), 0.065, 7))
    return pieces


def build_scene():
    builder = SceneBuilder()
    rng = np.random.default_rng(451115)
    post_positions: list[tuple[float, float]] = []

    # Floor: subtle earthen grid; central aisle carries the approved wet-floor note.
    floor = Category("EARTH_FLOOR", "EARTH_FLOOR")
    aisle = Category("WET_AISLE", "WET_EARTH_AISLE")
    xs = np.arange(-10.5, 10.5, 0.75)
    ys = np.arange(-20.0, 42.0, 1.0)
    for x0, x1 in zip(xs[:-1], xs[1:]):
        for y0, y1 in zip(ys[:-1], ys[1:]):
            q = make_quad((x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0))
            if abs((x0 + x1) / 2) < 2.25:
                base = jitter(rng, PALETTE["P3_EARTH_DARK"], 3)
                aisle.add(q, np.vstack([base, base]))
            else:
                base = jitter(rng, PALETTE["P5_WORN_EARTH"], 4)
                floor.add(q, np.vstack([base, base]))
    builder.add_category(floor)
    builder.add_category(aisle)

    # Earthen side walls with bright rectangular openings; no invented exterior geography.
    walls = Category("EARTHEN_WALLS", "EARTHEN_WALL")
    exposure = Category("RENDER_EXPOSURE_CARDS", "EXPOSURE_CARD")
    wall_color = np.asarray(PALETTE["P4_LATERITE"], dtype=np.uint8)
    for side in (-1.0, 1.0):
        for y0 in np.arange(-18.0, 40.0, 6.0):
            for piece in wall_bay_pieces(side, float(y0)):
                walls.add(piece, jitter(rng, PALETTE["P4_LATERITE"], 5))
            x = side * 10.72
            # Neutral exterior exposure gradient, not invented landscape geometry.
            for k in range(8):
                z0 = 0.82 + k * 0.245
                z1 = z0 + 0.245
                t = k / 7.0
                card = make_quad((x, y0 + 1.22, z0), (x, y0 + 4.78, z0),
                                 (x, y0 + 4.78, z1), (x, y0 + 1.22, z1))
                rgb = np.asarray([80 + 36 * t, 76 + 34 * t, 72 + 32 * t], dtype=np.uint8)
                exposure.add(card, rgb, emission=0.08 + 0.12 * t)
    # Far neutral exposure card; render-only, not world geography.
    for k in range(8):
        z0 = k * 1.075
        z1 = z0 + 1.075
        t = k / 7.0
        far = make_quad((-10.4, 41.2, z0), (10.4, 41.2, z0),
                        (10.4, 41.2, z1), (-10.4, 41.2, z1))
        rgb = np.asarray([70 + 40 * t, 66 + 38 * t, 62 + 36 * t], dtype=np.uint8)
        exposure.add(far, rgb, emission=0.06 + 0.10 * t)
    # Far end wall fragments around the pale opening.
    walls.add(make_box((-7.9, 40.4, 2.0), (5.2, 0.45, 4.0)), wall_color)
    walls.add(make_box((7.9, 40.4, 2.0), (5.2, 0.45, 4.0)), wall_color)
    builder.add_category(walls)
    builder.add_category(exposure)

    # Earthen benches for multitudes, repeated as modular bays.
    benches = Category("EARTHEN_BENCHES", "EARTHEN_BENCH")
    for side in (-1.0, 1.0):
        for y0 in np.arange(-17.0, 39.0, 6.0):
            for piece in bench_bay_pieces(side, float(y0)):
                benches.add(piece, jitter(rng, PALETTE["P5_WORN_EARTH"], 6))
    builder.add_category(benches)

    # Monumental carved hardwood posts, forked and lashed. Never stone.
    post_master = build_post_master()
    pv, pf, pc, pe, ps = post_master.arrays()
    post_geometry = trimesh.Trimesh(vertices=pv, faces=pf, process=False)
    posts = Category("HARDWOOD_POSTS", "HARDWOOD_POST")
    columns = (-8.3, -4.2, 4.2, 8.3)
    rows = np.arange(-14.0, 35.0, 6.0)
    for row_index, y in enumerate(rows):
        for col_index, x in enumerate(columns):
            angle = 0.055 * math.sin(row_index * 1.7 + col_index * 0.9)
            instance = transform_mesh(post_geometry, (x, float(y), 0.0), angle)
            posts.add(instance, pc, emission=pe, specular=ps)
            post_positions.append((float(x), float(y)))
    builder.add_category(posts)

    # Great beams, rafters, purlins and lashings running into depth.
    beams = Category("ROOF_BEAMS", "ROOF_BEAM")
    beam_color = np.asarray(PALETTE["P2_WOOD"], dtype=np.uint8)
    for x in columns:
        beams.add(make_beam((x, -18.0, 7.95), (x, 40.0, 7.95), 0.26, 9), beam_color)
    beams.add(make_beam((0.0, -18.0, 9.35), (0.0, 40.0, 9.35), 0.30, 10), beam_color)
    for y in np.arange(-18.0, 41.0, 1.5):
        for side in (-1, 1):
            beams.add(make_beam((side * 10.5, float(y), 6.25), (0.0, float(y), 9.45), 0.135, 6), beam_color)
            beams.add(make_beam((side * 7.0, float(y), 7.32), (0.0, float(y) + 3.0, 9.42), 0.095, 6), beam_color)
    for side in (-1, 1):
        for t in (0.30, 0.58, 0.82):
            x = side * 10.5 * (1 - t)
            z = 6.25 + (9.45 - 6.25) * t - 0.06
            beams.add(make_beam((x, -18.0, z), (x, 40.0, z), 0.10, 6), beam_color)
    builder.add_category(beams)

    # Dense thatch roof; dark upper half preserved.
    thatch = Category("THATCH_ROOF", "THATCH")
    for y0 in np.arange(-18.0, 40.0, 1.0):
        quads, _ = roof_bay_pieces(float(y0), 1.0)
        for k, q in enumerate(quads):
            base = jitter(rng, PALETTE["P1_CHAR"], 3)
            if k % 3 == 0:
                base = np.clip(np.asarray(base, dtype=float) + [4, 3, 2], 0, 255).astype(np.uint8)
            thatch.add(q, np.vstack([base, base]))
    # Eave fringes: short fibre/thatch reads, not invented decoration.
    for side in (-1, 1):
        for y in np.arange(-18.0, 40.0, 0.75):
            strip = make_quad((side * 10.52, float(y), 6.25), (side * 10.52, float(y) + 0.42, 6.25),
                              (side * 10.56, float(y) + 0.42, 5.92), (side * 10.56, float(y), 5.92))
            thatch.add(strip, jitter(rng, PALETTE["P1_CHAR"], 3))
    builder.add_category(thatch)

    # Exactly one ordinary stool; no figure or additional prop.
    stool = Category("SINGLE_STOOL", "STOOL_WOOD")
    for piece in stool_pieces():
        stool.add(piece, jitter(rng, PALETTE["P3_EARTH_DARK"], 4))
    builder.add_category(stool)

    return builder, post_master, post_positions


def write_glb(scene: trimesh.Scene, path: Path) -> None:
    data = scene.export(file_type="glb")
    path.write_bytes(data)


def export_module(cat: Category, name: str, path: Path) -> None:
    mesh = cat.to_trimesh()
    _, _, c, e, _ = cat.arrays()
    base = np.round(c.mean(axis=0)).astype(int).tolist()
    emission = float(np.clip(e.mean(), 0.0, 1.0))
    pbr = PBRMaterial(
        name=name,
        baseColorFactor=[*base, 255],
        metallicFactor=float(cat.material.get("metallic", 0.0)),
        roughnessFactor=float(cat.material.get("roughness", 0.9)),
        emissiveFactor=[min(1.0, emission * x / 255.0) for x in base] if emission > 0 else None,
        doubleSided=True,
    )
    mesh.visual = TextureVisuals(material=pbr)
    scene = trimesh.Scene()
    scene.add_geometry(mesh, node_name=name, geom_name=name)
    write_glb(scene, path)


def build_module_pack(post_master: Category) -> dict:
    modules: dict[str, Path] = {}
    out = M1 / "model" / "modules"

    export_module(post_master, "HALL_POST_MODULE", out / "HALL_POST_MODULE.glb")

    wall = Category("HALL_WALL_OPENING_MODULE", "EARTHEN_WALL")
    for piece in wall_bay_pieces(1.0, 0.0, 6.0):
        wall.add(piece, PALETTE["P4_LATERITE"])
    export_module(wall, "HALL_WALL_OPENING_MODULE", out / "HALL_WALL_OPENING_MODULE.glb")

    bench = Category("HALL_BENCH_MODULE", "EARTHEN_BENCH")
    for piece in bench_bay_pieces(1.0, 0.0, 6.0):
        bench.add(piece, PALETTE["P5_WORN_EARTH"])
    export_module(bench, "HALL_BENCH_MODULE", out / "HALL_BENCH_MODULE.glb")

    roof = Category("HALL_ROOF_BAY_MODULE", "THATCH")
    quads, beams = roof_bay_pieces(0.0, 6.0)
    for q in quads:
        roof.add(q, PALETTE["P1_CHAR"])
    for b in beams:
        roof.add(b, PALETTE["P1_CHAR"])
    export_module(roof, "HALL_ROOF_BAY_MODULE", out / "HALL_ROOF_BAY_MODULE.glb")

    stool = Category("HALL_STOOL_MODULE", "STOOL_WOOD")
    for piece in stool_pieces((0.0, 0.0, 0.0)):
        stool.add(piece, PALETTE["P3_EARTH_DARK"])
    export_module(stool, "HALL_STOOL_MODULE", out / "HALL_STOOL_MODULE.glb")

    for p in sorted(out.glob("*.glb")):
        modules[p.stem] = p
    return modules


def normalize(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n else v


class Renderer:
    def __init__(self, vertices, faces, colors, emission, specular):
        self.V = np.asarray(vertices, dtype=float)
        self.F = np.asarray(faces, dtype=np.int64)
        self.C = np.asarray(colors, dtype=float) / 255.0
        self.E = np.asarray(emission, dtype=float)
        self.S = np.asarray(specular, dtype=float)
        tri = self.V[self.F]
        normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        self.N = normals / np.maximum(lengths, 1e-9)
        self.centroids = tri.mean(axis=1)
        self.haze = np.asarray([0.48, 0.45, 0.43], dtype=float)
        self.exposure = 1.58

    def basis(self, eye, target):
        forward = normalize(np.asarray(target) - np.asarray(eye))
        world_up = np.asarray([0.0, 0.0, 1.0])
        right = normalize(np.cross(forward, world_up))
        up = normalize(np.cross(right, forward))
        return forward, right, up

    def project_vertices(self, eye, target, rw, rh, fov):
        forward, right, up = self.basis(eye, target)
        rel = self.V - np.asarray(eye)
        cam_x = rel @ right
        cam_y = rel @ up
        cam_z = rel @ forward
        f = 0.5 * rh / math.tan(math.radians(fov) * 0.5)
        px = rw * 0.5 + f * cam_x / np.maximum(cam_z, 1e-6)
        py = rh * 0.535 - f * cam_y / np.maximum(cam_z, 1e-6)
        return np.stack([px, py, cam_z], axis=1), f

    def lighting(self, eye):
        L1 = normalize(np.asarray([-0.82, 0.16, 0.64]))
        L2 = normalize(np.asarray([0.78, 0.12, 0.58]))
        L3 = normalize(np.asarray([0.0, 0.92, 0.24]))
        diffuse = (0.20 + 0.60 * np.abs(self.N @ L1)
                   + 0.30 * np.abs(self.N @ L2)
                   + 0.16 * np.maximum(0.0, self.N @ L3))
        view = normalize(np.asarray(eye) - self.centroids)
        H = normalize(L1[None, :] + view)
        spec = self.S * np.maximum(0.0, np.sum(self.N * H, axis=1)) ** 22.0
        base = self.C * (diffuse[:, None] * self.exposure + self.E[:, None])
        base += spec[:, None] * np.asarray([0.85, 0.78, 0.68])[None, :]
        # Restrained cool ambient sheen on the carried-forward wet-floor read.
        base += self.S[:, None] * np.asarray([0.035, 0.042, 0.052])[None, :]
        return base

    def render(self, eye, target, width, height, supersample=1.2, fov=62.0):
        rw, rh = int(width * supersample), int(height * supersample)
        proj, _ = self.project_vertices(eye, target, rw, rh, fov)
        base_shade = self.lighting(eye)
        yy = np.linspace(0.0, 1.0, rh)[:, None, None]
        background_top = np.asarray([0.045, 0.035, 0.032])[None, None, :]
        background_bottom = np.asarray([0.105, 0.088, 0.080])[None, None, :]
        color = background_top * (1 - yy) + background_bottom * yy
        color = np.broadcast_to(color, (rh, rw, 3)).astype(float).copy()
        zbuf = np.zeros((rh, rw), dtype=float)

        for i in range(len(self.F)):
            ia, ib, ic = self.F[i]
            x0, y0, z0 = proj[ia]
            x1, y1, z1 = proj[ib]
            x2, y2, z2 = proj[ic]
            if z0 <= 0.20 or z1 <= 0.20 or z2 <= 0.20:
                continue
            minx = max(0, int(math.floor(min(x0, x1, x2))))
            maxx = min(rw - 1, int(math.ceil(max(x0, x1, x2))))
            miny = max(0, int(math.floor(min(y0, y1, y2))))
            maxy = min(rh - 1, int(math.ceil(max(y0, y1, y2))))
            if minx > maxx or miny > maxy:
                continue
            xs = np.arange(minx, maxx + 1, dtype=float) + 0.5
            ys = np.arange(miny, maxy + 1, dtype=float) + 0.5
            X, Y = np.meshgrid(xs, ys)
            with np.errstate(divide="ignore", invalid="ignore"):
                den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
                w0 = ((y1 - y2) * (X - x2) + (x2 - x1) * (Y - y2)) / den
                w1 = ((y2 - y0) * (X - x2) + (x0 - x2) * (Y - y2)) / den
                w2 = 1.0 - w0 - w1
                invz = w0 / z0 + w1 / z1 + w2 / z2
            mask = (np.abs(den) > 1e-9) & (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4) & (invz > 0)
            if not mask.any():
                continue
            region_z = zbuf[miny : maxy + 1, minx : maxx + 1]
            visible = mask & (invz > region_z)
            if not visible.any():
                continue
            depth = np.where(visible, 1.0 / np.maximum(invz, 1e-9), 0.0)
            fog = np.clip((depth - 9.0) / 50.0, 0.0, 0.76) * (1.0 - 0.72 * self.E[i])
            fog = np.clip(fog, 0.0, 0.76)
            shaded = (base_shade[i][None, None, :] * (1.0 - fog[..., None])
                      + self.haze[None, None, :] * fog[..., None])
            region_c = color[miny : maxy + 1, minx : maxx + 1]
            region_c[visible] = shaded[visible]
            region_z[visible] = invz[visible]

        image = Image.fromarray(np.uint8(np.clip(color, 0, 1) * 255), "RGB")
        if supersample != 1.0:
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        return image


def project_point(point, eye, target, width, height, fov):
    forward = normalize(np.asarray(target) - np.asarray(eye))
    right = normalize(np.cross(forward, np.asarray([0, 0, 1])))
    up = normalize(np.cross(right, forward))
    rel = np.asarray(point, dtype=float) - np.asarray(eye, dtype=float)
    z = float(rel @ forward)
    if z <= 0.1:
        return None
    f = 0.5 * height / math.tan(math.radians(fov) * 0.5)
    x = width * 0.5 + f * float(rel @ right) / z
    y = height * 0.535 - f * float(rel @ up) / z
    return x, y, z, f


def postprocess(image: Image.Image, eye, target, width, height, fov,
                post_positions, seed=0, shadow_strength=118) -> Image.Image:
    image = image.convert("RGB")
    # Contact shadows projected from actual post-base positions.
    shadow = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(shadow)
    for x, y in post_positions:
        p = project_point((x, y, 0.02), eye, target, width, height, fov)
        if p is None:
            continue
        cx, cy, z, f = p
        rx = max(3.0, min(90.0, f * 1.25 / max(z, 1.0)))
        ry = max(2.0, rx * 0.30)
        alpha = int(np.clip(shadow_strength * (1.0 - min(z, 55.0) / 70.0) + 45, 45, 185))
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255 - alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=9))
    image = ImageChops.multiply(image, Image.merge("RGB", (shadow, shadow, shadow)))

    # Bloom only from actual bright exposure cards / openings.
    gray = ImageOps.grayscale(image)
    mask = gray.point(lambda p: 255 if p > 185 else 0)
    glow = image.filter(ImageFilter.GaussianBlur(radius=13))
    glow = ImageEnhance.Brightness(glow).enhance(0.18)
    black = Image.new("RGB", image.size, (0, 0, 0))
    image = ImageChops.screen(image, Image.composite(glow, black, mask))

    image = ImageEnhance.Contrast(image).enhance(1.07)
    image = ImageEnhance.Color(image).enhance(0.94)
    image = ImageEnhance.Brightness(image).enhance(1.04)
    arr = np.asarray(image).astype(float)
    rng = np.random.default_rng(seed)
    arr += rng.normal(0.0, 1.7, size=(height, width, 1))
    yy, xx = np.mgrid[0:height, 0:width]
    nx = (xx - width * 0.5) / (width * 0.5)
    ny = (yy - height * 0.5) / (height * 0.5)
    radius = np.sqrt(nx * nx + ny * ny)
    vignette = 1.0 - 0.27 * np.clip(radius, 0, 1) ** 2
    top_dark = 1.0 - 0.19 * np.clip(1.0 - yy / max(height - 1, 1), 0, 1) ** 1.4
    arr *= (vignette * top_dark)[..., None]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")


def camera_from_azimuth(azimuth_deg: float, radius=27.0, height=4.1,
                        target=(0.0, 9.0, 3.35)):
    a = math.radians(azimuth_deg)
    eye = np.asarray([
        radius * math.sin(a),
        9.0 - radius * math.cos(a),
        height,
    ], dtype=float)
    return eye, np.asarray(target, dtype=float)


def make_contact_sheet(views: list[tuple[str, Image.Image]], path: Path) -> None:
    cell_w, cell_h, margin, header = 640, 360, 24, 58
    sheet = Image.new("RGB", (cell_w * 2 + margin * 3, cell_h * 2 + margin * 3 + header), (10, 8, 7))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    draw.text((margin, 14), "HALL OF POSTS · M1 H2/H3 TECHNICAL BLOCKOUT — ACTUAL 3D RENDER VIEWS",
              font=font, fill=(224, 202, 158))
    for idx, (label, image) in enumerate(views[:4]):
        row, col = divmod(idx, 2)
        x = margin + col * (cell_w + margin)
        y = header + margin + row * (cell_h + margin + 22)
        thumb = image.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + cell_w, y + cell_h), outline=(110, 85, 55), width=2)
        draw.text((x + 8, y + cell_h + 5), label, font=small, fill=(205, 190, 165))
    sheet.save(path)


def make_review_sheet(source_path: Path, hero: Image.Image, path: Path) -> None:
    W, H = 1920, 1080
    sheet = Image.new("RGB", (W, H), (10, 8, 7))
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 40)
    label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    draw.text((48, 28), "THE DISOBEDIENT DAUGHTER — PHASE 3 / M1", font=title_font, fill=(230, 205, 157))
    draw.text((50, 82), "HALL OF POSTS V004 · APPROVED ENVIRONMENT DESIGN · CANON PENDING · H2/H3 TECHNICAL BLOCKOUT",
              font=body_font, fill=(177, 160, 137))
    draw.line((48, 112, W - 48, 112), fill=(116, 88, 51), width=2)

    source = Image.open(source_path).convert("RGB")
    # Exact artwork panel inside the approved 2560x1440 board.
    crop = ImageOps.fit(source.crop((56, 176, 1964, 1250)), (880, 660),
                        method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    render = ImageOps.fit(hero, (880, 660), method=Image.Resampling.LANCZOS,
                          centering=(0.5, 0.5))
    left_x, right_x, top_y = 48, 992, 146
    sheet.paste(crop, (left_x, top_y))
    sheet.paste(render, (right_x, top_y))
    draw.rectangle((left_x, top_y, left_x + 880, top_y + 660), outline=(119, 90, 55), width=2)
    draw.rectangle((right_x, top_y, right_x + 880, top_y + 660), outline=(119, 90, 55), width=2)
    draw.text((left_x + 12, 122), "SOURCE — APPROVED BOARD, ARTWORK PANEL", font=label_font, fill=(225, 201, 158))
    draw.text((right_x + 12, 122), "RESULT — ACTUAL 3D GEOMETRY, CPU LOOK-DEV RENDER", font=label_font, fill=(225, 201, 158))

    y = 830
    draw.text((48, y), "SOURCE AUTHORITY", font=label_font, fill=(225, 201, 158))
    draw.text((48, y + 28), "Drive ID 1MHCd25z3x-cfBUf-eoCJvDLqwvYj9Ins · OAD-45 approval, 2026-11-15 · board palette sampled exactly",
              font=body_font, fill=(187, 171, 148))
    draw.text((48, y + 56), "Giant carved hardwood posts, forked/lashed beams, thatch, earth benches, one stool, wet-looking floor, dark upper half.",
              font=body_font, fill=(187, 171, 148))
    draw.text((48, y + 84), "Restrictions retained: no stone, figures, flame, V013, Adanna, CQ-9, H3, rejected/superseded or limited-study asset.",
              font=body_font, fill=(187, 171, 148))
    draw.text((48, y + 112), "Not a finished film set, canon approval, measured plan, final UV/PBR, rig, animation or composited shot.",
              font=body_font, fill=(187, 171, 148))

    sw_x, sw_y = 48, 986
    for idx, (name, hex_value) in enumerate(PALETTE_HEX.items()):
        x = sw_x + idx * 104
        rgb = hexrgb(hex_value)
        draw.rectangle((x, sw_y, x + 88, sw_y + 34), fill=rgb, outline=(90, 75, 60))
        draw.text((x, sw_y + 38), hex_value, font=small_font, fill=(180, 165, 145))
    draw.text((820, 986), "NEXT GATE: CD FILM USE / CANON + SHARED LAYOUT → M2 FINAL H3 KIT",
              font=label_font, fill=(225, 201, 158))
    draw.text((820, 1018), "Deliverables: named GLB/OBJ, reusable module GLBs, production manifest, hero/3Q/side renders, turntable GIF.",
              font=body_font, fill=(187, 171, 148))
    sheet.save(path)


def make_turntable_gif(frames: list[Image.Image], path: Path) -> None:
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=180, loop=0, optimize=True)


def write_site(manifest: dict) -> None:
    site = M1 / "index.html"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Disobedient Daughter — Hall of Posts M1</title>
<style>
:root {{ color-scheme: dark; }}
body {{ margin:0; background:#0b0908; color:#e8dec8; font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif; }}
header {{ padding:28px 42px 18px; border-bottom:1px solid #4a3824; background:linear-gradient(180deg,#15100d,#0b0908); }}
h1 {{ margin:0 0 5px; font:700 34px Georgia,serif; letter-spacing:.02em; color:#e6cd9d; }}
.sub {{ color:#b8a78d; }}
main {{ max-width:1280px; margin:0 auto; padding:28px 42px 60px; }}
.panel {{ background:#12100e; border:1px solid #3d3022; border-radius:10px; padding:18px; margin:20px 0; box-shadow:0 12px 35px #0008; }}
img {{ max-width:100%; display:block; border:1px solid #4a3824; border-radius:6px; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
.badge {{ display:inline-block; padding:4px 9px; border:1px solid #8c6a3f; border-radius:999px; color:#e6cd9d; font-size:13px; margin-right:8px; }}
a {{ color:#d8b77e; }}
input[type=range] {{ width:100%; accent-color:#8c6a3f; }}
code {{ color:#d8c8aa; }}
footer {{ color:#8d816f; font-size:14px; }}
</style>
</head>
<body>
<header>
<h1>The Hall of Posts — M1 Visual Production Proof</h1>
<div class="sub">The Disobedient Daughter · Phase 3 · H2/H3 modular technical blockout · approved design, canon pending</div>
</header>
<main>
<section class="panel">
<span class="badge">SOURCE: HALL_OF_POSTS_V004</span><span class="badge">OAD-45 APPROVED</span><span class="badge">CANON PENDING</span><span class="badge">NOT FINAL FILM SET</span>
<p>Derived from the exact approved Chapter 8 environment board and Art Bible direction. No generic demo asset, invented character, V013, H3, CQ-9, rejected/superseded artwork, or limited internal study is used as production authority.</p>
<p><a href="renders/HALL_OF_POSTS_M1_REVIEW_SHEET.png">Open full review sheet</a> · <a href="model/hall_of_posts_m1.glb">Download assembled GLB</a> · <a href="model/hall_of_posts_m1.obj">Download OBJ</a> · <a href="production_manifest.json">Production manifest</a></p>
</section>
<section class="panel"><h2>Hero render from actual 3D geometry</h2><img src="renders/hall_of_posts_hero.png" alt="Hall of Posts hero render"></section>
<section class="panel"><h2>Interactive turntable scrubber</h2>
<img id="frame" src="renders/turntable_frames/frame_00.png" alt="Turntable frame">
<input id="scrub" type="range" min="0" max="{len(manifest['turntable_frames'])-1}" value="0" step="1">
<p class="sub">Frame <span id="frameNo">0</span> / {len(manifest['turntable_frames'])-1} · <a href="renders/hall_of_posts_turntable.gif">Download animated GIF</a></p>
</section>
<section class="panel"><h2>Source / result comparison</h2><img src="renders/reference_vs_render.png" alt="Source and result comparison"></section>
<section class="panel"><h2>Production state</h2>
<div class="grid"><div>
<h3>Geometry</h3><p>{manifest['geometry']['vertices']:,} vertices · {manifest['geometry']['triangles']:,} triangles · {len(manifest['nodes'])} named nodes</p>
<p>Modules: {', '.join(manifest['modules'].keys())}</p>
<p>Units are neutral proxies (<code>1 ≈ 1 m</code> for camera/layout only), not approved story dimensions.</p>
</div><div>
<h3>Exact next release gate</h3><p>CD selects film use/canon and approves one shared Chapter 8 spatial, metric and camera interpretation. Then M2 converts this proxy to final H3 topology/UVs and M3 delivers H4 earth/hardwood/thatch PBR plus H9 moving-camera lighting proof.</p>
</div></div></section>
<footer>Preserved Phase 1 authority · no calibrated texture maps, rig, animation, final compositing or final global readiness verdict claimed.</footer>
</main>
<script>
const frames = {json.dumps(manifest['turntable_frames'])};
const img = document.getElementById('frame');
const scrub = document.getElementById('scrub');
const label = document.getElementById('frameNo');
scrub.addEventListener('input', () => {{ const i = Number(scrub.value); img.src = frames[i]; label.textContent = i; }});
</script>
</body></html>"""
    site.write_text(html, encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="render one lower-resolution preview only")
    args = parser.parse_args()

    if not REFERENCE.exists():
        if not DOWNLOADED_SOURCE.exists():
            raise FileNotFoundError(f"Missing approved source board: {DOWNLOADED_SOURCE}")
        shutil.copy2(DOWNLOADED_SOURCE, REFERENCE)

    started = time.time()
    print("[M1] building scene", flush=True)
    builder, post_master, post_positions = build_scene()
    V, F, C, E, S = builder.arrays()

    glb_path = M1 / "model" / "hall_of_posts_m1.glb"
    obj_path = M1 / "model" / "hall_of_posts_m1.obj"
    write_glb(builder.scene, glb_path)
    builder.combined_mesh().export(obj_path)
    modules = build_module_pack(post_master)
    print(f"[M1] model: {len(V):,} vertices / {len(F):,} triangles", flush=True)

    renderer = Renderer(V, F, C, E, S)
    hero_eye = np.asarray([0.0, -25.0, 3.15], dtype=float)
    hero_target = np.asarray([0.0, 10.0, 3.35], dtype=float)

    if args.preview:
        preview_size = (960, 540)
        raw = renderer.render(hero_eye, hero_target, *preview_size, supersample=1.0, fov=62.0)
        preview = postprocess(raw, hero_eye, hero_target, *preview_size, 62.0, post_positions, seed=1)
        preview.save(M1 / "renders" / "preview.png")
        print(f"[M1] preview written in {time.time() - started:.1f}s", flush=True)
        return 0

    hero_size = (1600, 900)
    raw = renderer.render(hero_eye, hero_target, *hero_size, supersample=1.22, fov=62.0)
    hero = postprocess(raw, hero_eye, hero_target, *hero_size, 62.0, post_positions, seed=11)
    hero.save(M1 / "renders" / "hall_of_posts_hero.png")
    print("[M1] hero render written", flush=True)

    view_specs = [
        ("HERO · LOW CENTRAL AISLE", hero_eye, hero_target, hero_size, 62.0, 11),
        ("THREE-QUARTER · MODULAR BAYS", *camera_from_azimuth(36, 27.0, 4.4), (1200, 675), 60.0, 22),
        ("SIDE · HARDWOOD POST / THATCH READ", *camera_from_azimuth(82, 27.0, 4.0), (1200, 675), 60.0, 33),
        ("DETAIL · CENTRAL AISLE & STOOL", np.asarray([0.0, -10.0, 2.45]), np.asarray([0.0, 17.0, 3.0]), (1200, 675), 55.0, 44),
    ]
    contact_views: list[tuple[str, Image.Image]] = []
    for idx, (label, eye, target, size, fov, seed) in enumerate(view_specs):
        if idx == 0:
            image = hero
        else:
            raw = renderer.render(eye, target, *size, supersample=1.15, fov=fov)
            image = postprocess(raw, eye, target, *size, fov, post_positions, seed=seed, shadow_strength=105)
            image.save(M1 / "renders" / f"hall_of_posts_view_{idx:02d}.png")
        contact_views.append((label, image))
    make_contact_sheet(contact_views, M1 / "renders" / "hall_of_posts_contact_sheet.png")
    print("[M1] supporting views written", flush=True)

    turntable_angles = [-20, 0, 18, 36, 54, 72, 90, 108]
    turntable_frames: list[Image.Image] = []
    turntable_paths: list[str] = []
    for idx, angle in enumerate(turntable_angles):
        eye, target = camera_from_azimuth(angle, 27.0, 4.15)
        size = (960, 540)
        raw = renderer.render(eye, target, *size, supersample=1.12, fov=60.0)
        image = postprocess(raw, eye, target, *size, 60.0, post_positions, seed=100 + idx, shadow_strength=92)
        rel = f"renders/turntable_frames/frame_{idx:02d}.png"
        image.save(M1 / rel)
        turntable_frames.append(image)
        turntable_paths.append(rel)
        print(f"[M1] turntable frame {idx + 1}/{len(turntable_angles)}", flush=True)
    make_turntable_gif(turntable_frames, M1 / "renders" / "hall_of_posts_turntable.gif")

    make_review_sheet(REFERENCE, hero, M1 / "renders" / "HALL_OF_POSTS_M1_REVIEW_SHEET.png")
    reference_vs_render = Image.new("RGB", (1600, 600), (10, 8, 7))
    source = Image.open(REFERENCE).convert("RGB").crop((56, 176, 1964, 1250)).resize((800, 600), Image.Resampling.LANCZOS)
    result = hero.resize((800, 600), Image.Resampling.LANCZOS)
    reference_vs_render.paste(source, (0, 0))
    reference_vs_render.paste(result, (800, 0))
    reference_vs_render.save(M1 / "renders" / "reference_vs_render.png")

    bounds = np.vstack([V.min(axis=0), V.max(axis=0)]).tolist()
    source_hash = sha256(REFERENCE)
    manifest = {
        "milestone": "M1",
        "title": "The Hall of Posts — H2/H3 modular blockout and look-development proof",
        "status": "technical production proxy; not final film set, canon approval, or global readiness verdict",
        "created": "2026-11-19",
        "source": {
            "file": SOURCE_NAME,
            "drive_id": "1MHCd25z3x-cfBUf-eoCJvDLqwvYj9Ins",
            "sha256": source_hash,
            "approval": "STATUS APPROVED; client OAD-45, 2026-11-15; approved environment design",
            "canon": "PENDING APPROVAL",
            "consultant_review": "still required on board; no cultural claim made",
            "register_id": "CH08-INT-003",
            "cleared_for": "character compositions in the hall (CH08-SCN-017)",
            "carry_forward": ["floor looks wet", "carved bands deeper than plain and worn", "upper half very dark"],
        },
        "authority_boundary": {
            "production_authority_used": "approved Hall of Posts V004 environment design and Chapter 8 / Art Bible direction only",
            "not_used": [
                "V013 / Ancestral Establishing / Wall of Houses", "Adanna unapproved views or body interpretation",
                "CQ-9 blade/sheath", "H3 / Landing / Field of Cloth", "six visual-release-only passes",
                "rejected/superseded artwork", "failed corrections", "external-authority assets", "limited internal studies",
            ],
            "final_release_dependency": "CD film use/canon selection and one approved shared spatial/metric/camera interpretation (P2-G09 / P2-CD04)",
        },
        "units": "neutral technical proxy; 1 unit approximately 1 m for camera/layout only; not approved story or production dimensions",
        "geometry": {
            "vertices": int(len(V)),
            "triangles": int(len(F)),
            "bounds_xyz": bounds,
            "post_instances": len(post_positions),
            "stool_instances": 1,
        },
        "nodes": builder.nodes,
        "modules": {k: str(v.relative_to(M1)) for k, v in modules.items()},
        "materials": MATERIALS,
        "palette_hex": PALETTE_HEX,
        "deliverables": {
            "assembled_glb": "model/hall_of_posts_m1.glb",
            "assembled_obj": "model/hall_of_posts_m1.obj",
            "hero_render": "renders/hall_of_posts_hero.png",
            "review_sheet": "renders/HALL_OF_POSTS_M1_REVIEW_SHEET.png",
            "contact_sheet": "renders/hall_of_posts_contact_sheet.png",
            "turntable_gif": "renders/hall_of_posts_turntable.gif",
            "reference_vs_render": "renders/reference_vs_render.png",
            "site": "index.html",
        },
        "turntable_frames": turntable_paths,
        "camera_proxies": {
            "hero_eye": hero_eye.tolist(),
            "hero_target": hero_target.tolist(),
            "fov_degrees": 62.0,
            "note": "derived from approved board's low central one-point composition; no approved lens or camera is claimed",
        },
        "render": {
            "engine": "in-repo deterministic CPU triangle rasterizer",
            "lighting": "low-key neutral side/far exposure cards; no flame, lamp, neon or generic particles",
            "post": "depth haze, projected contact shadows, restrained bloom, vignette, grain",
            "source_calibrated_maps": False,
        },
        "evaluation": {
            "verdict": "H2/H3 technical blockout suitable for composition and modularity review; NOT a finished film set, final asset, or canon approval",
            "approved_reads_present": [
                "central aisle", "repeated giant carved hardwood post bays", "forked/lashed heads",
                "great beams into depth", "thatch roof", "earth benches", "one ordinary stool",
                "wet-looking floor", "dark upper half", "bright side openings", "board palette",
            ],
            "art_bible_reads": [
                "grounded dark palette", "low-key motivated side/far exposure", "no neon/generic particles",
                "no theatrical flame or invented fantasy lighting", "ordinary functional set dressing",
            ],
            "excluded": ["stone posts", "figures", "animals", "regalia", "extra tools", "flame", "wind", "day/night invention"],
            "deviations": [
                "carving is read as measured relief bands, not final figurative/cultural iconography",
                "post silhouettes and carved bands are simplified for a reproducible proxy",
                "exterior is a neutral exposure gradient, not an approved landscape or architectural view",
                "side openings and far aperture are composition/camera proxies pending CD spatial release",
                "CPU rasterizer uses palette-based colour and material intent, not calibrated PBR textures",
            ],
            "limitations": [
                "canon pending", "consultant review noted on board remains outstanding", "no approved dimensions",
                "no final topology/UVs/PBR maps", "no rig/animation/VFX/comp", "no native DCC or GPU benchmark in sandbox",
                "render exposure cards are non-production render aids",
            ],
        },
        "next_milestone": "M2: after CD release, final H3 modular kit with production topology/UVs; then M3 H4 PBR materials and H9 moving-camera lighting/render proof.",
    }
    (M1 / "production_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (M1 / "materials.json").write_text(json.dumps({"palette": PALETTE_HEX, "materials": MATERIALS}, indent=2), encoding="utf-8")
    write_site(manifest)

    print(f"[M1] complete in {time.time() - started:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
