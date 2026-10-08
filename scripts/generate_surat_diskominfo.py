#!/usr/bin/env python3
"""
generate_surat_diskominfo.py
============================
Script otomasi pembuatan Surat Dinas Resmi BPS Kabupaten Mempawah
kepada Dinas Komunikasi dan Informatika Kabupaten Mempawah terkait
permohonan pengisian mandiri (CAWI) SE2026 untuk pegawai OPD.

Lampiran ditarik langsung dari sheet "Data OPEN Match" pada Google Spreadsheet master:
ID: 1ZpwvQLXJUCwB5yqp7Y5mFMFv1JnHWw3WYP1ebcNsI1U
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
SHEET_RANGE = "'Data OPEN Match'!A1:H1200"

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
      image("{ASSETS_DIR}/logo_bps.png", width: 56pt),
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
      [Nomor], [:], [B- #h(30pt) /61046/HM.310/10/2026],
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

Adapun tata cara dan panduan langkah-langkah pengisian mandiri tersebut dapat diakses secara daring melalui tautan resmi berikut:

#v(2pt)
#align(center)[
  #block(
    fill: rgb("#EFF6FF"),
    inset: (x: 16pt, y: 7pt),
    radius: 4pt,
    stroke: 0.8pt + rgb("#3B82F6")
  )[
    #text(10pt, weight: "bold", fill: rgb("#1E40AF"))[Tautan Panduan & Langkah Pengisian Mandiri:] \\
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
  [Nomor], [:], [B- #h(30pt) /61046/HM.310/10/2026],
  [Tanggal], [:], [8 Oktober 2026]
)

#v(8pt)
#align(center)[
  #text(10.5pt, weight: "bold")[Daftar Nama Pegawai dan Instansi/OPD Sasaran Pengisian Mandiri Sensus Ekonomi 2026]
]
#v(4pt)

#set text(size: 8.5pt)
#table(
  columns: (35pt, 1.4fr, 1.6fr),
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
    [*Instansi / Perangkat Daerah*]
  ),
{table_rows_str}
)

#v(6pt)
#text(8pt, style: "italic", fill: rgb("#4B5563"))[Catatan: Data ditarik dari basis data pemadanan SE2026 (Data OPEN Match) Kabupaten Mempawah.]
'''
    return typst_code

def main():
    print("🔑 Mengambil Google Token...")
    token = get_google_token()
    
    print("📊 Mengunduh data dari Google Sheet 'Data OPEN Match'...")
    rows = fetch_sheet_data(token)
    
    records = []
    for r in rows[1:]:
        nama = r[6].strip() if len(r) > 6 else ""
        inst = r[7].strip() if len(r) > 7 else ""
        if nama:
            records.append((nama, inst))
            
    print(f"✅ Berhasil memuat {len(records)} pegawai.")
    
    typ_path = OUTPUT_DIR / "surat-permohonan-pengisian-mandiri-diskominfo.typ"
    pdf_path = OUTPUT_DIR / "surat-permohonan-pengisian-mandiri-diskominfo.pdf"
    
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

if __name__ == "__main__":
    main()
