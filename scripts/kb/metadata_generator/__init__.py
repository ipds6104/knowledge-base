"""Metadata Generator Package for Satu Data Indonesia (SDI).

Decoupled DTO & Engine architecture for metadata compilation.
"""

from .schemas import DesaMetadataDTO
from .builder import build_desa_metadata_dto
from .renderers.markdown_renderer import render_metadata_markdown
from .renderers.typst_renderer import render_metadata_typst

__all__ = [
    "DesaMetadataDTO",
    "build_desa_metadata_dto",
    "render_metadata_markdown",
    "render_metadata_typst",
]
