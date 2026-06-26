import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.se_monitor.data import download_sheet, compute_kab_stats, compute_timeline

def main():
    sheet_map, csv_text, data_source_info = download_sheet()
    kab_data, kab_list, prov_agg = compute_kab_stats(csv_text)
    
    print("Rank | Kabupaten/Kota | Target | Worked % | Done % | Approval % | Est. Selesai")
    print("-" * 90)
    for idx, (kab, m) in enumerate(kab_list, 1):
        elapsed_days, _, expected_pct = compute_timeline()
        from scripts.kb.se_monitor.data import get_est_completion
        est = get_est_completion(m["completed_rate"] * 100, elapsed_days)
        # strip ansi
        import re
        est_clean = re.sub(r'\033\[[0-9;]*m', '', est)
        
        print(f"{idx} | {kab} | {m['target']} | {m['worked_rate']*100:.2f}% | {m['completed_rate']*100:.2f}% | {m['approval_rate']*100:.2f}% | {est_clean}")
    
    est_prov = get_est_completion(prov_agg["done_rate"] * 100, elapsed_days)
    est_prov_clean = re.sub(r'\033\[[0-9;]*m', '', est_prov)
    print("-" * 90)
    print(f"TOTAL KALBAR | {prov_agg['target']} | {prov_agg['worked_rate']*100:.2f}% | {prov_agg['done_rate']*100:.2f}% | {prov_agg['approval_rate']*100:.2f}% | {est_prov_clean}")

if __name__ == "__main__":
    main()
