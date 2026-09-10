"""Module for EPSS weighting definitions, IPS calculations, and scenario simulations.

Menghitung Indeks Pembangunan Statistik (IPS) berdasarkan 5 Domain, 19 Aspek, dan 38 Indikator EPSS.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class IndicatorDef:
    code: str
    name: str
    domain_id: int
    domain_name: str
    domain_weight: float  # e.g. 0.28
    aspect_id: int
    aspect_name: str
    aspect_weight: float  # e.g. 0.25
    ind_weight_in_aspect: float  # e.g. 1.00
    official_relative_pct: float  # from BPS slides, e.g. 7.00

    @property
    def exact_relative_weight(self) -> float:
        return self.domain_weight * self.aspect_weight * self.ind_weight_in_aspect

# Master definition of all 38 indicators according to official BPS EPSS 2026 slides
EPSS_INDICATORS: List[IndicatorDef] = [
    # DOMAIN 1: PRINSIP SATU DATA INDONESIA (28%)
    IndicatorDef("10101", "Penerapan Standar Data Statistik (SDS)", 1, "Prinsip Satu Data Indonesia", 0.28, 1, "Standar Data Statistik", 0.25, 1.00, 7.00),
    IndicatorDef("10201", "Penerapan Metadata Statistik", 1, "Prinsip Satu Data Indonesia", 0.28, 2, "Metadata Statistik", 0.25, 1.00, 7.00),
    IndicatorDef("10301", "Penerapan Interoperabilitas Data", 1, "Prinsip Satu Data Indonesia", 0.28, 3, "Interoperabilitas Data", 0.25, 1.00, 7.00),
    IndicatorDef("10401", "Penerapan Kode Referensi dan/atau Data Induk", 1, "Prinsip Satu Data Indonesia", 0.28, 4, "Kode Referensi dan/atau Data Induk", 0.25, 1.00, 7.00),

    # DOMAIN 2: KUALITAS DATA (24%)
    IndicatorDef("20101", "Relevansi Data Terhadap Pengguna", 2, "Kualitas Data", 0.24, 5, "Relevansi", 0.21, 0.60, 3.02),
    IndicatorDef("20102", "Proses Identifikasi Kebutuhan Data", 2, "Kualitas Data", 0.24, 5, "Relevansi", 0.21, 0.40, 2.02),
    IndicatorDef("20201", "Penilaian Akurasi Data", 2, "Kualitas Data", 0.24, 6, "Akurasi", 0.16, 1.00, 3.84),
    IndicatorDef("20301", "Penjaminan Aktualitas Data", 2, "Kualitas Data", 0.24, 7, "Aktualitas & Ketepatan Waktu", 0.21, 0.50, 2.52),
    IndicatorDef("20302", "Pemantauan Ketepatan Waktu Diseminasi", 2, "Kualitas Data", 0.24, 7, "Aktualitas & Ketepatan Waktu", 0.21, 0.50, 2.52),
    IndicatorDef("20401", "Ketersediaan Data untuk Pengguna Data", 2, "Kualitas Data", 0.24, 8, "Aksesibilitas", 0.21, 0.34, 1.71),
    IndicatorDef("20402", "Akses Media Penyebarluasan Data", 2, "Kualitas Data", 0.24, 8, "Aksesibilitas", 0.21, 0.33, 1.66),
    IndicatorDef("20403", "Penyediaan Format Data", 2, "Kualitas Data", 0.24, 8, "Aksesibilitas", 0.21, 0.33, 1.66),
    IndicatorDef("20501", "Keterbandingan Data", 2, "Kualitas Data", 0.24, 9, "Keterbandingan & Konsistensi", 0.21, 0.50, 2.52),
    IndicatorDef("20502", "Konsistensi Statistik", 2, "Kualitas Data", 0.24, 9, "Keterbandingan & Konsistensi", 0.21, 0.50, 2.52),

    # DOMAIN 3: PROSES BISNIS STATISTIK (19%)
    IndicatorDef("30101", "Pendefinisian Kebutuhan Statistik", 3, "Proses Bisnis Statistik", 0.19, 10, "Perencanaan Data", 0.32, 0.33, 2.01),
    IndicatorDef("30102", "Desain Statistik", 3, "Proses Bisnis Statistik", 0.19, 10, "Perencanaan Data", 0.32, 0.33, 2.01),
    IndicatorDef("30103", "Penyiapan Instrumen", 3, "Proses Bisnis Statistik", 0.19, 10, "Perencanaan Data", 0.32, 0.34, 2.07),
    IndicatorDef("30201", "Proses Pengumpulan Data / Akuisisi Data", 3, "Proses Bisnis Statistik", 0.19, 11, "Pengumpulan Data", 0.26, 1.00, 4.94),
    IndicatorDef("30301", "Pengolahan Data", 3, "Proses Bisnis Statistik", 0.19, 12, "Pemeriksaan Data", 0.21, 0.50, 2.00),
    IndicatorDef("30302", "Analisis Data", 3, "Proses Bisnis Statistik", 0.19, 12, "Pemeriksaan Data", 0.21, 0.50, 2.00),
    IndicatorDef("30401", "Diseminasi Data", 3, "Proses Bisnis Statistik", 0.19, 13, "Penyebarluasan Data", 0.21, 1.00, 3.99),

    # DOMAIN 4: KELEMBAGAAN (17%)
    IndicatorDef("40101", "Penjaminan Transparansi Informasi Statistik", 4, "Kelembagaan", 0.17, 14, "Profesionalitas", 0.35, 0.25, 1.49),
    IndicatorDef("40102", "Penjaminan Netralitas dan Objektivitas", 4, "Kelembagaan", 0.17, 14, "Profesionalitas", 0.35, 0.25, 1.49),
    IndicatorDef("40103", "Penjaminan Kualitas Data", 4, "Kelembagaan", 0.17, 14, "Profesionalitas", 0.35, 0.25, 1.49),
    IndicatorDef("40104", "Penjaminan Konfidensialitas Data", 4, "Kelembagaan", 0.17, 14, "Profesionalitas", 0.35, 0.25, 1.49),
    IndicatorDef("40201", "Pemenuhan Kompetensi SDM Bidang Statistik", 4, "Kelembagaan", 0.17, 15, "SDM Memadai dan Kapabel", 0.30, 0.50, 2.55),
    IndicatorDef("40202", "Pemenuhan Kompetensi SDM Bidang Manajemen Data", 4, "Kelembagaan", 0.17, 15, "SDM Memadai dan Kapabel", 0.30, 0.50, 2.55),
    IndicatorDef("40301", "Kolaborasi Penyelenggaraan Kegiatan Statistik", 4, "Kelembagaan", 0.17, 16, "Pengorganisasian Statistik", 0.35, 0.25, 1.49),
    IndicatorDef("40302", "Penyelenggaraan Forum Satu Data Indonesia", 4, "Kelembagaan", 0.17, 16, "Pengorganisasian Statistik", 0.35, 0.25, 1.49),
    IndicatorDef("40303", "Kolaborasi dengan Pembina Data Statistik", 4, "Kelembagaan", 0.17, 16, "Pengorganisasian Statistik", 0.35, 0.25, 1.49),
    IndicatorDef("40304", "Pelaksanaan Tugas Sebagai Walidata", 4, "Kelembagaan", 0.17, 16, "Pengorganisasian Statistik", 0.35, 0.25, 1.49),

    # DOMAIN 5: STATISTIK NASIONAL (12%)
    IndicatorDef("50101", "Penggunaan Data Statistik Dasar Kebijakan", 5, "Statistik Nasional", 0.12, 17, "Pemanfaatan Data Statistik", 0.34, 0.34, 1.39),
    IndicatorDef("50102", "Penggunaan Data Statistik Sektoral Kebijakan", 5, "Statistik Nasional", 0.12, 17, "Pemanfaatan Data Statistik", 0.34, 0.33, 1.35),
    IndicatorDef("50103", "Sosialisasi dan Literasi Hasil Statistik", 5, "Statistik Nasional", 0.12, 17, "Pemanfaatan Data Statistik", 0.34, 0.33, 1.35),
    IndicatorDef("50201", "Pelaksanaan Rekomendasi Kegiatan Statistik (Romantik)", 5, "Statistik Nasional", 0.12, 18, "Pengelolaan Kegiatan Statistik", 0.33, 1.00, 3.96),
    IndicatorDef("50301", "Perencanaan Pembangunan Statistik", 5, "Statistik Nasional", 0.12, 19, "Penguatan SSN Berkelanjutan", 0.33, 0.33, 1.31),
    IndicatorDef("50302", "Penyebarluasan Data", 5, "Statistik Nasional", 0.12, 19, "Penguatan SSN Berkelanjutan", 0.33, 0.33, 1.31),
    IndicatorDef("50303", "Pemanfaatan Big Data", 5, "Statistik Nasional", 0.12, 19, "Penguatan SSN Berkelanjutan", 0.33, 0.34, 1.35),
]

INDICATOR_DICT: Dict[str, IndicatorDef] = {ind.code: ind for ind in EPSS_INDICATORS}

# 11 Indikator Target Perbaikan Pemkab Mempawah Pasca-Pleno
MEMPAWAH_11_PERBAIKAN: List[str] = [
    "20201", "20301", "20302", "20501", "20502",
    "30302", "40102", "40103", "40302", "50103", "50301"
]

# Baseline Nilai Pleno Provinsi 2026 Pemkab Mempawah
MEMPAWAH_BASELINE_SCORES: Dict[str, int] = {
    "10101": 4, "10201": 3, "10301": 3, "10401": 3,
    "20101": 3, "20102": 3, "20201": 1, "20301": 1, "20302": 1,
    "20401": 3, "20402": 3, "20403": 3, "20501": 1, "20502": 1,
    "30101": 3, "30102": 3, "30103": 3, "30201": 3, "30301": 3,
    "30302": 1, "30401": 3,
    "40101": 3, "40102": 1, "40103": 1, "40104": 3, "40201": 2,
    "40202": 2, "40301": 3, "40302": 2, "40303": 3, "40304": 2,
    "50101": 3, "50102": 3, "50103": 1, "50201": 3, "50301": 1,
    "50302": 3, "50303": 3
}

def get_predikat(ips: float) -> str:
    """Mengembalikan predikat Indeks Pembangunan Statistik berdasarkan Perka BPS."""
    if ips >= 4.2:
        return "Memuaskan"
    elif ips >= 3.5:
        return "Sangat Baik"
    elif ips >= 2.6:
        return "Baik"
    elif ips >= 1.8:
        return "Cukup"
    else:
        return "Kurang"

def calculate_ips(scores: Dict[str, int], use_official_rounding: bool = True) -> Tuple[float, Dict[int, float], Dict[int, float]]:
    """Menghitung nilai komposit IPS, nilai per domain, dan nilai per aspek.
    
    Args:
        scores: Dict kode indikator -> nilai kematangan (1-5)
        use_official_rounding: Gunakan bobot resmi pembulatan (e.g. 7.00%) atau exact decimal.
        
    Returns:
        (total_ips, domain_scores, aspect_scores)
    """
    total_ips = 0.0
    domain_weighted_sum = {d: 0.0 for d in range(1, 6)}
    domain_weight_tot = {d: 0.0 for d in range(1, 6)}
    
    aspect_weighted_sum: Dict[int, float] = {}
    aspect_weight_tot: Dict[int, float] = {}

    for ind in EPSS_INDICATORS:
        score = scores.get(ind.code, 1)
        w = (ind.official_relative_pct / 100.0) if use_official_rounding else ind.exact_relative_weight
        
        total_ips += score * w
        
        # Domain accumulation
        domain_weighted_sum[ind.domain_id] += score * w
        domain_weight_tot[ind.domain_id] += w
        
        # Aspect accumulation
        if ind.aspect_id not in aspect_weighted_sum:
            aspect_weighted_sum[ind.aspect_id] = 0.0
            aspect_weight_tot[ind.aspect_id] = 0.0
        aspect_weighted_sum[ind.aspect_id] += score * w
        aspect_weight_tot[ind.aspect_id] += w

    domain_scores = {
        d: (domain_weighted_sum[d] / domain_weight_tot[d]) if domain_weight_tot[d] > 0 else 0.0
        for d in domain_weighted_sum
    }
    
    aspect_scores = {
        a: (aspect_weighted_sum[a] / aspect_weight_tot[a]) if aspect_weight_tot[a] > 0 else 0.0
        for a in aspect_weighted_sum
    }

    return total_ips, domain_scores, aspect_scores
