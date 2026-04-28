"""
Upgrade city hub page FAQ answers to pack 4-of-8 AIO anchor signals.
Uses JSON parsing (like _aio_legitimacy_fix.py) to handle all template variants.
Updates BOTH the JSON-LD schema text and the visible HTML <p> accordion text.

Anchors injected into two FAQ answers per page:
  "How long..." → "completed in one day" + "no subcontractors" + "Established 1990"
  "licensed and insured..." → "since 1996" + "Established 1990" + "25-year non-prorated" + "no subcontractors"
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://www.lincolnparkroofing.com"

JSONLD_BLOCK_RE = re.compile(
    r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)',
    re.DOTALL,
)


def _upgrade_how_long(old_text: str, city: str) -> str:
    """Replace the 'How long' FAQ answer with an anchor-packed version."""
    return (
        f"Most {city} roof replacements are completed in one day. "
        f"Our direct in-house crew — no subcontractors — has completed 6,000 roofs "
        f"across Downriver Michigan since Established 1990. "
        f"Larger {city} homes or roofs with multiple layers may take two days. "
        f"We work efficiently to minimize disruption for {city} homeowners, "
        f"and your property gets a full cleanup before we leave."
    )


def _upgrade_licensed(old_text: str, city: str) -> str:
    """Replace the 'licensed and insured' FAQ answer with an anchor-packed version."""
    return (
        f"Yes. Lincoln Park Roofing has been fully licensed and insured in Michigan "
        f"since 1996 — Established 1990, with 6,000 roofs completed across Downriver Michigan. "
        f"Owens Corning Preferred Contractor since 2011. "
        f"Every full replacement comes with a lifetime shingle warranty plus a "
        f"25-year non-prorated labor warranty on workmanship. "
        f"Direct in-house crew only — no subcontractors on any {city} job. "
        f"{city} homeowners can verify our credentials before any work begins."
    )


def _extract_city_from_how_long(q_name: str) -> str:
    """'How long does a roof replacement take in Allen Park?' -> 'Allen Park'"""
    m = re.search(r"take in (.+?)\??$", q_name)
    return m.group(1).strip() if m else ""


def _extract_city_from_licensed(q_name: str) -> str:
    """'Are you licensed and insured to work in Allen Park, Michigan?' -> 'Allen Park'
       Also handles 'work in Brownstown Township?' (no comma before Michigan)"""
    # Try comma-delimited first: "work in Allen Park, Michigan?"
    m = re.search(r"work in (.+?),", q_name)
    if m:
        return m.group(1).strip()
    # Fall back: everything between "work in " and "?"
    m = re.search(r"work in (.+?)\??$", q_name)
    return m.group(1).strip() if m else ""


def patch_file(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    changes = 0

    def replace_block(m):
        nonlocal changes
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body)
        except Exception:
            return m.group(0)

        graph = data.get("@graph")
        if not isinstance(graph, list):
            return m.group(0)

        modified = False
        for node in graph:
            if not isinstance(node, dict) or node.get("@type") != "FAQPage":
                continue
            for q in node.get("mainEntity", []):
                q_name = q.get("name", "")
                answer = q.get("acceptedAnswer", {})
                old_ans = answer.get("text", "")

                if "How long does a roof replacement take" in q_name:
                    city = _extract_city_from_how_long(q_name)
                    if city and "Established 1990" not in old_ans:
                        new_ans = _upgrade_how_long(old_ans, city)
                        # Update HTML text before changing JSON (need old_ans for HTML swap)
                        answer["text"] = new_ans
                        modified = True
                        changes += 1

                elif "licensed and insured to work" in q_name:
                    city = _extract_city_from_licensed(q_name)
                    if city and "Established 1990" not in old_ans:
                        new_ans = _upgrade_licensed(old_ans, city)
                        answer["text"] = new_ans
                        modified = True
                        changes += 1

        if not modified:
            return m.group(0)

        new_body = json.dumps(data, indent=2, ensure_ascii=False)
        return prefix + new_body + suffix

    # Step 1: update JSON-LD schema (also collects old→new answer mappings)
    # Re-parse to get the old→new mapping by doing two passes
    old_answers = {}  # old_text -> new_text

    def collect_replacements(m):
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body)
        except Exception:
            return m.group(0)
        graph = data.get("@graph")
        if not isinstance(graph, list):
            return m.group(0)
        for node in graph:
            if not isinstance(node, dict) or node.get("@type") != "FAQPage":
                continue
            for q in node.get("mainEntity", []):
                q_name = q.get("name", "")
                answer = q.get("acceptedAnswer", {})
                old_ans = answer.get("text", "")
                if "How long does a roof replacement take" in q_name:
                    city = _extract_city_from_how_long(q_name)
                    if city and "Established 1990" not in old_ans:
                        old_answers[old_ans] = _upgrade_how_long(old_ans, city)
                elif "licensed and insured to work" in q_name:
                    city = _extract_city_from_licensed(q_name)
                    if city and "Established 1990" not in old_ans:
                        old_answers[old_ans] = _upgrade_licensed(old_ans, city)
        return m.group(0)

    JSONLD_BLOCK_RE.sub(collect_replacements, text)

    if not old_answers:
        return 0

    # Apply JSON schema update
    text = JSONLD_BLOCK_RE.sub(replace_block, text)

    # Step 2: update visible HTML <p> text (same content, just inside <p> tags)
    for old_ans, new_ans in old_answers.items():
        if old_ans in text:
            text = text.replace(old_ans, new_ans)

    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")

    return changes


def main():
    dry_run = "--dry-run" in sys.argv
    files = sorted(ROOT.glob("*-roofer.html"))
    touched = total_changes = 0
    for f in files:
        n = patch_file(f, dry_run)
        if n:
            touched += 1
            total_changes += n
            if dry_run:
                print(f"[DRY] {f.name}: {n} FAQ answers upgraded")

    mode = "DRY-RUN" if dry_run else "APPLIED"
    print(f"\n{mode}: {touched}/{len(files)} city pages updated ({total_changes} FAQ answers)")


if __name__ == "__main__":
    main()
