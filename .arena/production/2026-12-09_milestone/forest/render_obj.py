#!/usr/bin/env python3
"""Minimal flat-shaded OBJ preview (Z-up) for kit modules."""
import sys, math
from PIL import Image, ImageDraw
path, out = sys.argv[1], sys.argv[2]
verts=[]; faces=[]
for line in open(path):
    p=line.split()
    if not p: continue
    if p[0]=='v': verts.append(tuple(map(float,p[1:4])))
    elif p[0]=='f': faces.append([int(t.split('/')[0])-1 for t in p[1:]])
MAT={'wall_laterite_mud':(148,84,51),'foundation_laterite_rubble':(115,66,41),'thatch_ata_bundles':(158,122,66),'timber_lintel_plain':(77,51,31),'clay_pot_fired':(107,61,38),'woven_fibre_plain':(140,107,61),'courtyard_stone_plain':(82,77,71)}
cols=[]; cur=(150,150,150)
for line in open(path):
    p=line.split()
    if p and p[0]=='usemtl': cur=MAT.get(p[1],cur)
    elif p and p[0]=='f': cols.append(cur)
W,H=560,420
for view in ('iso','front'):
    img=Image.new('RGB',(W,H),(176,176,176)); dr=ImageDraw.Draw(img)
    def proj(v):
        x,y,z=v
        if view=='front': return (x,z,-y)
        t=math.radians(35); u=x*math.cos(t)-y*math.sin(t); dep=x*math.sin(t)+y*math.cos(t)
        return (u, z*0.9+dep*0.35, dep)
    allp=[proj(v) for v in verts]
    us=[p[0] for p in allp]; vs=[p[1] for p in allp]
    sc=min((W-40)/max(max(us)-min(us),0.01),(H-40)/max(max(vs)-min(vs),0.01))
    cu=(max(us)+min(us))/2; cv=(max(vs)+min(vs))/2
    pf=[]
    for f,c in zip(faces,cols):
        pts=[proj(verts[i]) for i in f]
        pf.append((sum(p[2] for p in pts)/len(pts),pts,c))
    pf.sort(key=lambda e:-e[0])
    for _,pts,c in pf:
        dr.polygon([(W/2+(p[0]-cu)*sc, H/2-(p[1]-cv)*sc) for p in pts], fill=c)
    img.save(f"{out}_{view}.png"); print(f"{out}_{view}.png")
