#!/usr/bin/env python3
"""
Helper script untuk mengeksekusi kueri SurrealDB dari lingkungan Aina.
Database host: 100.88.216.97:8900 (Tailscale)
Namespace: bps_mempawah
Database: se2026
"""

import sys
import json
import argparse
import urllib.request
import base64

SURREAL_URL = "http://100.88.216.97:8900/sql"
SURREAL_NS = "bps_mempawah"
SURREAL_DB = "se2026"
AUTH_USER = "root"
AUTH_PASS = "root"

def run_query(sql: str):
    auth_str = f"{AUTH_USER}:{AUTH_PASS}"
    auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "surreal-ns": SURREAL_NS,
        "surreal-db": SURREAL_DB,
        "Accept": "application/json",
        "Content-Type": "text/plain"
    }

    req = urllib.request.Request(SURREAL_URL, data=sql.encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Query SurrealDB SE2026")
    parser.add_argument("query", help="SurrealQL / SQL query string")
    parser.add_argument("--json", action="store_true", help="Print raw JSON response")
    args = parser.parse_args()

    res = run_query(args.query)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if isinstance(res, list) and len(res) > 0:
        for idx, item in enumerate(res):
            status = item.get("status")
            time_taken = item.get("time")
            result = item.get("result")
            print(f"[{idx+1}] Status: {status} ({time_taken})")
            if isinstance(result, list):
                print(f"Total rows: {len(result)}")
                for r in result[:10]:
                    print(r)
                if len(result) > 10:
                    print(f"... dan {len(result) - 10} baris lainnya.")
            else:
                print(result)
    else:
        print(res)

if __name__ == "__main__":
    main()
