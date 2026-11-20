#!/usr/bin/env python3
"""Record ONLY text ranges actually returned/read by the agent, never parsed-only coverage."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification';P=V/'DOCUMENT_SEGMENT_INSPECTIONS.json'
def source(source_id):
 rows=json.loads((V/'PAYLOAD_BINDINGS.json').read_text());rr=[r for r in rows if r['source_id']==source_id]
 assert len(rr)==1,source_id
 c=rr[0];d=(R/c['snapshot']).read_bytes();assert hashlib.sha256(d).hexdigest()==c['sha256'];return c,d.decode('utf-8').splitlines()
def record_segment(source_id,first,last,observation):
 c,lines=source(source_id);assert 1<=first<=last<=len(lines),(first,last,len(lines))
 rows=json.loads(P.read_text()) if P.exists() else [];assert not any(r['source_id']==source_id and r['first_line']==first and r['last_line']==last for r in rows),'already recorded'
 rows.append({'source_id':source_id,'name':c['name'],'sha256':c['sha256'],'snapshot':c['snapshot'],'first_line':first,'last_line':last,'total_source_lines':len(lines),'range_sha256':hashlib.sha256(('\n'.join(lines[first-1:last])).encode()).hexdigest(),'observation':observation,'basis':'Actual bounded functions.read_file text returned in full and semantically read, not an automated parse or selected-line keyword search. A segment is NOT a complete document inspection.','does_not_change_source_approval':True})
 P.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
def assert_complete_ranges(source_id):
 c,lines=source(source_id);rows=json.loads(P.read_text());covered=set()
 for r in rows:
  if r['source_id']==source_id and r['sha256']==c['sha256']:covered.update(range(r['first_line'],r['last_line']+1))
 assert covered==set(range(1,len(lines)+1)),('Unread lines remain',source_id,len(lines)-len(covered))
 return [[r['first_line'],r['last_line']] for r in rows if r['source_id']==source_id and r['sha256']==c['sha256']]
