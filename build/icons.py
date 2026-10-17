# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""Generates the windows-dez icon theme (scalable SVG, freedesktop names).
Usage: python3 icons.py OUTPUT_DIR"""
import os, sys

OUT = sys.argv[1]
B = "#0078D7"      # azul de destaque
LB = "#4CC2FF"     # azul claro
DB = "#005A9E"     # azul escuro
G = "#6E6E6E"

def svg(body, vb=48):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb}" height="{vb}" '
            f'viewBox="0 0 {vb} {vb}">{body}</svg>\n')

# --------------------------------------------------------------------------
# Small glyphs (drawn around 24,31 — the folder front)
# --------------------------------------------------------------------------
def g_doc(c=B):
    return (f'<path d="M19 24h7l4 4v10H19z" fill="#fff" stroke="{c}" stroke-width="1.2"/>'
            f'<path d="M21.5 31h6M21.5 33.5h6M21.5 36h4" stroke="{c}" stroke-width="1.1"/>')
def g_down(c=B):
    return (f'<path d="M24 23v10" stroke="{c}" stroke-width="2.4"/>'
            f'<path d="M18.5 28.5L24 34l5.5-5.5" fill="none" stroke="{c}" stroke-width="2.4"/>'
            f'<rect x="17" y="36.5" width="14" height="2.2" fill="{c}"/>')
def g_music(c="#E8590C"):
    return (f'<path d="M22 35V25l9-2v10" fill="none" stroke="{c}" stroke-width="1.8"/>'
            f'<ellipse cx="20" cy="35.2" rx="2.6" ry="2" fill="{c}"/>'
            f'<ellipse cx="29" cy="33.2" rx="2.6" ry="2" fill="{c}"/>')
def g_pic(c=B):
    return (f'<rect x="16.5" y="24" width="15" height="13" fill="#fff" stroke="{c}" stroke-width="1.2"/>'
            f'<path d="M17.5 36l4.5-5.5 3 3.5 2-2 3.5 4z" fill="{c}"/>'
            f'<circle cx="27.5" cy="27.6" r="1.6" fill="#FFB900"/>')
def g_video(c="#8E44AD"):
    return (f'<rect x="16" y="24.5" width="16" height="12" fill="{c}"/>'
            '<path d="M22 27.5v6l5-3z" fill="#fff"/>'
            + "".join(f'<rect x="{x}" y="25.3" width="1.4" height="1.4" fill="#fff"/><rect x="{x}" y="34.3" width="1.4" height="1.4" fill="#fff"/>'
                      for x in (17, 30)))
def g_desktop(c=B):
    return (f'<rect x="16" y="24" width="16" height="11" fill="{c}"/>'
            f'<rect x="17.2" y="25.2" width="13.6" height="8.6" fill="{LB}"/>'
            f'<path d="M21 38.5h6M24 35v3.5" stroke="{G}" stroke-width="1.6"/>')
def g_home(c=B):
    return (f'<path d="M24 23.5l-8.5 7.5h2.5v7.5h12V31h2.5z" fill="{c}"/>'
            '<rect x="22.2" y="33" width="3.6" height="5.5" fill="#fff"/>')
def g_tmpl(c=B):
    return (f'<rect x="18" y="24" width="12" height="14" fill="#fff" stroke="{c}" '
            'stroke-width="1.2" stroke-dasharray="2 1.5"/>')
def g_share(c=B):
    return (f'<circle cx="20.5" cy="27" r="2.6" fill="{c}"/><path d="M15.5 37a5 5 0 0 1 10 0z" fill="{c}"/>'
            f'<circle cx="28" cy="27.5" r="2.4" fill="{DB}"/><path d="M23.5 37a4.5 4.5 0 0 1 9 0z" fill="{DB}"/>')
def g_globe(c=B, cx=24, cy=31, r=7):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{LB}" stroke="{c}" stroke-width="1.3"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.45:.2f}" ry="{r}" fill="none" stroke="{c}" stroke-width="1.1"/>'
            f'<path d="M{cx-r} {cy}h{2*r}M{cx-r*0.85:.2f} {cy-r*0.5:.2f}h{1.7*r:.2f}M{cx-r*0.85:.2f} {cy+r*0.5:.2f}h{1.7*r:.2f}" '
            f'stroke="{c}" stroke-width="0.9"/>')
def g_bookmark(c=B):
    return f'<path d="M19 23.5h10v15l-5-4-5 4z" fill="{c}"/>'

# --------------------------------------------------------------------------
# Folders
# --------------------------------------------------------------------------
def folder(glyph="", open_=False, band=None):
    back = '<path d="M3 8.5h15.5l4 4H45v29.5H3z" fill="#E6AE34"/>'
    paper = ('<rect x="6" y="14.5" width="36" height="12" fill="#fff"/>'
             '<rect x="6" y="14.5" width="36" height="1" fill="#E5E5E5"/>')
    if open_:
        front = ('<path d="M7 19.5h40l-4 22.5H3z" fill="#FFD45F"/>'
                 '<path d="M7 19.5h40l-.2 1H6.8z" fill="#FFE8A3"/>')
    else:
        front = ('<rect x="3" y="18.5" width="42" height="23.5" fill="#FFD45F"/>'
                 '<rect x="3" y="18.5" width="42" height="1" fill="#FFE8A3"/>')
    b = f'<rect x="3" y="38" width="42" height="4" fill="{band}"/>' if band else ""
    return svg(back + paper + front + b + glyph)

# --------------------------------------------------------------------------
# Documents (file types)
# --------------------------------------------------------------------------
PAGE = ('<path d="M9.5 3.5h20l9 9v32h-29z" fill="#fff" stroke="#A6A6A6"/>'
        '<path d="M29.5 3.5v9h9" fill="#E9E9E9" stroke="#A6A6A6" stroke-linejoin="round"/>')

def page(inner=""):
    return svg(PAGE + inner)

def label(text, color, size=7.2):
    return (f'<rect x="4" y="30" width="27" height="11" fill="{color}"/>'
            f'<text x="17.5" y="38.2" font-family="Segoe UI,Noto Sans,DejaVu Sans,sans-serif" '
            f'font-weight="700" font-size="{size}" fill="#fff" text-anchor="middle">{text}</text>')

def lines(color="#8A8A8A", y0=17, n=6, x0=14, x1=33):
    return "".join(f'<path d="M{x0} {y0+i*3.6:.1f}H{x1 if i % 3 != 2 else x1-6}" stroke="{color}" stroke-width="1.4"/>'
                   for i in range(n))

# --------------------------------------------------------------------------
# Icon map: name -> (context, SVG content)
# --------------------------------------------------------------------------
I = {}

# Places
I["folder"] = ("places", folder())
I["folder-open"] = ("places", folder(open_=True))
# Home: the file-manager folder (blue base band) with the house raised above it
HOME_BAND = ('<rect x="3" y="36.4" width="42" height="4" fill="#0078D7"/>'
             '<rect x="3" y="36.4" width="42" height="1.1" fill="#4CC2FF"/>')
HOME_HOUSE = ('<g transform="translate(24 29.0) scale(0.8)">'
              '<path d="M0 -7.2l-7.8 6.9h2.3v7.1h11V-0.3h2.3z" fill="#0078D7"/>'
              '<rect x="-1.6" y="1.6" width="3.2" height="5.2" fill="#FFD45F"/></g>')
I["user-home"] = ("places", folder(HOME_HOUSE + HOME_BAND))
I["user-desktop"] = ("places", folder(g_desktop()))
I["folder-documents"] = ("places", folder(g_doc()))
I["folder-download"] = ("places", folder(g_down()))
I["folder-music"] = ("places", folder(g_music()))
I["folder-pictures"] = ("places", folder(g_pic()))
I["folder-videos"] = ("places", folder(g_video()))
I["folder-templates"] = ("places", folder(g_tmpl()))
I["folder-publicshare"] = ("places", folder(g_share()))
I["folder-remote"] = ("places", folder(g_globe()))
I["user-bookmarks"] = ("places", folder(g_bookmark()))
I["folder-drag-accept"] = ("places", folder(open_=True))

# Trash: 3D-style can (see trash.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trash
I["user-trash"] = ("places", trash.bin_svg(False))
I["user-trash-full"] = ("places", trash.bin_svg(True))

# Start button glyph (original design)
I["start-here"] = ("places", svg(
    "".join(f'<path d="M{cx} {cy-8}l8 8-8 8-8-8z" fill="#fff"/>'
            for cx, cy in ((24, 13), (13, 24), (35, 24), (24, 35)))))

# Start button glyph for the light taskbar (same design, dark fill)
I["windows-dez-start-light"] = ("places", svg(
    "".join(f'<path d="M{cx} {cy-8}l8 8-8 8-8-8z" fill="#1F1F1F"/>'
            for cx, cy in ((24, 13), (13, 24), (35, 24), (24, 35)))))

# Devices
monitor = (f'<rect x="3.5" y="7" width="41" height="27" fill="#3A3A3A"/>'
           f'<rect x="5.5" y="9" width="37" height="23" fill="{B}"/>'
           f'<path d="M5.5 32l37-23v23z" fill="{LB}" opacity=".35"/>'
           '<path d="M19 34h10l1.5 6h-13z" fill="#9A9A9A"/><rect x="14" y="40" width="20" height="2.5" fill="#7A7A7A"/>')
I["computer"] = ("devices", svg(monitor))
I["video-display"] = ("devices", svg(monitor))
I["drive-harddisk"] = ("devices", svg(
    '<rect x="4" y="16" width="40" height="18" fill="#D6D6D6" stroke="#8C8C8C"/>'
    '<rect x="4.5" y="28" width="39" height="5.5" fill="#B5B5B5"/>'
    '<rect x="34" y="30" width="6" height="1.8" fill="#16C60C"/>'
    f'<rect x="8" y="20" width="16" height="3" fill="{B}"/>'))
I["drive-removable-media"] = ("devices", svg(
    '<rect x="14" y="4" width="20" height="13" fill="#C9C9C9" stroke="#8C8C8C"/>'
    '<rect x="18" y="8" width="4" height="4" fill="#6E6E6E"/><rect x="26" y="8" width="4" height="4" fill="#6E6E6E"/>'
    f'<rect x="11" y="17" width="26" height="27" fill="{B}"/><rect x="11" y="17" width="26" height="3" fill="{DB}"/>'
    f'<circle cx="24" cy="33" r="4.5" fill="none" stroke="#fff" stroke-width="1.6"/>'))
I["media-optical"] = ("devices", svg(
    '<circle cx="24" cy="24" r="20" fill="#E8EEF4" stroke="#9AA8B5"/>'
    '<path d="M24 4a20 20 0 0 1 17.3 10L24 24z" fill="#C8E6FF"/>'
    '<path d="M24 44a20 20 0 0 1-17.3-10L24 24z" fill="#F6D9F0"/>'
    '<circle cx="24" cy="24" r="6" fill="#fff" stroke="#9AA8B5"/><circle cx="24" cy="24" r="2.5" fill="#9AA8B5"/>'))
I["printer"] = ("devices", svg(
    '<rect x="13" y="5" width="22" height="12" fill="#fff" stroke="#A6A6A6"/>'
    '<rect x="4" y="16" width="40" height="18" fill="#5A5A5A"/>'
    '<rect x="4" y="16" width="40" height="3" fill="#6E6E6E"/>'
    '<rect x="36" y="21" width="4" height="2" fill="#16C60C"/>'
    '<rect x="12" y="29" width="24" height="15" fill="#fff" stroke="#A6A6A6"/>'
    f'<path d="M16 34h16M16 38h11" stroke="{B}" stroke-width="1.4"/>'))
I["input-keyboard"] = ("devices", svg(
    '<rect x="2.5" y="13" width="43" height="22" fill="#4A4A4A"/>'
    + "".join(f'<rect x="{5.5+c*4.6:.1f}" y="{16+r*4.6:.1f}" width="3.6" height="3.4" fill="#D9D9D9"/>'
              for r in range(3) for c in range(8))
    + '<rect x="12" y="29.8" width="24" height="3" fill="#D9D9D9"/>'))
I["input-mouse"] = ("devices", svg(
    '<path d="M14 18a10 10 0 0 1 20 0v12a10 10 0 0 1-20 0z" fill="#D9D9D9" stroke="#8C8C8C"/>'
    '<path d="M24 8v12M14 20h20" stroke="#8C8C8C"/><rect x="22.8" y="11" width="2.4" height="5" rx="1.2" fill="#5A5A5A"/>'))
I["network-wired"] = ("devices", svg(
    '<rect x="8" y="5" width="32" height="22" fill="#3A3A3A"/>'
    f'<rect x="10" y="7" width="28" height="18" fill="{B}"/>'
    '<path d="M24 27v7M10 41h28M24 34v7" stroke="#6E6E6E" stroke-width="2.2"/>'
    '<rect x="20" y="33" width="8" height="5" fill="#6E6E6E"/>'))
I["audio-speakers"] = ("devices", svg(
    '<rect x="12" y="4" width="24" height="40" fill="#3A3A3A"/>'
    '<circle cx="24" cy="31" r="8" fill="#6E6E6E"/><circle cx="24" cy="31" r="3" fill="#2A2A2A"/>'
    '<circle cx="24" cy="13" r="4" fill="#6E6E6E"/>'))
I["network-workgroup"] = ("places", svg(
    g_globe(cx=24, cy=20, r=14).replace('stroke-width="1.3"', 'stroke-width="2"')
    + '<path d="M24 34v6M12 42h24" stroke="#6E6E6E" stroke-width="2.4"/>'))

# Applications
def window_frame(content, title=B):
    return (f'<rect x="3.5" y="6.5" width="41" height="35" fill="#fff" stroke="#8C8C8C"/>'
            f'<rect x="4" y="7" width="40" height="6" fill="{title}"/>' + content)

I["utilities-terminal"] = ("apps", svg(
    '<rect x="3.5" y="6.5" width="41" height="35" fill="#0C0C0C" stroke="#5A5A5A"/>'
    '<rect x="4" y="7" width="40" height="5" fill="#E6E6E6"/>'
    '<path d="M10 20l6 5-6 5" fill="none" stroke="#fff" stroke-width="2.4"/>'
    '<rect x="19" y="29" width="10" height="2.4" fill="#fff"/>'))
I["system-file-manager"] = ("apps", folder(band=B))
I["accessories-text-editor"] = ("apps", svg(
    '<rect x="9.5" y="7.5" width="29" height="37" fill="#fff" stroke="#8C8C8C"/>'
    f'<rect x="9" y="4" width="30" height="7" fill="{B}"/>'
    + "".join(f'<circle cx="{x}" cy="7.5" r="1.4" fill="#fff"/>' for x in (15, 21, 27, 33))
    + lines("#9A9A9A", y0=17, n=7, x0=13.5, x1=34.5)))
I["preferences-system"] = ("apps", svg(
    f'<path d="M21 3h6l1 5.2a16 16 0 0 1 4.2 2.4l5-1.8 3 5.2-4 3.4a16 16 0 0 1 0 4.8l4 3.4-3 5.2-5-1.8'
    f'a16 16 0 0 1-4.2 2.4L27 36h-6l-1-5.2a16 16 0 0 1-4.2-2.4l-5 1.8-3-5.2 4-3.4a16 16 0 0 1 0-4.8'
    f'l-4-3.4 3-5.2 5 1.8A16 16 0 0 1 20 8.2z" transform="translate(0 4.5)" fill="{B}"/>'
    '<circle cx="24" cy="24" r="6.5" fill="#fff"/><circle cx="24" cy="24" r="3.5" fill="#B9D9F5"/>'))
I["accessories-calculator"] = ("apps", svg(
    '<rect x="9.5" y="3.5" width="29" height="41" fill="#3A3A3A" stroke="#6E6E6E"/>'
    '<rect x="13" y="7" width="22" height="8" fill="#D9E6EF"/>'
    + "".join(f'<rect x="{13+c*5.8:.1f}" y="{18+r*6.4:.1f}" width="4.6" height="5" fill="{"#7A7A7A" if not (c == 3 and r == 3) else B}"/>'
              for r in range(4) for c in range(4))))
I["image-viewer"] = ("apps", svg(
    '<rect x="4.5" y="8.5" width="39" height="31" fill="#fff" stroke="#8C8C8C"/>'
    f'<rect x="7" y="11" width="34" height="26" fill="{LB}"/>'
    f'<path d="M7 37l11-13 8 9 5-5 10 9z" fill="{B}"/><circle cx="33" cy="17.5" r="3.2" fill="#FFB900"/>'))
I["multimedia-video-player"] = ("apps", svg(
    f'<circle cx="24" cy="24" r="20" fill="{B}"/><circle cx="24" cy="24" r="20" fill="none" stroke="{DB}" stroke-width="1.2"/>'
    '<path d="M19.5 14.5v19l15-9.5z" fill="#fff"/>'))
I["multimedia-audio-player"] = ("apps", svg(
    '<circle cx="24" cy="24" r="20" fill="#E8590C"/>'
    '<path d="M20 31V16l12-2.5v15" fill="none" stroke="#fff" stroke-width="2.4"/>'
    '<ellipse cx="17.5" cy="31.2" rx="3.6" ry="2.8" fill="#fff"/><ellipse cx="29.5" cy="28.7" rx="3.6" ry="2.8" fill="#fff"/>'))
I["internet-mail"] = ("apps", svg(
    f'<rect x="3.5" y="10.5" width="41" height="27" fill="{B}"/>'
    '<path d="M3.5 10.5L24 27l20.5-16.5" fill="none" stroke="#fff" stroke-width="2"/>'
    f'<path d="M3.5 37.5l15-13M44.5 37.5l-15-13" stroke="{DB}" stroke-width="1.4"/>'))
I["web-browser"] = ("apps", svg(g_globe(cx=24, cy=24, r=19).replace('stroke-width="1.3"', 'stroke-width="2"')))
box = ('<path d="M24 5l19 8.5v21L24 43 5 34.5v-21z" fill="#D9A55C"/>'
       '<path d="M24 22l19-8.5v21L24 43z" fill="#C18A3E"/><path d="M5 13.5L24 22l19-8.5L24 5z" fill="#ECC489"/>')
I["system-software-install"] = ("apps", svg(
    box + f'<circle cx="35" cy="35" r="10" fill="{B}"/>'
    '<path d="M35 28.5v10M30.5 34l4.5 4.5 4.5-4.5" fill="none" stroke="#fff" stroke-width="2.2"/>'))
I["package-x-generic"] = ("mimetypes", svg(box + '<path d="M14.5 9.2L33.5 17.8v6" fill="none" stroke="#F5DDB5" stroke-width="2.5"/>'))
I["utilities-system-monitor"] = ("apps", svg(window_frame(
    '<path d="M4 37h40" stroke="#D9D9D9"/><path d="M4 31h40M4 25h40M4 19h40" stroke="#EEEEEE"/>'
    '<path d="M6 34l7-6 5 4 7-12 6 7 5-4 6 3" fill="none" stroke="#16A34A" stroke-width="2.2"/>', "#3A3A3A")))
I["accessories-screenshot"] = ("apps", svg(
    f'<path d="M5 15V5h10M33 5h10v10M43 33v10H33M15 43H5V33" fill="none" stroke="{B}" stroke-width="3"/>'
    '<rect x="12" y="16" width="24" height="18" fill="#4A4A4A"/><circle cx="24" cy="25" r="6" fill="#9AC7EE"/>'
    '<circle cx="24" cy="25" r="3" fill="#2A2A2A"/><rect x="18" y="13" width="7" height="3" fill="#4A4A4A"/>'))
I["system-search"] = ("apps", svg(
    f'<circle cx="20" cy="20" r="13" fill="#E5F3FF" stroke="{B}" stroke-width="3.5"/>'
    '<path d="M29.5 29.5L42 42" stroke="#4A4A4A" stroke-width="5.5" stroke-linecap="square"/>'))
I["help-browser"] = ("apps", svg(
    f'<circle cx="24" cy="24" r="20" fill="{B}"/>'
    '<path d="M18 18.5a6 6 0 1 1 9 5.2c-2 1.2-3 2.3-3 4.6v1.2" fill="none" stroke="#fff" stroke-width="3.2"/>'
    '<circle cx="24" cy="35" r="2.2" fill="#fff"/>'))
I["preferences-desktop-wallpaper"] = ("apps", svg(
    '<rect x="4.5" y="8.5" width="39" height="31" fill="#fff" stroke="#8C8C8C"/>'
    '<rect x="7" y="11" width="34" height="26" fill="#1E3A8A"/>'
    f'<path d="M7 37l14-26h8L17 37z" fill="{LB}" opacity=".85"/><path d="M19 37l13-26h9v6L27 37z" fill="{B}" opacity=".9"/>'))
I["preferences-desktop-display"] = ("apps", svg(monitor))
I["system-users"] = ("apps", svg(
    f'<circle cx="24" cy="16" r="9" fill="{B}"/><path d="M7 43a17 15 0 0 1 34 0z" fill="{B}"/>'))
I["preferences-desktop"] = ("apps", svg(
    '<rect x="4" y="4" width="40" height="40" fill="#4A4A4A"/>'
    + "".join(f'<path d="M{x} 10v28" stroke="#9A9A9A" stroke-width="2"/><rect x="{x-4}" y="{y}" width="8" height="5" fill="{B}"/>'
              for x, y in ((14, 26), (24, 13), (34, 21)))))
I["preferences-desktop-theme"] = ("apps", svg(
    '<path d="M24 4C12 4 4 12.5 4 23.5 4 34 12 44 22 44c3 0 4-2 3-4.5-1-2.3.5-4.5 3-4.5h6c6 0 10-4.5 10-10C44 13 35 4 24 4z" fill="#F2F2F2" stroke="#8C8C8C"/>'
    f'<circle cx="14" cy="21" r="3.5" fill="#E81123"/><circle cx="20" cy="12.5" r="3.5" fill="#FFB900"/>'
    f'<circle cx="30" cy="12.5" r="3.5" fill="#16A34A"/><circle cx="36" cy="21" r="3.5" fill="{B}"/>'))
I["preferences-desktop-keyboard"] = ("apps", I["input-keyboard"][1])
I["preferences-desktop-peripherals"] = ("apps", I["input-mouse"][1])
I["system-log-out"] = ("apps", svg(
    f'<path d="M14.5 12.5a16 16 0 1 0 19 0" fill="none" stroke="{B}" stroke-width="4"/>'
    f'<path d="M24 4v18" stroke="{B}" stroke-width="4.5"/>'))
I["xfce4-power-manager-settings"] = ("apps", svg(
    '<rect x="5.5" y="13.5" width="34" height="21" fill="#fff" stroke="#6E6E6E" stroke-width="2"/>'
    '<rect x="40" y="19" width="4" height="10" fill="#6E6E6E"/><rect x="9" y="17" width="20" height="14" fill="#16A34A"/>'))
I["preferences-system-notifications"] = ("apps", svg(
    '<rect x="3.5" y="9.5" width="41" height="29" fill="#1F1F1F" stroke="#5A5A5A"/>'
    f'<rect x="8" y="14" width="9" height="9" fill="{B}"/>'
    '<path d="M21 16h18M21 21h13M8 29h31M8 33h22" stroke="#BFBFBF" stroke-width="1.6"/>'))
I["xfwm4"] = ("apps", svg(window_frame(
    '<path d="M33 9h3M38 9.5l2 2m0-2l-2 2" stroke="#fff" stroke-width="1"/>' + lines("#BFBFBF", 19, 5, 9, 38))))
I["xfce4-panel"] = ("apps", svg(
    '<rect x="3.5" y="9.5" width="41" height="29" fill="#fff" stroke="#8C8C8C"/>'
    '<rect x="4" y="31" width="40" height="7" fill="#1F1F1F"/>'
    f'<rect x="6" y="32.5" width="4" height="4" fill="{LB}"/><rect x="13" y="32.5" width="4" height="4" fill="#9A9A9A"/>'
    f'<rect x="12" y="37" width="6" height="1" fill="{LB}"/>'))

I["preferences-desktop-locale"] = ("apps", svg(
    '<rect x="3.5" y="5.5" width="25" height="25" fill="#E6E6E6" stroke="#8C8C8C"/>'
    '<path d="M9 13h14M16 10v3M11 13c1.5 5 5 8.5 10 10M21 13c-1.5 5-5 8.5-10 10" fill="none" stroke="#5A5A5A" stroke-width="1.8"/>'
    f'<rect x="19.5" y="17.5" width="25" height="25" fill="{B}"/>'
    '<path d="M25.5 37.5L32 22.5l6.5 15M27.8 32.2h8.4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/>'))

# Menu categories
I["applications-accessories"] = ("categories", svg(
    '<path d="M15 18L43 33M15 30L43 15" stroke="#6E6E6E" stroke-width="3.2"/>'
    f'<circle cx="11" cy="14" r="6" fill="#fff" stroke="{B}" stroke-width="3.5"/>'
    f'<circle cx="11" cy="34" r="6" fill="#fff" stroke="{B}" stroke-width="3.5"/>'
    '<circle cx="26" cy="24" r="1.8" fill="#3A3A3A"/>'))
I["applications-development"] = ("categories", svg(window_frame(
    f'<path d="M16 20l-6 6.5 6 6.5M32 20l6 6.5-6 6.5" fill="none" stroke="{B}" stroke-width="2.6"/>'
    '<path d="M27 18l-6 17" stroke="#6E6E6E" stroke-width="2.4"/>', "#3A3A3A")))
I["applications-games"] = ("categories", svg(
    '<path d="M12 14h24c5 0 8 4 8.5 10l1 12c.4 4-4 6-7 3l-5-5H14.5l-5 5c-3 3-7.4 1-7-3l1-12C4 18 7 14 12 14z" fill="#4A4A4A"/>'
    '<path d="M14 21v8M10 25h8" stroke="#fff" stroke-width="2.6"/>'
    f'<circle cx="33" cy="22" r="2.2" fill="{LB}"/><circle cx="37.5" cy="26.5" r="2.2" fill="#E81123"/>'
    f'<circle cx="28.5" cy="26.5" r="2.2" fill="#FFB900"/><circle cx="33" cy="31" r="2.2" fill="#16A34A"/>'))
I["applications-graphics"] = ("categories", I["preferences-desktop-theme"][1])
I["applications-internet"] = ("categories", I["web-browser"][1])
I["applications-multimedia"] = ("categories", svg(
    '<rect x="4" y="12" width="28" height="22" fill="#8E44AD"/>'
    '<path d="M14 17v12l9-6z" fill="#fff"/>'
    '<circle cx="35" cy="34" r="9" fill="#E8590C"/>'
    '<path d="M33 37.5V29l5.5-1v7" fill="none" stroke="#fff" stroke-width="1.8"/>'))
I["applications-office"] = ("categories", svg(
    PAGE + lines("#B5B5B5", 16, 3, 14, 34)
    + f'<rect x="14" y="34" width="4" height="6" fill="{B}"/><rect x="20" y="29" width="4" height="11" fill="#16A34A"/>'
    + '<rect x="26" y="31" width="4" height="9" fill="#E8590C"/>'))
I["applications-system"] = ("categories", I["preferences-system"][1])
I["applications-utilities"] = ("categories", I["applications-accessories"][1])
I["applications-other"] = ("categories", svg(
    f'<rect x="6" y="6" width="16" height="16" fill="{B}"/><circle cx="34" cy="14" r="8" fill="#E8590C"/>'
    '<path d="M14 26l9 16H5z" fill="#16A34A"/><rect x="26" y="26" width="16" height="16" fill="#8E44AD"/>'))
I["applications-science"] = ("categories", svg(
    '<path d="M18 5h12M20 5v13L8 40c-1 2 0 3 2 3h28c2 0 3-1 2-3L28 18V5" fill="#E5F3FF" stroke="#6E6E6E" stroke-width="2"/>'
    f'<path d="M13 31h22l4.3 8.5c.6 1.3 0 2-1.3 2H10c-1.3 0-1.9-.7-1.3-2z" fill="{B}"/>'))
I["applications-education"] = ("categories", svg(
    f'<path d="M24 9L2 19l22 10 22-10z" fill="{B}"/><path d="M11 24v9c0 4 26 4 26 0v-9l-13 6z" fill="{DB}"/>'
    '<path d="M42 21v12" stroke="#6E6E6E" stroke-width="2"/>'))

I["document-open-recent"] = ("categories", svg(
    f'<circle cx="24" cy="24" r="19" fill="#fff" stroke="{B}" stroke-width="3.5"/>'
    f'<path d="M24 12v13l8 5" fill="none" stroke="#3A3A3A" stroke-width="3"/>'))
# File types
I["text-x-generic"] = ("mimetypes", page(lines()))
I["image-x-generic"] = ("mimetypes", page(
    f'<rect x="13" y="18" width="22" height="18" fill="{LB}"/>'
    f'<path d="M13 36l7-8 5 5 3-3 7 6z" fill="{B}"/><circle cx="29.5" cy="22.5" r="2.2" fill="#FFB900"/>'))
I["audio-x-generic"] = ("mimetypes", page(
    '<path d="M21 34V20l10-2v13" fill="none" stroke="#E8590C" stroke-width="2.2"/>'
    '<ellipse cx="18.5" cy="34.2" rx="3.3" ry="2.6" fill="#E8590C"/><ellipse cx="28.5" cy="31.2" rx="3.3" ry="2.6" fill="#E8590C"/>'))
I["video-x-generic"] = ("mimetypes", page(
    '<rect x="12" y="19" width="24" height="17" fill="#8E44AD"/><path d="M21 23v9l7-4.5z" fill="#fff"/>'))
I["application-pdf"] = ("mimetypes", page(lines("#C9C9C9", 14, 4) + label("PDF", "#D13438")))
I["x-office-document"] = ("mimetypes", page(lines("#C9C9C9", 14, 4) + label("DOC", "#2B65B8")))
I["x-office-spreadsheet"] = ("mimetypes", page(
    "".join(f'<rect x="{13+c*7}" y="{12+r*4.5}" width="6" height="3.5" fill="{"#C7E8CF" if r else "#7CC48E"}"/>'
            for r in range(4) for c in range(3)) + label("XLS", "#1E7B45")))
I["x-office-presentation"] = ("mimetypes", page(
    '<rect x="13" y="12" width="21" height="14" fill="#FBE0D3"/><path d="M23.5 15v4.5h4.5a4.5 4.5 0 1 1-4.5-4.5z" fill="#D2531E"/>'
    + label("PPT", "#C4501B")))
I["application-x-executable"] = ("mimetypes", svg(window_frame(
    f'<rect x="10" y="18" width="12" height="9" fill="{LB}"/><rect x="26" y="18" width="12" height="9" fill="{LB}"/>'
    f'<rect x="10" y="30" width="28" height="6" fill="#E6E6E6"/>')))
I["text-x-script"] = ("mimetypes", page(
    '<rect x="12" y="16" width="23" height="20" fill="#1F1F1F"/>'
    '<path d="M15 21l4 3.5-4 3.5" fill="none" stroke="#4CC2FF" stroke-width="1.8"/><path d="M21 31h7" stroke="#fff" stroke-width="1.8"/>'))
I["text-html"] = ("mimetypes", page(g_globe(cx=24, cy=27, r=9)))
I["font-x-generic"] = ("mimetypes", page(
    '<text x="23.5" y="35" font-family="Georgia,DejaVu Serif,serif" font-size="17" fill="#3A3A3A" '
    'text-anchor="middle">Aa</text>'))
I["unknown"] = ("mimetypes", page(
    '<text x="24" y="35" font-family="Segoe UI,Noto Sans,DejaVu Sans,sans-serif" font-weight="700" '
    'font-size="18" fill="#A6A6A6" text-anchor="middle">?</text>'))
I["application-x-cd-image"] = ("mimetypes", I["media-optical"][1])


# Actions (thin dark-grey strokes) — viewBox 24
def act(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'
            f'<g fill="none" stroke="#333" stroke-width="1.3" stroke-linejoin="round">{body}</g></svg>\n')
I["go-previous"] = ("actions", act('<path d="M19 12H5.5M11 6.5L5.5 12l5.5 5.5"/>'))
I["go-next"] = ("actions", act('<path d="M5 12h13.5M13 6.5l5.5 5.5-5.5 5.5"/>'))
I["go-up"] = ("actions", act('<path d="M12 19V5.5M6.5 11L12 5.5l5.5 5.5"/>'))
I["go-down"] = ("actions", act('<path d="M12 5v13.5M6.5 13l5.5 5.5 5.5-5.5"/>'))
I["go-home"] = ("actions", act('<path d="M3.5 11.5L12 4l8.5 7.5M6 9.5V20h4.5v-5.5h3V20H18V9.5"/>'))
I["view-refresh"] = ("actions", act('<path d="M19 12a7 7 0 1 1-2.1-5"/><path d="M17.5 3v4.5H13"/>'))
I["edit-find"] = ("actions", act('<circle cx="10" cy="10" r="5.8"/><path d="M14.3 14.3L20 20"/>'))
I["document-new"] = ("actions", act('<path d="M6 3.5h8l4 4V20.5H6zM14 3.5v4h4"/><path d="M12 10.5v6M9 13.5h6" stroke="#0078D7"/>'))
I["document-open"] = ("actions", act('<path d="M3.5 6h6l2 2h8.5v11H3.5z"/><path d="M3.5 19l3-8h15l-2 8" />'))
I["document-save"] = ("actions", act('<path d="M4 4h13l3 3v13H4z"/><path d="M8 4v5h8V4M7.5 20v-6h9v6"/>'))
I["document-save-as"] = ("actions", act('<path d="M4 4h13l3 3v6M4 4v16h8M8 4v5h8V4"/><path d="M14 20l1-3 5-5 2 2-5 5z" stroke="#0078D7"/>'))
I["document-print"] = ("actions", act('<path d="M7 9V3.5h10V9M7 17H4V9h16v8h-3"/><path d="M7 13.5h10v7H7z"/>'))
I["document-properties"] = ("actions", act('<path d="M6 3.5h12v17H6z"/><path d="M9 8h6M9 11.5h6M9 15h4"/>'))
I["edit-copy"] = ("actions", act('<path d="M8.5 8.5h11v12h-11z"/><path d="M15.5 8.5v-5h-11v12h4"/>'))
I["edit-cut"] = ("actions", act('<circle cx="7" cy="17.5" r="2.5"/><circle cx="17" cy="17.5" r="2.5"/><path d="M8.6 15.6L17 3.5M15.4 15.6L7 3.5"/>'))
I["edit-paste"] = ("actions", act('<path d="M8 5H5v15.5h14V5h-3"/><path d="M8.5 3.5h7v3h-7z"/>'))
I["edit-delete"] = ("actions", act('<path d="M4 6h16M9.5 6V3.5h5V6M6 6l1 14.5h10L18 6M10 10v7M14 10v7"/>'))
I["edit-undo"] = ("actions", act('<path d="M5 9.5h9.5a5 5 0 0 1 0 10H9"/><path d="M9 5L4.5 9.5 9 14"/>'))
I["edit-redo"] = ("actions", act('<path d="M19 9.5H9.5a5 5 0 0 0 0 10H15"/><path d="M15 5l4.5 4.5L15 14"/>'))
I["edit-clear"] = ("actions", act('<path d="M5 5l14 14M19 5L5 19"/>'))
I["edit-select-all"] = ("actions", act('<path d="M4 4h16v16H4z" stroke-dasharray="2 2"/><path d="M8 8h8v8H8z" fill="#0078D7" stroke="#0078D7"/>'))
I["list-add"] = ("actions", act('<path d="M12 4v16M4 12h16"/>'))
I["list-remove"] = ("actions", act('<path d="M4 12h16"/>'))
I["view-list"] = ("actions", act('<path d="M4 6h2M4 12h2M4 18h2M9 6h11M9 12h11M9 18h11"/>'))
I["view-grid"] = ("actions", act('<path d="M4 4h6.5v6.5H4zM13.5 4H20v6.5h-6.5zM4 13.5h6.5V20H4zM13.5 13.5H20V20h-6.5z"/>'))
I["window-close"] = ("actions", act('<path d="M6 6l12 12M18 6L6 18"/>'))
I["process-stop"] = ("actions", act('<circle cx="12" cy="12" r="8.5"/><path d="M9 9l6 6M15 9l-6 6"/>'))
I["zoom-in"] = ("actions", act('<circle cx="10" cy="10" r="5.8"/><path d="M14.3 14.3L20 20M7.5 10h5M10 7.5v5"/>'))
I["zoom-out"] = ("actions", act('<circle cx="10" cy="10" r="5.8"/><path d="M14.3 14.3L20 20M7.5 10h5"/>'))
I["format-text-bold"] = ("actions", act('<path d="M7 4h6a3.8 3.8 0 0 1 0 7.6H7zM7 11.6h7a4.2 4.2 0 0 1 0 8.4H7z" stroke-width="1.8"/>'))
I["format-text-italic"] = ("actions", act('<path d="M10 4h8M6 20h8M14 4l-4 16"/>'))
I["format-text-underline"] = ("actions", act('<path d="M7 4v7a5 5 0 0 0 10 0V4M5 20.5h14"/>'))
I["mail-send"] = ("actions", act('<path d="M3.5 4.5l17 7.5-17 7.5 3-7.5zM6.5 12h14"/>'))
I["bookmark-new"] = ("actions", act('<path d="M6.5 3.5h11v17l-5.5-4-5.5 4z"/>'))
I["system-run"] = ("actions", act('<path d="M7 4.5v15l12-7.5z"/>'))

# --------------------------------------------------------------------------
# Aliases (names used by XFCE apps, distributions and specs)
# --------------------------------------------------------------------------
A = {
    "folder": ["inode-directory", "folder-new", "gtk-directory", "folder-visiting"],
    "folder-open": ["folder-drag-accept", "document-open-folder"],
    "user-home": ["folder-home", "gnome-fs-home"],
    "user-desktop": ["desktop", "folder-desktop", "gnome-fs-desktop"],
    "folder-download": ["folder-downloads"],
    "folder-publicshare": ["folder-public"],
    "folder-remote": ["folder-network", "gnome-fs-network", "network-server"],
    "user-trash": ["trashcan_empty", "user-trash-empty", "emptytrash"],
    "user-trash-full": ["trashcan_full"],
    "start-here": ["org.xfce.panel.whiskermenu", "xfce4-whiskermenu", "xfce4-panel-menu",
                   "org.xfce.panel.applicationsmenu", "applications-all"],
    "computer": ["user-desktop-computer", "gnome-fs-client", "system", "org.xfce.panel.showdesktop"],
    "drive-harddisk": ["drive-harddisk-system", "drive-harddisk-root", "drive-multidisk",
                       "gnome-dev-harddisk", "drive-harddisk-usb", "org.gnome.DiskUtility",
                       "gnome-disks", "drive-harddisk-solidstate"],
    "drive-removable-media": ["drive-removable-media-usb", "media-removable", "media-flash",
                              "drive-removable-media-usb-pendrive"],
    "media-optical": ["drive-optical", "media-optical-cd", "media-optical-dvd", "media-optical-bd"],
    "printer": ["printer-network", "system-config-printer", "preferences-desktop-printers"],
    "network-wired": ["network-wired-symbolic-fallback", "preferences-system-network",
                      "nm-device-wired", "network-manager", "nm-connection-editor"],
    "audio-speakers": ["audio-card", "multimedia-volume-control", "pavucontrol",
                       "org.pulseaudio.pavucontrol", "preferences-desktop-sound"],
    "utilities-terminal": ["org.xfce.terminalemulator", "org.xfce.terminal", "xfce4-terminal", "terminal", "Terminal",
                           "org.gnome.Terminal", "x-terminal-emulator", "gnome-terminal", "konsole",
                           "xterm"],
    "system-file-manager": ["org.xfce.thunar", "Thunar", "thunar", "file-manager", "org.xfce.filemanager",
                            "org.gnome.Nautilus", "nemo", "pcmanfm"],
    "accessories-text-editor": ["org.xfce.mousepad", "mousepad", "text-editor", "gedit",
                                "org.gnome.gedit", "org.gnome.TextEditor", "xed"],
    "preferences-system": ["org.xfce.settings.manager", "xfce4-settings-manager",
                           "gnome-control-center", "preferences-desktop-default-applications",
                           "org.xfce.settings.default-applications", "systemsettings"],
    "accessories-calculator": ["org.xfce.calculator", "galculator", "org.gnome.Calculator",
                               "gnome-calculator", "calc"],
    "image-viewer": ["org.xfce.ristretto", "ristretto", "eog", "org.gnome.eog",
                     "multimedia-photo-viewer", "shotwell", "gthumb"],
    "multimedia-video-player": ["org.xfce.parole", "parole", "totem", "vlc", "mpv", "celluloid",
                                "io.github.celluloid_player.Celluloid", "smplayer"],
    "multimedia-audio-player": ["rhythmbox", "audacious", "org.gnome.Rhythmbox3",
                                "org.gnome.Music", "quodlibet", "clementine", "strawberry"],
    "internet-mail": ["org.xfce.mailreader", "mail-client", "thunderbird", "evolution", "geary", "org.gnome.Geary",
                      "claws-mail", "mail-send-receive"],
    "go-previous": ["gtk-go-back-ltr", "back"],
    "go-next": ["gtk-go-forward-ltr", "forward"],
    "go-up": ["gtk-go-up"],
    "view-refresh": ["reload", "gtk-refresh"],
    "edit-delete": ["delete"],
    "list-add": ["add", "gtk-add"],
    "list-remove": ["remove", "gtk-remove"],
    "view-list": ["view-list-details", "view-list-compact"],
    "view-grid": ["view-list-icons", "view-app-grid"],
    "document-open": ["gtk-open"],
    "document-save": ["gtk-save"],
    "web-browser": ["internet-web-browser", "browser", "org.xfce.webbrowser", "exo-web-browser"],
    "system-software-install": ["software-store", "org.gnome.Software", "gnome-software",
                                "synaptic", "system-software-update", "software-properties",
                                "update-manager", "mintinstall", "pamac", "org.xfce.catfish"],
    "package-x-generic": ["application-x-archive", "application-zip", "application-x-tar",
                          "application-x-compressed-tar", "application-x-7z-compressed",
                          "application-x-rar", "application-gzip", "application-x-bzip",
                          "application-x-xz", "application-x-deb", "application-x-rpm",
                          "org.xfce.xarchiver", "xarchiver", "file-roller", "org.gnome.FileRoller",
                          "engrampa", "ark", "archive-manager"],
    "utilities-system-monitor": ["org.xfce.taskmanager", "xfce4-taskmanager",
                                 "gnome-system-monitor", "org.gnome.SystemMonitor", "htop"],
    "accessories-screenshot": ["org.xfce.screenshooter", "xfce4-screenshooter",
                               "applets-screenshooter", "gnome-screenshot", "org.gnome.Screenshot"],
    "document-open-recent": ["recently-used", "document-recent", "folder-recent"],
    "system-search": ["org.xfce.appfinder", "xfce4-appfinder", "catfish",
                      "org.xfce.panel.directorymenu"],
    "help-browser": ["help-contents", "help-about", "yelp", "org.gnome.Yelp", "xfce4-about",
                     "org.xfce.about", "system-help"],
    "preferences-desktop-wallpaper": ["org.xfce.xfdesktop", "xfdesktop", "preferences-desktop-background"],
    "preferences-desktop-display": ["org.xfce.settings.display", "xfce4-display",
                                    "preferences-desktop-screensaver", "org.xfce.ScreenSaver",
                                    "xscreensaver", "display"],
    "system-users": ["preferences-desktop-user", "user-info", "users-admin", "avatar-default",
                     "system-config-users", "org.xfce.settings.accessibility",
                     "preferences-desktop-accessibility"],
    "preferences-desktop": ["org.xfce.settings.editor", "xfce4-settings-editor",
                            "preferences-other", "dconf-editor", "ca.desrt.dconf-editor"],
    "preferences-desktop-theme": ["org.xfce.settings.appearance", "preferences-desktop-color",
                                  "preferences-desktop-font", "xfce4-appearance",
                                  "applications-graphics", "gimp", "org.gimp.GIMP", "inkscape",
                                  "org.inkscape.Inkscape", "krita", "mypaint"],
    "preferences-desktop-locale": ["language-selector", "config-language", "gnome-language-selector",
                                   "preferences-desktop-language", "org.gnome.Settings-region",
                                   "fcitx", "ibus-setup", "input-method"],
    "preferences-desktop-keyboard": ["org.xfce.settings.keyboard", "xfce4-keyboard",
                                     "preferences-desktop-keyboard-shortcuts"],
    "preferences-desktop-peripherals": ["org.xfce.settings.mouse", "xfce4-mouse",
                                        "preferences-desktop-mouse"],
    "system-log-out": ["system-shutdown", "xfsm-logout", "org.xfce.session",
                       "xfce4-session-settings", "system-restart", "gnome-session-halt"],
    "xfce4-power-manager-settings": ["org.xfce.powermanager", "preferences-system-power",
                                     "battery", "xfce4-battery-plugin", "gnome-power-manager"],
    "preferences-system-notifications": ["org.xfce.notification", "xfce4-notifyd",
                                         "xfce4-notifyd-config"],
    "xfwm4": ["org.xfce.xfwm4", "org.xfce.xfwm4-tweaks", "preferences-system-windows",
              "org.xfce.workspaces", "preferences-desktop-workspaces", "xfce4-workspaces"],
    "xfce4-panel": ["org.xfce.panel", "xfce4-panel-settings", "preferences-desktop-panel"],
    "applications-games": ["input-gaming", "gnome-mines", "aisleriot"],
    "applications-development": ["applications-engineering", "code", "codium",
                                 "org.gnome.Builder", "geany", "text-x-source"],
    "applications-other": ["applications-interfacedesign", "app-launcher", "application-default-icon",
                           "xfce4-launcher", "org.xfce.panel.launcher", "exec"],
    "text-x-generic": ["application-x-zerosize", "text-plain", "text-x-readme", "text-x-log", "text-x-changelog",
                       "text-x-copying", "text-x-csrc", "text-x-chdr", "text-x-c++src",
                       "text-x-java", "text-x-markdown", "application-json", "text-x-preview",
                       "text-x-generic-template", "application-xml", "text-xml", "gtk-file",
                       "empty", "x-office-document-template"],
    "image-x-generic": ["image-png", "image-jpeg", "image-gif", "image-bmp", "image-tiff",
                        "image-webp", "image-x-ico", "image-svg+xml", "image-x-xcf"],
    "audio-x-generic": ["audio-mpeg", "audio-x-mpeg", "audio-x-wav", "audio-flac", "audio-ogg",
                        "audio-x-vorbis+ogg", "audio-mp4", "audio-x-flac"],
    "video-x-generic": ["video-mp4", "video-x-matroska", "video-webm", "video-x-msvideo",
                        "video-mpeg", "video-quicktime", "video-x-ogm+ogg"],
    "x-office-document": ["application-msword", "application-vnd.oasis.opendocument.text",
                          "application-vnd.openxmlformats-officedocument.wordprocessingml.document",
                          "application-rtf", "libreoffice-writer", "libreoffice-oasis-text",
                          "libreoffice-main", "libreoffice-startcenter", "application-x-office-document"],
    "x-office-spreadsheet": ["application-vnd.ms-excel", "application-vnd.oasis.opendocument.spreadsheet",
                             "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             "text-csv", "libreoffice-calc", "libreoffice-oasis-spreadsheet",
                             "gnumeric"],
    "x-office-presentation": ["application-vnd.ms-powerpoint",
                              "application-vnd.oasis.opendocument.presentation",
                              "application-vnd.openxmlformats-officedocument.presentationml.presentation",
                              "libreoffice-impress", "libreoffice-oasis-presentation"],
    "application-pdf": ["application-x-pdf", "x-pdf", "org.gnome.Evince", "evince",
                        "atril", "org.xfce.ristretto-pdf", "okular"],
    "application-x-executable": ["application-x-sharedlib", "application-x-ms-dos-executable",
                                 "application-x-msi", "application-x-appimage", "binary",
                                 "gnome-mime-application-x-executable", "application-vnd.appimage"],
    "text-x-script": ["application-x-shellscript", "text-x-python", "application-x-python",
                      "text-x-sh", "application-x-perl", "application-javascript",
                      "text-x-javascript", "text-x-makefile", "application-x-ruby",
                      "text-x-python3", "application-x-desktop"],
    "text-html": ["application-xhtml+xml", "text-css", "text-x-css", "application-x-mswinurl"],
    "font-x-generic": ["application-x-font-ttf", "font-ttf", "font-otf", "application-x-font-otf",
                       "org.gnome.font-viewer", "gnome-font-viewer"],
    "unknown": ["application-octet-stream", "application-x-generic"],
        "application-x-cd-image": ["application-x-iso9660-image", "application-x-raw-disk-image",
                               "brasero", "xfburn", "org.xfce.xfburn"],
}

# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
# Thin-line symbolic icons (navigation, path bar, spinner, etc.)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symbolic
for _n, _b in symbolic.S.items():
    I[_n + "-symbolic"] = ("actions", symbolic.sym(_b))
# Thin system-tray glyphs (network, notifications, power, volume)
for _n, _b in symbolic.TRAY.items():
    I[_n + "-symbolic"] = ("status", symbolic.sym(_b))

cats = sorted({c for c, _ in I.values()})
for c in cats:
    os.makedirs(os.path.join(OUT, "scalable", c), exist_ok=True)

count = 0
for name, (cat, data) in I.items():
    with open(os.path.join(OUT, "scalable", cat, name + ".svg"), "w") as f:
        f.write(data)
    count += 1

links = 0
for base, aliases in A.items():
    cat = I[base][0]
    for al in aliases:
        if al in I:
            continue
        p = os.path.join(OUT, "scalable", cat, al + ".svg")
        if os.path.lexists(p):
            continue
        os.symlink(base + ".svg", p)
        links += 1

# nm-applet uses non-symbolic names that GTK does not recolor: ship a white set
# (dark taskbar, default) in scalable/panel and both sets in panel-variants/,
# from which install.sh copies the one that matches --dark / --light.
def write_panel(dirpath, color):
    os.makedirs(dirpath, exist_ok=True)
    for n, body in symbolic.NM_PANEL.items():
        with open(os.path.join(dirpath, n + ".svg"), "w") as f:
            f.write(symbolic.colored(body, color))
    with open(os.path.join(dirpath, "nm-connecting.svg"), "w") as f:
        f.write(symbolic.colored(symbolic.NM_CONNECTING, color))
    for st in range(1, 4):
        for fr in range(1, 12):
            os.symlink("nm-connecting.svg", os.path.join(dirpath, f"nm-stage{st:02d}-connecting{fr:02d}.svg"))
    for fr in range(1, 15):
        os.symlink("nm-connecting.svg", os.path.join(dirpath, f"nm-vpn-connecting{fr:02d}.svg"))

write_panel(os.path.join(OUT, "scalable", "panel"), "#FFFFFF")
write_panel(os.path.join(OUT, "panel-variants", "dark"), "#FFFFFF")
write_panel(os.path.join(OUT, "panel-variants", "light"), "#1A1A1A")
cats.append("panel")

dirs = ",".join(f"scalable/{c}" for c in cats)
with open(os.path.join(OUT, "index.theme"), "w") as f:
    f.write(f"""[Icon Theme]
Name=windows-dez
Comment=Flat icons for XFCE inspired by Windows 10 — by Rafael Carvalho Ramos
Inherits=elementary-xfce,Adwaita,hicolor
Example=folder
DisplayDepth=32
Directories={dirs}
""")
    for c in cats:
        ctx = {"places": "Places", "devices": "Devices", "apps": "Applications",
               "categories": "Categories", "mimetypes": "MimeTypes", "actions": "Actions",
               "status": "Status", "panel": "Status"}[c]
        size = 16 if c in ("status", "panel") else (24 if c == "actions" else 48)
        f.write(f"\n[scalable/{c}]\nContext={ctx}\nSize={size}\nMinSize=8\nMaxSize=512\nType=Scalable\n")
print(f"icons: {count} drawn, {links} aliases")
