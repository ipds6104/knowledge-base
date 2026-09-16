"""
Automated Layout Compliance Test Suite for Kecamatan Dalam Angka (KCDA) 2026.
Evaluates compiled Typst PDFs against Pedoman Pembuatan Publikasi BPS Edisi 2023.

Usage:
  python3 -m unittest tests/test_kcda_pdf_compliance.py
  python3 -m unittest discover tests -v
"""

import sys
import unittest
from pathlib import Path
from typing import List

# Ensure scripts/ directory is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from kb.pdf_audit import (
    KcdaPdfAuditor,
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
    Severity,
)

KCDA_OUTPUTS_DIR = REPO_ROOT / "kegiatan/kecamatan-dalam-angka/2026/outputs"


class TestKcdaPdfCompliance(unittest.TestCase):
    """Test Suite verifying physical PDF layout compliance with BPS 2023 Guidelines."""

    @classmethod
    def setUpClass(cls):
        """Finds all compiled KCDA PDFs in the repository outputs directory."""
        cls.pdf_files = sorted(list(KCDA_OUTPUTS_DIR.glob("*/kcda-2026-*.pdf")))
        cls.auditor = KcdaPdfAuditor()

    def test_01_compiled_pdfs_exist(self):
        """Verifies that all 9 kecamatan have compiled PDF files ready in outputs/."""
        self.assertGreaterEqual(
            len(self.pdf_files),
            9,
            f"Ditemukan {len(self.pdf_files)} PDF, diharapkan minimal 9 berkas PDF kecamatan.",
        )

    def test_02_flyleaf_rule_blank_page_2(self):
        """[R01] Halaman 2 (flyleaf di balik kover luar) harus 100% kosong (Hal. 45)."""
        rule = FlyleafRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Flyleaf pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message}" for v in error_violations),
                )

    def test_03_frontmatter_anatomy_and_roman_numbering(self):
        """[R02] Anatomi prelims dan penomoran romawi kecil sesuai prinsip Rekto-Verso (Hal. 46, 75)."""
        rule = FrontmatterSequenceRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Frontmatter pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_04_chapter_dividers_suppress_header_and_footer(self):
        """[R03] Halaman pembatas bab dilarang memuat running header dan footer (Hal. 47, 88)."""
        rule = ChapterDividerRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Halaman Pembatas Bab pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_05_blank_pages_hygiene(self):
        """[R04] Seluruh halaman sisipan kosong harus bersih sempurna tanpa teks bocor (Hal. 47)."""
        rule = BlankPageRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Halaman Kosong Sisipan pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_06_safety_trim_and_margins(self):
        """[R05] Jarak running header/footer ke tepi kertas minimal 0.85 cm (standar 1.00 cm) (Hal. 49-51)."""
        rule = SafetyTrimMarginRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Safety Trim / Margin pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_07_duplex_printability_even_page_count(self):
        """[R06] Total halaman buku harus genap dan kover belakang berada di lembar Verso genap (Hal. 44, 91)."""
        rule = DuplexPrintabilityRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Kesiapan Cetak Dupleks pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_08_running_title_content_and_bilingual_placement(self):
        """[R07] Judul Publikasi di Halaman Genap, Judul Bab di Halaman Ganjil, Kosong di Prelims (Hal. 49-52)."""
        rule = RunningTitleContentRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Konten Running Title pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_09_book_page_threshold_and_proportions(self):
        """[R08] Ketebalan minimal buku (>= 48 hal), prelims genap, dan prelims < arab (Hal. 7, 46-47)."""
        rule = BookPageThresholdRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Ambang Halaman Buku pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_10_cover_compliance_front_and_back(self):
        """[R09] Elemen wajib kover depan (Katalog, ISSN, Penerbit, Tanpa Garuda) & kover belakang (ISSN, Web) (Hal. 55-74)."""
        rule = CoverComplianceRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Standarisasi Kover pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_11_table_standards_and_numbering(self):
        """[R10] Standarisasi tabel BPS (Penomoran Kolom (1)(2)(3), Sumber data, larangan titik subbab) (Hal. 53, 90-103)."""
        rule = TableStandardsRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Standarisasi Tabel pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_12_page_dimensions_a5(self):
        """[R11] Standar Dimensi Kertas A5 KCDA (14,8 x 21,0 cm) (Hal. 11)."""
        rule = PageDimensionsRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Dimensi Kertas A5 pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_13_chapter_odd_page_start(self):
        """[R12] Setiap bab baru wajib dimulai pada halaman ganjil / Rekto (Hal. 47, 88)."""
        rule = ChapterOddStartRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Halaman Awal Bab pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_14_preface_compliance(self):
        """[R13] Standarisasi Kata Pengantar & Penandatanganan Ibu Kota Mempawah (Hal. 82-84)."""
        rule = PrefaceComplianceRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Format Kata Pengantar pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_15_early_prelims_suppression(self):
        """[R14] Nomor romawi fisik ditekan pada 4 halaman awal prelims (Hal. i s.d. iv) (Hal. 47, 81)."""
        rule = EarlyPrelimsSuppressionRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Penekanan Nomor Prelims Awal pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_16_toc_integrity(self):
        """[R15] Integritas Daftar Isi (Rekto) & Larangan Nomenklatur 'Daftar Grafik' (Hal. 84-86)."""
        rule = TocIntegrityRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Integritas Daftar Isi pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_17_backmatter_standards(self):
        """[R16] Standarisasi Daftar Pustaka (dimulai di Rekto & sitasi resmi BPS) (Hal. 104-107)."""
        rule = BackmatterStandardsRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Standar Daftar Pustaka pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_18_explanatory_notes(self):
        """[R17] Penjelasan Umum (dimulai di Rekto & simbol statistik baku BPS) (Hal. 87, 325-337)."""
        rule = ExplanatoryNotesRule()
        auditor = KcdaPdfAuditor(rules=[rule])

        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = auditor.audit_file(pdf)
                error_violations = [v for v in result.violations if v.severity == Severity.ERROR]
                self.assertEqual(
                    len(error_violations),
                    0,
                    f"Pelanggaran Penjelasan Umum pada {pdf.parent.name}:\n"
                    + "\n".join(f"- Hal {v.physical_page}: {v.message} ({v.measured_value})" for v in error_violations),
                )

    def test_19_full_audit_all_kecamatan(self):
        """Audit menyeluruh (semua 17 aturan gabungan) pada seluruh 9 publikasi KCDA 2026."""
        for pdf in self.pdf_files:
            with self.subTest(kecamatan=pdf.parent.name):
                result = self.auditor.audit_file(pdf)
                self.assertTrue(
                    result.is_passed,
                    f"Kecamatan {pdf.parent.name} tidak lulus audit!\n"
                    + KcdaPdfAuditor.format_cli_report(result),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
