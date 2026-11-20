#!/usr/bin/env python3
"""Prepare, NOT inspect, a losslessly resolvable reading copy of the location source.
Only long EXACT repeated paragraphs are back-referenced, never paraphrased.
All occurrences retain their actual source line ranges and entry context. The
first 2400 source lines were actually read verbatim; no later line is thereby
marked read. Each new readpack segment still requires actual agent reading.
"""
from pathlib import Path
import re,json,hashlib
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification'
ID='1IT5RVzd7kBsPeo3hdJpTliqj4h6O6C9R';PREFIX=2400
binding=next(x for x in json.loads((V/'PAYLOAD_BINDINGS.json').read_text()) if x['source_id']==ID)
p=R/binding['snapshot'];data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==binding['sha256']
lines=data.decode().splitlines(keepends=True);plain=data.decode().splitlines();assert len(lines)==len(plain)
# Contiguous nonblank paragraphs. Whitespace separators are preserved in the pack.
blocks=[];i=0
while i<len(lines):
 first=i;i+=1
 if lines[first].strip():
  while i<len(lines) and lines[i].strip():i+=1
 blocks.append((first+1,i,''.join(lines[first:i])))
seen={};out=[];manifest=[];entry='Opening / chapter tables';read_prefix_ranges=[]
header='LOSSLESS LOCATION READING COPY — source snapshot is unchanged.\nSource ID: '+ID+'\nSource SHA256: '+binding['sha256']+'\nSource lines1–2400 already read verbatim. Remainder below in ORIGINAL ORDER.\nOnly exact repeated paragraphs >=120characters use an earlier full-text back-reference.\nEach occurrence keeps source lines and current entry context. Back-references are not summaries.\nCreating this file is NOT content inspection. Read every line before claiming completion.\n\n'
out=header.splitlines(keepends=True)
for a,z,t in blocks:
 for ln in t.splitlines():
  if ln.startswith(('### ','# CHAPTER','## ')):entry=ln
 if z<=PREFIX:
  if len(t)>=120 and t not in seen:seen[t]={'source_lines':[a,z],'already_raw_read':True}
  continue
 # A paragraph crossing the raw-read boundary is included again IN FULL.
 start=len(out)+1
 if t in seen and len(t)>=120:
  ref=seen[t];source=ref['source_lines'];label=t.splitlines()[0]
  if len(label)>45:label=label[:42]+'...'
  out.append(f"[L{a}–{z}: EXACT SAME {label} AS L{source[0]}–{source[1]}; applies to preceding entry.]\n")
  mode='exact-back-reference'
 else:
  if t.strip():out.append(f'[L{a}–{z}]\n')
  out.extend(t.splitlines(keepends=True));ref=None;mode='verbatim'
  if len(t)>=120:seen[t]={'source_lines':[a,z],'already_raw_read':False}
 manifest.append({'source_first':a,'source_last':z,'source_paragraph_sha256':hashlib.sha256(t.encode()).hexdigest(),'entry_context':entry,'mode':mode,'reference':ref,'readpack_first':start,'readpack_last':len(out)})
text=''.join(out);dest=R/'_phase2_stage/readpacks/location_remaining_lossless.txt';dest.parent.mkdir(exist_ok=True,parents=True);dest.write_text(text)
# Full expansion equality check; not inspection.
lookup={(a,z):t for a,z,t in blocks};expanded=''.join(lookup[tuple(x['reference']['source_lines'])] if x['reference'] else lookup[(x['source_first'],x['source_last'])] for x in manifest)
assert expanded==''.join(lines[manifest[0]['source_first']-1:])
result={'source_id':ID,'source_sha256':binding['sha256'],'source_snapshot':binding['snapshot'],'total_source_lines':len(plain),'raw_read_prefix':[1,PREFIX],'readpack':str(dest.relative_to(R)),'readpack_sha256':hashlib.sha256(text.encode()).hexdigest(),'readpack_total_lines':len(text.splitlines()),'exact_expansion_equals_source_remaining':True,'blocks':manifest,'preparation_is_not_inspection':True}
(V/'LOCATION_LOSSLESS_READPACK_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Lossless readpack prepared, NOT inspected:',len(text.encode()),'bytes;',len(text.splitlines()),'lines;',sum(x['mode']=='exact-back-reference' for x in manifest),'exact paragraph references. Expansion verified.')
