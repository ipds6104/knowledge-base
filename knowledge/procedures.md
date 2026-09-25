# 📋 Standar Operasional & Alur Kerja BPS Kabupaten Mempawah

## 1. SOP Penomoran & Registrasi Surat Keluar Dinas BPS Kabupaten Mempawah
- **Buku Agenda Penomoran Resmi**: Setiap pembuatan surat dinas keluar resmi dari BPS Kabupaten Mempawah **WAJIB** mengambil dan mem-booking nomor surat dari Google Spreadsheet Buku Agenda Surat BPS Mempawah:
  * URL: `https://docs.google.com/spreadsheets/d/1kbvTnpEwlyt6HbtIlD7at-Eg7zgTUt7GUHP9uJx2wgA/edit?usp=drivesdk`
  * Spreadsheet ID: `1kbvTnpEwlyt6HbtIlD7at-Eg7zgTUt7GUHP9uJx2wgA`
  * Sheet Target: `Surat Keluar 2026` (atau sesuai tahun berjalan)
- **Struktur Format Nomor Surat BPS**:
  `B-[Nomor Urut]/[Kode Satker]/[Kode Klasifikasi Arsip]/[Bulan (opsional)]/[Tahun]`
  * `B-`: Sifat naskah dinas biasa
  * `[Nomor Urut]`: Running number berurutan dari baris terakhir terisi pada kolom `Nomor Surat`
  * `[Kode Satker]`:
    - `61040`: Pimpinan / Kepala BPS Kabupaten Mempawah
    - `61041`: Subbagian Umum / Tata Usaha
    - `61042`: Fungsi Statistik Sosial
    - `61043`: Fungsi Statistik Produksi
    - `61044`: Fungsi Statistik Distribusi
    - `61045`: Fungsi Neraca Wilayah dan Analisis Statistik (Nerwilis)
    - `61046`: Fungsi Integrasi Pengolahan dan Diseminasi Statistik (IPDS)
  * `[Kode Klasifikasi Arsip]`: Mengacu pada tab sheet `Klasifikasi` / `Klasifikasi_1` (misal `SS.190` untuk Koordinasi Sensus, `HM.310` untuk Permintaan Data/Publikasi, `VS.220` untuk Pelatihan Survei, `KS.200` untuk Rilis Publikasi, dsb.).
  * `[Tahun]`: Tahun naskah dinas (misal `2026`).
- **Alur Pengambilan Nomor Surat**:
  1. Buka spreadsheet `Agenda Surat BPS Mempawah` (`1kbvTnpEwlyt6HbtIlD7at-Eg7zgTUt7GUHP9uJx2wgA`).
  2. Buka tab `Surat Keluar <Tahun>` (misal `Surat Keluar 2026`).
  3. Cari baris paling akhir yang terisi di kolom C (`Nomor Surat`).
  4. Ambil nomor urut berikutnya (misal baris terakhir 1107 -> ambil 1108).
  5. Booking baris baru tersebut dengan mengisi: Tanggal Surat, Nomor Surat lengkap, Perihal, Tujuan, Pembuat (Tim Kerja), dan Nama File/Lampiran.
  6. Cantumkan nomor resmi tersebut pada naskah surat dinas dan lampirannya.

## 2. Standar Layout & Format Kop Surat Dinas Keluar BPS Kabupaten Mempawah
Seluruh pembuatan surat dinas/surat keluar BPS Kabupaten Mempawah (untuk konteks apapun di masa depan) **WAJIB** mematuhi format dan layout standar berikut:
- **Komposisi Kolom Kop**:
  * **Logo Kiri**: Logo resmi BPS (lebar ~54pt s.d. 60px).
  * **Teks Instansi & Alamat (Tengah/Kiri)**: Berada tepat di sebelah kanan logo BPS dengan jarak proporsional (*gutter / left padding* ~12–14px), format **rata kiri (*left-aligned*)**, mencakup:
    - Baris 1: `BADAN PUSAT STATISTIK` (Font Liberation Sans / Arial, 13pt, **Bold**, *Italic*, warna navy `#0a2540`).
    - Baris 2: `KABUPATEN MEMPAWAH` (Font Liberation Sans / Arial, 13pt, **Bold**, *Italic*, warna navy `#0a2540`).
    - Baris 3–4: Alamat lengkap, kontak telepon, laman web, dan email resmi (Font 8pt, regular, warna `#222222`).
      `Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;`
      `Laman: https://mempawahkab.bps.go.id; Pos-el: bps6104@bps.go.id`
  * **Logo Kanan**: Logo kegiatan spesifik (misal Logo SE2026 lebar ~86pt) atau dikosongkan untuk surat dinas umum.
- **Garis Pembatas Kop**: Garis horizontal tebal 2pt warna navy `#0a2540` sepanjang margin halaman (100% width).
- **Tanda Tangan & Cap**: Bagian penutup surat menyematkan tanda tangan resmi Kepala BPS Kabupaten Mempawah (Munawir, S.E., M.M.).
- **Jumlah Halaman**: Diatur rapi dan presisi tanpa baris menggantung (*orphan lines*). Untuk surat dengan lampiran matriks variabel, naskah surat dinas berada di Halaman 1 dan lampiran matriks data di Halaman 2.

