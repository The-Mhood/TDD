#!/usr/bin/env python3
"""Adanna AD-03 procedural texture set v1 (2026-11-20) - deterministic, seeded, license-clean.
PRODUCTION-TARGET BASES, NOT final art: TD must ratify texel density/values on first import.
Maps: BaseColor (sRGB) + Roughness (linear). No baked lighting. Palette per FP-01."""
from PIL import Image, ImageDraw, ImageFilter
import random, math, os, json

OUT = os.path.dirname(os.path.abspath(__file__))
S = 2048
random.seed(20261120)

def noise(size, sigma):
    return Image.effect_noise((size, size), sigma)

def blend(a, b, opacity):
    b2 = b.convert('RGB') if b.mode != 'RGB' else b
    return Image.blend(a, b2, opacity)

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p)
    print('wrote', name, img.size)

# ---------- 1. INDIGO HAND-WOVEN CLOTH (bandeau / wrap / sash family) ----------
def indigo_cloth():
    tile = 96
    t = Image.new('RGB', (tile, tile), (43, 56, 88))      # deep hand-dyed indigo
    d = ImageDraw.Draw(t)
    for y in range(0, tile, 6):                            # weft rows with slub variance
        tone = random.randint(-16, 14)
        d.rectangle([0, y, tile, y + 5], fill=(min(255, 43 + tone + 8), min(255, 56 + tone + 8), min(255, 88 + tone + 10)))
        d.line([0, y, tile, y], fill=(24, 32, 52), width=1)
    for x in range(0, tile, 6):                            # warp threads with stagger
        tone = random.randint(-10, 10)
        offset = 3 if (x // 6) % 2 == 0 else 0
        d.line([x, offset, x, tile], fill=(max(0, 43 + tone), max(0, 56 + tone), max(0, 88 + tone)), width=2)
    for _ in range(10):                                    # thicker warp accents, aged handloom irregularity
        x = random.randrange(0, tile, 4)
        tone = random.randint(-18, 22)
        d.line([x, 0, x, tile], fill=(max(0, 43 + tone), max(0, 56 + tone), max(0, 88 + tone)), width=3)
    for _ in range(14):                                    # slubs
        y = random.randrange(0, tile, 6)
        col = random.choice([(58, 74, 108), (30, 40, 64), (66, 84, 120)])
        d.rectangle([0, y, tile, y + 2], fill=col)
    img = t.resize((S, S), Image.NEAREST)
    macro = noise(S, 46).filter(ImageFilter.GaussianBlur(240))     # large-scale dye pooling
    img = blend(img, Image.merge('RGB', (macro, macro, macro)), 0.18)
    fine = noise(S, 12).filter(ImageFilter.GaussianBlur(1.2))       # fibre noise
    img = blend(img, Image.merge('RGB', (fine, fine, fine)), 0.10)
    rough = blend(Image.new('RGB', (S, S), (218, 218, 218)),
                  Image.merge('RGB', (noise(S, 18),) * 3), 0.22)
    return img, rough

# ---------- 2. VEGETABLE-TANNED LEATHER (baldric / straps, worn) ----------
def leather():
    base = Image.new('RGB', (S, S), (122, 84, 48))          # veg-tan mid brown
    grain = noise(S, 22).filter(ImageFilter.GaussianBlur(1.6))
    base = blend(base, Image.merge('RGB', (grain, grain, grain)), 0.28)
    d = ImageDraw.Draw(base, 'RGBA')
    for _ in range(46):                                    # long grain creases
        y = random.randrange(S); amp = random.uniform(2, 9); ph = random.uniform(0, 6.28)
        pts = [(x, y + amp * math.sin(x * 0.011 + ph)) for x in range(0, S + 8, 8)]
        d.line(pts, fill=(70, 46, 24, 70), width=random.randint(2, 5))
    for _ in range(22):                                    # scuff patches
        cx, cy = random.randrange(S), random.randrange(S); r = random.uniform(14, 60)
        d.ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], fill=(158, 118, 74, 60))
    base = base.filter(ImageFilter.GaussianBlur(0.6))
    worn = blend(base, Image.new('RGB', (S, S), (150, 112, 66)), 0.16)
    rough = blend(Image.new('RGB', (S, S), (150, 150, 150)),
                  Image.merge('RGB', (noise(S, 20),) * 3), 0.30)
    rough_worn = blend(rough, Image.new('RGB', (S, S), (120, 120, 120)), 0.25)
    return base, worn, rough, rough_worn

# ---------- 3. AGED CAST BRONZE (coiled armlet / pendant / cuffs) ----------
def bronze():
    base = Image.new('RGB', (S, S), (120, 92, 46))           # aged bronze, not gold
    brush = noise(S, 8)
    brush = brush.resize((S, S // 16), Image.BILINEAR).resize((S, S), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.8))
    base = blend(base, Image.merge('RGB', (brush, brush, brush)), 0.24)
    d = ImageDraw.Draw(base, 'RGBA')
    for _ in range(34):                                    # patina pools
        cx, cy = random.randrange(S), random.randrange(S); r = random.uniform(18, 90)
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(74, 96, 66, 84))
    base = base.filter(ImageFilter.GaussianBlur(2.0))
    d = ImageDraw.Draw(base, 'RGBA')
    for i, r in enumerate(range(120, 1400, 34)):           # faint concentric tooling marks
        alpha = 26 if i % 2 == 0 else 14
        d.ellipse([S // 2 - r, S // 2 - r, S // 2 + r, S // 2 + r], outline=(210, 178, 96, alpha), width=2)
    base = base.filter(ImageFilter.GaussianBlur(0.7))
    rough = blend(Image.new('RGB', (S, S), (110, 110, 110)),
                  Image.merge('RGB', (noise(S, 26),) * 3), 0.35)
    return base, rough

if __name__ == '__main__':
    ic_bc, ic_r = indigo_cloth()
    save(ic_bc, 'T_ADANNA_IndigoCloth_BC_2048.png')
    save(ic_r, 'T_ADANNA_IndigoCloth_R_2048.png')
    bc, worn, r, rw = leather()
    save(bc, 'T_ADANNA_VegetLeather_BC_2048.png')
    save(worn, 'T_ADANNA_VegetLeather_BC_worn_2048.png')
    save(r, 'T_ADANNA_VegetLeather_R_2048.png')
    save(rw, 'T_ADANNA_VegetLeather_R_worn_2048.png')
    b3, r3 = bronze()
    save(b3, 'T_ADANNA_Bronze_BC_2048.png')
    save(r3, 'T_ADANNA_Bronze_R_2048.png')
    sheet = Image.new('RGB', ((S // 2) * 4, (S // 2) * 2 + 40), (18, 18, 20))
    names = ['T_ADANNA_IndigoCloth_BC_2048.png', 'T_ADANNA_VegetLeather_BC_2048.png',
             'T_ADANNA_VegetLeather_BC_worn_2048.png', 'T_ADANNA_Bronze_BC_2048.png',
             'T_ADANNA_IndigoCloth_R_2048.png', 'T_ADANNA_VegetLeather_R_worn_2048.png',
             'T_ADANNA_Bronze_R_2048.png']
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).resize((S // 2, S // 2))
        sheet.paste(im, ((i % 4) * (S // 2), (i // 4) * (S // 2)))
    sheet.save(os.path.join(OUT, 'ADANNA_TEXSET_PREVIEW.png'))
    print('preview written')
    manifest = {
        'set': 'ADANNA_TEXSET_V1_PROCEDURAL',
        'date': '2026-11-20',
        'status': 'PRODUCTION-TARGET BASES v1 - NOT final art; TD ratifies on import (texel density, values). CQ-9 unaffected.',
        'authority': 'AD-03 (owner 2026-11-20: TD/CD may approve pipeline); palette FP-01; plain-textile-only respected (no emblems of cultural specificity); pendant/armlet FICTIONAL tags preserved',
        'files': [
            {'file': 'T_ADANNA_IndigoCloth_BC_2048.png', 'map': 'BaseColor', 'space': 'sRGB', 'use': 'bandeau, wrap skirt, sash', 'size': 2048},
            {'file': 'T_ADANNA_IndigoCloth_R_2048.png', 'map': 'Roughness', 'space': 'linear', 'use': 'cloth roughness (high, variable)', 'size': 2048},
            {'file': 'T_ADANNA_VegetLeather_BC_2048.png', 'map': 'BaseColor', 'space': 'sRGB', 'use': 'baldric strap, belt wraps', 'size': 2048},
            {'file': 'T_ADANNA_VegetLeather_BC_worn_2048.png', 'map': 'BaseColor', 'space': 'sRGB', 'use': 'baldric, contact-worn variant', 'size': 2048},
            {'file': 'T_ADANNA_VegetLeather_R_2048.png', 'map': 'Roughness', 'space': 'linear', 'use': 'leather roughness', 'size': 2048},
            {'file': 'T_ADANNA_VegetLeather_R_worn_2048.png', 'map': 'Roughness', 'space': 'linear', 'use': 'leather roughness, worn/contact zones', 'size': 2048},
            {'file': 'T_ADANNA_Bronze_BC_2048.png', 'map': 'BaseColor', 'space': 'sRGB', 'use': 'coiled armlet, spiral pendant (FICTIONAL), temple cuffs', 'size': 2048},
            {'file': 'T_ADANNA_Bronze_R_2048.png', 'map': 'Roughness', 'space': 'linear', 'use': 'bronze roughness (brushed + patina variance)', 'size': 2048},
        ],
        'exclusions': ['skin (SSS authored in shader, not baked here)', 'hair (strand geo/alpha, later)', 'blade/scabbard (CQ-9)', 'any patterned textile (plain only)'],
        'generator': 'build_textures.py - deterministic seed 20261120; pure PIL; no external assets',
    }
    with open(os.path.join(OUT, 'ADANNA_MATERIAL_MANIFEST.json'), 'w') as f:
        json.dump(manifest, f, indent=2)
    print('manifest written')
