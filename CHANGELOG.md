# Changelog

Windows Dez — by Rafael Carvalho Ramos <rafaelramosmacae@gmail.com>

## 1.2.0 — 2026-10-19

- New full dark mode (`--fulldark`), as requested on xfce-look: besides the dark taskbar, Start menu and notifications, application windows are dark too — Thunar, the XFCE settings dialogs, Mousepad, menus, dialogs, lists, tabs, entries, buttons, check boxes, switches and scrollbars — in the style of the Windows 10 dark app mode
- New `windows-dez-dark` theme (GTK 3, GTK 2, notifications) with its own xfwm4 window borders: dark title bars, white title and buttons, blue border on the active window
- New `windows-dez-dark` icon theme: the thin-line toolbar and menu icons are drawn light, and icons that are not part of the theme fall back to elementary-xfce-dark
- On XFCE 4.18 and later, the desktop color scheme also turns dark with `--fulldark` (XFCE does this for themes whose name ends in `-dark`), so GTK 4/libadwaita apps and Firefox follow the dark mode
- Start menu laid out like the Windows 10 one (`--taskbar` and `--full`): a 72 px rail of category icons (22 px) on the left, all applications from A to Z with plain names, 24 px icons and 8 pt text, the search box below them, and the user picture with the settings, lock and power buttons at the bottom
- New thin white glyphs for the Start menu settings, lock, log out, restart, shut down, switch user, suspend and hibernate buttons (dark in the light style)
- Scrollbar arrow buttons now use thin "boomerang" chevrons like Windows 10, instead of solid triangles
- The divider between side pane and file view (Thunar and other split windows) is now a plain 1 px line instead of a dotted one, and the frame around the status bar text is a bit lighter
- Taskbar window buttons are now 140 px wide (were 150 px)
- `--taskbar` now also sets the panel length to 100% on panels where that setting did not exist yet
- Fixed: the installer help and the README described the window list as "icon-only"; it shows icons and labels

## 1.0.1 — 2026-10-16

- New light style (`--light`): light taskbar, Start menu, panel menus and notifications inspired by Windows 10 light mode, with a dark Start button glyph. `--dark` stays the default
- Switching between `--light` and `--dark` keeps the theme's Start button readable
- `--taskbar` (and `--full`) now also puts the Start menu categories on the left, switches categories on hover and sets the window buttons to "None, allow drag-and-drop" so open apps can be reordered
- Fixed: the "Language Support" settings icon showed as a black flag (the icon theme now falls back to elementary-xfce before Adwaita, and has its own language icon)
- New default wallpaper "Glass": the four diamonds of the Start button as glowing glass panes on the right (1080p and 4K). It replaces the abstract wallpaper
- Trash icons (empty and full) redrawn with a 3D look: a square-section bin in perspective with two shaded faces, glossy ribs and a soft shadow
- Thinner, smaller system-tray icons (network, notifications, power/battery, volume), closer to Windows 10. The network icons follow the taskbar style
- Home folder icon now has the blue base band of the file-manager folder, with the house above it
- Taskbar height is now 33 px (was 35 px)
- Taskbar window buttons are 25% narrower (150 px) with 1 pt smaller labels. On XFCE 4.20, `--taskbar`/`--full` also add these rules to `~/.config/gtk-3.0/gtk.css` (in a marked block that `uninstall.sh` removes), as the XFCE documentation recommends
- Whisker Menu scrollbar arrows now blend with the menu background
- Fixed: after `uninstall.sh` the Start (menu) button could disappear when an earlier build had already been installed. The installer now reuses the backup of older builds and never records the theme's own values as originals, and the uninstaller always leaves the Start button with a visible icon. The uninstaller now removes the files first and then fully restarts the panel and desktop, so the original look comes back right away
- Fixed: in the dark style, the Start menu right-click menu had white text on a light background. It is now dark like the other panel menus, and dark menus use white monochrome icons
- Fixed: LibreOffice Calc cell cursor and selected cells were almost invisible (very light blue). Generic views and text selection now use the full Windows 10 accent blue; lists and folders keep the soft Explorer-style blue

## 1.0.0 — 2026-10-16

First public release.

- GTK 3 and GTK 2 themes, xfwm4 window borders, xfce4-notifyd theme
- Taskbar and Whisker Menu styling (35 px panel, accent underline on the active window)
- Icon theme with 146 original SVG icons and 386 aliases
- Thin-line symbolic icons for navigation, path bar and menus
- Windows 10 style scrollbars: 17 px track with solid arrow buttons at both ends; the installer turns off GTK overlay scrolling so they are always visible
- Fixed: idle spinners (e.g. in Thunar's menu bar) are now hidden instead of showing a frozen circle
- Installer with English options (`--full`, `--taskbar`, `--wallpaper[=FILE]`, `--start-icon=FILE`, `--system`, `--no-apply`) and automatic settings backup
- `--full` also sets desktop icons to 36 px and their tooltips to 48 px
- Uninstaller that restores the previous settings
- Original abstract wallpaper (1080p and 4K)
