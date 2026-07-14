"""kb/cmd_latsar.py — Implementasi sinkronisasi jadwal Latsar CPNS."""

import sys
import re
import urllib.request
import csv
from datetime import datetime
from pathlib import Path

from .colors import Colors
from .markdown_io import read_markdown_file, write_markdown_file

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1wcbKrwwuC0x1sK4_6N39j_inC59uhPMx/"
    "export?format=csv&gid=801895514"
)

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "juli": 7, "agustus": 8, "oktober": 10, "nopember": 11, "desember": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6, "jul": 7, "agt": 8, "sep": 9, "okt": 10, "nov": 11, "des": 12
}

def parse_date(date_str):
    """Parse date string like '05 July 2026' to 'YYYY-MM-DD'."""
    date_str = date_str.strip().lower()
    m = re.match(r'(\d+)\s+([a-z]+)\s+(\d{4})', date_str)
    if m:
        day = int(m.group(1))
        month_name = m.group(2)
        year = int(m.group(3))
        month = MONTHS.get(month_name)
        if month:
            return f"{year:04d}-{month:02d}-{day:02d}"
    return None

def is_milestone(event_str):
    """Filter for key milestones/sync sessions to display in deadlines."""
    event_lower = event_str.lower()
    keywords = ["sync", "seminar", "check in", "pembimbingan", "agenda 1", "agenda 2", "agenda 3", "agenda iv"]
    if "async" in event_lower and not any(kw in event_lower for kw in ["coaching", "pembimbingan", "seminar", "agenda"]):
        return False
    return any(kw in event_lower for kw in keywords)

def cmd_latsar(args) -> None:
    """Unduh jadwal Latsar CPNS dari Google Sheets, ekstrak milestones, dan inisialisasi folder."""
    # 1. Inisialisasi folder dan file jika belum ada
    latsar_dir = Path("kegiatan/latsar-cpns/2026")
    readme_path = latsar_dir / "README.md"
    
    # Buat subdirektori CPNS
    cpns_list = [
        ("akma-batrisyia-jazima", "Akma Batrisyia Jazima"),
        ("cpns-dua", "CPNS Kedua")
    ]
    
    for slug, fullname in cpns_list:
        cpns_dir = latsar_dir / slug
        cpns_dir.mkdir(parents=True, exist_ok=True)
        
        # CPNS README.md
        cpns_readme = cpns_dir / "README.md"
        if not cpns_readme.exists():
            metadata = {
                "nama": f"Latsar CPNS - {fullname}",
                "kategori": "non-survey",
                "rutinitas": "non-rutin",
                "frekuensi": "ad-hoc",
                "peran": "anggota",
                "status": "aktif",
                "deadlines": []
            }
            body = (
                f"# Latsar CPNS — {fullname}\n\n"
                f"## Profil CPNS\n"
                f"*   **Nama Lengkap:** {fullname}\n"
                f"*   **NIP:** -\n"
                f"*   **Unit Kerja:** BPS Kabupaten Mempawah\n"
                f"*   **Golongan:** III/a\n"
                f"*   **Jabatan:** -\n"
                f"*   **Mentor:** -\n"
                f"*   **Coach:** -\n\n"
                f"## Rancangan Aktualisasi\n"
                f"*   **Isu yang Diangkat:** -\n"
                f"*   **Gagasan Kreatif:** -\n"
                f"*   **Tautan Dokumen:** [Rancangan Aktualisasi](rancangan-aktualisasi.md)\n\n"
                f"## Laporan Aktualisasi\n"
                f"*   **Tautan Dokumen:** [Laporan Aktualisasi](laporan-aktualisasi.md)\n"
            )
            write_markdown_file(cpns_readme, metadata, body)
            print(f"{Colors.BLUE}Inisialisasi README CPNS: {cpns_readme}{Colors.ENDC}")
            
        # rancangan-aktualisasi.md
        rancangan_file = cpns_dir / "rancangan-aktualisasi.md"
        if not rancangan_file.exists():
            rancangan_file.write_text(
                f"# Rancangan Aktualisasi — {fullname}\n\n"
                f"Dokumen usulan pemecahan isu aktualisasi di lingkungan BPS Kabupaten Mempawah.\n",
                encoding='utf-8'
            )
            
        # laporan-aktualisasi.md
        laporan_file = cpns_dir / "laporan-aktualisasi.md"
        if not laporan_file.exists():
            laporan_file.write_text(
                f"# Laporan Aktualisasi — {fullname}\n\n"
                f"Dokumen laporan hasil habituasi aktualisasi nilai-nilai dasar ASN BerAKHLAK.\n",
                encoding='utf-8'
            )
            
        # mentoring-log.md
        log_file = cpns_dir / "mentoring-log.md"
        if not log_file.exists():
            log_file.write_text(
                f"# Log Bimbingan/Mentoring — {fullname}\n\n"
                f"Gunakan tabel ini untuk mencatat sesi bimbingan dengan Mentor di BPS Kabupaten Mempawah.\n\n"
                f"| No | Hari/Tanggal | Catatan Masukan Mentor | Paraf/Status |\n"
                f"|----|--------------|------------------------|--------------|\n"
                f"| 1  |              |                        |              |\n",
                encoding='utf-8'
            )

    # 2. Download dan Parse Spreadsheet Latsar
    print(f"{Colors.BLUE}Mengunduh jadwal Latsar CPNS dari Google Sheets...{Colors.ENDC}")
    try:
        req = urllib.request.Request(SHEET_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            csv_text = response.read().decode('utf-8-sig')
            
        print(f"{Colors.GREEN}Sukses mengunduh jadwal.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error mengunduh jadwal Latsar: {e}{Colors.ENDC}")
        print("Menggunakan fallback/data statis yang sudah ada.")
        return

    # Parse rows
    reader = csv.reader(csv_text.splitlines())
    rows = list(reader)
    
    current_dates = [None] * 7
    schedule_data = {} # date -> list of events
    
    kelompok_str = f"kel. {args.kelompok}"
    
    for row in rows:
        while len(row) < 7:
            row.append("")
            
        is_date_row = False
        parsed_row_dates = []
        for cell in row:
            p_date = parse_date(cell)
            parsed_row_dates.append(p_date)
            if p_date:
                is_date_row = True
                
        if is_date_row:
            current_dates = parsed_row_dates
            continue
            
        for col_idx, cell in enumerate(row):
            date = current_dates[col_idx]
            if not date:
                continue
                
            cell_content = cell.strip()
            if not cell_content:
                continue
                
            lines = [l.strip() for l in cell_content.split('\n') if l.strip()]
            for line in lines:
                # Filter out other kelompok
                if any(f"kel. {g}" in line.lower() or f"kelompok {g}" in line.lower() for g in [1, 2, 3, 4] if g != args.kelompok):
                    if not (kelompok_str in line.lower() or f"kelompok {args.kelompok}" in line.lower()):
                        continue
                
                # Filter for milestones
                if is_milestone(line):
                    if date not in schedule_data:
                        schedule_data[date] = []
                    schedule_data[date].append(line)
                    
    # Tambahkan milestone manual penting jika tidak ada
    fixed_milestones = {
        "2026-08-02": ["Mulai Masa Aktualisasi/Habituasi (Off-Campus)"],
        "2026-09-12": ["Selesai Masa Aktualisasi/Habituasi (Off-Campus)"]
    }
    
    for date, events in fixed_milestones.items():
        if date not in schedule_data:
            schedule_data[date] = []
        for event in events:
            if event not in schedule_data[date]:
                schedule_data[date].append(event)
                
    # 3. Compile Deadlines
    today_str = datetime.now().strftime("%Y-%m-%d")
    deadlines_list = []
    
    for date in sorted(schedule_data.keys()):
        events_str = " & ".join(schedule_data[date])
        # Bersihkan format teks
        events_str = re.sub(r'\s+', ' ', events_str)
        status = "selesai" if date < today_str else "belum"
        deadlines_list.append({
            "tanggal": date,
            "kegiatan": f"Kelompok {args.kelompok}: {events_str}",
            "status": status
        })
        
    # 4. Baca dan Perbarui main README.md
    metadata, body = read_markdown_file(readme_path)
    
    if not metadata:
        metadata = {
            "nama": "Latsar CPNS 2026",
            "kategori": "non-survey",
            "rutinitas": "non-rutin",
            "frekuensi": "ad-hoc",
            "peran": "anggota",
            "status": "aktif",
        }
        body = (
            f"# Latsar CPNS (2026)\n\n"
            f"## Deskripsi Kegiatan\n"
            f"Pelatihan Dasar (Latsar) CPNS BPS Kabupaten Mempawah Golongan III Angkatan 10 Tahun 2026. "
            f"Jadwal di bawah disinkronisasi secara otomatis dari Google Sheets untuk Kelompok {args.kelompok}.\n\n"
            f"## Daftar CPNS BPS Kabupaten Mempawah\n"
            f"*   [Akma Batrisyia Jazima](akma-batrisyia-jazima/README.md) (Kelompok 2)\n"
            f"*   [CPNS Kedua](cpns-dua/README.md) (Kelompok ...)\n\n"
            f"## Catatan Pelaksanaan\n"
            f"*   **14 Juli 2026**: Menginisialisasi folder kegiatan latsar-cpns dan melakukan sinkronisasi jadwal pertama.\n"
        )
        
    metadata["deadlines"] = deadlines_list
    write_markdown_file(readme_path, metadata, body)
    
    print(f"{Colors.GREEN}Sukses memperbarui jadwal Latsar CPNS kelompok {args.kelompok} di {readme_path}.{Colors.ENDC}")
    print(f"Total {len(deadlines_list)} milestones terdaftar.")

    # 5. Otomatis sinkronisasi ke Google Sheets
    try:
        from .cmd_sync_sheets import cmd_sync_sheets
        print(f"\n{Colors.BLUE}Menjalankan sinkronisasi otomatis ke Google Sheets...{Colors.ENDC}")
        cmd_sync_sheets(args)
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal melakukan sinkronisasi Google Sheets otomatis: {e}{Colors.ENDC}")
