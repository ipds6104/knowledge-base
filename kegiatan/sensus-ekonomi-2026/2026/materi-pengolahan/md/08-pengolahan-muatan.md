---
judul: "Pengolahan dan Rekonsiliasi Muatan Wilkerstat SE2026"
modul: "08"
kegiatan: "Sensus Ekonomi 2026 - Wilkerstat"
total_slide: 15
berkas_sumber:
  pdf: "../pdf/08-pengolahan-muatan.pdf"
topik_utama:
  - "Perhitungan Agregat Muatan Keluarga dan Bangunan Fisik per SLS"
  - "Integrasi Data Muatan dengan Master SLS FRS-MFDOnline"
  - "Unggah Data Muatan ke Portal Unggah Muatan BPS"
  - "Validasi Perbandingan Muatan SE2026 vs Proyeksi/Sensus Sebelumnya"
  - "Penyusunan Berita Acara Final Muatan Tingkat Kabupaten/Kota"
---

# Pengolahan dan Rekonsiliasi Muatan Wilkerstat SE2026

> **Pelatihan Instruktur Daerah (Inda)**  
> *Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026*  
> **Direktorat Metodologi Statistik dan Sains Data - BPS RI**


---

## 📑 Slide 1: Materi Bagian 1

PENGOLAHAN MUATAN

Pelatihan Instruktur Daerah Pengolahan Kerangka Geospasial dan Muatan Wilkerstat SE2026

Jakarta, 27 Agt – 02 Sept 2026


---

## 📑 Slide 2: ALUR PENGOLAHAN MUATAN

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 3: Materi Bagian 3

PROSES PENGOLAHAN MUATAN


---

## 📑 Slide 4: TAHAPAN PENGOLAHAN MUATAN

Atribut Geotagging

Peta Geotagging

Peta Geotagging hasil updating, QGIS


---

## 📑 Slide 5: [00] PERSIAPAN PROJECT DAN IMPORT LAYER

Peta Geotagging Hasil Pengolahan


---

## 📑 Slide 6: [01] UPDATE ATRIBUT DENGAN PETA TERMUTAKHIR

Peta Geotagging Hasil Pengolahan


---

## 📑 Slide 7: [02] PERHITUNGAN MUATAN

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 8: [03] PENGECEKAN ATRIBUT DAN PENYIMPANAN

Input Tools Output

Layer Vector Point QGIS:
- 
Hasil untuk Upload GS
- 
Hasil Pengolahan Muatan

QGIS Export File GeoJSON Lokasi penyimpanan: 03_Output/03_Peta Geotagging dan Muatan/ final_landmark_{idkab}_se_2026.geojson

File CSV: Lokasi penyimpanan: 03_Output/03_Peta Geotagging dan Muatan/{idkab}_muatan.csv


---

## 📑 Slide 9: Materi Bagian 9

UNGGAH DAN VALIDASI HASIL PENGOLAHAN MUATAN


---

## 📑 Slide 10: [01] UNGGAH HASIL PENGOLAHAN TITIK BANGUNAN

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 11: [02] VALIDASI DAN UNGGAH MUATAN (1)

Output hasil pengolahan muatan perlu divalidasi untuk memastikan kesesuaian format, kelengkapan variabel, tipe data, konsistensi nilai, dan kesesuaian dengan master sub- SLS. Proses validasi dilakukan melalui aplikasi web (akses via VPN BPS). File yang lolos validasi akan otomatis tersimpan di server pusat.

Proses validasi dan unggah file hasil pengolahan muatan
memerlukan 2 (dua) file input yang harus disiapkan oleh
tim wilkerstat BPS kabupaten/kota, meliputi:
- File Master Sub-SLS 2026 Semester 1
o
Format penamaan: msubsls_261_{idkab}.csv atau
msubsls_261_{idkab}.xlsx.
o
File ini berisi daftar sub-SLS kondisi pascalapangan
SE2026 yang digunakan sebagai master kondisi 2026
Semester 1. File ini dapat diakses dan diunduh
melalui tautan [https://s.bps.go.id/MFD_Rilis_Daerah.](https://s.bps.go.id/MFD_Rilis_Daerah.)

[https://unggah-muatan.web.bps.go.id/](https://unggah-muatan.web.bps.go.id/)

- File Hasil Pengolahan Muatan
o
Format penamaan: {idkab}_muatan.csv atau
{idkab}_muatan.xlsx.
o
File ini merupakan output dari tahapan pengolahan
muatan titik bangunan (geotagging).


---

## 📑 Slide 12: [02] VALIDASI DAN UNGGAH MUATAN (2)

Prosedur Validasi dan Unggah Muatan (1)

- 
Buka tautan [https://unggah-](https://unggah-)
muatan.web.bps.go.id/ menggunakan peramban (browser)
yang terhubung dengan internet. Pastikan koneksi internet juga
terhubung ke VPN pegawai BPS.

- 
Unggah file hasil pengolahan muatan dengan mengklik tombol
"Choose
File"
atau
area
unggah
pada
kolom
"File
Hasil
Pengolahan Muatan", kemudian pilih file {idkab}_muatan.csv
atau {idkab}_muatan.xlsx yang akan divalidasi. Pastikan nama
file sesuai dengan kode kabupaten/kota yang telah dipilih.

- 
Pada kolom “Kode Kabupaten/Kota”, cari dan pilih sesuai
satker masing-masing. Kolom ini juga dilengkapi fitur pencarian
untuk memudahkan navigasi.

- 
Unggah file master sub-SLS dengan klik tombol “Choose File”
atau area unggah pada kolom “File Master Sub-SLS", kemudian
pilih
file
msubsls_261_{idkab}.csv
atau
msubsls_261_{idkab}.xlsx. Pastikan nama file sesuai dengan
kode kabupaten/kota yang telah dipilih.

- 
Klik tombol "Validasi & Upload". Sistem akan mengecek:

o pengecekan format dan nama file (master dan muatan); o pengecekan kesesuaian master (one-to-one matching satu-satu ID Sub-SLS); o pengecekan kelengkapan variabel; o pengecekan tipe data dan panjang karakter; o serta pengecekan anomali data (konsistensi logis muatan).


---

## 📑 Slide 13: [02] VALIDASI DAN UNGGAH MUATAN (3)

Prosedur Validasi dan Unggah Muatan (2)

- 
Apabila hasil validasi
menunjukkan
adanya
error atau
warning,
pengguna dapat mengunduh daftar lengkap error atau warning
dalam format Excel dengan mengklik tombol "Download Daftar
Error & Warning". Laporan ini berisi dua sheet, yaitu:

- 
Hasil validasi ditampilkan dalam bentuk ringkasan dan detail.
Apabila masih terdapat error (
), maka file tidak dapat dilanjutkan ke
tahap unggah. Tim wilkerstat BPS kabupaten/kota diharuskan untuk
memperbaiki data pada file sumber sesuai dengan daftar error yang
ditampilkan, kemudian mengulangi proses validasi.

> [!IMPORTANT]
> Catatan:

o Error ( ): Kesalahan yang bersifat wajib diperbaiki (misalnya: variabel tidak lengkap, data tidak sesuai, adanya anomali muatan seperti btt > kk atau bku > usaha); o Warning ( ): Peringatan yang bersifat opsional untuk diperbaiki, tetapi tidak menggagalkan proses validasi (misalnya usaha > kk + btt).

o Ringkasan: Menampilkan status validasi serta jumlah error atau warning. o Detail Error & Warning: Menampilkan daftar lengkap error beserta lokasi baris dan keterangannya.

- 
Apabila file dinyatakan lolos validasi (seluruh indikator berstatus ✓),
sistem akan secara otomatis mengunggah file ke server pusat.
Pengguna
akan
menerima
notifikasi
bahwa
file
telah
berhasil
tersimpan. Jika file dengan kode kabupaten/kota yang sama sudah
pernah
diunggah
sebelumnya,
sistem
akan
menampilkan
konfirmasi untuk menimpa file yang lama.


---

## 📑 Slide 14: [03] MONITORING UNGGAH MUATAN

Monitoring Progres Unggah
Bertujuan untuk memastikan seluruh
kab/kota menyelesaikan unggah muatan
final tepat waktu
- 
Akses
Melalui dashboard pada aplikasi unggah-
muatan (menu Monitoring Progres)
- 
Informasi Utama
o
Progres nasional (%), jumlah
kab/kota
o
Status unggahan: Valid, Invalid,
Belum Upload
o
Detail per wilayah: error, warning,
waktu unggah
- 
Fitur
Filter per provinsi & status untuk fokus
pemantauan
- 
Kegunaan
Data real-time →memudahkan
identifikasi kendala & tindak lanjut

[https://unggah-muatan.web.bps.go.id/dashboard/](https://unggah-muatan.web.bps.go.id/dashboard/)


---

## 📑 Slide 15: Materi Bagian 15

TERIMA KASIH
