#!/usr/bin/env bash
# windows-dez — installer for XFCE
# Author: Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — License: GPL-3.0-or-later
# Usage: ./install.sh            (interactive menu)
#        ./install.sh [options]  (for scripts, see --help)
set -euo pipefail

NAME=windows-dez
VERSION=1.2.3

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

Usage: ./install.sh             interactive menu: answer each question and press Enter
       ./install.sh [options]   no questions, for scripts and advanced use

Options:
  (none of these)       the interactive menu
  --dark                dark taskbar, Start menu and notifications (default)
  --light               light taskbar, Start menu and notifications
  --fulldark            full dark mode: dark windows, file manager, settings, menus and title bars,
                        plus the dark taskbar, Start menu and notifications
  --taskbar             bottom panel, 32 px, full width, Start button without label, flat window buttons,
                        Start menu laid out like Windows 10 (category icons on the left, switched by
                        hovering, all apps A-Z, search box, user and power buttons at the bottom),
                        taskbar buttons reorderable by drag-and-drop
  --wallpaper           apply the theme wallpaper on every monitor
  --wallpaper=FILE      apply your own image (jpg/png) on every monitor
  --start-icon=FILE     use your own image (svg/png) for the Start button
  --full, --complete    --taskbar + --wallpaper + smaller desktop icons (36 px, tooltips 48 px)
  --system              install for all users in /usr/share (requires sudo)
  --no-apply            only copy the files, do not change any settings
  --theme-only          no questions: install and apply only the GTK theme, icons, window borders,
                        notifications and font (combine with the style options above)
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
    --theme-only)        ;;
    -h|--help)           usage; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)"; exit 1 ;;
  esac
done

# ---------- interactive menu (when run without options) ----------
# Answers are read from the terminal; Enter picks the default shown in [brackets].
ask_choice() {  # ask_choice "Question" "option 1 (default)" "option 2" ... -> sets CHOICE
  local q="$1"; shift
  local n=$# i ans
  echo
  echo "$q"
  i=1; for o in "$@"; do echo "  $i) $o"; i=$((i+1)); done
  while :; do
    read -r -p "Choose 1-$n [1]: " ans </dev/tty || exit 1
    ans="${ans:-1}"
    case "$ans" in
      *[!0-9]*|'') ;;
      *) if [ "$ans" -ge 1 ] && [ "$ans" -le "$n" ]; then CHOICE=$ans; return; fi ;;
    esac
    echo "  Please type a number from 1 to $n."
  done
}
ask_yes_no() {  # ask_yes_no "Question" Y|N -> returns 0 for yes
  local q="$1" def="$2" ans hint="[Y/n]"
  [ "$def" = N ] && hint="[y/N]"
  while :; do
    read -r -p "$q $hint: " ans </dev/tty || exit 1
    ans="${ans:-$def}"
    case "$ans" in
      [Yy]*) return 0 ;;
      [Nn]*) return 1 ;;
    esac
    echo "  Please answer y or n."
  done
}
ask_file() {  # ask_file "Prompt" -> sets FILE_ANSWER ("" = keep the default)
  local ans f
  while :; do
    read -r -p "$1 (Enter = theme default): " ans </dev/tty || exit 1
    [ -z "$ans" ] && { FILE_ANSWER=""; return; }
    f="${ans/#\~/$HOME}"
    [ -f "$f" ] && { FILE_ANSWER="$f"; return; }
    echo "  File not found: $ans"
  done
}

interactive_menu() {
  if ! { [ -r /dev/tty ] && : </dev/tty; } 2>/dev/null; then
    echo "The installer asks a few questions, so run it in a terminal: ./install.sh"
    echo "For scripts, use the options instead: ./install.sh --help"
    exit 1
  fi
  echo "$NAME $VERSION — Windows 10 inspired theme for XFCE"
  echo "Answer each question with its number and press Enter (Enter alone picks the default)."

  ask_choice "Style:" \
    "Dark taskbar and Start menu (default)" \
    "Light taskbar and Start menu" \
    "Full dark mode (windows, file manager and settings dark too)"
  case $CHOICE in 1) STYLE=dark ;; 2) STYLE=light ;; 3) STYLE=fulldark ;; esac

  ask_choice "What to install:" \
    "Complete (recommended): theme + Windows 10 taskbar and Start menu + wallpaper + desktop icons" \
    "Theme only: GTK theme, icons, window borders and notifications (keeps your panel and wallpaper)" \
    "Custom: choose each part" \
    "Copy the files only (change no settings)"
  case $CHOICE in
    1) TASKBAR=1; WALLPAPER=1; DESKTOP_ICONS=1 ;;
    2) ;;
    3) echo
       ask_yes_no "Bottom taskbar (32 px) with the Windows 10 style Start menu?" Y && TASKBAR=1
       ask_yes_no "Theme wallpaper?" Y && WALLPAPER=1
       ask_yes_no "Smaller desktop icons (36 px)?" Y && DESKTOP_ICONS=1 ;;
    4) APPLY=0 ;;
  esac

  if [ "$APPLY" = 1 ] && [ "$WALLPAPER" = 1 ]; then
    ask_choice "Wallpaper:" "Theme wallpaper (default)" "My own image (jpg/png)"
    if [ "$CHOICE" = 2 ]; then ask_file "Image file"; WALLPAPER_FILE="$FILE_ANSWER"; fi
  fi
  if [ "$APPLY" = 1 ] && [ "$TASKBAR" = 1 ]; then
    ask_choice "Start button:" "Theme Start button (default)" "My own image (svg/png)"
    if [ "$CHOICE" = 2 ]; then ask_file "Image file"; START_ICON_FILE="$FILE_ANSWER"; fi
  fi

  ask_choice "Install for:" "Only me (default)" "All users, in /usr/share (needs sudo)"
  if [ "$CHOICE" = 2 ]; then
    if [ "$(id -u)" != 0 ]; then
      echo
      echo "Installing for all users needs administrator rights. Run: sudo ./install.sh"
      exit 1
    fi
    SYSTEM=1
  fi

  echo
  echo "Summary:"
  case $STYLE in dark) echo "  style:      dark taskbar and Start menu" ;;
                 light) echo "  style:      light taskbar and Start menu" ;;
                 fulldark) echo "  style:      full dark mode" ;; esac
  if [ "$APPLY" = 0 ]; then
    echo "  settings:   left unchanged (files only)"
  else
    echo "  taskbar:    $([ "$TASKBAR" = 1 ] && echo "Windows 10 style taskbar and Start menu" || echo "keep my panel")"
    echo "  wallpaper:  $([ "$WALLPAPER" = 1 ] && echo "${WALLPAPER_FILE:-theme wallpaper}" || echo "keep mine")"
    [ "$TASKBAR" = 1 ] && echo "  Start icon: ${START_ICON_FILE:-theme Start button}"
    echo "  desktop:    $([ "$DESKTOP_ICONS" = 1 ] && echo "36 px icons" || echo "keep my icon size")"
  fi
  echo "  for:        $([ "$SYSTEM" = 1 ] && echo "all users (/usr/share)" || echo "only me")"
  echo
  ask_yes_no "Install now?" Y || { echo "Nothing was changed."; exit 0; }
  echo
}
[ $# -eq 0 ] && interactive_menu

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
  set_prop xfce4-panel $P/size uint 32
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
.tasklist { -XfceTasklist-max-button-length: 135;
  -XfceTasklist-min-button-length: 135; }
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
  # xfdesktop (4.12 and later) names these settings after each monitor's output
  # name, e.g. /backdrop/screen0/monitorVirtual-1/workspace0/last-image. Fresh
  # installs (e.g. Debian) may only have older names such as "monitor0", which
  # it ignores, so always add the connected outputs: from xrandr, or from the
  # kernel when xrandr is not installed. Existing last-image settings are kept.
  MONITORS=""
  if command -v xrandr >/dev/null; then
    MONITORS="$(xrandr --listactivemonitors 2>/dev/null | awk 'NR>1{print $NF}' || true)"
    [ -n "$MONITORS" ] || MONITORS="$(xrandr --query 2>/dev/null | awk '$2=="connected"{print $1}' || true)"
  fi
  if [ -z "$MONITORS" ]; then
    for s in /sys/class/drm/card*-*/status; do
      [ -f "$s" ] && [ "$(cat "$s" 2>/dev/null)" = connected ] || continue
      m="$(basename "$(dirname "$s")")"; m="${m#card*-}"
      MONITORS="$MONITORS $m ${m/-A-/-}"   # the X server calls HDMI-A-1 "HDMI-1"
    done
  fi
  PROPS="$(xfconf-query -c xfce4-desktop -l 2>/dev/null | grep -E '/last-image$' || true)"
  for m in $MONITORS; do
    for w in 0 1 2 3; do PROPS="$PROPS /backdrop/screen0/monitor$m/workspace$w/last-image"; done
  done
  PROPS="$(printf '%s\n' $PROPS | sort -u)"
  [ -n "$MONITORS" ] && echo "  monitors: $(echo $MONITORS | tr ' ' '\n' | sort -u | tr '\n' ' ')"
  for p in $PROPS; do
    set_prop xfce4-desktop "$p" string "$IMG"
    set_prop xfce4-desktop "${p%/last-image}/image-style" int 5
  done
fi

echo "✓ $NAME $VERSION installed. To undo: ./uninstall.sh"
echo "  Log out and back in so every application picks up the theme."
