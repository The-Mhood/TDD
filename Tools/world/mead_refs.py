#!/usr/bin/env python3
"""Locate the three divergent MEAD documents across refs, for tests and evidence.

The MEAD comparison is the finding that decides C-07, and it spans three branches.
Tests cannot depend on `/tmp` materialisations or on refs that happen to be fetched,
so this module resolves each document by an explicit ``(ref, path)`` pair and
returns ``None`` when a ref is unreachable. Callers decide whether to skip.

Why a module rather than inline code: two test modules and the evidence generator
all need the same answer, and a disagreement between them would be a silent error
of exactly the kind this milestone exists to catch.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Candidate MEADs. `ref` is a remote-tracking ref; `path` is relative to repo root.
CANDIDATES = {
    "A": {"ref": "origin/arena/5dde91a4-tdd", "path": "Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md"},
    "B": {"ref": "origin/a3branch", "path": "docs/MASTER_ENGINEERING_ARCHITECTURE.md"},
    "C": {"ref": "origin/a1branch", "path": "docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md"},
}


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def ref_exists(ref: str) -> bool:
    return _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}") is not None


def read(candidate: str) -> str | None:
    """Return the document text, or None if the candidate's ref is not fetched."""
    spec = CANDIDATES[candidate]
    if not ref_exists(spec["ref"]):
        return None
    return _git("show", f"{spec['ref']}:{spec['path']}")


def identity(text: str) -> dict:
    """Extract the formal identity block fields this project uses."""
    found = {"document_id": None, "version": None, "lines": len(text.splitlines())}
    for line in text.splitlines()[:40]:
        stripped = line.strip().lstrip("*# ").strip()
        if stripped.lower().startswith("document id:") and found["document_id"] is None:
            found["document_id"] = stripped.split(":", 1)[1].strip().strip("*").strip()
        if stripped.lower().startswith("version:") and found["version"] is None:
            found["version"] = stripped.split(":", 1)[1].strip().strip("*").strip()
    return found


def status_tags(text: str) -> set[str]:
    import re
    return set(re.findall(r"\bStatus\.[A-Za-z]+", text))


def has_section_5_4(text: str) -> bool:
    import re
    return bool(re.search(r"(?m)^#+\s*5\.4\s", text))


def all_identities() -> dict[str, dict | None]:
    out: dict[str, dict | None] = {}
    for key in CANDIDATES:
        text = read(key)
        out[key] = None if text is None else identity(text)
    return out
