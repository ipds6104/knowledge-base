#!/usr/bin/env python3
"""BPS Kabupaten Mempawah Knowledge Base Management Utility.

Entrypoint script yang mengimpor seluruh perintah dari package modular kb/.
"""

import os
import sys
import argparse
from pathlib import Path

# Sisipkan direktori scripts/ ke sys.path untuk impor package kb lokal
scripts_dir = Path(__file__).parent.resolve()
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from kb import (
    cmd_create,
    cmd_list,
    cmd_schedule,
    cmd_convert,
    cmd_se_monitor,
    cmd_latsar,
    cmd_sync_sheets,
    cmd_auto_update,
    cmd_chat,
    cmd_setup,
    cmd_sqllab,
    cmd_metadata,
    cmd_dda,
    cmd_gdrive_mirror,
    cmd_podes,
    whoami_str,
)


def main():
    # Reconfigure stdout to support UTF-8 on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(
        description="BPS Kabupaten Mempawah Knowledge Base Management Utility",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 10. SQLLAB command
    parser_sqllab = subparsers.add_parser(
        "sqllab", help="Penarikan, analisis 2-view, dan penyiapan berkas verifikasi RT SQL Lab SE2026."
    )
    parser_sqllab.add_argument(
        "sqllab_subcommand",
        choices=["sync", "pull", "pull-microdata", "pull-completed", "report", "print-prep", "surreal-sync"],
        help="Subcommand: 'sync' (workflow otomatis 5-step penuh), 'surreal-sync' (delta sync 599+ kolom ke SurrealDB), 'pull' (tarik massal agregat), 'pull-microdata' (tarik microdata CSV), 'pull-completed' (tarik CSV Sub-SLS selesai), 'report' (laporan 2-view), 'print-prep' (penyiapan PDF verifikasi RT)"
    )
    parser_sqllab.add_argument(
        "--min-not-found", "-m",
        type=int, default=5,
        help="Batas minimal kasus Tidak Ditemukan untuk SLS Siap Cetak (default: 5)"
    )


    # 0. WHOAMI command
    subparsers.add_parser(
        "whoami", help="Tampilkan identitas pengguna aktif repo ini."
    )

    # 0b. SETUP command
    parser_setup = subparsers.add_parser(
        "setup", help="Wizard setup identitas pengguna di laptop ini (jalankan sekali setelah clone)."
    )
    parser_setup.add_argument(
        "--force", "-f",
        action="store_true",
        help="Paksa ganti identitas meski sudah terkonfigurasi"
    )

    # 1. CREATE command
    parser_create = subparsers.add_parser(
        "create", help="Membuat folder dan template kegiatan baru."
    )
    parser_create.add_argument("nama", type=str, help="Nama kegiatan (contoh: 'Sakernas')")
    parser_create.add_argument(
        "periode", type=str, help="Periode pelaksanaan (contoh: '2026-06')"
    )
    parser_create.add_argument(
        "--kategori",
        type=str,
        choices=["survey", "non-survey"],
        default="survey",
        help="Kategori kegiatan (default: survey)",
    )
    parser_create.add_argument(
        "--rutinitas",
        type=str,
        choices=["rutin", "non-rutin"],
        default="rutin",
        help="Rutinitas kegiatan (default: rutin)",
    )
    parser_create.add_argument(
        "--frekuensi",
        type=str,
        choices=[
            "bulanan",
            "triwulanan",
            "semesteran",
            "tahunan",
            "10-tahunan",
            "ad-hoc",
        ],
        default="bulanan",
        help="Frekuensi kegiatan (default: bulanan)",
    )
    parser_create.add_argument(
        "--peran",
        type=str,
        choices=["ketua", "anggota"],
        default="ketua",
        help="Peran Anda dalam tim (default: ketua)",
    )
    parser_create.add_argument(
        "--force", action="store_true", help="Paksa buat/timpa jika sudah ada."
    )

    # 2. LIST command
    subparsers.add_parser("list", help="Menampilkan daftar semua kegiatan.")

    # 3. SCHEDULE command
    parser_sched = subparsers.add_parser(
        "schedule", help="Menampilkan timeline dan deadline jadwal."
    )
    group_sched = parser_sched.add_mutually_exclusive_group()
    group_sched.add_argument(
        "--week", action="store_true", help="Tampilkan jadwal minggu ini saja."
    )
    group_sched.add_argument(
        "--month", action="store_true", help="Tampilkan jadwal bulan ini saja."
    )
    group_sched.add_argument(
        "--overdue",
        action="store_true",
        help="Tampilkan jadwal yang terlambat (overdue) saja.",
    )

    # 4. CONVERT command
    parser_conv = subparsers.add_parser(
        "convert", help="Mengonversi dokumen PDF ke Markdown."
    )
    parser_conv.add_argument("pdf", type=str, help="Path ke berkas PDF")
    parser_conv.add_argument(
        "--ai",
        action="store_true",
        help="Gunakan AI Vision (Gemini Proxy) untuk konversi presisi tinggi.",
    )

    # 5. SE-MONITOR command
    parser_mon = subparsers.add_parser(
        "se-monitor", help="Monitoring progres petugas Sensus Ekonomi 2026."
    )
    parser_mon.add_argument(
        "--pj",
        type=str,
        default="Ihza Fikri Zaki Karunia",
        help="Nama PJ-Kuda target (default: 'Ihza Fikri Zaki Karunia')",
    )
    parser_mon.add_argument(
        "--all-pj", action="store_true", help="Tampilkan peringkat seluruh PJ-Kuda."
    )
    parser_mon.add_argument(
        "-i",
        "--intervention",
        action="store_true",
        help="Tampilkan daftar petugas se-kabupaten yang membutuhkan intervensi langsung.",
    )
    parser_mon.add_argument(
        "--prov",
        action="store_true",
        help="Tampilkan ringkasan progres dan peringkat seluruh Kabupaten/Kota di Provinsi Kalbar.",
    )
    parser_mon.add_argument(
        "-r",
        "--report",
        action="store_true",
        help="Cetak laporan 6-seksi baku (format standar pagi/sore).",
    )
    parser_mon.add_argument(
        "--pml-compare",
        action="store_true",
        help="Tampilkan tabel perbandingan kinerja PML (Freeze 15 Juli vs Sekarang) beserta penjelasan kolomnya."
    )
    parser_mon.add_argument(
        "--pml-40",
        action="store_true",
        help="Tampilkan ringkasan PML yang mencapai progres 40%% per kabupaten dan rincian detail PML Mempawah."
    )
    parser_mon.add_argument(
        "--anomaly",
        action="store_true",
        help="Tampilkan analisis deteksi moral hazard dan PPL anomali di Kabupaten Mempawah."
    )


    parser_mon.add_argument(
        "--trend",
        type=str,
        help="Cari dan tampilkan tren harian untuk PPL tertentu berdasarkan arsip data.",
    )

    # 5b. SE-SCHEDULE command
    subparsers.add_parser(
        "se-schedule",
        help="Evaluasi bentrokan jadwal, hari efektif, & penjadwalan query SQL Lab SE2026."
    )

    # 6. LATSAR command
    parser_latsar = subparsers.add_parser(
        "latsar", help="Penarikan dan sinkronisasi jadwal Latsar CPNS dari Google Sheets."
    )
    parser_latsar.add_argument(
        "--kelompok",
        type=int,
        default=2,
        help="Kelompok Latsar yang ingin dipantau (default: 2)",
    )
    parser_latsar.add_argument(
        "--force", action="store_true", help="Paksa update berkas README.md."
    )

    # 7. SYNC-SHEETS command
    subparsers.add_parser(
        "sync-sheets", help="Sinkronisasi seluruh milestones kegiatan ke Google Sheets."
    )

    # 8. AUTO-UPDATE command
    subparsers.add_parser(
        "auto-update", help="Workflow harian terpadu (git pull + update latsar + sync-sheets)."
    )

    # 11. METADATA command
    cmd_metadata.register_parser(subparsers)

    # 9. CHAT command
    parser_chat = subparsers.add_parser(
        "chat", help="Menganalisis obrolan WhatsApp grup kegiatan (EPSS)."
    )
    parser_chat.add_argument(
        "chat_subcommand",
        choices=["list", "info", "links", "search", "extract", "tail", "digest"],
        help="Sub-command untuk analisis chat"
    )
    parser_chat.add_argument(
        "target",
        nargs="?",
        default="1",
        help="Index atau nama file ZIP chat (default: '1')"
    )
    parser_chat.add_argument(
        "--query", "-q",
        type=str, default="",
        help="Query pencarian untuk sub-command 'search'"
    )
    parser_chat.add_argument(
        "--limit", "-l",
        type=int, default=None,
        help="Batasi jumlah pesan terbaru (fallback jika --days tidak digunakan)"
    )
    parser_chat.add_argument(
        "--days", "-d",
        type=int, default=None,
        help="Filter pesan N hari terakhir (contoh: --days 7 untuk seminggu terakhir)"
    )
    parser_chat.add_argument(
        "--since",
        type=str, default=None,
        help="Filter pesan sejak tanggal tertentu (format: YYYY-MM-DD)"
    )
    # DDA command
    parser_dda = subparsers.add_parser(
        "dda", help="Penyusunan dan kompilasi otomatis publikasi Desa Dalam Angka (DDA) berstandar BPS."
    )
    parser_dda.add_argument(
        "nama_desa",
        type=str,
        help="Nama desa dalam format kebab-case (contoh: 'sungai-bakau-kecil', 'pasir-palembang', 'pasir-wan-salim')"
    )
    parser_dda.add_argument(
        "--sheet-id", "-s",
        type=str, default=None,
        help="Google Sheet ID publikasi/AppSheet (opsional)"
    )
    parser_dda.add_argument(
        "--year", "-y",
        type=int, default=2026,
        help="Tahun publikasi (default: 2026)"
    )
    parser_dda.add_argument(
        "--no-upload",
        action="store_true",
        help="Jangan upload hasil ke Google Drive secara otomatis."
    )

    # 13. GDRIVE-MIRROR command
    parser_gdrive = subparsers.add_parser(
        "gdrive-mirror", help="Mirroring direktori lokal ke Google Drive secara rekursif."
    )
    parser_gdrive.add_argument(
        "source_path",
        nargs="?",
        default="kegiatan/desa-cantik",
        help="Path folder lokal yang ingin di-mirror (default: 'kegiatan/desa-cantik')"
    )
    parser_gdrive.add_argument(
        "--folder-id", "-f",
        type=str,
        default=None,
        help="Google Drive Folder ID atau URL target (default: dari GDRIVE_MIRROR_FOLDER_ID di .env)"
    )
    parser_gdrive.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Simulasi pemindaian tanpa mengunggah/membuat file di Google Drive"
    )
    parser_gdrive.add_argument(
        "--force",
        action="store_true",
        help="Paksa unggah ulang seluruh file meskipun checksum cocok"
    )

    # 14. PODES command
    cmd_podes.register_podes_subparser(subparsers)

    args = parser.parse_args()

    # Set cwd to repo root to make paths consistent
    repo_root = scripts_dir.parent
    os.chdir(repo_root)

    if args.command == "create":
        cmd_create(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "se-monitor":
        cmd_se_monitor(args)
    elif args.command == "se-schedule":
        from kb.se_monitor.schedule_checker import analyze_schedule_conflicts
        analyze_schedule_conflicts()
    elif args.command == "latsar":
        cmd_latsar(args)
    elif args.command == "sync-sheets":
        cmd_sync_sheets(args)
    elif args.command == "auto-update":
        cmd_auto_update(args)
    elif args.command == "chat":
        cmd_chat(args)
    elif args.command == "whoami":
        print(whoami_str())
    elif args.command == "setup":
        cmd_setup(args)
    elif args.command == "metadata":
        cmd_metadata.run(args)
    elif args.command == "dda":
        cmd_dda.handle_dda(args)
    elif args.command == "podes":
        cmd_podes.handle_podes(args)
    elif args.command == "sqllab":
        if args.sqllab_subcommand == "sync":
            cmd_sqllab.cmd_sqllab_sync(args)
        elif args.sqllab_subcommand == "pull":
            cmd_sqllab.cmd_sqllab_pull(args)
        elif args.sqllab_subcommand == "pull-microdata":
            cmd_sqllab.cmd_sqllab_pull_microdata(args)
        elif args.sqllab_subcommand == "pull-completed":
            cmd_sqllab.cmd_sqllab_pull_completed_subsls(args)
        elif args.sqllab_subcommand == "report":
            cmd_sqllab.cmd_sqllab_report(args)
        elif args.sqllab_subcommand == "print-prep":
            cmd_sqllab.cmd_sqllab_print_prep(args)
        elif args.sqllab_subcommand == "surreal-sync":
            cmd_sqllab.cmd_sqllab_surreal_sync(args)
    elif args.command == "gdrive-mirror":
        cmd_gdrive_mirror.run_gdrive_mirror(args)



if __name__ == "__main__":
    main()
