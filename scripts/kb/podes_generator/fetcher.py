"""CSV Fetcher Module for BPS Potensi Desa (PODES) Live Google Sheets."""

import csv
import io
import urllib.request
from typing import Dict, List, Any
from .config import PODES_SHEET_ID


def fetch_podes_raw_csv(sheet_id: str = PODES_SHEET_ID) -> List[Dict[str, str]]:
    """Mengunduh berkas CSV live dari Google Sheet Potensi Desa 2025."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    print(f"Mengunduh data live PODES 2025 Google Sheet (ID: {sheet_id})...")
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

    if not rows or len(rows) < 2:
        raise ValueError("Gagal mengunduh atau data Google Sheet PODES kosong.")

    headers = [h.strip() for h in rows[0]]
    result = []

    for row_idx, r in enumerate(rows[1:], 1):
        if not any(r):
            continue
        row_dict = {}
        for col_idx, val in enumerate(r):
            if col_idx < len(headers):
                row_dict[headers[col_idx]] = val.strip()
        result.append(row_dict)

    print(f"  -> Terunduh {len(result)} indikator Potensi Desa 2025.")
    return result


def fetch_podes_data(config: dict) -> List[Dict[str, str]]:
    """Fungsi pembungkus untuk mengambil data PODES."""
    sheet_id = config.get("sheet_id", PODES_SHEET_ID)
    return fetch_podes_raw_csv(sheet_id)
