# METADATA STATISTIK SEKTORAL
## Satu Data Indonesia (SDI) - Desa Cantik 2026
**Kelurahan Pasir Wan Salim, Kabupaten Mempawah**

---

## 📅 I. METADATA KEGIATAN (MS-KEGIATAN)

| No | Elemen Metadata | Keterangan / Nilai |
| :--- | :--- | :--- |
| **1** | **Nama Kegiatan** | Pendataan Sosial Keluarga Kelurahan Pasir Wan Salim 2026 |
| **2** | **Instansi Penyelenggara** | Pemerintah Kelurahan Pasir Wan Salim bekerjasama dengan BPS Kabupaten Mempawah |
| **3** | **Jenis Kegiatan** | Pendataan Langsung |
| **4** | **Tujuan Kegiatan** | Memetakan kondisi sosial-ekonomi penduduk di tingkat RT/RW untuk mendukung kebijakan pembangunan berbasis bukti (evidence-based policy). |
| **5** | **Cara Pengumpulan Data** | Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga menggunakan aplikasi mobile AppSheet. |
| **6** | **Cakupan Wilayah** | Seluruh wilayah Kelurahan Pasir Wan Salim (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 17 Rukun Tetangga (RT) dan 8 Rukun Warga (RW 01 s.d. RW 08). |
| **7** | **Unit Pengamatan** | Bangunan Tempat Tinggal Biasa / Keluarga (CAPI) |
| **8** | **Frekuensi Kegiatan** | Tahunan (Annual) |
| **9** | **Waktu Pelaksanaan** | Juni - Juli 2026 (Pengumpulan Lapangan), Agustus 2026 (Diseminasi & Integrasi Web) |
| **10** | **Media Rilis** | Portal Web Kelurahan Cantik Pasir Wan Salim & Publikasi Kelurahan Pasir Wan Salim Dalam Angka 2026 |

---

## 📊 II. METADATA VARIABEL (MS-VARIABEL)

### A. Tabel Variabel Data Mikro Bangunan Tempat Tinggal Biasa & Rumah Tangga CAPI

| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Pilihan Isian / Keterangan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Nama_RT` | Wilayah Administrasi | Nama rukun tetangga tempat pengumpulan data CAPI dilakukan. | - | String | Nama RT Tekstual |
| 2 | `ID_Rumah` | Identitas Rumah | Kode pengenal unik unit rumah. | - | String | Kode Alfanumerik |
| 3 | `Lokasi_Geotagging` | Geospasial | Titik koordinat presisi latitude dan longitude lokasi fisik rumah. | - | String | Latitude, Longitude (LatLong) |
| 4 | `Nama_Kepala_Keluarga` | Identitas Responden | Nama lengkap Kepala Keluarga utama yang mendiami rumah. | - | String | Nama Lengkap Tekstual |
| 5 | `Nomor_WhatsApp_ART` | Komunikasi | Nomor kontak telepon/WhatsApp anggota keluarga. | - | String | Nomor Telepon |
| 6 | `Jumlah_Kartu_Keluarga` | Rumah Tangga / KK | Banyaknya Kartu Keluarga (KK) yang mendiami rumah. | Keluarga | Integer | Nilai >= 1 |
| 7 | `Jenis_Kelamin_KK_Laki` | Identitas KK | Penanda Kepala Keluarga berjenis kelamin laki-laki. | Keluarga | Integer | 0 atau 1 |
| 8 | `Jenis_Kelamin_KK_Perempuan` | Identitas KK | Penanda Kepala Keluarga berjenis kelamin perempuan. | Keluarga | Integer | 0 atau 1 |
| 9 | `Jumlah_Orang_Laki_Dirumah` | Demografi / Gender | Jumlah anggota keluarga berjenis kelamin laki-laki di rumah. | Orang | Integer | Nilai >= 0 |
| 10 | `Jumlah_Orang_Perempuan_Dirumah` | Demografi / Gender | Jumlah anggota keluarga berjenis kelamin perempuan di rumah. | Orang | Integer | Nilai >= 0 |
| 11 | `Jumlah_orang_yang_tidak_ada_(meninggal)_tapi_masih_tercatatat_di_Kartu_Keluarga` | Administrasi Kependudukan | Jumlah anggota keluarga yang telah meninggal dunia namun masih di KK. | Orang | Integer | Nilai >= 0 |
| 12 | `Jumlah_orang_yang_pindah_tapi_masih_tercatatat_di_Kartu_Keluarga` | Administrasi Kependudukan | Jumlah anggota keluarga yang telah pindah domisili namun masih di KK. | Orang | Integer | Nilai >= 0 |
| 13 | `Agama_yang_Ada_di_Rumah` | Demografi / Agama | Rincian keberadaan agama anggota keluarga di rumah. | - | String | Rincian Agama Tekstual |
| 14 | `Jumlah_orang_beragama_islam_di_rumah` | Demografi / Agama | Banyaknya anggota keluarga beragama Islam. | Orang | Integer | Nilai >= 0 |
| 15 | `Jumlah_orang_beragama_kristen_di_rumah` | Demografi / Agama | Banyaknya anggota keluarga beragama Kristen. | Orang | Integer | Nilai >= 0 |
| 16 | `Jumlah_orang_beragama_khatolik_di_rumah` | Demografi / Agama | Banyaknya anggota keluarga beragama Katholik. | Orang | Integer | Nilai >= 0 |
| 17 | `Jumlah_orang_beragama_konghucu_di_rumah` | Demografi / Agama | Banyaknya anggota keluarga beragama Konghucu. | Orang | Integer | Nilai >= 0 |
| 18 | `Jumlah_orang_beragama_budha_di_rumah` | Demografi / Agama | Banyaknya anggota keluarga beragama Budha. | Orang | Integer | Nilai >= 0 |
| 19 | `Jumlah_Penduduk_Berusia_0-4` | Struktur Umur | Banyaknya balita berusia 0 s.d. 4 tahun. | Orang | Integer | Nilai >= 0 |
| 20 | `Jumlah_Penduduk_Berusia_5-14` | Struktur Umur | Banyaknya anak berusia 5 s.d. 14 tahun. | Orang | Integer | Nilai >= 0 |
| 21 | `Jumlah_Penduduk_Berusia_15-64` | Struktur Umur | Banyaknya penduduk usia kerja/produktif 15 s.d. 64 tahun. | Orang | Integer | Nilai >= 0 |
| 22 | `Jumlah_Penduduk_Berusia_65-74` | Struktur Umur | Banyaknya lansia berusia 65 s.d. 74 tahun. | Orang | Integer | Nilai >= 0 |
| 23 | `Jumlah_Penduduk_Berusia_75+` | Struktur Umur | Banyaknya lansia berusia 75 tahun ke atas. | Orang | Integer | Nilai >= 0 |
| 24 | `Jumlah_Anggota_Keluarga_Putus_Sekolah_(7-18_tahun_tetapi_tidak_sedang_sekolah)` | Pendidikan | Banyaknya anggota keluarga usia 7-18 tahun yang tidak sedang sekolah. | Orang | Integer | Nilai >= 0 |
| 25 | `Nama_Anggota_Keluarga_Putus_Sekolah` | Pendidikan | Nama anak usia 7-18 tahun yang tidak sedang sekolah. | - | String | Nama Tekstual |
| 26 | `Jumlah_orang_dengan_Disabilitas` | Kebutuhan Khusus | Banyaknya anggota keluarga yang memiliki disabilitas. | Orang | Integer | Nilai >= 0 |
| 27 | `Jumlah_Penduduk_usia_kerja_(15-64_tahun)_yang_bekerja` | Ketenagakerjaan | Jumlah penduduk usia kerja 15-64 tahun yang bekerja. | Orang | Integer | Nilai >= 0 |
| 28 | `Jumlah_Penduduk_usia_kerja_(15-64_tahun)_yang_tidak_bekerja` | Ketenagakerjaan | Jumlah penduduk usia kerja 15-64 tahun yang tidak bekerja. | Orang | Integer | Nilai >= 0 |
| 29 | `Jumlah_UMKM_Dalam_Keluarga` | Ekonomi | Banyaknya unit usaha mikro, kecil, atau menengah yang dikelola keluarga. | Unit Usaha | Integer | Nilai >= 0 |
| 30 | `Jumlah_ART_Memiliki_BPJS` | Perlindungan Sosial | Jumlah anggota keluarga yang memiliki jaminan kesehatan BPJS. | Orang | Integer | Nilai >= 0 |
| 31 | `Jml_Penerima_Terdaftar_Sembako_BPNT` | Bantuan Sosial | Banyaknya keluarga penerima bantuan BPNT. | Keluarga | Integer | Nilai >= 0 |
| 32 | `Jml_Penerima_Terdaftar_PKH` | Bantuan Sosial | Banyaknya keluarga penerima bantuan PKH. | Keluarga | Integer | Nilai >= 0 |
| 33 | `Kepemilikan_Fasilitas_Buang_Air_Besar` | Sanitasi | Keberadaan dan kepemilikan fasilitas buang air besar (jamban) sendiri. | - | String | Memiliki, Tidak Memiliki |
| 34 | `Foto_Rumah` | Visual | Lampiran foto tampak depan rumah. | - | String | Path Berkas Gambar |
| 35 | `Petugas` | Pengamatan Sektoral | Isian variabel Petugas pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 36 | `Tanggal_Pendataan` | Waktu Pencacahan | Tanggal dan waktu penginputan data. | - | DateTime | YYYY-MM-DD HH:MM:SS |
| 37 | `Status_Pendataan` | Metodologi CAPI | Status kelengkapan pengisian data CAPI. | - | String | Sudah Selesai, Belum Terdata |
| 38 | `Nama_Penerima_Manfaat_BPNT` | Bantuan Sosial | Nama penerima manfaat BPNT. | - | String | Nama Tekstual |
| 39 | `Nama_Penerima_Manfaat_PKH` | Bantuan Sosial | Nama penerima manfaat PKH. | - | String | Nama Tekstual |
| 40 | `Jumlah_Anggota_Keluarga_di_Rumah` | Ukuran Rumah Tangga | Total jumlah anggota keluarga yang mendiami rumah. | Orang | Integer | Nilai >= 1 |
| 41 | `Catatan` | Informasi Tambahan | Catatan temuan khusus petugas. | - | String | Narasi Bebas |

---

## 📈 III. METADATA INDIKATOR (MS-INDIKATOR)

| No | Nama Indikator | Definisi | Rumus / Formula Kalkulasi | Satuan | Ukuran / Klasifikasi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Rasio Jenis Kelamin (Sex Ratio)** | Perbandingan jumlah penduduk laki-laki dengan 100 penduduk perempuan di kelurahan tersebut. | $$frac(sum "L", sum "P") * 100$$ | Persen | Demografi |
| **2** | **Rata-rata Anggota Rumah Tangga (ART)** | Rata-rata banyaknya anggota keluarga yang mendiami satu rumah tangga/KK. | $$frac(sum "L" + sum "P", sum "KK")$$ | Orang per Keluarga | Kesejahteraan / Demografi |
| **3** | **Persentase Penduduk Lansia** | Proporsi jumlah lansia terhadap total penduduk kelurahan. | $$frac(sum "Lansia", "Total Penduduk") * 100$$ | Persen | Demografi / Kelompok Rentan |
| **4** | **Persentase Penerima Bantuan Sosial** | Proporsi penduduk yang terdaftar sebagai penerima bantuan sosial (PKH, BPNT, BLT) terhadap total penduduk. | $$frac(sum "Bansos", "Total Penduduk") * 100$$ | Persen | Kesejahteraan Rakyat |
| **5** | **Persentase Anak Putus Sekolah** | Proporsi anak usia sekolah (7-18 tahun) yang tidak bersekolah terhadap total anak usia sekolah. | $$frac(sum "Putus Sekolah", "Total Usia Sekolah") * 100$$ | Persen | Pendidikan |
| **6** | **Kepadatan Hunian Rumah** | Rata-rata jumlah penduduk yang menghuni setiap bangunan fisik tempat tinggal. | $$frac("Total Penduduk", sum "Bangunan")$$ | Orang per Unit | Infrastruktur / Kesehatan |
| **7** | **Persentase Penduduk Usia Kerja Bekerja** | Proporsi penduduk usia kerja (15-64 tahun) yang bekerja terhadap total penduduk usia kerja di kelurahan. | $$frac(sum "Usia Kerja Bekerja", sum "Usia Kerja") * 100$$ | Persen | Ketenagakerjaan |
| **8** | **Persentase Rumah Tangga Memiliki UMKM** | Proporsi rumah tangga yang mengelola usaha mikro, kecil, atau menengah di kelurahan. | $$frac(sum "Keluarga UMKM", sum "KK") * 100$$ | Persen | Perekonomian |
| **9** | **Persentase Kepemilikan Jaminan Kesehatan (BPJS)** | Proporsi anggota keluarga yang memiliki jaminan kesehatan BPJS. | $$frac(sum "Peserta BPJS", "Total Penduduk") * 100$$ | Persen | Kesehatan / Sosial |
