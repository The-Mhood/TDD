#!/usr/bin/env python3
"""Build B–G and held-cohort documentation from completed, separate ledgers.
No Drive mutation, new approval inference or raw-response fabrication.
"""
from pathlib import Path
import json,csv,collections,hashlib,shutil,re
B=Path(__file__).resolve().parents[1]
ROOT=B.parent
A=json.loads((B/'A_MASTER_FINAL_VERDICT_REGISTER.json').read_text())
BY={r['code']:r for r in A}
SCOPE={r['code']:r for r in json.loads((B/'verification/SOURCE_SCOPE_193.json').read_text())}
F=json.loads((B/'verification/DESTINATION_FOLDERS.json').read_text())
HIER=json.loads((B/'verification/FINAL_FOLDER_HIERARCHY.json').read_text())
PF=json.loads((B/'verification/package36_folders.json').read_text())
CP=json.loads((B/'verification/copy_plan.json').read_text())
CORR=json.loads((B/'correction_evidence/CORRECTION_ATTEMPTS.json').read_text())
ISS=json.loads((B/'verification/issue_decisions.json').read_text())
CLEAR=json.loads((B/'verification/PHYSICAL_CLEARANCE.json').read_text())
R36=json.loads((B/'verification/research_36_payload_checks.json').read_text())
assert len(A)==193 and all(r['destination_verification']['complete_destination_verified'] for r in A)
assert len(CP)==38 and all(r['complete_copy_verified'] for r in CP)
assert len(CORR)==6 and all(r['independent_download_verified'] for r in CORR)
assert CLEAR['status']=='PENDING CLEARED'
HELD=[r for r in A if r['in_held_36']]
assert len(HELD)==36 and {r['code'] for r in HELD}=={r['code'] for r in R36}
PNAMES={'release':'01_RELEASE_NOW_DEFINED_SCOPE','reference':'02_REFERENCE_PRESERVED_UNAPPROVED','external':'03_EXTERNAL_AUTHORITY_REQUIRED','rejected':'04_REJECTED','replacements':'05_SUPERSEDED_AND_SELECTED_REPLACEMENTS'}
COUNT=collections.Counter(r['final_verdict'] for r in A)
NO_PROD='No cultural authentication, engineering/production acceptance, canon promotion or complete scene/turnaround approval is granted by this operation.'
DATE='2026-11-16 (session execution date; embedded 2026-11-17/18 source labels are preserved historical labels, not adopted as the execution date)'

def out(name,text): (B/name).write_text(text.rstrip()+'\n')
def js(name,value): out(name,json.dumps(value,indent=2,ensure_ascii=False))
def filelink(ident,label=None): return f'[{label or ident}](https://drive.google.com/file/d/{ident}/view)'
def folderlink(ident,label): return f'[{label}](https://drive.google.com/drive/folders/{ident})'
def clean(s): return str(s).replace('|','/').replace('\n',' ')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers)]+['| '+' | '.join(clean(x) for x in r)+' |' for r in rows])
def csvout(name,rows,cols):
    with (B/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
        for r in rows: w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def fingerprint(p):
    raw=p.read_bytes();return {'bytes':len(raw),'md5':hashlib.md5(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest()}
def identity(r):
    return {k:r[k] for k in ['code','name','source_id','source_drive_version','source_size','source_md5','source_sha256','research_id','research_drive_version','research_sha256','role','final_verdict','final_parent_id','final_path']}

def build_c():
    enriched=[]
    lines=['# C — Issue closure and documentary errata report','',f'Execution record: {DATE}.','',
           '**All G01–G16 and documentary errata D01–D04 have final disposition decisions below. This is not a claim that every substantive cultural/technical gate or missing correction is complete.** External cases and failed lighting work are expressly reserved, with permanent storage and objective tests. Directions are not completion evidence.','',
           'Codes D01–D04 in this issue report are *erratum identifiers*; the separately named asset codes D01–D08 remain distinct. Exact affected source IDs, source hashes, Research IDs and final destinations are embedded in the companion JSON and in A. Historical assessment-only issue text remains unchanged in `evidence/HISTORICAL_ISSUES_ASSESSMENT_ONLY.md`.','',
           '## Decision index','',table(['Issue','Final state','Affected code scope'],[(r['issue_code'],r['final_state'],'all 193' if len(r['scope_codes'])==193 else ', '.join(r['scope_codes'])) for r in ISS]),'']
    for r in ISS:
        er={**r,'affected_exact_originals':[identity(BY[c]) for c in r['scope_codes']]}
        for p in r['evidence_paths']: assert (B/p).exists(),p
        enriched.append(er)
        lines.extend([f"## {r['issue_code']} — {r['title']}",'',f"**{r['final_state']}**",'',
                      '**Exact underlying scope:** '+('all 193 originals, resolved by the ID/hash map in A and C JSON' if len(r['scope_codes'])==193 else '; '.join(filelink(BY[c]['source_id'],c) for c in r['scope_codes'])), '',
                      '### Verified facts',r['verified_facts'],'','### CD decision and rationale',r['cd_decision_and_rationale'],'','### Precise directions / non-actions',r['precise_directions'],'','### What actually completed',r['actual_completion'],'','### Remaining dependency and objective closure test',r['remaining_dependency_and_objective_test'],'','### Assumptions expressly not made',r['assumptions_not_made'],'','### Recorded evidence','; '.join(f'[{Path(p).name}]({p})' for p in r['evidence_paths']),''])
    lines.extend(['## Reserved original-file authority and correction dependencies','',
                  'The following table is an explicit, finite handoff specification, not a notification, a claim of assignment acceptance or a new assessment cycle. Files are already permanently filed outside APPROVED. No individual consultant is invented; the precise competent role is specified because no named appointee was provided.',''])
    for r in [r for r in A if r['destination_category'] in ['external','corrections']]:
        lines.extend([f"### {r['code']} — {r['final_verdict']}",f"- Exact original: {filelink(r['source_id'],r['name'])}.",f"- Required role: {r['required_role']}",f"- Exact question: {r['authority_question']}",f"- Missing evidence/tool: {r['missing_input']}",f"- Objective test: {r['objective_closure_test']}",f"- Permanent storage: `{r['final_path']}`.",''])
    out('C_ISSUE_CLOSURE_REPORT.md','\n'.join(lines));js('C_ISSUE_CLOSURE_REPORT.json',enriched)
    return enriched


def build_d():
    lineage=[]
    for r in A:
        if r['destination_category']!='superseded':continue
        suc=BY.get(r['successor_code']);cr=r.get('correction_result')
        lineage.append({'source_code':r['code'],'source_id':r['source_id'],'source_name':r['name'],'source_sha256':r['source_sha256'],'source_preserved_verified':True,'relationship':'version_lineage_not_approval' if suc else 'actually_selected_bounded_derivative','successor_code':r['successor_code'] or r['selected_derivative'],'successor_id':suc['source_id'] if suc else cr['new_drive_id'],'successor_name':suc['name'] if suc else cr['output_name'],'successor_verdict':suc['final_verdict'] if suc else cr['cd_visual_decision'],'qualification':'Following a successor does not promote any older file; selected derivatives are internal studies only. Failed E53/E54 grades are never replacement links.'})
    assert len(lineage)==24 and sum(r['relationship']=='actually_selected_bounded_derivative' for r in lineage)==4
    attempts=[{'local_path':str(p.relative_to(B)),**fingerprint(p),'state':'UNSELECTED_LOCAL_FIRST_ATTEMPT_OR_HISTORICAL_GENERATION_LEDGER; not separately published replacement'} for p in sorted((B/'correction_evidence/attempt01').glob('*')) if p.is_file()]
    record={'executed_final_attempts':CORR,'accepted_selected_derivative_count':4,'failed_not_replacement_count':2,'original_successor_relationships':lineage,'local_first_attempt_evidence':attempts,'uncompleted_original_corrections':[identity(r)|{k:r[k] for k in ['direction','required_role','missing_input','objective_closure_test']} for r in A if r['destination_category']=='corrections'],'reproducibility_note':'The generator was actually executed to make these outputs. Later portability/ledger-protection edits use the identical bundled E46 patch and separate CORRECTION_GENERATION.json. Those later edits were compiled and outputs validated, not rerun over the adjudicated outputs. CORRECTION_ATTEMPTS.json remains final adjudication, never inferred from generator success.'}
    js('D_CORRECTION_AND_REPLACEMENT_RECORD.json',record)
    lines=['# D — Correction and replacement record','',
           '**Six final derivative attempts were actually generated, inspected, uploaded and independently downloaded/opened/hash-verified: four selected limited studies, two failed lighting grades.** No original was overwritten. Earlier unselected D06/E50 attempts remain in `correction_evidence/attempt01/`.','',NO_PROD,'',
           table(['Source','Separate output','Actual visual decision','Native size','Changed pixels'],[(r['source_code'],filelink(r['new_drive_id'],r['output_name']),r['completion_state'],'×'.join(map(str,r['dimensions'])),r['changed_pixels']) for r in CORR]),'']
    for r in CORR:
        selected=r['source_code'] in ['D03','D06','E46','E50']
        lines.extend([f"## {r['source_code']} — {'SELECTED LIMITED STUDY' if selected else 'FAILED; NOT A REPLACEMENT'}",'',
                      f"- Exact unchanged source: {filelink(r['source_id'],r['source_name'])}.",f"- Source SHA256: `{r['source_sha256']}`.",f"- Separate output: {filelink(r['new_drive_id'],r['output_name'])}.",f"- Output: {r['output_bytes']:,} B; MD5 `{r['output_md5']}`; SHA256 `{r['output_sha256']}`.",f"- Method: {r['method']}.",f"- Difference bbox: `{r['difference_bbox']}`; changed pixels {r['changed_pixels']:,}; out-of-mask changes: {r['out_of_mask_changed_pixels']}.",f"- Mask: [{Path(r['allowed_mask_path']).name}](correction_evidence/{Path(r['allowed_mask_path']).name}); actual changed-pixel map: [{Path(r['actual_difference_path']).name}](correction_evidence/{Path(r['actual_difference_path']).name}).",'- Upload and independent new-ID derivative download, full PNG decode, dimensions, byte count, MD5 and SHA256: **PASS**.'])
        if 'changed_art_pixels' in r:
            lines.extend([f"- **Art-only** changes: {r['changed_art_pixels']} pixels, bbox `{r['art_difference_bbox']}`; every figure-art RGB outside cord mask unchanged. The >1-million whole-board delta includes explicitly authorised new documentary-margin chrome; it is not a cord-only total.",'- Pendant silhouette, pose, alignment, scale, likeness, costume and baldric preserved; D06 repaired arm not repainted. LEFT_SIDE/BACK remain V003 / PRESERVE / UNAPPROVED.'])
        if r['source_code']=='E46':lines.append('- New AI-generated local patch is disclosed and bundled with its hash. It is not recovered historical artwork. Finite-mask composite adds only cold/unlit stacked fuel; no fire/smoke/figures. Architecture, three stones, pot and herb bundles outside the patch are unchanged.')
        if r['source_code']=='E50':lines.append('- Final native-ash clone donor offset is **[100,0]**. Only ambiguous far terminal prints changed; foreground trail remains and stops before mound. The initial ridge-transfer attempt was not selected. No snow/material reclassification or wall repaint.')
        if not selected:lines.append('- Whole-frame allowed mask makes outside-mask equality vacuous; it proves no unmasked edits because no outside exists. Algorithm uses no coordinate warp/resample, but the output still retained directional highlights/shadows and failed visual silver-overcast acceptance. V002 remains CORRECTION AUTHORISED.')
        lines.extend(['','Exact parameters and adjudicated metrics: `correction_evidence/CORRECTION_ATTEMPTS.json`; actual visual rationale: [CD execution results](CD_EXECUTION_RESULTS_AND_SCOPE.md).',''])
    lines.extend(['## Uncompleted lighting work — precise missing capability','',
                  'E53/E54 need a capable native-coordinate non-destructive relighting paint workflow/finishing artist, or editable lighting/material layers such as separable albedo, illumination, depth/normal inputs. Supplied flat JPEGs and the tried deterministic grade did not achieve the required diffuse silver-overcast read. A whole-frame generative rerender is not authorised. Preserve camera/geometry/house/canoe/tool/rack counts, unfinished hull/chips; no fire, smoke or people. Objective closure is an actually generated exact-source derivative that passes those controls and CD visual inspection. No completion/replacement is claimed.','',
                  '## Preserved successor chains','',
                  'Twenty links below are version lineage to an already existing original, **not an approval**. Four links select an actually accepted bounded derivative. Some existing successors are external/correction/rejected/reference files; following a link cannot release them.','',
                  table(['Original code / ID','Successor code / ID','Relationship','Successor verdict'],[(filelink(r['source_id'],r['source_code']),filelink(r['successor_id'],r['successor_code']),r['relationship'],r['successor_verdict']) for r in lineage]),'',
                  '## Reproducibility and limits','',record['reproducibility_note'],'',
                  'Pillow 13 / NumPy 2.4.6 were used. To reproduce generation, obtain the exact six source IDs/hashes into `google_drive/` and use the bundled patch plus script. Reproducing must not overwrite adjudication or originals. Inspection crops are enlarged evidence aids, not newly rendered detail. New RGB tests are independent; unavailable historical masks/pairs are not claimed rerun.'])
    out('D_CORRECTION_AND_REPLACEMENT_RECORD.md','\n'.join(lines))
    return record


def build_e():
    rows=[r for r in A if r['final_verdict']=='REJECTED'];assert len(rows)==11
    csvout('E_REJECTION_REGISTER.csv',rows,['code','name','source_id','rationale','permitted_use','direction','final_path','source_size','source_md5','source_sha256'])
    out('E_REJECTION_REGISTER.md','\n'.join(['# E — Rejection register','',
        '**11 originals rejected for their submitted use, physically retained unchanged.** Rejection is not deletion and does not authorise a new generation, patch, recovery or replacement. No approved replacement exists for these rejected uses. All 11 original-ID payloads open and match baseline hashes at their listed destinations.','',
        table(['Code','Exact rejected original','Reason / use not selected','Retained final path'],[(r['code'],filelink(r['source_id'],r['name']),r['rationale'],'`'+r['final_path']+'`') for r in rows]),'',
        'The dedicated held-cohort package includes only B29 and E12 from this register; the other nine rejected originals are excluded from its 36-original cohort. B23 is separate from the already quarantined bad-text EXP object, which was not touched again. No generic photoreal ban, universal stone/material ban, authenticated foreign geography, ritual/cultural diagnosis or invented dimension is used as a rejection rule.']))


def build_b():
    packrows=[]
    for cp in CP:
        key=next(k for k,v in PF.items() if v==cp['destination_id'])
        code=cp['code'].removesuffix('_SELECTED')
        r=BY[code]
        row={**cp,'package_folder':PNAMES[key],'package_relative_path':PNAMES[key]+'/'+cp['name'],'cohort_original_code':code,'original_final_verdict':r['final_verdict'],'object_permission':r['permitted_use'] if cp['kind']=='held_original_copy' else 'Selected replacement derivative: internal concept study only, outside APPROVED; not production/cultural/canon clearance.'}
        packrows.append(row)
    assert len(packrows)==38 and sum(r['kind']=='held_original_copy' for r in packrows)==36
    js('36_PACKAGE_MANIFEST.json',{'scope_originals':36,'intentional_asset_copies':38,'copies':packrows,'excluded_original_count':157,'qualification':'Only the held 36 original payloads and selected D03/E50 derivatives are included as package artwork. Supporting Research and new verdict/proof documents are separately identified evidence, not additional submitted originals.'})
    csvout('36_PACKAGE_MANIFEST.csv',packrows,['code','kind','cohort_original_code','source_id','new_id','name','package_relative_path','destination_id','source_size','source_md5','source_sha256','original_final_verdict','object_permission','complete_copy_verified'])
    stats=collections.Counter(r['final_verdict'] for r in HELD)
    js('B_36_ASSET_RELEASE_PACKAGE.json',{'fixed_held_cohort':[r['code'] for r in HELD],'original_count':36,'verdict_counts':dict(stats),'package_folder_id':F['release36']['id'],'intentional_copies':packrows,'original_final_decisions':HELD,'selected_package_replacement_codes':['D03','E50'],'excluded_other_original_count':157})
    lines=['# B — 36-asset final verdict and release package','',
           f"Dedicated permanent package: {folderlink(F['release36']['id'],'CD_FINAL_VERDICTS_AND_RELEASE_36')}.",'',
           '**Exactly 36 held originals, plus two selected derivative copies = 38 intentional artwork copies.** All are byte-identical to their identified source object, kept under distinct new IDs, independently downloaded by those IDs, fully opened and hash/parent-verified. The other 157 original payloads are excluded. Original files are filed at their final disposition destinations; package copies preserve provenance, not a second original count.','',
           '**No unrestricted production release is made.** Seventeen unchanged originals can be used immediately only within the stated internal concept scopes. Two superseded originals have actually selected limited-study replacements. Eight are references/preserved-unapproved; seven require external authority; two are rejected. The six existing visual passes are outside this held cohort.','',NO_PROD,'',
           '## Physical sections','',table(['Section','Originals','Selected derivative copies','Permitted action'],[(folderlink(PF['release'],PNAMES['release']),17,0,'Use now only as individually defined internal studies'),(folderlink(PF['reference'],PNAMES['reference']),8,0,'Reference / preserved UNAPPROVED only'),(folderlink(PF['external'],PNAMES['external']),7,0,'Evidence storage only; exact authority tests below'),(folderlink(PF['rejected'],PNAMES['rejected']),2,0,'Retained rejected evidence only'),(folderlink(PF['replacements'],PNAMES['replacements']),2,2,'Old originals as evidence; selected D03/E50 outputs as limited studies')]),'',
           '## Read this package','',
           '- `36_PACKAGE_MANIFEST.csv/json`: all 38 exact source→copy joins, package paths, hashes and verified copy state.\n- `verdicts/<code>.md`: one individual final verdict for each of the 36; this report also supplies every decision below.\n- `36_REFERENCE_AND_EVIDENCE_INDEX.md`: canonical Research, relevant governing sources and read-boundary qualifications.\n- `36_RELEVANT_ISSUE_CLOSURE.md`: exact relevant issue decisions, not an instruction-only correction cycle.\n- The portable ZIP includes the 36 unchanged original payloads, the two selected replacement payloads, 36 canonical Research files, historical assessment snapshots, instructions and bounded completion proof. Supporting documents are evidence, not extra originals.','']
    for r in HELD:
        cp=r['package_copy'];cr=r.get('correction_result')
        lines.extend([f"## {r['code']} — {r['final_verdict']}",'',
                      f"**Original:** {filelink(r['source_id'],r['name'])}.",f"**Intentional package copy:** {filelink(cp['new_id'],cp['new_id'])} · parent `{cp['destination_id']}`.",'',
                      f"**Allowed use:** {r['permitted_use']}",'',f"**Decision / rationale:** {r['rationale']}",'',f"**Precise direction:** {r['direction']}",'',
                      f"**Actual completion:** Final disposition filed, exact-original destination payload/open/listing checks passed; package NEW-ID copy independently downloaded, hash/open/parent verified. {'No raster change was made to this original; scope selection is not a completed paint correction.' if not cr else 'A separate bounded derivative was actually made; the original remains unchanged.'}",''])
        if cr:
            selectedcp=next(x for x in CP if x['kind']=='selected_derivative_copy' and x['code']==r['code']+'_SELECTED')
            lines.extend([f"**Established replacement:** {filelink(cr['new_drive_id'],cr['output_name'])}; package replacement copy {filelink(selectedcp['new_id'],selectedcp['new_id'])}.",f"- State: {cr['completion_state']}; output SHA256 `{cr['output_sha256']}`.",f"- Source artwork / output dimensions: {'×'.join(map(str,cr['dimensions']))}; difference bbox `{cr['difference_bbox']}`; total changed pixels {cr['changed_pixels']:,}; out-of-mask changes 0.",f"- {'Only 472 art pixels change; other whole-board differences are disclosed documentary chrome.' if r['code']=='D03' else 'Native-ash donor [100,0]; only far terminal footprint area changes, foreground trail preserved and ends before mound.'}",'- Output and its distinct package copy both independently downloaded/opened/hash-verified. Selected replacement is internal-study-only, not production/cultural/canon approval.',''])
        lines.extend([f"**Required role:** {r['required_role']}",f"**Exact authority/tool question:** {r['authority_question']}",f"**Missing evidence/tool:** {r['missing_input']}",f"**Objective closure test:** {r['objective_closure_test']}",'',
                      f"**Evidence:** canonical Research {filelink(r['research_id'],r['research_id'])}, SHA256 `{r['research_sha256']}`; [individual verdict](verdicts/{r['code']}.md). Fresh semantic reread is claimed only for the fifteen listed in the Research ledger; the other 21 held-cohort reports are fresh hash-verified downloads with historical semantic assessment.",'',
                      f"**Original provenance:** `{r['original_path']}` → `{r['final_path']}`.",f"**Unchanged original/copy payload:** {r['source_size']:,} B · MD5 `{r['source_md5']}` · SHA256 `{r['source_sha256']}`.",''])
    out('B_36_ASSET_RELEASE_PACKAGE.md','\n'.join(lines))
    ext=json.loads((B/'evidence/HISTORICAL_external_evidence_verified.json').read_text())['records']
    extby={r['source_id']:r for r in ext}
    support=[('1k08XH8VjNJAnSoMNU4YvBPtBEUdYD20y','Adanna primary master; fictional source-lock, not cultural authentication'),('1V12Sq2BZdIqjsgkx5GRpzGxc3nS3Gbac','Provisional blade board; REVIEW REQUIRED, NOT executable blade authority'),('1JIoAiQ20goibDA-ujYr95iyihBTLKZWj','Nneka V004 environment design; not realm canon'),('1qi7TsLi5v8pfM4mHYLWvJEaSdPPyl_qW','Establishing V005 current-best/in-review; not approved base'),('1l4zcjiDg-9M7Mff9BHFDJWfAxz_RG-fT','V012 mandatory brief; item 5 expressly waived only for current D08 study'),('1UuP2I9szyZvITuyT5Z8q1NilBZBboQZa','Canonical CH01 scene register; relevant sections read, not all scenes delivered'),('1IT5RVzd7kBsPeo3hdJpTliqj4h6O6C9R','Canonical proposed location register; relevant sections read, not established canon'),('1HkaV90iCq3Kmn3M8rgyNPiJ61m7UISPN','Open Art Decisions; controls remain scoped'),('1W9T-FqYIeAp41KyuZ4xlb3QlN0SnHMK1','Visual style guide; grounded photoreal dark fantasy allowed'),('1zMTwzOX8NBxpg-E72hda-ARIzoiXHa0O','Standing closed-cycle CD verdict, retained as history/limited controls')]
    reflines=['# Held-36 reference and evidence index','',
              'Canonical Research below is preserved verbatim, not rewritten as current verdict authority. All 36 payloads were downloaded/hash-checked in this execution; exactly 15 were freshly semantically reread. Full historical readings and reconciliations are in the preserved prior assessments. Current B/verdicts and C errata control final permissions. No extra 157 original payloads are bundled.','',
              table(['Code','Canonical Research exact ID','SHA256','Current read boundary'],[(r['code'],filelink(r['canonical_research_id'],r['name']),r['sha256'],'Fresh full read + hash check' if r['fresh_semantic_reread_in_this_execution'] else 'Fresh payload/hash check; historical full semantic reading') for r in R36]),'',
              '## Governing and reference sources outside the 193-original cohort','',
              'These are linked sources, not extra submitted originals or production/cultural approvals. The exact canonical location register is used, not its legacy duplicate. Hash checks are in `verification/additional_governing_hash_checks.json` and historical/current evidence ledgers. No new primary scholarship or living-custodian clearance was obtained.','',
              table(['Exact source','Permitted evidentiary role','Recorded SHA256'],[(filelink(ident,extby.get(ident,{}).get('name',ident)),label,extby.get(ident,{}).get('local_sha256','See current governing hash ledger')) for ident,label in support]),'',
              f"Current delegated authority: {filelink('1385LR0rgupAuP8sJwb5hVq_t1J-u60c5','CD_EXECUTION_AUTHORITY.md')}.",
              'The historical supplementary cultural review is trashed and is not a live clearance source. Bad-text EXP quarantine/audit is separate history and was not repeated.']
    out('36_REFERENCE_AND_EVIDENCE_INDEX.md','\n'.join(reflines))
    relevant=[r for r in ISS if set(r['scope_codes'])&{r['code'] for r in HELD}]
    lines=['# Held-36 relevant issue decisions','',
           'This is a linked subset of final C for the held cohort. External gates and failed/unperformed work are not labelled complete. No additional original payloads are supplied by this evidence note.','']
    for r in relevant:
        lines.extend([f"## {r['issue_code']} — {r['title']}",f"**{r['final_state']}**",f"Held-cohort members: {', '.join(sorted(set(r['scope_codes'])&{r['code'] for r in HELD}))}",r['verified_facts'],r['cd_decision_and_rationale'],f"**Directions:** {r['precise_directions']}",f"**Actual:** {r['actual_completion']}",f"**Remaining/test:** {r['remaining_dependency_and_objective_test']}",f"**Not assumed:** {r['assumptions_not_made']}",''])
    out('36_RELEVANT_ISSUE_CLOSURE.md','\n'.join(lines))
    return packrows


def build_f(packrows):
    primary=[]
    for r in A:
        primary.append(identity(r)|{'original_path':r['original_path'],'movement_type':r['movement_type'],'permitted_use':r['permitted_use'],'destination_payload_open_and_listing_verified':True,'package_copy_id':r['package_copy']['new_id'] if r['package_copy'] else None,'successor_code':r['successor_code'],'selected_derivative':r['selected_derivative']})
    deriv=[]
    for r in CORR:
        key='studies' if r['source_code'] in ['D03','D06','E46','E50'] else 'corrections'
        deriv.append({**r,'final_parent_id':F[key]['id'],'final_path':F[key]['path']+'/'+r['output_name'],'selected_replacement':key=='studies'})
    dc={}
    for key in ['visual_release','rejected','superseded','aids','studies','corrections','external','documents']:
        cat='release' if key=='visual_release' else key
        dc[key]={'originals':sum(r['destination_category']==cat for r in A),'additional_derivatives':sum(r['final_parent_id']==F[key]['id'] for r in deriv),'folder_id':F[key]['id'],'path':F[key]['path']}
    assert sum(r['originals'] for r in dc.values())==193 and sum(r['additional_derivatives'] for r in dc.values())==6
    manifest={'scope':'Fixed 193 original IDs; copies, derivatives and newly authored records are separately identified','execution_date_qualification':DATE,'physical_clearance':CLEAR,'verdict_counts':dict(COUNT),'role_counts':dict(collections.Counter(r['role'] for r in A)),'destination_counts':dc,'originals':primary,'new_derivatives':deriv,'intentional_package_copies':packrows,'preserved_containers':json.loads((B/'verification/container_move_ledger.json').read_text()),'final_folder_hierarchy':HIER,'original_total_bytes':sum(r['source_size'] for r in A),'primary_destination_file_payloads':199,'primary_destination_preserved_containers':2,'intentional_package_asset_copy_payloads':38,'total_primary_and_package_asset_file_objects':237,'counting_qualification':'199 primary asset files = 193 originals + 6 derivatives. Separate package has 38 intentional copies = 36 originals + 2 derivatives. Newly authored documentation/archives, evidence-mask/crop files and archive-internal payload entries are not counted as additional originals. Documentary root has A01 + two preserved containers; children hold 19/68 documents. Folder suffix REVIEW_AIDS_27 describes the original 26+1 aid cohort, not the final total 35 which also contains eight creative references.','evidence_method':'Source-ID downloads/returned names and complete folder observations were manually normalized from successful connector responses. They are NOT raw API archives. Independent byte hashes and full raster/UTF8 decode tests were computed locally. No semantic/cultural claim follows solely from opening.','verification_artifacts':['verification/destination_listing_observations.json','verification/destination_payload_checks.json','verification/move_ledger.json','verification/container_move_ledger.json','verification/copy_listing_observations.json','verification/copy_payload_checks.json','correction_evidence/CORRECTION_ATTEMPTS.json','verification/research_fresh_checks.json','verification/research_36_payload_checks.json']}
    assert manifest['original_total_bytes']==70416758
    js('F_FINAL_PACKAGE_MANIFEST.json',manifest)
    csvout('F_FINAL_PACKAGE_MANIFEST.csv',primary,['code','name','source_id','source_drive_version','role','final_verdict','source_size','source_md5','source_sha256','original_path','final_parent_id','final_path','movement_type','destination_payload_open_and_listing_verified','package_copy_id','successor_code','selected_derivative'])
    out('F_FINAL_PACKAGE_MANIFEST.md','\n'.join(['# F — Final package manifest and physical reconciliation','',
        '**PENDING CLEARED — physical disposition only.** All 193 original IDs remain present, open and byte-identical at their final destinations. This certificate is supported by the actual post-filing download checks and complete destination/empty-PENDING scans, not by directions or a proposed script.','',
        '## Fixed denominator and additional objects','',table(['Class','Count'],[(k,v) for k,v in manifest['role_counts'].items()]+[('Originals — total',193),('Additional generated derivatives, selected / failed', '6 = 4 / 2'),('Intentional held-original package copies',36),('Intentional selected-derivative package copies',2)]),'',
        '## Final primary destinations','',table(['Destination','Originals','Additional derivatives','Preserved containers'],[(folderlink(v['folder_id'],v['path']),v['originals'],v['additional_derivatives'],2 if k=='documents' else 0) for k,v in dc.items()]),'',
        'Documentary root: A01 + two containers, with 19 and 68 documentary children = 88 originals. The two containers were moved intact, not deleted. Primary listed destinations therefore contain **199 file payloads + 2 preserved containers**. The separate held package contains **38 intentional asset copies**. Documentation files, crops/masks and archives are additional records, not new original counts.','',
        '## Executed movement reconciliation','',
        '- Initial PENDING: **193 files + 2 submission containers**, no deeper original subfolders.\n- Direct original file-parent changes: **106**.\n- Documentary originals relocated inside two preserved containers: **87**.\n- Original locations changed: **193/193**; remaining PENDING originals: **0**.\n- Current complete PENDING root scan: **0 files / 0 folders**, no next page, incomplete-search false. Because its only two original descendant containers are relocated and completely re-enumerated, no old descendant remains below it.\n- Every original source ID downloaded again after filing: **193/193**.\n- Size + MD5 + SHA256 matches: **193/193**; total **70,416,758 bytes**.\n- Opening: **105 full raster decodes + 88 strict full UTF-8 decodes**; failures **0**.\n- Parent/destination membership joins: **193/193**.\n- Original loss / payload overwrite / filename rename / destination-name collision observed: **0**.\n- Ten external-authority originals and two correction originals are outside APPROVED in named permanent storage.\n- Six derivative new-ID payload checks and 38 separate copy-ID payload checks: all passed; four derivatives selected, two grades failed visual acceptance.','',
        '## Identity and version controls','',
        'A CSV/JSON and F CSV/JSON give every exact original ID, baseline Drive revision, unchanged filename/hashes, initial path, final path/parent, verdict, copy ID and successor relationship. Drive revisions may advance for metadata-only moves; artwork generation labels and historical versions were not renamed or overwritten. Copy IDs are intentional and do not replace original identities. A successor in a version chain is not automatically approved.','',
        'The immutable `verification/DESTINATION_FOLDERS.json` and source scope retain initial paths as provenance. `verification/FINAL_FOLDER_HIERARCHY.json` and final row paths contain the corrected post-move container paths. The aid-folder `_27` suffix is historical cohort naming; its final 35 originals include the 27 original aid objects plus eight creative references.','',
        '## Evidence method and limits','',manifest['evidence_method'],'',
        'No raw connector-response archive is claimed. Separate observed ledgers are joined against immutable source IDs, then independently computed payload hashes/open tests. Historical source/Research text, unavailable old masks and claims about past actors remain attributed. Fifteen canonical targeted Research reports were freshly reread; all 36 held-cohort Research payloads were freshly hash-checked. Technical opening is not a new semantic read, cultural clearance, material authentication or visual reapproval.','',
        '## Machine-readable inventory','',
        '- [A register JSON](A_MASTER_FINAL_VERDICT_REGISTER.json): all 193 final decisions, independent execution joins and per-code evidence.\n- [F manifest CSV](F_FINAL_PACKAGE_MANIFEST.csv) / [JSON](F_FINAL_PACKAGE_MANIFEST.json): all 193 original paths/identities plus six derivatives, 38 intentional copy relationships and final hierarchy.\n- [Held-36 CSV](36_PACKAGE_MANIFEST.csv) / [JSON](36_PACKAGE_MANIFEST.json): precise 38 copy objects and permissions.\n- `verification/PHYSICAL_CLEARANCE.json`: physical empty/destination reconciliation certificate.\n- `PACKAGE_FILE_MANIFEST.json` / `SHA256SUMS.txt`: sealed records-archive member fingerprints (explicit self/receipt/archive exclusions).\n- `PUBLICATION_RECEIPT.json/md`: external publication IDs and independent downloaded-file verification; generated after upload so it is deliberately outside the sealed bundle to avoid a self-referential hash.']))
    return manifest


def build_g():
    named=[('A','A_MASTER_FINAL_VERDICT_REGISTER.md','193 final verdicts; CSV/JSON and 193 individual verdict files'),('B','B_36_ASSET_RELEASE_PACKAGE.md','Held-36 release package; copies, permissions, evidence and two selected replacements'),('C','C_ISSUE_CLOSURE_REPORT.md','G01–G16 and documentary D01–D04 decisions, completion versus dependencies'),('D','D_CORRECTION_AND_REPLACEMENT_RECORD.md','Six executed final attempts; four selected, two failed; preserved successor chains'),('E','E_REJECTION_REGISTER.md','Eleven submitted uses rejected, originals retained'),('F','F_FINAL_PACKAGE_MANIFEST.md','193 identity/path/hash reconciliation plus derivatives/copies and clearance'),('G','G_EXECUTIVE_FINAL_REPORT.md','This executive final report')]
    lines=['# G — Executive final report','',f'Execution record: {DATE}.','',
        '## Final outcome','',
        '**PENDING CLEARED.** The final delegated disposition operation is executed, not merely proposed: all **193 originals** have one final role-appropriate verdict and a verified permanent destination; PENDING contains **zero files and zero folders**. No original was renamed, deleted or byte-overwritten. Physical clearance is not universal creative, cultural or production approval.','',
        'The fixed denominator remains **76 creative rasters + 26 comparisons + 1 diagnostic + 2 blocked guides + 88 documentary/support = 193 originals**. Historical Round 6 remains its own closed **6 / 21 / 12** review and is not re-counted as this operation.','',
        '## Final verdict totals','',table(['Final verdict','Originals'],[(k,COUNT[k]) for k in ['APPROVED / RELEASE','APPROVED WITH DEFINED CONDITIONS','CORRECTION AUTHORISED','REPLACED / SUPERSEDED','REJECTED','RETAIN AS DOCUMENTARY EVIDENCE','RETAIN AS REFERENCE / REVIEW AID','EXTERNAL AUTHORITY REQUIRED']]),'',
        'The **six existing visual passes** E15/E19/E20/E21/E47/E49 are retained at visual-review tier only, in a clearly labelled APPROVED subfolder. **Seventeen conditional originals and four selected new derivatives are internal concept studies outside APPROVED**, never production/canon/cultural releases. The 24 superseded originals include 20 historical version-lineage links and four links to actually selected bounded derivatives; successor existence is not approval.','',
        '## Held-36 release package','',
        f"{folderlink(F['release36']['id'],'Open CD_FINAL_VERDICTS_AND_RELEASE_36')}: **36 held originals + 2 selected derivative copies = 38 intentional copies**, each independently verified by its NEW ID. The other 157 original payloads are excluded.",
        '- **17** originals: usable now only for the defined internal studies.\n- **8**: references or preserved-unapproved views.\n- **7**: external-authority evidence only.\n- **2**: rejected.\n- **2**: superseded sources, accompanied by the actual selected D03 FRONT V005 and E50 Passages V003 replacement copies.\n- Individual verdicts, all 36 canonical Research reports, relevant references, instructions and actual completion proof are supplied in the portable package and B documentation.','',
        '## What was corrected, and what was not','',
        '**Actually selected:** D03 FRONT V005 and D06 THREE_QUARTER V005 cord work; E46 Kitchen V003 local cold-firewood composite; E50 Passages V003 native-ash terminal-footprint correction. Exact originals survive, dimensions/masks/changed pixels/hashes are disclosed, and all four outputs were inspected, published and independently verified. Only D03/E50 belong to the held-36 replacement subset.','',
        '**Actually attempted but FAILED:** E53 Canoe Shed V003 and E54 Landing V003 cooler grades. Directional-light cues remain; neither is a replacement. Their V002 originals are CORRECTION AUTHORISED. Closure needs capable native-coordinate non-destructive relighting/finishing or editable lighting/material passes, not another deterministic grade or an unauthorised whole-frame generative rerender. Preserve all geometry/counts and the cold/unlit rack; no fire/smoke/people.','',
        '**Decisions, not painted corrections:** V013 item 5 was expressly waived in BOTH components solely for unchanged internal exploratory composition and remains NOT DONE. E48 clay-toy concept reading and E51 actual 1376×768 canvas are limited CD adjudications, not material proof or completed raster edits. Adanna BACK/LEFT_SIDE remain V003 / PRESERVE / UNAPPROVED; no automatic V004. B43 sheath aesthetic selection does not establish blade/fit/rigging authority.','',
        '## Indispensable reserved authority — not hidden HOLD','',
        '**Ten original cases** are permanently stored outside APPROVED: B01/D07 H3 cloth/cargo/metaphor (D9/RQ-01); E03 textile/material; E07 forging process; E10 water-use/staging; E18 pottery/firing process; E51 fishing gear/cold hearth; E52 paddle craft; E44/E45 blade-authority guides. A/C provide the exact competent role, source-ID question, missing evidence and objective closure test for every case. No consultant/custodian clearance is invented, and no historical trashed review is treated as live authority.','',
        'H3 cargo is unidentified, not proven bodies. Blade-design authority precedes hand-scale/fit; withdrawn percentages/coordinates are unusable. Habitat/setting studies do not complete unshown scene activity, and no figures/animals were generated from scene-register suggestions. SCN028 loom and SCN030 replacement controls, Washing domestic-only U27, Costume interim partial upper-body, VR-008 V009 exploratory-only and CH03-INT-003 exploratory-only remain unchanged.','',
        '## Physical verification','',
        '- Initial PENDING **193 files + 2 containers** → **0 files / 0 folders**, complete scan, no pagination/incomplete search.\n- **106** direct original file moves + **87** originals relocated in two preserved containers = **193**.\n- **193** post-filing original-ID payload checks: unchanged size, MD5 and SHA256; **70,416,758 bytes** preserved.\n- **105** raster decodes + **88** strict UTF-8 decodes; **0** failures.\n- **193** final destination joins; **0** missing originals, overwrites, renames or observed within-folder name collisions.\n- **6** separate derivative downloads and **38** copy-ID downloads/open/hash checks passed.\n- Primary destinations contain **193 originals + 6 derivatives = 199 files**, plus two preserved documentary containers; package copies are separate.','',
        '## Delivered A–G','',table(['Item','Record','Contents'],[(code,f'[{Path(name).stem}]({name})',desc) for code,name,desc in named]),'',
        f"Final records: {folderlink(F['final_records']['id'],'OUR_EYES_CD_FINAL_VERDICTS_v1')}. Source/path/hash maps, 193 individual verdicts, documentary errata, masks/parameters/first attempts, canonical held-cohort Research, manifests and verification ledgers accompany the records archive. `PUBLICATION_RECEIPT.md/json` records returned publication IDs and independent download verification outside the sealed archive.",'',
        '## Evidence boundary','',
        'Current destination/copy observations are manually normalized successful connector results, not a raw API archive. Current hashes and full decode tests are independently computed. Fifteen targeted canonical Research reports were freshly semantically read; 36 held-cohort Research payloads were freshly hash-checked. Historical complete assessments remain labelled historical. No claim of 193 fresh Research rereads, new primary scholarship, actual material authentication or cultural/production clearance is made. Protected tracked history was not edited. No agent/consultant notification or acknowledgement is claimed.','',
        '**This concludes disposition, filing and the feasible bounded execution.** The named external gates and failed relighting corrections remain substantive dependencies, not unfiled originals, disguised approvals or a proposed repeat assessment cycle.']
    out('G_EXECUTIVE_FINAL_REPORT.md','\n'.join(lines))
    out('PENDING_CLEARED_CERTIFICATE.md','\n'.join(['# Physical clearance certificate — PENDING CLEARED','',f'Execution record: {DATE}.','',
        '**Certified scope: physical disposition of all 193 exact original IDs, not universal creative release.**','',
        '- Initial PENDING: 193 files and two submission containers.\n- Executed: 106 direct file-parent changes; two preserved container moves carrying 87 documentary originals.\n- Independently downloaded after filing: 193 exact original IDs; all size/MD5/SHA256 comparisons passed.\n- Original bytes retained: 70,416,758.\n- Full opening: 105 rasters and 88 UTF-8 texts passed.\n- Complete destination listings reconciled with all 193 IDs and expected final parents; two container child scans complete.\n- Complete PENDING rescan: zero files, zero folders; no next page; incomplete-search false.\n- Missing/lost/renamed/byte-overwritten originals or observed within-folder filename collisions: zero.\n- Separate derivatives: six, of which four selected and two failed (not replacements).\n- Separately verified intentional held-package copies: 36 original copies plus two selected derivative copies.\n- Ten authority-dependent originals and two correction originals are in named permanent storage outside APPROVED.','',
        'Evidence: `verification/PHYSICAL_CLEARANCE.json`, all 193 `destination_payload_checks.json` entries, complete `destination_listing_observations.json`, move/container ledgers, copy payload/listing checks and F manifest. Connector observations are manually transcribed/normalized, not archived raw responses; payload hashes and opening tests were independently computed.','',NO_PROD]))
    out('README.md','\n'.join(['# Our Eyes — final delegated CD disposition records','',
        '**Start with [G — Executive final report](G_EXECUTIVE_FINAL_REPORT.md).** Physical PENDING clearance is verified, with substantive authority/correction dependencies explicit.','',
        table(['Record','Purpose'],[(f'[{code}]({name})',desc) for code,name,desc in named]),'',
        '## Bundle boundaries','',
        '- This records archive contains A–G, 193 individual final verdicts, six disclosed derivative outputs, correction proof/first attempts, verification ledgers and preserved historical assessment evidence. It does NOT duplicate all 193 original artwork/support payloads; those remain at their verified Drive destinations with immutable ID/hash joins.\n- The dedicated held-36 portable ZIP separately includes exactly 36 original payloads and two selected derivative payloads, plus their verdicts/Research/proof. Other 157 original payloads are excluded.\n- `evidence/HISTORICAL_*` files are preserved prior assessment material, NOT current authority and not a claim that earlier work executed this operation. Their old HOLD/proposed/no-execution wording is historical. Current A–G and delegated authority control this operation.\n- `verification/SOURCE_SCOPE_193.json` and `DESTINATION_FOLDERS.json` retain immutable initial paths and historical assessment flags. Current execution is in A/F and the destination/copy ledgers; `FINAL_FOLDER_HIERARCHY.json` supplies post-move container paths.\n- Source artwork-generation version, Drive metadata revision, dependency code and package-copy identity are different concepts. Metadata moves may increment Drive revision but do not rename artwork generations or delete history.\n- Within C, D01–D04 name documentary errata; asset codes D01–D08 are separate.\n- No credential, notification, permission change, original deletion/overwrite, incident recovery or repeat EXP quarantine was performed.','',
        '## Rebuild / audit','',
        'Use Python 3 with Pillow 13 and NumPy 2.4.6. Current records builders need only this records tree: `build_issue_decisions.py`, `build_final_register.py`, `build_final_reports.py`. Generation requires exact original source-ID payloads locally, and must never be run to overwrite adjudication: the generator writes separate `CORRECTION_GENERATION.json`, not `CORRECTION_ATTEMPTS.json`. The bundled E46 generated patch is the recorded non-deterministic input; later compositing is deterministic. Portable/ledger-protection code edits were compiled but not rerun over adjudicated outputs.','',
        '`validate_release.py` checks identity joins, counts, actual pixel masks/differences and archive integrity. Original/copy payload rechecks use ignored local download snapshots when available; a later environment must download the exact known IDs/hashes, not invent replacements. Byte opening is not semantic or cultural approval.','',
        '`PACKAGE_FILE_MANIFEST.json` and `SHA256SUMS.txt` seal records-archive members. The publication receipt is deliberately generated after uploads and kept outside the sealed archive, avoiding self-referential hashes. Documentation archives and their internal copies are not extra original counts.']))


def build_packet_metadata():
    P=B/'CD_FINAL_VERDICTS_AND_RELEASE_36';P.mkdir(exist_ok=True)
    for name in ['B_36_ASSET_RELEASE_PACKAGE.md','36_PACKAGE_MANIFEST.json','36_PACKAGE_MANIFEST.csv','36_REFERENCE_AND_EVIDENCE_INDEX.md','36_RELEVANT_ISSUE_CLOSURE.md']:
        shutil.copy2(B/name,P/name)
    for r in HELD:
        for dest,src in [('verdicts',B/'verdicts'/f"{r['code']}.md"),('evidence/HISTORICAL_SOURCE_ASSESSMENTS',B/'evidence/HISTORICAL_SOURCE_ASSESSMENTS'/f"{r['code']}.md"),('evidence/CANONICAL_RESEARCH_HELD_36',B/'evidence/CANONICAL_RESEARCH_HELD_36'/SCOPE[r['code']]['report_name'])]:
            d=P/dest;d.mkdir(parents=True,exist_ok=True);shutil.copy2(src,d/src.name)
    cr=[r for r in CORR if r['source_code'] in ['D03','E50']]
    d=P/'correction_evidence';d.mkdir(exist_ok=True)
    (d/'CORRECTION_ATTEMPTS.json').write_text(json.dumps(cr,indent=2)+'\n')
    for r in cr:
        for key in ['allowed_mask_path','actual_difference_path']:shutil.copy2(ROOT/r[key],d/Path(r[key]).name)
    for name in ['D03_corrected_cord_inspection.png','E50_corrected_endpoint_inspection.png']:shutil.copy2(B/'correction_evidence'/name,d/name)
    checks={name:json.loads((B/'verification'/name).read_text()) for name in ['copy_payload_checks.json','copy_listing_observations.json','research_36_payload_checks.json']}
    v=P/'verification';v.mkdir(exist_ok=True)
    for name,a in checks.items():(v/name).write_text(json.dumps(a,indent=2)+'\n')
    selected=[r for r in CORR if r['source_code'] in ['D03','E50']]
    (P/'D_CORRECTION_AND_REPLACEMENT_RECORD.md').write_text('# Held-36 subset of D — actual selected replacements\n\nOnly D03 FRONT V005 and E50 Passages V003 are selected replacements for this held cohort. D06/E46 and failed E53/E54 outputs are outside it; no other original payloads are included.\n\n'+table(['Source','Actual output','SHA256','Completion'],[(r['source_code'],filelink(r['new_drive_id'],r['output_name']),r['output_sha256'],r['completion_state']) for r in selected])+'\n\nExact metrics/masks and source IDs are in correction_evidence/CORRECTION_ATTEMPTS.json. Both selected output IDs AND both distinct package-copy IDs were independently downloaded/opened/hash-verified. Originals remain unchanged; permissions are internal-study-only. The full D report is in the parent final-records package.\n')
    (P/'README.md').write_text('# CD_FINAL_VERDICTS_AND_RELEASE_36\n\nStart with B_36_ASSET_RELEASE_PACKAGE.md. This portable package contains exactly 36 held original payloads and the two selected D03/E50 derivative payloads, mirroring five physical package sections. The 38 artwork payloads preserve original basenames; 36_PACKAGE_MANIFEST.csv/json maps source IDs, distinct copy IDs, hashes, paths and permissions. Other 157 original payloads are excluded.\n\n17 originals are limited internal studies, 8 references/preserved-unapproved, 7 external-authority evidence, 2 rejected and 2 superseded. The 2 selected replacement copies are additional objects, not extra originals. No unrestricted production, cultural or canon release.\n\n36 individual verdicts, 36 exact canonical Research reports, 36 labelled historical assessments, relevant issue directions/closure and two replacement mask/inspection proofs accompany the artwork. Canonical Research and historical assessments may contain superseded HOLD/availability wording; current verdicts and B control. Fifteen Research reports were freshly read, the remaining 21 freshly downloaded/hash-checked with historical semantic assessment. New evidence crops/masks are documentary proof files, not additional original candidates.\n\nPACKAGE_FILE_MANIFEST.json / SHA256SUMS.txt enumerate and seal every portable member except the two manifest files themselves. Original/copy identity is not changed by archive-internal copies.\n')
    return P

if __name__=='__main__':
    build_c();build_d();build_e();pr=build_b();build_f(pr);build_g();p=build_packet_metadata()
    print('A–G complete; held-36 metadata staged at',p)
