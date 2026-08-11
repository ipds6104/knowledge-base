"""Markdown Renderer for Metadata Generator.

Pure DTO-to-Markdown renderer with dynamic section indexing based on active variable tables.
"""

from ..schemas import DesaMetadataDTO


def render_metadata_markdown(dto: DesaMetadataDTO) -> str:
    """Renders DesaMetadataDTO into a clean GFM Markdown document."""
    lines = []
    lines.append("# METADATA STATISTIK SEKTORAL")
    lines.append("## Satu Data Indonesia (SDI) - Desa Cantik 2026")
    lines.append(f"**{dto.admin_type} {dto.desa_title}, Kabupaten Mempawah**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📅 I. METADATA KEGIATAN (MS-KEGIATAN)")
    lines.append("")
    lines.append("| No | Elemen Metadata | Keterangan / Nilai |")
    lines.append("| :--- | :--- | :--- |")

    for k in dto.kegiatan:
        lines.append(f"| **{k.no}** | **{k.elemen}** | {k.keterangan} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 II. METADATA VARIABEL (MS-VARIABEL)")
    lines.append("")

    sec_char = ord('A')

    if dto.variabel.rt_variables:
        letter = chr(sec_char)
        lines.append(f"### {letter}. Tabel Variabel Tingkat Rukun Tetangga (Daftar_RT)")
        lines.append("")
        lines.append("| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Klasifikasi / Rentang Nilai |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for v in dto.variabel.rt_variables:
            lines.append(f"| {v.no} | `{v.nama_variabel}` | {v.konsep} | {v.definisi} | {v.satuan} | {v.tipe_data} | {v.pilihan_isian} |")
        lines.append("")
        sec_char += 1

    if dto.variabel.fasilitas_variables:
        letter = chr(sec_char)
        lines.append(f"### {letter}. Tabel Variabel Tingkat Sarana Prasarana (Fasilitas)")
        lines.append("")
        lines.append("| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Pilihan Isian / Keterangan |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for v in dto.variabel.fasilitas_variables:
            lines.append(f"| {v.no} | `{v.nama_variabel}` | {v.konsep} | {v.definisi} | {v.satuan} | {v.tipe_data} | {v.pilihan_isian} |")
        lines.append("")
        sec_char += 1

    if dto.variabel.capi_micro_variables:
        letter = chr(sec_char)
        lines.append(f"### {letter}. Tabel Variabel Data Mikro Bangunan Tempat Tinggal Biasa & Rumah Tangga CAPI")
        lines.append("")
        lines.append("| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Pilihan Isian / Keterangan |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for v in dto.variabel.capi_micro_variables:
            lines.append(f"| {v.no} | `{v.nama_variabel}` | {v.konsep} | {v.definisi} | {v.satuan} | {v.tipe_data} | {v.pilihan_isian} |")
        lines.append("")
        sec_char += 1

    lines.append("---")
    lines.append("")
    lines.append("## 📈 III. METADATA INDIKATOR (MS-INDIKATOR)")
    lines.append("")
    lines.append("| No | Nama Indikator | Definisi | Rumus / Formula Kalkulasi | Satuan | Ukuran / Klasifikasi |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for i in dto.indikator:
        rumus_fmt = f"$${i.rumus}$$" if i.rumus else "-"
        lines.append(f"| **{i.no}** | **{i.nama_indikator}** | {i.definisi} | {rumus_fmt} | {i.satuan} | {i.klasifikasi} |")

    lines.append("")
    return "\n".join(lines)
