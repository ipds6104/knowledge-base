"""CLI Handler Perintah DDA (Desa Dalam Angka Generator Engine).

Memproses penarikan data, kalkulasi indikator DTO, dan kompilasi publikasi Desa Dalam Angka.
"""

import os
from kb.dda_generator import (
    get_desa_config,
    fetch_desa_data,
    calculate_desa_metrics,
    build_capabilities_dto,
    DesaPublicationData,
    render_desa_md,
    render_desa_html,
    compile_html_to_pdf,
)


def handle_dda(args):
    """Handler utama subcommand 'kb dda'."""
    name_kebab = args.nama_desa.strip().lower()
    sheet_id = getattr(args, "sheet_id", None)
    year = getattr(args, "year", 2026)

    print("\n=======================================================")
    print(f"  BPS DDA GENERATOR ENGINE — DESA {name_kebab.upper()}")
    print("=======================================================\n")

    config = get_desa_config(name_kebab, sheet_id=sheet_id, year=year)
    print(f"Konfigurasi Desa: {config['name_title']} (Pub No: {config['pub_no']})")

    # Step 1: Ingestion (Layer 1)
    rt_data, fas_data = fetch_desa_data(config)
    if not rt_data:
        print("Error: Tidak ada data RT yang ditemukan untuk desa ini.")
        return

    # Step 2: Calculation (Layer 1)
    print("Mengalkulasi indikator statistik baku...")
    metrics = calculate_desa_metrics(rt_data, fas_raw_list=fas_data, pub_config=config)
    capabilities = build_capabilities_dto(metrics, config=config)

    print(f"  -> Total Penduduk: {metrics['tot_pop']:,} jiwa")
    print(f"  -> Total Bumbung Rumah: {metrics['tot_bumbung']:,} unit")
    print(f"  -> Total KK: {metrics['tot_kk']:,} KK")

    # Step 3: Package Data Contract DTO (Layer 1)
    pub_data = DesaPublicationData(
        config=config,
        metrics=metrics,
        capabilities=capabilities,
        raw_rt_data=rt_data,
        raw_fas_data=fas_data,
    )

    # Step 4: Render Markdown (Layer 3 Adapter)
    print("Menyusun naskah Markdown 5 Bab...")
    md_path = render_desa_md(pub_data)

    # Step 5: Render HTML (Layer 3 Adapter)
    print("Menyusun layout HTML BPS bilingual A4...")
    html_path = render_desa_html(pub_data)

    # Step 6: Compile PDF (Layer 3 Adapter)
    prefix = "publikasi-kelurahan" if config.get("is_kelurahan") else "publikasi-desa"
    pdf_filename = f"{prefix}-{config['name_kebab']}-dalam-angka-{config.get('year', 2026)}.pdf"
    pdf_path = html_path.parent / pdf_filename
    print("Mengompilasi PDF Siap Cetak A4...")
    compiled_pdf = compile_html_to_pdf(html_path, pdf_path)

    # Step 6b: Compile DOCX dari PDF (preservasi visual rapi BPS)
    docx_filename = f"{prefix}-{config['name_kebab']}-dalam-angka-{config.get('year', 2026)}.docx"
    docx_path = html_path.parent / docx_filename
    outputs_dir = html_path.parent.parent / "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    docx_copy = outputs_dir / docx_filename
    compiled_docx = None

    try:
        from pdf2docx import Converter
        import shutil
        print("Mengompilasi DOCX dari PDF resmi...")
        cv = Converter(str(pdf_path))
        cv.convert(str(docx_path), start=0, end=None)
        cv.close()
        print(f"DOCX rapi berhasil dikompilasi dari PDF: {docx_path}")
        shutil.copy(docx_path, docx_copy)
        compiled_docx = docx_path
    except Exception as e:
        print(f"Menggunakan fallback Pandoc untuk DOCX ({e})...")
        try:
            import subprocess, shutil
            cmd_docx = ["pandoc", str(md_path), "-o", str(docx_path)]
            res_docx = subprocess.run(cmd_docx, capture_output=True, text=True)
            if res_docx.returncode == 0:
                print(f"DOCX berhasil dikompilasi via Pandoc: {docx_path}")
                shutil.copy(docx_path, docx_copy)
                compiled_docx = docx_path
        except Exception:
            pass

    print("\n=======================================================")
    print("  SUKSES! PUBLIKASI DESA DALAM ANGKA BERHASIL DIBUAT")
    print("=======================================================")
    print(f"  1. Markdown : {md_path}")
    print(f"  2. HTML     : {html_path}")
    print(f"  3. PDF      : {compiled_pdf}")
    if compiled_docx:
        print(f"  4. DOCX     : {compiled_docx}")
    print(f"  5. Outputs  : outputs/{pdf_filename} & outputs/{docx_filename}\n")

    # Step 7: Auto-upload ke Google Drive jika token.json ada
    if not getattr(args, "no_upload", False) and os.path.exists("token.json"):
        from kb import cmd_gdrive_mirror
        import argparse
        print("🚀 Memulai auto-upload ke Google Drive...")
        upload_args = argparse.Namespace(
            source_path="kegiatan/desa-cantik",
            folder_id=None,
            dry_run=False,
            force=False
        )
        cmd_gdrive_mirror.run_gdrive_mirror(upload_args)
