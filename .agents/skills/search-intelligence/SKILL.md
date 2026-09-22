---
name: search-intelligence
description: >-
  Conduct rigorous, objective search intelligence: ingest target keywords, competitor URLs, or both;
  query DataForSEO for search volumes, CPC, ranked keywords, and URL ETV; classify SERPs via
  genus-species taxonomy; assemble competitor triads; extract exhaustive heading trees with indexed reference IDs;
  synthesize granular unabstracted competitor teardowns; generate an objective baseline article skeleton with
  clickable cross-referencing superscripts; document excluded topics; and publish natively formatted Google Docs reports.
---

# Search Intelligence Skill

This skill defines the end-to-end methodology and technical execution for conducting **Search Intelligence Research**—a systematic, practitioner-grade workflow for reverse-engineering what is winning in organic search for any topic or competitive URL, deconstructing the exact claims and mechanics of the competitor triad, and synthesizing those findings into an **objective baseline content brief and article skeleton**.

---

## 0. Fundamental Directive: Pure Objectivity (Zero POV Grafting)

> [!IMPORTANT]
> **Strict Separation Rule:** The Search Intelligence Brief must be **100% objective, descriptive, and un-grafted**.
> * Do **NOT** introduce subjective points of view, internal editorial theses, company slogans, or unique personal commentary into the Search Intelligence brief or the baseline skeleton.
> * There must be **ZERO mention of POV, editorial biases, or opinion hooks** in the Search Intelligence output.
> * The brief's sole mission is to document:
>   1. What search engines currently rank and reward.
>   2. What questions, claims, costs, timelines, and arguments competitors are *actually publishing*.
>   3. The exact structural skeleton required to satisfy search intent and surpass competitive coverage.
> * Strategic points of view (POV) and unique editorial layers are applied in a **subsequent phase** by the author/strategist.

---

## 1. Input Flexibility: Ingestion Modes

The search intelligence engine must accept and gracefully handle three distinct entry points:

```
                      +-----------------------------+
                      |       USER INPUT MODE       |
                      +-----------------------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
         v                           v                           v
+-------------------+       +-------------------+       +-------------------+
|  1. KEYWORD-FIRST |       |    2. URL-FIRST   |       |     3. HYBRID     |
| Seed keyword(s)   |       | Competitor URL(s) |       | Seed keyword(s) + |
| provided by user  |       | provided by user  |       | competitor URL(s) |
+-------------------+       +-------------------+       +-------------------+
         |                           |                           |
         | Query SERP                | Reverse-engineer KWs      | Expand SERP & KWs
         | Identify Top Triad        | Identify Triad Peers      | Validate Triad
         +---------------------------+---------------------------+
                                     |
                                     v
                      +-----------------------------+
                      |   LOCKED COMPETITOR TRIAD   |
                      |   (1 Kernel + 2 Peers)      |
                      +-----------------------------+
```

1. **Mode A: Keyword-First Input**
   * *Trigger:* User provides one or more seed keywords (e.g., `aeo agency vs in house`, `are aeo agencies worth it`).
   * *Action:* Query search volume data -> pull live Google SERP -> filter out non-matching formats -> identify the #1 Intent Kernel URL -> discover 2 peer URLs on the SERP sharing the identical intent.
2. **Mode B: URL-First Input**
   * *Trigger:* User provides a competitor article URL or industry piece (e.g., `https://automatonagency.com/insights/are-aeo-agencies-worth-it`).
   * *Action:* Extract ranked keywords for that URL via DataForSEO -> identify the core ranking intent query -> pull live SERP for that query to locate the 2 closest peer URLs.
3. **Mode C: Hybrid Input**
   * *Trigger:* User provides both seed keywords and target competitor URLs.
   * *Action:* Validate alignment between the provided URLs and the target keywords -> fill any gaps to ensure a robust triad.

---

## 2. Technical Data Extraction: DataForSEO Integration

Search intelligence relies on live search data from DataForSEO. Always use the active authenticated credentials configured in the environment.

### Environment & Authentication
* **Configuration Path:** `/Users/tylerkoshakow/Documents/antigravity/Screaming Frog Audit/.env`
* **Active Account:** `tyler.koshakow@hexagon.com`
* **Auth Scheme:** HTTP Basic Auth (`Authorization: Basic dHlsZXIua29zaGFrb3dAaGV4YWdvbi5jb206NTBmZjU1NWMwOTFlYzljNA==`)

### Core API Endpoints
1. **Keyword Search Volumes & CPC:**
   * `POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live`
   * Extracts exact monthly search volume, 12-month trend, competition index, and CPC for primary and parent category queries.
2. **Live SERP Analysis:**
   * `POST https://api.dataforseo.com/v3/serp/google/organic/live/regular`
   * Payload: `[{"keyword": "<query>", "location_code": 2840, "language_code": "en", "depth": 20}]`
   * Inspects real-time organic rankings, featured snippets, knowledge panels, and SERP features.
3. **URL & Domain Ranked Keywords:**
   * `POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live`
   * *Target Formatting:* Pass clean domain or subfolder without `https://` (e.g., `www.thebusinessrover.com/blog/aeo-tools-vs-agency-vs-in-house`).
   * Extracts total ranked keywords, rank distribution (Top 3, Top 10), and calculated **ETV (Estimated Traffic Volume)**.

---

## 3. The Genus-Species Taxonomy & Competitor Triad

Every SERP contains diverse content formats. To produce an actionable brief, you must enforce strict **Genus-Species alignment**:

### The Genus (Format Archetype)
* **Informational Strategic Teardown / Guide:** Deep long-form editorial, architectural breakdown, or evaluation framework.
* **Product / Feature Landing Page:** Commercial software sales page.
* **UGC / Community Forum:** Reddit, StackOverflow, or community threads (used as skepticism/voice-of-customer anchors, but not as structural peers).
* **Documentation / API Reference:** Official technical specs.

### The Competitor Triad Structure
Assemble exactly three closely matched competitors:
1. **URL #1 (The Kernel):** The highest-ranking organic piece strictly matching the target genus and species.
2. **URL #2 (Peer A):** A strong organic competitor offering an alternative angle or deeper tactical breakdown.
3. **URL #3 (Peer B):** An enterprise-level or high-authority peer offering clear budget, resourcing, or capability frameworks.

---

## 4. Extraction Anatomy: What Are They Actually Saying?

Search intelligence requires **extreme granularity and non-abstract extraction**. Never settle for vague summaries like *"they discuss pricing and capabilities."* Extract the literal facts, dollar figures, timelines, and arguments.

### Mandatory Fact Extraction Checklist
For every competitor piece, systematically extract:
1. **The Scope of Work:** What specific deliverables, technical tasks, or operational rhythms do they say the discipline actually entails?
2. **The Exact Financial Numbers:**
   * Published agency retainer rates (minimums, mid-tiers, enterprise retainers).
   * In-house salary benchmarks, tool costs, training budgets, and total loaded first-year costs.
   * Self-serve software fees and **hidden internal labor costs** (hours per month x loaded hourly rate).
3. **When to Buy (Rational Use Cases):** Deal size thresholds, ACV minimums, internal bandwidth bottlenecks, urgent time-to-market constraints.
4. **When NOT to Buy (Honest Disqualifiers):** Pre-positioning/pre-product stages, absence of content foundations, non-conversational buyer journeys, existing internal capability.
5. **Operational Limitations:** What can software tools *not* do? (e.g., why software fails at offsite publisher relationships, PR pitching, and relationship building).
6. **Ramp Timelines:** How long does it take an in-house team to become effective (e.g., with SEO background vs. starting from scratch)?
7. **Vetting Standards & Red Flags:** The "Who owns the checking?" test, published citation ledgers, red flags (guaranteed rankings, repurposed legacy SEO decks, lack of multi-platform tracking).
8. **Hybrid Operating Models:** Exact definitions of how high-performing companies divide responsibilities between internal owners and external specialists.
9. **Accountability & Verification Tests:** Time-bound testing cycles (e.g., 90-day closed-loop verification frameworks).

---

## 5. Indexed Heading Inventory & Clickable Cross-Referencing

To provide complete auditability, the brief links every observation directly to its source heading using an indexed reference system.

### Heading Indexing Rule
* In **Section 3 (Exhaustive Heading Inventory)**, extract **100% of headings (H1 through H3)** across all three competitors.
* Assign each heading a sequential, persistent number: `[1]`, `[2]`, `[3]`, ... `[N]`.
* Embed an HTML anchor target on every heading in the inventory:
  ```html
  <li><a name="h1" id="h1"></a><b>[1]</b> <code>H1: Competitor Heading Text</code></li>
  ```

### Cross-Referencing Rule
* In **Section 2 (Granular Competitor Teardown)**, **Section 4 (Baseline Skeleton)**, and **Section 5 (Excluded Topics)**, reference the corresponding headings using clickable superscripts:
  ```html
  <h3>Question A: Scope of Work <sup><a href="#h2">[2]</a>, <a href="#h22">[22]</a></sup></h3>
  ```
* When uploaded to Google Docs via HTML, Google Drive automatically compiles these anchors into **native interactive jump links / bookmarks**. Clicking any superscript instantly navigates the user to that heading in Section 3.

---

## 6. Objective Baseline Article Skeleton Formulation

The baseline skeleton is derived **purely from the search intelligence teardown**. It represents the optimal content architecture required to rank and satisfy executive search intent.

### Structural Rules for the Skeleton
1. **Intent Satisfaction:** Must directly answer every high-value question discovered in the competitor teardown.
2. **Mapped Validation:** Every major section of the skeleton must include parenthetical or superscript citations linking back to the competitor headings that validate its necessity (e.g., `(Derived from Headings: [1], [4], [21], [34])`).
3. **Zero POV:** Do not inject subjective biases, proprietary slogans, or opinion hooks into the skeleton. The skeleton is a neutral, practitioner-grade operational outline.

---

## 7. Section 5: Inventory of Excluded Competitive Topics

Every competitor piece contains tangents, edge cases, or peripheral topics. To ensure total transparency, document what was *omitted* from the baseline skeleton so the author can make conscious editorial choices.

### Excluded Topic Documentation Schema
For each excluded topic, record:
1. **Topic Title & Source Headings:** Name of the topic and the indexed heading IDs where it appeared.
2. **Competitor Treatment:** Exactly how competitors framed or discussed the topic.
3. **Rationale for Exclusion:** Why it was left out of the baseline skeleton (e.g., too introductory, B2B resale focus, tangential venture financing, localized edge case).
4. **Author Review Point:** A direct, actionable decision prompt asking the author whether they wish to fold the topic into the piece during the editorial phase.

---

## 8. Report Template & Google Docs Native Publishing

Search intelligence reports are published directly to Google Docs using the Google Drive API PATCH method with `uploadType=media` and `Content-Type: text/html`. This compiles clean semantic HTML into native Google Docs headings (`HEADING_1` through `HEADING_4`), bordered tables, styled lists, and native internal bookmarks.

### Google Docs Drive API Publishing Script Pattern

```python
import json, urllib.request, urllib.parse

# 1. Refresh OAuth Token
TOKEN_FILE = "/Users/tylerkoshakow/Documents/antigravity/Screaming Frog Audit/google_workspace_mcp/token.json"
with open(TOKEN_FILE) as f:
    token_data = json.load(f)

payload = urllib.parse.urlencode({
    "client_id": token_data["client_id"],
    "client_secret": token_data["client_secret"],
    "refresh_token": token_data["refresh_token"],
    "grant_type": "refresh_token"
}).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=payload)
with urllib.request.urlopen(req) as resp:
    access_token = json.loads(resp.read().decode())["access_token"]

# 2. Compile Native HTML with Interactive Anchors
html_payload = """
<html>
<head>
<style>
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #202124; }
h1 { font-size: 20pt; color: #1a73e8; margin-top: 18pt; margin-bottom: 8pt; }
h2 { font-size: 15pt; color: #202124; margin-top: 16pt; margin-bottom: 6pt; border-bottom: 1px solid #dadce0; padding-bottom: 4px; }
h3 { font-size: 12pt; color: #1a73e8; margin-top: 14pt; margin-bottom: 4pt; }
h4 { font-size: 11pt; color: #202124; margin-top: 10pt; margin-bottom: 2pt; font-weight: bold; }
table { border-collapse: collapse; width: 100%; margin-top: 10pt; margin-bottom: 14pt; }
th { background-color: #f1f3f4; font-weight: bold; text-align: left; padding: 8pt; border: 1px solid #dadce0; }
td { padding: 8pt; border: 1px solid #dadce0; vertical-align: top; }
code { font-family: monospace; background-color: #f1f3f4; padding: 2px 4px; border-radius: 3px; font-size: 10pt; }
sup { font-size: 8.5pt; color: #1a73e8; font-weight: bold; }
.notice { background-color: #f8f9fa; border: 1px solid #dadce0; padding: 14pt; margin-bottom: 18pt; border-radius: 4px; }
.omitted-box { background-color: #f8f9fa; border: 1px solid #dadce0; padding: 10pt 12pt; margin: 8pt 0 12pt 0; }
</style>
</head>
<body>
<!-- Notice Box, Overview, Table, Teardown, Indexed Headings, Skeleton, Excluded Topics -->
</body>
</html>
"""

# 3. Patch Existing Document
doc_id = "<TARGET_GOOGLE_DOC_ID>"
req = urllib.request.Request(
    f"https://www.googleapis.com/upload/drive/v3/files/{doc_id}?uploadType=media",
    data=html_payload.encode("utf-8"),
    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "text/html"},
    method="PATCH"
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print("Google Doc successfully updated with native styling:", res.get("id"))
```

---

## 9. Standard Search Intelligence Document Structure

Every completed brief must follow this 5-part architecture:

1. **Header & SERP Landscape Overview:** Target keywords with search volumes and CPCs, SERP intent profile, and the Competitor Triad table (word counts, ranks, URL ETV, other ranked keywords, domain authority, organic traffic value).
2. **Granular Competitor Teardown (What Are They Actually Saying?):** Factual, unabstracted breakdown of core questions, exact dollar figures/salaries, rational buy criteria vs. honest disqualifiers, ramp timelines, offsite limitations, vetting tests, and 90-day verification frameworks (all linked to heading IDs via clickable superscripts).
3. **Exhaustive Heading Inventory (100% Tree):** Every heading across all three competitor pieces indexed sequentially (`[1]` to `[N]`) with persistent anchor IDs (`id="hN"`).
4. **Objective Baseline Article Skeleton:** A complete structural outline mapped to the search intelligence teardown, with clickable superscripts validating each section's inclusion.
5. **Topics Found in Competitive Content Not Included in Skeleton Outline:** Clear documentation of omitted topics, their source headings, treatment, exclusion rationale, and author review points.
