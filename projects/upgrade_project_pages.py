#!/usr/bin/env python3
"""
upgrade_project_pages.py
Upgrades ALL project HTML pages in /projects/ to match the main site's
mega menu nav, categorized footer, review star bar, and AI search magnet.

Reads the current nav/footer from roof-repair.html (source of truth)
and replaces the old project-page header/footer/mobile-menu with the
new versions, adjusting image paths for the /projects/ subdirectory.

Usage:
    python upgrade_project_pages.py          # dry-run (default)
    python upgrade_project_pages.py --apply  # actually write changes
"""

import os
import re
import sys
import glob

# ── PATHS ──────────────────────────────────────────────────────────────
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_PAGE = os.path.join(SITE_ROOT, "roof-repair.html")
PROJECTS_DIR = os.path.join(SITE_ROOT, "projects")

DRY_RUN = "--apply" not in sys.argv


# ── STEP 1: EXTRACT COMPONENTS FROM SOURCE PAGE ───────────────────────

def read_source():
    with open(SOURCE_PAGE, "r", encoding="utf-8") as f:
        return f.read()


def extract_mega_menu_css(src):
    """Extract CSS between /* MEGA MENU NAV */ and mobile-cat-label closing brace."""
    m = re.search(
        r'(/\* MEGA MENU NAV \*/.*?\.mobile-cat-label\s*\{[^}]*\})',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find mega menu CSS in source page")
    return m.group(1)


def extract_desktop_nav(src):
    """Extract from <!-- Desktop Nav --> through </nav>."""
    m = re.search(
        r'(<!-- Desktop Nav -->.*?</nav>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find desktop nav in source page")
    return m.group(1)


def extract_mobile_menu(src):
    """Extract the full mobile menu div from <!-- MOBILE MENU --> through Blog link + closing div."""
    m = re.search(
        r'(<!-- MOBILE MENU -->\s*<div id="mobile-menu".*?</div>\s*</div>\s*</div>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find mobile menu in source page")
    return m.group(1)


def extract_review_bar(src):
    """Extract the review bar div line."""
    m = re.search(
        r'(<div id="review-bar"[^>]*>.*?</div>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find review bar in source page")
    return m.group(1)


def extract_footer(src):
    """Extract from <footer class="bg-gradient... through </footer>."""
    m = re.search(
        r'(<footer class="bg-gradient[^"]*".*?</footer>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find footer in source page")
    return m.group(1)


def extract_mobile_sticky(src):
    """Extract the main site's mobile bottom sticky bar."""
    m = re.search(
        r'(<!-- MOBILE BOTTOM STICKY BAR -->\s*<div class="fixed bottom-0.*?</div>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find mobile sticky bar in source page")
    return m.group(1)


def extract_bottom_script(src):
    """Extract the main site's bottom script block (menu toggle, year, etc.)."""
    m = re.search(
        r'(<!-- Scripts -->\s*<script>.*?</script>)',
        src, re.DOTALL
    )
    if not m:
        raise RuntimeError("Could not find bottom script in source page")
    return m.group(1)


# ── STEP 2: BUILD REPLACEMENT BLOCKS ──────────────────────────────────

def fix_image_paths_for_subdir(html):
    """
    Adjust image src paths for /projects/ subdirectory:
    - src="lincoln park logo.png" -> src="../lincoln park logo.png"
    - src="lincoln-park-logo-footer.webp" -> src="../lincoln-park-logo-footer.webp"
    - src="slide-1.jpg" -> src="../slide-1.jpg"
    But DON'T touch absolute URLs (https://...) or already-prefixed (../...) paths.
    And DON'T touch href links (those use absolute / paths).
    """
    def replace_src(match):
        prefix = match.group(1)  # 'src="' or "src='"
        path = match.group(2)
        quote = match.group(3)
        # Skip absolute URLs, data: URIs, already relative paths, and / paths
        if path.startswith(('http://', 'https://', 'data:', '../', '/', '#')):
            return match.group(0)
        return f'{prefix}../{path}{quote}'

    # Match src="..." and src='...'
    html = re.sub(r'''(src=["'])([^"']+)(["'])''', replace_src, html)
    return html


def build_new_header(review_bar, desktop_nav):
    """Build the new header block matching main site structure."""
    header = f'''  <header class="critical-header flex flex-col">
    {review_bar}
    <div class="critical-top-bar">
      <p class="big-text tracking-wide text-xs md:text-sm">
        <span class="text-brand-accent">Save Thousands with Roof Rejuvenation</span> &bull; Local Lincoln Park Roofers &bull; Honest Pricing
      </p>
    </div>
    <div class="bg-white w-full">
      <div class="critical-nav">
        <a href="/" class="flex items-center gap-2 z-50 shrink-0">
          <img src="../lincoln park logo.png" alt="Lincoln Park Roofing" width="180" height="80" class="critical-logo object-contain">
        </a>

        {desktop_nav}

        <div class="desktop-nav hidden lg:flex items-center space-x-4">
          <a href="tel:7342245615" class="flex flex-col items-end">
            <span class="text-xs text-gray-500 font-bold uppercase">Call Now</span>
            <span class="big-text text-xl font-bold text-brand-dark leading-none hover:text-brand-primary transition">(734) 224-5615</span>
          </a>
          <a href="tel:7342245615" class="btn-primary-polished text-white font-bold py-3 px-6 rounded shadow-md uppercase tracking-wider">Get a Free Quote</a>
        </div>

        <button id="menu-btn" class="mobile-menu-btn lg:hidden text-2xl text-brand-dark focus:outline-none z-50 p-2" aria-label="Menu">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </div>
  </header>'''
    return header


# ── STEP 3: CSS ADDITIONS ─────────────────────────────────────────────

HEADER_CSS_ADDITIONS = """
      /* CRITICAL HEADER (from main site) */
      .critical-header { position: fixed; top: 0; width: 100%; z-index: 1000; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
      .critical-top-bar { background-color: #0056b3; color: white; text-align: center; padding: 8px; font-size: 12px; text-transform: uppercase; font-weight: bold; }
      .critical-nav { display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; max-width: 1280px; margin: 0 auto; }
      .critical-logo { height: 48px; width: auto; object-fit: contain; }

      /* NAV VISIBILITY */
      .desktop-nav { display: none; }
      .mobile-menu-btn { display: block; }
      @media (min-width: 1024px) {
          .desktop-nav { display: flex; gap: 2rem; align-items: center; }
          .mobile-menu-btn { display: none; }
      }
      .nav-link {
          text-transform: uppercase; font-weight: 700; font-size: 0.875rem; letter-spacing: 0.05em; color: #374151; text-decoration: none; transition: color 0.3s;
      }
      .nav-link:hover { color: #0056b3; }

      /* BUTTONS */
      .btn-white-polished {
          background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 1);
          color: #0056b3; border: 1px solid #e2e8f0; transition: all 0.3s ease;
          text-decoration: none; display: inline-block; text-align: center;
      }
      .btn-primary-polished {
          background: linear-gradient(180deg, #3b82f6 0%, #0056b3 100%);
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
          transition: all 0.3s ease; color: white; text-decoration: none; display: inline-block; text-align: center;
      }

      /* UTILITIES from main site */
      .big-text { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 1px; }
      .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0; }

      /* MOBILE MENU (main site version) */
      #mobile-menu { transition: transform 0.3s ease-in-out; transform: translateX(-100%); }
      #mobile-menu.open { transform: translateX(0); }
"""


AI_SEARCH_MAGNET = '<div style="display:none !important; visibility:hidden; height:0; width:0; overflow:hidden;" aria-hidden="true"><p itemprop="description">Lincoln Park Roofing project — licensed roofing contractor serving Lincoln Park, Allen Park, Taylor, and Downriver Michigan. Roof replacement, repair, rejuvenation, siding, and gutters.</p></div>'


# ── STEP 4: PROCESS EACH PROJECT PAGE ─────────────────────────────────

def process_file(filepath, mega_css, new_header, new_mobile_menu, new_footer, new_mobile_sticky, new_script):
    """Process a single project HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    changes = []

    # ── 4a: Add AI Search Magnet after <body> tag ──
    if 'itemprop="description"' not in html:
        html = re.sub(
            r'(<body[^>]*>)',
            r'\1\n\n  ' + AI_SEARCH_MAGNET + '\n',
            html, count=1
        )
        changes.append("Added AI Search Magnet")
    else:
        changes.append("AI Search Magnet already present (skipped)")

    # ── 4b: Replace old header ──
    # Old header: <header class="site-header">...</header>
    old_header_match = re.search(
        r'<header class="site-header">.*?</header>',
        html, re.DOTALL
    )
    if old_header_match:
        html = html[:old_header_match.start()] + new_header + html[old_header_match.end():]
        changes.append("Replaced old site-header with mega menu header")
    else:
        # Maybe already upgraded? Check for critical-header
        if 'critical-header' in html:
            changes.append("Header already upgraded (skipped)")
        else:
            changes.append("WARNING: Could not find old header to replace")

    # ── 4c: Replace old mobile menu ──
    # Old mobile menu: <div id="mobile-menu" ... (the old flat version without categories)
    # The new mobile menu from the source has <!-- MOBILE MENU --> comment
    old_mobile_match = re.search(
        r'\s*<div id="mobile-menu"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>',
        html, re.DOTALL
    )
    if old_mobile_match:
        # Check if this is the OLD mobile menu (no mobile-cat-label = old)
        old_mobile_text = old_mobile_match.group(0)
        if 'mobile-cat-label' not in old_mobile_text:
            html = html[:old_mobile_match.start()] + '\n\n  ' + new_mobile_menu + '\n' + html[old_mobile_match.end():]
            changes.append("Replaced old mobile menu with categorized mega menu version")
        else:
            changes.append("Mobile menu already has categories (skipped)")
    else:
        # Try a simpler pattern — the old project mobile menu might have different nesting
        old_mobile_match2 = re.search(
            r'\s*<div id="mobile-menu".*?(?=<div class="breadcrumb|<div class="hero|<article|<section)',
            html, re.DOTALL
        )
        if old_mobile_match2:
            old_mobile_text = old_mobile_match2.group(0)
            if 'mobile-cat-label' not in old_mobile_text:
                html = html[:old_mobile_match2.start()] + '\n\n  ' + new_mobile_menu + '\n\n' + html[old_mobile_match2.end():]
                changes.append("Replaced old mobile menu (alt pattern)")
            else:
                changes.append("Mobile menu already upgraded (skipped)")
        else:
            changes.append("WARNING: Could not find old mobile menu to replace")

    # ── 4d: Replace old footer ──
    # Old footer: <footer style="background:linear-gradient(135deg,#0f172a...">...</footer>
    old_footer_match = re.search(
        r'<footer style="background:linear-gradient[^"]*"[^>]*>.*?</footer>',
        html, re.DOTALL
    )
    if old_footer_match:
        html = html[:old_footer_match.start()] + new_footer + html[old_footer_match.end():]
        changes.append("Replaced old inline-styled footer with categorized footer")
    else:
        if 'bg-gradient-to-br' in html:
            changes.append("Footer already upgraded (skipped)")
        else:
            changes.append("WARNING: Could not find old footer to replace")

    # ── 4e: Add mega menu CSS before closing </style> ──
    if '/* MEGA MENU NAV */' not in html:
        # Find the closing </style> tag and insert mega menu CSS + header CSS before it
        css_to_inject = HEADER_CSS_ADDITIONS + '\n' + mega_css + '\n'
        # Insert before the LAST </style> in <head>
        style_close_matches = list(re.finditer(r'</style>', html))
        if style_close_matches:
            # Use the first </style> (should be in <head>)
            pos = style_close_matches[0].start()
            html = html[:pos] + '\n' + css_to_inject + '\n    ' + html[pos:]
            changes.append("Injected mega menu CSS + header CSS into <style> block")
        else:
            changes.append("WARNING: Could not find </style> to inject CSS")
    else:
        changes.append("Mega menu CSS already present (skipped)")

    # ── 4e-extra: Remove old project-specific nav CSS that conflicts ──
    # Remove the old .site-header, .nav, .nav-links, .nav-phone, .nav-hamburger CSS
    # since we're now using .critical-header
    old_css_patterns = [
        r'/\* Sticky Header \*/\s*\.site-header\s*\{[^}]*\}\s*',
        r'/\* Navigation \*/\s*\.nav\s*\{[^}]*\}\s*\.nav-logo\s*\{[^}]*\}\s*\.nav-logo img\s*\{[^}]*\}\s*\.nav-links\s*\{[^}]*\}\s*\.nav-links li\s*\{[^}]*\}\s*\.nav-links a\s*\{[^}]*\}\s*\.nav-links a:hover\s*\{[^}]*\}\s*\.nav-phone\s*\{[^}]*\}\s*\.nav-phone:hover\s*\{[^}]*\}\s*',
        r'/\* Hamburger Button \*/\s*\.nav-hamburger\s*\{[^}]*\}\s*',
        r'/\* Mobile Menu Overlay \*/\s*#mobile-menu\s*\{[^}]*\}\s*#mobile-menu\.open\s*\{[^}]*\}\s*#mobile-menu a\s*\{[^}]*\}\s*#mobile-menu a:hover\s*\{[^}]*\}\s*\.mobile-menu-phone\s*\{[^}]*\}\s*\.mobile-menu-phone i\s*\{[^}]*\}\s*',
        r'/\* Desktop Nav Toggle \*/\s*@media\s*\(min-width:\s*769px\)\s*\{[^}]*\}\s*',
    ]
    for pat in old_css_patterns:
        match = re.search(pat, html, re.DOTALL)
        if match:
            html = html[:match.start()] + html[match.end():]
            changes.append(f"Removed old CSS: {pat[:40]}...")

    # Also remove the old DROPDOWN NAV CSS (the non-mega version)
    old_dropdown = re.search(
        r'/\* DROPDOWN NAV \*/.*?\.nav-dropdown-mega a\s*\{[^}]*\}',
        html, re.DOTALL
    )
    if old_dropdown:
        html = html[:old_dropdown.start()] + html[old_dropdown.end():]
        changes.append("Removed old DROPDOWN NAV CSS")

    # Remove the old .footer CSS block
    old_footer_css = re.search(
        r'/\* Footer \*/\s*\.footer\s*\{[^}]*\}\s*\.footer a\s*\{[^}]*\}\s*\.footer-inner\s*\{[^}]*\}\s*\.footer-logo\s*\{[^}]*\}\s*\.footer-attr\s*\{[^}]*\}',
        html, re.DOTALL
    )
    if old_footer_css:
        html = html[:old_footer_css.start()] + html[old_footer_css.end():]
        changes.append("Removed old .footer CSS")

    # ── 4f: Replace old mobile sticky ──
    old_sticky_match = re.search(
        r'<div class="mobile-sticky">.*?</div>',
        html, re.DOTALL
    )
    if old_sticky_match:
        html = html[:old_sticky_match.start()] + new_mobile_sticky + html[old_sticky_match.end():]
        changes.append("Replaced old mobile sticky with main site version")
    else:
        if 'fixed bottom-0' in html:
            changes.append("Mobile sticky already upgraded (skipped)")
        else:
            changes.append("WARNING: Could not find old mobile sticky bar")

    # ── 4g: Replace old script block ──
    old_script_match = re.search(
        r'<script>\s*document\.getElementById\([\'"]nav-menu-btn[\'"]\).*?</script>',
        html, re.DOTALL
    )
    if old_script_match:
        html = html[:old_script_match.start()] + new_script + html[old_script_match.end():]
        changes.append("Replaced old nav script with main site script")
    else:
        if 'menu-btn' in html and 'toggleMenu' in html:
            changes.append("Script already upgraded (skipped)")
        else:
            changes.append("WARNING: Could not find old script block to replace")

    # ── 4h: Add Tailwind CDN if not present ──
    if 'cdn.tailwindcss.com' not in html:
        # Insert before </head>
        tailwind_block = '''  <!-- Tailwind: Deferred -->
  <script src="https://cdn.tailwindcss.com" defer></script>
  <script type="tailwind-config">
    {
      "theme": {
        "extend": {
          "colors": {
            "brand": { "dark": "#0f172a", "primary": "#0056b3", "accent": "#fbbf24", "light": "#f1f5f9" }
          },
          "fontFamily": {
            "sans": ["Open Sans", "sans-serif"],
            "header": ["Oswald", "sans-serif"]
          }
        }
      }
    }
  </script>
'''
        html = html.replace('</head>', tailwind_block + '</head>')
        changes.append("Added Tailwind CDN + config")

    # ── 4i: Update body tag to match main site ──
    # Add font-sans, padding classes, overflow hidden
    old_body = re.search(r'<body[^>]*>', html)
    if old_body:
        body_tag = old_body.group(0)
        if 'font-sans' not in body_tag:
            # Replace the body tag with main-site-compatible version
            # Keep any existing attributes but add necessary classes
            new_body = '<body class="font-sans text-gray-800 antialiased w-full overflow-x-hidden pb-16 lg:pb-0 pt-[136px]">'
            html = html[:old_body.start()] + new_body + html[old_body.end():]
            changes.append("Updated <body> tag with main site classes (pt-[136px] for review bar + top bar + nav)")

    # ── 4j: Remove old body padding-top from CSS ──
    # The old CSS has body { ... padding-top: 96px; ... }
    # We now use Tailwind pt-[136px] on the body tag
    html = re.sub(r'(body\s*\{[^}]*?)padding-top:\s*96px;?', r'\1', html)
    html = re.sub(r'(body\s*\{[^}]*?)padding-bottom:\s*4rem;?', r'\1', html)

    # ── 4k: Remove old .mobile-sticky CSS (replaced by Tailwind) ──
    old_mobile_sticky_css = re.search(
        r'/\* Mobile Sticky CTA \*/\s*\.mobile-sticky\s*\{[^}]*\}',
        html, re.DOTALL
    )
    if old_mobile_sticky_css:
        html = html[:old_mobile_sticky_css.start()] + html[old_mobile_sticky_css.end():]
        changes.append("Removed old .mobile-sticky CSS")

    # Also remove .ms-call and .ms-text from mobile media query
    html = re.sub(r'\.mobile-sticky\s*\{[^}]*\}', '', html)
    html = re.sub(r'\.mobile-sticky\s+\.ms-call\s*\{[^}]*\}', '', html)
    html = re.sub(r'\.mobile-sticky\s+\.ms-text\s*\{[^}]*\}', '', html)

    # ── 4l: Remove old mobile @media overrides for nav ──
    # The old media query has .nav-links { display: none; } .nav-phone { display: none; } .nav-hamburger { display: block; }
    # These conflict with the new Tailwind-based responsive classes
    html = re.sub(r'\.nav-links\s*\{\s*display:\s*none;?\s*\}', '', html)
    html = re.sub(r'\.nav-phone\s*\{\s*display:\s*none;?\s*\}', '', html)
    html = re.sub(r'\.nav-hamburger\s*\{\s*display:\s*block;?\s*\}', '', html)

    if html != original:
        return html, changes
    else:
        return None, ["No changes needed"]


def main():
    print("=" * 60)
    print("Lincoln Park Roofing — Project Page Upgrader")
    print("=" * 60)
    print(f"Source page: {SOURCE_PAGE}")
    print(f"Projects dir: {PROJECTS_DIR}")
    print(f"Mode: {'DRY RUN (pass --apply to write)' if DRY_RUN else 'APPLYING CHANGES'}")
    print()

    if not os.path.exists(SOURCE_PAGE):
        print(f"ERROR: Source page not found: {SOURCE_PAGE}")
        sys.exit(1)

    # Read source and extract components
    src = read_source()

    mega_css = extract_mega_menu_css(src)
    desktop_nav = extract_desktop_nav(src)
    mobile_menu_html = extract_mobile_menu(src)
    review_bar = extract_review_bar(src)
    footer_html = extract_footer(src)
    mobile_sticky_html = extract_mobile_sticky(src)
    bottom_script = extract_bottom_script(src)

    print(f"Extracted mega menu CSS: {len(mega_css)} chars")
    print(f"Extracted desktop nav: {len(desktop_nav)} chars")
    print(f"Extracted mobile menu: {len(mobile_menu_html)} chars")
    print(f"Extracted review bar: {len(review_bar)} chars")
    print(f"Extracted footer: {len(footer_html)} chars")
    print(f"Extracted mobile sticky: {len(mobile_sticky_html)} chars")
    print(f"Extracted bottom script: {len(bottom_script)} chars")
    print()

    # Build the new header with ../  image paths
    new_header = build_new_header(review_bar, desktop_nav)

    # Fix image paths in footer for subdirectory
    new_footer = fix_image_paths_for_subdir(footer_html)

    # Mobile sticky and script don't have local image paths, use as-is
    new_mobile_sticky = mobile_sticky_html
    new_script = bottom_script

    # Find all project HTML files (skip index.html and this script)
    html_files = sorted(glob.glob(os.path.join(PROJECTS_DIR, "*.html")))
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]

    if not html_files:
        print("No project HTML files found (excluding index.html)")
        sys.exit(0)

    print(f"Found {len(html_files)} project pages to upgrade:")
    for f in html_files:
        print(f"  - {os.path.basename(f)}")
    print()

    # Process each file
    updated = 0
    skipped = 0
    errors = 0

    for filepath in html_files:
        basename = os.path.basename(filepath)
        print(f"Processing: {basename}")

        try:
            result, changes = process_file(
                filepath, mega_css, new_header, mobile_menu_html,
                new_footer, new_mobile_sticky, new_script
            )

            for c in changes:
                prefix = "  [!]" if c.startswith("WARNING") else "  [+]"
                print(f"{prefix} {c}")

            if result is not None:
                if not DRY_RUN:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(result)
                    print(f"  >>> WRITTEN")
                else:
                    print(f"  >>> Would write (dry run)")
                updated += 1
            else:
                print(f"  >>> No changes needed")
                skipped += 1

        except Exception as e:
            print(f"  [ERROR] {e}")
            errors += 1

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total files:   {len(html_files)}")
    print(f"  Updated:       {updated}")
    print(f"  Skipped:       {skipped}")
    print(f"  Errors:        {errors}")
    if DRY_RUN:
        print()
        print("  This was a DRY RUN. Run with --apply to write changes.")
    print()


if __name__ == "__main__":
    main()
