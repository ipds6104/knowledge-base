#!/usr/bin/env python3
"""
Script: extract_sakernas_intersect.py
Menarik data mikro kuesioner SE2026 (nested_dtsen & nested_dtsen_var) dari Superset SQL Lab
khusus untuk daftar SLS sampel Sakernas yang beririsan.

Kolom yang diekstrak:
1. SLS (level_6_full_code)
2. Nama Kepala Keluarga (nama_kepala_keluarga)
3. No Urut Bangunan (no_urut_bangunan)
4. Keberadaan Keluarga (keberadaan_keluarga_label)
5. Pendidikan KRT (ijazah_tertinggi_label dari ART Hub KK)
6. No HP (no_hp dari ART Hub KK)
"""

import csv
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    """Menarik data mikro SE2026 untuk SLS yang beririsan via SQL Lab API."""
    if not os.path.exists(FASIH_SYNC_DIR):
        print(f"❌ Error: Repositori fasih-sync-monitoring tidak ditemukan di {FASIH_SYNC_DIR}")
        return []

    all_rows = []
    chunk_size = 10  # Batch 10 SLS per query agar tidak melebih query limit / url length
    
    for i in range(0, len(sls_list), chunk_size):
        batch = sls_list[i:i + chunk_size]
        in_clause = ", ".join(f"'{code}'" for code in batch)
        
        sql = f"""
        SELECT 
          b.level_6_full_code AS sls,
          b.level_5_name AS nama_sls,
          b.level_3_name AS kecamatan,
          d.nama_kepala_keluarga,
          d.no_urut_bangunan,
          d.keberadaan_keluarga_label AS keberadaan_keluarga,
          v.ijazah_tertinggi_label AS pendidikan_krt,
          v.no_hp
        FROM base_table_assignment b
        JOIN nested_dtsen d ON b.assignment_id = d.assignment_id
        LEFT JOIN nested_dtsen_var v ON d.assignment_id = v.assignment_id AND (v.no_art = '1' OR v.no_art = 1)
        WHERE b.level_6_full_code IN ({in_clause})
          AND b.assignment_status_alias != 'DRAFT'
        ORDER BY b.level_6_full_code ASC, d.no_urut_bangunan ASC
        LIMIT 1000 OFFSET 0;
        """
        
        print(f"🔄 [Fetching Chunk {i//chunk_size + 1}/{(len(sls_list) + chunk_size - 1)//chunk_size}] Tarik data {len(batch)} SLS...")
        cmd = ["node", "src/execute-query.js", sql]
        try:
            res = subprocess.run(cmd, cwd=FASIH_SYNC_DIR, capture_output=True, text=True, check=True)
            stdout = res.stdout
            
            # Ekstrak JSON Array dari output stdout runner
            json_lines = []
            in_json = False
            for line in stdout.splitlines():
                if line.strip().startswith("[") and not in_json and ("{" in line or line.strip() == "["):
                    in_json = True
                    json_lines.append(line)
                elif in_json:
                    json_lines.append(line)
                    if line.strip() == "]" or line.strip().endswith("]"):
                        break
            
            if json_lines:
                rows = json.loads("\n".join(json_lines))
                print(f"   🟢 Berhasil mendapatkan {len(rows)} baris data responden.")
                all_rows.extend(rows)
            else:
                print("   ⚠️ Peringatan: Tidak ada data JSON terurai dari output.")
        except Exception as e:
            print(f"   ❌ Error saat menarik chunk: {e}")

    return all_rows


def main():
    print("==========================================================================================")
    print("🚀 [EXTRACT SAKERNAS INTERSECT DATA] PENARIKAN DATA KELUARGA IRISAN SE2026 UNTUK SAKERNAS")
    print("==========================================================================================\n")
    
    rows = fetch_sqllab_intersect_data(SAMPLE_SLS_CODES)
    if not rows:
        print("❌ Tidak ada data yang berhasil ditarik.")
        return

    # Tentukan header CSV baku sesuai permintaan Vaya
    fieldnames = [
        "sls",
        "nama_sls",
        "kecamatan",
        "nama_kepala_keluarga",
        "no_urut_bangunan",
        "keberadaan_keluarga",
        "pendidikan_krt",
        "no_hp"
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
                "no_urut_bangunan": r.get("no_urut_bangunan", ""),
                "keberadaan_keluarga": r.get("keberadaan_keluarga", ""),
                "pendidikan_krt": r.get("pendidikan_krt", ""),
                "no_hp": r.get("no_hp", "-") or "-"
            })

    print(f"\n💾 [HASIL EKSPOR] {len(rows)} data keluarga berhasil diekstrak dan disimpan ke:")
    print(f"   📁 {OUTPUT_CSV}")
    print("\n==========================================================================================")


if __name__ == "__main__":
    main()
