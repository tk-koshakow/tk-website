#!/usr/bin/env python3
"""
Site Telemetry Puller (GSC & GA4)
Pulls performance data from Google Search Console and Google Analytics 4
using the Antigravity Google Workspace OAuth credentials.
"""

import argparse
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

WORKSPACE_MCP_DIR = os.path.expanduser("~/Documents/antigravity/Screaming Frog Audit/google_workspace_mcp")
TOKEN_FILE = os.path.join(WORKSPACE_MCP_DIR, "token.json")
DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "telemetry_latest.json")

def load_and_refresh_token():
    if not os.path.exists(TOKEN_FILE):
        print(f"[ERROR] token.json not found at {TOKEN_FILE}. Run auth.py first.", file=sys.stderr)
        sys.exit(1)
    
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
    
    # Check expiry
    expires_at = token_data.get("expires_at", 0)
    # Refresh if expired or within 60 seconds of expiry
    now_ms = int(datetime.datetime.now().timestamp() * 1000)
    if now_ms >= expires_at and token_data.get("refresh_token"):
        print("[INFO] Refreshing access token...", file=sys.stderr)
        refresh_params = urllib.parse.urlencode({
            "client_id": token_data["client_id"],
            "client_secret": token_data["client_secret"],
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")
        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=refresh_params, headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(req) as resp:
                new_tokens = json.loads(resp.read().decode())
                token_data["access_token"] = new_tokens["access_token"]
                token_data["expires_at"] = now_ms + ((new_tokens.get("expires_in", 3600) - 120) * 1000)
                with open(TOKEN_FILE, "w") as f:
                    json.dump(token_data, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to refresh token: {e}", file=sys.stderr)
            sys.exit(1)
            
    return token_data["access_token"]

def google_api_request(url, access_token, method="GET", body=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"[ERROR] API request failed [{e.code}]: {error_body}", file=sys.stderr)
        return {"error": e.code, "message": error_body}

def fetch_gsc_sites(access_token):
    return google_api_request("https://www.googleapis.com/webmasters/v3/sites", access_token)

def fetch_gsc_performance(access_token, site_url, start_date, end_date):
    encoded_site = urllib.parse.quote(site_url, safe="")
    url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query", "page"],
        "rowLimit": 1000,
        "type": "web"
    }
    return google_api_request(url, access_token, method="POST", body=body)

def fetch_ga4_properties(access_token):
    return google_api_request("https://analyticsadmin.googleapis.com/v1beta/accountSummaries", access_token)

def fetch_ga4_report(access_token, property_id, start_date, end_date):
    prop_id = property_id if property_id.startswith("properties/") else f"properties/{property_id}"
    url = f"https://analyticsdata.googleapis.com/v1beta/{prop_id}:runReport"
    body = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "engagementRate"},
            {"name": "averageSessionDuration"}
        ],
        "limit": 100
    }
    return google_api_request(url, access_token, method="POST", body=body)

def main():
    parser = argparse.ArgumentParser(description="Pull Search Console and GA4 telemetry data.")
    parser.add_argument("--days", type=int, default=28, help="Number of days to look back (default: 28)")
    parser.add_argument("--site", type=str, default=None, help="GSC Site URL (e.g., sc-domain:tylerkoshakow.com)")
    parser.add_argument("--ga4", type=str, default=None, help="GA4 Property ID (e.g., 123456789)")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="Output JSON file path")
    args = parser.parse_args()

    token = load_and_refresh_token()

    end_d = datetime.date.today() - datetime.timedelta(days=1)
    start_d = end_d - datetime.timedelta(days=args.days)
    start_date_str = start_d.strftime("%Y-%m-%d")
    end_date_str = end_d.strftime("%Y-%m-%d")

    telemetry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "date_range": {"start_date": start_date_str, "end_date": end_date_str},
        "search_console": None,
        "ga4": None
    }

    # GSC Processing
    site_url = args.site
    if not site_url:
        print("[INFO] Checking GSC verified sites...", file=sys.stderr)
        sites_res = fetch_gsc_sites(token)
        if "siteEntry" in sites_res and sites_res["siteEntry"]:
            site_entries = sites_res["siteEntry"]
            # Look for tylerkoshakow
            for entry in site_entries:
                if "tylerkoshakow" in entry.get("siteUrl", ""):
                    site_url = entry["siteUrl"]
                    break
            if not site_url and site_entries:
                site_url = site_entries[0]["siteUrl"]

    if site_url:
        print(f"[INFO] Pulling GSC analytics for '{site_url}' ({start_date_str} to {end_date_str})...", file=sys.stderr)
        gsc_data = fetch_gsc_performance(token, site_url, start_date_str, end_date_str)
        telemetry["search_console"] = {
            "site_url": site_url,
            "data": gsc_data
        }
    else:
        print("[WARN] No GSC site found or specified.", file=sys.stderr)

    # GA4 Processing
    ga4_prop = args.ga4
    if not ga4_prop:
        print("[INFO] Checking GA4 properties...", file=sys.stderr)
        prop_res = fetch_ga4_properties(token)
        if "accountSummaries" in prop_res:
            for acc in prop_res["accountSummaries"]:
                for prop in acc.get("propertySummaries", []):
                    if "tyler" in prop.get("displayName", "").lower() or "tk" in prop.get("displayName", "").lower():
                        ga4_prop = prop["property"]
                        break
                if ga4_prop:
                    break
            if not ga4_prop and prop_res["accountSummaries"]:
                first_acc = prop_res["accountSummaries"][0]
                if first_acc.get("propertySummaries"):
                    ga4_prop = first_acc["propertySummaries"][0]["property"]

    if ga4_prop:
        print(f"[INFO] Pulling GA4 report for '{ga4_prop}' ({start_date_str} to {end_date_str})...", file=sys.stderr)
        ga4_data = fetch_ga4_report(token, ga4_prop, start_date_str, end_date_str)
        telemetry["ga4"] = {
            "property": ga4_prop,
            "data": ga4_data
        }
    else:
        print("[WARN] No GA4 property found or specified.", file=sys.stderr)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(telemetry, f, indent=2)

    print(f"[SUCCESS] Telemetry snapshot saved to {args.output}")

if __name__ == "__main__":
    main()
