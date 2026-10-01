---
name: blog-posts
description: Comprehensive editorial, typographic, abstract graphic design, and technical publishing guidelines for articles and signals on Tyler "TK" Koshakow's personal website.
---

# TK Blog Posts & Signals Publishing Skill

This skill defines the editorial standards, typographic rules, abstract minimalist graphic aesthetic, theme compatibility, and structured data specifications for creating and publishing posts on Tyler "TK" Koshakow's personal website.

---

## 1. Editorial Voice & Core Principles

- **Tone & Style:** In-house enterprise AEO/SEO strategist and AI consultant. Practitioner-first, contrarian, authoritative, and concise.
- **No Forced Slogans:** Do not insert repetitive catchphrases or slogans into editorial pieces. Let the technical evidence and data drive the narrative.
- **Perspective:** In-house enterprise AEO/SEO strategist and AI consultant. Practitioner-first, contrarian, authoritative, and concise.
- **Audience:** Dual-audience design:
  1. *Human Executives (C-Suite & Decision Makers):* Ultra-clean, distraction-free typography, stark minimalism, and strategic business relevance.
  2. *Machine Crawlers (LLMs, AI Answer Engines, Web Crawlers):* Semantic HTML5, deep JSON-LD entity graphs, and plain-text `/llms.txt` mirrors.
- **Zero Placeholder Policy:** Never publish synthetic directives, mock tables, placeholder logs, or dummy content. Every published signal must contain real, verified content.

---

## 2. Typographic & Formatting Rules (Strict Do's and Don'ts)

### Do NOT Use Oversized Lead Paragraphs
- **Rule:** Do **not** apply `.lead` or enlarged font styling to the first paragraph of an article.
- **Reason:** All body paragraphs must maintain a uniform, consistent font size (`var(--text-base)`) and line height (`var(--line-height-base)`) for optimal reading rhythm.

### Heading Hierarchy
- **`<h1>`**: Reserved strictly for the single main article title (e.g., `<h1 class="article-title" itemprop="headline">...</h1>`).
- **`<h2>`**: Major conceptual sections (e.g., `Goodhart’s Law and Outdated SEO Metrics`, `The Case for C-Suite Reporting`).
- **`<h3>`**: Subordinate subsections or drill-down questions (e.g., `So Why Is UGC Different?`).

### In-Text Theses & Quotations
- **Rule:** When highlighting an empirical finding or core thesis as a graphical pull quote, ensure the context is naturally embedded within the body paragraph.
- **Example in Paragraph:**
  ```html
  <p>
    Asynchronous downloads prevent DOM parsing blocks, but they cannot prevent main-thread execution freezes once third-party scripts compile.
  </p>
  ```

### Editorial Graphical Pull Quotes
- **Rule:** Pull quotes must be styled as a clean graphical element with top and bottom hairline borders, centered alignment, and **should break naturally with a `<br>` tag** where appropriate.
- **Markup:**
  ```html
  <figure class="pullquote">
    <blockquote>
      &ldquo;Asynchronous downloads don't block the DOM,<br>but they still freeze the main thread.&rdquo;
    </blockquote>
  </figure>
  ```
- **CSS Specifications:**
  - Border: `1px solid var(--border-subtle)` on top and bottom only (no heavy left border).
  - Alignment: `text-align: center;`
  - Font: `font-size: var(--text-lg); font-weight: 600; line-height: 1.35; font-style: normal; color: var(--fg); letter-spacing: -0.02em;`
  - Margin: `margin: var(--space-xl) 0; padding: var(--space-lg) var(--space-md);`

### Responsive Sticky Navigation Sidebar & Table of Contents (The 4+ H2 Rule)

#### Mandatory Inclusion Rule
- **Threshold:** Any article, signal, or long-form piece of content containing **four or more H2 headings (`>= 4 H2s`)** MUST implement the responsive sticky navigation sidebar, scrollspy, and mobile drawer.
- **Short Content Exemption:** Content with fewer than 4 H2 headings (`< 4 H2s`, e.g., `signals/aeo-reporting-c-suite.html`) MUST remain in the clean, single-column container (`<div class="container">`) without sidebar or drawer markup.
- **Bio-Card Handling:** The author bio card at the bottom (`<section class="bio-card" aria-labelledby="bio-heading">`) contains an `<h2>` for accessibility, but is **NOT** an article content section:
  - Do NOT wrap the bio card in `.article-section`.
  - Do NOT include the bio card in the sidebar or mobile TOC navigation links.
  - Count: If a post has 3 content H2s + 1 bio-card H2 = 4 total H2s in the document, it meets the `>= 4 H2s` rule and receives the sidebar layout (as demonstrated in `offline/tricholomopsis-sulphureoides-ai-mycology.html`).

#### Responsive Breakpoints
- **Desktop Grid (`@media (min-width: 58rem)`):**
  - Container `.container.has-sidebar` expands to `max-width: 72rem; padding: 0 var(--space-lg);`.
  - Two-column CSS grid: `.article-layout { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 3.5rem; align-items: start; }`.
  - Left column: `<aside class="article-sidebar">` is `position: sticky; top: 2rem; max-height: calc(100vh - 4rem);`.
  - Right column: `<main class="article-main">` is constrained to `max-width: var(--container-width);` (keeping reading line length strictly at `44rem`).
- **Mobile Sticky Bar & Drawer Modal (`@media (max-width: 57.99rem)`):**
  - Desktop sidebar is hidden (`display: none;`).
  - Mobile sticky pill bar (`.mobile-toc-bar`) appears at top (`position: sticky; top: 0; z-index: 100;`), showing the current section name and a "Jump to" trigger button.
  - Tapping the pill bar opens the sliding bottom sheet drawer modal (`.mobile-toc-drawer`), featuring full navigation links and action buttons.
  - Body scrolling is locked (`overflow: hidden`) while the drawer is open.

#### Required HTML Structure
Wrap the page in `.container.has-sidebar`:

```html
<div class="container has-sidebar">
  <header>...</header>

  <!-- MOBILE STICKY TOC BAR (Visible on viewports < 58rem) -->
  <div class="mobile-toc-bar" id="mobileTocBar">
    <button type="button" class="mobile-toc-trigger" id="mobileTocTrigger" aria-expanded="false" aria-controls="mobileTocDrawer" aria-label="Open article table of contents">
      <div class="mobile-toc-info">
        <span class="mobile-toc-indicator-dot" aria-hidden="true"></span>
        <span class="mobile-toc-label">Index //</span>
        <span class="mobile-toc-current" id="mobileTocCurrent">[First Section Title]</span>
      </div>
      <div class="mobile-toc-action-hint">
        <span class="mobile-toc-jump">Jump to</span>
        <svg class="mobile-toc-chevron" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="3 4.5 6 7.5 9 4.5"></polyline>
        </svg>
      </div>
    </button>
  </div>

  <!-- MOBILE TOC DRAWER MODAL -->
  <div class="mobile-toc-drawer" id="mobileTocDrawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Table of Contents">
    <div class="mobile-toc-backdrop" id="mobileTocBackdrop"></div>
    <div class="mobile-toc-sheet">
      <div class="mobile-toc-sheet-header">
        <div class="mobile-toc-sheet-title">
          <span class="toc-badge">Index //</span>
          <span>Table of Contents</span>
        </div>
        <button type="button" class="mobile-toc-close" id="mobileTocClose" aria-label="Close table of contents">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="mobile-toc-sheet-body">
        <ul class="mobile-toc-list">
          <li><a href="#section-1" class="mobile-toc-link">Section One Title</a></li>
          <li><a href="#section-2" class="mobile-toc-link">Section Two Title</a></li>
        </ul>
      </div>
      <div class="mobile-toc-sheet-footer">
        <a href="https://www.linkedin.com/in/tyler-koshakow/" target="_blank" rel="noopener noreferrer" class="sidebar-btn sidebar-btn-primary">
          <span>Connect on LinkedIn</span>
          <svg class="btn-arrow" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="3" y1="8" x2="13" y2="8"></line>
            <polyline points="9 4 13 8 9 12"></polyline>
          </svg>
        </a>
        <button type="button" class="sidebar-btn sidebar-btn-secondary mobile-share-btn" aria-label="Share this signal or copy citation">
          <svg class="share-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="18" cy="5" r="3"></circle>
            <circle cx="6" cy="12" r="3"></circle>
            <circle cx="18" cy="19" r="3"></circle>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
          </svg>
          <span class="btn-text">Share Signal</span>
        </button>
      </div>
    </div>
  </div>

  <!-- TWO-COLUMN ARTICLE LAYOUT -->
  <div class="article-layout">
    <!-- DESKTOP STICKY SIDEBAR -->
    <aside class="article-sidebar" aria-label="Article navigation">
      <div class="sidebar-sticky-wrapper">
        <nav class="sidebar-nav" aria-label="Article outline">
          <div class="sidebar-header">
            <span class="sidebar-label">Index //</span>
          </div>
          <ul class="sidebar-list">
            <li><a href="#section-1" class="sidebar-link">Section One Title</a></li>
            <li><a href="#section-2" class="sidebar-link">Section Two Title</a></li>
          </ul>
        </nav>
        <div class="sidebar-actions">
          <a href="https://www.linkedin.com/in/tyler-koshakow/" target="_blank" rel="noopener noreferrer" class="sidebar-btn sidebar-btn-primary">
            <span>Connect on LinkedIn</span>
            <svg class="btn-arrow" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="3" y1="8" x2="13" y2="8"></line>
              <polyline points="9 4 13 8 9 12"></polyline>
            </svg>
          </a>
          <button type="button" class="sidebar-btn sidebar-btn-secondary desktop-share-btn" aria-label="Share this signal or copy citation">
            <svg class="share-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="18" cy="5" r="3"></circle>
              <circle cx="6" cy="12" r="3"></circle>
              <circle cx="18" cy="19" r="3"></circle>
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
              <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
            </svg>
            <span class="btn-text">Share Signal</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- ARTICLE MAIN CONTENT -->
    <main class="article-main">
      <article class="article-detail" itemscope itemtype="https://schema.org/TechArticle">
        <header class="article-header">...</header>
        <div class="article-content" itemprop="articleBody">
          <!-- Each H2 section wrapped in section.article-section -->
          <section id="section-1" class="article-section">
            <h2>Section One Title</h2>
            <p>...</p>
          </section>

          <section id="section-2" class="article-section">
            <h2>Section Two Title</h2>
            <p>...</p>
          </section>

          <!-- BIO CARD (Excluded from sidebar TOC and NOT wrapped in article-section) -->
          <section class="bio-card" aria-labelledby="bio-heading">
            <h2 id="bio-heading">Professional Bio</h2>
            <p>...</p>
          </section>
        </div>
      </article>
    </main>
  </div>

  <footer>...</footer>
</div>
```

#### Action Buttons & Citation Copy Specification
- **LinkedIn Profile:** Must strictly link to Tyler's verified profile: `https://www.linkedin.com/in/tyler-koshakow/`
- **Citation Format:** Format string must be strictly:
  `Tyler Koshakow (${articleTitle}) (${url})`
- **Native Share Support:** On mobile devices supporting `navigator.share`, opens the OS share sheet.
- **Clipboard Fallback:** Automatically falls back to `navigator.clipboard.writeText` (with `<textarea>` fallback for older environments).
- **Visual Feedback:** Temporarily flips `.btn-text` to `"Citation Copied!"` and adds `.copied` class for 2500ms.

#### JavaScript Implementation Contract
Include this logic in the page's `DOMContentLoaded` listener:

```javascript
// --------------------------------------------------------------------------
// Responsive Sticky Navigation, Scrollspy & Mobile Drawer
// --------------------------------------------------------------------------
const sections = document.querySelectorAll('.article-section');
const desktopLinks = document.querySelectorAll('.sidebar-link');
const mobileLinks = document.querySelectorAll('.mobile-toc-link');
const mobileCurrent = document.getElementById('mobileTocCurrent');
const mobileDrawer = document.getElementById('mobileTocDrawer');
const mobileTrigger = document.getElementById('mobileTocTrigger');
const mobileClose = document.getElementById('mobileTocClose');
const mobileBackdrop = document.getElementById('mobileTocBackdrop');

function setActiveSection(id) {
  if (!id) return;
  desktopLinks.forEach(link => {
    const isMatch = link.getAttribute('href') === '#' + id;
    link.classList.toggle('active', isMatch);
    link.classList.toggle('\\:target-current', isMatch);
    link.setAttribute('aria-current', isMatch ? 'true' : 'false');
  });
  mobileLinks.forEach(link => {
    const isMatch = link.getAttribute('href') === '#' + id;
    link.classList.toggle('active', isMatch);
    link.classList.toggle('\\:target-current', isMatch);
    link.setAttribute('aria-current', isMatch ? 'true' : 'false');
    if (isMatch && mobileCurrent) {
      mobileCurrent.textContent = link.textContent.trim();
    }
  });
}

if ('IntersectionObserver' in window && sections.length > 0) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        setActiveSection(id);
      }
    });
  }, {
    rootMargin: '-15% 0px -70% 0px',
    threshold: 0
  });

  sections.forEach(sec => observer.observe(sec));
}

if (window.CSS && CSS.supports && CSS.supports('scroll-target-group: auto')) {
  const syncCurrent = () => {
    const currentLink = document.querySelector('.sidebar-link:target-current');
    if (currentLink) {
      const href = currentLink.getAttribute('href');
      if (href && href.startsWith('#')) {
        setActiveSection(href.substring(1));
      }
    }
  };
  document.addEventListener('scrollend', syncCurrent);
}

function openMobileDrawer() {
  if (!mobileDrawer) return;
  mobileDrawer.classList.add('open');
  mobileDrawer.setAttribute('aria-hidden', 'false');
  if (mobileTrigger) mobileTrigger.setAttribute('aria-expanded', 'true');
  document.body.style.overflow = 'hidden';
}

function closeMobileDrawer() {
  if (!mobileDrawer) return;
  mobileDrawer.classList.remove('open');
  mobileDrawer.setAttribute('aria-hidden', 'true');
  if (mobileTrigger) mobileTrigger.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}

function handleTocClick(e, link) {
  const href = link.getAttribute('href');
  if (!href || !href.startsWith('#')) return;
  e.preventDefault();
  const targetId = href.substring(1);
  const targetEl = document.getElementById(targetId);
  if (targetEl) {
    closeMobileDrawer();
    targetEl.scrollIntoView({ behavior: 'smooth' });
    if (history.pushState) {
      history.pushState(null, '', href);
    } else {
      location.hash = href;
    }
    setActiveSection(targetId);
  }
}

desktopLinks.forEach(link => link.addEventListener('click', (e) => handleTocClick(e, link)));
mobileLinks.forEach(link => link.addEventListener('click', (e) => handleTocClick(e, link)));

if (mobileTrigger) {
  mobileTrigger.addEventListener('click', () => {
    const isOpen = mobileDrawer && mobileDrawer.classList.contains('open');
    if (isOpen) closeMobileDrawer();
    else openMobileDrawer();
  });
}
if (mobileClose) mobileClose.addEventListener('click', closeMobileDrawer);
if (mobileBackdrop) mobileBackdrop.addEventListener('click', closeMobileDrawer);

// Share Signal & Citation Copy
async function handleShareSignal(btn) {
  const articleH1 = document.querySelector('h1.article-title, h1');
  const articleTitle = articleH1 ? articleH1.textContent.trim() : document.title.split('—')[0].trim();
  const url = window.location.href.split('#')[0];
  const citation = `Tyler Koshakow (${articleTitle}) (${url})`;
  
  if (navigator.share && /mobile|android|iphone|ipad/i.test(navigator.userAgent.toLowerCase())) {
    try {
      await navigator.share({
        title: articleTitle,
        text: `Tyler Koshakow (${articleTitle})`,
        url: url
      });
      return;
    } catch (err) {
      if (err.name !== 'AbortError') console.warn('Share failed, falling back to copy', err);
      else return;
    }
  }

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(citation);
    } else {
      const ta = document.createElement('textarea');
      ta.value = citation;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }

    const btnText = btn.querySelector('.btn-text');
    const originalText = btnText ? btnText.textContent : '';
    if (btnText) btnText.textContent = 'Citation Copied!';
    btn.classList.add('copied');
    
    setTimeout(() => {
      if (btnText) btnText.textContent = originalText;
      btn.classList.remove('copied');
    }, 2500);
  } catch (copyErr) {
    console.error('Failed to copy citation', copyErr);
  }
}

document.querySelectorAll('.desktop-share-btn, .mobile-share-btn').forEach(btn => {
  btn.addEventListener('click', () => handleShareSignal(btn));
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (mobileDrawer && mobileDrawer.classList.contains('open')) closeMobileDrawer();
    if (document.documentElement.getAttribute('data-theme') === 'goblin') applyTheme('dark', false);
  }
});
```

- **Theme & Goblin Mode Compatibility:** Full reactivity across Light, Dark, and Goblin modes. All navigation structural elements must be exempted from chaotic float physics (`animation: none !important; transform: none !important;`).

---

## 3. Abstract Minimalist Graphic & Diagram Aesthetic

Every technical diagram must adhere to the site's strict abstract minimalist aesthetic: pure HTML/SVG vector geometry, electronic engineering metaphors, theme-reactivity, and subtle micro-interactions.

### Architectural Guidelines
1. **Pure Semantic SVG:** Always embed directly in HTML wrapped in `<figure class="diagram-container"><div class="diagram-wrapper"><svg class="aeo-diagram" viewBox="...">...</svg></div></figure>`.
2. **Abstract Node Boxes:** Rectangles with subtle corner radii (`rx="3"` or `rx="4"`), filled with `var(--bg)` and stroked with `var(--border-subtle)`.
3. **Electronic Engineering Metaphors:**
   - Use operational amplifier / buffer symbols (`<polygon points="..." class="amp-triangle" />`) to illustrate **Marketing amplification & outward distribution**.
   - Radiating vector rays broadcasting outward into multiple channels.
4. **Closed Telemetry Loops:** Symmetrical 2x2 grid layouts with clean orthogonal paths and dashed return rails (`stroke-dasharray: 3 3`) routing intelligence back to `Product`.
5. **No Clutter:** Avoid wordy subtitles or redundant text inside nodes. Keep node titles clean, punchy, and centered.

### Interactive Micro-Telemetry on Hover
- **No Browser Default Tooltips:** Do not use native `<title>` elements inside inner SVG shapes that trigger delayed OS tooltip popups.
- **In-Card Monospace Status Readout:** Place a dedicated live status bar at the bottom of the card:
  ```html
  <div class="diagram-status" aria-live="polite">
    <span class="status-text" data-default="telemetry // hover node to inspect signal flow">telemetry // hover node to inspect signal flow</span>
  </div>
  ```
- **Node Data Hints:** Add `data-hint="..."` attributes to each `.diagram-node`. On `mouseenter`, JavaScript updates `.status-text` with the specific node's definition; on `mouseleave`, it restores the default hint.
- **Soft Focus Sibling Dimming:** When hovering over the diagram, non-hovered sibling nodes gently dim to `45%` opacity (`.aeo-diagram:hover .diagram-node:not(:hover) { opacity: 0.45; }`).
- **Animated Signal Pulse:** On diagram hover, connective vector paths animate with flowing dashed electron pulses (`@keyframes signalPulseFlow { from { stroke-dashoffset: 16; } to { stroke-dashoffset: 0; } }`).

---

## 4. Theme & Goblin Mode Compatibility

All pages and diagrams must seamlessly react to the three site themes:

Mode       | Aesthetic & Colors
:--------- | :-----------------------------------------------------------------------------------------------------
**Light**  | Stark, crisp `#111111` lines, clean background `#ffffff`, card background `#f6f6f6`, subtle `#eaeaea` borders.
**Dark**   | High-contrast `#f3f3f3` text, deep card `#161618`, dark background `#0e0e10`, subtle `#222225` borders.
**Goblin** | Deep radioactive swamp `#050f07`, toxic `#39ff14` neon phosphor glow, animated SVG signal surges, and full zero-gravity float physics.

### Goblin Mode Rules
- The fixed HUD capsule (`.theme-selector`) glides smoothly across the viewport to the screen center via JavaScript FLIP morphing (`morphThemeSelector`).
- High-amplitude breathing animation (`@keyframes goblinCapsuleBreathe`) begins after the FLIP transition settles.
- All body text elements participate in dynamic floating physics (`requestAnimationFrame` with sine/cosine offsets).
- Pressing `Escape` or clicking `Light`/`Dark` instantly stops float chaos and restores standard formatting.

---

## 5. Machine-Readable Structured Data & SEO Specs

Every new post must include comprehensive machine-readable metadata in the `<head>`:

### JSON-LD Entity Graph (`<script type="application/ld+json">`)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "@id": "https://tylerkoshakow.com/signals/SLUG.html#article",
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://tylerkoshakow.com/#website",
        "name": "Tyler 'TK' Koshakow",
        "url": "https://tylerkoshakow.com"
      },
      "headline": "ARTICLE_TITLE",
      "description": "ARTICLE_SUMMARY",
      "datePublished": "YYYY-MM-DD",
      "dateModified": "YYYY-MM-DD",
      "mainEntityOfPage": "https://tylerkoshakow.com/signals/SLUG.html",
      "author": {
        "@type": "Person",
        "@id": "https://tylerkoshakow.com/#person",
        "name": "Tyler 'TK' Koshakow",
        "jobTitle": "Enterprise AEO/SEO Strategist",
        "url": "https://tylerkoshakow.com"
      },
      "publisher": {
        "@type": "Person",
        "@id": "https://tylerkoshakow.com/#person",
        "name": "Tyler 'TK' Koshakow"
      },
      "about": [
        { "@type": "Thing", "name": "Answer Engine Optimization (AEO)" },
        { "@type": "Thing", "name": "User-Generated Content (UGC)" }
      ],
      "mentions": [
        { "@type": "Person", "name": "MENTIONED_ENTITY" }
      ]
    }
  ]
}
```

### Essential Meta Tags
- Canonical: `<link rel="canonical" href="https://tylerkoshakow.com/signals/SLUG.html">`
- OpenGraph: `og:title`, `og:description`, `og:type="article"`, `og:url`, `article:published_time`, `article:author`
- Twitter Card: `twitter:card="summary_large_image"`, `twitter:title`, `twitter:description`
- Immediate theme preload script in `<head>` to prevent Flash of Unstyled Content (FOUC).

---

## 6. Two-Phase Publishing & Editorial Review Workflow

**MANDATORY RULE:** Never promote drafts directly to production or synchronize feeds without explicit human editorial sign-off.

```
+-------------------------------------------------------------------------------+
| PHASE 1: DRAFTING & REVIEW (Isolated / Staging)                               |
|                                                                               |
| 1. Author Draft -> Save to /drafts/<slug>.html (or .md)                       |
|    - Excluded from sitemap.xml, index.html feed, and llms.txt                 |
| 2. Export to Google Docs -> `python3 scripts/gdocs_review.py export <file>`   |
|    - Or provide full in-chat markdown artifact for review                     |
| 3. Human Editorial Review -> User leaves comments, notes & suggested edits    |
| 4. Ingest Feedback -> `python3 scripts/gdocs_review.py pull <doc_id>`         |
|    - Apply edits to local draft until human sign-off is given                 |
+-------------------------------------------------------------------------------+
                                      |
                       [Explicit Human "Publish" Approval]
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2: PRODUCTION SYNCHRONIZATION & DEPLOYMENT                              |
|                                                                               |
| 1. Promote to Production: Move `/drafts/<slug>.html` to `/signals/<slug>.html`|
| 2. Update Homepage Feed: Add entry to `index.html` under `#content-feed`      |
| 3. Update Machine Knowledge Graphs: Update `llms.txt` and `llms-full.txt`     |
| 4. Regenerate XML Sitemap: Run `python3 scripts/generate_sitemap.py`          |
| 5. Run Pre-Publish QA: Run `python3 scripts/validate_site.py`                 |
| 6. Bump Stylesheet Cache-Buster: Increment `style.css?v=...` across all HTML  |
| 7. Commit & Push: Deploy live to Vercel                                       |
+-------------------------------------------------------------------------------+
```

---

## 7. Pre-Publish Quality Assurance (`scripts/validate_site.py`)

Before committing any published signal or draft:
1. Always run the automated validator:
   ```bash
   python3 scripts/validate_site.py
   ```
2. The validator guarantees:
   - All inline JavaScript blocks parse without syntax errors via `node --check`.
   - No string interpolation bugs or empty template literals (e.g. `style.transform = ;`).
   - JSON-LD structured data is 100% valid JSON.
   - Canonical URLs and OpenGraph tags are present.

---

## 7. Canonical Article Boilerplate Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <title>POST_TITLE — Tyler 'TK' Koshakow</title>
  <meta name="description" content="POST_SUMMARY">
  <link rel="canonical" href="https://tylerkoshakow.com/signals/POST_SLUG.html">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">
  
  <!-- OpenGraph Meta Tags -->
  <meta property="og:title" content="POST_TITLE">
  <meta property="og:description" content="POST_SUMMARY">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://tylerkoshakow.com/signals/POST_SLUG.html">
  <meta property="article:published_time" content="YYYY-MM-DD">
  <meta property="article:author" content="Tyler 'TK' Koshakow">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="POST_TITLE">
  <meta name="twitter:description" content="POST_SUMMARY">
  
  <link rel="stylesheet" href="../style.css?v=goblin12">
  
  <!-- Inline Script to Prevent Theme Flash (FOUC) -->
  <script>
    (function() {
      const savedTheme = localStorage.getItem('theme');
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', theme);
    })();
  </script>
  
  <!-- JSON-LD Entity Graph -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "TechArticle",
        "@id": "https://tylerkoshakow.com/signals/POST_SLUG.html#article",
        "isPartOf": {
          "@type": "WebSite",
          "@id": "https://tylerkoshakow.com/#website",
          "name": "Tyler 'TK' Koshakow",
          "url": "https://tylerkoshakow.com"
        },
        "headline": "POST_TITLE",
        "description": "POST_SUMMARY",
        "datePublished": "YYYY-MM-DD",
        "dateModified": "YYYY-MM-DD",
        "mainEntityOfPage": "https://tylerkoshakow.com/signals/POST_SLUG.html",
        "author": {
          "@type": "Person",
          "@id": "https://tylerkoshakow.com/#person",
          "name": "Tyler 'TK' Koshakow",
          "jobTitle": "Enterprise AEO/SEO Strategist",
          "url": "https://tylerkoshakow.com"
        },
        "publisher": {
          "@type": "Person",
          "@id": "https://tylerkoshakow.com/#person",
          "name": "Tyler 'TK' Koshakow"
        }
      }
    ]
  }
  </script>
</head>
<body>
  <div class="container">
    
    <!-- TOP NAVIGATION -->
    <header>
      <div class="header-top">
        <a href="/" class="nav-back">&larr; TK</a>
        <div class="theme-selector" role="group" aria-label="Select theme mode">
          <button type="button" class="theme-option" data-theme-val="light" aria-pressed="false">Light</button>
          <button type="button" class="theme-option" data-theme-val="dark" aria-pressed="false">Dark</button>
          <button type="button" class="theme-option" data-theme-val="goblin" aria-pressed="false">Goblin</button>
        </div>
      </div>
    </header>

    <!-- ARTICLE MAIN CONTENT -->
    <main>
      <article class="article-detail" itemscope itemtype="https://schema.org/TechArticle">
        
        <header class="article-header">
          <div class="feed-meta">
            <time datetime="YYYY-MM-DD" itemprop="datePublished">Month DD, YYYY</time>
            <span class="type-tag">Online // Signal XXX</span>
          </div>
          <h1 class="article-title" itemprop="headline">POST_TITLE</h1>
          <p class="article-author" itemprop="author">Tyler &ldquo;TK&rdquo; Koshakow</p>
        </header>

        <div class="article-content" itemprop="articleBody">
          <!-- Standard Paragraphs (No .lead class) -->
          <p>
            Opening paragraph text...
          </p>

          <!-- Key thesis followed by graphical pullquote -->
          <p>
            Asynchronous downloads prevent DOM parsing blocks, but they cannot prevent main-thread execution freezes once third-party scripts compile.
          </p>

          <figure class="pullquote">
            <blockquote>
              &ldquo;Asynchronous downloads don't block the DOM,<br>but they still freeze the main thread.&rdquo;
            </blockquote>
          </figure>

          <!-- SVG Abstract Diagram 1 -->
          <figure class="diagram-container" aria-label="Abstract diagram: Proof Creation & Marketing Distribution">
            <div class="diagram-wrapper">
              <svg viewBox="0 0 620 160" class="aeo-diagram" xmlns="http://www.w3.org/2000/svg" role="img">
                <!-- SVG Diagram Content -->
              </svg>
              <div class="diagram-status" aria-live="polite">
                <span class="status-text" data-default="telemetry // hover node to inspect signal flow">telemetry // hover node to inspect signal flow</span>
              </div>
            </div>
          </figure>

          <h2>Section Heading</h2>
          <p>Body paragraph text...</p>

          <h3>Subordinate Drilldown</h3>
          <p>Detailed analysis...</p>

          <h2>The Case for C-Suite Reporting</h2>

          <!-- SVG Abstract Diagram 2 (Closed Loop) -->
          <figure class="diagram-container" aria-label="Abstract diagram: The Product-AEO Telemetry Loop">
            <div class="diagram-wrapper">
              <svg viewBox="0 0 600 240" class="aeo-diagram" xmlns="http://www.w3.org/2000/svg" role="img">
                <!-- SVG 4-Node Closed Loop -->
              </svg>
              <div class="diagram-status" aria-live="polite">
                <span class="status-text" data-default="loop // hover node to inspect intelligence cycle">loop // hover node to inspect intelligence cycle</span>
              </div>
            </div>
          </figure>
          
          <p>Closing executive takeaways...</p>
        </div>

      </article>
    </main>

    <!-- FOOTER NODE -->
    <footer>
      <div class="footer-meta">
        <p>&copy; 2026 Tyler &ldquo;TK&rdquo; Koshakow. All rights reserved.</p>
      </div>
      <div class="footer-links">
        <a href="/" title="Home">/home</a> &bull;
        <a href="/llms.txt" title="Machine Readable Overview">/llms.txt</a> &bull; 
        <a href="/llms-full.txt" title="Unpaginated Knowledge Ingestion">/llms-full.txt</a> &bull; 
        <a href="/sitemap.xml" title="XML Sitemap">/sitemap.xml</a>
      </div>
    </footer>
    
  </div>

  <!-- Interactive Scripts (Theme Selector, Goblin Physics & Micro-Telemetry) -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const themeButtons = document.querySelectorAll('.theme-option');
      let goblinRAF = null;
      let goblinElements = [];

      function startGoblinChaos() {
        stopGoblinChaos();
        const selector = 'h1, h2, h3, h4, p, a, li, time, blockquote, .type-tag, .article-author, .article-title';
        const rawEls = document.querySelectorAll(selector);
        goblinElements = [];
        
        rawEls.forEach((el, index) => {
          if (el.closest('.header-top') || el.closest('.theme-selector')) return;
          
          goblinElements.push({
            el: el,
            speedX: 0.0012 + (index % 5) * 0.0005,
            speedY: 0.0016 + (index % 4) * 0.0006,
            speedRot: 0.0011 + (index % 3) * 0.0004,
            ampX: 40 + (index % 7) * 12,
            ampY: 35 + (index % 6) * 10,
            ampRot: 14 + (index % 5) * 5,
            phaseX: index * 1.3,
            phaseY: index * 2.1,
            phaseRot: index * 0.8
          });
          el.style.display = 'inline-block';
          el.style.position = 'relative';
          el.style.transition = 'none';
        });
        
        const startTime = performance.now();
        function loop(now) {
          const elapsed = now - startTime;
          goblinElements.forEach(item => {
            const x = Math.sin(elapsed * item.speedX + item.phaseX) * item.ampX;
            const y = Math.cos(elapsed * item.speedY + item.phaseY) * item.ampY;
            const rot = Math.sin(elapsed * item.speedRot + item.phaseRot) * item.ampRot;
            item.el.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0) rotate(${rot.toFixed(1)}deg)`;
          });
          goblinRAF = requestAnimationFrame(loop);
        }
        goblinRAF = requestAnimationFrame(loop);
      }

      function stopGoblinChaos() {
        if (goblinRAF) {
          cancelAnimationFrame(goblinRAF);
          goblinRAF = null;
        }
        if (goblinElements.length) {
          goblinElements.forEach(item => {
            item.el.style.transform = '';
            item.el.style.display = '';
            item.el.style.position = '';
            item.el.style.transition = '';
          });
          goblinElements = [];
        }
      }

      function morphThemeSelector(newTheme, callback) {
        const selector = document.querySelector('.theme-selector');
        if (!selector) {
          callback();
          return;
        }

        selector.classList.remove('breathe');

        const firstRect = selector.getBoundingClientRect();
        callback();
        const lastRect = selector.getBoundingClientRect();

        const deltaX = firstRect.left - lastRect.left;
        const deltaY = firstRect.top - lastRect.top;
        const scaleX = firstRect.width / (lastRect.width || 1);
        const scaleY = firstRect.height / (lastRect.height || 1);

        if (Math.abs(deltaX) < 1 && Math.abs(deltaY) < 1) {
          if (newTheme === 'goblin') {
            selector.classList.add('breathe');
          }
          return;
        }

        selector.style.transition = 'none';
        selector.style.transform = `translate3d(${deltaX}px, ${deltaY}px, 0) scale(${scaleX}, ${scaleY})`;
        
        selector.getBoundingClientRect();

        selector.style.transition = 'transform 0.65s cubic-bezier(0.34, 1.4, 0.64, 1), border-radius 0.65s ease, box-shadow 0.65s ease, background-color 0.55s ease, border-color 0.55s ease, padding 0.55s ease';
        selector.style.transform = (newTheme === 'goblin') ? 'translateX(-50%)' : 'none';

        setTimeout(() => {
          selector.style.transition = '';
          if (newTheme === 'goblin') {
            selector.classList.add('breathe');
          } else {
            selector.style.transform = '';
            selector.classList.remove('breathe');
          }
        }, 660);
      }

      function applyTheme(theme, isInitial) {
        const execute = () => {
          document.documentElement.setAttribute('data-theme', theme);
          localStorage.setItem('theme', theme);
          themeButtons.forEach(btn => {
            const val = btn.getAttribute('data-theme-val');
            if (val === theme) {
              btn.classList.add('active');
              btn.setAttribute('aria-pressed', 'true');
            } else {
              btn.classList.remove('active');
              btn.setAttribute('aria-pressed', 'false');
            }
          });

          if (theme === 'goblin') {
            startGoblinChaos();
          } else {
            stopGoblinChaos();
          }
        };

        if (isInitial) {
          execute();
          const selector = document.querySelector('.theme-selector');
          if (selector && theme === 'goblin') {
            selector.classList.add('breathe');
          }
        } else {
          morphThemeSelector(theme, execute);
        }
      }
      
      themeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const selected = btn.getAttribute('data-theme-val');
          applyTheme(selected, false);
        });
      });
      
      const initialTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      applyTheme(initialTheme, true);

      // Interactive Micro-Telemetry Status Readout
      document.querySelectorAll('.diagram-wrapper').forEach(wrapper => {
        const statusEl = wrapper.querySelector('.status-text');
        if (!statusEl) return;
        const defaultText = statusEl.getAttribute('data-default');
        const nodes = wrapper.querySelectorAll('.diagram-node');
        
        nodes.forEach(node => {
          node.addEventListener('mouseenter', () => {
            const hint = node.getAttribute('data-hint');
            if (hint) {
              statusEl.textContent = hint;
              statusEl.style.color = 'var(--fg)';
            }
          });
          node.addEventListener('mouseleave', () => {
            statusEl.textContent = defaultText;
            statusEl.style.color = '';
          });
        });
      });

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && document.documentElement.getAttribute('data-theme') === 'goblin') {
          applyTheme('dark', false);
        }
      });
    });
  </script>
</body>
</html>
```
