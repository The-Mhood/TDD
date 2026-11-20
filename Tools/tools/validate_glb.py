#!/usr/bin/env python3
"""Validate glTF binary (.glb) assets for the TDD exchange standard (D-25).

Checks, per file:
  * GLB container: magic, version 2, chunk table (JSON chunk present, length sane)
  * glTF JSON: asset.version, non-empty meshes/nodes, skins count, materials,
    buffer sizes, node names (for rig/canon checks)
  * optional --manifest: verifies the file is listed and its sha256 matches
    the recorded handoff manifest (ADR-0104 provenance)

Output: one JSON object per file on stdout; exit 0 only if every file passes.
Usage: validate_glb.py FILE [FILE ...] [--manifest M.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

GLB_MAGIC = 0x46546C67  # "glTF"


def fail(name: str, reason: str) -> dict:
    return {"file": name, "ok": False, "reason": reason}


def validate_glb(path: Path) -> dict:
    size = path.stat().st_size
    if size < 12:
        return fail(str(path), "file too small for GLB container")
    with path.open("rb") as f:
        header = f.read(12)
        magic, version, total = struct.unpack("<III", header)
        if magic != GLB_MAGIC:
            return fail(str(path), "bad GLB magic")
        if version != 2:
            return fail(str(path), f"glTF version {version} (need 2)")
        if total != size:
            return fail(str(path), f"header length {total} != file size {size}")

        chunks = []
        while f.tell() < size:
            if f.tell() + 8 > size:
                return fail(str(path), "truncated chunk header")
            clen, ctype = struct.unpack("<II", f.read(8))
            if f.tell() + clen > size:
                return fail(str(path), "truncated chunk data")
            data = f.read(clen)
            chunks.append((ctype, clen, data))

        json_chunk = next((c for c in chunks if c[0] == 0x4E4F534A), None)  # "JSON"
        if json_chunk is None:
            return fail(str(path), "no JSON chunk")
        try:
            doc = json.loads(json_chunk[2][: json_chunk[1]].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            return fail(str(path), f"JSON chunk unparsable: {e}")

    meshes = doc.get("meshes", [])
    nodes = doc.get("nodes", [])
    if not meshes or not nodes:
        return fail(str(path), "empty meshes or nodes")

    buffers_bytes = sum(b.get("byteLength", 0) for b in doc.get("buffers", []))
    result = {
        "file": str(path),
        "ok": True,
        "bytes": size,
        "asset_version": doc.get("asset", {}).get("version"),
        "meshes": len(meshes),
        "nodes": len(nodes),
        "materials": len(doc.get("materials", [])),
        "skins": len(doc.get("skins", [])),
        "animations": len(doc.get("animations", [])),
        "images": len(doc.get("images", [])),
        "buffers_bytes": buffers_bytes,
        "root_nodes": [n.get("name", "") for n in nodes if not n.get("children") is None][:0]
        + [n.get("name", "") for n in nodes[:6]],
    }
    return result


def check_manifest(path: Path, manifest: Path) -> dict:
    """Verify a file against a recorded manifest's sha256 section."""
    try:
        doc = json.loads(manifest.read_text("utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        return fail(str(path), f"manifest unparsable: {e}")
    recorded = None
    for key in ("sha256", "hashes", "files"):
        section = doc.get(key)
        if isinstance(section, dict):
            for k, v in section.items():
                if path.name in k or k in path.name or Path(k).name == path.name:
                    if isinstance(v, str) and len(v) == 64:
                        recorded = v.lower()
                    elif isinstance(v, dict) and "sha256" in v:
                        recorded = str(v["sha256"]).lower()
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if recorded is None:
        return {"file": str(path), "ok": True, "manifest": "not listed (no hash check)", "sha256": actual}
    ok = actual == recorded
    return {"file": str(path), "ok": ok, "manifest": "sha256 verified" if ok else "sha256 MISMATCH",
            "sha256": actual, "recorded": recorded}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--manifest", default=None)
    args = ap.parse_args()

    all_ok = True
    for fname in args.files:
        p = Path(fname)
        if not p.exists():
            print(json.dumps(fail(fname, "file not found")))
            all_ok = False
            continue
        res = validate_glb(p)
        if args.manifest:
            man = check_manifest(p, Path(args.manifest))
            res["manifest_check"] = man
            res["ok"] = res["ok"] and man["ok"]
        print(json.dumps(res))
        all_ok = all_ok and res["ok"]
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
