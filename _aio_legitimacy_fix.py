"""
LPR AI Overview legitimacy fix — applies §15.10 of web_design_master.md across the site.

Three patches:
  1. Strip the hidden "AI-SEARCH MAGNET" div (manual-action trigger) from every page that has it.
  2. Inject Person (Scott Kincaide) + BreadcrumbList graph nodes into every page that has the
     LocalBusiness @graph JSON-LD block, plus add image/logo/foundingDate/founder/employee/
     hasCredential fields to the LocalBusiness node itself.
  3. Verify (grep counts).

Usage:
  python _aio_legitimacy_fix.py --dry-run
  python _aio_legitimacy_fix.py --apply
  python _aio_legitimacy_fix.py --verify
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://www.lincolnparkroofing.com"

# ----- Patch 1: hidden div ----------------------------------------------------
# Two flavors:
# 1. With <!-- AI-SEARCH MAGNET --> comment prefix (original city pages)
# 2. Without comment — plain display:none+itemprop div (roofer + county pages)

HIDDEN_DIV_RE = re.compile(
    r'(?:\s*<!-- AI-SEARCH MAGNET \(HIDDEN TAG PROTOCOL\) -->\s*\n)?'
    r'\s*<div style="display:none[^"]*"[^>]*aria-hidden="true">'
    r'<p itemprop="description">[^<]*</p></div>[^\n]*\n',
    re.MULTILINE,
)

# ----- Patch 2: schema enrichment --------------------------------------------

# Insertion #1: add image/logo/foundingDate/founder/employee/hasCredential
# to the LocalBusiness graph node. We anchor on the `@id: #business` line
# (always the second line of the LB node) and inject right after the `"name":` field
# that follows it.
LB_NAME_LINE_RE = re.compile(
    r'(        "@id": "' + re.escape(SITE_URL) + r'/#business",\s*\n'
    r'        "name": "Lincoln Park Roofing",\s*\n)',
    re.MULTILINE,
)

LOCALBUSINESS_FIELDS_INJECT = (
    '        "image": "' + SITE_URL + '/lincoln park logo.png",\n'
    '        "logo": "' + SITE_URL + '/lincoln park logo.png",\n'
    '        "foundingDate": "1990",\n'
    '        "founder": { "@id": "' + SITE_URL + '/#owner" },\n'
    '        "employee": { "@id": "' + SITE_URL + '/#owner" },\n'
    '        "hasCredential": [\n'
    '          { "@type": "EducationalOccupationalCredential", "name": "Owens Corning Preferred Contractor", "credentialCategory": "manufacturer-certification" },\n'
    '          { "@type": "EducationalOccupationalCredential", "name": "Licensed in Michigan since 1996", "credentialCategory": "license" }\n'
    '        ],\n'
)

# Insertion #2: add Person + BreadcrumbList graph nodes immediately after the
# LocalBusiness closing `},` and before the next `{` graph node (Service).
# Multi-line layout (e.g., allen-park-roofer.html).
LB_TO_SERVICE_RE = re.compile(
    r'(\n      \},\s*\n)'              # closing LB node
    r'(      \{\s*\n'                   # opening of next node
    r'        "@type": "Service",)',
    re.MULTILINE,
)

# Compact layout (e.g., brownstown-roofer.html) — Service node on a single line.
LB_TO_SERVICE_COMPACT_RE = re.compile(
    r'(\n      \},\s*\n)'                          # closing LB node
    r'(      \{ "@type": "Service",)',              # opening + type all on one line
    re.MULTILINE,
)

# Compact layout — LB-fields injection point: anchor on the @id+name LB lines
# (compact form has these on consecutive lines but with extra fields after name).
LB_NAME_LINE_COMPACT_RE = re.compile(
    r'(        "@type": \["RoofingContractor","LocalBusiness"\], "@id": "' + re.escape(SITE_URL) + r'/#business",\s*\n'
    r'        "name": "Lincoln Park Roofing", "url": "' + re.escape(SITE_URL) + r'/", "telephone": "[^"]+",\s*\n)',
    re.MULTILINE,
)

PERSON_NODE = (
    '      {\n'
    '        "@type": "Person",\n'
    '        "@id": "' + SITE_URL + '/#owner",\n'
    '        "name": "Scott Kincaide",\n'
    '        "jobTitle": "Owner",\n'
    '        "worksFor": { "@id": "' + SITE_URL + '/#business" },\n'
    '        "image": "' + SITE_URL + '/lincoln park logo.png",\n'
    '        "knowsAbout": [\n'
    '          "Residential Roofing",\n'
    '          "Owens Corning Preferred Installation",\n'
    '          "Storm Damage Assessment",\n'
    '          "Roof Rejuvenation",\n'
    '          "Seamless Gutter Engineering",\n'
    '          "Michigan Residential Building Code"\n'
    '        ],\n'
    '        "hasCredential": [\n'
    '          { "@type": "EducationalOccupationalCredential", "name": "Owens Corning Preferred Contractor", "credentialCategory": "manufacturer-certification" },\n'
    '          { "@type": "EducationalOccupationalCredential", "name": "Licensed in Michigan since 1996", "credentialCategory": "license" }\n'
    '        ]\n'
    '      },\n'
)


def derive_breadcrumb(html_path: Path) -> str:
    """Build a BreadcrumbList graph node node for this page based on its filename."""
    slug = html_path.stem  # e.g. "allen-park-roofer" or "roof-replacement-belleville"
    canonical_url = f"{SITE_URL}/{slug}.html"

    # Heuristics to set the breadcrumb name. Tier 2 = service or city, tier 3 = combined.
    if slug == "index" or slug == "":
        return ""  # don't add to home
    name = slug.replace("-", " ").title()

    return (
        '      {\n'
        '        "@type": "BreadcrumbList",\n'
        '        "itemListElement": [\n'
        '          { "@type": "ListItem", "position": 1, "name": "Home", "item": "' + SITE_URL + '/" },\n'
        '          { "@type": "ListItem", "position": 2, "name": "' + name + '", "item": "' + canonical_url + '" }\n'
        '        ]\n'
        '      },\n'
    )


# ----- Patch 2 (universal): JSON-based mutation -------------------------------

JSONLD_BLOCK_RE = re.compile(
    r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)',
    re.DOTALL,
)


def _person_node():
    return {
        "@type": "Person",
        "@id": f"{SITE_URL}/#owner",
        "name": "Scott Kincaide",
        "jobTitle": "Owner",
        "worksFor": {"@id": f"{SITE_URL}/#business"},
        "image": f"{SITE_URL}/lincoln park logo.png",
        "knowsAbout": [
            "Residential Roofing",
            "Owens Corning Preferred Installation",
            "Storm Damage Assessment",
            "Roof Rejuvenation",
            "Seamless Gutter Engineering",
            "Michigan Residential Building Code",
        ],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "Owens Corning Preferred Contractor", "credentialCategory": "manufacturer-certification"},
            {"@type": "EducationalOccupationalCredential", "name": "Licensed in Michigan since 1996", "credentialCategory": "license"},
        ],
    }


def _breadcrumb_node(html_path: Path):
    slug = html_path.stem
    if slug in ("index", ""):
        return None
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": slug.replace("-", " ").title(), "item": f"{SITE_URL}/{slug}.html"},
        ],
    }


def _is_local_business(node):
    t = node.get("@type")
    if isinstance(t, list):
        return any(x in ("LocalBusiness", "RoofingContractor") for x in t)
    return t in ("LocalBusiness", "RoofingContractor")


def patch_jsonld_via_python(text: str, path: Path):
    """Mutate every @graph JSON-LD block to add LB fields + Person + BreadcrumbList.
    Returns (new_text, changed_count)."""
    changes = []

    def replace_block(m):
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body)
        except Exception:
            return m.group(0)  # leave alone if not valid JSON

        graph = data.get("@graph")
        if not isinstance(graph, list):
            return m.group(0)

        # Find LB index
        lb_idx = next((i for i, n in enumerate(graph) if isinstance(n, dict) and _is_local_business(n)), None)
        if lb_idx is None:
            return m.group(0)
        lb = graph[lb_idx]

        modified = False
        # LB fields
        if "foundingDate" not in lb:
            lb_addons = {
                "image": f"{SITE_URL}/lincoln park logo.png",
                "logo": f"{SITE_URL}/lincoln park logo.png",
                "foundingDate": "1990",
                "founder": {"@id": f"{SITE_URL}/#owner"},
                "employee": {"@id": f"{SITE_URL}/#owner"},
                "hasCredential": [
                    {"@type": "EducationalOccupationalCredential", "name": "Owens Corning Preferred Contractor", "credentialCategory": "manufacturer-certification"},
                    {"@type": "EducationalOccupationalCredential", "name": "Licensed in Michigan since 1996", "credentialCategory": "license"},
                ],
            }
            # Insert addons right after "name" if possible (preserves a sensible order)
            new_lb = {}
            inserted = False
            for k, v in lb.items():
                new_lb[k] = v
                if k == "name" and not inserted:
                    new_lb.update(lb_addons)
                    inserted = True
            if not inserted:
                new_lb.update(lb_addons)
            graph[lb_idx] = new_lb
            modified = True

        # Person + Breadcrumb
        has_person = any(isinstance(n, dict) and n.get("@type") == "Person" for n in graph)
        has_breadcrumb = any(isinstance(n, dict) and n.get("@type") == "BreadcrumbList" for n in graph)
        new_nodes = []
        if not has_person:
            new_nodes.append(_person_node())
        if not has_breadcrumb:
            bc = _breadcrumb_node(path)
            if bc:
                new_nodes.append(bc)
        if new_nodes:
            graph[lb_idx + 1:lb_idx + 1] = new_nodes
            modified = True

        if not modified:
            return m.group(0)

        changes.append("json-mutate")
        # Re-serialize with 2-space indent (compact-ish, readable)
        new_body = json.dumps(data, indent=2, ensure_ascii=False)
        return prefix + new_body + suffix

    new_text = JSONLD_BLOCK_RE.sub(replace_block, text)
    return new_text, len(changes)


# ----- Apply ------------------------------------------------------------------

def fix_file(path: Path, dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    original = text
    summary = {"path": str(path.relative_to(ROOT)), "patches": []}

    # Patch 1
    new, n_hidden = HIDDEN_DIV_RE.subn("\n", text)
    if n_hidden:
        text = new
        summary["patches"].append(f"strip-hidden-div×{n_hidden}")

    # Patch 2 — JSON-based mutation (handles ALL @graph layouts)
    new_text, n_json = patch_jsonld_via_python(text, path)
    if n_json:
        text = new_text
        summary["patches"].append(f"json-mutate×{n_json}")

    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")

    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="cap files processed (debug)")
    args = ap.parse_args()

    if not (args.apply or args.dry_run or args.verify):
        ap.error("pass --apply, --dry-run, or --verify")

    files = sorted(ROOT.glob("*.html"))
    if args.limit:
        files = files[: args.limit]

    if args.verify:
        bad_hidden = bad_no_person = bad_no_breadcrumb = 0
        for f in files:
            t = f.read_text(encoding="utf-8")
            if HIDDEN_DIV_RE.search(t):
                bad_hidden += 1
            # only count schema gaps on pages that have the LB @graph
            if "@graph" in t:
                if '"@type": "Person"' not in t:
                    bad_no_person += 1
                if '"@type": "BreadcrumbList"' not in t:
                    bad_no_breadcrumb += 1
        print(f"Verify: {len(files)} files scanned")
        print(f"  pages still carrying hidden manipulative div: {bad_hidden}")
        print(f"  pages with @graph missing Person:               {bad_no_person}")
        print(f"  pages with @graph missing BreadcrumbList:       {bad_no_breadcrumb}")
        return

    touched = 0
    by_patch = {"strip-hidden-div×1": 0, "add-LB-fields": 0, "add-Person+Breadcrumb": 0}
    for f in files:
        s = fix_file(f, dry_run=args.dry_run)
        if s["patches"]:
            touched += 1
            for p in s["patches"]:
                by_patch[p] = by_patch.get(p, 0) + 1
            if args.dry_run:
                print(f"[DRY] {s['path']}: {','.join(s['patches'])}")

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"\n{mode}: {touched}/{len(files)} files touched")
    for k, v in by_patch.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
