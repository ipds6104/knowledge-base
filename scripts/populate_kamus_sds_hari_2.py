#!/usr/bin/env python3
"""
scripts/populate_kamus_sds_hari_2.py
Populates the 'Kamus SDS Hari 2' tab with standardized metadata entries for all 23 OPDs.
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '19mp02bfJv3I_FPky6dUU9ZIRSbW7wEQlkgbXFdK6g6M'
TAB_NAME = 'Kamus SDS Hari 2'
TAB_ID = 1294767786

# 23 OPD Standar Data Statistik (SDS) Entries
ENTRIES = [
    [
        '1',
        'Badan Pengelola Keuangan dan Aset Daerah (BPKAD)',
        'Realisasi Pendapatan Asli Daerah (PAD)',
        'Pendapatan Daerah',
        'Penerimaan yang diperoleh daerah dari sumber-sumber dalam wilayahnya sendiri yang dipungut berdasarkan peraturan daerah sesuai peraturan perundang-undangan.',
        'Rupiah',
        'Jumlah Kumulatif',
        'Numerik (Mata Uang)'
    ],
    [
        '2',
        'Badan Kepegawaian dan Pengembangan SDM (BKPSDM)',
        'Jumlah Aparatur Sipil Negara (ASN) Menurut Tingkat Pendidikan',
        'Kepegawaian Daerah',
        'Jumlah pegawai negeri sipil dan PPPK yang aktif bekerja di lingkungan Pemerintah Kabupaten Mempawah yang dirinci berdasarkan kualifikasi ijazah pendidikan formal terakhir yang diakui.',
        'Orang',
        'Jumlah Mutlak',
        'Numerik (Diskrit)'
    ],
    [
        '3',
        'Badan Kesatuan Bangsa dan Politik (Bakesbangpol)',
        'Jumlah Organisasi Kemasyarakatan (Ormas) Terdaftar dan Aktif',
        'Kelembagaan Masyarakat',
        'Jumlah organisasi kemasyarakatan berbadan hukum atau ber-SKT yang terdata secara resmi dan berstatus aktif pada Badan Kesatuan Bangsa dan Politik Kabupaten Mempawah.',
        'Organisasi',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '4',
        'Badan Pendapatan dan Retribusi Daerah (BPPRD)',
        'Realisasi Penerimaan Retribusi Daerah',
        'Pendapatan Daerah',
        'Penerimaan daerah sebagai pembayaran atas jasa atau pemberian izin tertentu yang khusus disediakan dan/atau diberikan oleh Pemerintah Kabupaten Mempawah untuk kepentingan orang pribadi atau badan.',
        'Rupiah',
        'Jumlah Kumulatif',
        'Numerik (Mata Uang)'
    ],
    [
        '5',
        'Inspektorat Daerah',
        'Nilai Akuntabilitas Kinerja Instansi Pemerintah (SAKIP)',
        'Akuntabilitas Pemerintah',
        'Nilai evaluasi atas implementasi sistem akuntabilitas kinerja instansi pemerintah pada Pemerintah Kabupaten Mempawah yang dinilai oleh Kementerian PAN-RB pada skala 0–100.',
        'Poin / Nilai',
        'Indeks Komposit',
        'Numerik (Kontinu)'
    ],
    [
        '6',
        'Dinas Penanaman Modal, Koperasi UKM dan PTSP',
        'Jumlah Nomor Induk Berusaha (NIB) Terbit',
        'Legalitas Usaha',
        'Jumlah identitas pelaku usaha yang diterbitkan oleh Lembaga OSS setelah pelaku usaha melakukan pendaftaran di sistem OSS-RBA di Kabupaten Mempawah.',
        'Unit NIB',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '7',
        'Dinas Kesehatan, Pengendalian Penduduk dan KB',
        'Angka Kematian Balita (AKABA) per 1.000 Kelahiran Hidup',
        'Derajat Kesehatan Anak',
        'Jumlah kematian anak usia di bawah lima tahun (0–4 tahun) per 1.000 kelahiran hidup pada kurun waktu satu tahun berjalan di wilayah Kabupaten Mempawah.',
        'Per 1.000 Kelahiran Hidup',
        'Rasio',
        'Numerik (Kontinu)'
    ],
    [
        '8',
        'RSUD dr. Rubini Mempawah',
        'Tingkat Keterisian Tempat Tidur (Bed Occupancy Rate / BOR)',
        'Efisiensi Pelayanan Rawat Inap',
        'Persentase pemakaian tempat tidur yang tersedia di ruang rawat inap RSUD dr. Rubini Mempawah dalam suatu satuan waktu tertentu.',
        'Persen (%)',
        'Rasio Persentase',
        'Numerik (Kontinu, 0–100%)'
    ],
    [
        '9',
        'Dinas Sosial, P3APMPD',
        'Jumlah Pemerlu Pelayanan Kesejahteraan Sosial (PPKS) Terdata',
        'Penyelenggaraan Kesejahteraan Sosial',
        'Jumlah perseorangan, keluarga, atau kelompok yang karena suatu hambatan atau kesulitan tidak dapat melaksanakan fungsi sosialnya dan terdata dalam DTKS di Kabupaten Mempawah.',
        'Jiwa / Orang',
        'Jumlah Mutlak',
        'Numerik (Diskrit)'
    ],
    [
        '10',
        'Dinas Kependudukan dan Pencatatan Sipil',
        'Jumlah Penduduk Terdaftar',
        'Kependudukan De Jure',
        'Jumlah warga negara Indonesia dan orang asing yang bertempat tinggal dan tercatat dalam database kependudukan SIAK pada Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah.',
        'Jiwa / Orang',
        'Jumlah Mutlak',
        'Numerik (Diskrit)'
    ],
    [
        '11',
        'Dinas Perindustrian, Perdagangan dan Tenaga Kerja',
        'Jumlah Pencari Kerja Terdaftar (Pencari Kerja AK-1)',
        'Ketenagakerjaan',
        'Jumlah angkatan kerja yang mendaftarkan diri secara resmi pada Disperindagnaker Kabupaten Mempawah untuk mendapatkan Kartu Tanda Bukti Pendaftaran Pencari Kerja (Kartu AK-1).',
        'Orang',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '12',
        'Dinas Pertanian, Ketahanan Pangan dan Perikanan',
        'Jumlah Produksi Daging Ternak',
        'Produksi Peternakan',
        'Volume total daging dari pemotongan hewan ternak besar, kecil, dan unggas yang dihasilkan di Kabupaten Mempawah dalam kurun waktu satu tahun.',
        'Kilogram (Kg)',
        'Jumlah Kumulatif',
        'Numerik (Kontinu)'
    ],
    [
        '13',
        'Dinas Perhubungan dan Lingkungan Hidup',
        'Volume Timbulan Sampah Harian',
        'Pengelolaan Lingkungan Hidup',
        'Estimasi volume timbulan sampah domestik dan non-domestik yang dihasilkan per hari di wilayah Kabupaten Mempawah yang ditangani dan masuk ke TPA.',
        'Meter Kubik per Hari (m³/hari)',
        'Laju Harian',
        'Numerik (Kontinu)'
    ],
    [
        '14',
        'Dinas Pekerjaan Umum dan Penataan Ruang',
        'Panjang Jalan Kondisi Mantap',
        'Infrastruktur Jalan',
        'Panjang ruas jalan kabupaten dengan kondisi baik dan sedang berdasarkan hasil survei kondisi jalan semesteran.',
        'Kilometer',
        'Panjang',
        'Numerik (Kontinu)'
    ],
    [
        '15',
        'Dinas Perumahan, Kawasan Pemukiman dan Pertanahan',
        'Jumlah Rumah Tidak Layak Huni (RTLH) Terverifikasi',
        'Perumahan Layak Huni',
        'Jumlah unit rumah tinggal yang tidak memenuhi persyaratan keselamatan bangunan, kecukupan minimum luas ruang, dan kesehatan penghuni berdasarkan hasil verifikasi lapangan.',
        'Unit Rumah',
        'Jumlah Mutlak',
        'Numerik (Diskrit)'
    ],
    [
        '16',
        'Badan Penanggulangan Bencana Daerah (BPBD)',
        'Jumlah Korban Bencana yang Menerima Bantuan Logistik',
        'Penanggulangan Bencana',
        'Jumlah jiwa/penduduk terdampak kejadian bencana alam di Kabupaten Mempawah yang telah diverifikasi dan menerima penyaluran bantuan logistik tanggap darurat.',
        'Jiwa / Orang',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '17',
        'Satuan Polisi Pamong Praja',
        'Jumlah Kasus Pelanggaran Peraturan Daerah yang Ditindaklanjuti',
        'Ketertiban Umum dan Ketentraman Masyarakat',
        'Jumlah kejadian pelanggaran terhadap peraturan daerah (Perda) dan peraturan kepala daerah (Perkada) yang diproses dan ditindaklanjuti oleh Satpol PP.',
        'Kasus',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '18',
        'Dinas Perpustakaan dan Kearsipan',
        'Jumlah Kunjungan Pemustaka Perpustakaan Daerah',
        'Literasi dan Minat Baca',
        'Frekuensi kehadiran masyarakat yang berkunjung secara langsung ke layanan perpustakaan umum daerah Kabupaten Mempawah untuk membaca, meminjam buku, atau mengakses literasi.',
        'Orang / Kunjungan',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '19',
        'Sekretariat DPRD',
        'Jumlah Pelaksanaan Rapat Paripurna DPRD',
        'Fungsi Legislasi dan Pengawasan Dewan',
        'Jumlah sidang paripurna anggota DPRD Kabupaten Mempawah yang diselenggarakan dalam rangka pengambilan keputusan, penetapan perda, atau penyampaian LKPJ.',
        'Kali / Kegiatan',
        'Jumlah Kumulatif',
        'Numerik (Diskrit)'
    ],
    [
        '20',
        'Bapperida (Bappeda / Litbang)',
        'Nilai Rata-rata Indeks Desa Membangun (IDM)',
        'Kemandirian Desa',
        'Nilai indeks komposit dari Indeks Ketahanan Sosial, Ekonomi, dan Ekologi seluruh desa di Kabupaten Mempawah yang dirilis resmi oleh Kemendes PDTT.',
        'Indeks (Skala 0–1)',
        'Indeks Komposit',
        'Numerik (Kontinu)'
    ],
    [
        '21',
        'Dinas Komunikasi dan Informatika (Walidata)',
        'Indeks Sistem Pemerintahan Berbasis Elektronik (SPBE)',
        'Tata Kelola Pemerintahan Digital',
        'Nilai tingkat kematangan penerapan SPBE Pemerintah Kabupaten Mempawah hasil evaluasi Kementerian PAN-RB pada skala 1,00 hingga 5,00.',
        'Indeks (Skala 1–5)',
        'Indeks Komposit',
        'Numerik (Kontinu)'
    ],
    [
        '22',
        'Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata',
        'Jumlah Peserta Didik Putus Sekolah Tingkat SMP',
        'Aksesibilitas Pendidikan Dasar',
        'Jumlah siswa jenjang Sekolah Menengah Pertama (SMP) negeri dan swasta di Kabupaten Mempawah yang berhenti sekolah sebelum menyelesaikan jenjang pendidikannya pada tahun ajaran berjalan.',
        'Siswa / Orang',
        'Jumlah Mutlak',
        'Numerik (Diskrit)'
    ],
    [
        '23',
        'Sekretariat Daerah',
        'Skor Kematangan Perangkat Daerah',
        'Kelembagaan dan Tata Laksana Daerah',
        'Nilai hasil evaluasi kelembagaan perangkat daerah di lingkungan Pemkab Mempawah yang mengukur ketepatan fungsi dan kapasitas organisasi sesuai Permendagri No. 99/2018.',
        'Poin (Skala 0–100)',
        'Nilai Komposit',
        'Numerik (Kontinu)'
    ]
]


def main():
    token_file = Path('token.json')
    if not token_file.exists():
        print("Error: token.json tidak ditemukan", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # 1. Bersihkan dulu baris 7 s.d. 50 yang sebelumnya ada sisa nomor 4..36
    print("Membersihkan range Kamus SDS Hari 2!A7:H50...")
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{TAB_NAME}!A7:H50"
    ).execute()

    # 2. Update Nilai A4:H26 (23 OPD)
    range_name = f"{TAB_NAME}!A4:H26"
    print(f"Mengisi {len(ENTRIES)} baris data Kamus SDS ke range {range_name}...")
    res = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body={'values': ENTRIES}
    ).execute()
    print(f"✅ Berhasil mengupdate nilai: {res.get('updatedCells')} sel.")

    # 3. Format Sel: Border, Wrap, Alignment, Font Calibri 10
    border_style = {
        'style': 'SOLID',
        'width': 1,
        'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}
    }
    requests = [
        # Format Kolom No (Col index 0, A4:A26) -> Center
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 3,
                    'endRowIndex': 26,
                    'startColumnIndex': 0,
                    'endColumnIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontFamily': 'Calibri', 'fontSize': 10},
                        'borders': {'top': border_style, 'bottom': border_style, 'left': border_style, 'right': border_style}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        },
        # Format Kolom Teks (Col index 1-4, B4:E26) -> Left
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 3,
                    'endRowIndex': 26,
                    'startColumnIndex': 1,
                    'endColumnIndex': 5
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontFamily': 'Calibri', 'fontSize': 10},
                        'borders': {'top': border_style, 'bottom': border_style, 'left': border_style, 'right': border_style}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        },
        # Format Kolom Satuan & Ukuran (Col index 5-6, F4:G26) -> Center
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 3,
                    'endRowIndex': 26,
                    'startColumnIndex': 5,
                    'endColumnIndex': 7
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontFamily': 'Calibri', 'fontSize': 10},
                        'borders': {'top': border_style, 'bottom': border_style, 'left': border_style, 'right': border_style}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        },
        # Format Kolom Klasifikasi/Tipe Data (Col index 7, H4:H26) -> Left
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 3,
                    'endRowIndex': 26,
                    'startColumnIndex': 7,
                    'endColumnIndex': 8
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontFamily': 'Calibri', 'fontSize': 10},
                        'borders': {'top': border_style, 'bottom': border_style, 'left': border_style, 'right': border_style}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        }
    ]

    print("Menerapkan styling sel...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()
    print("✅ Berhasil menerapkan styling dan format tabel Kamus SDS Hari 2.")
    return 0


if __name__ == '__main__':
    sys.exit(main())

