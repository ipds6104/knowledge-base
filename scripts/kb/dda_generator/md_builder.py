"""BPS Markdown Document Builder Module for DDA Generator."""

from pathlib import Path


def build_desa_markdown(config: dict, metrics: dict) -> Path:
    """Menghasilkan berkas Markdown baku 5 Bab publikasi Desa/Kelurahan Dalam Angka."""
    name_title = config["name_title"]
    name_upper = config["name_upper"]
    name_kebab = config["name_kebab"]
    admin_type = config.get("admin_type", "Desa")
    admin_upper = admin_type.upper()
    admin_type_en = config.get("admin_type_en", "Village")
    kecamatan = config["kecamatan"]
    kabupaten = config["kabupaten"]
    provinsi = config["provinsi"]
    pub_no = config.get("pub_no", "61040.2026.001")
    year = config.get("year", 2026)
    kades_title = config.get("kades_title", f"Kepala Desa {name_title}")
    kades_name = config.get("kades_name", f"Kepala Desa {name_title}")
    pemberita = config.get("pemberita", "Tim Pembina Desa Cantik BPS Kabupaten Mempawah")

    rows = metrics["rows"]
    t_pop = metrics["tot_pop"]
    t_l = metrics["tot_l"]
    t_p = metrics["tot_p"]
    t_sr = metrics["tot_sr"]
    t_kk = metrics["tot_kk"]
    t_art = metrics["tot_art"]
    t_lansia = metrics["tot_lansia"]
    t_b1 = metrics["tot_b1"]
    t_b2 = metrics["tot_b2"]
    t_pendatang = metrics["tot_pendatang"]
    t_lahir = metrics["tot_lahir"]
    t_mati = metrics["tot_mati"]
    t_putus = metrics["tot_putus"]
    t_tk = metrics["tot_tk"]
    t_sd = metrics["tot_sd"]
    t_smp = metrics["tot_smp"]
    t_sma = metrics["tot_sma"]
    t_sarjana = metrics["tot_sarjana"]
    t_ktp = metrics["tot_ktp"]
    t_ktp_pct = metrics["tot_ktp_pct"]
    t_pkh = metrics["tot_pkh"]
    t_bpnt = metrics["tot_bpnt"]
    t_bst = metrics["tot_bst"]
    t_blt = metrics["tot_blt"]
    t_bansos = metrics["tot_bansos"]
    t_bumbung = metrics["tot_bumbung"]
    t_kepadatan = metrics["tot_kepadatan"]

    caps = pub_data.capabilities

    if caps.has_employment:
        md_bab3_toc = "| **BAB III: KELOMPOK UMUR, KETENAGAKERJAAN & UMKM** | 11 |\n| 3.1 Penduduk Usia Kerja Bekerja, UMKM, & BPJS | 11 |"
        md_bab3_lot = "| **Tabel 3.1** | Jumlah Penduduk Usia Kerja Bekerja, Rumah Tangga UMKM, dan Peserta BPJS per RT | 11 |"
        md_bab3_body = f"""## **BAB III: KELOMPOK UMUR, KETENAGAKERJAAN & UMKM**

### **3.1 PENDUDUK USIA KERJA BEKERJA, RUMAH TANGGA UMKM, & PESERTA BPJS**
Pendataan CAPI Kelurahan Cantik mencatat sebanyak **{metrics['tot_bekerja']:,} jiwa** penduduk usia kerja yang bekerja, **{metrics['tot_umkm']:,} rumah tangga** pengelola UMKM, serta **{metrics['tot_bpjs']:,} jiwa** peserta jaminan kesehatan BPJS.

**Tabel 3.1 Jumlah Penduduk Usia Kerja Bekerja, Rumah Tangga UMKM, dan Peserta BPJS per RT**
| Nama RT | Total Penduduk | Usia Kerja Bekerja | Rumah Tangga UMKM | Peserta BPJS |
| :--- | :---: | :---: | :---: | :---: |
"""
        for r in rows:
            md_bab3_body += f"| **{r['rt_name']}** | {r['tot']} | {r['bekerja']} | {r['umkm']} | {r['bpjs']} |\n"
        md_bab3_body += f"| **{admin_upper} {name_upper}** | **{t_pop}** | **{metrics['tot_bekerja']}** | **{metrics['tot_umkm']}** | **{metrics['tot_bpjs']}** |\n"

    elif caps.has_building_materials:
        md_bab3_toc = "| **BAB III: KUALITAS BANGUNAN & SANITASI** | 11 |\n| 3.1 Bahan Utama Dinding, Atap, & Sanitasi BAB | 11 |"
        md_bab3_lot = "| **Tabel 3.1** | Jumlah Bangunan Menurut Bahan Utama Dinding, Atap, dan Sanitasi BAB per RT | 11 |"
        md_bab3_body = f"""## **BAB III: KUALITAS BANGUNAN & INFRASTRUKTUR SANITASI**

### **3.1 BAHAN UTAMA DINDING, ATAP, & SANITASI BAB**
Pendataan CAPI Desa Cantik mencatat sebanyak **{metrics['tot_dinding_tembok']:,} bangunan** berdinding tembok/kayu, **{metrics['tot_atap_seng_genteng']:,} bangunan** beratap seng/genteng, dan **{metrics['tot_bab_sendiri']:,} keluarga** memiliki fasilitas sanitasi BAB sendiri.

**Tabel 3.1 Jumlah Bangunan Menurut Bahan Utama Dinding, Atap, dan Sanitasi BAB per RT**
| Nama RT | Bumbung Rumah | Dinding Tembok | Atap Seng/Genteng | Sanitasi BAB Sendiri |
| :--- | :---: | :---: | :---: | :---: |
"""
        for r in rows:
            md_bab3_body += f"| **{r['rt_name']}** | {r['bumbung']} | {r['dinding_tembok']} | {r['atap_seng_genteng']} | {r['bab_sendiri']} |\n"
        md_bab3_body += f"| **{admin_upper} {name_upper}** | **{t_bumbung}** | **{metrics['tot_dinding_tembok']}** | **{metrics['tot_atap_seng_genteng']}** | **{metrics['tot_bab_sendiri']}** |\n"

    else:
        md_bab3_toc = "| **BAB III: PENDIDIKAN & ADMINISTRASI KEPENDUDUKAN** | 11 |\n| 3.1 Penduduk Menurut Jenjang Pendidikan | 11 |\n| 3.2 Kepemilikan KTP-el | 12 |"
        md_bab3_lot = "| **Tabel 3.1** | Jumlah Penduduk Menurut Jenjang Pendidikan per RT | 11 |\n| **Tabel 3.2** | Penduduk Memiliki KTP-el dan Persentase Kepemilikan per RT | 12 |"
        md_bab3_body = f"""## **BAB III: PENDIDIKAN & ADMINISTRASI KEPENDUDUKAN**

### **3.1 PENDUDUK MENURUT JENJANG PENDIDIKAN**
Sebaran penduduk menurut jenjang pendidikan mencakup: TK ({t_tk}), SD ({t_sd}), SMP ({t_smp}), SMA ({t_sma}), dan Sarjana/Diploma ({t_sarjana}).

**Tabel 3.1 Jumlah Penduduk Menurut Jenjang Pendidikan per RT**
| Nama RT | TK/PAUD | SD/MI | SMP/MTs | SMA/MA/SMK | Sarjana/Diploma |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
        for r in rows:
            md_bab3_body += f"| **{r['rt_name']}** | {r['tk']} | {r['sd']} | {r['smp']} | {r['sma']} | {r['sarjana']} |\n"
        md_bab3_body += f"| **{admin_upper} {name_upper}** | **{t_tk}** | **{t_sd}** | **{t_smp}** | **{t_sma}** | **{t_sarjana}** |\n\n---\n\n### **3.2 KEPEMILIKAN KTP-EL**\nSebanyak **{t_ktp:,} penduduk** di {admin_type} {name_title} telah memiliki KTP-el ({t_ktp_pct:.2f}% dari total penduduk).\n\n**Tabel 3.2 Penduduk Memiliki KTP-el per RT**\n| Nama RT | Total Penduduk | Memiliki KTP-el | Persentase (%) |\n| :--- | :---: | :---: | :---: |\n"
        for r in rows:
            md_bab3_body += f"| **{r['rt_name']}** | {r['tot']} | {r['ktp']} | {r['ktp_pct']:.2f}% |\n"
        md_bab3_body += f"| **{admin_upper} {name_upper}** | **{t_pop}** | **{t_ktp}** | **{t_ktp_pct:.2f}%** |\n"

    md = f"""# **{admin_type} {name_title} Dalam Angka {year}**

Ukuran Buku : 21 cm x 29,7 cm  
Jumlah Halaman : iv + 16 halaman  

---

## **KATA PENGANTAR**

{md_preface_p1}

{md_preface_p2} Diharapkan publikasi ini dapat menjadi rujukan utama bagi Pemerintah {admin_type} dan pemangku kepentingan dalam perencanaan pembangunan berbasis bukti (*evidence-based policy*).

Kepada semua pihak yang telah membantu terwujudnya publikasi ini, khususnya para Agen Statistik {admin_type} dan Ketua RT se-{admin_type} {name_title}, kami sampaikan terima kasih dan penghargaan yang setinggi-tingginya.

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
| **PENJELASAN TEKNIS PENDATAAN** | 1 |
| **KONSEP DAN DEFINISI** | 2 |
| **BAB I: GEOGRAFIS & ADMINISTRASI** | 3 |
| 1.1 Kondisi Geografis & Batas Wilayah | 3 |
| 1.2 Pembagian Wilayah RT & Ketua RT | 3 |
| **BAB II: KEPENDUDUKAN & KELOMPOK RENTAN** | 5 |
| 2.1 Penduduk Menurut Jenis Kelamin & Sex Ratio | 5 |
| 2.2 Sebaran Penduduk per RT | 5 |
| 2.3 Jumlah Kartu Keluarga (KK) & Rata-rata ART | 7 |
| 2.4 Penduduk Lansia, Bayi, Balita & Pendatang | 8 |
| 2.5 Dinamika Kelahiran & Kematian | 9 |
| 2.6 Anak Putus Sekolah | 10 |
{md_bab3_toc}
| **BAB IV: KESEJAHTERAAN MASYARAKAT & BANTUAN SOSIAL** | 13 |
| 4.1 Sebaran Penerima PKH, BPNT, BST, & BLT | 13 |
| **BAB V: PERUMAHAN & INFRASTRUKTUR** | 14 |
| 5.1 Jumlah Bumbung Rumah & Kepadatan Hunian | 14 |

---

## **DAFTAR TABEL**

| No Tabel | Nama Tabel | Halaman |
| :--- | :--- | :--- |
| **Tabel 1.1** | Batas Wilayah Administrasi {admin_type} {name_title} | 3 |
| **Tabel 1.2** | Daftar Nama Ketua RT & Agen Statistik {admin_type} {name_title} | 3 |
| **Tabel 2.1** | Jumlah Penduduk {admin_type} {name_title} Menurut Wilayah RT dan Jenis Kelamin | 5 |
| **Tabel 2.2** | Jumlah Kartu Keluarga (KK) dan Rata-rata Anggota Rumah Tangga (ART) per RT | 7 |
| **Tabel 2.3** | Sebaran Penduduk Lansia, Bayi (0-1 Th), Balita (2-5 Th), dan Pendatang per RT | 8 |
| **Tabel 2.4** | Angka Kelahiran Bayi dan Kematian Penduduk per RT Tahun {year} | 9 |
| **Tabel 2.5** | Jumlah Anak Putus Sekolah (Usia 7-18 Tahun) per RT | 10 |
{md_bab3_lot}
| **Tabel 4.1** | Sebaran Keluarga Penerima Bantuan Sosial (PKH, BPNT, BST, BLT) per RT | 13 |
| **Tabel 5.1** | Jumlah Bumbung Rumah dan Kepadatan Hunian (Jiwa/Rumah) per RT | 14 |

---

## **PENJELASAN TEKNIS PENDATAAN**

- **A. Ruang Lingkup**: Pendataan mencakup seluruh wilayah administrasi {admin_type} {name_title}, Kecamatan {kecamatan}, Kabupaten {kabupaten}, Provinsi {provinsi}. Pendataan dilakukan pada {len(rows)} Rukun Tetangga (RT).
- **B. Pelaksanaan & Organisasi**: Pendataan dilaksanakan menggunakan metode *Computer-Assisted Personal Interviewing* (CAPI) berbasis aplikasi mobile **AppSheet**. Tim Pembina Desa Cantik BPS Kabupaten Mempawah bertindak sebagai supervisor & pengolah data, didampingi oleh Agen Statistik {admin_type} dan Ketua RT.
- **C. Referensi Waktu**: Data dikumpulkan berdasarkan kondisi objektif di lapangan pada saat pencacahan bulan Juni–Juli {year}.

---

## **KONSEP DAN DEFINISI**

- **Bumbung Rumah (Bangunan Tempat Tinggal)**: Bangunan fisik beratap dan berdinding yang digunakan secara aktif sebagai tempat tinggal rumah tangga.
- **Kartu Keluarga (KK)**: Unit rumah tangga/keluarga yang terdaftar atau berdomisili di wilayah RT terkait.
- **Rata-rata Anggota Rumah Tangga (ART)**: Rata-rata banyaknya anggota keluarga yang menghuni satu KK.
- **Sex Ratio (Rasio Jenis Kelamin)**: Perbandingan jumlah penduduk laki-laki dengan 100 penduduk perempuan.
- **Lansia**: Penduduk berusia 60 tahun ke atas.
- **Putus Sekolah**: Anak usia sekolah (7–18 tahun) yang tidak sedang menempuh pendidikan formal.
- **Kepadatan Hunian**: Rata-rata jumlah jiwa yang menempati satu bumbung rumah.

---

## **BAB I: GEOGRAFIS & ADMINISTRASI**

### **1.1 KONDISI GEOGRAFIS**
{admin_type} {name_title} terletak di Kecamatan {kecamatan}, Kabupaten {kabupaten}, Provinsi {provinsi}. Wilayah ini memiliki batas wilayah administrasi sebagai berikut:

**Tabel 1.1 Batas Wilayah Administrasi {admin_type} {name_title}**
| Batas Wilayah | Desa / Kelurahan / Laut | Kecamatan |
| :--- | :--- | :--- |
| **Sebelah Utara** | {config.get('north', '-')} | {kecamatan} |
| **Sebelah Selatan** | {config.get('south', '-')} | - |
| **Sebelah Timur** | {config.get('east', '-')} | {kecamatan} |
| **Sebelah Barat** | {config.get('west', '-')} | {kecamatan} |

---

### **1.2 PEMBAGIAN WILAYAH RT & NAMA KETUA RT**

**Tabel 1.2 Daftar Nama Ketua RT & Agen Statistik {admin_type} {name_title}**
| Nama RT | Ketua RT | Agen Statistik {admin_type} | Status |
| :--- | :--- | :--- | :--- |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['ketua_rt']} | {r['petugas']} | {r['status']} |\n"

    md += f"""
---

## **BAB II: KEPENDUDUKAN & KELOMPOK RENTAN**

### **2.1 GAMBARAN UMUM DEMOGRAFI**
Berdasarkan hasil pendataan Desa Cantik {year}, jumlah penduduk {admin_type} {name_title} tercatat sebanyak **{t_pop:,} jiwa**, terdiri dari **{t_l:,} jiwa laki-laki** dan **{t_p:,} jiwa perempuan**. Nilai *Sex Ratio* sebesar **{t_sr:.2f}**.

**Tabel 2.1 Jumlah Penduduk {admin_type} {name_title} Menurut Wilayah RT dan Jenis Kelamin**
| Nama RT | Laki-Laki | Perempuan | Total Penduduk | Sex Ratio |
| :--- | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['l']} | {r['p']} | **{r['tot']}** | {r['sr']:.2f} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_l}** | **{t_p}** | **{t_pop}** | **{t_sr:.2f}** |

---

### **2.2 JUMLAH KARTU KELUARGA (KK) & RATA-RATA ART**
Total Kartu Keluarga (KK) di {admin_type} {name_title} berjumlah **{t_kk:,} KK**, dengan rata-rata anggota rumah tangga sebesar **{t_art:.2f} jiwa per KK**.

**Tabel 2.2 Jumlah Kartu Keluarga (KK) dan Rata-rata Anggota Rumah Tangga (ART) per RT**
| Nama RT | Total Penduduk | Jumlah KK | Rata-rata ART |
| :--- | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tot']} | {r['kk']} | {r['art']:.2f} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_pop}** | **{t_kk}** | **{t_art:.2f}** |

---

### **2.3 PENDUDUK LANSIA, BAYI, BALITA & PENDATANG**
Jumlah penduduk lansia (60 tahun ke atas) tercatat sebanyak **{t_lansia} jiwa**. Jumlah anak usia bayi (0-1 tahun) sebanyak **{t_b1} anak**, balita (2-5 tahun) sebanyak **{t_b2} anak**, dan pendatang sebanyak **{t_pendatang} jiwa**.

**Tabel 2.3 Sebaran Penduduk Lansia, Bayi (0-1 Th), Balita (2-5 Th), dan Pendatang per RT**
| Nama RT | Lansia (>=60 Th) | Bayi (0-1 Th) | Balita (2-5 Th) | Pendatang |
| :--- | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['lansia']} | {r['b1']} | {r['b2']} | {r['pendatang']} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_lansia}** | **{t_b1}** | **{t_b2}** | **{t_pendatang}** |

---

### **2.4 DINAMIKA KELAHIRAN & KEMATIAN**
Dalam 1 tahun terakhir, tercatat **{t_lahir} kelahiran bayi** dan **{t_mati} kejadian kematian** di {admin_type} {name_title}.

**Tabel 2.4 Angka Kelahiran Bayi dan Kematian Penduduk per RT Tahun {year}**
| Nama RT | Kelahiran Bayi | Kematian |
| :--- | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['lahir']} | {r['mati']} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_lahir}** | **{t_mati}** |

---

### **2.5 ANAK PUTUS SEKOLAH**
Terdapat **{t_putus} anak** usia 7–18 tahun yang teridentifikasi putus sekolah di wilayah {admin_type} {name_title}.

**Tabel 2.5 Jumlah Anak Putus Sekolah (Usia 7-18 Tahun) per RT**
| Nama RT | Anak Putus Sekolah |
| :--- | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['putus']} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_putus}** |

---

{md_bab3_body}

---

## **BAB IV: KESEJAHTERAAN MASYARAKAT & BANTUAN SOSIAL**

### **4.1 SEBARAN PENERIMA BANTUAN SOSIAL**
Pemerintah menyalurkan bantuan sosial meliputi: PKH ({t_pkh}), BPNT ({t_bpnt}), BST ({t_bst}), dan BLT ({t_blt}).

**Tabel 4.1 Sebaran Keluarga Penerima Bantuan Sosial per RT**
| Nama RT | Penerima PKH | Penerima BPNT | Penerima BST | Penerima BLT | Total Penerima |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['pkh']} | {r['bpnt']} | {r['bst']} | {r['blt']} | **{r['tot_bansos']}** |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_pkh}** | **{t_bpnt}** | **{t_bst}** | **{t_blt}** | **{t_bansos}** |

---

## **BAB V: PERUMAHAN & INFRASTRUKTUR**

### **5.1 JUMLAH BUMBUNG RUMAH & KEPADATAN HUNIAN**
Total bumbung rumah di {admin_type} {name_title} sebanyak **{t_bumbung:,} unit**, dengan rata-rata kepadatan hunian **{t_kepadatan:.2f} jiwa per rumah**.

**Tabel 5.1 Jumlah Bumbung Rumah dan Kepadatan Hunian (Jiwa/Rumah) per RT**
| Nama RT | Total Penduduk | Bumbung Rumah | Kepadatan Hunian (Jiwa/Rumah) |
| :--- | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tot']} | {r['bumbung']} | {r['kepadatan']:.2f} |\n"

    md += f"""| **{admin_upper} {name_upper}** | **{t_pop}** | **{t_bumbung}** | **{t_kepadatan:.2f}** |

---

# **MENCERDASKAN BANGSA DENGAN DATA STATISTIK DESA**
"""

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = "publikasi-kelurahan" if config.get("is_kelurahan") else "publikasi-desa"
    out_path = out_dir / f"{prefix}-{name_kebab}-dalam-angka-{year}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Markdown file written: {out_path}")
    return out_path
