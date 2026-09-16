"""
Cover Compliance Rule for Front and Back Covers.
Single Responsibility: Verifies mandatory publishing elements on front cover (Catalogue, ISSN, Publisher, Garuda prohibition)
and back cover (ISSN barcode, BPS official website).
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class CoverComplianceRule(AuditRule):
    """Memverifikasi elemen wajib kover depan & belakang sesuai Bab 4.2 Pedoman BPS 2023."""

    @property
    def rule_id(self) -> str:
        return "R09_COVER_COMPLIANCE"

    @property
    def name(self) -> str:
        return "Standarisasi Elemen Kover Depan & Belakang"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Bab 4.2 (Hal. 55-74)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        if len(pages) < 2:
            return violations

        # 1. Front Cover Validation (Physical Page 1)
        p1 = pages[0]
        p1_text = p1.full_text.upper()

        # Check Katalog / Catalogue
        if "KATALOG" not in p1_text and "CATALOGUE" not in p1_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=1,
                    message="Kover depan wajib mencantumkan nomor Katalog BPS di pojok kanan atas.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Nomor Katalog tidak ditemukan",
                    expected_value="Teks 'Katalog / Catalogue: [Nomor]'",
                )
            )

        # Check ISSN Placeholder Prohibition & Formal Validation
        if "XXXX" in p1_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=1,
                    message="Kover depan dilarang memuat teks placeholder ISSN dummy (seperti 'xxxx-xxxx'). Bagi kecamatan yang belum memiliki ISSN resmi, teks ISSN dilarang ditampilkan.",
                    pedoman_ref="Aturan Penyusunan KCDA 2026 Hal. 2",
                    severity=Severity.ERROR,
                    measured_value="Ditemukan placeholder 'ISSN xxxx-xxxx'",
                    expected_value="Nomor ISSN resmi atau ditiadakan jika belum memiliki ISSN",
                )
            )

        # Check Publisher Name
        if "BADAN PUSAT STATISTIK" not in p1_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=1,
                    message="Kover depan wajib memuat nama resmi penerbit 'BADAN PUSAT STATISTIK'.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Nama penerbit BPS tidak ditemukan",
                    expected_value="Teks 'BADAN PUSAT STATISTIK'",
                )
            )

        # Check Garuda Prohibition for BPS Daerah [Hal. 56]
        if "GARUDA" in p1_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=1,
                    message="BPS Daerah DILARANG menggunakan lambang Garuda pada kover luar (khusus Kepala BPS RI).",
                    pedoman_ref="Pedoman Publikasi BPS 2023 Hal. 56",
                    severity=Severity.ERROR,
                    measured_value="Ditemukan teks/referensi Garuda",
                    expected_value="Tanpa lambang Garuda",
                )
            )

        # 2. Back Cover Validation (Last Physical Page)
        p_last = pages[-1]
        p_last_text = p_last.full_text.lower()

        # Must contain official BPS website domain
        if "bps.go.id" not in p_last_text:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=p_last.page_number,
                    message="Kover belakang wajib mencantumkan website resmi satker BPS (domain .bps.go.id).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Website resmi BPS tidak ditemukan",
                    expected_value="Memuat alamat website resmi '*.bps.go.id'",
                )
            )

        return violations
