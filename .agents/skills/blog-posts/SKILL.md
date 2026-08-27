---
name: blog-posts
description: Comprehensive editorial, typographic, abstract graphic design, and technical publishing guidelines for articles and signals on Tyler "TK" Koshakow's personal website.
---

# TK Blog Posts & Signals Publishing Skill

This skill defines the editorial standards, typographic rules, abstract minimalist graphic aesthetic, theme compatibility, and structured data specifications for creating and publishing posts on Tyler "TK" Koshakow's personal website.

---

## 1. Editorial Voice & Core Principles

- **Core Slogan / Philosophy:** *"Good marketing distributes proof, good product creates it."*
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

### In-Text Slogans & Quotations
- **Rule:** When pulling a slogan or thesis out into a graphical pull quote, **always preserve the full sentence inside the body paragraph text**.
- **Example in Paragraph:**
  ```html
  <p>
    Rankings and clicks are great, but the main thing they indicate is how good your SEO program is. Here is my new slogan: Good marketing distributes proof, good product creates it. The power of AEO analytics is its ability to tell you how good your product is.
  </p>
  ```

### Editorial Graphical Pull Quotes
- **Rule:** Pull quotes must be styled as a clean graphical element with top and bottom hairline borders, centered alignment, and **must break at the comma with a `<br>` tag**.
- **Markup:**
  ```html
  <figure class="pullquote">
    <blockquote>
      &ldquo;Good marketing distributes proof,<br>good product creates it.&rdquo;
    </blockquote>
  </figure>
  ```
- **CSS Specifications:**
  - Border: `1px solid var(--border-subtle)` on top and bottom only (no heavy left border).
  - Alignment: `text-align: center;`
  - Font: `font-size: var(--text-lg); font-weight: 600; line-height: 1.35; font-style: normal; color: var(--fg); letter-spacing: -0.02em;`
  - Margin: `margin: var(--space-xl) 0; padding: var(--space-lg) var(--space-md);`

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

## 6. Multi-Channel Synchronization Checklist

Whenever a new post is published:
1. **Create Standalone Page:** Save to `/signals/<slug>.html` using the template below.
2. **Update Homepage Feed:** Add active post card to `index.html` under `<section id="content-feed">` as `Online // Signal XXX`.
3. **Update Machine Knowledge Graphs:**
   - Add entry to `/llms.txt`.
   - Concatenate complete article text to `/llms-full.txt`.
4. **Bump Stylesheet Cache-Buster:** Increment `style.css?v=...` across all HTML files.

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

          <!-- In-text slogan followed by graphical pullquote -->
          <p>
            Contextual paragraph containing the full slogan: Good marketing distributes proof, good product creates it.
          </p>

          <figure class="pullquote">
            <blockquote>
              &ldquo;Good marketing distributes proof,<br>good product creates it.&rdquo;
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
        <a href="/llms-full.txt" title="Unpaginated Knowledge Ingestion">/llms-full.txt</a>
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
