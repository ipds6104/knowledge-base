import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.se_monitor.data import (
    download_sheet, aggregate_metrics, compute_timeline,
    get_est_completion, TARGET_DATE
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def clean_ansi(t):
    return re.sub(r'\033\[[0-9;]*m', '', t)

def get_status_emoji(pct, expected_pct):
    if pct >= max(10.0, expected_pct * 0.70): return "🟢"
    if pct < max(3.0, expected_pct * 0.25):   return "🔴"
    return "🟡"

def main():
    sheet_map, _, data_src = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    if not has_alokasi:
        print("Error: Alokasi Petugas.csv tidak ditemukan."); return

    elapsed_days, total_days, expected_pct = compute_timeline()

    # Build maps
    pml_to_sls   = {}
    pml_ppl_to_sls = {}
    pml_to_pj    = {}
    pml_to_kecs  = {}

    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            pml_to_pj[pml] = pj
            for ppl, sls_list in ppls.items():
                pml_to_sls.setdefault(pml, []).extend(sls_list)
                pml_ppl_to_sls.setdefault((pml, ppl), []).extend(sls_list)
                for idsls in sls_list:
                    pml_to_kecs.setdefault(pml, set()).add(
                        sls_info[idsls].get("kecamatan", ""))

    # Compute all PML metrics
    pml_metrics = {pml: aggregate_metrics(sls, sls_info, sheet_map)
                   for pml, sls in pml_to_sls.items()}

    total_pmls = len(pml_metrics)
    sorted_by_done = sorted(pml_metrics.items(),
                            key=lambda x: x[1]["completed_rate"], reverse=True)
    done_ranks   = {k: i+1 for i, (k,_) in enumerate(sorted_by_done)}
    worked_ranks = {k: i+1 for i, (k,_) in enumerate(
        sorted(pml_metrics.items(), key=lambda x: x[1]["worked_rate"], reverse=True))}

    top_pml  = sorted_by_done[0][0]
    bot_pml  = sorted_by_done[-1][0]

    avg_target    = sum(m["target"] for m in pml_metrics.values()) / total_pmls
    avg_done      = sum(m["completed_rate"] for m in pml_metrics.values()) / total_pmls
    avg_worked    = sum(m["worked_rate"] for m in pml_metrics.values()) / total_pmls
    all_app = sum(m["approved"] for m in pml_metrics.values())
    all_sub = sum(m["submitted"] for m in pml_metrics.values())
    avg_approval  = all_app / (all_app + all_sub) if (all_app + all_sub) > 0 else 0.0
    avg_pending   = sum(m["submitted"] for m in pml_metrics.values()) / total_pmls
    avg_daily_tgt = sum(m["pml_daily_target"] for m in pml_metrics.values()) / total_pmls

    targets = ["Abang Handri", top_pml, bot_pml]
    # Remove duplicates while preserving order
    seen = set()
    targets = [x for x in targets if not (x in seen or seen.add(x))]

    print(f"\n{'='*100}")
    print(f"   ANALISIS PERBANDINGAN PML — {datetime.now().strftime('%d %B %Y, pukul %H:%M WIB')}")
    print(f"   Hari ke-{elapsed_days} dari {total_days} hari lapangan | Target Ideal: {expected_pct:.2f}%")
    print(f"{'='*100}")

    # ─── TABEL 1: KLASEMEN MAKRO ──────────────────────────────────────────────
    print(f"\n{'─'*100}")
    print(f" 📊 TABEL 1: PERBANDINGAN MAKRO PML")
    print(f"{'─'*100}")

    col_w = 22
    header = f"{'Metrik':<35}"
    for t in targets:
        label = f"{'🏆 '+t if t==top_pml else ('⚠️ '+t if t=='Abang Handri' else '🔴 '+t)}"
        header += f"{label:<{col_w}}"
    header += f"{'Rata-rata Kab':<16}"
    print(header)
    print("─" * (35 + col_w * len(targets) + 16))

    def row(label, vals, avg_val, fmt=lambda v: v):
        line = f"  {label:<33}"
        for v in vals:
            line += f"{str(fmt(v)):<{col_w}}"
        line += f"{str(fmt(avg_val)):<16}"
        print(line)

    # Target Unit
    row("Target Unit",
        [pml_metrics[t]["target"] for t in targets], f"{avg_target:.0f}")

    # Completed Rate (Done %)
    r = f"Completed Rate (Done %) "
    line = f"  {r:<33}"
    for t in targets:
        m = pml_metrics[t]
        pct = m["completed_rate"] * 100
        line += f"{get_status_emoji(pct, expected_pct)} {pct:.2f}% (Rank #{done_ranks[t]})  "[:col_w].ljust(col_w)
    line += f"{avg_done*100:.2f}%"
    print(line)

    # Worked Rate
    r = "Worked Rate (Draft+Done) "
    line = f"  {r:<33}"
    for t in targets:
        m = pml_metrics[t]
        pct = m["worked_rate"] * 100
        line += f"{get_status_emoji(pct, expected_pct)} {pct:.2f}% (Rank #{worked_ranks[t]})  "[:col_w].ljust(col_w)
    line += f"{avg_worked*100:.2f}%"
    print(line)

    # Approval Rate
    r = "Approval Rate (Verifikasi) "
    line = f"  {r:<33}"
    for t in targets:
        m = pml_metrics[t]
        pct = m["approval_rate"] * 100
        emoji = "🟢" if pct >= 70 else ("🔴" if pct < 20 else "🟡")
        line += f"{emoji} {pct:.2f}%".ljust(col_w)
    line += f"{avg_approval*100:.2f}%"
    print(line)

    # Antrean Pending
    r = "Antrean Pending (Submit) "
    line = f"  {r:<33}"
    for t in targets:
        m = pml_metrics[t]
        sub = m["submitted"]
        emoji = "🔴" if sub > 20 and m["approval_rate"] < 0.20 else ("🟡" if sub > 20 else "🟢")
        line += f"{emoji} {sub} berkas".ljust(col_w)
    line += f"{avg_pending:.1f} berkas"
    print(line)

    # Target Harian
    r = "Target Harian (Approve/Hari)"
    line = f"  {r:<33}"
    for t in targets:
        line += f"{pml_metrics[t]['pml_daily_target']:.1f}/hari".ljust(col_w)
    line += f"{avg_daily_tgt:.1f}/hari"
    print(line)

    # Status Bottleneck
    def bot_status(t):
        m = pml_metrics[t]
        if m["submitted"] > 20 and m["approval_rate"] < 0.20: return "🔴 BOTTLENECK"
        if m["submitted"] > 20: return "🟡 WARNING"
        return "🟢 AMAN"
    r = "Status Bottleneck"
    line = f"  {r:<33}"
    for t in targets:
        line += bot_status(t).ljust(col_w)
    line += "—"
    print(line)

    print(f"{'─'*100}")

    # ─── TABEL 2: DETAIL PPL PER PML ─────────────────────────────────────────
    for target_pml in targets:
        pj = pml_to_pj[target_pml]
        kec_label = ", ".join(sorted(list(pml_to_kecs.get(target_pml, []))))
        m = pml_metrics[target_pml]

        is_bottleneck = m["submitted"] > 20 and m["approval_rate"] < 0.20
        bot_label = "🔴 BOTTLENECK KRITIS" if is_bottleneck else ("🟡 WARNING" if m["submitted"] > 20 else "🟢 AMAN")

        label_icon = "🏆" if target_pml == top_pml else ("⚠️" if target_pml == "Abang Handri" else "🔴")
        print(f"\n{'─'*100}")
        print(f" {label_icon} TABEL 2: Detail PPL di bawah PML {target_pml}")
        print(f"   PJ-Kuda: {pj} | Kecamatan: {kec_label} | Status: {bot_label}")
        print(f"   Done: {m['completed_rate']*100:.2f}% (Rank #{done_ranks[target_pml]}/{total_pmls}) | "
              f"Worked: {m['worked_rate']*100:.2f}% | "
              f"Approval: {m['approval_rate']*100:.2f}% | "
              f"Pending: {m['submitted']} berkas")
        print(f"{'─'*100}")
        print(f"  {'Nama PPL':<25} {'Kec':<16} {'Target':<7} {'Worked':<20} {'Submit':<7} {'Approve':<8} {'Tgt/Hari':<10} {'Done %':<10} {'Est. Selesai'}")
        print(f"  {'-'*125}")

        ppl_details = []
        for (pml, ppl), sls_list in pml_ppl_to_sls.items():
            if pml != target_pml:
                continue
            pm = aggregate_metrics(sls_list, sls_info, sheet_map)
            done_pct = pm["completed_rate"] * 100
            worked_pct = pm["worked_rate"] * 100
            kecs = sorted(list(set(
                sls_info[s].get("kecamatan", "") for s in sls_list if s in sls_info)))
            kec_str = "/".join(kecs) if kecs else "-"

            est_raw = get_est_completion(done_pct, elapsed_days)
            est_str = clean_ansi(est_raw)
            if "Tidak Terprediksi" in est_str or done_pct == 0:
                est_str = "Tdk Terproyeksi"

            ppl_details.append({
                "name": ppl, "kec": kec_str,
                "target": pm["target"], "worked": pm["worked"],
                "worked_pct": worked_pct, "submit": pm["submitted"],
                "approve": pm["approved"], "daily_tgt": pm["ppl_daily_target"],
                "done_pct": done_pct, "est": est_str,
            })

        ppl_details.sort(key=lambda x: x["done_pct"])
        for p in ppl_details:
            done_emoji  = get_status_emoji(p["done_pct"], expected_pct)
            wrk_emoji   = get_status_emoji(p["worked_pct"], expected_pct)
            worked_str  = f"{wrk_emoji} {p['worked']} ({p['worked_pct']:.1f}%)"
            print(
                f"  {p['name']:<25} {p['kec']:<16} {p['target']:<7} {worked_str:<20} "
                f"{p['submit']:<7} {p['approve']:<8} {p['daily_tgt']:>6.1f}/hari  "
                f"{done_emoji} {p['done_pct']:.2f}%   {p['est']}"
            )

        # Diagnosis
        kritis = [p for p in ppl_details if p["done_pct"] < max(3.0, expected_pct * 0.25)]
        print(f"\n  📌 Diagnosis:")
        if is_bottleneck:
            print(f"  🔴 PML {target_pml} dalam kondisi BOTTLENECK KRITIS — {m['submitted']} berkas pending "
                  f"dengan approval rate hanya {m['approval_rate']*100:.2f}%. "
                  f"PPL sudah submit tapi berkas tertahan di antrian verifikasi PML.")
        elif m["submitted"] > 20:
            print(f"  🟡 Antrean pending PML {target_pml} mulai tinggi ({m['submitted']} berkas). "
                  f"Perlu diciciil agar tidak menjadi bottleneck.")
        else:
            print(f"  🟢 PML {target_pml} berjalan sehat. Antrean terkendali.")

        if kritis:
            print(f"  ⚠️  PPL kritis (progres merah): {', '.join(p['name'] for p in kritis)}")
            for p in kritis:
                gap = p["worked_pct"] - p["done_pct"]
                if gap > 5:
                    print(f"     → {p['name']}: Worked {p['worked_pct']:.1f}% vs Done {p['done_pct']:.2f}% "
                          f"(gap {gap:.1f}% — kemungkinan MASALAH SUBMIT/TEMPLATE, bukan malas ke lapangan)")
                else:
                    print(f"     → {p['name']}: Worked {p['worked_pct']:.1f}% ≈ Done {p['done_pct']:.2f}% "
                          f"— PPL belum banyak turun lapangan, butuh pendampingan langsung")

    print(f"\n{'='*100}")
    print(f"  PML TERTINGGI  : {top_pml} (Done {pml_metrics[top_pml]['completed_rate']*100:.2f}%, "
          f"Rank #{done_ranks[top_pml]}/{total_pmls})")
    print(f"  PML TERENDAH   : {bot_pml} (Done {pml_metrics[bot_pml]['completed_rate']*100:.2f}%, "
          f"Rank #{done_ranks[bot_pml]}/{total_pmls})")
    print(f"  PML ABANG HANDRI: Done {pml_metrics['Abang Handri']['completed_rate']*100:.2f}%, "
          f"Rank #{done_ranks['Abang Handri']}/{total_pmls}")
    print(f"{'='*100}")

if __name__ == "__main__":
    main()
