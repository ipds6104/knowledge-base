"""Dataclass Schemas for BPS Potensi Desa (PODES) Publication Engine."""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class PodesMetricsDTO:
    """Metrik Terstruktur Hasil Ekstraksi Data PODES 2025."""
    status_daerah: str = "Perdesaan"
    alamat_lengkap: str = "-"
    kawasan_hutan: str = "Di luar kawasan hutan"
    jumlah_rw: int = 0
    jumlah_rt: int = 0
    penduduk_l: int = 0
    penduduk_p: int = 0
    total_penduduk: int = 0
    sex_ratio: float = 0.0
    jumlah_kk: int = 0
    kk_pertanian: int = 0
    listrik_pln: int = 0
    listrik_non_pln: int = 0
    bukan_listrik: int = 0
    penerangan_jalan: str = "-"
    bakar_masak: str = "-"
    air_minum: str = "-"
    bencana_alam: str = "-"
    mitigasi_bencana: str = "-"
    sarana_pendidikan: str = "-"
    sarana_kesehatan: str = "-"
    posyandu_aktif: int = 0
    posbindu: int = 0
    prasarana_transportasi: str = "-"
    jenis_jalan: str = "-"
    jalan_roda4: str = "-"
    angkutan_umum: str = "-"
    jumlah_bts: int = 0
    operator_seluler: str = "-"
    sinyal_hp: str = "-"
    sinyal_internet: str = "-"
    sarana_ekonomi: str = "-"
    sumber_penghasilan_utama: str = "-"
    subsektor_utama: str = "-"
    jumlah_imk: int = 0
    sistem_informasi_desa: str = "-"
    jumlah_sppg: str = "-"
    aparatur_pemdes: int = 0
    keberadaan_bpd: str = "-"
    musyawarah_desa: int = 0

    # Calculated percentages & helpers
    male_pct: float = 0.0
    female_pct: float = 0.0
    kk_pertanian_pct: float = 0.0


@dataclass
class PodesPublicationData:
    """DTO Utama Penampung Seluruh Data Publikasi PODES."""
    config: Dict[str, Any]
    metrics: PodesMetricsDTO
    raw_data: List[Dict[str, str]] = field(default_factory=list)
