# Inject Stage 5 interlinking grids into existing city + base service pages.
# Idempotent: detects marker comment and skips already-injected pages.

import re
from pathlib import Path

BASE = Path(__file__).parent
MARKER_START = "<!-- STAGE5-COMBO-LINKS-START -->"
MARKER_END = "<!-- STAGE5-COMBO-LINKS-END -->"

CITIES = {
    "grosse-ile": "Grosse Ile",
    "allen-park": "Allen Park",
    "wyandotte": "Wyandotte",
    "livonia": "Livonia",
}

# Each service: (slug, display, blurb)
SERVICES = [
    ("roof-repair", "Roof Repair", "Leak repair, flashing replacement, and shingle fixes by Owens Corning Preferred contractors."),
    ("roof-replacement", "Roof Replacement", "Full tear-off and replacement with TotalProtection warranty covering materials AND labor."),
    ("storm-damage-repair", "Storm Damage Repair", "Wind, hail, and tree-strike damage repaired fast. Insurance-claim friendly."),
    ("emergency-roof-repair", "Emergency Roof Repair", "Same-day tarping and emergency leak patching — 24/7 storm response."),
    ("gutters", "Gutter Installation", "Seamless aluminum gutters, guards, and downspouts sized for Downriver rainfall."),
    ("siding", "Siding Installation", "Vinyl, fiber cement, and insulated siding by a fully licensed Michigan contractor."),
    ("commercial-roofing", "Commercial Roofing", "Flat roof systems, TPO, EPDM, and metal roofing for commercial properties."),
]

# City page filename map (existing city landing pages)
CITY_PAGE_FILES = {
    "grosse-ile": "grosse-ile-roofer.html",
    "allen-park": "allen-park-roofer.html",
    "wyandotte": "wyandotte-roofer.html",
    "livonia": "livonia-roofer.html",
}

# Strategic Downriver / Wayne County cities for combo-page cross-city grids.
# All ten have full combo pages for every service. Lincoln Park excluded —
# no combos exist for it (Lincoln Park's hub serves all services).
NEARBY_CITIES = [
    ("allen-park", "Allen Park"),
    ("wyandotte", "Wyandotte"),
    ("taylor", "Taylor"),
    ("southgate", "Southgate"),
    ("trenton", "Trenton"),
    ("riverview", "Riverview"),
    ("brownstown", "Brownstown"),
    ("woodhaven", "Woodhaven"),
    ("grosse-ile", "Grosse Ile"),
    ("canton", "Canton"),
]

# Combo page filename detection — order matters (longer prefixes first).
SERVICE_PREFIXES = (
    "emergency-roof-repair",
    "storm-damage-repair",
    "commercial-roofing",
    "roof-replacement",
    "roof-repair",
    "gutters",
    "siding",
)

SERVICE_DISPLAY = {
    "roof-repair": "Roof Repair",
    "roof-replacement": "Roof Replacement",
    "storm-damage-repair": "Storm Damage Repair",
    "emergency-roof-repair": "Emergency Roof Repair",
    "commercial-roofing": "Commercial Roofing",
    "gutters": "Gutter Installation",
    "siding": "Siding Installation",
}


def build_city_grid(city_slug: str, city_name: str) -> str:
    """Grid injected into a city page — one card per service, each linking to the service×city combo."""
    cards = []
    for slug, name, blurb in SERVICES:
        url = f"/{slug}-{city_slug}.html"
        cards.append(f"""
      <a href="{url}" class="block bg-white border border-gray-200 rounded-lg p-6 hover:border-red-600 hover:shadow-lg transition">
        <h3 class="text-lg font-bold text-gray-900 mb-2">{name} in {city_name}</h3>
        <p class="text-sm text-gray-600 mb-3">{blurb}</p>
        <span class="text-red-600 font-semibold text-sm">View {name} in {city_name} &rarr;</span>
      </a>""")
    cards_html = "".join(cards)
    return f"""
{MARKER_START}
<section class="py-16 bg-gray-50">
  <div class="max-w-6xl mx-auto px-4">
    <div class="text-center mb-10">
      <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">All {city_name} Roofing Services — Owens Corning Preferred Since 2011</h2>
      <p class="text-gray-600 max-w-2xl mx-auto">Every {city_name} roofing service we offer — from emergency leak repair to full replacement — is handled by the same Owens Corning Preferred crew that has completed 6,000+ roofs across Downriver Michigan.</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">{cards_html}
    </div>
  </div>
</section>
{MARKER_END}
"""


def build_service_grid(service_slug: str, service_name: str) -> str:
    """Grid injected into a base service page — one card per city, each linking to the service×city combo."""
    cards = []
    for city_slug, city_name in CITIES.items():
        url = f"/{service_slug}-{city_slug}.html"
        cards.append(f"""
      <a href="{url}" class="block bg-white border border-gray-200 rounded-lg p-6 hover:border-red-600 hover:shadow-lg transition">
        <h3 class="text-lg font-bold text-gray-900 mb-2">{service_name} in {city_name}</h3>
        <p class="text-sm text-gray-600 mb-3">Local {service_name.lower()} specialists serving {city_name} homeowners with Owens Corning certified installation and workmanship warranty.</p>
        <span class="text-red-600 font-semibold text-sm">Learn More &rarr;</span>
      </a>""")
    cards_html = "".join(cards)
    return f"""
{MARKER_START}
<section class="py-16 bg-gray-50">
  <div class="max-w-6xl mx-auto px-4">
    <div class="text-center mb-10">
      <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">{service_name} in Nearby Cities</h2>
      <p class="text-gray-600 max-w-2xl mx-auto">See city-specific pages with local pricing, common {service_name.lower()} issues unique to each area, and neighborhood-level service details.</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-5">{cards_html}
    </div>
  </div>
</section>
{MARKER_END}
"""


def kebab_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def parse_combo(filename: str):
    """Return (service_slug, city_slug, city_name) for combo pages, else None."""
    if not filename.endswith(".html"):
        return None
    base = filename[:-len(".html")]
    for svc in SERVICE_PREFIXES:
        prefix = svc + "-"
        if base.startswith(prefix):
            city_slug = base[len(prefix):]
            if city_slug:
                return (svc, city_slug, kebab_to_title(city_slug))
    return None


def build_combo_grid(service_slug: str, page_city_slug: str, page_city_name: str) -> str:
    """Grid for combo pages — same service, nearby cities (cross-city interlinking).
    Distributes link equity across all 10 strategic cities and matches the Hardcore
    Epoxy winner pattern (2026-04-29 audit)."""
    service_name = SERVICE_DISPLAY[service_slug]
    cards = []
    for slug, name in NEARBY_CITIES:
        if slug == page_city_slug:
            continue
        url = f"/{service_slug}-{slug}.html"
        cards.append(f"""
      <a href="{url}" class="block bg-white border border-gray-200 rounded-lg p-6 hover:border-red-600 hover:shadow-lg transition">
        <h3 class="text-lg font-bold text-gray-900 mb-2">{service_name} in {name}</h3>
        <p class="text-sm text-gray-600 mb-3">Owens Corning Preferred {service_name.lower()} for {name} homeowners — same crew, same workmanship warranty.</p>
        <span class="text-red-600 font-semibold text-sm">View {service_name} in {name} &rarr;</span>
      </a>""")
    cards_html = "".join(cards)
    return f"""
{MARKER_START}
<section class="py-16 bg-gray-50">
  <div class="max-w-6xl mx-auto px-4">
    <div class="text-center mb-10">
      <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">{service_name} Across Downriver Michigan — Owens Corning Preferred Since 2011</h2>
      <p class="text-gray-600 max-w-2xl mx-auto">Need {service_name.lower()} outside {page_city_name}? Lincoln Park Roofing serves Downriver, Wayne County, and Monroe County — every job handled by the same Owens Corning Preferred crew that has completed 6,000+ roofs in 36 years.</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">{cards_html}
    </div>
  </div>
</section>
{MARKER_END}
"""


def inject(file_path: Path, grid_html: str) -> str:
    html = file_path.read_text(encoding="utf-8")
    # idempotent: if marker already present, replace the existing block
    if MARKER_START in html and MARKER_END in html:
        pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)
        new_html = pattern.sub(grid_html.strip(), html)
        file_path.write_text(new_html, encoding="utf-8")
        return "REPLACED"
    # insert immediately before <footer>
    m = re.search(r"<footer\b", html)
    if not m:
        return "NO FOOTER"
    new_html = html[:m.start()] + grid_html + "\n" + html[m.start():]
    file_path.write_text(new_html, encoding="utf-8")
    return "INJECTED"


def main():
    # city pages
    for city_slug, city_name in CITIES.items():
        fp = BASE / CITY_PAGE_FILES[city_slug]
        if not fp.exists():
            print(f"  [SKIP] missing: {fp.name}")
            continue
        grid = build_city_grid(city_slug, city_name)
        status = inject(fp, grid)
        print(f"  [{status}] {fp.name}")

    # base service pages
    for slug, name, _ in SERVICES:
        fp = BASE / f"{slug}.html"
        if not fp.exists():
            print(f"  [SKIP] missing: {fp.name}")
            continue
        grid = build_service_grid(slug, name)
        status = inject(fp, grid)
        print(f"  [{status}] {fp.name}")

    # combo pages — cross-city interlinking grid (Hardcore winner pattern)
    combo_count = 0
    for fp in sorted(BASE.glob("*.html")):
        parsed = parse_combo(fp.name)
        if not parsed:
            continue
        svc_slug, city_slug, city_name = parsed
        grid = build_combo_grid(svc_slug, city_slug, city_name)
        status = inject(fp, grid)
        combo_count += 1
        print(f"  [{status}] {fp.name}")
    print(f"  ({combo_count} combo pages processed)")

    print("\nDone.")


if __name__ == "__main__":
    main()
