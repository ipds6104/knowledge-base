"""BPS HTML Layout Renderer Module for PODES Generator Engine.
Strictly adheres to BPS Dissemination Guidelines and Page Card Layout Engine.
"""

from pathlib import Path
from typing import Any
from ..schemas import PodesPublicationData


def fmt_val(v: Any) -> str:
    """Format angka untuk tampilan HTML BPS."""
    if v is None or str(v).strip() in ("", "-", "0", "0.00", "0,00", "NA"):
        return "-"
    s = str(v).strip()
    if "." in s:
        s = s.replace(".", ",")
    if s.isdigit() and int(s) >= 1000:
        s = f"{int(s):,}".replace(",", ".")
    return s


def render_podes_html(pub_data: PodesPublicationData) -> Path:
    """Menyusun halaman HTML bilingual A4 berstandar BPS dari PodesPublicationData DTO."""
    config = pub_data.config
    m = pub_data.metrics

    name_title = config["name_title"]
    name_upper = name_title.upper()
    name_kebab = config["name_kebab"]
    admin_type = config.get("admin_type", "Desa")
    admin_type_en = config.get("admin_type_en", "Village")
    admin_upper = admin_type.upper()
    gov_name = config.get("gov_name", f"Pemerintah {admin_type} {name_title}")
    gov_name_en = config.get("gov_name_en", f"Government of {name_title} {admin_type_en}")

    kecamatan = config.get("kecamatan", "Mempawah")
    kabupaten = config.get("kabupaten", "Mempawah")
    year = config.get("year", 2026)
    data_year = config.get("data_year", 2025)
    pub_no = config.get("pub_no", "61040.2026.101")
    kades_title = config.get("kades_title", f"Kepala Desa {name_title}")
    kades_title_en = config.get("kades_title_en", f"Head of {name_title} Village")
    kades_name = config.get("kades_name", f"Pemerintah {admin_type} {name_title}")

    book_header_id = f"POTENSI {admin_upper} {name_upper} {year}"
    book_header_en = f"POTENTIALS OF {name_upper} {admin_type_en.upper()} {year}"

    tot_pop_str = fmt_val(m.total_penduduk)
    l_str = fmt_val(m.penduduk_l)
    p_str = fmt_val(m.penduduk_p)
    sr_str = f"{m.sex_ratio:.2f}".replace(".", ",")
    kk_str = fmt_val(m.jumlah_kk)
    kk_pert_str = fmt_val(m.kk_pertanian)

    def make_page_card(
        sec_title_id: str,
        sec_title_en: str,
        page_no_str: str,
        content_html: str,
        page_num: int,
        show_header: bool = True,
        show_footer: bool = True,
    ) -> str:
        is_even = page_num % 2 == 0
        hdr_cls = "even" if is_even else "odd"
        ftr_cls = "even" if is_even else "odd"

        hdr_html = ""
        if show_header:
            if is_even:
                hdr_html = f"""<div class="running-header {hdr_cls}">{book_header_id}<span class="en">{book_header_en}</span></div>"""
            else:
                hdr_html = f"""<div class="running-header {hdr_cls}">{sec_title_id}<span class="en">{sec_title_en}</span></div>"""

        ftr_html = ""
        if show_footer:
            ftr_html = f"""<div class="running-footer {ftr_cls}">{page_no_str}</div>"""

        return f"""  <div class="page-card">
    {hdr_html}
    <div class="page-content">
{content_html}
    </div>
    {ftr_html}
  </div>"""

    def make_cover_card(
        ch_num: str, ch_title_id: str, ch_title_en: str, info_html: str
    ) -> str:
        return f"""      <div style="background: linear-gradient(135deg, #0b3c5d 0%, #1e3a8a 50%, #eb8a3c 100%); border-radius: 14px; padding: 22px 25px; display: flex; align-items: center; gap: 22px; box-shadow: 0 8px 20px -4px rgba(11, 60, 93, 0.25); margin-top: 5px; margin-bottom: 22px; width: 100%;">
        <div style="width: 78px; height: 78px; background: #0b3c5d; border: 2.5px solid #eb8a3c; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #ffffff; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
          <span style="font-size: 30pt; font-weight: 900; line-height: 0.9; margin-top: -2px;">{ch_num}</span>
          <span style="font-size: 8.5pt; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 1px; color: #eb8a3c;">BAB</span>
          <span style="font-size: 7pt; font-style: italic; font-weight: 600; margin-top: -2px; color: #fef08a;">Chapter</span>
        </div>
        <div style="flex: 1;">
          <h2 style="font-size: 15pt; font-weight: 900; color: #ffffff; margin: 0 0 6px 0; line-height: 1.2; text-transform: uppercase; letter-spacing: 0.5px;">{ch_title_id}</h2>
          <div style="width: 100%; height: 2px; background: #eb8a3c; opacity: 0.9; margin-bottom: 6px;"></div>
          <h3 style="font-size: 11pt; font-weight: 800; font-style: italic; color: #fef08a; margin: 0; line-height: 1.2; text-transform: uppercase; letter-spacing: 0.5px;">{ch_title_en}</h3>
        </div>
      </div>
      <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); width: 100%;">
        <div style="font-size: 9pt; font-weight: 800; color: #0b3c5d; text-transform: uppercase; margin-bottom: 12px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 4px;">RINGKASAN INDIKATOR BAB {ch_num} / <i>CHAPTER {ch_num} HIGHLIGHTS</i></div>
        {info_html}
      </div>"""

    def make_blank_page() -> str:
        return """  <div class="page-card" style="justify-content: center; align-items: center;"><div style="color: #cbd5e1; font-style: italic; font-size: 9pt;">[ Halaman Ini Sengaja Dikosongkan / This Page Intentionally Left Blank ]</div></div>"""

    meta_std = f"""<div class="table-meta"><div class="meta-row"><div class="meta-lbl">Catatan/<i>Note:</i></div><div>Data hasil Pendataan Potensi Desa (PODES) Tahun {data_year} / <i>Village Potential Survey Data {data_year}</i></div></div><div class="meta-row"><div class="meta-lbl">Sumber/<i>Source:</i></div><div>{gov_name} & BPS Kabupaten Mempawah — PODES {data_year} / <i>{gov_name_en} & BPS-Statistics Mempawah Regency — PODES {data_year}</i></div></div></div>"""

    html_header = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Potensi {admin_type} {name_title} {year} / Potentials of {name_title} {admin_type_en} {year}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    @page {{ size: A4; margin: 0; }}

    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}

    body {{
      font-family: 'Inter', Arial, sans-serif;
      color: #2d3748;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
      font-size: 9pt;
      line-height: 1.4;
    }}

    p {{
      text-align: justify;
      text-justify: inter-word;
      line-height: 1.5;
      margin-top: 0;
    }}

    .page-container {{ max-width: 210mm; margin: 0 auto; background: #ffffff; }}

    .page-card {{
      width: 210mm;
      height: 297mm;
      padding: 15mm 20mm 15mm 20mm;
      page-break-after: always;
      page-break-inside: avoid;
      position: relative;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
      overflow: hidden;
    }}

    .page-content {{ flex: 1; padding-bottom: 30px; position: relative; }}

    .running-header {{
      font-size: 8.5pt;
      font-weight: 700;
      color: #eb8a3c;
      text-transform: uppercase;
      margin-bottom: 12px;
      line-height: 1.25;
    }}

    .running-header.even {{ text-align: left; }}
    .running-header.odd {{ text-align: right; }}

    .running-header .en {{
      display: block;
      font-style: italic;
      font-weight: 600;
      color: #eb8a3c;
      margin-top: 1px;
    }}

    .running-footer {{
      position: absolute;
      bottom: 5mm;
      left: 14mm;
      right: 14mm;
      font-size: 10.5pt;
      font-weight: 800;
      color: #eb8a3c;
    }}

    .running-footer.even {{ text-align: left; }}
    .running-footer.odd {{ text-align: right; }}

    .cover-box {{
      background: linear-gradient(135deg, #0b3c5d 0%, #1e3a8a 50%, #eb8a3c 100%);
      color: #ffffff;
      padding: 45px 25px;
      border-radius: 12px;
      text-align: center;
      margin-top: 15px;
      margin-bottom: 20px;
      position: relative;
      overflow: hidden;
    }}

    .cover-title {{ font-size: 24pt; font-weight: 800; margin: 0 0 8px 0; line-height: 1.25; }}
    .cover-subtitle {{ font-size: 13pt; color: #fef08a; font-weight: 500; margin-bottom: 22px; font-style: italic; }}

    .narrative-box {{ background: transparent; border: none; padding: 0; margin-bottom: 12px; }}
    .narrative-box p {{ text-align: justify; text-justify: inter-word; margin-bottom: 8px; line-height: 1.45; }}
    .narrative-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .narrative-col-id {{ padding-right: 10px; }}
    .narrative-col-en {{ padding-left: 15px; font-style: italic; color: #475569; }}
    .narrative-title {{ font-weight: 800; color: #0b3c5d; font-size: 8.8pt; margin-bottom: 4px; text-transform: uppercase; }}
    .narrative-title.en {{ font-style: italic; }}

    .section-header {{ font-size: 11pt; font-weight: 800; color: #0b3c5d; margin-bottom: 8px; padding-bottom: 2px; text-transform: uppercase; }}
    .section-header .en {{ display: block; font-size: 10pt; font-weight: 800; font-style: italic; color: #0b3c5d; text-transform: uppercase; margin-top: 1px; }}

    .table-title-block {{ display: flex; gap: 12px; align-items: flex-start; margin-bottom: 6px; }}
    .table-label {{ font-weight: 800; font-size: 9.5pt; color: #1a202c; white-space: nowrap; }}
    .table-label .id-lbl {{ text-decoration: underline; }}
    .table-label i {{ font-style: italic; font-weight: 700; text-decoration: none !important; }}
    .table-num {{ font-weight: 800; font-size: 9.5pt; color: #1a202c; }}
    .table-title-text {{ font-weight: 800; font-size: 9.5pt; color: #1a202c; line-height: 1.25; }}
    .table-title-text .en {{ display: block; font-weight: 700; font-style: italic; color: #475569; margin-top: 1px; }}

    table.bps-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
      font-size: 8.8pt;
    }}

    table.bps-table th, table.bps-table td {{
      border: 1px solid #718096;
      padding: 5px 8px;
    }}

    table.bps-table th {{
      background-color: #0b3c5d;
      color: #ffffff;
      font-weight: 700;
      text-align: center;
      vertical-align: middle;
      font-size: 8.5pt;
    }}

    table.bps-table th.main-header i {{ font-style: italic; font-weight: 600; font-size: 8pt; }}
    table.bps-table th.sub-header {{ background-color: #1d5c88; font-size: 8pt; }}
    table.bps-table th.col-num {{ background-color: #2c6e9b; font-size: 7.5pt; font-weight: 400; padding: 2px; }}

    table.bps-table td {{ vertical-align: middle; color: #1a202c; }}
    table.bps-table tr:nth-child(even) {{ background-color: #f8fafc; }}

    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}

    .table-meta {{ font-size: 7.5pt; color: #4a5568; margin-top: 6px; line-height: 1.35; }}
    .table-meta .meta-row {{ display: flex; margin-bottom: 2px; }}
    .table-meta .meta-lbl {{ font-weight: 700; width: 85px; flex-shrink: 0; color: #2d3748; }}

    .tech-notes-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 14px;
      margin-bottom: 15px;
    }}

    .tech-notes-title {{ font-size: 10pt; font-weight: 800; color: #0b3c5d; margin-bottom: 8px; text-transform: uppercase; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 4px; }}
    .tech-notes-list {{ list-style-type: decimal; padding-left: 18px; margin: 0; font-size: 8.2pt; line-height: 1.45; }}
    .tech-notes-list li {{ margin-bottom: 6px; text-align: justify; color: #334155; }}
    .tech-notes-list li .en {{ display: block; font-style: italic; color: #64748b; margin-top: 1px; }}
  </style>
</head>
<body>
<div class="page-container">
"""

    # Page 1 (Cover - ODD)
    card_1_cover = f"""  <div class="page-card" style="padding: 0; background: linear-gradient(135deg, #0b3c5d 0%, #1d5c88 100%); color: #ffffff; justify-content: space-between;">
    <div style="padding: 25mm 20mm 10mm; text-align: left;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px;">
        <div style="font-size: 11pt; font-weight: 800; letter-spacing: 1px; color: #f8fafc; text-transform: uppercase;">{gov_name.upper()}<br><span style="font-size: 8.5pt; font-weight: 600; color: #cbd5e1; letter-spacing: 0.5px;">KABUPATEN MEMPAWAH</span></div>
      </div>
      <div style="display: inline-block; background: #eb8a3c; color: #ffffff; font-size: 9pt; font-weight: 800; padding: 4px 14px; border-radius: 4px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">PUBLIKASI POTENSI DESA / PODES {data_year}</div>
      <div style="font-size: 26pt; font-weight: 900; line-height: 1.25; margin-bottom: 12px; text-transform: uppercase; color: #ffffff;">POTENSI {admin_upper}<br>{name_upper} {year}</div>
      <div style="font-size: 14pt; font-weight: 500; color: #cbd5e1; font-style: italic; margin-bottom: 20px;">Potentials of {name_title} {admin_type_en} {year}</div>
      <div style="border-top: 2px solid rgba(255,255,255,0.2); padding-top: 15px; font-size: 10pt; color: #e2e8f0;">
        <strong>Kecamatan {kecamatan} — Kabupaten {kabupaten}</strong><br>
        Disusun oleh {gov_name} & Disunting oleh BPS Kabupaten Mempawah
      </div>
    </div>
    <div style="padding: 20mm; background: #072a42; border-top: 4px solid #eb8a3c; text-align: left;">
      <div style="font-size: 12pt; font-weight: 800; color: #ffffff; text-transform: uppercase;">{gov_name.upper()}</div>
      <div style="font-size: 9.5pt; color: #eb8a3c; margin-top: 2px; font-weight: 700;">Disunting oleh BPS Kabupaten Mempawah</div>
    </div>
  </div>"""

    # Page 2 (ii - EVEN)
    card_2_catalog = make_page_card(
        "KATALOG DALAM TERBITAN",
        "KATALOG DALAM TERBITAN",
        "ii",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13pt; font-weight: 800; color: #0b3c5d; margin: 0; text-transform: uppercase;">POTENSI {admin_upper} {name_upper} {year}</h2>
        <div style="font-size: 10.5pt; font-weight: 700; font-style: italic; color: #475569; margin-top: 4px;">Potentials of {name_title} {admin_type_en} {year}</div>
      </div>
      <div style="font-size: 9pt; line-height: 1.6; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <table style="width: 100%; border: none; font-size: 8.8pt; margin-bottom: 20px;">
          <tr><td style="width: 170px; font-weight: 700;">Ukuran Buku / <i>Book Size</i></td><td>: 21 cm x 29,7 cm (A4)</td></tr>
          <tr><td style="font-weight: 700;">Jumlah Halaman / <i>Pages</i></td><td>: ix + 15 halaman</td></tr>
          <tr><td style="font-weight: 700;">Penyusun Naskah / <i>Manuscript</i></td><td>: {gov_name} (menggunakan data PODES BPS)</td></tr>
          <tr><td style="font-weight: 700;">Penyunting / <i>Editor</i></td><td>: Badan Pusat Statistik Kabupaten Mempawah</td></tr>
          <tr><td style="font-weight: 700;">Penerbit / <i>Publisher</i></td><td>: © {gov_name} & BPS Kabupaten Mempawah</td></tr>
          <tr><td style="font-weight: 700;">Sumber Data / <i>Source</i></td><td>: Hasil Pendataan Potensi Desa (PODES) Tahun {data_year}</td></tr>
        </table>
        
        <div style="border: 1.5px solid #0b3c5d; padding: 12px; border-radius: 6px; background: #f8fafc; margin-top: 30px;">
          <strong style="color: #0b3c5d; text-transform: uppercase;">KLAUSUL HAK CIPTA / COPYRIGHT NOTICE</strong><br>
          <p style="font-size: 8.2pt; color: #334155; margin-top: 6px; text-align: justify;">
            Dilarang mengumumkan, mendistribusikan, mengomunikasikan, dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari {gov_name} dan Badan Pusat Statistik Kabupaten Mempawah.<br>
            <i>It is prohibited to publish, distribute, communicate, and/or duplicate part or all of this book for commercial purposes without written permission from {gov_name_en} and BPS-Statistics Mempawah Regency.</i>
          </p>
        </div>
      </div>""",
        2,
        show_header=False,
        show_footer=True,
    )

    # Page 3 (iii - ODD)
    card_3_contrib = make_page_card(
        "KONTRIBUTOR DATA",
        "DATA CONTRIBUTORS",
        "iii",
        f"""      <h2 style="text-align: center; color: #0b3c5d; padding-bottom: 6px; font-size: 13pt; margin-bottom: 20px;">KONTRIBUTOR DATA / <i>DATA CONTRIBUTORS</i></h2>
      <ol style="font-size: 9.5pt; line-height: 1.8; color: #2d3748; padding-left: 20px; max-width: 90%; margin: 0 auto;">
        <li>{gov_name} / <i>{gov_name_en}</i> (Penyusun Utama / <i>Main Drafter</i>)</li>
        <li>Tim Pendataan Potensi Desa (PODES {data_year}) BPS Kabupaten Mempawah / <i>PODES {data_year} Team of BPS-Statistics Mempawah Regency</i> (Penyunting Data / <i>Data Editor</i>)</li>
      </ol>""",
        3,
        show_header=False,
        show_footer=True,
    )

    # Page 4 (iv - EVEN)
    card_4_preface_id = make_page_card(
        "KATA PENGANTAR",
        "PREFACE",
        "iv",
        f"""      <h2 style="text-align: center; color: #0b3c5d; font-size: 14pt; font-weight: 800; margin-top: 10px; margin-bottom: 25px;">KATA PENGANTAR</h2>
      <div style="font-size: 9.5pt; line-height: 1.6; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi resmi <strong>"Potensi {admin_type} {name_title} {year}"</strong> dapat diselesaikan dengan baik. Publikasi ini disusun oleh <strong>{gov_name}</strong> menggunakan data hasil Pendataan Potensi Desa (PODES) Tahun {data_year} dari Badan Pusat Statistik (BPS) dan disunting oleh Badan Pusat Statistik Kabupaten Mempawah.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">Data yang disajikan menggambarkan kondisi potensi kewilayahan, kependudukan, perumahan, energi, fasilitas sosial, prasarana komunikasi, hingga kelembagaan dan ekonomi masyarakat di {admin_type} {name_title}. Publikasi ini diharapkan dapat menjadi rujukan baku dalam perencanaan pembangunan kewilayahan berbasis bukti (<i>evidence-based policy</i>) demi meningkatkan kesejahteraan masyarakat.</p>
      </div>
      <div style="margin-top: 35px; font-size: 9.5pt; text-align: right; padding-right: 20px;">
        <div style="margin-bottom: 15px; font-weight: 500; color: #2d3748;">{name_title}, Agustus {year}</div>
        <div style="display: inline-block; text-align: center;">
          <div style="font-weight: 700; color: #0b3c5d;">{kades_title.upper()}</div>
          <div style="font-weight: 800; color: #0b3c5d; text-decoration: underline; margin-top: 55px; font-size: 10.5pt;">{kades_name.upper()}</div>
        </div>
      </div>""",
        4,
        show_header=False,
        show_footer=True,
    )

    # Page 5 (v - ODD)
    card_4_preface_en = make_page_card(
        "PREFACE",
        "PREFACE",
        "v",
        f"""      <h2 style="text-align: center; color: #0b3c5d; font-size: 14pt; font-weight: 800; font-style: italic; margin-top: 10px; margin-bottom: 25px;">PREFACE</h2>
      <div style="font-size: 9.5pt; line-height: 1.6; font-style: italic; color: #475569; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Praise be to God Almighty for His blessings, the official publication <i>"Potentials of {name_title} {admin_type_en} {year}"</i> has been successfully completed. This publication was compiled by <strong>{gov_name_en}</strong> using data from the Village Potential Survey (PODES) {data_year} by BPS-Statistics Indonesia and edited by BPS-Statistics Mempawah Regency.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">The presented data is expected to serve as a standard reference for the {admin_type_en} Government and stakeholders in evidence-based development planning.</p>
      </div>
      <div style="margin-top: 35px; font-size: 9.5pt; text-align: right; padding-right: 20px;">
        <div style="margin-bottom: 15px; font-style: italic; color: #475569;">{name_title}, August {year}</div>
        <div style="display: inline-block; text-align: center;">
          <div style="font-weight: 700; font-style: italic; color: #0b3c5d;">{kades_title_en.upper()}</div>
          <div style="font-weight: 800; color: #0b3c5d; text-decoration: underline; margin-top: 55px; font-size: 10.5pt;">{kades_name.upper()}</div>
        </div>
      </div>""",
        5,
        show_header=False,
        show_footer=True,
    )

    # Page 6 (vi - EVEN)
    card_5_toc = make_page_card(
        "DAFTAR ISI",
        "CONTENTS",
        "vi",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">DAFTAR ISI/<i>CONTENTS</i></h2>
        <div style="font-size: 10.5pt; font-weight: 700; color: #2d3748; margin-top: 4px;">Potensi {admin_type} {name_title} {year}</div>
        <div style="font-size: 10.5pt; font-weight: 700; font-style: italic; color: #475569;">Potentials of {name_title} {admin_type_en} {year}</div>
      </div>
      <style>
        .toc-list {{ list-style: none; padding: 0; margin: 0; }}
        .toc-list li {{ position: relative; overflow: hidden; line-height: 1.5; font-size: 9.5pt; margin-bottom: 6px; clear: both; color: #2d3748; }}
        .toc-list li .toc-page {{ position: absolute; right: 0; bottom: 0; background: #fff; padding-left: 6px; z-index: 2; font-size: 9.5pt; }}
        .toc-list li .toc-title {{ background: #fff; padding-right: 6px; position: relative; z-index: 2; }}
        .toc-list li::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 4px; border-bottom: 1.2px dotted #777; z-index: 1; }}
      </style>
      <ul class="toc-list">
        <li><span class="toc-title">Kata Pengantar/<i>Preface</i></span><span class="toc-page">iv</span></li>
        <li><span class="toc-title">Daftar Isi/<i>Contents</i></span><span class="toc-page">vi</span></li>
        <li><span class="toc-title">Daftar Tabel/<i>List of Tables</i></span><span class="toc-page">vii</span></li>
        <li><span class="toc-title">Penjelasan Umum/<i>Explanatory Notes</i></span><span class="toc-page">viii</span></li>
        <li><span class="toc-title">Daftar Singkatan/<i>List of Abbreviations</i></span><span class="toc-page">ix</span></li>
        <li><span class="toc-title">Statistik Kunci PODES {data_year}/<i>Key Statistics</i></span><span class="toc-page">1</span></li>
        <li><span class="toc-title">1.&nbsp;&nbsp;&nbsp;Wilayah Administrasi, Demografi & Kawasan</span><span class="toc-page">3</span></li>
        <li><span class="toc-title">2.&nbsp;&nbsp;&nbsp;Energi, Utilitas Perumahan & Mitigasi Bencana</span><span class="toc-page">6</span></li>
        <li><span class="toc-title">3.&nbsp;&nbsp;&nbsp;Fasilitas Sosial (Pendidikan & Kesehatan)</span><span class="toc-page">9</span></li>
        <li><span class="toc-title">4.&nbsp;&nbsp;&nbsp;Transportasi, Komunikasi & Ekonomi</span><span class="toc-page">12</span></li>
        <li><span class="toc-title">5.&nbsp;&nbsp;&nbsp;Pemerintahan, Kelembagaan & Informasi Desa</span><span class="toc-page">16</span></li>
      </ul>""",
        6,
        show_header=False,
        show_footer=True,
    )

    # Page 7 (vii - ODD)
    card_5b_lot = make_page_card(
        "DAFTAR TABEL",
        "LIST OF TABLES",
        "vii",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">DAFTAR TABEL/<i>LIST OF TABLES</i></h2>
      </div>
      <style>
        .lot-hdr {{ display: flex; justify-content: space-between; font-size: 8.8pt; color: #2d3748; margin-bottom: 12px; line-height: 1.3; font-weight: 700; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }}
        .lot-hdr-no {{ width: 50px; }}
        .lot-hdr-pg {{ text-align: right; }}
        .lot-list {{ list-style: none; padding: 0; margin: 0; }}
        .lot-list li {{ display: flex; align-items: flex-start; position: relative; line-height: 1.4; font-size: 8.8pt; margin-bottom: 10px; color: #2d3748; }}
        .lot-list li .lot-no {{ width: 50px; flex-shrink: 0; font-weight: 700; background: #fff; z-index: 2; font-size: 8.8pt; }}
        .lot-list li .lot-title-wrap {{ flex: 1; position: relative; padding-right: 35px; min-height: 1.4em; }}
        .lot-list li .lot-title {{ background: #fff; padding-right: 6px; position: relative; z-index: 2; display: inline; }}
        .lot-list li .lot-dots {{ position: absolute; left: 0; right: 0; bottom: 3px; border-bottom: 1.2px dotted #777; z-index: 1; }}
        .lot-list li .lot-page {{ position: absolute; right: 0; bottom: 0; background: #fff; padding-left: 6px; z-index: 2; font-size: 8.8pt; font-weight: 600; }}
        .lot-sec {{ font-weight: 800; color: #0b3c5d; font-size: 9pt; margin-top: 12px; margin-bottom: 6px; text-transform: uppercase; }}
      </style>
      <div class="lot-hdr"><span class="lot-hdr-no">Tabel<br><i>Table</i></span><span class="lot-hdr-pg">Halaman<br><i>Page</i></span></div>
      <div class="lot-sec">1.&nbsp;&nbsp;WILAYAH ADMINISTRASI & DEMOGRAFI</div>
      <ul class="lot-list">
        <li><span class="lot-no">1.1</span><div class="lot-title-wrap"><span class="lot-title">Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW</span><span class="lot-dots"></span></div><span class="lot-page">4</span></li>
        <li><span class="lot-no">1.2</span><div class="lot-title-wrap"><span class="lot-title">Jumlah Penduduk, Sex Ratio, dan Keluarga Pertanian</span><span class="lot-dots"></span></div><span class="lot-page">5</span></li>
      </ul>
      <div class="lot-sec">2.&nbsp;&nbsp;ENERGI, UTILITAS & MITIGASI BENCANA</div>
      <ul class="lot-list">
        <li><span class="lot-no">2.1</span><div class="lot-title-wrap"><span class="lot-title">Penggunaan Daya Listrik, Penerangan Jalan & Bahan Bakar</span><span class="lot-dots"></span></div><span class="lot-page">7</span></li>
        <li><span class="lot-no">2.2</span><div class="lot-title-wrap"><span class="lot-title">Sumber Air Minum Utama dan Mitigasi Bencana Alam</span><span class="lot-dots"></span></div><span class="lot-page">8</span></li>
      </ul>
      <div class="lot-sec">3.&nbsp;&nbsp;FASILITAS SOSIAL</div>
      <ul class="lot-list">
        <li><span class="lot-no">3.1</span><div class="lot-title-wrap"><span class="lot-title">Ketersediaan Sarana Pendidikan Formal dan Keagamaan</span><span class="lot-dots"></span></div><span class="lot-page">10</span></li>
        <li><span class="lot-no">3.2</span><div class="lot-title-wrap"><span class="lot-title">Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu</span><span class="lot-dots"></span></div><span class="lot-page">11</span></li>
      </ul>
      <div class="lot-sec">4.&nbsp;&nbsp;TRANSPORTASI, KOMUNIKASI & EKONOMI</div>
      <ul class="lot-list">
        <li><span class="lot-no">4.1</span><div class="lot-title-wrap"><span class="lot-title">Prasarana Transportasi, Akses Jalan, dan Angkutan Umum</span><span class="lot-dots"></span></div><span class="lot-page">13</span></li>
        <li><span class="lot-no">4.2</span><div class="lot-title-wrap"><span class="lot-title">Menara BTS, Operator Seluler, dan Sinyal Internet</span><span class="lot-dots"></span></div><span class="lot-page">14</span></li>
        <li><span class="lot-no">4.3</span><div class="lot-title-wrap"><span class="lot-title">Fasilitas Ekonomi Utama, Mata Pencaharian, dan IMK</span><span class="lot-dots"></span></div><span class="lot-page">15</span></li>
      </ul>
      <div class="lot-sec">5.&nbsp;&nbsp;PEMERINTAHAN & KELEMBAGAAN</div>
      <ul class="lot-list">
        <li><span class="lot-no">5.1</span><div class="lot-title-wrap"><span class="lot-title">Aparatur Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa</span><span class="lot-dots"></span></div><span class="lot-page">17</span></li>
      </ul>""",
        7,
        show_header=False,
        show_footer=True,
    )

    # Page 8 (viii - EVEN)
    card_6_tech_notes = make_page_card(
        "PENJELASAN UMUM",
        "EXPLANATORY NOTES",
        "viii",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">PENJELASAN UMUM/<i>EXPLANATORY NOTES</i></h2>
      </div>
      <div style="font-size: 9pt; line-height: 1.6; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 12px;"><strong>1. Tanda-tanda Khusus / <i>Symbols:</i></strong></p>
        <table style="width: 100%; border: none; font-size: 8.8pt; margin-bottom: 20px; line-height: 1.6;">
          <tr><td style="width: 80px; font-weight: 700;">-</td><td>Data tidak ada / <i>Data not available</i></td></tr>
          <tr><td style="font-weight: 700;">0 / 0,00</td><td>Data terkecil / <i>Data too small to be expressed</i></td></tr>
          <tr><td style="font-weight: 700;">NA</td><td>Data tidak dapat diaplikasikan / <i>Not applicable</i></td></tr>
        </table>
        <p style="margin-bottom: 12px;"><strong>2. Satuan / <i>Units:</i></strong></p>
        <p style="text-indent: 15px; margin-bottom: 15px;">Satuan berat, luas, dan volume yang digunakan dalam publikasi ini menggunakan Sistem Metrik Standar Internasional.</p>
      </div>""",
        8,
        show_header=False,
        show_footer=True,
    )

    # Page 9 (ix - ODD)
    card_7_abbreviations = make_page_card(
        "DAFTAR SINGKATAN",
        "LIST OF ABBREVIATIONS",
        "ix",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">DAFTAR SINGKATAN/<i>ABBREVIATIONS</i></h2>
      </div>
      <div style="font-size: 8.8pt; line-height: 1.7; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <table style="width: 100%; border: none; font-size: 8.5pt;">
          <tr><td style="width: 110px; font-weight: 700;">BPS</td><td>Badan Pusat Statistik / <i>BPS-Statistics Indonesia</i></td></tr>
          <tr><td style="font-weight: 700;">PODES</td><td>Potensi Desa / <i>Village Potential Survey</i></td></tr>
          <tr><td style="font-weight: 700;">RT / RW</td><td>Rukun Tetangga / Rukun Warga</td></tr>
          <tr><td style="font-weight: 700;">KK</td><td>Kepala Keluarga / <i>Head of Household</i></td></tr>
          <tr><td style="font-weight: 700;">PLN</td><td>Perusahaan Listrik Negara / <i>State Electricity Corporation</i></td></tr>
          <tr><td style="font-weight: 700;">BTS</td><td>Base Transceiver Station</td></tr>
          <tr><td style="font-weight: 700;">IMK</td><td>Industri Mikro dan Kecil / <i>Micro & Small Industries</i></td></tr>
          <tr><td style="font-weight: 700;">SID</td><td>Sistem Informasi Desa / <i>Village Information System</i></td></tr>
          <tr><td style="font-weight: 700;">BPD / LMK</td><td>Badan Permusyawaratan Desa / Lembaga Musyawarah Kelurahan</td></tr>
        </table>
      </div>""",
        9,
        show_header=False,
        show_footer=True,
    )

    # Page 10 (x - EVEN): Blank Page
    card_blank = make_blank_page()

    # Page 11 (Arab 1 - ODD): Key Stats Infographic
    card_8_keystats = make_page_card(
        "STATISTIK KUNCI PODES 2025",
        "KEY STATISTICS PODES 2025",
        "1",
        f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 18px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #0b3c5d; margin: 0; text-transform: uppercase;">STATISTIK KUNCI PODES {data_year}</h2>
        <div style="font-size: 10pt; font-weight: 700; font-style: italic; color: #475569;">Key Statistics of PODES {data_year}</div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
        <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-left: 4px solid #16a34a; padding: 12px; border-radius: 8px;">
          <div style="font-size: 8pt; font-weight: 800; color: #166534; text-transform: uppercase;">Total Penduduk / Population</div>
          <div style="font-size: 18pt; font-weight: 900; color: #15803d; margin: 4px 0;">{tot_pop_str} Jiwa</div>
          <div style="font-size: 7.5pt; color: #166534;">{l_str} Laki-laki | {p_str} Perempuan (Sex Ratio: {sr_str})</div>
        </div>
        <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-left: 4px solid #2563eb; padding: 12px; border-radius: 8px;">
          <div style="font-size: 8pt; font-weight: 800; color: #1e40af; text-transform: uppercase;">Total Keluarga / Households</div>
          <div style="font-size: 18pt; font-weight: 900; color: #1d4ed8; margin: 4px 0;">{kk_str} KK</div>
          <div style="font-size: 7.5pt; color: #1e40af;">Keluarga Pertanian: {kk_pert_str} KK ({m.kk_pertanian_pct}%)</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px;">
        <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #92400e;">LISTRIK PLN / ELECTRICITY</div>
          <div style="font-size: 13pt; font-weight: 800; color: #b45309; margin-top: 3px;">{fmt_val(m.listrik_pln)} KK</div>
          <div style="font-size: 7pt; color: #78350f;">{((m.listrik_pln/max(1, m.jumlah_kk))*100):.1f}% Cakupan PLN</div>
        </div>
        <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-left: 3.5px solid #9333ea; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #6b21a8;">MENARA BTS / BTS TOWERS</div>
          <div style="font-size: 13pt; font-weight: 800; color: #7e22ce; margin-top: 3px;">{m.jumlah_bts} Menara</div>
          <div style="font-size: 7pt; color: #581c87;">Sinyal: {m.sinyal_hp}</div>
        </div>
        <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #115e59;">INDUSTRI MIKRO (IMK)</div>
          <div style="font-size: 13pt; font-weight: 800; color: #0f766e; margin-top: 3px;">{m.jumlah_imk} Usaha</div>
          <div style="font-size: 7pt; color: #134e4a;">Usaha Pengolahan Mikro</div>
        </div>
      </div>

      <div class="narrative-box" style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 10px; border-radius: 6px;">
        <div class="narrative-title">RINGKASAN PROFIL DESA PODES {data_year}</div>
        <p style="margin-bottom: 4px; font-size: 8.5pt;">{admin_type} {name_title} berstatus wilayah <strong>{m.status_daerah}</strong> dengan lokasi kantor di <strong>{m.alamat_lengkap}</strong>. Jumlah wilayah terbagi atas <strong>{m.jumlah_rw} RW</strong> dan <strong>{m.jumlah_rt} RT</strong>. Mata pencaharian utama sebagian besar masyarakat adalah <strong>{m.sumber_penghasilan_utama} ({m.subsektor_utama})</strong>.</p>
      </div>""",
        11,
        show_header=True,
        show_footer=True,
    )

    # Chapters Construction
    # Chapter 1 Cover (Arab Page 3 - Page 13)
    info_ch1 = f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3.5px solid #16a34a; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #166534;">STATUS WILAYAH / REGIONAL STATUS</div>
        <div style="font-size: 12pt; font-weight: 900; color: #15803d; margin-top: 2px;">{m.status_daerah}</div>
        <div style="font-size: 7pt; color: #166534;">Kawasan Hutan: {m.kawasan_hutan}</div>
      </div>
      <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3.5px solid #2563eb; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #1e40af;">ADMINISTRASI RT / RW</div>
        <div style="font-size: 12pt; font-weight: 900; color: #1d4ed8; margin-top: 2px;">{m.jumlah_rw} RW | {m.jumlah_rt} RT</div>
        <div style="font-size: 7pt; color: #1e40af;">Wilayah Kerja Pembinaan Statis</div>
      </div>
    </div>
    <p style="font-size: 8.8pt; line-height: 1.5; color: #334155; text-align: justify; margin: 0;">{admin_type} {name_title} berstatus sebagai wilayah <strong>{m.status_daerah}</strong> dengan lokasi kantor berada di <strong>{m.alamat_lengkap}</strong>. Jumlah penduduk tercatat sebanyak <strong>{tot_pop_str} jiwa</strong> ({l_str} laki-laki, {p_str} perempuan) dengan <i>sex ratio</i> <strong>{sr_str}</strong>. Total keluarga sebanyak <strong>{kk_str} KK</strong>, di mana <strong>{kk_pert_str} KK ({m.kk_pertanian_pct}%)</strong> bergerak di sektor pertanian.</p>"""

    cover_ch1 = make_cover_card(
        "1",
        "WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN",
        "ADMINISTRATIVE AREA, DEMOGRAPHICS & REGION",
        info_ch1,
    )
    p_ch1_cover = make_page_card("BAB I WILAYAH ADMINISTRASI & DEMOGRAFI", "CHAPTER I ADMINISTRATIVE & DEMOGRAPHICS", "3", cover_ch1, 13, show_header=False)

    tech_ch1 = f"""<div class="tech-notes-card">
      <div class="tech-notes-title">PENJELASAN TEKNIS BAB I / TECHNICAL NOTES CHAPTER I</div>
      <ol class="tech-notes-list">
        <li><strong>Status Daerah</strong>: Pengklasifikasian wilayah menjadi Perdesaan atau Perkotaan.<span class="en">Regional status classification into Rural or Urban areas.</span></li>
        <li><strong>Keluarga Pertanian</strong>: Rumah tangga yang sekurang-kurangnya satu anggotanya mengelola usaha pertanian.<span class="en">Agricultural households with at least one member operating farming activities.</span></li>
      </ol>
    </div>"""

    tbl_1_1 = f"""<div class="section-header">1.1 STATUS WILAYAH & KAWASAN HUTAN<span class="en">1.1 REGIONAL STATUS & FOREST AREA</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 1.1</span><div class="table-title-text">Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW Tahun {data_year}<span class="en">Regional Identity, Forest Area Relation, and RT/RW Breakdown {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Kewilayahan<br><i>Regional Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Status Klasifikasi Wilayah / <i>Regional Status</i></td><td class="text-center"><strong>{m.status_daerah}</strong></td></tr>
        <tr><td>Alamat Lengkap Kantor / <i>Office Address</i></td><td>{m.alamat_lengkap}</td></tr>
        <tr><td>Lokasi Terhadap Kawasan Hutan / <i>Forest Relation</i></td><td>{m.kawasan_hutan}</td></tr>
        <tr><td>Jumlah Rukun Warga (RW) / <i>Number of RWs</i></td><td class="text-center"><strong>{m.jumlah_rw} RW</strong></td></tr>
        <tr><td>Jumlah Rukun Tetangga (RT) / <i>Number of RTs</i></td><td class="text-center"><strong>{m.jumlah_rt} RT</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch1_content = make_page_card("BAB I WILAYAH ADMINISTRASI & DEMOGRAFI", "CHAPTER I ADMINISTRATIVE & DEMOGRAPHICS", "4", tech_ch1 + tbl_1_1, 14, show_header=True)

    tbl_1_2 = f"""<div class="section-header">1.2 KEPENDUDUKAN & KELUARGA PERTANIAN<span class="en">1.2 DEMOGRAPHICS & AGRICULTURAL HOUSEHOLDS</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 1.2</span><div class="table-title-text">Jumlah Penduduk Menurut Jenis Kelamin, Sex Ratio, dan Keluarga Pertanian Tahun {data_year}<span class="en">Population by Gender, Sex Ratio, and Agricultural Households {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Demografi & Pertanian<br><i>Demographic & Agricultural Indicator</i></th><th class="main-header">Jumlah / Nilai<br><i>Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Penduduk Laki-laki / <i>Male Population</i></td><td class="text-right">{l_str} jiwa ({m.male_pct}%)</td></tr>
        <tr><td>Penduduk Perempuan / <i>Female Population</i></td><td class="text-right">{p_str} jiwa ({m.female_pct}%)</td></tr>
        <tr class="total-row"><td>Total Penduduk / <i>Total Population</i></td><td class="text-right">{tot_pop_str} jiwa</td></tr>
        <tr><td>Rasio Jenis Kelamin / <i>Sex Ratio</i></td><td class="text-right"><strong>{sr_str}</strong></td></tr>
        <tr><td>Total Keluarga (KK) / <i>Total Households</i></td><td class="text-right">{kk_str} KK</td></tr>
        <tr><td>Keluarga Pertanian / <i>Agricultural Households</i></td><td class="text-right"><strong>{kk_pert_str} KK ({m.kk_pertanian_pct}%)</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch1_tbl2 = make_page_card("BAB I WILAYAH ADMINISTRASI & DEMOGRAFI", "CHAPTER I ADMINISTRATIVE & DEMOGRAPHICS", "5", tbl_1_2, 15, show_header=True)

    # Chapter 2 Cover (Arab Page 6 - Page 16)
    info_ch2 = f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
      <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #92400e;">LISTRIK PLN / PLN ELECTRICITY</div>
        <div style="font-size: 12pt; font-weight: 900; color: #b45309; margin-top: 2px;">{fmt_val(m.listrik_pln)} KK</div>
        <div style="font-size: 7pt; color: #78350f;">{((m.listrik_pln/max(1, m.jumlah_kk))*100):.1f}% Pelanggan Listrik PLN</div>
      </div>
      <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #115e59;">AIR MINUM UTAMA / DRINKING WATER</div>
        <div style="font-size: 12pt; font-weight: 900; color: #0f766e; margin-top: 2px;">{m.air_minum}</div>
        <div style="font-size: 7pt; color: #134e4a;">Sumber Air Utama Masyarakat</div>
      </div>
    </div>
    <p style="font-size: 8.8pt; line-height: 1.5; color: #334155; text-align: justify; margin: 0;">Penggunaan daya listrik PLN mencakup <strong>{fmt_val(m.listrik_pln)} KK ({((m.listrik_pln/max(1, m.jumlah_kk))*100):.1f}%)</strong>. Sebagian besar keluarga memanfaatkan air minum utama berjenis <strong>{m.air_minum}</strong> dan bahan bakar utama memasak berjenis <strong>{m.bakar_masak}</strong>. Keberadaan upaya mitigasi bencana tercatat <strong>"{m.mitigasi_bencana}"</strong>.</p>"""

    cover_ch2 = make_cover_card(
        "2",
        "ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA",
        "ENERGY, HOUSING UTILITIES & DISASTER MITIGATION",
        info_ch2,
    )
    p_ch2_cover = make_page_card("BAB II ENERGI & BENCANA", "CHAPTER II ENERGY & DISASTER", "6", cover_ch2, 16, show_header=False)

    tbl_2_1 = f"""<div class="section-header">2.1 PENGGUNAAN LISTRIK & BAHAN BAKAR<span class="en">2.1 ELECTRICITY & COOKING FUEL USAGE</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 2.1</span><div class="table-title-text">Penggunaan Daya Listrik, Penerangan Jalan Utama, dan Bahan Bakar Memasak Tahun {data_year}<span class="en">Electricity Power, Road Lighting, and Fuel Usage {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Energi & Utilitas<br><i>Energy & Utility Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Pengguna Listrik PLN / <i>PLN Electricity Users</i></td><td class="text-right"><strong>{fmt_val(m.listrik_pln)} KK</strong></td></tr>
        <tr><td>Pengguna Listrik Non-PLN / <i>Non-PLN Users</i></td><td class="text-right">{fmt_val(m.listrik_non_pln)} KK</td></tr>
        <tr><td>Bukan Pengguna Listrik / <i>Non-Electricity Users</i></td><td class="text-right">{fmt_val(m.bukan_listrik)} KK</td></tr>
        <tr><td>Penerangan Jalan Utama / <i>Main Road Lighting</i></td><td>{m.penerangan_jalan}</td></tr>
        <tr><td>Bahan Bakar Memasak / <i>Cooking Fuel</i></td><td><strong>{m.bakar_masak}</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch2_tbl1 = make_page_card("BAB II ENERGI & BENCANA", "CHAPTER II ENERGY & DISASTER", "7", tbl_2_1, 17, show_header=True)

    tbl_2_2 = f"""<div class="section-header">2.2 AIR MINUM & MITIGASI BENCANA<span class="en">2.2 DRINKING WATER & DISASTER MITIGATION</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 2.2</span><div class="table-title-text">Sumber Air Minum Utama dan Keberadaan Mitigasi Bencana Alam Tahun {data_year}<span class="en">Main Drinking Water Source and Natural Disaster Mitigation {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Lingkungan & Bencana<br><i>Environment & Disaster Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Sumber Air Minum Utama / <i>Main Water Source</i></td><td><strong>{m.air_minum}</strong></td></tr>
        <tr><td>Kejadian Bencana Alam / <i>Natural Disaster Incident</i></td><td>{m.bencana_alam}</td></tr>
        <tr><td>Upaya & Mitigasi Bencana / <i>Disaster Mitigation Facilities</i></td><td>{m.mitigasi_bencana}</td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch2_tbl2 = make_page_card("BAB II ENERGI & BENCANA", "CHAPTER II ENERGY & DISASTER", "8", tbl_2_2, 18, show_header=True)

    # Chapter 3 Cover (Arab Page 9 - Page 19)
    info_ch3 = f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
      <div style="background: #fdf2f8; border: 1px solid #fbcfe8; border-left: 3.5px solid #db2777; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #9d174d;">POSYANDU AKTIF / ACTIVE POSYANDU</div>
        <div style="font-size: 12pt; font-weight: 900; color: #be185d; margin-top: 2px;">{m.posyandu_aktif} Unit</div>
        <div style="font-size: 7pt; color: #9d174d;">Pemeriksaan Kesehatan Bulanan</div>
      </div>
      <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-left: 3.5px solid #9333ea; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #6b21a8;">POSBINDU / POSBINDU UNITS</div>
        <div style="font-size: 12pt; font-weight: 900; color: #7e22ce; margin-top: 2px;">{m.posbindu} Unit</div>
        <div style="font-size: 7pt; color: #581c87;">Pos Pembinaan Terpadu Lansia</div>
      </div>
    </div>
    <p style="font-size: 8.8pt; line-height: 1.5; color: #334155; text-align: justify; margin: 0;">Pelayanan kesehatan masyarakat berbasis komunitas didukung oleh keberadaan <strong>{m.posyandu_aktif} Posyandu aktif</strong> yang rutin menyelenggarakan pelayanan bulanan dan <strong>{m.posbindu} Posbindu</strong>. Fasilitas pendidikan formal & keagamaan yang tersedia meliputi <strong>{m.sarana_pendidikan}</strong>.</p>"""

    cover_ch3 = make_cover_card(
        "3",
        "FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)",
        "SOCIAL FACILITIES (EDUCATION & HEALTH)",
        info_ch3,
    )
    p_ch3_cover = make_page_card("BAB III FASILITAS SOSIAL", "CHAPTER III SOCIAL FACILITIES", "9", cover_ch3, 19, show_header=False)

    tbl_3_1 = f"""<div class="section-header">3.1 SARANA PENDIDIKAN FORMAL & KEAGAMAAN<span class="en">3.1 FORMAL & RELIGIOUS EDUCATION FACILITIES</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 3.1</span><div class="table-title-text">Rekapitulasi Ketersediaan Sarana Pendidikan Formal dan Keagamaan Tahun {data_year}<span class="en">Availability of Formal and Religious Education Facilities {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Kategori Sarana / <i>Facility Category</i></th><th class="main-header">Rincian Ketersediaan Sarana / <i>Availability Details</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Fasilitas Pendidikan / <i>Education Facilities</i></td><td>{m.sarana_pendidikan}</td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch3_tbl1 = make_page_card("BAB III FASILITAS SOSIAL", "CHAPTER III SOCIAL FACILITIES", "10", tbl_3_1, 20, show_header=True)

    tbl_3_2 = f"""<div class="section-header">3.2 SARANA KESEHATAN, POSYANDU & POSBINDU<span class="en">3.2 HEALTH FACILITIES, POSYANDU & POSBINDU</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 3.2</span><div class="table-title-text">Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu Tahun {data_year}<span class="en">Health Facilities, Active Posyandu, and Posbindu {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Pelayanan Kesehatan<br><i>Health Service Indicator</i></th><th class="main-header">Jumlah / Keterangan<br><i>Value / Description</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Fasilitas Kesehatan Utama / <i>Main Health Facilities</i></td><td>{m.sarana_kesehatan}</td></tr>
        <tr><td>Posyandu Aktif (Bulanan) / <i>Active Posyandu</i></td><td class="text-right"><strong>{m.posyandu_aktif} unit</strong></td></tr>
        <tr><td>Posbindu / <i>Posbindu Units</i></td><td class="text-right"><strong>{m.posbindu} unit</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch3_tbl2 = make_page_card("BAB III FASILITAS SOSIAL", "CHAPTER III SOCIAL FACILITIES", "11", tbl_3_2, 21, show_header=True)

    # Chapter 4 Cover (Arab Page 12 - Page 22)
    info_ch4 = f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
      <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3.5px solid #2563eb; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #1e40af;">MENARA BTS & INTERNET / BTS TOWERS</div>
        <div style="font-size: 12pt; font-weight: 900; color: #1d4ed8; margin-top: 2px;">{m.jumlah_bts} Menara ({m.sinyal_internet})</div>
        <div style="font-size: 7pt; color: #1e40af;">Sinyal Telepon Seluler: {m.sinyal_hp}</div>
      </div>
      <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #115e59;">INDUSTRI MIKRO (IMK) / MICRO INDUSTRIES</div>
        <div style="font-size: 12pt; font-weight: 900; color: #0f766e; margin-top: 2px;">{fmt_val(m.jumlah_imk)} Usaha</div>
        <div style="font-size: 7pt; color: #134e4a;">Usaha Pengolahan Mikro & Kecil</div>
      </div>
    </div>
    <p style="font-size: 8.8pt; line-height: 1.5; color: #334155; text-align: justify; margin: 0;">Prasarana jalan utama di {admin_type} {name_title} memiliki permukaan jalan berjenis <strong>{m.jenis_jalan}</strong>. Sarana telekomunikasi ditopang oleh <strong>{m.jumlah_bts} Menara BTS</strong> dengan sinyal <strong>{m.sinyal_internet}</strong>. Sektor perekonomian didukung ketersediaan <strong>{fmt_val(m.jumlah_imk)} unit usaha Industri Mikro dan Kecil (IMK)</strong>.</p>"""

    cover_ch4 = make_cover_card(
        "4",
        "TRANSPORTASI, KOMUNIKASI & EKONOMI",
        "TRANSPORTATION, COMMUNICATION & ECONOMY",
        info_ch4,
    )
    p_ch4_cover = make_page_card("BAB IV TRANSPORTASI & EKONOMI", "CHAPTER IV TRANSPORT & ECONOMY", "12", cover_ch4, 22, show_header=False)

    tbl_4_1 = f"""<div class="section-header">4.1 TRANSPORTASI & PRASARANA JALAN<span class="en">4.1 TRANSPORT & ROAD INFRASTRUCTURE</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 4.1</span><div class="table-title-text">Prasarana Transportasi, Jenis Permukaan Jalan, dan Angkutan Umum Tahun {data_year}<span class="en">Transport Infrastructure, Road Surface, and Public Transit {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Transportasi<br><i>Transport Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Prasarana Transportasi Utama / <i>Main Infrastructure</i></td><td>{m.prasarana_transportasi}</td></tr>
        <tr><td>Jenis Permukaan Jalan Utama / <i>Road Surface</i></td><td><strong>{m.jenis_jalan}</strong></td></tr>
        <tr><td>Aksesibilitas Roda 4 atau Lebih / <i>4-Wheel Vehicle Access</i></td><td>{m.jalan_roda4}</td></tr>
        <tr><td>Operasional Angkutan Umum / <i>Public Transit Service</i></td><td>{m.angkutan_umum}</td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch4_tbl1 = make_page_card("BAB IV TRANSPORTASI & EKONOMI", "CHAPTER IV TRANSPORT & ECONOMY", "13", tbl_4_1, 23, show_header=True)

    tbl_4_2 = f"""<div class="section-header">4.2 TELEKOMUNIKASI, BTS & SINYAL INTERNET<span class="en">4.2 TELECOM, BTS & INTERNET SIGNAL</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 4.2</span><div class="table-title-text">Keberadaan Menara BTS, Operator Telekomunikasi, dan Sinyal Internet Tahun {data_year}<span class="en">BTS Towers, Telecom Operators, and Internet Network {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Telekomunikasi<br><i>Telecom Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Jumlah Menara BTS / <i>BTS Towers</i></td><td class="text-right"><strong>{m.jumlah_bts} unit</strong></td></tr>
        <tr><td>Operator Layanan Seluler / <i>Mobile Operators</i></td><td>{m.operator_seluler}</td></tr>
        <tr><td>Kekuatan Sinyal Telepon Seluler / <i>Cellular Signal Strength</i></td><td><strong>{m.sinyal_hp}</strong></td></tr>
        <tr><td>Jaringan Internet Seluler / <i>Mobile Internet Network</i></td><td><strong>{m.sinyal_internet}</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch4_tbl2 = make_page_card("BAB IV TRANSPORTASI & EKONOMI", "CHAPTER IV TRANSPORT & ECONOMY", "14", tbl_4_2, 24, show_header=True)

    tbl_4_3 = f"""<div class="section-header">4.3 FASILITAS EKONOMI & INDUSTRI MIKRO KECIL (IMK)<span class="en">4.3 ECONOMIC FACILITIES & MICRO SMALL INDUSTRIES</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 4.3</span><div class="table-title-text">Fasilitas Ekonomi Utama, Mata Pencaharian, dan IMK Tahun {data_year}<span class="en">Economic Facilities, Livelihood, and Micro Small Industries {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Ekonomi & Industri<br><i>Economic & Industry Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Mata Pencaharian Utama / <i>Main Livelihood</i></td><td><strong>{m.sumber_penghasilan_utama} ({m.subsektor_utama})</strong></td></tr>
        <tr><td>Fasilitas Ekonomi Utama / <i>Economic Facilities</i></td><td>{m.sarana_ekonomi}</td></tr>
        <tr><td>Industri Mikro & Kecil (IMK) / <i>Micro Small Industries</i></td><td class="text-right"><strong>{fmt_val(m.jumlah_imk)} unit usaha</strong></td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch4_tbl3 = make_page_card("BAB IV TRANSPORTASI & EKONOMI", "CHAPTER IV TRANSPORT & ECONOMY", "15", tbl_4_3, 25, show_header=True)

    # Chapter 5 Cover (Arab Page 16 - Page 26)
    info_ch5 = f"""<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3.5px solid #16a34a; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #166534;">APARATUR DESA / APPARATUS</div>
        <div style="font-size: 12pt; font-weight: 900; color: #15803d; margin-top: 2px;">{m.aparatur_pemdes} Orang</div>
        <div style="font-size: 7pt; color: #166534;">Aparatur Pemerintah {admin_type}</div>
      </div>
      <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px;">
        <div style="font-size: 7.5pt; font-weight: 800; color: #92400e;">SISTEM INFORMASI (SID) / INFO SYSTEM</div>
        <div style="font-size: 12pt; font-weight: 900; color: #b45309; margin-top: 2px;">{m.sistem_informasi_desa}</div>
        <div style="font-size: 7pt; color: #78350f;">Musyawarah Desa: {m.musyawarah_desa} kali/tahun</div>
      </div>
    </div>
    <p style="font-size: 8.8pt; line-height: 1.5; color: #334155; text-align: justify; margin: 0;">Penyelenggaraan pemerintah desa didukung oleh <strong>{m.aparatur_pemdes} orang aparatur</strong>, keberadaan BPD/LMK tercatat <strong>"{m.keberadaan_bpd}"</strong>, frekuensi musyawarah desa sebanyak <strong>{m.musyawarah_desa} kali</strong>, serta pemanfaatan Sistem Informasi Desa (SID) bernomenklatur <strong>"{m.sistem_informasi_desa}"</strong>.</p>"""

    cover_ch5 = make_cover_card(
        "5",
        "PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA",
        "GOVERNMENT, INSTITUTIONS & VILLAGE INFORMATION",
        info_ch5,
    )
    p_ch5_cover = make_page_card("BAB V PEMERINTAHAN & KELEMBAGAAN", "CHAPTER V GOVT & INSTITUTIONS", "16", cover_ch5, 26, show_header=False)

    tbl_5_1 = f"""<div class="section-header">5.1 APARATUR DESA, BPD/LMK & SISTEM INFORMASI DESA<span class="en">5.1 VILLAGE APPARATUS, BPD & INFO SYSTEM</span></div>
    <div class="table-title-block"><span class="table-num">Tabel 5.1</span><div class="table-title-text">Aparatur Pemerintah Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa Tahun {data_year}<span class="en">Village Apparatus, BPD/LMK Status, and Village Info System {data_year}</span></div></div>
    <table class="bps-table">
      <thead><tr><th class="main-header">Indikator Pemerintahan & Kelembagaan<br><i>Govt & Institutional Indicator</i></th><th class="main-header">Isian Data PODES {data_year}<br><i>Data Value</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr></thead>
      <tbody>
        <tr><td>Aparatur Pemerintah Desa/Kelurahan / <i>Village Apparatus</i></td><td class="text-right"><strong>{m.aparatur_pemdes} orang</strong></td></tr>
        <tr><td>Keberadaan BPD / LMK / <i>Representative Council Status</i></td><td><strong>{m.keberadaan_bpd}</strong></td></tr>
        <tr><td>Kegiatan Musyawarah Desa / <i>Village Meetings</i></td><td class="text-right"><strong>{m.musyawarah_desa} kali</strong></td></tr>
        <tr><td>Sistem Informasi Desa (SID) / <i>Village Info System</i></td><td>{m.sistem_informasi_desa}</td></tr>
        <tr><td>Ketersediaan SPPG / <i>SPPG Status</i></td><td>{m.jumlah_sppg}</td></tr>
      </tbody>
    </table>{meta_std}"""

    p_ch5_tbl1 = make_page_card("BAB V PEMERINTAHAN & KELEMBAGAAN", "CHAPTER V GOVT & INSTITUTIONS", "17", tbl_5_1, 27, show_header=True)

    full_out = html_header
    full_out += card_1_cover + "\n\n"
    full_out += card_2_catalog + "\n\n"
    full_out += card_3_contrib + "\n\n"
    full_out += card_4_preface_id + "\n\n"
    full_out += card_4_preface_en + "\n\n"
    full_out += card_5_toc + "\n\n"
    full_out += card_5b_lot + "\n\n"
    full_out += card_6_tech_notes + "\n\n"
    full_out += card_7_abbreviations + "\n\n"
    full_out += card_blank + "\n\n"  # Page x (10)
    full_out += card_8_keystats + "\n\n"  # Arab Page 1 (11)
    full_out += make_blank_page() + "\n\n"  # Arab Page 2 (12)
    full_out += p_ch1_cover + "\n\n"  # Arab Page 3 (13)
    full_out += p_ch1_content + "\n\n"  # Arab Page 4 (14)
    full_out += p_ch1_tbl2 + "\n\n"  # Arab Page 5 (15)
    full_out += p_ch2_cover + "\n\n"  # Arab Page 6 (16)
    full_out += p_ch2_tbl1 + "\n\n"  # Arab Page 7 (17)
    full_out += p_ch2_tbl2 + "\n\n"  # Arab Page 8 (18)
    full_out += p_ch3_cover + "\n\n"  # Arab Page 9 (19)
    full_out += p_ch3_tbl1 + "\n\n"  # Arab Page 10 (20)
    full_out += p_ch3_tbl2 + "\n\n"  # Arab Page 11 (21)
    full_out += p_ch4_cover + "\n\n"  # Arab Page 12 (22)
    full_out += p_ch4_tbl1 + "\n\n"  # Arab Page 13 (23)
    full_out += p_ch4_tbl2 + "\n\n"  # Arab Page 14 (24)
    full_out += p_ch4_tbl3 + "\n\n"  # Arab Page 15 (25)
    full_out += p_ch5_cover + "\n\n"  # Arab Page 16 (26)
    full_out += p_ch5_tbl1 + "\n\n"  # Arab Page 17 (27)
    full_out += "</div>\n</body>\n</html>"

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-potensi-{name_kebab}-{year}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_out)

    print(f"HTML file written: {out_path}")
    return out_path
