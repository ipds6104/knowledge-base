"""Generic Google Sheets & AppSheet Ingestion Module for DDA Generator.

Fetches live CSV data from Google Sheets based on village-specific sheet IDs and sheet tab names.
"""

import csv
import io
import json
import urllib.parse
import urllib.request
from pathlib import Path


def fetch_sheet_tab_by_name(sheet_id: str, tab_name: str) -> list:
    """Menarik data tab CSV dari Google Sheets berdasarkan sheet_id dan tab_name."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(tab_name)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    return [{k.strip(): (v.strip() if v else "") for k, v in row.items()} for row in reader]


def fetch_desa_data(config: dict) -> tuple:
    """Menarik dataset RT/CAPI dan Fasilitas untuk desa secara eksplisit sesuai sheet_id dan nama tab di config."""
    sheet_id = config.get("sheet_id", "")
    rt_tab = config.get("rt_tab", "Sheet1")
    fas_tab = config.get("fas_tab", "Sheet4")

    rt_data = []
    fas_data = []

    if sheet_id:
        try:
            print(f"Mengunduh data live Google Sheets (ID: {sheet_id})...")
            if rt_tab:
                rt_data = fetch_sheet_tab_by_name(sheet_id, rt_tab)
                print(f"  -> {rt_tab}: {len(rt_data)} baris")

            if fas_tab:
                fas_data = fetch_sheet_tab_by_name(sheet_id, fas_tab)
                print(f"  -> {fas_tab}: {len(fas_data)} baris")
            else:
                print("  -> Tidak ada pendataan Fasilitas Umum (fas_tab kosong).")

        except Exception as e:
            print(f"Gagal mengunduh live Google Sheet ({e}). Menggunakan cache lokal jika ada...")

    # Fallback to local cache if empty
    if not rt_data:
        cache_path = Path("scratch") / "sbk_rt_live.json"
        if cache_path.exists():
            with open(cache_path, "r", encoding="utf-8") as f:
                rt_data = json.load(f)
            print(f"Loaded {len(rt_data)} RT records from local cache.")

    if fas_tab and not fas_data:
        cache_path = Path("scratch") / "sbk_fas_live.json"
        if cache_path.exists():
            with open(cache_path, "r", encoding="utf-8") as f:
                fas_data = json.load(f)

    return rt_data, fas_data
