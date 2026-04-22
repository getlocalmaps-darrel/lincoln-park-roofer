"""Update sitemap.xml + ai.txt + llms.txt with the 28 new service x city combo URLs.
Idempotent: skips entries already present.
"""
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
BASE_URL = "https://www.lincolnparkroofing.com"
LASTMOD = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

CITIES = [
    ("grosse-ile", "Grosse Ile"),
    ("allen-park", "Allen Park"),
    ("wyandotte", "Wyandotte"),
    ("livonia", "Livonia"),
]
SERVICES = [
    ("roof-repair", "Roof Repair"),
    ("roof-replacement", "Roof Replacement"),
    ("storm-damage-repair", "Storm Damage Repair"),
    ("emergency-roof-repair", "Emergency Roof Repair"),
    ("gutters", "Gutter Installation"),
    ("siding", "Siding Installation"),
    ("commercial-roofing", "Commercial Roofing"),
]

def combo_html_url(s, c): return f"{BASE_URL}/{s}-{c}.html"
def combo_ai_url(s, c):   return f"{BASE_URL}/{s}-{c}-ai.txt"

# ---- sitemap.xml ----
sitemap_path = BASE / "sitemap.xml"
xml = sitemap_path.read_text(encoding="utf-8")
entries = []
for s, sn in SERVICES:
    for c, cn in CITIES:
        url = combo_html_url(s, c)
        if url in xml:
            continue
        entries.append(
            f'  <url>\n'
            f'    <loc>{url}</loc>\n'
            f'    <lastmod>{LASTMOD}</lastmod>\n'
            f'    <priority>0.85</priority>\n'
            f'  </url>\n'
        )
if entries:
    xml = xml.replace("</urlset>", "".join(entries) + "</urlset>")
    sitemap_path.write_text(xml, encoding="utf-8")
print(f"sitemap.xml: +{len(entries)} URLs")

# ---- ai.txt ----
ai_path = BASE / "ai.txt"
ai = ai_path.read_text(encoding="utf-8")
section_header = "### Service x City AI Files (Per-Combination)"
if section_header not in ai:
    block = ["", "", section_header, ""]
    for s, sn in SERVICES:
        for c, cn in CITIES:
            block.append(f"- [{sn} in {cn}]({combo_ai_url(s, c)})")
    block.append("")
    ai = ai.rstrip() + "\n" + "\n".join(block)
    ai_path.write_text(ai, encoding="utf-8")
    print("ai.txt: appended 28 combo ai.txt links")
else:
    print("ai.txt: section already exists, skipped")

# ---- llms.txt ----
llms_path = BASE / "llms.txt"
llms = llms_path.read_text(encoding="utf-8")
section_header = "## Service x City Pages (28 Combinations)"
if section_header not in llms:
    block = ["", section_header, ""]
    for s, sn in SERVICES:
        for c, cn in CITIES:
            block.append(
                f"- [{sn} in {cn}]({combo_html_url(s, c)}) — "
                f"local {sn.lower()} for {cn} homes with Owens Corning certified installation and workmanship warranty."
            )
    block.append("")
    llms = llms.rstrip() + "\n" + "\n".join(block)
    llms_path.write_text(llms, encoding="utf-8")
    print("llms.txt: appended 28 combo page links")
else:
    print("llms.txt: section already exists, skipped")

print("\nDone.")
