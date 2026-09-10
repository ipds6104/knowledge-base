"""adapters/__init__.py — Concrete driven adapters."""

from .renderer_pymupdf import PyMuPDFRenderer
from .vision_toptools import TopToolsVisionAdapter
from .writer_local import LocalMarkdownWriter

__all__ = [
    "PyMuPDFRenderer",
    "TopToolsVisionAdapter",
    "LocalMarkdownWriter",
]
