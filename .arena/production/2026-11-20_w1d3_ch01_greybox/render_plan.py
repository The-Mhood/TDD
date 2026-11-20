#!/usr/bin/env python3
"""CH01 greybox TOP-DOWN PLAN schematic (2D, engineering layout aid — NOT art).
Reads the same layout constants as build_ch01_greybox.py (kept data-identical).
Output: CH01_GREYBOX_PLAN.png"""
from PIL import Image, ImageDraw, ImageFont
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 9                 # px per metre
W, H = 150*S, 150*S   # matches 150x150 terrain block
OX, OY = W//2, H//2 - (-2*S)  # world (0,0) mapped; y inverted for screen
img = Image.new("RGB", (W, H), (246,244,238))
d = ImageDraw.Draw(img)
try:
    F  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    FB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
except Exception:
    F = FB = FS = None

def X(x): return OX + int(x*S)
def Y(y): return OY - int(y*S)
def rect(cx, cy, w, h, fill, outline=(60,55,50), wd=1, ang=0):
    pts = []
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for dx, dy in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]:
        rx, ry = dx*ca - dy*sa, dx*sa + dy*ca
        pts.append((X(cx+rx), Y(cy+ry)))
    d.polygon(pts, fill=fill, outline=outline)
def circ(cx, cy, r, fill, outline=(60,55,50)):
    x0, x1 = X(cx-r), X(cx+r); y0, y1 = Y(cy-r), Y(cy+r)
    d.ellipse([min(x0,x1), min(y0,y1), max(x0,x1), max(y0,y1)], fill=fill, outline=outline, width=1)
def txt(x, y, s, f=FS, anchor="mm", fill=(35,30,25)):
    d.text((X(x), Y(y)), s, font=f, anchor=anchor, fill=fill)

# terrain boundary + stream + roads
rect(0, -2, 150, 150, (236,233,224), outline=(120,116,105))
rect(18, -33, 70, 4.5, (158,182,205))
rect(52, 2, 22, 3.2, (178,168,151))
rect(23, 1.4, 46, 3.2, (178,168,151), ang=-2)
rect(9.5, -16, 3.0, 30, (178,168,151), ang=14)
rect(-10.5, 0, 21, 2.6, (188,178,160))
rect(39, 9, 16, 2.2, (178,168,151), ang=35)

# perimeter wall ring + gate (gap at east)
wall = (112,105,96)
for (x0,y0,x1,y1) in [(-46,-30,46,-30),(-46,28,46,28),(-46,-30,-46,28),(46,-30,46,1.0),(46,3.4,46,28)]:
    ang = math.degrees(math.atan2(y1-y0, x1-x0)); ln = math.hypot(x1-x0, y1-y0)
    rect((x0+x1)/2, (y0+y1)/2, ln, 0.35, wall, ang=ang)
rect(46, 1.0, 0.45, 0.45, (90,80,70)); rect(46, 3.4, 0.45, 0.45, (90,80,70))
rect(46, 1.7, 0.12, 1.4, (140,120,95)); rect(46, 2.7, 0.12, 1.4, (140,120,95))

# huts
huts = [("HUT_A_01",-12,14,4.2,3.1),("HUT_A_02",-22,12,4.0,3.0),("HUT_A_03",16,-24,4.6,3.4),
        ("HUT_B_01",28,-20,5.0,3.6),("HUT_A_04★",30,6,4.4,3.2),("HUT_A_05★",36,-7,4.0,3.0),
        ("HUT_C_01",-14,-14,2.4,2.0),("HUT_C_02",26,-9,2.4,2.0)]
for n,x,y,w,h in huts:
    rect(x, y, w, h, (206,186,142) if "★" not in n else (208,150,130))
    txt(x, y, n.split("\n")[0])
# interiors blockouts
for n,x,y,w,h in [("SMITHY",20,-8,4.5,3.4),("HEALER",-14,22,4.0,3.0),("WEAVER",-20,-6,4.0,3.0),
                  ("KITCHEN",-8,-18,4.2,3.2),("BACKROOMS",14,21,6.0,4.5)]:
    rect(x, y, w, h, (190,170,132)); txt(x, y, n)
rect(-28, 2, 5.0, 4.0, (196,138,120)); txt(-28, 2, "POTTER*")
# palace complex
rect(-30, 0, 16, 14, (186,178,168))
rect(-39, 0, 3.0, 6.5, (150,142,132)); txt(-39, 0, "PORTAL")
rect(-43.5, 0, 8.0, 10.0, (168,160,150)); txt(-43.5, 0, "THRONE HALL")
rect(-42, 0, 1.2, 1.0, (120,112,102))
for i in range(4):
    circ(-24.5-i*3.0,  7.6, 0.18, (150,142,132)); circ(-24.5-i*3.0, -7.6, 0.18, (150,142,132))
# market stalls
for r, y in enumerate([8.5, 12.5]):
    for c, x in enumerate([14, 17.5, 21]):
        rect(x, y, 2.0, 1.5, (206,186,120)); txt(x, y, f"S{r+1}{c+1}")
# square / tree / well / ekwe
circ(0, 0, 0.8, (96,140,70)); circ(0, 0, 3.6, (150,190,120))
txt(0, 5.4, "TREE_SHD")
circ(-8, 4, 0.55, (140,140,150)); txt(-8, 2.6, "WELL")
circ(6.5, -3.5, 0.18, (120,90,60)); txt(6.5, -5.2, "EKWE?")
# farms + pens + compound wall + gate shelter
for n,x,y in [("FARM_01",-60,12),("FARM_02",-62,-4),("FARM_03",-58,-19)]:
    rect(x, y, 7, 6, (205,200,150)); txt(x, y, n)
rect(12, -17, 8, 8, (214,206,190)); txt(12, -17, "PEN")
rect(28.5, -23, 31, 0.32, (112,105,96))
rect(43, 6, 2.2, 1.8, (208,150,130)); txt(43, 6, "RG-SHEL*")

# anchors
anchors = [("SPAWN",54,2,(200,60,60)),("GATE_TRG",46,2.2,(200,140,40)),("PAT_A",42,2.2,(60,60,200)),
           ("PAT_B",18,2.0,(60,60,200)),("PAT_C",2.5,-1.0,(60,60,200)),("PAT_D",8,2.0,(60,60,200)),
           ("BRM_D1",15,18.8,(140,60,180)),("BRM_D2",20,18.8,(140,60,180)),("PAL_APR",-16,0,(200,90,160)),
           ("THR_APR",-37,0,(200,90,160)),("EKWE",6.5,-3.5,(150,90,40)),("FARM_L23",56,2,(90,90,90)),
           ("DOCK_N",12,-30.5,(40,110,160)),("DOCK_S",26,-35.5,(40,110,160))]
for n,x,y,c in anchors:
    d.ellipse([X(x)-5, Y(y)-5, X(x)+5, Y(y)+5], outline=c, width=2)
    txt(x, y+1.6, n, FS, anchor="ma", fill=c)

# frame, title, legend
d.rectangle([4,4,W-4,34], fill=(24,22,20))
txt(6, 12, "CH01 GREYBOX PLAN — PROVISIONAL PLAYABLE LAYOUT", FB, anchor="lm", fill=(240,236,225))
txt(6, 27, "engineering layout aid — NOT art · NOT canon", FS, anchor="lm", fill=(200,196,185))
txt(6, H-26, "★ / POTTER* / RG-SHEL* = PROPOSED subject (ruling pending)", FS, anchor="lm", fill=(70,65,58))
txt(6, H-12, "grid 10 m · tree F3-gated · ekwe F1/F2-gated · regalia excluded", FS, anchor="lm", fill=(70,65,58))
for gx in range(-70, 91, 10):
    d.line([(X(gx), Y(-38)), (X(gx), Y(36))], fill=(220,217,208), width=1)
    d.line([(X(-48), Y(gx*0.6)), (X(48), Y(gx*0.6))], fill=(220,217,208), width=1)
img.save(os.path.join(HERE, "CH01_GREYBOX_PLAN.png"))
print("saved CH01_GREYBOX_PLAN.png", img.size)
