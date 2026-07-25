#!/usr/bin/env python3
"""
Script: extract_sakernas_intersect.py
Menarik 100% data mikro keluarga/responden SE2026 dari Superset SQL Lab 
secara ter-batch (5 SLS per query) dilengkapi Paginasi Loop Offset untuk menjamin 0% data terpotong limit 1.000 baris.

Pemetaan Kolom dari Kamus Data Resmi (data-dictionary-se2026.md):
1. SLS                   : base_table_assignment.level_6_full_code & level_5_name
2. Nama Kepala Keluarga  : COALESCE(root_table.dtsen_nama_kk, base_table_assignment.data1)
3. No Urut Bangunan      : base_table_assignment.data3
4. Keberadaan Keluarga   : COALESCE(root_table.ada_keluarga_label, base_table_assignment.data9)
5. Pendidikan KRT        : nested_dtsen_var.ijazah_label (saat no_urut_kk_var = '1')
6. No HP                 : root_table.telp_info
"""

import csv
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(BASE_DIR) != "knowledge-base":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(BASE_DIR) == "scripts":
        BASE_DIR = os.path.dirname(BASE_DIR)

FASIH_SYNC_DIR = "/home/ihza/Projects/fasih-sync-monitoring"
OUTPUT_DIR = os.path.join(BASE_DIR, "kegiatan", "sakernas", "2026-08")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "prelist_updating_sakernas_se2026_intersect.csv")

# 48 Kode Sub-SLS Irisan dari Sakernas Agustus 2026
SAMPLE_SLS_CODES = [
    "6104080002004900", "6104080002004100", "6104080002004300", "6104080004005200",
    "6104080004006900", "6104080004001500", "6104080006000300", "6104081005003600",
    "6104081003002100", "6104081001002000", "6104081001002100", "6104081006000800",
    "6104090001001900", "6104090004000300", "6104090004000900", "6104090009005300",
    "6104090009001700", "6104090009005700", "6104090012001600", "6104090005001200",
    "6104091005000500", "6104091006000300", "6104091006001200", "6104091002001000",
    "6104100008002000", "6104101006001600", "6104100007001600", "6104100012003200",
    "6104100012001900", "6104100014000700", "6104100014000200", "6104100015001700",
    "6104101001001500", "6104101003000600", "6104101004001100", "6104101006000200",
    "6104101002002900", "6104101008000200", "6104110002000600", "6104110002000800",
    "6104110006001200", "6104110010000900", "6104110012000300", "6104120005001000",
    "6104120002000900", "6104121003000500", "6104121003000700", "6104121002000100"
]


def fetch_sqllab_intersect_data(sls_list):
    """Menarik 100% data mikro SE2026 untuk 48 SLS irisan dengan paginasi batch & offset."""
    if not os.path.exists(FASIH_SYNC_DIR):
        print(f"❌ Error: Repositori fasih-sync-monitoring tidak ditemukan di {FASIH_SYNC_DIR}")
        return []

    all_rows = []
    chunk_size = 1000
    batch_size = 5  # Batch 5 SLS per query untuk efisiensi
    
    total_batches = (len(sls_list) + batch_size - 1) // batch_size
    print(f"🔄 [Fetching Complete Data] Memulai penarikan 100% data mikro untuk {len(sls_list)} SLS ({total_batches} Batch)...\n")
    
    for i in range(0, len(sls_list), batch_size):
        batch_codes = sls_list[i:i + batch_size]
        in_clause = ", ".join(f"'{code}'" for code in batch_codes)
        batch_idx = (i // batch_size) + 1
        
        offset = 0
        batch_rows_count = 0
        
        while True:
            sql = f"""
            SELECT 
              b.level_6_full_code AS sls,
              b.level_5_name AS nama_sls,
              b.level_3_name AS kecamatan,
              COALESCE(r.dtsen_nama_kk, b.data1) AS nama_kepala_keluarga,
              b.data2 AS alamat_bangunan,
              b.data3 AS no_urut_bangunan_keluarga,
              COALESCE(r.ada_keluarga_label, b.data9) AS keberadaan_keluarga,
              v.ijazah_label AS pendidikan_krt,
              r.telp_info AS no_hp,
              b.assignment_status_alias AS status_dokumen
            FROM base_table_assignment b
            LEFT JOIN root_table r ON b.assignment_id = r.assignment_id
            LEFT JOIN nested_dtsen_var v ON b.assignment_id = v.assignment_id AND v.no_urut_kk_var = '1'
            WHERE b.level_6_full_code IN ({in_clause})
              AND b.assignment_status_alias != 'DRAFT'
            ORDER BY b.level_6_full_code ASC, b.data1 ASC
            LIMIT {chunk_size} OFFSET {offset};
            """
            
            cmd = ["node", "src/execute-query.js", sql]
            try:
                res = subprocess.run(cmd, cwd=FASIH_SYNC_DIR, capture_output=True, text=True, check=True)
                stdout = res.stdout
                
                stdout_text = res.stdout
                start_idx = stdout_text.find("[")
                end_idx = stdout_text.rfind("]")
                
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = stdout_text[start_idx:end_idx + 1]
                    rows = json.loads(json_str)
                    all_rows.extend(rows)
                    batch_rows_count += len(rows)
                    
                    if len(rows) < chunk_size:
                        break  # Batch ini selesai ditarik
                    offset += chunk_size  # Lanjut paginasi jika baris mencapai limit 1000
                else:
                    break
            except Exception as e:
                print(f"   ⚠️ Error saat menarik Batch {batch_idx}: {e}")
                break

        print(f"   🟢 [Batch {batch_idx:02d}/{total_batches}] {len(batch_codes)} SLS: {batch_rows_count} keluarga ditarik (Total Akumulasi: {len(all_rows)}).")

    return all_rows


def main():
    print("==========================================================================================")
    print("🚀 [EXTRACT SAKERNAS INTERSECT DATA] PENARIKAN 100% DATA KELUARGA IRISAN UNTUK SAKERNAS")
    print("==========================================================================================\n")
    
    rows = fetch_sqllab_intersect_data(SAMPLE_SLS_CODES)
    print(f"DEBUG MAIN: len(rows) = {len(rows)}")
    if not rows:
        print("❌ Tidak ada data yang berhasil ditarik.")
        return

    # Header CSV baku sesuai 6 request Vaya
    fieldnames = [
        "sls",
        "nama_sls",
        "kecamatan",
        "nama_kepala_keluarga",
        "no_urut_bangunan_keluarga",
        "keberadaan_keluarga",
        "pendidikan_krt",
        "no_hp",
        "alamat_bangunan",
        "status_dokumen"
    ]

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "sls": r.get("sls", ""),
                "nama_sls": r.get("nama_sls", ""),
                "kecamatan": r.get("kecamatan", ""),
                "nama_kepala_keluarga": r.get("nama_kepala_keluarga", ""),
                "no_urut_bangunan_keluarga": r.get("no_urut_bangunan_keluarga", ""),
                "keberadaan_keluarga": r.get("keberadaan_keluarga", "1. Ditemukan") or "1. Ditemukan",
                "pendidikan_krt": r.get("pendidikan_krt", "-") or "-",
                "no_hp": r.get("no_hp", "-") or "-",
                "alamat_bangunan": r.get("alamat_bangunan", ""),
                "status_dokumen": r.get("status_dokumen", "")
            })

    print(f"\n💾 [HASIL EKSPOR TOTAL] {len(rows)} data keluarga berhasil diekstrak dan disimpan ke:")
    print(f"   📁 {OUTPUT_CSV}")
    print("\n==========================================================================================")


if __name__ == "__main__":
    main()
