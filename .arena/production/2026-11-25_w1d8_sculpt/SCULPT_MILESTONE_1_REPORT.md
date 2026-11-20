# SCULPT MILESTONE 1 — REPORT (2026-11-25, W1 D8)
Execution mode: Blender is unavailable in the Design sandbox, so sculpting was performed in the parametric sources that generate the qualified GLBs; the Mac finisher package (updated, checksums re-issued) regenerates `.blend`/FBX/previews from them. Qualified V2/V1 outputs remain untouched and recoverable (`6999ea7`/`a341f33`/`3fd912a`).

## Delivered
| Asset | File | Geometry | QC (sandbox, executed) |
|---|---|---|---|
| ADANNA_AD03_V3 | `out/ADANNA_AD03_V3.glb/.obj` (sha `ff570f8e…`) | 36 parts, 7,004 v / 13,668 tris | budget PASS 1.837 m; deformation PASS; 0 unweighted |
| GUARD_CLASS_V2 | `out/GUARD_CLASS_V2.glb/.obj` (sha `d4d5b060…`) | 23 parts, ~5.7k v / ~11k tris | budget PASS 1.772 m; deformation PASS; 0 unweighted |

## Sculpt changes (both, from D7–D10 register)
- **Face/head:** jaw volume, nose, brow band, lips (Adanna), dark eye insets, ears; neck retained.
- **Hands/feet:** palm + 4 fingers + thumb per hand; toe caps (Guard: sandal sole + toe strap).
- **Joints:** intersection joint-spheres removed (the scalloped ridges); limbs rebuilt as 6-ring tapered profiles — continuous shoulder/elbow/wrist/hip/knee transitions, weights/blends unchanged in scheme.
- **Garments (no more ellipsoid shells):** lathe-constructed wrap top + flared skirt with radial cloth folds and hem rings (Adanna); Guard wrap lathe + shoulder drape, skirt lathe, sash as a waist band standing proud of the skirt (two buried-sash iterations caught by preview inspection and fixed). Baldric retained with thickness; pendant now a 2-ring spiral stack.
- Skeleton, bone names, scale, material slots: **unchanged**. Identity locks intact; Guard unarmed/emblem-free; no blade/scabbard.

## Visual self-inspection (Design-side orthographic previews, `previews/`)
All 8 views rendered locally and read. Confirmed: face features readable; armlet coils on anatomical left; pendant forward; braids seated at back of head; fingers/toes present; Guard armband ring, shoulders connected, sash band visible. Known remaining (sculpt milestone 2 / in-Blender work): garment plan is circular-lathe (torso is elliptical — cloth sits slightly uniform), waist skin band between wrap and skirt by design of the two-piece wrap, facial modelling is base-volume level, no cloth thickness at hems yet (hem rings only).

## Mac rerun (regenerates .blend/FBX/official previews from V3/V2)
```bash
git pull
cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
find output -name '.DS_Store' -delete; find output -name '*.blend1' -delete
git add output && git commit -m "W1 D8 sculpt milestone 1 outputs: Adanna V3 + Guard V2" && git push origin arena/6e649a9b-tdd
```
New outputs land in `output/ADANNA_AD03_V3/` and `output/GUARD_CLASS_V2/`; the qualified V2/V1 folders stay as-is. Design re-inspects the 8 Blender previews on arrival; PM: hold integration on V3/V2 FBX until that visual pass, V2/V1 FBX remain the qualified builds meanwhile.
