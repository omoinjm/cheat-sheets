/* =============================================================
   Cheat Sheets — GitHub Pages Viewer
   assets/app.js

   Responsibilities:
   1. Load nav.json and build the sidebar tree
   2. Hash-based routing — load markdown on hash change
   3. Parse YAML front matter and render meta card
   4. Render markdown via marked.js + highlight.js
   5. Breadcrumb generation
   6. Mobile sidebar toggle
   7. Modal popup support (openModal(path))
   ============================================================= */

'use strict';

// ── Configuration ────────────────────────────────────────────
// ✏️ Point to the root of your raw markdown files.
// For GitHub Pages served from root, leave as ''.
// For a /docs subfolder deployment, change to '/docs'.
const RAW_BASE = '';

// ── State ────────────────────────────────────────────────────
let navData = null;       // parsed nav.json
let currentPath = null;   // currently loaded markdown path

// Flat map of path → breadcrumb chain built during nav rendering
const pathMeta = new Map();

// ── DOM References ────────────────────────────────────────────
const navTree       = document.getElementById('nav-tree');
const contentEl     = document.getElementById('content');
const breadcrumbEl  = document.getElementById('breadcrumb');
const fmCard        = document.getElementById('front-matter-card');
const fmTitle       = document.getElementById('fm-title');
const fmDesc        = document.getElementById('fm-description');
const fmTags        = document.getElementById('fm-tags');
const modalOverlay  = document.getElementById('modal-overlay');
const modalContent  = document.getElementById('modal-content');
const modalClose    = document.getElementById('modal-close');
const hamburger     = document.getElementById('hamburger');
const sidebar       = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');

// ── Marked.js Setup ──────────────────────────────────────────
marked.setOptions({
  breaks: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try { return hljs.highlight(code, { language: lang }).value; } catch (_) {}
    }
    return hljs.highlightAuto(code).value;
  }
});

// ── Init ─────────────────────────────────────────────────────
async function init() {
  try {
    const res = await fetch('nav.json');
    navData = await res.json();
    buildNav(navData);
  } catch (e) {
    navTree.innerHTML = '<div class="nav-loading">⚠️ Failed to load nav.json</div>';
    console.error('nav.json load error:', e);
  }

  // Load initial page from hash, or home
  loadFromHash();
  window.addEventListener('hashchange', loadFromHash);

  // Mobile sidebar
  hamburger.addEventListener('click', toggleSidebar);
  sidebarOverlay.addEventListener('click', closeSidebar);

  // Modal close
  modalClose.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', e => {
    if (e.target === modalOverlay) closeModal();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });
}

// ── Nav Builder ───────────────────────────────────────────────
function buildNav(data) {
  navTree.innerHTML = '';

  // Home link
  const homeEl = document.createElement('div');
  homeEl.className = 'nav-home';
  homeEl.dataset.path = data.home;
  homeEl.innerHTML = `<span>🏠</span><span>Home</span>`;
  homeEl.addEventListener('click', () => navigate(data.home));
  pathMeta.set(data.home, [{ label: 'Home', path: data.home }]);
  navTree.appendChild(homeEl);

  // Top-level sections
  for (const section of data.sections) {
    navTree.appendChild(buildSection(section, [{ label: section.label }]));
  }
}

function buildSection(section, breadcrumb) {
  const wrapper = document.createElement('div');
  wrapper.className = 'nav-section';
  wrapper.dataset.id = section.id;

  // Header row
  const header = document.createElement('div');
  header.className = 'nav-section-header';
  header.innerHTML = `
    <span>${section.icon || '📁'}</span>
    <span>${section.label}</span>
    <span class="chevron">▶</span>
  `;

  // Clicking header: toggle expand AND navigate to overview if present
  header.addEventListener('click', () => {
    const isOpen = wrapper.classList.contains('open');
    wrapper.classList.toggle('open');
    header.classList.toggle('open');
    if (!isOpen && section.overview) {
      navigate(section.overview);
    } else if (isOpen && section.overview) {
      // collapse without navigating
    }
  });

  wrapper.appendChild(header);

  // Register overview path in pathMeta
  if (section.overview) {
    pathMeta.set(section.overview, [...breadcrumb, { label: 'Overview', path: section.overview }]);
  }

  // Container for entries + nested children
  const entriesEl = document.createElement('div');
  entriesEl.className = 'nav-entries';

  // Direct entries
  if (section.entries && section.entries.length > 0) {
    for (const entry of section.entries) {
      const el = buildEntry(entry, breadcrumb);
      entriesEl.appendChild(el);
    }
  }

  // Nested children sections
  if (section.children && section.children.length > 0) {
    const childrenEl = document.createElement('div');
    childrenEl.className = 'nav-children';
    for (const child of section.children) {
      childrenEl.appendChild(buildSection(child, [...breadcrumb, { label: child.label }]));
    }
    entriesEl.appendChild(childrenEl);
  }

  wrapper.appendChild(entriesEl);
  return wrapper;
}

function buildEntry(entry, breadcrumb) {
  const el = document.createElement('div');
  el.className = 'nav-entry';
  el.dataset.path = entry.path;
  el.textContent = entry.label;
  el.title = entry.label;

  const crumbs = [...breadcrumb, { label: entry.label, path: entry.path }];
  pathMeta.set(entry.path, crumbs);

  el.addEventListener('click', () => navigate(entry.path));
  return el;
}

// ── Routing ───────────────────────────────────────────────────
function loadFromHash() {
  const hash = decodeURIComponent(window.location.hash.slice(1));
  const path = hash || (navData ? navData.home : 'README.md');
  navigate(path, false); // false = don't push hash again
}

function navigate(path, pushHash = true) {
  if (!path) return;
  currentPath = path;

  if (pushHash) {
    window.location.hash = encodeURIComponent(path);
    return; // hashchange will fire and call loadFromHash → navigate(false)
  }

  loadMarkdown(path);
  updateActiveLink(path);
  expandToPath(path);
  renderBreadcrumb(path);
  closeSidebar();
}

// ── Markdown Loader ───────────────────────────────────────────
async function loadMarkdown(path) {
  contentEl.innerHTML = '<p style="opacity:.5">Loading…</p>';
  hideFmCard();

  try {
    const url = RAW_BASE + '/' + path;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const raw = await res.text();

    const { frontMatter, body } = parseFrontMatter(raw);

    if (frontMatter && (frontMatter.title || frontMatter.description || frontMatter.tags)) {
      renderFmCard(frontMatter);
    }

    contentEl.innerHTML = marked.parse(body);

    // Re-run highlight.js on rendered blocks
    contentEl.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block);
    });

    // Intercept internal markdown links to use hash routing
    contentEl.querySelectorAll('a[href]').forEach(a => {
      const href = a.getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('#') && href.endsWith('.md')) {
        a.addEventListener('click', e => {
          e.preventDefault();
          const resolved = resolvePath(path, href);
          navigate(resolved);
        });
      }
    });

    // Scroll to top
    window.scrollTo(0, 0);

  } catch (err) {
    contentEl.innerHTML = `<p style="color:#cc3333">⚠️ Could not load <code>${path}</code><br><small>${err.message}</small></p>`;
  }
}

// Resolve a relative href from a base path
function resolvePath(base, rel) {
  if (!rel.startsWith('.')) return rel;
  const parts = base.split('/');
  parts.pop(); // remove filename
  for (const seg of rel.split('/')) {
    if (seg === '..') parts.pop();
    else if (seg !== '.') parts.push(seg);
  }
  return parts.join('/');
}

// ── Front Matter ──────────────────────────────────────────────
function parseFrontMatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return { frontMatter: null, body: raw };

  try {
    const frontMatter = jsyaml.load(match[1]);
    return { frontMatter, body: match[2] };
  } catch (_) {
    return { frontMatter: null, body: raw };
  }
}

function renderFmCard(fm) {
  fmTitle.textContent = fm.title || '';
  fmDesc.textContent  = fm.description || '';
  fmTags.innerHTML = '';

  if (Array.isArray(fm.tags)) {
    for (const tag of fm.tags) {
      const pill = document.createElement('span');
      pill.className = 'tag-pill';
      pill.textContent = tag;
      fmTags.appendChild(pill);
    }
  }

  fmTitle.style.display    = fm.title       ? '' : 'none';
  fmDesc.style.display     = fm.description ? '' : 'none';
  fmTags.style.display     = (fm.tags && fm.tags.length) ? '' : 'none';
  fmCard.classList.remove('hidden');
}

function hideFmCard() {
  fmCard.classList.add('hidden');
  fmTitle.textContent = '';
  fmDesc.textContent  = '';
  fmTags.innerHTML    = '';
}

// ── Breadcrumb ────────────────────────────────────────────────
function renderBreadcrumb(path) {
  const crumbs = pathMeta.get(path) || [{ label: path }];
  breadcrumbEl.innerHTML = '';

  crumbs.forEach((crumb, i) => {
    if (i > 0) {
      const sep = document.createElement('span');
      sep.className = 'sep';
      sep.textContent = '/';
      breadcrumbEl.appendChild(sep);
    }
    const el = document.createElement('span');
    if (i === crumbs.length - 1) {
      el.className = 'current';
      el.textContent = crumb.label;
    } else {
      el.textContent = crumb.label;
      if (crumb.path) el.addEventListener('click', () => navigate(crumb.path));
    }
    breadcrumbEl.appendChild(el);
  });
}

// ── Active Link Highlighting ──────────────────────────────────
function updateActiveLink(path) {
  // Clear previous
  document.querySelectorAll('.nav-entry.active, .nav-home.active').forEach(el => {
    el.classList.remove('active');
  });

  // Activate matching
  document.querySelectorAll(`[data-path]`).forEach(el => {
    if (el.dataset.path === path) el.classList.add('active');
  });
}

// ── Auto-expand Sidebar to Active Item ───────────────────────
function expandToPath(path) {
  const crumbs = pathMeta.get(path);
  if (!crumbs) return;

  // Open all ancestor sections
  const entry = document.querySelector(`.nav-entry[data-path="${CSS.escape(path)}"]`);
  if (!entry) return;

  let node = entry.parentElement;
  while (node && node !== navTree) {
    if (node.classList.contains('nav-section')) {
      node.classList.add('open');
      const header = node.querySelector(':scope > .nav-section-header');
      if (header) header.classList.add('open');
    }
    node = node.parentElement;
  }
}

// ── Modal ─────────────────────────────────────────────────────
// Public API: call openModal('path/to/file.md') from markdown links
window.openModal = async function(path) {
  modalContent.innerHTML = '<p style="opacity:.5">Loading…</p>';
  modalOverlay.classList.remove('hidden');
  document.body.style.overflow = 'hidden';

  try {
    const res = await fetch(RAW_BASE + '/' + path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const raw = await res.text();
    const { body } = parseFrontMatter(raw);
    modalContent.innerHTML = marked.parse(body);
    modalContent.querySelectorAll('pre code').forEach(b => hljs.highlightElement(b));
  } catch (err) {
    modalContent.innerHTML = `<p style="color:#cc3333">⚠️ Could not load <code>${path}</code></p>`;
  }
};

function closeModal() {
  modalOverlay.classList.add('hidden');
  modalContent.innerHTML = '';
  document.body.style.overflow = '';
}

// ── Mobile Sidebar ────────────────────────────────────────────
function toggleSidebar() {
  const open = sidebar.classList.toggle('open');
  if (open) {
    sidebarOverlay.classList.add('visible');
  } else {
    sidebarOverlay.classList.remove('visible');
  }
}

function closeSidebar() {
  sidebar.classList.remove('open');
  sidebarOverlay.classList.remove('visible');
}

// ── Bootstrap ─────────────────────────────────────────────────
init();
