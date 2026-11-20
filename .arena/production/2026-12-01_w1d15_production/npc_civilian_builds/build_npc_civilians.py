#!/usr/bin/env python3
"""NPC CIVILIAN BUILDS V1 (2026-12-01) - production assets from the approved
civilian clothing reference (Register #10). Two background-population variants
on the shared HUMAN_BASE_PROPOSED skeleton (11 joints, same names/scale):
 - NPC_CIVILIAN_M1: man, bare chest, undyed waist wrapper, bare feet.
 - NPC_CIVILIAN_F1: woman, indigo chest wrapper + wrapper skirt, sandals.
Everyday dress only (research record W1 D14); no ceremonial/regalia/jewellery.
Generic unnamed background characters - no identity locks. Same pipeline,
weights convention (prox_blend) and materials family as hero builds.
"""
import io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "2026-11-23_w1d7_production", "pipeline"))
from charbuild import Part, ellipsoid, limb, torus, box, lathe, hand, toes, write_obj, write_glb
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,"..","..","2026-11-20_w1d4_research","textures"))
OUT=os.path.join(HERE,"out"); os.makedirs(OUT,exist_ok=True)
def blend(zlo,zhi,low,high):
    return lambda x,y,zz:{low:1-max(0.0,min(1.0,(zz-zlo)/(zhi-zlo))),high:max(0.0,min(1.0,(zz-zlo)/(zhi-zlo)))}
def prox(z_joint,prox,main,amt=0.45,span=0.14):
    def fn(x,y,zz):
        t=max(0.0,min(1.0,(zz-(z_joint-span))/span))*amt if zz<z_joint else amt
        return {prox:t,main:1-t}
    return fn
def tex(name):
    im=Image.open(os.path.join(ROOT,name)).convert("RGB").resize((512,512)); b=io.BytesIO(); im.save(b,"PNG"); return b.getvalue()

def build(name, female, wrap_mat, skin_mat, sandals):
    parts=[]
    def P(n,m,w): p=Part(n,m,w); parts.append(p); return p
    S=1.02 if female else 1.10
    h=P("head",skin_mat,blend(1.50,1.58,"spine","head"))
    ellipsoid(h,(0,0,1.655),(0.086*S,0.098,0.110),24,16)
    ellipsoid(h,(0,-0.013,1.592),(0.054*S,0.062,0.044),18,10)
    limb(h,(0,0,1.40),(0,0,1.60),0.047,0.041,14)
    ellipsoid(P("nose",skin_mat,"head"),(0,0.094,1.636),(0.014,0.019,0.023),10,8)
    for sx in (-1,1):
        ellipsoid(P(f"eye_{sx}", "eye_dark_v1","head"),(sx*0.032,0.087,1.660),(0.010,0.006,0.007),8,6)
        ellipsoid(P(f"ear_{sx}", skin_mat,"head"),(sx*0.087*S,-0.002,1.652),(0.009,0.015,0.021),8,6)
    ellipsoid(P("torso",skin_mat,blend(1.22,1.40,"pelvis","spine")),(0,0,1.37),(0.150*S,0.108,0.160),24,14)
    ellipsoid(P("pelvis",skin_mat,blend(1.02,1.20,"pelvis","spine")),(0,0,1.07),(0.155*S,0.112,0.150),24,14)
    for side,sx in (("L",-1),("R",1)):
        ua=P(f"upperarm.{side}",skin_mat,prox(1.45,"spine",f"upperarm.{side}",0.30,0.12))
        limb(ua,(sx*0.200*S,0,1.45),(sx*0.290*S,0,1.185),0.048,0.041,18,rings_n=6)
        ellipsoid(ua,(sx*0.200*S,0,1.45),(0.054,0.054,0.054),14,10)
        fa=P(f"forearm_hand.{side}",skin_mat,prox(1.185,f"upperarm.{side}",f"forearm.{side}"))
        limb(fa,(sx*0.290*S,0,1.185),(sx*0.330*S,0,0.945),0.038,0.029,18,rings_n=6)
        hand(fa,(sx*0.332*S,0,0.945),sx)
        th=P(f"thigh.{side}",skin_mat,prox(0.95,"pelvis",f"thigh.{side}",0.40,0.16))
        limb(th,(sx*0.096,0,0.95),(sx*0.106,0,0.525),0.068,0.050,18,rings_n=6)
        sh=P(f"shin_foot.{side}",skin_mat,prox(0.525,f"thigh.{side}",f"shin.{side}"))
        limb(sh,(sx*0.106,0,0.525),(sx*0.106,0,0.07),0.047,0.032,18,rings_n=6)
        ellipsoid(sh,(sx*0.106,0.046,0.030),(0.040,0.100,0.026),12,8)
        toes(sh,(sx*0.106,0.046,0.028))
        if sandals:
            sd=P(f"sandal.{side}","leather_plain_v1",f"shin.{side}")
            box(sd,sx*0.106,0.050,0.006,0.084,0.215,0.010); box(sd,sx*0.106,0.072,0.036,0.076,0.028,0.008)
    if female:
        wrap=P("chest_wrapper",wrap_mat,blend(1.24,1.40,"pelvis","spine"))
        lathe(wrap,[(0.156,0.118,1.262),(0.152,0.115,1.28),(0.166,0.126,1.33),(0.170,0.129,1.385),(0.148,0.110,1.428),(0.152,0.113,1.44)],24,fold_amp=0.02,fold_n=7,cap_top=False,cap_bot=False)
        skirt=P("wrapper_skirt",wrap_mat,"pelvis")
        lathe(skirt,[(0.208,0.157,0.70),(0.204,0.154,0.72),(0.196,0.148,0.84),(0.186,0.141,0.98),(0.182,0.138,1.08),(0.186,0.141,1.16)],24,fold_amp=0.028,fold_n=9,cap_top=False,cap_bot=False)
        ellipsoid(P("head_tie","cloth_undyed_v1","head"),(0,-0.012,1.718),(0.099,0.107,0.062),18,10)
    else:
        skirt=P("waist_wrapper",wrap_mat,"pelvis")
        lathe(skirt,[(0.196,0.148,0.60),(0.192,0.145,0.63),(0.186,0.141,0.80),(0.180,0.136,0.92),(0.176,0.133,1.04),(0.182,0.138,1.13),(0.178,0.135,1.16)],24,fold_amp=0.026,fold_n=9,cap_top=False,cap_bot=False)
    MATS={skin_mat:(0.40,0.26,0.17),"cloth_indigo_plain_v1":(0.10,0.12,0.32),"cloth_undyed_v1":(0.66,0.57,0.44),
          "leather_plain_v1":(0.30,0.19,0.11),"eye_dark_v1":(0.03,0.02,0.02)}
    TEXT={"cloth_indigo_plain_v1":tex("T_ADANNA_IndigoCloth_BC_2048.png")}
    nv,tris=write_obj(os.path.join(OUT,name+".obj"),parts,MATS)
    write_glb(os.path.join(OUT,name+".glb"),parts,MATS,TEXT,meta=name+" civilian NPC V1")
    qc={"asset":name,"tier":"production asset - NOT qualified, NOT Unreal-integrated","parts":len(parts),"verts":nv,"tris":tris,
        "skeleton":"HUMAN_BASE_PROPOSED unchanged (11 joints)","source_reference":"NPC_CIVILIAN_CLOTHING_REFERENCE_V1 (approved 2026-11-30)"}
    json.dump(qc,open(os.path.join(OUT,name+"_QC.json"),"w"),indent=2); print(json.dumps(qc))

build("NPC_CIVILIAN_M1",False,"cloth_undyed_v1","skin_npc_v1",False)
build("NPC_CIVILIAN_F1",True,"cloth_indigo_plain_v1","skin_npc_v1",True)
