"""Data Transfer Objects (DTOs) for DDA Publication Generator.
Decouples data gathering, calculation, frontmatter metadata, and chapter infographics/narratives.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CompilerTeamDTO:
    """DTO Tim Penyusun / Compilers Card (Halaman ii)."""

    person_in_charge_id: str = "Penanggung Jawab"
    person_in_charge_en: str = "Persons in Charge"
    person_in_charge_name: str = ""

    editors_id: str = "Penyunting"
    editors_en: str = "Editors"
    editors_name: str = "Tim Pembina Desa Cantik BPS Kabupaten Mempawah"

    writers_id: str = "Penulis Naskah"
    writers_en: str = "Data Writers"
    writers_name: str = ""

    processors_id: str = "Pengolah Data"
    processors_en: str = "Data Processors"
    processors_name: str = ""

    layouters_id: str = "Penata Letak"
    layouters_en: str = "Layouters"
    layouters_name: str = ""


@dataclass
class ContributorItemDTO:
    """DTO Item Kontributor Data (Halaman iii)."""

    name_id: str
    name_en: str


@dataclass
class AbbreviationItemDTO:
    """DTO Item Singkatan / Acronym (Halaman ix)."""

    acronym: str
    desc_id: str
    desc_en: str


@dataclass
class PublicationFrontmatterDTO:
    """DTO Frontmatter Metadata (Tim Penyusun, Kontributor Data, Daftar Singkatan)."""

    compilers: CompilerTeamDTO
    contributors: List[ContributorItemDTO] = field(default_factory=list)
    abbreviations: List[AbbreviationItemDTO] = field(default_factory=list)


@dataclass
class ChapterInfographicDTO:
    """DTO Visualisasi Infografis Pembatas Bab 1-5 (Dihitung Dinamis)."""

    # Bab 1
    dusun_breakdown: List[Dict[str, Any]] = field(default_factory=list)

    # Bab 2
    male_pct: float = 50.0
    female_pct: float = 50.0
    dash_gender: str = "50 50"

    # Bab 3
    ktp_pct: float = 0.0
    dash_ktp: str = "0 100"

    # Bab 4
    pkh_pct: float = 0.0
    bpnt_pct: float = 0.0
    bst_blt_pct: float = 0.0

    # Bab 5
    layak_pct: float = 92.33
    dash_layak: str = "92.33 7.67"


@dataclass
class TechnicalNoteItemDTO:
    """DTO Poin Penjelasan Teknis per Bab."""

    term_id: str
    term_en: str


@dataclass
class ChapterContentDTO:
    """DTO Konten Narasi Ulasan & Penjelasan Teknis per Bab."""

    narrative_id: str
    narrative_en: str
    tech_notes: List[TechnicalNoteItemDTO] = field(default_factory=list)


@dataclass
class VillageConfigDTO:
    """DTO Konfigurasi Domain dan Identitas Wilayah Desa/Kecamatan."""

    name_kebab: str
    name_title: str
    name_upper: str
    kecamatan: str
    kabupaten: str
    provinsi: str
    pub_no: str
    year: int
    kades_title: str
    kades_title_en: str
    kades_name: str
    north: str
    south: str
    east: str
    west: str
    sheet_id: str


@dataclass
class StatisticalMetricsDTO:
    """DTO Hasil Kalkulasi Indikator Statistik Baku Publikasi."""

    tot_pop: int
    tot_l: int
    tot_p: int
    tot_sr: float
    tot_bumbung: int
    tot_kk: int
    tot_art: float
    tot_kepadatan: float
    tot_lansia: int
    tot_b1: int
    tot_b2: int
    tot_pendatang: int
    tot_lahir: int
    tot_mati: int
    tot_tk: int
    tot_sd: int
    tot_smp: int
    tot_sma: int
    tot_sarjana: int
    tot_putus: int
    tot_ktp: int
    tot_ktp_pct: float
    tot_pkh: int
    tot_bpnt: int
    tot_bst: int
    tot_blt: int
    tot_bansos: int
    tot_layak: int
    tot_layak_pct: float
    rows: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class FacilityMetricsDTO:
    """DTO Rekapitulasi Fasilitas Umum & Infrastruktur Desa per RT."""

    rows: List[Dict[str, Any]] = field(default_factory=list)
    tot_masjid: int = 0
    tot_musholla: int = 0
    tot_vihara: int = 0
    tot_gereja: int = 0
    tot_ibadah: int = 0

    tot_paud_tk: int = 0
    tot_sd_mi: int = 0
    tot_smp_mts: int = 0
    tot_sma_ma: int = 0
    tot_ponpes: int = 0
    tot_pendidikan: int = 0

    tot_posyandu: int = 0
    tot_polindes: int = 0
    tot_kesehatan: int = 0

    tot_kantor: int = 0
    tot_ekonomi: int = 0
    tot_tpu: int = 0
    tot_bts: int = 0
    tot_fasum_lain: int = 0

    tot_kondisi_baik: int = 0
    tot_kondisi_rusak: int = 0

    tot_jalan_aspal: int = 0
    tot_jalan_batu: int = 0
    tot_jalan_tanah: int = 0

    tot_listrik_pln: int = 0
    tot_air_pdam: int = 0
    tot_sinyal_4g: int = 0



@dataclass
class DatasetCapabilitiesDTO:
    """Capabilities matrix DTO indicating available data dimensions in a village dataset."""

    has_employment: bool = False
    has_msme: bool = False
    has_health_insurance: bool = False
    has_building_materials: bool = False
    has_decent_housing: bool = False
    has_ktp_el: bool = False
    has_education: bool = False
    has_public_facilities: bool = False
    admin_type: str = "Desa"
    admin_title: str = "Desa"


@dataclass
class DesaPublicationData:
    """Universal Data Contract DTO Utama untuk Rendering Publikasi DDA."""

    config: Dict[str, Any]
    metrics: Dict[str, Any]
    capabilities: DatasetCapabilitiesDTO = field(default_factory=DatasetCapabilitiesDTO)
    frontmatter: Optional[PublicationFrontmatterDTO] = None
    infographics: Optional[ChapterInfographicDTO] = None
    chapters: Dict[int, ChapterContentDTO] = field(default_factory=dict)
    raw_rt_data: List[Dict[str, Any]] = field(default_factory=list)
    raw_fas_data: List[Dict[str, Any]] = field(default_factory=list)
