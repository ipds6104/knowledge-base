"""
Backmatter Standards Compliance Rule.
Single Responsibility: Verifies Daftar Pustaka exists, starts on Recto, and contains standard citations.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class BackmatterStandardsRule(AuditRule):
    """Memverifikasi kehadiran dan standar format Daftar Pustaka pada bagian penutup buku."""

    @property
    def rule_id(self) -> str:
        return "R16_BACKMATTER_STANDARDS"

    @property
    def name(self) -> str:
        return "Standarisasi Daftar Pustaka & Halaman Ganjil Penutup"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.5.1 (Hal. 104-107)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        found_pustaka = False
        pustaka_page = None

        total_p = len(pages)
        search_start = max(0, total_p - 10)

        for page in pages[search_start:-1]:  # Exclude back cover
            if "DAFTAR PUSTAKA" in page.full_text.upper():
                found_pustaka = True
                pustaka_page = page
                break

        if not found_pustaka or pustaka_page is None:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=total_p - 1,
                    message="Daftar Pustaka (Bibliography) tidak ditemukan pada bagian penutup buku.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.WARNING,
                    measured_value="Tidak ditemukan",
                    expected_value="Ada bagian Daftar Pustaka",
                )
            )
            return violations

        # 1. Verifikasi dimulai di halaman ganjil (Rekto)
        if pustaka_page.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=pustaka_page.page_number,
                    message=f"Daftar Pustaka berada di halaman fisik genap ({pustaka_page.page_number}). Pedoman BPS mewajibkan di halaman ganjil (Rekto).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"Halaman {pustaka_page.page_number} (Verso)",
                    expected_value="Halaman Rekto (Ganjil)",
                )
            )

        # 2. Verifikasi konten sitasi BPS
        if "BADAN PUSAT STATISTIK" not in pustaka_page.full_text.upper():
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=pustaka_page.page_number,
                    message="Daftar Pustaka tidak memuat rujukan publikasi resmi Badan Pusat Statistik.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.WARNING,
                    measured_value=pustaka_page.full_text[:60],
                    expected_value="Memuat rujukan publikasi BPS",
                )
            )

        return violations
