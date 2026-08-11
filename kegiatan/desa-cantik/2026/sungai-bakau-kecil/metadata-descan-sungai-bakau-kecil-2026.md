# METADATA STATISTIK SEKTORAL
## Satu Data Indonesia (SDI) - Desa Cantik 2026
**Desa Sungai Bakau Kecil, Kabupaten Mempawah**

---

## 📅 I. METADATA KEGIATAN (MS-KEGIATAN)

| No | Elemen Metadata | Keterangan / Nilai |
| :--- | :--- | :--- |
| **1** | **Nama Kegiatan** | Pendataan Potensi Kewilayahan Rukun Tetangga (RT) dan Inventarisasi Fasilitas Umum Desa Cantik Sungai Bakau Kecil 2026 |
| **2** | **Instansi Penyelenggara** | Pemerintah Desa Sungai Bakau Kecil bekerjasama dengan BPS Kabupaten Mempawah |
| **3** | **Jenis Kegiatan** | Pendataan Langsung |
| **4** | **Tujuan Kegiatan** | Memetakan kondisi sosial-ekonomi penduduk di tingkat RT serta kondisi kelayakan sarana prasarana desa untuk mendukung kebijakan pembangunan berbasis bukti (evidence-based policy). |
| **5** | **Cara Pengumpulan Data** | Wawancara langsung dengan Ketua RT (Agregat RT) dan observasi lapangan titik koordinat fasilitas desa menggunakan aplikasi mobile AppSheet. |
| **6** | **Cakupan Wilayah** | Seluruh wilayah Desa Sungai Bakau Kecil (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 37 Rukun Tetangga (RT) dan 3 Dusun (Dusun Senggiring, Dusun Benteng Raya, Dusun Sepakat). |
| **7** | **Unit Pengamatan** | Rukun Tetangga (RT), Sarana Prasarana (Fasilitas Umum) |
| **8** | **Frekuensi Kegiatan** | Tahunan (Annual) |
| **9** | **Waktu Pelaksanaan** | Juni - Juli 2026 (Pengumpulan Lapangan), Agustus 2026 (Diseminasi & Integrasi Web) |
| **10** | **Media Rilis** | Portal Web Desa Cantik Sungai Bakau Kecil & Publikasi Desa Sungai Bakau Kecil Dalam Angka 2026 |

---

## 📊 II. METADATA VARIABEL (MS-VARIABEL)

### A. Tabel Variabel Tingkat Rukun Tetangga (Daftar_RT)

| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Klasifikasi / Rentang Nilai |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Nama_RT` | Wilayah Administrasi | Nama rukun tetangga tempat pengumpulan data CAPI dilakukan. | - | String | Nama RT Tekstual |
| 2 | `Nama_Petugas` | Petugas Pendata | Nama petugas pembina/agen statistik yang menginput data. | - | String | Nama Petugas |
| 3 | `Tanggal_Waktu` | Waktu Pencacahan | Tanggal dan waktu observasi dilakukan. | - | DateTime | YYYY-MM-DD HH:MM:SS |
| 4 | `Nama_Ketua_RT` | Identitas RT | Nama Ketua RT aktif yang bertindak sebagai narasumber. | - | String | Nama Ketua RT |
| 5 | `Jumlah_Penduduk_Laki_Laki` | Penduduk Laki-Laki | Jumlah penduduk berjenis kelamin laki-laki di RT. | Orang | Integer | Nilai >= 0 |
| 6 | `Jumlah_Penduduk_Perempuan` | Penduduk Perempuan | Jumlah penduduk berjenis kelamin perempuan di RT. | Orang | Integer | Nilai >= 0 |
| 7 | `Jumlah_Bumbung_Rumah` | Bangunan Fisik | Jumlah atap/bangunan fisik tempat tinggal di RT. | Unit | Integer | Nilai >= 0 |
| 8 | `Jumlah_KK` | Rumah Tangga / KK | Jumlah kepala keluarga di RT. | Keluarga | Integer | Nilai >= 0 |
| 9 | `Jumlah_Penduduk_Lansia` | Penduduk Lansia | Jumlah penduduk berusia 60 tahun ke atas di RT. | Orang | Integer | Nilai >= 0 |
| 10 | `Jumlah_Kelahiran_Bayi` | Kelahiran | Jumlah bayi lahir hidup dalam 1 tahun terakhir. | Bayi | Integer | Nilai >= 0 |
| 11 | `Jumlah_Kematian` | Kematian | Jumlah kematian penduduk dalam 1 tahun terakhir. | Orang | Integer | Nilai >= 0 |
| 12 | `Jumlah_Penerima_PKH` | Bansos PKH | Jumlah penduduk penerima PKH di RT. | Orang | Integer | Nilai >= 0 |
| 13 | `Jumlah_Penerima_BPNT` | Bansos BPNT | Jumlah penduduk penerima BPNT di RT. | Orang | Integer | Nilai >= 0 |
| 14 | `Jumlah_Penerima_BST` | Bansos BST | Jumlah penduduk penerima BST di RT. | Orang | Integer | Nilai >= 0 |
| 15 | `Jumlah_Penerima_BLT` | Bansos BLT | Jumlah penduduk penerima BLT di RT. | Orang | Integer | Nilai >= 0 |
| 16 | `Jumlah_Memiliki_KTP` | Administrasi KTP | Jumlah penduduk wajib KTP yang sudah memiliki KTP-el fisik. | Orang | Integer | Nilai >= 0 |
| 17 | `Jumlah_Sekolah_TK` | Pendidikan TK | Jumlah penduduk menempuh pendidikan TK/PAUD. | Orang | Integer | Nilai >= 0 |
| 18 | `Jumlah_Sekolah_SD` | Pendidikan SD | Jumlah penduduk menempuh pendidikan SD/MI. | Orang | Integer | Nilai >= 0 |
| 19 | `Jumlah_Sekolah_SMP` | Pendidikan SMP | Jumlah penduduk menempuh pendidikan SMP/MTs. | Orang | Integer | Nilai >= 0 |
| 20 | `Jumlah_Sekolah_SMA` | Pendidikan SMA | Jumlah penduduk menempuh pendidikan SMA/MA/SMK. | Orang | Integer | Nilai >= 0 |
| 21 | `Jumlah_Sekolah_Sarjana` | Pendidikan Tinggi | Jumlah penduduk lulusan Diploma/Sarjana. | Orang | Integer | Nilai >= 0 |
| 22 | `Jumlah_Penduduk_Putus_Sekolah` | Putus Sekolah | Jumlah anak usia sekolah (7-18 thn) yang tidak sekolah. | Orang | Integer | Nilai >= 0 |
| 23 | `Jumlah_Anak_Usia_0_1_Tahun` | Kategori Bayi | Jumlah anak berusia di bawah 1 tahun. | Anak | Integer | Nilai >= 0 |
| 24 | `Jumlah_Anak_Usia_2_5_Tahun` | Kategori Balita | Jumlah anak berusia antara 2 s.d. 5 tahun. | Anak | Integer | Nilai >= 0 |
| 25 | `Jumlah_Pendatang` | Migrasi Masuk | Jumlah penduduk baru pindah masuk ke RT. | Orang | Integer | Nilai >= 0 |
| 26 | `Status_Pendataan` | Metodologi CAPI | Status kelengkapan pengisian data CAPI. | - | String | Sudah Selesai, Belum Terdata |

### B. Tabel Variabel Tingkat Sarana Prasarana (Fasilitas)

| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Pilihan Isian / Keterangan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ID_Fasilitas` | Identitas Sarana | Kode pengenal unik setiap fasilitas. | - | String | Kode Alfanumerik |
| 2 | `Nama_Petugas` | Petugas Pendata | Nama petugas pembina/agen statistik yang menginput data. | - | String | Nama Petugas |
| 3 | `Tanggal_Waktu` | Waktu Pencacahan | Tanggal dan waktu observasi dilakukan. | - | DateTime | YYYY-MM-DD HH:MM:SS |
| 4 | `Lokasi_GPS` | Geospasial | Titik koordinat latitude dan longitude lokasi fasilitas. | - | String | Koordinat Geografis |
| 5 | `Foto_Fasilitas` | Visual | Lampiran foto kondisi fasilitas. | - | String | Path Berkas Gambar |
| 6 | `RT` | Wilayah Administrasi | Nama rukun tetangga tempat pengumpulan data dilakukan. | - | String | Nama RT Tekstual |
| 7 | `Nama_Fasilitas` | Nama Sarana | Nama resmi fasilitas. | - | String | Nama Tekstual |
| 8 | `Kategori_Fasilitas` | Klasifikasi Sarana | Kategori utama fasilitas. | - | String | Ibadah, Pendidikan, Kesehatan, Ekonomi, Pemerintahan, dll. |
| 9 | `Sub_Kategori` | Sub-Klasifikasi | Rincian jenis sarana prasarana. | - | String | Masjid, SD, Posyandu, Toko, dll. |
| 10 | `Kondisi_Bangunan` | Kualitas Fisik | Kelayakan fisik bangunan sarana. | - | String | Baik, Rusak Ringan, Rusak Berat |
| 11 | `Sumber_Listrik` | Utilitas Listrik | Sumber pasokan daya listrik utama sarana. | - | String | PLN 24 Jam, Non-PLN, dll. |
| 12 | `Sumber_Air_Bersih` | Utilitas Air | Sumber penyediaan air bersih utama sarana. | - | String | PDAM/PAMSIMAS, Sumur Bor, dll. |
| 13 | `Akses_Jalan` | Infrastruktur | Jenis permukaan jalan terdekat. | - | String | Aspal/Beton, Batu, Jalan Tanah |
| 14 | `Sinyal_Seluler` | Telekomunikasi | Kekuatan sinyal telekomunikasi seluler. | - | String | Sangat Baik (4G/LTE), Cukup, dll. |
| 15 | `Catatan` | Informasi Tambahan | Catatan temuan khusus petugas. | - | String | Narasi Bebas |

---

## 📈 III. METADATA INDIKATOR (MS-INDIKATOR)

| No | Nama Indikator | Definisi | Rumus / Formula Kalkulasi | Satuan | Ukuran / Klasifikasi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Rasio Jenis Kelamin (Sex Ratio)** | Perbandingan jumlah penduduk laki-laki dengan 100 penduduk perempuan di desa tersebut. | $$frac(sum "L", sum "P") * 100$$ | Persen | Demografi |
| **2** | **Rata-rata Anggota Rumah Tangga (ART)** | Rata-rata banyaknya anggota keluarga yang mendiami satu rumah tangga/KK. | $$frac(sum "L" + sum "P", sum "KK")$$ | Orang per Keluarga | Kesejahteraan / Demografi |
| **3** | **Persentase Penduduk Lansia** | Proporsi jumlah lansia terhadap total penduduk desa. | $$frac(sum "Lansia", "Total Penduduk") * 100$$ | Persen | Demografi / Kelompok Rentan |
| **4** | **Persentase Kepemilikan KTP-el** | Proporsi jumlah penduduk yang telah memiliki KTP fisik dari total penduduk wajib KTP. | $$frac(sum "KTP", "Total Wajib KTP") * 100$$ | Persen | Administrasi Kependudukan |
| **5** | **Persentase Penerima Bantuan Sosial** | Proporsi penduduk yang terdaftar sebagai penerima bantuan sosial (PKH, BPNT, BLT) terhadap total penduduk. | $$frac(sum "Bansos", "Total Penduduk") * 100$$ | Persen | Kesejahteraan Rakyat |
| **6** | **Persentase Anak Putus Sekolah** | Proporsi anak usia sekolah (7-18 tahun) yang tidak bersekolah terhadap total anak usia sekolah. | $$frac(sum "Putus Sekolah", "Total Usia Sekolah") * 100$$ | Persen | Pendidikan |
| **7** | **Kepadatan Hunian Rumah** | Rata-rata jumlah penduduk yang menghuni setiap bangunan fisik tempat tinggal. | $$frac("Total Penduduk", sum "Bangunan")$$ | Orang per Unit | Infrastruktur / Kesehatan |
| **8** | **Rasio Sarana Keagamaan per 1000 Penduduk** | Ketersediaan sarana tempat ibadah desa untuk setiap 1.000 jiwa penduduk. | $$frac("Sarana Keagamaan", "Total Penduduk") * 1000$$ | Unit per 1000 Jiwa | Sosial / Agama |
