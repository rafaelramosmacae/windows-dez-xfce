#!/usr/bin/env bash
# windows-dez — removes the theme and restores the settings saved by install.sh
# Author: Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — License: GPL-3.0-or-later
# Usage: ./uninstall.sh [--system]
set -uo pipefail

NAME=windows-dez

# Full restart of the panel and desktop, so the restored settings are drawn from
# scratch (a plain "xfce4-panel -r" could leave the Start button blank until the
# next login)
restart_desktop() {
  if pgrep -x xfce4-panel >/dev/null; then
    timeout 5 xfce4-panel --quit >/dev/null 2>&1 || pkill -x xfce4-panel
    for _ in $(seq 1 20); do pgrep -x xfce4-panel >/dev/null || break; sleep 0.25; done
    pkill -9 -x xfce4-panel 2>/dev/null
    (setsid xfce4-panel >/dev/null 2>&1 &)
    for _ in $(seq 1 20); do pgrep -x xfce4-panel >/dev/null && break; sleep 0.25; done
  fi
  if pgrep -x xfdesktop >/dev/null; then
    timeout 5 xfdesktop --reload >/dev/null 2>&1 || true
  fi
}

# Safety net: the Start (menu) button must never end up pointing at this theme's
# icons (which are about to be removed) or with both its icon and label hidden.
ensure_start_button() {
  local id type icon rc def
  xfconf-query -c xfce4-panel -p /plugins -l -v 2>/dev/null \
    | awk '$2=="whiskermenu" || $2=="applicationsmenu" {print $1, $2}' \
    | while read -r id type; do
        def="org.xfce.panel.$type"
        icon="$(xfconf-query -c xfce4-panel -p "$id/button-icon" 2>/dev/null || true)"
        case "$icon" in
          start-here|"$NAME-start-light"|*"/$NAME/"*|*"/$NAME-dark/"*|*"/Dez/"*)
            xfconf-query -c xfce4-panel -p "$id/button-icon" -s "$def" 2>/dev/null \
              || xfconf-query -c xfce4-panel -p "$id/button-icon" -n -t string -s "$def" ;;
        esac
        if [ "$(xfconf-query -c xfce4-panel -p "$id/show-button-icon" 2>/dev/null)" = false ] \
           && [ "$(xfconf-query -c xfce4-panel -p "$id/show-button-title" 2>/dev/null)" = false ]; then
          xfconf-query -c xfce4-panel -p "$id/show-button-icon" -s true
        fi
        if [ "$type" = whiskermenu ]; then   # older Whisker Menu versions use an rc file
          rc="${XDG_CONFIG_HOME:-$HOME/.config}/xfce4/panel/whiskermenu-${id##*-}.rc"
          [ -f "$rc" ] && sed -i -E "s#^button-icon=(start-here|$NAME-start-light|.*/$NAME/.*|.*/$NAME-dark/.*|.*/Dez/.*)\$#button-icon=$def#" "$rc"
        fi
      done
}

if [ "${1:-}" = "--system" ]; then
  THEMES=/usr/share/themes; ICONS=/usr/share/icons; BACKGROUNDS=/usr/share/backgrounds/$NAME
else
  THEMES="$HOME/.themes"; ICONS="$HOME/.icons"; BACKGROUNDS="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/$NAME"
fi

BACKUP="${XDG_CONFIG_HOME:-$HOME/.config}/$NAME/backup.tsv"
if [ -f "$BACKUP" ] && command -v xfconf-query >/dev/null; then
  echo "› Restoring previous settings…"
  while IFS=$'\t' read -r channel prop value; do
    if [ -z "$value" ]; then
      xfconf-query -c "$channel" -p "$prop" -r 2>/dev/null
    else
      xfconf-query -c "$channel" -p "$prop" -s "$value" 2>/dev/null
    fi
  done < "$BACKUP"
  for rc in "${XDG_CONFIG_HOME:-$HOME/.config}"/xfce4/panel/whiskermenu-*.rc.$NAME-backup; do
    [ -f "$rc" ] && mv -f "$rc" "${rc%.$NAME-backup}"
  done
  rm -f "$BACKUP"
  rm -f "${XDG_CONFIG_HOME:-$HOME/.config}/dez-tema/backup.tsv"
  ensure_start_button
  RESTORED=1
fi

if [ "${RESTORED:-0}" = 0 ] && command -v xfconf-query >/dev/null; then
  ensure_start_button
fi

# Remove the taskbar block that install.sh added to the user's gtk.css
USER_CSS="${XDG_CONFIG_HOME:-$HOME/.config}/gtk-3.0/gtk.css"
if [ -f "$USER_CSS" ] && grep -q "windows-dez:begin" "$USER_CSS"; then
  sed -i '/\/\* windows-dez:begin/,/\/\* windows-dez:end \*\//d' "$USER_CSS"
  [ -s "$USER_CSS" ] || rm -f "$USER_CSS"
fi

echo "› Removing files…"
rm -rf "$THEMES/$NAME" "$THEMES/$NAME-light" "$THEMES/$NAME-dark" "$ICONS/$NAME" "$ICONS/$NAME-dark" "$BACKGROUNDS"

# Restart the panel only now, after the theme files are gone
echo "› Restarting the panel…"
restart_desktop

echo "✓ $NAME removed."
echo "  Log out and back in to finish restoring the original look in every application."
