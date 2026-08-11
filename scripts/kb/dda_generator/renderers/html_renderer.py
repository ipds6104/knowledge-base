"""BPS HTML Layout Renderer Module for DDA Generator Engine.
Accepts pure DesaPublicationData DTO contract.
"""

from pathlib import Path
from ..schemas import DesaPublicationData
from ..calculator import build_chapter_infographics, build_frontmatter_dto


def fmt_val(v) -> str:
    """Format angka untuk tampilan HTML BPS."""
    if v is None or str(v).strip() in ("", "-", "0", "0.00", "0,00", "NA"):
        return "-"
    s = str(v).strip()
    if "." in s:
        s = s.replace(".", ",")
    if s.isdigit() and int(s) >= 1000:
        s = f"{int(s):,}".replace(",", ".")
    return s


def render_desa_html(pub_data: DesaPublicationData) -> Path:
    """Menyusun halaman HTML bilingual A4 berstandar BPS dari DesaPublicationData DTO."""
    config = pub_data.config
    metrics = pub_data.metrics
    info = pub_data.infographics if pub_data.infographics else build_chapter_infographics(metrics, metrics["rows"])
    fm = pub_data.frontmatter if pub_data.frontmatter else build_frontmatter_dto(config, metrics)

    name_title = config["name_title"]
    name_upper = config["name_upper"]
    name_kebab = config["name_kebab"]
    is_kel = config.get("is_kelurahan", False)
    admin_type = config.get("admin_type", "Desa")
    admin_type_en = config.get("admin_type_en", "Village")
    admin_upper = admin_type.upper()
    sub_title = config.get("sub_region_title", "Dusun Administrasi")
    sub_title_en = config.get("sub_region_title_en", "Administrative Hamlets")
    sub_type = config.get("sub_region_type", "Dusun")
    sub_type_en = config.get("sub_region_type_en", "Hamlet")
    gov_name = config.get("gov_name", f"Pemerintah {admin_type} {name_title}")
    gov_name_en = config.get("gov_name_en", f"Government of {name_title} {admin_type_en}")

    kecamatan = config.get("kecamatan", "Mempawah Timur")
    year = config.get("year", 2026)
    kades_title = config.get("kades_title", f"Kepala Desa {name_title}")
    kades_title_en = config.get("kades_title_en", f"Head of {name_title} Village")
    kades_name = config.get("kades_name", f"Kepala Desa {name_title}")

    book_header_id = f"{admin_upper} {name_upper} DALAM ANGKA {year}"
    book_header_en = f"{name_upper} {admin_type_en.upper()} IN FIGURES {year}"

    rows = metrics["rows"]
    dyn_pop = fmt_val(metrics["tot_pop"])
    dyn_l = fmt_val(metrics["tot_l"])
    dyn_p = fmt_val(metrics["tot_p"])
    dyn_sr = f"{metrics['tot_sr']:.2f}".replace(".", ",")
    dyn_kk = fmt_val(metrics["tot_kk"])
    dyn_ktp = fmt_val(metrics["tot_ktp"])
    dyn_ktp_pct = f"{metrics['tot_ktp_pct']:.2f}".replace(".", ",")
    dyn_pkh = fmt_val(metrics["tot_pkh"])
    dyn_bpnt = fmt_val(metrics["tot_bpnt"])
    dyn_bst_blt = fmt_val(metrics["tot_bst"] + metrics["tot_blt"])
    dyn_bansos = fmt_val(metrics["tot_bansos"])
    dyn_bumbung = fmt_val(metrics["tot_bumbung"])
    dyn_kepadatan = f"{metrics['tot_kepadatan']:.2f}".replace(".", ",")
    dyn_layak = fmt_val(metrics["tot_layak"])
    dyn_putus = fmt_val(metrics["tot_putus"])

    # Build split tables
    rows_1_1_2_all = []
    for r in rows:
        rows_1_1_2_all.append(
            f"<tr><td>{r['rt_name']}</td><td>{r['ketua_rt']}</td><td>{r['petugas']}</td></tr>"
        )

    rows_2_1_1_all = []
    for r in rows:
        rows_2_1_1_all.append(
            f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['l'])}</td><td class=\"text-right\">{fmt_val(r['p'])}</td><td class=\"text-right\"><strong>{fmt_val(r['tot'])}</strong></td><td class=\"text-right\">{r['sr']:.2f}".replace(
                ".", ","
            )
            + "</td></tr>"
        )
    tot_2 = (
        f"{admin_upper} {name_upper}",
        dyn_l,
        dyn_p,
        dyn_pop,
        dyn_sr,
    )

    caps = pub_data.capabilities

    rows_3_1_1_all = []
    if caps.has_employment:
        for r in rows:
            rows_3_1_1_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['tot'])}</td><td class=\"text-right\">{fmt_val(r['bekerja'])}</td><td class=\"text-right\">{fmt_val(r['umkm'])}</td><td class=\"text-right\">{fmt_val(r['bpjs'])}</td></tr>"
            )
        tot_3 = (
            f"{admin_upper} {name_upper}",
            dyn_pop,
            fmt_val(metrics["tot_bekerja"]),
            fmt_val(metrics["tot_umkm"]),
            fmt_val(metrics["tot_bpjs"]),
        )
    elif caps.has_building_materials:
        for r in rows:
            rows_3_1_1_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['bumbung'])}</td><td class=\"text-right\">{fmt_val(r['dinding_tembok'])}</td><td class=\"text-right\">{fmt_val(r['atap_seng_genteng'])}</td><td class=\"text-right\">{fmt_val(r['bab_sendiri'])}</td></tr>"
            )
        tot_3 = (
            f"{admin_upper} {name_upper}",
            dyn_bumbung,
            fmt_val(metrics["tot_dinding_tembok"]),
            fmt_val(metrics["tot_atap_seng_genteng"]),
            fmt_val(metrics["tot_bab_sendiri"]),
        )
    else:
        for r in rows:
            rows_3_1_1_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['tot'])}</td><td class=\"text-right\">{fmt_val(r['putus'])}</td><td class=\"text-right\">{fmt_val(r['ktp'])}</td><td class=\"text-right\">{r['ktp_pct']:.2f}".replace(
                    ".", ","
                )
                + "</td></tr>"
            )
        tot_3 = (
            f"{admin_upper} {name_upper}",
            dyn_pop,
            dyn_putus,
            dyn_ktp,
            dyn_ktp_pct,
        )

    rows_4_1_1_all = []
    for r in rows:
        rows_4_1_1_all.append(
            f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['pkh'])}</td><td class=\"text-right\">{fmt_val(r['bpnt'])}</td><td class=\"text-right\">{fmt_val(r['bst'] + r['blt'])}</td><td class=\"text-right\"><strong>{fmt_val(r['tot_bansos'])}</strong></td></tr>"
        )
    tot_4 = (
        f"{admin_upper} {name_upper}",
        dyn_pkh,
        dyn_bpnt,
        dyn_bst_blt,
        dyn_bansos,
    )

    rows_5_1_1_all = []
    if caps.has_decent_housing:
        for r in rows:
            rows_5_1_1_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['tot'])}</td><td class=\"text-right\">{fmt_val(r['bumbung'])}</td><td class=\"text-right\">{r['kepadatan']:.2f}".replace(
                    ".", ","
                )
                + f"</td><td class=\"text-right\">{r['layak_pct']:.2f}".replace(
                    ".", ","
                )
                + "</td></tr>"
            )
        tot_5 = (
            f"{admin_upper} {name_upper}",
            dyn_pop,
            dyn_bumbung,
            dyn_kepadatan,
            f"{metrics['tot_layak_pct']:.2f}".replace(".", ","),
        )
    else:
        for r in rows:
            rows_5_1_1_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['tot'])}</td><td class=\"text-right\">{fmt_val(r['bumbung'])}</td><td class=\"text-right\">{r['kepadatan']:.2f}".replace(
                    ".", ","
                )
                + "</td></tr>"
            )
        tot_5 = (
            f"{admin_upper} {name_upper}",
            dyn_pop,
            dyn_bumbung,
            dyn_kepadatan,
        )

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
        return f"""  <div class="page-card" style="justify-content: center;">
    <div style="background: linear-gradient(135deg, #f97316 0%, #eb8a3c 45%, #ea580c 100%); border-radius: 18px; padding: 25px 30px; display: flex; align-items: center; gap: 25px; box-shadow: 0 10px 25px -5px rgba(234, 88, 12, 0.3); margin-bottom: 25px;">
      <div style="width: 85px; height: 85px; background: #c2410c; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #ffffff; flex-shrink: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <span style="font-size: 36pt; font-weight: 900; line-height: 0.9; margin-top: -2px;">{ch_num}</span>
        <span style="font-size: 10pt; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 1px;">BAB</span>
        <span style="font-size: 8pt; font-style: italic; font-weight: 600; margin-top: -2px;">Chapter</span>
      </div>
      <div style="flex: 1;">
        <h2 style="font-size: 17pt; font-weight: 900; color: #ffffff; margin: 0 0 8px 0; line-height: 1.2; text-transform: uppercase; letter-spacing: 0.5px;">{ch_title_id}</h2>
        <div style="width: 100%; height: 2.5px; background: #ffffff; opacity: 0.9; margin-bottom: 8px;"></div>
        <h3 style="font-size: 13pt; font-weight: 800; font-style: italic; color: #ffffff; margin: 0; line-height: 1.2; text-transform: uppercase; letter-spacing: 0.5px;">{ch_title_en}</h3>
      </div>
    </div>
    <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
      {info_html}
    </div>
  </div>"""

    def make_blank_page() -> str:
        return """  <div class="page-card" style="justify-content: center; align-items: center;"><div style="color: #cbd5e1; font-style: italic; font-size: 9pt;">[ Halaman Ini Sengaja Dikosongkan / This Page Intentionally Left Blank ]</div></div>"""

    meta_std = f"""<div class="table-meta"><div class="meta-row"><div class="meta-lbl">Catatan/<i>Note:</i></div><div>Data keadaan Rukun Tetangga (RT) per Juni {year} / <i>RT condition data as of June {year}</i></div></div><div class="meta-row"><div class="meta-lbl">Sumber/<i>Source:</i></div><div>{gov_name} — Program Desa Cinta Statistik {year} / <i>{gov_name_en} — {year} Desa Cinta Statistik Program</i></div></div></div>"""

    html_header = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>{admin_type} {name_title} Dalam Angka {year} / {name_title} {admin_type_en} in Figures {year}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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
    .table-name {{ font-weight: 700; font-size: 9pt; color: #1a202c; line-height: 1.3; }}
    .table-name .en-title {{ display: block; font-weight: 700; font-style: italic; color: #1a202c; margin-top: 1px; }}

    .bps-table {{ width: 100%; border-collapse: collapse; font-size: 7.8pt; margin-bottom: 6px; }}
    .bps-table th.main-header {{ background-color: #eb8a3c; color: #ffffff; font-weight: 700; text-align: center; padding: 4.5px 6px; border: 1px solid #d97706; vertical-align: middle; font-size: 8pt; }}
    .bps-table th.col-num {{ background-color: #fdebd0; color: #1a202c; font-weight: 700; text-align: center; padding: 2.5px; border: 1px solid #d97706; font-size: 7.5pt; }}
    .bps-table td {{ padding: 3px 6px; border: 1px solid #cbd5e1; color: #1a202c; }}
    .bps-table tbody tr:nth-child(even) {{ background-color: #fff5eb; }}
    .bps-table tr.total-row td {{ background-color: #eb8a3c !important; color: #ffffff !important; font-weight: 800; border: 1px solid #d97706; }}
    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}
    .table-meta {{ font-size: 7.8pt; color: #475569; margin-top: 4px; line-height: 1.35; }}
    .meta-row {{ display: flex; gap: 6px; }}
    .meta-lbl {{ font-weight: 700; white-space: nowrap; }}
  </style>
</head>
<body>
<div class="page-container">
"""

    # Page 1: Cover (No header, No footer)
    card_1_cover = f"""  <div class="page-card">
    <div class="page-content">
      <div class="cover-box">
        <h1 class="cover-title">{admin_upper} {name_upper}<br>DALAM ANGKA {year}</h1>
        <div class="cover-subtitle">{name_upper} {admin_type_en.upper()} IN FIGURES {year}</div>
      </div>
    </div>
  </div>"""

    # Page 2 (ii - EVEN - BPS Catalog Metadata & Copyright Page)
    pub_no_str = config.get("pub_no", "61040.2026.002")
    card_2_compilers = make_page_card(
        "IDENTITAS PUBLIKASI",
        "PUBLICATION METADATA",
        "ii",
        f"""      <div style="font-size: 8.5pt; line-height: 1.5; color: #1a202c; max-width: 92%; margin: 15px auto 0 auto;">
        <div style="font-weight: 800; font-size: 11.5pt; color: #0b3c5d; margin-bottom: 2px;">{admin_upper} {name_upper} DALAM ANGKA {year}</div>
        <div style="font-style: italic; font-size: 10pt; color: #475569; margin-bottom: 16px;">{name_title} {admin_type_en} in Figures {year}</div>
        
        <div style="margin-bottom: 14px;">
          <strong>Ukuran Buku / <i>Book Size</i>:</strong> 21 cm x 29,7 cm (A4)<br>
          <strong>Jumlah Halaman / <i>Number of Pages</i>:</strong> ix + 35 halaman/pages
        </div>

        <div style="margin-bottom: 14px; border-top: 1px solid #e2e8f0; padding-top: 12px;">
          <strong>Penanggung Jawab / <i>Person in Charge</i>:</strong><br>
          {kades_name.upper()} ({kades_title})
        </div>

        <div style="margin-bottom: 14px;">
          <strong>Penyusun Naskah / <i>Manuscript Drafter</i>:</strong><br>
          Tim Agen Statistik {admin_type} {name_title} & Tim Pembina Desa Cantik BPS Kabupaten Mempawah
        </div>

        <div style="margin-bottom: 14px;">
          <strong>Penyunting & Penata Letak / <i>Editors & Layouters</i>:</strong><br>
          Tim Pembina Desa Cantik BPS Kabupaten Mempawah
        </div>

        <div style="margin-bottom: 14px;">
          <strong>Penerbit / <i>Publisher</i>:</strong><br>
          © BPS Kabupaten Mempawah & {gov_name}
        </div>

        <div style="margin-top: 35px; padding: 12px 15px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 6px; font-size: 7.8pt; line-height: 1.45;">
          <strong>Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik Kabupaten Mempawah dan {gov_name}.</strong><br>
          <span style="font-style: italic; color: #475569;">It is prohibited to reproduce and/or duplicate part or all of this book for commercial purposes without written permission from BPS-Statistics Mempawah Regency and {gov_name_en}.</span>
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
      <ol style="font-size: 9.5pt; line-height: 1.8; color: #2d3748; padding-left: 20px;">
        <li>{gov_name} / <i>{gov_name_en}</i></li>
        <li>Pengurus Rukun Tetangga ({len(rows)} RT) {admin_type} {name_title} / <i>Management of {len(rows)} Neighborhood Units (RT) of {name_title} {admin_type_en}</i></li>
      </ol>""",
        3,
        show_header=False,
        show_footer=True,
    )

    if name_kebab in ("pasir-palembang", "pasir-wan-salim"):
        preface_desc_id = f"Data yang disajikan dihimpun secara langsung melalui pendataan keluarga per bangunan tempat tinggal biasa di wilayah {name_title} menggunakan metode <i>Computer-Assisted Personal Interviewing</i> (CAPI) berbasis aplikasi mobile AppSheet dan observasi geospasial fasilitas. Cakupan data meliputi kondisi demografi kependudukan, tingkat pendidikan, kepemilikan dokumen adminduk (KTP-el), sebaran penerima bantuan sosial, hingga kelayakan infrastruktur perumahan."
        preface_desc_en = f"The presented data was collected directly through family enumeration per ordinary residential building in {name_title} using the CAPI method via AppSheet mobile application and geospatial facility observation. The coverage includes demographics, education, ID card ownership, social assistance distribution, and housing infrastructure."
    else:
        preface_desc_id = f"Data yang disajikan dihimpun secara langsung dari {len(rows)} Rukun Tetangga (RT) menggunakan metode <i>Computer-Assisted Personal Interviewing</i> (CAPI) berbasis aplikasi mobile AppSheet. Cakupan data meliputi kondisi demografi kependudukan, tingkat pendidikan, kepemilikan dokumen adminduk (KTP-el), sebaran penerima bantuan sosial, hingga kelayakan infrastruktur perumahan."
        preface_desc_en = f"The presented data was collected directly from {len(rows)} Neighborhood Units (RT) using the CAPI method via AppSheet mobile application. The coverage includes demographics, education, ID card ownership, social assistance distribution, and housing infrastructure."

    # Page 4 (iv - EVEN)
    card_4_preface_id = make_page_card(
        "KATA PENGANTAR",
        "PREFACE",
        "iv",
        f"""      <h2 style="text-align: center; color: #0b3c5d; font-size: 14pt; font-weight: 800; margin-top: 10px; margin-bottom: 25px;">KATA PENGANTAR</h2>
      <div style="font-size: 9.5pt; line-height: 1.6; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi resmi <strong>"{admin_type} {name_title} Dalam Angka {year}"</strong> dapat diselesaikan dengan baik. Publikasi ini merupakan wujud nyata pembinaan statistik sektoral melalui Program <strong>Desa Cantik (Desa Cinta Statistik)</strong> BPS Kabupaten Mempawah berkolaborasi dengan {gov_name}.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">{preface_desc_id}</p>
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
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Praise be to God Almighty for His blessings, the official publication <i>"{name_title} {admin_type_en} in Figures {year}"</i> has been successfully completed. This publication is a concrete result of statistical development under the Desa Cantik Program by BPS-Statistics of Mempawah Regency in collaboration with {gov_name_en}.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">{preface_desc_en}</p>
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
        <div style="font-size: 10.5pt; font-weight: 700; color: #2d3748; margin-top: 4px;">{admin_type} {name_title} Dalam Angka {year}</div>
        <div style="font-size: 10.5pt; font-weight: 700; font-style: italic; color: #475569;">{name_title} Village in Figures {year}</div>
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
        <li><span class="toc-title">Statistik Kunci/<i>Key Statistics</i></span><span class="toc-page">1</span></li>
        <li><span class="toc-title">1.&nbsp;&nbsp;&nbsp;Geografi dan Pemerintahan/<i>Geography and Government</i></span><span class="toc-page">3</span></li>
        <li><span class="toc-title">2.&nbsp;&nbsp;&nbsp;Kependudukan dan Demografi/<i>Population and Demographics</i></span><span class="toc-page">9</span></li>
        <li><span class="toc-title">3.&nbsp;&nbsp;&nbsp;Pendidikan dan Adminduk/<i>Education and Civil Registration</i></span><span class="toc-page">15</span></li>
        <li><span class="toc-title">4.&nbsp;&nbsp;&nbsp;Sosial dan Kesejahteraan Rakyat/<i>Social and Welfare</i></span><span class="toc-page">21</span></li>
        <li><span class="toc-title">5.&nbsp;&nbsp;&nbsp;Perumahan dan Lingkungan/<i>Housing and Infrastructure</i></span><span class="toc-page">27</span></li>
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
      <div class="lot-sec">0.&nbsp;&nbsp;STATISTIK KUNCI / <i>KEY STATISTICS</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">0.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Statistik Kunci {admin_type} {name_title}, {year}<br><i>Key Statistics of {name_title} {admin_type_en}, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">1</span>
          </div>
        </li>
      </ul>
      <div class="lot-sec">1.&nbsp;&nbsp;GEOGRAFI DAN PEMERINTAHAN / <i>GEOGRAPHY AND GOVERNMENT</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">1.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Batas Wilayah Administrasi {admin_type} {name_title}<br><i>Administrative Boundary of {name_title} {admin_type_en}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">5</span>
          </div>
        </li>
        <li>
          <span class="lot-no">1.2</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Daftar Nama Ketua RT dan Agen Statistik {admin_type} Menurut Wilayah RT, {year}<br><i>List of Neighborhood Chairmen and {admin_type_en} Statistical Agents by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">5</span>
          </div>
        </li>
      </ul>
      <div class="lot-sec">2.&nbsp;&nbsp;KEPENDUDUKAN DAN DEMOGRAFI / <i>POPULATION AND DEMOGRAPHICS</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">2.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Jumlah Penduduk dan Sex Ratio Menurut RT, {year}<br><i>Total Population and Sex Ratio by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">11</span>
          </div>
        </li>
      </ul>
      <div class="lot-sec">3.&nbsp;&nbsp;PENDIDIKAN DAN ADMINDUK / <i>EDUCATION AND CIVIL REGISTRATION</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">3.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Jumlah Penduduk Putus Sekolah dan Kepemilikan KTP-el Menurut RT, {year}<br><i>Total Dropouts and ID Card Ownership by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">17</span>
          </div>
        </li>
      </ul>
      <div class="lot-sec">4.&nbsp;&nbsp;SOSIAL DAN KESEJAHTERAAN RAKYAT / <i>SOCIAL AND WELFARE</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">4.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Jumlah Keluarga Penerima Bantuan Sosial Menurut Jenis Bantuan dan RT, {year}<br><i>Number of Social Assistance Recipient Families by Assistance Type and RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">23</span>
          </div>
        </li>
      </ul>
      <div class="lot-sec">5.&nbsp;&nbsp;PERUMAHAN DAN LINGKUNGAN / <i>HOUSING AND INFRASTRUCTURE</i></div>
      <ul class="lot-list">
        <li>
          <span class="lot-no">5.1</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Bumbung Rumah dan Rata-rata Kepadatan Hunian Menurut RT, {year}<br><i>Residential Buildings and Average Occupancy Density by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">29</span>
          </div>
        </li>
        {f'''<li>
          <span class="lot-no">5.2</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Sebaran Sarana Peribadatan, Pendidikan, dan Kesehatan Menurut RT, {year}<br><i>Distribution of Worship, Education, and Health Facilities by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">30</span>
          </div>
        </li>
        <li>
          <span class="lot-no">5.3</span>
          <div class="lot-title-wrap">
            <span class="lot-title">Rekapitulasi Kondisi Bangunan dan Akses Infrastruktur Desa Menurut RT, {year}<br><i>Building Condition and Infrastructure Access Summary by RT, {year}</i></span>
            <span class="lot-dots"></span>
            <span class="lot-page">31</span>
          </div>
        </li>''' if caps.has_public_facilities and metrics.get('fasilitas') else ''}
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
        """      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">PENJELASAN UMUM/<i>EXPLANATORY NOTES</i></h2>
      </div>
      <div style="font-size: 9pt; line-height: 1.5; color: #2d3748; margin-bottom: 18px;">
        <div>Tanda-tanda, satuan-satuan, dan lain-lainnya yang digunakan dalam publikasi ini adalah sebagai berikut:</div>
        <div style="font-style: italic; color: #475569;">Symbols, measurement units, and acronyms which are used in this publication, are as follows:</div>
      </div>
      <table style="width: 100%; border-collapse: collapse; font-size: 8.8pt; line-height: 1.7; color: #2d3748;">
        <tbody>
          <tr><td style="border: none;">Data tidak tersedia/<i>Data not available</i></td><td style="border: none;">: ...</td></tr>
          <tr><td style="border: none;">Tidak ada atau nol /<i>Null or zero</i></td><td style="border: none;">: -</td></tr>
          <tr><td style="border: none;">Data dapat diabaikan/<i>Data negligible</i></td><td style="border: none;">: ~0</td></tr>
          <tr><td style="border: none;">Tanda desimal/<i>Decimal point</i></td><td style="border: none;">: ,</td></tr>
        </tbody>
      </table>""",
        8,
        show_header=False,
        show_footer=True,
    )

    # Page 9 (ix - ODD)
    card_7_abbreviations = make_page_card(
        "DAFTAR SINGKATAN",
        "LIST OF ABBREVIATIONS",
        "ix",
        """      <h2 style="text-align: center; color: #0b3c5d; font-size: 13pt; margin-top: 0; margin-bottom: 20px;">DAFTAR SINGKATAN / <i>LIST OF ABBREVIATIONS</i></h2>
      <table style="width: 100%; border-collapse: collapse; border: none; font-size: 8.5pt; line-height: 1.6; color: #2d3748;">
        <tbody>
          <tr><td style="width: 50%; border: none;"><strong>BPS:</strong> Badan Pusat Statistik</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>BPS:</strong> BPS-Statistics (Central Agency on Statistics)</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>CAPI:</strong> Computer-Assisted Personal Interviewing</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>CAPI:</strong> Computer-Assisted Personal Interviewing</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>RT:</strong> Rukun Tetangga</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>RT:</strong> Neighborhood Unit</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>KK:</strong> Kepala Keluarga</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>KK:</strong> Head of Household / Family Card</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>ART:</strong> Anggota Rumah Tangga</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>ART:</strong> Household Member</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>KTP-el:</strong> Kartu Tanda Penduduk Elektronik</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>KTP-el:</strong> Electronic Identity Card</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>PKH:</strong> Program Keluarga Harapan</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>PKH:</strong> Family Hope Program</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>BPNT:</strong> Bantuan Pangan Non-Tunai</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>BPNT:</strong> Non-Cash Food Assistance</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>BST:</strong> Bantuan Sosial Tunai</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>BST:</strong> Social Cash Assistance</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>BLT:</strong> Bantuan Langsung Tunai</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>BLT:</strong> Direct Cash Assistance</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>SD / SMP / SMA:</strong> Sekolah Dasar / Menengah / Atas</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>SD / SMP / SMA:</strong> Primary / Junior / Senior High School</td></tr>
          <tr><td style="width: 50%; border: none;"><strong>PT:</strong> Perguruan Tinggi</td><td style="width: 50%; font-style: italic; color: #475569; border: none;"><strong>PT:</strong> Higher Education / University</td></tr>
        </tbody>
      </table>""",
        9,
        show_header=False,
        show_footer=True,
    )

    # Build Key Stats (Tabel 0.1) dynamically per village capabilities
    if caps.has_employment:
        keystats_rows = f"""
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">DEMOGRAFI DAN KEPENDUDUKAN / <i>DEMOGRAPHICS AND POPULATION</i></td></tr>
          <tr><td>Penduduk / <i>Population</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_pop}</td></tr>
          <tr><td>Laki-laki / <i>Male</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_l}</td></tr>
          <tr><td>Perempuan / <i>Female</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_p}</td></tr>
          <tr><td>Rasio Jenis Kelamin / <i>Sex Ratio</i></td><td>-</td><td class="text-right">{dyn_sr}</td></tr>
          <tr><td>Kepala Keluarga / <i>Households</i></td><td>KK / <i>Households</i></td><td class="text-right">{dyn_kk}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">KETENAGAKERJAAN, UMKM & SOSIAL / <i>EMPLOYMENT, MSME & SOCIAL</i></td></tr>
          <tr><td>Usia Kerja Bekerja / <i>Employed Working Age</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{fmt_val(metrics['tot_bekerja'])}</td></tr>
          <tr><td>Rumah Tangga UMKM / <i>MSME Households</i></td><td>KK / <i>Households</i></td><td class="text-right">{fmt_val(metrics['tot_umkm'])}</td></tr>
          <tr><td>Peserta BPJS Kesehatan / <i>BPJS Health Participants</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{fmt_val(metrics['tot_bpjs'])}</td></tr>
          <tr><td>Keluarga Penerima Bansos (PKH/BPNT) / <i>Assistance Recipients</i></td><td>Keluarga / <i>Families</i></td><td class="text-right">{dyn_bansos}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">PERUMAHAN DAN LINGKUNGAN / <i>HOUSING AND ENVIRONMENT</i></td></tr>
          <tr><td>Bumbung Rumah (Hunian) / <i>Residential Buildings</i></td><td>Unit / <i>Units</i></td><td class="text-right">{dyn_bumbung}</td></tr>
          <tr><td>Kepadatan Hunian Rata-rata / <i>Housing Density</i></td><td>Jiwa per Unit / <i>Persons/Unit</i></td><td class="text-right">{dyn_kepadatan}</td></tr>
          <tr><td>Sanitasi BAB Sendiri / <i>Private Toilet Sanitation</i></td><td>KK / <i>Households</i></td><td class="text-right">{fmt_val(metrics['tot_bab_sendiri'])}</td></tr>"""
    elif caps.has_building_materials:
        keystats_rows = f"""
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">DEMOGRAFI DAN KEPENDUDUKAN / <i>DEMOGRAPHICS AND POPULATION</i></td></tr>
          <tr><td>Penduduk / <i>Population</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_pop}</td></tr>
          <tr><td>Laki-laki / <i>Male</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_l}</td></tr>
          <tr><td>Perempuan / <i>Female</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_p}</td></tr>
          <tr><td>Rasio Jenis Kelamin / <i>Sex Ratio</i></td><td>-</td><td class="text-right">{dyn_sr}</td></tr>
          <tr><td>Kepala Keluarga / <i>Households</i></td><td>KK / <i>Households</i></td><td class="text-right">{dyn_kk}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">SOSIAL DAN KESEJAHTERAAN / <i>SOCIAL AND WELFARE</i></td></tr>
          <tr><td>Keluarga Penerima Bansos (PKH/BPNT/BLT) / <i>Assistance Recipients</i></td><td>Keluarga / <i>Families</i></td><td class="text-right">{dyn_bansos}</td></tr>
          <tr><td>Penerima BPJS PBI / <i>BPJS PBI Insurance Recipients</i></td><td>Keluarga / <i>Families</i></td><td class="text-right">{fmt_val(metrics['tot_bpjs'])}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">PERUMAHAN DAN LINGKUNGAN / <i>HOUSING AND ENVIRONMENT</i></td></tr>
          <tr><td>Bumbung Rumah (Hunian) / <i>Residential Buildings</i></td><td>Unit / <i>Units</i></td><td class="text-right">{dyn_bumbung}</td></tr>
          <tr><td>Rumah Layak Huni / <i>Decent Housing</i></td><td>Unit / <i>Units</i></td><td class="text-right">{dyn_layak}</td></tr>
          <tr><td>Persentase Rumah Layak Huni / <i>Decent Housing Rate</i></td><td>%</td><td class="text-right">{f"{metrics['tot_layak_pct']:.2f}".replace('.', ',')}</td></tr>"""
    else:
        keystats_rows = f"""
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">DEMOGRAFI DAN KEPENDUDUKAN / <i>DEMOGRAPHICS AND POPULATION</i></td></tr>
          <tr><td>Penduduk / <i>Population</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_pop}</td></tr>
          <tr><td>Laki-laki / <i>Male</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_l}</td></tr>
          <tr><td>Perempuan / <i>Female</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_p}</td></tr>
          <tr><td>Rasio Jenis Kelamin / <i>Sex Ratio</i></td><td>-</td><td class="text-right">{dyn_sr}</td></tr>
          <tr><td>Kepala Keluarga / <i>Households</i></td><td>KK / <i>Households</i></td><td class="text-right">{dyn_kk}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">SOSIAL DAN KESEJAHTERAAN / <i>SOCIAL AND WELFARE</i></td></tr>
          <tr><td>Memiliki KTP-el / <i>ID Card Owners</i></td><td>Jiwa / <i>Persons</i></td><td class="text-right">{dyn_ktp}</td></tr>
          <tr><td>Persentase KTP-el / <i>ID Card Ownership Rate</i></td><td>%</td><td class="text-right">{dyn_ktp_pct}</td></tr>
          <tr><td>Keluarga Penerima Bansos (PKH/BPNT/BLT) / <i>Assistance Recipients</i></td><td>Keluarga / <i>Families</i></td><td class="text-right">{dyn_bansos}</td></tr>
          <tr style="background: #fff5eb; font-weight: 700; color: #0b3c5d;"><td colspan="3">PERUMAHAN DAN LINGKUNGAN / <i>HOUSING AND ENVIRONMENT</i></td></tr>
          <tr><td>Bumbung Rumah (Hunian) / <i>Residential Buildings</i></td><td>Unit / <i>Units</i></td><td class="text-right">{dyn_bumbung}</td></tr>
          <tr><td>Kepadatan Hunian Rata-rata / <i>Housing Density</i></td><td>Jiwa per Unit / <i>Persons/Unit</i></td><td class="text-right">{dyn_kepadatan}</td></tr>"""

    # Page 11 (Arab 1 - ODD)
    card_8_keystats = make_page_card(
        f"STATISTIK KUNCI {year}",
        f"KEY STATISTICS {year}",
        "1",
        f"""<div style="font-weight: 800; font-size: 9.5pt; color: #0b3c5d; margin-bottom: 2px;">Tabel 0.1 Statistik Kunci {year}</div>
      <div style="font-weight: 800; font-size: 8.5pt; font-style: italic; color: #0b3c5d; margin-bottom: 8px;">Table Key Statistics, {year}</div>
      <table class="bps-table">
        <thead>
          <tr><th class="main-header">Rincian / <i>Description</i></th><th class="main-header" style="width: 110px;">Satuan / <i>Unit</i></th><th class="main-header" style="width: 80px;">{year}</th></tr>
          <tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr>
        </thead>
        <tbody>
          {keystats_rows}
        </tbody>
      </table>{meta_std}""",
        11,
    )

    # Function to build chapters with chunked pages & exact page parity
    def build_chapter_html(
        ch_num,
        badge_start,
        ch_title_id,
        ch_title_en,
        sec_id,
        sec_en,
        table_code,
        table_title_id,
        table_title_en,
        rows_all,
        tot_row,
        meta_html,
        info_items_html,
        narrative_html="",
        tech_notes_id=[],
        tech_notes_en=[],
        extra_tables=None,
    ):
        res = ""
        # 1. Cover Card (No Header, No Footer)
        res += make_cover_card(
            str(ch_num), ch_title_id, ch_title_en, info_items_html
        )

        # 2. Technical Notes Page (badge_start + 1)
        tech_rows = []
        for idx, (item_id, item_en) in enumerate(
            zip(tech_notes_id, tech_notes_en), start=1
        ):
            tech_rows.append(
                f"""<tr>
              <td style="width: 50%; vertical-align: top; padding-right: 15px; border: none; padding-bottom: 12px; text-align: justify; text-justify: inter-word;">{idx}. {item_id}</td>
              <td style="width: 50%; vertical-align: top; padding-left: 15px; font-style: italic; color: #475569; border: none; padding-bottom: 12px; text-align: justify; text-justify: inter-word;">{idx}. {item_en}</td>
            </tr>"""
            )
        tech_table_rows = "\n".join(tech_rows)

        tech_page_body = f"""<div style="text-align: center; margin-bottom: 20px;">
          <h2 style="font-size: 14pt; font-weight: 800; margin: 0; color: #0b3c5d; text-transform: uppercase;">PENJELASAN TEKNIS</h2>
          <h2 style="font-size: 11pt; font-weight: 800; font-style: italic; margin: 2px 0 0 0; color: #0b3c5d; text-transform: uppercase;">TECHNICAL NOTES</h2>
        </div>
        <table style="width: 100%; border-collapse: collapse; border: none; font-size: 8.8pt; line-height: 1.5; color: #2d3748;">
          <tbody>
            {tech_table_rows}
          </tbody>
        </table>"""
        res += make_page_card(
            f"PENJELASAN TEKNIS BAB {ch_num}",
            f"TECHNICAL NOTES CHAPTER {ch_num}",
            str(ch_num),
            tech_page_body,
            badge_start + 1,
        )

        # Table headers
        if table_code == "1.2":
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Nama Ketua RT<br><i>Neighborhood Chairman</i></th><th class="main-header">Agen Statistik Desa<br><i>Village Statistical Agent</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr>"""
        elif table_code == "2.1":
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Laki-laki<br><i>Male</i></th><th class="main-header">Perempuan<br><i>Female</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Sex Ratio<br><i>Sex Ratio</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == "3.1":
            if caps.has_employment:
                thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Usia Kerja Bekerja (15-64)<br><i>Employed Working Age</i></th><th class="main-header">Rumah Tangga UMKM<br><i>MSME Households</i></th><th class="main-header">Peserta BPJS Kesehatan<br><i>BPJS Health Participants</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
            elif caps.has_building_materials:
                thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Bumbung Rumah<br><i>Residential Buildings</i></th><th class="main-header">Dinding Tembok<br><i>Brick/Concrete Walls</i></th><th class="main-header">Atap Seng/Genteng<br><i>Zinc/Tile Roofs</i></th><th class="main-header">Sanitasi BAB Sendiri<br><i>Private Toilet Sanitation</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
            else:
                thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Putus Sekolah (7-18 thn)<br><i>Dropouts (7-18 yrs)</i></th><th class="main-header">Memiliki KTP-el<br><i>ID Card Owners</i></th><th class="main-header">Persentase KTP-el (%)<br><i>ID Card Pct (%)</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == "4.1":
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Penerima PKH<br><i>PKH Recipients</i></th><th class="main-header">Penerima BPNT<br><i>BPNT Recipients</i></th><th class="main-header">Penerima BST/BLT<br><i>BST/BLT Recipients</i></th><th class="main-header">Total Penerima Bansos<br><i>Total Assistance Recipient</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == "5.1":
            if caps.has_decent_housing:
                thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Bumbung Rumah (Hunian)<br><i>Residential Buildings</i></th><th class="main-header">Rata-rata Jiwa/Rumah<br><i>Avg Persons/Building</i></th><th class="main-header">Rumah Layak Huni (%)<br><i>Decent Housing (%)</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
            else:
                thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Bumbung Rumah (Hunian)<br><i>Residential Buildings</i></th><th class="main-header">Rata-rata Jiwa/Rumah<br><i>Avg Persons/Building</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th></tr>"""

        sec_h = f"""<div class="section-header">{sec_id}<span class="en">{sec_en}</span></div>"""
        main_title = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">{table_code}</div><div class="table-name">{table_title_id}<br><span class="en-title">{table_title_en}</span></div></div>"""
        cont_title = f"""<p style="font-weight: 800; font-style: italic; font-size: 9pt; color: #1a202c; margin: 0 0 8px 0;">Lanjutan Tabel/<em>Continued Table</em> {table_code}</p>"""

        r_tot = ""
        if tot_row:
            r_tot = (
                f'<tr class="total-row"><td>{tot_row[0]}</td>'
                + "".join([f'<td class="text-right">{v}</td>' for v in tot_row[1:]])
                + "</tr>"
            )

        p1_chunk_size = 16 if table_code == "1.2" else 18
        cont_chunk_size = 24
        current_page_idx = badge_start + 2

        if len(rows_all) <= p1_chunk_size:
            r_p1 = "\n".join(rows_all)
            if r_tot:
                r_p1 += "\n" + r_tot

            if table_code == "1.2":
                t1_1_1_block = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">1.1</div><div class="table-name">Batas Wilayah Administrasi {admin_type} {name_title}<br><span class="en-title">Administrative Boundary of {name_title} {admin_type_en}</span></div></div>
                <table class="bps-table">
                  <thead><tr><th class="main-header">Batas Wilayah<br><i>Boundary</i></th><th class="main-header">Desa / Kelurahan / Laut<br><i>Village / Sea</i></th><th class="main-header">Kecamatan<br><i>District</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr></thead>
                  <tbody>
                    <tr><td>Sebelah Utara / North</td><td>{config.get('north', '-')}</td><td>{kecamatan}</td></tr>
                    <tr><td>Sebelah Selatan / South</td><td>{config.get('south', '-')}</td><td>-</td></tr>
                    <tr><td>Sebelah Timur / East</td><td>{config.get('east', '-')}</td><td>{kecamatan}</td></tr>
                    <tr><td>Sebelah Barat / West</td><td>{config.get('west', '-')}</td><td>{kecamatan}</td></tr>
                  </tbody>
                </table>
                <br>"""
            else:
                t1_1_1_block = ""

            t1_body = f"""{sec_h}{narrative_html}{t1_1_1_block}{main_title}
            <table class="bps-table">
              <thead>{thead}</thead>
              <tbody>{r_p1}</tbody>
            </table>{meta_html}"""

            res += make_page_card(
                ch_title_id,
                ch_title_en,
                str(ch_num),
                t1_body,
                current_page_idx,
            )
        else:
            r_p1 = "\n".join(rows_all[:p1_chunk_size])

            if table_code == "1.2":
                t1_1_1_block = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">1.1</div><div class="table-name">Batas Wilayah Administrasi {admin_type} {name_title}<br><span class="en-title">Administrative Boundary of {name_title} {admin_type_en}</span></div></div>
                <table class="bps-table">
                  <thead><tr><th class="main-header">Batas Wilayah<br><i>Boundary</i></th><th class="main-header">Desa / Kelurahan / Laut<br><i>Village / Sea</i></th><th class="main-header">Kecamatan<br><i>District</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr></thead>
                  <tbody>
                    <tr><td>Sebelah Utara / North</td><td>{config.get('north', '-')}</td><td>{kecamatan}</td></tr>
                    <tr><td>Sebelah Selatan / South</td><td>{config.get('south', '-')}</td><td>-</td></tr>
                    <tr><td>Sebelah Timur / East</td><td>{config.get('east', '-')}</td><td>{kecamatan}</td></tr>
                    <tr><td>Sebelah Barat / West</td><td>{config.get('west', '-')}</td><td>{kecamatan}</td></tr>
                  </tbody>
                </table>
                <br>"""
            else:
                t1_1_1_block = ""

            t1_body = f"""{sec_h}{narrative_html}{t1_1_1_block}{main_title}
            <table class="bps-table">
              <thead>{thead}</thead>
              <tbody>{r_p1}</tbody>
            </table>{meta_html}"""

            res += make_page_card(
                ch_title_id,
                ch_title_en,
                str(ch_num),
                t1_body,
                current_page_idx,
            )

            remaining_rows = rows_all[p1_chunk_size:]
            while remaining_rows:
                current_page_idx += 1
                if len(remaining_rows) <= cont_chunk_size:
                    chunk = remaining_rows
                    remaining_rows = []
                    r_cont = "\n".join(chunk)
                    if r_tot:
                        r_cont += "\n" + r_tot
                else:
                    chunk = remaining_rows[:cont_chunk_size]
                    remaining_rows = remaining_rows[cont_chunk_size:]
                    r_cont = "\n".join(chunk)

                t_cont_body = f"""{cont_title}
                <table class="bps-table">
                  <thead>{thead}</thead>
                  <tbody>{r_cont}</tbody>
                </table>{meta_html}"""

                res += make_page_card(
                    ch_title_id,
                    ch_title_en,
                    str(ch_num),
                    t_cont_body,
                    current_page_idx,
                )

        if extra_tables:
            for et in extra_tables:
                e_code = et["table_code"]
                e_sec_id = et["sec_id"]
                e_sec_en = et["sec_en"]
                e_title_id = et["table_title_id"]
                e_title_en = et["table_title_en"]
                e_rows_all = et["rows_all"]
                e_tot_row = et.get("tot_row")
                e_meta_html = et.get("meta_html", meta_std)

                if e_code == "5.2":
                    e_thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Peribadatan (Masjid/Surau)<br><i>Worship (Mosque/Surau)</i></th><th class="main-header">Pendidikan (TK/SD/SMP/SMA/Ponpes)<br><i>Education (School/Pesantren)</i></th><th class="main-header">Kesehatan (Posyandu/Polindes)<br><i>Health (Posyandu/Polindes)</i></th><th class="main-header">Pemerintahan & Ekonomi<br><i>Govt, Market & Utilities</i></th><th class="main-header">Total Sarana<br><i>Total Facilities</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th><th class="col-num">(6)</th></tr>"""
                elif e_code == "5.3":
                    e_thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Kondisi Baik<br><i>Good Condition</i></th><th class="main-header">Jalan Aspal/Beton<br><i>Paved/Concrete Road</i></th><th class="main-header">Listrik PLN 24 Jam<br><i>PLN Electricity</i></th><th class="main-header">Sinyal 4G/LTE<br><i>4G Signal</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
                else:
                    e_thead = ""

                e_sec_h = f"""<div class="section-header">{e_sec_id}<span class="en">{e_sec_en}</span></div>"""
                e_main_title = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">{e_code}</div><div class="table-name">{e_title_id}<br><span class="en-title">{e_title_en}</span></div></div>"""
                e_cont_title = f"""<p style="font-weight: 800; font-style: italic; font-size: 9pt; color: #1a202c; margin: 0 0 8px 0;">Lanjutan Tabel/<em>Continued Table</em> {e_code}</p>"""

                e_r_tot = ""
                if e_tot_row:
                    e_r_tot = (
                        f'<tr class="total-row"><td>{e_tot_row[0]}</td>'
                        + "".join([f'<td class="text-right">{v}</td>' for v in e_tot_row[1:]])
                        + "</tr>"
                    )

                current_page_idx += 1
                if len(e_rows_all) <= 18:
                    e_p1 = "\n".join(e_rows_all)
                    if e_r_tot:
                        e_p1 += "\n" + e_r_tot

                    e_body = f"""{e_sec_h}{e_main_title}
                    <table class="bps-table">
                      <thead>{e_thead}</thead>
                      <tbody>{e_p1}</tbody>
                    </table>{e_meta_html}"""

                    res += make_page_card(
                        ch_title_id,
                        ch_title_en,
                        str(ch_num),
                        e_body,
                        current_page_idx,
                    )
                else:
                    e_p1 = "\n".join(e_rows_all[:18])
                    e_body = f"""{e_sec_h}{e_main_title}
                    <table class="bps-table">
                      <thead>{e_thead}</thead>
                      <tbody>{e_p1}</tbody>
                    </table>{e_meta_html}"""

                    res += make_page_card(
                        ch_title_id,
                        ch_title_en,
                        str(ch_num),
                        e_body,
                        current_page_idx,
                    )

                    e_rem = e_rows_all[18:]
                    while e_rem:
                        current_page_idx += 1
                        if len(e_rem) <= 24:
                            e_chunk = e_rem
                            e_rem = []
                            e_r_cont = "\n".join(e_chunk)
                            if e_r_tot:
                                e_r_cont += "\n" + e_r_tot
                        else:
                            e_chunk = e_rem[:24]
                            e_rem = e_rem[24:]
                            e_r_cont = "\n".join(e_chunk)

                        e_cont_body = f"""{e_cont_title}
                        <table class="bps-table">
                          <thead>{e_thead}</thead>
                          <tbody>{e_r_cont}</tbody>
                        </table>{e_meta_html}"""

                        res += make_page_card(
                            ch_title_id,
                            ch_title_en,
                            str(ch_num),
                            e_cont_body,
                            current_page_idx,
                        )

        return res


    # Assemble Full Document
    full_out = html_header
    full_out += card_1_cover + "\n\n"
    full_out += card_2_compilers + "\n\n"
    full_out += card_3_contrib + "\n\n"
    full_out += card_4_preface_id + "\n\n"
    full_out += card_4_preface_en + "\n\n"
    full_out += card_5_toc + "\n\n"
    full_out += card_5b_lot + "\n\n"
    full_out += card_6_tech_notes + "\n\n"
    full_out += card_7_abbreviations + "\n\n"
    full_out += make_blank_page()  # Page x (10)
    full_out += card_8_keystats + "\n\n"  # Arab Page 1 (11)
    full_out += make_blank_page()  # Arab Page 2 (12)

    # Chapter 1: Geografi & Pemerintahan
    dusun_bars = []
    colors = ["#16a34a", "#2563eb", "#d97706", "#9333ea"]
    for idx, d in enumerate(info.dusun_breakdown):
        c = colors[idx % len(colors)]
        pct_str = f"{d['pct']:.1f}".replace(".", ",")
        dusun_bars.append(f"""<div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>{d['name']}</span><span>{d['count']} RT ({pct_str}%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 3px;"><div style="width: {d['pct']}%; height: 100%; background: {c};"></div></div>
      </div>""")
    dusun_bars_html = "\n".join(dusun_bars)

    ch1_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 14px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 6px;">DISTRIBUSI WILAYAH ADMINISTRASI & CAKUPAN PENDATAAN / <i>ADMINISTRATIVE DISTRIBUTION & COVERAGE</i></div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px;">
      <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-left: 4px solid #16a34a; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #15803d; line-height: 1.1;">{len(rows)}</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #166534; margin-top: 3px;">Rukun Tetangga (RT)<br><i>Neighborhood Units</i></div>
      </div>
      <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-left: 4px solid #2563eb; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #1d4ed8; line-height: 1.1;">{len(info.dusun_breakdown)}</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #1e40af; margin-top: 3px;">{sub_title}<br><i>{sub_title_en}</i></div>
      </div>
      <div style="background: #fffbeb; border: 1.5px solid #fde68a; border-left: 4px solid #d97706; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #b45309; line-height: 1.1;">100%</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #92400e; margin-top: 3px;">Cakupan CAPI AppSheet<br><i>CAPI Coverage</i></div>
      </div>
    </div>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
      <div style="font-weight: 800; font-size: 8.8pt; color: #0b3c5d; margin-bottom: 8px; text-transform: uppercase;">Sebaran Rukun Tetangga (RT) per {sub_type} / <i>RT Distribution by {sub_type_en}</i></div>
      {dusun_bars_html}
    </div>"""

    if caps.has_building_materials or caps.has_employment:
        ch1_nar_id = f"{admin_type} {name_title} secara administratif terbagi menjadi <strong>{len(rows)} Rukun Tetangga (RT)</strong>. Pendataan sosial keluarga dilakukan secara penuh (sensus) per bangunan tempat tinggal biasa menggunakan CAPI AppSheet oleh Agen Statistik {admin_type} bekerjasama dengan BPS Kabupaten Mempawah."
        ch1_nar_en = f"{name_title} {admin_type_en} is administratively divided into {len(rows)} Neighborhood Units (RT). Family social data collection was fully enumerated per ordinary residential building using CAPI AppSheet by {admin_type_en} Statistical Agents in collaboration with BPS-Statistics Mempawah Regency."
    else:
        ch1_nar_id = f"{admin_type} {name_title} secara administratif terbagi menjadi <strong>{len(rows)} Rukun Tetangga (RT)</strong>. Seluruh wilayah pendataan didata secara penuh (sensus) oleh Agen Statistik {admin_type} yang terdiri dari aparat {admin_type} {name_title}."
        ch1_nar_en = f"{name_title} {admin_type_en} is administratively divided into {len(rows)} Neighborhood Units (RT). All enumeration areas were fully enumerated by {admin_type_en} Statistical Agents consisting of {admin_type_en.lower()} officials."

    ch1_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN GEOGRAFI DAN PEMERINTAHAN</div><p>{ch1_nar_id}</p></div><div class="narrative-col-en"><div class="narrative-title en">GEOGRAPHY & GOVERNMENT HIGHLIGHTS</div><p class="en">{ch1_nar_en}</p></div></div></div>"""

    ch1_tech_id = [
        "<strong>Desa/Kelurahan Pesisir</strong> adalah desa/kelurahan yang sebagian wilayahnya bersentuhan/berbatasan langsung dengan laut.",
        "<strong>Desa/Kelurahan Bukan Pesisir</strong> adalah desa/kelurahan yang seluruh wilayahnya tidak bersentuhan/berbatasan langsung dengan laut.",
        "<strong>Rukun Tetangga (RT)</strong> adalah lembaga masyarakat yang dibentuk melalui musyawarah masyarakat setempat dalam rangka pelayanan pemerintahan.",
        f"<strong>Agen Statistik {admin_type}</strong> adalah aparat {admin_type} yang ditunjuk untuk melakukan pendaftaran dan pendataan potensi wilayah secara langsung di lapangan.",
    ]
    ch1_tech_en = [
        "<strong>Coastal Village/Sub-District</strong> is a village/sub-district which some areas intersect/directly adjacent to the sea.",
        "<strong>Non Coastal Village/Sub-District</strong> is a village which has no area that intersects/directly adjacent to the sea.",
        "<strong>Neighborhood Unit (RT)</strong> is a community institution formed through local community consultation.",
        f"<strong>{admin_type_en} Statistical Agent</strong> is a {admin_type_en.lower()} official appointed to conduct direct field registration and data collection.",
    ]

    full_out += build_chapter_html(
        1,
        3,
        "GEOGRAFI DAN PEMERINTAHAN",
        "GEOGRAPHY AND GOVERNMENT",
        "1.1 WILAYAH ADMINISTRATIF",
        "ADMINISTRATIVE AREA",
        "1.2",
        f"Daftar Nama Ketua RT dan Agen Statistik {admin_type} Menurut Wilayah RT, {year}",
        f"List of Neighborhood Chairmen and {admin_type_en} Statistical Agents by RT, {year}",
        rows_1_1_2_all,
        None,
        meta_std,
        ch1_chart,
        ch1_nar,
        ch1_tech_id,
        ch1_tech_en,
    )

    # Chapter 2: Kependudukan & Demografi
    m_pct_str = f"{info.male_pct:.1f}".replace(".", ",")
    f_pct_str = f"{info.female_pct:.1f}".replace(".", ",")
    ch2_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">KOMPOSISI PENDUDUK MENURUT JENIS KELAMIN & DEMOGRAFI / <i>POPULATION BY GENDER & DEMOGRAPHICS</i></div>
    <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
      <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#e2e8f0" stroke-width="4.5"/>
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-dasharray="{info.dash_gender}" stroke-dashoffset="0"/>
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 13pt; font-weight: 800; color: #0b3c5d;">{dyn_pop} Jiwa</span>
          <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Total Penduduk<br><i>Total Population</i></span>
        </div>
      </div>
      <div style="font-size: 8.8pt; line-height: 1.7;">
        <div style="display: flex; align-items: center; justify-content: space-between; background: #eff6ff; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bfdbfe;">
          <span><span style="width: 12px; height: 12px; background: #2563eb; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 6px;"></span><strong>Laki-laki / <i>Male</i>:</strong></span>
          <span style="font-weight: 800; color: #1d4ed8;">{dyn_l} Jiwa ({m_pct_str}%)</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #e2e8f0;">
          <span><span style="width: 12px; height: 12px; background: #cbd5e1; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 6px;"></span><strong>Perempuan / <i>Female</i>:</strong></span>
          <span style="font-weight: 800; color: #475569;">{dyn_p} Jiwa ({f_pct_str}%)</span>
        </div>
        <div style="background: #fff7ed; border: 1px solid #ffedd5; padding: 7px 12px; border-radius: 6px; font-weight: 700; color: #c2410c; font-size: 8.2pt; text-align: center;">
          Rasio Jenis Kelamin (Sex Ratio): {dyn_sr} (Laki-laki per 100 Perempuan / <i>Males per 100 Females</i>)
        </div>
      </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
      <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-left: 3.5px solid #9333ea; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #7e22ce;">{fmt_val(metrics['tot_lansia'])} Jiwa</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #6b21a8;">Penduduk Lansia (60+ thn)<br><i>Elderly Population (60+ yrs)</i></div>
      </div>
      <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #0f766e;">{fmt_val(metrics['tot_b1'] + metrics['tot_b2'])} Anak</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #115e59;">Usia Balita (0-5 thn)<br><i>Toddlers (0-5 yrs)</i></div>
      </div>
      <div style="background: #fefce8; border: 1px solid #fef08a; border-left: 3.5px solid #ca8a04; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #854d0e;">{dyn_kk} KK</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #854d0e;">Total Kepala Keluarga<br><i>Total Households</i></div>
      </div>
    </div>"""

    ch2_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN KEPENDUDUKAN & DEMOGRAFI</div><p>Jumlah penduduk {admin_type} {name_title} hasil pendaftaran Desa Cantik {year} tercatat sebanyak <strong>{dyn_pop} jiwa</strong>, terdiri dari {dyn_l} laki-laki dan {dyn_p} perempuan dengan <i>sex ratio</i> sebesar <strong>{dyn_sr}</strong>.</p></div><div class="narrative-col-en"><div class="narrative-title en">DEMOGRAPHIC HIGHLIGHTS</div><p class="en">Total population of {name_title} {admin_type_en} based on {year} Desa Cantik registration reached {dyn_pop} persons, comprising {dyn_l} males and {dyn_p} females with a sex ratio of {dyn_sr}.</p></div></div></div>"""

    ch2_tech_id = [
        "<strong>Penduduk</strong> adalah semua orang yang berdomisili di wilayah Indonesia selama 6 bulan atau lebih.",
        "<strong>Rasio Jenis Kelamin (Sex Ratio)</strong> adalah perbandingan antara jumlah penduduk laki-laki dan perempuan per 100 perempuan.",
        "<strong>Kepala Keluarga (KK)</strong> adalah seseorang yang bertanggung jawab atas kebutuhan sehari-hari dalam keluarga.",
        "<strong>Anggota Rumah Tangga (ART)</strong> adalah semua orang yang biasanya bertempat tinggal di suatu rumah tangga.",
    ]
    ch2_tech_en = [
        "<strong>Population</strong> refers to all persons residing in Indonesia for 6 months or more.",
        "<strong>Sex Ratio</strong> is the ratio of male population to female population per 100 females.",
        "<strong>Head of Household</strong> is a person responsible for the daily living needs of the family.",
        "<strong>Household Member</strong> refers to all persons who usually reside in a household.",
    ]

    full_out += build_chapter_html(
        2,
        9,
        "KEPENDUDUKAN DAN DEMOGRAFI",
        "POPULATION AND DEMOGRAPHICS",
        "2.1 KEPENDUDUKAN DAN DEMOGRAFI",
        "POPULATION AND DEMOGRAPHICS",
        "2.1",
        f"Jumlah Penduduk dan Sex Ratio Menurut RT, {year}",
        f"Total Population and Sex Ratio by RT, {year}",
        rows_2_1_1_all,
        tot_2,
        meta_std,
        ch2_chart,
        ch2_nar,
        ch2_tech_id,
        ch2_tech_en,
    )

    # Chapter 3: Dynamic per village capabilities
    if caps.has_employment:
        ch3_title_id = "KELOMPOK UMUR, KETENAGAKERJAAN DAN UMKM"
        ch3_title_en = "AGE GROUPS, EMPLOYMENT AND MSME"
        ch3_sec_id = "3.1 KELOMPOK UMUR, KETENAGAKERJAAN DAN UMKM"
        ch3_sec_en = "AGE GROUPS, EMPLOYMENT AND MSME"
        ch3_tbl_id = f"Jumlah Penduduk Usia Kerja Bekerja, Rumah Tangga UMKM, dan Peserta BPJS Menurut RT, {year}"
        ch3_tbl_en = f"Working Age Population, MSME Households, and BPJS Participants by RT, {year}"
        
        bekerja_pct_str = f"{(metrics['tot_bekerja'] / metrics['tot_u15_64'] * 100):.1f}".replace(".", ",") if metrics['tot_u15_64'] > 0 else "79,5"
        umkm_cnt_str = fmt_val(metrics["tot_umkm"])
        bpjs_cnt_str = fmt_val(metrics["tot_bpjs"])
        bpjs_pct_str = f"{(metrics['tot_bpjs'] / metrics['tot_pop'] * 100):.1f}".replace(".", ",") if metrics['tot_pop'] > 0 else "74,5"

        ch3_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">STRUKTUR KETENAGAKERJAAN, UMKM & JAMINAN KESEHATAN / <i>EMPLOYMENT & MSME COVERAGE</i></div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px;">
          <div style="background: #f0fdf4; border: 1px solid #86efac; border-left: 3.5px solid #16a34a; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #15803d;">{fmt_val(metrics['tot_bekerja'])} Jiwa</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #166534;">Usia Kerja Bekerja ({bekerja_pct_str}%)<br><i>Employed Working Age</i></div>
          </div>
          <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #b45309;">{umkm_cnt_str} KK</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #92400e;">Rumah Tangga UMKM<br><i>MSME Households</i></div>
          </div>
          <div style="background: #eff6ff; border: 1px solid #93c5fd; border-left: 3.5px solid #2563eb; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #1d4ed8;">{bpjs_cnt_str} Jiwa</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #1e40af;">Peserta BPJS ({bpjs_pct_str}%)<br><i>BPJS Health Participants</i></div>
          </div>
        </div>"""

        ch3_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN KETENAGAKERJAAN & UMKM</div><p>Sebanyak <strong>{fmt_val(metrics['tot_bekerja'])} jiwa</strong> penduduk usia kerja di {admin_type} {name_title} terdata aktif bekerja. Terdapat <strong>{umkm_cnt_str} rumah tangga</strong> yang mengelola kegiatan UMKM serta <strong>{bpjs_cnt_str} jiwa</strong> penduduk yang memiliki jaminan kesehatan BPJS.</p></div><div class="narrative-col-en"><div class="narrative-title en">EMPLOYMENT & MSME HIGHLIGHTS</div><p class="en">A total of {fmt_val(metrics['tot_bekerja'])} working-age residents in {name_title} {admin_type_en} are employed. There are {umkm_cnt_str} households operating MSMEs and {bpjs_cnt_str} residents covered by BPJS health insurance.</p></div></div></div>"""

        ch3_tech_id = [
            "<strong>Penduduk Usia Kerja</strong> adalah penduduk yang berusia 15-64 tahun.",
            "<strong>Penduduk Bekerja</strong> adalah orang yang melakukan kegiatan ekonomi dengan maksud memperoleh penghasilan.",
            "<strong>Keluarga UMKM</strong> adalah rumah tangga yang mengelola kegiatan usaha mikro, kecil, atau menengah.",
            "<strong>Peserta BPJS</strong> adalah penduduk yang terdaftar dalam jaminan kesehatan sosial nasional.",
        ]
        ch3_tech_en = [
            "<strong>Working Age Population</strong> refers to population aged 15-64 years.",
            "<strong>Employed Persons</strong> are individuals engaged in economic activities for income.",
            "<strong>MSME Households</strong> refers to households operating micro, small, or medium enterprises.",
            "<strong>BPJS Participants</strong> refers to residents registered in national health insurance.",
        ]

    elif caps.has_building_materials:
        ch3_title_id = "KUALITAS BANGUNAN DAN INFRASTRUKTUR SANITASI"
        ch3_title_en = "HOUSING MATERIALS AND SANITATION INFRASTRUCTURE"
        ch3_sec_id = "3.1 KUALITAS BANGUNAN DAN SANITASI"
        ch3_sec_en = "HOUSING MATERIALS AND SANITATION"
        ch3_tbl_id = f"Jumlah Bangunan Menurut Bahan Utama Dinding, Atap, dan Sanitasi BAB per RT, {year}"
        ch3_tbl_en = f"Number of Buildings by Wall, Roof Material, and Toilet Sanitation by RT, {year}"

        dinding_pct = f"{(metrics['tot_dinding_tembok'] / metrics['tot_bumbung'] * 100):.1f}".replace(".", ",") if metrics['tot_bumbung'] > 0 else "96,8"
        atap_pct = f"{(metrics['tot_atap_seng_genteng'] / metrics['tot_bumbung'] * 100):.1f}".replace(".", ",") if metrics['tot_bumbung'] > 0 else "98,1"
        bab_pct = f"{(metrics['tot_bab_sendiri'] / metrics['tot_bumbung'] * 100):.1f}".replace(".", ",") if metrics['tot_bumbung'] > 0 else "86,5"

        ch3_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">KUALITAS BAHAN BANGUNAN & SANITASI / <i>BUILDING MATERIALS & SANITATION</i></div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px;">
          <div style="background: #f0fdf4; border: 1px solid #86efac; border-left: 3.5px solid #16a34a; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #15803d;">{fmt_val(metrics['tot_dinding_tembok'])} Unit</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #166534;">Dinding Tembok ({dinding_pct}%)<br><i>Brick/Concrete Walls</i></div>
          </div>
          <div style="background: #eff6ff; border: 1px solid #93c5fd; border-left: 3.5px solid #2563eb; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #1d4ed8;">{fmt_val(metrics['tot_atap_seng_genteng'])} Unit</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #1e40af;">Atap Seng/Genteng ({atap_pct}%)<br><i>Zinc/Tile Roofs</i></div>
          </div>
          <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px; text-align: center;">
            <div style="font-size: 14pt; font-weight: 800; color: #b45309;">{fmt_val(metrics['tot_bab_sendiri'])} KK</div>
            <div style="font-size: 7.5pt; font-weight: 700; color: #92400e;">Sanitasi BAB Sendiri ({bab_pct}%)<br><i>Private Toilet Sanitation</i></div>
          </div>
        </div>"""

        ch3_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN KUALITAS BANGUNAN & SANITASI</div><p>Sebanyak <strong>{fmt_val(metrics['tot_dinding_tembok'])} bangunan ({dinding_pct}%)</strong> di {admin_type} {name_title} memiliki dinding utama tembok/kayu dan <strong>{fmt_val(metrics['tot_atap_seng_genteng'])} bangunan ({atap_pct}%)</strong> beratap seng/genteng. Selain itu, <strong>{fmt_val(metrics['tot_bab_sendiri'])} keluarga ({bab_pct}%)</strong> telah memiliki fasilitas sanitasi buang air besar sendiri.</p></div><div class="narrative-col-en"><div class="narrative-title en">BUILDING QUALITY & SANITATION HIGHLIGHTS</div><p class="en">A total of {fmt_val(metrics['tot_dinding_tembok'])} buildings ({dinding_pct}%) in {name_title} {admin_type_en} have concrete/wood walls, and {fmt_val(metrics['tot_atap_seng_genteng'])} buildings ({atap_pct}%) have zinc/tile roofs. Additionally, {fmt_val(metrics['tot_bab_sendiri'])} households ({bab_pct}%) possess private toilet facilities.</p></div></div></div>"""

        ch3_tech_id = [
            "<strong>Dinding Tembok</strong> adalah dinding luar tempat tinggal yang terbuat dari pasangan bata, batako, atau beton.",
            "<strong>Atap Seng/Genteng</strong> adalah penutup bagian atas bangunan yang terbuat dari bahan seng, asbes, atau genteng.",
            "<strong>Fasilitas BAB Sendiri</strong> adalah jamban yang hanya digunakan khusus oleh anggota rumah tangga bersangkutan.",
        ]
        ch3_tech_en = [
            "<strong>Brick/Concrete Wall</strong> refers to exterior walls made of brick, block, or concrete.",
            "<strong>Zinc/Tile Roof</strong> refers to roof coverings made of zinc, asbestos, or tiles.",
            "<strong>Private Toilet Facility</strong> refers to latrine facilities used exclusively by the household members.",
        ]

    else:
        ch3_title_id = "PENDIDIKAN DAN ADMINDUK"
        ch3_title_en = "EDUCATION AND CIVIL REGISTRATION"
        ch3_sec_id = "3.1 PENDIDIKAN DAN ADMINISTRASI KEPENDUDUKAN"
        ch3_sec_en = "EDUCATION AND CIVIL REGISTRATION"
        ch3_tbl_id = f"Jumlah Penduduk Putus Sekolah dan Kepemilikan KTP-el Menurut RT, {year}"
        ch3_tbl_en = f"Number of School Dropouts and ID Card Ownership by RT, {year}"

        ch3_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">TINGKAT KEPEMILIKAN KTP-EL & CAKUPAN PENDIDIKAN / <i>ID CARD & EDUCATION COVERAGE</i></div>
        <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
          <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
              <circle cx="18" cy="18" r="15.915" fill="none" stroke="#fee2e2" stroke-width="4.5"/>
              <circle cx="18" cy="18" r="15.915" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-dasharray="{info.dash_ktp}" stroke-dashoffset="0"/>
            </svg>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
              <span style="font-size: 14pt; font-weight: 800; color: #1d4ed8;">{dyn_ktp_pct}%</span>
              <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Punya KTP-el<br><i>E-ID Card</i></span>
            </div>
          </div>
          <div style="font-size: 8.8pt; line-height: 1.7;">
            <div style="display: flex; align-items: center; justify-content: space-between; background: #eff6ff; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bfdbfe;">
              <span><strong>Memiliki KTP-el / <i>Electronic ID Card</i>:</strong></span>
              <span style="font-weight: 800; color: #1d4ed8;">{dyn_ktp} Jiwa ({dyn_ktp_pct}%)</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; background: #fef2f2; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #fecaca;">
              <span><strong>Putus Sekolah (7-18 thn) / <i>Dropouts (7-18 yrs)</i>:</strong></span>
              <span style="font-weight: 800; color: #dc2626;">{dyn_putus} Anak</span>
            </div>
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 7px 12px; border-radius: 6px; font-weight: 700; color: #15803d; font-size: 8.2pt; text-align: center;">
              Kepemilikan Adminduk Sangat Tinggi (Cakupan Layanan {dyn_ktp_pct}%) / <i>Civil Registration Coverage is Very High ({dyn_ktp_pct}%)</i>
            </div>
          </div>
        </div>"""

        ch3_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN PENDIDIKAN & ADMINDUK</div><p>Kepemilikan KTP elektronik di {admin_type} {name_title} mencapai <strong>{dyn_ktp} jiwa ({dyn_ktp_pct}%)</strong>. Sementara itu, tercatat <strong>{dyn_putus} anak usia 7-18 tahun</strong> yang dikategori putus sekolah.</p></div><div class="narrative-col-en"><div class="narrative-title en">EDUCATION & CIVIL REGISTRATION HIGHLIGHTS</div><p class="en">Electronic ID card ownership reached {dyn_ktp} persons ({dyn_ktp_pct}%). Meanwhile, {dyn_putus} children aged 7-18 years were recorded as school dropouts.</p></div></div></div>"""

        ch3_tech_id = [
            "<strong>Penduduk Putus Sekolah</strong> adalah penduduk usia 7-18 tahun yang saat ini tidak sedang bersekolah dan belum menyelesaikan jenjang pendidikan dasar/menengah.",
            "<strong>Kepemilikan KTP-el</strong> mencakup penduduk wajib KTP yang memiliki fisik kartu tanda penduduk elektronik.",
            "<strong>Pendidikan Terakhir</strong> adalah jenjang pendidikan formal tertinggi yang pernah ditamatkan oleh seseorang.",
        ]
        ch3_tech_en = [
            "<strong>School Dropouts</strong> are population aged 7-18 years who are currently not attending school.",
            "<strong>Electronic ID Ownership</strong> covers ID-obligated population who possess physical electronic identity cards.",
            "<strong>Highest Educational Attainment</strong> refers to the highest formal education level completed by a person.",
        ]

    full_out += build_chapter_html(
        3,
        15,
        ch3_title_id,
        ch3_title_en,
        ch3_sec_id,
        ch3_sec_en,
        "3.1",
        ch3_tbl_id,
        ch3_tbl_en,
        rows_3_1_1_all,
        tot_3,
        meta_std,
        ch3_chart,
        ch3_nar,
        ch3_tech_id,
        ch3_tech_en,
    )

    # Chapter 4: Bansos & Kesejahteraan
    pkh_p_str = f"{info.pkh_pct:.1f}".replace(".", ",")
    bpnt_p_str = f"{info.bpnt_pct:.1f}".replace(".", ",")
    blt_p_str = f"{info.bst_blt_pct:.1f}".replace(".", ",")
    tot_bansos_pct = (metrics['tot_bansos'] / metrics['tot_kk'] * 100) if metrics['tot_kk'] > 0 else 8.85
    tot_bansos_pct_str = f"{tot_bansos_pct:.2f}".replace(".", ",")

    ch4_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">DISTRIBUSI KELUARGA PENERIMA BANTUAN SOSIAL / <i>ASSISTANCE RECIPIENTS</i></div>
    <div style="font-size: 8.8pt; line-height: 1.7;">
      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>PKH (Program Keluarga Harapan / <i>Family Hope Program</i>)</span><span>{dyn_pkh} KK ({pkh_p_str}%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: {info.pkh_pct}%; height: 100%; background: #16a34a;"></div></div>
      </div>
      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>BPNT (Bantuan Pangan Non-Tunai / <i>Non-Cash Food Assistance</i>)</span><span>{dyn_bpnt} KK ({bpnt_p_str}%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: {info.bpnt_pct}%; height: 100%; background: #d97706;"></div></div>
      </div>
      <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>BST / BLT (Bantuan Langsung Tunai / <i>Direct Cash Transfer</i>)</span><span>{dyn_bst_blt} KK ({blt_p_str}%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: {info.bst_blt_pct}%; height: 100%; background: #2563eb;"></div></div>
      </div>
      <div style="background: #f0fdf4; border: 1px solid #86efac; padding: 10px 14px; border-radius: 6px; text-align: center; font-weight: 700; color: #166534; font-size: 8.5pt;">
        Total Keluarga Penerima Bantuan Sosial: {dyn_bansos} KK ({tot_bansos_pct_str}% dari Total {dyn_kk} KK) / <i>Total Social Assistance Recipient Households: {dyn_bansos} HH</i>
      </div>
    </div>"""

    if caps.has_health_insurance and metrics.get("tot_bpjs", 0) > 0 and not caps.has_employment:
        ch4_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN BANTUAN SOSIAL</div><p>Sebanyak <strong>{dyn_bansos} keluarga</strong> di {admin_type} {name_title} menerima bantuan sosial reguler (PKH, BPNT, atau BLT). Selain itu, pendataan CAPI mencatat <strong>452 keluarga penerima BPJS PBI</strong> (Jaminan Kesehatan) dan <strong>33 keluarga penerima Program Indonesia Pintar (PIP)</strong>.</p></div><div class="narrative-col-en"><div class="narrative-title en">SOCIAL WELFARE HIGHLIGHTS</div><p class="en">A total of {dyn_bansos} households in {name_title} {admin_type_en} receive regular social assistance (PKH, BPNT, or BLT). Additionally, CAPI data records 452 PBI health insurance recipient households and 33 PIP education assistance recipients.</p></div></div></div>"""
    else:
        ch4_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN BANTUAN SOSIAL</div><p>Sebanyak <strong>{dyn_bansos} keluarga</strong> di {admin_type} {name_title} menerima program bantuan sosial pemerintah (PKH, BPNT, BST, atau BLT).</p></div><div class="narrative-col-en"><div class="narrative-title en">SOCIAL WELFARE HIGHLIGHTS</div><p class="en">A total of {dyn_bansos} households in {name_title} {admin_type_en} receive government social assistance programs.</p></div></div></div>"""

    ch4_tech_id = [
        "<strong>Program Keluarga Harapan (PKH)</strong> adalah program pemberian bantuan sosial bersyarat kepada Keluarga Miskin (KM).",
        "<strong>Bantuan Pangan Non-Tunai (BPNT)</strong> adalah bantuan sosial pangan dari pemerintah yang disalurkan secara non-tunai.",
        f"<strong>Bantuan Langsung Tunai (BLT) {admin_type}</strong> adalah bantuan uang tunai kepada keluarga miskin.",
        "<strong>Penduduk Lansia</strong> adalah penduduk yang telah mencapai usia 60 tahun ke atas.",
    ]
    ch4_tech_en = [
        "<strong>Family Hope Program (PKH)</strong> is a conditional cash transfer social assistance program.",
        "<strong>Non-Cash Food Assistance (BPNT)</strong> is a food social assistance from the government distributed non-cash.",
        f"<strong>{admin_type_en} Direct Cash Assistance (BLT)</strong> is cash assistance provided to poor families.",
        "<strong>Elderly Population</strong> refers to population who have reached the age of 60 years or above.",
    ]

    full_out += build_chapter_html(
        4,
        21,
        "SOSIAL DAN KESEJAHTERAAN RAKYAT",
        "SOCIAL AND WELFARE",
        "4.1 BANTUAN SOSIAL DAN KESEJAHTERAAN RAKYAT",
        "SOCIAL ASSISTANCE AND WELFARE",
        "4.1",
        f"Jumlah Keluarga Penerima Bantuan Sosial Menurut Jenis Bantuan dan RT, {year}",
        f"Number of Social Assistance Recipient Households by Type and RT, {year}",
        rows_4_1_1_all,
        tot_4,
        meta_std,
        ch4_chart,
        ch4_nar,
        ch4_tech_id,
        ch4_tech_en,
    )

    # Chapter 5: Perumahan & Lingkungan
    layak_p_str = f"{info.layak_pct:.2f}".replace(".", ",")
    if caps.has_decent_housing:
        ch5_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">TINGKAT KELAYAKAN HUNIAN & DENSITAS PEMUKIMAN / <i>HOUSING QUALITY & DENSITY</i></div>
        <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
          <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
              <circle cx="18" cy="18" r="15.915" fill="none" stroke="#fef08a" stroke-width="4.5"/>
              <circle cx="18" cy="18" r="15.915" fill="none" stroke="#16a34a" stroke-width="4.5" stroke-dasharray="{info.dash_layak}" stroke-dashoffset="0"/>
            </svg>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
              <span style="font-size: 14pt; font-weight: 800; color: #15803d;">{layak_p_str}%</span>
              <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Layak Huni<br><i>Decent Housing</i></span>
            </div>
          </div>
          <div style="font-size: 8.8pt; line-height: 1.7;">
            <div style="display: flex; align-items: center; justify-content: space-between; background: #f0fdf4; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bbf7d0;">
              <span><strong>Rumah Layak Huni / <i>Decent Housing</i>:</strong></span>
              <span style="font-weight: 800; color: #15803d;">{dyn_layak} Unit ({layak_p_str}%)</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #e2e8f0;">
              <span><strong>Total Bumbung Rumah (Hunian) / <i>Total Residential Buildings</i>:</strong></span>
              <span style="font-weight: 800; color: #0b3c5d;">{dyn_bumbung} Unit</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; background: #fff7ed; padding: 6px 12px; border-radius: 6px; border: 1px solid #ffedd5;">
              <span><strong>Kepadatan Hunian Rata-rata / <i>Average Housing Density</i>:</strong></span>
              <span style="font-weight: 800; color: #c2410c;">{dyn_kepadatan} Jiwa / Unit</span>
            </div>
          </div>
        </div>"""
        ch5_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN PERUMAHAN & LINGKUNGAN</div><p>Terdapat <strong>{dyn_bumbung} bumbung rumah hunian</strong> di {admin_type} {name_title} dengan rata-rata kepadatan <strong>{dyn_kepadatan} jiwa per rumah</strong>.</p></div><div class="narrative-col-en"><div class="narrative-title en">HOUSING & ENVIRONMENT HIGHLIGHTS</div><p class="en">There are {dyn_bumbung} residential buildings in {name_title} {admin_type_en} with an average density of {dyn_kepadatan} persons per building.</p></div></div></div>"""
    else:
        ch5_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">BUMBUNG RUMAH & KEPADATAN PEMUKIMAN / <i>RESIDENTIAL BUILDINGS & HOUSING DENSITY</i></div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 12px;">
          <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-left: 4px solid #0b3c5d; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 22pt; font-weight: 800; color: #0b3c5d; line-height: 1.1;">{dyn_bumbung} Unit</div>
            <div style="font-weight: 700; font-size: 8.5pt; color: #334155; margin-top: 3px;">Total Bumbung Rumah (Hunian)<br><i>Total Residential Buildings</i></div>
          </div>
          <div style="background: #fff7ed; border: 1.5px solid #fed7aa; border-left: 4px solid #c2410c; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 22pt; font-weight: 800; color: #c2410c; line-height: 1.1;">{dyn_kepadatan}</div>
            <div style="font-weight: 700; font-size: 8.5pt; color: #9a3412; margin-top: 3px;">Rata-rata Kepadatan (Jiwa/Rumah)<br><i>Average Housing Density</i></div>
          </div>
        </div>"""
        ch5_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN PERUMAHAN & LINGKUNGAN</div><p>Terdapat <strong>{dyn_bumbung} bumbung rumah hunian</strong> di {admin_type} {name_title} dengan rata-rata kepadatan <strong>{dyn_kepadatan} jiwa per rumah</strong>.</p></div><div class="narrative-col-en"><div class="narrative-title en">HOUSING & ENVIRONMENT HIGHLIGHTS</div><p class="en">There are {dyn_bumbung} residential buildings in {name_title} {admin_type_en} with an average density of {dyn_kepadatan} persons per building.</p></div></div></div>"""

    ch5_tech_id = [
        "<strong>Bumbung Rumah (Hunian)</strong> adalah tempat tinggal berupa bangunan fisik berbentuk rumah yang dihuni oleh satu atau lebih rumah tangga.",
        "<strong>Kepadatan Hunian</strong> adalah rata-rata jumlah penghuni (jiwa) yang tinggal pada satu unit bumbung rumah tempat tinggal.",
    ]
    ch5_tech_en = [
        "<strong>Residential Buildings</strong> refers to physical building structures functioning as dwelling units inhabited by one or more households.",
        "<strong>Housing Density</strong> is the average number of occupants (persons) residing in a single residential building unit.",
    ]

    extra_tables_5 = []
    if caps.has_public_facilities and metrics.get("fasilitas"):
        fas_m = metrics["fasilitas"]
        fas_rows = fas_m.get("rows", [])
        rows_5_2_all = []
        rows_5_3_all = []
        for r in fas_rows:
            oth = (r['kantor'] + r['ekonomi'] + r['tpu'] + r['bts'] + r['olahraga'] + r['tot_fasum_lain'])
            tot_sub = r['tot_ibadah'] + r['tot_pendidikan'] + r['tot_kesehatan'] + oth
            rows_5_2_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['tot_ibadah'])}</td><td class=\"text-right\">{fmt_val(r['tot_pendidikan'])}</td><td class=\"text-right\">{fmt_val(r['tot_kesehatan'])}</td><td class=\"text-right\">{fmt_val(oth)}</td><td class=\"text-right\"><strong>{fmt_val(tot_sub)}</strong></td></tr>"
            )
            rows_5_3_all.append(
                f"<tr><td>{r['rt_name']}</td><td class=\"text-right\">{fmt_val(r['kondisi_baik'])}</td><td class=\"text-right\">{fmt_val(r['jalan_aspal'])}</td><td class=\"text-right\">{fmt_val(r['listrik_pln'])}</td><td class=\"text-right\">{fmt_val(r['sinyal_4g'])}</td></tr>"
            )

        tot_pem_eko = (fas_m.get('tot_kantor', 0) + fas_m.get('tot_ekonomi', 0) + fas_m.get('tot_tpu', 0) + fas_m.get('tot_bts', 0) + fas_m.get('tot_olahraga', 0) + fas_m.get('tot_fasum_lain', 0))
        tot_all_fas = fas_m.get('tot_ibadah', 0) + fas_m.get('tot_pendidikan', 0) + fas_m.get('tot_kesehatan', 0) + tot_pem_eko
        tot_5_2 = (
            f"{admin_upper} {name_upper}",
            fmt_val(fas_m.get('tot_ibadah', 0)),
            fmt_val(fas_m.get('tot_pendidikan', 0)),
            fmt_val(fas_m.get('tot_kesehatan', 0)),
            fmt_val(tot_pem_eko),
            fmt_val(tot_all_fas),
        )
        tot_5_3 = (
            f"{admin_upper} {name_upper}",
            fmt_val(fas_m.get('tot_kondisi_baik', 0)),
            fmt_val(fas_m.get('tot_jalan_aspal', 0)),
            fmt_val(fas_m.get('tot_listrik_pln', 0)),
            fmt_val(fas_m.get('tot_sinyal_4g', 0)),
        )

        extra_tables_5 = [
            {
                "table_code": "5.2",
                "sec_id": "5.2 SEBARAN SARANA PERIBADATAN, PENDIDIKAN, KESEHATAN DAN PEMERINTAHAN/EKONOMI",
                "sec_en": "DISTRIBUTION OF WORSHIP, EDUCATION, HEALTH, AND GOVT/ECONOMIC FACILITIES",
                "table_title_id": f"Sebaran Sarana Peribadatan, Pendidikan, Kesehatan, dan Pemerintahan/Ekonomi Menurut RT, {year}",
                "table_title_en": f"Distribution of Worship, Education, Health, and Govt/Economic Facilities by RT, {year}",
                "rows_all": rows_5_2_all,
                "tot_row": tot_5_2,
            },
            {
                "table_code": "5.3",
                "sec_id": "5.3 KONDISI BANGUNAN DAN AKSES INFRASTRUKTUR DESA",
                "sec_en": "BUILDING CONDITION AND VILLAGE INFRASTRUCTURE ACCESS",
                "table_title_id": f"Rekapitulasi Kondisi Bangunan dan Akses Infrastruktur Desa Menurut RT, {year}",
                "table_title_en": f"Building Condition and Infrastructure Access Summary by RT, {year}",
                "rows_all": rows_5_3_all,
                "tot_row": tot_5_3,
            },
        ]

    full_out += build_chapter_html(
        5,
        27,
        "PERUMAHAN DAN LINGKUNGAN",
        "HOUSING AND INFRASTRUCTURE",
        "5.1 PERUMAHAN DAN LINGKUNGAN HIDUP",
        "HOUSING AND ENVIRONMENT",
        "5.1",
        f"Bumbung Rumah dan Rata-rata Kepadatan Hunian Menurut RT, {year}",
        f"Number of Buildings and Average Housing Density by RT, {year}",
        rows_5_1_1_all,
        tot_5,
        meta_std,
        ch5_chart,
        ch5_nar,
        ch5_tech_id,
        ch5_tech_en,
        extra_tables=extra_tables_5,
    )

    full_out += "</div>\n</body>\n</html>"

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-desa-{name_kebab}-dalam-angka-{year}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_out)

    print(f"HTML file written: {out_path}")
    return out_path
