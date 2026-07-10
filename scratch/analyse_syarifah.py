import sys
import json
from pathlib import Path

# Reconfigure stdout to support UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.se_monitor.data import (
    download_sheet,
    aggregate_metrics,
    download_alokasi
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    download_alokasi()
    sheet_map, _, _ = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    target_pml = "Syarifah Desti Pratiwi"
    
    # Map PPL to SLS under Syarifah Desti Pratiwi
    pml_ppl_to_sls = {}
    pml_to_pj = None

    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            if pml == target_pml:
                pml_to_pj = pj
                for ppl, sls_list in ppls.items():
                    pml_ppl_to_sls[ppl] = sls_list

    if not pml_ppl_to_sls:
        print(f"Error: PML '{target_pml}' tidak ditemukan.")
        return

    print(f"=== TIM PML: {target_pml} (PJ: {pml_to_pj}) ===")
    
    ppl_results = []
    total_target = 0
    total_completed = 0
    total_draft = 0
    total_open = 0

    for ppl, sls_list in pml_ppl_to_sls.items():
        ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
        done_pct = ppl_m["completed_rate"] * 100
        worked_pct = ppl_m["worked_rate"] * 100
        
        # Hitung sisa dokumen untuk mencapai 20%
        target_20_pct = ppl_m["target"] * 0.20
        needed_to_20_pct = max(0, int(target_20_pct) - ppl_m["completed"])
        
        total_target += ppl_m["target"]
        total_completed += ppl_m["completed"]
        total_draft += ppl_m["draft"]
        total_open += ppl_m["open"]

        ppl_results.append({
            "name": ppl,
            "target": ppl_m["target"],
            "completed": ppl_m["completed"],
            "draft": ppl_m["draft"],
            "open": ppl_m["open"],
            "submit": ppl_m["submitted"],
            "approve": ppl_m["approved"],
            "done_pct": done_pct,
            "worked_pct": worked_pct,
            "target_20_pct": int(target_20_pct),
            "needed_to_20_pct": needed_to_20_pct
        })

    # Urutkan berdasarkan Done % terkecil
    ppl_results.sort(key=lambda x: x["done_pct"])

    overall_pct = (total_completed / total_target) * 100 if total_target > 0 else 0.0
    overall_needed = max(0, int(total_target * 0.20) - total_completed)

    print(json.dumps({
        "overall": {
            "target": total_target,
            "completed": total_completed,
            "draft": total_draft,
            "open": total_open,
            "done_pct": overall_pct,
            "needed_to_20_pct": overall_needed
        },
        "ppls": ppl_results
    }, indent=2))

if __name__ == "__main__":
    main()
