# sheets-desk

A tiny tray-resident desktop window that shows the hosted cheat-sheets site
(**sheets.njmtech.co.za**) in a native web view. Built with
[Wails v2](https://wails.io) + [fyne.io/systray](https://github.com/fyne-io/systray),
mirroring the `rmt-desk` pattern.

- **Lives in the system tray.** Closing the window hides it; the tray icon (or a
  second launch) brings it back. "Quit" exits.
- **Hotkey → window.** The app takes a single-instance lock. Bind an OS keyboard
  shortcut to run the binary again; the second launch is caught by
  `OnSecondInstanceLaunch`, which pops the existing window forward instead of
  starting a new copy. So the shortcut toggles the cheat sheets into view from
  anywhere.
- **Always current.** The window loads the live hosted site, so new cheatsheets
  appear with no rebuild.

## Build

Requires Go 1.24+ and the Wails CLI (`go install github.com/wailsapp/wails/v2/cmd/wails@v2.17.1`).

```bash
# Linux (needs webkit2gtk-4.1 dev libs)
wails build -skipbindings -tags webkit2_41
# → build/bin/sheets-desk

# Windows (cross-build from WSL/Linux, with NSIS installer)
wails build -platform windows/amd64 -nsis -skipbindings
# → build/bin/sheets-desk.exe  and  build/bin/sheets-desk-amd64-installer.exe
```

Stamp a version: add `-ldflags "-X main.version=v0.1.0"`.

## Set up the keyboard shortcut

The app itself registers no global hotkey — you bind the shortcut in the OS to
launch `sheets-desk`. The running instance catches it and shows the window.

### Windows
Pick whichever you prefer:

- **Shortcut key (built in):** put `sheets-desk.exe` (or a shortcut to it) on the
  Desktop or Start menu → right-click → **Properties** → click the **Shortcut key**
  box → press e.g. `Ctrl+Alt+C` → **OK**. Windows launches it on that combo;
  the single-instance lock brings the window forward if it's already running.
  (Windows requires `Ctrl+Alt+<key>` for these.)
- **PowerToys Keyboard Manager / Run:** map a shortcut to run
  `sheets-desk.exe` — more flexible modifiers.
- **AutoHotkey:** `^!c::Run "C:\path\to\sheets-desk.exe"`  (Ctrl+Alt+C).

Add `sheets-desk.exe` to your Startup folder (`shell:startup`) so it's always
in the tray and the hotkey is instant.

### Linux (KDE / GNOME with AppIndicator)
Add a custom shortcut that runs the binary:

- **KDE:** System Settings → Shortcuts → Custom Shortcuts → New → Global
  Shortcut → Command/URL → command `=/path/to/sheets-desk`, assign a key.
- **GNOME:** Settings → Keyboard → Custom Shortcuts → `+` → command
  `/path/to/sheets-desk`, assign a key. (Tray icon needs the AppIndicator
  extension.)

The tray only appears where a StatusNotifier host is running (KDE, most desktops;
GNOME needs the AppIndicator extension). Without a tray, the window simply closes
normally instead of hiding.

## How it works

- `main.go` — Wails app: embedded `frontend/dist/index.html` immediately
  redirects the web view to `https://sheets.njmtech.co.za`. Sets
  `HideWindowOnClose` + `SingleInstanceLock`.
- `app.go` — window lifecycle + `onSecondInstance` (show window on relaunch).
- `tray.go` — systray icon + menu (Open / Quit), Linux & Windows.
- `tray_linux.go` / `tray_windows.go` / `tray_other.go` — per-OS tray
  availability and taskbar-button handling.

## Icons

`build/tray.png`, `build/appicon.png`, and `build/windows/icon.ico` are
placeholders copied from rmt-desk — replace them with your own branding.
