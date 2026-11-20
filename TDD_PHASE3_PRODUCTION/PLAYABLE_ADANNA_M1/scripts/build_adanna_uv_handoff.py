#!/usr/bin/env python3
"""Build a labelled technical UV/material/collision import handoff for Adanna M1.

This does NOT overwrite the preserved rigged technical GLB. It creates a new
face-corner UV0 atlas GLB, a provisional material atlas, a neutral collision
proxy, a reusable UE setup helper reference, an import manifest and a local
validation report. Nothing here is final character art, final textures, final
dimensions, a Creative Director approval, or a verified Unreal import.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import struct
import sys
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
from trimesh.exchange.obj import export_obj

BASE = Path(__file__).resolve().parents[1]
MODEL = BASE / "model"
WEB = BASE / "web_build"
CAPTURES = WEB / "captures"
SOURCE_GLB = MODEL / "adanna_m1_technical_proxy.glb"
OUTPUT_GLB = MODEL / "adanna_m1_technical_proxy_uv.glb"
ATLAS = MODEL / "adanna_m1_uv_atlas.png"
LAYOUT = MODEL / "adanna_m1_uv_layout.png"
CAPTURE_ATLAS = CAPTURES / "adanna_m1_uv_atlas.png"
CAPTURE_LAYOUT = CAPTURES / "adanna_m1_uv_layout.png"
COLLISION = MODEL / "adanna_m1_collision_proxy.obj"
IMPORT_MANIFEST = MODEL / "adanna_m1_ue_import_manifest.json"
VALIDATION = MODEL / "adanna_m1_uv_validation.json"
PARTS_JSON = WEB / "internal" / "character_parts.json"
RIG_JSON = MODEL / "adanna_m1_character_rig.json"
WORLD_JSON = BASE / "world.json"
SOURCE_AUTHORITY = BASE / "source_authority.json"
OWNER_REQUEST = BASE.parents[1] / "OWNER_STUDIO_UNREAL_REQUEST.md"
UE_SETUP = BASE / "ue_project" / "Tools" / "TDD_M1_Unreal_Setup_macOS.py"
UE_SETUP_PRESERVED = BASE / "ue_project" / "Tools" / "TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py"

PATCH = 128
COLS = 4
ROWS = 2
ATLAS_W = PATCH * COLS
ATLAS_H = PATCH * ROWS
JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942

COMPONENT_DTYPE = {
    5120: np.dtype("<i1"),
    5121: np.dtype("<u1"),
    5122: np.dtype("<i2"),
    5123: np.dtype("<u2"),
    5125: np.dtype("<u4"),
    5126: np.dtype("<f4"),
}
TYPE_ITEMS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}

# Palette is recovered from the existing labelled technical proxy, which was
# sampled from the APPROVED master identity reference. These are provisional
# material intents only, not final calibrated PBR textures.
MATERIALS = [
    {"id": 0, "key": "SKIN", "label": "Deep brown skin / provisional", "rgb": [67, 45, 39], "roughness": 0.86, "metallic": 0.0},
    {"id": 1, "key": "SKIN_LIT", "label": "Lit skin / limb read / provisional", "rgb": [87, 61, 54], "roughness": 0.86, "metallic": 0.0},
    {"id": 2, "key": "HAIR", "label": "Thin braids / high knot / provisional", "rgb": [18, 18, 21], "roughness": 0.78, "metallic": 0.0},
    {"id": 3, "key": "INDIGO", "label": "Hand-woven indigo / provisional", "rgb": [37, 45, 80], "roughness": 0.92, "metallic": 0.0},
    {"id": 4, "key": "LEATHER", "label": "Vegetable-tanned leather / provisional", "rgb": [64, 42, 31], "roughness": 0.88, "metallic": 0.0},
    {"id": 5, "key": "BRONZE", "label": "Aged cast bronze / provisional", "rgb": [154, 112, 57], "roughness": 0.64, "metallic": 0.55},
    {"id": 6, "key": "CORAL", "label": "Coral beads / provisional", "rgb": [176, 74, 51], "roughness": 0.56, "metallic": 0.0},
    {"id": 7, "key": "SCAR", "label": "Left cheekbone scar / provisional", "rgb": [52, 35, 30], "roughness": 0.90, "metallic": 0.0},
]
COLOR_TO_MATERIAL = {tuple(m["rgb"]): m["id"] for m in MATERIALS}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_glb(path: Path) -> tuple[dict, bytearray, bytes]:
    data = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total != len(data):
        raise ValueError("not a valid GLB 2.0 file")
    json_len, json_type = struct.unpack_from("<II", data, 12)
    if json_type != JSON_CHUNK:
        raise ValueError("GLB JSON chunk type invalid")
    gltf = json.loads(data[20 : 20 + json_len].decode("utf-8"))
    off = 20 + json_len
    bin_len, bin_type = struct.unpack_from("<II", data, off)
    if bin_type != BIN_CHUNK:
        raise ValueError("GLB BIN chunk type invalid")
    binary = bytearray(data[off + 8 : off + 8 + bin_len])
    return gltf, binary, data


def read_accessor(gltf: dict, binary: bytearray, index: int) -> np.ndarray:
    acc = gltf["accessors"][index]
    view = gltf["bufferViews"][acc["bufferView"]]
    dtype = COMPONENT_DTYPE[acc["componentType"]]
    items = TYPE_ITEMS[acc["type"]]
    count = int(acc["count"])
    start = int(view.get("byteOffset", 0)) + int(acc.get("byteOffset", 0))
    stride = view.get("byteStride")
    if stride:
        arr = np.ndarray(
            (count, items),
            dtype=dtype,
            buffer=binary,
            offset=start,
            strides=(int(stride), dtype.itemsize),
        ).copy()
    else:
        arr = np.frombuffer(binary, dtype=dtype, count=count * items, offset=start).reshape(count, items).copy()
    return arr[:, 0] if items == 1 else arr


def add_buffer_view(gltf: dict, binary: bytearray, raw: bytes, target: int | None = None) -> int:
    pad = (-len(binary)) % 4
    if pad:
        binary.extend(b"\0" * pad)
    offset = len(binary)
    binary.extend(raw)
    view = {"buffer": 0, "byteOffset": offset, "byteLength": len(raw)}
    if target is not None:
        view["target"] = target
    gltf["bufferViews"].append(view)
    return len(gltf["bufferViews"]) - 1


def add_accessor(
    gltf: dict,
    view_index: int,
    component_type: int,
    type_name: str,
    count: int,
    minimum: list[float] | None = None,
    maximum: list[float] | None = None,
) -> int:
    acc: dict = {
        "bufferView": view_index,
        "byteOffset": 0,
        "componentType": component_type,
        "count": int(count),
        "type": type_name,
    }
    if minimum is not None:
        acc["min"] = [float(x) for x in minimum]
    if maximum is not None:
        acc["max"] = [float(x) for x in maximum]
    gltf["accessors"].append(acc)
    return len(gltf["accessors"]) - 1


def make_atlas() -> None:
    rng = np.random.default_rng(20261119)
    yy, xx = np.mgrid[0:PATCH, 0:PATCH]
    atlas = np.zeros((ATLAS_H, ATLAS_W, 3), dtype=np.uint8)
    for mat in MATERIALS:
        base = np.zeros((PATCH, PATCH, 3), dtype=np.float32)
        base[:] = np.asarray(mat["rgb"], dtype=np.float32)
        noise = rng.normal(0.0, 2.6, (PATCH, PATCH)).astype(np.float32)
        key = mat["key"]
        if key.startswith("SKIN"):
            modulation = noise + 1.3 * np.sin(xx * 0.31 + yy * 0.06)
        elif key == "HAIR":
            modulation = noise + 4.5 * np.sin(xx * 0.72) + 2.0 * np.sin(yy * 0.18)
        elif key == "INDIGO":
            weave = np.sin(xx * np.pi / 8.0) * np.sin(yy * np.pi / 8.0)
            modulation = noise + 5.5 * weave + 1.5 * np.sin((xx + yy) * 0.17)
        elif key == "LEATHER":
            modulation = noise * 1.5 + 4.0 * np.sin((xx * 0.7 + yy) * 0.16)
        elif key == "BRONZE":
            radius = np.sqrt((xx - PATCH / 2) ** 2 + (yy - PATCH / 2) ** 2)
            modulation = noise * 1.8 + 4.5 * np.sin(radius * 0.34)
        elif key == "CORAL":
            modulation = noise + 4.0 * np.sin(xx * 0.28) * np.sin(yy * 0.28)
        elif key == "SCAR":
            line = np.exp(-((yy - 0.55 * xx - 30.0) ** 2) / 24.0)
            modulation = noise + 7.0 * line
        else:
            modulation = noise
        for c in range(3):
            base[..., c] = np.clip(base[..., c] + modulation, 0, 255)
        x0 = (mat["id"] % COLS) * PATCH
        y0 = (mat["id"] // COLS) * PATCH
        atlas[y0 : y0 + PATCH, x0 : x0 + PATCH] = base.astype(np.uint8)
    Image.fromarray(atlas, "RGB").save(ATLAS, "PNG")


def material_patch_rect(material_id: int) -> tuple[float, float, float, float]:
    u0 = (material_id % COLS) / COLS
    v0 = (material_id // COLS) / ROWS
    return u0, v0, 1.0 / COLS, 1.0 / ROWS


def build_face_corner_uvs(gltf: dict, binary: bytearray, parts: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[int]]:
    prim = gltf["meshes"][0]["primitives"][0]
    attrs = prim["attributes"]
    positions = read_accessor(gltf, binary, attrs["POSITION"])
    normals = read_accessor(gltf, binary, attrs["NORMAL"])
    joints = read_accessor(gltf, binary, attrs["JOINTS_0"])
    weights = read_accessor(gltf, binary, attrs["WEIGHTS_0"])
    indices = read_accessor(gltf, binary, prim["indices"]).astype(np.uint32)

    vertex_part = np.full(len(positions), -1, dtype=np.int32)
    part_offsets: list[int] = []
    cursor = 0
    for pi, part in enumerate(parts):
        n = len(part["vertices"])
        vertex_part[cursor : cursor + n] = pi
        part_offsets.append(cursor)
        cursor += n
    if cursor != len(positions):
        raise ValueError(f"parts vertex count {cursor} != GLB vertex count {len(positions)}")

    part_material = []
    for part in parts:
        color = tuple(int(v) for v in part["color"])
        if color not in COLOR_TO_MATERIAL:
            raise ValueError(f"unmapped part colour {color} for {part['name']}")
        part_material.append(COLOR_TO_MATERIAL[color])

    face_count = len(indices) // 3
    uvs = np.zeros((face_count * 3, 2), dtype=np.float32)
    face_material_ids: list[int] = []
    for face in range(face_count):
        tri = indices[face * 3 : face * 3 + 3]
        part_ids = vertex_part[tri]
        if not np.all(part_ids == part_ids[0]):
            raise ValueError(f"face {face} crosses part boundaries")
        pid = int(part_ids[0])
        material_id = part_material[pid]
        face_material_ids.append(material_id)
        part = parts[pid]
        part_vertices = np.asarray(part["vertices"], dtype=np.float32)
        a, b, c = positions[tri]
        normal = np.cross(b - a, c - a)
        drop = int(np.argmax(np.abs(normal)))
        axes = [i for i in range(3) if i != drop]
        low = part_vertices[:, axes].min(axis=0)
        high = part_vertices[:, axes].max(axis=0)
        extent = np.maximum(high - low, np.array([1e-4, 1e-4], dtype=np.float32))
        u0, v0, uw, vh = material_patch_rect(material_id)
        for corner in range(3):
            coords = positions[tri[corner], axes]
            un = float(np.clip((coords[0] - low[0]) / extent[0], 0.0, 1.0))
            vn = float(np.clip((coords[1] - low[1]) / extent[1], 0.0, 1.0))
            u = u0 + (0.08 + 0.84 * un) * uw
            v = v0 + (0.08 + 0.84 * (1.0 - vn)) * vh
            uvs[face * 3 + corner] = (u, v)

    flat_indices = indices.astype(np.uint32)
    new_positions = np.ascontiguousarray(positions[flat_indices], dtype=np.float32)
    new_normals = np.ascontiguousarray(normals[flat_indices], dtype=np.float32)
    new_joints = np.ascontiguousarray(joints[flat_indices], dtype=np.uint16)
    new_weights = np.ascontiguousarray(weights[flat_indices], dtype=np.float32)
    new_indices = np.arange(len(flat_indices), dtype=np.uint32)
    return new_positions, new_normals, new_joints, new_weights, new_indices, uvs, face_material_ids


def write_uv_glb(parts: list[dict], face_material_ids: list[int]) -> dict:
    gltf, binary, source_bytes = parse_glb(SOURCE_GLB)
    prim = gltf["meshes"][0]["primitives"][0]
    arrays = build_face_corner_uvs(gltf, binary, parts)
    new_positions, new_normals, new_joints, new_weights, new_indices, uvs, actual_face_materials = arrays
    if actual_face_materials != face_material_ids:
        raise ValueError("face material id mismatch")

    def append_array(arr: np.ndarray, target: int | None = None) -> int:
        return add_buffer_view(gltf, binary, np.ascontiguousarray(arr).tobytes(), target)

    pos_view = append_array(new_positions, 34962)
    normal_view = append_array(new_normals, 34962)
    joint_view = append_array(new_joints, 34962)
    weight_view = append_array(new_weights, 34962)
    uv_view = append_array(uvs, 34962)
    index_view = append_array(new_indices, 34963)
    image_view = add_buffer_view(gltf, binary, ATLAS.read_bytes(), None)

    pos_acc = add_accessor(
        gltf, pos_view, 5126, "VEC3", len(new_positions),
        np.min(new_positions, axis=0).tolist(), np.max(new_positions, axis=0).tolist(),
    )
    normal_acc = add_accessor(gltf, normal_view, 5126, "VEC3", len(new_normals))
    joint_acc = add_accessor(gltf, joint_view, 5123, "VEC4", len(new_joints))
    weight_acc = add_accessor(gltf, weight_view, 5126, "VEC4", len(new_weights))
    uv_acc = add_accessor(
        gltf, uv_view, 5126, "VEC2", len(uvs),
        np.min(uvs, axis=0).tolist(), np.max(uvs, axis=0).tolist(),
    )
    index_acc = add_accessor(gltf, index_view, 5125, "SCALAR", len(new_indices))

    prim["attributes"] = {
        "POSITION": pos_acc,
        "NORMAL": normal_acc,
        "TEXCOORD_0": uv_acc,
        "JOINTS_0": joint_acc,
        "WEIGHTS_0": weight_acc,
    }
    prim["indices"] = index_acc
    prim["material"] = 0
    prim["mode"] = 4
    prim["extras"] = {
        "uv_method": "face-corner dominant-axis planar projection; technical import UV0, not a seam-aware final unwrap",
        "vertex_count": int(len(new_positions)),
        "triangle_count": int(len(new_indices) // 3),
        "atlas_material_ids": [m["id"] for m in MATERIALS],
        "classification": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
    }

    gltf["samplers"] = [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]
    gltf["images"] = [{
        "name": "Adanna_M1_Provisional_UV_Atlas",
        "mimeType": "image/png",
        "bufferView": image_view,
    }]
    gltf["textures"] = [{"name": "Adanna_M1_Provisional_BaseColor", "sampler": 0, "source": 0}]
    gltf["materials"] = [{
        "name": "Adanna_M1_UVAtlas_PBR_Intent_PROVISIONAL",
        "pbrMetallicRoughness": {
            "baseColorTexture": {"index": 0},
            "baseColorFactor": [1.0, 1.0, 1.0, 1.0],
            "metallicFactor": 0.0,
            "roughnessFactor": 0.82,
        },
        "doubleSided": True,
        "extras": {
            "classification": "provisional technical material atlas; NOT final calibrated PBR textures",
            "material_slots": MATERIALS,
        },
    }]
    extras = gltf["asset"].setdefault("extras", {})
    extras["uv_handoff"] = {
        "classification": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
        "source_glb_sha256": sha256(SOURCE_GLB),
        "source_glb_bytes": len(source_bytes),
        "note": "UV0/atlas/collision are technical import aids; no final appearance, dimensions, groom, costume or texture approval is claimed.",
    }
    restrictions = list(extras.get("restrictions", []))
    restrictions.append("UV0/atlas/collision handoff is technical preparation only; final topology/UVs/PBR/groom remain unapproved.")
    extras["restrictions"] = restrictions
    gltf["asset"]["generator"] = "TDD Playable Adanna M1 UV/material/collision handoff builder"

    gltf["buffers"][0]["byteLength"] = len(binary)
    json_bytes = json.dumps(gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    json_pad = b" " * ((-len(json_bytes)) % 4)
    bin_pad = b"\0" * ((-len(binary)) % 4)
    total = 12 + 8 + len(json_bytes) + len(json_pad) + 8 + len(binary) + len(bin_pad)
    out = bytearray()
    out.extend(struct.pack("<4sII", b"glTF", 2, total))
    out.extend(struct.pack("<II", len(json_bytes) + len(json_pad), JSON_CHUNK))
    out.extend(json_bytes)
    out.extend(json_pad)
    out.extend(struct.pack("<II", len(binary) + len(bin_pad), BIN_CHUNK))
    out.extend(binary)
    out.extend(bin_pad)
    OUTPUT_GLB.write_bytes(out)
    return {
        "source_vertex_count": 870,
        "source_triangle_count": 1584,
        "face_corner_vertex_count": int(len(new_positions)),
        "uv_min": np.min(uvs, axis=0).astype(float).tolist(),
        "uv_max": np.max(uvs, axis=0).astype(float).tolist(),
        "face_material_ids": face_material_ids,
    }


def make_layout(uvs: np.ndarray, face_material_ids: list[int]) -> None:
    atlas = Image.open(ATLAS).convert("RGBA")
    scale = 2
    atlas_big = atlas.resize((ATLAS_W * scale, ATLAS_H * scale), Image.Resampling.NEAREST)
    overlay = Image.new("RGBA", atlas_big.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    face_uvs = uvs.reshape(-1, 3, 2)
    for face, triangle in enumerate(face_uvs):
        mid = int(face_material_ids[face])
        colour = tuple(MATERIALS[mid]["rgb"]) + (70,)
        points = [(float(u) * atlas_big.width, float(v) * atlas_big.height) for u, v in triangle]
        od.line(points + [points[0]], fill=colour, width=1)
    atlas_overlay = Image.alpha_composite(atlas_big, overlay).convert("RGB")

    W, H = 1200, 900
    sheet = Image.new("RGB", (W, H), (9, 11, 12))
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.load_default(size=24)
    header_font = ImageFont.load_default(size=17)
    small_font = ImageFont.load_default(size=14)
    gold = (220, 190, 130)
    muted = (150, 145, 132)
    white = (230, 225, 212)
    draw.text((40, 24), "TDD - PLAYABLE ADANNA M1 - TECHNICAL UV / MATERIAL HANDOFF", font=title_font, fill=gold)
    draw.text((40, 56), "PROVISIONAL - AWAITING CREATIVE APPROVAL | NOT FINAL CHARACTER | NOT FINAL TEXTURES", font=header_font, fill=muted)
    sheet.paste(atlas_overlay, (40, 94))
    draw.rectangle((40, 94, 40 + atlas_big.width, 94 + atlas_big.height), outline=(120, 95, 55), width=2)

    for mat in MATERIALS:
        col = mat["id"] % COLS
        row = mat["id"] // COLS
        x = 40 + col * PATCH * scale
        y = 94 + row * PATCH * scale
        label = f"{mat['id']} {mat['key']}"
        draw.rectangle((x + 4, y + 4, x + 154, y + 28), fill=(8, 9, 10))
        draw.text((x + 9, y + 8), label, font=small_font, fill=white)

    draw.text((40, 630), "ATLAS SLOTS AND FACE-CORNER UV COVERAGE", font=header_font, fill=gold)
    for mat in MATERIALS:
        col = mat["id"] % 4
        row = mat["id"] // 4
        x = 40 + col * 280
        y = 664 + row * 82
        draw.rectangle((x, y, x + 262, y + 66), outline=(75, 65, 48), width=1)
        draw.rectangle((x + 8, y + 10, x + 42, y + 44), fill=tuple(mat["rgb"]), outline=(190, 175, 150), width=1)
        draw.text((x + 52, y + 9), f"{mat['id']} - {mat['key']}", font=small_font, fill=white)
        draw.text((x + 52, y + 30), mat["label"], font=small_font, fill=muted)
        draw.text((x + 52, y + 48), f"RGB {tuple(mat['rgb'])} | R {mat['roughness']:.2f} | M {mat['metallic']:.2f}", font=small_font, fill=muted)

    draw.text((40, 842), "UV0: dominant-axis face-corner planar projection into material patches; seams are split by face corners, not a final production unwrap.", font=small_font, fill=muted)
    draw.text((40, 864), "Validation: model/adanna_m1_uv_validation.json | UE import remains BLOCKED - OWNER-STUDIO DEPENDENCY.", font=small_font, fill=muted)
    sheet.save(LAYOUT, "PNG")


def make_collision_proxy() -> dict:
    world = json.loads(WORLD_JSON.read_text(encoding="utf-8"))
    radius_m = float(world["character"]["radius"])
    half_height_m = 0.88  # neutral gameplay capsule from UE source; NOT approved character dimensions
    total_height_m = half_height_m * 2.0
    cylinder_height = max(0.01, total_height_m - 2.0 * radius_m)
    mesh = trimesh.creation.capsule(radius=radius_m, height=cylinder_height, count=[16, 24])
    mesh.apply_translation([0.0, 0.0, -float(mesh.bounds[0, 2])])
    COLLISION.write_text(export_obj(mesh), encoding="utf-8")
    return {"radius_m": radius_m, "height_m": float(mesh.extents[2]), "half_height_m": half_height_m, "vertices": len(mesh.vertices), "faces": len(mesh.faces)}


def write_import_manifest(collision: dict, build_facts: dict) -> None:
    source_authority = json.loads(SOURCE_AUTHORITY.read_text(encoding="utf-8"))
    rig = json.loads(RIG_JSON.read_text(encoding="utf-8"))
    manifest = {
        "name": "Adanna M1 technical UE import handoff",
        "date": "2026-11-19",
        "status": "PRODUCED — NOT YET VERIFIED",
        "classification": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
        "scope": "labelled technical preparation for eventual UE import; NOT a final character, final texture set, UE asset, compile, PIE, cook or package",
        "source_authority": {
            "approved_master": source_authority["sources"]["adanna_master"],
            "phase1_restrictions": source_authority["phase1_restrictions"],
        },
        "files": {
            "preserved_source_glb": str(SOURCE_GLB.relative_to(BASE)),
            "uv_glb": str(OUTPUT_GLB.relative_to(BASE)),
            "uv_atlas": str(ATLAS.relative_to(BASE)),
            "uv_layout": str(LAYOUT.relative_to(BASE)),
            "collision_proxy_obj": str(COLLISION.relative_to(BASE)),
            "owner_request": "../../OWNER_STUDIO_UNREAL_REQUEST.md",
            "ue_setup_script_macos": "ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py",
            "ue_setup_script_superseded": "ue_project/Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py",
            "macos_runbook": "ue_project/README_MACOS_UE58.md",
            "macos_static_audit": "ue_project/Tools/tdd_m1_macos_audit.json",
            "validation_report": str(VALIDATION.relative_to(BASE)),
        },
        "sha256": {
            "preserved_source_glb": sha256(SOURCE_GLB),
            "uv_glb": sha256(OUTPUT_GLB),
            "uv_atlas": sha256(ATLAS),
            "uv_layout": sha256(LAYOUT),
            "collision_proxy_obj": sha256(COLLISION),
        },
        "scale_and_coordinates": {
            "source_units": "neutral gameplay metres; glTF coordinates are Z-up",
            "ue_import_scale": 100.0,
            "ue_unit": "centimetres",
            "axis_conversion_status": "PRODUCED — NOT YET VERIFIED; verify owner UE importer orientation",
            "approved_dimensions_status": "BLOCKED — CREATIVE APPROVAL",
        },
        "uv": {
            "channel": "TEXCOORD_0",
            "method": "face-corner dominant-axis planar projection into an 8-slot atlas",
            "vertex_count": build_facts["face_corner_vertex_count"],
            "triangle_count": build_facts["source_triangle_count"],
            "uv_min": build_facts["uv_min"],
            "uv_max": build_facts["uv_max"],
            "status": "PRODUCED — NOT YET VERIFIED",
            "note": "Technical UV0 only; final production requires seam-aware unwrap, UV validation and calibrated texture maps.",
        },
        "material_slots": [
            {
                "id": m["id"],
                "key": m["key"],
                "label": m["label"],
                "base_color_rgb": m["rgb"],
                "roughness_intent": m["roughness"],
                "metallic_intent": m["metallic"],
                "uv_rect": list(material_patch_rect(m["id"])),
                "status": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
            }
            for m in MATERIALS
        ],
        "skeleton": {
            "joint_count_from_existing_rig": rig.get("joint_count", 21),
            "animation_clips": ["idle", "walk", "run", "jump", "land"],
            "native_ue_skeletal_mesh": False,
            "native_ue_animation_assets": False,
            "status": "TECHNICALLY DEMONSTRATED — NOT INTEGRATED",
        },
        "collision": {
            "file": str(COLLISION.relative_to(BASE)),
            "radius_m": collision["radius_m"],
            "height_m": collision["height_m"],
            "half_height_m": collision["half_height_m"],
            "vertices": collision["vertices"],
            "faces": collision["faces"],
            "status": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
            "note": "Neutral gameplay capsule derived from world.json radius and UE source collision height; not approved character dimensions.",
        },
        "unreal_integration": {
            "project": "ue_project/TDD_GAME.uproject",
            "engine_association": "5.8 (owner-verified installed engine)",
            "compile_verified": False,
            "pie_verified": False,
            "cook_verified": False,
            "package_verified": False,
            "project_owned_umap": False,
            "native_uasset_import": False,
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "precise_blocker": source_authority["precise_blocker"],
        },
        "creative_approval_dependencies": [
            "Final Adanna turnaround, dimensions and proportions.",
            "Final hair/groom authority.",
            "Final costume authority.",
            "Final facial design authority.",
            "Final calibrated materials/textures and seam-aware production UVs.",
        ],
        "status_classification": {
            "technical_uv_glb_and_atlas": "PRODUCED — NOT YET VERIFIED",
            "neutral_collision_proxy": "PROVISIONAL — AWAITING CREATIVE APPROVAL",
            "browser_and_node_gameplay": "TECHNICALLY DEMONSTRATED — NOT INTEGRATED",
            "ue_compile_pie_cook_package": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "final_character_and_forest": "BLOCKED — CREATIVE APPROVAL",
            "m3_m4_gameplay": "NOT STARTED",
        },
    }
    IMPORT_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def validate(uvs: np.ndarray, face_material_ids: list[int], collision: dict) -> dict:
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    gltf, binary, data = parse_glb(OUTPUT_GLB)
    prim = gltf["meshes"][0]["primitives"][0]
    attrs = prim["attributes"]
    check("GLB magic/version/total length", struct.unpack_from("<4sII", data, 0)[0] == b"glTF" and struct.unpack_from("<4sII", data, 0)[1] == 2 and struct.unpack_from("<4sII", data, 0)[2] == len(data))
    check("GLB buffer length valid", gltf["buffers"][0]["byteLength"] <= len(binary), f"declared={gltf['buffers'][0]['byteLength']} binary={len(binary)}")
    check("TEXCOORD_0 present", "TEXCOORD_0" in attrs)
    check("COLOR_0 removed to avoid atlas double tint", "COLOR_0" not in attrs)
    pos = read_accessor(gltf, binary, attrs["POSITION"])
    uv = read_accessor(gltf, binary, attrs["TEXCOORD_0"])
    joints = read_accessor(gltf, binary, attrs["JOINTS_0"])
    weights = read_accessor(gltf, binary, attrs["WEIGHTS_0"])
    indices = read_accessor(gltf, binary, prim["indices"])
    check("POSITION/TEXCOORD_0 counts match", len(pos) == len(uv) == len(uvs), f"{len(pos)}/{len(uv)}/{len(uvs)}")
    check("UVs finite and inside 0..1", bool(np.all(np.isfinite(uv)) and np.all(uv >= 0.0) and np.all(uv <= 1.0)), f"min={uv.min(axis=0).tolist()} max={uv.max(axis=0).tolist()}")
    cells = sorted({int(min(COLS - 1, int(u * COLS))) + COLS * int(min(ROWS - 1, int(v * ROWS))) for u, v in uv})
    check("all 8 atlas material patches covered", cells == list(range(8)), str(cells))
    check("face-corner vertex count", len(pos) == 3 * 1584, str(len(pos)))
    check("indices cover new vertices", int(indices.max()) == len(pos) - 1 and int(indices.min()) == 0, f"min={int(indices.min())} max={int(indices.max())}")
    check("joint indices below 21", int(joints.max()) < 21, str(int(joints.max())))
    sums = weights.sum(axis=1)
    check("skin weights approximately normalised", bool(np.all(np.abs(sums - 1.0) < 0.02)), f"min={float(sums.min()):.5f} max={float(sums.max()):.5f}")
    mat = gltf["materials"][prim["material"]]
    check("material has baseColorTexture", "baseColorTexture" in mat.get("pbrMetallicRoughness", {}))
    check("texture source/sampler valid", len(gltf.get("textures", [])) == 1 and gltf["textures"][0]["source"] == 0 and len(gltf.get("samplers", [])) >= 1)
    image = gltf.get("images", [{}])[0]
    check("image is embedded bufferView, no URI", "bufferView" in image and "uri" not in image)
    image_view = gltf["bufferViews"][image["bufferView"]]
    image_bytes = bytes(binary[image_view["byteOffset"] : image_view["byteOffset"] + image_view["byteLength"]])
    check("embedded image has PNG magic", image_bytes[:8] == b"\x89PNG\r\n\x1a\n")
    check("animations preserved", [a.get("name") for a in gltf.get("animations", [])] == ["idle", "walk", "run", "jump", "land"])
    check("21-joint skin preserved", len(gltf.get("skins", [{}])[0].get("joints", [])) == 21)
    check("source GLB preserved", sha256(SOURCE_GLB) == json.loads(IMPORT_MANIFEST.read_text(encoding="utf-8"))["sha256"]["preserved_source_glb"])

    atlas_img = Image.open(ATLAS)
    layout_img = Image.open(LAYOUT)
    check("atlas dimensions", atlas_img.size == (ATLAS_W, ATLAS_H), str(atlas_img.size))
    check("layout dimensions", layout_img.size[0] >= 1000 and layout_img.size[1] >= 700, str(layout_img.size))
    check("capture copies exist", CAPTURE_ATLAS.is_file() and CAPTURE_LAYOUT.is_file())
    check("face material ids recorded", len(face_material_ids) == 1584 and sorted(set(face_material_ids)) == list(range(8)))

    collision_mesh = trimesh.load(COLLISION, force="mesh")
    extents = collision_mesh.extents
    check("collision OBJ reopens in Trimesh", len(collision_mesh.vertices) > 0 and len(collision_mesh.faces) > 0, f"{len(collision_mesh.vertices)}v/{len(collision_mesh.faces)}f")
    check("collision bounds match neutral capsule", abs(extents[0] - 2 * collision["radius_m"]) < 0.02 and abs(extents[2] - collision["height_m"]) < 0.02, str(extents.tolist()))
    check("collision feet origin at Z=0", abs(float(collision_mesh.bounds[0, 2])) < 0.02, str(float(collision_mesh.bounds[0, 2])))

    manifest = json.loads(IMPORT_MANIFEST.read_text(encoding="utf-8"))
    required_statuses = {
        "COMPLETED AND VERIFIED",
        "PRODUCED — NOT YET VERIFIED",
        "TECHNICALLY DEMONSTRATED — NOT INTEGRATED",
        "PROVISIONAL — AWAITING CREATIVE APPROVAL",
        "BLOCKED — OWNER-STUDIO DEPENDENCY",
        "BLOCKED — CREATIVE APPROVAL",
        "NOT STARTED",
    }
    check("import manifest valid", isinstance(manifest, dict) and manifest.get("status") in required_statuses)
    check("UE integration not overclaimed", manifest["unreal_integration"]["compile_verified"] is False and manifest["unreal_integration"]["package_verified"] is False and manifest["unreal_integration"]["project_owned_umap"] is False)
    check("owner request file exists", OWNER_REQUEST.is_file() and OWNER_REQUEST.stat().st_size > 500)
    check("macOS UE setup helper exists", UE_SETUP.is_file() and UE_SETUP.stat().st_size > 500)
    check("superseded setup helper preserved",
          UE_SETUP_PRESERVED.is_file() and UE_SETUP_PRESERVED.stat().st_size > 500)
    check("macOS runbook exists", (BASE / "ue_project" / "README_MACOS_UE58.md").is_file())

    # Geometry sanity regression guard. A transform-order bug previously threw the spiral
    # pendant 1.3 m in front of the body, which passed every UV check because UVs were fine.
    # Bind POSITION against a plausible 2 m humanoid envelope so that class of defect fails
    # the build instead of shipping into the Unreal handoff again.
    parts_doc = json.loads(PARTS_JSON.read_text(encoding="utf-8"))["parts"]
    outside = []
    for part in parts_doc:
        pts = np.asarray(part["vertices"], dtype=float)
        if pts[:, 2].min() < -0.05 or pts[:, 2].max() > 2.05 or np.abs(pts[:, 1]).max() > 0.45 or np.abs(pts[:, 0]).max() > 0.45:
            outside.append(part["name"])
    check("all parts inside 2 m humanoid envelope", not outside, "outside=" + str(outside))
    pendant = next((p for p in parts_doc if p["name"] == "SPIRAL_PENDANT"), None)
    pendant_ok = bool(
        pendant
        and 1.30 <= float(np.asarray(pendant["vertices"])[:, 2].mean()) <= 1.60
        and abs(float(np.asarray(pendant["vertices"])[:, 1].mean())) < 0.20
    )
    check("spiral pendant sits on the chest", pendant_ok,
          "mean=" + (str(np.asarray(pendant["vertices"]).mean(axis=0).round(3).tolist()) if pendant else "missing"))

    overall = all(c["ok"] for c in checks)
    report = {
        "generated": "2026-11-19",
        "overallPass": overall,
        "status": "COMPLETED AND VERIFIED" if overall else "PRODUCED — NOT YET VERIFIED",
        "scope": "local GLB binary/accessor, UV atlas, import manifest, owner request, setup helper and collision OBJ validation only; NOT Unreal import/compile/PIE/cook/package",
        "checks": checks,
        "checksPassed": sum(1 for c in checks if c["ok"]),
        "checksTotal": len(checks),
        "classification": "PROVISIONAL — AWAITING CREATIVE APPROVAL; BLOCKED — OWNER-STUDIO DEPENDENCY for UE execution",
    }
    VALIDATION.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def update_manifest_after_validation(report: dict) -> None:
    manifest = json.loads(IMPORT_MANIFEST.read_text(encoding="utf-8"))
    manifest["status"] = "COMPLETED AND VERIFIED"
    manifest["status_classification"]["technical_uv_glb_and_atlas"] = "COMPLETED AND VERIFIED"
    manifest["status_classification"]["local_validation"] = "COMPLETED AND VERIFIED"
    manifest["local_validation"] = {
        "report": str(VALIDATION.relative_to(BASE)),
        "checks_passed": report["checksPassed"],
        "checks_total": report["checksTotal"],
        "scope": "local file/GLB validation only; UE integration remains blocked",
    }
    manifest["uv"]["status"] = "COMPLETED AND VERIFIED"
    IMPORT_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    for directory in (MODEL, CAPTURES, UE_SETUP.parent):
        directory.mkdir(parents=True, exist_ok=True)
    parts = json.loads(PARTS_JSON.read_text(encoding="utf-8"))["parts"]
    make_atlas()
    # A first UV pass is required before layout drawing. Build the GLB and capture its UVs.
    gltf, binary, _ = parse_glb(SOURCE_GLB)
    arrays = build_face_corner_uvs(gltf, binary, parts)
    uvs = arrays[5]
    face_material_ids = arrays[6]
    make_layout(uvs, face_material_ids)
    build_facts = write_uv_glb(parts, face_material_ids)
    collision = make_collision_proxy()
    shutil.copy2(ATLAS, CAPTURE_ATLAS)
    shutil.copy2(LAYOUT, CAPTURE_LAYOUT)
    write_import_manifest(collision, build_facts)
    report = validate(uvs, face_material_ids, collision)
    if not report["overallPass"]:
        failed = [c for c in report["checks"] if not c["ok"]]
        raise SystemExit("validation failed: " + json.dumps(failed, indent=2))
    update_manifest_after_validation(report)
    print(f"[UV handoff] {report['checksPassed']}/{report['checksTotal']} local checks passed")
    print(f"[UV handoff] wrote {OUTPUT_GLB.relative_to(BASE)} ({OUTPUT_GLB.stat().st_size} bytes)")
    print(f"[UV handoff] wrote {ATLAS.relative_to(BASE)}, {LAYOUT.relative_to(BASE)}, {COLLISION.relative_to(BASE)}")
    print(f"[UV handoff] wrote {IMPORT_MANIFEST.relative_to(BASE)} and {VALIDATION.relative_to(BASE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
