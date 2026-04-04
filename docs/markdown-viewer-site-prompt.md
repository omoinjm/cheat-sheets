# Prompt: Generate a Markdown Viewer GitHub Pages Website

Use this prompt to generate a static GitHub Pages website for any repository containing
markdown notes or documentation organized in folders.

---

```
I have a GitHub repository containing markdown notes/documentation organized in folders.
I want to convert it into a static GitHub Pages website with the following features:

## Structure
- The repo has a root `README.md` (homepage) and markdown files organized in subdirectories
  (e.g., Labs/, Projects/, etc.)
- No build step — pure HTML/CSS/JS served directly by GitHub Pages (no Jekyll, include a `.nojekyll` file)

## Core Files to Generate
1. `index.html` — single-page app entry point
2. `assets/styles.css` — all styles
3. `assets/app.js` — all client-side logic
4. `nav.json` — navigation config (sections, labels, icons, paths to markdown files)

## Features
- **Sidebar** with a collapsible tree navigation built dynamically from `nav.json`
- **Markdown rendering** using marked.js (CDN) with syntax highlighting via highlight.js (CDN)
- **Hash-based routing** (`#path/to/file.md`) so every page is deep-linkable
- **Front matter support**: parse YAML front matter (`title`, `description`, `tags`) from markdown
  files and render a styled meta card above the content
- **Breadcrumb** showing the current location in the nav tree
- **Mobile responsive**: collapsible hamburger sidebar for small screens
- **Modal popups** for secondary markdown files (e.g., instructions, architecture docs) and PDFs
- **Active link highlighting** in the sidebar when a section is selected
- Home page loads `README.md` by default

## nav.json Schema
{
  "home": "README.md",
  "sections": [
    {
      "id": "unique-id",
      "label": "Section Name",
      "icon": "🧪",
      "overview": "FolderName/README.md",
      "children": [
        {
          "id": "sub-id",
          "label": "Sub Section",
          "icon": "📁",
          "overview": "FolderName/SubFolder/README.md",
          "entries": [
            { "label": "Page Title", "path": "FolderName/SubFolder/filename" }
          ]
        }
      ]
    }
  ]
}

## Style
- Dark sidebar, light content area
- Clean, readable typography for markdown content
- Code blocks with dark theme syntax highlighting
- Tag pills for front matter tags
- No external CSS frameworks — vanilla CSS only

The site title, icon/emoji, and color scheme should be easy to customize via CSS variables.
Generate all files with comments explaining the structure and how to adapt it to a new repo.
```

---

## How to Adapt This Prompt

| Element | Where to Customize |
|---|---|
| Site title & icon | `index.html` `<title>` and sidebar header |
| Color scheme | CSS variables in `assets/styles.css` |
| Navigation structure | `nav.json` — mirrors your folder layout |
| Home page | Point `"home"` in `nav.json` to your root `README.md` |
| Custom domain | Add a `CNAME` file with your domain |

## Reference Implementation

This prompt was derived from the **AWS re/Start Portfolio** site:
- Repo: `aws-restart-portfolio`
- Key files: `index.html`, `assets/portfolio.css`, `assets/portfolio.js`, `nav.json`
