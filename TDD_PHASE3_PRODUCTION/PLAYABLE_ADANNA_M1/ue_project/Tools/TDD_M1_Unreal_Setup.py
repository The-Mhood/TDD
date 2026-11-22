#!/usr/bin/env python3
"""SUPERSEDED - do not run this file.

The original owner-side setup helper was written against a provisional UE 5.4 /
Windows-era assumption and contains defects that would leave the project without a
saved map and with a stale game-mode target:

  * uses unreal.EditorLevelLibrary (deprecated since UE 5.0, removed from the default
    path in UE 5.7+)
  * calls new_level(), which leaves no saved .umap on disk
  * never repoints GameDefaultMap/EditorStartupMap
  * imports a skinned GLB with no skeletal-mesh options

Nothing was deleted. The original file is preserved verbatim, with an explanatory
banner added at the top, at:

    Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py

The supported helper for the verified owner environment
(Apple M4 / 16 GB / macOS 27.2.1 / Unreal Engine 5.8) is:

    Tools/TDD_M1_Unreal_Setup_macOS.py

Run that one, following Tools/../README_MACOS_UE58.md. This stub replaces the old
filename only so that the obsolete helper cannot be launched by mistake; the audit
copy above still holds the original content for review.
"""

from __future__ import annotations

SUPERSEDED_BY = "Tools/TDD_M1_Unreal_Setup_macOS.py"
ORIGINAL_PRESERVED_AT = "Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py"


def main() -> None:
    message = (
        "[TDD M1] This helper is superseded and will not run.\n"
        "  Use:      %s\n"
        "  Original: %s\n"
        "  Runbook:  README_MACOS_UE58.md" % (SUPERSEDED_BY, ORIGINAL_PRESERVED_AT)
    )
    print(message)
    try:
        import unreal  # noqa: F401

        unreal.log_warning(message)
    except ImportError:
        pass


if __name__ == "__main__":
    main()
