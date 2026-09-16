"""
Preface Compliance Rule.
Single Responsibility: Verifies Kata Pengantar format, recto start, and Regency Capital signatory.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class PrefaceComplianceRule(AuditRule):
    """Memverifikasi kepatuhan halaman Kata Pengantar terhadap standar BPS 2023."""

    @property
    def rule_id(self) -> str:
        return "R13_PREFACE_COMPLIANCE"

    @property
    def name(self) -> str:
        return "Standarisasi Kata Pengantar & Lokasi TTD Ibu Kota"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.3 Poin 6 (Hal. 82-84)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        found_preface = False
        preface_page = None

        for page in pages[:15]:
            if "KATA PENGANTAR" in page.full_text.upper():
                found_preface = True
                preface_page = page
                break

        if not found_preface or preface_page is None:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=5,
                    message="Halaman Kata Pengantar tidak ditemukan pada bagian prelims publikasi.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Tidak ditemukan",
                    expected_value="Ada halaman Kata Pengantar",
                )
            )
            return violations

        # 1. Periksa halaman ganjil (Rekto)
        if preface_page.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=preface_page.page_number,
                    message=f"Kata Pengantar berada di halaman fisik genap ({preface_page.page_number}). Pedoman BPS mewajibkan di halaman ganjil (Rekto).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"Halaman {preface_page.page_number} (Verso)",
                    expected_value="Halaman Rekto (Ganjil)",
                )
            )

        # 2. Periksa Tempat Tanda Tangan Wajib Ibu Kota ("Mempawah")
        if "Mempawah" not in preface_page.full_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=preface_page.page_number,
                    message="Lokasi penandatanganan Kata Pengantar tidak mencantumkan nama Ibu Kota Kabupaten ('Mempawah').",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Tidak ada kata 'Mempawah'",
                    expected_value="Mempawah, [Bulan] [Tahun]",
                )
            )

        # 3. Periksa Jabatan Penandatangan (Kepala BPS)
        if "KEPALA BPS" not in preface_page.full_text.upper() and "KEPALA BADAN PUSAT STATISTIK" not in preface_page.full_text.upper():
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=preface_page.page_number,
                    message="Kata Pengantar sebaiknya ditandatangani oleh Kepala BPS Kabupaten/Kota.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.WARNING,
                    measured_value=preface_page.full_text[-100:],
                    expected_value="Kepala BPS Kabupaten Mempawah",
                )
            )

        return violations
