#!/usr/bin/env python3
"""Independent local audit of completed filing/copy/pixel proof, no Drive writes.
Requires the exact original/copy download snapshots for a full current audit.
Historical semantic readings and cultural approval are not inferred from this.
"""
from pathlib import Path
import json,hashlib,collections,subprocess,ast
import numpy as np
from PIL import Image
B=Path(__file__).resolve().parents[1]
ROOT=B.parent
load=lambda name:json.loads((B/name).read_text())
A=load('A_MASTER_FINAL_VERDICT_REGISTER.json');BY={r['code']:r for r in A}
S=load('verification/SOURCE_SCOPE_193.json');SB={r['code']:r for r in S}
CP=load('verification/copy_plan.json');CO=load('correction_evidence/CORRECTION_ATTEMPTS.json')
D=load('verification/destination_payload_checks.json');OBS=load('verification/destination_listing_observations.json')
F=load('verification/DESTINATION_FOLDERS.json');H=load('verification/FINAL_FOLDER_HIERARCHY.json')
results=[]
def check(name,truth,details):
    assert truth,(name,details)
    results.append({'check':name,'passed':True,'details':details})
def fp(raw):return len(raw),hashlib.md5(raw).hexdigest(),hashlib.sha256(raw).hexdigest()
check('fixed_original_identity_set',len(A)==193 and len(BY)==193 and {r['source_id'] for r in A}=={r['source_id'] for r in S},'193 unique unchanged source IDs')
expect={'APPROVED / RELEASE':6,'APPROVED WITH DEFINED CONDITIONS':17,'CORRECTION AUTHORISED':2,'REPLACED / SUPERSEDED':24,'REJECTED':11,'RETAIN AS DOCUMENTARY EVIDENCE':88,'RETAIN AS REFERENCE / REVIEW AID':35,'EXTERNAL AUTHORITY REQUIRED':10}
check('final_verdicts',dict(collections.Counter(r['final_verdict'] for r in A))==expect,'Eight final labels, no indefinite HOLD')
check('fixed_roles',dict(collections.Counter(r['role'] for r in A))=={'creative raster':76,'comparison aid':26,'diagnostic aid':1,'blocked retouch guide':2,'support record':88},'76+26+1+2+88=193')
parentseen={}
for obs in OBS:
    check('complete_listing_'+obs['destination_key'],obs['next_page_token'] is None and not obs['incomplete_search'] and len(obs['observed_ids'])==obs['observed_total'],'Observed complete connector enumeration, manually normalized')
    check('no_name_collision_'+obs['destination_key'],len({r['name_joined_to_fixed_identity'] for r in obs['files']})==len(obs['files']),'Within-folder only; intentional cross-folder copies are not collisions')
    for ident in obs['observed_ids']:
        assert ident not in parentseen;parentseen[ident]=obs['folder_id']
check('destination_sets',len(parentseen)==201 and all(parentseen[r['source_id']]==r['final_parent_id'] for r in A),'199 primary files + two preserved containers; every original exact parent joined')
check('payload_ledger',len(D)==193 and all(r['source_size_match'] and r['source_md5_match'] and r['source_sha256_match'] and r['open_check']['open_success'] and r['complete_destination_verified'] for r in D),'193 post-filing exact-original-ID download/hash/open/listing passes')
rasters=texts=total=0
for r in A:
    p=ROOT/'_final_release_stage/verified_originals'/r['code']/r['name']
    raw=p.read_bytes();assert fp(raw)==(r['source_size'],r['source_md5'],r['source_sha256']),r['code'];total+=len(raw)
    if r['role']=='support record':raw.decode('utf-8',errors='strict');texts+=1
    else:
        with Image.open(p) as im:im.load();rasters+=1
    assert r['name']==SB[r['code']]['name'] and r['source_sha256']==SB[r['code']]['source_sha256']
    assert (B/'verdicts'/f"{r['code']}.md").exists()
check('independent_original_snapshot_recheck',(rasters,texts,total)==(105,88,70416758),'All 193 source-ID snapshots rehashed and fully reopened, no new semantic/visual approval inferred')
held={r['code'] for r in A if r['in_held_36']}
check('held_cohort_copy_scope',len(held)==36 and {r['code'] for r in CP if r['kind']=='held_original_copy'}==held and {r['code'] for r in CP if r['kind']=='selected_derivative_copy'}=={'D03_SELECTED','E50_SELECTED'},'Only 36 held originals + selected D03/E50 derivatives; other 157 originals excluded')
check('copy_identity_is_distinct',len(CP)==38 and len({r['new_id'] for r in CP})==38 and not {r['new_id'] for r in CP}&set(parentseen),'All 38 package IDs are distinct from primary originals/derivatives/containers')
for r in CP:
    p=ROOT/'_final_release_stage/verified_package_copies'/r['code']/r['name'];raw=p.read_bytes();assert fp(raw)==(r['source_size'],r['source_md5'],r['source_sha256'])
    with Image.open(p) as im:im.load()
    assert r['complete_copy_verified'] and r['copy_success'] and r['download_verified'] and r['destination_listing_verified'] and r['open_verified']
check('independent_copy_snapshot_recheck',True,'38 exact-copy-ID snapshots rehashed and full raster decoded; all passed')
newtests=[]
for r in CO:
    src=BY[r['source_code']]
    sp=ROOT/'_final_release_stage/verified_originals'/r['source_code']/src['name'];op=ROOT/r['output_path']
    assert fp(op.read_bytes())==(r['output_bytes'],r['output_md5'],r['output_sha256'])
    with Image.open(sp) as im:a=np.array(im.convert('RGB'))
    with Image.open(op) as im:im.load();assert list(im.size)==r['dimensions'];b=np.array(im.convert('RGB'))
    assert a.shape==b.shape
    with Image.open(ROOT/r['allowed_mask_path']) as im:mask=np.asarray(im)>0
    with Image.open(ROOT/r['actual_difference_path']) as im:saved_diff=np.asarray(im)>0
    diff=np.any(a!=b,axis=2);assert np.array_equal(diff,saved_diff)
    yy,xx=np.where(diff);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    assert bbox==r['difference_bbox'] and int(diff.sum())==r['changed_pixels'] and not np.any(diff & ~mask)
    if 'changed_art_pixels' in r:
        art=diff[130:1310,60:1930];assert int(art.sum())==r['changed_art_pixels'];ay,ax=np.where(art);assert [int(ax.min()+60),int(ay.min()+130),int(ax.max()+61),int(ay.max()+131)]==r['art_difference_bbox']
    if r['source_code'] in ['E53','E54']:
        assert np.all(mask) and r['completion_state']=='GENERATED_AND_VISUALLY_REJECTED_NOT_REPLACEMENT'
    else:assert r['completion_state']=='COMPLETED_AND_VISUALLY_ACCEPTED_LIMITED_STUDY'
    assert r['independent_download_verified'] and r['upload_success'] and src['source_sha256']==r['source_sha256']
    newtests.append({'code':r['source_code'],'output_hashes_match':True,'native_dimensions_match':True,'changed_pixels_recomputed':int(diff.sum()),'difference_bbox_recomputed':bbox,'out_of_mask_changes_recomputed':0,'art_changed_pixels_recomputed':r.get('changed_art_pixels'),'whole_frame_mask_vacuity_disclosed':r['source_code'] in ['E53','E54'],'decision_not_inferred_from_pixel_test':True})
check('six_derivative_pixel_recomputations',len(newtests)==6,'Actual byte hashes, full PNG opening, dimensions, saved difference bitmap, bounds/counts and exact finite-mask RGB tests recomputed. Whole-frame tests are explicitly vacuous outside mask.')
patch=B/'correction_evidence/E46_firewood_patch_generated.png';assert hashlib.sha256(patch.read_bytes()).hexdigest()==next(r for r in CO if r['source_code']=='E46')['additional_inputs'][0]['sha256']
check('generated_patch_provenance',True,'Exact E46 non-deterministic generated patch input is bundled and hash-identical')
for r in load('verification/research_36_payload_checks.json'):
    raw=(B/r['bundled_path']).read_bytes();assert fp(raw)==(r['bytes'],r['md5'],r['sha256']);raw.decode('utf-8',errors='strict')
check('research_payloads_and_read_boundary',len(load('verification/research_36_payload_checks.json'))==36 and len(load('verification/research_fresh_checks.json'))==15,'36 exact canonical held-cohort Research payloads checked; only 15 fresh semantic rereads claimed')
issues=load('C_ISSUE_CLOSURE_REPORT.json')
check('all_issue_ids', [r['issue_code'] for r in issues]==[f'G{i:02d}' for i in range(1,17)]+[f'D{i:02d}' for i in range(1,5)],'16 substantive issue decisions + four explicitly distinct documentary errata')
for r in issues:
    for x in r['affected_exact_originals']:assert x['source_id']==BY[x['code']]['source_id'] and x['source_sha256']==BY[x['code']]['source_sha256']
for r in A:
    if r['destination_category']=='release':assert r['final_parent_id']==F['visual_release']['id']
    else:assert r['final_parent_id']!=F['visual_release']['id']
    if r['destination_category'] in ['external','corrections']:assert all(r[k] and not r[k].startswith('None') for k in ['required_role','authority_question','missing_input','objective_closure_test'])
check('approval_segregation_and_finite_dependencies',True,'Only six old visual passes in APPROVED; conditional, external and correction objects outside. All ten authority/two correction cases have exact finite roles/questions/tools/tests.')
mov=load('verification/move_ledger.json');cont=load('verification/container_move_ledger.json')
check('movement_reconciliation',len(mov)==106 and len(cont)==2 and sum(r['verified_descendant_count'] for r in cont)==87 and all(r['complete_child_enumeration_verified'] and r['parent_membership_listing_verified'] for r in cont),'106 direct + 87 contained = 193; intact containers verified')
cl=load('verification/PHYSICAL_CLEARANCE.json')
check('empty_pending_rescan',cl['status']=='PENDING CLEARED' and cl['pending_remaining_files']==cl['pending_remaining_folders']==0 and cl['latest_empty_rescan_observation']['total_count']==0 and cl['latest_empty_rescan_observation']['next_page_token'] is None and not cl['latest_empty_rescan_observation']['incomplete_search'],'Complete latest scan request '+cl['latest_empty_rescan_request_id'])
for p in (B/'scripts').glob('*.py'):ast.parse(p.read_text())
gen=(B/'scripts/build_bounded_corrections.py').read_text();assert "(EVIDENCE/'CORRECTION_GENERATION.json').write_text" in gen and "(EVIDENCE/'CORRECTION_ATTEMPTS.json').write_text" not in gen and "patch_path=EVIDENCE/'E46_firewood_patch_generated.png'" in gen
check('generation_ledger_protected_and_code_parses',True,'Post-execution portability/ledger protection edits parsed, not rerun over adjudicated output')
prev=ROOT/'_final_release_stage/previous_refresh/assessments'
assert len(list((B/'evidence/HISTORICAL_SOURCE_ASSESSMENTS').glob('*.md')))==193
if prev.exists():
    for p in prev.glob('*.md'):assert p.read_bytes()==(B/'evidence/HISTORICAL_SOURCE_ASSESSMENTS'/p.name).read_bytes()
check('historical_assessment_preservation',True,'193 labelled historical assessment files copied unchanged; old wording is not current authority')
proc=subprocess.run(['git','diff','--exit-code','--quiet'],cwd=ROOT)
check('tracked_history_unchanged',proc.returncode==0,'No tracked baseline/history/screenshot/DOCX file edits')
report={'result':'PASS','scope_originals':193,'original_payloads_reopened':193,'original_raster_decodes':105,'original_utf8_decodes':88,'original_total_bytes':total,'copy_payloads_reopened':38,'final_derivative_attempts_recomputed':6,'all_20_issue_decisions_present':True,'checks':results,'derivative_tests':newtests,'qualification':'Local computed verification of actual saved downloads plus normalized observed connector joins; no raw API archive, semantic reread or cultural/production approval inferred. Archive/publication checks are separate post-seal receipts.'}
(B/'verification/FINAL_QA_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','derivative_tests']},indent=2))
