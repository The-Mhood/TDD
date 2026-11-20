#!/usr/bin/env python3
"""Read-only source staging. Hash/CRC/full decode checks are NOT visual review.
Incoming tool downloads are hash-joined to observed Drive metadata, placed under
ID-keyed paths, and ZIP members stored under their SHA256 (no archive path writes).
No downloaded scripts or source instructions are executed by this program.
"""
from pathlib import Path
import json,hashlib,zipfile,io,os
from PIL import Image
B=Path(__file__).resolve().parents[1]; R=B.parent; V=B/'verification'; S=R/'_phase2_stage'
N=json.loads((V/'remote_nodes.json').read_text())
def load(name):
 p=V/name;return json.loads(p.read_text()) if p.exists() else []
def digest(d):return hashlib.md5(d).hexdigest(),hashlib.sha256(d).hexdigest()
def put(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(d).digest(),p
 else:p.write_bytes(d)
def image_fields(d):
 with Image.open(io.BytesIO(d)) as im:
  im.load();return dict(width=im.width,height=im.height,mode=im.mode,format=im.format,icc_profile_present=bool(im.info.get('icc_profile')),decode_pass=True,aspect_ratio=im.width/im.height)
checks={r['source_id']:r for r in load('DOWNLOAD_HASH_CHECKS.json')}; members={(r['archive_id'],r['member_path']):r for r in load('ARCHIVE_MEMBERS.json')}; unmatched=[];fresh=[]
native_exports={r['sha256']:r for r in load('NATIVE_EXPORT_SNAPSHOTS.json')}
for p in sorted((R/'google_drive').iterdir()):
 if not p.is_file():continue
 d=p.read_bytes();md,sha=digest(d); matches=[n for n in N.values() if not n.get('is_folder') and n.get('md5')==md and n.get('bytes')==len(d)]
 if not matches:
  if sha in native_exports:
   e=native_exports[sha];assert len(d)==e['export_returned_bytes'] and (R/e['snapshot']).read_bytes()==d
   continue # Native exports have explicit separate receipts; never assert a Drive MD5 join.
  unmatched.append({'path':str(p.relative_to(R)),'bytes':len(d),'md5':md,'sha256':sha});continue
 for n in matches:
  target=S/'drive'/n['id']/n['name'];put(target,d)
  c=dict(source_id=n['id'],name=n['name'],source_snapshot=str(target.relative_to(R)),bytes=len(d),md5=md,sha256=sha,metadata_hash_match=True,payload_verification_basis='Downloaded payload matches this current listed object by byte count and Drive MD5; equal-hash objects may share one payload. Not a claim of independent download of every physical ID.',inspection_state='See separate content inspection ledger; full decoding is not visual/semantic review')
  if p.suffix.lower() in ('.jpg','.jpeg','.png','.webp','.gif'):c.update(image_fields(d))
  checks[n['id']]={**checks.get(n['id'],{}),**c}
 if p.suffix.lower()=='.zip':
  aid=matches[0]['id'];existing=[r for (i,k),r in members.items() if i==aid]
  if existing and all(Path(R/r['snapshot']).exists() for r in existing):continue
  with zipfile.ZipFile(io.BytesIO(d)) as z:
   infos=z.infolist();assert sum(i.file_size for i in infos)<2_000_000_000,'Archive expansion limit requires explicit review'
   assert z.testzip() is None
   for info in infos:
    if info.is_dir():continue
    b=z.read(info);mm,ss=digest(b);out=S/'archive_payloads'/ss/Path(info.filename).name;put(out,b)
    r=dict(archive_id=aid,archive_name=p.name,archive_sha256=sha,member_path=info.filename,bytes=len(b),md5=mm,sha256=ss,snapshot=str(out.relative_to(R)),crc_pass=True,inspection_state='NOT YET VISUALLY OR SEMANTICALLY INSPECTED')
    if out.suffix.lower() in ('.jpg','.jpeg','.png','.webp','.gif'):r.update(image_fields(b))
    members[(aid,info.filename)]={**members.get((aid,info.filename),{}),**r}
   fresh.append((p.name,len(infos)))
(V/'DOWNLOAD_HASH_CHECKS.json').write_text(json.dumps(list(checks.values()),ensure_ascii=False,indent=2)+'\n')
(V/'ARCHIVE_MEMBERS.json').write_text(json.dumps(list(members.values()),ensure_ascii=False,indent=2)+'\n')
(V/'UNJOINED_INCOMING_DOWNLOADS.json').write_text(json.dumps(unmatched,ensure_ascii=False,indent=2)+'\n')
print('Metadata-hash joined physical IDs:',len(checks),'distinct payloads',len({r['sha256'] for r in checks.values()}))
print('ZIP members:',len(members),'distinct member payloads',len({r['sha256'] for r in members.values()}))
for a,c in fresh:print('CRC/decode inventoried',a,c)
for r in unmatched:print('UNJOINED',r['path'])
