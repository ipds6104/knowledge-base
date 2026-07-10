import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Reconfigure stdout to support UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.colors import Colors
from scripts.kb.se_monitor.data import (
    download_sheet,
    aggregate_metrics,
    compute_timeline,
    TARGET_DATE,
    download_alokasi
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    download_alokasi()

    sheet_map, csv_text, data_source_info = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    elapsed_days, _, expected_pct = compute_timeline()
    today = datetime.now().date()

    ppl_list = []
    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            for ppl, sls_list in ppls.items():
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                worked_pct = ppl_m["worked_rate"] * 100
                
                # Hitung estimasi selesai berdasarkan worked_rate
                if elapsed_days > 0 and worked_pct > 0:
                    daily_speed = worked_pct / elapsed_days
                    days_needed = (100.0 - worked_pct) / daily_speed
                    est_date = today + timedelta(days=days_needed)
                    est_str = est_date.strftime("%d %b %Y")
                else:
                    est_date = None
                    est_str = "Tdk Terproyeksi"

                # Extract kecamatan from sls_info
                kec = "Kecamatan Lain"
                if sls_list and sls_list[0] in sls_info:
                    kec = sls_info[sls_list[0]].get("kecamatan", "Kecamatan Lain")

                ppl_list.append({
                    "name": ppl,
                    "pml": pml,
                    "pj": pj,
                    "kecamatan": kec,
                    "target": ppl_m["target"],
                    "completed": ppl_m["completed"],
                    "worked": ppl_m["worked"],
                    "worked_pct": worked_pct,
                    "done_pct": done_pct,
                    "est_str": est_str,
                })

    # Sort exactly by worked_pct ascending. If same, sort by target descending.
    ppl_list.sort(key=lambda x: (x["worked_pct"], -x["target"]))

    print("### WORST WORKED PPL LIST")
    print(json.dumps({
        "expected_pct": expected_pct,
        "elapsed_days": elapsed_days,
        "ppls": ppl_list[:20]  # Get top 20 worst by worked%
    }, indent=2))

if __name__ == "__main__":
    main()
