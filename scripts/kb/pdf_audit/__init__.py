"""
PDF Layout Compliance Audit Package for BPS Publications.
Provides automated layout, geometry, and publishing guideline auditing tools.
"""

from .models import (
    Severity,
    TextBlock,
    PageGeometry,
    Violation,
    AuditResult,
)
from .inspector import PdfInspector
from .rules import (
    AuditRule,
    FlyleafRule,
    FrontmatterSequenceRule,
    ChapterDividerRule,
    BlankPageRule,
    SafetyTrimMarginRule,
    DuplexPrintabilityRule,
    RunningTitleContentRule,
    BookPageThresholdRule,
    CoverComplianceRule,
    TableStandardsRule,
    PageDimensionsRule,
    ChapterOddStartRule,
    PrefaceComplianceRule,
    EarlyPrelimsSuppressionRule,
    TocIntegrityRule,
    BackmatterStandardsRule,
    ExplanatoryNotesRule,
    get_default_kcda_rules,
)
from .auditor import KcdaPdfAuditor

__all__ = [
    "Severity",
    "TextBlock",
    "PageGeometry",
    "Violation",
    "AuditResult",
    "PdfInspector",
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
    "KcdaPdfAuditor",
]
