# Adanna Facial-Likeness PoC — Qualification Checklist

**The Disobedient Daughter · TDD-IMPL-FACIAL-001 / TDD-IMPL-QUALPKG-001**
**To be completed by the OWNER on the owner Mac. Record actual results — do not pre-check.**

## A. Blender pipeline (agent-authored, owner-executed)
| # | Check | Expected | Result | Evidence |
|---|---|---|---|---|
| A1 | Build runs headless, exit 0 | no errors | ___ | `evidence/RUN_<ts>.log` |
| A2 | FBX exported (7.400, metric, scale 1.0) | `ADANNA_FACIAL_POC_V2.fbx` | ___ | sha256 in bundle |
| A3 | `.blend` saved | `ADANNA_FACIAL_POC_V2.blend` | ___ | sha256 in bundle |

## B. Technical QC (verify_facial_poc.py → QC_RESULT.json) — v2
| # | Check | Expected | Result | Evidence |
|---|---|---|---|---|
| B1 | file_integrity | FBX sha256 present | ___ | `QC_RESULT.json` |
| B2 | scale_orientation | METRIC, scale 1.0 | ___ | `QC_RESULT.json` |
| B3 | geometry | tris ≤ 20,000 | ___ | `QC_RESULT.json` |
| B4 | topology | 0 degenerate, 0 non-manifold | ___ | `QC_RESULT.json` |
| B5 | UV | objects have UV data | ___ | `QC_RESULT.json` |
| B6 | material_slots | all 7 canonical slots present | ___ | `QC_RESULT.json` |
| B7 | skin_weights | head bound to armature, weights set | ___ | `QC_RESULT.json` |
| B8 | skeleton | all 11 `HUMAN_BASE_PROPOSED` joints present | ___ | `QC_RESULT.json` |
| B9 | portrait_loaded | approved portrait loaded as reference | ___ | `QC_RESULT.json` |
| B10 | binding_consistency | all meshes bound to armature | ___ | `QC_RESULT.json` |

## C. Owner visual review (the likeness test — the actual quality gate)
Compare `previews/*.png` against `REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg`:
| # | Identity lock | Present & correct | Evidence |
|---|---|---|---|
| C1 | Deep brown skin (PBR) | ___ | front render |
| C2 | Thin braids, top half in high knot | ___ | front/side |
| C3 | **Left** temple: 3 bronze cuffs + 2 coral beads | ___ | left-side render |
| C4 | **Left** cheekbone: diagonal scar | ___ | left render |
| C5 | Coiled bronze armlet, **left** upper arm | ___ | side render |
| C6 | Spiral bronze pendant (fictional) | ___ | front render |
| C7 | Indigo hand-woven wrap | ___ | front render |
| C8 | Guarded/defiant default expression | ___ | turntable |
| C9 | No gold | ___ | all renders |
| C10 | Never mirrored; features not moved/duplicated | ___ | all renders |
| C11 | Reads as approved identity at gameplay camera distance (not generic/artificial) | ___ | owner verdict |

## D. UE integration acceptance (owner Mac, per INTSPEC-001 §6)
| # | Check | Expected | Result | Evidence |
|---|---|---|---|---|
| D1 | Import clean (no errors) | 0 errors | ___ | UE log |
| D2 | Skeleton binds to `Skeleton_HUMAN_BASE_PROPOSED` | correct bones | ___ | UE log |
| D3 | Collision + LOD present | capsule + LOD | ___ | UE |
| D4 | Materials/textures resolved | no missing | ___ | UE |
| D5 | Spawns in M1 greybox + renders | renders | ___ | screenshot |

## Verdict
- **PoC QUALIFIED** — all of A, B, C, D pass.
- **PoC FAILED** — any fail recorded above; record the failure, do not promote to production.
- **PoC NOT QUALIFIED** — not yet executed.

**Sign-off:** Technical Art ____ / Character Art ____ / Design Lead (owner) ____ / Engineering ____
**Do not promote to APPROVED PRODUCTION without all signatures + evidence.**
