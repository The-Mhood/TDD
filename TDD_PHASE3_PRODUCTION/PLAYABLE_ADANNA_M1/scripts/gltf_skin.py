#!/usr/bin/env python3
"""Generate a compact, skinned glTF 2.0 technical proxy for Adanna M1.

This is NOT the final production character. It is a rigged gameplay proxy built
from approved identity locks only: deep brown skin, high-knot braids, indigo
wrap, leather baldric, aged bronze, coral accent, left temple cuffs/beads,
left upper-arm armlet, spiral pendant, diagonal left-cheek scar. No blade,
unapproved turnaround, invented costume, or canon claim is introduced.
"""
from __future__ import annotations

import json
import math
import struct
import sys
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "TDD_PHASE3_PRODUCTION" / "HALL_OF_POSTS_M1" / "scripts"))
import build_hall_of_posts_m1 as m1  # noqa: E402

COMPONENT = {
    np.dtype("uint8"): 5121,
    np.dtype("uint16"): 5123,
    np.dtype("uint32"): 5125,
    np.dtype("float32"): 5126,
}
NUM_COMPONENTS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


class GLTFBuilder:
    def __init__(self):
        self.binary = bytearray()
        self.buffer_views = []
        self.accessors = []

    def add_accessor(self, array, type_: str, target: int | None = None, minmax: bool = False):
        arr = np.asarray(array)
        expected = NUM_COMPONENTS[type_]
        if arr.ndim == 1:
            arr = arr.reshape(-1, expected) if expected > 1 else arr.reshape(-1, 1)
        elif arr.ndim == 3 and type_ == "MAT4":
            arr = arr.reshape(arr.shape[0], 16)
        if arr.shape[-1] != expected:
            raise ValueError(f"accessor {type_} expects {expected} components, got {arr.shape}")
        if arr.dtype not in COMPONENT:
            arr = arr.astype(np.float32 if np.issubdtype(arr.dtype, np.floating) else np.uint32)
        arr = np.ascontiguousarray(arr)
        while len(self.binary) % 4:
            self.binary.append(0)
        offset = len(self.binary)
        self.binary.extend(arr.tobytes(order="C"))
        view = {"buffer": 0, "byteOffset": offset, "byteLength": arr.nbytes}
        if target is not None:
            view["target"] = target
        self.buffer_views.append(view)
        accessor = {
            "bufferView": len(self.buffer_views) - 1,
            "byteOffset": 0,
            "componentType": COMPONENT[arr.dtype],
            "count": int(arr.shape[0]),
            "type": type_,
        }
        if minmax:
            flat = arr.reshape(arr.shape[0], -1)
            accessor["min"] = flat.min(axis=0).tolist()
            accessor["max"] = flat.max(axis=0).tolist()
        self.accessors.append(accessor)
        return len(self.accessors) - 1

    @staticmethod
    def write_glb(path: Path, gltf: dict, binary: bytes) -> None:
        json_bytes = json.dumps(gltf, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        while len(json_bytes) % 4:
            json_bytes += b" "
        bin_bytes = bytes(binary)
        while len(bin_bytes) % 4:
            bin_bytes += b"\x00"
        total = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
        with path.open("wb") as f:
            f.write(struct.pack("<4sII", b"glTF", 2, total))
            f.write(struct.pack("<I4s", len(json_bytes), b"JSON"))
            f.write(json_bytes)
            f.write(struct.pack("<I4s", len(bin_bytes), b"BIN\x00"))
            f.write(bin_bytes)


def quat_axis(axis, angle: float) -> list[float]:
    a = np.asarray(axis, dtype=float)
    a = a / max(np.linalg.norm(a), 1e-9)
    s = math.sin(angle * 0.5)
    return [float(a[0] * s), float(a[1] * s), float(a[2] * s), float(math.cos(angle * 0.5))]


def quat_x(angle: float) -> list[float]:
    return quat_axis((1, 0, 0), angle)


def quat_z(angle: float) -> list[float]:
    return quat_axis((0, 0, 1), angle)


def inv_translation_matrix(t) -> np.ndarray:
    x, y, z = [float(v) for v in t]
    # Return the matrix already laid out as glTF column-major floats.
    # Flattening this array in C order yields [1,0,0,0, 0,1,0,0, 0,0,1,0, -x,-y,-z,1].
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-x, -y, -z, 1],
    ], dtype=np.float32)


def sample_skin(master_path: Path) -> tuple[int, int, int]:
    im = np.asarray(Image.open(master_path).convert("RGB"))
    crop = im[170:1280, 60:780]
    r, g, b = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    mask = (r > g * 1.08) & (g > b * 0.95) & (r > 45) & (r < 190) & (g > 25) & (b > 18) & ((r - b) > 12)
    pix = crop[mask]
    med = np.median(pix, axis=0).astype(int)
    return tuple(int(v) for v in med)


def rotation_x_matrix(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def transform_vertices(vertices: np.ndarray, origin: np.ndarray, angle: float, axis: str = "x") -> np.ndarray:
    if abs(angle) < 1e-8:
        return vertices
    R = rotation_x_matrix(angle) if axis == "x" else np.eye(3)
    return (vertices - origin) @ R.T + origin


def build_adanna_proxy(
    glb_path: Path,
    obj_path: Path,
    rig_json_path: Path,
    parts_json_path: Path,
    master_path: Path,
    source_meta: dict,
) -> dict:
    skin_rgb = sample_skin(master_path)
    # Identity-lock palette; exact approved master sheet swatches retained separately.
    COLORS = {
        "SKIN": skin_rgb,  # median of approved portrait skin pixels, lifted for readability
        "SKIN_LIT": tuple(min(255, int(v * 1.18 + 8)) for v in skin_rgb),
        "HAIR": (18, 18, 21),
        "INDIGO": (37, 45, 80),
        "LEATHER": (64, 42, 31),
        "BRONZE": (154, 112, 57),
        "CORAL": (176, 74, 51),
        "SCAR": tuple(max(0, int(v * 0.78)) for v in skin_rgb),
    }

    joints = [
        ("Adanna_Root", None, (0.0, 0.0, 0.0)),
        ("Hips", "Adanna_Root", (0.0, 0.0, 0.96)),
        ("Spine", "Hips", (0.0, 0.0, 0.28)),
        ("Chest", "Spine", (0.0, 0.0, 0.28)),
        ("Neck", "Chest", (0.0, 0.0, 0.12)),
        ("Head", "Neck", (0.0, 0.0, 0.10)),
        ("HairKnot", "Head", (0.0, -0.03, 0.16)),
        ("LeftShoulder", "Chest", (-0.19, 0.0, 0.02)),
        ("LeftUpperArm", "LeftShoulder", (-0.10, 0.0, -0.06)),
        ("LeftForearm", "LeftUpperArm", (0.0, 0.0, -0.31)),
        ("LeftHand", "LeftForearm", (0.0, 0.0, -0.28)),
        ("RightShoulder", "Chest", (0.19, 0.0, 0.02)),
        ("RightUpperArm", "RightShoulder", (0.10, 0.0, -0.06)),
        ("RightForearm", "RightUpperArm", (0.0, 0.0, -0.31)),
        ("RightHand", "RightForearm", (0.0, 0.0, -0.28)),
        ("LeftUpperLeg", "Hips", (-0.11, 0.0, -0.08)),
        ("LeftLowerLeg", "LeftUpperLeg", (0.0, 0.0, -0.43)),
        ("LeftFoot", "LeftLowerLeg", (0.0, 0.08, -0.40)),
        ("RightUpperLeg", "Hips", (0.11, 0.0, -0.08)),
        ("RightLowerLeg", "RightUpperLeg", (0.0, 0.0, -0.43)),
        ("RightFoot", "RightLowerLeg", (0.0, 0.08, -0.40)),
    ]
    joint_names = [j[0] for j in joints]
    bone_index = {name: i for i, name in enumerate(joint_names)}
    joint_parent = {name: parent for name, parent, _ in joints}
    joint_local = {name: np.asarray(t, dtype=float) for name, _, t in joints}
    joint_global = {}
    for name, parent, _ in joints:
        joint_global[name] = joint_local[name] if parent is None else joint_global[parent] + joint_local[name]

    parts: list[dict] = []

    def add_part(name: str, mesh: trimesh.Trimesh, color, bone: str, *, swing: float = 0.0,
                 phase_offset: float = 0.0, category: str = "body") -> None:
        mesh = mesh.copy()
        v = np.asarray(mesh.vertices, dtype=float)
        f = np.asarray(mesh.faces, dtype=np.int64)
        if f.ndim != 2 or f.shape[1] != 3:
            raise ValueError(f"{name}: expected triangles, got {f.shape}")
        rgb = np.asarray(color, dtype=np.uint8)
        parts.append({
            "name": name,
            "vertices": v.tolist(),
            "faces": f.tolist(),
            "color": [int(x) for x in rgb],
            "bone": bone,
            "bone_index": bone_index[bone],
            "origin": joint_global[bone].tolist(),
            "swing": float(swing),
            "phase_offset": float(phase_offset),
            "category": category,
        })

    # Torso, wrap, neck, head. Geometry is a neutral technical proxy, not a likeness pass.
    add_part("TORSO", m1.make_beam((0, 0, 1.02), (0, 0, 1.54), 0.185, 12), COLORS["SKIN"], "Chest")
    add_part("CHEST_MASS", m1.make_beam((0, 0, 1.28), (0, 0, 1.56), 0.215, 12), COLORS["SKIN"], "Chest")
    add_part("NECK", m1.make_beam((0, 0, 1.58), (0, 0, 1.68), 0.062, 10), COLORS["SKIN"], "Neck")
    head = trimesh.creation.icosphere(subdivisions=1, radius=1.0)
    head.apply_scale((0.135, 0.118, 0.17))
    head.apply_translation((0, 0, 1.74))
    add_part("HEAD", head, COLORS["SKIN"], "Head")
    # Indigo hand-woven wrap: single approved costume read, no invented armour.
    add_part("INDIGO_WRAP", m1.make_beam((0, 0, 0.74), (0, 0, 1.22), 0.218, 14), COLORS["INDIGO"], "Hips")
    # Leather baldric from LEFT shoulder toward RIGHT hip; no blade or scabbard fit claim.
    add_part("LEATHER_BALDRIC", m1.make_beam((-0.17, 0.008, 1.53), (0.15, 0.008, 1.02), 0.032, 8), COLORS["LEATHER"], "Chest")
    # Spiral pendant (fictional design, mother keepsake) on chest.
    # Build at the origin, stand it upright, THEN move it to the sternum. Rotating the
    # already-lifted torus about the world origin (the previous order) threw the pendant
    # to knee height roughly 1.3 m in front of the body.
    pendant = m1.make_torus(0.055, 0.011, 0.0)
    pendant.apply_transform(trimesh.transformations.rotation_matrix(-math.pi / 2, [1, 0, 0]))
    pendant.apply_translation((0, 0.115, 1.43))
    add_part("SPIRAL_PENDANT", pendant, COLORS["BRONZE"], "Chest")
    # Coiled bronze armlet, LEFT upper arm only.
    armlet = m1.make_torus(0.082, 0.015, 1.37)
    armlet.apply_translation((-0.29, 0, 0))
    add_part("BRONZE_ARMLET", armlet, COLORS["BRONZE"], "LeftUpperArm")
    # Temple beads: 3 bronze cuffs + 2 coral beads at LEFT temple.
    for i in range(5):
        bead = trimesh.creation.icosphere(subdivisions=0, radius=0.018 if i >= 3 else 0.022)
        bead.apply_translation((-0.112, 0.015, 1.80 - i * 0.055))
        add_part(f"TEMPLE_BEAD_{i+1}", bead, COLORS["CORAL"] if i >= 3 else COLORS["BRONZE"], "Head")
    # Diagonal scar on LEFT cheekbone, as a subtle geometric read only.
    add_part("LEFT_CHEEK_SCAR", m1.make_beam((-0.055, 0.108, 1.745), (-0.095, 0.095, 1.695), 0.0045, 5), COLORS["SCAR"], "Head")
    # Thin braids, top half in a high knot. Approved identity lock, simplified groom.
    knot = trimesh.creation.icosphere(subdivisions=1, radius=1.0)
    knot.apply_scale((0.105, 0.095, 0.09))
    knot.apply_translation((0, -0.035, 1.91))
    add_part("HIGH_HAIR_KNOT", knot, COLORS["HAIR"], "HairKnot")
    rng = np.random.default_rng(4511)
    for i in range(14):
        t = i / 13.0
        x = (t - 0.5) * 0.20
        z0 = 1.83 + 0.02 * math.cos(t * math.pi)
        z1 = 1.34 + 0.14 * abs(t - 0.5) - 0.04 * rng.random()
        y1 = -0.11 - 0.10 * rng.random()
        braid = m1.make_beam((x, -0.015, z0), (x * 1.15, y1, z1), 0.010 + 0.002 * rng.random(), 5)
        add_part(f"BRAID_{i+1:02d}", braid, COLORS["HAIR"], "Head", swing=0.10, phase_offset=t * math.pi)

    # Limbs from joint pivots.
    limb_defs = [
        ("LEFT_UPPER_ARM", "LeftUpperArm", "LeftForearm", 0.058, -0.9, 0.0, "SKIN"),
        ("LEFT_FOREARM", "LeftForearm", "LeftHand", 0.048, -0.5, 0.7, "SKIN"),
        ("RIGHT_UPPER_ARM", "RightUpperArm", "RightForearm", 0.058, 0.9, math.pi, "SKIN"),
        ("RIGHT_FOREARM", "RightForearm", "RightHand", 0.048, 0.5, math.pi + 0.7, "SKIN"),
        ("LEFT_UPPER_LEG", "LeftUpperLeg", "LeftLowerLeg", 0.082, 1.0, math.pi, "SKIN_LIT"),
        ("LEFT_LOWER_LEG", "LeftLowerLeg", "LeftFoot", 0.060, 0.55, math.pi + 0.8, "SKIN_LIT"),
        ("RIGHT_UPPER_LEG", "RightUpperLeg", "RightLowerLeg", 0.082, -1.0, 0.0, "SKIN_LIT"),
        ("RIGHT_LOWER_LEG", "RightLowerLeg", "RightFoot", 0.060, -0.55, 0.8, "SKIN_LIT"),
    ]
    for name, bone_a, bone_b, radius, swing, phase_offset, color_key in limb_defs:
        p1 = joint_global[bone_a]
        p2 = joint_global[bone_b]
        add_part(name, m1.make_beam(p1, p2, radius, 8), COLORS[color_key], bone_a,
                 swing=swing, phase_offset=phase_offset, category="limb")
    for side in ("Left", "Right"):
        hand_bone = f"{side}Hand"
        hand = trimesh.creation.icosphere(subdivisions=0, radius=0.055)
        hand.apply_scale((1.0, 0.75, 1.3))
        hand.apply_translation(joint_global[hand_bone])
        add_part(f"{side.upper()}_HAND", hand, COLORS["SKIN"], hand_bone, category="limb")
        foot_bone = f"{side}Foot"
        foot = m1.make_box(joint_global[foot_bone] + np.array([0, 0.055, 0]), (0.11, 0.22, 0.065))
        add_part(f"{side.upper()}_FOOT", foot, COLORS["LEATHER"], foot_bone,
                 swing=0.25 if side == "Left" else -0.25, category="limb")

    # Combine parts into one skinned mesh.
    V, N, C, J, W, F = [], [], [], [], [], []
    offset = 0
    for part in parts:
        v = np.asarray(part["vertices"], dtype=np.float32)
        f_local = np.asarray(part["faces"], dtype=np.int64)
        mesh = trimesh.Trimesh(vertices=v, faces=f_local, process=False)
        normals = np.asarray(mesh.vertex_normals, dtype=np.float32)
        colors = np.tile(np.asarray(part["color"], dtype=np.float32) / 255.0, (len(v), 1))
        joints0 = np.tile(np.asarray([part["bone_index"], 0, 0, 0], dtype=np.uint16), (len(v), 1))
        weights0 = np.tile(np.asarray([1, 0, 0, 0], dtype=np.float32), (len(v), 1))
        V.append(v)
        N.append(normals)
        C.append(colors)
        J.append(joints0)
        W.append(weights0)
        F.append((f_local + offset).astype(np.uint32))
        offset += len(v)
    V = np.vstack(V)
    N = np.vstack(N)
    C = np.vstack(C)
    J = np.vstack(J)
    W = np.vstack(W)
    F = np.vstack(F)

    builder = GLTFBuilder()
    acc_pos = builder.add_accessor(V, "VEC3", 34962, minmax=True)
    acc_norm = builder.add_accessor(N, "VEC3", 34962)
    acc_color = builder.add_accessor(C, "VEC3", 34962)
    acc_joints = builder.add_accessor(J, "VEC4", 34962)
    acc_weights = builder.add_accessor(W, "VEC4", 34962)
    acc_indices = builder.add_accessor(F.reshape(-1), "SCALAR", 34963)
    acc_ibm = builder.add_accessor(
        np.stack([inv_translation_matrix(joint_global[n]) for n in joint_names]), "MAT4"
    )

    nodes = []
    for i, (name, parent, translation) in enumerate(joints):
        node = {"name": name, "translation": [float(x) for x in translation]}
        children = [j for j, (_, p, _) in enumerate(joints) if p == name]
        if children:
            node["children"] = children
        nodes.append(node)
    mesh_node_index = len(nodes)
    nodes.append({"name": "Adanna_SkinnedMesh", "mesh": 0, "skin": 0})

    # Animation clips. Quaternion order is x,y,z,w. Z is up in this proxy.
    animations = []

    def add_animation(name: str, times: np.ndarray, tracks: dict[str, list]) -> None:
        times = np.asarray(times, dtype=np.float32)
        acc_time = builder.add_accessor(times, "SCALAR", minmax=True)
        samplers, channels = [], []
        for joint_name, values in tracks.items():
            arr = np.asarray(values, dtype=np.float32)
            path = "translation" if arr.shape[-1] == 3 else "rotation"
            acc_out = builder.add_accessor(arr, "VEC3" if path == "translation" else "VEC4")
            samplers.append({"input": acc_time, "output": acc_out, "interpolation": "LINEAR"})
            channels.append({"sampler": len(samplers) - 1, "target": {"node": bone_index[joint_name], "path": path}})
        animations.append({"name": name, "samplers": samplers, "channels": channels})

    def cyclic(name: str, duration: float, amp: float, bob: float, samples: int = 9):
        times = np.linspace(0, duration, samples)
        tracks: dict[str, list] = {}
        for joint_name, swing, off in [
            ("LeftUpperArm", -0.85, 0.0), ("RightUpperArm", 0.85, math.pi),
            ("LeftForearm", -0.45, 0.7), ("RightForearm", 0.45, math.pi + 0.7),
            ("LeftUpperLeg", 1.0, math.pi), ("RightUpperLeg", -1.0, 0.0),
            ("LeftLowerLeg", 0.55, math.pi + 0.8), ("RightLowerLeg", -0.55, 0.8),
            ("LeftFoot", 0.20, math.pi), ("RightFoot", -0.20, 0.0),
            ("Head", 0.06, math.pi * 0.5),
        ]:
            tracks[joint_name] = [quat_x(swing * amp * math.sin(2 * math.pi * t / duration + off)) for t in times]
        tracks["Chest"] = [quat_z(0.045 * amp * math.sin(2 * math.pi * t / duration)) for t in times]
        tracks["Hips"] = [[0.0, 0.0, 0.96 + bob * (0.5 - 0.5 * math.cos(4 * math.pi * t / duration))] for t in times]
        add_animation(name, times, tracks)

    cyclic("idle", 2.0, 0.035, 0.008, 9)
    cyclic("walk", 1.0, 0.42, 0.035, 9)
    cyclic("run", 0.66, 0.78, 0.075, 9)

    # Jump: anticipation, extension, landing preparation.
    jump_times = np.array([0.0, 0.12, 0.30, 0.55, 0.82], dtype=np.float32)
    jump_tracks = {
        "Hips": [[0, 0, 0.86], [0, 0, 0.88], [0, 0, 1.02], [0, 0, 1.00], [0, 0, 0.90]],
        "LeftUpperArm": [quat_x(0.25), quat_x(-0.45), quat_x(-1.05), quat_x(-0.85), quat_x(-0.25)],
        "RightUpperArm": [quat_x(-0.25), quat_x(0.45), quat_x(1.05), quat_x(0.85), quat_x(0.25)],
        "LeftUpperLeg": [quat_x(0.55), quat_x(0.30), quat_x(-0.25), quat_x(0.15), quat_x(0.60)],
        "RightUpperLeg": [quat_x(-0.55), quat_x(-0.30), quat_x(0.25), quat_x(-0.15), quat_x(-0.60)],
        "Chest": [quat_z(0.0), quat_z(0.0), quat_z(0.04), quat_z(0.0), quat_z(0.0)],
    }
    add_animation("jump", jump_times, jump_tracks)
    land_times = np.array([0.0, 0.10, 0.24, 0.42], dtype=np.float32)
    land_tracks = {
        "Hips": [[0, 0, 0.83], [0, 0, 0.82], [0, 0, 0.92], [0, 0, 0.96]],
        "LeftUpperLeg": [quat_x(0.65), quat_x(0.60), quat_x(0.20), quat_x(0.0)],
        "RightUpperLeg": [quat_x(-0.65), quat_x(-0.60), quat_x(-0.20), quat_x(0.0)],
        "LeftUpperArm": [quat_x(-0.35), quat_x(-0.30), quat_x(-0.10), quat_x(0.0)],
        "RightUpperArm": [quat_x(0.35), quat_x(0.30), quat_x(0.10), quat_x(0.0)],
        "Chest": [quat_z(0.02), quat_z(0.02), quat_z(0.0), quat_z(0.0)],
    }
    add_animation("land", land_times, land_tracks)

    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "TDD Playable Adanna M1 proxy builder",
            "extras": {
                "classification": "RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER",
                "source": source_meta,
                "identity_locks": ["deep brown skin", "thin braids in high knot", "3 bronze cuffs + 2 coral beads at LEFT temple",
                                   "diagonal scar on LEFT cheekbone", "coiled bronze armlet on LEFT upper arm",
                                   "spiral bronze pendant", "indigo hand-woven wrap", "leather baldric LEFT shoulder to RIGHT hip"],
                "restrictions": ["no blade", "no unapproved V003 BACK/LEFT_SIDE", "no V013 item-5 claim",
                                 "no invented dimensions/canon/costume", "no final topology/UVs/PBR/groom"],
            },
        },
        "scene": 0,
        "scenes": [{"nodes": [0, mesh_node_index], "name": "Adanna_M1_Proxy"}],
        "nodes": nodes,
        "meshes": [{
            "name": "Adanna_M1_SkinnedProxy",
            "primitives": [{
                "attributes": {
                    "POSITION": acc_pos, "NORMAL": acc_norm, "COLOR_0": acc_color,
                    "JOINTS_0": acc_joints, "WEIGHTS_0": acc_weights,
                },
                "indices": acc_indices,
                "material": 0,
                "mode": 4,
            }],
        }],
        "materials": [{
            "name": "Adanna_M1_VertexColor_PBR_Intent",
            "pbrMetallicRoughness": {"baseColorFactor": [1.0, 1.0, 1.0, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.82},
            "doubleSided": True,
        }],
        "skins": [{
            "name": "Adanna_M1_Skeleton",
            "joints": list(range(len(joint_names))),
            "skeleton": 0,
            "inverseBindMatrices": acc_ibm,
        }],
        "animations": animations,
        "accessors": builder.accessors,
        "bufferViews": builder.buffer_views,
        "buffers": [{"byteLength": 0}],
    }
    # Patch buffer length after accessors are known.
    gltf["buffers"][0]["byteLength"] = len(builder.binary)
    GLTFBuilder.write_glb(glb_path, gltf, bytes(builder.binary))

    # Bind-pose OBJ for interchange/reopen test.
    obj_mesh = trimesh.Trimesh(vertices=V, faces=F, process=False)
    obj_mesh.visual.vertex_colors = np.uint8(np.clip(C, 0, 1) * 255)
    obj_mesh.export(obj_path)

    rig_info = {
        "classification": "RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER",
        "glb": str(glb_path.name),
        "obj": str(obj_path.name),
        "joint_count": len(joint_names),
        "joints": [{"index": i, "name": n, "parent": joint_parent[n], "translation": joint_local[n].tolist()} for i, n in enumerate(joint_names)],
        "animation_clips": [a["name"] for a in animations],
        "vertex_count": int(len(V)),
        "triangle_count": int(len(F)),
        "skin_weights": "single-bone rigid weights; proxy only, not final deformation",
        "source": source_meta,
        "restrictions": gltf["asset"]["extras"]["restrictions"],
        "colors": {k: list(v) for k, v in COLORS.items()},
    }
    rig_json_path.write_text(json.dumps(rig_info, indent=2), encoding="utf-8")
    parts_json_path.write_text(json.dumps({
        "classification": "CPU replay geometry parts for the rigged technical proxy",
        "parts": parts,
        "joint_positions": {k: v.tolist() for k, v in joint_global.items()},
    }, indent=2), encoding="utf-8")

    return {
        "vertex_count": int(len(V)),
        "triangle_count": int(len(F)),
        "joint_count": len(joint_names),
        "animation_clips": [a["name"] for a in animations],
        "skin_rgb": list(skin_rgb),
        "parts": len(parts),
    }
