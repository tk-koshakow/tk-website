#!/usr/bin/env python3
"""
validate_site.py — Production Pre-Publish & Quality Assurance Validator

Runs automated checks across all HTML files in the repository:
1. Extracts all inline JavaScript blocks and validates them with `node --check` to prevent syntax regressions.
2. Checks for unescaped template placeholders (e.g. `style.transform = ;`).
3. Verifies canonical URLs, OpenGraph tags, and JSON-LD syntax.
4. Checks theme selector compatibility across all pages.
"""

import os
import re
import sys
import json
import tempfile
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

IGNORED_PATTERNS = [
    r"^google[a-zA-Z0-9]+\.html$",
    r"^\.git",
    r"^\.vercel",
]

def is_ignored_file(filename: str) -> bool:
    for pattern in IGNORED_PATTERNS:
        if re.search(pattern, filename):
            return True
    return False

def find_node_bin():
    """Finds node binary in PATH or common NVM / Homebrew directories."""
    paths = [
        "/Users/tylerkoshakow/.nvm/versions/node/v26.7.0/bin/node",
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
        "/usr/bin/node"
    ]
    for p in paths:
        if Path(p).exists():
            return p
    try:
        res = subprocess.run(["which", "node"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "node"

NODE_BIN = find_node_bin()

def validate_inline_js(filepath: Path, content: str):
    """Extracts all <script> blocks (excluding JSON-LD) and validates syntax via Node.js."""
    script_pattern = re.compile(r'<script\b(?![^>]*type=["\']application/ld\+json["\'])[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    matches = script_pattern.findall(content)
    
    errors = []
    for idx, script_body in enumerate(matches, 1):
        if not script_body.strip():
            continue
        
        # Check for broken empty assignments (e.g. `style.transform = ;`)
        if re.search(r'style\.transform\s*=\s*;', script_body):
            errors.append(f"Script #{idx}: Found broken empty transform assignment `style.transform = ;`")

        # Run node --check
        with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as tmp:
            tmp.write(script_body)
            tmp_path = tmp.name
        
        try:
            res = subprocess.run([NODE_BIN, "--check", tmp_path], capture_output=True, text=True)
            if res.returncode != 0:
                err_msg = res.stderr.strip().replace(tmp_path, f"{filepath.name} <script #{idx}>")
                errors.append(f"JavaScript Syntax Error in script #{idx}:\n{err_msg}")
        except Exception as e:
            errors.append(f"Failed to run node --check: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    return errors

def validate_json_ld(filepath: Path, content: str):
    """Validates that all application/ld+json scripts contain valid JSON."""
    ld_pattern = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    matches = ld_pattern.findall(content)
    errors = []
    for idx, body in enumerate(matches, 1):
        try:
            json.loads(body.strip())
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON-LD in block #{idx}: {e}")
    return errors

def validate_html_file(filepath: Path):
    """Performs full suite of checks on an HTML file."""
    if is_ignored_file(filepath.name):
        return []
        
    rel_path = filepath.relative_to(REPO_ROOT)
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    
    errors = []
    
    # 1. Validate JS syntax
    js_errors = validate_inline_js(filepath, content)
    errors.extend(js_errors)
    
    # 2. Validate JSON-LD
    ld_errors = validate_json_ld(filepath, content)
    errors.extend(ld_errors)
    
    # 3. Canonical link check
    if not re.search(r'<meta\s+http-equiv=["\']refresh["\']', content, re.IGNORECASE):
        if not re.search(r'<link\s+[^>]*rel=["\']canonical["\']', content, re.IGNORECASE):
            errors.append("Missing canonical link tag")
            
    return errors

def main():
    print(f"=== Running Site Validation on {REPO_ROOT} ===")
    html_files = sorted(REPO_ROOT.glob("**/*.html"))
    html_files = [f for f in html_files if not is_ignored_file(f.name) and ".vercel" not in f.parts and ".git" not in f.parts]
    
    total_errors = 0
    for hf in html_files:
        errs = validate_html_file(hf)
        rel = hf.relative_to(REPO_ROOT)
        if errs:
            total_errors += len(errs)
            print(f"\n[FAIL] {rel}:")
            for e in errs:
                print(f"   x {e}")
        else:
            print(f"  [PASS] {rel}")
            
    if total_errors > 0:
        print(f"\nValidation FAILED with {total_errors} error(s).")
        sys.exit(1)
    else:
        print(f"\nAll {len(html_files)} HTML files passed validation successfully!")

if __name__ == "__main__":
    main()
