# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""Builds the windows-dez-light and windows-dez-dark GTK themes from windows-dez,
and the windows-dez-dark-icons icon theme from windows-dez-icons.
Usage: python3 variants.py THEMES_DIR   (the folder that contains windows-dez/)"""
import os, re, shutil, subprocess, sys

root = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(root, "windows-dez")


def read(path):
    with open(path) as f:
        return f.read()


def write(path, text):
    with open(path, "w") as f:
        f.write(text)


def copy_theme(name, with_xfwm=False):
    dst = os.path.join(root, name)
    shutil.rmtree(dst, ignore_errors=True)
    ignore = None if with_xfwm else shutil.ignore_patterns("xfwm4")
    shutil.copytree(src, dst, symlinks=True, ignore=ignore)
    return dst


def set_index(dst, name, comment_suffix, metacity="windows-dez", icons="windows-dez"):
    idx = os.path.join(dst, "index.theme")
    s = read(idx)
    s = (s.replace("Name=windows-dez", f"Name={name}")
          .replace("GtkTheme=windows-dez", f"GtkTheme={name}")
          .replace("MetacityTheme=windows-dez", f"MetacityTheme={metacity}")
          .replace("IconTheme=windows-dez", f"IconTheme={icons}")
          .replace("Comment=Flat XFCE theme inspired by Windows 10",
                   f"Comment=Flat XFCE theme inspired by Windows 10 ({comment_suffix})"))
    write(idx, s)


def replace_style(g, style, body):
    start = g.index(f'style "{style}"')
    end = g.index("}", start) + 1
    return g[:start] + f'style "{style}" {{\n{body}\n}}' + g[end:]


# ---------------------------------------------------------------- light
dst = copy_theme("windows-dez-light")
with open(os.path.join(dst, "gtk-3.0", "gtk.css"), "a") as f:
    f.write(read(os.path.join(here, "light.css")))
shutil.copy(os.path.join(here, "light-notify.css"), os.path.join(dst, "xfce-notify-4.0", "gtk.css"))

rc = os.path.join(dst, "gtk-2.0", "gtkrc")
g = replace_style(read(rc), "dez-panel", """  bg[NORMAL]   = "#EEEEEE"
  bg[PRELIGHT] = "#DCDCDC"
  bg[ACTIVE]   = "#D0D0D0"
  bg[SELECTED] = "#D0D0D0"
  fg[NORMAL]   = "#000000"
  fg[PRELIGHT] = "#000000"
  fg[ACTIVE]   = "#000000"
  fg[SELECTED] = "#000000"
  text[NORMAL] = "#000000\"""")
write(rc, g)
set_index(dst, "windows-dez-light", "light taskbar and Start menu")
print("built", dst)

# ---------------------------------------------------------------- dark
# Full dark mode: windows, dialogs and applications are dark too. It has its
# own xfwm4 borders (dark title bars) and uses the windows-dez-dark icons.
dst = copy_theme("windows-dez-dark")
with open(os.path.join(dst, "gtk-3.0", "gtk.css"), "a") as f:
    f.write(read(os.path.join(here, "dark.css")))
subprocess.run([sys.executable, os.path.join(here, "xfwm.py"), os.path.join(dst, "xfwm4"), "--dark"], check=True)

rc = os.path.join(dst, "gtk-2.0", "gtkrc")
g = read(rc)
g = g.replace("# windows-dez — GTK 2 theme (legacy apps).", "# windows-dez-dark — GTK 2 theme (legacy apps), full dark mode.")
g = re.sub(r'gtk-color-scheme = ".*"',
           'gtk-color-scheme = "bg_color:#202020\\\\nfg_color:#FFFFFF\\\\nbase_color:#191919\\\\ntext_color:#FFFFFF'
           '\\\\nselected_bg_color:#0078D7\\\\nselected_fg_color:#FFFFFF\\\\ntooltip_bg_color:#2B2B2B\\\\ntooltip_fg_color:#FFFFFF"', g)
pairs = {
    'GtkWidget::link-color       = "#0066CC"': 'GtkWidget::link-color       = "#4CC2FF"',
    'GtkWidget::visited-link-color = "#5C2D91"': 'GtkWidget::visited-link-color = "#C3A6FF"',
    'bg[PRELIGHT]      = "#E5F1FB"': 'bg[PRELIGHT]      = "#3A3A3A"',
    'bg[ACTIVE]        = "#CCE4F7"': 'bg[ACTIVE]        = "#4D4D4D"',
    'fg[INSENSITIVE]   = "#838383"': 'fg[INSENSITIVE]   = "#7A7A7A"',
    'base[PRELIGHT]    = "#E5F3FF"': 'base[PRELIGHT]    = "#2D2D2D"',
    'base[SELECTED]    = "#CCE8FF"': 'base[SELECTED]    = "#4D4D4D"',
    'base[ACTIVE]      = "#D9D9D9"': 'base[ACTIVE]      = "#3A3A3A"',
    'base[INSENSITIVE] = "#F7F7F7"': 'base[INSENSITIVE] = "#262626"',
    'text[INSENSITIVE] = "#838383"': 'text[INSENSITIVE] = "#7A7A7A"',
}
for a, b in pairs.items():
    assert a in g, a
    g = g.replace(a, b)
g = replace_style(g, "dez-button", """  bg[NORMAL]   = "#333333"
  bg[PRELIGHT] = "#3D3D3D"
  bg[ACTIVE]   = "#4D4D4D\"""")
g = replace_style(g, "dez-menu", """  xthickness = 1
  ythickness = 2
  bg[NORMAL]   = "#2B2B2B"
  bg[PRELIGHT] = "#414141"
  bg[SELECTED] = "#414141"
  fg[NORMAL]   = "#FFFFFF"
  fg[PRELIGHT] = "#FFFFFF"
  fg[SELECTED] = "#FFFFFF"
  text[NORMAL] = "#FFFFFF"
  text[PRELIGHT] = "#FFFFFF\"""")
g = replace_style(g, "dez-menubar", """  bg[NORMAL]   = "#202020"
  bg[PRELIGHT] = "#414141"
  bg[SELECTED] = "#414141"
  fg[NORMAL]   = "#FFFFFF"
  fg[PRELIGHT] = "#FFFFFF"
  fg[SELECTED] = "#FFFFFF\"""")
g = replace_style(g, "dez-scrollbar", """  bg[NORMAL]   = "#4D4D4D"
  bg[PRELIGHT] = "#7A7A7A"
  bg[ACTIVE]   = "#171717\"""")
g = replace_style(g, "dez-progress", """  bg[SELECTED] = "#0078D7"
  bg[NORMAL]   = "#333333\"""")
write(rc, g)
set_index(dst, "windows-dez-dark", "full dark mode", metacity="windows-dez-dark", icons="windows-dez-dark")
print("built", dst)

# ---------------------------------------------------------------- dark icons
# A full copy of the icon theme (the theme inherits elementary-xfce-dark, so
# icons that are not drawn here also come in their dark-mode version), with
# the thin-line action icons (toolbar, menus) drawn light instead of dark grey.
isrc = os.path.join(root, "windows-dez-icons")
idst = os.path.join(root, "windows-dez-dark-icons")
shutil.rmtree(idst, ignore_errors=True)
shutil.copytree(isrc, idst, symlinks=True)
recolored = 0
for dirpath, _, files in os.walk(os.path.join(idst, "scalable", "actions")):
    for n in files:
        p = os.path.join(dirpath, n)
        if os.path.islink(p) or n.endswith("-symbolic.svg"):
            continue
        s = read(p)
        t = s.replace('stroke="#333"', 'stroke="#E6E6E6"')
        if t != s:
            write(p, t)
            recolored += 1
idx = os.path.join(idst, "index.theme")
s = read(idx)
s = (s.replace("Name=windows-dez", "Name=windows-dez-dark")
      .replace("Inherits=elementary-xfce,", "Inherits=elementary-xfce-dark,elementary-xfce,")
      .replace("inspired by Windows 10", "inspired by Windows 10 (full dark mode)"))
write(idx, s)
print("built", idst, f"({recolored} action icons recolored)")
