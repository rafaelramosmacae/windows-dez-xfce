# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""Builds the windows-dez-light GTK theme from windows-dez.
Usage: python3 variants.py THEMES_DIR   (the folder that contains windows-dez/)"""
import os, shutil, sys

root = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
src, dst = os.path.join(root, "windows-dez"), os.path.join(root, "windows-dez-light")
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns("xfwm4"))

with open(os.path.join(here, "light.css")) as f:
    light = f.read()
with open(os.path.join(dst, "gtk-3.0", "gtk.css"), "a") as f:
    f.write(light)
shutil.copy(os.path.join(here, "light-notify.css"), os.path.join(dst, "xfce-notify-4.0", "gtk.css"))

# GTK 2: light panel colors
rc = os.path.join(dst, "gtk-2.0", "gtkrc")
with open(rc) as f:
    g = f.read()
start = g.index('style "dez-panel"'); end = g.index("}", start) + 1
g = g[:start] + """style "dez-panel" {
  bg[NORMAL]   = "#EEEEEE"
  bg[PRELIGHT] = "#DCDCDC"
  bg[ACTIVE]   = "#D0D0D0"
  bg[SELECTED] = "#D0D0D0"
  fg[NORMAL]   = "#000000"
  fg[PRELIGHT] = "#000000"
  fg[ACTIVE]   = "#000000"
  fg[SELECTED] = "#000000"
  text[NORMAL] = "#000000"
}""" + g[end:]
with open(rc, "w") as f:
    f.write(g)

idx = os.path.join(dst, "index.theme")
with open(idx) as f:
    s = f.read()
s = (s.replace("Name=windows-dez", "Name=windows-dez-light")
      .replace("GtkTheme=windows-dez", "GtkTheme=windows-dez-light")
      .replace("Comment=Flat XFCE theme inspired by Windows 10",
               "Comment=Flat XFCE theme inspired by Windows 10 (light taskbar and Start menu)"))
with open(idx, "w") as f:
    f.write(s)
print("built", dst)
