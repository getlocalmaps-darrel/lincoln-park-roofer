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
      <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">Roofing Services in {city_name}</h2>
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

    print("\nDone.")


if __name__ == "__main__":
    main()
