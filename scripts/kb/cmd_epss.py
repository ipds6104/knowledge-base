"""Command handler for EPSS evaluation and IPS simulation (kb epss)."""

import argparse
import sys
from typing import Dict, List, Optional
from kb.epss_calc import (
    EPSS_INDICATORS,
    INDICATOR_DICT,
    MEMPAWAH_BASELINE_SCORES,
    MEMPAWAH_11_PERBAIKAN,
    calculate_ips,
    get_predikat,
)


def run_summary(args):
    """Menampilkan ringkasan nilai baseline pra-harmonisasi Mempawah dan estimasi perbaikan."""
    baseline_scores = dict(MEMPAWAH_BASELINE_SCORES)
    
    ips_base, dom_base, _ = calculate_ips(baseline_scores)
    
    # Skenario Target Level 2 untuk 11 Indikator
    scores_lvl2 = dict(baseline_scores)
    for code in MEMPAWAH_11_PERBAIKAN:
        scores_lvl2[code] = max(scores_lvl2[code], 2)
    ips_lvl2, dom_lvl2, _ = calculate_ips(scores_lvl2)
    
    # Skenario Target Level 3 untuk 11 Indikator
    scores_lvl3 = dict(baseline_scores)
    for code in MEMPAWAH_11_PERBAIKAN:
        scores_lvl3[code] = max(scores_lvl3[code], 3)
    ips_lvl3, dom_lvl3, _ = calculate_ips(scores_lvl3)

    print("=" * 80)
    print("SIMULASI & ESTIMASI INDEKS PEMBANGUNAN STATISTIK (IPS) KABUPATEN MEMPAWAH")
    print("Evaluasi Penyelenggaraan Statistik Sektoral (EPSS) 2026")
    print("=" * 80)
    print(f"Predikat Baseline Saat Ini : {ips_base:.3f} ({get_predikat(ips_base)})")
    print(f"Target Skenario Moderat    : {ips_lvl2:.3f} ({get_predikat(ips_lvl2)}) [Semua 11 Indikator naik ke Level 2]")
    print(f"Target Skenario Optimal    : {ips_lvl3:.3f} ({get_predikat(ips_lvl3)}) [Semua 11 Indikator naik ke Level 3]")
    print("-" * 80)
    print("Rincian Nilai per Domain:")
    print(f"{'Domain':<35} | {'Bobot':<6} | {'Baseline':<8} | {'Target L2':<10} | {'Target L3':<10}")
    print("-" * 80)
    
    domain_names = {
        1: ("Prinsip Satu Data Indonesia", "28%"),
        2: ("Kualitas Data", "24%"),
        3: ("Proses Bisnis Statistik", "19%"),
        4: ("Kelembagaan", "17%"),
        5: ("Statistik Nasional", "12%"),
    }
    
    for d in range(1, 6):
        d_name, d_weight = domain_names[d]
        print(f"{d}. {d_name:<32} | {d_weight:<6} | {dom_base[d]:<8.2f} | {dom_lvl2[d]:<10.2f} | {dom_lvl3[d]:<10.2f}")
        
    print("-" * 80)
    delta_l2 = ips_lvl2 - ips_base
    delta_l3 = ips_lvl3 - ips_base
    print(f"Kenaikan Skor IPS (Target L2) : +{delta_l2:.3f} poin")
    print(f"Kenaikan Skor IPS (Target L3) : +{delta_l3:.3f} poin")
    print("=" * 80)
    print("\nCatatan Analisis:")
    print("1. Kenaikan 11 indikator ke Level 2 mengangkat skor IPS melompat sebesar +0,215 poin.")
    print("2. Jika berhasil mencapai Level 3 dengan kelengkapan SOP & regulasi formal,")
    print(f"   skor IPS melonjak +{delta_l3:.3f} poin menjadi {ips_lvl3:.3f} (Kategori {get_predikat(ips_lvl3)}).")
    print("3. Untuk melihat ranking dampak masing-masing indikator, jalankan: python scripts/kb.py epss impact")


def run_weights(args):
    """Menampilkan tabel pembobotan lengkap seluruh 38 indikator EPSS."""
    print("=" * 95)
    print(f"{'Kode':<6} | {'Indikator':<45} | {'Domain':<8} | {'Aspek':<8} | {'Ind/Asp':<8} | {'Bobot Relatif':<12}")
    print("=" * 95)
    
    current_domain = None
    for ind in EPSS_INDICATORS:
        if ind.domain_id != current_domain:
            current_domain = ind.domain_id
            print("-" * 95)
            print(f"DOMAIN {ind.domain_id}: {ind.domain_name.upper()} (Bobot: {int(ind.domain_weight*100)}%)")
            print("-" * 95)
        
        d_pct = f"{int(ind.domain_weight*100)}%"
        a_pct = f"{int(ind.aspect_weight*100)}%"
        i_pct = f"{int(ind.ind_weight_in_aspect*100)}%"
        r_pct = f"{ind.official_relative_pct:.2f}%"
        print(f"{ind.code:<6} | {ind.name[:45]:<45} | {d_pct:<8} | {a_pct:<8} | {i_pct:<8} | {r_pct:<12}")
        
    print("=" * 95)
    tot_weight = sum(ind.official_relative_pct for ind in EPSS_INDICATORS)
    print(f"Total Akumulasi Bobot Relatif 38 Indikator: {tot_weight:.2f}%")
    print("=" * 95)


def run_impact(args):
    """Menganalisis ranking dampak 11 indikator target perbaikan Mempawah."""
    print("=" * 85)
    print("RANKING DAMPAK 11 INDIKATOR PERBAIKAN PEMKAB MEMPAWAH (URUT BOBOT RELATIF)")
    print("=" * 85)
    print(f"{'No':<3} | {'Kode':<6} | {'Indikator':<36} | {'Domain':<12} | {'Bobot':<8} | {'Gain +1 Lvl':<11}")
    print("-" * 85)
    
    perbaikan_defs = [INDICATOR_DICT[c] for c in MEMPAWAH_11_PERBAIKAN]
    # Urutkan berdasarkan bobot relatif terbesar
    perbaikan_defs.sort(key=lambda x: x.official_relative_pct, reverse=True)
    
    tot_weight = 0.0
    for idx, ind in enumerate(perbaikan_defs, start=1):
        tot_weight += ind.official_relative_pct
        gain_plus_1 = ind.official_relative_pct / 100.0
        print(f"{idx:<3} | {ind.code:<6} | {ind.name[:36]:<36} | {ind.domain_name[:12]:<12} | {ind.official_relative_pct:>5.2f}%  | +{gain_plus_1:.4f}")
        
    print("-" * 85)
    print(f"TOTAL AKUMULASI BOBOT 11 INDIKATOR : {tot_weight:.2f}%")
    print(f"TOTAL POTENSI GAIN (+1 LEVEL SEMUA) : +{tot_weight/100.0:.4f} poin IPS")
    print(f"TOTAL POTENSI GAIN (+2 LEVEL SEMUA) : +{(tot_weight*2)/100.0:.4f} poin IPS")
    print("=" * 85)
    print("Rekomendasi Prioritas Eksekusi:")
    print("1. Indikator 20201 (Akurasi Data): Kontributor terbesar (3,84%). Wajib dokumen verifikasi.")
    print("2. Empat Serangkai Kualitas Data (20301, 20302, 20501, 20502): Masing-masing bernilai 2,52%.")
    print("   Total 4 indikator ini menyumbang 10,08% bobot komposit!")
    print("3. Analisis Data 30302 (2,00%) & Kelembagaan 40102, 40103, 40302 (1,49% masing-masing).")


def run_simulate(args):
    """Menjalankan simulasi interaktif atau kustom nilai per indikator."""
    scores = dict(MEMPAWAH_BASELINE_SCORES)
    
    target_lvl = args.target_level
    if target_lvl is not None:
        for c in MEMPAWAH_11_PERBAIKAN:
            scores[c] = max(scores[c], target_lvl)
            
    # Custom indicator overrides from args
    if args.override:
        for item in args.override:
            if "=" in item:
                k, v = item.split("=", 1)
                k = k.strip()
                try:
                    scores[k] = int(v.strip())
                except ValueError:
                    print(f"Peringatan: Nilai tidak valid untuk {k}: {v}")

    ips, dom_scores, _ = calculate_ips(scores)
    base_ips, base_dom, _ = calculate_ips(MEMPAWAH_BASELINE_SCORES)
    
    print("=" * 70)
    print(f"HASIL SIMULASI SKENARIO KUSTOM IPS MEMPAWAH")
    print("=" * 70)
    print(f"Nilai Baseline Awal : {base_ips:.3f} ({get_predikat(base_ips)})")
    print(f"Nilai Hasil Simulasi: {ips:.3f} ({get_predikat(ips)})")
    print(f"Perubahan (Delta)   : {ips - base_ips:+.3f} poin")
    print("-" * 70)
    for d in range(1, 6):
        d_name = {
            1: "Domain 1 (Prinsip SDI)",
            2: "Domain 2 (Kualitas Data)",
            3: "Domain 3 (Proses Bisnis)",
            4: "Domain 4 (Kelembagaan)",
            5: "Domain 5 (Statistik Nasional)"
        }[d]
        print(f"{d_name:<30} : {dom_scores[d]:.2f} (Awal: {base_dom[d]:.2f}, Delta: {dom_scores[d] - base_dom[d]:+.2f})")
    print("=" * 70)


def add_subparser(subparsers):
    """Mendaftarkan subparser 'epss' ke parser argumen utama kb.py."""
    parser_epss = subparsers.add_parser(
        "epss",
        help="Kalkulator bobot resmi EPSS 2026 dan simulasi Indeks Pembangunan Statistik (IPS).",
        description="Utilitas kalkulasi pembobotan 5 Domain, 19 Aspek, 38 Indikator EPSS dan estimasi skor IPS.",
    )
    
    epss_sub = parser_epss.add_subparsers(dest="epss_subcommand")
    
    # Subcommand: summary (default)
    sub_summary = epss_sub.add_parser("summary", help="Tampilkan estimasi skor Mempawah (baseline vs target)")
    sub_summary.set_defaults(func=run_summary)
    
    # Subcommand: weights
    sub_weights = epss_sub.add_parser("weights", help="Tampilkan tabel lengkap pembobotan resmi 38 indikator")
    sub_weights.set_defaults(func=run_weights)
    
    # Subcommand: impact
    sub_impact = epss_sub.add_parser("impact", help="Analisis ranking sensitivitas dan dampak 11 indikator perbaikan")
    sub_impact.set_defaults(func=run_impact)
    
    # Subcommand: simulate
    sub_sim = epss_sub.add_parser("simulate", help="Simulasikan skor IPS dengan skenario kustom")
    sub_sim.add_argument("--target-level", "-t", type=int, choices=[1, 2, 3, 4, 5], help="Set level target untuk 11 indikator perbaikan")
    sub_sim.add_argument("--override", "-o", nargs="*", help="Override indikator spesifik, contoh: -o 20201=3 50301=3")
    sub_sim.set_defaults(func=run_simulate)
    
    parser_epss.set_defaults(func=run_summary)
