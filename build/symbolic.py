# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""Thin-line symbolic icons (16px, filled shapes so GTK can recolor them)."""
import math

W = 1.25  # line weight at 16px

def _seg(x1, y1, x2, y2, w=W):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return (f'<path d="M{x1+nx:.3f} {y1+ny:.3f}L{x2+nx:.3f} {y2+ny:.3f}'
            f'L{x2-nx:.3f} {y2-ny:.3f}L{x1-nx:.3f} {y1-ny:.3f}Z"/>')

def _dot(x, y, r=W / 2):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}"/>'

def line(*pts, w=W, caps=True):
    out = "".join(_seg(*pts[i], *pts[i + 1], w=w) for i in range(len(pts) - 1))
    joints = pts if caps else pts[1:-1]
    return out + "".join(_dot(x, y, w / 2) for x, y in joints)

def arc(cx, cy, r, a0, a1, n=28, w=W):
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return line(*pts, w=w)

def ring(cx, cy, r, w=W):
    ro, ri = r + w / 2, r - w / 2
    return (f'<path fill-rule="evenodd" d="M{cx-ro} {cy}a{ro} {ro} 0 1 0 {2*ro} 0a{ro} {ro} 0 1 0 {-2*ro} 0Z'
            f'M{cx-ri} {cy}a{ri} {ri} 0 1 0 {2*ri} 0a{ri} {ri} 0 1 0 {-2*ri} 0Z"/>')

def sym(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
            f'<g fill="#2e3436">{body}</g></svg>\n')

house = line((2, 8.2), (8, 2.6), (14, 8.2)) + line((4, 6.6), (4, 13.5), (12, 13.5), (12, 6.6)) \
        + line((6.8, 13.5), (6.8, 10), (9.2, 10), (9.2, 13.5))
magnifier = ring(6.6, 6.6, 4.2) + line((9.7, 9.7), (13.8, 13.8))

S = {
    "go-previous":  line((13.5, 8), (2.8, 8)) + line((7.2, 3.6), (2.8, 8), (7.2, 12.4)),
    "go-next":      line((2.5, 8), (13.2, 8)) + line((8.8, 3.6), (13.2, 8), (8.8, 12.4)),
    "go-up":        line((8, 13.5), (8, 2.8)) + line((3.6, 7.2), (8, 2.8), (12.4, 7.2)),
    "go-down":      line((8, 2.5), (8, 13.2)) + line((3.6, 8.8), (8, 13.2), (12.4, 8.8)),
    "go-home":      house,
    "user-home":    house,
    "edit-find":    magnifier,
    "system-search": magnifier,
    "view-refresh": arc(8, 8, 5.3, -50, 270) + line((6.6, 0.6), (8.9, 2.7), (6.6, 4.8)),
    "document-edit": line((3, 13), (3.4, 10.6), (10.8, 3.2), (12.8, 5.2), (5.4, 12.6), (3, 13)) + line((9.4, 4.6), (11.4, 6.6)),
    "edit":         line((3, 13), (3.4, 10.6), (10.8, 3.2), (12.8, 5.2), (5.4, 12.6), (3, 13)) + line((9.4, 4.6), (11.4, 6.6)),
    "pan-start":    line((10, 3.5), (5.5, 8), (10, 12.5)),
    "pan-end":      line((6, 3.5), (10.5, 8), (6, 12.5)),
    "pan-up":       line((3.5, 10), (8, 5.5), (12.5, 10)),
    "pan-down":     line((3.5, 6), (8, 10.5), (12.5, 6)),
    "window-close": line((3.5, 3.5), (12.5, 12.5)) + line((12.5, 3.5), (3.5, 12.5)),
    "edit-clear":   line((4.5, 4.5), (11.5, 11.5)) + line((11.5, 4.5), (4.5, 11.5)),
    "list-add":     line((8, 2.5), (8, 13.5)) + line((2.5, 8), (13.5, 8)),
    "list-remove":  line((2.5, 8), (13.5, 8)),
    "object-select": line((2.8, 8.4), (6.2, 11.8), (13.2, 4.6), w=1.6),
    "open-menu":    line((2.5, 4), (13.5, 4)) + line((2.5, 8), (13.5, 8)) + line((2.5, 12), (13.5, 12)),
    "view-more":    _dot(3.5, 8, 1.1) + _dot(8, 8, 1.1) + _dot(12.5, 8, 1.1),
    "view-more-horizontal": _dot(3.5, 8, 1.1) + _dot(8, 8, 1.1) + _dot(12.5, 8, 1.1),
    "view-list":    line((2.5, 4), (13.5, 4)) + line((2.5, 8), (13.5, 8)) + line((2.5, 12), (13.5, 12)),
    "view-grid":    line((2.5, 2.5), (6.8, 2.5), (6.8, 6.8), (2.5, 6.8), (2.5, 2.5)) + line((9.2, 2.5), (13.5, 2.5), (13.5, 6.8), (9.2, 6.8), (9.2, 2.5))
                    + line((2.5, 9.2), (6.8, 9.2), (6.8, 13.5), (2.5, 13.5), (2.5, 9.2)) + line((9.2, 9.2), (13.5, 9.2), (13.5, 13.5), (9.2, 13.5), (9.2, 9.2)),
    "process-working": arc(8, 8, 5.6, -90, 180, n=36, w=1.5),
    "process-stop": line((4, 4), (12, 12)) + line((12, 4), (4, 12)),
}

# Solid arrows for scrollbar buttons (Windows 10 style). These ship inside the GTK
# theme (gtk-3.0/assets) so they work with any icon theme.
SCROLL_ARROWS = {
    "scroll-up":    '<path d="M8 5.2L12.2 10H3.8z"/>',
    "scroll-down":  '<path d="M8 10.8L3.8 6h8.4z"/>',
    "scroll-left":  '<path d="M5.2 8L10 3.8v8.4z"/>',
    "scroll-right": '<path d="M10.8 8L6 12.2V3.8z"/>',
}

if __name__ == "__main__":
    # Usage: python3 symbolic.py GTK3_ASSETS_DIR
    import os, sys
    os.makedirs(sys.argv[1], exist_ok=True)
    for n, b in SCROLL_ARROWS.items():
        with open(os.path.join(sys.argv[1], n + "-symbolic.svg"), "w") as f:
            f.write(sym(b))
    print("scrollbar arrows:", len(SCROLL_ARROWS))


# ---------------------------------------------------------------------------
# Thin system-tray glyphs (network, notifications, power, volume). Drawn with
# a ~1 px stroke inside an ~11 px area of the 16 px grid, so they read smaller
# and lighter in the panel, closer to Windows 10 tray icons.
# ---------------------------------------------------------------------------
TW = 1.0


def bez(p0, p1, p2, p3, n=10):
    pts = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return pts


def poly(*pts, w=TW):
    return line(*pts, w=w)


def faint(svg_body, op=0.35):
    return f'<g opacity="{op}">{svg_body}</g>'


# Bell
_bell_l = bez((4.6, 10.6), (5.0, 9.4), (4.6, 4.0), (8.0, 3.6))
_bell_r = bez((8.0, 3.6), (11.4, 4.0), (11.0, 9.4), (11.4, 10.6))
BELL = (poly(*_bell_l, *_bell_r[1:]) + poly((3.6, 10.8), (12.4, 10.8))
        + arc(8, 11.6, 1.25, 0, 180, n=10, w=TW) + _dot(8, 2.9, 0.55))
SLASH = poly((3.2, 3.2), (12.8, 12.8))

# Speaker
SPEAKER = poly((3.0, 6.4), (5.0, 6.4), (7.6, 4.0), (7.6, 12.0), (5.0, 9.6), (3.0, 9.6), (3.0, 6.4))
def waves(n):
    return "".join(arc(7.6, 8, r, -42, 42, n=12, w=TW) for r in (2.3, 4.1, 5.9)[:n])
MUTE_X = poly((10.0, 6.3), (13.2, 9.7)) + poly((13.2, 6.3), (10.0, 9.7))

# Monitor (wired network)
MONITOR = (poly((2.8, 3.6), (13.2, 3.6), (13.2, 10.4), (2.8, 10.4), (2.8, 3.6))
           + poly((8, 10.4), (8, 12.4)) + poly((5.6, 12.6), (10.4, 12.6)))
def wifi(n):
    arcs = [arc(8, 12.4, r, -135, -45, n=14, w=TW) for r in (2.6, 5.0, 7.4)]
    body = _dot(8, 12.4, 0.9)
    for i, a in enumerate(arcs):
        body += a if i < n else faint(a)
    return body

# Plug and battery
PLUG = (poly((6.3, 2.6), (6.3, 5.0)) + poly((9.7, 2.6), (9.7, 5.0))
        + poly((4.6, 5.0), (11.4, 5.0), (11.4, 7.8), (9.4, 10.2), (6.6, 10.2), (4.6, 7.8), (4.6, 5.0))
        + poly((8, 10.2), (8, 13.4)))
BATT = poly((2.6, 5.2), (12.4, 5.2), (12.4, 10.8), (2.6, 10.8), (2.6, 5.2)) + '<path d="M12.9 6.9h1.2v2.2h-1.2z"/>'
def batt(level):
    w = 8.2 * level / 100
    return BATT + (f'<path d="M3.5 6.1h{w:.2f}v3.8h-{w:.2f}z"/>' if w > 0.2 else "")
BOLT = '<path d="M8.6 5.4L5.6 8.4h2.2L7.2 10.8l3.2-3.2H8.2z"/>'

TRAY = {
    "notification": BELL, "notifications": BELL,
    "notification-disabled": BELL + SLASH, "notifications-disabled": BELL + SLASH,
    "audio-volume-high": SPEAKER + waves(3), "audio-volume-overamplified": SPEAKER + waves(3),
    "audio-volume-medium": SPEAKER + waves(2), "audio-volume-low": SPEAKER + waves(1),
    "audio-volume-muted": SPEAKER + MUTE_X, "audio-volume-off": SPEAKER + MUTE_X,
    "audio-volume-muted-blocking": SPEAKER + MUTE_X,
    "network-wired": MONITOR, "nm-device-wired": MONITOR, "network-transmit-receive": MONITOR,
    "network-idle": MONITOR, "network-wired-acquiring": MONITOR + _dot(5.6, 7, 0.7) + _dot(8, 7, 0.7) + _dot(10.4, 7, 0.7),
    "network-wired-disconnected": MONITOR + SLASH, "network-wired-offline": MONITOR + SLASH,
    "network-wired-no-route": MONITOR + SLASH, "network-offline": MONITOR + SLASH,
    "network-error": MONITOR + SLASH, "nm-no-connection": MONITOR + SLASH,
    "network-wireless-signal-excellent": wifi(3), "network-wireless-connected": wifi(3),
    "network-wireless-signal-good": wifi(2), "network-wireless-signal-ok": wifi(2),
    "network-wireless-signal-weak": wifi(1), "network-wireless-signal-none": wifi(0),
    "network-wireless-acquiring": wifi(0), "network-wireless-offline": wifi(0) + SLASH,
    "network-wireless-disconnected": wifi(0) + SLASH, "network-wireless-no-route": wifi(0) + SLASH,
    "ac-adapter": PLUG, "battery-missing": BATT + SLASH,
    "battery-full-charged": batt(100), "battery-full-charging": BATT + BOLT,
}
for name, lvl in (("full", 100), ("good", 70), ("low", 30), ("caution", 15), ("empty", 0)):
    TRAY[f"battery-{name}"] = batt(lvl)
    TRAY.setdefault(f"battery-{name}-charging", BATT + BOLT)
for lvl in range(0, 101, 10):
    TRAY[f"battery-level-{lvl}"] = batt(lvl)
    TRAY[f"battery-level-{lvl}-charging"] = BATT + BOLT
TRAY["battery-level-100-charged"] = batt(100)

# nm-applet asks for NON-symbolic names, which GTK does not recolor, so these
# are generated in two fixed colors (see icons.py: panel-dark / panel-light).
NM_PANEL = {
    "nm-device-wired": MONITOR, "nm-no-connection": MONITOR + SLASH,
    "nm-device-wireless": wifi(3),
    "nm-signal-100": wifi(3), "nm-signal-75": wifi(3), "nm-signal-50": wifi(2),
    "nm-signal-25": wifi(1), "nm-signal-00": wifi(0),
    "nm-vpn-active-lock": MONITOR, "nm-device-wwan": wifi(3),
}
NM_CONNECTING = MONITOR + _dot(5.6, 7, 0.7) + _dot(8, 7, 0.7) + _dot(10.4, 7, 0.7)


def colored(body, color):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
            f'<g fill="{color}">{body}</g></svg>\n')
