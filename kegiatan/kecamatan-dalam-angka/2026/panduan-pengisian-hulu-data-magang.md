# Panduan Pengisian Hulu Data Lapangan KCDA 2026
## Untuk Tim Pengumpul Data Lapangan, PIC Kecamatan, & Tim Magang

Dokumen ini merupakan panduan praktis penugasan pengumpulan data sektoral ke **Kantor Camat** untuk 9 kecamatan di Kabupaten Mempawah pada publikasi **Kecamatan Dalam Angka (KCDA) 2026**.

---

## 🎯 Di Mana Hulu Data yang Harus Diisi?

Seluruh data mentah yang menjadi hulu sistem otomasi KCDA 2026 berada di **Google Drive IPDS**:
👉 **Folder Utama**: `33. KCDA 2026` ([Buka Folder Drive](https://drive.google.com/drive/folders/1CiqfhV9v7Fh5tSZWf5DSqh_ya2QI6Tpg))  
👉 **Subfolder Hulu Data**: **`1. Data`** ([Buka Subfolder 1. Data](https://drive.google.com/drive/folders/1b3xsTrouRl3mQ1pRLFViciKl9S4cRHmQ))

Di dalam subfolder **`1. Data`**, terdapat 34 berkas Google Spreadsheet.  
**Tim Magang & Lapangan TIDAK PERLU mengisi semua berkas!** Sebagian besar data (Dukcapil, Pendidikan, IDM, Podes, Hortikultura) telah disediakan terpusat oleh tim IPDS/Pusat.

---

## 📝 9 Tabel Utama yang Wajib Diisi dari Kantor Camat

Berikut adalah **9 berkas Google Spreadsheet spesifik** yang wajib dikonfirmasi, dimintakan ke Kantor Camat, dan diisikan oleh tim magang:

| No | Nama Tabel di Folder `1. Data` | Hal yang Dikonfirmasi ke Kantor Camat | Tautan Langsung Spreadsheet Hulu |
| :-: | :--- | :--- | :--- |
| **1** | **1.2 Jarak ke Ibukota Kecamatan** | Jarak dari tiap kantor desa ke kantor camat & ibukota Mempawah (km). | [Buka Sheet 1.2](https://docs.google.com/spreadsheets/d/14FvPtJSYS2EgAQ1nzKzY-CX8l7t7A1rWJeHCgCZ3XzY) |
| **2** | **1.3 Batas Administrasi Kecamatan** | Batas wilayah Utara, Selatan, Barat, Timur kecamatan. | [Buka Sheet 1.3](https://docs.google.com/spreadsheets/d/12Ohl8ShLolVXWRD7dBBtNNPqNfX_9pgAFFVYNbMLJ0U) |
| **3** | **1.4 Jarak Kantor Camat** | Jarak kantor camat ke tempat penting / RSUD / pelabuhan (km). | [Buka Sheet 1.4](https://docs.google.com/spreadsheets/d/10DAiZQaRpS7-w0qfA6OO_D6oIPCLzmVODciMRdu5Guo) |
| **4** | **2.1.1 Jumlah RW dan RT** | Jumlah mutakhir RW dan RT per desa/kelurahan tahun 2025. | [Buka Sheet 2.1.1](https://docs.google.com/spreadsheets/d/1Z-0jhg8zWUhqZrL1Raaju-W5fpGUwn_gBCViU-ZeL88) |
| **5** | **2.1.2 Nama-Nama Camat** | Daftar nama Camat, masa jabatan, dan Camat aktif saat ini. | [Buka Sheet 2.1.2](https://docs.google.com/spreadsheets/d/1BjxvpODk5TZR8aLXCbzzPt4yoa9F9vpQ4t1nIXQG2gg) |
| **6** | **2.1.3 Nama-Nama Kepala Desa** | Nama Kades/Lurah definitif/Pj aktif tahun 2025 per desa. | [Buka Sheet 2.1.3](https://docs.google.com/spreadsheets/d/1x-XjDE3rupSaBIwFGqyHpyYjz6S9ur0PVFORXY9AdW4) |
| **7** | **2.1.4 Nama-Nama Kepala Dusun** | Nama Kepala Dusun / Ketua RW per desa (jika ada pembagiannya). | [Buka Sheet 2.1.4](https://docs.google.com/spreadsheets/d/10eEof1SE5ucO6hUAvP7EJ8X7GQLyuGwiRpM4Ltc_Vkk) |
| **8** | **2.2.1 Jumlah PNS Menurut Pemda & JK** | Jumlah pegawai PNS di kantor camat menurut jenis kelamin (L/P). | [Buka Sheet 2.2.1](https://docs.google.com/spreadsheets/d/1Vqx2_TCs27HqnxYcoYHhLASZROf6gEJDvo6J6CjEQ8g) |
| **9** | **2.2.2 Jumlah PNS Menurut Pendidikan** | Jumlah pegawai PNS kantor camat menurut ijazah terakhir (SMA, D3, S1, S2). | [Buka Sheet 2.2.2](https://docs.google.com/spreadsheets/d/1gc5ZbcBNwU17rBqE6tcIlXxzR7RfFzi_F9OVI6HtJIQ) |

> 💡 **Cara Mengisi**:
> Buka tautan spreadsheet di atas $\rightarrow$ Pilih **Tab Nama Kecamatan** yang ditugaskan (misal tab `Jongkat`, `Toho`, dll.) $\rightarrow$ Masukkan angka/teks hasil konfirmasi dari Kantor Camat.

---

## 🚨 Register Bahaya Fallback Data (Hazard Register)

Pencatatan area rawan kesalahan jika data belum diverifikasi lapangan:

| Titik Data Rawan | Mengapa Berbahaya Jika Fallback Otomatis? | Prosedur Penanganan Aman di Sistem |
| :--- | :--- | :--- |
| **Nama Camat & Kades** *(Tabel 2.1.2 & 2.1.3)* | ⚠️ **SANGAT BERBAHAYA**. Pergantian pejabat definitif / Pj baru sering terjadi. Jika otomatis menyalin nama tahun lalu, nama pejabat di publikasi resmi bisa salah dan memicu teguran dari Pemda. | Jika belum dikonfirmasi lapangan, biarkan nama berstatus draft dengan penanda verifikasi atau tanda `...`. |
| **Jumlah PNS Camat** *(Tabel 2.2.1 & 2.2.2)* | ⚠️ **BERBAHAYA**. Mutasi, pensiun, dan pengangkatan PPPK baru mengubah jumlah pegawai secara dinamis. Mengisi angka 2024 tanpa konfirmasi dapat dianggap disinformasi. | Wajib menyertakan catatan kaki resmi jika terpaksa menggunakan angka tahun sebelumnya. |
| **Jumlah RT & RW** *(Tabel 2.1.1)* | ⚠️ **BERBAHAYA**. Rawan terjadi pemekaran atau penggabungan RT. Data ini menjadi dasar alokasi beban sensus/survei BPS. | Wajib dicek silang dengan dokumen monografi kecamatan terbaru. |
| **Data Fasilitas Podes** *(Bab 4, 6, 7)* | ⚠️ **RAWAN SALAH SUMBER**. Fasilitas sekolah/kesehatan bersumber dari data PODES resmi BPS, bukan kira-kira dari camat. | Injeksi langsung dari database master PODES BPS Mempawah (`1xNPk7PZeK...`). |

---

## 🔄 Mekanisme 1-Script Update

Sistem otomasi kita telah dirancang **deterministik dan toleran terhadap kekosongan data**:
1. **Saat Data Masih Kosong (Tim Belum ke Lapangan)**:
   - Sistem secara otomatis merender tabel berstruktur rapi dengan format baku BPS (seluruh baris desa/kelurahan tetap utuh), tetapi sel data yang belum ada diisi notasi standar `...` (*data belum tersedia*).
   - Draf publikasi tetap dapat dicompile menjadi buku utuh berstandar BPS 2023 tanpa error/crash, sehingga tata letak visual (*page layout*) dapat langsung direview oleh pimpinan.
2. **Saat Tim Magang Selesai Mengisi Google Sheet**:
   - Cukup jalankan **1 perintah** di terminal:
     ```bash
     python scripts/kb.py kcda sync
     ```
     *(atau memicu flow Windmill di `https://wind.dvlpid.my.id`)*.
   - Sistem secara otomatis mengunduh pembaruan dari Google Sheets, mengaudit kesiapan, mengompilasi ulang buku KCDA 9 kecamatan, dan mengunggah draft PDF baru ke Google Drive (`3. Draft Publikasi`).
