"""BPS Potensi Desa (PODES) Publication Generator Package."""

from .config import get_podes_config, PODES_VILLAGE_CONFIGS
from .fetcher import fetch_podes_data
from .calculator import calculate_podes_metrics
from .schemas import PodesPublicationData
from .renderers.md_renderer import render_podes_md
from .renderers.html_renderer import render_podes_html
from .pdf_compiler import compile_podes_pdf

__all__ = [
    "get_podes_config",
    "PODES_VILLAGE_CONFIGS",
    "fetch_podes_data",
    "calculate_podes_metrics",
    "PodesPublicationData",
    "render_podes_md",
    "render_podes_html",
    "compile_podes_pdf",
    "generate_podes_publication",
]


def generate_podes_publication(name_kebab: str) -> dict:
    """Menggenerasikan seluruh artifak publikasi PODES (MD, HTML, PDF, DOCX) untuk desa/kelurahan tertentu."""
    config = get_podes_config(name_kebab)
    raw_data = fetch_podes_data(config)
    pub_data = calculate_podes_metrics(raw_data, config)

    md_path = render_podes_md(pub_data)
    html_path = render_podes_html(pub_data)
    pdf_path = compile_podes_pdf(html_path, config)

    return {
        "md": md_path,
        "html": html_path,
        "pdf": pdf_path,
        "config": config,
    }
