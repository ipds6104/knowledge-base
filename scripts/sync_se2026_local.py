#!/usr/bin/env python3
"""
Sync & Local Database Engine untuk SE2026 (SurrealDB -> SQLite WAL Single Source of Truth Mirror)

Fitur:
- Dump & Mirror data dari SurrealDB (100.88.216.97:8900) ke SQLite lokal (/app/shared_data/se2026_local.db)
- Dukungan mode WAL (Write-Ahead Logging) super cepat & tahan gangguan listrik
- Incremental Upsert (INSERT OR REPLACE) per SLS, per Desa, atau All
- Menyimpan field terstruktur penting + raw JSON lengkap untuk zero-loss data
- Mengaitkan koordinat latitude/longitude dari tabel assignment
- Interface query lokal offline sub-milidetik
"""

import sys
import os
import json
import sqlite3
import argparse
import urllib.request
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional

SURREAL_URL = os.environ.get("SURREAL_URL", "http://100.88.216.97:8900/sql")
SURREAL_NS = os.environ.get("SURREAL_NS", "bps_mempawah")
SURREAL_DB = os.environ.get("SURREAL_DB", "se2026")
AUTH_USER = os.environ.get("AUTH_USER", "root")
AUTH_PASS = os.environ.get("AUTH_PASS", "root")

DB_DIR = "/app/shared_data"
DB_PATH = os.path.join(DB_DIR, "se2026_local.db")

def get_surreal_headers() -> Dict[str, str]:
    auth_str = f"{AUTH_USER}:{AUTH_PASS}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {auth_b64}",
        "surreal-ns": SURREAL_NS,
        "surreal-db": SURREAL_DB,
        "Accept": "application/json",
        "Content-Type": "text/plain"
    }

def query_surreal(sql: str, timeout: int = 60) -> List[Dict[str, Any]]:
    headers = get_surreal_headers()
    req = urllib.request.Request(SURREAL_URL, data=sql.encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and len(data) > 0 and data[0].get("result") is not None:
                return data[0]["result"]
            return []
    except Exception as e:
        print(f"[Surreal Error]: {e}", file=sys.stderr)
        return []

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS se2026_nested (
                id TEXT PRIMARY KEY,
                assignment_id TEXT,
                level_4_full_code TEXT,
                level_6_full_code TEXT,
                level_6_name TEXT,
                nama_usaha TEXT,
                pengusaha TEXT,
                keberadaan_usaha_value TEXT,
                keberadaan_usaha_label TEXT,
                kategori TEXT,
                kbli_akhir TEXT,
                kbli_label TEXT,
                keg_utama TEXT,
                produk TEXT,
                total_tk_bayar INTEGER DEFAULT 0,
                total_tk_jk INTEGER DEFAULT 0,
                tk_dibayar INTEGER DEFAULT 0,
                tk_tdk_dibayar INTEGER DEFAULT 0,
                tk_laki INTEGER DEFAULT 0,
                tk_pr INTEGER DEFAULT 0,
                total_pendapatan REAL DEFAULT 0,
                total_pengeluaran REAL DEFAULT 0,
                hp TEXT,
                no_bang_l TEXT,
                sls_l TEXT,
                skala_usaha TEXT,
                raw_json TEXT,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assignment_geo (
                id TEXT PRIMARY KEY,
                level_6_full_code TEXT,
                level_6_name TEXT,
                nama_kk TEXT,
                no_kk TEXT,
                nik TEXT,
                jalan_domisili TEXT,
                no_bang TEXT,
                latitude REAL,
                longitude REAL,
                raw_json TEXT,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scope TEXT,
                records_synced INTEGER,
                status TEXT,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Indexes
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sls ON se2026_nested (level_6_full_code);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_desa ON se2026_nested (level_4_full_code);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON se2026_nested (keberadaan_usaha_value);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_asgn_id ON se2026_nested (assignment_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_geo_sls ON assignment_geo (level_6_full_code);")

    return conn

def safe_int(val: Any) -> int:
    try:
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return 0

def safe_float(val: Any) -> float:
    try:
        return float(str(val).strip())
    except (ValueError, TypeError):
        return 0.0

def sync_sls_list(sls_list: List[str], conn: sqlite3.Connection) -> int:
    sls_str = ", ".join(f"'{s}'" for s in sls_list)
    print(f"[*] Mengambil data se2026_nested untuk {len(sls_list)} SLS dari SurrealDB...")
    
    sql = f"SELECT * FROM se2026_nested WHERE level_6_full_code IN [{sls_str}];"
    records = query_surreal(sql, timeout=45)
    
    if not records:
        print("[!] Tidak ada record yang ditemukan atau kueri gagal.")
        return 0

    print(f"[*] Ditemukan {len(records)} record usaha. Menyimpan ke database lokal SQLite...")
    
    assignment_ids = set()
    rows_to_insert = []
    
    for r in records:
        rid = str(r.get("id", ""))
        # assignment_id is the part before the last underscore if it follows the pattern 'se2026_nested:UUID_idx'
        asgn_id = ""
        clean_id = rid.replace("se2026_nested:", "")
        if "_" in clean_id:
            asgn_id = clean_id.rsplit("_", 1)[0]
            assignment_ids.add(asgn_id)
        
        row = (
            rid,
            asgn_id,
            str(r.get("level_4_full_code", "") or ""),
            str(r.get("level_6_full_code", "") or ""),
            str(r.get("level_6_name", "") or ""),
            str(r.get("nama_usaha", "") or ""),
            str(r.get("pengusaha_var_label", "") or r.get("pengusaha", "") or ""),
            str(r.get("keberadaan_usaha_value", "") or ""),
            str(r.get("keberadaan_usaha_label", "") or ""),
            str(r.get("kategori", "") or r.get("kategori_2025", "") or ""),
            str(r.get("kbli_akhir", "") or r.get("kbli_value", "") or ""),
            str(r.get("kbli_label", "") or ""),
            str(r.get("keg_utama", "") or ""),
            str(r.get("produk", "") or ""),
            safe_int(r.get("total_tk_bayar", 0)),
            safe_int(r.get("total_tk_jk", 0)),
            safe_int(r.get("tk_dibayar", 0)),
            safe_int(r.get("tk_tdk_dibayar", 0)),
            safe_int(r.get("tk_laki", 0)),
            safe_int(r.get("tk_pr", 0)),
            safe_float(r.get("total_pendapatan", 0)),
            safe_float(r.get("total_pengeluaran", 0)),
            str(r.get("hp", "") or r.get("no_telp", "") or ""),
            str(r.get("no_bang_l", "") or ""),
            str(r.get("sls_l", "") or ""),
            str(r.get("skala_usaha", "") or ""),
            json.dumps(r, ensure_ascii=False),
            datetime.now().isoformat()
        )
        rows_to_insert.append(row)

    with conn:
        conn.executemany("""
            INSERT OR REPLACE INTO se2026_nested (
                id, assignment_id, level_4_full_code, level_6_full_code, level_6_name,
                nama_usaha, pengusaha, keberadaan_usaha_value, keberadaan_usaha_label,
                kategori, kbli_akhir, kbli_label, keg_utama, produk,
                total_tk_bayar, total_tk_jk, tk_dibayar, tk_tdk_dibayar, tk_laki, tk_pr,
                total_pendapatan, total_pengeluaran, hp, no_bang_l, sls_l, skala_usaha,
                raw_json, synced_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, rows_to_insert)

    print(f"[✓] Berhasil menyimpan {len(rows_to_insert)} usaha ke tabel lokal se2026_nested.")

    # Sinkronkan Geotag & Info Keluarga dari assignment
    if assignment_ids:
        print(f"[*] Mengambil geotag & metadata keluarga untuk {len(assignment_ids)} assignment...")
        asgn_list = list(assignment_ids)
        chunk_size = 50
        geo_rows = []
        
        for i in range(0, len(asgn_list), chunk_size):
            chunk = asgn_list[i:i+chunk_size]
            # Build assignment table query
            queries = "; ".join(f"SELECT * FROM assignment:⟨{aid}⟩" for aid in chunk)
            res = query_surreal(queries, timeout=45)
            # When multiple queries are sent separated by semicolon, res is a list of results
            # Each result has status and result
            headers = get_surreal_headers()
            req = urllib.request.Request(SURREAL_URL, data=queries.encode("utf-8"), headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    multi_res = json.loads(resp.read().decode("utf-8"))
                    for qres in multi_res:
                        item_list = qres.get("result", [])
                        if item_list and isinstance(item_list, list):
                            item = item_list[0]
                            aid = str(item.get("id", "")).replace("assignment:", "").replace("⟨", "").replace("⟩", "")
                            lat = safe_float(item.get("root_geotag_latitude"))
                            lng = safe_float(item.get("root_geotag_longitude"))
                            geo_rows.append((
                                aid,
                                str(item.get("root_level_6_full_code", "") or ""),
                                str(item.get("root_level_6_name", "") or ""),
                                str(item.get("root_nama_kk", "") or ""),
                                str(item.get("root_no_kk", "") or ""),
                                str(item.get("root_nik", "") or ""),
                                str(item.get("root_jalan_domisili", "") or ""),
                                str(item.get("root_no_bang", "") or ""),
                                lat,
                                lng,
                                json.dumps(item, ensure_ascii=False),
                                datetime.now().isoformat()
                            ))
            except Exception as e:
                print(f"[!] Error syncing chunk assignments: {e}", file=sys.stderr)

        if geo_rows:
            with conn:
                conn.executemany("""
                    INSERT OR REPLACE INTO assignment_geo (
                        id, level_6_full_code, level_6_name, nama_kk, no_kk, nik,
                        jalan_domisili, no_bang, latitude, longitude, raw_json, synced_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, geo_rows)
            print(f"[✓] Berhasil menyimpan {len(geo_rows)} titik geotag & keluarga ke assignment_geo.")

    with conn:
        conn.execute("""
            INSERT INTO sync_history (scope, records_synced, status)
            VALUES (?, ?, ?);
        """, (f"{len(sls_list)} SLS", len(rows_to_insert), "SUCCESS"))

    return len(rows_to_insert)

def show_stats(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM se2026_nested;")
    total_usaha = cur.fetchone()[0]
    
    cur.execute("SELECT keberadaan_usaha_label, count(*) FROM se2026_nested GROUP BY keberadaan_usaha_label;")
    status_breakdown = cur.fetchall()
    
    cur.execute("SELECT count(*) FROM assignment_geo;")
    total_geo = cur.fetchone()[0]

    cur.execute("SELECT count(DISTINCT level_6_full_code) FROM se2026_nested;")
    total_sls = cur.fetchone()[0]

    print("=" * 60)
    print("📊 STATISTIK LOCAL DATABASE SE2026 (SQLite WAL Mirror)")
    print("=" * 60)
    print(f"Path Database   : {DB_PATH}")
    print(f"Total Unit Usaha: {total_usaha:,} record")
    print(f"Total Geotag KK : {total_geo:,} keluarga/bangunan")
    print(f"Total SLS       : {total_sls:,} SLS")
    print("-" * 60)
    print("Rincian Keberadaan Usaha:")
    for lbl, cnt in status_breakdown:
        print(f"  • {lbl or '(Kosong)'}: {cnt:,} usaha")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="SE2026 SurrealDB -> Local SQLite Sync Engine")
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-perintah")
    
    # sync
    sync_p = subparsers.add_parser("sync", help="Sinkronkan data dari SurrealDB ke SQLite lokal")
    sync_p.add_argument("--sls", nargs="+", help="Daftar 16-digit kode SLS yang ingin disinkronkan")
    sync_p.add_argument("--desa", help="10-digit kode desa (misal: 6104091006)")
    
    # stats
    subparsers.add_parser("stats", help="Tampilkan statistik database lokal")

    # query
    query_p = subparsers.add_parser("query", help="Jalankan kueri SQL langsung ke database lokal")
    query_p.add_argument("sql", help="SQL string")
    query_p.add_argument("--json", action="store_true", help="Print json")

    args = parser.parse_args()
    conn = init_db()

    if args.cmd == "sync":
        if args.sls:
            sync_sls_list(args.sls, conn)
        elif args.desa:
            # Query all SLS under this desa from SurrealDB
            desa_sql = f"SELECT level_6_full_code FROM se2026_nested WHERE level_4_full_code = '{args.desa}' GROUP BY level_6_full_code;"
            res = query_surreal(desa_sql)
            sls_codes = [r["level_6_full_code"] for r in res if r.get("level_6_full_code")]
            print(f"[*] Ditemukan {len(sls_codes)} SLS di desa {args.desa}.")
            sync_sls_list(sls_codes, conn)
        else:
            print("[!] Harap tentukan --sls atau --desa")
            sys.exit(1)
        show_stats(conn)
    elif args.cmd == "stats":
        show_stats(conn)
    elif args.cmd == "query":
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute(args.sql)
            rows = [dict(r) for r in cur.fetchall()]
            if args.json:
                print(json.dumps(rows, indent=2, ensure_ascii=False))
            else:
                print(f"Total baris: {len(rows)}")
                for r in rows[:15]:
                    print(r)
                if len(rows) > 15:
                    print(f"... dan {len(rows) - 15} baris lainnya.")
        except Exception as e:
            print(f"SQL Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
