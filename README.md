# Cheat Sheets

A personal knowledge base of notes, guides, and technical references — published
as a static site and viewable as a tray-resident desktop app.

## Layout

```
.
├── docs/   → the content + hosted site (GitHub Pages web root)
└── app/    → sheets-desk: a desktop window that shows the site, in the tray
```

### `docs/` — content & site
A client-side SPA (`index.html` + `assets/app.js`) that renders the markdown
notes organized under category folders (`development/`, `infrastructure/`,
`security/`, `systems/`, `workspace/`, …). Navigation is driven by `nav.json`;
`.nojekyll` means GitHub Pages serves the files as-is.

> **Hosting:** this folder is the published web root. Set GitHub Pages to
> **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs`**.
> The custom domain (`docs/CNAME` → sheets.njmtech.co.za) is served from here.
> Because every path in the SPA is web-root-relative, serving `/docs` keeps all
> links working with no edits.

Add a page: drop a markdown file in the right category folder (front matter like
the existing pages), then register it in `docs/nav.json`.

### `app/` — sheets-desk desktop app
A thin [Wails v2](https://wails.io) window that loads the hosted site, lives in
the system tray, and uses a single-instance lock so an OS keyboard shortcut pops
the window forward. See [`app/README.md`](app/README.md) for build steps and
hotkey setup.

```bash
cd app
wails build -platform windows/amd64 -nsis -skipbindings   # Windows .exe
wails build -skipbindings -tags webkit2_41                 # Linux (needs webkit2gtk)
```
