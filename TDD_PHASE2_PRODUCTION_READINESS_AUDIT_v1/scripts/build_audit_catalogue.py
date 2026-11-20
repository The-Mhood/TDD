#!/usr/bin/env python3
"""Additive audit catalogue; no approval inference and no source mutation.
Inventory/measurement/deduplication are explicitly separate from human inspection.
"""
from pathlib import Path
import json,hashlib,csv,subprocess,mimetypes,collections
from PIL import Image
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification';O=B/'inventory';O.mkdir(exist_ok=True)
def load(n):return json.loads((V/n).read_text())
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def hashes(p):
 d=p.read_bytes();return len(d),hashlib.md5(d).hexdigest(),hashlib.sha256(d).hexdigest()
def csvwrite(name,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (O/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  for r in rows:
   x={}
   for k in keys:
    val=r.get(k,'')
    if isinstance(val,(dict,list)):val=json.dumps(val,ensure_ascii=False,separators=(',',':'))
    if isinstance(val,str) and val.startswith(('=','+','-','@')):val="'"+val
    x[k]=val
   w.writerow(x)
N=load('remote_nodes.json');bindings=load('PAYLOAD_BINDINGS.json');BM={x['source_id']:x for x in bindings};arc=load('ARCHIVE_MEMBERS.json');ins=load('CONTENT_INSPECTION_LEDGER.json');amendments=load('CONTENT_INSPECTION_AMENDMENTS.json');PH={x['source_id']:x for x in load('PHASE1_STATUS_CROSSWALK.json')}
byhash=collections.defaultdict(list)
for j,x in enumerate(ins,1):byhash[x['sha256']].append((j,x))
# Use an available identical payload if a historical selected snapshot was omitted
# by sandbox persistence. Never overwrite the historical receipt or its identity.
available={}
for x in bindings+arc+ins:
 p=R/x.get('snapshot','')
 if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==x.get('sha256'):available[x['sha256']]=p
for x in load('NATIVE_EXPORT_ADDITIONAL_SNAPSHOTS.json'):
 p=R/x['snapshot']
 if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']:available[x['sha256']]=p
# Keep previously measured exact-payload dimensions when ignored byte snapshots
# disappear between loads. A historical decode receipt is not a fresh decode or
# content inspection; never infer a dimension from a filename or board text.
historical_measurements={}
for x in load('DOWNLOAD_HASH_CHECKS.json')+arc:
 if x.get('width') and x.get('height') and x.get('sha256'):
  h=x['sha256'];w,hh=x['width'],x['height']
  prior=historical_measurements.get(h)
  if prior:assert (prior['width_px'],prior['height_px'])==(w,hh)
  historical_measurements[h]={'width_px':w,'height_px':hh,'aspect_ratio':round(w/hh,9),'raster_format':x.get('format'),'raster_mode':x.get('mode'),'full_decode_pass':True,'icc_profile_present':x.get('icc_profile_present'),'measurement_basis':'Historical exact-SHA256 raw-download/archive full-decode receipt; not a fresh decode in this build','measurement_snapshot_available_now':h in available}
mcache={}
def measure(h):
 if not h:return {}
 if h in mcache:return mcache[h]
 p=available.get(h);m={}
 if p:
  try:
   with Image.open(p) as im:
    im.load();w,hh=im.size;m={'width_px':w,'height_px':hh,'aspect_ratio':round(w/hh,9),'raster_format':im.format,'raster_mode':im.mode,'full_decode_pass':True,'icc_profile_present':bool(im.info.get('icc_profile')),'measurement_basis':'Fresh full decode of available exact-SHA256 payload in this build; not content inspection','measurement_snapshot_available_now':True}
  except (OSError,ValueError):pass
 if not m:m=dict(historical_measurements.get(h,{}))
 mcache[h]=m;return m
ROOT='1lzJBgHHSO2OJMB0LFmwQoU6R7Kv2iGlZ'
def path_for(ident,visited=()):
 if ident in visited:return '[ancestry cycle:'+ident+']'
 n=N.get(ident,{});name=n.get('name') or ('THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE' if ident==ROOT else '['+ident+']');parents=n.get('parents',[])
 if not parents:return name
 return path_for(parents[0],visited+(ident,))+'/'+name

def inspect_state(h,mime):
 matches=byhash.get(h,[]);kind='visual' if mime.startswith('image/') else 'semantic'
 good=[j for j,x in matches if x['inspection_kind']==kind]
 return ('ACTUALLY_INSPECTED_EXACT_PAYLOAD' if good else ('ARCHIVE_INTEGRITY_ONLY_NOT_CONTENT_COMPLETE' if mime=='application/zip' else 'NOT_YET_CONTENT_INSPECTED')),good
# Native export is a representation, never a stored-native-byte MD5 claim.
exports=load('NATIVE_EXPORT_ADDITIONAL_SNAPSHOTS.json');EX={x['source_id']:x for x in exports}
physical=[]
for ident,n in N.items():
 if n.get('is_folder'):continue
 b=BM.get(ident,{});mime=n.get('mime_type') or 'UNKNOWN';h=b.get('sha256');native=mime.startswith('application/vnd.google-apps.')
 if native and ident in EX:h=EX[ident]['sha256']
 state,refs=inspect_state(h,mime);ph=PH.get(ident,{});p=available.get(h)
 row={'record_key':'drive:'+ident,'source_id':ident,'name':n.get('name','UNKNOWN'),'current_listed_path':path_for(ident),'parents_at_listing':n.get('parents',[]),'drive_version_at_listing':n.get('drive_version'),'mime_at_listing':mime,'listed_stored_bytes':n.get('bytes'),'metadata_md5':n.get('md5'),'verified_representation_sha256':h,'verified_representation_bytes':EX[ident]['export_returned_bytes'] if native and ident in EX else b.get('bytes'),'payload_available_now':bool(p),'available_snapshot':str(p.relative_to(R)) if p else None,'binding_basis':('Explicit new native export receipt; not stored-native bytes' if native and ident in EX else b.get('binding_basis','NOT_YET_HASH_BOUND')),'content_inspection_state':state,'inspection_ledger_rows_1based':refs,'exact_source_phase1_code':ph.get('code'),'exact_source_phase1_disposition':ph.get('final_verdict'),'exact_source_permitted_use':ph.get('permitted_use'),'approval_inherited_from_matching_bytes':False}
 row.update(measure(h));physical.append(row)
archives=[]
for x in arc:
 h=x['sha256'];name=Path(x['member_path']).name;mime=mimetypes.guess_type(name)[0] or 'application/octet-stream'
 if x.get('width'):mime='image/'+('png' if x.get('format')=='PNG' else 'jpeg')
 state,refs=inspect_state(h,mime);p=available.get(h)
 row={'record_key':'archive:'+x['archive_id']+'::'+x['member_path'],'archive_id':x['archive_id'],'archive_name':x['archive_name'],'archive_sha256':x['archive_sha256'],'member_path':x['member_path'],'bytes':x['bytes'],'md5':x['md5'],'sha256':h,'crc_pass':x['crc_pass'],'content_inspection_state':state,'inspection_ledger_rows_1based':refs,'payload_available_now':bool(p),'available_snapshot':str(p.relative_to(R)) if p else None,'approval_inherited_from_archive_or_name':False}
 row.update(measure(h) or {k:x[k] for k in ('width','height','format','mode','aspect_ratio','decode_pass') if k in x});archives.append(row)
# Protected pre-existing repo files and sealed Phase1 outputs are associated
# evidence, not silently omitted because their bytes also occur in a ZIP.
localpaths=[R/x for x in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if x]
localpaths += [p for p in (R/'OUR_EYES_CD_FINAL_VERDICTS_v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.zip')]
local=[]
for p in dict.fromkeys(localpaths):
 size,md5,h=hashes(p);available[h]=p;mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream';state,refs=inspect_state(h,mime)
 row={'record_key':'local:'+str(p.relative_to(R)),'local_path':str(p.relative_to(R)),'bytes':size,'md5':md5,'sha256':h,'mime_hint_not_authority':mime,'content_inspection_state':state,'inspection_ledger_rows_1based':refs,'original_source_unchanged':True,'approval_inherited_from_local_existence':False};row.update(measure(h));local.append(row)
observed=[]
for h,rows in byhash.items():
 for j,x in rows:
  matches=[a for a in amendments if a['sha256']==h and a['source_id']==x['source_id']]
  ob=x['observation'];li=x['limitations']
  for a in matches:ob=a.get('replaces_observation_text',ob);li=a.get('replaces_limitations_text',li)
  observed.append({'inspection_row_1based':j,'source_id_actually_read':x['source_id'],'name':x['name'],'sha256':h,'inspection_kind':x['inspection_kind'],'scope':x['inspection_scope'],'observed_information':ob,'limitations_and_unknowns':li,'controlling_amendments':[a['amendment'] for a in matches],'read_ranges':x.get('read_ranges'),'does_not_change_source_approval':True})
# One provenance group can contain several independent approval statuses.
groups=collections.defaultdict(list)
for row in physical+archives+local:
 h=row.get('verified_representation_sha256',row.get('sha256'))
 if h:groups[h].append(row['record_key'])
exact=[{'sha256':h,'record_count':len(ids),'records':ids,'inspection_rows_1based':[j for j,_ in byhash.get(h,[])],'shared_content_inspection_only_never_shared_approval':True} for h,ids in groups.items() if len(ids)>1]
pending=[{'record_key':x['record_key'],'source_id':x.get('source_id'),'name':x.get('name',Path(x.get('member_path',x.get('local_path',''))).name),'sha256':x.get('verified_representation_sha256',x.get('sha256')),'state':x['content_inspection_state']} for x in physical+archives+local if x['content_inspection_state']!='ACTUALLY_INSPECTED_EXACT_PAYLOAD']
# No technical pass is manufactured from seeing a flat raster.
matrix=[]
for x in physical:
 if not x['mime_at_listing'].startswith('image/'):continue
 seen=x['content_inspection_state']=='ACTUALLY_INSPECTED_EXACT_PAYLOAD'
 matrix.append({'source_id':x['source_id'],'name':x['name'],'sha256':x['verified_representation_sha256'],'measured_width':x.get('width_px'),'measured_height':x.get('height_px'),'measured_aspect':x.get('aspect_ratio'),'visual_evidence':x['content_inspection_state'],'reference_use':x.get('exact_source_permitted_use') or 'Consult exact source authority; filename/folder does not grant approval','modelling':'NOT TECHNICALLY VERIFIED — raster is not a delivered mesh' if seen else 'UNASSESSABLE — visual inspection outstanding','materials':'NO SEPARATED PHYSICAL MAP SET IN THIS RASTER; project package not fully inspected' if seen else 'UNASSESSABLE','rigging':'NO NATIVE RIG IN THIS RASTER; deformation and facial tests not established' if seen else 'UNASSESSABLE','scene_assembly':'SHOT COVERAGE / CONNECTIONS / SCALE NOT TECHNICALLY VALIDATED' if seen else 'UNASSESSABLE','animation':'NO TIMED MOTION / CONTACT / SECONDARY MOTION PROOF IN THIS STILL' if seen else 'UNASSESSABLE','lighting_render':'VISUAL INTENT ONLY; native lighting/render continuity not technically tested' if seen else 'UNASSESSABLE','compositing':'FLATTENED SOURCE; layer/AOV and moving-camera use require shot-specific proof' if seen else 'UNASSESSABLE','film_shot_demand':'NOT ESTABLISHED; historical game register is not a film shot order','inspection_refs':x['inspection_ledger_rows_1based'],'no_source_or_stage_approval_changed':True})
for name,rows in [('A1_PHYSICAL_FILE_CATALOGUE.csv',physical),('A2_ARCHIVE_MEMBER_CATALOGUE.csv',archives),('A3_ASSOCIATED_LOCAL_FILES.csv',local),('A4_ACTUAL_CONTENT_OBSERVATIONS.csv',observed),('A5_EXACT_BYTE_DUPLICATES.csv',exact),('A6_OUTSTANDING_INSPECTION_QUEUE.csv',pending),('C_PER_RASTER_EVIDENCE_MATRIX.csv',matrix)]:csvwrite(name,rows)
folderids=[i for i,x in N.items() if x.get('is_folder')];listings=[json.loads(p.read_text()) for p in (V/'listings').glob('*.json')];complete={x['parent_id'] for x in listings if x.get('complete_final_page') and x.get('incomplete_search') is False};missing_listing=sorted(set(folderids)-complete)
summary={'audit_state':'INCOMPLETE_ALL_FILE_INSPECTION — NOT A FINAL PRODUCTION-READINESS CERTIFICATION','enumerated_nodes':len(N),'enumerated_folders':len(folderids),'saved_normalized_listing_pages':len(listings),'known_folders_without_complete_final_page':missing_listing,'physical_files':len(physical),'physical_hash_bound_source_ids':len(bindings),'physical_current_representation_available':sum(x['payload_available_now'] for x in physical),'physical_sources_with_actual_exact_payload_content_inspection':sum(x['content_inspection_state']=='ACTUALLY_INSPECTED_EXACT_PAYLOAD' for x in physical),'inspection_ledger_observations':len(ins),'visual_observations':sum(x['inspection_kind']=='visual' for x in ins),'semantic_observations':sum(x['inspection_kind']=='semantic' for x in ins),'distinct_actually_inspected_payload_hashes':len(byhash),'archive_member_records':len(archives),'distinct_archive_payload_hashes':len({x['sha256'] for x in arc}),'distinct_archive_raster_payloads':len({x['sha256'] for x in arc if x.get('width')}),'distinct_uninspected_archive_raster_payloads':len({x['sha256'] for x in arc if x.get('width') and not any(z['inspection_kind']=='visual' for _,z in byhash.get(x['sha256'],[]))}),'associated_local_files':len(local),'all_catalogue_records':len(physical)+len(archives)+len(local),'distinct_hash_bound_catalogued_payloads':len(groups),'all_catalogue_uninspected_record_count_not_distinct_assets':len(pending),'exact_duplicate_groups':len(exact),'phase1_scope_sources':len(PH),'phase1_verdicts':dict(collections.Counter(x['final_verdict'] for x in PH.values())),'phase2_remote_writes':0,'all_known_folders_enumerated':not missing_listing,'all_actual_files_inspected':False,'final_distinct_logical_asset_denominator_established':False,'final_film_shot_build_order_established':False,'all_corpus_native_asset_absence_asserted':False,'notes':['Metadata sizes/hashes/listing pagination/ZIP CRC/full decode are not content inspection.','Exact bytes can share recorded inspection only, never authority/status. Differently encoded/visually similar versions have not been silently merged.','All counts are current bookkeeping of this snapshot, not a film asset count or global readiness verdict.','Ignored staging may not survive workspace restoration; historical receipts are retained honestly when snapshots are absent.','Source date strings may differ from session date; no actor/source-drift inference is made.']}
dump(V/'AUDIT_COVERAGE_STATUS.json',summary);dump(O/'CATALOGUE_DATA.json',{'physical':physical,'archives':archives,'local':local,'observations':observed,'duplicates':exact,'matrix':matrix})
print(json.dumps(summary,ensure_ascii=False,indent=2))
