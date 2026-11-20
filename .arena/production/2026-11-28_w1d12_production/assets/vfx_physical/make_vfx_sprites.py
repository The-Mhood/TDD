#!/usr/bin/env python3
"""Physical VFX sprite package V1 (2026-11-28) - production-ready source
sprites for the approved physical-effects direction (W1 D11 board).
Procedural PIL sprites, sRGB PNG with alpha, tile/loop-safe where noted.
Effects: dust puff flipbook (8f), mud debris burst (single + 4 variants),
rain streak tile (looping), ember set, smoke puff. NO supernatural effects.
Unreal: import as flipbook/subUV or particle sprites; params in VFX_PHYSICAL_SPEC_V1.json.
"""
import json, math, os, random
from PIL import Image, ImageDraw, ImageFilter
random.seed(11)
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"sprites"); os.makedirs(OUT,exist_ok=True)
def puff(size, cx, cy, r, col, n=260, spread=0.55):
    im=Image.new("RGBA",(size,size),(0,0,0,0)); d=ImageDraw.Draw(im)
    for _ in range(n):
        a=random.uniform(0,6.283); rr=r*math.sqrt(random.random())*spread
        x,y=cx+rr*math.cos(a), cy+rr*math.sin(a)*0.8
        rad=random.uniform(r*0.08,r*0.30); al=int(random.uniform(28,95))
        d.ellipse([x-rad,y-rad*0.8,x+rad,y+rad*0.8], fill=col+(al,))
    return im.filter(ImageFilter.GaussianBlur(size/64))
# dust flipbook 8 frames 128px: grows, rises slightly, fades
frames=[]
for i in range(8):
    t=i/7; im=puff(128,64,86-18*t,26+34*t,(176,138,96),n=300)
    alpha=im.getchannel("A").point(lambda a: int(a*(1.0-0.55*t)))
    im.putalpha(alpha); frames.append(im)
sheet=Image.new("RGBA",(128*8,128),(0,0,0,0))
for i,f in enumerate(frames): sheet.paste(f,(i*128,0))
sheet.save(f"{OUT}/VFX_DUST_PUFF_FLIPBOOK_8F.png")
# mud debris burst variants
for v in range(4):
    im=Image.new("RGBA",(256,256),(0,0,0,0)); d=ImageDraw.Draw(im)
    for _ in range(46):
        a=random.uniform(-2.6,-0.5); sp=random.uniform(28,105)
        x,y=60+sp*math.cos(a)*-1, 200+sp*math.sin(a)
        s=random.uniform(2,8); d.ellipse([x-s,y-s*0.7,x+s,y+s*0.7], fill=(112,74,46,random.randint(160,235)))
    im.filter(ImageFilter.GaussianBlur(0.6)).save(f"{OUT}/VFX_MUD_DEBRIS_V{v+1}.png")
# rain streak tile 128x256 (vertical loop)
im=Image.new("RGBA",(128,256),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(70):
    x=random.uniform(0,128); y=random.uniform(-20,256); L=random.uniform(14,34)
    d.line([x,y,x-2,y+L], fill=(190,210,225,random.randint(60,140)), width=1)
im.save(f"{OUT}/VFX_RAIN_STREAK_TILE.png")
# embers + smoke
im=Image.new("RGBA",(128,128),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(60):
    x,y=random.uniform(10,118),random.uniform(10,118); s=random.uniform(0.8,2.6)
    d.ellipse([x-s,y-s,x+s,y+s], fill=(255,random.randint(120,190),40,random.randint(140,255)))
im.filter(ImageFilter.GaussianBlur(0.8)).save(f"{OUT}/VFX_EMBER_SET.png")
puff(256,128,140,72,(120,118,112),n=340).save(f"{OUT}/VFX_SMOKE_PUFF.png")
spec={"package":"VFX-PHYSICAL","version":"1.0","date":"2026-11-28","direction":"physical only (approved W1 D11); no supernatural/ability effects",
 "effects":[
  {"name":"footstep_dust","sprite":"sprites/VFX_DUST_PUFF_FLIPBOOK_8F.png","type":"subUV flipbook 8f @12fps","colour":"dry earth tan (176,138,96)","unreal":"Niagara sprite renderer, soft particles, spawn on footstep events"},
  {"name":"mud_wall_impact","sprites":"sprites/VFX_MUD_DEBRIS_V1..V4.png","type":"burst sprites + dust puff reuse","colour":"clay brown (112,74,46)","unreal":"burst 12-20 sprites, gravity -3, life 0.4-0.8s + dust flipbook at contact"},
  {"name":"rain_on_thatch","sprite":"sprites/VFX_RAIN_STREAK_TILE.png","type":"looping streak tile","unreal":"GPU rain volume; splash = dust flipbook desaturated/shortened at eaves (TD tune)"},
  {"name":"cooking_fire_ambience","sprites":["sprites/VFX_EMBER_SET.png","sprites/VFX_SMOKE_PUFF.png"],"type":"ember points + smoke puffs","unreal":"ember rate 6/s rise 0.4 m/s; smoke rate 2/s, growth 2x, life 3s; point light flicker 8 Hz (TD)"}],
 "acceptance":"sprites are source art; final look requires Niagara assembly + in-engine check by TD/PM (not claimed here)"}
json.dump(spec, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"VFX_PHYSICAL_SPEC_V1.json"),"w"), indent=2)
print("sprites:", sorted(os.listdir(OUT)))
