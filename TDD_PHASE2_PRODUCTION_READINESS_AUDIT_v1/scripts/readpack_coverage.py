#!/usr/bin/env python3
"""Coverage receipts must be added ONLY after an actual bounded tool read.
Does not read files semantically; only verifies byte identity/coverage joins.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1];V=B/'verification'
def state(prefix='HISTORY'):
 m=json.loads((V/(prefix+'_LOSSLESS_READPACK_MANIFEST.json')).read_text());p=Path(m['pack_path']);d=p.read_bytes();assert hashlib.sha256(d).hexdigest()==m['pack_sha256'];return m,p

def record(start,end,note,prefix='HISTORY'):
 m,p=state(prefix);assert 1<=start<=end<=m['pack_lines'];f=V/(prefix+'_READPACK_READS.json');r=json.loads(f.read_text()) if f.exists() else []
 assert not any(z['pack_sha256']==m['pack_sha256'] and z['start']==start and z['end']==end for z in r),'Already recorded range'
 r.append({'pack_sha256':m['pack_sha256'],'pack_path':str(p),'start':start,'end':end,'actual_read_note':note,'basis':'Actual bounded functions.read_file text return; source/repeat expansion validated by independently roundtripped manifest. Preparation alone never supplies this receipt.'});f.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def require_document(source_id,prefix='HISTORY'):
 m,p=state(prefix);f=V/(prefix+'_READPACK_READS.json');r=json.loads(f.read_text()) if f.exists() else [];covered=set()
 for z in r:
  if z['pack_sha256']==m['pack_sha256']:covered.update(range(z['start'],z['end']+1))
 matches=[x for x in m['documents'] if x['source_id']==source_id];assert len(matches)==1;doc=matches[0];needed=set(range(doc['pack_start_inclusive']-1,doc['pack_end_inclusive']+1))
 for line in doc['mapping']:
  if line['kind']=='repeat' and line['reference']['kind']=='pack_verbatim':needed.add(line['reference']['pack_line'])
 assert needed<=covered,('Unread required pack lines',source_id,sorted(needed-covered)[:30])
 payload=Path(doc['snapshot']).read_bytes();assert hashlib.sha256(payload).hexdigest()==doc['sha256'] and len(payload)==doc['source_bytes'];assert doc['independent_roundtrip_equal']
 return {'readpack':str(p),'readpack_sha256':m['pack_sha256'],'source_sha256':doc['sha256'],'source_lines':doc['source_lines'],'document_pack_range_inclusive':[doc['pack_start_inclusive']-1,doc['pack_end_inclusive']],'exact_repeat_references':doc['exact_repeat_references'],'all_required_literal_and_reference_lines_read':True,'manifest':'verification/'+prefix+'_LOSSLESS_READPACK_MANIFEST.json','reads':'verification/'+prefix+'_READPACK_READS.json'}
