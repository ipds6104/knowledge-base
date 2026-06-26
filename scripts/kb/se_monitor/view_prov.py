"""kb/se_monitor/view_prov.py — Tampilkan tabel peringkat Kalbar (--prov)."""

from ..colors import Colors
from .data import get_target_status, get_est_completion


def print_prov(
    kab_list: list,
    prov_agg: dict,
    elapsed_days: int,
    total_days: int,
    expected_pct: float,
    data_source_info: str,
) -> None:
    """Cetak tabel peringkat seluruh Kabupaten/Kota di Kalbar."""
    prov_pct = prov_agg["done_rate"] * 100
    prov_approved_pct = prov_agg["approved"] / prov_agg["target"] * 100 if prov_agg.get("target", 0) > 0 else 0.0

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== MONITORING PROGRES SE-2026 PROVINSI KALBAR ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days} hari lapangan)"
    )
    # Hitung kabupaten terlama di Kalbar
    if kab_list:
        slowest_kab, slowest_m = kab_list[-1]
        slowest_pct = slowest_m["completed_rate"] * 100
        slowest_est = get_est_completion(slowest_pct, elapsed_days)
        import re
        visible_slowest_est = re.sub(r'\033\[[0-9;]*m', '', slowest_est)
        prov_worst_str = f"{slowest_kab} ({visible_slowest_est}, progres {slowest_pct:.2f}%)"
    else:
        prov_worst_str = "-"

    print(f"Status Prov. Kalbar : {get_target_status(prov_pct, expected_pct)}")
    print(f"Estimasi PPL Selesai (Agregat): {get_est_completion(prov_pct, elapsed_days)}")
    print(f"Estimasi Kabupaten Terlama    : {prov_worst_str}")
    print(f"Estimasi PML Selesai (Agregat): {get_est_completion(prov_approved_pct, elapsed_days)}")

    sep = "-" * 138
    print(sep)
    print(
        f"{'Rank':<4} | {'Kabupaten/Kota':<20} | {'Target':<7} | {'Worked %':<10} | {'Done %':<8} "
        f"| {'Approval %':<10} | {'Tgt PPL/PML':<11} | {'Status':<30} | {'Est. Selesai'}"
    )
    print(sep)

    for idx, (kab, m) in enumerate(kab_list, 1):
        kab_pct = m["completed_rate"] * 100
        worked_pct = m["worked_rate"] * 100
        status  = get_target_status(kab_pct, expected_pct)
        est     = get_est_completion(kab_pct, elapsed_days)
        print(
            f"{idx:<4} | {kab:<20} | {m['target']:<7} | {worked_pct:>8.2f}% | {kab_pct:>6.2f}% "
            f"| {m['approval_rate']*100:>10.2f}% "
            f"| {m['ppl_daily_target']:>4.1f}/{m['pml_daily_target']:<6.1f} "
            f"| {status:<41} | {est}"
        )

    print(sep)
    prov_worked_pct = prov_agg["worked_rate"] * 100
    print(
        f"{'TOTAL PROVINSI KALBAR':<27} | {prov_agg['target']:<7} | {prov_worked_pct:>8.2f}% | {prov_pct:>6.2f}% "
        f"| {prov_agg['approval_rate']*100:>10.2f}% "
        f"| {prov_agg['ppl_daily_target']:>4.1f}/{prov_agg['pml_daily_target']:<6.1f} "
        f"| {get_target_status(prov_pct, expected_pct):<41} | {get_est_completion(prov_pct, elapsed_days)}"
    )
    print(sep)
    print()
