---
name: search-intelligence
description: >-
  Perform deep search intelligence research: analyze target keywords, classify SERP results via
  genus-species content taxonomy, identify competitor triads, extract ranked keywords, search volume,
  and ETV (Estimated Traffic Volume) using DataForSEO, deconstruct heading and topic hierarchies,
  diagnose winning content mechanics, and produce actionable, authoritative content briefs.
---

# Search Intelligence Skill

This skill defines the end-to-end workflow for conducting **Search Intelligence Research**—a systematic, practitioner-grade methodology for reverse-engineering what is winning in organic search for any target topic and synthesizing those insights into an actionable content blueprint.

---

## 1. Core Methodology Overview

```
+-------------------------------------------------------------------------------+
| 1. TARGET KEYWORD & SERP INGESTION                                            |
|    Input seed topic -> Fetch live Google SERP (DataForSEO / Search APIs)      |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| 2. GENUS-SPECIES TAXONOMY CLASSIFICATION                                      |
|    Genus = Content Format / Type (e.g. Informational Article, Product Page)   |
|    Species = Specific Topical Intent (e.g. GA4 Impact on PageSpeed)           |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| 3. KERNEL SELECTION & COMPETITOR TRIAD (1–3 URLs)                             |
|    Pick #1 Kernel matching Genus-Species -> Find 1–2 matching peer URLs       |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| 4. KEYWORD & ETV INTELLIGENCE (DataForSEO)                                    |
|    Pull ranking keywords, positions, search volumes, and ETV per URL          |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| 5. STRUCTURAL ANATOMY & HEADING DECONSTRUCTION                                |
|    Extract H1, H2, H3 hierarchy, topic coverage, tables, and media assets     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| 6. WINNER DIAGNOSIS & ACTIONABLE REPORT ARTIFACT                              |
|    Identify why the top ETV piece is winning -> Generate Intelligence Report  |
+-------------------------------------------------------------------------------+
```

---

## 2. Genus-Species Content Taxonomy

Always classify every SERP result using the **Genus-Species Framework**:

### The Genus (Content Format / Intent Archetype)
Genus                   | Description & Identifying Characteristics
:---------------------- | :------------------------------------------------------------------------------------
**Informational Article** | In-depth editorial guide, analysis, case study, or conceptual explainer.
**Product / Feature Page** | Commercial landing page, software feature showcase, or conversion-focused asset.
**Third-Party Review**    | Independent multi-vendor comparison, affiliate roundup, or editorial evaluation.
**UGC / Community**       | Reddit threads, StackOverflow discussions, Netlify/community forum answers.
**Documentation / Ref**   | Official API reference, developer documentation, or standard specification.
**Tool / Calculator**     | Interactive web application, benchmark scanner, or calculation tool.

### The Species (Specific Problem Angle & Topic)
The **Species** defines the precise topical query and user problem being addressed (e.g., *"Does GA4 affect mobile PageSpeed Insights scores?"*).

---

## 3. Step-by-Step Execution Workflow

### Step 1: Query the SERP
1. Run a live Google SERP query for the seed target keyword using `dataforseo_cli.py serp "<keyword>"` (or web search tools).
2. Review the top 10 organic results.

### Step 2: Select the Kernel & Assemble the Competitor Triad
1. **The Kernel (URL #1):** Select the highest-ranking organic result that strictly matches your target **Genus-Species**.
2. **The Peers (URLs #2 & #3):** Find 1 to 2 additional URLs on the same or adjacent SERPs that share the identical genus-species classification.
3. *Discard false matches:* Do not pair a Reddit thread (UGC) or an official Google API doc (Documentation) with an Informational Article. Maintain strict genus alignment.

### Step 3: Extract Ranking Keywords & ETV
For each URL in the triad, pull ranking intelligence via DataForSEO:
* **Ranking Keywords:** What distinct queries is this specific URL ranking for?
* **Rank Positions:** Positions 1–10 (first page).
* **Monthly Search Volume:** Search demand for each keyword.
* **ETV (Estimated Traffic Volume / Value):** The calculated organic traffic driven to that specific URL.

### Step 4: Deconstruct Headings & Content Architecture
For each URL in the triad, fetch the content (`read_url_content`) and extract:
1. **Heading Skeleton:** Full `<h1>`, `<h2>`, `<h3>` tree.
2. **Subtopics & Key Concepts Covered:** What questions, technical depth, or definitions are included?
3. **Content Assets:** Tables, diagrams, code blocks, screenshots, original benchmark data, FAQs.
4. **Shared Common Characteristics:** What structural elements appear across *all* winning pieces?

### Step 5: Diagnose the Winning Piece
Identify the #1 top-performing piece (highest ETV and top positions) and answer:
* **What is it doing that makes it win?**
  * Did it provide a more direct, definitive answer above the fold?
  * Does it include comprehensive comparison tables or code snippets?
  * Does it have superior technical depth or fresh empirical data?
  * Is it targeting high-volume secondary keywords in its subheadings?

---

## 4. Search Intelligence Report Template

Every search intelligence task must produce a structured Markdown artifact following this standard format:

```markdown
# Search Intelligence Brief: [Topic / Target Keyword]

> **Target Keyword:** [Primary Keyword]  
> **Genus:** [e.g. Informational Article]  
> **Species:** [e.g. Does GA4 Slow Down PageSpeed]  
> **Date:** [YYYY-MM-DD]

---

## 1. Competitor Triad & SERP Landscape

| URL | Domain | Target Genus | Top Ranking Keyword | Total Ranking Keywords | Peak ETV |
| :-- | :----- | :----------- | :------------------ | :--------------------- | :------- |
| **URL #1 (Kernel)** | domain.com | Informational Article | keyword | XX | XXX |
| **URL #2 (Peer)** | domain.com | Informational Article | keyword | XX | XXX |
| **URL #3 (Peer)** | domain.com | Informational Article | keyword | XX | XXX |

---

## 2. Keyword Universe & Traffic Distribution

### High-Value Shared Keywords
* `keyword 1` (Vol: XX | CPC: $X.XX | Top Rank: #X)
* `keyword 2` (Vol: XX | CPC: $X.XX | Top Rank: #X)

---

## 3. Structural Teardown & Heading Hierarchy Matrix

| Content Section / Topic | URL #1 (Winner) | URL #2 | URL #3 | Standard Requirement? |
| :---------------------- | :-------------- | :----- | :----- | :-------------------- |
| **Core Problem Definition** | ✅ H2 | ✅ H2 | ❌ | Mandatory |
| **Empirical / Benchmark Data** | ✅ Tables | ❌ Text | ❌ | Competitive Differentiator |
| **Step-by-Step Fix / Code** | ✅ H2 + Code | ✅ H2 | ✅ H2 | Mandatory |
| **FAQ Section** | ✅ 4 FAQs | ❌ | ✅ 3 FAQs | Recommended |

---

## 4. Why the Winner is Winning (The #1 Teardown)
* **Core Advantage:** [Why this URL holds the top position / ETV]
* **Content Gaps & Vulnerabilities:** [What the winner missed that we can exploit]

---

## 5. Strategic Content Recommendations
1. **Primary Keyword Strategy:** [Primary H1 and title tag formulation]
2. **Heading & Subtopic Blueprint:** [Recommended H2 and H3 skeleton]
3. **Data & Asset Integration:** [Tables, diagrams, or original test figures to include]
4. **Tone & Angle:** [How to merge original research with winning search intent]
```
