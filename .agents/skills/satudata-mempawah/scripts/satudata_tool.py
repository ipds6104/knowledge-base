#!/usr/bin/env python3
"""
Satu Data Mempawah CLI Tool
Interact with Portal Satu Data Kabupaten Mempawah CKAN 2.9 API.
Official Portal: https://satudata.mempawahkab.go.id/
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List

# Tambahkan direktori script ke path agar import client lokal berhasil
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from satudata_client import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, SatuDataAPIError, SatuDataClient


def render_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Render plain ASCII table tanpa dependensi eksternal."""
    if not rows:
        return "Tidak ada data."
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            str_val = str(cell)
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(str_val))
            else:
                col_widths.append(len(str_val))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    lines = [sep, header_line, sep]
    for row in rows:
        padded = []
        for i, w in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            padded.append(val.ljust(w))
        lines.append("| " + " | ".join(padded) + " |")
    lines.append(sep)
    return "\n".join(lines)


# --- Subcommand Handlers ---

def cmd_status(client: SatuDataClient, args: argparse.Namespace) -> int:
    status = client.get_status()
    stats = client.get_statistics()
    data = {"status": status, "statistics": stats}

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print("==================================================")
    print(" 🏛️  PORTAL SATU DATA KABUPATEN MEMPAWAH")
    print("==================================================")
    print(f"Judul Portal   : {status.get('site_title')}")
    print(f"Deskripsi      : {status.get('site_description')}")
    print(f"Versi CKAN     : {status.get('ckan_version')}")
    print(f"Versi Backend  : Laravel {status.get('laravel_version')}")
    print("--------------------------------------------------")
    print("📊 STATISTIK DATASET & PRODUSEN:")
    print(f" - Total Dataset Publik : {stats.get('public_datasets', 0):,} dataset")
    print(f" - Total Berkas File    : {stats.get('total_resources', 0):,} resources")
    print(f" - Produsen Data (OPD)  : {stats.get('total_organizations', 0)} OPD")
    print(f" - Kategori / Topik     : {stats.get('total_groups', 0)} topik sektoral")
    print(f" - Tag / Kata Kunci     : {stats.get('total_tags', 0)} tag")
    print("==================================================")
    return 0


def cmd_stats(client: SatuDataClient, args: argparse.Namespace) -> int:
    stats = client.get_statistics()
    if args.json:
        print(json.dumps(stats, indent=2))
        return 0

    headers = ["Metrik", "Jumlah"]
    rows = [
        ["Total Dataset", stats.get("total_datasets")],
        ["Dataset Publik", stats.get("public_datasets")],
        ["Dataset Privat", stats.get("private_datasets")],
        ["Total Berkas Resources", stats.get("total_resources")],
        ["Total Produsen Data (OPD)", stats.get("total_organizations")],
        ["Total Topik / Grup", stats.get("total_groups")],
        ["Total Tag Terdaftar", stats.get("total_tags")],
    ]
    print(render_table(headers, rows))
    return 0


def cmd_search(client: SatuDataClient, args: argparse.Namespace) -> int:
    fq = f"organization:{args.opd}" if args.opd else None
    res = client.search_packages(
        q=args.query,
        fq=fq,
        rows=args.rows,
        start=args.start,
        sort=args.sort
    )

    datasets = res.get("results", [])
    if args.group:
        grp_lower = args.group.lower()
        datasets = [
            d for d in datasets
            if any(g.get("name", "").lower() == grp_lower or g.get("title", "").lower() == grp_lower for g in d.get("groups", []))
        ]

    if args.json:
        out = dict(res)
        if args.group:
            out["results"] = datasets
            out["count"] = len(datasets)
        print(json.dumps(out, indent=2))
        return 0

    total_count = res.get("count", 0) if not args.group else len(datasets)
    print(f"\n🔍 Ditemukan {total_count} dataset (menampilkan {len(datasets)} mulai offset {args.start}):\n")
    headers = ["No", "Judul Dataset", "OPD Produsen", "Resources", "Slug/ID"]
    rows = []
    for idx, d in enumerate(datasets, 1):
        org = d.get("organization") or {}
        org_title = org.get("title") or org.get("name") or "-"
        res_count = len(d.get("resources", []))
        slug = d.get("name") or d.get("id")
        title = d.get("title", "")
        title_disp = (title[:47] + "...") if len(title) > 50 else title
        rows.append([str(idx + args.start), title_disp, org_title[:32], f"{res_count} file", slug])

    print(render_table(headers, rows))
    return 0


def cmd_dataset(client: SatuDataClient, args: argparse.Namespace) -> int:
    dataset = client.get_package(args.id_or_slug)
    if args.json:
        print(json.dumps(dataset, indent=2))
        return 0

    org = dataset.get("organization") or {}
    print("\n==================================================")
    print(f"📦 DATASET: {dataset.get('title')}")
    print("==================================================")
    print(f"ID           : {dataset.get('id')}")
    print(f"Slug / Name  : {dataset.get('name')}")
    print(f"Produsen OPD : {org.get('title')} ({org.get('name')})")
    print(f"Author       : {dataset.get('author') or '-'}")
    print(f"Status       : {dataset.get('state')} (Privat: {dataset.get('private')})")
    print(f"Dibuat       : {dataset.get('metadata_created')}")
    print(f"Dimutakhirkan: {dataset.get('metadata_modified')}")
    print(f"Deskripsi    : {dataset.get('notes') or '-'}")

    resources = dataset.get("resources", [])
    print(f"\n📂 DAFTAR BERKAS LAMPIRAN ({len(resources)} file):")
    if resources:
        headers = ["No", "Nama Berkas", "Format", "Tahun/Desc", "Ukuran", "Download URL"]
        rows = []
        for i, r in enumerate(resources, 1):
            sz = f"{r.get('size', 0):,} B" if r.get("size") else "-"
            rows.append([
                str(i),
                r.get("name")[:35],
                r.get("format", "-").upper(),
                str(r.get("description") or "-"),
                sz,
                r.get("url", "")
            ])
        print(render_table(headers, rows))
    else:
        print("  (Belum ada file lampiran)")
    print()
    return 0


def cmd_list_packages(client: SatuDataClient, args: argparse.Namespace) -> int:
    pkgs = client.list_packages(limit=args.limit, offset=args.offset)
    if args.json:
        print(json.dumps(pkgs, indent=2))
        return 0

    print(f"\n📋 Daftar Nama/Slug Dataset ({len(pkgs)} dataset):")
    for idx, p in enumerate(pkgs, 1):
        print(f"  {idx + args.offset}. {p}")
    return 0


def cmd_organizations(client: SatuDataClient, args: argparse.Namespace) -> int:
    orgs = client.list_organizations(all_fields=True)
    if args.json:
        print(json.dumps(orgs, indent=2))
        return 0

    print(f"\n🏢 DAFTAR ORGANISASI PRODUSEN DATA ({len(orgs)} OPD):\n")
    headers = ["No", "Slug Nama OPD", "Nama Resmi Instansi", "Paket Data"]
    rows = []
    for idx, o in enumerate(orgs, 1):
        cnt = str(o.get("package_count")) if o.get("package_count") is not None else "-"
        rows.append([str(idx), o.get("name"), o.get("title"), cnt])
    print(render_table(headers, rows))
    return 0


def cmd_opd(client: SatuDataClient, args: argparse.Namespace) -> int:
    org = client.get_organization(args.id_or_slug)
    datasets = client.search_packages(fq=f"organization:{org.get('name')}", rows=args.rows)

    data = {"organization": org, "datasets": datasets}
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print("\n==================================================")
    print(f"🏢 PRODUSEN DATA: {org.get('title')}")
    print("==================================================")
    print(f"ID          : {org.get('id')}")
    print(f"Slug        : {org.get('name')}")
    print(f"Status      : {org.get('state')}")
    print(f"Dibuat Pada : {org.get('created')}")
    print(f"Logo URL    : {org.get('image_url') or '-'}")

    pkg_list = datasets.get("results", [])
    total = datasets.get("count", 0)
    print(f"\n📦 DATASET DITERBITKAN ({total} total, menampilkan {len(pkg_list)}):\n")
    if pkg_list:
        headers = ["No", "Judul Dataset", "Berkas", "Slug"]
        rows = []
        for i, p in enumerate(pkg_list, 1):
            r_cnt = len(p.get("resources", []))
            rows.append([str(i), p.get("title")[:45], f"{r_cnt} file", p.get("name")])
        print(render_table(headers, rows))
    else:
        print("  (Belum ada dataset yang dipublikasikan)")
    print()
    return 0


def cmd_groups(client: SatuDataClient, args: argparse.Namespace) -> int:
    groups = client.list_groups(all_fields=True)
    if args.json:
        print(json.dumps(groups, indent=2))
        return 0

    print(f"\n📂 DAFTAR TOPIK / KATEGORI SEKTORAL ({len(groups)} topik):\n")
    headers = ["No", "Slug Topik", "Nama Topik", "Deskripsi"]
    rows = []
    for idx, g in enumerate(groups, 1):
        rows.append([str(idx), g.get("name"), g.get("title"), (g.get("description") or "-")[:40]])
    print(render_table(headers, rows))
    return 0


def cmd_tags(client: SatuDataClient, args: argparse.Namespace) -> int:
    tags = client.list_tags(query=args.query)
    if args.json:
        print(json.dumps(tags, indent=2))
        return 0

    filter_info = f" (filter kata kunci: '{args.query}')" if args.query else ""
    print(f"\n🏷️  DAFTAR TAG / KATA KUNCI{filter_info} ({len(tags)} tag):\n")
    for i in range(0, len(tags), 3):
        chunk = tags[i:i+3]
        print("   " + "   |   ".join(f"- {t}" for t in chunk))
    print()
    return 0


def cmd_download(client: SatuDataClient, args: argparse.Namespace) -> int:
    dest = client.download_resource(args.url_or_id, args.output)
    sz = dest.stat().st_size
    if args.json:
        print(json.dumps({"success": True, "path": str(dest.resolve()), "size_bytes": sz}))
        return 0

    print(f"✅ Berhasil mengunduh berkas:")
    print(f" - Lokasi Simpan : {dest.resolve()}")
    print(f" - Ukuran Berkas : {sz:,} bytes")
    return 0


def cmd_preview(client: SatuDataClient, args: argparse.Namespace) -> int:
    rows = client.preview_resource(args.url_or_id, max_rows=args.rows)
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    if not rows:
        print("⚠️ Tidak ada data untuk ditampilkan.")
        return 0

    headers = [f"Col {i+1}: {col}" for i, col in enumerate(rows[0])]
    data_rows = rows[1:] if len(rows) > 1 else []
    print(f"\n👀 Cuplikan {len(data_rows)} Baris Data:\n")
    print(render_table(headers, data_rows))
    return 0


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Base API URL (default: {DEFAULT_BASE_URL})")
    common_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"Timeout dalam detik (default: {DEFAULT_TIMEOUT})")
    common_parser.add_argument("--json", action="store_true", help="Format keluaran JSON deterministik untuk AI agent")

    parser = argparse.ArgumentParser(
        prog="satudata_tool.py",
        description="Portal Satu Data Kabupaten Mempawah CKAN 2.9 API CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common_parser],
        epilog="""
Contoh Penggunaan:
  %(prog)s status
  %(prog)s stats
  %(prog)s search "kesehatan"
  %(prog)s search --opd badan-pengelola-keuangan-dan-aset-daerah
  %(prog)s search --opd dinas-penanaman-modal-koperasi-ukm-dan-pelayanan-terpadu-satu-pintu
  %(prog)s dataset realisasi-jumlah-perizinan-oss-rba-tahun-2021
  %(prog)s opds
  %(prog)s opd badan-pengelola-keuangan-dan-aset-daerah
  %(prog)s groups
  %(prog)s tags --query "pajak"
  %(prog)s preview https://satudata.mempawahkab.go.id/datasets/.../download --rows 5
  %(prog)s download https://satudata.mempawahkab.go.id/datasets/.../download --output /tmp/data.csv
        """
    )

    subparsers = parser.add_subparsers(dest="subcommand", required=True, help="Subperintah yang tersedia")

    # status
    p_status = subparsers.add_parser("status", parents=[common_parser], help="Cek status portal dan versi API")
    p_status.set_defaults(func=cmd_status)

    # stats
    p_stats = subparsers.add_parser("stats", parents=[common_parser], help="Statistik agregat portal")
    p_stats.set_defaults(func=cmd_stats)

    # search
    p_search = subparsers.add_parser("search", parents=[common_parser], help="Cari dataset dengan kata kunci atau filter OPD")
    p_search.add_argument("query", nargs="?", default=None, help="Kata kunci pencarian (judul / catatan)")
    p_search.add_argument("--opd", help="Filter slug OPD (contoh: dinas-kesehatan...)")
    p_search.add_argument("--group", help="Filter kategori/grup (contoh: kesehatan, ekonomi)")
    p_search.add_argument("--rows", type=int, default=10, help="Jumlah dataset per halaman (default: 10)")
    p_search.add_argument("--start", type=int, default=0, help="Offset data pagination (default: 0)")
    p_search.add_argument("--sort", help="Sorting hasil (contoh: 'metadata_modified desc')")
    p_search.set_defaults(func=cmd_search)

    # dataset / show
    p_dataset = subparsers.add_parser("dataset", aliases=["show"], parents=[common_parser], help="Detail lengkap dataset dan file lampiran")
    p_dataset.add_argument("id_or_slug", help="UUID atau slug nama dataset")
    p_dataset.set_defaults(func=cmd_dataset)

    # list
    p_list = subparsers.add_parser("list", parents=[common_parser], help="Daftar seluruh slug nama dataset")
    p_list.add_argument("--limit", type=int, default=50, help="Batas jumlah slug yang diambil (default: 50)")
    p_list.add_argument("--offset", type=int, default=0, help="Offset pagination")
    p_list.set_defaults(func=cmd_list_packages)

    # opds / organizations
    p_opds = subparsers.add_parser("opds", aliases=["organizations"], parents=[common_parser], help="Daftar 23 OPD produsen data")
    p_opds.set_defaults(func=cmd_organizations)

    # opd / organization
    p_opd = subparsers.add_parser("opd", aliases=["organization"], parents=[common_parser], help="Detail OPD dan daftar datasetnya")
    p_opd.add_argument("id_or_slug", help="UUID atau slug OPD")
    p_opd.add_argument("--rows", type=int, default=20, help="Jumlah dataset ditampilkan (default: 20)")
    p_opd.set_defaults(func=cmd_opd)

    # groups / topics
    p_groups = subparsers.add_parser("groups", aliases=["topics"], parents=[common_parser], help="Daftar kategori/topik sektoral")
    p_groups.set_defaults(func=cmd_groups)

    # tags
    p_tags = subparsers.add_parser("tags", parents=[common_parser], help="Daftar kata kunci/tag dataset")
    p_tags.add_argument("--query", "-q", help="Saring tag berdasarkan kata kunci")
    p_tags.set_defaults(func=cmd_tags)

    # download
    p_dl = subparsers.add_parser("download", parents=[common_parser], help="Unduh file resource dataset ke disk lokal")
    p_dl.add_argument("url_or_id", help="Direct download URL atau Resource UUID")
    p_dl.add_argument("--output", "-o", help="Jalur file penyimpanan lokal")
    p_dl.set_defaults(func=cmd_download)

    # preview
    p_prev = subparsers.add_parser("preview", parents=[common_parser], help="Lihat cuplikan tabel CSV/XLSX langsung tanpa download")
    p_prev.add_argument("url_or_id", help="Direct download URL atau Resource UUID")
    p_prev.add_argument("--rows", "-r", type=int, default=10, help="Jumlah baris cuplikan (default: 10)")
    p_prev.set_defaults(func=cmd_preview)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    client = SatuDataClient(base_url=args.base_url, timeout=args.timeout)
    try:
        return args.func(client, args)
    except SatuDataAPIError as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e), "status_code": e.status_code}, indent=2))
        else:
            print(f"❌ Error API Satu Data Mempawah: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan pengguna.", file=sys.stderr)
        return 130
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": f"Internal unexpected error: {str(e)}"}, indent=2))
        else:
            print(f"❌ Terjadi kesalahan tak terduga: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
