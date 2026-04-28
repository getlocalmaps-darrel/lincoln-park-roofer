# Lincoln Park Roofing — Master Operating Manual
**Last updated: 2026-04-28**

## 1. BUSINESS IDENTITY & NAP
- **Business Name:** Lincoln Park Roofing
- **Owner:** Scott
- **Phone:** (734) 224-5615
- **Address:** 2026 Thomas St, Lincoln Park, MI 48146
- **Domain:** https://www.lincolnparkroofing.com/ (ALWAYS use www)
- **Niche:** Roofing Contractor (Residential & Commercial)
- **Certification:** Owens Corning Preferred Contractor since 2011 — EXCLUSIVE, never mention GAF / IKO / Tamko / CertainTeed / Atlas / Malarkey / PABCO
- **Job Count:** 6,000+ roofs completed in 36 years (Michigan-licensed since 1996)
- **Rating:** 4.9/5 (33 verified reviews)
- **Brand Colors:** Primary #0056b3, Accent #fbbf24, Dark #0f172a
- **Fonts:** Oswald (headings), Open Sans (body)
- **Platform:** Static HTML + Tailwind CDN, deployed on Vercel via GitHub

## 2. COMPETITOR CONTEXT
- **Competitor:** Kincaide Construction (kincaideconstruction.com) — same owner, different marketer (Hibu, $1k/mo)
- **Darrel's domains:** roofingandsidingdetroit.com, brownstownroofing.com (owned by us, not redirected yet)
- **Competitive edge:** Our pages beat Kincaide on 15/20 on-page SEO elements. His advantage = entity authority (15yr BBB/Yelp) + 34 city pages vs our 37

## 3. CORE SERVICES (8 categories, 19 pages)

### Mega Menu Categories (h5 headings in nav + footer)
| Category | Pages |
|---|---|
| **Residential Roofing** | /roof-repair.html, /roof-replacement.html, /new-roof-construction.html, /residential-roof-repair.html |
| **Roof Replacement** | /roof-replacement.html, /asphalt-shingle-replacement.html, /storm-damage-roof-replacement.html, /roof-insurance-claim-lincoln-park-mi.html |
| **Roof Repair** | /roof-repair.html, /emergency-roof-repair.html, /storm-damage-repair.html |
| **Roof Rejuvenation** | /roof-rejuvenation.html |
| **Commercial Roofing** | /commercial-roofing.html, /commercial-roof-repair.html, /flat-roof-installation.html |
| **Siding & Trim** | /siding.html |
| **Gutters & Guards** | /gutters.html, /seamless-gutter-installation.html |
| **Insulation** | /attic-insulation.html, /blown-in-insulation.html |

### Additional
| Service | Page |
|---|---|
| Dumpster Rental | /dumpster-rental-lincoln-park.html |

### Navigation Structure (2026-04-01)
- Desktop: 4-column mega menu with h5 category headings + ARIA (`role="navigation"`, `aria-haspopup`, `role="menu"`, `role="group"`, `aria-labelledby`)
- Mobile: Accordion with `mobile-cat-label` spans for each category
- Areas: 4 geographic regions (Downriver, Western Wayne, Southern Wayne, Monroe & Nearby)
- Footer: 3-row layout — NAP+Quick Links+Map | Categorized services with h5 | Geographic city groups with h5
- **ALL 75 pages** (index + 37 city + 8 service-original + 11 service-new + 8 project + 10 policy/other) use identical nav/footer template
- Mobile menu JS: `"#mobile-menu a.mobile-link"` selector (NOT `.mobile-link` — buttons close menu otherwise)

## 4. CITY PAGES — Blueprint (FOLLOW FOR ALL NEW CITIES)

### Page Structure
```
1. Review Star Bar (4.9 rating · 33 reviews → /reviews.html)
2. Header with dropdown nav (Services + Areas We Serve + Reviews + Projects + Blog)
3. AI Search Magnet (hidden div)
4. Hero with slide-1.jpg background + H1 + CTA buttons
5. Content body (2-column: 8/4 grid, main + sidebar)
   - Intro paragraph with homepage backlink
   - H3 sections (6 total, geo-targeted)
   - Internal links to service pages (rotate anchors)
   - Comparison table (Replacement vs Rejuvenation)
   - Review quote with stars
6. FAQ section (8 FAQs, heavy city name repetition, FAQPage schema)
7. Service Areas section (all cities as clickable links)
8. Standardized footer (services, cities, NAP, map, policy links)
9. Mobile sticky bar (Call + Text)
```

### SEO Elements Per City Page
| Element | Rule |
|---|---|
| **Title** | `Roofer [City] MI \| (734) 224-5615 \| Lincoln Park Roofing` (under 60 chars) |
| **Meta desc** | Under 155 chars, include city 2x, CTA with phone |
| **H1** | `Roofer in [City], MI` (exact match, only 1 H1) |
| **H2s** | 5 total: intro, services, FAQs, service areas, process |
| **H3s** | 6 total: geo-targeted content headings |
| **H4s** | 3-4 under service sections (e.g., "Shingle Roof Repair in [City]") |
| **FAQs** | 8 questions, city name in EVERY question AND 2-4x in every answer |
| **City mentions** | Target 115-145 per page |
| **Schema** | LocalBusiness + FAQPage + Product + Service + BreadcrumbList |
| **Internal links** | All service pages + all city pages via nav + footer |
| **Images** | Hero (slide-1.jpg), logo, footer logo — all with keyword alts |
| **Canonical** | `https://www.lincolnparkroofing.com/[city]-roofer.html` (ALWAYS www) |

### Content Rules
- **Anti-AI voice:** No "seamlessly", "leverage", "elevate", "picture this", "at [Company] we"
- **Homepage backlink:** Every page must link "Lincoln Park Roofing" → `/` in body text
- **Anchor rotation:** Never use same anchor text for same destination across pages
- **Rule of Two:** Max 2 internal links per paragraph
- **Local landmarks:** Include real streets, parks, neighborhoods per city
- **Review quote:** Include 1 review excerpt with stars on each page
- **Contact form:** Include estimate request form (phone-only loses after-hours prospects)

### URL Pattern
- City pages: `/[city]-roofer.html` (e.g., `/taylor-roofer.html`)
- Exception: Lincoln Park uses `/roofer-lincoln-park-mi.html`

## 5. CURRENT CITY PAGES (37 total after expansion)

### Existing (16):
Lincoln Park, Allen Park, Taylor, Southgate, Wyandotte, Dearborn Heights, Riverview, Trenton, Melvindale, Ecorse, River Rouge, Wayne, Plymouth, Livonia, Grosse Ile, Ypsilanti

### New (21):
Belleville, Brownstown, Canton, Carleton, Flat Rock, Garden City, Gibraltar, Huron Township, Inkster, Newport, Northville, Northville Township, Plymouth Township, Redford, Rockwood, Romulus, South Rockwood, Sumpter Township, Van Buren, Westland, Woodhaven

## 5b. SERVICE × CITY COMBO MESH (2026-04-28 — Hardcore Epoxy blueprint port)

**Generator:** `generate_combo_pages.py` at the project root. Run any time the city or service list changes.

**Mesh size:** 7 services × 37 cities = **259 combo HTML pages + 259 ai.txt files**.

| Services (7) | Cities (37 — see CITIES dict in script) |
|---|---|
| roof-repair, roof-replacement, storm-damage-repair, emergency-roof-repair, gutters, siding, commercial-roofing | Detroit + 36 Downriver/Western/Southern Wayne + Monroe cities |

**File pattern:** `[service]-[city].html` and `[service]-[city]-ai.txt` (suffix style — NOT folder/index.html like Hardcore Epoxy's Astro setup).

**Each combo ai.txt contains:**
1. **City-specific hazard** — real streets, neighborhoods, housing era, climate signals (NEVER generic "Michigan winters")
2. **Core differentiator** for that service (in-house crews, same-day, Owens Corning, etc.)
3. **Proximity** — distance/minutes from 2026 Thomas St HQ
4. **Authority signals** — 6,000+ roofs, 36 years, Owens Corning Preferred, 4.9/5, A+ BBB
5. **Owner blockquote** — Scott quote per service tied to local conditions, ending with "Owens Corning Preferred Contractor since 2011 · (734) 224-5615"

**Root `ai.txt` index** — has all 259 combo URLs grouped by service under `### Service x City AI Files (Per-Combination)`. Re-generate the block via the same Python helper used 2026-04-28.

**Why this mesh exists:** Hardcore Epoxy reverse-engineering showed 357 service×city combo pages were the load-bearing pattern for AI Overview / ChatGPT citations. LPR was sitting at 28 (4 cities × 7 services) — the mesh was too thin for AI to cite. Bumping to 259 matches the proven pattern.

**Adding a new city later:** add the city dict entry to `CITIES` in `generate_combo_pages.py` (16 fields — copy an existing entry, swap city-specific data), re-run the script, regenerate the root ai.txt combo block, commit + push.

**Adding a new service later:** add to `SERVICES` dict in the script (with differentiator + price range + issues + owner_quote_ai_map entry), re-run.

**Owner quote rule:** new services must add a per-service Scott quote in `owner_quote_ai_map` inside `build_ai_txt`. Never fabricate customer reviews — use generic "Verified Lincoln Park Roofing customer · [City], MI" attribution if real per-city reviews aren't available (FTC 16 CFR Part 465 — $51,744 per fabricated review).

## 6. SITE-WIDE ELEMENTS (must appear on EVERY page)

### Review Star Bar
```html
<div id="review-bar" style="width:100%;background:#09090b;padding:6px 12px;...">
  ★★★★★ 4.9 rating · 33 homeowner reviews → /reviews.html
</div>
```

### Product Schema (separate from LocalBusiness)
Every page has Product schema with aggregateRating 4.9/33 for Google star snippets.

### Dropdown Navigation
- Home | Services (dropdown: 8 links) | Areas We Serve (dropdown: all cities) | Reviews | Projects | Blog | Phone + CTA

### Standardized Footer
- Services links (8) + Reviews + Blog + Projects
- All city links (4 columns)
- NAP (2026 Thomas St, Lincoln Park, MI 48146)
- Google Maps embed
- Policy links (Privacy, Terms, Accessibility)
- Get Local Maps credit

## 7. TECHNICAL RULES

### www Canonical (CRITICAL)
- ALL URLs use `https://www.lincolnparkroofing.com/`
- NEVER use non-www
- vercel.json has 301 redirect: non-www → www
- Sitemap, robots.txt, canonical tags, OG URLs, schema URLs — ALL www

### Git & Deploy
```bash
# Always selective staging — never git add -A
git add [specific files]
git commit -m "description"
git push origin main
vercel --prod --yes
```
- NEVER blindly `git add index.html` without diffing first
- Local Vercel deploys get overwritten by GitHub auto-deploy — git push is critical

### Image Rules
- Use plain `<img>` tags — NOT `<picture>` with webp sources (caused layout collapse)
- Hero image: `slide-1.jpg` (relative path from root)
- Logo: `lincoln park logo.png` (relative path)
- All images need keyword-rich alt text

## 8. REVIEWS
- **Reviews page:** /reviews.html — 33 reviews (30 five-star, 3 four-star = 4.9 avg)
- **Numbers must match everywhere:** Product schema ratingCount = review bar count = actual reviews on page
- **Target:** 4.8-4.9 average (not 5.0 — looks fake)

## 9. TRELLO WORK LOG (MANDATORY)
```powershell
& "D:\html websites\Agency_Master\_REPORT_FACTORY\post_trello.ps1" -ClientName "Lincoln Park" -Comment "[summary]"
```
Always include URLs if any were created. Never skip.

## 10. LINK BUILDING
- Link Builder state: `_MARKETING_FACTORY/Link_Builder/data/link_builder_state_Lincoln_Park_Roofing.json`
- Reddit autopilot: Michigan shared account (see memory)
- Citation Engine: Active
- IndexIgnite: Active

## 11. MARKETING CONFIG
- Location: `Agency_Master/Clients/Marketing/Lincoln_Park_Roofing/marketing_config.json`
- Blog Factory: HTML deploy type, VPS scheduled

## 12. AI VISIBILITY EXPERIMENTS — TIMESTAMPED LOG

### Methodology: Dark Query + ai.txt Optimization
We use `ai_search_checker.py` (OpenAI Responses API with web_search) to run 3 query styles per city:
1. Direct: "best roofer in [City] MI"
2. Near-me: geo-located "roofer near me"
3. Casual: "who's a good roofer in [City]?"

ChatGPT also returns **tips at the bottom of results** (e.g., "Downriver homes have ice dams, rotten decking, chimney flashing failures"). We feed those tips back into our ai.txt files and city page content.

---

### Experiment 1: Per-City ai.txt Deploy (2026-04-15)
- **What:** Generated 37 city-specific ai.txt files using GEO Module script
- **Deployed:** 3 cities to live subdirectories (ecorse, wyandotte, melvindale)
- **Result (2026-04-17):** Ecorse ranks for "roof repair ecorse" in ChatGPT. Wyandotte and Melvindale do NOT rank.
- **Analysis:** All 3 had identical template-swapped content. Ecorse wins likely due to low competition (~9k population), not ai.txt quality. The ai.txt content itself was generic.

### Experiment 2: Downriver-Specific ai.txt Rewrite (2026-04-17)
- **What:** Rewrote 7 city ai.txt files with REAL Downriver roofing content:
  - Ice dams, rotten decking under shingles, chimney flashing as #1 failure point
  - Detroit River humidity, industrial fallout from Rouge River corridor
  - Post-war ranch home vulnerabilities, low-slope eave ice dam patterns
  - Specific street names, neighborhoods, housing era details per city
- **Cities rewritten:** Ecorse, Wyandotte, Melvindale, River Rouge, Allen Park, Southgate, Taylor
- **Content source:** ChatGPT dark query tips + local knowledge
- **Deployed:** All 7 to live subdirectories at `/[city]-roofer/ai.txt`
- **Status:** Waiting for ChatGPT to re-crawl. Re-run dark queries in 1-2 weeks.

### Experiment 3: Taylor "Roofer" Keyword Stuffing Test (2026-04-17)
- **What:** Taylor's ai.txt intentionally stuffs the word "roofer" in every section header, service listing, business identity field, pricing table, and contact section. Much higher keyword density than the other 6 cities.
- **Hypothesis:** If Taylor starts ranking for "roofer Taylor MI" but the other cities don't move, keyword density in ai.txt matters. If Taylor doesn't rank either, it's not about density.
- **Control group:** The other 6 cities use natural language with moderate "roofer" usage.
- **Status:** Deployed 2026-04-17. Will re-run dark queries in 1-2 weeks.

### Dark Query Baseline Results (2026-04-17)
Lincoln Park Roofing was NOT recommended in ANY of these 5 cities:

| City | Top ChatGPT Picks | Key Signals They Have |
|---|---|---|
| **Melvindale** | Prime Home Remod (141 reviews), Home Genius (214 reviews), Sterling Construction | Angi profiles, high review counts |
| **River Rouge** | Best Choice Roofing, MacDermott (40yr), Pete's Roofing | Physical presence, longevity |
| **Allen Park** | AllPoint (648 reviews, GAF Master Elite), MCM Services (since 1981), Tittle Brothers | GAF certs, city-specific URLs, massive reviews |
| **Southgate** | Roofing RPGs (5,000 jobs), Ripcord, MCM, McGlinch (100yr) | BBB, lifetime warranties, job counts |
| **Taylor** | Advantage Roofing, Mr. Roof (60yr), Chuck's Roofing (52yr), Taylor Roof Pros | City-named businesses, GAF certs |

### Competitive Intelligence (from dark queries)
ChatGPT rewards these signals — we need to keep them in Lincoln Park content:
1. **Review volume** — competitors have 100-648 reviews (we have 33). Still a gap.
2. **Manufacturer certs** — we lead with Owens Corning Preferred Contractor since 2011 (NEVER GAF/IKO/etc.)
3. **Job counts** — 6,000+ completed jobs in 36 years (Michigan-licensed since 1996)
4. **City-specific URLs** — covered: 37 city pages + 259 service×city combo pages
5. **Directory profiles** — Angi, BBB profiles still heavily cited by ChatGPT (we have BBB A+, Angi pending)

### Experiment 4: Hardcore Epoxy Blueprint Port (2026-04-28)
- **What:** Bumped service×city combo pages from 28 (4 cities × 7) to **259 (37 × 7)**. Each combo ai.txt now has 4-bullet formula + Scott owner blockquote ending with "Owens Corning Preferred Contractor since 2011 · (734) 224-5615". Fixed IKO contradiction in commercial-roofing differentiator template.
- **Why:** Hardcore Epoxy ranks #1 in ChatGPT for `epoxy flooring [city]` across Wayne County using exactly this pattern (357 combo pages). LPR's 28 combos were too thin for AI mesh citation.
- **Deployed:** All 259 HTML + 259 ai.txt files live, sample verified: `roof-repair-taylor.html`, `roof-repair-taylor-ai.txt`, `siding-detroit.html` all return 200 from Vercel.
- **Re-test ChatGPT:** 2026-05-12 (14 days post-deploy per AI.txt Optimization Playbook). Compare against 2026-04-22 dark query baseline at `_MARKETING_FACTORY/ChatGPT_Checker/results/Lincoln_Park_Roofing/`.
- **Commit:** `4aabf86` on `main`.

### TODO: Remaining Content Work
- [x] Switch certification language to Owens Corning Preferred (was incorrectly listed as GAF)
- [x] Update job count to 6,000+ / 36 years across ai.txt
- [x] Build out service×city combo mesh (28 → 259 done 2026-04-28)
- [ ] Re-run dark query tracker on 2026-05-12 and compare
- [ ] Push for review volume — currently 33, competitors at 100-648
- [ ] Claim BBB profile + Angi profile (still heavily cited by ChatGPT)
- [ ] Optional: rewrite the 37 standalone city ai.txt files (`[city]-roofer-ai.txt`) to also have the Scott owner blockquote. Combo ai.txt files already have it; the per-city hub files do not.
