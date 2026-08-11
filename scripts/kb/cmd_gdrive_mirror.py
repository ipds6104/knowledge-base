"""kb/cmd_gdrive_mirror.py — Subcommand CLI untuk mirroring direktori lokal ke Google Drive."""

import os
import sys
from pathlib import Path
from typing import List, Set

from kb.google_drive import (
    compute_file_md5,
    extract_folder_id,
    get_drive_service,
    get_or_create_gdrive_folder,
    list_gdrive_contents,
    upload_or_update_file,
)

IGNORED_NAMES: Set[str] = {
    ".git",
    "__pycache__",
    ".DS_Store",
    ".venv",
    ".env",
    "node_modules",
    ".githooks",
    ".pytest_cache",
    ".idea",
    ".vscode",
}

IGNORED_SUFFIXES: Set[str] = {
    ".pyc",
    ".tmp",
    ".swp",
}

def is_ignored(path: Path) -> bool:
    """Memeriksa apakah berkas/folder harus diabaikan dalam sinkronisasi."""
    if path.name in IGNORED_NAMES or path.name.startswith("."):
        return True
    if path.suffix in IGNORED_SUFFIXES:
        return True
    return False

def mirror_recursive(
    service,
    local_dir: Path,
    parent_gdrive_id: str,
    dry_run: bool = False,
    force: bool = False,
    rel_prefix: str = ""
) -> dict:
    """Mengunggah/memperbarui folder lokal secara rekursif ke Google Drive."""
    stats = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}

    print(f"\n📁 Memindai folder Google Drive: {rel_prefix or local_dir.name}...")
    if not dry_run:
        remote_contents = list_gdrive_contents(service, parent_gdrive_id)
    else:
        remote_contents = {}

    children = sorted(list(local_dir.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))

    for child in children:
        if is_ignored(child):
            continue

        rel_path = f"{rel_prefix}/{child.name}" if rel_prefix else child.name

        if child.is_dir():
            print(f"\n📂 [DIR] {rel_path}/")
            if dry_run:
                sub_stats = mirror_recursive(
                    service, child, "DRY_RUN_ID", dry_run=True, force=force, rel_prefix=rel_path
                )
            else:
                sub_gdrive_id = get_or_create_gdrive_folder(service, child.name, parent_gdrive_id)
                sub_stats = mirror_recursive(
                    service, child, sub_gdrive_id, dry_run=False, force=force, rel_prefix=rel_path
                )
            for k in stats:
                stats[k] += sub_stats[k]
        else:
            existing = remote_contents.get(child.name)
            action = None

            if existing:
                remote_md5 = existing.get("md5Checksum")
                if not force and remote_md5 and compute_file_md5(child) == remote_md5:
                    action = "SKIP"
                else:
                    action = "UPDATE"
            else:
                action = "CREATE"

            if dry_run:
                print(f"  [DRY-RUN] [{action:<6}] {child.name}")
                if action == "CREATE":
                    stats["created"] += 1
                elif action == "UPDATE":
                    stats["updated"] += 1
                else:
                    stats["skipped"] += 1
            else:
                if action == "SKIP":
                    print(f"  🟢 [SKIP]   {child.name} (TIDAK BERUBAH)")
                    stats["skipped"] += 1
                else:
                    symbol = "✨ [CREATE]" if action == "CREATE" else "🔄 [UPDATE]"
                    print(f"  {symbol} {child.name}...", end="", flush=True)
                    try:
                        _, res_type = upload_or_update_file(
                            service, child, parent_gdrive_id, existing_file=existing
                        )
                        print(" SUKSES!")
                        if res_type == "CREATE":
                            stats["created"] += 1
                        else:
                            stats["updated"] += 1
                    except Exception as e:
                        print(f" GAGAL! ({e})")
                        stats["failed"] += 1

    return stats

def run_gdrive_mirror(args) -> int:
    """Fungsi utama pengesekusi perintah `kb gdrive-mirror`."""
    local_path = Path(args.source_path).resolve()
    if not local_path.exists() or not local_path.is_dir():
        print(f"❌ Error: Direktori lokal '{args.source_path}' tidak ditemukan!")
        return 1

    raw_folder_id = args.folder_id
    if not raw_folder_id:
        raw_folder_id = os.getenv("GDRIVE_MIRROR_FOLDER_ID", "15Uc6P3b5nCDvnq0c0KJoiKZwyB7PQAy0")

    gdrive_id = extract_folder_id(raw_folder_id)

    print("=========================================================")
    print("🚀 BPS KABUPATEN MEMPAWAH - GOOGLE DRIVE REPO MIRRORING")
    print("=========================================================")
    print(f"📍 Direktori Lokal : {local_path}")
    print(f"☁️ Google Drive ID : {gdrive_id}")
    print(f"🔍 Mode Dry-Run    : {'YA (Simulasi)' if args.dry_run else 'TIDAK (Aktual Upload)'}")
    print(f"⚡ Mode Force      : {'YA (Re-upload Semua)' if args.force else 'TIDAK'}")
    print("---------------------------------------------------------")

    try:
        repo_root = Path.cwd()
        try:
            rel_path = local_path.relative_to(repo_root)
        except ValueError:
            rel_path = Path(args.source_path)

        if not args.dry_run:
            print("🔑 Mengaitkan koneksi OAuth ke Google Drive API...")
            service = get_drive_service()
        else:
            service = None

        # Buat/navigasi hirarki folder induk di Google Drive
        target_gdrive_id = gdrive_id
        for part in rel_path.parts:
            if part in (".", ".."):
                continue
            print(f"📂 Navigasi/Buat folder induk Google Drive: {part}/")
            if not args.dry_run:
                target_gdrive_id = get_or_create_gdrive_folder(service, part, target_gdrive_id)
            else:
                target_gdrive_id = f"DRY_RUN_{part}"

        stats = mirror_recursive(
            service, local_path, target_gdrive_id, dry_run=args.dry_run, force=args.force, rel_prefix=str(rel_path)
        )

        print("\n=========================================================")
        print("📊 RINGKASAN REKAPITULASI MIRRORING")
        print("=========================================================")
        print(f"✨ File Baru Terunggah  : {stats['created']}")
        print(f"🔄 File Diperbarui      : {stats['updated']}")
        print(f"🟢 File Didefleksi/Skip : {stats['skipped']}")
        if stats['failed'] > 0:
            print(f"❌ File Gagal           : {stats['failed']}")
        print("=========================================================")
        return 0

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat sinkronisasi: {e}")
        return 1
