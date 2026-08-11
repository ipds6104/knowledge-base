"""DDA Generator Subpackage.
Universal Decoupled Architecture Engine for BPS Publication Generation.
"""

from pathlib import Path
from .config import DESA_CONFIGS, get_desa_config
from .fetcher import fetch_desa_data
from .calculator import calculate_desa_metrics, build_capabilities_dto
from .schemas import DesaPublicationData, VillageConfigDTO, StatisticalMetricsDTO, DatasetCapabilitiesDTO
from .renderers import render_desa_html, render_desa_md, compile_html_to_pdf


def generate_publication(desa_kebab: str, sheet_id: str = None, year: int = 2026) -> dict:
    """Pipeline eksekusi terkoordinasi: Ingest -> Calculate -> DTO Contract -> Render Adapters -> PDF."""
    config = get_desa_config(desa_kebab, sheet_id=sheet_id, year=year)

    print("=======================================================")
    print(f"  BPS DDA GENERATOR ENGINE — DESA {config['name_upper']}")
    print("=======================================================")
    print(f"Konfigurasi Desa: {config['name_title']} (Pub No: {config.get('pub_no')})")

    # Layer 1: Ingest Data
    rt_data, fas_data = fetch_desa_data(config)

    # Layer 1: Pure Statistical Calculation
    print("Mengalkulasi indikator statistik baku...")
    metrics = calculate_desa_metrics(rt_data, pub_config=config, fas_raw_list=fas_data)
    capabilities = build_capabilities_dto(metrics, config=config)

    print(f"  -> Total Penduduk: {metrics['tot_pop']:,} jiwa")
    print(f"  -> Total Bumbung Rumah: {metrics['tot_bumbung']:,} unit")
    print(f"  -> Total KK: {metrics['tot_kk']:,} KK")

    # Layer 1: Package Data Contract DTO
    pub_data = DesaPublicationData(
        config=config,
        metrics=metrics,
        capabilities=capabilities,
        raw_rt_data=rt_data,
        raw_fas_data=fas_data
    )

    # Layer 3: Render Markdown
    print("Menyusun naskah Markdown 5 Bab...")
    md_path = render_desa_md(pub_data)

    # Layer 3: Render HTML/CSS
    print("Menyusun layout HTML BPS bilingual A4...")
    html_path = render_desa_html(pub_data)

    # Layer 3: Compile PDF via Headless Chrome
    pdf_filename = f"publikasi-desa-{config['name_kebab']}-dalam-angka-{config.get('year', 2026)}.pdf"
    pdf_path = html_path.parent / pdf_filename
    print("Mengompilasi PDF Siap Cetak A4...")
    compiled_pdf = compile_html_to_pdf(html_path, pdf_path)

    return {
        "md": md_path,
        "html": html_path,
        "pdf": compiled_pdf,
        "outputs": Path("outputs") / pdf_filename if compiled_pdf else None
    }


__all__ = [
    "DESA_CONFIGS",
    "get_desa_config",
    "fetch_desa_data",
    "calculate_desa_metrics",
    "build_capabilities_dto",
    "DesaPublicationData",
    "DatasetCapabilitiesDTO",
    "VillageConfigDTO",
    "StatisticalMetricsDTO",
    "render_desa_html",
    "render_desa_md",
    "compile_html_to_pdf",
    "generate_publication",
]
