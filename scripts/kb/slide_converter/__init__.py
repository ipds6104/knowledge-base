"""slide_converter — Modular Slide-to-Markdown Converter Package.

Menerapkan Hexagonal Architecture (Ports & Adapters) dan Single Responsibility Principle:
- Ports: Kontrak interface abstrak (PDFRendererPort, VisionClientPort, MarkdownWriterPort).
- Domain: Entitas data (SlidePage, ConversionResult) dan aturan ekstraksi visual (Mermaid, Tabel, Callout).
- Adapters: Implementasi konkrit pihak luar (PyMuPDF, Top Tools AI Vision API, Local File Writer).
- Service: Orchestrator logika bisnis yang diinjeksi dependensi (SlideConverterService).
"""

from pathlib import Path
from typing import Optional

from .adapters import LocalMarkdownWriter, PyMuPDFRenderer, TopToolsVisionAdapter
from .domain import ConversionResult, SlidePage
from .ports import MarkdownWriterPort, PDFRendererPort, VisionClientPort
from .service import ProgressCallback, SlideConverterService


def create_slide_converter(config: Optional[dict] = None) -> SlideConverterService:
    """Factory function untuk membuat instans SlideConverterService dengan adapter default."""
    cfg = config or {}

    # Gunakan TOP_TOOLS_AI_API_KEY
    api_key = (
        cfg.get("TOP_TOOLS_AI_API_KEY")
        or "sk-6045449828a7e882dd9b39b06f5a20fdc0f5d3d0930ee34d0e287567a2981b22"
    )

    base_url = (
        cfg.get("TOP_TOOLS_AI_BASE_URL")
        or "https://top-tools-ai.com/api/v1"
    )

    model = (
        cfg.get("TOP_TOOLS_AI_MODEL")
        or "Top-Tools-Ai"
    )

    renderer = PyMuPDFRenderer(default_dpi=200)
    vision_client = TopToolsVisionAdapter(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )
    writer = LocalMarkdownWriter()

    return SlideConverterService(
        renderer=renderer,
        vision_client=vision_client,
        writer=writer,
    )


__all__ = [
    "PDFRendererPort",
    "VisionClientPort",
    "MarkdownWriterPort",
    "SlidePage",
    "ConversionResult",
    "SlideConverterService",
    "ProgressCallback",
    "PyMuPDFRenderer",
    "TopToolsVisionAdapter",
    "LocalMarkdownWriter",
    "create_slide_converter",
]
