# M1 Adanna Character — Artist & Animator Production Specification

**Status:** Engineering-facing brief; not an art approval, character redesign, or authorization to generate/promote artwork.
**Project:** *The Disobedient Daughter* · Unreal Engine 5.8 canonical project
**M1 scope:** First playable character: launch, control, traverse a real 3D test space, use implemented movement actions, and interact with the world. No M2 environment production or M3 combat.

## 1. Purpose and current integration contract

The current project owns an `ATDDAdannaCharacter : ACharacter` pawn. It already uses Unreal's `CharacterMovementComponent`, a collision capsule, camera-relative movement input, jump input, and a collision-tested third-person spring arm/follow camera. The canonical GameMode selects this pawn and the project player controller.

The C++ pawn currently references **no** skeletal mesh, physics asset, animation Blueprint, skeleton, socket, weapon, or retargeted animation asset. The project has no character `Content/` asset tree or established character animation/retarget pipeline. Therefore:

- Provide an Unreal-importable skeletal character asset set; do not assume a mesh path, skeleton asset, socket name, or animation class already exists.
- Keep locomotion and collision authority in `CharacterMovementComponent` and the capsule. Animation presents movement; it must not drive authoritative traversal or replace collision.
- Mesh dimensions, root placement, capsule fit, mesh-relative offset, and camera composition must be checked together in Unreal. Do not bake arbitrary offsets into the mesh to compensate for a camera or capsule mismatch.
- Use a project-owned animation Blueprint and explicit asset references when integration is implemented; no hard-coded `/Game/...` path is prescribed by the present code.
- The game is not yet verified as compiled or playable in Unreal. Owner Mac build/editor/play verification remains required.

Relevant implementation: `Source/TheDisobedientDaughter/Public/Player/TDDAdannaCharacter.h`, `Source/TheDisobedientDaughter/Private/Player/TDDAdannaCharacter.cpp`, `Source/TheDisobedientDaughter/Private/TDDGameMode.cpp`, `Config/DefaultInput.ini`, and `docs/implementation/M1_FIRST_PLAYABLE_IMPLEMENTATION_PLAN.md`.

## 2. Design authority and exact references

### Approved identity references

1. **Primary, approved OAD-02 character master:** [`CHAR_ADANNA_MASTER_REFERENCE_V001.jpg` — location folder](https://drive.google.com/file/d/1k08XH8VjNJAnSoMNU4YvBPtBEUdYD20y/view) (`01_CHARACTERS/Adanna`, Drive ID `1k08XH8VjNJAnSoMNU4YvBPtBEUdYD20y`). Its approved-designs copy is [`CHAR_ADANNA_MASTER_REFERENCE_V001.jpg`](https://drive.google.com/file/d/1FY3hw3602iB-1405RgUIO3ih2USmck_Y/view) (ID `1FY3hw3602iB-1405RgUIO3ih2USmck_Y`). Use the location-folder master as the working source and retain the copy as a provenance cross-check.
2. **Supporting approved, text-free identity anchor:** [`REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg`](https://drive.google.com/file/d/1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF/view) (`18_REFERENCE_MATERIAL/Approved_Reference_Images`, ID `1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF`). This is identity support, not a full-body or costume turnaround.
3. **Interim, partial costume reference only:** [`B2_CAND_COSTUME_BREAKDOWN_V002_2560x1440.png`](https://drive.google.com/file/d/1OcNpG55dadGkIUUar7W0Vm5Lkb2QGLJR/view) (`01_CHARACTERS/Adanna`, ID `1OcNpG55dadGkIUUar7W0Vm5Lkb2QGLJR`). The current Art Bible index classifies it as **APPROVED — INTERIM PARTIAL UPPER-BODY WORKING REFERENCE ONLY**. It is not complete costume breakdown, final full-body costume canon, or authority to fill its hatched/blank areas. The image itself carries an older “unapproved/pending CD” panel; consult the current index/verdict status, not that stale embedded panel. The documented open items include three hatched placeholders, CQ-9, RQ-10-1, and approved full-body/back turnaround plates.

### Explicitly not approved as final modeling/turnaround source

The current Art Bible review continuation and controlling CD verdict do **not** approve a complete Adanna turnaround set. The front V004 has a blocked material-read issue; THREE_QUARTER V004 is not approved; LEFT_SIDE and BACK V003 are preserve/unapproved. Earlier V001/V002 candidates and newer V003/V004 candidates are not promoted by search visibility, existence, or a “preserve” direction. Do not combine them into a synthetic approved sheet, mirror them, repair them, regenerate from them, or infer missing anatomy/costume from them. Current review is closed; Round 7 is unexecuted and no regeneration is authorized by that verdict.

### Identity locks visible in approved records

Keep the approved identity as recorded: adult Adanna (25), deep brown skin, thin braids with the top half in a high knot, three bronze cuffs plus two coral beads at the **left** temple, diagonal scar on the **left** cheekbone, coiled aged-bronze armlet on the **left upper arm**, spiral bronze pendant (explicitly a fictional design), indigo hand-woven wrap, vegetable-tanned leather strap, athletic build, about 7.5 heads tall, not slimmed or glamorized, guarded/defiant default expression. No gold. Do not mirror the character or move/duplicate identifying features to improve recognition.

The current written reference says RIGHT temple, RIGHT cheek, and RIGHT arm are plain. The full-body clothing, lower-body garment and construction, back, closures/fasteners, blade/scabbard construction and strap-to-scabbard junction remain unresolved in the partial sheet. A character register records a single LEFT shoulder guard as approved and a short blade at the LEFT hip as a resolved placement decision, but the weapon asset itself is still listed REVIEW REQUIRED in the Art Bible index. Do not invent the guard's unseen construction or build/equip a production weapon from that placement decision alone. For M1's non-combat traversal lab, omit the weapon until its design asset and production permission are confirmed.

## 3. Work packages and priority

### A. M1 integration prototype — can begin now, separately from final art

A temporary visual proxy may be used to exercise pawn/animation wiring while the approved full-body art is pending. It must be obviously labelled **TEMPORARY / NOT ADANNA ART / NOT APPROVED**, must not be presented in screenshots or reviews as her finished model, and must be easy to replace without changing gameplay code. A capsule or neutral mannequin is acceptable as an engineering proxy only; do not customize it to imply Adanna's final clothing or silhouette. No proxy is required to start movement, obstacle lab, interaction, or Mac verification work.

The first asset-integration test should be a minimal import check in the canonical UE project: skeletal mesh visible on the existing pawn; feet visually grounded at rest; capsule encloses the body without excessive clipping; spring-arm camera frames the whole playable figure in motion; and walking, jump, fall, land, and dodge/traversal tests remain functional with animation disabled. Do not wait for final costume or animation polish to progress engineering.

### B. Final M1 Adanna production — gated by missing approved design

Before final full-body mesh production, obtain an approved full-body/front-side-back design or an explicit art-direction package that resolves the currently open construction. Until that happens, the artist may prepare a neutral technical blockout only, not make visual decisions to fill missing areas. Keep open questions visible in the delivery and seek approval; do not silently choose a lower-body garment, weapon build, rear costume, braid-tip details, belt/fastener, or armor construction.

Once design authority supplies the missing approved plates/specifications, produce the final game-ready body, costume, hair and approved accessories, then the M1 locomotion animation set and Unreal integration described below. New or revised art remains subject to the project's normal review and approval process; this spec is not a waiver.

## 4. Technical asset deliverables (recommended production contract)

These are technical delivery requirements for integration, **not new canon or visual direction**.

### Mesh and source files

- Deliver editable source scene in the artist's native DCC format plus interchange FBX for skeletal mesh, and FBX animation clips (or an agreed Unreal-compatible source format confirmed with engineering before production). Include a short README naming DCC/version, export settings, units, axis/orientation, scale, frame rate, and file/asset list.
- One deforming, game-ready skeletal body mesh for the approved final design. Separate rigid accessories only when useful for deformation/material management; preserve approved left/right placement. Do not add a weapon to this M1 non-combat deliverable unless the weapon review is cleared.
- Clean topology around shoulders, elbows, wrists, hips, knees, ankles, neck, and face for the required locomotion range. Provide sensible UVs, consistent normals/tangents, no accidental duplicate/internal faces, and a documented LOD0 plus reduced LODs appropriate to the target platform after profiling. Do not claim a polygon/texture budget is project-approved; propose budgets and get engineering approval against the actual Mac/target platform.
- Apply transforms, freeze/clean scale, one consistent human scale, and a clear forward axis. Author a neutral A-pose or T-pose only if needed for rigging/retargeting, and deliver a separate approved-rest-pose screenshot/turntable for review. Preserve proportions from approved references; do not use an unapproved turnaround as the measurement authority.
- Supply a suitable physics asset (or collision/physics authoring notes) for skeletal simulation needs. Player locomotion collision remains the existing capsule; the skeletal physics asset must not replace it.

### Skeleton and naming

- Deliver a humanoid deform skeleton with a single root, pelvis, spine chain, neck/head, clavicles, arms/hands, legs/feet, and optional facial controls/joints only if facial animation is in scope and approved. Use stable, documented bone names and a clean hierarchy; include no unexplained helper bones in the deform chain.
- Skin weights must support walk/run, start/stop, turns, jump/fall/land, dodge, and interaction reach without visible collapse or severe accessory penetration. Accessory bones, if any, must be documented and must not introduce unexplained alternate anatomy.
- Keep root motion out of M1 locomotion unless engineering explicitly decides otherwise. The intended M1 integration is in-place locomotion driven by CharacterMovementComponent, with any root-motion clip clearly separated and not enabled by default.
- Provide a skeleton hierarchy/export screenshot and a short retargeting note. UE retarget compatibility to the project-standard humanoid skeleton is a goal to validate in the actual UE 5.8 project, not an assumed guarantee. No project standard skeleton asset currently exists; engineering must choose/create and test the target before animation retarget is signed off.

### Materials and textures

- Create physically based Unreal materials with clear slots for skin, indigo cloth, leather, aged bronze, and any separately approved accessory. Avoid unnecessary material-slot proliferation; document which mesh sections map to which material.
- Deliver source textures and UE-ready textures with documented color space/compression/import settings. Include base color, normal, and packed masks only as needed by the approved look; use roughness/metallic values appropriate to the material rather than making everything shiny. Keep bronze aged, not gold. Do not introduce symbolic or culturally specific patterns/markings not present in an approved source.
- Skin and cloth microdetail should support the approved master at gameplay camera distance without overriding likeness or making the finish glamorized. The approved master image is a visual identity/costume cue, not a source photograph or a texture bake.
- Resolve final material interpretation of the braided-cord pendant and any open costume detail through the current review/approval path; do not assume the interim sheet's unresolved cord reading is settled.

## 5. Animation package

### Immediate M1 locomotion clips

Provide in-place, looping or one-shot clips as appropriate, with consistent frame rate, naming, root orientation, and start/end pose continuity:

- idle / locomotion idle, walk, run (or one locomotion cycle if the final M1 speed set is still being tuned);
- start and stop transitions, directional starts/stops if needed by the chosen blend graph;
- turn-in-place only if the implemented controller requires it;
- jump start, rising, falling, and land/recovery;
- dodge/traversal action clip(s) matching the implemented M1 movement action, including cancel/recovery poses as agreed with engineering;
- interaction reach/use and return-to-locomotion pose (one generic non-combat interaction is sufficient for the M1 lab).

Do not create attacks, hit reactions, combat states, parries, weapon flourish, or combat idle for M1; those belong to later authorized scope. Do not design a combat animation around an unapproved sword.

### Unreal animation setup and acceptance

- Supply an Animation Blueprint (or documented project-owned equivalent) for locomotion state selection, speed/direction, jump/fall/land state, and the agreed dodge/interaction states. It should consume movement state from the pawn and never move the authoritative capsule by itself.
- Provide a blend-space/state-machine diagram, clip list, notify list, and brief note describing any foot locking, turn behavior, additive layers, or curve dependencies. Use notifies only for non-authoritative presentation cues; gameplay timing/state remains in code.
- Validate retargeted clips on the actual final skeleton in Unreal 5.8. Deliver screenshots or a short capture of the mannequin-to-Adanna retarget preview, then a project test showing the imported assets on the pawn. Retarget pose, bone mapping, root settings, and any IK rig/retargeter assets must be included and named; never say “retarget-ready” without the actual test.
- Test transitions under acceleration changes, abrupt direction reversals, jump input, airborne control, landing on the lab's varied surfaces, dodge interruption/collision, and camera-facing movement. Check feet sliding, foot penetration, cloth/strap clipping, braid/accessory motion, armlet/pendant stability, and left/right fidelity.

## 6. Unreal import and handoff checklist

1. Engineer confirms the project target skeleton/retarget plan, content path/naming, LOD and texture budgets, collision expectations, and exact UE 5.8 exporter/importer settings before final export.
2. Artist delivers source scene, skeletal mesh FBX, animation FBXs, textures, material/slot map, physics asset or notes, LODs, skeleton hierarchy, retarget notes, and README as a versioned package. No replacement or edit of approved Drive references is part of this handoff.
3. Import into a dedicated, project-owned character content folder; create/verify skeleton, mesh, physics asset, materials, Animation Blueprint, IK/retarget assets if used, and clips. Keep filenames stable and use project conventions agreed at import.
4. Validate scale/orientation, bind pose, normals, material response, skinning, capsule fit, foot contact, camera framing, LOD transitions, animation retarget, and asset references in the canonical project.
5. Run owner-executed Mac Editor/Game builds and Unreal Automation; perform a manual M1 lab playtest at the exact tested commit. Record failures and asset versions. Static checks or successful file import alone do not prove playable M1 acceptance.
6. Retain a replaceable engineering proxy until final art passes import and review; then remove/disable only the proxy asset/reference through a reviewed change. Never rename or delete source art or Drive references as part of this integration.

## 7. Visual and production guardrails

- Exact approved identity sources and their scope in §2 take precedence over moodboards, unapproved character sheets, candidate turnarounds, screenshots, generated concepts, or this technical document.
- Do not use the broad World Bible moodboard as an Adanna modeling sheet. It contains mixed/legacy imagery and is not the OAD-02 reference.
- Do not treat a search result, file presence, file copy, “PRESERVE”, or exploratory/review status as design approval.
- Do not fill the missing rear/lower-body costume, reverse-side features, full armor, or blade/scabbard with plausible inventions. Submit questions/turnaround needs to the art authority and keep the affected work blocked/neutral.
- Keep all design review and cultural/technical gates intact. The current review is closed, Round 7 is unexecuted, and no regeneration is authorized by the current-cycle verdict.

## 8. Production authority documents to consult

- **Current exact candidate statuses and review limits:** `ART_BIBLE_MASTER_INDEX_CURRENT_REVIEW_VERDICT_v7.md` (Drive ID `1rpbhHDyWvlW4iTGeEw4tuThPDIA2YXSU`) and controlling `OUR_EYES_CURRENT_REVIEW_CD_VERDICT.md` (Drive ID `1zMTwzOX8NBxpg-E72hda-ARIzoiXHa0O`). The review handoff says Round 6 closed / Round 7 unexecuted; it does not authorize regeneration.
- **Approved identity and character locks:** OAD-02 master reference (Drive ID above), `CHARACTER_DESIGN_REGISTER.md` (Drive ID `1naNn0D7jAXOVc01Xvnl4YYEvS_zwcTjH`), and `OPEN_ART_DECISIONS.md` (Drive ID `1HkaV90iCq3Kmn3M8rgyNPiJ61m7UISPN`; use exact individual resolved/open entries, not a truncated search excerpt).
- **Costume partial only:** `B2_CAND_COSTUME_BREAKDOWN_V002_2560x1440.png` and its exact status/qualifications in the current index. Never treat as full-body approval.
- **M1 engineering contract:** `docs/implementation/M1_FIRST_PLAYABLE_IMPLEMENTATION_PLAN.md` plus the source files listed in §1. This is the code integration reference, not art authority.
- **Weapon authority, if the weapon is later brought into scope:** `WEAPON_ADANNA_PRIMARY_BLADE_V001.jpg` (Drive ID `1V12Sq2BZdIqjsgkx5GRpzGxc3nS3Gbac`) is listed as REVIEW REQUIRED in the Art Bible index. It is not an approved production weapon asset; M1 locomotion can proceed without it.

## 9. Gate summary

| Work | Can proceed now? | Gate / acceptance |
|---|---:|---|
| M1 movement, dodge integration, traversal lab, interaction, proxy pawn | Yes | Independent of final character art; proxy clearly marked temporary. |
| Technical rig/retarget planning | Yes | Engineering can select and test a target skeleton; document choices without implying design approval. |
| Final full-body Adanna model and definitive costume materials | Not from current refs alone | Requires approved full-body/rear/side design resolving open costume construction; preserve OAD-02 identity. |
| Final weapon and weapon animations | No for current M1 scope | Separate weapon asset remains review-required; M3 combat is out of scope. |
| Final M1 animation integration | Partial work can be prepared; final sign-off pending | Requires an approved final mesh/rig and successful UE 5.8 retarget/integration tests. |
| M1 playable acceptance | Not yet | Requires owner Mac build, Automation, and real manual playtest evidence at the tested commit. |
