"""kb/cmd_sync_sheets.py — Implementasi perintah `kb sync-sheets`."""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

from .colors import Colors
from .utils import load_env, slugify
from .markdown_io import read_markdown_file
from .google_sheets import get_sheets_service, push_rows, push_readme_tab, ensure_sheet_tab

MILESTONES_HEADERS = [
    'activity_id', 
    'kategori', 
    'tanggal', 
    'kegiatan', 
    'status', 
    'pic', 
    'attributes_json'
]

METRICS_HEADERS = [
    'activity_id',
    'metric_id',
    'label',
    'target',
    'completed',
    'worked',
    'percentage',
    'context_json'
]

def cmd_sync_sheets(args) -> None:
    """Memindai seluruh kegiatan lokal dan mengunggahnya ke Google Sheets."""
    config = load_env()
    spreadsheet_id = config.get("SPREADSHEET_ID", "").strip('"\'')
    
    if not spreadsheet_id:
        print(f"{Colors.FAIL}Error: SPREADSHEET_ID tidak ditemukan di berkas .env!{Colors.ENDC}")
        print("Silakan tambahkan: SPREADSHEET_ID=\"ID_SPREADSHEET_ANDA\" ke berkas .env")
        sys.exit(1)
        
    print(f"{Colors.BLUE}Memulai pemindaian kegiatan lokal...{Colors.ENDC}")
    
    milestones_rows = []
    
    # Pindai seluruh README.md di folder kegiatan/ secara rekursif
    kegiatan_dir = Path("kegiatan")
    if not kegiatan_dir.exists():
        print(f"{Colors.FAIL}Error: Direktori 'kegiatan' tidak ditemukan!{Colors.ENDC}")
        sys.exit(1)
        
    readme_files = list(kegiatan_dir.glob("**/README.md"))
    print(f"Ditemukan {len(readme_files)} berkas README.md.")
    
    for path in readme_files:
        # Lewati root kegiatan/README.md jika ada
        if path.parent == kegiatan_dir:
            continue
            
        try:
            metadata, body = read_markdown_file(path)
            if not metadata:
                continue
                
            activity_name = metadata.get("nama", path.parent.parent.name)
            activity_id = slugify(activity_name)
            kategori = metadata.get("kategori", "non-survey")
            pic = metadata.get("peran", "anggota")
            
            deadlines = metadata.get("deadlines", [])
            if not isinstance(deadlines, list):
                continue
                
            for deadline in deadlines:
                if not isinstance(deadline, dict):
                    continue
                    
                tanggal = deadline.get("tanggal", "")
                keg_desc = deadline.get("kegiatan", "")
                status = deadline.get("status", "belum")
                
                # Buat atribut kustom dalam JSON
                attr = {
                    "activity_name": activity_name,
                    "rutinitas": metadata.get("rutinitas", "rutin"),
                    "frekuensi": metadata.get("frekuensi", "bulanan"),
                    "path": path.as_posix()
                }
                
                # Masukkan semua detail tambahan dari deadline
                for k, v in deadline.items():
                    if k not in ["tanggal", "kegiatan", "status"]:
                        attr[k] = v
                
                # Deteksi kelompok latsar secara cerdas jika ada di dalam deskripsi kegiatan
                if "kelompok" in keg_desc.lower():
                    m = re.search(r'(?:kelompok|kel\.)\s*(\d+)', keg_desc, re.I)
                    if m:
                        attr["kelompok"] = int(m.group(1))
                        
                milestones_rows.append([
                    activity_id,
                    kategori,
                    tanggal,
                    keg_desc,
                    status,
                    pic,
                    json.dumps(attr)
                ])
        except Exception as e:
            print(f"{Colors.WARNING}Gagal membaca {path}: {e}{Colors.ENDC}")

    # Urutkan baris berdasarkan tanggal untuk keterbacaan yang rapi di Google Sheets
    # Tanggal kosong diletakkan di akhir
    milestones_rows.sort(key=lambda x: x[2] if x[2] else "9999-12-31")

    print(f"Berhasil mengumpulkan {len(milestones_rows)} milestones.")
    
    # Inisialisasi API Google Sheets
    try:
        service = get_sheets_service()
        print(f"{Colors.BLUE}Menghubungkan ke Google Sheets dengan ID: {spreadsheet_id}...{Colors.ENDC}")
        
        # Lakukan push README
        push_readme_tab(service, spreadsheet_id)
        
        # Pastikan tab unified_metrics terbuat (meski kosong) agar sesuai dokumentasi
        ensure_sheet_tab(service, spreadsheet_id, "unified_metrics", METRICS_HEADERS)
        
        # Lakukan push ke Google Sheets
        push_rows(
            service=service,
            spreadsheet_id=spreadsheet_id,
            title="unified_milestones",
            headers=MILESTONES_HEADERS,
            rows=milestones_rows
        )
        
        print(f"{Colors.GREEN}🎉 SINKRONISASI SELESAI DENGAN SUKSES!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Sinkronisasi gagal: {e}{Colors.ENDC}")
        sys.exit(1)
