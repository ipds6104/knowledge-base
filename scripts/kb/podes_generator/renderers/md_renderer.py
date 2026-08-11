"""Markdown Renderer Module for BPS Potensi Desa (PODES) Publication Engine."""

from pathlib import Path
from ..schemas import PodesPublicationData


def render_podes_md(pub_data: PodesPublicationData) -> Path:
    """Menggenerasikan naskah Markdown 5 Bab Publikasi Potensi Desa 2026 (Tahun Data 2025)."""
    cfg = pub_data.config
    m = pub_data.metrics

    name_title = cfg["name_title"]
    name_kebab = cfg["name_kebab"]
    admin_type = cfg["admin_type"]
    admin_upper = admin_type.upper()
    pub_no = cfg["pub_no"]
    kades_title = cfg["kades_title"]
    kades_name = cfg["kades_name"]
    gov_name = cfg.get("gov_name", f"Pemerintah {admin_type} {name_title}")

    year = cfg.get("year", 2026)
    data_year = cfg.get("data_year", 2025)

    md = f"""# **Potensi {admin_type} {name_title} {year}**

Ukuran Buku : 21 cm x 29,7 cm  
Jumlah Halaman : ix + 15 halaman  
Penyusun : {gov_name} (menggunakan data PODES BPS)  
Penyunting : BPS Kabupaten Mempawah  
Penerbit : © {gov_name} & BPS Kabupaten Mempawah  
Tahun Terbit : {year}  
Tahun Pendataan : {data_year}  

---

## **KATA PENGANTAR**

Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi **"Potensi {admin_type} {name_title} {year}"** ini dapat diselesaikan dengan baik. Publikasi ini disusun oleh **{gov_name}** menggunakan data hasil Pendataan Potensi Desa (PODES) Tahun {data_year} dari Badan Pusat Statistik (BPS) dan disunting oleh BPS Kabupaten Mempawah.

Publikasi ini menyajikan gambaran komprehensif mengenai potensi kewilayahan, kependudukan, perumahan, energi, fasilitas sosial, prasarana komunikasi, hingga kelembagaan dan ekonomi masyarakat di {admin_type} {name_title}.

Data yang disajikan diharapkan dapat menjadi rujukan baku bagi Pemerintah {admin_type} dan para pemangku kepentingan dalam perencanaan pembangunan kewilayahan (*evidence-based policy*) demi meningkatkan kesejahteraan masyarakat.

Kami menyampaikan ucapan terima kasih dan penghargaan setinggi-tingginya kepada seluruh pihak yang telah membantu terwujudnya publikasi ini.

{name_title}, Agustus {year}  
**{kades_title.upper()}**  

<u>**{kades_name.upper()}**</u>

---

## **DAFTAR ISI**

| Judul Bab / Bagian | Halaman |
| :--- | :--- |
| **KATA PENGANTAR** | iv |
| **DAFTAR ISI** | vi |
| **DAFTAR TABEL** | vii |
| **PENJELASAN UMUM** | viii |
| **DAFTAR SINGKATAN** | ix |
| **STATISTIK KUNCI PODES {data_year}** | 1 |
| **BAB I: WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN** | 3 |
| 1.1 Status Wilayah, Kawasan Hutan & Administrasi RT/RW | 4 |
| 1.2 Kependudukan, Rasio Jenis Kelamin & Keluarga Pertanian | 5 |
| **BAB II: ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA** | 6 |
| 2.1 Penggunaan Listrik, Penerangan Jalan & Bahan Bakar | 7 |
| 2.2 Air Minum & Potensi/Mitigasi Bencana Alam | 8 |
| **BAB III: FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)** | 9 |
| 3.1 Ketersediaan Sarana Pendidikan Formal & Keagamaan | 10 |
| 3.2 Sarana Kesehatan, Posyandu & Posbindu | 11 |
| **BAB IV: TRANSPORTASI, KOMUNIKASI, EKONOMI & INDUSTRI** | 12 |
| 4.1 Prasarana Transportasi, Akses Jalan & Angkutan Umum | 13 |
| 4.2 Menara BTS, Layanan Telekomunikasi & Sinyal Internet | 14 |
| 4.3 Fasilitas Ekonomi, Mata Pencaharian & Industri Mikro/Kecil (IMK) | 15 |
| **BAB V: PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA** | 16 |
| 5.1 Aparatur Pemerintah Desa, BPD/LMK & Sistem Informasi Desa | 17 |

---

## **DAFTAR TABEL**

| No Tabel | Nama Tabel | Halaman |
| :--- | :--- | :--- |
| **Tabel 1.1** | Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW Tahun {data_year} | 4 |
| **Tabel 1.2** | Jumlah Penduduk Menurut Jenis Kelamin, Sex Ratio, dan Keluarga Pertanian Tahun {data_year} | 5 |
| **Tabel 2.1** | Penggunaan Daya Listrik, Penerangan Jalan Utama, dan Bahan Bakar Memasak Tahun {data_year} | 7 |
| **Tabel 2.2** | Sumber Air Minum Utama dan Keberadaan Mitigasi Bencana Alam Tahun {data_year} | 8 |
| **Tabel 3.1** | Rekapitulasi Ketersediaan Sarana Pendidikan Formal dan Keagamaan Tahun {data_year} | 10 |
| **Tabel 3.2** | Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu Tahun {data_year} | 11 |
| **Tabel 4.1** | Prasarana Transportasi, Jenis Permukaan Jalan, dan Angkutan Umum Tahun {data_year} | 13 |
| **Tabel 4.2** | Keberadaan Menara BTS, Operator Telekomunikasi, dan Sinyal Internet Tahun {data_year} | 14 |
| **Tabel 4.3** | Fasilitas Ekonomi Utama, Mata Pencaharian, dan Industri Mikro Kecil (IMK) Tahun {data_year} | 15 |
| **Tabel 5.1** | Aparatur Pemerintah Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa Tahun {data_year} | 17 |

---

## **PENJELASAN UMUM & KONSEP DEFINISI PODES**

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

**Tabel 1.1 Identitas Wilayah, Kawasan Hutan, dan Pembagian RT/RW Tahun {data_year}**
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

**Tabel 1.2 Jumlah Penduduk Menurut Jenis Kelamin, Sex Ratio, dan Keluarga Pertanian Tahun {data_year}**
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

**Tabel 2.1 Penggunaan Daya Listrik, Penerangan Jalan Utama, dan Bahan Bakar Memasak Tahun {data_year}**
| Indikator Energi & Utilitas | Isian Data PODES {data_year} |
| :--- | :--- |
| **Pengguna Listrik PLN** | {m.listrik_pln:,} KK |
| **Pengguna Listrik Non-PLN** | {m.listrik_non_pln} KK |
| **Bukan Pengguna Listrik** | {m.bukan_listrik} KK |
| **Penerangan Jalan Utama Desa** | {m.penerangan_jalan} |
| **Bahan Bakar Utama Memasak** | {m.bakar_masak} |

---

### **2.2 AIR MINUM & POTENSI/MITIGASI BENCANA ALAM**
Sumber air minum utama yang paling banyak digunakan masyarakat di {admin_type} {name_title} berasal dari **{m.air_minum}**. Terkait dengan potensi bencana, kejadian bencana alam dalam beberapa waktu terakhir tercatat **"{m.bencana_alam}"**, dengan ketersediaan sistem/upaya mitigasi bencana tergolong **"{m.mitigasi_bencana}"**.

**Tabel 2.2 Sumber Air Minum Utama dan Keberadaan Mitigasi Bencana Alam Tahun {data_year}**
| Indikator Lingkungan & Bencana | Isian Data PODES {data_year} |
| :--- | :--- |
| **Sumber Air Minum Utama** | {m.air_minum} |
| **Kejadian Bencana Alam** | {m.bencana_alam} |
| **Fasilitas & Upaya Mitigasi Bencana** | {m.mitigasi_bencana} |

---

## **BAB III: FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)**

### **3.1 KETERSEDIAAN SARANA PENDIDIKAN FORMAL & KEAGAMAAN**
Ketersediaan sarana pendidikan di {admin_type} {name_title} tercatat meliputi **{m.sarana_pendidikan}**.

**Tabel 3.1 Rekapitulasi Ketersediaan Sarana Pendidikan Formal dan Keagamaan Tahun {data_year}**
| Kategori Sarana Pendidikan | Rincian Ketersediaan Sarana |
| :--- | :--- |
| **Fasilitas Pendidikan Formal & Non-Formal** | {m.sarana_pendidikan} |

---

### **3.2 SARANA KESEHATAN, POSYANDU & POSBINDU**
Fasilitas pelayanan kesehatan masyarakat didukung oleh keberadaan **{m.sarana_kesehatan}**. Untuk pelayanan kesehatan balita dan lansia berbasis masyarakat, terdapat **{m.posyandu_aktif} unit Posyandu aktif** dan **{m.posbindu} unit Posbindu**.

**Tabel 3.2 Ketersediaan Sarana Kesehatan, Posyandu Aktif, dan Posbindu Tahun {data_year}**
| Indikator Pelayanan Kesehatan | Jumlah / Keterangan |
| :--- | :--- |
| **Fasilitas Kesehatan Utama** | {m.sarana_kesehatan} |
| **Posyandu Aktif (Pemeriksaan Rutin Bulanan)** | {m.posyandu_aktif} unit |
| **Posbindu (Pos Pembinaan Terpadu)** | {m.posbindu} unit |

---

## **BAB IV: TRANSPORTASI, KOMUNIKASI, EKONOMI & INDUSTRI**

### **4.1 PRASARANA TRANSPORTASI, AKSES JALAN & ANGKUTAN UMUM**
Prasarana jalan utama di {admin_type} {name_title} memiliki permukaan jalan berjenis **{m.jenis_jalan}**. Aksesibilitas jalan dapat dilalui kendaraan roda 4 atau lebih sepanjang tahun tercatat **"{m.jalan_roda4}"**, dan operasional angkutan umum tergolong **"{m.angkutan_umum}"**.

**Tabel 4.1 Prasarana Transportasi, Jenis Permukaan Jalan, dan Angkutan Umum Tahun {data_year}**
| Indikator Transportasi | Isian Data PODES {data_year} |
| :--- | :--- |
| **Prasarana Transportasi Utama** | {m.prasarana_transportasi} |
| **Jenis Permukaan Jalan Utama** | {m.jenis_jalan} |
| **Aksesibilitas Kendaraan Roda 4 atau Lebih** | {m.jalan_roda4} |
| **Keberadaan & Operasional Angkutan Umum** | {m.angkutan_umum} |

---

### **4.2 MENARA BTS, LAYANAN TELEKOMUNIKASI & SINYAL INTERNET**
Akses komunikasi seluler di {admin_type} {name_title} ditopang oleh keberadaan **{m.jumlah_bts} Menara Base Transceiver Station (BTS)**. Layanan operator seluler yang menjangkau wilayah ini tergolong **"{m.operator_seluler}"** dengan kekuatan sinyal telepon **"{m.sinyal_hp}"** dan jangkauan sinyal internet seluler sebesar **"{m.sinyal_internet}"**.

**Tabel 4.2 Keberadaan Menara BTS, Operator Telekomunikasi, dan Sinyal Internet Tahun {data_year}**
| Indikator Telekomunikasi | Isian Data PODES {data_year} |
| :--- | :--- |
| **Jumlah Menara BTS** | {m.jumlah_bts} unit |
| **Operator Layanan Seluler** | {m.operator_seluler} |
| **Kekuatan Sinyal Telepon Seluler** | {m.sinyal_hp} |
| **Jaringan & Sinyal Internet Seluler** | {m.sinyal_internet} |

---

### **4.3 FASILITAS EKONOMI, MATA PENCAHARIAN & INDUSTRI MIKRO KECIL (IMK)**
Sebagian besar penduduk di {admin_type} {name_title} menggantungkan mata pencaharian utama pada sektor **{m.sumber_penghasilan_utama} ({m.subsektor_utama})**. Aktivitas perekonomian didukung ketersediaan sarana berupa **{m.sarana_ekonomi}**, serta kegiatan sektor pengolahan sebanyak **{m.jumlah_imk} unit Industri Mikro dan Kecil (IMK)**.

**Tabel 4.3 Fasilitas Ekonomi Utama, Mata Pencaharian, dan Industri Mikro Kecil (IMK) Tahun {data_year}**
| Indikator Ekonomi & Industri | Isian Data PODES {data_year} |
| :--- | :--- |
| **Mata Pencaharian Utama Penduduk** | {m.sumber_penghasilan_utama} ({m.subsektor_utama}) |
| **Fasilitas Ekonomi Utama** | {m.sarana_ekonomi} |
| **Jumlah Industri Mikro dan Kecil (IMK)** | {m.jumlah_imk} unit usaha |

---

## **BAB V: PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA**

### **5.1 APARATUR PEMERINTAH DESA, BPD/LMK & SISTEM INFORMASI DESA**
Roda pemerintahan {admin_type} {name_title} dijalankan oleh **{m.aparatur_pemdes} orang aparatur pemerintah desa/kelurahan**. Keberadaan badan perwakilan (BPD/LMK) tercatat **"{m.keberadaan_bpd}"** dengan frekuensi musyawarah desa sebanyak **{m.musyawarah_desa} kali**. Pemanfaatan teknologi informasi diwujudkan melalui Sistem Informasi Desa (SID) bernomenklatur **"{m.sistem_informasi_desa}"**, serta ketersediaan SPPG tercatat **"{m.jumlah_sppg}"**.

**Tabel 5.1 Aparatur Pemerintah Desa, Keberadaan BPD/LMK, dan Sistem Informasi Desa Tahun {data_year}**
| Indikator Pemerintahan & Kelembagaan | Isian Data PODES {data_year} |
| :--- | :--- |
| **Jumlah Aparatur Pemerintah Desa/Kelurahan** | {m.aparatur_pemdes} orang |
| **Keberadaan BPD / LMK** | {m.keberadaan_bpd} |
| **Frekuensi Musyawarah Desa dalam 1 Tahun** | {m.musyawarah_desa} kali |
| **Keberadaan Sistem Informasi Desa (SID)** | {m.sistem_informasi_desa} |
| **Ketersediaan SPPG** | {m.jumlah_sppg} |
"""

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-potensi-{name_kebab}-{year}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Markdown PODES file written: {out_path}")
    return out_path
