# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""windows-dez default wallpaper "Glass": four translucent glass diamonds (the
theme's Start button glyph) glowing on the right of a cyan → royal-blue
gradient. Original artwork, GPL-3.0-or-later.
Usage: python3 wallpaper.py OUTPUT_DIR"""
import cairosvg, io, sys
from PIL import Image, ImageEnhance

SATURATION = 0.87  # 1.0 = full colors

DEFS = '''<linearGradient id="bg" x1="0" y1="0.7" x2="1" y2="0.3">
 <stop offset="0" stop-color="#00B4F4"/><stop offset="0.5" stop-color="#0090E8"/>
 <stop offset="0.85" stop-color="#0560D2"/><stop offset="1" stop-color="#0741AE"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
 <stop offset="0" stop-color="#A8EAFF" stop-opacity="0.75"/><stop offset="1" stop-color="#00A2F0" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.50"/><stop offset="0.55" stop-color="#CFF2FF" stop-opacity="0.22"/>
 <stop offset="1" stop-color="#9FDFFF" stop-opacity="0.12"/></linearGradient>
<filter id="b40"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="b12"><feGaussianBlur stdDeviation="12"/></filter>'''

CX, CY, H, GAP = 1400, 520, 118, 22   # cluster center, diamond half-diagonal, gap


def diamond(cx, cy, h):
    return f"M{cx:.1f} {cy-h:.1f}L{cx+h:.1f} {cy:.1f}L{cx:.1f} {cy+h:.1f}L{cx-h:.1f} {cy:.1f}Z"


def cluster():
    o = H + GAP / 1.414
    return [(CX, CY - o), (CX - o, CY), (CX + o, CY), (CX, CY + o)]


body = f'<ellipse cx="{CX}" cy="{CY}" rx="600" ry="470" fill="url(#glow)" filter="url(#b40)"/>'
body += "".join(f'<path d="{diamond(x, y, H)}" fill="#FFFFFF" fill-opacity="0.18" filter="url(#b12)"/>'
                for x, y in cluster())
body += "".join(f'<path d="{diamond(x, y, H)}" fill="url(#glass)" stroke="#E9FAFF" '
                f'stroke-opacity="0.9" stroke-width="2.2"/>' for x, y in cluster())

svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
       f'<defs>{DEFS}</defs><rect width="1920" height="1080" fill="url(#bg)"/>{body}</svg>')

for w, h in ((1920, 1080), (3840, 2160)):
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h)
    img = Image.open(io.BytesIO(png)).convert("RGB")
    # light grain to avoid gradient banding
    img = Image.blend(img, Image.effect_noise((w, h), 6).convert("RGB"), 0.02)
    img = ImageEnhance.Color(img).enhance(SATURATION)
    img.save(f"{sys.argv[1]}/windows-dez-glass-{w}x{h}.jpg", quality=92)
print("ok")
