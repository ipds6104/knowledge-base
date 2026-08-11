# METADATA STATISTIK SEKTORAL
## Satu Data Indonesia (SDI) - Desa Cantik 2026
**Desa Pasir Palembang, Kabupaten Mempawah**

---

## 📅 I. METADATA KEGIATAN (MS-KEGIATAN)

| No | Elemen Metadata | Keterangan / Nilai |
| :--- | :--- | :--- |
| **1** | **Nama Kegiatan** | Pendataan Sosial Keluarga dan Fasilitas Umum Desa Cantik Pasir Palembang 2026 |
| **2** | **Instansi Penyelenggara** | Pemerintah Desa Pasir Palembang bekerjasama dengan BPS Kabupaten Mempawah |
| **3** | **Jenis Kegiatan** | Pendataan Langsung |
| **4** | **Tujuan Kegiatan** | Memetakan kondisi sosial-ekonomi penduduk di tingkat RT serta kondisi kelayakan sarana prasarana desa untuk mendukung kebijakan pembangunan berbasis bukti (evidence-based policy). |
| **5** | **Cara Pengumpulan Data** | Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga dan observasi geospasial fasilitas desa menggunakan aplikasi mobile AppSheet. |
| **6** | **Cakupan Wilayah** | Seluruh wilayah Desa Pasir Palembang (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 3 Dusun (Dusun Pelaik, Dusun Tengah, Dusun Tekam Baru). |
| **7** | **Unit Pengamatan** | Bangunan Tempat Tinggal Biasa / Keluarga (CAPI), Sarana Prasarana (Fasilitas Umum) |
| **8** | **Frekuensi Kegiatan** | Tahunan (Annual) |
| **9** | **Waktu Pelaksanaan** | Juni - Juli 2026 (Pengumpulan Lapangan), Agustus 2026 (Diseminasi & Integrasi Web) |
| **10** | **Media Rilis** | Portal Web Desa Cantik Pasir Palembang & Publikasi Desa Pasir Palembang Dalam Angka 2026 |

---

## 📊 II. METADATA VARIABEL (MS-VARIABEL)

### A. Tabel Variabel Tingkat Sarana Prasarana (Fasilitas)

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
| 10 | `Kondisi_Bangunan_Jalan` | Kualitas Fisik | Kelayakan fisik bangunan sarana. | - | String | Baik, Rusak Ringan, Rusak Berat |
| 11 | `Sumber_Listrik` | Utilitas Listrik | Sumber pasokan daya listrik utama sarana. | - | String | PLN 24 Jam, Non-PLN, dll. |
| 12 | `Sumber_Air_Bersih` | Utilitas Air | Sumber penyediaan air bersih utama sarana. | - | String | PDAM/PAMSIMAS, Sumur Bor, dll. |
| 13 | `Akses_Jalan` | Infrastruktur | Jenis permukaan jalan terdekat. | - | String | Aspal/Beton, Batu, Jalan Tanah |
| 14 | `Sinyal_Seluler` | Telekomunikasi | Kekuatan sinyal telekomunikasi seluler. | - | String | Sangat Baik (4G/LTE), Cukup, dll. |
| 15 | `Catatan` | Informasi Tambahan | Catatan temuan khusus petugas. | - | String | Narasi Bebas |

### B. Tabel Variabel Data Mikro Bangunan Tempat Tinggal Biasa & Rumah Tangga CAPI

| No | Nama Variabel | Konsep | Definisi | Satuan | Tipe Data | Pilihan Isian / Keterangan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Nomor_Bangunan` | Identitas Bangunan | Nomor urut fisik bangunan tempat tinggal biasa. | Unit | Integer | Nilai > 0 |
| 2 | `Nomor_SLS` | Wilayah Administrasi | Kode SLS/RT tempat pendataan. | - | String | Kode SLS |
| 3 | `Nama_RT` | Wilayah Administrasi | Nama rukun tetangga tempat pengumpulan data CAPI dilakukan. | - | String | Nama RT Tekstual |
| 4 | `Koordinat` | Geospasial | Titik koordinat presisi latitude dan longitude lokasi fisik bangunan. | - | String | Latitude, Longitude (LatLong) |
| 5 | `Nama_Kepala_Keluarga` | Identitas Responden | Nama lengkap Kepala Keluarga utama yang mendiami bangunan. | - | String | Nama Lengkap Tekstual |
| 6 | `Jumlah_Kartu_Keluarga` | Rumah Tangga / KK | Banyaknya Kartu Keluarga (KK) yang mendiami bangunan. | Keluarga | Integer | Nilai >= 1 |
| 7 | `Nama_Kepala_Keluarga_Tambahan` | Identitas Responden | Nama lengkap Kepala Keluarga tambahan yang tinggal di bangunan yang sama. | - | String | Nama Lengkap Tekstual |
| 8 | `Nama_Kepala_Keluarga_Tambahan_2` | Identitas Responden | Nama lengkap Kepala Keluarga tambahan kedua di bangunan yang sama. | - | String | Nama Lengkap Tekstual |
| 9 | `Jumlah_Orang_Laki-Laki_di_Rumah` | Demografi / Gender | Banyaknya anggota keluarga berjenis kelamin laki-laki di rumah. | Orang | Integer | Nilai >= 0 |
| 10 | `Jumlah_Orang_Perempuan_di_Rumah` | Demografi / Gender | Banyaknya anggota keluarga berjenis kelamin perempuan di rumah. | Orang | Integer | Nilai >= 0 |
| 11 | `Jumlah_orang_yang_tidak_ada_(meninggal)_tapi_masih_tercatat_di_Kartu_Keluarga` | Administrasi Kependudukan | Jumlah anggota keluarga yang telah meninggal dunia namun masih di KK. | Orang | Integer | Nilai >= 0 |
| 12 | `Nama_orang_yang_tidak_ada_(meninggal)_tapi_masih_tercatat_di_Kartu_Keluarga` | Administrasi Kependudukan | Nama anggota keluarga yang telah meninggal dunia namun masih di KK. | - | String | Nama Tekstual |
| 13 | `Jumlah_Anggota_Keluarga_Putus_Sekolah_(7-18_tahun_tetapi_tidak_sedang_sekolah)` | Pendidikan | Banyaknya anggota keluarga usia 7-18 tahun yang tidak sedang sekolah. | Orang | Integer | Nilai >= 0 |
| 14 | `Nama_Anggota_Keluarga_Putus_Sekolah` | Pendidikan | Nama anak usia 7-18 tahun yang tidak sedang sekolah. | - | String | Nama Tekstual |
| 15 | `Gambar_Rumah` | Visual | Lampiran foto tampak depan rumah. | - | String | Path Berkas Gambar |
| 16 | `Pekerjaan_anggota_rumah_tangga_yang_merupakah_penghasilan_utama_dalam_rumah` | Mata Pencaharian | Jenis pekerjaan anggota rumah tangga penopang penghasilan utama. | - | String | Petani, Buruh, Pedagang, PNS, Swasta, dll. |
| 17 | `Apa_bahan_utama_dinding_rumah` | Pengamatan Sektoral | Isian variabel Apa bahan utama dinding rumah? pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 18 | `Apa_bahan_utama_lantai_terluas_rumah` | Bahan Bangunan | Bahan fisik utama lantai terluas rumah. | - | String | Semen, Keramik, Ubin, Kayu, Tanah, Lainnya |
| 19 | `Apa_bahan_atap_terluas_rumah` | Bahan Bangunan | Bahan fisik utama atap terluas rumah. | - | String | Seng, Asbes, Genteng, Rumbia, Lainnya |
| 20 | `Apakah_rumah_ini_memiliki_fasilitas_buang_air_besar_sendiri` | Sanitasi | Keberadaan dan kepemilikan fasilitas buang air besar (jamban) sendiri. | - | String | Ya, Tidak |
| 21 | `Bagaimana_cara_keluarga_membuang_sampah_rumah_tangga` | Lingkungan | Cara utama keluarga membuang dan mengelola sampah rumah tangga. | - | String | Dibakar, Angkut Petugas, Sungai, dll. |
| 22 | `Petugas` | Pengamatan Sektoral | Isian variabel Petugas pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 23 | `Jumlah_Laki_per_ID_WIlkerstat` | Pengamatan Sektoral | Isian variabel Jumlah Laki per ID WIlkerstat pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 24 | `Jumlah_Perempuan_per_ID_Wilkerstat` | Pengamatan Sektoral | Isian variabel Jumlah Perempuan per ID Wilkerstat pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 25 | `Nomor_Whatsapp` | Komunikasi | Nomor kontak telepon/WhatsApp anggota keluarga. | - | String | Nomor Telepon |
| 26 | `Persentase_Kelengkapan_Isian` | Pengamatan Sektoral | Isian variabel Persentase Kelengkapan Isian pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 27 | `Apakah_rumah_ini_mendapat_bantuan_dari_pemerintah_(PKH,_BPNT,_BLTS,_BCP,_BLTDD,_PIP,_BPJS_PBI)` | Bantuan Sosial | Status penerima bantuan sosial pemerintah. | - | String | MENERIMA, TIDAK |
| 28 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_PKH` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan PKH pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 29 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_BPNT` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPNT pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 30 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_BLTS` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTS pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 31 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_BCP` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BCP pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 32 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_BLTDD` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTDD pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 33 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_PIP` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan PIP pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 34 | `Jika_menerima_bantuan,_berapa_jumlah_keluarga_penerima_bantuan_BPJS_PBI` | Pengamatan Sektoral | Isian variabel Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPJS PBI pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 35 | `Tanggal_Pendataan` | Pengamatan Sektoral | Isian variabel Tanggal Pendataan pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 36 | `Status_Pendataan` | Pengamatan Sektoral | Isian variabel Status Pendataan pada pengumpulan data lapangan. | - | String | Isian Tekstual |
| 37 | `Kategori_Pekerjaan` | Pengamatan Sektoral | Isian variabel Kategori Pekerjaan pada pengumpulan data lapangan. | - | String | Isian Tekstual |

---

## 📈 III. METADATA INDIKATOR (MS-INDIKATOR)

| No | Nama Indikator | Definisi | Rumus / Formula Kalkulasi | Satuan | Ukuran / Klasifikasi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Rasio Jenis Kelamin (Sex Ratio)** | Perbandingan jumlah penduduk laki-laki dengan 100 penduduk perempuan di desa tersebut. | $$frac(sum "L", sum "P") * 100$$ | Persen | Demografi |
| **2** | **Rata-rata Anggota Rumah Tangga (ART)** | Rata-rata banyaknya anggota keluarga yang mendiami satu rumah tangga/KK. | $$frac(sum "L" + sum "P", sum "KK")$$ | Orang per Keluarga | Kesejahteraan / Demografi |
| **3** | **Persentase Penerima Bantuan Sosial** | Proporsi penduduk yang terdaftar sebagai penerima bantuan sosial (PKH, BPNT, BLT) terhadap total penduduk. | $$frac(sum "Bansos", "Total Penduduk") * 100$$ | Persen | Kesejahteraan Rakyat |
| **4** | **Persentase Anak Putus Sekolah** | Proporsi anak usia sekolah (7-18 tahun) yang tidak bersekolah terhadap total anak usia sekolah. | $$frac(sum "Putus Sekolah", "Total Usia Sekolah") * 100$$ | Persen | Pendidikan |
| **5** | **Kepadatan Hunian Rumah** | Rata-rata jumlah penduduk yang menghuni setiap bangunan fisik tempat tinggal. | $$frac("Total Penduduk", sum "Bangunan")$$ | Orang per Unit | Infrastruktur / Kesehatan |
| **6** | **Rasio Sarana Keagamaan per 1000 Penduduk** | Ketersediaan sarana tempat ibadah desa untuk setiap 1.000 jiwa penduduk. | $$frac("Sarana Keagamaan", "Total Penduduk") * 1000$$ | Unit per 1000 Jiwa | Sosial / Agama |
| **7** | **Persentase Kepemilikan Jaminan Kesehatan (BPJS)** | Proporsi anggota keluarga yang memiliki jaminan kesehatan BPJS. | $$frac(sum "Peserta BPJS", "Total Penduduk") * 100$$ | Persen | Kesehatan / Sosial |
