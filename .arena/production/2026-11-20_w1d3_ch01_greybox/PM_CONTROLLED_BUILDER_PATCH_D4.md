# PM-controlled builder corrections — W1 D4

**Upstream:** Design builder from `d50658a346a9cda4ba851aa24979f1b9d9cddc70` (original imported blob SHA-1 `e0dc070c365ffcce187842da3b3a5d42004626fb`).
**Working file:** `build_ch01_greybox.py`; the Design branch remains untouched.
**Status:** source changes and Python syntax validated; Blender execution, FBX generation, UE import and collision/PIE behavior are still unverified.

Static review against the imported §9 spec found that the original gate leaves spanned the entire 2.4 m opening and all registered interior buildings were solid cubes. The PM branch now carries an explicit, separately documented follow-up rather than silently treating the Design snapshot as playable:

1. Repositioned both gate leaves alongside the east wall and labeled them `GATE_LEAF_OPEN_A/B`, so the intended doorway is clear in the plan geometry.
2. Added a reusable `room_shell` helper with floor, perimeter walls and an open 0.95 m south doorway (1.2 m for backrooms); huts and the registered small interiors now use shells rather than solid room blocks.
3. Replaced the proposed Potter's Yard block with an open ground plane.
4. Replaced the solid Palace Portal with two piers plus a lintel and changed the Palace Hall to an enterable shell facing the square-to-palace approach.
5. Added gate state and enterable-shell inventory to the generated manifest.
6. Updated `render_plan.py` to draw the gate leaves in their open positions. Preserved the original Design schematic as `CH01_GREYBOX_PLAN_DESIGN_D506.png` and rendered the corrected 1350×1350 working plan.

This is a functional greybox correction, not a cultural/architectural approval. The primitive collision, clearances, wall/floor contacts, entrance orientation, FBX actor separation, navigation and route playability must still be checked in actual Blender/UE. If those tests fail, adjust and regenerate; do not infer success from source geometry or the schematic.

The exact pre-patch Design blob hashes are retained in `evidence/IMPORT_HASH_VERIFICATION.txt`; post-import working hashes and validation are recorded separately in `evidence/POST_IMPORT_PATCH_VALIDATION.txt`.
