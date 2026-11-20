#!/usr/bin/env python3
"""Build human-readable, explicitly qualified reports from the actual ledger.
Does not inspect source art, execute source scripts or issue approval.
"""
from pathlib import Path
import json,csv,html,re,hashlib
import markdown
B=Path(__file__).resolve().parents[1];V=B/'verification'
load=lambda p:json.loads(p.read_text())
C=load(V/'AUDIT_COVERAGE_STATUS.json');DATA=load(B/'inventory/CATALOGUE_DATA.json');G=load(B/'production_gap_register.json');BR=load(B/'artist_ready_briefs.json');J=load(B/'cd_decision_register.json');N=load(V/'remote_nodes.json');A=load(V/'ARCHIVE_MEMBERS.json');AK={x['archive_id']+'::'+x['member_path']:x for x in A}
def esc(s):return html.escape(str(s),quote=False).replace('|','&#124;').replace('\n','<br>')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+['| '+' | '.join(esc(x) for x in row)+' |' for row in rows])
def refs(sources):
 out=[]
 for s in sources:
  if s in N:out.append('- `'+s+'` — ['+esc(N[s].get('name',s))+'](https://drive.google.com/file/d/'+s+'/view)')
  elif s in AK:
   x=AK[s];out.append('- ['+esc(x['archive_name'])+'](https://drive.google.com/file/d/'+x['archive_id']+'/view) :: `'+x['member_path']+'`')
  else:out.append('- ['+s+']('+s+')')
 return '\n'.join(out)
def writecsv(path,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
# Full D, G, J are not replaced by summaries.
d=['# D. Production gap register','',G['status'],'',G['priority_rule'],'','Every recommendation below is unexecuted. Existing restrictions remain intact. The register is not exhaustive while actual inspection is incomplete.','']
labels=[('asset_scene','Asset / scene'),('current_material','Current material'),('deficiency','Deficiency'),('production_impact','Production impact'),('priority','Priority'),('required_solution','Required solution'),('production_instructions','Production instructions'),('acceptance_criteria','Acceptance criteria'),('dependency','Dependency'),('owner_expertise','Responsible specialist')]
for x in G['gaps']:
 d+=['## '+x['gap_id']+' — '+x['asset_scene'],'']
 for k,label in labels:d+=['**'+label+':** '+x[k],'']
 d+=['**Exact affected sources:**','',refs(x['affected_sources']),'','---','']
(B/'D_PRODUCTION_GAP_REGISTER.md').write_text('\n'.join(d));writecsv(B/'D_PRODUCTION_GAP_REGISTER.csv',G['gaps'])
g=['# G. Artist-ready production briefs','',BR['status'],'',BR['scope_rule'],'']
for x in BR['briefs']:
 g+=['## '+x['brief_id']+' — '+x['title'],'','**Related gaps:** '+', '.join(x['related_gaps']),'','**Specialist:** '+x['specialist'],'','**Start condition:** '+x['start_condition'],'','### Inputs','']+['- '+s for s in x['inputs']]+['','### Instructions','']+[str(i)+'. '+s for i,s in enumerate(x['instructions'],1)]+['','### Deliverables','']+['- '+s for s in x['deliverables']]+['','### Objective acceptance tests','']+['- '+s for s in x['acceptance_tests']]+['','**Do not:** '+x['do_not'],'','**Dependencies:** '+x['dependencies'],'','---','']
(B/'G_ARTIST_READY_BRIEFS.md').write_text('\n'.join(g));writecsv(B/'G_ARTIST_READY_BRIEFS.csv',BR['briefs'])
j=['# J. Creative Director decision register','',J['status'],'',J['evidence_first_rule'],'']
for x in J['decisions']:
 j+=['## '+x['decision_id']+' — '+x['topic'],'']
 for k,label in [('state','State / not a new approval'),('existing_control','Existing control — preserve'),('decision_needed','Genuinely needed decision / evidence'),('decision_owner','Decision owner'),('consequence','Production consequence'),('closure_evidence','Closure evidence'),('recommendation_not_execution','Recommendation, not execution')]:j+=['**'+label+':** '+x[k],'']
 j+=['**Related gaps:** '+', '.join(x['related_gaps']),'','---','']
(B/'J_CD_DECISION_REGISTER.md').write_text('\n'.join(j));writecsv(B/'J_CD_DECISION_REGISTER.csv',J['decisions'])
coverage=table(['Measure','Verified accounting / limitation'],[
 ('Known folders / saved listing pages',f"{C['enumerated_folders']} / {C['saved_normalized_listing_pages']}; no known folder lacks a complete final page"),
 ('Known physical files',str(C['physical_files'])+'; not a logical-asset count'),
 ('Physical source-ID/hash bindings',str(C['physical_hash_bound_source_ids'])+'; some historical selected snapshots are unavailable locally'),
 ('Physical current representations available',str(C['physical_current_representation_available'])+'; availability is not inspection'),
 ('Actual inspection observations',f"{C['inspection_ledger_observations']} = {C['visual_observations']} whole-raster visual + {C['semantic_observations']} complete-semantic observations"),
 ('Distinct actually inspected payload hashes',str(C['distinct_actually_inspected_payload_hashes'])+'; repeated representations/observations are not additional assets'),
 ('Physical sources linked to actually inspected exact bytes',str(C['physical_sources_with_actual_exact_payload_content_inspection'])+'; shared bytes do not share approval'),
 ('Archive members / distinct archive payloads',f"{C['archive_member_records']} / {C['distinct_archive_payload_hashes']}; CRC/hash/decode do not imply content inspection"),
 ('Distinct archive rasters still visually uninspected',str(C['distinct_uninspected_archive_raster_payloads'])+'; additional unbound/other records remain'),
 ('Associated local files / total catalogue records',f"{C['associated_local_files']} / {C['all_catalogue_records']}; includes intentional duplicates and evidence copies"),
 ('Outstanding catalogue records',str(C['all_catalogue_uninspected_record_count_not_distinct_assets'])+'; record count, NOT distinct logical assets'),
 ('All-file inspection / final logical denominator','NOT COMPLETE / NOT ESTABLISHED'),
 ('Phase2 remote writes / source design alterations','0 / 0'),
])
P={x['source_id']:x for x in DATA['physical']}
chosen=[
 ('Adanna approved portrait','1k08XH8VjNJAnSoMNU4YvBPtBEUdYD20y','Identity/reference anchor; not a body/rig','G03/G05/G08'),
 ('Adanna LEFT_SIDE V003','14uOMGJYXucAHpfCByFi8TW_i1ZxriKMy','PRESERVE / UNAPPROVED; no V004','G03/G04'),
 ('Adanna BACK V003','11MmHTZ-CawZrvknG21bsgqqKXJ-7x2nP','PRESERVE / UNAPPROVED; settled anatomical LEFT','G03/G04'),
 ('Costume V002','1OcNpG55dadGkIUUar7W0Vm5Lkb2QGLJR','Interim partial UPPER-BODY working reference only','G03/G07'),
 ('Primary blade V001','1V12Sq2BZdIqjsgkx5GRpzGxc3nS3Gbac','X: CQ-9 before fit/rig; provisional dimensions','G04'),
 ('Hall of Posts V004','1MHCd25z3x-cfBUf-eoCJvDLqwvYj9Ins','Design-approved, canon pending','G09'),
 ('Mothers Courtyard V007','1EMYjEMCzfqhwEAfpvN8uDNfAddgLpVue','Design-approved, canon pending; panels not measured layout','G09'),
 ('Nneka interior V003','1kT8ucpt6HVWhWEM8xvLRxTyGGjrNIxgf','Design-approved, canon pending; doorway not connectivity proof','G09'),
 ('Nneka house V004','1JIoAiQ20goibDA-ujYr95iyihBTLKZWj','Design-approved, canon pending','G09'),
 ('Sealed Quarter V003','13jAtOMkXBazG2jbcFWZeBLsI1mufWJqU','Design-approved, canon pending; no parent assignment inferred','G09'),
 ('Establishing V013','1MuhupyLWP2fqLn0mhfAzXXTjy0q6sqa0','Internal exploratory only; item5 NOT DONE / limited waiver','G10'),
 ('H3 / VR011 V002','1_vJFw7KNJRn435OijQHdjDhds0G-gF6n','X: D9/RQ-01, no fresh H3 visual/cultural release','G18'),
 ('Sleeping Room V002','1SR7CRZC9MZjTBsEi84_N3b4sesAmDsiq','Accepted visual-only endpoint; not engineering/canon approval','G08/G09/G13'),
 ('Streets V002','1lnMePbbXNHmDZTnbmcJW47RGbMtIfjo4','Accepted visual-only endpoint; preserve','G11'),
 ('Kitchen V003 / E46','1b2vTn10kpAsmmMaN53yzQ8G4pJZc1wR0','Selected accepted internal firewood study, NOT failed','G13'),
 ('Narrow Passages V003 / E50','1p1erIKGaOy4UX3MWCFgJTnIAcX1XSz0e','Selected accepted internal endpoint study','G13'),
 ('Fishing Shelter V002','13Dc48FnSA9nvCUzL2zBq6zNv6axFLtIG','Internal canvas accepted; specialist craft question remains','G14'),
 ('Canoe Shed V002','16E4umob2MQdXGMRt1M9upT5yYOJ8-3UV','Native overcast proof needed if commissioned; failed V003 not replacement','G15'),
]
selrows=[]
for title,ident,use,gap in chosen:
 x=P[ident];dims=str(x.get('width_px','?'))+' × '+str(x.get('height_px','?'));refs1=','.join(map(str,x['inspection_ledger_rows_1based'])) or 'U'
 selrows.append([title+' / '+ident,dims,use,'V (A4 rows '+refs1+')' if x['content_inspection_state']=='ACTUALLY_INSPECTED_EXACT_PAYLOAD' else 'U','NV / NV / NV',gap])
selected=table(['Source / exact ID','Measured pixels','Authority / permitted use','Actual inspection','Model / rig / final-shot evidence','Gap'],selrows)
gapsummary=table(['Gap','Affected production area','Priority','Required closure / specialist'],[[x['gap_id'],x['asset_scene'],x['priority'],x['required_solution']+' — '+x['owner_expertise']] for x in G['gaps']])
briefsummary=table(['Brief','Deliverable focus','Specialist / prerequisites'],[[x['brief_id'],x['title'],x['specialist']+'; '+x['start_condition']] for x in BR['briefs']])
cdsummary=table(['Decision','Topic / status','Owner / closure'],[[x['decision_id'],x['topic']+' — '+x['state'],x['decision_owner']+'; '+x['closure_evidence']] for x in J['decisions']])
s=(B/'report_source.md').read_text()
for token,value in {'COVERAGE_TABLE':coverage,'SELECTED_ASSET_TABLE':selected,'GAP_COUNT':str(len(G['gaps'])),'GAP_SUMMARY_TABLE':gapsummary,'BRIEF_TABLE':briefsummary,'CD_TABLE':cdsummary}.items():s=s.replace('{{'+token+'}}',value)
assert not re.search(r'\{\{[A-Z_]+\}\}',s)
(B/'TDD_PHASE2_A_TO_J_WORKING_AUDIT.md').write_text(s)
# Useful standalone B/E/F/H/I sections; D/G/J retain the full detailed versions.
section_files={'A':'A_VISUAL_INVENTORY_SCOPE.md','B':'B_ART_BIBLE_COMPLETENESS_ASSESSMENT.md','C':'C_READINESS_MATRIX_GUIDE.md','E':'E_IMMEDIATE_OPPORTUNITIES.md','F':'F_PRODUCTION_BLOCKERS.md','H':'H_RECOMMENDED_PRODUCTION_PIPELINE.md','I':'I_SOFTWARE_AND_HARDWARE_RECOMMENDATIONS.md'}
for letter,name in section_files.items():
 match=re.search(r'^# '+letter+r'\. .*?(?=^# [A-J]\. |^## Source and verification navigation|\Z)',s,re.S|re.M);assert match,name
 (B/name).write_text('> Coverage-qualified working audit. Phase2 all-file inspection is incomplete; no approval/execution is issued.\n\n'+match.group(0))
style='''
:root{--paper:#fffefa;--ink:#202a32;--muted:#5a6770;--line:#d8dfdc;--accent:#25675e;--warn:#8e4928;--back:#edf1ee}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--back);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}.shell{max-width:1480px;margin:auto;display:grid;grid-template-columns:290px minmax(0,1fr);gap:28px;padding:28px}.side{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;padding:22px 18px;border:1px solid var(--line);border-radius:12px;background:#f7f9f5}.eyebrow{font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:750;color:var(--accent)}.badge{display:inline-block;background:#fff0e5;border:1px solid #e5c6ad;border-radius:100px;color:var(--warn);font-size:12px;font-weight:700;padding:4px 11px;margin:12px 0}.side .toc ul{padding-left:16px}.side .toc>ul{padding-left:0;list-style:none}.side .toc{font-size:12px;line-height:1.5}.side .toc a{text-decoration:none;display:inline-block;margin:4px 0}.side p{font-size:12px;color:var(--muted)}main{background:var(--paper);padding:50px 52px 64px;border:1px solid var(--line);border-radius:14px;min-width:0;box-shadow:0 12px 40px #1d3b2a08}h1,h2,h3{line-height:1.23;letter-spacing:-.025em}h1{font-size:30px;margin:60px 0 24px;border-top:2px solid var(--accent);padding-top:24px}h1:first-child{margin:0;border:0;padding:0;font-size:37px}h2{font-size:23px;margin-top:32px}h3{font-size:18px;color:var(--accent);margin-top:27px}p,li{max-width:90ch}strong{font-weight:680}hr{border:0;border-top:1px solid var(--line);margin:34px 0}blockquote{margin:20px 0;padding:14px 20px;background:#fff2e8;border-left:4px solid var(--warn)}table{border-collapse:collapse;width:100%;font-size:12px;line-height:1.5;margin:23px 0;table-layout:auto}th,td{text-align:left;vertical-align:top;border:1px solid var(--line);padding:11px 12px;overflow-wrap:anywhere}th{background:#eaf2ed;font-size:11px;letter-spacing:.025em}tr:nth-child(even) td{background:#f8faf7}code{font:11px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere;background:#eff2ec;border-radius:3px;padding:2px 4px}pre{overflow:auto;white-space:pre-wrap}.footer{margin-top:42px;padding-top:20px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}.jump{display:inline-block;padding:7px 11px;border:1px solid var(--line);border-radius:7px;margin:3px 2px;font-size:12px;text-decoration:none;background:white}@media(max-width:1050px){.shell{grid-template-columns:1fr;padding:12px;gap:14px}.side{position:static;max-height:none;padding:18px}.side .toc{display:none}main{padding:28px 23px}h1:first-child{font-size:29px}table{font-size:11px}td,th{padding:8px 7px}}@media print{@page{size:A4;margin:17mm}.shell{display:block;padding:0}.side{display:none}body{background:white;font-size:10pt}main{padding:0;border:0;box-shadow:none}h1{page-break-before:always;font-size:22pt}h1:first-child{page-break-before:auto;font-size:27pt}h2,h3{break-after:avoid}table{font-size:7.5pt}tr{break-inside:avoid}a{color:inherit}th{background:#eef2ee!important}.footer{font-size:8pt}}
'''
def render(mdpath,title,nav=True):
 text=mdpath.read_text();converter=markdown.Markdown(extensions=['tables','fenced_code','toc','sane_lists'],extension_configs={'toc':{'toc_depth':'1-3'}});body=converter.convert(text);toc=converter.toc
 page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(title)+'</title><style>'+style+'</style></head><body><div class="shell"><aside class="side"><div class="eyebrow">TDD / Production audit</div><div class="badge">Coverage qualified · not final</div><p>Audit only. No design change, approval promotion or gate waiver.</p><a class="jump" href="TDD_PHASE2_A_TO_J_WORKING_AUDIT.html">A–J report</a><a class="jump" href="D_PRODUCTION_GAP_REGISTER.html">Detailed gaps</a><a class="jump" href="G_ARTIST_READY_BRIEFS.html">Artist briefs</a><a class="jump" href="J_CD_DECISION_REGISTER.html">CD register</a>'+toc+'</aside><main>'+body+'<div class="footer">Additive working audit. Raw source art/download staging is not bundled as a complete source backup. The explicit remaining-inspection queue controls completeness. Recommendations are not execution.</div></main></div></body></html>'
 mdpath.with_suffix('.html').write_text(page)
for name,title in [('TDD_PHASE2_A_TO_J_WORKING_AUDIT.md','TDD — Phase2 A–J working production-readiness audit'),('D_PRODUCTION_GAP_REGISTER.md','TDD — Detailed production gaps'),('G_ARTIST_READY_BRIEFS.md','TDD — Conditional artist-ready briefs'),('J_CD_DECISION_REGISTER.md','TDD — CD decision register')]:render(B/name,title)
print('Built qualified A–J report, detailed D/G/J, standalone A/B/C/E/F/H/I and CSV/JSON companions. No source altered or approval issued.')
