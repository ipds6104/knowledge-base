"""kb/cmd_create.py — Implementasi perintah `kb create`."""

import sys
from datetime import datetime
from pathlib import Path

from .colors import Colors
from .utils import slugify
from .markdown_io import write_markdown_file, dump_yaml


def cmd_create(args) -> None:
    """Buat folder dan template README.md untuk kegiatan baru."""
    slug_name = slugify(args.nama)
    period_path = Path('kegiatan') / slug_name / args.periode
    readme_path = period_path / 'README.md'

    if readme_path.exists() and not args.force:
        print(
            f"{Colors.FAIL}Error: Kegiatan '{args.nama}' periode '{args.periode}' "
            f"sudah ada di {readme_path}. Gunakan --force untuk menimpa.{Colors.ENDC}"
        )
        sys.exit(1)

    metadata = {
        "nama": args.nama,
        "kategori": args.kategori,
        "rutinitas": args.rutinitas,
        "frekuensi": args.frekuensi,
        "peran": args.peran,
        "status": "aktif",
        "deadlines": [
            {
                "tanggal": datetime.now().strftime("%Y-%m-%d"),
                "kegiatan": "Kick-off / Persiapan awal",
                "status": "belum",
            }
        ],
    }

    body = (
        f"# {args.nama} ({args.periode})\n\n"
        "## Deskripsi Kegiatan\n"
        "Tambahkan detail deskripsi kegiatan di sini.\n\n"
        "## Catatan Pelaksanaan\n"
        "Tambahkan catatan penting pelaksanaan di sini.\n"
    )

    write_markdown_file(readme_path, metadata, body)
    print(f"{Colors.GREEN}Sukses membuat kegiatan baru!{Colors.ENDC}")
    print(f"Path: {readme_path}")
    print("Metadata:")
    print(dump_yaml(metadata))
