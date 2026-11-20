#!/usr/bin/env python3
"""Record actual bounded reading of an unchanged losslessly referenced source.
The readpack preparation/roundtrip check is NEVER recorded as reading.
"""
from pathlib import Path
import hashlib,json
from document_segments import source
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification';P=V/'LOSSLESS_READPACK_INSPECTIONS.json'
def record(first,last,observation):
 m=json.loads((V/'LOCATION_LOSSLESS_READPACK_MANIFEST.json').read_text());d=(R/m['readpack']).read_bytes();assert hashlib.sha256(d).hexdigest()==m['readpack_sha256']
 lines=d.decode().splitlines();assert 1<=first<=last<=len(lines)
 a=json.loads(P.read_text()) if P.exists() else [];assert not any(x['readpack_sha256']==m['readpack_sha256'] and x['first_line']==first and x['last_line']==last for x in a),'Already recorded'
 a.append({'source_id':m['source_id'],'source_sha256':m['source_sha256'],'readpack':m['readpack'],'readpack_sha256':m['readpack_sha256'],'first_line':first,'last_line':last,'readpack_total_lines':len(lines),'range_sha256':hashlib.sha256('\n'.join(lines[first-1:last]).encode()).hexdigest(),'observation':observation,'basis':'Actual full bounded read_file text returned/read. Complete source content remains in original order: every novel paragraph is verbatim, each exact repeat explicitly references an earlier verbatim paragraph with current preceding-entry context; roundtrip equality is verified separately and is not itself content reading. This row is partial, not complete-source inspection.','does_not_change_source_approval':True})
 P.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
def assert_complete():
 m=json.loads((V/'LOCATION_LOSSLESS_READPACK_MANIFEST.json').read_text());c,src=source(m['source_id']);assert c['sha256']==m['source_sha256']
 d=(R/m['readpack']).read_bytes();assert hashlib.sha256(d).hexdigest()==m['readpack_sha256']
 raw=json.loads((V/'DOCUMENT_SEGMENT_INSPECTIONS.json').read_text());prefix=set()
 for x in raw:
  if x['source_id']==m['source_id'] and x['sha256']==m['source_sha256']:prefix.update(range(x['first_line'],x['last_line']+1))
 assert set(range(1,m['raw_read_prefix'][1]+1))<=prefix,'Raw prefix not fully read'
 read=json.loads(P.read_text());covered=set()
 for x in read:
  if x['readpack_sha256']==m['readpack_sha256']:covered.update(range(x['first_line'],x['last_line']+1))
 assert covered==set(range(1,m['readpack_total_lines']+1)),('Unread readpack lines remain',m['readpack_total_lines']-len(covered))
 full={};expanded=[]
 # Verify each reference against raw source text and the earlier actual full-text
 # occurrence. No approximate/semantic deduplication is allowed.
 for x in m['blocks']:
  t='\n'.join(src[x['source_first']-1:x['source_last']]);ref=x.get('reference')
  if ref:
   a,z=ref['source_lines'];assert z<x['source_first'];other='\n'.join(src[a-1:z]);assert t==other
   assert z<=m['raw_read_prefix'][1] or (a,z) in full
  else:full[(x['source_first'],x['source_last'])]=True
  expanded.extend(range(x['source_first'],x['source_last']+1))
 assert prefix|set(expanded)==set(range(1,len(src)+1))
 return {'raw_source_ranges':[[x['first_line'],x['last_line']] for x in raw if x['source_id']==m['source_id']],'lossless_readpack':m['readpack'],'readpack_sha256':m['readpack_sha256'],'readpack_ranges':[[x['first_line'],x['last_line']] for x in read if x['readpack_sha256']==m['readpack_sha256']],'method':'All unique source text actually read verbatim; all exact repeated paragraph occurrences explicitly read in original context via verified earlier-full-text references. Source unchanged; no summary or keyword excerpt substituted.'}
