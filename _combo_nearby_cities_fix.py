"""
Convert combo-page bottom grid (between STAGE5-COMBO-LINKS markers) from the
wrong-city "all services in Grosse Ile" copy-paste to the proven Hardcore Epoxy
cross-city interlinking pattern: "[Service] across Southeast Michigan" with
cards linking to the SAME service in nearby Downriver / Wayne County cities.

Why:
  - City hubs already show "All [City] Roofing Services" (correct, untouched).
  - Combo pages already have a sidebar listing other services in the same city.
  - The bottom grid was duplicating the sidebar (when working) AND was hardcoded
    to Grosse Ile (when broken). Cross-city interlinking is the right job for
    that surface — distributes link equity across all Downriver cities and
    matches the Hardcore winner pattern.

Scope: combo pages only ([service]-[city].html). City hubs are NOT touched.

Run:
  python _combo_nearby_cities_fix.py --dry-run
  python _combo_nearby_cities_fix.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Order matters: longer prefixes MUST come before shorter ones that share a
# common stem (none collide today, but defensive).
SERVICE_PREFIXES = (
    "emergency-roof-repair",
    "storm-damage-repair",
    "commercial-roofing",
    "roof-replacement",
    "roof-repair",
    "gutters",
    "siding",
)

SERVICE_NAMES = {
    "roof-repair": "Roof Repair",
    "roof-replacement": "Roof Replacement",
    "storm-damage-repair": "Storm Damage Repair",
    "emergency-roof-repair": "Emergency Roof Repair",
    "commercial-roofing": "Commercial Roofing",
    "gutters": "Gutter Installation",
    "siding": "Siding Installation",
}

# Strategic Downriver / Wayne County cities for the cross-city interlinking
# grid. All ten have full combo pages for every service. Lincoln Park is
# excluded because no combo pages exist for it (Lincoln Park's hub serves all
# services). Order = visual order in grid.
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

MARKER_START = "<!-- STAGE5-COMBO-LINKS-START -->"
MARKER_END = "<!-- STAGE5-COMBO-LINKS-END -->"

SECTION_RE = re.compile(
    re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
    re.DOTALL,
)


def kebab_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def parse_combo(filename: str):
    """Return (service_slug, city_slug, city_name) for combo pages, else None."""
    if not filename.endswith(".html"):
        return None
    base = filename[: -len(".html")]
    for svc in SERVICE_PREFIXES:
        prefix = svc + "-"
        if base.startswith(prefix):
            city_slug = base[len(prefix):]
            if city_slug:
                return (svc, city_slug, kebab_to_title(city_slug))
    return None


def build_section(service_slug: str, page_city_slug: str, page_city_name: str) -> str:
    service_name = SERVICE_NAMES[service_slug]
    cards = []
    for slug, name in NEARBY_CITIES:
        if slug == page_city_slug:
            continue
        url = f"/{service_slug}-{slug}.html"
        cards.append(
            f"""
      <a href="{url}" class="block bg-white border border-gray-200 rounded-lg p-6 hover:border-red-600 hover:shadow-lg transition">
        <h3 class="text-lg font-bold text-gray-900 mb-2">{service_name} in {name}</h3>
        <p class="text-sm text-gray-600 mb-3">Owens Corning Preferred {service_name.lower()} for {name} homeowners — same crew, same workmanship warranty.</p>
        <span class="text-red-600 font-semibold text-sm">View {service_name} in {name} &rarr;</span>
      </a>"""
        )
    cards_html = "".join(cards)
    return f"""{MARKER_START}
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
{MARKER_END}"""


def patch_file(path: Path, dry_run: bool) -> tuple[bool, str]:
    parsed = parse_combo(path.name)
    if not parsed:
        return False, "not-combo"
    text = path.read_text(encoding="utf-8")
    if MARKER_START not in text or MARKER_END not in text:
        return False, "no-markers"
    service_slug, city_slug, city_name = parsed
    new_section = build_section(service_slug, city_slug, city_name)
    new_text = SECTION_RE.sub(new_section, text, count=1)
    if new_text == text:
        return False, "no-change"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True, "ok"


def main():
    dry_run = "--dry-run" in sys.argv
    files = sorted(ROOT.glob("*.html"))
    changed = 0
    skipped_non_combo = 0
    skipped_no_markers = 0
    skipped_no_change = 0

    for f in files:
        ok, status = patch_file(f, dry_run)
        if ok:
            changed += 1
            if dry_run:
                parsed = parse_combo(f.name)
                if parsed:
                    svc, _, cn = parsed
                    print(f"[DRY] {f.name}  ({svc} -> {cn})")
        elif status == "not-combo":
            skipped_non_combo += 1
        elif status == "no-markers":
            skipped_no_markers += 1
        elif status == "no-change":
            skipped_no_change += 1

    mode = "DRY-RUN" if dry_run else "APPLIED"
    print(f"\n{mode}: {changed} combo pages updated")
    print(f"  Skipped non-combo files (hubs, static): {skipped_non_combo}")
    print(f"  Skipped combo pages w/o markers:        {skipped_no_markers}")
    print(f"  Skipped combo pages already-correct:    {skipped_no_change}")


if __name__ == "__main__":
    main()
