---
nama: "Sosialisasi Sistem Backend Website BPS"
kategori: "ti"
rutinitas: "non-rutin"
frekuensi: "ad-hoc"
peran: "anggota"
status: "aktif"
deadlines:
  - tanggal: "2026-10-20"
    kegiatan: "Batas Akhir Penetapan & Pendaftaran Akun Admin BPS Kab/Kota oleh BPS Provinsi"
    status: "selesai"
  - tanggal: "2026-10-21"
    kegiatan: "Pelaksanaan Sosialisasi Sistem Backend Website BPS (08.00 - 12.00 WIB via LMS BPS)"
    status: "selesai"
  - tanggal: "2026-10-23"
    kegiatan: "Cut-Off Backend Lama & Batas Akhir Upload Konten Lama (Pukul 16.00/18.00 WIB) sebelum Migrasi Server Baru (Pukul 19.00 WIB)"
    status: "aktif"
  - tanggal: "2026-10-26"
    kegiatan: "Go-Live Penuh Website Versi 5.0 (Backend Lama Ditutup Total & Semua Satker Menggunakan web-be.apps.bps.go.id)"
    status: "belum"
---

# Sosialisasi Sistem Backend Website BPS TA 2026

> [!IMPORTANT]
> Kegiatan Sosialisasi Implementasi Sistem Backend Website Baru BPS (`https://web-be.apps.bps.go.id`) berdasarkan Surat Undangan BPS RI Nomor: `B-1644/03200/SS.610/2026`.
> **Perwakilan Tim Teknis BPS Kabupaten Mempawah (Satker 6104)**: Ihza Karunia (Bang Ihza) dan Akma Batrisyia (Mba Akma).

---

## 1. Deskripsi & Ruang Lingkup Kegiatan

Sosialisasi ini diselenggarakan oleh BPS RI untuk memperkenalkan dan mengimplementasikan sistem manajemen konten / *backend* baru bagi portal website resmi BPS (Provinsi dan Kabupaten/Kota) yang mulai aktif diterapkan serentak per 21 Oktober 2026.

Kegiatan ini mencakup:
1. Pengenalan fitur, arsitektur, dan alur kerja sistem *backend* website baru di `https://web-be.apps.bps.go.id`.
2. Pelatihan teknis pengelolaan konten, publikasi berita resmi, dan rilis data statistik bagi pengelola website daerah.
3. Tata kelola manajemen hak akses akun admin dan kontributor website satker daerah.

---

## 2. Rujukan Surat Resmi & Transkrip Sesi

- **Instansi Penerbit**: Badan Pusat Statistik (BPS RI)
- **Nomor Surat**: `B-1644/03200/SS.610/2026`
- **Perihal**: Undangan Sosialisasi Sistem Backend Website
- **Dokumen Surat**: `B-1644 SS610 2026 Und Sosialisasi Sistem Backend Website.pdf` (Tersimpan di `media/ACDC3058E44A3A32EC055BD1352EBF79.pdf`)
- **Transkrip Sesi Zoom**: Dokumen Google Docs `11lERNWuQ5GHSxw5RhGXjWBKMulKJXJNjp8KHzV2z1BM` ([Salinan Teks Lokal](file:///app/workspaces/default/knowledge/transkrip_zoom_backend.txt))

---

## 3. Jadwal Kunci & Agenda Pelaksanaan

- **Selasa, 20 Oktober 2026**:
  - Batas waktu BPS Provinsi menetapkan dan mendaftarkan akun admin untuk BPS Kabupaten/Kota pada portal `https://web-be.apps.bps.go.id`.
- **Rabu, 21 Oktober 2026 (08.00 – 12.00 WIB)**:
  - Pelaksanaan sosialisasi daring serentak melalui platform Pembelajaran BPS (LMS).
  - **Tautan LMS**: `https://lms.bps.go.id/course/view.php?id=5051`
  - **Enrollment Key**: `website`
  - **Peserta BPS Kab. Mempawah**: Bang Ihza dan Mba Akma.
- **Jumat, 23 Oktober 2026**:
  - **Pukul 16.00 / 18.00 WIB**: Batas akhir daerah meng-upload atau update konten di sistem/backend lama agar tidak ada konten yang tertinggal saat migrasi.
  - **Pukul 19.00 WIB**: Akses backend lama (archive & webdesk) **RESMI DITUTUP** untuk proses migrasi database dan sistem ke server mesin baru oleh Tim Inka (Infrastruktur & Keamanan BPS RI / SIS).
- **Senin, 26 Oktober 2026**:
  - **Go-Live Resmi Website Versi 5.0**: Backend lama sudah ditutup permanen dan seluruh satker (Provinsi & Kab/Kota) resmi menggunakan backend baru secara penuh.
- **Januari 2027**:
  - Stabilisasi pencatatan statistik pengunjung web di Webdash menggunakan Google Analytics baru.

---

## 4. Rangkuman Inti & Poin Teknis Sosialisasi Backend Website (21 Oktober 2026)

### A. Arsitektur Frontend vs Backend
1. **Frontend Portal Web**: Tampilan publik website resmi BPS telah diseragamkan (*template Sabang sampai Merauke sama persis*) untuk standarisasi identitas digital BPS.
2. **Backend Portal Web (`https://web-be.apps.bps.go.id`)**: Merupakan ruang kendali mandiri masing-masing satker (Pusat, Provinsi, Kab/Kota) untuk mengatur seluruh konten lokal: jadwal rilis, naskah berita resmi/BRS, publikasi buku, infografis, tabel statis, dan indikator strategis.

### B. Otentikasi & Manajemen Pengguna
- **Otentikasi Single Sign-On (SSO Baru BPS)**: Seluruh admin dan pengelola konten wajib login menggunakan akun SSO BPS teraktivasi dengan OTP pengaman. Tidak ada lagi akun terpisah/password lokal per aplikasi.
- **Peralihan Website Satker via Kode MFD**:
  - Pengguna dengan hak multi-satker dapat beralih mengelola website satker melalui menu *Pilih Website* berbasis kode MFD (misal: BPS Pusat `0000`, Provinsi Kalbar `6100`, BPS Mempawah `6104`).
- **Role & Kewenangan**:
  - Saat pertama kali login, menu utama hanya beranda (*home*). Hak akses (*role*) kontributor/admin konten diberikan oleh Admin Satker Provinsi/Pusat.

### C. Pengelolaan Data & Indikator Strategis
- **Master Indikator & Entry Data**:
  - Form input indikator dirancang menyerupai *spreadsheet cell grid* (dapat langsung *copy-paste* dari sel Microsoft Excel ke tabel web backend).
  - Dilengkapi tombol unduh template/tabel Excel langsung dari sistem.
  - Fitur simpan dan hapus data per tahun rujukan (misal tahun 2026, 2025, dst.).
- **Tabel Statis**:
  - Mendukung klasifikasi subjek statistik (CSA / Classification of Statistical Activities), mapping metadata indikator/SIMDASI, unggah berkas Excel, status tampil (*publish/draft*), dan pratinjau tabel sebelum tayang.

### D. Fitur Publikasi, Berita & Headline (Catatan Diskusi / Q&A)
- **Format Judul vs Headline**:
  - Tersedia kolom *Headline* khusus yang ramah mesin pencari (SEO-friendly) dan menarik bagi audiens media sosial/masyarakat, tanpa menghilangkan struktur judul baku BPS (seperti *"Perkembangan Ekspor dan Impor Kabupaten Mempawah Bulan X Tahun Y"*).
  - *Catatan Integrasi Otomasi*: Untuk script bot otomatis (seperti WhatsApp Gateway / Bot BRS), penyesuaian parser judul perlu mempertimbangkan ketersediaan kolom judul baku dan teks headline.
