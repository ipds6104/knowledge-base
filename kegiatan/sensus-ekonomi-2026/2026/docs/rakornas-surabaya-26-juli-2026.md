# Arahan Operasional Rakornas SE2026 Surabaya (26 Juli 2026)

**Narasumber**: Sonny Harry Budiutomo Harmadi (Wakil Kepala BPS RI)  
**Tema Utama**: *"Dari Lapangan Menjadi Cerita Bersama"* — Mengawal Pendataan Lapangan SE2026 yang Berkualitas, Bermakna, dan Berdampak.  
**Tanggal Eksekusi Dokumen**: 26 Juli 2026  
**Lokasi Penerapan**: BPS Kabupaten Mempawah (6104)

---

## 🎯 1. Ringkasan Eksekutif & Pergeseran Paradigma Operasional

 Rakornas Evaluasi dan Monitoring Pelaksanaan Lapangan SE2026 di Surabaya menyepakati pergeseran strategi lapangan secara nasional:

1. **Shift ke Penyisiran Door-to-Door (Menyisir Bangunan)**:
   - Petugas **dilarang keras** hanya bergantung pada Prelist.
   - Banyak usaha aktif di lapangan yang belum masuk prelist; demikian pula terdapat usaha prelist yang sudah tutup/beralih fungsi. Ada maupun tidak ada dalam Prelist, **seluruh usaha aktif di wilayah SLS wajib terdata**.
2. **Target Internal Penyelesaian Lapangan (17 Agustus 2026)**:
   - Sensus resmi berakhir pada 31 Agustus 2026. Namun BPS menetapkan **target internal selesai pada 17 Agustus 2026** (2 minggu lebih awal).
   - *Rasional*: Menyediakan jendela waktu 14 hari untuk penanganan data anomali, re-validasi, dan *missing values* selagi petugas PPL/PML **masih dalam masa aktif kontrak**.
3. **Komitmen Kepemimpinan Satker (BPS Kab/Kota)**:
   - Kepala BPS Kabupaten/Kota **WAJIB turun langsung ke lapangan** untuk mendampingi petugas pada kasus-kasus sulit, terutama penolakan korporasi/usaha besar (UB). Kehadiran Kepala Satker meningkatkan kepercayaan responden dan moral petugas.

---

## 📋 2. Matriks Tindakan Taktis per Peran (Actionable Checklist)

| Peran | Tindakan Wajib pasca-Rakornas | Frekuensi / Waktu |
|---|---|---|
| **Kepala BPS Kabupaten** | • Turun pendampingan lapangan langsung pada usaha besar (UB) yang menolak.<br>• Memastikan pembayaran honorarium petugas tepat waktu.<br>• Monitoring harian progres macro kabupaten vs Kalbar. | Harian / Sesuai Kasus |
| **PJ-Kuda** | • Memonitor laju submisi PPL & antrean verifikasi PML 2x sehari (`./scripts/kb.py se-monitor -r`).<br>• Melakukan evaluasi taktis PML bottleneck (>20 pending, approval < 20%).<br>• Mengoordinasikan penanganan wilayah perbatasan SLS / kecamatan. | Pagi (06.30) & Sore (17.30) |
| **PML (Pengawas)** | • Melakukan verifikasi berkas CAPI minimal 2x sehari.<br>• Melakukan *double-check* 100% pada status UB/UM yang dilaporkan tutup/tidak ditemukan.<br>• Memastikan stiker sensus tertempel di lokasi yang mudah terlihat oleh responden. | Harian (Setiap Hari) |
| **PPL (Pencacah)** | • Menyisir seluruh bangunan SLS door-to-door (bukan hanya mendatangi prelist).<br>• Jangan pernah *reset* Handphone saat terjadi kendala FASIH.<br>• Bila responden menolak/sibuk: tawarkan janji ketemu, jelaskan kerahasiaan data, atau alihkan ke moda CAWI dengan OTP. | Setiap Jam Kerja Lapangan |

---

## 🔍 3. SOP Re-Validasi & Penanganan 7 Jenis Anomali Data SE2026

Berdasarkan temuan *random check* BPS RI, berikut adalah 7 anomali data kritis yang wajib dibersihkan di Kabupaten Mempawah:

### 1. Konfirmasi 100% Usaha Besar (UB) & Usaha Menengah (UM) Tutup / Tidak Ditemukan
- **Aturan Bisnis**: UB & UM memiliki *churn rate* sangat rendah. Status "Tidak Ditemukan" atau "Tutup" pada UB/UM berpotensi tinggi merupakan kesalahan verifikasi.
- **Prosedur**: Setiap temuan UB/UM tidak ditemukan **wajib dikonfirmasi ulang** oleh PML ke penanggung jawab kawasan/pemilik usaha sebelum disetujui.

### 2. Koreksi Misklasifikasi Unit Penunjang (>100 per Kab/Kota)
- **Aturan Bisnis**: Banyak usaha salah digolongkan sebagai Unit Penunjang.
- **Daftar Usaha Dilarang Ditulis Unit Penunjang**: Sekolah (SD/SMP/SMA/TK/PAUD), SPBU/SPPG, Bank (BRI, Mandiri, Pegadaian), Drivers Ojek Online/Affiliate/Olshop, Peternakan/Pertanian, Jasa Menjahit/Sopir/Bersih Jalan.

### 3. Usaha Berdiri Sebelum 2025 dengan Pengeluaran > Pendapatan
- **Aturan Bisnis**: Usaha yang sudah lama beroperasi tetapi melaporkan pengeluaran > pendapatan merupakan indikasi anomali isian keuangan.
- **Prosedur**: Lakukan *probing* ulang mengenai rincian biaya operasional vs omset bulanan/tahunan.

### 4. Inkonsistensi Kategori KBLI vs Nama Usaha
- **Grup Akomodasi/Makan Minum**: Nama memuat *"Restoran/Resto/Warung Makan/Hotel/Villa/Hostel"* tetapi KBLI bukan Kategori I.
- **Grup Keuangan**: Nama memuat *"Bank/BPR/Koperasi/Pegadaian/Gadai/Asuransi/Simpan Pinjam"* tetapi KBLI bukan Kategori L.

### 5. Usaha Menetap Tanpa Penguasaan Tanah (Luas Tanah = 0 m²)
- **Aturan Bisnis**: Usaha selain keliling dan selain online/daring yang mengaku Luas Tanah Dikuasai = 0 m² merupakan anomali.

### 6. MBG / Koperasi dengan Jumlah Pekerja Dibayar < 3 Orang
- **Aturan Bisnis**: Usaha berbadan hukum Koperasi atau unit MBG (SPPG) wajib diverifikasi ulang jika melaporkan jumlah pekerja dibayar < 3 orang.

### 7. Apartemen di Wilayah Perdesaan
- **Aturan Bisnis**: Pencatatan keluarga yang tinggal di apartemen di wilayah desa wajib dikonfirmasi ulang kebenaran jenis bangunannya.

---

## 📊 4. Formula Indeks Keberhasilan Sensus (IKS)

BPS RI mengukur performa pelaksanaan SE2026 Kab/Kota menggunakan Indeks Keberhasilan Sensus:

$$IKS = 0.4 \times SP + 0.4 \times SK + 0.2 \times SM$$

1. **Skor Pendataan ($SP$)**:
   $$SP = 0.25 \times \%UB + 0.25 \times \%UM + 0.25 \times \%UMK + 0.25 \times KF$$
   *(di mana $KF = \text{persentase keluarga ditemukan}$)*
2. **Skor Kualitas ($SK$)**:
   $$SK = \frac{KBLI + MV}{2}$$
   *(di mana $KBLI = 100 - \% \text{anomali KBLI}$, $MV = 100 - \% \text{missing values}$)*
3. **Skor Pemerataan ($SM$)**:
   $$SM = 100 \times \left(1 - \frac{SD - SD_{min}}{SD_{max} - SD_{min}}\right) \times \frac{SP}{100}$$
   *(di mana $SD = \text{Standar Deviasi capaian antar kecamatan}$)*

---

## ⏰ 5. Penjadwalan Query SQL Lab Superset & Matriks Bebas Bentrokan

Untuk menjaga data pendataan & anomali selalu terbarui tanpa mengganggu jadwal kerja utama lainnya:

### Jadwal Running Data SQL Lab Superset FASIH SE2026:
- **06.30 - 07.30 WIB (Pagi)**: `./scripts/kb.py sqllab pull && ./scripts/kb.py se-monitor -r`  
  *Penarikan submisi malam PPL & penyiapan laporan 6-seksi sebelum turun lapangan.*
- **12.30 - 13.00 WIB (Siang)**: `./scripts/kb.py sqllab report`  
  *Monitoring pertengahan hari & verifikasi antrean PML.*
- **17.30 - 18.30 WIB (Sore)**: `./scripts/kb.py sqllab pull-completed && ./scripts/kb.py se-monitor -r`  
  *Penarikan SLS 100% approved & rekap harian sore.*
- **21.00 - 22.00 WIB (Malam)**: `./scripts/kb.py sqllab pull-microdata`  
  *Running query microdata Superset untuk 7 deteksi anomali Rakornas saat server sepi.*

### Catatan Kritis Replikasi OLTP FASIH ke SQL Lab Superset:
> [!WARNING]
> **Limitasi Data Status `OPEN`**: Replikasi dari OLTP FASIH ke StarRocks/Trino Superset **hanya mencatat dokumen yang minimal pernah berstatus `DRAFT`** (tersimpan ke server). Assignment berstatus `OPEN` (belum pernah disentuh PPL) **TIDAK ADA** pada database SQL Lab.
> - **Dampak**: `COUNT(assignment_id)` dari SQL Lab mengekspresikan *worked assignments*, bukan total target alokasi sejati.
> - **Penanganan**: Total target alokasi penyebut ($Target$) wajib dibaca dari master file `Alokasi Petugas.csv`, sedangkan SQL Lab digunakan khusus untuk pencacahan pembilang (*submitted, approved, completed admin*) dan pemindaian 7 anomali microdata.

### Penanganan Kantong Bentrokan Jadwal Utama:
1. **30 Juli 2026 (Seminar Latsar CPNS Full Day 08.00-17.00 WIB)**:
   - Slot monitoring SE2026 dialihkan ke **06.30 WIB** dan **19.30 WIB**.
2. **31 Juli 2026 (Batas CAWI SE2026, Kepegawaian, SAKIP TW II, EPSS)**:
   - Penutupan CAWI SE2026 dieksekusi via SQL Lab pada 31 Juli malam. SAKIP TW II dikunci 30 Juli malam.
3. **1 - 10 Agustus 2026 (Sakernas Updating RT vs SE2026 Sprint Final)**:
   - Updating Sakernas diselesaikan pada 1-5 Agustus agar 6-17 Agustus fokus penuh pada submit final SE2026.
