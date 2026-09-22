#!/usr/bin/env python3
"""
run_gtm_benchmark.py
Automated benchmark runner that:
1. Starts a local HTTP server.
2. Runs Lighthouse 13.5 (mobile emulation, throttled CPU/network) against each variant.
3. Captures full JSON/HTML reports and generates screenshots.
4. Outputs a consolidated comparison table.
"""

import os
import sys
import time
import json
import subprocess
import http.server
import socketserver
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "experiments" / "gtm-benchmark" / "reports"
SCREENSHOTS_DIR = REPO_ROOT / "images" / "benchmarks"
PORT = 8089

VARIANTS = [
    {
        "id": "variant-a-baseline",
        "name": "Variant A: Control (Sequenced GA4)",
        "path": "experiments/gtm-benchmark/variant-a-baseline.html"
    },
    {
        "id": "variant-b-gtm-standard",
        "name": "Variant B: Standard Client-Side GTM",
        "path": "experiments/gtm-benchmark/variant-b-gtm-standard.html"
    },
    {
        "id": "variant-c-gtm-bloat",
        "name": "Variant C: GTM with Marketing Tag Bloat (Meta + LinkedIn)",
        "path": "experiments/gtm-benchmark/variant-c-gtm-bloat.html"
    },
    {
        "id": "variant-d1-gtm-sequenced",
        "name": "Variant D1: Interaction-Sequenced GTM ($0)",
        "path": "experiments/gtm-benchmark/variant-d1-gtm-sequenced.html"
    },
    {
        "id": "variant-d2-edge-proxy",
        "name": "Variant D2: Edge Proxy / Server-Side ($0)",
        "path": "experiments/gtm-benchmark/variant-d2-edge-proxy.html"
    }
]

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def start_server():
    os.chdir(str(REPO_ROOT))
    httpd = socketserver.TCPServer(("", PORT), QuietHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

def capture_screenshot(url, output_png):
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=412,823",  # Moto G Power viewport
        f"--screenshot={output_png}",
        url
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
    except Exception as e:
        print(f"[WARN] Screenshot failed for {url}: {e}", file=sys.stderr)

def run_lighthouse(url, report_prefix):
    json_path = f"{report_prefix}.report.json"
    html_path = f"{report_prefix}.report.html"
    
    node_bin_dir = "/Users/tylerkoshakow/.nvm/versions/node/v26.7.0/bin"
    env = os.environ.copy()
    env["PATH"] = f"{node_bin_dir}:{env.get('PATH', '')}"
    
    cmd = [
        f"{node_bin_dir}/npx",
        "--yes",
        "lighthouse",
        url,
        "--form-factor=mobile",
        "--throttling-method=devtools",
        "--screenEmulation.mobile=true",
        "--screenEmulation.width=412",
        "--screenEmulation.height=823",
        "--screenEmulation.deviceScaleFactor=1.75",
        "--output=json,html",
        f"--output-path={report_prefix}",
        "--chrome-flags=--headless --disable-gpu --no-sandbox"
    ]
    
    print(f"[INFO] Running Lighthouse on {url}...", file=sys.stderr)
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Lighthouse failed: {res.stderr}", file=sys.stderr)
        return None
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    return None

def extract_metrics(lh_data):
    if not lh_data:
        return {}
    audits = lh_data.get("audits", {})
    categories = lh_data.get("categories", {})
    
    perf_score = int(round((categories.get("performance", {}).get("score", 0) or 0) * 100))
    fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")
    lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
    tbt = audits.get("total-blocking-time", {}).get("displayValue", "0 ms")
    cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "0")
    si = audits.get("speed-index", {}).get("displayValue", "N/A")
    
    # Main thread work
    bootup = audits.get("bootup-time", {}).get("displayValue", "0 ms")
    total_js = audits.get("total-byte-weight", {}).get("displayValue", "N/A")
    
    return {
        "score": perf_score,
        "fcp": fcp,
        "lcp": lcp,
        "tbt": tbt,
        "cls": cls,
        "speed_index": si,
        "main_thread_work": bootup,
        "total_weight": total_js
    }

def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    httpd = start_server()
    print(f"[INFO] Local server listening on http://localhost:{PORT}", file=sys.stderr)
    time.sleep(1)
    
    results = []
    
    for v in VARIANTS:
        url = f"http://localhost:{PORT}/{v['path']}"
        report_prefix = str(REPORTS_DIR / v["id"])
        screenshot_path = str(SCREENSHOTS_DIR / f"{v['id']}.png")
        
        # Capture screenshot
        capture_screenshot(url, screenshot_path)
        
        # Run Lighthouse
        lh_data = run_lighthouse(url, report_prefix)
        metrics = extract_metrics(lh_data)
        
        v_result = {
            "id": v["id"],
            "name": v["name"],
            "metrics": metrics,
            "screenshot": str(Path("images/benchmarks") / f"{v['id']}.png")
        }
        results.append(v_result)
        print(f"[DONE] {v['name']} -> Score: {metrics.get('score')} | TBT: {metrics.get('tbt')} | LCP: {metrics.get('lcp')}")
    
    # Save consolidated summary
    summary_path = REPO_ROOT / "experiments" / "gtm-benchmark" / "benchmark_summary.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "="*80)
    print(" EMPIRICAL GTM BENCHMARK RESULTS")
    print("="*80)
    print(f"{'Configuration':<45} | {'Score':<6} | {'TBT':<8} | {'FCP':<8} | {'LCP':<8}")
    print("-" * 80)
    for r in results:
        m = r["metrics"]
        print(f"{r['name']:<45} | {m.get('score', 0):<6} | {m.get('tbt', 'N/A'):<8} | {m.get('fcp', 'N/A'):<8} | {m.get('lcp', 'N/A'):<8}")
    print("="*80)

if __name__ == "__main__":
    main()
