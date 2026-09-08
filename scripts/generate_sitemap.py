#!/usr/bin/env python3
"""
generate_sitemap.py — Production XML Sitemap Generator for tylerkoshakow.com

Scans the repository for canonical HTML pages, filters out redirects and utility
files (such as search engine verification tokens), extracts published/modified dates,
and produces a validated sitemap.xml adhering to sitemaps.org schema 0.9.
"""

import os
import re
import sys
import subprocess
from datetime import datetime, date
from pathlib import Path
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://tylerkoshakow.com"
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"

# Files or patterns to strictly ignore
IGNORED_PATTERNS = [
    r"^google[a-zA-Z0-9]+\.html$",  # Google site verification stubs
    r"^\.git",
    r"^\.vercel",
]


def is_ignored_file(filename: str) -> bool:
    for pattern in IGNORED_PATTERNS:
        if re.search(pattern, filename):
            return True
    return False


def get_git_lastmod(filepath: Path) -> str:
    """Fallback: Get last commit date for a file via git."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", str(filepath)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        val = result.stdout.strip()
        if val and re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            return val
    except Exception:
        pass
    
    # Fallback to filesystem mtime
    mtime = filepath.stat().st_mtime
    return date.fromtimestamp(mtime).isoformat()


def parse_page(filepath: Path):
    """
    Parses an HTML file to determine if it should be included in the sitemap.
    Returns (canonical_url, lastmod_date) or None if page should be excluded.
    """
    if is_ignored_file(filepath.name):
        return None

    content = filepath.read_text(encoding="utf-8", errors="ignore")

    # Exclude pages with meta refresh redirects
    if re.search(r'<meta\s+http-equiv=["\']refresh["\']', content, re.IGNORECASE):
        print(f"  [EXCLUDE] Skipping redirect stub: {filepath.relative_to(REPO_ROOT)}")
        return None

    # Extract canonical link
    canonical_match = re.search(
        r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
        content,
        re.IGNORECASE
    )
    if not canonical_match:
        # Fallback regex in case attributes are in different order
        canonical_match = re.search(
            r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']',
            content,
            re.IGNORECASE
        )

    if filepath.name == "index.html" and filepath.parent == REPO_ROOT:
        expected_canonical = f"{BASE_URL}/"
    else:
        rel_path = filepath.relative_to(REPO_ROOT).as_posix()
        expected_canonical = f"{BASE_URL}/{rel_path}"

    canonical_url = canonical_match.group(1).strip() if canonical_match else expected_canonical

    # If canonical points elsewhere (e.g. redirected or duplicate), skip it
    normalized_canonical = canonical_url.rstrip("/") or "/"
    normalized_expected = expected_canonical.rstrip("/") or "/"
    if normalized_canonical != normalized_expected:
        print(f"  [EXCLUDE] Canonical mismatch for {filepath.relative_to(REPO_ROOT)}: {canonical_url} != {expected_canonical}")
        return None

    # Extract lastmod date:
    # 1. Look for article:modified_time or article:published_time
    lastmod = None
    time_match = re.search(
        r'<meta\s+property=["\']article:(?:modified_time|published_time)["\']\s+content=["\']([^"\']+)["\']',
        content,
        re.IGNORECASE
    )
    if time_match:
        raw_date = time_match.group(1).strip()
        date_sub = re.match(r"^(\d{4}-\d{2}-\d{2})", raw_date)
        if date_sub:
            lastmod = date_sub.group(1)

    # 2. Look for JSON-LD dateModified or datePublished
    if not lastmod:
        json_date = re.search(r'["\']date(?:Modified|Published)["\']\s*:\s*["\'](\d{4}-\d{2}-\d{2})["\']', content)
        if json_date:
            lastmod = json_date.group(1)

    # 3. Fallback to git lastmod
    if not lastmod:
        lastmod = get_git_lastmod(filepath)

    return (canonical_url, lastmod)


def collect_urls():
    """Collects all canonical URLs from the site."""
    entries = []

    # 1. Root index.html
    root_index = REPO_ROOT / "index.html"
    if root_index.exists():
        parsed = parse_page(root_index)
        if parsed:
            entries.append(parsed)

    # 2. Signals directory
    signals_dir = REPO_ROOT / "signals"
    if signals_dir.exists():
        for html_file in sorted(signals_dir.glob("*.html")):
            parsed = parse_page(html_file)
            if parsed:
                entries.append(parsed)

    # If root index lastmod should reflect the newest signal date:
    if entries and entries[0][0] == f"{BASE_URL}/":
        root_url = entries[0][0]
        other_dates = [e[1] for e in entries[1:] if e[1]]
        if other_dates:
            newest_date = max(other_dates)
            entries[0] = (root_url, newest_date)

    return entries


def generate_sitemap_xml(entries):
    """Generates formatted XML string for sitemap.xml."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for loc, lastmod in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")

    lines.append("</urlset>")
    lines.append("")  # Trailing newline
    return "\n".join(lines)


def main():
    print(f"Scanning {REPO_ROOT} for canonical HTML pages...")
    entries = collect_urls()

    print(f"Discovered {len(entries)} valid sitemap entries:")
    for loc, lastmod in entries:
        print(f"  + {loc} (lastmod: {lastmod})")

    xml_content = generate_sitemap_xml(entries)

    # Validate with ElementTree
    try:
        ET.fromstring(xml_content.encode("utf-8"))
    except ET.ParseError as e:
        print(f"ERROR: Generated XML failed validation: {e}", file=sys.stderr)
        sys.exit(1)

    SITEMAP_PATH.write_text(xml_content, encoding="utf-8")
    print(f"\nSuccessfully wrote verified sitemap to {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
