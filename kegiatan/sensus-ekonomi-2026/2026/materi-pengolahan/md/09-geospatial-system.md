---
judul: "Pemanfaatan Web Geospatial System (GS) BPS"
modul: "09"
kegiatan: "Sensus Ekonomi 2026 - Wilkerstat"
total_slide: 43
berkas_sumber:
  pdf: "../pdf/09-geospatial-system.pdf"
topik_utama:
  - "Navigasi dan Menu Fitur Web Geospatial System (GS)"
  - "Alur Kerja Unduh Peta Dasar dan Template GIS"
  - "Unggah Hasil Olahan Peta Spasial (.shp / .gpkg / .zip)"
  - "Mekanisme Quality Control (QC) dan Catatan Supervisi di GS"
  - "Approval Peta Digital oleh BPS Kab/Kota dan BPS Provinsi"
---

# Pemanfaatan Web Geospatial System (GS) BPS

> **Pelatihan Instruktur Daerah (Inda)**  
> *Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026*  
> **Direktorat Metodologi Statistik dan Sains Data - BPS RI**


---

## 📑 Slide 1: Materi Bagian 1

GEOSPATIAL SYSTEM (GS)

Pelatihan Instruktur Daerah Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026

27 Agt – 02 Sept 2026


---

## 📑 Slide 2: GS

Geospatial System (GS) merupakan system berbasis web yang digunakan untuk manajemen

transfer dan monitoring data geospasial di lingkungan BPS. GS merupakan Single Source of

Truth untuk data-data berbasis geospasial.

Dalam kegiatan pengolahan peta, GS digunakan

untuk upload, quality control, approval, dan synchronizing peta digital hasil perbaikan lapanga

n.


---

## 📑 Slide 3: Geospatial System (GS) Login

[https://dataspasial.bps.go.id/gs/](https://dataspasial.bps.go.id/gs/)


---

## 📑 Slide 4: Geospatial System (GS) Kabupaten/Kota

Menu Keterangan

Menu GS user Kabupaten/Kota

Rekap Menu untuk melihat ringkasan data dan progres pekerjaan

Absensi Peta Digunakan untuk memantau keberadaan atau kelengkapan peta dari tiap wilayah

Peta Digital Menu untuk mendownload data peta digital

Landmark Menu untuk mendownload data landmark

Peta Analog Menu untuk mendownload peta hasil scan atau peta non- digital

Unggah Menu digunakan untuk melakukan unggah data baik peta digital maupun data geotagging melalui mekanisme open job

Bahan/Template Tempat penyimpanan template dan bahan pendukung

Master Digunakan untuk menwonload master wilayah yang dapat digunakan untuk proses editing dan matching

Referensi Berisi keterangan jenis status untuk setiap proses yanga ada di sistem GS


---

## 📑 Slide 5: Geospatial System (GS) Provinsi

Menu Keterangan

Rekap Menu untuk melihat ringkasan data dan progres pekerjaan

Absesnsi Peta Digunakan untuk memantau keberadaan atau kelengkapan peta dari tiap wilayah

Peta Digital Menu untuk mendownload data peta digital

Landmark Menu untuk mendownload data landmark

Peta Analog Menu untuk mendownload peta hasil scan atau peta non- digital

Bahan/Template Tempat penyimpanan template dan bahan pendukung

Master Digunakan untuk menwonload master wilayah yang dapat digunakan untuk proses editing dan matching

Referensi Berisi keterangan jenis status untuk setiap proses yanga ada di sistem GS

Menu GS user Provinsi


---

## 📑 Slide 6: Materi Bagian 6

Alur Pengecekan Peta di GS


---

## 📑 Slide 7: Materi Bagian 7

1. Kabupaten / Kota
2. Provinsi
3. Pusat

1. Alur Status Pengecekan
Peta di GS​


---

## 📑 Slide 8: Alur Status Pengecekan Peta di GS

Flowchart tersebut menggambarkan

alur validasi dan persetujuan peta

secara berjenjang dari tingkat Kabupaten/Kota →Provinsi → Pusat. Flowchart ini menunjukkan proses quality control (QC) spasial bertingkat untuk memastikan data peta bebas kesalahan topologi dan

atribut sebelum menjadi peta final

nasional.


---

## 📑 Slide 9: Alur Status Pengecekan Peta di GS (lanjutan)

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 10: Materi Bagian 10

1. Open Job
2. Unggah
3. Proses Check Error
4. Monitoring Error
dan Perbaikan
5. Kirim Ke Provinsi

2. PEMROSESAN
DI BPS KABUPATEN /
KOTA


---

## 📑 Slide 11: ALUR PEMROSESAN DI BPS KABUPATEN / KOTA

1

2

Unggah Peta

Open Job

Digital

Pilih level peta & buka job pemrosesan untuk

BPS Kab/Kota upload

peta digital hasil perbaikan lapangan

memulai unggah peta

Status Proses:

Open Job Sedang Proses

3

Cek Error Otomatis

Sistem cek geometri,

atribut, topologi (gap/overlap), &

duplikasi

Cek Error Invalid File Proses Cek Selesai Kirim Provinsi Provinsi Reject

4

5

Lihat Hasil QC

Kirim ke Provinsi

Tinjau laporan error &

Submit peta digital ke BPS Provinsi untuk QC &

perbaiki peta di QGIS

jika diperlukan

approval lanjutan


---

## 📑 Slide 12: Geospatial System (GS)

Unggah:
- Unggah Peta Digital
- Unggah Landmark


---

## 📑 Slide 13: 1. OPEN JOB

[Penjelasan]

1. Status awal.
2. BPS Kab/kota mulai
melakukan upload
peta digital ke
aplikasi GS.
3. Upload peta digital
aktif setelah 'Open
Job' diaktifkan.


---

## 📑 Slide 14: 2. UNGGAH PETA DIGITAL

[Penjelasan]

Unggah dilakukan oleh

BPS Kab/Kota dan dilakukan secara utuh

satu kab/kota tidak

secara parsial.


---

## 📑 Slide 15: 3. PROSES CHECK ERROR PADA FILE

[JUDUL SLIDE SATU BARIS]

[Penjelasan]

1. Sistem melakukan import
file kedalam temporary
database.
2. Sistem mulai melakukan
pengecekan secara
berurutan, yaitu:

1. Pengecekan tipe file
2. Pengecekan
kelengkapan
atribut/field


---

## 📑 Slide 16: 3. PROSES CHECK ERROR PADA FILE

[JUDUL SLIDE SATU BARIS]

INVALID FILE

- Ketika format tidak
GeoJSON
- Geometri ada yang
NULL/invalid
geometri
- Field/Atribut wajib
tidak lengkap

Atribut Wajib

kdprov (string – 2) nmprov (string)

kdkab (string – 2) nmkab (string)

kdkec (string – 3) nmkec (string)

kddesa (string – 3) nmdesa (string)

idsls (string - 14) kdsls (string – 4)

idsubsls (string –
16) =as primary
key

kdsubsls (string – 2)

nmsls (String) rw_dki (String)

tingkat (Integer) nm_gedung (String)

posisi (String)

> [!IMPORTANT]
> Catatan: Penyimpanan dalam bentuk string harus dilakukan agar tidak kehilanga n informasi, misalnya: kode sls ‘0003’ tidak berubah menjadi ‘3’


---

## 📑 Slide 17: 3. PROSES CHECK ERROR TOPOLOGI DAN  DUPLIKAT

[JUDUL SLIDE SATU BARIS]

Proses Check Error

1. Cek Duplikat pada
setiap record.
2. Cek topologi
geometri.

- Gap
- Overlap


---

## 📑 Slide 18: 4. LIHAT PETA

[Penjelasan]

1. Memungkinkan untuk memonitor bagian peta yang masih mengandung eror untuk nantinya diperbaiki. 2. Mengunggah ulang peta yang sudah diperbaiki.


---

## 📑 Slide 19: [JUDUL SLIDE SATU BARIS]

[Penjelasan]

BPS Kab/Kota melakukan proses pengiriman peta ke Provinsi untuk dicek

oleh BPS Provinsi.


---

## 📑 Slide 20: [JUDUL SLIDE SATU BARIS]

Kriteria

1. Ketika masih ada gap
dan overlap antar
kabupaten
2. Masih ada gap
overlap antar SLS
3. Masih ada record
duplikat.


---

## 📑 Slide 21: [JUDUL SLIDE SATU BARIS]

[Penjelasan]

Ketika Provinsi terlanjur

menyetujui peta sebelum Provinsi melakukan pengecekan

lanjutan.


---

## 📑 Slide 22: [JUDUL SLIDE SATU BARIS]

[Penjelasan]

Memonitor Semua

proses yang telah dilakukan dalam sistem

GS pada peta yang

bersangkutan.


---

## 📑 Slide 23: Materi Bagian 23

1. Proses Check Error
Batas Kab/Kota
2. Pengecekan
Manual
3. Persetujuan Peta
4. Pembatalan
Persetujuan
5. Kirim Ke Pusat

3. PEMROSESAN
DI BPS PROVINSI


---

## 📑 Slide 24: 1. PASTIKAN PETA 100% SUDAH DIUNGGAH OLEH  USER KAB/KOT

[JUDUL SLIDE SATU BARIS]

[Penjelasan]

Pastikan status peta tiap kabupaten kota adalah ‘Kirim Ke Provinsi’


---

## 📑 Slide 25: [JUDUL SLIDE SATU BARIS] 2. CEK BATAS KABUPATEN/KOTA

[Penjelasan]

Sistem akan melakukan cek batas, apakah masih terdapat gap/overlap antar kabupaten kota.


---

## 📑 Slide 26: [JUDUL SLIDE SATU BARIS] 2. CEK MANUAL

[Penjelasan]

Admin provinsi harus melakukan cek secara manual

dengan cara mendownload hasil peta yang telah di upload dan di cek oleh GS. Download semua file lalu

lakukan dissolve di qgis untuk mendapatkan batas

kab/kota

Beberapa hal yang perlu diperhatikan untuk pengecekan manual adalah beberapa hal dibawah:

- Polygon lengkap menutupi semua bagian daratan.

- Ada tidaknya wilayah kantong, dan lakukan konfirmasi apa bila ada wilayah kantong.


---

## 📑 Slide 27: [JUDUL SLIDE SATU BARIS] 3. PERSETUJUAN PETA DIGITAL

[Penjelasan]

Peta yang status nya sudah selesai diperiksa dan di cek batas kabupaten/kota nya selanjutnya dilakukan proses approval (persetujuan) oleh BPS Provinsi.


---

## 📑 Slide 28: [JUDUL SLIDE SATU BARIS] 3. KIRIM KE PUSAT

[Penjelasan]

Jika proses pemeriksaan dan persetujuan peta selesai dilakukan untuk seluruh Kabupaten/kota, maka selanjutnya peta digital dalam satu provinsi dikirimkan ke BPS Pusat dengan cara memilih Tombol “Submit ke Pusat”.


---

## 📑 Slide 29: [JUDUL SLIDE SATU BARIS] 4. PUSAT REJECT

[Penjelasan]

1. Peta yang tidak disetujui oleh user pusat akan dikembalikan pada user Provinsi. 2. PIC pusat akan memberikan keterangan kab/kot mana saja yang masih bermasalah. 3. Provinsi mengembalikan peta pada user kab/kot yang bersangkutan


---

## 📑 Slide 30: Status Transfer Data dan Pengecekan Geotagging di GS

- 
Alur
pemrosesan
geotagging
di
GS
hampir
sama
dengan alur pemrosesan peta. Hanya saja terdapat
perbedaan di bagian pengecekan error.

- 
Pengecekan
error
atau
kontrol
kualitas
pada
pemrosesan titik bangunan di GS dilakukan untuk
memvalidasi apakah terdapat ketidaklengkapan atribut
pada peta geotagging yang diunggah atau tidak.

- 
Perlu diperhatikan bahwa upload peta geotagging
hanya dapat dilakukan jika sudah masuk ke dalam
jadwal upload peta geotagging, yaitu mulai tanggal 16
November 2026. Dengan kata lain, pastikan jadwal
upload geotagging telah mencakup tanggal tersebut
agar sistem dapat menerima dan memproses data
geotagging dengan benar.


---

## 📑 Slide 31: Proses Pengecekan Peta Geotagging di  Geospatial System

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 32: Proses Pengecekan Peta Geotagging di Geospatial System

1 OPEN JOB

Tahap awal dalam proses pengecekan peta geotagging di GS adalah membuka (open) job pemrosesan landmark untuk mengunggah hasil lapangan.

1.1 Tampilan Awal Daftar Job Pemrosesan 1.2 Konfirmasi Open Job

1 1

Pada menu Unggah Landmark, pilih jenis landmark yang akan diproses. Klik ikon folder pada kolom paling kanan. Akan muncul notifikasi konfirmasi open job.


---

## 📑 Slide 33: Proses Pengecekan Peta Geotagging di Geospatial System

2 UNGGAH

Tahap awal dalam proses pengecekan peta geotagging di GS adalah membuka (open) job pemrosesan landmark untuk mengunggah hasil lapangan.

2.1 Pilih jenis landmark

1

1. Pada menu Unggah Landmark, pilih jenis
landmark yang akan diunggah.
2. Klik Ikon Unggah pada kolom paling kanan

2.2 Isi form unggah 2.3 Status Unggahan 2.1 2.2

1 1

1. Isi kolom Keterangan (opsional) sesuai
kebutuhan.
2. Klik "Pilih file..." lalu pilih file GeoJSON yang
sudah dikompres (.zip).
3. Klik "Mulai Unggah" untuk memulai proses
unggah.

Checklist Sebelum Unggah Unggah peta geotagging dilakukan ketika unggah Peta SLS/sub-SLS telah selesai hingga submit ke provinsi.

1. Setelah unggah berhasil, sistem akan otomatis
melakukan pengecekan error.
2. File yang telah diunggah dapat diunduh kembali
atau melihat riwayat melalui ikon yang tersedia.


---

## 📑 Slide 34: Proses Pengecekan Peta Geotagging di Geospatial System

2.1 KETENTUAN FILE YANG DIUNGGAH

Sebelum sistem melakukan proses pengecekan error, pastikan file peta geotagging yang diunggah telah sesuai ketentuan berikut.

Atribut Wajib pada Peta Geotagging

1

Atribut berikut wajib memiliki dan tidak boleh kosong (not null), kecuali yang berstatus nullable.

Format File dan Penamaan File 2

File yang diunggah adalah file GEOJSON (.geojson) yang dikompres ke dalam ZIP (.zip)

Sumber Format Nama Contoh

03_Output/03_Pet a Geotagging dan Muatan

final_landmark_{idkab}_ se_2026.geojson

final_landmark_1101_se_ 2026.geojson


---

## 📑 Slide 35: Proses Pengecekan Peta Geotagging di Geospatial System

3 Pengecekan Error

Setelah file berhasil diunggah, sistem akan secara otomatis melakukan pengecekan kualitas file dan kelengkapan atribut. Status pada tabel akan berubah sesuai dengan hasil pengecekan.

3.1 Sedang Proses Check Error

Sistem sedang melakukan pengecekan kualitas file setelah unggah berhasil.

1

2.2 Proses Pengecekan Selesai 3.3 Invalid File 2.1 3.2

Pengecekan selesai dan file dinyatakan valid (tidak ada kesalahan format/atribut). File tidak sesuai ketentuan atau terdapat kesalahan format/atribut.

1 1


---

## 📑 Slide 36: Proses Pengecekan Peta Geotagging di Geospatial System

4 Lihat Laporan Hasil Pengecekan

Setelah proses pengecekan selesai, BPS Kabupaten/Kota dapat melihat laporan hasil pengecekan untuk mengetahui apakah titik bangunan sesuai dengan batas desa atau terdapat titik bangunan di luar batas desa.

Klik ikon pada tanda untuk melihat laporan hasil pengecekan

4.1 Tombol Lihat Laporan 4.2 Laporan Hasil Pengecekan

1 1

Sistem akan menampilkan ringkasan hasil pengecekan.
- 
Jika semua titik bangunan sesuai dengan batas SLS/Sub SLS →"Tidak ada
titik bangunan di luar batas SLS/Sub SLS"
- 
Jika terdapat titik bangunan di luar batas SLS/Sub SLS →"Terdapat titik
bangunan di luar batas SLS/Sub SLS"


---

## 📑 Slide 37: Proses Pengecekan Peta Geotagging di Geospatial System

5 Kirim ke Provinsi

Setelah hasil pengecekan sesuai (tidak terdapat error), landmark dapat dikirim ke Admin Provinsi untuk proses validasi dan persetujuan.

5.1 Tombol kirim ke provinsi 5.2 Konfirmasi kirim ke provinsi

1 1

Akan muncul notifikasi konfirmasi pengiriman. Klik "Ya, Kirim" untuk mengirim landmark ke Admin Provinsi.

Klik ikon pada tanda


---

## 📑 Slide 38: Proses Pengecekan Peta Geotagging di Geospatial System

6 Provinsi Approve / Reject

Admin Provinsi akan melakukan pemeriksaan (validasi) terhadap landmark yang dikirim oleh BPS Kabupaten/Kota, kemudian memberikan keputusan Approve atau Reject.

6.1 Provinsi Approve 6.2 Provinsi Reject

Pilih data landmark yang akan diperiksa. 1

Pilih data landmark yang akan diperiksa. 1

1 1

2 Pilih hasil pemeriksaan "Approve".

2 Pilih hasil pemeriksaan "Reject".

3 Isi catatan (opsional), lalu klik "Simpan".

3 Isi catatan berisi alasan/masukan, lalu klik "Simpan".


---

## 📑 Slide 39: Proses Pengecekan Peta Geotagging di Geospatial System

7 Sinkronisasi ke Production

Status "Selesai Sync ke Production" menunjukkan bahwa Landmark telah berhasil disinkronisasikan ke Production.


---

## 📑 Slide 40: Monitoring Pengolahan Peta Pada Geospasial System

[https://dataspasial.bps.go.id/gs](https://dataspasial.bps.go.id/gs)

- 
Monitoring pengolahan peta dilakukan untuk memantau progres pada
setiap tahapan proses pengolahan, mulai dari unggah peta,
pengecekan kualitas, pengiriman ke provinsi, pengecekan batas
kabupaten, pengiriman ke pusat, pengecekan batas provinsi, persetujuan
dari pusat, hingga penetapan status final peta.

1

- 
Monitoring ini dilakukan melalui aplikasi Geospatial System yang dapat
diakses pada link berikut

- 
Login menggunakan akun SSO masing-masing pegawai. Jika terdapat
user yang belum dapat mengakses dapat melaporkan ke admin
wilayahnya masing-masing agar ditambahkan pada sistem.

CARA MENGAKSES MONITORING

Klik menu Rekap dan pilih Peta Digital. 1

2 Pilih level peta (Provinsi atau Kabupaten/Kota) dan periode untuk menampilkan hasil monitoring. Akan muncul beberapa informasi terkait progres pengolahan peta pada kotak ringkasan (textbox).

3 Akan muncul beberapa informasi terkait progres pengolahan peta pada kotak ringkasan (textbox).


---

## 📑 Slide 41: Monitoring Pengolahan Peta Pada Geospasial System

Informasi Kolom Monitoring

Pengecekan Kualitas (%) 3

Upload Peta (%) 2

Provinsi 1

Menunjukkan nama wilayah administrasi provinsi yang sedang dimonitor progres pengolahannya.

1

Submit ke Provinsi (%) 4

Persentase peta yang sudah dikirim (submit) dari Kabupaten ke Provinsi untuk proses verifikasi lebih lanjut.

1

Pengecekan Batas Provinsi 7

Status hasil pengecekan batas antar provinsi, biasanya mencakup: - Bebas Gap (tidak ada celah antar wilayah) - Bebas Overlap (tidak ada tumpang tindih wilayah)

1

Jika masih tanda X, berarti belum lolos atau belum dilakukan pengecekan.

Persentase jumlah peta yang sudah berhasil diunggah ke sistem dibandingkan dengan total peta yang seharusnya tersedia.

1

Pengecekan Batas Kabupaten (%) 5

Persentase peta yang telah diperiksa terkait kesesuaian batas wilayah administrasi kabupaten/kota, termasuk potensi overlap atau gap antar wilayah.

1

Pusat Approve (%) 8

Persentase data yang telah disetujui oleh pusat setelah melalui seluruh tahapan pengecekan.

1

Persentase peta yang telah melalui proses pengecekan kualitas, seperti kesesuaian format, kelengkapan atribut, dan standar topologi.

1

Submit ke Pusat 6

Menunjukkan status apakah data sudah dikirim ke pusat: - : sudah dikirim - : belum dikirim

1

Final 9

Status akhir proses: - : seluruh tahapan telah selesai dan disetujui - : masih terdapat tahapan yang belum selesai atau belum disetujui

1


---

## 📑 Slide 42: Monitoring Pengolahan Peta Pada Geospasial System

Halaman Progres Pengolahan Peta

HALAMAN PROGRES PENGOLAHAN PETA LEVEL PROVINSI HALAMAN PROGRES PENGOLAHAN PETA LEVEL KABUPATEN/KOTA


---

## 📑 Slide 43: Materi Bagian 43

TERIMA KASIH
