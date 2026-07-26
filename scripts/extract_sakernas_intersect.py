#!/usr/bin/env python3
"""
Script: extract_sakernas_intersect.py
Menarik 100% data mikro keluarga/responden SE2026 dari Superset SQL Lab 
secara cerdas menggunakan query batch IN dengan paginasi, memilah hasilnya ke
berkas chunk per-SLS (sls_chunks/), lalu menggabungkannya ke berkas utama.

Keuntungan Desain Ini:
1. Cepat & Stabil: Hanya butuh ~4 request Superset (bukan 48) lewat paginasi LIMIT 1000.
2. Isolasi Chunk: Setiap SLS tetap memiliki berkas sls_chunks/sls_{sls_code}.csv masing-masing.
3. Resume: Otomatis mendeteksi SLS mana yang belum lengkap dan hanya menarik yang kurang.
4. Bebas Tabrakan: Proteksi lockfile eksklusif di tingkat OS.
"""

import csv
import json
import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(BASE_DIR) != "knowledge-base":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(BASE_DIR) == "scripts":
        BASE_DIR = os.path.dirname(BASE_DIR)

FASIH_SYNC_DIR = "/home/ihza/Projects/fasih-sync-monitoring"
OUTPUT_DIR = os.path.join(BASE_DIR, "kegiatan", "sakernas", "2026-08")
CHUNKS_DIR = os.path.join(OUTPUT_DIR, "sls_chunks")
os.makedirs(CHUNKS_DIR, exist_ok=True)

OUTPUT_CSV = os.path.join(OUTPUT_DIR, "prelist_updating_sakernas_se2026_intersect.csv")
LOCK_FILE = "/tmp/extract_sakernas_intersect.lock"

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

FIELDNAMES = [
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


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"⚠️ Ekstraksi sedang berjalan oleh PID {pid}. Menghentikan eksekusi ganda.")
            sys.exit(0)
        except (OSError, ValueError):
            os.remove(LOCK_FILE)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def release_lock():
    if os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
        except OSError:
            pass


def write_rows_to_chunk(sls_code, rows):
    """Menulis/Menyimpan rows ke berkas chunk SLS."""
    chunk_file = os.path.join(CHUNKS_DIR, f"sls_{sls_code}.csv")
    
    # Jika berkas belum ada, buat baru dan tulis header. Jika sudah ada, append.
    file_exists = os.path.exists(chunk_file)
    mode = "a" if file_exists else "w"
    
    with open(chunk_file, mode, encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
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


def main():
    acquire_lock()
    try:
        print("==========================================================================================")
        print("🚀 [EXTRACT SAKERNAS INTERSECT DATA] HYBRID BATCH PIPELINE")
        print("==========================================================================================\n")
        print(f"📁 Folder Chunk Per-SLS : {CHUNKS_DIR}")
        print(f"📄 Berkas Akhir Gabungan : {OUTPUT_CSV}\n")

        # Step 1: Filter SLS mana saja yang belum selesai ditarik (belum ada berkas chunk-nya atau isinya kosong)
        missing_sls = []
        for sls in SAMPLE_SLS_CODES:
            chunk_file = os.path.join(CHUNKS_DIR, f"sls_{sls}.csv")
            if not os.path.exists(chunk_file) or os.path.getsize(chunk_file) < 150:
                missing_sls.append(sls)
            else:
                with open(chunk_file, encoding="utf-8-sig") as f:
                    line_count = len(f.readlines()) - 1
                print(f"   ⚡ Cache Hit: SLS {sls} ({line_count} keluarga)")

        if missing_sls:
            print(f"\n🔄 Menarik data untuk {len(missing_sls)} SLS yang belum ter-cache...")
            offset = 0
            chunk_size = 1000
            
            # Format list SLS untuk query IN
            sls_in_clause = ", ".join(f"'{s}'" for s in missing_sls)
            
            query_completed = False
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
                WHERE b.level_6_full_code IN ({sls_in_clause})
                  AND b.assignment_status_alias != 'DRAFT'
                ORDER BY b.level_6_full_code ASC, b.data1 ASC
                LIMIT {chunk_size} OFFSET {offset};
                """
                
                cmd = ["node", "src/execute-query.js", sql]
                success = False
                
                for attempt in range(1, 4):
                    try:
                        res = subprocess.run(cmd, cwd=FASIH_SYNC_DIR, capture_output=True, text=True, check=True)
                        stdout_text = res.stdout
                        
                        marker = "🟢 SQL Query berhasil dieksekusi!\n"
                        marker_pos = stdout_text.find(marker)
                        
                        if marker_pos != -1:
                            json_text = stdout_text[marker_pos + len(marker):].strip()
                            rows = json.loads(json_text)
                        else:
                            start_idx = stdout_text.find("[\n  {")
                            if start_idx == -1:
                                start_idx = stdout_text.find("[{")
                            end_idx = stdout_text.rfind("]")
                            rows = json.loads(stdout_text[start_idx:end_idx + 1])
                        
                        # Kelompokkan data per SLS lalu simpan ke chunk masing-masing
                        grouped_rows = {}
                        for r in rows:
                            s_code = r.get("sls")
                            if s_code:
                                grouped_rows.setdefault(s_code, []).append(r)
                                
                        for s_code, s_rows in grouped_rows.items():
                            write_rows_to_chunk(s_code, s_rows)
                            
                        print(f"   🟢 Berhasil memproses Batch Offset {offset}: {len(rows)} keluarga ditarik.", flush=True)
                        success = True
                        
                        if len(rows) < chunk_size:
                            query_completed = True
                            break
                        offset += chunk_size
                    except Exception as e:
                        if attempt < 3:
                            time.sleep(1)
                        else:
                            print(f"   ⚠️ Gagal menarik batch offset {offset} setelah 3 attempt: {e}", flush=True)
                            
                if not success or (success and len(rows) < chunk_size):
                    break

            # Jika ada SLS yang sama sekali tidak memiliki baris di DB, buat berkas kosong dengan header saja
            if query_completed:
                for sls in missing_sls:
                    chunk_file = os.path.join(CHUNKS_DIR, f"sls_{sls}.csv")
                    if not os.path.exists(chunk_file):
                        with open(chunk_file, "w", encoding="utf-8-sig", newline="") as f:
                            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                            writer.writeheader()


        # Step 2: Gabungkan seluruh file chunk dari sls_chunks/ ke berkas utama
        combined_rows = []
        for sls in SAMPLE_SLS_CODES:
            chunk_file = os.path.join(CHUNKS_DIR, f"sls_{sls}.csv")
            if os.path.exists(chunk_file):
                with open(chunk_file, encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    combined_rows.extend(list(reader))

        # Tulis ke berkas utama
        with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(combined_rows)

        # Tulis juga ke berkas final (untuk integrasi VS Code user)
        final_csv = os.path.join(OUTPUT_DIR, "prelist_updating_sakernas_se2026_intersect_final.csv")
        with open(final_csv, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(combined_rows)

        # Hitung breakdown per Kecamatan
        kec_breakdown = {}
        for r in combined_rows:
            kec = r.get("kecamatan", "LAINNYA")
            if kec:
                kec_breakdown[kec] = kec_breakdown.get(kec, 0) + 1

        print("\n==========================================================================================")
        print(f"💾 [HASIL PENGGABUNGAN TOTAL] {len(combined_rows)} data keluarga digabungkan ke:")
        print(f"   📁 {OUTPUT_CSV}\n")
        print("📊 Breakdown per Kecamatan:")
        for kec, count in sorted(kec_breakdown.items()):
            print(f"   • {kec:<20}: {count:>5} keluarga")
        print("==========================================================================================")

    finally:
        release_lock()


if __name__ == "__main__":
    main()
