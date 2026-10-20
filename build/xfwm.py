# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""Generates the PNG pieces of the windows-dez xfwm4 theme.
Usage: python3 xfwm.py OUTPUT_DIR [--dark]
       --dark  dark title bars, for the windows-dez-dark (full dark mode) theme"""
import os, sys
from PIL import Image, ImageDraw

OUT = sys.argv[1]
DARK = "--dark" in sys.argv[2:]
os.makedirs(OUT, exist_ok=True)

H = 30          # title bar height
BW = 46         # button width
SIDE = 4        # espessura das bordas laterais/inferior
ACC = (0, 120, 215, 255)       # borda da janela ativa
INA = (170, 170, 170, 255)     # borda da janela inativa
WHITE = (255, 255, 255, 255)
BAR_A = BAR_I = WHITE          # title bar background (active / inactive)
if DARK:
    INA = (85, 85, 85, 255)
    BAR_A = (32, 32, 32, 255)      # #202020
    BAR_I = (43, 43, 43, 255)      # #2B2B2B

def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))

# ---------- title bar and borders ----------
for state, border, WHITE in (("active", ACC, BAR_A), ("inactive", INA, BAR_I)):
    # title pieces: 1px border on top, white below
    t = Image.new("RGBA", (1, H), WHITE)
    t.putpixel((0, 0), border)
    for i in range(1, 6):
        save(t, f"title-{i}-{state}")
    # top corners
    for side in ("left", "right"):
        c = Image.new("RGBA", (SIDE, H), WHITE)
        d = ImageDraw.Draw(c)
        d.line([(0, 0), (SIDE - 1, 0)], fill=border)
        x = 0 if side == "left" else SIDE - 1
        d.line([(x, 0), (x, H - 1)], fill=border)
        save(c, f"top-{side}-{state}")
    # sides
    for side in ("left", "right"):
        s = Image.new("RGBA", (SIDE, 1), WHITE)
        s.putpixel((0 if side == "left" else SIDE - 1, 0), border)
        save(s, f"{side}-{state}")
    # bottom
    b = Image.new("RGBA", (1, SIDE), WHITE)
    b.putpixel((0, SIDE - 1), border)
    save(b, f"bottom-{state}")
    for side in ("left", "right"):
        c = Image.new("RGBA", (SIDE, SIDE), WHITE)
        d = ImageDraw.Draw(c)
        d.line([(0, SIDE - 1), (SIDE - 1, SIDE - 1)], fill=border)
        x = 0 if side == "left" else SIDE - 1
        d.line([(x, 0), (x, SIDE - 1)], fill=border)
        save(c, f"bottom-{side}-{state}")

# ---------- button glyphs ----------
S = 4  # supersampling para linhas diagonais suaves

def glyph(kind, color):
    g = Image.new("RGBA", (10 * S, 10 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    w = S  # 1px
    if kind == "close":
        d.line([(0, 0), (10 * S - 1, 10 * S - 1)], fill=color, width=int(w * 1.15))
        d.line([(0, 10 * S - 1), (10 * S - 1, 0)], fill=color, width=int(w * 1.15))
    elif kind == "maximize":
        d.rectangle([0, 0, 10 * S - 1, 10 * S - 1], outline=color, width=w)
    elif kind == "maximize-toggled":
        d.rectangle([0, 2 * S, 8 * S - 1, 10 * S - 1], outline=color, width=w)
        d.line([(2 * S, 2 * S), (2 * S, 0), (10 * S - 1, 0), (10 * S - 1, 8 * S - 1), (8 * S, 8 * S - 1)], fill=color, width=w)
    elif kind == "hide":
        d.rectangle([0, 5 * S, 10 * S - 1, 6 * S - 1], fill=color)
    elif kind in ("shade", "shade-toggled"):
        pts = [(1 * S, 7 * S), (5 * S, 3 * S), (9 * S, 7 * S)]
        if kind == "shade-toggled":
            pts = [(1 * S, 3 * S), (5 * S, 7 * S), (9 * S, 3 * S)]
        d.line(pts, fill=color, width=w)
    elif kind in ("stick", "stick-toggled"):
        if kind == "stick-toggled":
            d.ellipse([2 * S, 2 * S, 8 * S - 1, 8 * S - 1], fill=color)
        else:
            d.ellipse([2 * S, 2 * S, 8 * S - 1, 8 * S - 1], outline=color, width=w)
    return g.resize((10, 10), Image.LANCZOS)

def button(kind, bg, fg):
    img = Image.new("RGBA", (BW, H), bg)
    if kind == "menu":
        return img  # xfwm4 draws the app icon on top
    gl = glyph(kind, fg)
    img.alpha_composite(gl, ((BW - 10) // 2, (H - 10) // 2 + 0))
    # top border line (continues the title bar)
    return img

def with_top(img, border):
    d = ImageDraw.Draw(img)
    d.line([(0, 0), (img.width - 1, 0)], fill=border)
    return img

BLACK = (0, 0, 0, 255)
GREY = (153, 153, 153, 255)
HOV = (229, 229, 229, 255)
PRS = (202, 202, 202, 255)
RED = (232, 17, 35, 255)
RED2 = (241, 112, 122, 255)
WHITE = (255, 255, 255, 255)
if DARK:
    GREY = (138, 138, 138, 255)
    HOV = (51, 51, 51, 255)
    PRS = (77, 77, 77, 255)
FG_A = WHITE if DARK else BLACK

kinds = ["close", "maximize", "maximize-toggled", "hide", "shade",
         "shade-toggled", "stick", "stick-toggled", "menu"]
for k in kinds:
    w = 30 if k == "menu" else BW
    hov, prs, fg_h = (RED, RED2, WHITE) if k == "close" else (HOV, PRS, FG_A)
    variants = {
        "active":   (BAR_A, FG_A, ACC),
        "inactive": (BAR_I, GREY, INA),
        "prelight": (hov, fg_h, ACC),
        "pressed":  (prs, fg_h, ACC),
    }
    for st, (bg, fg, border) in variants.items():
        if k == "menu":
            img = Image.new("RGBA", (w, H), BAR_I if st == "inactive" else BAR_A)
        else:
            img = button(k, bg, fg)
        save(with_top(img, border), f"{k}-{st}")

# ---------- themerc ----------
if DARK:
    head = """# windows-dez-dark — xfwm4 (full dark mode)
active_text_color=#FFFFFF
inactive_text_color=#8A8A8A
active_text_shadow_color=#202020
inactive_text_shadow_color=#2B2B2B
"""
else:
    head = """# windows-dez — xfwm4
active_text_color=#000000
inactive_text_color=#999999
active_text_shadow_color=#FFFFFF
inactive_text_shadow_color=#FFFFFF
"""
with open(os.path.join(OUT, "themerc"), "w") as f:
    f.write("""# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
""" + head + """title_shadow_active=false
title_shadow_inactive=false
title_alignment=left
full_width_title=true
title_horizontal_offset=6
title_vertical_offset_active=1
title_vertical_offset_inactive=1
button_layout=O|HMC
button_spacing=0
button_offset=0
maximized_offset=0
show_app_icon=true
shadow_delta_height=2
shadow_delta_width=0
shadow_delta_x=0
shadow_delta_y=-2
shadow_opacity=40
""")
print("xfwm4 ok:", len(os.listdir(OUT)), "files")
