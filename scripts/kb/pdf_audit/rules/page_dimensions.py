"""
Page Dimensions Compliance Rule.
Single Responsibility: Verifies all pages match official BPS A5 dimensions (14.8 x 21.0 cm).
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class PageDimensionsRule(AuditRule):
    """Memverifikasi bahwa seluruh halaman buku publikasi KCDA menggunakan dimensi A5 (14,8 x 21,0 cm)."""

    @property
    def rule_id(self) -> str:
        return "R11_PAGE_DIMENSIONS"

    @property
    def name(self) -> str:
        return "Standar Dimensi Kertas A5 KCDA (14,8 x 21,0 cm)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Bab 1 & 2 (Tabel 1, Hal. 11)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        expected_w_cm = 14.80
        expected_h_cm = 21.00
        tolerance_cm = 0.20  # 2 mm tolerance

        for page in pages:
            diff_w = abs(page.width_cm - expected_w_cm)
            diff_h = abs(page.height_cm - expected_h_cm)

            if diff_w > tolerance_cm or diff_h > tolerance_cm:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message=(
                            f"Dimensi halaman {page.page_number} tidak sesuai standar A5 BPS: "
                            f"{page.width_cm:.2f} x {page.height_cm:.2f} cm (seharusnya 14,8 x 21,0 cm)."
                        ),
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"{page.width_cm:.2f} x {page.height_cm:.2f} cm",
                        expected_value="14,80 x 21,00 cm",
                    )
                )

        return violations
