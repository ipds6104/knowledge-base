# BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH
Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;
Laman https://mempawahkab.bps.go.id; Pos-el bps6104@bps.go.id

---

**Nomor**       : B-1108/61040/SS.190/09/2026  
**Sifat**       : Penting  
**Lampiran**    : 1 (satu) Berkas  
**Hal**         : Permintaan Pemadanan Data Sekunder Usaha dan Keluarga Berbasis Satuan Lingkungan Setempat (SLS) dalam Rangka Optimalisasi Pelaksanaan Lapangan Sensus Ekonomi 2026  
**Tanggal**     : Mempawah, 23 September 2026  

**Yth. Kepala Badan Pusat Statistik Provinsi Kalimantan Barat**  
di Pontianak  

Dengan hormat,

Sehubungan dengan pelaksanaan pendataan lapangan Sensus Ekonomi 2026 (SE2026) di Kabupaten Mempawah yang saat ini telah memasuki tahapan evaluasi cakupan (*coverage check*) dan penyisiran ulang (*revisit/sweeping*), kami memandang perlunya langkah pengawalan kualitas data secara intensif guna meminimalkan potensi unit usaha dan rumah tangga usaha yang belum teridentifikasi (*under-coverage*), khususnya pada sektor-sektor usaha mikro, informal, dan aktivitas ekonomi keluarga di tingkat lapangan.

Dalam rangka mendukung efektivitas penelusuran tersebut, BPS Kabupaten Mempawah bermaksud mengajukan permohonan bantuan pemadanan (*matching*) data sekunder direktori usaha dan karakteristik keluarga berbasis wilayah yang tersedia di tingkat provinsi dengan basis data hasil pencacahan SE2026 Kabupaten Mempawah. Pemadanan ini sangat kami butuhkan untuk mengidentifikasi unit-unit usaha yang belum terjangkau pada saat pencacahan awal, sehingga petugas lapangan (PPL dan PML) dapat melakukan kunjungan ulang (*revisit*) secara presisi dan tepat sasaran hingga ke level Satuan Lingkungan Setempat (SLS).

Adapun rincian spesifikasi struktur kolom dan variabel data yang kami butuhkan untuk keperluan pemadanan dan penelusuran lapangan tertera pada Lampiran surat ini. Kerahasiaan data individual sepenuhnya dijamin dan hanya dipergunakan untuk kepentingan penguatan cakupan sensus resmi BPS.

Demikian permohonan ini kami sampaikan. Atas perhatian, arahan, dan kerja sama yang baik dari Bapak/Ibu, kami ucapkan terima kasih.


Kepala Badan Pusat Statistik  
Kabupaten Mempawah,  


**Munawir, S.E., M.M.**  

---

## LAMPIRAN SURAT DINAS
**Nomor**   : B-1108/61040/SS.190/09/2026  
**Tanggal** : 23 September 2026  
**Hal**     : Spesifikasi Struktur Variabel Data Sekunder untuk Pemadanan (Matching) dan Pelacakan (Tracking) Lapangan SE2026  

### STRUKTUR VARIABEL DATA PERMINTAAN PEMADANAN (MATCHING SE2026)

| No | Nama Variabel | Tipe Data | Deskripsi & Kegunaan Lapangan |
|:---|:---|:---|:---|
| **A. Identitas Wilayah Administrasi & Geospasial SLS** |
| 1 | `kdkec` | Teks (3) | Kode Kecamatan BPS Kabupaten Mempawah (contoh: 080) |
| 2 | `nmkec` | Teks | Nama Kecamatan (contoh: JONGKAT, TOHO, MEMPAWAH HILIR) |
| 3 | `kddesa` | Teks (3) | Kode Desa/Kelurahan BPS (contoh: 001) |
| 4 | `nmdesa` | Teks | Nama Desa/Kelurahan |
| 5 | `kdsls` | Teks (4) | Kode Satuan Lingkungan Setempat (contoh: 0002) |
| 6 | `idsls` | Teks (14) | ID SLS Unik BPS (kdprov + kdkab + kdkec + kddesa + kdsls) sebagai kunci agregasi SLS |
| 7 | `nmsls` | Teks | Nama SLS / RT / RW / Dusun sesuai master data wilkerstat lapangan |
| **B. Identitas Subjek / Responden (Kunci Matching)** |
| 8 | `nik` | Teks (16) | **Kunci Utama Pemadanan:** NIK Pelaku Usaha / Kepala Rumah Tangga / ART Pengelola Usaha |
| 9 | `nama_responden` | Teks | Nama Lengkap Pengelola Usaha / Kepala Rumah Tangga |
| 10 | `no_kk` | Teks (16) | Nomor Kartu Keluarga responden (jika tersedia) |
| 11 | `alamat_domisili` | Teks | Alamat domisili lengkap / nama jalan / nomor rumah / blok perumahan |
| 12 | `no_telepon` | Teks | Nomor telepon/HP responden yang dapat dihubungi untuk konfirmasi janji temu |
| **C. Status Hasil Pemadanan (Matching SE2026)** |
| 13 | `status_match_se2026` | Teks | Status hasil pemadanan data: **Ditemukan** atau **Tidak Ditemukan** |
