#!/usr/bin/env python3
"""Verify exact-ID independent downloads; write external publication receipt.
Run only after all20 successful upload IDs and their independent downloads have
been observed. Folder ID sets below are manually transcribed complete results,
not computed from a plan and misrepresented as observation. No Drive mutation.
This script is a late verification aid outside the already sealed ZIP.
"""
from pathlib import Path
import json,hashlib,csv,zipfile,io,collections
from PIL import Image
B=Path(__file__).resolve().parents[1];ROOT=B.parent
PLAN=json.loads((B/'PUBLICATION_PLAN.json').read_text())
F=json.loads((B/'verification/DESTINATION_FOLDERS.json').read_text())
OBS=[{'folder_id':'1JxQwdks0hObYrtMyC4yW6Gqg2xkeN_cM','request_id':'65aa19cb-e39a-4527-a61d-09d08ffaa71c','total_count':17,'next_page_token':None,'incomplete_search':False,'observed_ids':'''18XkF3lncnUUFNd2MfthIrd1jSkbhqQ1M 1OCD3dOOn4EbWiScv70cnqUDDTdr8iq82 1x8Et6StNsea_s1Cw0gGgLB8oOGyMXwN9 1YArVvPj-WrotkeASnaxgsDk_5OiUoxSF 1385LR0rgupAuP8sJwb5hVq_t1J-u60c5 1cHkURp_U0vtNqEfLr8txw1oOC4oypF6W 1_ZCBW8wqDh941tkc60wdXFhOnRX3HEmb 1tL33d_oIFfQypFNKBF3LSw7J6Xd8gmbs 1P-5sX_fz2pkJCo0QnmU9T2zHu8iaqbFk 1ju3yK2DwRrMn1GZJH7F3Tr6Y_TT5MeIX 19EiUGwMaDHAN_4zQtm5WZc2T-QjsgUXb 1BfoHox3wsVGbmGF5ezegLXKsiLaTx8_C 1RR1K2zy4RomwTqxzg89MgV0w14F6rzHY 1sMv4iplE6mtIXElYaqu5rpY7oSOA6CXJ 1H-6LmVD6umUYHo74TyQUmfdXsfXYelXh 1DLrjetJMAzrKrtZcMD-lZ8rkhphmgVXY 11ChG1VHDcJkLCHTzyHH7pMyp-87eOUDz'''.split()},
{'folder_id':'1_ZCBW8wqDh941tkc60wdXFhOnRX3HEmb','request_id':'2b47e5dd-9a92-4ec3-bd01-e9dc69568142','total_count':11,'next_page_token':None,'incomplete_search':False,'observed_ids':'''1RBWzDazxAvig6mPQ4Q3t5HYw6c3Lf4c4 1IRAxyBBYsjEcB7DbRk2D3yHjCqAO5Spm 1v308HMpOQKLF__O-oo9V05ZfxBjkCoBY 1Ti7k9bJTmIhe0AORZMtYiLzzTqxd4-Eq 1kXmUlkhvHOlPep9dnJ2VSCiHQg_nkbmM 1DFlL1_qJ0O9jRlxya-c5xBLaDFxTcjyH 1L_E81CJnBvaWyjFaz-MKnqDufg2Dv4iN 1BTJ1JGmHjMwJuTKFAiusITo3ADlEvcR4 1DYrqU3tAZAx3_wdf-JfRIWd0fRsxMfmo 1MNlBW0TpQpEGPvyhy0-6fqy_rFvXxAEx 1Baus84vKG0dO3NTkfLTJbxXy7Wf0QztH'''.split()}]
seen={}
for o in OBS:
    assert len(o['observed_ids'])==o['total_count'] and len(set(o['observed_ids']))==o['total_count']
    o['basis']='Manually transcribed successful complete named/hash/parent listing; no raw response archive. All returned names/parents/MD5/size were manually equal-checked with the upload observations and expected fingerprints.'
    for ident in o['observed_ids']:assert ident not in seen;seen[ident]=o['folder_id']
assert len(PLAN)==20
checks=[]
for r in PLAN:
    assert r['upload_success'] and r['new_drive_id'] in seen and seen[r['new_drive_id']]==r['parent_id']
    p=ROOT/'google_drive'/r['name'];raw=p.read_bytes();assert len(raw)==r['bytes'] and hashlib.md5(raw).hexdigest()==r['md5'] and hashlib.sha256(raw).hexdigest()==r['sha256'],r['name']
    opening={}
    if p.suffix=='.zip':
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            prefix='CD_FINAL_VERDICTS_AND_RELEASE_36' if r['folder_key']=='release36' else 'OUR_EYES_CD_FINAL_VERDICTS_v1'
            mf=json.loads(z.read(prefix+'/PACKAGE_FILE_MANIFEST.json'));counts=collections.Counter();openedimages=openedtext=0
            for m in mf['members']:
                data=z.read(prefix+'/'+m['path']);assert len(data)==m['bytes'] and hashlib.md5(data).hexdigest()==m['md5'] and hashlib.sha256(data).hexdigest()==m['sha256'];counts[m['role']]+=1
                suffix=Path(m['path']).suffix.lower()
                if suffix in ['.png','.jpg','.jpeg']:
                    with Image.open(io.BytesIO(data)) as im:im.load();openedimages+=1
                elif suffix in ['.md','.json','.csv','.txt','.py']:
                    data.decode('utf-8',errors='strict');openedtext+=1
            if r['folder_key']=='release36':assert counts['held_original_copy']==36 and counts['selected_derivative_copy']==2 and len(z.namelist())==165
            else:assert len(z.namelist())==506 and sum(n.startswith(prefix+'/verdicts/') and n.endswith('.md') for n in z.namelist())==193
            opening={'format':'ZIP','crc_all_members_pass':True,'member_hashes_all_pass':True,'member_count':len(z.namelist()),'raster_members_fully_decoded':openedimages,'text_members_strict_utf8_decoded':openedtext,'role_counts':dict(counts)}
    elif p.suffix=='.json':
        a=json.loads(raw.decode('utf-8'))
        if r['name'].startswith('A_'):assert len(a)==193
        elif r['name'].startswith('F_'):assert len(a['originals'])==193 and len(a['new_derivatives'])==6 and len(a['intentional_package_copies'])==38
        else:assert a['scope_originals']==36 and len(a['copies'])==38
        opening={'format':'JSON','full_parse_pass':True}
    elif p.suffix=='.csv':
        rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8'))));expected=193 if r['name'].startswith(('A_','F_')) else 11 if r['name'].startswith('E_') else 38
        assert len(rows)==expected;opening={'format':'CSV','full_parse_pass':True,'data_rows':len(rows)}
    else:raw.decode('utf-8',errors='strict');opening={'format':'UTF8 Markdown','full_decode_pass':True}
    r['independent_download_verified']=True;r['complete_publication_parent_verified']=True;r['download_open_result']=opening;r['download_path']=str(p.relative_to(ROOT));r['verification_basis']='Exact NEW publication ID download observed after upload; independent local size/MD5/SHA256 and full-format checks; separate complete parent enumeration.'
    checks.append(r)
# Existing authority was not duplicated/overwritten. It was freshly downloaded
# once more after final publication and compared to the unchanged local source.
p=ROOT/'google_drive/CD_EXECUTION_AUTHORITY.md';raw=p.read_bytes();local=(B/'CD_EXECUTION_AUTHORITY.md').read_bytes();assert raw==local and len(raw)==13229 and hashlib.md5(raw).hexdigest()=='cc96a885b844e89d679b3fa368e52e45';raw.decode('utf-8')
authority={'name':'CD_EXECUTION_AUTHORITY.md','new_drive_id':'1385LR0rgupAuP8sJwb5hVq_t1J-u60c5','existing_publication_not_reuploaded':True,'parent_id':F['final_records']['id'],'bytes':len(raw),'md5':hashlib.md5(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'independent_download_verified':True,'complete_publication_parent_verified':seen['1385LR0rgupAuP8sJwb5hVq_t1J-u60c5']==F['final_records']['id'],'full_utf8_decode_pass':True}
(B/'PUBLICATION_PLAN.json').write_text(json.dumps(PLAN,indent=2)+'\n')
(B/'verification/PUBLICATION_PARENT_OBSERVATIONS.json').write_text(json.dumps(OBS,indent=2)+'\n')
(B/'verification/PUBLICATION_DOWNLOAD_CHECKS.json').write_text(json.dumps(checks+[authority],indent=2)+'\n')
receipt={'status':'CORE PUBLICATION VERIFIED','new_core_upload_count':20,'new_core_independent_download_verified_count':20,'existing_authority_independent_download_verified':True,'core_payloads_verified_including_existing_authority':21,'new_core_files':checks,'existing_authority':authority,'publication_parent_observations':OBS,'physical_clearance':json.loads((B/'verification/PHYSICAL_CLEARANCE.json').read_text()),'archive_verification':json.loads((B/'verification/ARCHIVE_BUILD_AND_VERIFY.json').read_text()),'self_reference_exclusion':'This receipt and the later live navigation page are generated after the sealed bundles and are deliberately outside those ZIPs. Receipt/index IDs and independent checks are recorded in a later local external ledger; no self-hash or pre-existing receipt upload is falsely claimed.','qualification':'21 core publication payloads independently verified =20 new records/archive uploads +1 existing unchanged authority. This is not extra original scope; all193 original files remain unchanged at their own verified destinations. No permissions, notifications, original overwrite/deletion or repeat EXP operation.'}
(B/'PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
lines=['# Final publication receipt','',
       '**CORE PUBLICATION VERIFIED: 20 newly uploaded core records/archives plus the existing unchanged authority = 21 independent exact-ID re-download, size/MD5/SHA256 and full-format passes.** Separate complete final-records/package-root enumerations confirm all names, parents and no collisions.','',
       '**PENDING CLEARED physically:** all193 exact originals verified, unchanged; complete PENDING rescan zero files/folders. This does not waive the10 substantive external-authority cases or complete the2 failed relighting corrections.','',
       '| Published file | Drive ID | Bytes | SHA256 | Verification |','|---|---|---|---|---|']
for r in checks+[authority]:lines.append(f"| {r['name']} | [{r['new_drive_id']}](https://drive.google.com/file/d/{r['new_drive_id']}/view) | {r['bytes']} | `{r['sha256']}` | PASS — independently downloaded/opened/hash/parent verified |")
lines.extend(['','## Portable bundle integrity','',
              '- Records archive: **506 entries**, all CRC/member hashes passed after independent Drive download;193 individual final verdict files present.\n- Held36 archive: **165 entries**, all CRC/member hashes passed after independent Drive download; exactly36 unchanged original payloads+2 selected derivative payloads, each raster fully decoded. Other157 original payloads excluded.\n- Records ZIP SHA256: `b1c1b3f2de0a9382f188e72746ccc14c24f00fbcc14d8a0cf3ddcc1e2b46afc7`.\n- Held36 ZIP SHA256: `fa9c00e1aac647b10e36e55e968c37b9227f81fe92a6b6d72030a80f65193651`.','',
              '## Receipt scope / self-reference','',receipt['self_reference_exclusion'],'',
              'Observed upload/listing results are manually transcribed/normalized, not raw API archives. Hashes, CSV/JSON/UTF8 parsing and all archive-member/decode tests are computed independently on the downloaded payloads. No new semantic/cultural approval is inferred. Core standalone files are identical to their sealed-bundle counterparts. Current independent downloads did not rewrite those sealed bundles.','',
              'See G for final verdict totals and scope; A/F for every193 original ID, initial→final path, preserved hashes, intentional copy and successor joins; B for the held36; C for exact issue/dependency closure; D for4 selected/2 failed actual attempts; E for11 retained rejections.'])
(B/'PUBLICATION_RECEIPT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'new_core_uploads_verified':20,'existing_authority_verified':True,'core_payloads_verified':21,'zip_members_verified':[506,165],'receipt_written_not_yet_uploaded':True},indent=2))
