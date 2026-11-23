---
title: Book/Author Website Blueprint (TanStack Start + Sanity + Cloudflare)
description: A master prompt and step-by-step playbook for shipping a book/author promotional site with headless CMS, SEO+GEO, consent-gated analytics, and a Claude Code-driven CI/CD workflow — distilled from labourdialectics.org.
type: content
path: prompts/app-generation/book-author-website-blueprint.md
tags: [prompts, app-generation, tanstack-start, sanity-cms, cloudflare-workers, seo, geo, analytics, clarity, google-analytics, claude-code, mcp, playbook]
---
# Book/Author Website Blueprint: TanStack Start + Sanity + Cloudflare

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## 📌 Overview
This is a distilled, step-by-step playbook for standing up a book/author promotional site — book info, blog, FAQ, contact, buy links — with a headless CMS, dual SEO+GEO (AI-citation) optimization, consent-gated analytics, and a fully automated deploy pipeline. It is reverse-engineered from a real production build (labourdialectics.org) so every step names the actual package, script, or file involved, not just the concept.

Use this the same way as [ecommerce-blueprint.md](./ecommerce-blueprint.md): hand the whole document to an AI assistant as the master prompt for a new site in this genre, and work through the phases in roughly this order. Phases 6–7 (analytics) and 9 (AI tooling) are the ones most worth reading closely even if you skip the rest — they're where the non-obvious footguns live.

---

## 🛠️ The Master Prompt

**Role:** Act as a Senior Full-Stack Engineer building a marketing/content site for a book or author, optimized for both traditional search and AI answer engines.

**Objective:** Ship a fast, prerendered, CMS-editable site with working analytics and a CI/CD pipeline that can't silently ship broken SEO.

### Phase 1: Core Scaffold
1. **Framework:** [TanStack Start](https://tanstack.com/start) + React 19 + Vite 8 + TypeScript. Routes live in `src/routes/` (file-based), shared UI in `src/components/`, static/derived data in `src/data/`, small stateless helpers in `src/lib/`.
2. **Styling & UI:** Tailwind CSS 4 with brand colors defined once as CSS custom properties in `src/styles.css` using **oklch** (`--primary`, `--accent`, `--background`, `--foreground`) — every component and every generated asset (favicons, charts) should reference these tokens instead of inventing new hex values. Add shadcn/ui for accessible primitives (`Sheet`, `Dialog`, `Button`) and `motion/react` (Framer Motion) for page-transition and scroll-reveal animation.
3. **Hosting target:** Cloudflare Workers via `wrangler`, with TanStack Start's own Worker entry (`src/server.ts`) — not Cloudflare Pages. `wrangler.jsonc` needs `"run_worker_first"` listing every CMS-backed route (`/`, `/blog`, `/blog/*`, etc.) so Sanity content is fetched live instead of served from stale prerendered HTML forever.
4. **Branching model:** `development` = preview/staging, `main` = production. **Never commit directly to `main`.** Standard promotion flow used throughout this project:
   ```bash
   git add <files> && git commit -m "..." && git push origin development
   git checkout main && git pull origin main --ff-only
   git merge origin/development --ff-only && git push origin main
   git checkout development
   ```
   Fast-forward only — if it's not a fast-forward, `development` and `main` have diverged and need a real look, not a force-push.

### Phase 2: Headless CMS (Sanity)
1. Embed **Sanity Studio** into the app, served at `/studio` on the same Worker (bundled at deploy time, not a separate app).
2. Content model as singletons + documents (e.g. `siteSettings`, `post`, `faqItem`) with references between them rather than duplicated strings.
3. Fetch a build-time manifest of dynamic slugs (`scripts/fetch-sanity-manifest.mjs` → `sanity/manifest.json`) so the prerenderer knows which blog/FAQ URLs exist without a live CMS call at build time.
4. Env vars: `VITE_SANITY_PROJECT_ID`, `VITE_SANITY_DATASET`. Local dev reads them from `.env.local` (gitignored via the blanket `*.local` rule — verify that rule exists before assuming any `.env.*` file is safe).
5. **Sanity MCP server** (`mcp__Sanity__*` tools in Claude Code) — use `get_schema` before writing any GROQ query or patch, and `query_documents`/`patch_documents` directly from the editor instead of hand-rolling scripts for one-off content fixes.

### Phase 3: SEO Foundations
1. Central meta/schema builders (e.g. `buildRootMetaTags`, `buildWebSiteSchema`, `buildPersonSchema`, `buildOrganizationSchema`, `buildDefinedTermSetSchema`) in `src/data/seo.ts`, composed once in the root route (`src/routes/__root.tsx`) and per-page where needed (`FAQPage`, `BreadcrumbList`).
2. `scripts/generate-sitemap.mjs` writes `public/sitemap.xml` (**base URLs only — never include `#fragment` anchors**, Google doesn't treat fragments as distinct documents and will ignore them if submitted) plus `public/robots.txt`.
3. **Favicon/brand mark as a single source of truth:**
   - One hand-authored SVG at `public/favicon.svg`, `viewBox="0 0 64 64"`, referencing the exact same hex values as the CSS brand tokens (convert oklch → hex once via a throwaway headless-browser canvas trick if you don't have them memorized — `getComputedStyle` + `canvas.fillStyle` + `getImageData` round-trips any CSS color function to RGB reliably).
   - `scripts/generate-favicons.mjs` (needs `@resvg/resvg-js` + `to-ico`, install with `--no-save` since they're build-tool-only) rasterizes that one SVG into every required size: `favicon-32x32.png`, `favicon-48x48.png`, `favicon.ico` (multi-size ICO via `to-ico`), `apple-touch-icon.png` (180px, **background rect un-rounded** — iOS applies its own corner mask, a rounded-rect source produces double-rounding), `icon-192.png`, `icon-512.png`.
   - Nav bar logo should just `<img src="/favicon.svg">` — one file, zero duplication, and any brand color change only needs editing in one place.
   - Keep `theme-color` meta, `msapplication-TileColor`, and `public/site.webmanifest`'s `background_color`/`theme_color` all in sync with the SVG's background fill. Grep the old hex across the repo after a rebrand — it hides in more places than you expect.
4. **`scripts/test-seo.mjs` is a hard CI gate, not a lint suggestion** — it asserts specific strings/schema types exist in the *prerendered* HTML output for each route. Run it locally (`npm run test:seo`) after any homepage/section copy change, before pushing — it WILL block the production deploy if a hardcoded assertion (e.g. an exact heading string) goes stale after you remove or rename a section.

### Phase 4: GEO — AI Citation Optimization
1. Generate `public/llms.txt` (short) and `public/llms-full.txt` (detailed, with a "when to cite this site" section and extractable Q&A) alongside the sitemap — same generator script, same build step.
2. `robots.txt` should carry explicit **Content-Signals** (a machine-readable statement of intent, e.g. `search & ai-input yes; ai-train no; use=reference`) plus an explicit allow-list for AI answer-engine crawlers, distinct from a blanket disallow on training-only scrapers.
3. Answer-first Q&A content (40–70 word self-contained answers, one question per block) belongs on **one canonical page** — a `/faq` route with `FAQPage` JSON-LD is the natural home. **Don't also duplicate it on the homepage** — a dense keyword-cluster block reads as over-optimized on a page meant for human visitors, and it's redundant with the FAQ once that page exists. If you do remove it from the homepage later, remember Phase 3's SEO test may have a hardcoded assertion tied to that section's heading — update the test in the same commit.

### Phase 5: Cookie Consent Framework
1. One localStorage-backed flag gates *every* third-party script on the site — analytics and any embed that sets its own cookies (YouTube/Vimeo/Spotify/etc.). Don't give each tracker its own consent flag; one flag, one banner, one mental model for future you.
2. Two independent boolean reads (`useCookieConsent`, `useConsentBannerDismissed`) backed by the same small module (`src/lib/cookie-consent.ts`), each re-rendering on a custom same-tab event *and* the cross-tab `storage` event.
3. Banner component renders `null` once either accepted or dismissed; "Dismiss" ≠ "Accept" — dismissing hides the banner without granting tracking consent.
4. Every analytics component (Clarity, GA4, ...) is a standalone `<XAnalytics />` that reads the same consent hook and no-ops until it flips true — rendered once, together, in the root route.

### Phase 6: Analytics — Microsoft Clarity
1. `npm install @microsoft/clarity`.
2. Component pattern — dynamic import, gated on consent, no-op without a project ID:
   ```tsx
   const CLARITY_PROJECT_ID = import.meta.env.VITE_CLARITY_PROJECT_ID as string | undefined;
   export function ClarityAnalytics() {
     const hasConsent = useCookieConsent();
     useEffect(() => {
       if (!hasConsent || !CLARITY_PROJECT_ID) return;
       import("@microsoft/clarity").then(({ default: Clarity }) => Clarity.init(CLARITY_PROJECT_ID));
     }, [hasConsent]);
     return null;
   }
   ```
3. Env var `VITE_CLARITY_PROJECT_ID` needs to be injected at **build time** in **every** deploy workflow that ships to a real audience — not just the one you happened to test first. This project shipped it to the dev/preview workflow and forgot the production workflow for two weeks; the fix is a one-line `env:` addition, the lesson is to add new build-time vars to both workflows in the same commit.
4. **Clarity MCP server** for querying analytics from Claude Code directly (session recordings, dashboard queries) — register in `~/.claude.json` (user-level, not the repo) under `mcpServers`:
   ```json
   "clarity": {
     "type": "stdio",
     "command": "npx",
     "args": ["-y", "@microsoft/clarity-mcp-server"],
     "env": { "CLARITY_API_TOKEN": "<token from Clarity dashboard → Settings → Data Export>" }
   }
   ```
   Restart Claude Code after editing — `~/.claude.json` is only read at startup. Tools exposed: `query-analytics-dashboard` (natural-language query, needs an explicit time range), `list-session-recordings`, `query-documentation-resources`.
   **Never pass the API token as a bare CLI arg** (`--clarity_api_token=...`) in a terminal you might screenshot or share — it's then plaintext in shell history and the process list. Put it in the MCP config's `env` field (or better, reference a shell env var) and `chmod 600` the config file since it now holds a live secret.

### Phase 7: Analytics — Google Analytics 4
1. Same consent-gate pattern as Clarity, but GA4 has no npm package for this — inject `gtag.js` as a plain `<script>` tag manually:
   ```tsx
   const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID as string | undefined;
   declare global { interface Window { dataLayer?: unknown[] } }
   export function GoogleAnalytics() {
     const hasConsent = useCookieConsent();
     useEffect(() => {
       if (!hasConsent || !GA_MEASUREMENT_ID) return;
       if (document.querySelector(`script[data-ga-id="${GA_MEASUREMENT_ID}"]`)) return;
       const script = document.createElement("script");
       script.async = true;
       script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
       script.dataset.gaId = GA_MEASUREMENT_ID;
       document.head.appendChild(script);
       window.dataLayer = window.dataLayer || [];
       const gtag = (...args: unknown[]) => window.dataLayer?.push(args);
       gtag("js", new Date());
       gtag("config", GA_MEASUREMENT_ID);
     }, [hasConsent]);
     return null;
   }
   ```
2. `VITE_GA_MEASUREMENT_ID` — same dual-workflow, both-secrets-at-once rule as Phase 6.
3. Multiple trackers can share the same `window.dataLayer`/consent gate without conflict — verify with a live network-request check (Phase 9) rather than assuming.

### Phase 8: CI/CD Pipeline (GitHub Actions → Cloudflare Workers)
1. Two workflows, kept in lockstep on every build-time env var:
   - `deploy-cloudflare-dev.yml` — triggers on push to `development`, deploys to a `*-development.workers.dev` preview URL.
   - `deploy-cloudflare.yml` — triggers on push to `main`, deploys to production.
2. Gate order inside each: install deps → build → **verify Sanity date helpers** → **verify SEO in prerendered HTML** (`npm run test:seo`) → inject Worker vars from secrets → `wrangler deploy`. If any gate fails, nothing ships — that's the point.
3. Full GitHub secrets checklist (keep README's secrets table current as you add each one): `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `VITE_SANITY_PROJECT_ID`, `VITE_SANITY_DATASET`, `VITE_GOOGLE_SITE_VERIFICATION`, `WEB3FORMS_ACCESS_KEY` (or your form-submission provider's key), `VITE_CLARITY_PROJECT_ID`, `VITE_GA_MEASUREMENT_ID`.
4. Prune stale branches periodically — check `ahead`/`behind` counts against `main` before bulk-deleting (`git log origin/main..<branch> --oneline`), since a branch that's merely old isn't automatically safe to delete; one that's genuinely unmerged and abandoned is.

### Phase 9: AI-Assisted Dev Workflow (Claude Code specifics)
This is the part that makes rebuilding this *seamless* rather than just documented — the actual tool loop used to build and verify this site.
1. **`gh` CLI** for everything GitHub-shaped: `gh auth login -h github.com` (interactive browser flow — the user runs this themselves, an agent can't drive an OAuth browser prompt), then `gh secret set NAME` / `gh secret list` for secrets, `gh run list --workflow=X.yml` / `gh run watch <id> --exit-status` for watching a deploy to completion instead of guessing.
2. **Headless browser verification is not optional** — "the code looks right" and "it works on the live site" are different claims. The pattern used throughout this build:
   ```js
   const { chromium } = require('playwright');
   const browser = await chromium.launch();
   const page = await browser.newPage();
   const requests = [];
   page.on('request', r => { if (r.url().includes('tracker-domain')) requests.push(r.url()); });
   await page.goto('https://your-site.com', { waitUntil: 'networkidle' });
   // assert pre-consent state, click accept, assert post-consent state, screenshot
   ```
   Requires `npx playwright install chromium` once per machine (needs a real terminal for the `sudo`-gated system deps the first time — have the user run this step themselves if the agent's sandbox can't elevate).
3. **Context-mode / sandboxed execution** — route build commands, `gh` calls, and the Playwright checks above through a sandboxed code-execution tool rather than a raw shell, so verbose CI logs and full-page accessibility snapshots don't flood the conversation — only the printed summary should come back.
4. **Never retype a secret you only saw in a screenshot.** If a credential was exposed in a screenshot or pasted into chat, treat it as compromised and ask before reusing it, and rotate it once the immediate task is done.
5. **Sanity MCP** for CMS content/schema work, as in Phase 2 — avoid one-off scripts for what a direct `patch_documents` call handles.

### Phase 10: Post-Launch Maintenance Notes
- Favicon/branding changes need **no** Search Console re-indexing action — Google recrawls favicons on its own independent (slow) schedule regardless of page-content indexing; there's no dedicated "refresh favicon" request. Browsers also cache favicons aggressively client-side, separate from anything Google-related.
- URL fragments (`#anchor`) are never indexed as separate documents — they're stripped before the request reaches your server. Keep them out of `sitemap.xml`; they're purely for direct deep-linking and (as a side benefit) Google can auto-generate on-page jump links in search results from your heading structure without any submission.
- After removing or renaming any homepage/landing section, re-run `npm run test:seo` before pushing — see Phase 3, note 4.

---

## 📋 Execution Checklist
- [ ] Brand colors defined once as CSS tokens; favicon SVG and every raster export derived from the same values via `generate-favicons.mjs`
- [ ] `development` → `main` fast-forward promotion flow, never a direct commit to `main`
- [ ] Sanity Studio bundled at `/studio`; MCP server available for schema/content work
- [ ] `sitemap.xml`, `robots.txt` (with Content-Signals), `llms.txt`/`llms-full.txt` all generated in the same build step
- [ ] `test:seo` passing locally before every push; wired as a hard CI gate before deploy
- [ ] One consent flag gates Clarity + GA4 + all third-party embeds; verified live (0 tracking requests pre-consent, N post-consent)
- [ ] Every `VITE_*` build-time var added to **both** GitHub Actions workflows and the README secrets table in the same commit
- [ ] Clarity MCP server registered in `~/.claude.json` for direct analytics queries from Claude Code
- [ ] No API tokens passed as bare CLI args or left in files without restricted permissions
- [ ] Stale AI-agent branches pruned after checking ahead/behind counts, not on assumption
