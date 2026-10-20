#!/usr/bin/env bash
# windows-dez — installer for XFCE
# Author: Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — License: GPL-3.0-or-later
# Usage: ./install.sh [--full] [--light|--dark|--fulldark] [--taskbar] [--wallpaper[=FILE]] [--start-icon=FILE] [--system] [--no-apply]
set -euo pipefail

NAME=windows-dez
VERSION=1.2.0

restart_panel() {
  pgrep -x xfce4-panel >/dev/null || return 0
  timeout 8 xfce4-panel -r >/dev/null 2>&1 || true
  for _ in 1 2 3 4 5 6; do sleep 0.5; pgrep -x xfce4-panel >/dev/null && return 0; done
  (setsid xfce4-panel >/dev/null 2>&1 &)
}

usage() {
  cat <<EOF
$NAME $VERSION — Windows 10 inspired theme for XFCE
by Rafael Carvalho Ramos <rafaelramosmacae@gmail.com>

Usage: ./install.sh [options]

  (no options)          install and apply GTK theme, icons, window borders, notifications and font
  --dark                dark taskbar, Start menu and notifications (default)
  --light               light taskbar, Start menu and notifications
  --fulldark            full dark mode: dark windows, file manager, settings, menus and title bars,
                        plus the dark taskbar, Start menu and notifications
  --taskbar             bottom panel, 33 px, full width, Start button without label, flat window buttons,
                        Start menu laid out like Windows 10 (category icons on the left, switched by
                        hovering, all apps A-Z, search box, user and power buttons at the bottom),
                        taskbar buttons reorderable by drag-and-drop
  --wallpaper           apply the theme wallpaper on every monitor
  --wallpaper=FILE      apply your own image (jpg/png) on every monitor
  --start-icon=FILE     use your own image (svg/png) for the Start button
  --full, --complete    --taskbar + --wallpaper + smaller desktop icons (36 px, tooltips 48 px)
  --system              install for all users in /usr/share (requires sudo)
  --no-apply            only copy the files, do not change any settings
  -h, --help            show this help

Undo everything with ./uninstall.sh
EOF
}

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STYLE=dark; SYSTEM=0; APPLY=1; TASKBAR=0; WALLPAPER=0; DESKTOP_ICONS=0; WALLPAPER_FILE=""; START_ICON_FILE=""

for arg in "$@"; do
  case "$arg" in
    --light)             STYLE=light ;;
    --dark)              STYLE=dark ;;
    --fulldark)          STYLE=fulldark ;;
    --system)            SYSTEM=1 ;;
    --no-apply)          APPLY=0 ;;
    --taskbar)           TASKBAR=1 ;;
    --wallpaper)         WALLPAPER=1 ;;
    --wallpaper=*)       WALLPAPER=1; WALLPAPER_FILE="${arg#*=}" ;;
    --start-icon=*)      START_ICON_FILE="${arg#*=}" ;;
    --full|--complete)   TASKBAR=1; WALLPAPER=1; DESKTOP_ICONS=1 ;;
    -h|--help)           usage; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)"; exit 1 ;;
  esac
done

# Expand ~ and make paths absolute
absolute() {
  local f="${1/#\~/$HOME}"
  [ -f "$f" ] || { echo "File not found: $1" >&2; exit 1; }
  echo "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
}
[ -n "$WALLPAPER_FILE" ] && WALLPAPER_FILE="$(absolute "$WALLPAPER_FILE")"
[ -n "$START_ICON_FILE" ] && START_ICON_FILE="$(absolute "$START_ICON_FILE")"

if [ "$SYSTEM" = 1 ]; then
  [ "$(id -u)" = 0 ] || { echo "Run with sudo to use --system."; exit 1; }
  THEMES=/usr/share/themes; ICONS=/usr/share/icons; BACKGROUNDS=/usr/share/backgrounds/$NAME
else
  THEMES="$HOME/.themes"; ICONS="$HOME/.icons"; BACKGROUNDS="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/$NAME"
fi

echo "› Copying files…"
mkdir -p "$THEMES" "$ICONS" "$BACKGROUNDS"
rm -rf "$THEMES/$NAME" "$THEMES/$NAME-light" "$THEMES/$NAME-dark" "$ICONS/$NAME" "$ICONS/$NAME-dark"
cp -a "$HERE/$NAME" "$THEMES/$NAME"
cp -a "$HERE/$NAME-light" "$THEMES/$NAME-light"
cp -a "$HERE/$NAME-dark" "$THEMES/$NAME-dark"
cp -a "$HERE/$NAME-icons" "$ICONS/$NAME"
cp -a "$HERE/$NAME-dark-icons" "$ICONS/$NAME-dark"
cp -a "$HERE/wallpaper/." "$BACKGROUNDS/"
# Earlier builds shipped an abstract wallpaper that the "Glass" wallpaper replaces
rm -f "$BACKGROUNDS/$NAME-abstract-1920x1080.jpg" "$BACKGROUNDS/$NAME-abstract-3840x2160.jpg"

# User-supplied images are copied next to the theme so they survive deleting the originals
if [ -n "$WALLPAPER_FILE" ]; then
  cp -f "$WALLPAPER_FILE" "$BACKGROUNDS/custom.${WALLPAPER_FILE##*.}"
  WALLPAPER_FILE="$BACKGROUNDS/custom.${WALLPAPER_FILE##*.}"
fi
if [ -n "$START_ICON_FILE" ]; then
  mkdir -p "$ICONS/$NAME/custom"
  cp -f "$START_ICON_FILE" "$ICONS/$NAME/custom/start.${START_ICON_FILE##*.}"
  START_ICON_FILE="$ICONS/$NAME/custom/start.${START_ICON_FILE##*.}"
fi

# Network tray icons (nm-applet) are not recolored by GTK: use the set that
# matches the taskbar style (white glyphs on dark, dark glyphs on light)
# (the full dark mode always has a dark taskbar)
if [ "$STYLE" = light ]; then PANEL_STYLE=light; else PANEL_STYLE=dark; fi
if [ -d "$ICONS/$NAME/panel-variants/$PANEL_STYLE" ]; then
  rm -rf "$ICONS/$NAME/scalable/panel"
  cp -a "$ICONS/$NAME/panel-variants/$PANEL_STYLE" "$ICONS/$NAME/scalable/panel"
fi
if command -v gtk-update-icon-cache >/dev/null; then
  gtk-update-icon-cache -f -t -q "$ICONS/$NAME" || true
  gtk-update-icon-cache -f -t -q "$ICONS/$NAME-dark" || true
fi
echo "  themes:      $THEMES/$NAME, $THEMES/$NAME-light, $THEMES/$NAME-dark"
echo "  icons:       $ICONS/$NAME, $ICONS/$NAME-dark"
echo "  wallpapers:  $BACKGROUNDS"

[ "$APPLY" = 1 ] || { echo "Done (settings left unchanged)."; exit 0; }
if ! command -v xfconf-query >/dev/null; then
  echo "xfconf-query not found — pick the theme in Settings › Appearance and Window Manager."
  exit 0
fi

# ---------- backup of current settings ----------
BACKUP_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/$NAME"
BACKUP="$BACKUP_DIR/backup.tsv"
mkdir -p "$BACKUP_DIR"
OLD_BACKUP="${XDG_CONFIG_HOME:-$HOME/.config}/dez-tema/backup.tsv"   # pre-rename builds ("Dez")
save() {  # channel property
  local v
  [ -f "$BACKUP" ] && grep -q "^$1	$2	" "$BACKUP" && return 0
  if [ -f "$OLD_BACKUP" ] && grep -q "^$1	$2	" "$OLD_BACKUP"; then
    # an older build already changed this setting: its backup holds the true original
    v="$(grep "^$1	$2	" "$OLD_BACKUP" | head -1 | cut -f3-)"
  else
    v="$(xfconf-query -c "$1" -p "$2" 2>/dev/null || true)"
  fi
  # Never record one of this theme's own values as the "original" (e.g. after a
  # lost backup): restoring it later would point at files the uninstaller removes
  case "$v" in
    start-here|"$NAME-start-light"|"$NAME"|"$NAME-light"|"$NAME-dark"|Dez|*"/$NAME/"*|*"/$NAME-dark/"*|*"/Dez/"*) v="" ;;
  esac
  printf '%s\t%s\t%s\n' "$1" "$2" "$v" >> "$BACKUP"
}
set_prop() {  # channel property type value
  save "$1" "$2"
  xfconf-query -c "$1" -p "$2" -s "$4" 2>/dev/null || xfconf-query -c "$1" -p "$2" -n -t "$3" -s "$4"
}

echo "› Applying theme (backup in $BACKUP)…"
case "$STYLE" in
  light)     GTK_THEME="$NAME-light"; ICON_THEME="$NAME";      WM_THEME="$NAME" ;;
  fulldark)  GTK_THEME="$NAME-dark";  ICON_THEME="$NAME-dark"; WM_THEME="$NAME-dark" ;;
  *)         GTK_THEME="$NAME";       ICON_THEME="$NAME";      WM_THEME="$NAME" ;;
esac
echo "  style: $STYLE"
set_prop xsettings /Net/ThemeName string "$GTK_THEME"
set_prop xsettings /Net/IconThemeName string "$ICON_THEME"
set_prop xfwm4 /general/theme string "$WM_THEME"
# (XFCE 4.18+ also switches the desktop color scheme to dark for themes whose
# name ends in "-dark", so GTK 4/libadwaita apps and Firefox follow --fulldark)
set_prop xfwm4 /general/button_layout string "O|HMC"
set_prop xfwm4 /general/title_alignment string left
set_prop xfce4-notifyd /theme string "$GTK_THEME"
# Classic, always-visible scrollbars (with arrow buttons) instead of overlay indicators
set_prop xsettings /Gtk/OverlayScrolling bool false

# Font: Segoe UI if installed, otherwise Noto Sans / Open Sans
FONT=""
for f in "Segoe UI" "Noto Sans" "Open Sans"; do
  if [ -n "$(fc-list ":family=$f" 2>/dev/null)" ]; then FONT="$f"; break; fi
done
if [ -n "$FONT" ]; then
  set_prop xsettings /Gtk/FontName string "$FONT 9"
  set_prop xfwm4 /general/title_font string "$FONT 9"
  echo "  font: $FONT 9"
fi

# ---------- Start button ----------
if [ "$STYLE" = light ]; then DEFAULT_START_ICON="$NAME-start-light"; else DEFAULT_START_ICON="start-here"; fi
START_ICON="${START_ICON_FILE:-$DEFAULT_START_ICON}"
apply_start_icon() {
  local id rc
  for id in $(xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null | awk '$2=="whiskermenu"{print $1}'); do
    set_prop xfce4-panel "$id/button-icon" string "$START_ICON"
    set_prop xfce4-panel "$id/show-button-title" bool false
    rc="${XDG_CONFIG_HOME:-$HOME/.config}/xfce4/panel/whiskermenu-${id##*-}.rc"
    if [ -f "$rc" ]; then
      cp -n "$rc" "$rc.$NAME-backup"
      sed -i "s|^button-icon=.*|button-icon=$START_ICON|; s|^show-button-title=.*|show-button-title=false|" "$rc"
    fi
  done
  for id in $(xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null | awk '$2=="applicationsmenu"{print $1}'); do
    set_prop xfce4-panel "$id/button-icon" string "$START_ICON"
    set_prop xfce4-panel "$id/show-button-title" bool false
  done
}

# ---------- taskbar ----------
if [ "$TASKBAR" = 1 ]; then
  echo "› Turning panel 1 into a taskbar…"
  P=/panels/panel-1
  set_prop xfce4-panel $P/position string "p=8;x=0;y=0"
  set_prop xfce4-panel $P/position-locked bool true
  set_prop xfce4-panel $P/mode uint 0
  set_prop xfce4-panel $P/size uint 33
  set_prop xfce4-panel $P/icon-size uint 24
  set_prop xfce4-panel $P/background-style uint 0
  save xfce4-panel $P/length
  xfconf-query -c xfce4-panel -p $P/length -s 100 2>/dev/null \
    || xfconf-query -c xfce4-panel -p $P/length -s 100.0 2>/dev/null \
    || xfconf-query -c xfce4-panel -p $P/length -n -t uint -s 100 2>/dev/null || true

  apply_start_icon
  # Whisker Menu laid out like the Windows 10 Start menu: a narrow rail of
  # category icons on the left (switched by hovering), all applications in
  # alphabetical order with plain names, then the search box and the user
  # picture with the settings, lock and power buttons at the bottom
  WHISKER_SETTINGS="position-categories-alternate:bool:true hover-switch-category:bool:true
    category-show-name:bool:false category-icon-size:int:1 default-category:int:2 view-mode:int:1
    launcher-show-description:bool:false launcher-icon-size:int:1
    position-search-alternate:bool:true position-profile-alternate:bool:true
    position-commands-alternate:bool:false menu-width:int:400 menu-height:int:640"
  for id in $(xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null | awk '$2=="whiskermenu"{print $1}'); do
    kvs=""
    for s in $WHISKER_SETTINGS; do
      k="${s%%:*}"; t="${s#*:}"; t="${t%%:*}"; v="${s##*:}"
      set_prop xfce4-panel "$id/$k" "$t" "$v"
      kvs="$kvs $k=$v"
    done
    rc="${XDG_CONFIG_HOME:-$HOME/.config}/xfce4/panel/whiskermenu-${id##*-}.rc"
    if [ -f "$rc" ]; then   # older Whisker Menu versions keep settings in an rc file
      cp -n "$rc" "$rc.$NAME-backup"
      for kv in $kvs; do
        k="${kv%%=*}"
        if grep -q "^$k=" "$rc"; then sed -i "s|^$k=.*|$kv|" "$rc"; else echo "$kv" >> "$rc"; fi
      done
    fi
  done
  # Window list: no drag handle, flat buttons
  for id in $(xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null | awk '$2=="tasklist"{print $1}'); do
    set_prop xfce4-panel "$id/show-handle" bool false
    set_prop xfce4-panel "$id/flat-buttons" bool true
    # Sorting order: "None, allow drag-and-drop" (lets you reorder open apps)
    set_prop xfce4-panel "$id/sort-order" uint 4
  done
  # Narrower taskbar buttons and smaller labels. XFCE 4.20 applies these style
  # properties reliably only from the user's gtk.css (see docs.xfce.org, Window
  # Buttons > Style Properties), so a marked block is added there too.
  USER_CSS="${XDG_CONFIG_HOME:-$HOME/.config}/gtk-3.0/gtk.css"
  mkdir -p "$(dirname "$USER_CSS")"
  [ -f "$USER_CSS" ] && sed -i '/\/\* windows-dez:begin/,/\/\* windows-dez:end \*\//d' "$USER_CSS"
  cat >> "$USER_CSS" <<'CSS'
/* windows-dez:begin — added by the windows-dez installer, removed by uninstall.sh */
.tasklist { -XfceTasklist-max-button-length: 140;
  -XfceTasklist-min-button-length: 140; }
.tasklist button label { font-size: 8pt; }
/* windows-dez:end */
CSS
  restart_panel
  echo "  (if you had a second panel at the bottom, move or remove it in Settings › Panel)"
elif [ -n "$START_ICON_FILE" ]; then
  echo "› Applying custom Start button icon…"
  apply_start_icon
  restart_panel
else
  # Switching between --light, --dark and --fulldark: keep the theme's own Start glyph readable
  changed=0
  for id in $(xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null | awk '$2=="whiskermenu" || $2=="applicationsmenu"{print $1}'); do
    cur="$(xfconf-query -c xfce4-panel -p "$id/button-icon" 2>/dev/null || true)"
    if [ "$cur" = start-here ] || [ "$cur" = "$NAME-start-light" ]; then
      [ "$cur" = "$START_ICON" ] || { set_prop xfce4-panel "$id/button-icon" string "$START_ICON"; changed=1; }
    fi
  done
  if [ "$changed" = 1 ]; then restart_panel; fi
fi

# ---------- desktop icons (--full only) ----------
if [ "$DESKTOP_ICONS" = 1 ]; then
  echo "› Setting desktop icons to 36 px (tooltips 48 px)…"
  set_prop xfce4-desktop /desktop-icons/icon-size uint 36
  set_prop xfce4-desktop /desktop-icons/tooltip-size double 48
fi

# ---------- wallpaper ----------
if [ "$WALLPAPER" = 1 ]; then
  echo "› Applying wallpaper…"
  if [ -n "$WALLPAPER_FILE" ]; then
    IMG="$WALLPAPER_FILE"
  elif [ -f "$HERE/wallpaper/$NAME-default.jpg" ]; then
    IMG="$BACKGROUNDS/$NAME-default.jpg"
  else
    IMG="$BACKGROUNDS/$NAME-glass-3840x2160.jpg"
  fi
  PROPS="$(xfconf-query -c xfce4-desktop -l 2>/dev/null | grep -E '/last-image$' || true)"
  if [ -z "$PROPS" ] && command -v xrandr >/dev/null; then
    for m in $(xrandr --listactivemonitors 2>/dev/null | awk 'NR>1{print $NF}'); do
      for w in 0 1 2 3; do PROPS="$PROPS /backdrop/screen0/monitor$m/workspace$w/last-image"; done
    done
  fi
  for p in $PROPS; do
    set_prop xfce4-desktop "$p" string "$IMG"
    set_prop xfce4-desktop "${p%/last-image}/image-style" int 5
  done
fi

echo "✓ $NAME $VERSION installed. To undo: ./uninstall.sh"
echo "  Log out and back in so every application picks up the theme."
