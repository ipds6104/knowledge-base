"""
kb/se_monitor/schedule_checker.py — Utilitas evaluasi irisan jadwal, kalkulasi jam kerja efektif,
dan penjadwalan query SQL Lab Superset SE2026.
"""

import glob
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

from ..colors import Colors
from ..markdown_io import read_markdown_file


# Hari libur / event blok penuh (misal: 30 Juli Latsar Seminar Full Day)
FULL_DAY_BLOCKED_DATES = {
    "2026-07-30": "Latsar CPNS Seminar Rancangan (08.00 - 17.00 WIB)",
}

# Slot Waktu Ideal Penjadwalan Query SQL Lab Superset
SQL_LAB_SCHEDULE_SLOTS = [
    {
        "slot": "06.30 - 07.30 WIB",
        "nama": "SQL Lab Pull Pagi & Morning Briefing",
        "perintah": "./scripts/kb.py sqllab pull && ./scripts/kb.py se-monitor -r",
        "tujuan": "Menarik data submisi malam PPL & mencetak laporan 6-seksi sebelum turun lapangan.",
        "kategori": "Pagi",
    },
    {
        "slot": "12.30 - 13.00 WIB",
        "nama": "SQL Lab Quick Check ISHOMA",
        "perintah": "./scripts/kb.py sqllab report",
        "tujuan": "Memantau pergerakan data pertengahan hari dan status antrean PML.",
        "kategori": "Siang",
    },
    {
        "slot": "17.30 - 18.30 WIB",
        "nama": "SQL Lab Pull Sore & Rekap Harian",
        "perintah": "./scripts/kb.py sqllab pull-completed && ./scripts/kb.py se-monitor -r",
        "tujuan": "Menarik SLS 100% approved, update rekap harian, & evaluasi sore PJ-Kuda.",
        "kategori": "Sore",
    },
    {
        "slot": "21.00 - 22.00 WIB",
        "nama": "SQL Lab Batch Anomaly Scan (Night Run)",
        "perintah": "./scripts/kb.py sqllab pull-microdata",
        "tujuan": "Query berat microdata Superset untuk 7 deteksi anomali Rakornas saat beban server rendah.",
        "kategori": "Malam",
    },
]


def load_all_deadlines() -> List[Dict[str, Any]]:
    """Membaca seluruh deadline dari berkas README.md kegiatan di repo."""
    readmes = glob.glob('kegiatan/*/*/README.md')
    deadlines = []

    for r_path in readmes:
        p = Path(r_path)
        metadata, _ = read_markdown_file(r_path)
        if not metadata or "deadlines" not in metadata:
            continue
        for dl in metadata["deadlines"]:
            tgl_str = dl.get("tanggal")
            if not tgl_str:
                continue
            try:
                tgl = datetime.strptime(tgl_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            deadlines.append({
                "nama_kegiatan": metadata.get("nama", p.parent.parent.name),
                "periode": p.parent.name,
                "tanggal": tgl,
                "tgl_str": tgl_str,
                "kegiatan": dl.get("kegiatan", ""),
                "status": dl.get("status", "belum"),
            })

    deadlines.sort(key=lambda x: x["tanggal"])
    return deadlines


def analyze_schedule_conflicts(today: datetime.date = None) -> None:
    """Menganalisis irisan jadwal dan menampilkan rekomendasi eksekusi bebas bentrokan."""
    if today is None:
        today = datetime.now().date()

    deadlines = load_all_deadlines()
    target_internal = datetime.strptime("2026-08-17", "%Y-%m-%d").date()
    target_resmi = datetime.strptime("2026-08-31", "%Y-%m-%d").date()

    print(f"\n{Colors.BOLD}{Colors.HEADER}========================================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN} 📅 ANALISIS IRISAN JADWAL & PENJADWALAN AUTOMATION RUNNING (SE2026 & UTAMA){Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}========================================================================={Colors.ENDC}\n")
    print(f"📌 {Colors.BOLD}Tanggal Evaluasi Saat Ini:{Colors.ENDC} {today.strftime('%d %B %Y')}")
    print(f"🎯 {Colors.BOLD}Target Internal Rakornas (Buffer 2 Mgg):{Colors.ENDC} 17 Agustus 2026")
    print(f"🏁 {Colors.BOLD}Batas Akhir Sensus Resmi:{Colors.ENDC} 31 Agustus 2026\n")

    # Grouping deadlines per date for future dates
    by_date: Dict[str, List[Dict[str, Any]]] = {}
    for dl in deadlines:
        if dl["tanggal"] >= today and dl["status"].lower() != "selesai":
            d_str = dl["tgl_str"]
            by_date.setdefault(d_str, []).append(dl)

    # Calculate effective working days to target internal
    days_to_internal = (target_internal - today).days
    blocked_count = sum(1 for d_str in FULL_DAY_BLOCKED_DATES if today <= datetime.strptime(d_str, "%Y-%m-%d").date() <= target_internal)
    effective_days = max(1, days_to_internal - blocked_count)

    print(f"{Colors.BOLD}{Colors.BLUE}--- 1. KALKULASI HARI KERJA EFEKTIF PERIODE SPRINT AKHIR ---{Colors.ENDC}")
    print(f"• Total Hari Kalender (s.d. 17 Agt): {Colors.BOLD}{days_to_internal} hari{Colors.ENDC}")
    print(f"• Hari Terblokir Penuh (Latsar Seminar dll): {Colors.FAIL}{blocked_count} hari{Colors.ENDC}")
    print(f"• Hari Kerja Efektif Lapangan: {Colors.GREEN}{Colors.BOLD}{effective_days} hari{Colors.ENDC}\n")

    # Show Conflict Matrix (Dates with >1 high priority deadlines or full-day block)
    print(f"{Colors.BOLD}{Colors.BLUE}--- 2. MATRIKS IRISAN JADWAL & DETEKSI BENTROKAN KANTONG TINGGI ---{Colors.ENDC}")
    
    conflict_found = False
    for d_str in sorted(by_date.keys()):
        d_items = by_date[d_str]
        tgl_obj = datetime.strptime(d_str, "%Y-%m-%d").date()
        if tgl_obj > target_resmi:
            continue

        is_blocked = d_str in FULL_DAY_BLOCKED_DATES
        is_dense = len(d_items) >= 2 or is_blocked

        if is_dense:
            conflict_found = True
            badge = f"{Colors.FAIL}[BENTROKAN TINGGI]{Colors.ENDC}" if is_blocked or len(d_items) >= 3 else f"{Colors.WARNING}[PERHATIAN]{Colors.ENDC}"
            print(f"{Colors.BOLD}{Colors.CYAN}► Tanggal: {d_str}{Colors.ENDC} {badge}")
            if is_blocked:
                print(f"  {Colors.FAIL}⚠️ BLOKIR FULL DAY:{Colors.ENDC} {FULL_DAY_BLOCKED_DATES[d_str]}")
            for item in d_items:
                print(f"  • [{item['nama_kegiatan']}] {item['kegiatan']}")
            print()

    if not conflict_found:
        print(f"{Colors.OKGREEN}Tidak ditemukan bentrokan kritis pada rentang jadwal mendatang.{Colors.ENDC}\n")

    # SQL Lab Running Schedule Recommendations
    print(f"{Colors.BOLD}{Colors.BLUE}--- 3. PENJADWALAN RUNNING DATA SQL LAB SUPERSET (FASIH SE2026) ---{Colors.ENDC}")
    print("Untuk memastikan data pendataan & anomali selalu up-to-date tanpa mengganggu jam kerja lapangan:\n")

    for slot in SQL_LAB_SCHEDULE_SLOTS:
        print(f"⏰ {Colors.BOLD}{Colors.CYAN}{slot['slot']}{Colors.ENDC} ({slot['kategori']}) — {Colors.BOLD}{slot['nama']}{Colors.ENDC}")
        print(f"   💻 Perintah : {Colors.WARNING}{slot['perintah']}{Colors.ENDC}")
        print(f"   🎯 Tujuan   : {slot['tujuan']}\n")

    # Tactical Guidance for Mitigating Conflicts
    print(f"{Colors.BOLD}{Colors.BLUE}--- 4. PANDUAN STRATEGIS MEMINIMALISIR IRISAN & HASIL TANGGAL OPTIMAL ---{Colors.ENDC}")
    print(f"1. 📌 {Colors.BOLD}30 Juli 2026 (Seminar Latsar CPNS 08.00-17.00){Colors.ENDC}:")
    print("   - Monitoring SE2026 dialihkan penuh ke Slot Pagi (06.30-07.30) dan Slot Malam (19.30-20.30).")
    print("   - Tidak ada penugasan lapangan baru untuk PJ-Kuda selama jam 08.00-17.00 WIB.")
    print(f"2. 📌 {Colors.BOLD}31 Juli 2026 (Quadruple Deadline: CAWI SE2026, Kepegawaian, SAKIP TW II, EPSS){Colors.ENDC}:")
    print("   - Tutup CAWI SE2026 dilakukan via query SQL Lab pada 31 Juli malam.")
    print("   - Penyelesaian SAKIP TW II dikunci pada 30 Juli malam agar 31 Juli fokus verifikasi CAWI & EPSS.")
    print(f"3. 📌 {Colors.BOLD}1 - 10 Agustus 2026 (Sakernas Updating RT vs SE2026 Final Sprint){Colors.ENDC}:")
    print("   - Petugas yang merangkap Sakernas diprioritaskan menyelesaikan updating Sakernas pada 1-5 Agt.")
    print("   - Monitoring SE2026 dijalankan ketat 2x sehari (06.30 dan 17.30) menggunakan `./scripts/kb.py se-monitor -r`.")
    print(f"\n{Colors.BOLD}{Colors.HEADER}========================================================================={Colors.ENDC}\n")
