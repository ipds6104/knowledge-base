"""
Frontmatter: Katalog, Tim Penyusun, & Kontributor Data for KCDA 2026.
Menangani Halaman Katalog (ii), Tim Penyusun (iii), dan Kontributor Data (iv).
"""

from typing import Dict, Any

def render_katalog_and_contributors(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_pub = cfg["no_publikasi"]
    no_katalog = cfg["no_katalog"]
    pic_polos = cfg["pic_nama_polos"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()
    issn = cfg.get("issn")
    volume = cfg.get("volume", "Volume 48, 2026")

    issn_katalog = f"\n  #v(2pt)\n  #text(weight: \"bold\")[ISSN:] {issn} \\\\" if issn else ""
    issn_tim = f"#align(right)[\n  #text(7pt, fill: luma(120))[ISSN {issn}]\n]\n" if issn else ""

    return f"""// ==========================================
// 3. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================

// Judul Publikasi Langsung di Bagian Atas (Hitam)
#text(10.5pt, weight: "bold", fill: black)[KECAMATAN {nama_singkat.upper()} DALAM ANGKA 2026] \\
#v(1pt)
#text(9pt, style: "italic", fill: black)[{nama_en.upper()} DISTRICT IN FIGURES 2026] \\
#v(2pt)
#text(7.5pt, fill: black)[{volume}]

#let total_frontmatter_pages = context {{
  let elems = query(<transisi_isi>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    let final_p = if calc.odd(p) {{ p + 1 }} else {{ p }}
    numbering("i", final_p)
  }} else {{
    "xii"
  }}
}}
#let total_arabic_pages = context {{
  let elems = query(<akhir_buku>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  }} else {{
    "28"
  }}
}}

#v(9pt)
#text(7.5pt)[
  #text(weight: "bold")[Katalog/Catalogue:] {no_katalog}{issn_katalog}
  #v(2pt)
  #text(weight: "bold")[Nomor Publikasi/Publication Number:] {no_pub}
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Ukuran Buku/Book Size:] 14,8 cm x 21,0 cm \\
  #v(2pt)
  #text(weight: "bold")[Jumlah Halaman/Number of Pages:] #total_frontmatter_pages+#total_arabic_pages Halaman/Pages
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyusun Naskah/Manuscript Drafter:] \\
  #text(weight: "bold")[BPS Kabupaten Mempawah] \\
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyunting/Editor:] \\
  #text(weight: "bold")[BPS Kabupaten Mempawah] \\
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Pembuat Kover/Cover Designer:] \\
  #text(weight: "bold")[BPS Kabupaten Mempawah] \\
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Sumber Ilustrasi/Illustration Source:] \\
  magnific.com, unsplash.com, BPS Kabupaten Mempawah
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penerbit/Publisher:] \\
  #text(weight: "bold")[© Badan Pusat Statistik Kabupaten Mempawah/]#text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(1fr)

#text(6.8pt)[
  #text(weight: "bold")[Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik] \\
  #v(2pt)
  #text(style: "italic")[It is prohibited to reproduce and/or duplicate part or all of this book for commercial purpose without permission from BPS-Statistics Indonesia]
]

#pagebreak()

// ==========================================
// 4. TIM PENYUSUN / COMPILERS (HALAMAN iii)
// ==========================================
{issn_tim}#v(0.6cm)

#align(center)[
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \\
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026] \\
  #text(8pt, style: "italic")[{nama_en} District in Figures 2026] \\
  #text(7.5pt)[{volume}]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/_Director_] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \\
  #text(8pt)[Kurniawan #sym.circle.filled.small Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \\
  #text(8pt)[{pic_polos}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \\
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/_Translators_] \\
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
]

#pagebreak()

// ==========================================
// 5. KONTRIBUTOR DATA (HALAMAN iv)
// ==========================================
#align(center)[
  #text(10.5pt, weight: "bold")[KONTRIBUTOR DATA/]#text(10.5pt, weight: "bold", style: "italic")[DATA CONTRIBUTORS]
]
#v(14pt)

#set enum(indent: 0pt, body-indent: 7pt, spacing: 9.5pt)
#text(8pt)[
+ Kantor Camat {nama_singkat}/#text(style: "italic")[{nama_singkat} District Office]
+ Kementerian Agama/#text(style: "italic")[Ministry of Religious Affairs]
+ Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology]
+ Badan Pusat Statistik/#text(style: "italic")[BPS-Statistics Indonesia]
+ Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]
+ Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata Kabupaten Mempawah/#text(style: "italic")[Education, Youth, Sports, and Tourism Office of Mempawah Regency]
+ Dinas Pertanian, Ketahanan Pangan dan Perikanan Kabupaten Mempawah/#text(style: "italic")[Agriculture, Food Security, and Fisheries Office of Mempawah Regency]
+ Dinas Kesehatan, Pengendalian Penduduk dan Keluarga Berencana Kabupaten Mempawah/#text(style: "italic")[Health, Population Control, and Family Planning Office of Mempawah Regency]
+ Dinas Perindustrian, Perdagangan dan Tenaga Kerja Kabupaten Mempawah/#text(style: "italic")[Industry, Trade, and Manpower Office of Mempawah Regency]
+ Bagian Tata Pemerintahan Sekretariat Daerah Kabupaten Mempawah/#text(style: "italic")[Governance Division of Regional Secretariat of Mempawah Regency]
+ Pemerintah Desa/Kelurahan se-Kecamatan {nama_singkat}/#text(style: "italic")[Village/Subdistrict Administrations throughout {nama_singkat} District]
]

#pagebreak()
"""
