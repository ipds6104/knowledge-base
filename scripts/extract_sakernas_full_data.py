#!/usr/bin/env python3
"""
Full Zero-Pruning Extractor for Sakernas Agustus 2026 (Kabupaten Mempawah - 6104).
Bypasses Superset's 25-column restriction via deterministic Column-Chunking.
Pulls 100% of columns without leaving a single column behind across all core tables:
- art_roster (637 cols, 1756 rows)
- root_table (120 cols, 479 rows)
- base_table_assignment (86 cols, 479 rows)
- petugas (21 cols, 479 rows)
And produces an integrated master dataset.
"""

import csv
import json
import os
import random
import re
import string
import sys
import time
import requests
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "kegiatan", "sakernas", "2026-08", "raw_data")
METADATA_FILE = os.path.join(BASE_DIR, "kegiatan", "sakernas", "2026-08", "metadata_tables_sakernas.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPERSET_URL = "https://fasih-dashboard.bps.go.id/api/v1/sqllab/execute/"
DATABASE_ID = 15
SCHEMA = "tok_3fd42e0e"
KODE_KAB = "04"  # Mempawah


def rand_str(n=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def save_rows_to_excel(fieldnames, rows, output_path):
    """Menyimpan list of dicts ke XLSX menggunakan mode write_only yang cepat dan hemat RAM."""
    wb = openpyxl.Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(fieldnames)
    for r in rows:
        row_vals = []
        for f in fieldnames:
            v = r.get(f)
            if v is not None and isinstance(v, str):
                v = ILLEGAL_CHARACTERS_RE.sub("", v)
            row_vals.append(v)
        ws.append(row_vals)
    wb.save(output_path)


def get_active_session():
    """Mengambil session cookie dan CSRF token dari active_sakernas_session.json."""
    active_json = os.path.join(BASE_DIR, "data", "cookies", "active_sakernas_session.json")
    if os.path.exists(active_json):
        with open(active_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["cookie_str"], data["csrf_token"]

    raise RuntimeError("File active_sakernas_session.json tidak ditemukan.")


def execute_query(sql, cookie_str, csrf_token, max_retries=3):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "cookie": cookie_str,
        "origin": "https://fasih-dashboard.bps.go.id",
        "referer": "https://fasih-dashboard.bps.go.id/superset/sqllab",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "x-csrftoken": csrf_token
    }

    for attempt in range(1, max_retries + 1):
        payload = {
            "client_id": rand_str(10),
            "database_id": DATABASE_ID,
            "json": True,
            "runAsync": False,
            "schema": SCHEMA,
            "sql": sql,
            "sql_editor_id": "1037101",
            "tab": "Zero Pruning Extractor",
            "select_as_cta": False,
            "ctas_method": "TABLE",
            "queryLimit": 9000,
            "expand_data": True
        }

        try:
            r = requests.post(SUPERSET_URL, headers=headers, json=payload, timeout=90)
            if r.status_code == 429:
                wait_sec = attempt * 15
                print(f"⚠️ [HTTP 429 Rate Limit] Menunggu {wait_sec}s sebelum retry...")
                time.sleep(wait_sec)
                continue

            if r.status_code != 200:
                print(f"⚠️ HTTP {r.status_code}: {r.text[:300]}")
                time.sleep(3)
                continue

            res = r.json()
            if "data" in res:
                return res["data"]
            elif "errors" in res:
                print(f"❌ SQLLab Error: {res['errors']}")
                time.sleep(3)
        except Exception as e:
            print(f"⚠️ Request exception: {e}")
            time.sleep(3)

    raise RuntimeError("Gagal mengeksekusi query setelah retry.")


def extract_table_full(table_name, key_cols, filter_clause, all_cols, cookie_str, csrf_token, chunk_size=22, custom_from=None):
    print(f"\n========================================================")
    print(f"🚀 Memulai Ekstraksi: {table_name}")
    print(f"   Total Kolom: {len(all_cols)} | Key: {key_cols}")
    print(f"========================================================")

    from_clause = custom_from if custom_from else f"{SCHEMA}.{table_name}"
    prefix = "t." if custom_from else ""

    # TRIK TUNGGAL: Gunakan MSSQL FOR JSON PATH untuk bypass limit 25 kolom Superset dalam 1 request!
    # Superset hanya melihat 2-3 kolom di outer SELECT, sementara database mengemas 100% kolom ke JSON.
    use_fast_json = True
    final_rows = []

    if use_fast_json:
        try:
            print(f"   ⚡ [FAST-JSON] Menarik seluruh {len(all_cols)} kolom dalam 1 request...", end="", flush=True)
            key_select = ", ".join(f"{prefix}[{k}]" for k in key_cols)
            inner_cols = ",\n        ".join(f"{prefix}[{c}]" for c in all_cols)
            
            sql = f"""
            SELECT 
              {key_select},
              (
                SELECT {inner_cols}
                FOR JSON PATH, WITHOUT_ARRAY_WRAPPER, INCLUDE_NULL_VALUES
              ) AS [raw_json]
            FROM {from_clause}
            {filter_clause}
            ORDER BY {', '.join(f'{prefix}[{k}] ASC' for k in key_cols)};
            """
            
            t0 = time.time()
            raw_data = execute_query(sql, cookie_str, csrf_token)
            t1 = time.time()
            print(f" ✓ ({len(raw_data)} baris dalam {t1 - t0:.2f}s)")

            for r in raw_data:
                raw_json_str = r.get("raw_json")
                if raw_json_str:
                    row_data = json.loads(raw_json_str)
                else:
                    row_data = {c: None for c in all_cols}
                
                # Pastikan key columns terisi
                for k in key_cols:
                    if k in r and row_data.get(k) is None:
                        row_data[k] = r[k]
                final_rows.append(row_data)

        except Exception as e:
            print(f"\n   ⚠️ Fast-JSON gagal ({e}), beralih ke mode fallback Chunking...")
            final_rows = []

    # Fallback jika Fast-JSON tidak mengembalikan data
    if not final_rows:
        non_key_cols = [c for c in all_cols if c not in key_cols]
        chunks = []
        for i in range(0, len(non_key_cols), chunk_size):
            chunks.append(non_key_cols[i:i + chunk_size])

        merged_data = {}  # key_tuple -> dict of all columns
        total_chunks = len(chunks)

        for idx, chunk in enumerate(chunks, 1):
            select_cols = key_cols + chunk
            cols_str = ",\n  ".join(f"{prefix}[{c}]" for c in select_cols)

            sql = f"""
            SELECT 
              {cols_str}
            FROM {from_clause}
            {filter_clause}
            ORDER BY {', '.join(f'{prefix}[{k}] ASC' for k in key_cols)};
            """

            print(f"   [{idx}/{total_chunks}] Mengambil {len(chunk)} kolom ({chunk[0]} s.d. {chunk[-1]})...", end="", flush=True)
            t0 = time.time()
            rows = execute_query(sql, cookie_str, csrf_token)
            t1 = time.time()
            print(f" ✓ ({len(rows)} baris, {t1 - t0:.2f}s)")

            for r in rows:
                if len(key_cols) == 1:
                    k = r[key_cols[0]]
                else:
                    k = tuple(r[kc] for kc in key_cols)

                if k not in merged_data:
                    merged_data[k] = {}

                for c in select_cols:
                    merged_data[k][c] = r.get(c)

            time.sleep(1.2)

        final_rows = list(merged_data.values())

    print(f"✓ Selesai! Total baris terkumpul: {len(final_rows)}, total kolom: {len(all_cols)}")

    # Simpan ke CSV
    csv_file = os.path.join(OUTPUT_DIR, f"{table_name}_mempawah_full_{len(all_cols)}cols.csv")
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_cols)
        writer.writeheader()
        writer.writerows(final_rows)
    print(f"💾 File CSV tersimpan : {csv_file}")

    # Simpan ke XLSX
    xlsx_file = os.path.join(OUTPUT_DIR, f"{table_name}_mempawah_full_{len(all_cols)}cols.xlsx")
    save_rows_to_excel(all_cols, final_rows, xlsx_file)
    print(f"💾 File XLSX tersimpan: {xlsx_file}")

    # Simpan ke JSON
    json_file = os.path.join(OUTPUT_DIR, f"{table_name}_mempawah_full_{len(all_cols)}cols.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(final_rows, f, ensure_ascii=False, indent=2)
    print(f"💾 File JSON tersimpan: {json_file}")

    return final_rows


def main():
    cookie_str, csrf_token = get_active_session()
    print("🔑 Sesi aktif berhasil dimuat.")

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # 1. Base Table Assignment (86 Kolom)
    assignment_cols = metadata["base_table_assignment"]["columns"]
    assignment_rows = extract_table_full(
        table_name="base_table_assignment",
        key_cols=["id"],
        filter_clause=f"WHERE level_2_code = '{KODE_KAB}'",
        all_cols=assignment_cols,
        cookie_str=cookie_str,
        csrf_token=csrf_token
    )

    # 2. Petugas (21 Kolom)
    petugas_cols = metadata["petugas"]["columns"]
    petugas_rows = extract_table_full(
        table_name="petugas",
        key_cols=["assignment_id"],
        filter_clause=f"WHERE b.level_2_code = '{KODE_KAB}'",
        all_cols=petugas_cols,
        cookie_str=cookie_str,
        csrf_token=csrf_token,
        custom_from=f"{SCHEMA}.petugas t JOIN {SCHEMA}.base_table_assignment b ON t.assignment_id = b.id"
    )

    # 3. Root Table (120 Kolom)
    root_cols = metadata["root_table"]["columns"]
    root_rows = extract_table_full(
        table_name="root_table",
        key_cols=["assignment_id"],
        filter_clause=f"WHERE level_2_code = '{KODE_KAB}'",
        all_cols=root_cols,
        cookie_str=cookie_str,
        csrf_token=csrf_token
    )

    # 4. ART Roster (637 Kolom)
    art_cols = metadata["art_roster"]["columns"]
    art_rows = extract_table_full(
        table_name="art_roster",
        key_cols=["assignment_id", "ppno"],
        filter_clause=f"WHERE level_2_code = '{KODE_KAB}'",
        all_cols=art_cols,
        cookie_str=cookie_str,
        csrf_token=csrf_token
    )

    # 5. Build Master Flat Dataset (Joined)
    print("\n========================================================")
    print("🔄 Menyusun Master Flat Dataset Terpadu (ART + RT + Assignment + Petugas)...")
    print("========================================================")

    # Indexing
    assignment_map = {r["id"]: r for r in assignment_rows}
    petugas_map = {r["assignment_id"]: r for r in petugas_rows}
    root_map = {r["assignment_id"]: r for r in root_rows}

    master_rows = []
    # Prefixing duplicate column names to maintain 100% data integrity
    master_fieldnames = []

    # Art roster columns first
    for col in art_cols:
        if col not in master_fieldnames:
            master_fieldnames.append(col)

    # Root table columns
    root_col_map = {}
    for col in root_cols:
        if col == "assignment_id":
            continue
        mapped = f"rt_{col}" if col in master_fieldnames else col
        root_col_map[col] = mapped
        if mapped not in master_fieldnames:
            master_fieldnames.append(mapped)

    # Assignment columns
    assign_col_map = {}
    for col in assignment_cols:
        if col == "id":
            continue
        mapped = f"assign_{col}" if col in master_fieldnames else col
        assign_col_map[col] = mapped
        if mapped not in master_fieldnames:
            master_fieldnames.append(mapped)

    # Petugas columns
    petugas_col_map = {}
    for col in petugas_cols:
        if col == "assignment_id":
            continue
        mapped = f"petugas_{col}" if col in master_fieldnames else col
        petugas_col_map[col] = mapped
        if mapped not in master_fieldnames:
            master_fieldnames.append(mapped)

    for art in art_rows:
        aid = art.get("assignment_id")
        flat = dict(art)

        # Merge root
        rt = root_map.get(aid, {})
        for orig, mapped in root_col_map.items():
            flat[mapped] = rt.get(orig)

        # Merge assignment
        asg = assignment_map.get(aid, {})
        for orig, mapped in assign_col_map.items():
            flat[mapped] = asg.get(orig)

        # Merge petugas
        ptg = petugas_map.get(aid, {})
        for orig, mapped in petugas_col_map.items():
            flat[mapped] = ptg.get(orig)

        master_rows.append(flat)

    master_csv = os.path.join(OUTPUT_DIR, "sakernas_agustus_2026_mempawah_master_flat.csv")
    with open(master_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=master_fieldnames)
        writer.writeheader()
        writer.writerows(master_rows)

    master_xlsx = os.path.join(OUTPUT_DIR, "sakernas_agustus_2026_mempawah_master_flat.xlsx")
    save_rows_to_excel(master_fieldnames, master_rows, master_xlsx)

    print(f"🎉 MASTER DATASET SELESAI!")
    print(f"   Jumlah ART (Baris) : {len(master_rows)}")
    print(f"   Total Kolom Unik   : {len(master_fieldnames)} kolom")
    print(f"   File Master CSV    : {master_csv}")
    print(f"   File Master XLSX   : {master_xlsx}")

    if "--no-upload" not in sys.argv:
        print("\n☁️ [GOOGLE DRIVE] Memulai sinkronisasi otomatis ke Google Drive...")
        sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
        import upload_sakernas_to_gdrive
        upload_sakernas_to_gdrive.main()


if __name__ == "__main__":
    main()
