"""
AIO winner pattern fix — apply Hardcore Epoxy citation-winning H2 patterns
to all existing LPR city hub + service x city combo pages.

Source of truth: Hardcore audit at
  Clients/Web_Design/hardcore-epoxy/audit/aio_winner_pattern_2026-04-29.md

Fixes (in priority order, by AIO citation rate observed on Hardcore):
  1. FAQ H2 (cited 4/5):  "[Service] FAQs for [City] Homeowners" -> "[Service] FAQ — [City]"
                          "[City] Roofing FAQs"                  -> "Roofing FAQ — [City]"
  2. Hero H2 (cited 3/5): "[Service] Contractor Serving [City]"  -> "[Service] Experts Serving [City]"
                          "Local Roofing Company Serving [City]" -> "Roofing Experts Serving [City]"
  3. Stage5 H2 (cited 0/5 + Grosse Ile copy-paste bug):
       "Roofing Services in [WrongCity]" ->
       "All [PageCity] Roofing Services — Owens Corning Preferred Since 2011"
       (PageCity derived from filename so the bug self-corrects per page)

Generator sources have already been patched in this same commit:
  inject_stage5_links.py  line 55  (stage5 H2)
  generate_combo_pages.py line 1600 (hero H2)
  generate_combo_pages.py line 1807 (faq H2)

Run:
  python _aio_winner_pattern_fix.py --dry-run    # preview
  python _aio_winner_pattern_fix.py              # apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SERVICE_PREFIXES = (
    "roof-replacement",
    "roof-repair",
    "storm-damage-repair",
    "emergency-roof-repair",
    "commercial-roofing",
    "gutters",
    "siding",
)


def kebab_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def page_city(filename: str) -> str | None:
    name = filename
    if name == "roofer-lincoln-park-mi.html":
        return "Lincoln Park"
    m = re.match(r"^(.+)-roofer\.html$", name)
    if m:
        return kebab_to_title(m.group(1))
    for svc in SERVICE_PREFIXES:
        prefix = svc + "-"
        if name.startswith(prefix) and name.endswith(".html"):
            slug = name[len(prefix):-len(".html")]
            if slug:
                return kebab_to_title(slug)
    return None


def is_city_hub(filename: str) -> bool:
    return filename == "roofer-lincoln-park-mi.html" or filename.endswith("-roofer.html")


def is_combo(filename: str) -> bool:
    return any(filename.startswith(svc + "-") for svc in SERVICE_PREFIXES) and filename.endswith(".html")


# Regex patterns scoped to <h2>...</h2> tags so we never touch nav/footer/schema
H2_FAQS_FOR_HOMEOWNERS = re.compile(
    r'(<h2[^>]*>)([^<]+?)\s+FAQs\s+for\s+([^<]+?)\s+Homeowners(</h2>)',
)
H2_CITY_ROOFING_FAQS = re.compile(
    r'(<h2[^>]*>)([^<]+?)\s+Roofing\s+FAQs(</h2>)',
)
H2_CONTRACTOR_SERVING = re.compile(
    r'(<h2[^>]*>)([^<]+?)\s+Contractor\s+Serving\s+([^<]+?),\s+Michigan(</h2>)',
)
H2_LOCAL_ROOFING_COMPANY = re.compile(
    r'(<h2[^>]*>)Local\s+Roofing\s+Company\s+Serving\s+([^<]+?),\s+Michigan(</h2>)',
)
H2_ROOFING_SERVICES_IN = re.compile(
    r'(<h2[^>]*>)Roofing\s+Services\s+in\s+([^<]+?)(</h2>)',
)
# Combo pages have a paragraph below the stage5 H2 that hardcodes the wrong city name
# (Grosse Ile copy-paste bug). Fix it to match the page city.
P_EVERY_CITY_SERVICE = re.compile(
    r'(<p[^>]*>)Every\s+([^<]+?)\s+roofing\s+service\s+we\s+offer',
)


def patch_file(path: Path, dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    original = text
    counts = {"faq_homeowners": 0, "city_roofing_faqs": 0, "contractor_serving": 0,
              "local_roofing_company": 0, "stage5_h2": 0, "stage5_p": 0}

    fname = path.name
    correct_city = page_city(fname)

    def faq_homeowners_sub(m):
        counts["faq_homeowners"] += 1
        service, city = m.group(2).strip(), m.group(3).strip()
        return f"{m.group(1)}{service} FAQ — {city}{m.group(4)}"

    def city_roofing_faqs_sub(m):
        counts["city_roofing_faqs"] += 1
        city = m.group(2).strip()
        return f"{m.group(1)}Roofing FAQ — {city}{m.group(3)}"

    def contractor_serving_sub(m):
        counts["contractor_serving"] += 1
        service, city = m.group(2).strip(), m.group(3).strip()
        return f"{m.group(1)}{service} Experts Serving {city}, Michigan{m.group(4)}"

    def local_roofing_company_sub(m):
        counts["local_roofing_company"] += 1
        city = m.group(2).strip()
        return f"{m.group(1)}Roofing Experts Serving {city}, Michigan{m.group(3)}"

    def stage5_sub(m):
        counts["stage5_h2"] += 1
        # Always force the page-correct city (fixes Grosse Ile copy-paste bug)
        target_city = correct_city if correct_city else m.group(2).strip()
        return f"{m.group(1)}All {target_city} Roofing Services — Owens Corning Preferred Since 2011{m.group(3)}"

    def stage5_p_sub(m):
        counts["stage5_p"] += 1
        target_city = correct_city if correct_city else m.group(2).strip()
        return f"{m.group(1)}Every {target_city} roofing service we offer"

    text = H2_FAQS_FOR_HOMEOWNERS.sub(faq_homeowners_sub, text)
    text = H2_CITY_ROOFING_FAQS.sub(city_roofing_faqs_sub, text)
    text = H2_CONTRACTOR_SERVING.sub(contractor_serving_sub, text)
    text = H2_LOCAL_ROOFING_COMPANY.sub(local_roofing_company_sub, text)
    text = H2_ROOFING_SERVICES_IN.sub(stage5_sub, text)
    text = P_EVERY_CITY_SERVICE.sub(stage5_p_sub, text)

    total = sum(counts.values())
    if total and text != original and not dry_run:
        path.write_text(text, encoding="utf-8")
    counts["_total"] = total
    counts["_changed"] = total > 0 and text != original
    return counts


def main():
    dry_run = "--dry-run" in sys.argv
    files = sorted(p for p in ROOT.glob("*.html") if is_city_hub(p.name) or is_combo(p.name))

    totals = {"faq_homeowners": 0, "city_roofing_faqs": 0, "contractor_serving": 0,
              "local_roofing_company": 0, "stage5_h2": 0, "stage5_p": 0}
    files_changed = 0

    for f in files:
        result = patch_file(f, dry_run)
        if result["_changed"] or (dry_run and result["_total"]):
            files_changed += 1
            for k in totals:
                totals[k] += result[k]
            if dry_run:
                bits = [f"{k}={v}" for k, v in result.items() if not k.startswith("_") and v]
                print(f"[DRY] {f.name}: {', '.join(bits)}")

    mode = "DRY-RUN" if dry_run else "APPLIED"
    print(f"\n{mode}: {files_changed}/{len(files)} pages updated")
    print(f"  FAQ '...for [City] Homeowners' -> 'FAQ — [City]':       {totals['faq_homeowners']}")
    print(f"  '[City] Roofing FAQs'          -> 'Roofing FAQ — [City]': {totals['city_roofing_faqs']}")
    print(f"  '[Svc] Contractor Serving'     -> '[Svc] Experts Serving': {totals['contractor_serving']}")
    print(f"  'Local Roofing Company Serving' -> 'Roofing Experts Serving': {totals['local_roofing_company']}")
    print(f"  'Roofing Services in [X]'      -> 'All [PageCity] ... Preferred Since 2011': {totals['stage5_h2']}")
    print(f"  'Every [WrongCity] roofing service' paragraph -> '[PageCity]':                {totals['stage5_p']}")


if __name__ == "__main__":
    main()
