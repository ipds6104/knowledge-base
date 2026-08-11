"""Metadata DTO Builder.

Constructs strongly-typed DesaMetadataDTO for any village in a clean, decoupled, and fully dynamic manner by inspecting live Google Sheets data.
"""

from typing import List, Dict, Tuple
from .schemas import (
    DesaMetadataDTO,
    KegiatanItemDTO,
    VariabelItemDTO,
    VariabelMetadataDTO,
    IndikatorItemDTO,
)
from ..dda_generator import get_desa_config, fetch_desa_data


# Master dictionary mapping raw column names to One Data Indonesia (SDI) metadata attributes
COLUMN_ATTRS: Dict[str, Tuple[str, str, str, str, str]] = {
    # Geospasial & Identitas
    'Nomor Bangunan': ('Identitas Bangunan', 'Nomor urut fisik bangunan tempat tinggal biasa.', 'Unit', 'Integer', 'Nilai > 0'),
    'Nomor SLS': ('Wilayah Administrasi', 'Kode SLS/RT tempat pendataan.', '-', 'String', 'Kode SLS'),
    'Nama RT': ('Wilayah Administrasi', 'Nama rukun tetangga tempat pengumpulan data CAPI dilakukan.', '-', 'String', 'Nama RT Tekstual'),
    'Nama_RT': ('Wilayah Administrasi', 'Nama rukun tetangga tempat pengumpulan data CAPI dilakukan.', '-', 'String', 'Nama RT Tekstual'),
    'RT': ('Wilayah Administrasi', 'Nama rukun tetangga tempat pengumpulan data dilakukan.', '-', 'String', 'Nama RT Tekstual'),
    'ID_Rumah': ('Identitas Rumah', 'Kode pengenal unik unit rumah.', '-', 'String', 'Kode Alfanumerik'),
    'Koordinat': ('Geospasial', 'Titik koordinat presisi latitude dan longitude lokasi fisik bangunan.', '-', 'String', 'Latitude, Longitude (LatLong)'),
    'Lokasi_Geotagging': ('Geospasial', 'Titik koordinat presisi latitude dan longitude lokasi fisik rumah.', '-', 'String', 'Latitude, Longitude (LatLong)'),
    'Lokasi_GPS': ('Geospasial', 'Titik koordinat latitude dan longitude lokasi fasilitas.', '-', 'String', 'Koordinat Geografis'),
    'Nama Kepala Keluarga': ('Identitas Responden', 'Nama lengkap Kepala Keluarga utama yang mendiami bangunan.', '-', 'String', 'Nama Lengkap Tekstual'),
    'Nama_Kepala_Keluarga': ('Identitas Responden', 'Nama lengkap Kepala Keluarga utama yang mendiami rumah.', '-', 'String', 'Nama Lengkap Tekstual'),
    'Nama Kepala Keluarga Tambahan': ('Identitas Responden', 'Nama lengkap Kepala Keluarga tambahan yang tinggal di bangunan yang sama.', '-', 'String', 'Nama Lengkap Tekstual'),
    'Nama Kepala Keluarga Tambahan 2': ('Identitas Responden', 'Nama lengkap Kepala Keluarga tambahan kedua di bangunan yang sama.', '-', 'String', 'Nama Lengkap Tekstual'),
    'Jumlah Kartu Keluarga': ('Rumah Tangga / KK', 'Banyaknya Kartu Keluarga (KK) yang mendiami bangunan.', 'Keluarga', 'Integer', 'Nilai >= 1'),
    'Jumlah_Kartu_Keluarga': ('Rumah Tangga / KK', 'Banyaknya Kartu Keluarga (KK) yang mendiami rumah.', 'Keluarga', 'Integer', 'Nilai >= 1'),
    'Nomor_WhatsApp_ART': ('Komunikasi', 'Nomor kontak telepon/WhatsApp anggota keluarga.', '-', 'String', 'Nomor Telepon'),
    'Nomor Whatsapp': ('Komunikasi', 'Nomor kontak telepon/WhatsApp anggota keluarga.', '-', 'String', 'Nomor Telepon'),

    # Demografi & Gender
    'Jumlah Orang Laki-Laki di Rumah': ('Demografi / Gender', 'Banyaknya anggota keluarga berjenis kelamin laki-laki di rumah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Orang Perempuan di Rumah': ('Demografi / Gender', 'Banyaknya anggota keluarga berjenis kelamin perempuan di rumah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Orang_Laki_Dirumah': ('Demografi / Gender', 'Jumlah anggota keluarga berjenis kelamin laki-laki di rumah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Orang_Perempuan_Dirumah': ('Demografi / Gender', 'Jumlah anggota keluarga berjenis kelamin perempuan di rumah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jenis_Kelamin_KK_Laki': ('Identitas KK', 'Penanda Kepala Keluarga berjenis kelamin laki-laki.', 'Keluarga', 'Integer', '0 atau 1'),
    'Jenis_Kelamin_KK_Perempuan': ('Identitas KK', 'Penanda Kepala Keluarga berjenis kelamin perempuan.', 'Keluarga', 'Integer', '0 atau 1'),
    'Jumlah Anggota Keluarga di Rumah': ('Ukuran Rumah Tangga', 'Total jumlah anggota keluarga yang mendiami rumah.', 'Orang', 'Integer', 'Nilai >= 1'),

    # Agama (Pasir Wan Salim)
    'Agama_yang_Ada_di_Rumah': ('Demografi / Agama', 'Rincian keberadaan agama anggota keluarga di rumah.', '-', 'String', 'Rincian Agama Tekstual'),
    'Jumlah orang beragama islam di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Islam.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama kristen di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Kristen.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama khatolik di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Katholik.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama konghucu di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Konghucu.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama budha di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Budha.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama hindu di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama Hindu.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang beragama lainnya di rumah': ('Demografi / Agama', 'Banyaknya anggota keluarga beragama lainnya.', 'Orang', 'Integer', 'Nilai >= 0'),

    # Kelompok Umur (Pasir Wan Salim)
    'Jumlah Penduduk Berusia 0-4': ('Struktur Umur', 'Banyaknya balita berusia 0 s.d. 4 tahun.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Penduduk Berusia 5-14': ('Struktur Umur', 'Banyaknya anak berusia 5 s.d. 14 tahun.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Penduduk Berusia 15-64': ('Struktur Umur', 'Banyaknya penduduk usia kerja/produktif 15 s.d. 64 tahun.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Penduduk Berusia 65-74': ('Struktur Umur', 'Banyaknya lansia berusia 65 s.d. 74 tahun.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Penduduk Berusia 75+': ('Struktur Umur', 'Banyaknya lansia berusia 75 tahun ke atas.', 'Orang', 'Integer', 'Nilai >= 0'),

    # Administrasi & Pendidikan
    'Jumlah orang yang tidak ada (meninggal) tapi masih tercatat di Kartu Keluarga': ('Administrasi Kependudukan', 'Jumlah anggota keluarga yang telah meninggal dunia namun masih di KK.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah orang yang tidak ada (meninggal) tapi masih tercatatat di Kartu Keluarga': ('Administrasi Kependudukan', 'Jumlah anggota keluarga yang telah meninggal dunia namun masih di KK.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Nama orang yang tidak ada (meninggal) tapi masih tercatat di Kartu Keluarga': ('Administrasi Kependudukan', 'Nama anggota keluarga yang telah meninggal dunia namun masih di KK.', '-', 'String', 'Nama Tekstual'),
    'Jumlah orang yang pindah tapi masih tercatatat di Kartu Keluarga': ('Administrasi Kependudukan', 'Jumlah anggota keluarga yang telah pindah domisili namun masih di KK.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Anggota Keluarga Putus Sekolah (7-18 tahun tetapi tidak sedang sekolah)': ('Pendidikan', 'Banyaknya anggota keluarga usia 7-18 tahun yang tidak sedang sekolah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Nama Anggota Keluarga Putus Sekolah': ('Pendidikan', 'Nama anak usia 7-18 tahun yang tidak sedang sekolah.', '-', 'String', 'Nama Tekstual'),
    'Jumlah orang dengan Disabilitas': ('Kebutuhan Khusus', 'Banyaknya anggota keluarga yang memiliki disabilitas.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Nama orang dengan Disabilitas': ('Kebutuhan Khusus', 'Nama anggota keluarga yang memiliki disabilitas.', '-', 'String', 'Nama Tekstual'),

    # Pekerjaan & Ekonomi
    'Pekerjaan anggota rumah tangga yang merupakah penghasilan utama dalam rumah': ('Mata Pencaharian', 'Jenis pekerjaan anggota rumah tangga penopang penghasilan utama.', '-', 'String', 'Petani, Buruh, Pedagang, PNS, Swasta, dll.'),
    'Jumlah Penduduk usia kerja (15-64 tahun) yang bekerja': ('Ketenagakerjaan', 'Jumlah penduduk usia kerja 15-64 tahun yang bekerja.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah Penduduk usia kerja (15-64 tahun) yang tidak bekerja': ('Ketenagakerjaan', 'Jumlah penduduk usia kerja 15-64 tahun yang tidak bekerja.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_UMKM_Dalam_Keluarga': ('Ekonomi', 'Banyaknya unit usaha mikro, kecil, atau menengah yang dikelola keluarga.', 'Unit Usaha', 'Integer', 'Nilai >= 0'),
    'Jumlah_ART_Memiliki_BPJS': ('Perlindungan Sosial', 'Jumlah anggota keluarga yang memiliki jaminan kesehatan BPJS.', 'Orang', 'Integer', 'Nilai >= 0'),

    # Fisik Rumah & Lingkungan
    'Apa bahan utama dinding rumah? ': ('Bahan Bangunan', 'Bahan fisik utama dinding terluas rumah.', '-', 'String', 'Tembok, Kayu, Seng, Bambu, Lainnya'),
    'Apa bahan utama lantai terluas rumah?': ('Bahan Bangunan', 'Bahan fisik utama lantai terluas rumah.', '-', 'String', 'Semen, Keramik, Ubin, Kayu, Tanah, Lainnya'),
    'Apa bahan atap terluas rumah?': ('Bahan Bangunan', 'Bahan fisik utama atap terluas rumah.', '-', 'String', 'Seng, Asbes, Genteng, Rumbia, Lainnya'),
    'Apakah rumah ini memiliki fasilitas buang air besar sendiri?': ('Sanitasi', 'Keberadaan dan kepemilikan fasilitas buang air besar (jamban) sendiri.', '-', 'String', 'Ya, Tidak'),
    'Kepemilikan_Fasilitas_Buang_Air_Besar': ('Sanitasi', 'Keberadaan dan kepemilikan fasilitas buang air besar (jamban) sendiri.', '-', 'String', 'Memiliki, Tidak Memiliki'),
    'Bagaimana cara keluarga membuang sampah rumah tangga?': ('Lingkungan', 'Cara utama keluarga membuang dan mengelola sampah rumah tangga.', '-', 'String', 'Dibakar, Angkut Petugas, Sungai, dll.'),

    # Bantuan Pemerintah
    'Apakah rumah ini mendapat bantuan dari pemerintah (PKH, BPNT, BLTS, BCP, BLTDD, PIP, BPJS PBI)': ('Bantuan Sosial', 'Status penerima bantuan sosial pemerintah.', '-', 'String', 'MENERIMA, TIDAK'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan PKH': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan PKH.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPNT': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BPNT.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTS': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BLTS.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BCP': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BCP.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTDD': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BLT-DD.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan PIP': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan PIP.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    ' Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPJS PBI': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BPJS PBI.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    'Jml_Penerima_Terdaftar_Sembako/BPNT': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan BPNT.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    'Jml_Penerima_Terdaftar_PKH': ('Bantuan Sosial', 'Banyaknya keluarga penerima bantuan PKH.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    'Nama Penerima Manfaat BPNT': ('Bantuan Sosial', 'Nama penerima manfaat BPNT.', '-', 'String', 'Nama Tekstual'),
    'Nama Penerima Manfaat PKH': ('Bantuan Sosial', 'Nama penerima manfaat PKH.', '-', 'String', 'Nama Tekstual'),

    # Fasilitas Umum (Sheet4)
    'ID_Fasilitas': ('Identitas Sarana', 'Kode pengenal unik setiap fasilitas.', '-', 'String', 'Kode Alfanumerik'),
    'Nama_Petugas': ('Petugas Pendata', 'Nama petugas pembina/agen statistik yang menginput data.', '-', 'String', 'Nama Petugas'),
    'Tanggal_Waktu': ('Waktu Pencacahan', 'Tanggal dan waktu observasi dilakukan.', '-', 'DateTime', 'YYYY-MM-DD HH:MM:SS'),
    'Foto_Fasilitas': ('Visual', 'Lampiran foto kondisi fasilitas.', '-', 'String', 'Path Berkas Gambar'),
    'Nama_Fasilitas': ('Nama Sarana', 'Nama resmi fasilitas.', '-', 'String', 'Nama Tekstual'),
    'Kategori_Fasilitas': ('Klasifikasi Sarana', 'Kategori utama fasilitas.', '-', 'String', 'Ibadah, Pendidikan, Kesehatan, Ekonomi, Pemerintahan, dll.'),
    'Sub_Kategori': ('Sub-Klasifikasi', 'Rincian jenis sarana prasarana.', '-', 'String', 'Masjid, SD, Posyandu, Toko, dll.'),
    'Kondisi_Bangunan/Jalan': ('Kualitas Fisik', 'Kelayakan fisik bangunan sarana.', '-', 'String', 'Baik, Rusak Ringan, Rusak Berat'),
    'Kondisi_Bangunan': ('Kualitas Fisik', 'Kelayakan fisik bangunan sarana.', '-', 'String', 'Baik, Rusak Ringan, Rusak Berat'),
    'Sumber_Listrik': ('Utilitas Listrik', 'Sumber pasokan daya listrik utama sarana.', '-', 'String', 'PLN 24 Jam, Non-PLN, dll.'),
    'Sumber_Air_Bersih': ('Utilitas Air', 'Sumber penyediaan air bersih utama sarana.', '-', 'String', 'PDAM/PAMSIMAS, Sumur Bor, dll.'),
    'Akses_Jalan': ('Infrastruktur', 'Jenis permukaan jalan terdekat.', '-', 'String', 'Aspal/Beton, Batu, Jalan Tanah'),
    'Sinyal_Seluler': ('Telekomunikasi', 'Kekuatan sinyal telekomunikasi seluler.', '-', 'String', 'Sangat Baik (4G/LTE), Cukup, dll.'),
    'Gambar_Rumah': ('Visual', 'Lampiran foto tampak depan rumah.', '-', 'String', 'Path Berkas Gambar'),
    'Foto_Rumah': ('Visual', 'Lampiran foto tampak depan rumah.', '-', 'String', 'Path Berkas Gambar'),
    'Tanggal_Pendataan': ('Waktu Pencacahan', 'Tanggal dan waktu penginputan data.', '-', 'DateTime', 'YYYY-MM-DD HH:MM:SS'),
    'Status_Pendataan': ('Metodologi CAPI', 'Status kelengkapan pengisian data CAPI.', '-', 'String', 'Sudah Selesai, Belum Terdata'),
    'Catatan': ('Informasi Tambahan', 'Catatan temuan khusus petugas.', '-', 'String', 'Narasi Bebas'),

    # Sungai Bakau Kecil (Appsheet_RT)
    'Nama_Ketua_RT': ('Identitas RT', 'Nama Ketua RT aktif yang bertindak sebagai narasumber.', '-', 'String', 'Nama Ketua RT'),
    'Jumlah_Penduduk_Laki_Laki': ('Penduduk Laki-Laki', 'Jumlah penduduk berjenis kelamin laki-laki di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penduduk_Perempuan': ('Penduduk Perempuan', 'Jumlah penduduk berjenis kelamin perempuan di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Bumbung_Rumah': ('Bangunan Fisik', 'Jumlah atap/bangunan fisik tempat tinggal di RT.', 'Unit', 'Integer', 'Nilai >= 0'),
    'Jumlah_KK': ('Rumah Tangga / KK', 'Jumlah kepala keluarga di RT.', 'Keluarga', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penduduk_Lansia': ('Penduduk Lansia', 'Jumlah penduduk berusia 60 tahun ke atas di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Kelahiran_Bayi': ('Kelahiran', 'Jumlah bayi lahir hidup dalam 1 tahun terakhir.', 'Bayi', 'Integer', 'Nilai >= 0'),
    'Jumlah_Kematian': ('Kematian', 'Jumlah kematian penduduk dalam 1 tahun terakhir.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penerima_PKH': ('Bansos PKH', 'Jumlah penduduk penerima PKH di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penerima_BPNT': ('Bansos BPNT', 'Jumlah penduduk penerima BPNT di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penerima_BST': ('Bansos BST', 'Jumlah penduduk penerima BST di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penerima_BLT': ('Bansos BLT', 'Jumlah penduduk penerima BLT di RT.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Memiliki_KTP': ('Administrasi KTP', 'Jumlah penduduk wajib KTP yang sudah memiliki KTP-el fisik.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Sekolah_TK': ('Pendidikan TK', 'Jumlah penduduk menempuh pendidikan TK/PAUD.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Sekolah_SD': ('Pendidikan SD', 'Jumlah penduduk menempuh pendidikan SD/MI.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Sekolah_SMP': ('Pendidikan SMP', 'Jumlah penduduk menempuh pendidikan SMP/MTs.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Sekolah_SMA': ('Pendidikan SMA', 'Jumlah penduduk menempuh pendidikan SMA/MA/SMK.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Sekolah_Sarjana': ('Pendidikan Tinggi', 'Jumlah penduduk lulusan Diploma/Sarjana.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Penduduk_Putus_Sekolah': ('Putus Sekolah', 'Jumlah anak usia sekolah (7-18 thn) yang tidak sekolah.', 'Orang', 'Integer', 'Nilai >= 0'),
    'Jumlah_Anak_Usia_0_1_Tahun': ('Kategori Bayi', 'Jumlah anak berusia di bawah 1 tahun.', 'Anak', 'Integer', 'Nilai >= 0'),
    'Jumlah_Anak_Usia_2_5_Tahun': ('Kategori Balita', 'Jumlah anak berusia antara 2 s.d. 5 tahun.', 'Anak', 'Integer', 'Nilai >= 0'),
    'Jumlah_Pendatang': ('Migrasi Masuk', 'Jumlah penduduk baru pindah masuk ke RT.', 'Orang', 'Integer', 'Nilai >= 0'),
}


def get_default_kegiatan(desa_title: str, desa_kebab: str, admin_type: str = "Desa", sub_type: str = "Dusun") -> List[KegiatanItemDTO]:
    if desa_kebab == "sungai-bakau-kecil":
        nama_keg = f"Pendataan Potensi Kewilayahan Rukun Tetangga (RT) dan Inventarisasi Fasilitas Umum Desa Cantik {desa_title} 2026"
        cara = f"Wawancara langsung dengan Ketua RT (Agregat RT) dan observasi lapangan titik koordinat fasilitas {admin_type.lower()} menggunakan aplikasi mobile AppSheet."
        unit = "Rukun Tetangga (RT), Sarana Prasarana (Fasilitas Umum)"
        cakupan = f"Seluruh wilayah {admin_type} {desa_title} (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 37 Rukun Tetangga (RT) dan 3 Dusun (Dusun Senggiring, Dusun Benteng Raya, Dusun Sepakat)."
        media_rilis = f"Portal Web Desa Cantik {desa_title} & Publikasi {admin_type} {desa_title} Dalam Angka 2026"
    elif desa_kebab == "pasir-palembang":
        nama_keg = f"Pendataan Sosial Keluarga dan Fasilitas Umum Desa Cantik {desa_title} 2026"
        cara = f"Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga dan observasi geospasial fasilitas {admin_type.lower()} menggunakan aplikasi mobile AppSheet."
        unit = "Bangunan Tempat Tinggal Biasa / Keluarga (CAPI), Sarana Prasarana (Fasilitas Umum)"
        cakupan = f"Seluruh wilayah {admin_type} {desa_title} (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 3 Dusun (Dusun Pelaik, Dusun Tengah, Dusun Tekam Baru)."
        media_rilis = f"Portal Web Desa Cantik {desa_title} & Publikasi {admin_type} {desa_title} Dalam Angka 2026"
    else:  # pasir-wan-salim
        nama_keg = f"Pendataan Sosial Keluarga Kelurahan Pasir Wan Salim 2026"
        cara = f"Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga menggunakan aplikasi mobile AppSheet."
        unit = "Bangunan Tempat Tinggal Biasa / Keluarga (CAPI)"
        cakupan = f"Seluruh wilayah {admin_type} {desa_title} (Kecamatan Mempawah Timur, Kabupaten Mempawah, Provinsi Kalimantan Barat) mencakup 17 Rukun Tetangga (RT) dan 8 Rukun Warga (RW 01 s.d. RW 08)."
        media_rilis = f"Portal Web Kelurahan Cantik {desa_title} & Publikasi {admin_type} {desa_title} Dalam Angka 2026"

    has_fas = (desa_kebab != "pasir-wan-salim")
    tujuan = f"Memetakan kondisi sosial-ekonomi penduduk di tingkat RT serta kondisi kelayakan sarana prasarana {admin_type.lower()} untuk mendukung kebijakan pembangunan berbasis bukti (evidence-based policy)." if has_fas else f"Memetakan kondisi sosial-ekonomi penduduk di tingkat RT/RW untuk mendukung kebijakan pembangunan berbasis bukti (evidence-based policy)."

    return [
        KegiatanItemDTO(1, "Nama Kegiatan", nama_keg),
        KegiatanItemDTO(2, "Instansi Penyelenggara", f"Pemerintah {admin_type} {desa_title} bekerjasama dengan BPS Kabupaten Mempawah"),
        KegiatanItemDTO(3, "Jenis Kegiatan", "Pendataan Langsung"),
        KegiatanItemDTO(4, "Tujuan Kegiatan", tujuan),
        KegiatanItemDTO(5, "Cara Pengumpulan Data", cara),
        KegiatanItemDTO(6, "Cakupan Wilayah", cakupan),
        KegiatanItemDTO(7, "Unit Pengamatan", unit),
        KegiatanItemDTO(8, "Frekuensi Kegiatan", "Tahunan (Annual)"),
        KegiatanItemDTO(9, "Waktu Pelaksanaan", "Juni - Juli 2026 (Pengumpulan Lapangan), Agustus 2026 (Diseminasi & Integrasi Web)"),
        KegiatanItemDTO(10, "Media Rilis", media_rilis),
    ]


def map_active_columns(data_rows: List[dict]) -> List[VariabelItemDTO]:
    """Dynamically parses active non-empty columns from live data rows into strongly-typed VariabelItemDTO."""
    if not data_rows:
        return []

    items = []
    no = 1
    for raw_col in data_rows[0].keys():
        col_clean = raw_col.strip()
        if not col_clean:
            continue
        
        # Check if the column has at least 1 non-empty value
        has_content = any(r.get(raw_col) and str(r.get(raw_col)).strip() not in ("", "-", "NONE", "null") for r in data_rows)
        if not has_content:
            continue

        # Look up metadata attributes from dictionary or auto-generate fallback
        attr = COLUMN_ATTRS.get(raw_col) or COLUMN_ATTRS.get(col_clean)
        if attr:
            konsep, definisi, satuan, tipe_data, rentang = attr
        else:
            konsep = "Pengamatan Sektoral"
            definisi = f"Isian variabel {col_clean} pada pengumpulan data lapangan."
            satuan = "-"
            tipe_data = "String"
            rentang = "Isian Tekstual"

        # Sanitize name for display
        display_name = col_clean.replace(" ", "_").replace("?", "").replace("/", "_")
        items.append(VariabelItemDTO(
            no=no,
            nama_variabel=display_name,
            konsep=konsep,
            definisi=definisi,
            satuan=satuan,
            tipe_data=tipe_data,
            pilihan_isian=rentang
        ))
        no += 1

    return items


def build_dynamic_indicators(active_cols: List[str], admin_type: str = "Desa", has_fas_data: bool = True) -> List[IndikatorItemDTO]:
    """Dynamically includes indicators ONLY if required forming variables exist in the active column list."""
    all_c = set(active_cols)
    inds = []
    no = 1

    # 1. Sex Ratio
    has_male = any(x in all_c for x in ['Jumlah_Penduduk_Laki_Laki', 'Jumlah_Orang_Laki-Laki_di_Rumah', 'Jumlah_Orang_Laki_Dirumah', 'Jumlah Orang Laki-Laki di Rumah'])
    has_female = any(x in all_c for x in ['Jumlah_Penduduk_Perempuan', 'Jumlah_Orang_Perempuan_di_Rumah', 'Jumlah_Orang_Perempuan_Dirumah', 'Jumlah Orang Perempuan di Rumah'])
    if has_male and has_female:
        inds.append(IndikatorItemDTO(no, "Rasio Jenis Kelamin (Sex Ratio)", f"Perbandingan jumlah penduduk laki-laki dengan 100 penduduk perempuan di {admin_type.lower()} tersebut.", 'frac(sum "L", sum "P") * 100', "Persen", "Demografi"))
        no += 1

    # 2. Average Household Size
    has_kk = any(x in all_c for x in ['Jumlah_KK', 'Jumlah_Kartu_Keluarga', 'Jumlah Kartu Keluarga'])
    if has_male and has_female and has_kk:
        inds.append(IndikatorItemDTO(no, "Rata-rata Anggota Rumah Tangga (ART)", "Rata-rata banyaknya anggota keluarga yang mendiami satu rumah tangga/KK.", 'frac(sum "L" + sum "P", sum "KK")', "Orang per Keluarga", "Kesejahteraan / Demografi"))
        no += 1

    # 3. Lansia
    has_lansia = any('Lansia' in c or '65-74' in c or '75+' in c for c in active_cols)
    if has_lansia:
        inds.append(IndikatorItemDTO(no, "Persentase Penduduk Lansia", f"Proporsi jumlah lansia terhadap total penduduk {admin_type.lower()}.", 'frac(sum "Lansia", "Total Penduduk") * 100', "Persen", "Demografi / Kelompok Rentan"))
        no += 1

    # 4. KTP
    has_ktp = any('Jumlah_Memiliki_KTP' in c for c in active_cols)
    if has_ktp:
        inds.append(IndikatorItemDTO(no, "Persentase Kepemilikan KTP-el", "Proporsi jumlah penduduk yang telah memiliki KTP fisik dari total penduduk wajib KTP.", 'frac(sum "KTP", "Total Wajib KTP") * 100', "Persen", "Administrasi Kependudukan"))
        no += 1

    # 5. Bansos
    has_bansos = any('bantuan' in c.lower() or 'PKH' in c or 'BPNT' in c or 'Sembako' in c for c in active_cols)
    if has_bansos:
        inds.append(IndikatorItemDTO(no, "Persentase Penerima Bantuan Sosial", "Proporsi penduduk yang terdaftar sebagai penerima bantuan sosial (PKH, BPNT, BLT) terhadap total penduduk.", 'frac(sum "Bansos", "Total Penduduk") * 100', "Persen", "Kesejahteraan Rakyat"))
        no += 1

    # 6. Putus Sekolah
    has_putus_sekolah = any('putus' in c.lower() or 'Putus' in c for c in active_cols)
    if has_putus_sekolah:
        inds.append(IndikatorItemDTO(no, "Persentase Anak Putus Sekolah", "Proporsi anak usia sekolah (7-18 tahun) yang tidak bersekolah terhadap total anak usia sekolah.", 'frac(sum "Putus Sekolah", "Total Usia Sekolah") * 100', "Persen", "Pendidikan"))
        no += 1

    # 7. Kepadatan Hunian Rumah
    has_bumbung = any(x in all_c for x in ['Jumlah_Bumbung_Rumah', 'Nomor_Bangunan', 'Nomor Bangunan', 'ID_Rumah'])
    if has_bumbung:
        inds.append(IndikatorItemDTO(no, "Kepadatan Hunian Rumah", "Rata-rata jumlah penduduk yang menghuni setiap bangunan fisik tempat tinggal.", 'frac("Total Penduduk", sum "Bangunan")', "Orang per Unit", "Infrastruktur / Kesehatan"))
        no += 1

    # 8. Rumah Layak Huni
    has_layak = all(any(k in c.lower() for c in active_cols) for k in ['dinding', 'lantai', 'atap', 'buang air besar'])
    if has_layak:
        inds.append(IndikatorItemDTO(no, "Persentase Rumah Layak Huni", "Proporsi rumah fisik yang memenuhi 4 kriteria kelayakan (dinding tembok/kayu, lantai semen/keramik/ubin/kayu, atap seng/genteng/asbes, dan jamban BAB sendiri).", 'frac(sum "Rumah Layak", sum "Bangunan") * 100', "Persen", "Perumahan & Lingkungan"))
        no += 1

    # 9. Rasio Sarana Keagamaan
    if has_fas_data:
        inds.append(IndikatorItemDTO(no, "Rasio Sarana Keagamaan per 1000 Penduduk", f"Ketersediaan sarana tempat ibadah {admin_type.lower()} untuk setiap 1.000 jiwa penduduk.", 'frac("Sarana Keagamaan", "Total Penduduk") * 1000', "Unit per 1000 Jiwa", "Sosial / Agama"))
        no += 1

    # 10. Partisipasi Usia Kerja Bekerja
    has_bekerja = any('bekerja' in c.lower() for c in active_cols)
    if has_bekerja:
        inds.append(IndikatorItemDTO(no, "Persentase Penduduk Usia Kerja Bekerja", f"Proporsi penduduk usia kerja (15-64 tahun) yang bekerja terhadap total penduduk usia kerja di {admin_type.lower()}.", 'frac(sum "Usia Kerja Bekerja", sum "Usia Kerja") * 100', "Persen", "Ketenagakerjaan"))
        no += 1

    # 11. UMKM
    has_umkm = any('UMKM' in c for c in active_cols)
    if has_umkm:
        inds.append(IndikatorItemDTO(no, "Persentase Rumah Tangga Memiliki UMKM", f"Proporsi rumah tangga yang mengelola usaha mikro, kecil, atau menengah di {admin_type.lower()}.", 'frac(sum "Keluarga UMKM", sum "KK") * 100', "Persen", "Perekonomian"))
        no += 1

    # 12. BPJS
    has_bpjs = any('BPJS' in c for c in active_cols)
    if has_bpjs:
        inds.append(IndikatorItemDTO(no, "Persentase Kepemilikan Jaminan Kesehatan (BPJS)", "Proporsi anggota keluarga yang memiliki jaminan kesehatan BPJS.", 'frac(sum "Peserta BPJS", "Total Penduduk") * 100', "Persen", "Kesehatan / Sosial"))
        no += 1

    return inds


def build_desa_metadata_dto(desa_kebab: str, desa_title: str) -> DesaMetadataDTO:
    """Builds the complete DesaMetadataDTO for any given village strictly by dynamically fetching and inspecting its live sheet columns."""
    is_kel = (desa_kebab == "pasir-wan-salim")
    admin_type = "Kelurahan" if is_kel else "Desa"
    sub_type = "RW" if is_kel else "Dusun"

    cfg = get_desa_config(desa_kebab)
    d1, d2 = fetch_desa_data(cfg)

    kegiatan = get_default_kegiatan(desa_title, desa_kebab=desa_kebab, admin_type=admin_type, sub_type=sub_type)

    has_fas = bool(d2)

    if desa_kebab == "sungai-bakau-kecil":
        rt_vars = map_active_columns(d1)
        fas_vars = map_active_columns(d2)
        capi_vars = []
        all_active_cols = [v.nama_variabel for v in rt_vars]
    else:  # pasir-palembang & pasir-wan-salim
        rt_vars = []
        fas_vars = map_active_columns(d2)
        capi_vars = map_active_columns(d1)
        all_active_cols = [v.nama_variabel for v in capi_vars]

    variabel_dto = VariabelMetadataDTO(
        rt_variables=rt_vars,
        fasilitas_variables=fas_vars,
        capi_micro_variables=capi_vars,
    )
    indikator_dto = build_dynamic_indicators(all_active_cols, admin_type=admin_type, has_fas_data=has_fas)

    return DesaMetadataDTO(
        desa_kebab=desa_kebab,
        desa_title=desa_title,
        admin_type=admin_type,
        kegiatan=kegiatan,
        variabel=variabel_dto,
        indikator=indikator_dto,
    )
