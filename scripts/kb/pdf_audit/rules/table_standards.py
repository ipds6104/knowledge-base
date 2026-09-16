"""
Table Standards Compliance Rule.
Single Responsibility: Verifies BPS standard table presentation (column numbering bar (1)(2)(3), Table numbering, and Source attribution).
"""

import re
from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class TableStandardsRule(AuditRule):
    """Memverifikasi standar tabel BPS (Tabel Bab.Subbab.No, baris nomor kolom (1)(2)(3), dan sumber data)."""

    @property
    def rule_id(self) -> str:
        return "R10_TABLE_STANDARDS"

    @property
    def name(self) -> str:
        return "Standarisasi Format Tabel BPS (Nomor Kolom (1)(2)(3) & Sumber Data)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.4.2 (Hal. 90-103)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        table_title_pattern = re.compile(r"Tabel\s*/\s*Table\s+\d+\.\d+(\.\d+)?", re.IGNORECASE)
        col_number_pattern = re.compile(r"\(1\)\s*\(2\)", re.IGNORECASE)

        # Look for pages with tables in body
        for page in pages:
            text = page.full_text

            # If page contains a table title
            if "Tabel" in text and ("Table" in text or "Sumber" in text or "Source" in text):
                # 1. Check Table Column Numbering Bar: (1) (2)...
                # Only check if page contains a substantial table header
                if "Tabel / Table" in text:
                    # Look for (1) (2) or (1)
                    has_col_numbers = "(1)" in text and ("(2)" in text or "(1)" in text)
                    if not has_col_numbers:
                        violations.append(
                            Violation(
                                rule_id=self.rule_id,
                                rule_name=self.name,
                                physical_page=page.page_number,
                                message="Tabel BPS wajib menyertakan baris penomoran kolom (1), (2), (3)... di bawah kepala kolom.",
                                pedoman_ref=self.pedoman_ref,
                                severity=Severity.WARNING,
                                measured_value="Baris penomoran (1) (2) tidak ditemukan",
                                expected_value="Baris penomoran kolom '(1)', '(2)', dst.",
                            )
                        )

                # 2. Check Source Attribution
                if "Tabel / Table" in text and "Sumber" not in text and "Source" not in text:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message="Tabel BPS wajib memuat atribusi Sumber Data ('Sumber / Source: ...') di bawah tabel.",
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.WARNING,
                            measured_value="Sumber data tidak ditemukan",
                            expected_value="Teks 'Sumber / Source: [Nama Instansi]'",
                        )
                    )

            # 3. Check Trailing Period on Headings / Subbabs [Subbab 4.1.5 Poin 6, Hal. 53]
            # Forbidden: "1.1." or "2.1.1."
            invalid_subbabs = re.findall(r"\b([1-7]\.\d+(\.\d+)?\.)\s+[A-Z]", text)
            if invalid_subbabs:
                bad_example = invalid_subbabs[0][0]
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name="Larangan Titik Setelah Nomor Subbab Terakhir",
                        physical_page=page.page_number,
                        message=f"Dilarang menaruh titik setelah nomor subbab terakhir ('{bad_example}'). Standar yang benar: '{bad_example[:-1]}'.",
                        pedoman_ref="Pedoman Publikasi BPS 2023 Subbab 4.1.5 Poin 6 (Hal. 53)",
                        severity=Severity.ERROR,
                        measured_value=bad_example,
                        expected_value=bad_example[:-1],
                    )
                )

        return violations
