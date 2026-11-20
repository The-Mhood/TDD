#!/usr/bin/env python3
"""Build evidence joins without changing sources or transferring authority.
A physical Drive ID joins local bytes ONLY on observed MD5 + size, or on an
explicit native-Workspace export receipt. Archive membership/name is NOT approval.
No source file, script, instruction or design is executed or changed here.
"""
from pathlib import Path
import hashlib,json,subprocess
from collections import defaultdict
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification'
def read(n):
 p=V/n;return json.loads(p.read_text()) if p.exists() else []
N=read('remote_nodes.json');previous={x['source_id']:x for x in read('PAYLOAD_BINDINGS.json')};candidates=defaultdict(list);seen=set()
def candidate(path,origin,identity):
 p=R/path
 if not p.is_file():return
 key=(str(path),origin,identity)
 if key in seen:return
 seen.add(key);d=p.read_bytes();md5=hashlib.md5(d).hexdigest();sha=hashlib.sha256(d).hexdigest()
 candidates[(len(d),md5)].append({'snapshot':str(path),'sha256':sha,'origin':origin,'origin_identity':identity})
for c in read('DOWNLOAD_HASH_CHECKS.json'):candidate(c['source_snapshot'],'Previously verified connector-download MD5/size join',c['source_id'])
for c in read('ARCHIVE_MEMBERS.json'):candidate(c['snapshot'],'Verified ZIP member; not an independent download of this physical Drive ID',c['archive_id']+'::'+c['member_path'])
for p in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0'):
 if p:candidate(p,'Protected pre-existing tracked repository source copy; not an independent Drive download',p)
# Reuse intact, sealed Phase1 package bytes when the CURRENT observed MD5/size
# match. This is a new evidence join only; it neither rebuilds/reseals Phase1 nor
# imports its historical assessments as Phase2 content inspection or approval.
for p in (R/'OUR_EYES_CD_FINAL_VERDICTS_v1').rglob('*'):
 if p.is_file():candidate(str(p.relative_to(R)),'Pre-existing sealed Phase1 local package bytes; not an independent download of this physical Drive ID',str(p.relative_to(R)))
rows=[]
for ident,n in N.items():
 if n.get('is_folder'):continue
 cs=candidates.get((n.get('bytes'),n.get('md5')),[]) if n.get('md5') else []
 if not cs:continue
 assert len({x['sha256'] for x in cs})==1,('Ambiguous MD5 match: manual investigation required',ident)
 # Prefer an ID's own independently downloaded/staged payload if available.
 cs=sorted(cs,key=lambda x:0 if x['origin_identity']==ident else 1)
 rows.append({'source_id':ident,'name':n['name'],'drive_version_at_listing':n['drive_version'],'parents_at_listing':n.get('parents',[]),'bytes':n['bytes'],'metadata_md5':n['md5'],'sha256':cs[0]['sha256'],'snapshot':cs[0]['snapshot'],'binding_basis':'Current observed Drive size and MD5 equal actual local bytes; SHA256 pins the inspected local payload. This is not a claim every equal-hash physical ID was independently downloaded.','selected_payload_origin':cs[0],'all_equal_hash_payload_origins':cs,'source_approval_is_not_inherited_from_payload_equivalence':True})
for e in read('NATIVE_EXPORT_SNAPSHOTS.json'):
 n=N[e['source_id']];p=R/e['snapshot']
 if not p.is_file():continue
 d=p.read_bytes();assert hashlib.sha256(d).hexdigest()==e['sha256']
 rows.append({'source_id':e['source_id'],'name':n['name'],'drive_version_at_listing':n['drive_version'],'parents_at_listing':n.get('parents',[]),'bytes':len(d),'metadata_md5':None,'sha256':e['sha256'],'snapshot':e['snapshot'],'binding_basis':'Explicit connector native-Workspace export; export bytes are not the stored native document bytes or its listed size. No Drive MD5 assertion.','selected_payload_origin':e,'source_approval_is_not_inherited_from_payload_equivalence':True})
# Keep historical verified joins when ignored snapshots were omitted by workspace
# restoration. Missing bytes MUST NOT become a fresh inspection or be silently
# discarded from the provenance record. inspection_ledger still requires bytes.
current_ids={x['source_id'] for x in rows}
for ident,old in previous.items():
 if ident not in current_ids:
  old=dict(old);old['historical_binding_snapshot_currently_missing']=not (R/old['snapshot']).is_file()
  rows.append(old)
(V/'PAYLOAD_BINDINGS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Physical source-ID/payload bindings',len(rows),'distinct payload SHA256',len({x['sha256'] for x in rows}))
print('Independent raw-download joins remain separately counted in DOWNLOAD_HASH_CHECKS.json; no content review implied by this script.')
