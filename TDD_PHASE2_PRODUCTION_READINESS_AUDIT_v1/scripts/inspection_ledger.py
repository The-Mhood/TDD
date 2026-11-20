#!/usr/bin/env python3
"""Record actual agent visual/text observations separately from hash/decode tests."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1];V=B/'verification'
P=V/'CONTENT_INSPECTION_LEDGER.json'
def add(source_id,kind,scope,observation,limitations='',read_ranges=None):
    rows=json.loads(P.read_text()) if P.exists() else []
    checks=json.loads((V/'DOWNLOAD_HASH_CHECKS.json').read_text())
    matches=[r for r in checks if r['source_id']==source_id]
    if not matches and (V/'PAYLOAD_BINDINGS.json').exists():
        matches=[r for r in json.loads((V/'PAYLOAD_BINDINGS.json').read_text()) if r['source_id']==source_id]
    assert len(matches)==1,('Need exact hash-joined snapshot or explicit native export',source_id)
    c=matches[0];snapshot=c.get('source_snapshot',c.get('snapshot'));d=Path(snapshot).read_bytes();assert hashlib.sha256(d).hexdigest()==c['sha256']
    key=(source_id,kind,scope)
    assert not any((r['source_id'],r['inspection_kind'],r['inspection_scope'])==key for r in rows),('Already recorded',key)
    rows.append({'source_id':source_id,'name':c['name'],'sha256':c['sha256'],'bytes':c['bytes'],'snapshot':snapshot,'inspection_kind':kind,'inspection_scope':scope,'observation':observation,'limitations':limitations,'read_ranges':read_ranges,'inspection_basis':'Actual functions.read_file raster display or complete document text returned by read_file/read_file_text in this Phase2; not inferred from filename, hash or old audit.','does_not_change_source_approval':True})
    P.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')

def add_member(archive_id,member_name,observation,limitations='',kind='visual',read_ranges=None,member_path=None):
    cat=json.loads((V/'ARCHIVE_MEMBERS.json').read_text());rr=[x for x in cat if x['archive_id']==archive_id and (x['member_path']==member_path if member_path else Path(x['member_path']).name==member_name)]
    assert len(rr)==1,(archive_id,member_name,len(rr));c=rr[0]
    payload=Path(c['snapshot']).read_bytes()
    assert len(payload)==c['bytes'] and hashlib.sha256(payload).hexdigest()==c['sha256'],('Member snapshot mismatch',c['member_path'])
    assert kind in ('visual','semantic'),kind
    rows=json.loads(P.read_text()) if P.exists() else []
    assert not any(r.get('archive_id')==archive_id and r.get('member_path')==c['member_path'] for r in rows),('Already recorded member',member_name)
    rows.append({'source_id':archive_id+'::'+c['member_path'],'archive_id':archive_id,'member_path':c['member_path'],'name':member_name,'sha256':c['sha256'],'bytes':c['bytes'],'snapshot':c['snapshot'],'inspection_kind':kind,'inspection_scope':'entire actual raster' if kind=='visual' else 'complete document','observation':observation,'limitations':limitations,'read_ranges':read_ranges,'inspection_basis':'Actual functions.read_file display/read of verified extracted member in this Phase2. Exact-byte duplicates share this inspection; distinct board text and differently encoded variants do not automatically inherit it.','does_not_change_source_approval':True})
    P.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
