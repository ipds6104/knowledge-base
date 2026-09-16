"""
Blank Page Hygiene Compliance Rule.
Single Responsibility: Verifies that empty transition pages contain zero leaking headers or footers.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class BlankPageRule(AuditRule):
    """Memverifikasi bahwa seluruh halaman sisipan kosong bersih sempurna dari teks, header, dan footer."""

    @property
    def rule_id(self) -> str:
        return "R04_BLANK_PAGE_HYGIENE"

    @property
    def name(self) -> str:
        return "Kebersihan Halaman Sisipan Kosong (Zero Leakage)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 9 (Hal. 47)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []

        for page in pages:
            # A blank transition page is one where body has no content,
            # but we must ensure it doesn't accidentally have a running header or footer.
            if not page.body_blocks and (page.header_blocks or page.footer_blocks):
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message="Halaman sisipan kosong memuat teks running header atau footer yang bocor.",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"{len(page.header_blocks)} header blocks, {len(page.footer_blocks)} footer blocks",
                        expected_value="Halaman kosong sempurna tanpa teks",
                    )
                )

        return violations
