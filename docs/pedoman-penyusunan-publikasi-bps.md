# PEDOMAN PENYUSUNAN PUBLIKASI BPS (BPS PUBLICATION GUIDELINES & AGENTIC AI SKILL)
## Standar Teknis Baku BPS Edisi 2023 Revisi 2026 & Panduan Implementasi Otomatisasi AI Agent

Dokumen ini merupakan **Pedoman Teknis Baku Penyusunan Publikasi Statistik BPS (Katalog 1303004 Edisi 2023 Revisi 2026)** sekaligus **Spesifikasi Skill & Panduan Kodifikasi untuk Agentic AI** dalam memproduksi publikasi resmi Badan Pusat Statistik (Sensus, Survei, Evaluasi EPSS/SAKIP, Desa Cantik, Kecamatan Dalam Angka, Kabupaten/Provinsi Dalam Angka, dll) secara otomatis berbasis HTML, CSS Print A4, Python Generator, dan Headless Chrome PDF compilation.

> [!NOTE]
> Panduan operasional *agentic workflow* berbasis AI Agent untuk pembuatan publikasi Desa Dalam Angka (DDA) secara otomatis dikemas di dalam Skill: [.agents/skills/dda-publication/SKILL.md](file:///home/ihza/Projects/knowledge-base/.agents/skills/dda-publication/SKILL.md).

---

## 📌 DAFTAR ISI PEDOMAN
1. **[I. Ketentuan Umum, Penomoran, & Mode Bahasa](#i-ketentuan-umum-penomoran--mode-bahasa)**
2. **[II. Anatomi & Urutan Halaman Baku (Front Matter, Batang Tubuh, Back Matter)](#ii-anatomi--urutan-halaman-baku)**
3. **[III. Format Halaman Pembatas Bab (Infographic Chapter Cover)](#iii-format-halaman-pembatas-bab)**
4. **[IV. Format Halaman Penjelasan Teknis Bab (Chapter Technical Notes)](#iv-format-halaman-penjelasan-teknis-bab)**
5. **[V. Standardisasi Tata Letak & Format Tabel BPS (Main Table & Continued Table)](#v-standardisasi-tata-letak--format-tabel-bps)**
6. **[VI. Format Ulasan Deskriptif & Tata Aturan Bahasa](#vi-format-ulasan-deskriptif--tata-aturan-bahasa)**
7. **[VII. Palet Warna, Tipografi, & CSS Tokens Resmi BPS](#vii-palet-warna-tipografi--css-tokens-resmi-bps)**
8. **[VIII. Code Template HTML5 & Print CSS A4 (Full Reference)](#viii-code-template-html5--print-css-a4)**
9. **[IX. Python Generator Script Standard (Automation Engine)](#ix-python-generator-script-standard)**
10. **[X. Alur Eksekusi & Zero-Overlap Print Budget Rule](#x-alur-eksekusi--zero-overlap-print-budget-rule)**

---

## 🎯 I. KETENTUAN UMUM, PENOMORAN, & MODE BAHASA

### 1. Dasar Rujukan Baku
Mengacu pada **Pedoman Pembuatan Publikasi BPS Edisi 2023 / Revisi 2026 (Katalog BPS: 1303004, Nomor Publikasi: 03200.2322)** yang diterbitkan oleh Direktorat Diseminasi Statistik BPS RI.

### 2. Mode Bahasa Publikasi
Publikasi BPS wajib dikompilasi dalam salah satu dari 2 mode bahasa berikut:

- **Mode 1 Bahasa (Bahasa Indonesia)**: Seluruh elemen naskah, judul bab, judul tabel, header kolom, ulasan deskriptif, dan catatan sumber ditulis penuh menggunakan Bahasa Indonesia. Digunakan untuk dokumen internal/lokal.
- **Mode 2 Bahasa / Bilingual (Bahasa Indonesia & English)**: Seluruh elemen disajikan berdampingan atau berurutan: **Bahasa Indonesia (Teks Utama / Normal / Bold)** dan **Bahasa Inggris (Cetak Miring / *Italics* / ***Bold Italic***)**.

#### 8 Perincian Wajib Mode 2 Bahasa (Bilingual):
1. **Running Header Kanan Atas**: Menampilkan nama bab bilingual, contoh: `GEOGRAFI DAN PEMERINTAHAN / GEOGRAPHY AND GOVERNMENT`.
2. **Penjelasan Teknis (Technical Notes)**: Disajikan 2 kolom berdampingan (`PENJELASAN TEKNIS` di kiri, `TECHNICAL NOTES` di kanan).
3. **Judul Tabel (Table Title)**: Judul Bahasa Indonesia (normal) di atas, terjemahan Bahasa Inggris (bold italic) di bawahnya.
4. **Judul Lanjutan Tabel (Continued Table Title)**: Format inline `Lanjutan Tabel/Continued Table X.Y.Z` (di mana `Lanjutan Tabel` tebal, `Continued Table` bold italic).
5. **Baris Total / Jumlah Tabel**: Baris total bilingual, contoh: `DESA SUNGAI BAKAU KECIL / SUNGAI BAKAU KECIL VILLAGE` atau `JUMLAH / TOTAL`.
6. **Catatan Kaki & Sumber Data**: `Catatan / Note:` dan `Sumber / Source:` wajib menyertakan terjemahan Bahasa Inggris.
7. **Kata Pengantar (Preface)**: Paragraf Bahasa Indonesia di kolom kiri, terjemahan Bahasa Inggris (*Italics*) di kolom kanan.
8. **Statistik Kunci (Highlights)**: Label indikator utama memuat teks Bahasa Indonesia dan Bahasa Inggris (*Italic*).

### 3. Standardisasi Penomoran Publikasi BPS
- **Nomor Katalog BPS**: Kode 7 digit yang menunjukkan kelompok publikasi (contoh: `61040.2026` untuk Desa Cantik Mempawah 2026).
- **Nomor Publikasi BPS**: Format `[Kode Wilayah].[Tahun].[Nomor Urut]` (contoh: `61040.2026.001`).
- **ISSN (International Standard Serial Number)**: Untuk publikasi serial/berkala tahunan (contoh: `ISSN 0215-2509`).
- **ISBN (International Standard Book Number)**: Untuk terbitan monografi/sekali terbit.
- **KDT (Katalog Dalam Terbitan / Cataloging in Publication)**: Wajib diletakkan di bagian *Front Matter* (Halaman v).

### 4. Standardisasi Ukuran Buku & Margin BPS
Berdasarkan **Pedoman Pembuatan Publikasi BPS Katalog 1303004 (Subbab 2.2 Tabel 1 & Subbab 4.1.2 Margin)**:

* **Pilihan Ukuran Kertas Resmi BPS**:
  1. **A4 (21 cm x 29.7 cm)**: Standar baku publikasi *Desa Dalam Angka*, *Daerah Dalam Angka*, dan *Statistik Indonesia*.
  2. **A5 (14.8 cm x 21 cm)**: Ukuran *pocketbook* / buku saku.
  3. **B5 JIS (18.2 cm x 25.7 cm)** / **B5 ISO (17.6 cm x 25 cm)**: Ukuran buku analisis tematik.

* **Batas Margin Resmi & Pengaturan CSS Print**:
  - **Inside Margin (Garis Lipatan Penjilidan)**: Minimal **1.5 cm (15 mm)** agar naskah tidak terpotong saat buku dijilid.
  - **Top Margin**: Menampung area *Running Header*.
  - **Bottom Margin**: Menampung area *Running Footer* & Nomor Halaman.
  - **CSS Print Rule (Anti-Double Margin)**:
    - `@page { size: A4; margin: 0; }` -> Wajib diset zero pada `@page` untuk mencegah kompilator Chromium/Headless Chrome menambahkan double margin di atas padding `.page-card`.
    - `.page-card { width: 210mm; height: 297mm; padding: 15mm 20mm 15mm 20mm; box-sizing: border-box; }` -> Menghasilkan ukuran margin fisik presisi di atas kertas A4 (Top 15mm, Left/Right 20mm, Bottom 15mm) seidentik dengan standar publikasi nasional BPS RI (*Statistik Indonesia*).

### 5. Aturan Halaman Kosong (Blank Page) & Kaidah Rekto-Verso
Berdasarkan **Pedoman Pembuatan Publikasi BPS Katalog 1303004 (Subbab 4.1.3 Poin 2, 3, 7, 9 & Subbab 4.1.5 Poin 3)**:

* **Kaidah Rekto-Verso (Posisi Buku Cetak)**:
  - **Halaman Ganjil (*Rekto*)**: Selalu berada di **sisi kanan** saat buku cetak dibuka.
  - **Halaman Genap (*Verso*)**: Selalu berada di **sisi kiri**.
* **Aturan Halaman Pertama Setiap Bab**:
  - **Wajib Dimulai pada Halaman Ganjil (Rekto/Sisi Kanan)**: Setiap bab baru (termasuk halaman pembatas bab) wajib dimulai di halaman ganjil.
  - **Sisipan Halaman Kosong Bab**: Jika bab sebelumnya berakhir di halaman ganjil (kanan), **wajib ditambahkan 1 halaman kosong (genap/kiri)** sebelum masuk pada bab berikutnya.
* **Aturan Jumlah Halaman Pendahuluan (Front Matter)**:
  - Jumlah halaman pendahuluan (penomoran angka Romawi `i`, `ii`, `iii`, dst) **wajib bernilai genap**.
  - Jika jumlah halaman pendahuluan ganjil, **wajib ditambahkan 1 halaman kosong di akhir bagian pendahuluan** (sebelum Bab 1 / Halaman 1 Arab).
* **Ketentuan Tampilan Halaman Kosong**:
  - Halaman kosong yang ditambahkan **TIDAK mencantumkan nomor halaman, running header, maupun running footer**.
  - Halaman kosong tersebut **TETAP dihitung dalam urutan penomoran halaman**.

---

## 📐 II. ANATOMI & URUTAN HALAMAN BAKU

Setiap publikasi resmi BPS disusun menurut urutan halaman baku sebagai berikut:

```
├── FRONT MATTER (HALAMAN PENDAHULUAN — TOTAL HARUS GENAP)
│   ├── 1. Halaman Sampul Depan (Front Cover Card) — (Tanpa Badge, Page 1)
│   ├── 2. Halaman Tim Penyusun (Compilers Page) — (Tanpa Badge, Lay out: Center Aligned Borderless, Page 2)
│   ├── 3. Halaman Kontributor Data & KDT (Cataloging in Publication) — (Badge iii, Page 3)
│   ├── 4. Halaman Kata Pengantar (Versi Bahasa Indonesia) — (Badge iv, Page 4)
│   ├── 5. Halaman Preface (Versi Bahasa Inggris Italics) — (Badge v, Page 5)
│   ├── 6. Halaman Daftar Isi (Table of Contents) — (Badge vi, Page 6)
│   ├── 7. Halaman Daftar Tabel (List of Tables) — (Badge vii, Page 7)
│   ├── 8. Halaman Penjelasan Umum (Explanatory Notes) — (Badge viii, Page 8)
│   ├── 9. Halaman Daftar Singkatan (List of Abbreviations) — (Badge ix, Page 9)
│   └── 10. Halaman Kosong Sisipan Pendahuluan — (Tanpa Badge/Header/Footer, Page x) [Total = 10 Halaman Genap]
│
├── BATANG TUBUH (BAB 1 s.d. BAB N — SETIAP BAB MULAI HALAMAN GANJIL / REKTO)
│   ├── 11. Halaman Tabel 0.1 Statistik Kunci (Table 0.1 Key Statistics) — (Badge 1 Arab, Rekto)
│   ├── 12. Halaman Kosong Sisipan — (Tanpa Badge/Header/Footer, Page 2 Arab, Verso)
│   │
│   ├── 13. BAB 1: Halaman Sampul Bab 1 / Infografis (Chapter Cover Card) — (Tanpa Badge, Page 3 Arab, Rekto)
│   ├── 14. Halaman Penjelasan Teknis Bab 1 — (Badge 4 Arab, Verso)
│   ├── 15. Halaman Ulasan Deskriptif & Tabel Utama 1.1.2 Part 1 — (Badge 5 Arab, Rekto)
│   ├── 16. Halaman Lanjutan Tabel 1.1.2 Part 2 — (Badge 6 Arab, Verso)
│   ├── 17. Halaman Lanjutan Tabel 1.1.2 Part 3 — (Badge 7 Arab, Rekto)
│   ├── 18. Halaman Kosong Sisipan — (Tanpa Badge/Header/Footer, Page 8 Arab, Verso)
│   │
│   ├── 19. BAB 2: Halaman Sampul Bab 2 / Infografis — (Tanpa Badge, Page 9 Arab, Rekto)
│   │   └── ... (Siklus 5 halaman + 1 Halaman Kosong untuk menjaga awal Bab di Halaman Ganjil)
│   │
│   └── 20. BAB N: Bab Terakhir
│
└── BACK MATTER (HALAMAN PENUTUP)
    └── Daftar Pustaka (References) & Lampiran
```

---

## 🎨 III. FORMAT HALAMAN PEMBATAS BAB (CHAPTER DIVIDER INFOGRAPHIC COVER)

Setiap awal bab diawali dengan **Halaman Pembatas Bab (Infographic Chapter Cover Page)** penuh 1 halaman A4:

### Elemen Pembatas Bab:
1. **Lencana Nomor Bab (Chapter Badge)**: Circle/Badge di sudut kanan atas berlabel `BAB / Chapter X` dengan nomor bab berukuran besar (font 26pt+) warna BPS Coral `#eb8a3c`.
2. **Banner Judul Bab (Bilingual)**: Banner Navy BPS `#0b3c5d` memuat Nama Bab Bahasa Indonesia dan Bahasa Inggris (*Italics* UPPERCASE).
3. **Visualisasi Grafik Infografis Tematik (Chart Block)**: Blok visualisasi khusus di bawah judul bab yang menyajikan grafik tematik sesuai topik bab:
   - **Bab 1 (Geografi & Pemerintahan)**: Horizontal Stacked Bar Distribusi Wilayah RT Per Dusun (Senggiring vs Benteng Raya).
   - **Bab 2 (Kependudukan & Demografi)**: SVG Donut Chart Komposisi Penduduk Laki-laki vs Perempuan & Center Value *Sex Ratio*.
   - **Bab 3 (Pendidikan & Adminduk)**: SVG Donut Chart Cakupan Kepemilikan KTP-el Usia ≥17 Tahun (98,31%).
   - **Bab 4 (Sosial & Kesejahteraan)**: Horizontal Bar Chart Distribusi Penerima Program Bansos (PKH, BPNT, BST/BLT).
   - **Bab 5 (Perumahan & Lingkungan)**: SVG Donut Chart Persentase Rumah Layak Huni (91,76%).

---

## 📘 IV. FORMAT HALAMAN PENJELASAN TEKNIS BAB (CHAPTER TECHNICAL NOTES)

### Aturan Baku Penjelasan Teknis Bab:
1. **Posisi Wajib**: Diletakkan tepat pada **Halaman Kedua setiap Bab** (setelah Halaman Sampul Bab / Infografis).
2. **Tata Letak 2-Kolom Berdampingan (Kiri-Kanan)**:
   - **Kolom Kiri**: Teks Bahasa Indonesia (`PENJELASAN TEKNIS`, font 14pt bold navy). Istilah konsep dicetak **Bold**.
   - **Kolom Kanan**: Teks Bahasa Inggris (`TECHNICAL NOTES`, font 14pt bold italic navy, text-align right). Istilah konsep dicetak ***Bold Italic***, naskah penjelasan dicetak *Italic* dengan pembatas garis vertikal tipis (`border-left: 1px solid #cbd5e1`).
3. **Mekanisme Tabel Tanpa Garis (Borderless HTML Table Standard)**:
   - **Wajib Menggunakan `<table>` Borderless**: Guna menjamin 100% sejajar horisontal di seluruh mesin pencetak PDF (Headless Chrome/Print Engine), daftar naskah Penjelasan Teknis **wajib disajikan dalam struktur HTML `<table>` tanpa garis (`border: none; border-collapse: collapse; width: 100%;`)**.
   - **Baris `<tr>` Per Pasangan Nomor**: Setiap nomor (misal 1. ID dan 1. EN) **wajib dibungkus dalam satu baris `<tr>` yang sama** dengan properti `vertical-align: top;`.
   - **Sel `<td>` Kiri & Kanan**:
     - `td` Kolom Kiri (`width: 50%; padding: 4px 12px 6px 0; border: none;`): Menampung nomor & penjelasan Bahasa Indonesia.
     - `td` Kolom Kanan (`width: 50%; padding: 4px 0 6px 12px; border: none; border-left: 1px solid #cbd5e1; font-style: italic; color: #475569;`): Menampung nomor & terjemahan Bahasa Inggris. Proper `border-left` pada `td` kanan secara otomatis membentuk garis pembatas vertikal yang tersambung sempurna dari atas ke bawah.
4. **Strict Formatting Rule**:
   - **DILARANG KERAS**: Menggunakan emoticon/emoji (misal `📌`) atau menggunakan box background/caption berwarna pada naskah resmi BPS. Latar belakang harus polos / transparan (`background: transparent; border: none;`).

---

## 📊 V. STANDARDISASI TATA LETAK & FORMAT TABEL BPS (MAIN & CONTINUED TABLE)

Format penulisan tabel BPS mematuhi tata aturan ketat mengacu pada Pedoman BPS 2023/2026 (Gambar 38 Komponen Tabel):

### 1. Blok Judul Tabel Utama (Main Table Title Block - Gambar 38 BPS)
Sesuai dengan spesifikasi resmi BPS (Gambar 38 Pedoman BPS 2023/2026), judul tabel wajib disusun dalam **Struktur Tabel HTML 3-Kolom Tanpa Garis (`table.table-title-block`)** untuk menjamin presisi posisi vertical-align top pada seluruh browser/PDF renderer:

```html
<table class="table-title-block">
  <tbody>
    <tr>
      <td class="table-label-td">
        <span class="table-label-title">Tabel</span>
        <span class="table-label-sub">Table</span>
      </td>
      <td class="table-num-td">1.1.1</td>
      <td class="table-name-td">
        <div class="table-name-id">Luas Daerah dan Jumlah Pulau Menurut Kabupaten/Kota, 2025</div>
        <div class="table-name-en">Total Area and Number of Islands by Regency/Municipality, 2025</div>
      </td>
    </tr>
  </tbody>
</table>
```

#### Spesifikasi Elemen Judul Tabel:
- **`td.table-label-td`**: Kolom 1 (lebar 45px). Memuat `Tabel` dengan garis bawah tipis (`border-bottom: 1.5px solid #1a202c`), `font-weight: 700; font-size: 8.5pt;` dan `Table` *italic* di bawahnya (`font-style: italic; font-weight: 400;`).
- **`td.table-num-td`**: Kolom 2 (lebar 55px). Memuat nomor kode tabel (contoh: `1.1.1`), `font-weight: 800; font-size: 11pt; color: #1a202c;`.
- **`td.table-name-td`**: Kolom 3.
  - Baris 1 (`.table-name-id`): Judul Bahasa Indonesia (`font-size: 9pt; font-weight: 700; color: #1a202c;`).
  - Baris 2 (`.table-name-en`): Judul Bahasa Inggris (`font-size: 9pt; font-weight: 700; font-style: italic; color: #1a202c;`).

#### Aturan Penulisan Teks Judul Tabel:
- **Tanpa Titik di Akhir**: Judul tabel tidak diakhiri tanda titik (`.`).
- **Capitalize Each Word**: Huruf pertama setiap kata ditulis kapital, kecuali kata sambung/depan.
- **Keterangan Waktu**: Didahului tanda koma (contoh: `, 2026`). Kata "Tahun/Bulan" tidak perlu ditulis. Rentang waktu menggunakan *En Dash* `–` tanpa spasi (contoh: `2018–2022`).
- **Satuan Data**: Ditulis menggunakan huruf kecil sebelum keterangan waktu, contoh: `(%), 2026` atau `(ribu ton), 2026`.

---

### 2. Header Kolom & Nomor Kolom (`<thead>`)
- **Header Kolom Utama (`th.main-header`)**: Latar solid BPS Coral/Orange (`#eb8a3c`) atau Navy (`#0b3c5d`), font putih bold 8.5pt.
- **Baris Nomor Kolom (`th.col-num`)**: Baris khusus bernomor `(1)`, `(2)`, `(3)`, ... dengan latar shading pastel (`#fdebd0`), font cokelat tua `#78350f` 8pt bold.

---

### 3. Baris Data & Baris Total (`<tbody>`)
- **Zebra Stripping**: Baris ganjil putih (`#ffffff`), baris genap warm tint soft cream (`#fff5eb`).
- **Presisi Sel Data**: Setiap kolom `<th>` pada header wajib memiliki sel `<td>` yang terisi penuh (tidak boleh ada kolom kosong di ujung kanan tabel).
- **Baris Total / Jumlah (`tr.total-row`)**:
  - Background Solid Coral/Orange (`#eb8a3c`), font putih bold 800.
  - Teks Total Bilingual: `DESA SUNGAI BAKAU KECIL / SUNGAI BAKAU KECIL VILLAGE` atau `JUMLAH / TOTAL`.

---

### 4. Judul Lanjutan Tabel (Continued Table Format)
Apabila tabel bersambung ke halaman berikutnya:

- **Format Judul Lanjutan**: Wajib menggunakan teks inline bold italic tanpa blok terpisah:
  ```html
  <p style="font-weight: 800; font-style: italic; font-size: 9pt; color: #1a202c; margin: 0 0 8px 0;">
    Lanjutan Tabel/<em>Continued Table</em> 1.1.1
  </p>
  ```
- **Header Kolom Berulang**: Seluruh header kolom dan baris nomor kolom `(1)`, `(2)`, `(3)` **wajib diulang secara presisi** di halaman lanjutan.

---

### 5. Catatan Kaki & Sumber Data (Meta Area)
Diletakkan di bagian kiri bawah di bawah baris total tabel:
```html
<div class="table-meta">
  <div class="meta-row">
    <div class="meta-lbl">Catatan/<i>Note:</i></div>
    <div>Data keadaan Rukun Tetangga (RT) per Juni 2026 / <i>RT condition data as of June 2026</i></div>
  </div>
  <div class="meta-row">
    <div class="meta-lbl">Sumber/<i>Source:</i></div>
    <div>BPS Kabupaten Mempawah — Pendataan Desa Cantik SBK 2026 / <i>BPS-Statistics of Mempawah Regency — 2026 SBK Desa Cantik Data Collection</i></div>
  </div>
</div>
```

---

## 📝 VI. FORMAT ULASAN DESKRIPTIF & TATA ATURAN BAHASA

### 1. Format Ulasan Deskriptif Bab (Narrative Analysis)
- Disajikan dalam format **2 Kolom Berdampingan (Kiri-Kanan)**:
  - **Kolom Kiri**: Judul ulasan (e.g. `ULASAN DESKRIPTIF GEOGRAFIS`, font 8.8pt bold navy) & paragraf Bahasa Indonesia (normal).
  - **Kolom Kanan**: Judul ulasan (e.g. `NARRATIVE ANALYSIS`, font 8.8pt italic navy) & paragraf Bahasa Inggris (*Italics* dengan `border-left: 1px solid #cbd5e1`).
- **Strict Rule**: Latar belakang harus transparan (`background: transparent; border: none; padding: 0;`), **dilarang keras menggunakan emoticon/emoji** atau box background berwarna.

---

## 📑 VI-B. STANDARDISASI FACING PAGES RUNNING HEADER & FOOTER BPS (STATISTIK INDONESIA 2026 STANDARD)

Sesuai **Contoh Resmi Publikasi BPS (Statistik Indonesia 2026 / Statistical Yearbook of Indonesia 2026)**, tata letak Header dan Footer publikasi BPS dwibahasa disusun presisi berdasarkan mekanisme **Halaman Berhadapan (*Facing Pages*)**:

### 1. Halaman Genap / Verso (Sisi Kiri saat Buku Dibuka)
- **Running Header (Atas Kiri / `text-align: left`)**: Blok 2 baris warna Oranye BPS (`#eb8a3c`):
  - Baris 1: `DESA SUNGAI BAKAU KECIL DALAM ANGKA 2026` (*Uppercase Bold*)
  - Baris 2: `SUNGAI BAKAU KECIL VILLAGE IN FIGURES 2026` (*Uppercase Bold Italic*)
  ```html
  <div class="running-header even">
    <div>DESA SUNGAI BAKAU KECIL DALAM ANGKA 2026</div>
    <div class="en">SUNGAI BAKAU KECIL VILLAGE IN FIGURES 2026</div>
  </div>
  ```
- **Running Footer (Bawah Kiri / `text-align: left`)**: Nomor Halaman bersih tanpa box:
  ```html
  <div class="running-footer even">18</div>
  ```

### 2. Halaman Ganjil / Rekto (Sisi Kanan saat Buku Dibuka)
- **Running Header (Atas Kanan / `text-align: right`)**: Blok 2 baris warna Oranye BPS (`#eb8a3c`):
  - Baris 1: `GEOGRAFI DAN PEMERINTAHAN` (*Uppercase Bold*)
  - Baris 2: `GEOGRAPHY AND GOVERNMENT` (*Uppercase Bold Italic*)
  ```html
  <div class="running-header odd">
    <div>GEOGRAFI DAN PEMERINTAHAN</div>
    <div class="en">GEOGRAPHY AND GOVERNMENT</div>
  </div>
  ```
- **Running Footer (Bawah Kanan / `text-align: right`)**: Nomor Halaman bersih tanpa box:
  ```html
  <div class="running-footer odd">17</div>
  ```

### 3. CSS Positioning Rules untuk Running Footer
```css
.running-footer {
  position: absolute;
  bottom: 10mm;
  left: 15mm;
  right: 15mm;
  font-size: 10pt;
  font-weight: 700;
  color: #eb8a3c;
  background: transparent;
}
```
*Note*: `bottom: 10mm; left: 15mm; right: 15mm;` wajib digunakan (bukan `bottom: 0`) agar nomor halaman sejajar dengan margin isi (15mm) dan memberi jarak aman 10mm di atas tepi bawah kertas A4.

### 4. Pengecualian Pencetakan Header & Footer (Subbab 4.1.3 Poin 9)
- **Cover Depan**, **Halaman Tim Penyusun**, dan **Halaman Pembatas Bab (*Chapter Cover Infographic Cards*)** **DILARANG DICANTUMKAN RUNNING HEADER & NOMOR HALAMAN**, namun tetap dihitung nomor halamannya.

---

## 🏷️ VI-C. STANDARDISASI PENAMAAN JUDUL BAB & SUBBAB BPS (STATISTIK INDONESIA 2026 STANDARD)

Berdasarkan halaman acuan **Daftar Tabel (List of Tables) Publikasi Resmi BPS (Statistik Indonesia 2026)**, penamaan Judul Bab dan Subbab disusun dengan aturan tata tulis sebagai berikut:

### 1. Format Judul Bab Utama (Chapter Level)
- **Format**: `[Nomor Bab].   [JUDUL BAB INDONESIA]/[JUDUL BAB INGGRIS]`
- **Styling**: **UPPERCASE BOLD** (`font-weight: 700`). Naskah Bahasa Inggris ditulis miring (*Italic*). Kedua bahasa dipisahkan oleh tanda `/` (slash).
- **Contoh**: `1.   GEOGRAFI DAN PEMERINTAHAN/GEOGRAPHY AND GOVERNMENT`

### 2. Format Judul Subbab / Seksi & Penjelasan Teknis (Sub-Chapter Level)
- **Format Judul Penjelasan Teknis (Centered Layout)**:
  ```html
  <div style="text-align: center; margin-bottom: 20px;">
    <h2 style="font-size: 14pt; font-weight: 800; margin: 0; color: #0b3c5d;">PENJELASAN TEKNIS</h2>
    <h2 style="font-size: 11pt; font-weight: 800; font-style: italic; margin: 2px 0 0 0; color: #0b3c5d;">TECHNICAL NOTES</h2>
  </div>
  ```
- **Format Kata Pengantar & Preface (2-Page Facing Pages Standard)**:
  - **Halaman iv (Halaman Genap/Kiri)**: `KATA PENGANTAR` (Full Naskah Bahasa Indonesia, Judul Centered `14pt Bold Navy`, Paragraf Terindentasi, Tempat/Tanggal `Sungai Bakau Kecil, Agustus 2026`, dan Blok Tanda Tangan Tunggal `PEMERINTAH DESA SUNGAI BAKAU KECIL — Plt. KEPALA DESA — RIANDI PRAYUDA`).
  - **Halaman v (Halaman Ganjil/Kanan)**: `PREFACE` (Full Naskah Bahasa Inggris *Italics*, Judul Centered `14pt Bold Italic Navy`, Paragraf Terindentasi *Italics*, Date Line `Sungai Bakau Kecil, August 2026`, dan Blok Tanda Tangan Tunggal `GOVERNMENT OF SUNGAI BAKAU KECIL VILLAGE — ACTING HEAD OF VILLAGE — RIANDI PRAYUDA`).
- **Rule Layout Bebas Garis Pembatas (Clean Minimalist)**: Sesuai standar BPS 2026, area Judul Subbab (`.section-header`), Ulasan Deskriptif, Halaman *Front Matter*, dan Halaman Penjelasan Teknis (`PENJELASAN TEKNIS / TECHNICAL NOTES`) **tidak menggunakan garis pembatas horizontal (`border-bottom`) maupun vertikal (`border-left`)**, sehingga tampilan halaman bersih, lega, dan estetis.
- **Format Penjelasan Umum (Explanatory Notes Standard)**:
  - **Judul**: Centered `PENJELASAN UMUM/EXPLANATORY NOTES`
  - **Paragraf Pembuka**: Disusun bertingkat dwibahasa (Bahasa Indonesia reguler & Bahasa Inggris *Italics*).
  - **Seksi 1 (1. TANDA-TANDA/SYMBOLS)**: Memuat daftar simbol resmi BPS (`...`, `-`, `~0`, `,`, `NA`, `e`, `r`, `*`) yang dihubungkan menggunakan garis titik-titik (*leader dots* `border-bottom: 1px dotted #cbd5e1;`).
  - **Seksi 2 (2. SATUAN/UNITS)**: Rincian daftar satuan pengukuran yang digunakan dalam publikasi.
  - **Disclaimer Pembulatan**: Ditutup dengan pernyataan dwibahasa: *"Perbedaan angka di belakang koma disebabkan oleh pembulatan angka / The difference in decimal numbers is caused by rounding."*
- **Format Penyelarasan Angka Baku BPS (BPS Indonesian Numbering Rules Standard)**:
  - **Tanda Desimal**: Menggunakan tanda koma (`,`), contoh: `103,68`, `98,31`, `91,76`, `4,16`.
  - **Pemisah Ribuan**: Menggunakan tanda titik (`.`), contoh: `5.701`, `2.902`, `2.799`, `1.661`, `4.090`, `4.021`, `1.371`, `1.258`.
  - **Nilai Nol / Tidak Ada Data**: Dituliskan dengan tanda strip (`-`).
- **Vertical Centering Lanjutan Tabel Tunggal (`margin: auto 0`)**: Jika suatu halaman berdiri sendiri hanya memuat 1 blok lanjutan tabel (`Lanjutan Tabel / Continued Table X.Y.Z`), seluruh kontainer lanjutan tabel dibungkus `<div style="margin: auto 0;">` agar otomatis terpusat secara vertikal di tengah halaman antara *Running Header* (atas) dan *Running Footer* (bawah) untuk meminimalisasi ruang kosong berlebih di bagian bawah.
- **Styling**:
  - Baris 1 (Bahasa Indonesia): **UPPERCASE BOLD** (`font-weight: 800`).
  - Baris 2 (Bahasa Inggris): **UPPERCASE BOLD ITALIC** (`font-style: italic; font-weight: 800`).
  - Warna font: BPS Primary Navy (`#0b3c5d`) atau BPS Coral (`#eb8a3c`).

---

| Elemen Desain | Kode Warna (HEX) | Penggunaan / Keterangan |
| :--- | :--- | :--- |
| **BPS Coral/Orange Header** | `#eb8a3c` / `#d97706` | Header Tabel Utama, Baris Total, Running Header/Footer |
| **BPS Primary Navy** | `#0b3c5d` / `#1e3a8a` | Header Cover, Judul Bab Utama, Subbab Header |
| **Column Number Shading** | `#fdebd0` / `#fcd34d` | Latar belakang baris nomor kolom `(1)`, `(2)`, `(3)` |
| **Table Alt Row (Zebra)** | `#fff5eb` / `#f8fafc` | Latar belakang baris tabel genap |
| **Page Card Border / Line** | `#e2e8f0` / `#cbd5e1` | Garis tepi tabel, divider 2-kolom, running header border |
| **Text Utama (Body & Sel)** | `#1a202c` / `#2d3748` | Teks paragraf narasi deskriptif & angka sel tabel (Hitam Netral) |

### 🎨 VII-B. ATURAN WARNA TEKS & KONTRASTING BPS
1. **Body Text & Sel Angka**: Menggunakan warna **Hitam Netral (`#1a202c` / `#2d3748`)** di atas latar belakang terang/putih untuk menjamin *contrast ratio* dan keterbacaan (*readability*) maksimal (bebas dari kelelahan mata pembaca).
2. **Elemen Aksen Berwarna**: Warna Oranye BPS (`#eb8a3c`) dan Navy BPS (`#0b3c5d`) diperbolehkan dan digunakan pada kover, infografis, running header/footer, subbab header, dan shading header tabel.
3. **Nama BPS Penerbit**: Wajib disajikan dalam warna **Biru BPS (`#0080ff`)**, **Hitam**, atau **Putih** di sebelah kanan logo resmi.

---

---

## 💻 VIII. CODE TEMPLATE HTML5 & PRINT CSS A4 (FULL REFERENCE)

Berikut adalah template CSS + HTML5 baku yang digunakan oleh Agentic AI untuk memproduksi publikasi BPS:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

@page {
  size: A4;
  margin: 10mm 15mm 12mm 15mm;
}

* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}

body {
  font-family: 'Inter', Arial, sans-serif;
  color: #2d3748;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
  font-size: 9.2pt;
  line-height: 1.45;
}

.page-container {
  max-width: 210mm;
  margin: 0 auto;
  background: #ffffff;
}

.page-card {
  width: 100%;
  height: 270mm;
  position: relative;
  page-break-after: always;
  page-break-inside: avoid;
  break-inside: avoid;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  padding: 2mm 0 0 0;
  overflow: hidden;
}

.page-content {
  flex: 1;
  padding-bottom: 30px;
}

/* Running Header & Footer */
.running-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 8.5pt;
  font-weight: 700;
  color: #eb8a3c;
  text-transform: uppercase;
  margin-bottom: 10px;
  border-bottom: 1.5px solid #fed7aa;
  padding-bottom: 4px;
}

.running-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1.5px solid #f1f5f9;
  padding-top: 5px;
  background: #ffffff;
  height: 25px;
}

.bps-pill-badge {
  background: #eb8a3c;
  color: #ffffff;
  font-weight: 700;
  font-size: 9pt;
  padding: 2px 14px;
  border-radius: 12px;
}

.footer-title-en {
  font-style: italic;
  color: #eb8a3c;
  font-weight: 600;
  font-size: 8.5pt;
  text-transform: uppercase;
}

/* Table Title Block (BPS Official 2023/2026 Spec) */
.table-title-block {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
}

.table-label {
  font-weight: 700;
  font-size: 8.5pt;
  color: #1a202c;
  border-bottom: 1.5px solid #1a202c;
  line-height: 1.3;
  white-space: nowrap;
  padding-bottom: 1px;
  flex-shrink: 0;
}

.table-label i {
  display: block;
  font-style: italic;
  font-weight: 400;
}

.table-num {
  font-weight: 800;
  font-size: 11pt;
  color: #1a202c;
  line-height: 1.2;
  flex-shrink: 0;
  padding-top: 1px;
}

.table-name {
  font-size: 9pt;
  font-weight: 400;
  color: #1a202c;
  line-height: 1.4;
}

.table-name .en-title {
  display: block;
  font-weight: 700;
  font-style: italic;
  color: #1a202c;
}

/* Table Specs */
table.bps-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 6px;
  font-size: 8.5pt;
}

table.bps-table th.main-header {
  background-color: #eb8a3c;
  color: #ffffff;
  padding: 5px 4px;
  border: 1px solid #d97706;
  text-align: center;
  font-weight: 700;
}

table.bps-table th.col-num {
  background-color: #fdebd0;
  color: #78350f;
  padding: 2px;
  border: 1px solid #fcd34d;
  text-align: center;
  font-size: 8pt;
  font-weight: 600;
}

table.bps-table td {
  padding: 4px 5px;
  border: 1px solid #e2e8f0;
}

table.bps-table tr:nth-child(even) td {
  background-color: #fff5eb;
}

table.bps-table tr.total-row td {
  background-color: #eb8a3c;
  color: #ffffff;
  font-weight: 800;
  border-top: 2px solid #d97706;
  border-bottom: 2px solid #d97706;
}

/* 2-Column Side-by-Side Narrative & Technical Notes */
.narrative-box {
  background: transparent;
  border: none;
  padding: 0;
  margin-bottom: 12px;
  font-size: 8.8pt;
  line-height: 1.45;
}

.narrative-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.narrative-col-id {
  color: #1a202c;
}

.narrative-col-en {
  border-left: 1px solid #cbd5e1;
  padding-left: 14px;
  color: #475569;
  font-style: italic;
}
```

---

## 🐍 IX. PYTHON GENERATOR SCRIPT STANDARD (AUTOMATION ENGINE)

AI Agent di repositori `knowledge-base` menggunakan skrip Python otomatisasi (misal: `scratch/generate_perfect_pub.py`) untuk mengekstrak data dari basis data/markdown dan menyusun seluruh `page-card` secara presisi.

### Prinsip Kerja Generator Script:
1. **Fungsi Extract Rows**: Mengekstrak seluruh 37 baris RT dari data mentah/HTML/CSV dan menyalin baris total (`tr.total-row`).
2. **Helper `make_page_card(header_en, badge, body_inner)`**: Membungkus setiap naskah/tabel ke dalam kontainer `.page-card` berukuran `270mm` dengan running header dan footer.
3. **Helper `build_chapter_html(...)`**: Membangun 5 halaman per bab:
   - Page 1: Chapter Cover Card (Infographics)
   - Page 2: Dedicated Penjelasan Teknis Bab (Technical Notes)
   - Page 3: Ulasan Deskriptif & Table Part 1 (Rows 1–12)
   - Page 4: Continued Table Part 2 (Rows 13–25)
   - Page 5: Continued Table Part 3 (Rows 26–37) + Baris Total & Catatan/Sumber

---

## 🛠️ X. ALUR EKSEKUSI & ZERO-OVERLAP PRINT BUDGET RULE

### 1. Perintah Eksekusi Kompilasi PDF Siap Cetak:
```bash
# 1. Jalankan Python Generator untuk menghasilkan HTML Publikasi
python3 scratch/generate_perfect_pub.py

# 2. Compile HTML ke PDF A4 Siap Cetak via Headless Chrome
# Gunakan flag --no-pdf-header-footer agar tanggal/URL browser tidak muncul
google-chrome-stable --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=outputs/publikasi-desa-sungai-bakau-kecil-dalam-angka-2026.pdf \
  kegiatan/desa-cantik/2026/sungai-bakau-kecil/publikasi-desa-sungai-bakau-kecil-dalam-angka-2026.html
```

### 2. Aturan Batas Baris Data per Halaman (Page Print Budget):
Untuk menjamin tidak terjadi penumpukan (*overlapping*) teks dengan running footer:
- **Halaman Pertama Bab (dengan Ulasan Deskriptif / Narrative Box)**: Maksimal **12 baris data**.
- **Halaman Lanjutan Tabel (*Continued Table*)**: Maksimal **13 s.d. 14 baris data**.
- **Halaman Lanjutan Akhir (dengan Baris Total & Meta Catatan/Sumber)**: Maksimal **12 baris data** + 1 baris total + 2 baris meta.

---

*Dokumen Pedoman Penyusunan Publikasi BPS ini dibakukan di repositori BPS Kabupaten Mempawah Basis Pengetahuan (`knowledge-base`) berdasarkan Pedoman Pembuatan Publikasi BPS Katalog 1303004 Edisi 2023 / Revisi 2026.*
