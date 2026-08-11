"""Markdown Renderer Module for BPS Potensi Desa (PODES) Publication Engine."""

from pathlib import Path
from ..schemas import PodesPublicationData


def render_podes_md(pub_data: PodesPublicationData) -> Path:
    """Menggenerasikan naskah Markdown 5 Bab Publikasi Potensi Desa 2026 (Tahun Data 2025)."""
    cfg = pub_data.config
    m = pub_data.metrics

    name_title = cfg["name_title"]
    name_kebab = cfg["name_kebab"]
    name_upper = name_title.upper()
    admin_type = cfg["admin_type"]
    admin_upper = admin_type.upper()
    pub_no = cfg["pub_no"]
    kades_title = cfg["kades_title"]
    kades_name = cfg["kades_name"]

    year = cfg.get("year", 2026)
    data_year = cfg.get("data_year", 2025)

    md = f"""# **Potensi {admin_type} {name_title} {year}**

Nomor Publikasi : {pub_no}  
Ukuran Buku : 21 cm x 29,7 cm  
Jumlah Halaman : iv + 16 halaman  
Tahun Terbit : {year}  
Tahun Pendataan : {data_year}  

---

## **KATA PENGANTAR**

Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi **"Potensi {admin_type} {name_title} {year}"** ini dapat diselesaikan dengan baik. Publikasi ini menyajikan gambaran komprehensif mengenai potensi kewilayahan, kependudukan, perumahan, energi, fasilitas sosial, prasarana komunikasi, hingga kelembagaan dan ekonomi masyarakat di {admin_type} {name_title} berdasarkan Pendataan Potensi Desa (PODES) Tahun {data_year}.

Data yang disajikan diharapkan dapat menjadi rujukan baku bagi Pemerintah {admin_type} dan para pemangku kepentingan dalam perencanaan pembangunan kewilayahan (*evidence-based policy*) demi meningkatkan kesejahteraan masyarakat.

Kami menyampaikan ucapan terima kasih dan penghargaan setinggi-tingginya kepada seluruh pihak yang telah membantu terwujudnya publikasi ini.

{name_title}, Agustus {year}  
**{kades_title}**  

<u>**{kades_name.upper()}**</u>

---

## **DAFTAR ISI**

| Judul Bab / Bagian | Halaman |
| :--- | :--- |
| **KATA PENGANTAR** | i |
| **DAFTAR ISI** | ii |
| **DAFTAR TABEL** | iii |
| **PENJELASAN TEKNIS & KONSEP DEFINISI PODES** | 1 |
| **BAB I: WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN** | 3 |
| 1.1 Status Wilayah, Kawasan Hutan & Administrasi RT/RW | 3 |
| 1.2 Kependudukan, Rasio Jenis Kelamin & Keluarga Pertanian | 4 |
| **BAB II: ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA** | 6 |
| 2.1 Penggunaan Listrik, Penerangan Jalan & Bahan Bakar | 6 |
| 2.2 Air Minum & Potensi/Mitigasi Bencana Alam | 7 |
| **BAB III: FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)** | 9 |
| 3.1 Ketersediaan Sarana Pendidikan Formal & Keagamaan | 9 |
| 3.2 Sarana Kesehatan, Posyandu & Posbindu | 10 |
| **BAB IV: TRANSPORTASI, KOMUNIKASI, EKONOMI & INDUSTRI** | 12 |
| 4.1 Prasarana Transportasi, Akses Jalan & Angkutan Umum | 12 |
| 4.2 Menara BTS, Layanan Telekomunikasi & Sinyal Internet | 13 |
| 4.3 Fasilitas Ekonomi, Mata Pencaharian & Industri Mikro/Kecil (IMK) | 14 |
| **BAB V: PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA** | 15 |
| 5.1 Aparatur Pemerintah Desa, BPD/LMK & Sistem Informasi Desa | 15 |

---

## **DAFTAR TABEL**

| No Tabel | Nama Tabel | Halaman |
| :--- | :--- | :--- |
| **Tabel 1** | Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW Tahun {data_year} | 3 |
| **Tabel 2** | Jumlah Penduduk Menurut Jenis Kelamin, Sex Ratio, dan Keluarga Pertanian Tahun {data_year} | 4 |
| **Tabel 3** | Penggunaan Daya Listrik, Penerangan Jalan Utama, dan Bahan Bakar Memasak Tahun {data_year} | 6 |
| **Tabel 4** | Sumber Air Minum Utama dan Keberadaan Mitigasi Bencana Alam Tahun {data_year} | 7 |
| **Tabel 5** | Rekapitulasi Ketersediaan Sarana Pendidikan Formal dan Keagamaan Tahun {data_year} | 9 |
| **Tabel 6** | Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu Tahun {data_year} | 10 |
| **Tabel 7** | Prasarana Transportasi, Jenis Permukaan Jalan, dan Angkutan Umum Tahun {data_year} | 12 |
| **Tabel 8** | Keberadaan Menara BTS, Operator Telekomunikasi, dan Sinyal Internet Tahun {data_year} | 13 |
| **Tabel 9** | Fasilitas Ekonomi Utama, Mata Pencaharian, dan Industri Mikro Kecil (IMK) Tahun {data_year} | 14 |
| **Tabel 10** | Aparatur Pemerintah Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa Tahun {data_year} | 15 |

---

## **PENJELASAN TEKNIS & KONSEP DEFINISI PODES**

1. **Potensi Desa (PODES)**: Pendataan inventarisasi potensi kewilayahan di tingkat desa/kelurahan yang mengumpulkan data prasarana, sarana, dan kondisi sosio-ekonomi wilayah.
2. **Status Daerah**: Pengklasifikasian wilayah desa/kelurahan menjadi Perdesaan atau Perkotaan berdasarkan skor kepadatan penduduk, persentase keluarga pertanian, dan aksesibilitas fasilitas umum.
3. **Kawasan Hutan**: Keberadaan atau posisi geografis wilayah desa/kelurahan terhadap batas kawasan hutan yang ditetapkan oleh Kementerian Lingkungan Hidup dan Kehutanan.
4. **Keluarga Pertanian**: Rumah tangga yang sekurang-kurangnya satu anggota keluarganya melakukan kegiatan pertanian dengan tujuan sebagian atau seluruh hasilnya untuk dijual/ditukar.
5. **Base Transceiver Station (BTS)**: Infrastruktur telekomunikasi yang memfasilitasi komunikasi nirkabel antara peranti komunikasi dan jaringan operator seluler.
6. **Industri Mikro dan Kecil (IMK)**: Usaha pengolahan yang memiliki jumlah tenaga kerja 1 hingga 19 orang (1-4 pekerja untuk Mikro, 5-19 pekerja untuk Kecil).

---

## **BAB I: WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN**

### **1.1 STATUS WILAYAH, KAWASAN HUTAN & ADMINISTRASI RT/RW**
{admin_type} {name_title} berstatus sebagai wilayah **{m.status_daerah}** dengan lokasi perkantoran berada di **{m.alamat_lengkap}**. Keberadaan wilayah terhadap kawasan hutan tercatat **{m.kawasan_hutan}**. Secara administratif, wilayah {admin_type} {name_title} terbagi atas **{m.jumlah_rw} Rukun Warga (RW)** dan **{m.jumlah_rt} Rukun Tetangga (RT)**.

**Tabel 1. Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW Tahun {data_year}**
| Indikator Kewilayahan | Isian Data PODES {data_year} |
| :--- | :--- |
| **Status Klasifikasi Wilayah** | {m.status_daerah} |
| **Alamat Lengkap Kantor Desa/Kelurahan** | {m.alamat_lengkap} |
| **Lokasi Terhadap Kawasan Hutan** | {m.kawasan_hutan} |
| **Jumlah Rukun Warga (RW)** | {m.jumlah_rw} RW |
| **Jumlah Rukun Tetangga (RT)** | {m.jumlah_rt} RT |

---

### **1.2 KEPENDUDUKAN, RASIO JENIS KELAMIN & KELUARGA PERTANIAN**
Jumlah penduduk di {admin_type} {name_title} hasil pendataan {data_year} sebanyak **{m.total_penduduk:,} jiwa**, terdiri dari **{m.penduduk_l:,} jiwa laki-laki ({m.male_pct}%)** dan **{m.penduduk_p:,} jiwa perempuan ({m.female_pct}%)**, dengan *sex ratio* sebesar **{m.sex_ratio}**. Total keluarga tercatat sebanyak **{m.jumlah_kk:,} KK**, di mana sebanyak **{m.kk_pertanian:,} keluarga ({m.kk_pertanian_pct}%)** bergerak di sektor pertanian.

**Tabel 2. Jumlah Penduduk Menurut Jenis Kelamin, Sex Ratio, dan Keluarga Pertanian Tahun {data_year}**
| Indikator Demografi & Pertanian | Jumlah / Nilai |
| :--- | :---: |
| **Jumlah Penduduk Laki-laki** | {m.penduduk_l:,} jiwa |
| **Jumlah Penduduk Perempuan** | {m.penduduk_p:,} jiwa |
| **Total Penduduk** | **{m.total_penduduk:,} jiwa** |
| **Rasio Jenis Kelamin (Sex Ratio)** | **{m.sex_ratio}** |
| **Total Keluarga (KK)** | {m.jumlah_kk:,} KK |
| **Jumlah Keluarga Pertanian** | **{m.kk_pertanian:,} KK ({m.kk_pertanian_pct}%)** |

---

## **BAB II: ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA**

### **2.1 PENGGUNAAN LISTRIK, PENERANGAN JALAN & BAHAN BAKAR**
Sebanyak **{m.listrik_pln:,} keluarga ({((m.listrik_pln/max(1, m.jumlah_kk))*100):.1f}%)** telah memanfaatkan sumber listrik PLN. Kondisi penerangan di jalan utama desa tergolong **"{m.penerangan_jalan}"**. Sebagian besar keluarga memanfaatkan **{m.bakar_masak}** sebagai bahan bakar utama untuk memasak.

**Tabel 3. Penggunaan Daya Listrik, Penerangan Jalan Utama, dan Bahan Bakar Memasak Tahun {data_year}**
| Indikator Energi & Utilitas | Isian Data PODES {data_year} |
| :--- | :--- |
| **Pengguna Listrik PLN** | {m.listrik_pln:,} KK |
| **Pengguna Listrik Non-PLN** | {m.listrik_non_pln} KK |
| **Bukan Pengguna Listrik** | {m.bukan_listrik} KK |
| **Penerangan Jalan Utama Desa** | {m.penerangan_jalan} |
| **Bahan Bakar Utama Memasak** | {m.bakar_masak} |

---

### **2.2 AIR MINUM & POTENSI/MITIGASI BENCANA ALAM**
Sumber air utama untuk konsumsi minum keluarga sebagian besar berasal dari **{m.air_minum}**. Terkait kejadian bencana alam, dalam satu tahun terakhir tercatat **"{m.bencana_alam}"**. Upaya mitigasi dan kesiapsiagaan bencana yang tersedia mencakup **{m.mitigasi_bencana}**.

**Tabel 4. Sumber Air Minum Utama dan Keberadaan Mitigasi Bencana Alam Tahun {data_year}**
| Indikator Lingkungan & Bencana | Isian Data PODES {data_year} |
| :--- | :--- |
| **Sumber Air Minum Utama** | {m.air_minum} |
| **Kejadian Bencana Alam Setahun Terakhir** | {m.bencana_alam} |
| **Fasilitas & Mitigasi Kesiapsiagaan Bencana** | {m.mitigasi_bencana} |

---

## **BAB III: FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)**

### **3.1 KETERSEDIAAN SARANA PENDIDIKAN FORMAL & KEAGAMAAN**
Fasilitas pendidikan di {admin_type} {name_title} meliputi: **{m.sarana_pendidikan}**.

**Tabel 5. Rekapitulasi Ketersediaan Sarana Pendidikan Formal dan Keagamaan Tahun {data_year}**
| Kategori Sarana | Rincian Ketersediaan Sarana Pendidikan |
| :--- | :--- |
| **Fasilitas Pendidikan** | {m.sarana_pendidikan} |

---

### **3.2 SARANA KESEHATAN, POSYANDU & POSBINDU**
Fasilitas pelayanan kesehatan yang tersedia meliputi: **{m.sarana_kesehatan}**. Dukungan pelayanan kesehatan bersumberdaya masyarakat mencakup **{m.posyandu_aktif} posyandu aktif** dengan pelayanan rutin sebulan sekali serta **{m.posbindu} posbindu**.

**Tabel 6. Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu Tahun {data_year}**
| Indikator Sarana Kesehatan | Rincian Ketersediaan Data |
| :--- | :--- |
| **Fasilitas Pelayanan Kesehatan** | {m.sarana_kesehatan} |
| **Posyandu Aktif (Bulanan)** | {m.posyandu_aktif} unit |
| **Posbindu** | {m.posbindu} unit |

---

## **BAB IV: TRANSPORTASI, KOMUNIKASI, EKONOMI & INDUSTRI**

### **4.1 PRASARANA TRANSPORTASI, AKSES JALAN & ANGKUTAN UMUM**
Prasarana transportasi antar desa terhubung via lalu lintas **{m.prasarana_transportasi}** dengan jenis permukaan jalan utama berupa **{m.jenis_jalan}**. Jalan darat dapat dilalui kendaraan roda 4 atau lebih **{m.jalan_roda4}**. Keberadaan angkutan umum teridentifikasi **"{m.angkutan_umum}"**.

**Tabel 7. Prasarana Transportasi, Jenis Permukaan Jalan, dan Angkutan Umum Tahun {data_year}**
| Indikator Transportasi | Isian Data PODES {data_year} |
| :--- | :--- |
| **Prasarana Transportasi Antar Desa** | {m.prasarana_transportasi} |
| **Jenis Permukaan Jalan Utama** | {m.jenis_jalan} |
| **Aksesibilitas Roda 4 atau Lebih** | {m.jalan_roda4} |
| **Keberadaan & Operasional Angkutan Umum** | {m.angkutan_umum} |

---

### **4.2 MENARA BTS, LAYANAN TELEKOMUNIKASI & SINYAL INTERNET**
Dukungan infrastruktur telekomunikasi mencakup **{m.jumlah_bts} menara BTS** dengan jangkuan operator meliputi **{m.operator_seluler}**. Kualitas sinyal telepon seluler tergolong **"{m.sinyal_hp}"** dengan jaringan internet seluler mendukung **{m.sinyal_internet}**.

**Tabel 8. Keberadaan Menara BTS, Operator Telekomunikasi, dan Sinyal Internet Tahun {data_year}**
| Indikator Komunikasi & Sinyal | Isian Data PODES {data_year} |
| :--- | :--- |
| **Jumlah Menara BTS** | {m.jumlah_bts} unit |
| **Operator Layanan Seluler** | {m.operator_seluler} |
| **Kekuatan Sinyal Telepon** | {m.sinyal_hp} |
| **Jaringan Internet Seluler** | {m.sinyal_internet} |

---

### **4.3 FASILITAS EKONOMI, MATA PENCAHARIAN & INDUSTRI MIKRO/KECIL (IMK)**
Mata pencaharian utama sebagian besar penduduk adalah **{m.sumber_penghasilan_utama}** (subsektor **{m.subsektor_utama}**). Aktivitas ekonomi didukung oleh fasilitas berupa **{m.sarana_ekonomi}**. Selain itu, berkembang sebanyak **{m.jumlah_imk} unit Industri Mikro dan Kecil (IMK)** di wilayah {admin_type}.

**Tabel 9. Fasilitas Ekonomi Utama, Mata Pencaharian, dan Industri Mikro Kecil (IMK) Tahun {data_year}**
| Indikator Ekonomi & Industri | Isian Data PODES {data_year} |
| :--- | :--- |
| **Mata Pencaharian Utama Penduduk** | {m.sumber_penghasilan_utama} ({m.subsektor_utama}) |
| **Fasilitas Ekonomi Utama** | {m.sarana_ekonomi} |
| **Jumlah Industri Mikro & Kecil (IMK)** | {m.jumlah_imk} unit usaha |

---

## **BAB V: PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA**

### **5.1 APARATUR PEMERINTAH DESA, BPD/LMK & SISTEM INFORMASI DESA**
Penyelenggaraan pemerintahan {admin_type} {name_title} didukung oleh **{m.aparatur_pemdes} orang aparatur pemerintah**. Keberadaan lembaga perwakilan rakyat desa (BPD/LMK) tercatat **"{m.keberadaan_bpd}"** dengan frekuensi musyawarah sebanyak **{m.musyawarah_desa} kali kegiatan** dalam sebulan/setahun terakhir. Keberadaan Sistem Informasi Desa (SID) teridentifikasi **"{m.sistem_informasi_desa}"** dan ketersediaan SPPG tercatat **"{m.jumlah_sppg}"**.

**Tabel 10. Aparatur Pemerintah Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa Tahun {data_year}**
| Indikator Pemerintahan & Kelembagaan | Isian Data PODES {data_year} |
| :--- | :--- |
| **Jumlah Aparatur Pemerintah Desa/Kelurahan** | {m.aparatur_pemdes} orang |
| **Keberadaan BPD / LMK** | {m.keberadaan_bpd} |
| **Jumlah Kegiatan Musyawarah Desa** | {m.musyawarah_desa} kali |
| **Sistem Informasi Desa (SID)** | {m.sistem_informasi_desa} |
| **Ketersediaan SPPG** | {m.jumlah_sppg} |

---

# **MENCERDASKAN BANGSA DENGAN DATA STATISTIK DESA**
"""

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-potensi-{name_kebab}-{year}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Markdown file written: {out_path}")
    return out_path
