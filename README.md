# JEE Prep Guide

A free, comprehensive **JEE Main & Advanced 2026** preparation platform built as a static website. It hosts chapter-wise notes for Physics, Chemistry, and Mathematics, a JEE complete guide, a tips/updates blog, and standard site pages (About, Contact, Privacy, Terms) — all served as pre-rendered HTML for fast loading and SEO.

- **Live site:** https://jeeprepguide.netlify.app
- **Repository:** https://github.com/syedrazamd/JEE-PREP-GUIDE
- **License:** ISC

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Build & Development](#build--development)
- [Content Architecture](#content-architecture)
- [Theming System](#theming-system)
- [SEO & Analytics](#seo--analytics)
- [Automation Scripts](#automation-scripts)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Features

- **40+ chapter note pages** across Physics (25), Chemistry (9), and Maths (6), each with formulas, worked examples, PYQ-style content, and related-notes recirculation.
- **JEE 2026 Complete Guide** — a single-page reference covering exam pattern, syllabus, chapter-wise weightage, cutoffs, best books, and preparation strategy with FAQ schema.
- **Blog** with category filters, search, featured post, and newsletter section.
- **Search & filter** on the homepage (chapter search + subject category filters).
- **Reading progress bar**, active-section nav highlighting, sticky table of contents, scroll-to-top, and print/PDF support on chapter pages.
- **MathJax** rendering for LaTeX formulas across all chapter pages.
- **Per-subject color themes** (Physics = purple, Chemistry = emerald, Maths = rose).
- **Lazy-loaded images** via `IntersectionObserver`, with WebP hero images.
- **Copy-to-clipboard** for formulas.
- **Installable PWA** via `manifest.json`.
- **Extensive SEO**: per-page canonical URLs, Open Graph, Twitter Cards, and Schema.org JSON-LD (`EducationalOrganization`, `WebSite`, `Course`, `ItemList`, `FAQPage`, `BreadcrumbList`).
- **Monetization-ready**: Google AdSense (`ads.txt` + per-page ad scripts).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Markup | Static HTML5 (no templating engine, no SPA framework) |
| Styling | Tailwind CSS v3.4.19 (compiled) + per-subject custom CSS |
| Interactivity | Vanilla JavaScript (no frameworks) |
| Math | MathJax v3 via CDN |
| Fonts | Inter, JetBrains Mono (Google Fonts) |
| Build | `tailwindcss` CLI (single dev dependency) |
| Automation | Python 3, PowerShell, Node.js (ESM) scripts |
| Hosting | Netlify (`_redirects`, sitemap, robots) |
| Analytics | Google Analytics (`G-FX8E0XX3KV`) |
| Ads | Google AdSense (`ca-pub-6638196555392555`) |

---

## Project Structure

```
jeeprepguide/
├── index.html                      # Homepage (hero, search, chapter grid)
├── about-us.html
├── contact-us.html
├── privacy-policy.html
├── terms-and-conditions.html
├── manifest.json                   # PWA manifest
├── robots.txt
├── sitemap.xml                     # 357-line XML sitemap
├── ads.txt                         # Google AdSense verification
├── _redirects                      # Netlify redirect rules
├── logo-header.webp / logo.png     # Site logo
│
├── src/
│   └── input.css                   # Tailwind source (dark-theme CSS vars)
├── css/
│   └── tailwind.min.css            # Compiled Tailwind output
├── tailwind.config.js              # Tailwind config (content, theme, colors)
├── package.json                    # npm scripts (build:css)
│
├── jee/
│   ├── index.html                  # JEE 2026 Complete Guide (single-page)
│   ├── physics/
│   │   ├── index.html              # Physics subject index (25 chapters)
│   │   └── *.html                  # 25 chapter note pages
│   ├── chemistry/
│   │   ├── index.html              # Chemistry subject index
│   │   └── *.html                  # 9 chapter note pages
│   ├── maths/
│   │   ├── index.html              # Maths subject index
│   │   └── *.html                  # 6 chapter note pages
│   └── assets/
│       ├── css/
│       │   ├── notes-physics.css   # Purple theme
│       │   ├── notes-chemistry.css # Emerald theme
│       │   └── notes-maths.css     # Rose theme
│       └── js/
│           └── notes.js            # Shared JS for all chapter pages
│
├── blog/
│   ├── index.html                  # Blog listing
│   └── *.html                      # Blog posts (UGEE, COMEDK, WBJEE, JEE Main, etc.)
│
└── Automation scripts (see below)
```

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (for Tailwind build)
- Optional: Python 3, PowerShell, or Node.js — only needed to run the automation scripts.

### Install & Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/syedrazamd/JEE-PREP-GUIDE.git
cd JEE-PREP-GUIDE

# 2. Install dev dependencies (Tailwind CSS)
npm install

# 3. Build the CSS (compiles src/input.css -> css/tailwind.min.css)
npm run build:css

# 4. Preview locally
#    Use any static server, e.g.:
npx serve .
#    or open index.html directly in a browser
```

Because this is a static site, no application server is required. The only build
step is compiling Tailwind utilities.

---

## Build & Development

### Compile Tailwind CSS

```bash
npm run build:css
# Equivalent to: tailwindcss -i ./src/input.css -o ./css/tailwind.min.css --minify
```

`tailwind.config.js` scans every `./**/*.html` file for class usage and purges
unused styles. The theme exposes custom color tokens (`primary`, `canvas`,
`surface-1…4`, `ink`, `hairline`, …) backed by CSS custom properties defined in
`src/input.css`, so themes can be swapped by overriding the `:root` variables.

### Editing Content

- Edit any `.html` file directly — there is no templating layer.
- Chapter pages share a common template (see [Content Architecture](#content-architecture)).
- For batch changes across the 40 chapter pages, prefer the automation scripts over manual edits.

---

## Content Architecture

### Homepage (`index.html`)

Hero with glassmorphism stats -> syllabus coverage bar -> search + subject filter
-> chapter grid (Physics, Chemistry, Maths, 6 cards each) -> footer.

### Chapter Pages (`jee/<subject>/<chapter>.html`)

Every chapter page follows the same template:

1. **`<head>`** — SEO meta, canonical, OG/Twitter, fonts, inline MathJax config,
   MathJax CDN script, AdSense, BreadcrumbList JSON-LD, Google Analytics,
   subject-specific CSS link, compiled Tailwind link.
2. **Header** — logo + nav (Home, Physics, Chemistry, Maths, Blog) + mobile menu.
3. **Breadcrumb**.
4. **Quick navigation pills** — jump links to key concepts.
5. **Hero** — subject-themed gradient.
6. **Main grid** — sticky sidebar (table of contents, official links, PDF/print)
   + main content (topic cards, formula boxes, example boxes, tip boxes, tables,
   diagrams, MathJax-rendered equations).
7. **"Builds on these concepts"** — prerequisite links (added by
   `_add_related_concepts.py`).
8. **"Related Notes"** — 3 related chapter cards (added by
   `_add_related_notes.py`).
9. **Footer** + scroll-to-top.
10. **`<script src="../assets/js/notes.js">`** — shared interactivity.

### JEE Complete Guide (`jee/index.html`)

A long single-page guide (~1700 lines) with sticky sidebar TOC and nine sections:
Overview, JEE Main 2026, JEE Advanced 2026, Eligibility, Syllabus, Chapter-wise
Weightage, Cutoff Trends, Best Books, Preparation Strategy + FAQs.

### Blog (`blog/`)

Listing page with category filter bar, featured post, post grid, newsletter
section. Individual posts are standalone HTML files with their own hero images
(WebP + PNG fallbacks).

---

## Theming System

The site uses **two complementary theming layers**:

1. **Global dark theme** — `src/input.css` defines `:root` CSS custom properties
   (`--color-primary`, `--color-canvas`, `--color-ink`, …) consumed by
   `tailwind.config.js` as Tailwind color tokens. Used by the homepage and
   top-level pages (`bg-canvas text-ink`).

2. **Per-subject light themes** — `jee/assets/css/notes-{physics,chemistry,maths}.css`
   override the `:root` variables and add subject-specific component styles
   (`.formula-box`, `.example-box`, `.topic-card`, `.custom-table`, scrollbar):
   - Physics: `--color-primary: #7c3aed` (purple)
   - Chemistry: `--color-primary: #059669` (emerald)
   - Maths: `--color-primary: #e11d48` (rose)

   Each chapter page loads its subject CSS *after* `tailwind.min.css` so the
   overrides take effect.

The `update-theme-colors.mjs` script batch-updates progress-bar gradients, body
classes, and hero gradients per subject.

---

## SEO & Analytics

Every page ships with:

- Canonical URLs (pointing to `https://jeeprepguide.netlify.app/...`)
- Open Graph + Twitter Card meta tags
- Schema.org JSON-LD (`EducationalOrganization`, `WebSite`, `Course`,
  `ItemList`, `FAQPage`, `BreadcrumbList`)
- `robots.txt` (allows Googlebot/Bingbot, blocks AhrefsBot/SemrushBot/MJ12bot/DotBot)
- `sitemap.xml` (357 lines, all public URLs)
- Google Analytics (`G-FX8E0XX3KV`)
- Google AdSense (`ca-pub-6638196555392555`) + `ads.txt`
- `manifest.json` for PWA installability

---

## Automation Scripts

The 40 chapter pages share a common template, so bulk maintenance is performed
through one-off scripts. These are **not** part of the build — run them manually
when needed. Scripts prefixed with `_` are historical fix-up scripts.

### Python (`_*.py`)

| Script | Purpose |
|---|---|
| `_add_mobile_menu.py` | Insert hamburger button + mobile menu panel into all 40 chapter HTMLs |
| `_add_related_concepts.py` | Add "Builds on these concepts" prerequisite links at the top of `<main>` |
| `_add_related_notes.py` | Add "Related Notes" section (next 3 chapters, wrapping) before `</main>` |
| `_convert_hero_images.py` | Convert hero PNGs to WebP (quality 80, method 6) |
| `_convert_to_webp.py` | Broader PNG -> WebP conversion (handles RGBA/LA/palette transparency) |
| `_fix_header_nav.py` | Standardize header nav links to canonical Netlify URLs across all HTMLs |
| `_fix_mathjax_config.py` | Add inline MathJax config in `<head>` (fixes async race), remove it from `notes.js` |
| `_fix_missing.py` | Add mobile menu to the one missing file (`work-energy-and-power.html`) |
| `_fix_mobile_order.py` | Hide quick-nav on mobile, reorder sidebar after main content |
| `_spotcheck.py` | Debug: inspect header nav links in 3 chapter files |
| `_throttle_scroll.py` | Combine multiple scroll listeners in `notes.js` into one rAF-throttled handler |

### PowerShell (`*.ps1`)

| Script | Purpose |
|---|---|
| `_update_blog_imgs.ps1` | Update `.png` -> `.webp` `img src` refs in blog HTMLs |
| `_update_header_logos.ps1` | Replace `logo.png` src with `logo-header.webp` in all HTMLs |
| `_update_jee_imgs.ps1` | Update PNG -> WebP `img src` refs in `jee/physics` and `jee/chemistry` |
| `_update_tailwind_cdn.ps1` | Replace Tailwind CDN `<script>` tags with compiled CSS `<link>` |
| `update-notes-assets.ps1` | Replace inline `<style>`/`<script>` in chapter HTMLs with external CSS/JS links |

### Node.js (`.mjs`)

| Script | Purpose |
|---|---|
| `update-notes.mjs` | Same as `update-notes-assets.ps1`, written in ESM (more robust regex patterns) |
| `update-theme-colors.mjs` | Batch-update tailwind colors, progress-bar gradients, body classes, hero gradients per subject |

### Shared JS (`jee/assets/js/notes.js`)

~100 lines of vanilla JS loaded by all 40 chapter pages:

- Mobile menu toggle
- rAF-throttled scroll handler (reading progress bar + active nav highlighting)
- Print/PDF
- Dark mode toggle
- IntersectionObserver lazy image loading
- Copy formula to clipboard
- Reading time estimation

---

## Deployment

The site is deployed on **Netlify** and served from the repository's default
branch. Configuration details:

- **`_redirects`** — Netlify redirect rules:
  - `/units-and-measurement-notes` -> `/jee/physics/units-and-dimensions` (301)
  - `www.jeeprepguide.netlify.app/*` -> `jeeprepguide.netlify.app/:splat` (301)
- **`sitemap.xml`** — all URLs use `https://jeeprepguide.netlify.app/...`
- **No build command required for Netlify** — the CSS is committed to
  `css/tailwind.min.css`. Run `npm run build:css` locally only when Tailwind
  utilities change, then commit the compiled output.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make changes to the static HTML/CSS/JS files.
3. If you add or remove Tailwind utility classes, recompile the CSS:
   ```bash
   npm run build:css
   ```
   and commit `css/tailwind.min.css`.
4. For bulk changes across chapter pages, consider extending or reusing an
   existing automation script rather than editing files by hand.
5. Verify locally with `npx serve .` before opening a pull request.

### Notes

- The `.gitignore` currently does not exclude `node_modules/` or build
  artifacts — be careful not to commit generated files unintentionally.
- Two theming systems coexist (global dark theme in `src/input.css` and
  per-subject light themes in `jee/assets/css/`). When redesigning, decide
  which layer owns each component's styles to avoid conflicts.
- Google AdSense and Analytics IDs are committed to the repo; rotate them in
  your fork if you deploy a copy.

---

## License

ISC — see `package.json`. Free to use for educational purposes.
