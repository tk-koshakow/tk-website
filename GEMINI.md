# TK Website - Project Guidelines & Rules

## 1. Editorial Workflow & Google Docs Collaboration (Mandatory)

For all new articles, signals, prompt intelligence briefings, and pitches created for TK Website:

1. **Publish Drafts to Google Docs First:**
   * Do not immediately push draft content or raw HTML to production files.
   * Call `google_docs_create` using the **TK Website / Drafts** folder ID: `1OXScFvvjdkR_V4TxqKcouGTA-Ojhm2iR`.
   * Title convention: `[Draft] <Article Title> - <YYYY-MM-DD>`.
   * Place the standard **Editorial Feedback & Notes** section at the top of the document for Tyler to review on mobile or desktop:
     ```markdown
     ================================================================================
     EDITORIAL FEEDBACK & NOTES (FOR TYLER)
     Instructions: Add your review comments, punch-up notes, or direction changes below.
     When ready, reply in chat: "Reviewed doc [Title] - proceed with edits."
     --------------------------------------------------------------------------------
     Status: Pending Tyler's Review
     Target Audience: [Audience]
     Primary Angle: [Thesis / Angle]
     Notes for Tyler: [Brief rationale of structure and tone]
     ================================================================================
     ```
2. **Present Link to Tyler:**
   * Provide the direct Google Docs edit URL to Tyler in chat.
3. **Ingest Editorial Notes & Iterate:**
   * When Tyler indicates review is ready, call `google_docs_read` with the `document_id`.
   * **Inspect `result.comments` first**: This captures Tyler's Google Drive comment bubbles, author, text, and quoted phrases.
   * **In-Place Revision Only**: Call `google_docs_replace_content` to rewrite the draft in place. **NEVER append "Revision v2" blocks to the bottom.**
   * **Zero Tangents**: Only make the explicit changes requested by Tyler. Do not invent unrequested sections or insert artificial meta-headings.
   * Update the revision status block at the top to `Status: Revision v2 Applied (In-Place)`.
4. **Final Production Build:**
   * Only once approved by Tyler, transform the finalized copy into semantic HTML5, SVG diagrams, and JSON-LD schema adhering to `skills/blog-posts/SKILL.md`.

---

## 2. Editorial Voice & Style

* **Core Philosophy:** *"Good marketing distributes proof, good product creates it."*
* **Tone:** Practitioner-first, authoritative, concise, contrarian enterprise AI/SEO strategist.
* **No synthetic placeholders:** Never create dummy logs, mock data, or fake quotes.
* **Typographic Standards:** Uniform body font sizes (`var(--text-base)`), no `.lead` enlargement, graphical pull quotes breaking at the comma with `<br>`.
* **Theme Reactivity:** All diagrams and layouts must seamlessly support Light, Dark, and Goblin modes.

---

## 3. Professional Identity & Background

* **Tyler's In-House Role:** Tyler works in-house at **Octave**, leading enterprise AEO, SEO, and AI search intelligence initiatives. He previously worked agency-side for years before transitioning in-house, giving him authentic practitioner perspective from both sides of the industry.

---

## 4. Automation & Scheduled Tasks Architecture (Mandatory)

* **Never Use Internal Conversational `schedule` for Standing Recurring Jobs:**
  The agent tool `schedule` creates an in-memory timer inside the active `language_server` process bound strictly to the current conversation. When Antigravity closes, reloads, or updates, these in-session timers are permanently destroyed and never resurrected.
* **Use First-Class Antigravity Scheduled Tasks or System Daemons:**
  All recurring automations must be registered in the **Scheduled Tasks** UI panel in Antigravity's left sidebar (or via the user-facing `/schedule` slash command), or installed as persistent macOS `launchd` services.
* **Active Standing Antigravity Scheduled Tasks:**
  1. **AEO/GEO Content Intelligence Briefing:**
     * **Schedule:** `0 9 * * 2,5` (Every Tuesday & Friday at 9:00 AM)
     * **Action:** Scrapes latest 72h industry posts, drafts pitches in Tyler's practitioner voice, writes to `pitches/YYYY-MM-DD-pitch-briefing.md`, and runs `python3 send_briefing.py <path>`.
  2. **AI Prompt & Citation Tracker:**
     * **Schedule:** `0 9 * * 1,3,5` (Every Monday, Wednesday & Friday at 9:00 AM)
     * **Action:** Runs `python3 scripts/prompt_tracker.py --mode live`, reviews deltas, calculates rolling stability % across recent runs, syncs updated visibility and citations to Google Sheet (`1Py3PUuK2mvDKNXthakY8rLHDOEaqLPNvBRG3lwRuqiQ`), and presents a summary.

