"""
Rules package registry for PDF publishing compliance audits.
Single Responsibility: Central registry and factory for all BPS publishing compliance rules.
"""

from typing import List
from .base import AuditRule
from .flyleaf import FlyleafRule
from .frontmatter import FrontmatterSequenceRule
from .chapter_divider import ChapterDividerRule
from .blank_page import BlankPageRule
from .margins import SafetyTrimMarginRule
from .duplex import DuplexPrintabilityRule
from .running_title import RunningTitleContentRule
from .book_threshold import BookPageThresholdRule
from .cover_compliance import CoverComplianceRule
from .table_standards import TableStandardsRule
from .page_dimensions import PageDimensionsRule
from .chapter_odd_start import ChapterOddStartRule
from .preface_compliance import PrefaceComplianceRule
from .early_prelims_suppression import EarlyPrelimsSuppressionRule
from .toc_integrity import TocIntegrityRule
from .backmatter_standards import BackmatterStandardsRule
from .explanatory_notes import ExplanatoryNotesRule


def get_default_kcda_rules() -> List[AuditRule]:
    """Mengembalikan daftar 17 aturan kepatuhan baku untuk publikasi KCDA 2026."""
    return [
        FlyleafRule(),
        FrontmatterSequenceRule(),
        ChapterDividerRule(),
        BlankPageRule(),
        SafetyTrimMarginRule(),
        DuplexPrintabilityRule(),
        RunningTitleContentRule(),
        BookPageThresholdRule(),
        CoverComplianceRule(),
        TableStandardsRule(),
        PageDimensionsRule(),
        ChapterOddStartRule(),
        PrefaceComplianceRule(),
        EarlyPrelimsSuppressionRule(),
        TocIntegrityRule(),
        BackmatterStandardsRule(),
        ExplanatoryNotesRule(),
    ]


__all__ = [
    "AuditRule",
    "FlyleafRule",
    "FrontmatterSequenceRule",
    "ChapterDividerRule",
    "BlankPageRule",
    "SafetyTrimMarginRule",
    "DuplexPrintabilityRule",
    "RunningTitleContentRule",
    "BookPageThresholdRule",
    "CoverComplianceRule",
    "TableStandardsRule",
    "PageDimensionsRule",
    "ChapterOddStartRule",
    "PrefaceComplianceRule",
    "EarlyPrelimsSuppressionRule",
    "TocIntegrityRule",
    "BackmatterStandardsRule",
    "ExplanatoryNotesRule",
    "get_default_kcda_rules",
]

