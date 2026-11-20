# Our Eyes — final delegated CD disposition records

**Start with [G — Executive final report](G_EXECUTIVE_FINAL_REPORT.md).** Physical PENDING clearance is verified, with substantive authority/correction dependencies explicit.

| Record | Purpose |
|---|---|
| [A](A_MASTER_FINAL_VERDICT_REGISTER.md) | 193 final verdicts; CSV/JSON and 193 individual verdict files |
| [B](B_36_ASSET_RELEASE_PACKAGE.md) | Held-36 release package; copies, permissions, evidence and two selected replacements |
| [C](C_ISSUE_CLOSURE_REPORT.md) | G01–G16 and documentary D01–D04 decisions, completion versus dependencies |
| [D](D_CORRECTION_AND_REPLACEMENT_RECORD.md) | Six executed final attempts; four selected, two failed; preserved successor chains |
| [E](E_REJECTION_REGISTER.md) | Eleven submitted uses rejected, originals retained |
| [F](F_FINAL_PACKAGE_MANIFEST.md) | 193 identity/path/hash reconciliation plus derivatives/copies and clearance |
| [G](G_EXECUTIVE_FINAL_REPORT.md) | This executive final report |

## Bundle boundaries

- This records archive contains A–G, 193 individual final verdicts, six disclosed derivative outputs, correction proof/first attempts, verification ledgers and preserved historical assessment evidence. It does NOT duplicate all 193 original artwork/support payloads; those remain at their verified Drive destinations with immutable ID/hash joins.
- The dedicated held-36 portable ZIP separately includes exactly 36 original payloads and two selected derivative payloads, plus their verdicts/Research/proof. Other 157 original payloads are excluded.
- `evidence/HISTORICAL_*` files are preserved prior assessment material, NOT current authority and not a claim that earlier work executed this operation. Their old HOLD/proposed/no-execution wording is historical. Current A–G and delegated authority control this operation.
- `verification/SOURCE_SCOPE_193.json` and `DESTINATION_FOLDERS.json` retain immutable initial paths and historical assessment flags. Current execution is in A/F and the destination/copy ledgers; `FINAL_FOLDER_HIERARCHY.json` supplies post-move container paths.
- Source artwork-generation version, Drive metadata revision, dependency code and package-copy identity are different concepts. Metadata moves may increment Drive revision but do not rename artwork generations or delete history.
- Within C, D01–D04 name documentary errata; asset codes D01–D08 are separate.
- No credential, notification, permission change, original deletion/overwrite, incident recovery or repeat EXP quarantine was performed.

## Rebuild / audit

Use Python 3 with Pillow 13 and NumPy 2.4.6. Current records builders need only this records tree: `build_issue_decisions.py`, `build_final_register.py`, `build_final_reports.py`. Generation requires exact original source-ID payloads locally, and must never be run to overwrite adjudication: the generator writes separate `CORRECTION_GENERATION.json`, not `CORRECTION_ATTEMPTS.json`. The bundled E46 generated patch is the recorded non-deterministic input; later compositing is deterministic. Portable/ledger-protection code edits were compiled but not rerun over adjudicated outputs.

`validate_release.py` checks identity joins, counts, actual pixel masks/differences and archive integrity. Original/copy payload rechecks use ignored local download snapshots when available; a later environment must download the exact known IDs/hashes, not invent replacements. Byte opening is not semantic or cultural approval.

`PACKAGE_FILE_MANIFEST.json` and `SHA256SUMS.txt` seal records-archive members. The publication receipt is deliberately generated after uploads and kept outside the sealed archive, avoiding self-referential hashes. Documentation archives and their internal copies are not extra original counts.
