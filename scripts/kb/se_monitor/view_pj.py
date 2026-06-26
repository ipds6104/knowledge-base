"""kb/se_monitor/view_pj.py — Tampilkan breakdown detail tim PJ tertentu (default view)."""

import sys
import re

from ..colors import Colors
from .data import get_target_status, get_est_completion


def format_visible(text: str, width: int, align: str = "<") -> str:
    """Format string yang mengandung escape code ANSI agar memiliki visual width tertentu."""
    visible = re.sub(r'\033\[[0-9;]*m', '', text)
    val_len = len(visible)
    padding = width - val_len
    if padding <= 0:
        return text
    if align == "<":
        return text + " " * padding
    elif align == ">":
        return " " * padding + text
    else:
        left = padding // 2
        right = padding - left
        return " " * left + text + " " * right


def print_pj(
    target_pj_name: str,
    pj_summaries: list,
    pj_kuda_groups: dict,
    aggregate_fn,
    kab_avg_completed: float,
    kab_avg_worked: float,
    kab_avg_approval: float,
    elapsed_days: int,
    total_days: int,
    expected_pct: float,
    data_source_info: str,
) -> None:
    """Cetak breakdown detail tim PJ-Kuda tertentu beserta diagnosis."""
    target_pj = next(
        (p for p in pj_summaries if p["pj"].lower() == target_pj_name.lower()),
        None,
    )

    if not target_pj:
        print(f"{Colors.FAIL}Error: PJ-Kuda '{target_pj_name}' tidak ditemukan.{Colors.ENDC}")
        print("Nama PJ-Kuda yang tersedia:")
        for p in sorted(pj_summaries, key=lambda x: x["pj"]):
            print(f" - {p['pj']}")
        sys.exit(1)

    rank = pj_summaries.index(target_pj) + 1
    pj_pct = target_pj["completed_rate"] * 100

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== STATUS MONITORING PJ-KUDA: {target_pj['pj']} ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Peringkat Kabupaten : {Colors.BOLD}{rank} dari {len(pj_summaries)}{Colors.ENDC}")
    print(f"Target Total        : {target_pj['target']} unit sensus (SLS: {target_pj['sls_count']})")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days} hari lapangan)"
    )
    pj_approved_pct = target_pj["approved"] / target_pj["target"] * 100 if target_pj.get("target", 0) > 0 else 0.0
    print(f"Status Target       : {get_target_status(pj_pct, expected_pct)}")
    print(f"Target Harian Tim   : PPL: {Colors.BOLD}{target_pj['ppl_daily_target']:.1f}/hari{Colors.ENDC} (submit), PML: {Colors.BOLD}{target_pj['pml_daily_target']:.1f}/hari{Colors.ENDC} (approve)")
    
    # Hitung PPL terlama di tim PJ ini
    team_worst_name = None
    team_worst_date = None
    team_worst_pct = 0.0
    from datetime import datetime, timedelta
    today_dt = datetime.now().date()
    pmls = pj_kuda_groups.get(target_pj["pj"], {})
    for pml, ppls in pmls.items():
        for ppl, sls_list in ppls.items():
            ppl_m = aggregate_fn(sls_list)
            pct = ppl_m["completed_rate"] * 100
            if elapsed_days > 0 and pct > 0:
                daily_speed = pct / elapsed_days
                days_needed = (100.0 - pct) / daily_speed
                est_date = today_dt + timedelta(days=days_needed)
            else:
                est_date = None
                
            if est_date is None:
                if ppl_m["target"] > 0 and (team_worst_date is not None or team_worst_name is None):
                    team_worst_name = ppl
                    team_worst_date = None
                    team_worst_pct = pct
            else:
                if team_worst_name is None:
                    team_worst_name = ppl
                    team_worst_date = est_date
                    team_worst_pct = pct
                elif team_worst_date is not None and est_date > team_worst_date:
                    team_worst_name = ppl
                    team_worst_date = est_date
                    team_worst_pct = pct

    if team_worst_name:
        if team_worst_date is None:
            team_worst_str = f"Tdk Terproyeksi ({team_worst_name}, progres 0.00%)"
        else:
            team_worst_str = f"{team_worst_date.strftime('%d %b %Y')} ({team_worst_name}, progres {team_worst_pct:.2f}%)"
    else:
        team_worst_str = "-"

    print(f"Estimasi PPL Selesai (Agregat): {get_est_completion(pj_pct, elapsed_days)}")
    print(f"Estimasi PPL Selesai Terlama  : {team_worst_str}")
    print(f"Estimasi PML Selesai (Agregat): {get_est_completion(pj_approved_pct, elapsed_days)}")
    print("-" * 55)

    def _cmp(label, team_val, kab_val):
        color = Colors.GREEN if team_val >= kab_val else Colors.WARNING
        print(f"{label:<19}: {color}{team_val*100:>6.2f}%{Colors.ENDC} (Kabupaten: {kab_val*100:.2f}%)")

    _cmp("Worked Rate",    target_pj["worked_rate"],    kab_avg_worked)
    _cmp("Completed Rate", target_pj["completed_rate"], kab_avg_completed)
    _cmp("Approval Rate",  target_pj["approval_rate"],  kab_avg_approval)

    pmls = pj_kuda_groups.get(target_pj["pj"], {})
    warnings = []

    for pml, ppls in pmls.items():
        pml_sls = []
        for _, sls_list in ppls.items():
            pml_sls.extend(sls_list)
        pml_agg = aggregate_fn(pml_sls)

        pml_worked_color = Colors.GREEN if pml_agg["worked_rate"] >= kab_avg_worked else Colors.WARNING
        pml_done_color = Colors.GREEN if pml_agg["completed_rate"] >= kab_avg_completed else Colors.WARNING
        pml_app_color = (
            Colors.GREEN if pml_agg["approval_rate"] >= 0.7
            else (Colors.FAIL if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 0
                  else Colors.WARNING)
        )

        print(f"\n{Colors.BOLD}▶ PML: {pml}{Colors.ENDC} (SLS: {pml_agg['sls_count']}, Target: {pml_agg['target']})")
        print(
            f"  └─ Worked (Draft+Done): {pml_worked_color}{pml_agg['worked']} ({pml_agg['worked_rate']*100:.2f}%){Colors.ENDC}, "
            f"Selesai: {pml_done_color}{pml_agg['completed_rate']*100:.2f}%{Colors.ENDC}, "
            f"Approval: {pml_app_color}{pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}, "
            f"Tgt Approve: {Colors.BOLD}{pml_agg['pml_daily_target']:.1f}/hari{Colors.ENDC}"
        )
        header_line = (
            f"  {'Nama PPL':<25} | {'SLS':<3} | {'Target':<6} | {'Open':<5} "
            f"| {'Draft':<5} | {'Draft %':<7} | {'Worked (Drf+Dn)':<16} | {'Submit':<6} | {'Approve':<7} | {'Tgt/Hari':<8} | {'Done %':<8} | {'Est. Selesai':<15}"
        )
        sep = "  " + "-" * (len(header_line) - 2)
        print(sep)
        print(header_line)
        print(sep)

        ppl_list = []
        for ppl, sls_list in ppls.items():
            ppl_agg = aggregate_fn(sls_list)
            ppl_agg["name"] = ppl
            ppl_list.append(ppl_agg)
        ppl_list.sort(key=lambda x: x["completed_rate"])

        # Batas dinamis status PPL: Hijau jika >= 70% dari expected_pct (min 10%), Merah jika < 25% (min 3%)
        threshold_green = max(0.10, (expected_pct / 100) * 0.70)
        threshold_fail  = max(0.03, (expected_pct / 100) * 0.25)

        for ppl in ppl_list:
            if ppl["completed_rate"] >= threshold_green:
                done_color = Colors.GREEN
                emoji = "🟢"
            elif ppl["completed_rate"] < threshold_fail:
                done_color = Colors.FAIL
                emoji = "🔴"
            else:
                done_color = Colors.WARNING
                emoji = "🟡"
            
            done_text = f"{done_color}{emoji} {ppl['completed_rate']*100:>6.2f}%{Colors.ENDC}"
            done_formatted = format_visible(done_text, 8, "<")

            # Draft %
            ppl_draft_pct = ppl["draft"] / ppl["target"] * 100 if ppl["target"] > 0 else 0.0
            draft_pct_str = f"{ppl_draft_pct:>6.2f}%"

            # Worked %
            if ppl["worked_rate"] >= threshold_green:
                worked_color = Colors.GREEN
                worked_emoji = "🟢"
            elif ppl["worked_rate"] < threshold_fail:
                worked_color = Colors.FAIL
                worked_emoji = "🔴"
            else:
                worked_color = Colors.WARNING
                worked_emoji = "🟡"
            worked_text = f"{worked_color}{worked_emoji} {ppl['worked']} ({ppl['worked_rate']*100:.1f}%){Colors.ENDC}"
            worked_formatted = format_visible(worked_text, 16, "<")

            est_val = get_est_completion(ppl["completed_rate"] * 100, elapsed_days)
            if "Tidak Terprediksi" in est_val or ppl["completed_rate"] == 0:
                est_val = f"{Colors.FAIL}Tdk Terproyeksi{Colors.ENDC}"
            est_formatted = format_visible(est_val, 15, "<")

            print(
                f"  {ppl['name']:<25} | {ppl['sls_count']:<3} | {ppl['target']:<6} "
                f"| {ppl['open']:<5} | {ppl['draft']:<5} | {draft_pct_str:<7} | {worked_formatted} | {ppl['submitted']:<6} "
                f"| {ppl['approved']:<7} | {ppl['ppl_daily_target']:>8.1f} | {done_formatted} | {est_formatted}"
            )
            if ppl["completed_rate"] < threshold_fail:
                warnings.append(
                    f"PPL {Colors.BOLD}{ppl['name']}{Colors.ENDC} di bawah PML {pml} "
                    f"lambat pencacahan ({ppl['completed_rate']*100:.2f}% Selesai, {ppl['open']} Open, Batas Kritis: {threshold_fail*100:.2f}%)"
                )

        if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 5:
            warnings.append(
                f"PML {Colors.BOLD}{pml}{Colors.ENDC} menumpuk pekerjaan PPL "
                f"({Colors.FAIL}Approval Rate: {pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}, "
                f"{pml_agg['submitted']} kiriman menunggu persetujuan)"
            )

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DIAGNOSIS & TINDAKAN KOREKTIF ==={Colors.ENDC}")
    if warnings:
        for w in warnings:
            print(f" ⚠️  {w}")
    else:
        print(f" {Colors.GREEN}✔ Semua progres tim berjalan sehat sesuai dengan standar rata-rata kabupaten.{Colors.ENDC}")
    print()
