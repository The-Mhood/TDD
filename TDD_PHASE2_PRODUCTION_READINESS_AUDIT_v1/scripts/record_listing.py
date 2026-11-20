#!/usr/bin/env python3
"""Normalize manually transcribed successful connector folder listings.
NOT a raw API archive; never creates observations from a planned inventory.
Folder rows: F|id|name|DriveRevision
File rows: id|name|bytes|md5|DriveRevision[|mimeType]
"""
from pathlib import Path
import json
B=Path(__file__).resolve().parents[1]
V=B/'verification';V.mkdir(exist_ok=True)
MIME={'.md':'text/markdown','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.zip':'application/zip','.json':'application/json','.csv':'text/csv','.txt':'text/plain','.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','.pdf':'application/pdf'}

def record(parent,request,rows='',next_token=None,page=1,complete=True):
    p=V/'remote_nodes.json';nodes=json.loads(p.read_text()) if p.exists() else {}
    entries=[]
    for line in rows.strip().splitlines():
        if not line.strip():continue
        a=line.split('|');folder=a[0]=='F'
        if folder:
            _,ident,name,version=a;item={'id':ident,'name':name,'mime_type':'application/vnd.google-apps.folder','parents':[parent],'drive_version':version,'is_folder':True}
        else:
            ident,name,size,md5,version,*mime=a
            item={'id':ident,'name':name,'mime_type':mime[0] if mime else MIME.get(Path(name).suffix.lower(),'application/octet-stream'),'parents':[parent],'drive_version':version,'is_folder':False,'bytes':int(size),'md5':md5,'content_inspection_state':'NOT YET INSPECTED'}
        old=nodes.get(ident,{})
        if old.get('parents') and old['parents']!=[parent]:raise AssertionError(('Parent changed or mistyped observation',ident,old['parents'],parent))
        nodes[ident]={**old,**item};entries.append(item)
    d=V/'listings';d.mkdir(exist_ok=True)
    observation={'parent_id':parent,'connector_response_request_id':request,'page':page,'observed_count':len(entries),'entries':entries,'next_page_token':next_token,'next_page_token_present':next_token is not None,'incomplete_search':False,'complete_final_page':bool(complete and next_token is None),'basis':'Manually transcribed successful current connector list_files result; fields shown were equal-checked, not a raw API capture. Content is not claimed inspected by enumeration.'}
    (d/f'{parent}_p{page:03d}.json').write_text(json.dumps(observation,indent=2,ensure_ascii=False)+'\n')
    parent_node=nodes.setdefault(parent,{'id':parent,'is_folder':True})
    pages=sorted(d.glob(parent+'_p*.json'));allentries=[]
    for f in pages:allentries.extend(json.loads(f.read_text())['entries'])
    ids=[x['id'] for x in allentries];assert len(ids)==len(set(ids)),('Duplicated page/member',parent)
    parent_node.update(listed_child_ids=ids,listing_pages=len(pages),listing_complete=observation['complete_final_page'],listing_incomplete_search=False)
    p.write_text(json.dumps(nodes,indent=2,ensure_ascii=False)+'\n')
    print(parent,'page',page,'observed',len(entries),'complete',observation['complete_final_page'])
