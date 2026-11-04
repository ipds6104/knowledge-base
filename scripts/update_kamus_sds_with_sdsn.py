import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = '19mp02bfJv3I_FPky6dUU9ZIRSbW7wEQlkgbXFdK6g6M'
TAB_NAME = 'Kamus SDS Hari 2'

creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

# 23 OPD rows definition (Rows 4 to 26)
# Each item has: [No, OPD, Nama Variabel, Konsep, Definisi Operasional, Satuan, Ukuran, Klasifikasi, Kode SDSN]
rows_data = [
    # 1. BPKAD
    [
        '1',
        'Badan Pengelola Keuangan dan Aset Daerah (BPKAD)',
        'Realisasi Pendapatan Daerah',
        'Pendapatan Daerah',
        'Jumlah penerimaan oleh bendahara umum daerah atau entitas pemerintah lainnya yang menambah saldo anggaran dalam periode tahun anggaran bersangkutan yang menjadi hak pemerintah daerah dan tidak perlu dibayar kembali.',
        'Rupiah',
        'Nilai',
        'Jenis Pendapatan (PAD, Transfer, Lain-lain), Wilayah',
        'SDSN [25010023]'
    ],
    # 2. BKPSDM
    [
        '2',
        'Badan Kepegawaian dan Pengembangan SDM (BKPSDM)',
        'Jumlah Pegawai Aparatur Sipil Negara (ASN)',
        'Aparatur Sipil Negara (ASN)',
        'Banyaknya pegawai negeri sipil (PNS) dan pegawai pemerintah dengan perjanjian kerja (PPPK) yang diangkat oleh pejabat pembina kepegawaian dan diserahi tugas dalam suatu jabatan pemerintahan atau diserahi tugas negara lainnya dan digaji berdasarkan peraturan perundang-undangan.',
        'Orang',
        'Total',
        'Tingkat Pendidikan, Jenis Jabatan, Jenis Pegawai (PNS/PPPK), Jenis Kelamin',
        'SDSN [25010050]'
    ],
    # 3. Bakesbangpol
    [
        '3',
        'Badan Kesatuan Bangsa dan Politik (Bakesbangpol)',
        'Jumlah Organisasi Kemasyarakatan (Ormas) Terdaftar',
        'Organisasi Kemasyarakatan',
        'Banyaknya organisasi kemasyarakatan berbadan hukum atau ber-Surat Keterangan Terdaftar (SKT) yang terdata secara resmi dan berstatus aktif pada Badan Kesatuan Bangsa dan Politik Kabupaten Mempawah.',
        'Organisasi',
        'Total',
        'Bentuk Badan Hukum, Bidang Kegiatan, Status Keaktifan',
        'Standar Daerah (SDSD)'
    ],
    # 4. BPPRD
    [
        '4',
        'Badan Pendapatan dan Retribusi Daerah (BPPRD)',
        'Jumlah Retribusi Daerah',
        'Retribusi Daerah',
        'Banyaknya pendapatan atas pungutan daerah sebagai pembayaran atas jasa atau pemberian izin tertentu yang khusus disediakan dan/atau diberikan oleh pemerintah daerah untuk kepentingan orang pribadi atau badan.',
        'Rupiah',
        'Nilai',
        'Jenis Retribusi (Jasa Umum, Jasa Usaha, Perizinan Tertentu), Wilayah',
        'SDSN [25010026]'
    ],
    # 5. Inspektorat
    [
        '5',
        'Inspektorat Daerah',
        'Nilai Akuntabilitas Kinerja Instansi Pemerintah (SAKIP)',
        'Akuntabilitas Kinerja',
        'Nilai evaluasi atas implementasi akuntabilitas kinerja instansi pemerintah pada Pemerintah Kabupaten Mempawah berdasarkan hasil penilaian Kementerian PAN-RB pada skala 0–100.',
        'Poin (0–100)',
        'Indeks Komposit',
        'Predikat Kinerja (AA, A, BB, B, CC, C, D)',
        'Standar Daerah (SDSD)'
    ],
    # 6. DPMPTSPUKM
    [
        '6',
        'Dinas Penanaman Modal, Koperasi UKM dan PTSP',
        'Jumlah Izin Usaha / NIB yang Diterbitkan',
        'Izin Usaha',
        'Banyaknya persetujuan berupa dokumen legal (termasuk Nomor Induk Berusaha / NIB) yang diberikan kepada pelaku usaha untuk memulai dan menjalankan kegiatan usaha pada bidang tertentu yang telah disahkan dan diterbitkan oleh instansi yang berwenang.',
        'Dokumen / NIB',
        'Total',
        'Skala Usaha (Mikro, Kecil, Menengah, Besar), Sektor Usaha (KBLI), Wilayah',
        'SDSN [23010100]'
    ],
    # 7. Dinkes PPKB
    [
        '7',
        'Dinas Kesehatan, Pengendalian Penduduk dan KB',
        'Prevalensi Stunting pada Balita',
        'Stunting (Tengkes)',
        'Bagian dari populasi anak berusia di bawah lima tahun (balita) yang bertubuh pendek dan sangat pendek, ditandai dengan panjang atau tinggi badannya berada di bawah standar (Z-score < -2 SD WHO).',
        'Persen',
        'Proporsi',
        'Jenis Kelamin, Kelompok Umur Balita, Wilayah Puskesmas',
        'SDSN [10410162]'
    ],
    # 8. RSUD dr. Rubini
    [
        '8',
        'RSUD dr. Rubini Mempawah',
        'Jumlah Kunjungan Pasien RSUD (Rawat Jalan dan Rawat Inap)',
        'Pelayanan Medis Rumah Sakit',
        'Banyaknya penerimaan pasien yang memanfaatkan layanan pemeriksaan, pengobatan, atau perawatan medis pada instalasi rawat jalan maupun rawat inap RSUD dr. Rubini Mempawah dalam kurun waktu satu tahun.',
        'Kunjungan / Orang',
        'Total',
        'Jenis Pelayanan (Rawat Jalan, Rawat Inap), Jenis Pembiayaan (BPJS, Umum, Asuransi Lain), Wilayah Domisili',
        'Standar Daerah (SDSD)'
    ],
    # 9. Dinsos P3APMPD (BELUM MENGISI LK-01)
    [
        '9',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ],
    # 10. Disdukcapil
    [
        '10',
        'Dinas Kependudukan dan Pencatatan Sipil',
        'Persentase Anak Berumur 0–17 Tahun Memiliki Akta Kelahiran',
        'Akta Kelahiran',
        'Bagian dari penduduk yang berumur 0—17 tahun yang memiliki akta kelahiran baik yang diterbitkan oleh Dinas Kependudukan dan Catatan Sipil, Kantor Urusan Agama, atau instansi yang berwenang.',
        'Persen',
        'Proporsi',
        'Jenis Kelamin, Kelompok Umur, Wilayah Kecamatan',
        'SDSN [25010031]'
    ],
    # 11. Disperindagnaker
    [
        '11',
        'Dinas Perindustrian, Perdagangan dan Tenaga Kerja',
        'Jumlah Pencari Kerja Terdaftar (Pencari Kerja AK-1)',
        'Pencari Kerja',
        'Banyaknya penduduk yang sedang mencari pekerjaan dan telah mendaftarkan diri pada instansi yang bertanggung jawab di bidang ketenagakerjaan di Kabupaten Mempawah.',
        'Orang',
        'Total',
        'Jenis Kelamin, Tingkat Pendidikan Terakhir, Kelompok Umur, Wilayah',
        'SDSN [10210029]'
    ],
    # 12. Distanpangan
    [
        '12',
        'Dinas Pertanian, Ketahanan Pangan dan Perikanan',
        'Produksi Padi Sawah dan Ladang',
        'Produksi Tanaman Pangan',
        'Banyaknya hasil panen tanaman padi dalam bentuk Gabah Kering Giling (GKG) yang diproduksi oleh petani dalam kurun waktu satu tahun di wilayah Kabupaten Mempawah.',
        'Ton',
        'Total',
        'Subsektor Tanaman (Padi Sawah, Padi Ladang), Wilayah Kecamatan',
        'Standar Daerah (SDSD / BPS)'
    ],
    # 13. Dishub LH
    [
        '13',
        'Dinas Perhubungan dan Lingkungan Hidup',
        'Jumlah Timbulan Sampah',
        'Sampah',
        'Berat sampah yang dihasilkan dari sumber sampah, baik sampah rumah tangga maupun sampah lainnya, di wilayah Kabupaten Mempawah.',
        'Ton',
        'Massa',
        'Sumber Sampah (Rumah Tangga, Pasar, Kawasan Komersial), Wilayah',
        'SDSN [31010153]'
    ],
    # 14. DPUPR
    [
        '14',
        'Dinas Pekerjaan Umum dan Penataan Ruang',
        'Panjang Jalan Kabupaten Menurut Kondisi Permukaan',
        'Infrastruktur Jalan',
        'Panjang prasarana transportasi darat yang berada di bawah kewenangan Pemerintah Kabupaten Mempawah yang dirinci berdasarkan kondisi kemantapan fisiknya.',
        'Kilometer (Km)',
        'Panjang',
        'Kondisi Jalan (Baik, Sedang, Rusak Ringan, Rusak Berat), Jenis Permukaan (Aspal, Kerikil, Tanah)',
        'SDSN [24410046]'
    ],
    # 15. Disperkimtan
    [
        '15',
        'Dinas Perumahan, Kawasan Pemukiman dan Pertanahan',
        'Jumlah Rumah Tidak Layak Huni (RTLH) Terverifikasi',
        'Rumah Layak Huni',
        'Banyaknya unit bangunan tempat tinggal yang tidak memenuhi persyaratan keselamatan bangunan, kecukupan minimum luas bangunan, serta kesehatan penghuni yang telah diverifikasi dan divalidasi oleh instansi yang berwenang.',
        'Unit Rumah',
        'Total',
        'Komponen Kerusakan (Atap, Lantai, Dinding, Sanitasi), Wilayah Kecamatan',
        'SDSN [10710076]'
    ],
    # 16. BPBD
    [
        '16',
        'Badan Penanggulangan Bencana Daerah (BPBD)',
        'Jumlah Kejadian Bencana Daerah',
        'Bencana',
        'Banyaknya kejadian peristiwa atau rangkaian peristiwa yang mengancam dan mengganggu kehidupan dan penghidupan masyarakat yang disebabkan faktor alam dan/atau nonalam di wilayah Kabupaten Mempawah.',
        'Kejadian',
        'Total',
        'Jenis Bencana (Banjir, Karhutla, Angin Puting Beliung, Abrasi), Wilayah Kecamatan',
        'SDSN [31010045]'
    ],
    # 17. Satpol PP
    [
        '17',
        'Satuan Polisi Pamong Praja',
        'Jumlah Pelanggaran Peraturan Daerah yang Ditindaklanjuti',
        'Pelanggaran Peraturan Daerah',
        'Banyaknya kejadian perilaku menyimpang dan pelanggaran terhadap Peraturan Daerah atau Peraturan Kepala Daerah Kabupaten Mempawah yang ditindaklanjuti melalui penegakan yustisial maupun nonyustisial.',
        'Kasus / Kejadian',
        'Total',
        'Jenis Perda yang Dilanggar, Bentuk Tindakan (Teguran, Pembongkaran, Sidang Tipiring), Wilayah',
        'SDSN [10810028]'
    ],
    # 18. Dispusip (BELUM MENGISI LK-01)
    [
        '18',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ],
    # 19. Sekretariat DPRD
    [
        '19',
        'Sekretariat DPRD',
        'Jumlah Pelaksanaan Rapat Paripurna DPRD',
        'Rapat Paripurna DPRD',
        'Banyaknya forum rapat resmi tertinggi anggota Dewan Perwakilan Rakyat Daerah Kabupaten Mempawah yang diselenggarakan untuk mengambil keputusan penetapan Perda, persetujuan anggaran, dan agenda strategis daerah lainnya.',
        'Kegiatan / Kali',
        'Total',
        'Agenda Rapat (Penetapan Perda, LKPJ, APBD, Rapat Paripurna Istimewa)',
        'Standar Daerah (SDSD)'
    ],
    # 20. Bapperida (BELUM MENGISI LK-01)
    [
        '20',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ],
    # 21. Diskominfo
    [
        '21',
        'Dinas Komunikasi dan Informatika (Walidata)',
        'Indeks Sistem Pemerintahan Berbasis Elektronik (SPBE)',
        'Sistem Pemerintahan Berbasis Elektronik',
        'Nilai tingkat kematangan pemanfaatan teknologi informasi dan komunikasi dalam penyelenggaraan tata kelola pemerintahan di lingkungan Pemerintah Kabupaten Mempawah berdasarkan hasil evaluasi KemenPAN-RB pada skala 1,00–5,00.',
        'Indeks (1,00–5,00)',
        'Indeks Komposit',
        'Predikat Kematangan (Rintisan, Terkelola, Terstandarisasi, Terpadu, Optimum)',
        'Standar Daerah (SDSD)'
    ],
    # 22. Disdikporapar
    [
        '22',
        'Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata',
        'Jumlah Ruang Kelas Menurut Kondisi Bangunan',
        'Ruang Kelas',
        'Banyaknya ruangan di dalam bangunan sekolah (SD dan SMP) di Kabupaten Mempawah yang berfungsi sebagai tempat proses kegiatan belajar mengajar (KBM) yang dirinci berdasarkan kondisi kelayakan fisiknya.',
        'Unit Ruang',
        'Total',
        'Kondisi Bangunan (Baik, Rusak Ringan, Rusak Sedang, Rusak Berat), Jenjang Pendidikan (SD, SMP)',
        'SDSN [10310066]'
    ],
    # 23. Setda (BELUM MENGISI LK-01)
    [
        '23',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ]
]

header_row = [
    'No',
    'Perangkat Daerah (OPD)',
    'Nama Variabel Statistik',
    'Konsep',
    'Definisi Operasional',
    'Satuan',
    'Ukuran',
    'Klasifikasi / Tipe Data',
    'Rujukan / Kode SDSN (Kepka BPS 996/2025)'
]

print("Menulis Header Row 3 (A3:I3)...")
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"{TAB_NAME}!A3:I3",
    valueInputOption='RAW',
    body={'values': [header_row]}
).execute()

print("Menulis 23 Baris Data (A4:I26)...")
service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"{TAB_NAME}!A4:I26",
    valueInputOption='RAW',
    body={'values': rows_data}
).execute()

print("Mendapatkan sheetId untuk styling...")
sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheet_id = None
for s in sheet_metadata.get('sheets', []):
    if s.get('properties', {}).get('title') == TAB_NAME:
        sheet_id = s.get('properties', {}).get('sheetId')
        break

if sheet_id is not None:
    print(f"Menerapkan styling pada sheetId {sheet_id}...")
    requests = [
        # Format Header A3:I3
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 2,
                    'endRowIndex': 3,
                    'startColumnIndex': 0,
                    'endColumnIndex': 9
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.102, 'green': 0.212, 'blue': 0.365}, # #1A365D Dark Navy
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'fontSize': 10,
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        },
        # Column I Width (Col index 8): 180px
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 8,
                    'endIndex': 9
                },
                'properties': {'pixelSize': 180},
                'fields': 'pixelSize'
            }
        },
        # Alignment & text format for Data Rows (A4:I26)
        # Col I (index 8): CENTER alignment, bold if SDSN
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 3,
                    'endRowIndex': 26,
                    'startColumnIndex': 8,
                    'endColumnIndex': 9
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {'fontSize': 9, 'bold': True}
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        },
        # Borders for full table A3:I26
        {
            'updateBorders': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 2,
                    'endRowIndex': 26,
                    'startColumnIndex': 0,
                    'endColumnIndex': 9
                },
                'top': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
                'bottom': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
                'left': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
                'right': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
                'innerHorizontal': {'style': 'SOLID', 'color': {'red': 0.85, 'green': 0.85, 'blue': 0.85}},
                'innerVertical': {'style': 'SOLID', 'color': {'red': 0.85, 'green': 0.85, 'blue': 0.85}}
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()
    print("✅ Berhasil styling dan update tabel Kamus SDS Hari 2 dengan rujukan SDSN!")

print("Selesai sempurna!")
