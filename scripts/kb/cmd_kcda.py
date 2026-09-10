"""CLI Handler Subcommand 'kb kcda' for Kecamatan Dalam Angka (KCDA) 2026 Engine."""

import os
import sys
import json
import glob
from pathlib import Path
from .kcda_audit import run_kcda_audit, download_all_kcda_tables
from .kcda_generator.compiler import compile_kecamatan, compile_all_kcda
from .kcda_generator.uploader import upload_kcda_drafts
from .kcda_generator.config import KCDA_KECAMATAN_CONFIG

def register_kcda_subparser(subparsers):
    """Mendaftarkan subcommand 'kcda' ke ArgumentParser CLI kb."""
    parser = subparsers.add_parser(
        "kcda",
        help="Pengelolaan, audit kesiapan data, dan kompilasi publikasi Kecamatan Dalam Angka (KCDA) 2026",
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="audit",
        choices=["audit", "sync", "report", "build", "seed-legacy"],
        help="Aksi: 'audit' (evaluasi data), 'sync' (unduh dari Sheets), 'build' (kompilasi naskah), 'seed-legacy' (ekstrak & injeksi data carry-over 2025)",
    )
    parser.add_argument(
        "--kecamatan", "-k",
        default=None,
        help="Nama spesifik kecamatan (contoh: 'jongkat', 'mempawah-hilir', 'sungai-pinyuh')",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Lewati penarikan data terbaru dari Google Sheets hulu sebelum build (gunakan cache lokal)",
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Lewati pengunggahan otomatis draf PDF ke Google Drive setelah build",
    )
    parser.add_argument(
        "--upload", "-u",
        action="store_true",
        default=True,
        help="[Deprecated/Default] Unggah draf PDF yang dihasilkan langsung ke Google Drive subfolder '3. Draft Publikasi'",
    )
    parser.add_argument(
        "--push-gsheet",
        action="store_true",
        help="Tuliskan data hasil ekstraksi langsung ke Google Sheets hulu",
    )


def handle_kcda(args):
    """Memproses eksekusi subcommand kcda."""
    action = args.action
    if action == "seed-legacy":
        from .kcda_generator.legacy_seeder import seed_legacy_data_to_cache
        seed_legacy_data_to_cache(push_gsheet=args.push_gsheet)
    elif action == "sync":
        print("🔄 Memulai sinkronisasi 35 nested spreadsheet KCDA 2026...")
        download_all_kcda_tables()
        print("✅ Sinkronisasi selesai. Menjalankan audit...")
        run_kcda_audit(filter_kec=args.kecamatan)
    elif action in ["audit", "report"]:
        run_kcda_audit(filter_kec=args.kecamatan)
    elif action == "build":
        # 1. Step 1: Tarik data terbaru dari Google Sheets hulu (default: aktif)
        if not args.no_sync:
            print("\n📥 [1/3] Menarik data terbaru dari Google Sheets hulu...")
            download_all_kcda_tables()
            # Auto seed legacy data ke cache lokal agar data statis 2025 melengkapi yang kosong
            from .kcda_generator.legacy_seeder import seed_legacy_data_to_cache
            seed_legacy_data_to_cache(push_gsheet=False)
        else:
            print("\n⏩ [1/3] Melewati penarikan Google Sheets (--no-sync aktif, memakai cache lokal)...")

        # 2. Step 2: Kompilasi naskah publikasi PDF via Typst
        print("\n🔨 [2/3] Memulai kompilasi naskah Typst KCDA 2026...")
        should_upload = not args.no_upload

        if args.kecamatan:
            slug = args.kecamatan.lower().strip()
            slug = slug.replace("kecamatan ", "").replace(" ", "-")
            if slug not in KCDA_KECAMATAN_CONFIG:
                for k, v in KCDA_KECAMATAN_CONFIG.items():
                    if slug in k:
                        slug = k
                        break
            print(f"🚀 Memulai kompilasi KCDA 2026 untuk: {slug}...")
            res = compile_kecamatan(slug)
            print(f"✅ Selesai: {res['pdf_path']} ({res['pages']} hal, {res['file_size_kb']} KB, {res['duration_sec']}s)")
            if should_upload:
                print("\n☁️  [3/3] Mengunggah draf ke Google Drive...")
                upload_kcda_drafts([res])
            else:
                print("\n⏩ [3/3] Melewati pengunggahan Google Drive (--no-upload aktif)...")
        else:
            results = compile_all_kcda()
            if should_upload:
                print("\n☁️  [3/3] Mengunggah 9 draf ke Google Drive secara paralel...")
                upload_kcda_drafts(results)
            else:
                print("\n⏩ [3/3] Melewati pengunggahan Google Drive (--no-upload aktif)...")

