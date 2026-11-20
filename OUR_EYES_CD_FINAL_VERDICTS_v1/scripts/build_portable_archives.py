#!/usr/bin/env python3
"""Seal portable records and held-36 payload archives; never changes Drive.
Manifests exclude themselves/checksum text to avoid self-reference. Late
publication/index/receipt and archive-check records live outside sealed records.
"""
from pathlib import Path
import json,hashlib,zipfile
B=Path(__file__).resolve().parents[1]
ROOT=B.parent
P=B/'CD_FINAL_VERDICTS_AND_RELEASE_36'
CP=json.loads((B/'verification/copy_plan.json').read_text())
PM=json.loads((B/'36_PACKAGE_MANIFEST.json').read_text())['copies']
assert len(CP)==38 and all(r['complete_copy_verified'] for r in CP)
assert json.loads((B/'verification/FINAL_QA_RESULTS.json').read_text())['result']=='PASS'
MANIFESTS={'PACKAGE_FILE_MANIFEST.json','SHA256SUMS.txt'}

def fp(path):
    raw=path.read_bytes();return {'bytes':len(raw),'md5':hashlib.md5(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest()}

def seal(base,members,scope):
    rows=[{'path':name,**fp(path),'role':role} for name,path,role in sorted(members,key=lambda r:r[0])]
    assert len(rows)==len({r['path'] for r in rows})
    (base/'PACKAGE_FILE_MANIFEST.json').write_text(json.dumps({'scope':scope,'members':rows,'excludes':['PACKAGE_FILE_MANIFEST.json','SHA256SUMS.txt'],'qualification':'These two manifest files are included in the ZIP but not self-hashed. External ZIP hash and late publication verification are separate.'},indent=2)+'\n')
    (base/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in rows))
    return members+[(name,base/name,'manifest_without_self_hash') for name in sorted(MANIFESTS)]

def archive(filename,prefix,members):
    path=B/filename
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=False) as z:
        for name,source,role in sorted(members,key=lambda r:r[0]):
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
            z.write(source,prefix+'/'+name)
    assert path.stat().st_size<100*1024*1024
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names=z.namelist();assert len(names)==len(set(names))==len(members)
        mf=json.loads(z.read(prefix+'/PACKAGE_FILE_MANIFEST.json'))
        for r in mf['members']:
            raw=z.read(prefix+'/'+r['path']);assert len(raw)==r['bytes'] and hashlib.md5(raw).hexdigest()==r['md5'] and hashlib.sha256(raw).hexdigest()==r['sha256'],r['path']
        assert set(names)=={prefix+'/'+r['path'] for r in mf['members']}|{prefix+'/'+x for x in MANIFESTS}
    return {'name':filename,'local_path':str(path.relative_to(ROOT)),**fp(path),'zip_members':len(members),'crc_all_pass':True,'member_manifest_payloads_all_hash_verified':True,'prefix':prefix}

# Held cohort ZIP: image payloads come from the exact NEW-copy-ID snapshots,
# never from a same-name unverified source. No other157 original is included.
packet=[]
for p in P.rglob('*'):
    if p.is_file() and p.name not in MANIFESTS and '__pycache__' not in p.parts:
        packet.append((str(p.relative_to(P)),p,'supporting_verdict_research_or_completion_evidence'))
for r in PM:
    source=ROOT/'_final_release_stage/verified_package_copies'/r['code']/r['name']
    h=fp(source);assert h['sha256']==r['source_sha256'] and h['md5']==r['source_md5'] and h['bytes']==r['source_size']
    packet.append((r['package_relative_path'],source,r['kind']))
assert sum(r[2]=='held_original_copy' for r in packet)==36 and sum(r[2]=='selected_derivative_copy' for r in packet)==2
packet=seal(P,packet,'Dedicated held36: exactly36 original payloads +2 selected derivative payloads, plus named supporting documentation/evidence. Other157 original payloads excluded.')
pinfo=archive('CD_FINAL_VERDICTS_AND_RELEASE_36.zip','CD_FINAL_VERDICTS_AND_RELEASE_36',packet)
pinfo['held_original_payloads']=36;pinfo['selected_derivative_payloads']=2;pinfo['other_157_original_payloads']=0

# Records ZIP is distinct: all193 final verdicts, but not all193 raw original
# payloads. The held36 payload archive is deliberately separate and not nested.
records=[]
late_names={'PUBLICATION_PLAN.json','PUBLICATION_RECEIPT.json','PUBLICATION_RECEIPT.md','00_START_HERE_FINAL_RELEASE.md'}
for p in B.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if rel.parts[0]=='CD_FINAL_VERDICTS_AND_RELEASE_36' or '__pycache__' in rel.parts:continue
    if p.suffix=='.zip' or p.name in MANIFESTS or p.name in late_names:continue
    if rel.parts[0]=='verification' and (p.name.startswith(('PUBLICATION_','RECEIPT_')) or p.name=='ARCHIVE_BUILD_AND_VERIFY.json'):continue
    records.append((str(rel),p,'final_record_or_disclosed_derivative_or_evidence'))
records=seal(B,records,'Final A–G records,193 individual verdicts,193 labelled historical assessments,36 canonical held-cohort Research reports,6 disclosed final derivative attempts,first-attempt/proof files and completed verification ledgers. Raw193-original payloads remain at verified Drive destinations; held36 payload ZIP is separate.')
rinfo=archive('OUR_EYES_CD_FINAL_VERDICTS_v1.zip','OUR_EYES_CD_FINAL_VERDICTS_v1',records)
report={'records_archive':rinfo,'held36_archive':pinfo,'all_archive_tests_passed':True,'qualification':'Independent local CRC/member hash/decode QA precedes upload. Connector publication and independent new-ID re-download tests are recorded separately, never inferred from this archive build.'}
(B/'verification/ARCHIVE_BUILD_AND_VERIFY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
