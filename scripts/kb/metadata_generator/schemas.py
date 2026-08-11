"""Data Transfer Objects (DTOs) for Metadata Generator Engine.

Provides isolated Single Source of Truth contracts between data calculation/builder
and output renderers (Markdown, Typst PDF).
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KegiatanItemDTO:
    no: int
    elemen: str
    keterangan: str


@dataclass
class VariabelItemDTO:
    no: int
    nama_variabel: str
    konsep: str
    definisi: str
    satuan: str
    tipe_data: str
    pilihan_isian: str


@dataclass
class IndikatorItemDTO:
    no: int
    nama_indikator: str
    definisi: str
    rumus: str
    satuan: str
    klasifikasi: str


@dataclass
class VariabelMetadataDTO:
    rt_variables: List[VariabelItemDTO] = field(default_factory=list)
    fasilitas_variables: List[VariabelItemDTO] = field(default_factory=list)
    capi_micro_variables: List[VariabelItemDTO] = field(default_factory=list)


@dataclass
class DesaMetadataDTO:
    desa_title: str
    desa_kebab: str
    admin_type: str = "Desa"
    kegiatan: List[KegiatanItemDTO] = field(default_factory=list)
    variabel: VariabelMetadataDTO = field(default_factory=VariabelMetadataDTO)
    indikator: List[IndikatorItemDTO] = field(default_factory=list)
