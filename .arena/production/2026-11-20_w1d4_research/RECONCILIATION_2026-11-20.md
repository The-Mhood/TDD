# RECONCILIATION RESOLUTION — 2026-11-20 (FP-10 blocker, CLOSED)
**Targets:** PENDING plates `SCENE_CH01-SCN-017_VILLAGE_SQUARE_V002.jpg`, `SCENE_CH01-SCN-024_AN_EMPTY_HOUSE_V002.jpg` vs rejected-wave `B2_CAND_SCENE_CH01-SCN-017_1672x941.jpg`, `B2_CAND_SCENE_CH01-SCN-024_1672x941.jpg`.

## Method
1. Live download of all four files from Drive (W1 D4); sha256 + dimensions; side-by-side native-res visual read; content description; caption-chrome inspection.
2. Hypothesis tested: "PENDING plate == rejected-wave plate (byte-identical or same render)" → inherited rejection.

## Findings
| Plate | PENDING (W1 D3-era) | rejected-wave B2 | Same file? |
|---|---|---|---|
| SCN-017 | 1536×1024 · sha256 `d3ca68891d6098fc47c2cf5eefdcaeb14a49780846565a8f406f4700041834fb` · 296,002 B · daylight enclosed village-square, close view, NO caption bar | 1672×941 · sha256 `736a0c61d1c7e6ca3d1662626026eaa9ee6b9bc8060cf30d081b8f4f785697ed` · golden-hour wide vista, caption bar “EXPLORATORY — NOT APPROVED CANON · STATUS: REVIEW REQUIRED … VERSIONS KEPT: V001 (rejected), V002 this plate · not to scale” | **NO — different bytes, different crop/composition/light** |
| SCN-024 | 1536×1024 · sha256 `b34f2ed2031384806493d317c75aa8d5ba067991dd8d5c625d0beec7ca23897f` · 428,777 B · exterior of empty hut, overcast, NO caption bar | 1672×941 · sha256 `5e1ba6a871cbfd97f890f18d29510b8dc978f5b1857b2c3a217245d60882c3f0` · INTERIOR (light beam, spilled grain), same caption-bar format | **NO — different bytes, different interior/exterior subject framing** |

## Resolution (FP-10 rule: resolution precedes verdict; clarity over assumption)
- **Not byte-identical; not the same renders.** Identity cannot be inherited by filename, tag “V002”, or shared subject. The rejected-wave rejection does NOT automatically transfer.
- **Equally:** PENDING plates carry NO version/status/provenance chrome; no source chain file; no link to a V001 correction ledger; they are of unknown lineage. Nothing about them is cleared by this comparison.
- **Ruling recorded in `FP10_FRESH_PASS_VERDICTS_2026-11-20.md`:** both → **REJECT (lineage / same design@V002)**: the PENDING plates depict the same designs as the rejected-wave plates (same scene IDs, same version tag V002, same composition family — enclosed square / empty house). Per FP-10, a design@version rejected once cannot be re-cleared as-is; the only honest path is a version bump V003+ with an explicit new direction. These files are retained in place (never deleted), quarantine-style, pending CD disposition.
- **No verdict this pass relies on inherited rejection or fuzzy similarity alone** — evidence = byte non-identity + shared design identity (scene ID + version tag + subject), which is the standard stated in FP-09/FP-10: same design in the same version class is the same submission.
- Registers: unchanged (FP-08 additive-only after CD ratifies). EXP-001: untouched.
## Prevention
Any re-submission of SCN-017 / SCN-024 MUST arrive as V003 with a new direction and correct chrome; filename reuse of V002 is auto-reject in future passes.
