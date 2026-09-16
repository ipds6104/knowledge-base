"""
TOC Integrity and Prohibited Naming Rule.
Single Responsibility: Verifies Table of Contents starts on Recto and enforces prohibition of 'Daftar Grafik'.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class TocIntegrityRule(AuditRule):
    """Memverifikasi keutuhan Daftar Isi dan kepatuhan nomenklatur Daftar Gambar BPS."""

    @property
    def rule_id(self) -> str:
        return "R15_TOC_INTEGRITY"

    @property
    def name(self) -> str:
        return "Integritas Daftar Isi & Larangan Nomenklatur 'Daftar Grafik'"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.3 Poin 7-9 (Hal. 84-86)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        found_toc = False
        toc_page = None

        for page in pages[:15]:
            if "DAFTAR ISI" in page.full_text.upper():
                found_toc = True
                toc_page = page
                break

        if not found_toc or toc_page is None:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=7,
                    message="Daftar Isi (Table of Contents) tidak ditemukan pada bagian prelims publikasi.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Tidak ditemukan",
                    expected_value="Ada halaman Daftar Isi",
                )
            )
            return violations

        # 1. Verifikasi Daftar Isi dimulai di halaman ganjil (Rekto)
        if toc_page.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=toc_page.page_number,
                    message=f"Daftar Isi dimulai di halaman fisik genap ({toc_page.page_number}). Pedoman BPS mewajibkan di halaman ganjil (Rekto).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"Halaman {toc_page.page_number} (Verso)",
                    expected_value="Halaman Rekto (Ganjil)",
                )
            )

        # 2. Verifikasi Larangan "Daftar Grafik" di seluruh buku (Hal. 86)
        for page in pages:
            if "DAFTAR GRAFIK" in page.full_text.upper():
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message=(
                            f"Ditemukan judul 'DAFTAR GRAFIK' pada halaman {page.page_number}. "
                            "Pedoman BPS melarang keras penggunaan istilah 'Daftar Grafik' dan mewajibkan penamaan 'Daftar Gambar' (Hal. 86)."
                        ),
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value="Judul 'DAFTAR GRAFIK'",
                        expected_value="Judul 'Daftar Gambar / List of Figures'",
                    )
                )

        return violations
