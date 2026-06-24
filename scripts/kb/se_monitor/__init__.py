"""kb/se_monitor — Orkestrator utama perintah `kb se-monitor`."""

import sys

from ..colors import Colors
from .data import (
    download_sheet,
    compute_kab_stats,
    compute_timeline,
    aggregate_metrics,
    download_alokasi,
)
from .hierarchy import build_hierarchy, build_lookup_maps, pj_first_name
from .history import (
    load_history,
    save_history,
    build_snapshot,
    should_save,
    update_history,
)
from .report import print_report
from .view_prov import print_prov
from .view_all_pj import print_all_pj
from .view_intervention import print_intervention
from .view_pj import print_pj


def cmd_se_monitor(args) -> None:
    """Implementasi perintah `kb se-monitor`."""
    # Download/update alokasi petugas terlebih dahulu jika terhubung internet
    download_alokasi()

    # 1. Bangun hierarki petugas
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()


    # 2. Ambil data dari Google Sheets (atau fallback ke cache lokal)
    sheet_map, csv_text, data_source_info = download_sheet()
    elapsed_days, total_days, expected_pct = compute_timeline()

    # 3. Hitung statistik makro Kabupaten Mempawah & PJ
    pj_summaries = []
    kab_avg_completed = 0.0
    kab_avg_worked = 0.0
    kab_avg_approval = 0.0

    # Wrapper fungsi agregasi agar tidak perlu mempassing sls_info dan sheet_map berkali-kali
    def aggregate_fn(sls_list):
        return aggregate_metrics(sls_list, sls_info, sheet_map)

    if has_alokasi:
        for pj, pmls in pj_kuda_groups.items():
            if not pj:
                continue
            all_sls = []
            for pml, ppls in pmls.items():
                for ppl, sls_list in ppls.items():
                    all_sls.extend(sls_list)
            agg = aggregate_fn(all_sls)
            agg["pj"] = pj
            pj_summaries.append(agg)

        total_target = sum(p["target"] for p in pj_summaries)
        total_completed = sum(p["completed"] for p in pj_summaries)
        total_worked = sum(p["worked"] for p in pj_summaries)
        total_approved = sum(p["approved"] for p in pj_summaries)
        total_submitted = sum(p["submitted"] for p in pj_summaries)

        kab_avg_completed = total_completed / total_target if total_target > 0 else 0.0
        kab_avg_worked = total_worked / total_target if total_target > 0 else 0.0
        kab_avg_approval = (
            total_approved / (total_approved + total_submitted)
            if (total_approved + total_submitted) > 0
            else 0.0
        )
        pj_summaries.sort(key=lambda x: x["completed_rate"], reverse=True)

    # 4. Agregasi data level Provinsi Kalbar
    kab_data, kab_list, prov_agg = compute_kab_stats(csv_text)
    prov_pct = prov_agg["done_rate"] * 100

    # 5. Manajemen Snapshot & Perbandingan Delta
    current_snapshot = build_snapshot(
        prov_agg, kab_data, pj_summaries, pj_kuda_groups, aggregate_fn
    )
    history_list = load_history()
    latest_history = history_list[-1] if history_list else None

    # Simpan snapshot baru jika ada perubahan nyata
    if should_save(current_snapshot, latest_history):
        history_list = update_history(history_list, current_snapshot)
        save_history(history_list)

    # Cetak delta perbandingan secara global jika bukan mode --report dan latest_history tersedia
    if latest_history and not args.report:
        print_comparison_delta(
            args,
            current_snapshot,
            latest_history,
            prov_pct,
            kab_data,
            pj_kuda_groups,
            aggregate_fn,
        )

    # 6. Render Output berdasarkan Flags
    if args.prov:
        print_prov(
            kab_list,
            prov_agg,
            elapsed_days,
            total_days,
            expected_pct,
            data_source_info,
        )
        return

    # Validasi file alokasi untuk mode non-prov
    if not has_alokasi:
        print(
            f"{Colors.FAIL}Error: Berkas alokasi petugas tidak ditemukan di "
            f"kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv. "
            f"Mode ini memerlukan file alokasi.{Colors.ENDC}"
        )
        sys.exit(1)

    if args.report:
        print_report(
            prov_agg,
            kab_data,
            kab_list,
            pj_summaries,
            pj_kuda_groups,
            sls_info,
            aggregate_fn,
            elapsed_days,
            total_days,
            expected_pct,
            args.pj,
            current_snapshot,
            latest_history,
        )
    elif args.intervention:
        print_intervention(
            pj_kuda_groups,
            sls_info,
            aggregate_fn,
            kab_avg_completed,
            kab_avg_worked,
            kab_avg_approval,
            elapsed_days,
            total_days,
            expected_pct,
            data_source_info,
        )
    elif args.all_pj:
        print_all_pj(
            pj_summaries,
            kab_avg_completed,
            elapsed_days,
            total_days,
            expected_pct,
            data_source_info,
            args.pj,
        )
    else:
        # Default view: status monitoring per PJ-Kuda
        print_pj(
            args.pj,
            pj_summaries,
            pj_kuda_groups,
            aggregate_fn,
            kab_avg_completed,
            kab_avg_worked,
            kab_avg_approval,
            elapsed_days,
            total_days,
            expected_pct,
            data_source_info,
        )


def print_comparison_delta(
    args,
    current: dict,
    latest: dict,
    prov_pct: float,
    kab_data: dict,
    pj_kuda_groups: dict,
    aggregate_fn,
) -> None:
    """Cetak ringkasan delta perbandingan antara pengecekan saat ini dengan sebelumnya."""
    print(
        f"\n{Colors.BOLD}{Colors.CYAN}🔄 PERBANDINGAN DENGAN PENGECEKAN TERAKHIR "
        f"({latest.get('timestamp')}){Colors.ENDC}"
    )
    print("-" * 115)

    # 1. Delta Prov Kalbar
    l_prov = latest.get("prov", {})
    if l_prov and l_prov.get("target", 0) > 0:
        l_pct = l_prov["completed"] / l_prov["target"] * 100
        diff = prov_pct - l_pct
        diff_str = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
        color = Colors.GREEN if diff > 0 else Colors.ENDC
        print(
            f" * Progres Prov. Kalbar    : {l_pct:.2f}% -> "
            f"{Colors.BOLD}{prov_pct:.2f}%{Colors.ENDC} ({color}{diff_str}{Colors.ENDC})"
        )

    # 2. Delta Kab Mempawah
    c_memp = current["kab"].get("MEMPAWAH")
    l_memp = latest.get("kab", {}).get("MEMPAWAH")
    if c_memp and l_memp:
        c_pct = (c_memp["completed"] / c_memp["target"] * 100) if c_memp["target"] > 0 else 0.0
        l_pct = (l_memp["completed"] / l_memp["target"] * 100) if l_memp.get("target", 0) > 0 else 0.0
        diff = c_pct - l_pct
        diff_str = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
        color = Colors.GREEN if diff > 0 else Colors.ENDC
        print(
            f" * Progres Kab. Mempawah   : {l_pct:.2f}% -> "
            f"{Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({color}{diff_str}{Colors.ENDC})"
        )

    # 3. Delta Target PJ-Kuda
    target_pj = args.pj
    c_pj = current.get("pj", {}).get(target_pj)
    l_pj = latest.get("pj", {}).get(target_pj)
    if c_pj and l_pj:
        c_pct = (c_pj["completed"] / c_pj["target"] * 100) if c_pj["target"] > 0 else 0.0
        l_pct = (l_pj["completed"] / l_pj["target"] * 100) if l_pj.get("target", 0) > 0 else 0.0
        diff = c_pct - l_pct
        diff_str = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
        color = Colors.GREEN if diff > 0 else Colors.ENDC
        pj_short = target_pj.split()[0] if target_pj else ""
        print(
            f" * Progres Tim PJ {pj_short:<10}: {l_pct:.2f}% -> "
            f"{Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({color}{diff_str}{Colors.ENDC})"
        )

    # Lookup maps untuk PML -> PJ dan PPL -> (PML, PJ)
    pml_to_pj: dict = {}
    ppl_to_sup: dict = {}
    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            pml_to_pj[pml_name] = pj_name
            for ppl_name in ppls:
                ppl_to_sup[ppl_name] = (pml_name, pj_name)

    # 4. Delta Antrean PML
    c_pmls = current.get("pml_pending", {})
    l_pmls = latest.get("pml_pending", {})
    pml_diffs = []
    for pml, c_val in c_pmls.items():
        c_pend = c_val["pending"] if isinstance(c_val, dict) else c_val
        c_pj_v = c_val["pj"] if isinstance(c_val, dict) else pml_to_pj.get(pml, "")
        l_val  = l_pmls.get(pml, c_val)
        l_pend = l_val["pending"] if isinstance(l_val, dict) else l_val
        diff = c_pend - l_pend
        if diff != 0:
            pml_diffs.append((pml, c_pend, diff, c_pj_v))

    if pml_diffs:
        print("\n Perubahan Antrean PML:")
        for pml, c_pend, diff, c_pj in sorted(
            pml_diffs, key=lambda x: abs(x[2]), reverse=True
        )[:5]:
            diff_str = f"+{diff}" if diff > 0 else f"{diff}"
            color = Colors.GREEN if diff < 0 else Colors.FAIL
            pj_lbl = f" (PJ {pj_first_name(c_pj)})" if c_pj else ""
            print(
                f"   - PML {pml:<25}{pj_lbl}: {c_pend} pending "
                f"({color}{diff_str} berkas{Colors.ENDC})"
            )

    # 5. Delta Progres PPL
    c_ppls = current.get("ppl_completed", {})
    l_ppls = latest.get("ppl_completed", {})
    ppl_diffs = []
    for ppl, c_val in c_ppls.items():
        c_comp = c_val["completed"] if isinstance(c_val, dict) else c_val
        c_pml  = c_val.get("pml", "") if isinstance(c_val, dict) else ppl_to_sup.get(ppl, ("", ""))[0]
        l_val  = l_ppls.get(ppl, c_val)
        l_comp = l_val["completed"] if isinstance(l_val, dict) else l_val
        diff = c_comp - l_comp
        if diff > 0:
            ppl_diffs.append((ppl, c_comp, diff, c_pml))

    if ppl_diffs:
        print("\n Kemajuan PPL Teratas:")
        for ppl, c_comp, diff, c_pml in sorted(
            ppl_diffs, key=lambda x: x[2], reverse=True
        )[:5]:
            pml_lbl = f" (PML {c_pml})" if c_pml else ""
            print(
                f"   - PPL {ppl:<25}{pml_lbl}: +{diff} dokumen selesai "
                f"disubmit (total: {c_comp})"
            )

    print("-" * 115)
