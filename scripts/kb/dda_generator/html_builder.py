"""BPS HTML Layout Engine for DDA Generator.

Menyusun publikasi BPS 5 Bab lengkap dengan aturan Facing Pages Running Header & Footer
berstandar BPS Katalog 1303004 / Statistik Indonesia 2026.
"""

from pathlib import Path


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


def build_desa_html(config: dict, metrics: dict) -> Path:
    """Menyusun halaman HTML bilingual A4 berstandar BPS untuk publikasi DDA."""
    name_title = config["name_title"]
    name_upper = config["name_upper"]
    name_kebab = config["name_kebab"]
    kecamatan = config.get("kecamatan", "Mempawah Timur")
    year = config.get("year", 2026)
    kades_title = config.get("kades_title", f"Kepala Desa {name_title}")
    kades_title_en = config.get("kades_title_en", f"Head of {name_title} Village")
    kades_name = config.get("kades_name", f"Kepala Desa {name_title}")

    book_header_id = f"DESA {name_upper} DALAM ANGKA {year}"
    book_header_en = f"{name_upper} VILLAGE IN FIGURES {year}"

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

    # Table rows
    rows_1_1_2_all = [
        f'<tr><td><strong>{r["rt_name"]}</strong></td><td>{r["ketua_rt"]}</td><td class="text-center">{r["petugas"]}</td></tr>'
        for r in rows
    ]

    rows_2_1_1_all = []
    for r in rows:
        sr_str = f"{r['sr']:.2f}".replace(".", ",")
        rows_2_1_1_all.append(
            f'<tr><td><strong>{r["rt_name"]}</strong></td><td class="text-center">{fmt_val(r["l"])}</td><td class="text-center">{fmt_val(r["p"])}</td><td class="text-center">{fmt_val(r["tot"])}</td><td class="text-center">{sr_str}</td></tr>'
        )
    tot_2 = f'<tr class="total-row"><td><strong>DESA {name_upper} / {name_upper} VILLAGE</strong></td><td class="text-center">{dyn_l}</td><td class="text-center">{dyn_p}</td><td class="text-center">{dyn_pop}</td><td class="text-center">{dyn_sr}</td></tr>'

    rows_3_1_1_all = []
    for r in rows:
        ktp_str = f"{r['ktp_pct']:.2f}".replace(".", ",")
        rows_3_1_1_all.append(
            f'<tr><td><strong>{r["rt_name"]}</strong></td><td class="text-center">{fmt_val(r["tot"])}</td><td class="text-center">{fmt_val(r["putus"])}</td><td class="text-center">{fmt_val(r["ktp"])}</td><td class="text-center">{ktp_str}%</td></tr>'
        )
    tot_3 = f'<tr class="total-row"><td><strong>DESA {name_upper} / {name_upper} VILLAGE</strong></td><td class="text-center">{dyn_pop}</td><td class="text-center">{dyn_putus}</td><td class="text-center">{dyn_ktp}</td><td class="text-center">{dyn_ktp_pct}%</td></tr>'

    rows_4_1_1_all = [
        f'<tr><td><strong>{r["rt_name"]}</strong></td><td class="text-center">{fmt_val(r["pkh"])}</td><td class="text-center">{fmt_val(r["bpnt"])}</td><td class="text-center">{fmt_val(r["bst"] + r["blt"])}</td><td class="text-center">{fmt_val(r["tot_bansos"])}</td></tr>'
        for r in rows
    ]
    tot_4 = f'<tr class="total-row"><td><strong>DESA {name_upper} / {name_upper} VILLAGE</strong></td><td class="text-center">{dyn_pkh}</td><td class="text-center">{dyn_bpnt}</td><td class="text-center">{dyn_bst_blt}</td><td class="text-center">{dyn_bansos}</td></tr>'

    rows_5_1_1_all = []
    for r in rows:
        kep_str = f"{r['kepadatan']:.2f}".replace(".", ",")
        layak_str = f"{r['layak_pct']:.2f}".replace(".", ",")
        rows_5_1_1_all.append(
            f'<tr><td><strong>{r["rt_name"]}</strong></td><td class="text-center">{fmt_val(r["tot"])}</td><td class="text-center">{fmt_val(r["bumbung"])}</td><td class="text-center">{kep_str}</td><td class="text-center">{layak_str}</td></tr>'
        )
    tot_5 = f'<tr class="total-row"><td><strong>DESA {name_upper} / {name_upper} VILLAGE</strong></td><td class="text-center">{dyn_pop}</td><td class="text-center">{dyn_bumbung}</td><td class="text-center">{dyn_kepadatan}</td><td class="text-center">92,33</td></tr>'

    meta_std = f"""<div class="table-meta">
        <div class="meta-row"><div class="meta-lbl">Catatan/<i>Note:</i></div><div>Data keadaan Rukun Tetangga (RT) per Juni {year} / <i>RT condition data as of June {year}</i></div></div>
        <div class="meta-row"><div class="meta-lbl">Sumber/<i>Source:</i></div><div>Pemerintah Desa {name_title} — Program Desa Cinta Statistik {year} / <i>Government of {name_title} Village — {year} Desa Cinta Statistik Program</i></div></div>
      </div>"""

    # Helper: Facing Pages Page Card Builder
    def make_page_card(ch_title_id, ch_title_en, badge_text, body_inner, page_num):
        is_even = (page_num % 2 == 0)

        # Header & Footer Parity (BPS Facing Pages Standard)
        if is_even:
            h_html = f"""<div class="running-header even"><div>{book_header_id}</div><div class="en">{book_header_en}</div></div>"""
            f_html = f"""<div class="running-footer even">{badge_text}</div>"""
        else:
            h_html = f"""<div class="running-header odd"><div>{ch_title_id}</div><div class="en">{ch_title_en}</div></div>"""
            f_html = f"""<div class="running-footer odd">{badge_text}</div>"""

        return f"""  <div class="page-card">
    <div class="page-content">
      {h_html}
      {body_inner}
      {f_html}
    </div>
  </div>\n\n"""

    def make_blank_page():
        return """  <div class="page-card" style="background: #ffffff;">
    <div class="page-content">
      <!-- Intentionally left blank page per BPS guidelines (Recto/Verso rule) -->
    </div>
  </div>\n\n"""

    # Chapter Cover Card: NO running header, NO running footer (BPS 2026 Standard)
    def make_cover_card(badge_no, title_id, title_en, chart_html):
        return f"""  <div class="page-card">
    <div class="page-content" style="background: #ffffff; padding: 25px 20px; position: relative;">
      <!-- BPS 2026 Chapter Header Banner -->
      <div style="background: linear-gradient(135deg, #f97316 0%, #eb8a3c 45%, #ea580c 100%); border-radius: 16px; padding: 25px; display: flex; align-items: center; gap: 25px; box-shadow: 0 4px 15px rgba(235, 138, 60, 0.25);">
        
        <!-- Left Badge Circle: Number on Top, BAB, Chapter -->
        <div style="background: #c2410c; color: #ffffff; width: 105px; height: 105px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 3px solid rgba(255,255,255,0.3);">
          <div style="font-size: 36pt; font-weight: 900; line-height: 0.85; margin-top: -2px;">{badge_no}</div>
          <div style="font-size: 10pt; font-weight: 800; letter-spacing: 1px; margin-top: 2px;">BAB</div>
          <div style="font-size: 8pt; font-style: italic; opacity: 0.9; margin-top: -1px;">Chapter</div>
        </div>

        <!-- Right Header Title Text with Separator Line -->
        <div style="flex: 1;">
          <h1 style="color: #ffffff; margin: 0; border: none; padding: 0; font-size: 20pt; font-weight: 800; text-transform: uppercase; line-height: 1.2;">{title_id}</h1>
          <div style="border-bottom: 2.5px solid rgba(255, 255, 255, 0.85); margin: 8px 0; width: 100%;"></div>
          <div style="font-style: italic; font-size: 13.5pt; font-weight: 700; color: #ffffff; text-transform: uppercase; line-height: 1.2;">{title_en}</div>
        </div>
      </div>

      <!-- Infographic & Highlight Chart Block -->
      <div style="margin-top: 25px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
        {chart_html}
      </div>
    </div>
  </div>\n\n"""

    html_header = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Desa {name_title} Dalam Angka {year} / {name_title} Village in Figures {year}</title>
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
      padding: 10mm 15mm 12mm 15mm;
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
      bottom: 7mm;
      left: 12mm;
      right: 12mm;
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

    .narrative-box {{ background: transparent; border: none; padding: 0; margin-bottom: 15px; }}
    .narrative-box p {{ text-align: justify; text-justify: inter-word; margin-bottom: 8px; line-height: 1.5; }}
    .narrative-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .narrative-col-id {{ padding-right: 10px; }}
    .narrative-col-en {{ padding-left: 15px; font-style: italic; color: #475569; }}
    .narrative-title {{ font-weight: 800; color: #0b3c5d; font-size: 8.8pt; margin-bottom: 4px; text-transform: uppercase; }}
    .narrative-title.en {{ font-style: italic; }}

    .section-header {{ font-size: 11pt; font-weight: 800; color: #0b3c5d; margin-bottom: 10px; padding-bottom: 3px; text-transform: uppercase; }}
    .section-header .en {{ display: block; font-size: 10pt; font-weight: 800; font-style: italic; color: #0b3c5d; text-transform: uppercase; margin-top: 1px; }}

    .table-title-block {{ display: flex; gap: 12px; align-items: flex-start; margin-bottom: 8px; }}
    .table-label {{ font-weight: 800; font-size: 9.5pt; color: #1a202c; white-space: nowrap; }}
    .table-label .id-lbl {{ text-decoration: underline; }}
    .table-label i {{ font-style: italic; font-weight: 700; text-decoration: none !important; }}
    .table-num {{ font-weight: 800; font-size: 9.5pt; color: #1a202c; }}
    .table-name {{ font-weight: 700; font-size: 9pt; color: #1a202c; line-height: 1.35; }}
    .table-name .en-title {{ display: block; font-weight: 700; font-style: italic; color: #1a202c; margin-top: 1px; }}

    .bps-table {{ width: 100%; border-collapse: collapse; font-size: 8pt; margin-bottom: 8px; }}
    .bps-table th.main-header {{ background-color: #eb8a3c; color: #ffffff; font-weight: 700; text-align: center; padding: 6px 8px; border: 1px solid #d97706; vertical-align: middle; font-size: 8.2pt; }}
    .bps-table th.col-num {{ background-color: #fdebd0; color: #1a202c; font-weight: 700; text-align: center; padding: 3px; border: 1px solid #d97706; font-size: 7.8pt; }}
    .bps-table td {{ padding: 4.5px 8px; border: 1px solid #cbd5e1; color: #1a202c; }}
    .bps-table tbody tr:nth-child(even) {{ background-color: #fff5eb; }}
    .bps-table tr.total-row td {{ background-color: #eb8a3c !important; color: #ffffff !important; font-weight: 800; border: 1px solid #d97706; }}
    .text-center {{ text-align: center; }}
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
        <h1 class="cover-title">DESA {name_upper}<br>DALAM ANGKA {year}</h1>
        <div class="cover-subtitle">{name_upper} VILLAGE IN FIGURES {year}</div>
      </div>
    </div>
  </div>"""

    # Page 2: Compilers (No header, No footer)
    card_2_compilers = f"""  <div class="page-card">
    <div class="page-content">
      <div style="text-align: center; margin-top: 35px; margin-bottom: 25px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0 0 4px 0; text-transform: uppercase;">TIM PENYUSUN/<i>COMPILERS</i></h2>
        <div style="font-size: 10.5pt; font-weight: 600; color: #2d3748;">Desa {name_title} Dalam Angka {year}</div>
        <div style="font-size: 10.5pt; font-style: italic; color: #475569;">{name_title} Village in Figures {year}</div>
        <div style="font-size: 9.5pt; color: #2d3748; margin-top: 2px;">Volume 1, {year}</div>
      </div>
      <div style="text-align: center; max-width: 90%; margin: 0 auto; font-size: 9.5pt; line-height: 1.6; color: #1a202c;">
        <div style="margin-bottom: 18px;"><div style="font-weight: 800;">Penanggung Jawab/<i>Persons in Charge:</i></div><div style="color: #2d3748; margin-top: 2px; font-weight: 700;">{kades_name.upper()}</div></div>
        <div style="margin-bottom: 18px;"><div style="font-weight: 800;">Penyunting/<i>Editors:</i></div><div style="color: #2d3748; margin-top: 2px;">Tim Pembina Desa Cantik BPS Kabupaten Mempawah</div></div>
        <div style="margin-bottom: 18px;"><div style="font-weight: 800;">Penulis Naskah/<i>Data Writers:</i></div><div style="color: #2d3748; margin-top: 2px;">Tim Agen Statistik Desa {name_title}</div></div>
        <div style="margin-bottom: 18px;"><div style="font-weight: 800;">Pengolah Data/<i>Data Processors:</i></div><div style="color: #2d3748; margin-top: 2px;">Tim Agen Statistik Desa {name_title}</div></div>
        <div style="margin-bottom: 18px;"><div style="font-weight: 800;">Penata Letak/<i>Layouters:</i></div><div style="color: #2d3748; margin-top: 2px;">Tim Agen Statistik Desa {name_title}</div></div>
      </div>
    </div>
  </div>"""

    # Page 3 (iii - ODD)
    card_3_contrib = make_page_card("KONTRIBUTOR DATA", "DATA CONTRIBUTORS", "iii", f"""      <h2 style="text-align: center; color: #0b3c5d; padding-bottom: 6px; font-size: 13pt; margin-bottom: 20px;">KONTRIBUTOR DATA / <i>DATA CONTRIBUTORS</i></h2>
      <ol style="font-size: 9.5pt; line-height: 1.8; color: #2d3748; padding-left: 20px;">
        <li>Pemerintah Desa {name_title} / <i>Government of {name_title} Village</i></li>
        <li>Pengurus Rukun Tetangga ({len(rows)} RT) Desa {name_title} / <i>Management of {len(rows)} Neighborhood Units (RT) of {name_title} Village</i></li>
      </ol>""", 3)

    # Page 4 (iv - EVEN)
    card_4_preface_id = make_page_card("KATA PENGANTAR", "PREFACE", "iv", f"""      <h2 style="text-align: center; color: #0b3c5d; font-size: 14pt; font-weight: 800; margin-top: 10px; margin-bottom: 25px;">KATA PENGANTAR</h2>
      <div style="font-size: 9.5pt; line-height: 1.6; color: #2d3748; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi resmi <strong>"Desa {name_title} Dalam Angka {year}"</strong> dapat diselesaikan dengan baik. Publikasi ini merupakan wujud nyata pembinaan statistik sektoral melalui Program <strong>Desa Cantik (Desa Cinta Statistik)</strong> BPS Kabupaten Mempawah berkolaborasi dengan Pemerintah Desa {name_title}.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">Data yang disajikan dihimpun secara langsung dari {len(rows)} Rukun Tetangga (RT) menggunakan metode <i>Computer-Assisted Personal Interviewing</i> (CAPI) berbasis aplikasi mobile AppSheet. Cakupan data meliputi kondisi demografi kependudukan, tingkat pendidikan, kepemilikan dokumen adminduk (KTP-el), sebaran penerima bantuan sosial, hingga kelayakan infrastruktur perumahan.</p>
      </div>
      <div style="margin-top: 35px; font-size: 9.5pt; text-align: right; padding-right: 20px;">
        <div style="margin-bottom: 15px; font-weight: 500; color: #2d3748;">{name_title}, Agustus {year}</div>
        <div style="display: inline-block; text-align: center;">
          <div style="font-weight: 700; color: #0b3c5d;">{kades_title.upper()}</div>
          <div style="font-weight: 800; color: #0b3c5d; text-decoration: underline; margin-top: 55px; font-size: 10.5pt;">{kades_name.upper()}</div>
        </div>
      </div>""", 4)

    # Page 5 (v - ODD)
    card_4_preface_en = make_page_card("PREFACE", "PREFACE", "v", f"""      <h2 style="text-align: center; color: #0b3c5d; font-size: 14pt; font-weight: 800; font-style: italic; margin-top: 10px; margin-bottom: 25px;">PREFACE</h2>
      <div style="font-size: 9.5pt; line-height: 1.6; font-style: italic; color: #475569; max-width: 95%; margin: 0 auto;">
        <p style="margin-bottom: 16px; text-align: justify; text-indent: 30px;">Praise be to God Almighty for His blessings, the official publication <i>"{name_title} Village in Figures {year}"</i> has been successfully completed. This publication is a concrete result of statistical development under the Desa Cantik Program by BPS-Statistics of Mempawah Regency in collaboration with the Government of {name_title} Village.</p>
        <p style="margin-bottom: 25px; text-align: justify; text-indent: 30px;">The presented data was collected directly from {len(rows)} Neighborhood Units (RT) using the CAPI method via AppSheet mobile application. The coverage includes demographics, education, ID card ownership, social assistance distribution, and housing infrastructure.</p>
      </div>
      <div style="margin-top: 35px; font-size: 9.5pt; text-align: right; padding-right: 20px;">
        <div style="margin-bottom: 15px; font-style: italic; color: #475569;">{name_title}, August {year}</div>
        <div style="display: inline-block; text-align: center;">
          <div style="font-weight: 700; font-style: italic; color: #0b3c5d;">{kades_title_en.upper()}</div>
          <div style="font-weight: 800; color: #0b3c5d; text-decoration: underline; margin-top: 55px; font-size: 10.5pt;">{kades_name.upper()}</div>
        </div>
      </div>""", 5)

    # Page 6 (vi - EVEN)
    card_5_toc = make_page_card("DAFTAR ISI", "CONTENTS", "vi", f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">DAFTAR ISI/<i>CONTENTS</i></h2>
        <div style="font-size: 10.5pt; font-weight: 700; color: #2d3748; margin-top: 4px;">Desa {name_title} Dalam Angka {year}</div>
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
      </ul>""", 6)

    # Page 7 (vii - ODD)
    card_5b_lot = make_page_card("DAFTAR TABEL", "LIST OF TABLES", "vii", f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <h2 style="font-size: 13.5pt; font-weight: 800; color: #1a202c; margin: 0; text-transform: uppercase;">DAFTAR TABEL/<i>LIST OF TABLES</i></h2>
      </div>
      <style>
        .lot-hdr {{ display: flex; font-size: 8.8pt; color: #2d3748; margin-bottom: 8px; line-height: 1.3; }}
        .lot-hdr-no {{ width: 45px; flex-shrink: 0; }}
        .lot-hdr-pg {{ flex: 1; text-align: right; }}
        .lot-list {{ list-style: none; padding: 0; margin: 0; }}
        .lot-list li {{ position: relative; overflow: hidden; line-height: 1.5; font-size: 8.8pt; margin-bottom: 6px; clear: both; color: #2d3748; }}
        .lot-list li .lot-no {{ float: left; width: 45px; font-weight: 600; background: #fff; position: relative; z-index: 2; }}
        .lot-list li .lot-page {{ position: absolute; right: 0; bottom: 0; background: #fff; padding-left: 6px; z-index: 2; }}
        .lot-list li .lot-title {{ background: #fff; padding-right: 6px; position: relative; z-index: 2; }}
        .lot-list li::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 4px; border-bottom: 1.2px dotted #777; z-index: 1; }}
        .lot-sec {{ font-weight: 800; color: #0b3c5d; font-size: 8.8pt; margin-top: 7px; margin-bottom: 2px; }}
      </style>
      <div class="lot-hdr"><div class="lot-hdr-no">Tabel<br><i style="color:#475569;">Table</i></div><div class="lot-hdr-pg">Halaman<br><i style="color:#475569;">Page</i></div></div>
      <ul class="lot-list"><li><span class="lot-no">0.1</span><span class="lot-page">1</span><span class="lot-title">Statistik Kunci {year} / <i>Key Statistics, {year}</i></span></li></ul>
      <div class="lot-sec">1.&nbsp;&nbsp;GEOGRAFI DAN PEMERINTAHAN / <i>GEOGRAPHY AND GOVERNMENT</i></div>
      <ul class="lot-list"><li><span class="lot-no">1.2</span><span class="lot-page">5</span><span class="lot-title">Daftar Nama Ketua RT dan Petugas Pendata Menurut Wilayah RT, {year}</span></li></ul>
      <div class="lot-sec">2.&nbsp;&nbsp;KEPENDUDUKAN DAN DEMOGRAFI / <i>POPULATION AND DEMOGRAPHICS</i></div>
      <ul class="lot-list"><li><span class="lot-no">2.1</span><span class="lot-page">11</span><span class="lot-title">Jumlah Penduduk dan Sex Ratio Menurut RT, {year}</span></li></ul>
      <div class="lot-sec">3.&nbsp;&nbsp;PENDIDIKAN DAN ADMINDUK / <i>EDUCATION AND CIVIL REGISTRATION</i></div>
      <ul class="lot-list"><li><span class="lot-no">3.1</span><span class="lot-page">17</span><span class="lot-title">Jumlah Penduduk Putus Sekolah dan Kepemilikan KTP-el Menurut RT, {year}</span></li></ul>
      <div class="lot-sec">4.&nbsp;&nbsp;SOSIAL DAN KESEJAHTERAAN RAKYAT / <i>SOCIAL AND WELFARE</i></div>
      <ul class="lot-list"><li><span class="lot-no">4.1</span><span class="lot-page">23</span><span class="lot-title">Jumlah Keluarga Penerima Bantuan Sosial Menurut Jenis Bantuan dan RT, {year}</span></li></ul>
      <div class="lot-sec">5.&nbsp;&nbsp;PERUMAHAN DAN LINGKUNGAN / <i>HOUSING AND INFRASTRUCTURE</i></div>
      <ul class="lot-list"><li><span class="lot-no">5.1</span><span class="lot-page">29</span><span class="lot-title">Bumbung Rumah dan Rata-rata Kepadatan Hunian Menurut RT, {year}</span></li></ul>""", 7)

    # Page 8 (viii - EVEN)
    card_6_tech_notes = make_page_card("PENJELASAN UMUM", "EXPLANATORY NOTES", "viii", f"""      <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
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
      </table>""", 8)

    # Page 9 (ix - ODD)
    card_7_abbreviations = make_page_card("DAFTAR SINGKATAN", "LIST OF ABBREVIATIONS", "ix", """      <h2 style="text-align: center; color: #0b3c5d; font-size: 13pt; margin-top: 0; margin-bottom: 20px;">DAFTAR SINGKATAN / <i>LIST OF ABBREVIATIONS</i></h2>
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
      </table>""", 9)

    # Page 11 (Arab 1 - ODD)
    card_8_keystats = make_page_card("STATISTIK KUNCI", "KEY STATISTICS", "1", f"""      <div class="table-title-block" style="margin-top: 10px; margin-bottom: 15px;">
        <div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div>
        <div class="table-num">0.1</div>
        <div class="table-name">Statistik Kunci {year}<br><span class="en-title">Key Statistics, {year}</span></div>
      </div>
      <table class="bps-table" style="font-size: 8.8pt;">
        <thead>
          <tr><th class="main-header" style="text-align: left;">Rincian / <i>Description</i></th><th class="main-header" style="width: 120px;">Satuan / <i>Unit</i></th><th class="main-header" style="width: 90px;">{year}</th></tr>
          <tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr>
        </thead>
        <tbody>
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
          <tr><td>Rumah Layak Huni / <i>Decent Housing</i></td><td>Unit / <i>Units</i></td><td class="text-right">{dyn_layak}</td></tr>
          <tr><td>Persentase Rumah Layak Huni / <i>Decent Housing Rate</i></td><td>%</td><td class="text-right">92,33</td></tr>
        </tbody>
      </table>{meta_std}""", 11)

    # Function to build chapters with chunked pages & exact page parity
    def build_chapter_html(ch_num, badge_start, ch_title_id, ch_title_en, sec_id, sec_en, table_code, table_title_id, table_title_en, rows_all, tot_row, meta_html, info_items_html, narrative_html="", tech_notes_id=[], tech_notes_en=[]):
        res = ""
        # 1. Cover Card (No Header, No Footer)
        res += make_cover_card(str(ch_num), ch_title_id, ch_title_en, info_items_html)

        # 2. Technical Notes Page (badge_start + 1)
        tech_rows = []
        for idx, (item_id, item_en) in enumerate(zip(tech_notes_id, tech_notes_en), start=1):
            tech_rows.append(f"""<tr>
              <td style="width: 50%; vertical-align: top; padding-right: 15px; border: none; padding-bottom: 12px; text-align: justify; text-justify: inter-word;">{idx}. {item_id}</td>
              <td style="width: 50%; vertical-align: top; padding-left: 15px; font-style: italic; color: #475569; border: none; padding-bottom: 12px; text-align: justify; text-justify: inter-word;">{idx}. {item_en}</td>
            </tr>""")
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
        res += make_page_card(ch_title_id, ch_title_en, str(badge_start + 1), tech_page_body, badge_start + 1)

        # Chunk rows for 3 pages
        r_p1 = "\n".join(rows_all[0:12])
        r_p2 = "\n".join(rows_all[12:25])
        r_p3_list = rows_all[25:37]
        if tot_row:
            r_p3_list.append(tot_row)
        r_p3 = "\n".join(r_p3_list)

        # Table headers
        if table_code == '1.1.2':
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Nama Ketua RT<br><i>Neighborhood Chairman</i></th><th class="main-header">Agen Statistik Desa<br><i>Village Statistical Agent</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr>"""
        elif table_code == '2.1.1':
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Laki-laki<br><i>Male</i></th><th class="main-header">Perempuan<br><i>Female</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Sex Ratio<br><i>Sex Ratio</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == '3.1.1':
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Putus Sekolah (7-18 thn)<br><i>Dropouts (7-18 yrs)</i></th><th class="main-header">Memiliki KTP-el<br><i>ID Card Owners</i></th><th class="main-header">Persentase KTP-el (%)<br><i>ID Card Pct (%)</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == '4.1.1':
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Penerima PKH<br><i>PKH Recipients</i></th><th class="main-header">Penerima BPNT<br><i>BPNT Recipients</i></th><th class="main-header">Penerima BST/BLT<br><i>BST/BLT Recipients</i></th><th class="main-header">Total Penerima Bansos<br><i>Total Assistance Recipient</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""
        elif table_code == '5.1.1':
            thead = """<tr><th class="main-header">Nama RT<br><i>RT Name</i></th><th class="main-header">Total Penduduk<br><i>Total Population</i></th><th class="main-header">Bumbung Rumah (Hunian)<br><i>Residential Buildings</i></th><th class="main-header">Rata-rata Jiwa/Rumah<br><i>Avg Persons/Building</i></th><th class="main-header">Rumah Layak Huni (%)<br><i>Decent Housing (%)</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th><th class="col-num">(4)</th><th class="col-num">(5)</th></tr>"""

        sec_h = f"""<div class="section-header">{sec_id}<span class="en">{sec_en}</span></div>"""
        main_title = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">{table_code}</div><div class="table-name">{table_title_id}<br><span class="en-title">{table_title_en}</span></div></div>"""
        cont_title = f"""<p style="font-weight: 800; font-style: italic; font-size: 9pt; color: #1a202c; margin: 0 0 8px 0;">Lanjutan Tabel/<em>Continued Table</em> {table_code}</p>"""

        if table_code == '1.1.2':
            t1_1_1_block = f"""<div class="table-title-block"><div class="table-label"><span class="id-lbl">Tabel</span><br><i>Table</i></div><div class="table-num">1.1.1</div><div class="table-name">Batas Wilayah Administrasi Desa {name_title}<br><span class="en-title">Administrative Boundary of {name_title} Village</span></div></div>
            <table class="bps-table">
              <thead><tr><th class="main-header">Batas Wilayah<br><i>Boundary</i></th><th class="main-header">Desa / Kelurahan / Laut<br><i>Village / Sea</i></th><th class="main-header">Kecamatan<br><i>District</i></th></tr><tr><th class="col-num">(1)</th><th class="col-num">(2)</th><th class="col-num">(3)</th></tr></thead>
              <tbody>
                <tr><td>Sebelah Utara / North</td><td>{config.get('north', '-')}</td><td>{kecamatan}</td></tr>
                <tr><td>Sebelah Selatan / South</td><td>{config.get('south', '-')}</td><td>-</td></tr>
                <tr><td>Sebelah Timur / East</td><td>{config.get('east', '-')}</td><td>{kecamatan}</td></tr>
                <tr><td>Sebelah Barat / West</td><td>{config.get('west', '-')}</td><td>{kecamatan}</td></tr>
              </tbody>
            </table>
            <div class="table-meta" style="margin-bottom: 12px;"><div class="meta-row"><div class="meta-lbl">Sumber/<i>Source:</i></div><div>Pemerintah Desa {name_title} / <i>Government of {name_title} Village</i></div></div></div>"""
            b1 = f"""{sec_h}\n{narrative_html}\n{t1_1_1_block}\n{main_title}<table class="bps-table"><thead>{thead}</thead><tbody>{r_p1}</tbody></table>"""
        else:
            nar_b = f"\n{narrative_html}" if narrative_html else ""
            b1 = f"""{sec_h}{nar_b}\n{main_title}<table class="bps-table"><thead>{thead}</thead><tbody>{r_p1}</tbody></table>"""

        # Table Page 1 (badge_start + 2)
        res += make_page_card(ch_title_id, ch_title_en, str(badge_start + 2), b1, badge_start + 2)

        # Table Page 2 (badge_start + 3)
        b2 = f"""<div style="margin: auto 0;">{cont_title}<table class="bps-table"><thead>{thead}</thead><tbody>{r_p2}</tbody></table></div>"""
        res += make_page_card(ch_title_id, ch_title_en, str(badge_start + 3), b2, badge_start + 3)

        # Table Page 3 (badge_start + 4)
        b3 = f"""<div style="margin: auto 0;">{cont_title}<table class="bps-table"><thead>{thead}</thead><tbody>{r_p3}</tbody></table>{meta_html}</div>"""
        res += make_page_card(ch_title_id, ch_title_en, str(badge_start + 4), b3, badge_start + 4)

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
    ch1_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 14px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 6px;">DISTRIBUSI WILAYAH ADMINISTRASI & CAKUPAN PENDATAAN / <i>ADMINISTRATIVE DISTRIBUTION & COVERAGE</i></div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px;">
      <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-left: 4px solid #16a34a; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #15803d; line-height: 1.1;">{len(rows)}</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #166534; margin-top: 3px;">Rukun Tetangga (RT)<br><i>Neighborhood Units</i></div>
      </div>
      <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-left: 4px solid #2563eb; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #1d4ed8; line-height: 1.1;">2</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #1e40af; margin-top: 3px;">Dusun Administrasi<br><i>Administrative Hamlets</i></div>
      </div>
      <div style="background: #fffbeb; border: 1.5px solid #fde68a; border-left: 4px solid #d97706; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 22pt; font-weight: 800; color: #b45309; line-height: 1.1;">100%</div>
        <div style="font-weight: 700; font-size: 8.5pt; color: #92400e; margin-top: 3px;">Cakupan CAPI AppSheet<br><i>CAPI Coverage</i></div>
      </div>
    </div>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
      <div style="font-weight: 800; font-size: 8.8pt; color: #0b3c5d; margin-bottom: 8px; text-transform: uppercase;">Sebaran Rukun Tetangga (RT) per Dusun / <i>RT Distribution by Hamlet</i></div>
      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>Dusun Senggiring (RT 001 - RT 018)</span><span>18 RT (48,6%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 3px;"><div style="width: 48.6%; height: 100%; background: #16a34a;"></div></div>
      </div>
      <div>
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>Dusun Benteng Raya & Sepakat (RT 019 - RT 037)</span><span>19 RT (51,4%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 3px;"><div style="width: 51.4%; height: 100%; background: #2563eb;"></div></div>
      </div>
    </div>"""

    ch1_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN GEOGRAFI DAN PEMERINTAHAN</div><p>Desa {name_title} secara administratif terbagi menjadi <strong>{len(rows)} Rukun Tetangga (RT)</strong>. Seluruh wilayah pendataan didata secara penuh (sensus) oleh Agen Statistik Desa yang terdiri dari aparat Desa {name_title}.</p></div><div class="narrative-col-en"><div class="narrative-title en">GEOGRAPHY & GOVERNMENT HIGHLIGHTS</div><p class="en">{name_title} Village is administratively divided into {len(rows)} Neighborhood Units (RT). All enumeration areas were fully enumerated by Village Statistical Agents consisting of village officials.</p></div></div></div>"""

    ch1_tech_id = [
        "<strong>Desa/Kelurahan Pesisir</strong> adalah desa/kelurahan yang sebagian wilayahnya bersentuhan/berbatasan langsung dengan laut.",
        "<strong>Desa/Kelurahan Bukan Pesisir</strong> adalah desa/kelurahan yang seluruh wilayahnya tidak bersentuhan/berbatasan langsung dengan laut.",
        "<strong>Rukun Tetangga (RT)</strong> adalah lembaga masyarakat yang dibentuk melalui musyawarah masyarakat setempat dalam rangka pelayanan pemerintahan.",
        "<strong>Agen Statistik Desa</strong> adalah aparat Desa yang ditunjuk untuk melakukan pendaftaran dan pendataan potensi wilayah secara langsung di lapangan."
    ]
    ch1_tech_en = [
        "<strong>Coastal Village/Sub-District</strong> is a village/sub-district which some areas intersect/directly adjacent to the sea.",
        "<strong>Non Coastal Village/Sub-District</strong> is a village which has no area that intersects/directly adjacent to the sea.",
        "<strong>Neighborhood Unit (RT)</strong> is a community institution formed through local community consultation.",
        "<strong>Village Statistical Agent</strong> is a village official appointed to conduct direct field registration and data collection."
    ]

    full_out += build_chapter_html(
        1, 3, "GEOGRAFI DAN PEMERINTAHAN", "GEOGRAPHY AND GOVERNMENT",
        "1.1 WILAYAH ADMINISTRATIF", "ADMINISTRATIVE AREA",
        "1.1.2", f"Daftar Nama Ketua RT dan Agen Statistik Desa Menurut Wilayah RT, {year}", f"List of Neighborhood Chairmen and Village Statistical Agents by RT, {year}",
        rows_1_1_2_all, None, meta_std, ch1_chart, ch1_nar, ch1_tech_id, ch1_tech_en
    )

    # Chapter 2: Kependudukan & Demografi
    ch2_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">KOMPOSISI PENDUDUK MENURUT JENIS KELAMIN & DEMOGRAFI / <i>POPULATION BY GENDER & DEMOGRAPHICS</i></div>
    <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
      <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#e2e8f0" stroke-width="4.5"/>
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-dasharray="51.1 48.9" stroke-dashoffset="0"/>
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 13pt; font-weight: 800; color: #0b3c5d;">{dyn_pop} Jiwa</span>
          <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Total Penduduk</span>
        </div>
      </div>
      <div style="font-size: 8.8pt; line-height: 1.7;">
        <div style="display: flex; align-items: center; justify-content: space-between; background: #eff6ff; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bfdbfe;">
          <span><span style="width: 12px; height: 12px; background: #2563eb; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 6px;"></span><strong>Laki-laki / Male:</strong></span>
          <span style="font-weight: 800; color: #1d4ed8;">{dyn_l} Jiwa (51,1%)</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #e2e8f0;">
          <span><span style="width: 12px; height: 12px; background: #cbd5e1; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 6px;"></span><strong>Perempuan / Female:</strong></span>
          <span style="font-weight: 800; color: #475569;">{dyn_p} Jiwa (48,9%)</span>
        </div>
        <div style="background: #fff7ed; border: 1px solid #ffedd5; padding: 7px 12px; border-radius: 6px; font-weight: 700; color: #c2410c; font-size: 8.2pt; text-align: center;">
          Rasio Jenis Kelamin (Sex Ratio): {dyn_sr} (Laki-laki per 100 Perempuan)
        </div>
      </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
      <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-left: 3.5px solid #9333ea; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #7e22ce;">520 Jiwa</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #6b21a8;">Penduduk Lansia (60+ thn)</div>
      </div>
      <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #0f766e;">410 Anak</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #115e59;">Usia Balita (0-5 thn)</div>
      </div>
      <div style="background: #fefce8; border: 1px solid #fef08a; border-left: 3.5px solid #ca8a04; padding: 8px 10px; border-radius: 6px; text-align: center;">
        <div style="font-size: 14pt; font-weight: 800; color: #a16207;">1.661 KK</div>
        <div style="font-size: 7.5pt; font-weight: 700; color: #854d0e;">Total Kepala Keluarga</div>
      </div>
    </div>"""

    ch2_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN KEPENDUDUKAN & DEMOGRAFI</div><p>Jumlah penduduk Desa {name_title} hasil pendaftaran Desa Cantik {year} tercatat sebanyak <strong>{dyn_pop} jiwa</strong>, terdiri dari {dyn_l} laki-laki dan {dyn_p} perempuan dengan <i>sex ratio</i> sebesar <strong>{dyn_sr}</strong>.</p></div><div class="narrative-col-en"><div class="narrative-title en">DEMOGRAPHIC HIGHLIGHTS</div><p class="en">Total population of {name_title} Village based on {year} Desa Cantik registration reached {dyn_pop} persons, comprising {dyn_l} males and {dyn_p} females with a sex ratio of {dyn_sr}.</p></div></div></div>"""

    ch2_tech_id = [
        "<strong>Penduduk</strong> adalah semua orang yang berdomisili di wilayah Indonesia selama 6 bulan atau lebih.",
        "<strong>Rasio Jenis Kelamin (Sex Ratio)</strong> adalah perbandingan antara jumlah penduduk laki-laki dan perempuan per 100 perempuan.",
        "<strong>Kepala Keluarga (KK)</strong> adalah seseorang yang bertanggung jawab atas kebutuhan sehari-hari dalam keluarga.",
        "<strong>Anggota Rumah Tangga (ART)</strong> adalah semua orang yang biasanya bertempat tinggal di suatu rumah tangga."
    ]
    ch2_tech_en = [
        "<strong>Population</strong> refers to all persons residing in Indonesia for 6 months or more.",
        "<strong>Sex Ratio</strong> is the ratio of male population to female population per 100 females.",
        "<strong>Head of Household</strong> is a person responsible for the daily living needs of the family.",
        "<strong>Household Member</strong> refers to all persons who usually reside in a household."
    ]

    full_out += build_chapter_html(
        2, 9, "KEPENDUDUKAN DAN DEMOGRAFI", "POPULATION AND DEMOGRAPHICS",
        "2.1 KEPENDUDUKAN DAN DEMOGRAFI", "POPULATION AND DEMOGRAPHICS",
        "2.1", f"Jumlah Penduduk dan Sex Ratio Menurut RT, {year}", f"Total Population and Sex Ratio by RT, {year}",
        rows_2_1_1_all, tot_2, meta_std, ch2_chart, ch2_nar, ch2_tech_id, ch2_tech_en
    )

    # Chapter 3: Pendidikan & Adminduk
    ch3_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">TINGKAT KEPEMILIKAN KTP-EL & CAKUPAN PENDIDIKAN / <i>ID CARD & EDUCATION COVERAGE</i></div>
    <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
      <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#fee2e2" stroke-width="4.5"/>
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-dasharray="71.17 28.83" stroke-dashoffset="0"/>
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 14pt; font-weight: 800; color: #1d4ed8;">{dyn_ktp_pct}%</span>
          <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Punya KTP-el</span>
        </div>
      </div>
      <div style="font-size: 8.8pt; line-height: 1.7;">
        <div style="display: flex; align-items: center; justify-content: space-between; background: #eff6ff; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bfdbfe;">
          <span><strong>Memiliki KTP-el (E-ID Card):</strong></span>
          <span style="font-weight: 800; color: #1d4ed8;">{dyn_ktp} Jiwa ({dyn_ktp_pct}%)</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; background: #fef2f2; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #fecaca;">
          <span><strong>Putus Sekolah (7-18 thn):</strong></span>
          <span style="font-weight: 800; color: #dc2626;">{dyn_putus} Anak (0,31%)</span>
        </div>
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 7px 12px; border-radius: 6px; font-weight: 700; color: #15803d; font-size: 8.2pt; text-align: center;">
          Kepemilikan Adminduk Sangat Tinggi (Cakupan Layanan {dyn_ktp_pct}%)
        </div>
      </div>
    </div>"""

    ch3_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN PENDIDIKAN & ADMINDUK</div><p>Kepemilikan KTP elektronik di Desa {name_title} mencapai <strong>{dyn_ktp} jiwa ({dyn_ktp_pct}%)</strong>. Sementara itu, tercatat <strong>{dyn_putus} anak usia 7-18 tahun</strong> yang dikategori putus sekolah.</p></div><div class="narrative-col-en"><div class="narrative-title en">EDUCATION & CIVIL REGISTRATION HIGHLIGHTS</div><p class="en">Electronic ID card ownership reached {dyn_ktp} persons ({dyn_ktp_pct}%). Meanwhile, {dyn_putus} children aged 7-18 years were recorded as school dropouts.</p></div></div></div>"""

    ch3_tech_id = [
        "<strong>Penduduk Putus Sekolah</strong> adalah penduduk usia 7-18 tahun yang saat ini tidak sedang bersekolah dan belum menyelesaikan jenjang pendidikan dasar/menengah.",
        "<strong>Kepemilikan KTP-el</strong> mencakup penduduk wajib KTP yang memiliki fisik kartu tanda penduduk elektronik.",
        "<strong>Pendidikan Terakhir</strong> adalah jenjang pendidikan formal tertinggi yang pernah ditamatkan oleh seseorang."
    ]
    ch3_tech_en = [
        "<strong>School Dropouts</strong> are population aged 7-18 years who are currently not attending school.",
        "<strong>Electronic ID Ownership</strong> covers ID-obligated population who possess physical electronic identity cards.",
        "<strong>Highest Educational Attainment</strong> refers to the highest formal education level completed by a person."
    ]

    full_out += build_chapter_html(
        3, 15, "PENDIDIKAN DAN ADMINDUK", "EDUCATION AND CIVIL REGISTRATION",
        "3.1 PENDIDIKAN DAN ADMINISTRASI KEPENDUDUKAN", "EDUCATION AND CIVIL REGISTRATION",
        "3.1", f"Jumlah Penduduk Putus Sekolah dan Kepemilikan KTP-el Menurut RT, {year}", f"Number of School Dropouts and ID Card Ownership by RT, {year}",
        rows_3_1_1_all, tot_3, meta_std, ch3_chart, ch3_nar, ch3_tech_id, ch3_tech_en
    )

    # Chapter 4: Bansos & Kesejahteraan
    ch4_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">DISTRIBUSI KELUARGA PENERIMA BANTUAN SOSIAL / <i>ASSISTANCE RECIPIENTS</i></div>
    <div style="font-size: 8.8pt; line-height: 1.7;">
      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>PKH (Program Keluarga Harapan)</span><span>{dyn_pkh} KK (42,2%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: 42.2%; height: 100%; background: #16a34a;"></div></div>
      </div>
      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>BPNT (Bantuan Pangan Non-Tunai)</span><span>{dyn_bpnt} KK (36,1%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: 36.1%; height: 100%; background: #d97706;"></div></div>
      </div>
      <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 8.2pt; color: #334155;"><span>BST / BLT Desa (Bantuan Langsung Tunai)</span><span>{dyn_bst_blt} KK (21,7%)</span></div>
        <div style="height: 12px; background: #e2e8f0; border-radius: 6px; overflow: hidden; margin-top: 2px;"><div style="width: 21.7%; height: 100%; background: #2563eb;"></div></div>
      </div>
      <div style="background: #f0fdf4; border: 1px solid #86efac; padding: 10px 14px; border-radius: 6px; text-align: center; font-weight: 700; color: #166534; font-size: 8.5pt;">
        Total Keluarga Penerima Bantuan Sosial: {dyn_bansos} KK (8,85% dari Total 1.661 KK)
      </div>
    </div>"""

    ch4_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN BANTUAN SOSIAL</div><p>Sebanyak <strong>{dyn_bansos} keluarga</strong> di Desa {name_title} menerima program bantuan sosial pemerintah (PKH, BPNT, BST, atau BLT Desa).</p></div><div class="narrative-col-en"><div class="narrative-title en">SOCIAL WELFARE HIGHLIGHTS</div><p class="en">A total of {dyn_bansos} households in {name_title} Village receive government social assistance programs.</p></div></div></div>"""

    ch4_tech_id = [
        "<strong>Program Keluarga Harapan (PKH)</strong> adalah program pemberian bantuan sosial bersyarat kepada Keluarga Miskin (KM).",
        "<strong>Bantuan Pangan Non-Tunai (BPNT)</strong> adalah bantuan sosial pangan dari pemerintah yang disalurkan secara non-tunai.",
        "<strong>Bantuan Langsung Tunai (BLT) Desa</strong> adalah bantuan uang tunai kepada keluarga miskin yang bersumber dari Dana Desa.",
        "<strong>Penduduk Lansia</strong> adalah penduduk yang telah mencapai usia 60 tahun ke atas."
    ]
    ch4_tech_en = [
        "<strong>Family Hope Program (PKH)</strong> is a conditional cash transfer social assistance program.",
        "<strong>Non-Cash Food Assistance (BPNT)</strong> is a food social assistance from the government distributed non-cash.",
        "<strong>Village Direct Cash Assistance (BLT)</strong> is cash assistance provided to poor families sourced from Village Funds.",
        "<strong>Elderly Population</strong> refers to population who have reached the age of 60 years or above."
    ]

    full_out += build_chapter_html(
        4, 21, "SOSIAL DAN KESEJAHTERAAN RAKYAT", "SOCIAL AND WELFARE",
        "4.1 BANTUAN SOSIAL DAN KESEJAHTERAAN RAKYAT", "SOCIAL ASSISTANCE AND WELFARE",
        "4.1", f"Jumlah Keluarga Penerima Bantuan Sosial Menurut Jenis Bantuan dan RT, {year}", f"Number of Social Assistance Recipient Households by Type and RT, {year}",
        rows_4_1_1_all, tot_4, meta_std, ch4_chart, ch4_nar, ch4_tech_id, ch4_tech_en
    )

    # Chapter 5: Perumahan & Lingkungan
    ch5_chart = f"""<div style="font-weight: 800; font-size: 11pt; color: #0b3c5d; margin-bottom: 12px; border-bottom: 2.5px solid #eb8a3c; padding-bottom: 5px;">TINGKAT KELAYAKAN HUNIAN & DENSITAS PEMUKIMAN / <i>HOUSING QUALITY & DENSITY</i></div>
    <div style="display: grid; grid-template-columns: 160px 1fr; gap: 18px; align-items: center; margin-bottom: 12px;">
      <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg); border-radius: 50%;">
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#fef08a" stroke-width="4.5"/>
          <circle cx="18" cy="18" r="15.915" fill="none" stroke="#16a34a" stroke-width="4.5" stroke-dasharray="92.33 7.67" stroke-dashoffset="0"/>
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 14pt; font-weight: 800; color: #15803d;">92,33%</span>
          <span style="font-size: 7.2pt; font-weight: 700; color: #475569;">Layak Huni</span>
        </div>
      </div>
      <div style="font-size: 8.8pt; line-height: 1.7;">
        <div style="display: flex; align-items: center; justify-content: space-between; background: #f0fdf4; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #bbf7d0;">
          <span><strong>Rumah Layak Huni:</strong></span>
          <span style="font-weight: 800; color: #15803d;">{dyn_layak} Unit (92,33%)</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #e2e8f0;">
          <span><strong>Total Bumbung Rumah (Hunian):</strong></span>
          <span style="font-weight: 800; color: #0b3c5d;">{dyn_bumbung} Unit</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; background: #fff7ed; padding: 6px 12px; border-radius: 6px; border: 1px solid #ffedd5;">
          <span><strong>Kepadatan Hunian Rata-rata:</strong></span>
          <span style="font-weight: 800; color: #c2410c;">{dyn_kepadatan} Jiwa / Unit</span>
        </div>
      </div>
    </div>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 8px 12px; font-weight: 700; color: #1d4ed8; font-size: 8.2pt; text-align: center;">
      Fasilitas Sanitasi & Listrik PLN: 100% Akses Terdata di Seluruh RT
    </div>"""

    ch5_nar = f"""<div class="narrative-box"><div class="narrative-grid"><div class="narrative-col-id"><div class="narrative-title">ULASAN PERUMAHAN & LINGKUNGAN</div><p>Terdapat <strong>{dyn_bumbung} bumbung rumah hunian</strong> di Desa {name_title} dengan rata-rata kepadatan <strong>{dyn_kepadatan} jiwa per rumah</strong>. Persentase rumah layak huni mencapai <strong>92,33%</strong> dari total bangunan.</p></div><div class="narrative-col-en"><div class="narrative-title en">HOUSING & ENVIRONMENT HIGHLIGHTS</div><p class="en">There are {dyn_bumbung} residential buildings in {name_title} Village with an average density of {dyn_kepadatan} persons per building. Decent housing percentage reached 92.33% of total buildings.</p></div></div></div>"""

    ch5_tech_id = [
        "<strong>Bumbung Rumah (Hunian)</strong> adalah tempat tinggal berupa bangunan fisik berbentuk rumah yang dihuni oleh satu atau lebih rumah tangga.",
        "<strong>Kepadatan Hunian</strong> adalah rata-rata jumlah penghuni (jiwa) yang tinggal pada satu unit bumbung rumah tempat tinggal.",
        "<strong>Rumah Layak Huni</strong> mencakup rumah yang memenuhi persyaratan keselamatan bangunan, kecukupan luas minimum, serta kesehatan penghuni."
    ]
    ch5_tech_en = [
        "<strong>Residential Buildings</strong> refers to physical building structures functioning as dwelling units inhabited by one or more households.",
        "<strong>Housing Density</strong> is the average number of occupants (persons) residing in a single residential building unit.",
        "<strong>Decent Housing</strong> covers housing that meets structural safety requirements, minimum space adequacy, and occupant health standards."
    ]

    full_out += build_chapter_html(
        5, 27, "PERUMAHAN DAN LINGKUNGAN", "HOUSING AND INFRASTRUCTURE",
        "5.1 PERUMAHAN DAN LINGKUNGAN HIDUP", "HOUSING AND ENVIRONMENT",
        "5.1", f"Bumbung Rumah dan Rata-rata Kepadatan Hunian Menurut RT, {year}", f"Number of Buildings and Average Housing Density by RT, {year}",
        rows_5_1_1_all, tot_5, meta_std, ch5_chart, ch5_nar, ch5_tech_id, ch5_tech_en
    )

    full_out += "</div>\n</body>\n</html>"

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-desa-{name_kebab}-dalam-angka-{year}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_out)

    print(f"HTML file written: {out_path}")
    return out_path
