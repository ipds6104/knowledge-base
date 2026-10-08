#!/usr/bin/env python3
"""
generate_surat_diskominfo.py
============================
Script otomasi pembuatan Surat Dinas Resmi BPS Kabupaten Mempawah
kepada Dinas Komunikasi dan Informatika Kabupaten Mempawah terkait
permohonan pengisian mandiri (CAWI) SE2026 untuk pegawai OPD.

Menghasilkan format PDF (via Typst) dan DOCX (via python-docx).
"""

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path("/app/workspaces/bps-mempawah")
ASSETS_DIR = REPO_ROOT / "kegiatan" / "kecamatan-dalam-angka" / "2026" / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
OUTPUT_DIR = REPO_ROOT / "kegiatan" / "sensus-ekonomi-2026" / "2026" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPREADSHEET_ID = "1ZpwvQLXJUCwB5yqp7Y5mFMFv1JnHWw3WYP1ebcNsI1U"
SHEET_RANGE = "'Data OPEN Match'!A1:AZ1200"
NOMOR_SURAT = "B-1143/61046/HM.310/2026"

def get_google_token() -> str:
    token_file = Path("/app/data/google_token.json")
    if not token_file.exists():
        raise FileNotFoundError(f"Google token file not found at {token_file}")
    with open(token_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    token = data.get("access_token")
    if not token:
        raise ValueError("access_token not found in token file")
    return token

def fetch_sheet_data(token: str) -> list:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{urllib.parse.quote(SHEET_RANGE)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    rows = res.get("values", [])
    if not rows:
        raise ValueError("No data found in sheet")
    return rows

def escape_typst(text: str) -> str:
    if not text:
        return ""
    chars = ["\\", "[", "]", "#", "$", "*", "_", "`", "@", "<", ">"]
    for c in chars:
        text = text.replace(c, f"\\{c}")
    return text

def build_typst_content(records: list) -> str:
    table_rows = []
    for idx, (nama, inst) in enumerate(records, 1):
        nama_esc = escape_typst(nama)
        inst_esc = escape_typst(inst) if inst else "-"
        table_rows.append(f"  [{idx}], [{nama_esc}], [{inst_esc}],")
    
    table_rows_str = "\n".join(table_rows)
    total_records = len(records)
    
    typst_code = f'''// =============================================================================
// SURAT DINAS RESMI BPS KABUPATEN MEMPAWAH
// PERMOHONAN FASILITASI PENGISIAN MANDIRI DATA SE2026 KE DISKOMINFO
// =============================================================================

#set document(
  title: "Surat Permohonan Pengisian Mandiri SE2026 - Diskominfo Mempawah",
  author: "BPS Kabupaten Mempawah"
)

#set page(
  paper: "a4",
  margin: (
    top: 4.1cm,
    bottom: 1.8cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: [
    #grid(
      columns: (58pt, 1fr, 95pt),
      gutter: 10pt,
      align: (center + horizon, left + horizon, right + horizon),
      [#v(7pt)#image("{ASSETS_DIR}/logo_bps.png", width: 54pt)],
      [
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[BADAN PUSAT STATISTIK] \\
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[KABUPATEN MEMPAWAH] \\
        #v(2.5pt)
        #text(8.2pt, font: "Arial", fill: black)[Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;] \\
        #text(8.2pt, font: "Arial", fill: black)[Laman https://mempawahkab.bps.go.id; Pos-el bps6104\\@bps.go.id.]
      ],
      image("{ASSETS_DIR}/logo_se2026.png", width: 92pt)
    )
    #v(3pt)
    #line(length: 100%, stroke: 2.2pt + black)
  ]
)

#set text(font: "Arial", size: 11pt, lang: "id")
#set par(justify: true, leading: 0.6em)

// =============================================================================
// METADATA SURAT DINAS (HALAMAN 1)
// =============================================================================
#v(2pt)
#grid(
  columns: (1fr, 160pt),
  gutter: 10pt,
  [
    #grid(
      columns: (60pt, 8pt, 1fr),
      gutter: 3pt,
      [Nomor], [:], [{NOMOR_SURAT}],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [#par(justify: false)[*Permohonan Fasilitasi Pengisian Mandiri (CAWI) Data Sensus Ekonomi 2026*]]
    )
  ],
  [
    #align(right)[
      Mempawah, 8 Oktober 2026
    ]
  ]
)

#v(8pt)
Yth. *Kepala Dinas Komunikasi dan Informatika* \\
#h(20pt)*Kabupaten Mempawah* \\
di Mempawah

#v(8pt)
Dengan hormat,

Sehubungan dengan pelaksanaan rangkaian kegiatan Sensus Ekonomi 2026 (SE2026) dan pemadanan data di wilayah Kabupaten Mempawah, Badan Pusat Statistik (BPS) Kabupaten Mempawah bermaksud memohon bantuan dan fasilitasi Bapak/Ibu Kepala Dinas Komunikasi dan Informatika Kabupaten Mempawah untuk mengimbau seluruh Organisasi Perangkat Daerah (OPD) di lingkungan Pemerintah Kabupaten Mempawah agar pegawai yang bersangkutan dapat melakukan pengisian mandiri (*Computer Assisted Web Interviewing / CAWI*).

Adapun tautan/link pengisian mandiri tersebut dapat diakses secara daring melalui tautan resmi berikut:

#v(2pt)
#align(center)[
  #block(
    fill: rgb("#EFF6FF"),
    inset: (x: 16pt, y: 7pt),
    radius: 4pt,
    stroke: 0.8pt + rgb("#3B82F6")
  )[
    #text(10pt, weight: "bold", fill: rgb("#1E40AF"))[Tautan Pengisian Mandiri:] \\
    #v(2pt)
    #link("https://s.bps.go.id/61_ECKalbar")[#text(11pt, weight: "bold", fill: rgb("#2563EB"))[https://s.bps.go.id/61_ECKalbar]]
  ]
]
#v(2pt)

Bersama surat ini, kami lampirkan daftar nama pegawai beserta instansi/OPD terkait (sejumlah {total_records} pegawai) yang menjadi sasaran pengisian mandiri. Untuk koordinasi teknis, pertanyaan, dan konfirmasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, *Sarah Pratiwi* (WhatsApp: *0856-4121-9375*).

Demikian permohonan ini kami sampaikan, atas perhatian, dukungan, dan kerja sama yang baik kami ucapkan terima kasih.

#v(10pt)

#align(right)[
  #block(width: 220pt)[
    #align(center)[
      Kepala Badan Pusat Statistik \\
      Kabupaten Mempawah,
      #v(42pt)
      *Munawir*
    ]
  ]
]

// =============================================================================
// HALAMAN LAMPIRAN
// =============================================================================
#pagebreak()

#v(2pt)
#grid(
  columns: (60pt, 8pt, 1fr),
  gutter: 3pt,
  [Lampiran], [:], [1 (satu) Berkas],
  [Nomor], [:], [{NOMOR_SURAT}],
  [Tanggal], [:], [8 Oktober 2026]
)

#v(8pt)
#align(center)[
  #text(10.5pt, weight: "bold")[Daftar Nama Pegawai dan Organisasi Perangkat Daerah (OPD) Sasaran Pengisian Mandiri SE2026]
]
#v(4pt)

#set text(size: 8.5pt)
#table(
  columns: (35pt, 1.4fr, 1.8fr),
  inset: 4.5pt,
  align: (center, left, left),
  stroke: (col, row) => {{
    let norm = 0.4pt + luma(180)
    let top_b = if row == 0 {{ 1.2pt + black }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: norm, right: norm)
  }},
  fill: (col, row) => {{
    if row == 0 {{
      rgb("#F3F4F6")
    }} else if calc.even(row) {{
      rgb("#FAFAFA")
    }} else {{
      none
    }}
  }},
  table.header(
    [*No*],
    [*Nama Pegawai*],
    [*Organisasi Perangkat Daerah (OPD)*]
  ),
{table_rows_str}
)

#v(6pt)
#text(8pt, style: "italic", fill: rgb("#4B5563"))[Catatan: Daftar pegawai di atas disaring dari basis data pemadanan SE2026 (Data OPEN Match) khusus Organisasi Perangkat Daerah (OPD) di lingkungan Pemerintah Kabupaten Mempawah.]
'''
    return typst_code

def generate_docx(records: list, docx_path: Path):
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    
    doc = Document()
    
    # Page setup A4
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Kop Surat (Table 1 row, 3 cols)
    header_table = doc.add_table(rows=1, cols=3)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    
    widths = [Inches(1.1), Inches(4.3), Inches(1.3)]
    row = header_table.rows[0]
    for i, w in enumerate(widths):
        row.cells[i].width = w
        
    # Col 0: Logo BPS
    p_logo = row.cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(6)
    logo_bps_path = str(ASSETS_DIR / "logo_bps.png")
    if os.path.exists(logo_bps_path):
        p_logo.add_run().add_picture(logo_bps_path, width=Inches(0.95))
        
    # Col 1: Teks Kop
    p_text = row.cells[1].paragraphs[0]
    p_text.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_text.paragraph_format.line_spacing = 1.05
    p_text.paragraph_format.space_after = Pt(0)
    
    r_bps1 = p_text.add_run("BADAN PUSAT STATISTIK\nKABUPATEN MEMPAWAH\n")
    r_bps1.bold = True
    r_bps1.italic = True
    r_bps1.font.size = Pt(13)
    
    r_addr = p_text.add_run(
        "Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;\n"
        "Laman https://mempawahkab.bps.go.id; Pos-el bps6104@bps.go.id."
    )
    r_addr.font.size = Pt(8)
    
    # Col 2: Logo SE2026
    p_se = row.cells[2].paragraphs[0]
    p_se.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    logo_se_path = str(ASSETS_DIR / "logo_se2026.png")
    if os.path.exists(logo_se_path):
        p_se.add_run().add_picture(logo_se_path, width=Inches(1.25))
        
    # Remove borders from header table
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for b_name in ['top', 'left', 'bottom', 'right']:
            b = OxmlElement(f'w:{b_name}')
            b.set(qn('w:val'), 'none')
            tcBorders.append(b)
        tcPr.append(tcBorders)
        
    # Horizontal Rule separator
    p_hr = doc.add_paragraph()
    p_hr.paragraph_format.space_before = Pt(4)
    p_hr.paragraph_format.space_after = Pt(12)
    pBdr = OxmlElement('w:pBdr')
    bottomBdr = OxmlElement('w:bottom')
    bottomBdr.set(qn('w:val'), 'single')
    bottomBdr.set(qn('w:sz'), '16') # 2pt
    bottomBdr.set(qn('w:space'), '1')
    bottomBdr.set(qn('w:color'), '000000')
    pBdr.append(bottomBdr)
    p_hr._p.get_or_add_pPr().append(pBdr)
    
    # Metadata Surat (Table 2 cols: Left info, Right date)
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    m_row = meta_table.rows[0]
    m_row.cells[0].width = Inches(4.3)
    m_row.cells[1].width = Inches(2.4)
    
    # Metadata kiri
    p_m1 = m_row.cells[0].paragraphs[0]
    p_m1.paragraph_format.line_spacing = 1.15
    p_m1.paragraph_format.space_after = Pt(0)
    p_m1.add_run(f"Nomor     : {NOMOR_SURAT}\n")
    p_m1.add_run("Sifat         : Biasa\n")
    p_m1.add_run("Lampiran : 1 (satu) Berkas\n")
    r_hal = p_m1.add_run("Hal           : Permohonan Fasilitasi Pengisian Mandiri (CAWI) Data Sensus Ekonomi 2026")
    r_hal.bold = True
    
    # Tanggal kanan
    p_m2 = m_row.cells[1].paragraphs[0]
    p_m2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_m2.add_run("Mempawah, 8 Oktober 2026")
    
    # Clear borders
    for cell in m_row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for b_name in ['top', 'left', 'bottom', 'right']:
            b = OxmlElement(f'w:{b_name}')
            b.set(qn('w:val'), 'none')
            tcBorders.append(b)
        tcPr.append(tcBorders)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Tujuan Surat
    p_tujuan = doc.add_paragraph()
    p_tujuan.paragraph_format.line_spacing = 1.15
    p_tujuan.paragraph_format.space_after = Pt(10)
    r_t1 = p_tujuan.add_run("Yth. Kepala Dinas Komunikasi dan Informatika\n        Kabupaten Mempawah\n")
    r_t1.bold = True
    p_tujuan.add_run("di Mempawah")
    
    # Isi Surat
    p_isi1 = doc.add_paragraph()
    p_isi1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_isi1.paragraph_format.line_spacing = 1.15
    p_isi1.add_run(
        "Dengan hormat,\n\n"
        "Sehubungan dengan pelaksanaan rangkaian kegiatan Sensus Ekonomi 2026 (SE2026) dan pemadanan "
        "data di wilayah Kabupaten Mempawah, Badan Pusat Statistik (BPS) Kabupaten Mempawah bermaksud "
        "memohon bantuan dan fasilitasi Bapak/Ibu Kepala Dinas Komunikasi dan Informatika Kabupaten Mempawah "
        "untuk mengimbau seluruh Organisasi Perangkat Daerah (OPD) di lingkungan Pemerintah Kabupaten Mempawah "
        "agar pegawai yang bersangkutan dapat melakukan pengisian mandiri "
    )
    r_cawi = p_isi1.add_run("(Computer Assisted Web Interviewing / CAWI)")
    r_cawi.bold = True
    p_isi1.add_run(".\n\n")
    p_isi1.add_run(
        "Adapun tautan/link pengisian mandiri tersebut dapat diakses secara daring melalui tautan resmi berikut:"
    )
    
    # Box Link Pengisian
    box_table = doc.add_table(rows=1, cols=1)
    box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_cell = box_table.rows[0].cells[0]
    b_cell.width = Inches(5.5)
    
    # Background light blue
    tcPr = b_cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'EFF6FF')
    tcPr.append(shd)
    
    # Blue border
    tcBorders = OxmlElement('w:tcBorders')
    for b_name in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '8')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '3B82F6')
        tcBorders.append(b)
    tcPr.append(tcBorders)
    
    p_box = b_cell.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(6)
    p_box.paragraph_format.space_after = Pt(6)
    r_bxtitle = p_box.add_run("Tautan Pengisian Mandiri:\n")
    r_bxtitle.bold = True
    r_bxtitle.font.size = Pt(10)
    r_bxtitle.font.color.rgb = RGBColor(0x1E, 0x40, 0xAF)
    
    r_bxlink = p_box.add_run("https://s.bps.go.id/61_ECKalbar")
    r_bxlink.bold = True
    r_bxlink.font.size = Pt(11)
    r_bxlink.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    
    # Paragraf Penutup & PIC
    p_isi2 = doc.add_paragraph()
    p_isi2.paragraph_format.space_before = Pt(10)
    p_isi2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_isi2.paragraph_format.line_spacing = 1.15
    p_isi2.add_run(
        f"Bersama surat ini, kami lampirkan daftar nama pegawai beserta instansi/OPD terkait "
        f"(sejumlah {len(records)} pegawai) yang menjadi sasaran pengisian mandiri. Untuk koordinasi teknis, "
        f"pertanyaan, dan konfirmasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, "
    )
    r_pic = p_isi2.add_run("Sarah Pratiwi")
    r_pic.bold = True
    p_isi2.add_run(" (WhatsApp: ")
    r_picno = p_isi2.add_run("0856-4121-9375")
    r_picno.bold = True
    p_isi2.add_run(").\n\n")
    p_isi2.add_run(
        "Demikian permohonan ini kami sampaikan, atas perhatian, dukungan, dan kerja sama yang baik kami ucapkan terima kasih."
    )
    
    # Tanda Tangan
    p_ttd = doc.add_paragraph()
    p_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ttd.paragraph_format.space_before = Pt(14)
    p_ttd.paragraph_format.line_spacing = 1.15
    p_ttd.add_run("Kepala Badan Pusat Statistik\nKabupaten Mempawah,\n\n\n\n")
    r_muna = p_ttd.add_run("Munawir")
    r_muna.bold = True
    
    # ==========================
    # HALAMAN LAMPIRAN
    # ==========================
    doc.add_page_break()
    
    p_lhdr = doc.add_paragraph()
    p_lhdr.paragraph_format.line_spacing = 1.15
    p_lhdr.paragraph_format.space_after = Pt(8)
    p_lhdr.add_run(f"Lampiran : 1 (satu) Berkas\nNomor     : {NOMOR_SURAT}\nTanggal  : 8 Oktober 2026")
    
    p_ltitle = doc.add_paragraph()
    p_ltitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ltitle.paragraph_format.space_after = Pt(10)
    r_lt = p_ltitle.add_run("Daftar Nama Pegawai dan Organisasi Perangkat Daerah (OPD) Sasaran Pengisian Mandiri SE2026")
    r_lt.bold = True
    r_lt.font.size = Pt(10.5)
    
    # Tabel Lampiran (3 cols)
    table_lamp = doc.add_table(rows=1, cols=3)
    table_lamp.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lamp.autofit = False
    
    l_widths = [Inches(0.6), Inches(2.8), Inches(3.3)]
    
    # Header Row
    hdr_row = table_lamp.rows[0]
    # Repeat header row on every page
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    
    hdr_titles = ["No", "Nama Pegawai", "Organisasi Perangkat Daerah (OPD)"]
    for i, title in enumerate(hdr_titles):
        cell = hdr_row.cells[i]
        cell.width = l_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(8.5)
        # Background grey
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'F3F4F6')
        tcPr.append(shd)
        
    for idx, (nama, inst) in enumerate(records, 1):
        row = table_lamp.add_row()
        # No
        cell_no = row.cells[0]
        cell_no.width = l_widths[0]
        p0 = cell_no.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(str(idx))
        r0.font.size = Pt(8.5)
        
        # Nama
        cell_nama = row.cells[1]
        cell_nama.width = l_widths[1]
        p1 = cell_nama.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(nama)
        r1.font.size = Pt(8.5)
        
        # Instansi
        cell_inst = row.cells[2]
        cell_inst.width = l_widths[2]
        p2 = cell_inst.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r2 = p2.add_run(inst if inst else "-")
        r2.font.size = Pt(8.5)
        
        # Alternate zebra background
        if idx % 2 == 0:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), 'FAFAFA')
                tcPr.append(shd)
                
    # Style borders of table_lamp
    tblPr = table_lamp._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4') # 0.5pt
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), 'D1D5DB') # Light gray
        tblBorders.append(b)
    tblPr.append(tblBorders)
    
    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(8)
    r_nt = p_note.add_run(
        "Catatan: Daftar pegawai di atas disaring dari basis data pemadanan SE2026 (Data OPEN Match) "
        "khusus Organisasi Perangkat Daerah (OPD) di lingkungan Pemerintah Kabupaten Mempawah."
    )
    r_nt.italic = True
    r_nt.font.size = Pt(8)
    r_nt.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)
    
    doc.save(docx_path)

def main():
    print("🔑 Mengambil Google Token...")
    token = get_google_token()
    
    print("📊 Mengunduh data dari Google Sheet 'Data OPEN Match'...")
    rows = fetch_sheet_data(token)
    
    records = []
    # Kolom G = index 6 (Nama Pegawai)
    # Kolom AT = index 45 (Instansi BKSDM)
    # Kolom AV = index 47 (Adalah OPD == '1')
    for r in rows[1:]:
        nama = r[6].strip() if len(r) > 6 else ""
        inst = r[45].strip() if len(r) > 45 else ""
        is_opd = r[47].strip() if len(r) > 47 else ""
        if is_opd == "1" and nama:
            records.append((nama, inst))
            
    print(f"✅ Berhasil memuat {len(records)} pegawai dengan kriteria AV = 1.")
    
    typ_path = OUTPUT_DIR / "surat-permohonan-pengisian-mandiri-diskominfo.typ"
    pdf_path = OUTPUT_DIR / "surat-permohonan-pengisian-mandiri-diskominfo.pdf"
    docx_path = OUTPUT_DIR / "surat-permohonan-pengisian-mandiri-diskominfo.docx"
    
    print(f"📝 Menyusun dokumen Typst: {typ_path}...")
    typst_content = build_typst_content(records)
    typ_path.write_text(typst_content, encoding="utf-8")
    
    print(f"⚙️ Mengompilasi Typst ke PDF: {pdf_path}...")
    cmd = [
        "typst", "compile",
        "--root", "/",
        "--font-path", str(FONTS_DIR),
        str(typ_path), str(pdf_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Kompilasi gagal:\n{res.stderr}")
        sys.exit(1)
        
    file_size_kb = pdf_path.stat().st_size / 1024
    print(f"🎉 Sukses! PDF terbuat: {pdf_path} ({file_size_kb:.1f} KB)")
    
    print(f"📄 Menghasilkan berkas Word DOCX: {docx_path}...")
    generate_docx(records, docx_path)
    docx_size_kb = docx_path.stat().st_size / 1024
    print(f"🎉 Sukses! DOCX terbuat: {docx_path} ({docx_size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
