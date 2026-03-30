# Lincoln Park Roofing — Master Operating Manual
**Last updated: 2026-03-30**

## 1. BUSINESS IDENTITY & NAP
- **Business Name:** Lincoln Park Roofing
- **Owner:** Scott
- **Phone:** (734) 224-5615
- **Address:** 2026 Thomas St, Lincoln Park, MI 48146
- **Domain:** https://www.lincolnparkroofing.com/ (ALWAYS use www)
- **Niche:** Roofing Contractor (Residential)
- **Brand Colors:** Primary #0056b3, Accent #fbbf24, Dark #0f172a
- **Fonts:** Oswald (headings), Open Sans (body)
- **Platform:** Static HTML + Tailwind CDN, deployed on Vercel via GitHub

## 2. COMPETITOR CONTEXT
- **Competitor:** Kincaide Construction (kincaideconstruction.com) — same owner, different marketer (Hibu, $1k/mo)
- **Darrel's domains:** roofingandsidingdetroit.com, brownstownroofing.com (owned by us, not redirected yet)
- **Competitive edge:** Our pages beat Kincaide on 15/20 on-page SEO elements. His advantage = entity authority (15yr BBB/Yelp) + 34 city pages vs our 37

## 3. CORE SERVICES
| Service | Page |
|---|---|
| Roof Repair | /roof-repair.html |
| Roof Replacement | /roof-replacement.html |
| Roof Rejuvenation | /roof-rejuvenation.html |
| New Roof Construction | /new-roof-construction.html |
| Insurance Claims | /roof-insurance-claim-lincoln-park-mi.html |
| Siding | /siding.html |
| Gutters | /gutters.html |
| Dumpster Rental | /dumpster-rental-lincoln-park.html |

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
