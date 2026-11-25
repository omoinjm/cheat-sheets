# sheets-desk

An always-on-top corner overlay that watches your terminal and suggests
matching cheat sheets from **sheets.njmtech.co.za** as you type. Built with
[Wails v2](https://wails.io) + [fyne.io/systray](https://github.com/fyne-io/systray).

- **Terminal-aware.** A shell hook streams your current command line to the
  overlay; it ranks the 74 cheat-sheet pages by keyword and shows the best few.
  Type `git merge` → *Git Merge Conflicts*; `nvim` → *Vim*; `psql` → *PostgreSQL*.
- **Always on top, top-left corner.** Frameless, docked to the corner, floats
  above every other window. Drag the header to move it; the 📌 toggles on-top.
- **Click to read.** A suggestion opens the full sheet inside the panel (fetched
  live, so content is always current); ⤢ expands to the full cheat-sheet browser,
  ✕ hides to the tray.
- **System tray + hotkey.** Single-instance lock, so an OS shortcut that relaunches
  the binary pops the overlay back to the corner.

## Use it

1. Run `sheets-desk` (add it to `shell:startup` on Windows so it's always up).
2. Install the shell hook so it can see what you type. **fish** (recommended —
   true live-as-you-type):

   ```fish
   # ~/.config/fish/config.fish
   source /path/to/app/shell/sheets.fish
   ```

   **bash** (fallback — updates on each command you run):

   ```bash
   # ~/.bashrc
   source /path/to/app/shell/sheets.bash
   ```

The hook writes your command line to `%USERPROFILE%\.sheets-desk\ctx.txt`
(resolved via `cmd.exe` + `wslpath` on WSL; `~/.sheets-desk/ctx.txt` otherwise),
and the overlay polls that file ~8×/sec. No ports, no network between WSL and
Windows — it works in any WSL networking mode. The command line never leaves your
machine.

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

## Releasing

Releases are built and published automatically by
[`.github/workflows/release-app.yml`](../.github/workflows/release-app.yml).
Push a version tag and the workflow builds Windows + Linux and attaches the
binaries to a GitHub Release:

```bash
git tag app-v0.1.0        # or plain v0.1.0
git push origin app-v0.1.0
```

Assets produced:

| File                                      | Platform              |
|-------------------------------------------|-----------------------|
| `sheets-desk-windows-amd64.exe`           | Windows, portable     |
| `sheets-desk-windows-amd64-installer.exe` | Windows, NSIS setup   |
| `sheets-desk-linux-amd64.tar.gz`          | Linux (webkit2gtk-4.1)|

You can also trigger it manually from the **Actions** tab ("Run workflow"),
which publishes a prerelease named by the version input.

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

- `main.go` — Wails app: frameless, always-on-top, small window docked top-left;
  serves the embedded overlay UI. Tray + `SingleInstanceLock`.
- `app.go` — lifecycle; on startup positions the corner, floats on top, starts
  the watcher, loads the index.
- `watcher.go` — polls `~/.sheets-desk/ctx.txt`, matches the command line, emits
  a `suggest` event to the UI.
- `matcher.go` — loads `nav.json` (live, with an embedded `navdata/nav.json`
  fallback), flattens it to sheets, and keyword-ranks them (`matcher_test.go`
  covers the ranking).
- `sheet.go` — `FetchSheet` pulls a page's markdown server-side (no CORS) for the
  in-panel view.
- `frontend/dist/index.html` — the overlay UI (list → detail → expand).
- `shell/sheets.fish`, `shell/sheets.bash` — the terminal hooks.
- `tray*.go` — per-OS systray + taskbar handling.

## Icons

`build/tray.png`, `build/appicon.png`, and `build/windows/icon.ico` are the
sheets-desk clipboard mark.
