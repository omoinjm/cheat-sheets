# Copilot Instructions

## Repository Purpose

This is a personal knowledge base / wiki deployed as a static GitHub Pages site. It is **documentation-only** — no build step, no tests, no linter. The live site is at `https://omoinjm.github.io/cheat-sheets`.

## Architecture

The viewer is a single-page app with no framework or build toolchain:

| File | Role |
|---|---|
| `index.html` | SPA entry point; sidebar, content area, modal skeleton |
| `assets/app.js` | All client logic: nav tree rendering, hash-based routing, YAML front matter parsing, markdown rendering (marked.js), syntax highlighting (highlight.js), breadcrumbs, mobile sidebar toggle |
| `assets/styles.css` | All styles — vanilla CSS, no framework |
| `nav.json` | Drives the sidebar tree; defines every page's label, icon, and path |

**Routing**: Hash-based (`#path/to/file.md`). Changing the hash triggers a fetch of the corresponding markdown file from the repo root.

**nav.json schema** (must match exactly):
```json
{
  "home": "README.md",
  "sections": [
    {
      "id": "unique-kebab-id",
      "label": "Display Name",
      "icon": "emoji",
      "overview": "section/README.md",
      "entries": [{ "label": "Page", "path": "section/page.md" }],
      "children": []
    }
  ]
}
```

## Markdown File Conventions ("Wiki-fication")

Every markdown file follows this structure:

**Content files** (`type: content`):
```yaml
---
title: Short Descriptive Title
description: One-sentence summary.
type: content
path: relative/path/from/root.md
tags: [tag1, tag2]
---
```

**Directory README files** (`type: directory`) — act as Maps of Content (MOC):
```yaml
---
type: directory
path: relative/path
parent: parent/path
tags: [repo, documentation, category]
---
```

Every file includes a `## 🔗 Navigation` section with relative links to its parent README and the root README.

Every directory README includes these sections:
- `## 📌 Overview`
- `## 📁 Contents` (links to child files with one-line descriptions)
- `## 🧠 Responsibilities`
- `## 🔄 Relationships`

**Rules**: No HTML tags in content files. Use `##` Markdown headers only. All relative paths in links must be accurate for the file's depth.

## Adding New Content

When adding a new cheat sheet or note:

1. **Create the `.md` file** in the appropriate category directory with correct YAML frontmatter.
2. **Update the parent `README.md`** — add an entry to the `## 📁 Contents` list.
3. **Update `nav.json`** — add an entry under the matching section/subsection so the page appears in the sidebar.
4. **Cross-link** — if the content references topics that have primary docs elsewhere in the repo (e.g., Docker, SSH, SQL), link to those files using relative paths.

The full autonomous workflow is documented in `prompts/documentation/automated-wiki-maintenance.md`.

## Content Categories

| Directory | Covers |
|---|---|
| `development/` | Languages (C#, Python, C/C++), databases (MSSQL, MySQL, PostgreSQL), standards (JWT) |
| `infrastructure/` | Cloud (Azure, AWS), containers (Docker, Portainer), web servers (Nginx) |
| `systems/` | Linux, Windows, automation, webhooks |
| `security/` | Pentesting (HackTheBox), reverse engineering, OSINT |
| `workspace/` | IDEs, Git, SSH/networking |
| `professional/` | Work-specific notes |
| `prompts/` | Reusable AI prompts for app generation, code improvement, documentation |

## GitHub Pages Deployment

- Deployed from the repo root via GitHub Pages.
- Uses `jekyll-theme-hacker` theme with `jekyll-feed` and `jekyll-seo-tag` plugins (`_config.yml`).
- A `.nojekyll` file is present — the custom SPA viewer (`index.html`) is served directly alongside Jekyll for the GitHub Pages URL.
- `baseurl` is `/cheat-sheets`; `RAW_BASE` in `app.js` is `''` (files fetched relative to repo root).
