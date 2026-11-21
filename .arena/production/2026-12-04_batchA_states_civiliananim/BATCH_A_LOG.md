# BATCH A LOG (2026-12-04) - ST02 day key + civilian animation reference
Quality criteria set before generation: same compound/camera as approved state series; light-only change; plain solid cloth (approved civilian spec); West African identity; full-body uncropped; pose readability (idle/walk/look-back).
| Asset | Attempts | Decisions |
|---|---|---|
| ST02_DAY.jpg | 1 | ACCEPT attempt 1 - same compound/framing, neutral midday, short shadows, no people. PROVISIONAL lighting key (completes ST01-ST04 set with its own file; ST02 no longer borrowed from Kit V1). |
| CIVILIAN_ANIMATION_REFERENCE_V1.jpg | 4 (+2 generation failures, retried with simplified prompts) | REJECT a1: woven stripe borders on wrappers vs approved plain cloth (`_rejected/..._attempt1_stripedcloth.jpg`). REJECT a2: figures not West African (`_rejected/..._attempt2_wrong_identity.jpg`). REJECT a3: bottom-row cropping + men's one-shoulder toga read (`_rejected/..._attempt3_toga_and_crop.jpg`). ACCEPT a4: identity, plain cream/indigo cloth, waist-wrapper men, chest+skirt women, idle/walk/look-back readable, uncropped. Note: pose reference only - costume lengths governed by clothing board + 3D models. |
Batch consistency check: ST02 + population reference (Batch B) share compound, palette and midday values; civilian board cloth colours match NPC material family.
