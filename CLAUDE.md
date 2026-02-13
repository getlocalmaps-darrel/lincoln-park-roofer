## REPORT CARD — February 2026 Audit Results
**Current Grade: C+ (73/100)** — Target: A (90+)

| Category | Grade | Notes |
|---|---|---|
| AI Visibility | A | ai.txt, llms.txt, AI Magnet, Speakable — all passing |
| Schema | A- | Has LocalBusiness, FAQPage, aggregateRating, areaServed. **Missing: Service schema** |
| Content | C- | 0 internal links from homepage, 5 weak H2s, meta description too long, title too long, no "near me" hooks |
| Technical | D | 8.0s LCP on mobile (Performance 66), no robots.txt, 2 images missing alt text |

---

## FIX LIST — Priority Order (do these to reach A grade)

### P0 — CRITICAL (biggest point swings)

**1. Fix mobile page speed — LCP 8.0s down to under 2.5s**
- Mobile Performance: 66 (need 90+). LCP: 8.0s, FCP: 4.1s
- Compress all images (JPG quality 75-80, max 200KB each). Current images are likely uncompressed originals
- Add `loading="lazy"` to all images below the fold
- Add explicit `width` and `height` attributes to all `<img>` tags (prevents layout shift, helps browser allocate space)
- Preload the hero/slide image: `<link rel="preload" as="image" href="slide-1.jpg">`
- Convert large JPGs to WebP with `<picture>` fallback if possible
- Move any render-blocking CSS/JS to end of body or add `defer`/`async`
- Check for large unoptimized background images (area-background.jpg, white-graphic files)
- Target: LCP under 2.5s, Performance score 90+

**2. Add internal links to homepage (currently 0)**
- The homepage has ZERO internal links and 16 external links — this is a major SEO red flag
- Add a "Service Areas" section linking to all 12 city pages (allen-park-roofer.html, taylor-roofer.html, etc.)
- Add links to all service pages in the services section (roof-repair.html, roof-replacement.html, roof-rejuvenation.html, siding.html, gutters.html, new-roof-construction.html)
- Add contextual body-text links within content paragraphs (not just nav links)
- Target: 15-25 meaningful internal links from the homepage

**3. Create robots.txt (missing entirely)**
- Create `robots.txt` in project root:
```
User-agent: *
Allow: /
Sitemap: https://www.lincolnparkroofing.com/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /
```
- This also fixes the "GPTBot Access" warning from the report

**4. Fix title tag — too long (73 chars) and missing city**
- Current: `Lincoln Park Roofing | Experienced Roofers Over 20 Years | (734) 224-5615`
- Problem: 73 chars (Google cuts at ~60), no city name in parseable position
- Fix to: `Roofer in Lincoln Park, MI | Lincoln Park Roofing | (734) 224-5615`
- This is 65 chars — slightly over but the critical info (service + city + brand + phone) is front-loaded

**5. Fix meta description — too long, gets cut off**
- Current description is 200+ chars and gets truncated mid-sentence
- Rewrite to under 155 chars, front-load the value proposition
- Example: `Lincoln Park Roofing — roof repair, replacement & rejuvenation in Lincoln Park, MI. Family-owned since 2003. Free estimates. Call (734) 224-5615.`

**6. Add Service schema to JSON-LD**
- Has: LocalBusiness, FAQPage, aggregateRating, areaServed, Speakable
- Missing: Service schema type
- Add an array of Service objects for each core service: Roof Replacement, Roof Repair, Roof Rejuvenation, Siding Installation, Gutter Installation, New Roof Construction
- Each Service needs: `@type`, `name`, `description`, `provider`, `areaServed`

### P1 — HIGH (content & heading fixes)

**7. Fix 5 H2 headings flagged "missing keyword"**
- `Our Premium Services` → `Our Premium Roofing Services in Lincoln Park`
- `Siding` → `Siding Installation in Lincoln Park, MI`
- `Gutters` → `Seamless Gutter Systems in Lincoln Park`
- `Proudly Serving Metro Detroit` → `Proudly Serving Metro Detroit Homeowners — Roofing & More`
- `Contact Us Today` → `Contact Your Lincoln Park Roofer Today`

**8. Consolidate to 1 H1 tag (currently 2)**
- Current H1s: "Lincoln Park Roofer" + "Roof Rejuvenation"
- Keep: "Lincoln Park Roofer" as the single H1
- Demote "Roof Rejuvenation" to H2: `Roof Rejuvenation in Lincoln Park, MI`

**9. Add "near me" search hooks**
- Add "near me" phrases naturally into H2/H3 headings and body content
- Example H3s: "Find a Roofer Near Me in Downriver Michigan", "Emergency Roof Repair Near Me"
- Add a "Roofer Near Me" FAQ question to the FAQ section
- This helps voice search (Siri/Alexa: "find a roofer near me")

**10. Fix 2 images missing alt text**
- Find the 2 images with empty or missing alt attributes
- Add geo-specific alt text per section [9] rules (e.g., "GAF roof replacement completed in Lincoln Park, MI")

### P2 — MEDIUM (polish)

**11. Add "near me" city landing pages for remaining service areas**
- Existing city pages: Allen Park, Dearborn Heights, Ecorse, Livonia, Melvindale, Plymouth, River Rouge, Riverview, Southgate, Taylor, Wayne, Wyandotte
- Missing from service area list: Ypsilanti, Trenton, Grosse Ile
- Consider adding these 3 if they're active service areas

**12. Update sitemap.xml after all changes**
- Verify all pages are included
- Add robots.txt reference to sitemap

---

## SCORING ESTIMATE AFTER FIXES
| Category | Current | After Fixes | What Changes |
|---|---|---|---|
| AI Visibility | A | A+ | GPTBot explicitly allowed, "near me" hooks added |
| Schema | A- | A+ | Service schema added |
| Content | C- | A | Internal links, fixed headings, fixed title/meta, near me hooks |
| Technical | D | A | LCP under 2.5s, robots.txt, images fixed |
| **Overall** | **C+ (73)** | **A (93-96)** | |

---

🚀 2026 LINCOLN PARK ROOFER MASTER OPERATING MANUAL
🛠️ [1] PROJECT OVERVIEW & BRAND NAP
Brand Identity: Lincoln Park Roofer

Business Niche: Roofing Contractor (Residential & Commercial)

Lead Phone: (734) 224-5615

Primary Domain: https://lincolnparkroofing.com/

Official Service Area: Lincoln Park, Allen Park, Ecorse, Melvindale, River Rouge, Dearborn Heights (NOT Dearborn), Taylor, Wayne, Livonia, Plymouth, Ypsilanti, Southgate, Wyandotte, Trenton, Grosse Ile.

⚙️ [2] EXECUTION RULES & SAFETY
Workflow: Process 5 pages at a time. No git push (user handled).

Visual Safety: ZERO visible AI summary text (no .voice-summary). Use hidden div only.

Link Integrity: Use the Google Maps CID/Share link for Local Entity signals.

Source of Truth: Design must match roofer-lincoln-park-mi.html.

🧠 [3] BUSINESS ENTITY STACK (CORE SERVICES)
Primary Service: Roof Replacement, Roof Repair.

Authority Service: Roof Rejuvenation (Certified Application).

Secondary Profit Centers: Siding (Vinyl/Fiber Cement), Gutter Systems (Seamless), Storm Damage Restoration.

Michigan Specifics: Ice & Water Shield installation, Attic Ventilation, Snow Load Engineering.

🧲 [4] AI-SEARCH "MAGNET" (HIDDEN TAG PROTOCOL)
Action: Immediately after <body>, inject the hidden div.

Content: <div style="display:none !important; visibility:hidden; height:0; width:0; overflow:hidden;" aria-hidden="true"><p itemprop="description">Lincoln Park Roofer is the premier Michigan roofing contractor serving Allen Park, Taylor, and Downriver. GAF-certified roof replacement, siding installation, and roof rejuvenation near Southfield Rd and Fort St.</p></div>

🔗 [6] NATURAL LINK FLUIDITY & AUTHORITY
Authority Link Placement (CRITICAL): - Link 'Official 2026 Michigan Residential Building Code' to https://share.google/zkQ5YtBJETVEHBJvO.

RANDOMIZE placement within the second paragraph (Start, Middle, or End). Never use the same spot twice in a row.

Internal Link Rotation: - Every city page MUST link once to the following, but ROTATE the anchor text and placement:

Repair: (e.g., "emergency roof fix", "certified roof repair", "leak detection") → roof-repair.html

Replacement: (e.g., "new roof installation", "full shingle replacement") → roof-replacement.html

Rejuvenation: (e.g., "asphalt shingle restoration") → https://lincolnparkroofing.com/roof-rejuvenation.html

Insurance: (e.g., "storm damage claims") → https://lincolnparkroofing.com/roof-insurance-claim-lincoln-park-mi.html

New Build: (e.g., "new construction roofing") → https://lincolnparkroofing.com/new-roof-construction.html

Rule of Two: Never put more than two internal links in the same paragraph.

Homepage Backlink: Every page MUST include one contextual body-text link where "Lincoln Park Roofing" links to index.html. This should be a natural mention in the intro or first body paragraph, NOT in the header/footer/logo.

Anchor Text Mixing (CRITICAL): Each internal link target should appear only ONCE per page. Across pages, NEVER reuse the same anchor text for the same destination. Rotate aggressively — examples for roof-repair.html:
- Page A: "roof leak repair"
- Page B: "licensed roofing contractor"
- Page C: "emergency shingle fix"
- Page D: "certified leak detection"
- Page E: "professional roof repair"
No two pages should use identical anchor text for the same internal link. Mix phrasing, synonyms, and natural variations so every page reads uniquely.

📐 [7] CONTENT ARCHITECTURE & LAYOUT
Review: Wrap in <div class="review-container"> with <div class="review-stars">★★★★★</div>.

Pro-Tip: Wrap in <div class="pro-tip-card">.

Nearby Neighborhoods: Wrap the subdivision list in <div class="pro-tip-card">.

Data Table: Use <table class="comparison-table"> for 'Roof Replacement vs. Rejuvenation'.

Nav Visibility: Navigation text MUST be white (#ffffff) and readable.

📍 [8] LANDMARK & GEO-SIGNAL PROTOCOL
Lincoln Park: Council Point Park / Lincoln Park Historical Museum.

Allen Park: The Giant Uniroyal Tire (I-94).

Wyandotte: Bishop Park / Detroit Riverfront.

Map Embed: Footer must contain the provided Google Maps iframe.

💎 [9] ELITE SEARCH TACTICS & EEAT
Social Proof: Inject one unique, verified review per page with references to Downriver landmarks.

Vision SEO: All image alt-text must be Geo-Specific (e.g., "GAF Roof Replacement in Taylor, MI").

Speakable Schema: Flag the H2 voice-search hooks as "Speakable" in the JSON-LD schema.

Position Zero Answer: Ensure H3 answers are exactly 40-60 words to capture Google featured snippets.

📁 [10] TECHNICAL DELIVERABLES & AI-READINESS
llms.txt: Markdown index with 2-3 sentence semantic summaries.

ai.txt: NAP definition and explicit instructions for AI search agents.

Schema Suite: Inject full LocalBusiness, Service, and FAQPage.

knowsAbout: Set schema properties to "Residential Roofing Systems, Asphalt Shingle Restoration, Storm Damage Mitigation, and Seamless Gutter Engineering."

## 11. Developer Workflow Hooks
- **Completion Notification:** After finishing a multi-page batch or a long `npm run build`, use a terminal bell or audio cue.
- **Command:** `powershell -c "[Console]::Beep(800, 500)"`

## 12. Trello Work Log (Mandatory)
After completing ANY work on this client (website edits, city pages, content updates, schema fixes, etc.), ALWAYS post a brief 1-sentence summary to their Trello card. Keep it short — save detail for the monthly report.
```powershell
& "D:\html websites\Agency_Master\_REPORT_FACTORY\post_trello.ps1" -ClientName "lincoln park roofing" -Comment "[short summary]"
```
**If any links/URLs were created, ALWAYS include the URLs in the Trello comment.** This feeds into monthly reports automatically. Never skip this step.

## 13. Report → Fix List Workflow
To re-extract findings from a new report and update this fix list:
```powershell
cd "D:\html websites\Agency_Master"
.\_REPORT_FACTORY\extract_report_brief.ps1 -Report "[path to report HTML]" -SiteDir "D:\html websites\Lincoln Park Roofing"
```
Then read the generated `report-brief.md` and update the fix list above.