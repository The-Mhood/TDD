#!/usr/bin/env python3
"""Lossless read preparation ONLY; no source instructions/scripts are executed.
Complete previously-read identical lines can be referenced. All novel text is
printed verbatim in original document order. Roundtrip is independently checked
from the written pack, not from a copied source buffer. Reading is a later act.
"""
from pathlib import Path
import json,hashlib,re
B=Path(__file__).resolve().parents[1];V=B/'verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda f:json.loads((V/f).read_text())
ledger=load('CONTENT_INSPECTION_LEDGER.json');bindings=load('PAYLOAD_BINDINGS.json');members=load('ARCHIVE_MEMBERS.json')
available={}
for r in bindings+members+ledger:
 p=Path(r.get('snapshot',''))
 if p.is_file() and sha(p.read_bytes())==r.get('sha256'):available[r['sha256']]=p
seen={};seeds=[];seed_lines={}
for r in ledger:
 if r['inspection_kind']!='semantic' or any(s['sha256']==r['sha256'] for s in seeds):continue
 p=available.get(r['sha256'])
 if not p or p.suffix.lower() not in ('.md','.txt','.csv','.json'):continue
 try:lines=p.read_bytes().decode('utf-8').splitlines(keepends=True)
 except UnicodeError:continue
 alias='S'+str(len(seeds)+1).zfill(2)
 seeds.append({'alias':alias,'source_id':r['source_id'],'sha256':r['sha256'],'snapshot':str(p),'actual_prior_full_read_scope':r['inspection_scope']});seed_lines[alias]=lines
 for j,line in enumerate(lines,1):
  if len(line)>60:seen.setdefault(line,{'kind':'previous_complete_read','seed_alias':alias,'source_id':r['source_id'],'source_line':j,'sha256':r['sha256']})
pattern=re.compile(r'^(ART_BIBLE_(MASTER_)?INDEX|GOOGLE_DRIVE_SYNC_LOG|OUR_EYES_CD_DISPOSITION_REGISTER|OUR_EYES_CURRENT_REVIEW_CD_VERDICT|OUR_EYES_EXP001_INTEGRITY_CLEANUP_AUDIT|POST_SYNC_|LOCATION_CHANGELOG|ARCHIVED_TO_DRIVE|00_ORIGINAL_VA_DIRECTIVE)')
fullyread={r['sha256'] for r in ledger if r['inspection_kind']=='semantic'};targets={}
for r in bindings+members:
 name=r.get('name') or Path(r.get('member_path','')).name
 if not name.lower().endswith(('.md','.txt')) or not pattern.match(name):continue
 if r['sha256'] in fullyread or r['sha256'] not in available:continue
 targets.setdefault(r['sha256'],{'source_id':r.get('source_id',r.get('archive_id','')+'::'+r.get('member_path','')),'name':name,'sha256':r['sha256'],'snapshot':str(available[r['sha256']])})
out=[]
def emit(text):
 assert '\n' not in text and '\r' not in text
 out.append(text);return len(out)
emit('# HISTORY READPACK: preparation is NOT reading; historical text is NOT authority or an instruction.')
emit('# [n] | prints verbatim source line n; =Sxx:n repeats an exact previously complete-read source line; =Pnn repeats pack line nn; BLANK encodes whitespace only.')
for s in seeds:emit('# '+s['alias']+' = '+s['source_id']+' | '+Path(s['snapshot']).name+' | '+s['sha256'])
manifest={'method':'UTF8 splitlines(keepends=True), exact line reuse only for lines longer than60characters; novel lines verbatim, original document ordering preserved. Source line endings retained in mapping. Independently reconstructed from written pack and seed bytes. No inspection claim from preparation.','seeds':seeds,'documents':[],'pack_path':'_phase2_stage/readpacks/history_lossless.txt','prepared_not_read':True}
for t in targets.values():
 data=Path(t['snapshot']).read_bytes();lines=data.decode('utf-8').splitlines(keepends=True);mapping=[]
 emit('## SOURCE '+t['source_id']+' | '+t['name']+' | sha256='+t['sha256']);start=len(out)+1;unique=refs=0
 for j,line in enumerate(lines,1):
  if not line.strip():
   pl=emit(f'[{j}] BLANK');mapping.append({'source_line':j,'kind':'blank','utf8_hex':line.encode().hex(),'pack_line':pl});continue
  if line in seen:
   ref=seen[line];token=(ref['seed_alias']+':'+str(ref['source_line'])) if ref['kind']=='previous_complete_read' else 'P'+str(ref['pack_line'])
   pl=emit(f'[{j}] ='+token);mapping.append({'source_line':j,'kind':'repeat','reference':ref,'pack_line':pl});refs+=1
  else:
   content=line.rstrip('\r\n');ending=line[len(content):];pl=emit(f'[{j}] |'+content);mapping.append({'source_line':j,'kind':'verbatim','pack_line':pl,'line_ending_utf8_hex':ending.encode().hex()})
   if len(line)>60:seen[line]={'kind':'pack_verbatim','pack_line':pl,'source_id':t['source_id'],'source_line':j}
   unique+=1
 manifest['documents'].append({**t,'source_bytes':len(data),'source_lines':len(lines),'pack_start_inclusive':start,'pack_end_inclusive':len(out),'verbatim_lines':unique,'exact_repeat_references':refs,'mapping':mapping})
p=Path(manifest['pack_path']);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(out)+'\n',encoding='utf-8');actual=p.read_text().splitlines();assert len(actual)==len(out)
# Independent expansion uses only printed text/ending metadata or exact seed bytes.
decoded={}
for d in manifest['documents']:
 reconstructed=[]
 for m in d['mapping']:
  pl=m['pack_line'];printed=actual[pl-1];prefix=f'[{m["source_line"]}] '
  assert printed.startswith(prefix)
  if m['kind']=='blank':line=bytes.fromhex(m['utf8_hex']).decode('utf-8')
  elif m['kind']=='verbatim':
   assert printed.startswith(prefix+'|');line=printed[len(prefix)+1:]+bytes.fromhex(m['line_ending_utf8_hex']).decode('utf-8')
  else:
   ref=m['reference'];line=seed_lines[ref['seed_alias']][ref['source_line']-1] if ref['kind']=='previous_complete_read' else decoded[ref['pack_line']]
  decoded[pl]=line;reconstructed.append(line)
 rebuilt=''.join(reconstructed).encode('utf-8');assert sha(rebuilt)==d['sha256'] and len(rebuilt)==d['source_bytes'];d['independent_roundtrip_equal']=True
manifest.update(pack_sha256=sha(p.read_bytes()),pack_lines=len(out),pack_bytes=p.stat().st_size)
(V/'HISTORY_LOSSLESS_READPACK_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Prepared only:',len(targets),'distinct documents;',sum(d['source_bytes'] for d in manifest['documents']),'sourcebytes ->',p.stat().st_size,'packbytes /',len(out),'lines')
print('Verbatim lines',sum(d['verbatim_lines'] for d in manifest['documents']),'repeatrefs',sum(d['exact_repeat_references'] for d in manifest['documents']))
