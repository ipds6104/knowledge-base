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

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== MONITORING PROGRES SE-2026 PROVINSI KALBAR ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days} hari lapangan)"
    )
    print(f"Status Prov. Kalbar : {get_target_status(prov_pct, expected_pct)}")
    print(f"Estimasi PPL Selesai (Worked): {get_est_completion(prov_agg['worked_rate'] * 100, elapsed_days)}")
    print(f"Estimasi PML Selesai (Done)  : {get_est_completion(prov_pct, elapsed_days)}")

    sep = "-" * 120
    print(sep)
    print(
        f"{'Rank':<4} | {'Kabupaten/Kota':<25} | {'Target':<7} | {'Done %':<8} "
        f"| {'Worked %':<8} | {'Approval %':<10} | {'Status':<30} | {'Est. Selesai'}"
    )
    print(sep)

    for idx, (kab, m) in enumerate(kab_list, 1):
        kab_pct = m["completed_rate"] * 100
        status  = get_target_status(kab_pct, expected_pct)
        est     = get_est_completion(kab_pct, elapsed_days)
        print(
            f"{idx:<4} | {kab:<25} | {m['target']:<7} | {kab_pct:>6.2f}% "
            f"| {m['worked_rate']*100:>8.2f}% | {m['approval_rate']*100:>10.2f}% "
            f"| {status:<41} | {est}"
        )

    print(sep)
    print(
        f"{'TOTAL PROVINSI KALBAR':<30} | {prov_agg['target']:<7} | {prov_pct:>6.2f}% "
        f"| {prov_agg['worked_rate']*100:>8.2f}% | {prov_agg['approval_rate']*100:>10.2f}% "
        f"| {get_target_status(prov_pct, expected_pct):<41} | {get_est_completion(prov_pct, elapsed_days)}"
    )
    print(sep)
    print()
