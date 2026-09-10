---
judul: "Pengolahan Titik Bangunan Geotagging SE2026"
modul: "06"
kegiatan: "Sensus Ekonomi 2026 - Wilkerstat"
total_slide: 18
berkas_sumber:
  pdf: "../pdf/06-pengolahan-titik-bangunan.pdf"
topik_utama:
  - "Import dan Penggabungan Titik Geotagging Lapangan"
  - "Model Pengecekan Titik Bangunan di QGIS"
  - "Koreksi Titik Anomali, Outlier, dan Titik di Luar Batas SLS"
  - "Pemisahan Muatan Tempat Tinggal Biasa vs Usaha"
  - "Validasi Akurasi Koordinat dan Kelengkapan Atribut"
---

# Pengolahan Titik Bangunan Geotagging SE2026

> **Pelatihan Instruktur Daerah (Inda)**  
> *Penetapan Kerangka Geospasial dan Muatan Wilkerstat SE2026*  
> **Direktorat Metodologi Statistik dan Sains Data - BPS RI**


---

## 📑 Slide 1: Materi Bagian 1

PENGOLAHAN TITIK BANGUNAN

Pelatihan Instruktur Daerah Pengolahan Kerangka Geospasial dan Muatan Wilkerstat SE2026

Jakarta, 27 Agt – 02 Sept 2026


---

## 📑 Slide 2: ALUR PENGOLAHAN TITIK BANGUNAN Mengolah posisi titik yang berada di luar batas SLS/Sub-SLS

Proses untuk memperbaiki posisi titik bangunan hasil pendataan lapangan SE2026 yang berada di luar batas peta wilayah kerja (SLS / Non-SLS / Sub-SLS), sekaligus memastikan seluruh atribut data-nya lengkap dan konsisten sebelum digunakan pada tahap berikutnya.


---

## 📑 Slide 3: Materi Bagian 3

PROSES PENGOLAHAN TITIK BANGUNAN


---

## 📑 Slide 4: TAHAPAN PENGOLAHAN TITIK BANGUNAN

Proses pengolahan titik bangunan dilakukan melalui 3 tahapan utama untuk memastikan posisi titik berada dalam SLS/Sub-SLS yang sesuai.

Peta Geotagging

Peta Geotagging

Peta Geotagging

Peta Geotagging

Peta Geotagging

Notes: Tahapan proses pengolahan titik bangunan ini bersifat iteratif. Jika masih ada titik yang berada di luar batas SLS/Sub-SLS

maka proses editing dan pengecekan di iterasi hingga seluruh titik berada dalam batas SLS/Sub-SLS yang sesuai.


---

## 📑 Slide 5: HAL YANG PERLU DIPERHATIKAN

Sebelum melakukan proses pengolahan titik bangunan, pastikan folder dan kelengkapan tools maupun data input telah sesuai agar proses berjalan dengan lancer.

(Peta Geotagging)


---

## 📑 Slide 6: [00] PERSIAPAN PROJECT DAN IMPORT LAYER

[Ctrl + S]

02_Proses 03_Editing Geotagging dan Muatan


---

## 📑 Slide 7: [00] PERSIAPAN IMPORT MODEL

Shorkey: Ctrl + Alt + T


---

## 📑 Slide 8: [01] IDENTIFIKASI TITIK DI LUAR BATAS

Peta Geotagging

Cari model yang sudah di import sebelumnya.

Identifikasi Titik Bangunan

Layer Vector Point QGIS: Hasil Identifikasi Titik Bangunan


---

## 📑 Slide 9: [02] EDITING POSISI TITIK BANGUNAN

Input
Tools
Output
- Peta SLS/sub-SLS lapangan SE2026 (Periode 2025

Model QGIS: 01 Identifikasi Titik di Luar Batas.model3

Layer Vector Point QGIS: Hasil Identifikasi Titik Bangunan

Semester 2)

- Peta geotagging

QGIS Style: batas_wilkerstat.qml


---

## 📑 Slide 10: [02] EDITING POSISI TITIK BANGUNAN

Part 1


---

## 📑 Slide 11: [02] EDITING POSISI TITIK BANGUNAN

Part 2

Idsubsls dimana titik

seharusnya berada Idsubsls posisi

titik saat ini


---

## 📑 Slide 12: [02] EDITING POSISI TITIK BANGUNAN

Part 3


---

## 📑 Slide 13: [02] EDITING POSISI TITIK BANGUNAN

Part 3


---

## 📑 Slide 14: [04] PENGECEKAN DAN VALIDASI HASIL EDITING

Periode 2025_2


---

## 📑 Slide 15: Materi Bagian 15

ATRIBUT TITIK BANGUNAN


---

## 📑 Slide 16: [01] ATRIBUT TITIK BANGUNAN

bttk


---

## 📑 Slide 17: [02] PENYIMPANAN HASIL PENGOLAHAN

02_Proses 03_Editing Geotagging dan Muatan

{idkab}_geotagging_kor eksi.geojson


---

## 📑 Slide 18: Materi Bagian 18

TERIMA KASIH
