---
judul: "Pengolahan Peta Digital Wilkerstat di QGIS"
modul: "07"
kegiatan: "Sensus Ekonomi 2026 - Wilkerstat"
total_slide: 52
berkas_sumber:
  pdf: "../pdf/07-pengolahan-peta.pdf"
topik_utama:
  - "Georeferencing Peta Sketsa Lapangan (Freehand Raster Georeferencer)"
  - "Digitasi dan Editing Poligon Batas SLS/Non-SLS"
  - "Penggunaan Plugin Clipper & Dissect/Dissolve Overlap"
  - "Pengecekan Topologi Batas (Topology Checker) - Anti Gap & Overlap"
  - "Pembuatan Layout Peta Final, QR Barcode, dan Ekspor PDF Siap Cetak"
---

# Pengolahan Peta Digital Wilkerstat di QGIS

> **Pelatihan Instruktur Daerah (Inda)**  
> *Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026*  
> **Direktorat Metodologi Statistik dan Sains Data - BPS RI**


---

## 📑 Slide 1: Materi Bagian 1

PENGOLAHAN PETA

Pelatihan Instruktur Daerah Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026

27 Agt – 02 Sept 2026


---

## 📑 Slide 2: KERANGKA PAPARAN

Alur Pengolahan Peta 01

Editing Peta Digital 02

Cleaning dan Validasi Peta Hasil Editing 03

Dissolving Peta WIlkerstat 04

Pengecekkan Kualitas Peta 05

Layouting Peta 06


---

## 📑 Slide 3: Materi Bagian 3

01 ALUR PENGOLAHAN PETA


---

## 📑 Slide 4: Alur Pengolahan Peta

Kegiatan pengolahan peta wilkerstat hasil SE2026 terdiri dari :

BPS Kabupaten/Kota bertanggungjawab pada kegiatan nomor : 1,2,3,4,5,6 dan 9​

BPS Provinsi bertanggungjawab pada kegiatan nomor : 7

BPS Pusat/Direktorat MSSD bertanggungjawab pada kegiatan nomor : 8​


---

## 📑 Slide 5: Materi Bagian 5

Diagram Alur

Pengolahan

Peta


---

## 📑 Slide 6: Materi Bagian 6

Diagram Alur Pemeriksaan, approval dan layouting Peta Wilkerstat


---

## 📑 Slide 7: Materi Bagian 7

02 EDITING PETA DIGITAL


---

## 📑 Slide 8: Identifikasi perubahan SLS/sub-SLS

Identifikasi perubahan batas SLS/sub-SLS dilakukan untuk memfilter / menunjukan wilayah SLS/sub-SLS mana saja yang mengalami perubahan batas dan harus dilakukan pemutakhiran batas wilayahnya.

Langkah-langkah dalam identififikasi:

1. Join peta SLS/sub-SLS dengan data hierarki SLS/sub-SLS yang dilengkapi dengan flag perubahan batas SLS/sub-SLS 2. Simbolisasi SLS yang berubah 3. Identifikasi perubahan SLS

Contoh Peta SLS/sub-SLS Kota Tangerang Selatan (3674)

Contoh Hierarki Kota Tangerang Selatan (3674) yang

Mengalami Perubahan Batas


---

## 📑 Slide 9: Identifikasi perubahan SLS/sub-SLS

1. Join hierarki SLS/sub-SLS dengan peta SLS/sub-SLS
Tahapan:
1)
Siapkan data hierarki SLS/sub-SLS
yang dilengkapi dengan flag perubahan batas SLS/sub-
SLS dan peta SLS/sub-SLS. Pastikan terdapat IDSLS pada
data hierarki dan pada peta SLS/sub-SLS.
2)
Import peta SLS/sub-SLS dan data hirarki ke dalam layer di
QGIS.
3)
Klik kanan pada layer peta SLS/sub-SLS, pilih ‘Properties’ →
‘Join’ →klik tombol (+) →atur ‘Join field’ = idsubsls_25_2
(data hirarki) dan ‘Target field’ = idsubsls.
4)
(Opsional) Klik (√) pada ‘Joined fields’ →Klik (√) pada field
‘‘idsubsls_26_1”, “nmsls_26_1”, “id_perub”, “ket_perub”,
“berubah_batas”, kemudian klik OK.
5)
(Opsional) Klik (√) pada Custom field name prefix dan ubah
sesuai kebutuhan.


---

## 📑 Slide 10: Identifikasi perubahan SLS/sub-SLS

2. Simbolisasi SLS/sub-SLS yang berubah
Setelah menjoinkan peta SLS/sub-SLS dengan data hierarki, selanjutnya dilakukan pengaturan simbolisasi warna untuk
memudahkan identifikasi SLS/sub-SLS yang mengalami perubahan wilayah.
Tahapan yang dilakukan:
1)
Klik kanan pada layer peta SLS/sub-SLS →pilih Properties →Symbology →Categorized
2)
Pilih ‘berubah_batas’ sebagai Value →kemudian klik Classify
3)
Atur warna simbol ‘all others’ transparan fill →Klik OK
4)
Pada Legend, ubah value (1) = ‘Ada Perubahan Batas’ dan (2) = ‘Tidak Ada Perubahan Batas’

2

1

4

3


---

## 📑 Slide 11: Identifikasi perubahan SLS/sub-SLS

3. Identifikasi Perubahan SLS/sub-
SLS

Langkah identifikasi SLS/sub-SLS yang mengalami perubahan: 1) Klik kanan layer peta SLS/sub-SLS →pilih ‘Open Attribute Table’ 2) Klik 'Select features using an expression’, kemudian masukkan formula “berubah_batas” = 1. Kemudian, klik ‘Select Features’ 3) Klik dan ganti ‘Show All Features’ menjadi ‘Show Selected Features’ untuk melihat daftar SLS/sub-SLS yang mengalami perubahan batas


---

## 📑 Slide 12: Editing Peta Digital

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 13: Koreksi Non Topologis

Memotong Poligon : Digunakan untuk mengoreksi perubahan batas wilayah SLS/sub-SLS.

Muat file peta digital SLS dan peta scan hasil

georeferensi

hasil pemotongan klik “toogle editing” untuk

mengakiri proses editing

Aktifkan peta digital SLS ->

Klik Toggle editing untuk

memulai editing

Lengkapi attribute polygon

Pilih SLS yang akan di

koreksi batasnya ->

Zoom In

Potong polygon dengan menggunakan tool “split

feature”


---

## 📑 Slide 14: Koreksi Non Topologis

Menggabungkan Poligon : Digunakan untuk menggabungkan dua atau lebih poligon

wilayah SLS/sub-SLS untuk membentuk satu wilayah baru.

Muat file peta digital SLS dan peta scan hasil

georeferensi

klik “toogle editing” untuk

mengakiri proses editing

Aktifkan peta digital SLS ->

Klik Toggle editing untuk

memulai editing

Pilih Attribute polygon yang

akan digunakan sebagai

attribute polygon hasil

gabung

Pilih SLS  yang akan di

gabung

Gabung polygon SLS menggunakan “ Merge

Selected Feature”


---

## 📑 Slide 15: Koreksi Non Topologis

Membuat Poligon dalam polygon (poligon Kantong) : Digunakan untuk menggambar/membuat polygon SLS/sub-SLS/non-SLS kantong .

Muat file peta digital SLS dan peta scan hasil

georeferensi

Simpan hasil edit lalu non

aktifkan “toggle editing”

untuk ‘stop editing

Aktifkan peta digital SLS ->

Klik Toggle editing untuk

memulai editing

Pilih Attribute polygon yang

akan digunakan sebagai

attribute polygon hasil

gabung

Klik “fill Ring Button”

Buat polygon sesuai dengan yang batas yang

tergambar di peta scan”


---

## 📑 Slide 16: Koreksi Non Topologis

Editing Attribut peta:

Muat file peta digital SLS dan peta scan hasil

georeferensi

Untuk mengupdate attribute polygon wilayah sls yang mengalami perubahan baik dengan perubahan batas maupun tidak.

Aktifkan peta digital SLS ->

Klik Toggle editing untuk

memulai editing

Simpan hasil edit lalu non

aktifkan “toggle editing”

untuk ‘stop editing

Select polygon SLS/SubSLS yang akan di

ubah attributnya

Isi attribute polygon sls

dengan benar dan

lengkap


---

## 📑 Slide 17: Contoh Kasus

5. Contoh SLS/sub-SLS yang terdampak karena
Perubahan Batas SLS/sub-SLS

idsubsls_1 Nama SLS Lengkap Prov Kab / Kota Kec Desa/ Kel

Nama Desa / Kelurahan

Kode SLS /Non SLS Sub SLS idsubsls_2 Muatan Dominan

1 - Ya 2 - Tidak 3674010001001101 RT 010 RW 004 36 74 010 001 KRANGGAN 0011 00 3674010001001100 1 RT 010 RW 004 MULYADI 1 1 3674010001001102 RT 010 RW 004 36 74 010 001 KRANGGAN 0024 00 3674010001002400 1 RT 011 RW 004 CASLI 1 1 3674010001001102 RT 010 RW 004 36 74 010 001 KRANGGAN 0025 00 3674010001002500 1 RT 012 RW 004 WIDA 1 1 3674010001000900 RT 014 RW 003 36 74 010 001 KRANGGAN 0009 00 3674010001000900 1 RT 014 RW 003 SAMWANI 1 1 3674010001000900 RT 014 RW 003 36 74 010 001 KRANGGAN 0026 00 3674010001002600 1 RT 015 RW 003 TATAT 1 1 3674010002001300 RT 003 RW 004 36 74 010 002 MUNCUL 0013 00 3674010002001300 1 RT 003 RW 004 IIN .H 2 1 3674010002001400 RT 004 RW 004 36 74 010 002 MUNCUL 0013 00 3674010002001300 1 RT 003 RW 004 IIN .H 2 1

- 
Wilayah SLS RT 010 RW 04 Kelurahan kranggan Kecamatan Setu Kota Tangerang Selatan (ID SLS 36740100010001)
memiliki dua Sub SLS yaitu Sub SLS 01 dan 02 mengalami pemekaran menjadi 3 wilayah RT,  yaitu: RT 010 sebagai induk ,
RT 11, dan RT 12 sebagai wilayah SLS Baru.
- 
Wilayah SLS RT 014 RW 003 Kelurahan kranggan Kecamatan Setu Kota Tangerang Selatan (ID SLS 36740100010009) pecah
menjadi RT 014 dan RT 015
- 
Wilayah SLS RT 004 RW 04 kelurahan Muncul Kecamatan Setu Kota Tanggerang Selatan (ID SLS 3674010002001400)
bergabung dengan RT 003 RW 04 kelurahan Muncul Kecamatan Setu Kota Tanggerang Selatan

Status Peruba han Wilayah SLS / Sub SLS

Apakah terdapat perubahan batas SLS?

Nama SLS Lengkap

Ketua SLS (Terkecil)


---

## 📑 Slide 18: Materi Bagian 18

03 CLEANING DAN VALIDASI PETA HASIL EDITING


---

## 📑 Slide 19: Cleaning dan Validasi Peta Hasil Editing

Tools Cleaning dan Validasi Peta Digital
Untuk memudahkan proses cleaning dan validasi peta digital, Tim BPS Pusat telah
menyediakan Model QGIS. Berikut adalah tahapan untuk mendownload tools
tersebut.
1. Buka Geospasial System
2. Menu Bahan/Template
3. Download bahan yang Bernama “QGIS Model Pengolahan Peta”
4. Extract
5. Import Model ke dalam QGIS

Tujuan

Menghilangkan error

dan meningkatkan kualitas peta digital

hasil editing

Tipe Koreksi Cleaning / Validasi

2

- 
Cleaning Null dan
Invalid Geometry
- 
Cleaning Error
Topology
(Gap/Overlap)
- 
Validasi Atribut
- 
Export Peta Digital

3

4

5


---

## 📑 Slide 20: Jenis Geometry Error dan Topology Error

2. Gap

1. Invalid Geometry

Null Geometry Attribut ada tapi geometry

tidak ada.

Duplicate Vertices Titik-titik (vertices) yang berulang pada lokasi yang sama dalam sebuah garis atau

polygon.

Self-Intersection Polygon yang memiliki garis-garis

yang saling berpotongan dengan

dirinya sendiri, menciptakan area

yang tidak valid.

Non-closed Rings Polygon yang tidak tertutup dengan benar, yaitu garis awal dan akhir tidak

bertemu pada titik yang sama.

Gap mengacu pada area kosong atau celah yang tidak tertutup antara dua atau lebih polygon yang seharusnya bersebelahan tanpa ada ruang kosong.

3. Overlaps

Overlap terjadi ketika dua atau lebih polygon saling menutupi sebagian atau seluruh area yang sama.


---

## 📑 Slide 21: Cleaning Error Topology (QGIS)

1. Pengecekkan Topology

Gunakan tools Topology Checker untuk mendeteksi adanya Gap ataupun Overlaps antar poligon. Buka tools Topology Checker melalui Tab Vector, kemudian akan mucul Topology Checker Panel. Klik tombol untuk mengisikan konfigurasi Topology Rule. Isikan seperti contoh berikut.

Penjelasan:

Rule #1 : Must not have gaps (untuk mendeteksi keberadaan gaps)

Rule #2 : Must not overlap (untuk mendeteksi keberadaan overlap)

Rule #3 : Must not have duplicates (untuk mendeteksi adanya duplikasi)

Rule #4 : Must not have invalid geometries (untuk mengetahui poligon yang masih memiliki invalid geometri)


---

## 📑 Slide 22: Cleaning Error Topology (QGIS) - Null Geometry

2. Cleaning Null Geometry

Tahapan cleaning Null Geometry menggunakan QGIS:

1. Tampilkan peta SLS/sub-SLS di QGIS kemudian gunakan tools “Remove Null Geometries” pada Processing Toolbox.

2. Double klik untuk mengaktifkan tools tersebut sehingga muncul dialog box Remove Null Geometries.

3. Isikan parameter sesuai dengan kebutuhan:

- 
Input layer : Layer Peta Digital (Peta SLS/sub-SLS)

- 
Centang “Also remove empty geometries”

- 
Atur non null geometries menjadi create temporary layer

- 
Atur null geometries menadi create temporary layer

Kemudian, klik Run hingga menghasilkan dua layer: null geometries dan non null geometries.

4. Cek pada layer Null geometries untuk mengetahui ada tidaknya kasus null geometries. Jika tidak ada Null geometries maka Save layer Non null geometries menjadi file *.gpkg

5. Jika terdapat null geometries, lakukan pembuatan polygon baru seperti yang dilakukan pada tahapan editing peta digital dan isikan atribut yang sesuai.


---

## 📑 Slide 23: Cleaning Error Topology (QGIS) - Invalid Geometry

3. Cleaning Invalid Geometry

1) Cek Validitas

Lakukan pengecekan invalid dengan menggunakan tools Cek_Validitas. Tools ini akan menghasilkan tiga layer temporary yaitu:

- 
Layer
Point_Invalid_Geometry,
merupakan
layer
yang
menginformasikan lokasi adanya
invalid geometry.

- 
Layer Fix_Geometries, merupakan
layer
hasil
perbaikan
geometri
dengan menggunakan algoritma
QGIS.

- 
Layer Poligon_Invalid_Geometry,
merupakan
layer
yang
menginformasikan
poligon
yang
memiliki invalid geometry.


---

## 📑 Slide 24: Cleaning Error Topology (QGIS) - Invalid Geometry

2) Perbaikan Invalid Geometry

Contoh Perbaikan

Sebelum melakukan perbaikan invalid geometri, pastikan pengaturan “Avoid Overlap to Active Layer” telah diaktifkan pada Snapping Toolbar.

Selanjutnya, untuk mengatasi invalid geometry, dapat dilakukan dengan dua cara yaitu:

- 
Perbaikan Poligon

Hapus vertex

Select pada poligon yang akan diperbaiki →potong poligon dengan menggunakan Split Feature →hapus potongan poligon yang mengandung vertex yang mengalami invalid geometry →buat poligon baru pada lokasi yang kosong tersebut →gabungkan poligon baru dengan poligon potongan yang lain.

- 
Perbaikan Vertex

Perbaikan dengan vertex dapat dilakukan dengan cara menghapus atau menggeser vertex yang mengalami invalid geometry.

Setelah melakukan perbaikan invalid geometry, ulangi proses cek validitas untuk mengetahui masih ada tidaknya invalid geometry.


---

## 📑 Slide 25: Cleaning Error Topology (QGIS)

4. Cleaning Overlaps

1

Plugin Clippers

Cara ini digunakan untuk overlap yang perlu diatasi secara manual/satu per satu (misal memiliki luasan daerah overlap yang luas). Tahapan: 1. Zoom pada lokasi overlap dengan cara klik 2x pada daftar error di topology checker panel. 2. Select pada poligon yang akan digunakan untuk memotong. 3. Kemudian potong dengan menggunakan plugins clipper dengan cara mengakses melalui tab Vector →Clipper →Clipper.

2

3

Hasil


---

## 📑 Slide 26: Cleaning Error Topology (QGIS)

5. Cleaning Gaps

1 2

3

Cara 1: Fitur Digitasi dengan Avoid Overlap on Active Layer Cara ini digunakan untuk permasalahan gap yang perlu diatasi secara manual/satu per satu (misal memiliki luasan daerah gap yang luas). 1. Zoom pada lokasi gap dengan cara klik 2x pada daftar error di topology checker panel. 2. Aktifkan fitur Avoid Overlap on Active Layer melalui Snapping Toolbar. 3. Aktifkan Toogle Editing pada layer yang akan di-edit. 4. Klik icon (Ctrl+.) untuk menambahkan poligon baru. 5. Digitasi di area yang terjadi gap. 6. Gabungkan poligon yang baru terbentuk dengan poligon SLS yang sesuai. Pastikan atribut yang terisi menggunakan poligon SLS yang benar.

4

Hasil

5 6


---

## 📑 Slide 27: Cleaning Error Topology (QGIS)

5. Cleaning Gaps

Cara 2: Processing Tool

Fill_Gaps
Cara ini digunakan untuk
permasalahan gap yang perlu
diatasi secara massal (misal gaps
tipis diantara perbatasan).
- 
Jalankan processing tool
Fill_Gaps dari Processing
toolbox panel.
- 
Isikan parameter Peta
SLS/sub-SLS dengan peta
SLS/sub-SLS yang
mengandung gap. Tools ini
akan menghasilkan satu layer
temporary bernama Result
yang telah clean dari gap.

Untuk memastikan file hasil cleaning topology terbebas dari invalid geometry, maka ulangi lagi

proses Cleaning Invalid Geometries


---

## 📑 Slide 28: Validasi Atribut

Pada tahap ini, dilakukan pengecekkan kelengkapan atribut (penamaan, tipe dan panjang data, dan atribut lainnya), apakah sudah sesuai dengan standar yang ditetapkan. Proses lainnya adalah pengecekan ID duplikat, sebelum dilakukan proses matching. Berikut adalah informasi mengenai atribut peta SLS/sub-SLS yang mutakhir dan diharapkan peta yang dibuat sudah mengikuti nama field dan tipe datanya.

No Nama Field Jenis Field Length

1 kdprov string 2

2 kdkab string 2

3 kdkec string 3

4 kddesa string 3

5 kdsls string 4

6 kdsubsls string 2

7 idsls string 14

8 idsubsls string 18

9 nmprov string 50

10 nmkab string 50

11 nmkec string 50

12 nmdesa string 50

13 nmsls string 100

14 rw_dki string 3

15 tingkat integer 1

16 nm_gedung string 50

17 posisi string 50

Selain itu, juga perlu dilakukan proses pengecekan atribut baik match atribut peta dengan master juga sebaliknya yaitu match master dengan atribut peta. Master SLS yang digunakan untuk melakukan pengecekan adalah Master Tahun 2026 Semester 1. Proses ini akan menggunakan tool Cek_Master_PetaSLS. Tahapan dalam melakukan pengecekan kesesuaian master dan peta SLS/sub-SLS adalah sebagai berikut:

1. Tampilkan layer Master dan Peta SLS/sub-SLS Hasil Editing.

2. Klik processing tools Cek_Master_PetaSLS.

3. Lengkapi isian parameter

Master : Master 2026 Semester 1

4. Klik Run.

5. Akan terbentuk temporary layer PetaSLS_Unmatch.

6. Cek atribut output, perbaiki peta batas SLS jika terdapat SLS yang memiliki nilai idsls_count tidak sama dengan 1.

Peta SLS/sub-SLS edit : Peta SLS/sub-SLS hasil edit


---

## 📑 Slide 29: Export File to GeoJSON

Pada tahapan ini, peta SLS/sub-SLS yang sudah tidak ada error (geometri, duplikat, atribut, dan topology) dapat diexport ke dalam bentuk format file “geojson” menggunakan software QGIS.

Beberapa kesalahan yang ditemui dari kegiatan sebelumnya antara lain:

1. Tidak menggunakan format file GeoJSON.

2. Tipe geometri tidak ada di GeoJSON.

3. Coordinate Reference System (CRS) bukan 4326.

4. CRS sudah 4326 namun extent-nya masih metric.

5. Tipe data bukan poligon (multipoligon).

6. Penamaan atribut bukan UTF-8.

Pastikan atribut peta yang diexport

sesuai dengan daftar atribut yang dijelaskan pada tahap validasi atribut

Untuk mencegah kesalahan tersebut terjadi, maka proses export ke GeoJSON perlu memperhatikan langkah-langkah berikut ini:

1. Pastikan format GeoJSON.

2. Nama file dengan format final_sls_<idkab>_2026- 1.geojson

3. CRS pilih EPSG:4326 – WGS 84.Cek Encoding UTF-8 (jika bukan UTF-8 maka perlu dilakukan encoding).

4. Geometry Type pilih Poligon.

5. Cek extent bukan metric (jika bukan metric maka perlu dilakukan reproject).


---

## 📑 Slide 30: Materi Bagian 30

04 DISSOLVING PETA WILKERSTAT


---

## 📑 Slide 31: Pembuatan Peta Desa dengan Dissolving Peta SLS/SubSLS

Tahapan ini akan membentuk peta desa dari peta SLS/sub-SLS yang sudah selesai dan final dengan cara dissolve. Tahapannya adalah sebagai berikut:

1. Tampilkan layer hasil finalisasi Peta SLS/sub- SLS.

2. Klik processing tools Dissolve_Desa_Kec.

3. Pilih peta SLS/sub-SLS pada Peta_SLS_Final.

4. Klik Run.

5. Ekspor temporary layer menjadi file permanen dengan nama file <idkab>_desa_2026-1.geojson dengan proyeksi peta EPSG 4326 untuk peta desa.

6. Unggah file peta desa yang terbentuk ke Geospatial System.

1

5

3

4

2

Pastikan batas desa hasil dissolve sudah sesuai dengan

penggabungan batas SLS


---

## 📑 Slide 32: Materi Bagian 32

05 PENGECEKAN KUALITAS PETA


---

## 📑 Slide 33: Tujuan:

Peta yang dihasilkan telah sesuai dengan kondisi hasil lapangan; Peta yang dihasilkan telah sesuai dengan master; Peta yang dihasilkan telah terbebas dari kesalahan geometri.

Cara Pengecekan: Manual --> menggunakan lembar pemeriksaan kualitas peta Otomatis --> Melalui GS

Form Pemeriksaan kualitas peta dapat di unduh di alamat:

"[http://s.bps.go.id/form_pengecekan_kualitas_peta"](http://s.bps.go.id/form_pengecekan_kualitas_peta")


---

## 📑 Slide 34: Lembar Pemeriksaan Kualitas Peta

*(Slide memuat diagram/grafis alur visual)*


---

## 📑 Slide 35: Lembar Pemeriksaan Kualitas Peta (Rincian Kolom)

Kolom (1): “Nomor urut”, Isikan nomor urut pengecekan

Kolom (2): “IDSLS”, Isikan Identitas wilayah SLS yang di periksa

Kolom (3): “Nama SLS”, Isikan Nama Wilayah SLS yang diperiksa

Kolom (4): “Georeferensi sudah benar ?”, Isikan kode hasil pemeriksaan georefensi peta scan

SLS pada wilayah SLS yang diperiksa

Kolom (5): “Jumlah Perubahan Batas SLS pada Peta WS”,Isikan jumlah perubahan Batas SLS

di peta WS pada wilayah SLS yang diperiksa (jumlah lokasi)

Kolom (6): “Jumlah Perubahan Batas SLS pada Peta Digital”, Isikan jumlah perubahan Batas

SLS di peta digital pada wilayah SLS yang diperiksa (jumlah batas

yang sudah dilakukan editing)

Kolom (7): “Editing Perubahan Batas sudah sesuai ?”, Isikan kode yang sesuai dengan hasil

pemeriksaan pada wilayah SLS yang diperiksa


---

## 📑 Slide 36: Lembar Pemeriksaan Kualitas Peta (Rincian Kolom)

Kolom (8): “Jumlah Sub SLS pada Peta WS”, Isikan jumlah sub SLS yang terdapat di Peta WS

yang diperiksa

Kolom (9): “Jumlah Sub SLS pada Peta Digital”, Isikan jumlah subsls yang terdapat di peta

digital pada wilayah SLS yang diperiksa

Kolom (10): “Jumlah Sub SLS sudah sesuai ?” Isikan kode yang sesuai dengan hasil

pemeriksaan pada wilayah SLS yang diperiksa

Kolom (11): “Batas seluruh Sub SLS sudah sesuai ?”, Isikan kode yang sesuai dengan hasil

pemeriksaan pada wilayah SLS yang diperiksa

Kolom (12): “Atribut seluruh Sub SLS sudah sesuai ?”, Isikan kode yang sesuai dengan hasil

pemeriksaan pada wilayah SLS yang diperiksa

Kolom (13): “Tindak Lanjut”, Isikan kode yang sesuai dengan hasil pemeriksaan pada wilayah

SLS yang diperiksa


---

## 📑 Slide 37: Tata Cara pengecekan:

1.
Persiapkan dokumen berikut :
- Peta digital SLS/Sub-SLS hasil editing;
- Peta WS/WSS hasil lapangan (peta analog);
- Scan Peta WS/WSS yang telah di-georeferensi.

2.Pilih paling sedikit 10 SLS tiap kecamatan untuk dilakukan pemeriksaan. 3.Tampilkan scan Peta WS yang telah di-georeferensi di QGIS dan overlay- kan dengan peta digital SLS/Sub-SLS hasil editing. 4.Periksa kesesuaian peta digital SLS/Sub-SLS hasil editing dengan scan Peta WSS yang telah di-georeferensi.


---

## 📑 Slide 38: Tata Cara pengecekan:

Kesesuaian yang dimaksud yaitu:

- 
Ketepatan dalam melakukan georeferensi (georeferensi sudah benar?)


---

## 📑 Slide 39: Kesesuaian yang dimaksud yaitu:

- 
Kelengkapan dan ketepatan dalam melakukan editing perubahan batas (editing perubahan batas

sudah sesuai?)


---

## 📑 Slide 40: Kesesuaian yang dimaksud yaitu:

- 
Kelengkapan dalam melakukan penyesuaian atribut tiap SLS/sub-SLS

(atribut seluruh SLS/sub-SLS sudah sesuai?)

5. Berikan rekomendasi tindak lanjut setelah dilakukan pengecekan.


---

## 📑 Slide 41: Pengiriman hasil Pemeriksaan

Setelah pemeriksaan kualitas peta selesai semua , tabel hasil pemeriksaan

diunggah ke folder hasil pemeriksaan kualitas peta pada tautan berikut:

[http://s.bps.go.id/Hasil_pemeriksaan_kualitas_peta.](http://s.bps.go.id/Hasil_pemeriksaan_kualitas_peta.)


---

## 📑 Slide 42: Materi Bagian 42

06 LAYOUTING PETA


---

## 📑 Slide 43: Layouting Peta Digital

➢Unduh folder template layout (versi Layout_Peta_WAWBWSWSS_2025) melalui Geospatial System pada menu ‘Bahan dan Template’.

Proses
ini
bertujuan
untuk
menyusun
tata
letak
peta
wilkerstat sehingga didapatkan file peta yang dapat dicetak
menjadi peta analog. Output file peta yang dihasilkan yaitu
Peta SLS/sub-SLS dan Peta WA menurut SLS/sub-SLS.
1. Persiapan Layouting Peta
➢Pastikan QGIS yang terinstal minimal QGIS 3.28.5.
➢Pastikan
telah
terinstal
plugin
yang
dibutuhkan
yaitu Quickmapservices dan QR Barcode Layout Item.

Pastikan folder tersebut telah lengkap berisi file berikut:

o Batas Perairan Indonesia.gpkg o Batas Provinsi Indonesia.gpkg o Batas Kabupaten Indonesia.gpkg o xxxx_Layout_Peta_WAWBWSWSS-2025.qgz o Layout_PETA_WAWBWS-2025.qpt o Logo BPS.png o Folder Peta Digital


---

## 📑 Slide 44: Layouting Peta Digital

2. Pelaksanaan Layouting Peta
➢Buka file template Project Layout Peta pada QGIS

1. Persiapan Layouting Peta
➢Ubah penamaan (xxxx) pada file

xxxx_Layout_Peta_WAWBWSWSS-2025.qgz menjadi 4 digit kode masing-masing kabupaten/kota.

dengan cara klik 2x pada file template Project Peta WAWBWSWSS-2025.

➢Siapkan file peta digital wilkerstat yang dapat

diunduh melalui Geospatial System dan simpan ke dalam folder Peta Digital, yaitu :

o final_kec_20261xxxx.geojson o final_desa_20261xxxx.geojson o final_sls_20261xxxx.geojson

Pada dialog box yang muncul (Handle Unavailable Layer), koneksikan layer dengan file peta digital yang sesuai.


---

## 📑 Slide 45: Layouting Peta Digital

2. Pelaksanaan Layouting Peta
Koneksikan dengan Peta Batas Kecamatan

Koneksikan dengan Peta Batas Desa


---

## 📑 Slide 46: Layouting Peta Digital

➢Setelah tampilan projek QGIS muncul maka dalam layer panel

2. Pelaksanaan Layouting Peta

akan terdapat 7 grup layer yaitu :

o Batas Wilayah : menampilkan batas Perairan Indonesia hingga batas desa o Peta WS : digunakan untuk membuat Peta SLS/non-SLS o Peta WS Inset : digunakan untuk membuat inset Peta SLS/non-SLS o Peta WSS : digunakan untuk membuat Peta SLS/sub-SLS o Peta WB : digunakan untuk membuat Peta blok sensus o Peta WB Inset : digunakan untuk membuat Inset Peta blok sensus o Peta WA : digunakan untuk membuat Peta desa/kelurahan o Basemap : kumpulan basemap yang digunakan.

Koneksikan dengan Peta Batas SLS/Sub SLS

Setelah semua layer terkoneksi lalu klik Apply Changes. Jika masih ada yang berwarna merah maka source data tidak ditemukan, cari dengan menekan tombol browse untuk melakukan koneksi secara manual. Namun jika layer tidak digunakan maka dapat diabaikan dengan klik tombol Keep Unavailable Layers.


---

## 📑 Slide 47: Layouting Peta Digital

2. Pelaksanaan Layouting Peta

➢Buka template layout peta WSS

(Project →Layouts →PETA WSS).

➢Untuk membuat Peta WSS (Peta SLS/Sub-SLS) aktifkan

(check box) Grup Layer Batas Wilayah, Peta WSS dan Basemap.


---

## 📑 Slide 48: Layouting Peta Digital

➢Untuk menghasilkan output file image klik tombol 'Exports

2. Pelaksanaan Layouting Peta

Atlas as Images'. Kemudian atur sesuai output yang diinginkan.

➢Kemudian klik tombol preview image untuk

menjalankan proses generate atlas.


---

## 📑 Slide 49: Layouting Peta Digital

2. Pelaksanaan Layouting Peta

➢Untuk membuat Peta WA (Peta Desa/Kelurahan) aktifkan

(check box) Grup Layer Batas Wilayah, Peta WA dan

non-aktifkan (uncheck box) Basemap, karena basemap Peta WA menggunakan google road.

➢Pastikan layer terpiilih sudah tidak ada tanda

Setelah tidak ada tanda , artinya semua layer sudah terkoneksi dengan peta digitalnya. Selanjutnya memilih Project --> Layouts --> PETA WA


---

## 📑 Slide 50: Layouting Peta Digital

2. Pelaksanaan Layouting Peta

Karena belum tampil peta lokasi maka perlu koneksikan dengan layer peta digitalnya, yaitu dengan memilih menu View --> Panels --> Item Properties.

Saat dibuka pilih icon preview image untuk melihat gambar Peta. Maka akan tampil peta desa/Peta WA dengan inset peta lokasi (masih proses tampil).


---

## 📑 Slide 51: Layouting Peta Digital

Selanjutnya, sama seperti Peta sub-SLS (Peta-WSS), untuk menghasilkan output file image klik tombol 'Exports Atlas as Images'. Kemudian atur sesuai output yang diinginkan.

2. Pelaksanaan Layouting Peta

Maka akan tampil seperti gambar berikut. Aktifkan (check box) pada 'Controlled by Atlas', karena pada 'scale' masih belum ada angka skala (‘nan’). Setelah 'Controlled by Atlas' aktif maka ‘nan’ pada skala akan terisi angka secara otomatis oleh sistem dan pada peta lokasi akan muncul gambar lokasi relatif peta desa pada ekstent yang sudah ditentukan (posisi desa dalam kecamatan).

Untuk menghaluskan garis batas dan warna beri tanda cek (√) pada ‘Enable antialiasing’, untuk mendapatkan image yang bergeoreference dan orientasi peta yang sesuai (portrait/landscape) beri tanda cek (√) pada ‘Generate world file’.


---

## 📑 Slide 52: Materi Bagian 52

TERIMA KASIH
