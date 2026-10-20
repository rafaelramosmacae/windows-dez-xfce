# Windows Dez — XFCE theme inspired by Windows 10

By **Rafael Carvalho Ramos** — rafaelramosmacae@gmail.com

A complete, original theme for XFCE 4.16+ with the flat look of Windows 10:

- white windows with a 1 px blue border and wide title buttons (close turns red on hover)
- classic, always-visible scrollbars with arrow buttons at both ends
- dark taskbar with a blue underline on the active window, dark Start menu (Whisker Menu) and dark notifications — or the same in **light**, like Windows 10 light mode
- **full dark mode** (`--fulldark`): dark windows, file manager, settings, dialogs, menus and title bars, like the Windows 10 dark app mode
- a Start menu laid out like the Windows 10 one: a narrow rail of category icons, all applications from A to Z, and the search box, user picture and power buttons at the bottom
- 232 hand-drawn icons, including thin-line navigation glyphs
- an original wallpaper, "Glass": the four diamonds of the Start button as glowing glass panes

| Dark (default) | Light (`--light`) |
|---|---|
| ![Dark](previews/start-menu.png) | ![Light](previews/start-menu-light.png) |

| Windows | Icons |
|---|---|
| ![Windows](previews/windows.png) | ![Icons](previews/icons.png) |

| Full dark mode (`--fulldark`) |
|---|
| ![Full dark mode](previews/full-dark.png) |

## Screenshots

Xubuntu 26.04 with XFCE 4.20:

| Dark Start menu | Light Start menu |
|---|---|
| ![Dark Start menu](previews/windows-dez-print1.png) | ![Light Start menu](previews/windows-dez-print2.png) |

| Dark taskbar with apps | Light taskbar with apps |
|---|---|
| ![Dark taskbar](previews/windows-dez-print3.png) | ![Light taskbar](previews/windows-dez-print4.png) |

| Full dark mode (`--fulldark`) with apps |
|---|
| ![Full dark mode with apps](previews/windows-dez-print5.png) |

## What's inside

| Folder | Contents |
|---|---|
| `windows-dez/gtk-3.0` | GTK 3 theme: buttons, entries, tabs, lists, menus, switches, scrollbars with arrow buttons, panel and Whisker Menu |
| `windows-dez/gtk-2.0` | Matching colors for legacy GTK 2 applications |
| `windows-dez/xfwm4` | Window borders and buttons (PNG) + `themerc` |
| `windows-dez/xfce-notify-4.0` | Dark notifications in the style of Windows 10 toasts |
| `windows-dez-light` | Same theme with a light taskbar, Start menu and notifications |
| `windows-dez-dark` | Full dark mode: dark GTK 3/GTK 2 applications and dialogs, dark xfwm4 title bars, dark taskbar, Start menu and notifications |
| `windows-dez-icons` | 232 SVG icons drawn from scratch + 386 aliases (folders, devices, XFCE apps, menu categories, file types, actions, symbolic navigation and system-tray icons) |
| `windows-dez-dark-icons` | The same icons for the full dark mode: light toolbar and menu glyphs, falling back to elementary-xfce-dark |
| `wallpaper` | Original "Glass" wallpaper — four glass diamonds on a cyan to royal-blue gradient (1080p and 4K) |
| `build` | Python scripts that generate the icons, window borders, wallpaper and the light and dark variants (`variants.py` + `light.css` / `dark.css`) |

## Installation

```bash
tar xzf windows-dez-xfce-1.2.0.tar.gz
cd windows-dez-xfce-1.2.0
./install.sh --full                # dark taskbar and Start menu (default)
./install.sh --full --light        # light taskbar and Start menu
./install.sh --full --fulldark    # full dark mode: dark windows and applications too
```

Log out and back in afterwards so every application picks up the theme.
You can switch between the styles at any time by running `./install.sh --light`, `./install.sh --dark` or `./install.sh --fulldark` again.

### Installer options

| Option | What it does |
|---|---|
| *(none)* | Installs and applies the GTK theme, icons, window borders, notifications and font, and turns off overlay scrollbars so the classic scrollbars are always visible |
| `--dark` | Dark taskbar, Start menu and notifications (default) |
| `--light` | Light taskbar, Start menu and notifications |
| `--fulldark` | Full dark mode: dark windows, file manager, settings, dialogs, menus and title bars, plus the dark taskbar, Start menu and notifications. On XFCE 4.18 and later the desktop color scheme turns dark too, so GTK 4/libadwaita apps and Firefox follow it |
| `--taskbar` | Moves panel 1 to the bottom (33 px, full width), sets the Start button icon without a label, gives the window list flat buttons without a handle, lays out the Start menu like Windows 10 (see below), and lets you reorder taskbar buttons by drag-and-drop |
| `--wallpaper` | Applies the theme wallpaper on every monitor |
| `--wallpaper=FILE` | Applies your own image (jpg/png) on every monitor |
| `--start-icon=FILE` | Uses your own image (svg/png) for the Start button |
| `--full` / `--complete` | `--taskbar` + `--wallpaper`, plus smaller desktop icons (36 px) and icon tooltips (48 px) |
| `--system` | Installs for all users in `/usr/share` (run with `sudo`) |
| `--no-apply` | Only copies the files; pick the theme yourself in *Settings › Appearance* and *Window Manager* |

The installer saves your previous settings to `~/.config/windows-dez/backup.tsv`. To go back to how things were:

```bash
./uninstall.sh            # or: sudo ./uninstall.sh --system
```

### Using your own images

```bash
./install.sh --full --wallpaper=~/Pictures/my-wallpaper.jpg --start-icon=~/Pictures/my-start.svg
```

Images are copied into the theme folders, so they keep working even if you delete the originals; `uninstall.sh` removes them too. For the Start button, use an SVG or a PNG of at least 48×48 px with a transparent background and a light design (the taskbar is dark).

## Getting closer to Windows 10

- **Panel layout:** Whisker Menu · Launchers · Window Buttons · Separator (expand) · Notification Area · Clock · Show Desktop. Set it up in *Settings › Panel › Items*.
- **Whisker Menu:** install `xfce4-whiskermenu-plugin` if you don't have it. The *Docklike Taskbar* plugin (`xfce4-docklike-plugin`) is styled too.
- **Start menu layout:** `--taskbar` (and `--full`) arrange the Whisker Menu like the Windows 10 Start menu: category icons in a 72 px rail on the left (switched by hovering), all applications from A to Z with plain names and 24 px icons, the search box below them, and the user picture with the settings, lock and power buttons at the bottom (400×640 px). Any of this can be changed in the Whisker Menu properties, and `uninstall.sh` restores your previous layout. Live tiles are not possible with the Whisker Menu.
- **Compositing:** enable it in *Window Manager Tweaks › Compositor* for window shadows and a translucent taskbar.
- **Font:** the installer uses *Segoe UI* if it is installed, otherwise *Noto Sans* or *Open Sans*, at size 9.

## Notes

- Tested on XFCE 4.18 (Ubuntu/Xubuntu 24.04) and on Xubuntu 26.04 with XFCE 4.20 (xfwm4, xfce4-panel, Thunar, Mousepad, Whisker Menu); the CSS is validated with GTK 3's own parser.
- The icons need GTK's SVG loader (`librsvg2-common` on Debian/Ubuntu, `librsvg2` on Fedora, `librsvg` on Arch), which virtually every distribution ships.
- GTK 4/libadwaita (GNOME) apps and Snap apps such as Firefox on Ubuntu ignore GTK themes and keep their own look. With `--fulldark` on XFCE 4.18 and later they switch to their own dark look, because XFCE sets the desktop color scheme to dark for themes whose name ends in `-dark`.
- In the full dark mode, apps that draw their own content (LibreOffice documents, web pages, terminals) may keep their own colors; most of them have a dark option in their preferences.
- Tray icons come from the inherited Adwaita theme; they are symbolic and turn white on the dark taskbar.

## Author

**Rafael Carvalho Ramos**  
rafaelramosmacae@gmail.com

Bug reports, suggestions and contributions are welcome by e-mail.

## Credits and license

All artwork in this package — icons, glyphs, window borders, CSS and wallpaper — is original and released under the **GNU General Public License v3.0 or later** (see `LICENSE`).

Copyright © 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com>

"Windows" is a trademark of Microsoft Corporation. This project is not affiliated with or endorsed by Microsoft; the name only describes the visual inspiration. No Microsoft logos or artwork are included.
