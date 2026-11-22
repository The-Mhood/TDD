#!/usr/bin/env python3
"""Sandbox-safe Adanna skeletal GLB import-preparation audit.

This is a naming/presence audit only: it does not approve the proxy or claim
native Unreal import, retargeting, deformation, PIE, cook, or package success.
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

REQUIRED_NODES = {
    "Adanna_Root", "Hips", "Spine", "Chest", "Neck", "Head",
    "LeftShoulder", "LeftUpperArm", "LeftForearm", "LeftHand",
    "RightShoulder", "RightUpperArm", "RightForearm", "RightHand",
    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
    "RightUpperLeg", "RightLowerLeg", "RightFoot",
}
REQUIRED_ANIMATIONS = {"idle", "walk", "run", "jump", "land"}


def glb_document(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) < 20:
        raise ValueError("file too small for GLB JSON chunk")
    magic, version, total, chunk_len, chunk_type = struct.unpack_from("<IIIII", raw, 0)
    if magic != 0x46546C67 or version != 2 or total != len(raw):
        raise ValueError("invalid GLB v2 container/header length")
    if chunk_type != 0x4E4F534A or 20 + chunk_len > len(raw):
        raise ValueError("first GLB chunk is not a valid JSON chunk")
    return json.loads(raw[20:20 + chunk_len].decode("utf-8"))


def audit(path: Path) -> dict:
    doc = glb_document(path)
    nodes = {n.get("name", "") for n in doc.get("nodes", [])}
    animations = {a.get("name", "") for a in doc.get("animations", [])}
    missing_nodes = sorted(REQUIRED_NODES - nodes)
    missing_animations = sorted(REQUIRED_ANIMATIONS - animations)
    return {
        "asset": str(path),
        "classification": "technical proxy; provisional; not creative-approved",
        "ok": not missing_nodes and not missing_animations and bool(doc.get("skins")),
        "node_count": len(nodes),
        "skin_count": len(doc.get("skins", [])),
        "animation_count": len(animations),
        "missing_required_nodes": missing_nodes,
        "missing_required_animations": missing_animations,
        "native_ue_import_verified": False,
        "compile_pie_cook_package_verified": False,
        "scope": "static GLB skeleton/clip names only",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("glb", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    try:
        result = audit(args.glb)
    except (OSError, ValueError, json.JSONDecodeError, struct.error) as exc:
        result = {"asset": str(args.glb), "ok": False, "error": str(exc)}
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
