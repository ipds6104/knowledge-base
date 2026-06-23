"""kb/cmd_list.py — Implementasi perintah `kb list`."""

import glob
from pathlib import Path

from .colors import Colors
from .markdown_io import read_markdown_file


def cmd_list(args) -> None:
    """Tampilkan daftar semua kegiatan dalam tabel."""
    readmes = glob.glob('kegiatan/*/*/README.md')
    if not readmes:
        print(f"{Colors.WARNING}Tidak ada kegiatan yang ditemukan.{Colors.ENDC}")
        return

    activities = []
    for r_path in readmes:
        p = Path(r_path)
        periode = p.parent.name
        metadata, _ = read_markdown_file(r_path)
        if metadata:
            activities.append({
                "path": r_path,
                "nama": metadata.get("nama", p.parent.parent.name),
                "periode": periode,
                "kategori": metadata.get("kategori", "N/A"),
                "frekuensi": metadata.get("frekuensi", "N/A"),
                "peran": metadata.get("peran", "N/A"),
                "status": metadata.get("status", "N/A"),
            })

    activities.sort(key=lambda x: (x["nama"], x["periode"]))

    header = (
        f"| {'Nama Kegiatan':<25} | {'Periode':<8} | {'Kategori':<11} "
        f"| {'Frekuensi':<10} | {'Peran':<8} | {'Status':<8} |"
    )
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    for act in activities:
        status_color = Colors.GREEN if act['status'].lower() == 'selesai' else Colors.BLUE
        status_str = f"{status_color}{act['status'].upper()}{Colors.ENDC}"
        print(
            f"| {act['nama'][:25]:<25} | {act['periode']:<8} | {act['kategori']:<11} "
            f"| {act['frekuensi']:<10} | {act['peran']:<8} | {status_str:<17} |"
        )
    print(divider)
