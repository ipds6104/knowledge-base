# DDA Data Audit & Anomaly Detection Rules

Dokumen ini memuat standar audit data dan aturan deteksi kejanggalan untuk pendataan Desa Cantik (CAPI AppSheet):

## 1. Variabel Bumbung Rumah (Hunian)
- **Rule 1 (Bumbung Rumah = 0)**: Jika `Jumlah_Bumbung_Rumah == 0` tetapi `Jumlah_KK > 0` atau `Total_Penduduk > 0`, tandai sebagai **CRITICAL ANOMALY**. Minta konfirmasi isian atau gunakan estimasi `Bumbung ≈ KK`.
- **Rule 2 (Bumbung Tertukar dengan Penduduk)**: Jika `Jumlah_Bumbung_Rumah == Total_Penduduk` dan `Jumlah_Bumbung_Rumah > Jumlah_KK * 2`, tandai sebagai **INPUT ERROR** (jumlah penduduk salah ter-input ke kolom bumbung rumah).
- **Rule 3 (Kepadatan Ekstrim)**: Jika `Total_Penduduk / Jumlah_Bumbung_Rumah > 8.0` atau `< 1.0`, periksa kembali keabsahan data RT tersebut.

## 2. Variabel KTP-el & Demografi
- **Rule 4 (KTP-el = 0)**: Jika `Jumlah_Memiliki_KTP == 0` padahal `Total_Penduduk > 50`, periksa kemungkinan isian KTP terlewati oleh petugas CAPI.
- **Rule 5 (Sex Ratio Outlier)**: Jika `Sex Ratio > 150` atau `< 70`, periksa komposisi gender RT.

## 3. Variabel Bantuan Sosial (PKH, BPNT, BLT)
- **Rule 6 (Bansos Overcount)**: Total penerima bansos (`PKH + BPNT + BST + BLT`) tidak boleh melebihi `Jumlah_KK * 2` (kecuali jika ada keluarga penerima bantuan ganda).
