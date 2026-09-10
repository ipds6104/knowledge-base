"""Frontmatter generator for KCDA 2026 (Cover, Catalog, Drafting Team, Preface, TOC)."""

from typing import Dict, Any

def render_frontmatter(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    no_pub = cfg["no_publikasi"]
    pic_nama = cfg["pic_nama"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")

    return f"""
// ==========================================
// 1. KOVER DEPAN (FRONT COVER)
// ==========================================
#align(center)[
  #v(1.2cm)
  #text(10pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \\
  #text(8pt, fill: rgb("#00A0E9"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
  
  #v(3.5cm)
  #block(
    fill: rgb("#FEF3C7"),
    inset: (x: 20pt, y: 25pt),
    radius: 4pt,
    width: 100%,
    stroke: 1.5pt + rgb("#D97706"),
    [
      #text(22pt, weight: "bold", fill: rgb("#B45309"))[{nama_resmi.upper()}] \\
      #v(6pt)
      #text(18pt, weight: "bold", fill: rgb("#B45309"))[DALAM ANGKA 2026] \\
      #v(10pt)
      #text(13pt, style: "italic", fill: rgb("#92400E"))[{nama_en} in Figures 2026]
    ]
  )
  
  #v(4.0cm)
  #rect(fill: rgb("#F3F4F6"), inset: 8pt, radius: 3pt)[
    #text(8.5pt)[Nomor Publikasi / Publication Number: *{no_pub}*]
  ]
  
  #v(1.5cm)
  #text(10pt, weight: "bold", fill: rgb("#374151"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH]
]

#pagebreak()

// ==========================================
// 2. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================
#v(1cm)
#text(12pt, weight: "bold")[{nama_resmi} Dalam Angka 2026] \\
#text(10pt, style: "italic")[{nama_en} in Figures 2026]

#v(12pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))
#v(6pt)
#grid(
  columns: (1.5fr, 3fr),
  row-gutter: 8pt,
  [*Nomor Publikasi*], [: {no_pub}],
  [*Katalog BPS*], [: -],
  [*Ukuran Buku*], [: 21 cm x 29,7 cm (A4)],
  [*Jumlah Halaman*], [: viii + 48 halaman],
  [*Naskah*], [: BPS Kabupaten Mempawah],
  [*Penyunting*], [: Tim IPDS BPS Kabupaten Mempawah],
  [*Desain Kover*], [: BPS Kabupaten Mempawah],
  [*Penerbit*], [: © BPS Kabupaten Mempawah]
)
#v(6pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))

#v(15pt)
#block(
  fill: rgb("#F9FAFB"),
  inset: 10pt,
  stroke: 0.5pt + rgb("#E5E7EB"),
  radius: 3pt,
  [
    #text(8pt)[
      *Dilarang mengumumkan, mendistribusikan, mengomunikasikan, dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik.* \\
      _Prohibited to announce, distribute, communicate, and/or copy part or all of this book for commercial purposes without written permission from BPS-Statistics Indonesia._
    ]
  ]
)

#pagebreak()

// ==========================================
// 3. TIM PENYUSUN & KONTRIBUTOR DATA (HALAMAN iii - Suppressed)
// ==========================================
#align(center)[
  #text(13pt, weight: "bold", fill: rgb("#B45309"))[TIM PENYUSUN / DRAFTING TEAM]
]
#v(15pt)

#table(
  columns: (1.8fr, 3fr),
  stroke: none,
  row-gutter: 10pt,
  [*Pengarah / Director*], [Munawir, S.E., M.M. (Kepala BPS Kabupaten Mempawah)],
  [*Penanggung Jawab / Person in Charge*], [Kurniawan, S.Si., M.E.],
  [*Koordinator Teknis / Technical Coordinator*], [Sukma Andini, S.Tr.Stat.],
  [*Penyusun Naskah / Author*], [{pic_nama}],
  [*Pengolah Data / Data Processor*], [{pic_nama}],
  [*Penata Letak / Layout Editor*], [Tim Otomasi Publikasi BPS Kabupaten Mempawah]
)

#v(25pt)
#align(center)[
  #text(13pt, weight: "bold", fill: rgb("#B45309"))[KONTRIBUTOR DATA / DATA CONTRIBUTORS]
]
#v(12pt)
#grid(
  columns: (1fr, 1fr),
  row-gutter: 8pt,
  [1. Kantor Camat {nama_singkat}], [5. Dinas Pertanian, KP & P Kab. Mempawah],
  [2. Dinas Kependudukan & Capil], [6. Dinas Perindagnaker Kab. Mempawah],
  [3. Dinas Dikporapar Kab. Mempawah], [7. Dinas Kesehatan, PP & KB Kab. Mempawah],
  [4. Kantor Kementerian Agama], [8. Bagian Tata Pemerintahan Setda Mempawah]
)

#pagebreak()

// ==========================================
// 4. KATA PENGANTAR (HALAMAN v)
// ==========================================
#align(center)[
  #text(14pt, weight: "bold", fill: rgb("#B45309"))[KATA PENGANTAR / PREFACE]
]
#v(15pt)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 18pt,
  [
    Puji syukur ke hadirat Tuhan Yang Maha Kuasa atas terbitnya publikasi *"{nama_resmi} Dalam Angka 2026"*. Publikasi ini merupakan publikasi tahunan yang menyajikan beragam data statistik dasar dan sektoral mengenai kondisi geografis, pemerintahan, kependudukan, sosial, pertanian, serta perekonomian di tingkat desa/kelurahan se-Kecamatan {nama_singkat}.

    Data yang disajikan dihimpun dari instansi pemerintah daerah, kantor camat, dan hasil sensus/survei Badan Pusat Statistik. Diharapkan publikasi ini dapat menjadi rujukan utama dalam perencanaan dan evaluasi pembangunan daerah berbasis bukti (*evidence-based policy*).

    Kami menyampaikan penghargaan dan terima kasih yang setinggi-tingginya kepada Camat {nama_singkat}, kepala desa/lurah, serta seluruh pimpinan instansi atas kerja sama yang baik. Kritik dan saran konstruktif sangat kami harapkan guna penyempurnaan pada edisi mendatang.
  ],
  [
    #text(style: "italic")[
      Praise be to God Almighty for the publication of *"{nama_en} in Figures 2026"*. This annual publication presents a wide range of basic and sectoral statistical data concerning geography, government, population, social, agriculture, and economic conditions across villages in {nama_en}.

      The data compiled originates from regional government agencies, subdistrict offices, and BPS censuses/surveys. We hope this publication serves as a primary reference in planning and evaluating regional development based on empirical evidence.

      We express our highest appreciation and gratitude to the Head of {nama_en}, village heads, and agency leaders for their valuable cooperation. Constructive feedback is welcomed for future editions.
    ]
  ]
)

#v(20pt)
#align(right)[
  #block(width: 55%)[
    Mempawah, September 2026 \\
    *Kepala BPS Kabupaten Mempawah* \\
    _Chief Statistician of Mempawah Regency_ \\
    #v(1.8cm)
    *Munawir, S.E., M.M.* \\
    NIP. 19740510 199803 1 003
  ]
]

#pagebreak()

// ==========================================
// 5. DAFTAR ISI (HALAMAN vii)
// ==========================================
#text(14pt, weight: "bold", fill: rgb("#B45309"))[DAFTAR ISI / CONTENTS]
#v(10pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D97706"))
#v(8pt)

#grid(
  columns: (1fr, auto),
  row-gutter: 8pt,
  [*Halaman Judul / Title Page*], [i],
  [*Halaman Katalog & Hak Cipta / Catalog and Copyright*], [ii],
  [*Tim Penyusun & Kontributor / Drafting Team & Contributors*], [iii],
  [*Kata Pengantar / Preface*], [v],
  [*Daftar Isi / Table of Contents*], [vii],
  [*Bab 1: Geografi dan Iklim / Geography and Climate*], [1],
  [*Bab 2: Pemerintahan / Government*], [5],
  [*Bab 3: Kependudukan / Population*], [10],
  [*Bab 4: Sosial dan Kesejahteraan Rakyat / Social and Welfare*], [13],
  [*Bab 5: Pertanian / Agriculture*], [23],
  [*Bab 6: Pariwisata, Transportasi & Komunikasi / Tourism, Transport & Comm.*], [31],
  [*Bab 7: Perbankan, Koperasi & Perdagangan / Banking, Cooperative & Trade*], [35]
)

#pagebreak()
"""
