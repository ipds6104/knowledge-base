"""Subcommand untuk pembuatan dan kompilasi Metadata Statistik Sektoral (Satu Data Indonesia).

Menggunakan arsitektur Decoupled DTO & Engine (kb.metadata_generator).
"""

import os
import subprocess
import shutil
from pathlib import Path
from kb import Colors
from kb.metadata_generator import (
    build_desa_metadata_dto,
    render_metadata_markdown,
    render_metadata_typst,
)


def register_parser(subparsers):
    parser = subparsers.add_parser(
        "metadata", 
        help="Pembuatan dan kompilasi PDF Metadata Satu Data Indonesia (SDI) Desa Cantik 2026."
    )
    parser.add_argument(
        "desa", 
        choices=["sungai-bakau-kecil", "pasir-palembang", "pasir-wan-salim"],
        help="Nama desa sasaran pembinaan Desa Cantik."
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Jangan upload hasil ke Google Drive secara otomatis."
    )
    return parser


def run(args):
    desa_kebab = args.desa
    desa_title = " ".join(word.capitalize() for word in desa_kebab.split("-"))
    
    print(f"{Colors.BLUE}Memulai penyusunan metadata untuk: {Colors.BOLD}{desa_title}{Colors.ENDC}...")
    
    # 1. Build Single Source of Truth DTO
    dto = build_desa_metadata_dto(desa_kebab, desa_title)
    
    # Tentukan path output
    workspace_root = Path(__file__).resolve().parent.parent.parent
    village_dir = workspace_root / "kegiatan" / "desa-cantik" / "2026" / desa_kebab
    outputs_dir = workspace_root / "kegiatan" / "desa-cantik" / "2026" / "outputs"
    
    os.makedirs(village_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    md_out = village_dir / f"metadata-descan-{desa_kebab}-2026.md"
    pdf_out = village_dir / f"metadata-descan-{desa_kebab}-2026.pdf"
    pdf_copy = outputs_dir / f"metadata-descan-{desa_kebab}-2026.pdf"
    docx_out = village_dir / f"metadata-descan-{desa_kebab}-2026.docx"
    docx_copy = outputs_dir / f"metadata-descan-{desa_kebab}-2026.docx"
    
    # 2. Render & Write Markdown
    md_content = render_metadata_markdown(dto)
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"{Colors.GREEN}Markdown metadata ditulis di: {md_out}{Colors.ENDC}")
    
    # 3. Render & Write Typst
    tmp_dir = Path("/home/ihza/.gemini/antigravity-ide/brain/ae073056-e26b-4aa6-ae4f-4d00ac588abb/scratch")
    os.makedirs(tmp_dir, exist_ok=True)
    typst_temp = tmp_dir / f"metadata_{desa_kebab}.typ"
    
    typst_content = render_metadata_typst(dto)
    with open(typst_temp, "w", encoding="utf-8") as f:
        f.write(typst_content)
    
    # 4. Compile Typst PDF & DOCX
    try:
        cmd = ["typst", "compile", str(typst_temp), str(pdf_out)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"{Colors.GREEN}PDF berhasil dikompilasi di: {pdf_out}{Colors.ENDC}")
            shutil.copy(pdf_out, pdf_copy)
            print(f"{Colors.GREEN}Salinan PDF dibuat di: {pdf_copy}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Gagal kompilasi PDF via Typst: {res.stderr}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.FAIL}Aplikasi 'typst' tidak terpasang di sistem. Silakan install via pacman.{Colors.ENDC}")

    try:
        from pdf2docx import Converter
        print(f"{Colors.BLUE}Mengompilasi DOCX dari PDF resmi Typst...{Colors.ENDC}")
        cv = Converter(str(pdf_out))
        cv.convert(str(docx_out), start=0, end=None)
        cv.close()
        print(f"{Colors.GREEN}DOCX rapi berhasil dikompilasi dari PDF di: {docx_out}{Colors.ENDC}")
        shutil.copy(docx_out, docx_copy)
        print(f"{Colors.GREEN}Salinan DOCX dibuat di: {docx_copy}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}Menggunakan fallback Pandoc untuk DOCX ({e})...{Colors.ENDC}")
        try:
            cmd_docx = ["pandoc", str(md_out), "-o", str(docx_out)]
            res_docx = subprocess.run(cmd_docx, capture_output=True, text=True)
            if res_docx.returncode == 0:
                print(f"{Colors.GREEN}DOCX berhasil dikompilasi di: {docx_out}{Colors.ENDC}")
                shutil.copy(docx_out, docx_copy)
                print(f"{Colors.GREEN}Salinan DOCX dibuat di: {docx_copy}{Colors.ENDC}")
        except Exception:
            pass

    # 5. Auto-upload ke Google Drive
    if not getattr(args, "no_upload", False) and os.path.exists("token.json"):
        from kb import cmd_gdrive_mirror
        import argparse
        print(f"\n{Colors.BLUE}🚀 Memulai auto-upload ke Google Drive...{Colors.ENDC}")
        upload_args = argparse.Namespace(
            source_path="kegiatan/desa-cantik",
            folder_id=None,
            dry_run=False,
            force=False
        )
        cmd_gdrive_mirror.run_gdrive_mirror(upload_args)
