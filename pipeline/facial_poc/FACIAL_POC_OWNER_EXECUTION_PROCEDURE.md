# Facial PoC — Owner-Mac Execution Procedure (Produce the Actual Adanna Face)

**Document ID:** TDD-IMPL-FACIAL-PROC · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM. **Purpose:** Give the owner a single, complete, executable procedure to produce the **actual Adanna facial-likeness PoC** in Blender, with verifiable renders and technical evidence. **PM owns driving this to completion.**
**Deliverable:** an actual Adanna facial model built in Blender from the approved portrait, with renders, turntable, QC report and evidence bundle — **not** the pipeline itself. The task closes only when the face is built, visually reviewed against the portrait, and technically qualified.

---

## 0. Current status (accurate)

- **Pipeline:** v2.3 — **BACKGROUND-SAFE + colour-socket fix** (all context-dependent Blender operators removed; BMesh mesh editing; portable shell error handling; `normalize_color` accepts RGB/RGBA and rejects invalid lengths; all material call sites audited). **Logic-tested in-sandbox** (stub-bpy end-to-end: build produces all outputs, verifier QUALIFIED, non-zero exit on FAILED; stub now enforces 4-component colour sockets) **+ syntax-verified**. **NOT functionally validated** (no real Blender execution — Blender cannot run in-sandbox; the v2.3 colour fix is code-complete and logic-verified but NOT Blender-verified).
- **The actual face has NOT been built.** This owner-Mac run is the single genuine Blender execution step — and it is now a clean run, not a debugging cycle: every context-dependent operator and logic bug has been caught and fixed in-sandbox.
- **PM completed everything possible in-sandbox:** full code audit, background-safe rewrite, BMesh topology, strict shell error handling, logic test (caught 4 real bugs invisible to syntax checks), syntax verification, runbook + checklist + orchestrator staged.
- **Character Art** owns facial modelling + likeness improvement. **Technical Art** owns Blender implementation/rigging/binding/QC. **Design** owns visual comparison/review. **PM** owns coordination, deadlines, escalation, evidence-based acceptance. **Owner** provides the approved portrait, executes the steps below, and gives the final creative likeness verdict.

## 1. Why this action is required
The facial-likeness task has been carried across multiple updates as pipeline documents. The **required deliverable is the actual face**, not more pipeline docs. The v2.1 pipeline is the means; the owner-Mac run produces the end. This step: builds the face → generates renders/QC → enables visual comparison → unlocks UE import + acceptance.

## 2. Prerequisites and required files
- **Blender 4.2.23 LTS** installed on the owner Mac.
- **Approved portrait:** `REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg` (Google Drive ID `1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF`). Place it at:
  ```
  <repo>/pipeline/facial_poc/reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg
  ```
  (or keep it anywhere and set `PORTRAIT_PATH` in Step 5).
- **Repository:** `The-Mhood/TDD`, branch **`arena/553fb02d-tdd`**, latest commit (ensure `git pull` is current before running).

## 3. Repository, branch, commit
- **Repo:** `The-Mhood/TDD`
- **Branch:** `arena/553fb02d-tdd`
- **Path:** `pipeline/facial_poc/`
- **Files present:** `build_adanna_facial_poc.py` (v2.1), `verify_facial_poc.py` (v2.1), `run_facial_poc.sh`, `FACIAL_POC_QUALIFICATION_CHECKLIST.md`.

## 4. Application to open
**Terminal + Blender 4.2.23 LTS (headless, background mode).** No Unreal Engine needed for this step (UE import is a later step).

## 5. Exact terminal commands, in execution order
```bash
# 1. Ensure the branch is current
cd /path/to/TDD
git fetch origin arena/553fb02d-tdd
git pull origin arena/553fb02d-tdd

# 2. Place the approved portrait (if not already in reference/)
mkdir -p pipeline/facial_poc/reference
cp "/path/to/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg" \
   pipeline/facial_poc/reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg

# 3. Make the orchestrator executable
chmod +x pipeline/facial_poc/run_facial_poc.sh

# 4. (If the portrait is NOT in reference/, point at it explicitly)
export PORTRAIT_PATH="/exact/path/to/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg"

# 5. Run the full pipeline (build → verify → evidence bundle)
cd pipeline/facial_poc
./run_facial_poc.sh
```

## 6. Expected successful output
- Exit code 0; console prints each QC check **PASS**.
- Files produced under `pipeline/facial_poc/output/`:
  - `ADANNA_FACIAL_POC_V2.fbx` — the character mesh + armature (backdrop excluded).
  - `ADANNA_FACIAL_POC_V2.blend` — the saved Blender scene.
  - `previews/ADANNA_FACIAL_POC_V2_{front,side,three_quarter,back}.png` — four still renders.
  - `turntable/frame_*.png` — the turntable sequence.
  - `evidence/BUILD_MANIFEST.json` — build metadata (tri count, vert count, skeleton, portrait).
  - `evidence/QC_RESULT.json` — **verdict = `QUALIFIED`** with every check PASS.
  - `evidence/EVIDENCE_BUNDLE_<timestamp>.txt` — consolidated evidence.

## 7. What to do if the result differs
- **Build errors:** capture `pipeline/facial_poc/output/evidence/RUN_<ts>.log` (or console) and return it to PM. PM owns the correction + re-iteration (Character Art / Tech Art fix; PM re-syntax-checks). **Do not** mark the face reviewed/qualified on a failed build.
- **QC_RESULT = FAILED:** read the failing check in `QC_RESULT.json` (e.g. skeleton missing a joint, binding inconsistent, portrait not loaded). Return the QC report + the `.blend` to PM. The specific correction is applied and the run repeated.
- **Likeness weak (QC passes but face does not resemble the portrait):** this is a **Character Art likeness iteration**, not a QC failure. Record the specific likeness problem (jaw shape, proportion, feature placement) and iterate the modelling — PM coordinates Character Art to correct and re-run. The task is **not** closed at the first face.

## 8. What to return (screenshots, logs, files, evidence)
Return to PM the **entire** `pipeline/facial_poc/output/` directory:
- `ADANNA_FACIAL_POC_V2.fbx` and `.blend`
- all `previews/*.png` and `turntable/*.png`
- `evidence/BUILD_MANIFEST.json`, `evidence/QC_RESULT.json`, `evidence/EVIDENCE_BUNDLE_<ts>.txt`
- **Visual comparison:** your assessment of `previews/ADANNA_FACIAL_POC_V2_front.png` against the approved portrait — **PASS / FAIL** with specific notes on what matches and what does not.

## 9. Where the evidence must be saved
- Save a copy of `output/` to the project evidence store on the Mac, e.g.:
  ```
  <project>/Saved/BuildEvidence/<timestamp>/facial_poc/
  ```
- Commit/push the returned evidence to the repo (or attach it to the PM report) so it is in the authoritative record.

## 10. What the result unlocks
- **QC PASS + likeness PASS:** the facial PoC is **technically qualified** → proceed to **UE import + integration acceptance** (Step 11 below). The facial-likeness deliverable is then closed (built, reviewed, qualified).
- **QC PASS but likeness FAIL:** Character Art iterates likeness → re-run → re-review. Not closed.
- **QC FAIL:** PM/Tech Art correct → re-run. Not closed.

## 11. UE import + integration acceptance (after Blender qualification passes)
1. **Why:** the PoC must work in Unreal, not just Blender.
2. **Prerequisites:** UE 5.8.4 project; the `ADANNA_FACIAL_POC_V2.fbx` from a qualified Blender run.
3. **Commands/steps:** import the FBX into UE (skeleton retarget to the shared `HUMAN_BASE_PROPOSED`, material/texture binding); place in a test level; render/capture the in-engine result.
4. **Expected output:** FBX imports cleanly; the face renders in UE; skeleton/expression controls function.
5. **If differs:** capture the import/run log; PM/Tech Art correct; iterate.
6. **Evidence:** UE import log + in-engine render captures; save to `Saved/BuildEvidence/<ts>/facial_poc_ue/`.
7. **Unlocks:** full facial-likeness PoC acceptance → informs the quality tier for full production.

## 12. Iteration rule
**Do not close the facial task at script completion or at the first generated face.** Close it only when: the actual Adanna face is built in Blender, renders + turntable + QC report + evidence bundle exist, QC passes, the face is visually compared against the approved portrait (PASS), and UE import + acceptance are demonstrated. PM tracks each iteration in the dependency register; Character Art/Tech Art own the corrections; the owner gives the final creative verdict.
