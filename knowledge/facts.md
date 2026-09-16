# 💡 Fakta & Parameter Utama: BPS Mempawah

*Dokumentasikan fakta penting, parameter kegiatan, dan catatan rujukan di sini.*

- **Sistem**: Aina asisten mandiri berbasis Rust & Google Antigravity CLI.
- **Zona Waktu**: Asia/Jakarta (WIB, UTC+7).

## Indikator Strategis Makro Kabupaten Mempawah (s.bps.go.id/indikator_strategis6104)
- **Persentase Kemiskinan**:
  - 2023: 5,21%
  - 2024: 4,83% (turun 0,38%)
  - 2025: 4,49% (turun 0,34%)
- **IPM**: 2023: 68,91 | 2024: 69,63 | 2025: 70,59
- **Tingkat Pengangguran Terbuka (TPT)**: 2023: 7,33% | 2024: 6,78% | 2025: 4,74%
- **Pertumbuhan Ekonomi (y-o-y)**: 2023: 5,09% | 2024: 6,62% | 2025: 8,24%
- **Gini Ratio**: 2023: 0,291 | 2024: 0,254 | 2025: 0,257

## Sensus Ekonomi 2026 (SE2026) - Audit Matching Prelist DTSEN ke Regsosek CETAR
- **Konteks**: Prelist DTSEN desil rendah (< 7) yang berstatus tidak ditemukan di manapun di Kalbar.
- **Data Makro**: 7.509 KK di tingkat provinsi tidak ditemukan; setelah filter koordinasi dengan IPDS BPS Provinsi diperoleh 6.662 KK.
- **Validasi Spasial CETAR**: Dari 6.662 KK tersebut, terdapat **1.839 KK** yang memiliki titik koordinat di database CETAR.
- **Rincian Catatan Petugas di CAPI/Fasih (6.662 KK)**:
  - 1.810 KK (27,2%): Catatan kosong di CAPI (hanya klik opsi STOP).
  - 162 KK (2,4%): Catatan tautologi (hanya menulis teks "tidak ada/nihil").
  - 2.269 KK (34,1%): Keterangan pindah domisili / merantau.
  - 626 KK (9,4%): Keterangan bukan warga / tidak dikenal RT.
  - 133 KK (2,0%): Keterangan meninggal dunia.
  - 1.662 KK (24,9%): Catatan deskriptif lainnya.
- **Poin Kritis**: 29,6% catatan (kosong + tautologi) berisiko tinggi karena di aplikasi Fasih tidak menceritakan usaha/upaya pencarian yang dilakukan petugas.
- **Dokumen Teknis**: [`audit-dtsen-hilang-regsosek-cetar.md`](../kegiatan/sensus-ekonomi-2026/2026/docs/audit-dtsen-hilang-regsosek-cetar.md)
- **Rujukan Google Sheet**: `https://docs.google.com/spreadsheets/d/1iK-N0xVKViNbzTIc64qBOjESJFdcR9IEtv1RjMWN9b0/edit?pli=1&gid=2072569417#gid=2072569417` (Sheet: *Audit DTSEN Hilang*).

## Monitoring Sensus Ekonomi 2026 (SE2026)
- **Siklus Pembaruan Status Tandai Selesai SLS**: Pembaruan/sinkronisasi status tandai selesai SLS pada spreadsheet monitoring (`1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0`) ditarik berkala 1 jam sekali, tepat setiap jam di menit :00 (misal: 14:00, 15:00, dst).

## POK BPS Kabupaten Mempawah TA 2026 (SAKTI Kemenkeu)
- **Sumber Data**: Sistem SAKTI Kementerian Keuangan (Rincian Kertas Kerja Satker).
- **Waktu Penarikan**: Rabu, 16 September 2026 pukul 09:00 WIB (dibagikan oleh Bang Ihza Karunia).
- **Berkas Data Lokal**: `data/POK_BPS_Mempawah_2026_SAKTI.xlsx`
- **Total Pagu Satker**: **Rp 9.224.066.000,-**
- **Ringkasan Program**:
  1. **Program Penyediaan dan Pelayanan Informasi Statistik (054.01.GG)**: **Rp 5.113.471.000,-**
     - Alokasi Terbesar: Kegiatan 2902 (Statistik Distribusi / Sensus Ekonomi 2026) sebesar **Rp 3.610.255.000,-**.
     - Sub-alokasi SE2026:
       - 2902.BMA.006 (Publikasi/Laporan Sensus Ekonomi baseline): Rp 348.639.000,-
       - 2902.BMA.006 (Penambahan alokasi dari SABA): Rp 2.564.322.000,-
       - 2902.FAN.ZZ1 (Pemenuhan Prioritas Direktif Presiden - SE2026): Rp 691.694.000,-
     - Kegiatan Statistik Lainnya: Statistik Harga (2903: Rp 495,2 jt), Kesra/Susenas (2906: Rp 385,2 jt), Pertanian (2910: Rp 211 jt), Kependudukan/Ketenagakerjaan (2905: Rp 141,1 jt), Industri (2904: Rp 87,3 jt), Peternakan/Perikanan (2909: Rp 69,1 jt), dll.
  2. **Program Dukungan Manajemen (054.01.WA / 2886)**: **Rp 4.110.595.000,-**
     - Gaji, tunjangan operasional, dan pemeliharaan perkantoran BPS Kabupaten Mempawah.

## Skala Gaji Pokok PNS (PP Nomor 5 Tahun 2024)
- **Dasar Hukum**: Peraturan Pemerintah Republik Indonesia Nomor 5 Tahun 2024 tentang Perubahan Kesembilan Belas atas Peraturan Pemerintah Nomor 7 Tahun 1977 tentang Peraturan Gaji Pegawai Negeri Sipil (LNRI 2024 No. 15, TLNRI No. 6917).
- **TMT Berlaku**: **1 Januari 2024** (ditetapkan dan diundangkan 26 Januari 2024).
- **Penyesuaian**: Kenaikan gaji pokok rata-rata sebesar **8%** dari ketentuan sebelumnya (PP No. 15 Tahun 2019).
- **Sifat Angka Gaji Pokok**: **Nominal Baku Tunggal (Fixed Basic Salary Scale)**, **BUKAN** upah minimum (*floor wage*). Instansi/bendahara tidak dapat mengubah atau menegosiasikan besaran ini. Besaran mengikat nasional untuk seluruh ASN PNS sesuai Golongan Ruang dan Masa Kerja Golongan (MKG).
- **MKG (Masa Kerja Golongan)**: Akumulasi masa dinas sah dalam golongan bersangkutan (0–27 tahun untuk Gol I; 0–33 tahun untuk Gol II; 0–32 tahun untuk Gol III & IV). Setiap 2 tahun memenuhi syarat berhak atas Kenaikan Gaji Berkala (KGB).
- **Komponen Penghasilan Tambahan**: Di luar gaji pokok, PNS menerima hak tunjangan melekat (suami/istri 10%, anak 2%, uang makan, tunjangan beras) serta Tunjangan Kinerja (Tukin BPS berdasarkan Perpres) dan tunjangan fungsional/jabatan.
- **Rujukan Google Spreadsheet**: [Tabel Gaji Pokok PNS - PP Nomor 5 Tahun 2024 (BPS Mempawah)](https://docs.google.com/spreadsheets/d/1JXiDTejaxXRqasALOMsXYWfPydCatZtmf1kIzqLeFpA/edit?usp=sharing)
- **Lokasi Folder Google Drive**: Folder `Kepegawaian` (ID: `1RrF76RT2GOqQjKREL14x-TXizqQgXCSP`, [Akses Google Drive](https://drive.google.com/drive/folders/1RrF76RT2GOqQjKREL14x-TXizqQgXCSP)).
