#!/usr/bin/env python3
"""Reproducible bounded raster attempts, never original-file edits.

Run with Pillow+NumPy installed. The generated E46 patch is an explicitly
non-deterministic input whose SHA-256 is recorded. All compositing after that
input is deterministic. No source or documentary history is overwritten.
"""
from pathlib import Path
import hashlib, json, math, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / '_final_release_stage'
OUT = ROOT / 'OUR_EYES_CD_FINAL_VERDICTS_v1'
RASTERS = OUT / 'corrections'
EVIDENCE = OUT / 'correction_evidence'
for p in (RASTERS, EVIDENCE): p.mkdir(parents=True, exist_ok=True)
SCOPE = {x['code']: x for x in json.loads((OUT/'verification/SOURCE_SCOPE_193.json').read_text())}
RESULTS = []
ART_BOX = (60,130,1930,1310)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(code):
    r = SCOPE[code]
    p = ROOT/'google_drive'/r['name']
    assert sha(p) == r['source_sha256'], f'Changed source {code}'
    im = Image.open(p).convert('RGB'); im.load()
    return p, im


def font(size=20, bold=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)


def record(code, src_path, before, after, name, method, allowed_mask, params, art_only_mask=None, inputs=None):
    assert before.size == after.size
    a,b = np.asarray(before),np.asarray(after)
    changed = np.any(a!=b,axis=2)
    allow = np.asarray(allowed_mask)>0
    assert not np.any(changed & ~allow), f'Out-of-mask changes {code}'
    ys,xs = np.where(changed)
    bbox = [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None
    dest = RASTERS/name
    after.save(dest,format='PNG',compress_level=9)
    with Image.open(dest) as im: assert np.array_equal(np.asarray(im.convert('RGB')),b)
    mask_path = EVIDENCE/f'{code}_allowed_mask.png'; allowed_mask.save(mask_path)
    diff_im=Image.fromarray((changed.astype(np.uint8)*255),'L')
    diff_path=EVIDENCE/f'{code}_actual_difference.png'; diff_im.save(diff_path)
    row = {'source_code':code,'source_id':SCOPE[code]['source_id'],'source_name':SCOPE[code]['name'],
           'source_sha256':sha(src_path),'output_name':name,'output_path':str(dest.relative_to(ROOT)),
           'output_sha256':sha(dest),'output_md5':hashlib.md5(dest.read_bytes()).hexdigest(),
           'output_bytes':dest.stat().st_size,'dimensions':list(before.size),'method':method,
           'parameters':params,'additional_inputs':inputs or [],'difference_bbox':bbox,
           'changed_pixels':int(changed.sum()),'out_of_mask_changed_pixels':0,
           'outside_mask_original_RGB_identical':True,'geometry_resampling_or_warp':False,
           'allowed_mask_path':str(mask_path.relative_to(ROOT)),
           'actual_difference_path':str(diff_path.relative_to(ROOT)),
           'completion_state':'GENERATED_AND_PIXEL_TESTED_AWAITING_CD_VISUAL_DECISION',
           'cd_visual_decision':None,'new_drive_id':None,'original_preserved':sha(src_path)==SCOPE[code]['source_sha256']}
    if art_only_mask is not None:
        art_allow=np.asarray(art_only_mask)>0
        art_changed=changed[130:1310,60:1930]
        assert not np.any(art_changed & ~art_allow[130:1310,60:1930])
        yy,xx=np.where(art_changed)
        row['changed_art_pixels']=int(art_changed.sum())
        row['art_difference_bbox']=[int(xx.min()+60),int(yy.min()+130),int(xx.max()+61),int(yy.max()+131)] if len(xx) else None
        row['art_outside_cord_mask_RGB_identical']=True
    RESULTS.append(row)
    return row


def draw_braid(im, paths):
    # Antialiased geometric cord strokes only. Coordinates are this newly
    # authorised correction's native mask, NOT withdrawn weapon/fit guides.
    scale=4
    box=(1035,385,1100,464)
    patch=im.crop(box)
    hi=patch.resize((patch.width*scale,patch.height*scale),Image.Resampling.NEAREST)
    mask=Image.new('L',hi.size,0)
    d=ImageDraw.Draw(hi);md=ImageDraw.Draw(mask)
    for points in paths:
        ps=[((x-box[0])*scale,(y-box[1])*scale) for x,y in points]
        d.line(ps,fill=(57,43,34),width=9,joint='curve')
        md.line(ps,fill=255,width=14,joint='curve')
        # Fine alternating diagonal fibres avoid a smooth flat strap read.
        for (x0,y0),(x1,y1) in zip(ps,ps[1:]):
            le=math.hypot(x1-x0,y1-y0)
            count=max(2,int(le/7))
            nx,ny=(-(y1-y0)/le,(x1-x0)/le) if le else (1,0)
            for k in range(count):
                t=k/count
                x=x0+(x1-x0)*t;y=y0+(y1-y0)*t
                col=(104,85,66) if k%2 else (84,68,52)
                d.line((x-2.3*nx,y-2.3*ny,x+2.3*nx+1,y+2.3*ny+2),fill=col,width=2)
    lo=hi.resize(patch.size,Image.Resampling.LANCZOS)
    ma=mask.resize(patch.size,Image.Resampling.LANCZOS)
    # Quantise a finite support; no sub-threshold mask pixels outside it.
    ma=ma.point(lambda x:0 if x<3 else x)
    out=im.copy();out.paste(lo,box[:2],ma)
    full=Image.new('L',im.size,0);full.paste(ma,box[:2])
    return out,full


def accurate_chrome(im, code):
    out=im.copy();d=ImageDraw.Draw(out);bg=(9,13,23);fg=(224,219,204);gold=(170,148,101)
    d.rectangle((1950,130,2559,1309),fill=bg)
    y=155
    blocks=[('DERIVATIVE / V005',True),
            (SCOPE[code]['name'].split('_V004_')[0].replace('B2_CAND_',''),False),
            ('CORD-ONLY CONCEPT CORRECTION',True),
            ('New local braided-cord treatment from exact V004. Original and all predecessors retained unchanged.',False),
            ('PRESERVATION',True),
            ('Native 2560 x 1440; no resize or warp. Figure-art pixels outside the disclosed cord mask are RGB-identical to V004. Geometry, pose, alignment, scale, likeness, braids, costume, pendant and baldric are unchanged.',False),
            ('LIMITED USE',True),
            ('Internal character concept study only. NOT a full-turnaround approval; NOT production or canon. Exact final verdict is in the accompanying register.',False),
            ('OPEN CONTROLS',True),
            ('CQ-9 weapon / fit, RQ-10-1 armlet, U-11 fictional ornament and applicable textile/material qualifications remain. No blade added. LEFT_SIDE and BACK stay V003 / PRESERVE / UNAPPROVED.',False),
            ('PROVENANCE',True),
            (f"Source {code}: {SCOPE[code]['source_id']}. Cord paths, mask, changed-pixel proof and exact source/output hashes are filed in correction_evidence.",False)]
    for text,bold in blocks:
        f=font(22 if bold else 20,bold)
        for line in textwrap.wrap(text,43 if bold else 49):
            d.text((1970,y),line,font=f,fill=gold if bold else fg);y+=29
        y+=17
    d.rectangle((0,1311,2559,1439),fill=bg)
    d.text((60,1330),'V005  |  CORD-ONLY DERIVATIVE  |  INTERNAL CONCEPT STUDY - NOT PRODUCTION / CANON',font=font(22,True),fill=gold)
    d.text((60,1367),'Exact V004 original preserved. No side/back increment. Source and pixel-mask audit accompany this derivative.',font=font(19),fill=fg)
    d.text((60,1397),'No cultural authentication, weapon-scale or full-turnaround clearance. Geometry/pose/likeness unchanged outside cord mask.',font=font(18),fill=(145,150,160))
    return out

# D03 / D06. The existing pendant itself is excluded from the cord masks.
for code,paths in [('D03',[[(1051.0,399.5),(1055.0,418.0),(1060.0,440.0),(1063.0,458.0)],[(1074.5,399.5),(1071.0,419.0),(1067.2,439.0),(1064.4,458.0)]]),
                   ('D06',[[(1069.0,402.0),(1070.0,418.0),(1069.0,431.0),(1070.0,438.0),(1073.8,442.5)],[(1084.0,402.0),(1082.0,419.0),(1078.5,432.0),(1072.4,439.0),(1073.8,442.5)]])]:
    src,im=load(code)
    corrected,cord=draw_braid(im,paths)
    corrected=accurate_chrome(corrected,code)
    allowed=cord.copy();ad=ImageDraw.Draw(allowed);ad.rectangle((1950,130,2559,1309),fill=255);ad.rectangle((0,1311,2559,1439),fill=255)
    name=SCOPE[code]['name'].replace('_V004_','_V005_')
    record(code,src,im,corrected,name,'Native cord-only antialiased braid strokes plus accurate documentary-margin chrome',allowed,{'cord_paths':paths,'cord_patch_box':[1035,385,1100,464],'chrome_rectangles':[[1950,130,2560,1310],[0,1311,2560,1440]],'source_art_box':list(ART_BOX),'supersampling':4},cord)
    corrected.crop((1015,355,1120,490)).resize((420,540),Image.Resampling.NEAREST).save(EVIDENCE/f'{code}_corrected_cord_inspection.png')

# E46: one local generative patch; compositing mask contains the new wood and
# its contact shadow only. All original room/stone/pot pixels outside survive.
src,im=load('E46')
patch_path=EVIDENCE/'E46_firewood_patch_generated.png'
box=(300,430,690,800)
p=Image.open(patch_path).convert('RGB').resize((390,370),Image.Resampling.LANCZOS)
mask=Image.new('L',(390,370),0)
poly=[(170,172),(231,155),(279,162),(375,185),(382,254),(363,281),(318,302),(222,307),(166,294)]
ImageDraw.Draw(mask).polygon(poly,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(4))
mask=mask.point(lambda x:0 if x<2 else x)
out=im.copy();out.paste(p,box[:2],mask)
full=Image.new('L',im.size,0);full.paste(mask,box[:2])
record('E46',src,im,out,'ENV_CH03-INT-004_THE_FORGOTTEN_KITCHEN_V003.png','AI-generated local firewood patch, then deterministic finite-mask composite',full,{'crop_box':list(box),'patch_polygon_crop_coordinates':poly,'feather_radius':4,'mask_threshold':2,'patch_resized_to':[390,370],'source_native_resampled':False},inputs=[{'path':str(patch_path.relative_to(ROOT)),'sha256':sha(patch_path),'role':'New generated wood-patch input; not recovered historical artwork'}])

# E50: native translated clone of blank ash to remove ambiguous far terminal
# prints. Last complete foreground footprints and all walls are unchanged.
src,im=load('E50');w,h=im.size
poly=[(708,512),(821,512),(833,589),(797,611),(716,608)]
mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(poly,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(3)).point(lambda x:0 if x<2 else x)
a=np.asarray(im).copy();donor=a.copy();donor[:,:w-100]=a[:,100:]
# This is a disclosed source-native clone, not an invention of new texture.
out=Image.composite(Image.fromarray(donor),im,mask)
record('E50',src,im,out,'ENV_CH03-TRV-003_THE_NARROW_PASSAGES_V003.png','Native blank-ash translated clone confined to far-end footprint mask',mask,{'polygon':poly,'donor_offset_xy':[100,0],'feather_radius':3,'mask_threshold':2,'wall_repaint':False,'weather_reinterpretation':False})
out.crop((650,470,950,730)).save(EVIDENCE/'E50_corrected_endpoint_inspection.png')

# E53 / E54: pure native-coordinate 2D concept grades. No geometry may change.
for code,name in [('E53','ENV_CH04-INT-003_THE_CANOE_SHED_V003.png'),('E54','ENV_CH04-SET-002_THE_TWO_HOUSE_LANDING_V003.png')]:
    src,im=load(code)
    a=np.asarray(im).astype(np.float32)/255.0
    gain=np.array([0.91,0.99,1.15],dtype=np.float32)
    a=np.clip(a*gain,0,1)
    lum=np.sum(a*np.array([.2126,.7152,.0722]),axis=2)
    low=np.asarray(Image.fromarray(np.uint8(np.clip(lum*255,0,255))).filter(ImageFilter.GaussianBlur(64))).astype(np.float32)/255
    field=np.clip((max(float(lum.mean()),.01)/np.maximum(low,.04))**.20,.82,1.27)
    a=a*field[:,:,None]
    grey=np.sum(a*np.array([.2126,.7152,.0722]),axis=2,keepdims=True)
    a=grey+(a-grey)*.73
    a=np.clip(a,0,1)**.92
    a=np.clip((a-.42)*.91+.42,0,1)
    out=Image.fromarray(np.uint8(np.round(a*255)),'RGB')
    mask=Image.new('L',im.size,255)
    record(code,src,im,out,name,'Deterministic whole-frame native-coordinate silver-overcast concept grade; not physical relighting',mask,{'rgb_gain':gain.tolist(),'gaussian_illumination_radius':64,'illumination_exponent':.20,'field_limits':[.82,1.27],'chroma_scale':.73,'gamma':.92,'contrast':.91,'pivot':.42,'added_objects':0,'resampling':False,'physical_albedo_or_lighting_reconstruction':False})

# Do not overwrite the separately adjudicated/published execution ledger.
(EVIDENCE/'CORRECTION_GENERATION.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['source_code','output_name','changed_pixels','difference_bbox','outside_mask_original_RGB_identical','completion_state']} for r in RESULTS],indent=2))
