#!/usr/bin/env python3
"""
Search Intelligence Tool
Reusable CLI and module for reverse-engineering competitor SERPs, extracting ranked keywords and ETV via DataForSEO,
scraping heading trees with persistent reference IDs, and publishing natively formatted Google Docs briefs with clickable anchors.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import re
import html

TOKEN_FILE = "/Users/tylerkoshakow/Documents/antigravity/Screaming Frog Audit/google_workspace_mcp/token.json"
ENV_FILE = "/Users/tylerkoshakow/Documents/antigravity/Screaming Frog Audit/.env"

def load_dataforseo_auth():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                if line.startswith("DATAFORSEO_BASIC_AUTH="):
                    return line.strip().split("=", 1)[1]
    return "dHlsZXIua29zaGFrb3dAaGV4YWdvbi5jb206NTBmZjU1NWMwOTFlYzljNA=="

def get_google_token():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"Google Workspace token file not found at {TOKEN_FILE}")
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)
    payload = urllib.parse.urlencode({
        "client_id": token_data["client_id"],
        "client_secret": token_data["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token"
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=payload)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())["access_token"]

def get_keyword_volumes(keywords):
    auth = load_dataforseo_auth()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    post_data = json.dumps([{"keywords": keywords, "location_code": 2840, "language_code": "en"}]).encode('utf-8')
    req = urllib.request.Request("https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live", data=post_data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        results = {}
        for item in data.get("tasks", [])[0].get("result", []):
            kw = item.get("keyword")
            results[kw] = {
                "search_volume": item.get("search_volume"),
                "cpc": item.get("cpc"),
                "competition": item.get("competition")
            }
        return results

def get_live_serp(query, depth=20):
    auth = load_dataforseo_auth()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    post_data = json.dumps([{"keyword": query, "location_code": 2840, "language_code": "en", "depth": depth}]).encode('utf-8')
    req = urllib.request.Request("https://api.dataforseo.com/v3/serp/google/organic/live/regular", data=post_data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        items = data.get("tasks", [])[0].get("result", [])[0].get("items", [])
        return items

def extract_headings(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    raw_html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
    clean_html = re.sub(r'<script[^>]*>.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
    matches = re.findall(r'<(h[1-3])[^>]*>(.*?)</\1>', clean_html, re.IGNORECASE | re.DOTALL)
    cleaned = []
    for tag, text in matches:
        t = re.sub(r'<[^>]+>', '', text)
        t = html.unescape(re.sub(r'\s+', ' ', t).strip())
        if t and not any(nav in t.lower() for nav in ["menu", "navigation", "footer", "cookie", "privacy policy"]):
            cleaned.append((tag.upper(), t))
    return cleaned

def publish_html_to_google_doc(doc_id, html_content):
    token = get_google_token()
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/drive/v3/files/{doc_id}?uploadType=media",
        data=html_content.encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/html"},
        method="PATCH"
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        return res.get("id")

if __name__ == "__main__":
    print("Search Intelligence Tool Loaded. Module ready.")
