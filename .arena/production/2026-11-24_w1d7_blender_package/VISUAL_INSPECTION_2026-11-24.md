# VISUAL INSPECTION — Mac qualification previews (Blender 4.2.23, owner commit `6999ea7`)
Inspector: Design (actual PNGs read directly, 2026-11-24). Scope: all 8 renders in `output/{ADANNA_AD03_V2,GUARD_CLASS_V1}/previews/`. Judged against the declared tier (parametric production-intent base mesh, Workbench shading), NOT against final-sculpt quality. Automated QC is recorded separately and not repeated here.

## What is actually visible — Adanna
Upright, correctly proportioned overall (head-torso-leg balance plausible; 1.837 m), arms/legs as smooth tapered tubes, indigo areas render **light grey** (see D5), skin a flat mid-brown. Front-named view actually shows her **back** (D1); the back-named view shows the chest: baldric diagonal and pendant-cord V are present and correctly placed, braided bars sit on the face side of the head in the front-named (rear) view (D6), the left-arm armlet renders as a **vertical grey strip**, not coils (D2). Hair knot reads as a clean black top sphere — good silhouette. Temple beads: tiny nubs at the head side, barely readable. Scar marker: not discernible at this shading/scale (geometry-audited, not visual). Feet are flat discs; hands are blunt tube ends; knee/elbow joint spheres ridge visibly (D8/D9). No NaN/explosions; no missing parts.

## What is actually visible — Guard
Broader torso, but the **arms hang detached from the torso at the shoulders** with a clear air gap (D3) and the **head floats** above the torso on a visible neck gap (D4 — both characters, worst on Guard). One-shoulder wrap reads as a grey ellipsoid intersecting the torso with a scalloped seam (D7); waist sash protrudes as a thin horizontal plate in side view (D11); armband is the same vertical-strip defect as Adanna (D2); sandal soles are thin discs barely visible under the feet. Silhouette otherwise coherent; no emblems/weapons (correct per V003 order).

## Defect register (severity: M=major at this tier, m=moderate, L=low/expected-at-tier)
| ID | Sev | Defect (evidence) | Fix applied this commit | Status |
|---|---|---|---|---|
| D1 | M | Finisher view labels swapped: `*_front.png` shows the back, `*_back.png` the chest (characters face +Y in Blender) | `finish_character.py` v1.3 camera positions corrected | FIXED in source; verify on rerun |
| D2 | M | Armlet coils (Adanna L) + armband (Guard R) render as vertical strips, not rings — torus `axis='x'` put the ring in the YZ plane | Builders: default Z-axis rings; pendant now `axis='y'` (faces forward; was edge-on front / full-circle side) | FIXED in GLBs (rebuilt) |
| D3 | M | Guard arms detached at shoulders (no shoulder volume; scaled offset) | Shoulder ellipsoid added per upper arm | FIXED in GLB (rebuilt) |
| D4 | M/m | Head floats; no neck (Guard major, Adanna minor) | Neck limb added to head part, both characters | FIXED in GLBs (rebuilt) |
| D5 | m | Workbench previews ignore embedded textures: indigo cloth renders light grey; cultural colour unreadable in QC renders | Finisher v1.3 `color_type = "TEXTURE"` | FIXED in source; verify on rerun |
| D6 | m | Adanna braids read as rigid black bars, proud of the head | Thinner (0.010/0.0075), seated closer | FIXED in GLB (rebuilt) |
| D11 | m | Guard sash protrudes as thin plate (R 0.175 < skirt radius) | Sash R 0.205, tube 0.030 | FIXED in GLB (rebuilt) |
| D7 | m | Wrap/skirt = intersecting ellipsoids; hard "swimsuit" cuts, exposed midriff band (Adanna), scalloped seam (Guard) | Not in this fix round — costume shells need the Blender sculpt pass | OPEN (sculpt phase) |
| D8 | L | Knee/elbow joint spheres ridge through limbs (scalloped rings) | — | OPEN (sculpt phase) |
| D9 | L | Blunt hand ends; flat disc feet; featureless head; beads/scar sub-readable | — | OPEN (sculpt phase; scar/beads geometry-audited present) |
| D10 | L | Guard proportions still mannequin-like (narrow head vs torso) | — | OPEN (sculpt phase) |

## Re-qualification after fixes (run in Design sandbox)
GLBs rebuilt: Adanna 4,404 v / 8,660 tris; Guard 3,212 v / 6,344 tris. Budget PASS (heights 1.837 / 1.771 m), deformation suite PASS both, weight audit 0 unweighted (`evidence/GLB_WEIGHT_AUDIT.json`), `INPUT_CHECKSUMS.sha256` updated (Adanna `90ebc864…`, Guard `a19208b4…`). **The committed `output/` renders remain the pre-fix qualification record (history preserved); the fixed models require one Mac rerun (§README) to produce matching `.blend`/FBX/previews.**

## Verdict
**Visually acceptable at the declared production-intent tier, conditional on the rerun confirming D1–D6/D11.** Not final-character approval; D7–D10 are the sculpt-phase work list. No identity-lock violations seen: baldric L→R, pendant present, coils on the correct (left) arm, no blade/scabbard, Guard unarmed and emblem-free.
