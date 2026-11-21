# Blender Qualification — PREPARATION package (2026-12-05)
**This is preparation, NOT qualification.** Qualification happens only when the package runs on the owner's Mac (Blender 4.2 LTS) and its outputs are committed back.
## Ready and verified from the sandbox side
- Package: `2026-11-24_w1d7_blender_package/run_all.sh` — fail-safe verified (exit 3, checksum pass, no Blender in sandbox).
- Inputs pinned by SHA-256 in `INPUT_CHECKSUMS.sha256`: ADANNA_AD03_V5 `7d8ff320...`, GUARD_CLASS_V3 `70bd81fe...`.
- Source evidence complete: joint-influence PASS, deformation PASS, inspected previews, concept-vs-3D comparison (V5).
## Mac run (owner, ~one command)
`git pull` -> `cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh` -> commit `output/ADANNA_AD03_V5/` + `output/GUARD_CLASS_V3/` back.
## Acceptance criteria for the qualification result (pre-agreed)
FBX exports import clean; joint pose deltas match source validation; previews match concept locks (Adanna) / V3 costume authority (Guard); no scale/height regression (ROOT_CAUSE_HEIGHT/ICOSPHERE docs in package).
## After heroes qualify (optional second Mac batch)
NPC family (6 GLBs, hashes in readiness review JSON) can be added to the package the same way — Design will extend INPUT_CHECKSUMS + run_all inputs on request; they are not in the current pinned run.
