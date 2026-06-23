#!/usr/bin/env python3
"""
dump_tree.py — Repo Structure Dumper
Mencetak struktur direktori repositori beserta jumlah baris setiap file,
dan menampilkan 5 file terbesar (berdasarkan jumlah baris).

Penggunaan:
    ./scripts/dump_tree.py              # Dump seluruh repo
    ./scripts/dump_tree.py [path]       # Dump dari direktori tertentu
    ./scripts/dump_tree.py --no-top     # Tanpa daftar Top 5
    ./scripts/dump_tree.py --max-depth 3  # Batasi kedalaman tampilan
"""

import os
import sys
import argparse
from pathlib import Path

# Ekstensi file teks yang dihitung baris nya
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".sh", ".bash", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".conf", ".html", ".css", ".js", ".ts",
    ".sql", ".r", ".R", ".rst", ".xml"
}

# Ekstensi yang diabaikan (data mentah, generated, cache)
SKIP_EXTENSIONS = {
    ".csv", ".json", ".jsonl", ".log", ".lock",
    ".pkl", ".pickle", ".parquet", ".feather", ".h5", ".hdf5",
    ".db", ".sqlite", ".sqlite3",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".rar",
    ".xlsx", ".xls", ".ods",
    ".pdf", ".docx", ".doc", ".pptx", ".ppt",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
    ".mp3", ".mp4", ".wav", ".avi",
    ".whl", ".egg",
}

# File spesifik yang diabaikan (nama persis)
SKIP_FILES = {
    ".env", ".env.local", ".env.example",
    ".DS_Store", ".gitignore", ".gitkeep",
    "Thumbs.db", "desktop.ini",
}

# Direktori yang dilewati
SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", ".eggs", "dist", "build", ".DS_Store"
}

# Warna terminal
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def count_lines(filepath: Path) -> int | None:
    """Hitung jumlah baris file teks. Kembalikan None jika binary/tidak bisa dibaca."""
    if filepath.suffix.lower() not in TEXT_EXTENSIONS:
        return None
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return None


def format_lines(n: int | None) -> str:
    """Format jumlah baris dengan warna sesuai ukuran."""
    if n is None:
        return f"{DIM}[binary]{RESET}"
    if n >= 1000:
        return f"{RED}{n:>5} baris{RESET}"
    if n >= 300:
        return f"{YELLOW}{n:>5} baris{RESET}"
    return f"{DIM}{n:>5} baris{RESET}"


def dump_tree(
    root: Path,
    prefix: str = "",
    all_files: list = None,
    skipped_files: list = None,
    max_depth: int | None = None,
    current_depth: int = 0,
):
    if all_files is None:
        all_files = []
    if skipped_files is None:
        skipped_files = []

    if max_depth is not None and current_depth >= max_depth:
        return all_files, skipped_files

    try:
        entries = sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        return all_files, skipped_files

    dirs  = [e for e in entries if e.is_dir()  and e.name not in SKIP_DIRS]
    files = [
        e for e in entries
        if e.is_file()
        and e.name not in SKIP_FILES
        and e.suffix.lower() not in SKIP_EXTENSIONS
    ]
    ignored = [
        e for e in entries
        if e.is_file()
        and (e.name in SKIP_FILES or e.suffix.lower() in SKIP_EXTENSIONS)
    ]
    # Track ignored for summary
    skipped_files.extend(ignored)

    total = len(dirs) + len(files)
    for idx, entry in enumerate(dirs + files):
        is_last = (idx == total - 1)
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if entry.is_dir():
            # Peek: does dir have any visible content after filtering?
            print(f"{prefix}{connector}{BOLD}{CYAN}{entry.name}/{RESET}")
            dump_tree(
                entry,
                prefix=prefix + extension,
                all_files=all_files,
                skipped_files=skipped_files,
                max_depth=max_depth,
                current_depth=current_depth + 1,
            )
        else:
            lines = count_lines(entry)
            lines_str = format_lines(lines)
            print(f"{prefix}{connector}{entry.name}  {lines_str}")
            all_files.append((entry, lines))

    return all_files, skipped_files


def print_top5(all_files: list):
    """Tampilkan 5 file terbesar berdasarkan jumlah baris."""
    countable = [(f, n) for f, n in all_files if n is not None]
    if not countable:
        print(f"{DIM}(Tidak ada file teks yang ditemukan){RESET}")
        return

    top5 = sorted(countable, key=lambda x: x[1], reverse=True)[:5]

    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{YELLOW}🏆 TOP 5 FILE TERBESAR (berdasarkan jumlah baris){RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")
    for rank, (filepath, lines) in enumerate(top5, 1):
        # Relative path from cwd
        try:
            rel = filepath.relative_to(Path.cwd())
        except ValueError:
            rel = filepath
        bar_len = min(40, lines // 50)
        bar = "█" * bar_len
        color = RED if lines >= 1000 else (YELLOW if lines >= 300 else GREEN)
        print(f"  {BOLD}{rank}.{RESET} {rel}")
        print(f"     {color}{bar} {lines} baris{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Dump struktur repositori dengan jumlah baris setiap file.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Direktori yang akan di-dump (default: direktori saat ini)",
    )
    parser.add_argument(
        "--no-top",
        action="store_true",
        help="Jangan tampilkan daftar Top 5 file terbesar",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        metavar="N",
        help="Batasi kedalaman tampilan pohon (default: tanpa batas)",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"{RED}Error: Path '{args.path}' tidak ditemukan.{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  STRUKTUR REPOSITORI: {root.name}/{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    print(f"{BOLD}{CYAN}{root.name}/{RESET}")

    all_files, skipped_files = dump_tree(root, max_depth=args.max_depth)

    # Summary stats
    total_files = len(all_files)
    total_lines = sum(n for _, n in all_files if n is not None)
    binary_count = sum(1 for _, n in all_files if n is None)
    skipped_count = len(skipped_files)
    skipped_exts = sorted({f.suffix.lower() for f in skipped_files if f.suffix} | {f.name for f in skipped_files if f.name in SKIP_FILES})

    print(f"\n{DIM}{'─'*60}{RESET}")
    print(f"{DIM}Ditampilkan : {total_files} file | {total_lines:,} baris{RESET}")
    if skipped_count:
        exts_str = ", ".join(skipped_exts[:8]) + (" ..." if len(skipped_exts) > 8 else "")
        print(f"{DIM}Diabaikan   : {skipped_count} file ({exts_str}){RESET}")
    if binary_count:
        print(f"{DIM}Binary      : {binary_count} file{RESET}")

    if not args.no_top:
        print_top5(all_files)


if __name__ == "__main__":
    # Set cwd ke root repo jika dipanggil dari mana saja
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    main()
