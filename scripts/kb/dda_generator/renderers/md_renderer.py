"""BPS Markdown Document Renderer for DDA Generator Engine.
Accepts pure DesaPublicationData DTO contract.
"""

from pathlib import Path
from ..schemas import DesaPublicationData


def render_desa_md(pub_data: DesaPublicationData) -> Path:
    """Menghasilkan berkas Markdown baku 5 Bab publikasi Desa Dalam Angka dari DesaPublicationData DTO."""
    config = pub_data.config
    metrics = pub_data.metrics

    name_title = config["name_title"]
    name_upper = config["name_upper"]
    name_kebab = config["name_kebab"]
    kecamatan = config["kecamatan"]
    kabupaten = config["kabupaten"]
    provinsi = config["provinsi"]
    pub_no = config.get("pub_no", "61040.2026.001")
    year = config.get("year", 2026)
    kades_title = config.get("kades_title", f"Kepala Desa {name_title}")
    kades_name = config.get("kades_name", f"Kepala Desa {name_title}")

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
    has_fas = caps.has_public_facilities and bool(metrics.get("fasilitas"))
    fas_m = metrics.get("fasilitas", {})
    fas_rows = fas_m.get("rows", [])

    toc_fas = ""
    tbl_fas = ""
    if has_fas:
        toc_fas = f"| 5.2 Sebaran Sarana Peribadatan, Pendidikan & Kesehatan | 15 |\n| 5.3 Kondisi Bangunan & Akses Infrastruktur Desa | 16 |\n"
        tbl_fas = f"| **Tabel 12** | Sebaran Sarana Peribadatan, Pendidikan, dan Kesehatan per RT | 15 |\n| **Tabel 13** | Rekapitulasi Kondisi Bangunan dan Akses Infrastruktur Desa per RT | 16 |\n"

    md = f"""# **Desa {name_title} Dalam Angka {year}**

Nomor Publikasi : {pub_no}  
Ukuran Buku : 21 cm x 29,7 cm  
Jumlah Halaman : iv + 16 halaman  

---

## **KATA PENGANTAR**

Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi **"Desa {name_title} Dalam Angka {year}"** ini dapat diselesaikan dengan baik. Publikasi ini merupakan hasil kompilasi data potensi desa berbasis Rukun Tetangga (RT) yang dikumpulkan melalui kegiatan Desa Cantik (Desa Cinta Statistik) BPS Kabupaten Mempawah bekerjasama dengan Pemerintah Desa {name_title}.

Data yang disajikan mencakup kondisi demografi kependudukan, tingkat pendidikan, kepemilikan administrasi KTP-el, penerima bantuan sosial, hingga kelayakan bangunan dan perumahan di tingkat RT. Diharapkan publikasi ini dapat menjadi rujukan utama bagi Pemerintah Desa dan pemangku kepentingan dalam perencanaan pembangunan desa berbasis bukti (*evidence-based policy*).

Kepada semua pihak yang telah membantu terwujudnya publikasi ini, khususnya para Agen Statistik Desa dan Ketua RT se-Desa {name_title}, kami sampaikan terima kasih dan penghargaan yang setinggi-tingginya.

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
| **BAB III: PENDIDIKAN & ADMINISTRASI KEPENDUDUKAN** | 11 |
| 3.1 Penduduk Menurut Jenjang Pendidikan | 11 |
| 3.2 Kepemilikan KTP-el | 12 |
| **BAB IV: KESEJAHTERAAN MASYARAKAT & BANTUAN SOSIAL** | 13 |
| 4.1 Sebaran Penerima PKH, BPNT, BST, & BLT | 13 |
| **BAB V: PERUMAHAN & INFRASTRUKTUR** | 14 |
| 5.1 Jumlah Bumbung Rumah & Kepadatan Hunian | 14 |
{toc_fas}
---

## **DAFTAR TABEL**

| No Tabel | Nama Tabel | Halaman |
| :--- | :--- | :--- |
| **Tabel 1** | Batas Wilayah Administrasi Desa {name_title} | 3 |
| **Tabel 2** | Daftar Nama Ketua RT & Agen Statistik Desa {name_title} | 3 |
| **Tabel 3** | Jumlah Penduduk Desa {name_title} Menurut Wilayah RT dan Jenis Kelamin | 5 |
| **Tabel 4** | Jumlah Kartu Keluarga (KK) dan Rata-rata Anggota Rumah Tangga (ART) per RT | 7 |
| **Tabel 5** | Sebaran Penduduk Lansia, Bayi (0-1 Th), Balita (2-5 Th), dan Pendatang per RT | 8 |
| **Tabel 6** | Angka Kelahiran Bayi dan Kematian Penduduk per RT Tahun {year} | 9 |
| **Tabel 7** | Jumlah Anak Putus Sekolah (Usia 7-18 Tahun) per RT | 10 |
| **Tabel 8** | Jumlah Penduduk Menurut Jenjang Pendidikan per RT | 11 |
| **Tabel 9** | Penduduk Memiliki KTP-el dan Persentase Kepemilikan per RT | 12 |
| **Tabel 10** | Sebaran Keluarga Penerima Bantuan Sosial (PKH, BPNT, BST, BLT) per RT | 13 |
| **Tabel 11** | Jumlah Bumbung Rumah dan Kepadatan Hunian (Jiwa/Rumah) per RT | 14 |
{tbl_fas}
---

## **PENJELASAN TEKNIS PENDATAAN**

- **A. Ruang Lingkup**: Pendataan mencakup seluruh wilayah administrasi Desa {name_title}, Kecamatan {kecamatan}, Kabupaten {kabupaten}, Provinsi {provinsi}. Pendataan dilakukan pada {len(rows)} Rukun Tetangga (RT).
- **B. Pelaksanaan & Organisasi**: Pendataan dilaksanakan menggunakan metode *Computer-Assisted Personal Interviewing* (CAPI) berbasis aplikasi mobile **AppSheet**. Tim Pembina Desa Cantik BPS Kabupaten Mempawah bertindak sebagai supervisor & pengolah data, didampingi oleh Agen Statistik Desa dan Ketua RT.
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
- **Fasilitas Umum**: Sarana dan prasarana fisik yang digunakan untuk kepentingan bersama di desa.

---

## **BAB I: GEOGRAFIS & ADMINISTRASI**

### **1.1 KONDISI GEOGRAFIS**
Desa {name_title} terletak di Kecamatan {kecamatan}, Kabupaten {kabupaten}, Provinsi {provinsi}. Wilayah ini memiliki batas wilayah administrasi sebagai berikut:

**Tabel 1. Batas Wilayah Administrasi Desa {name_title}**
| Batas Wilayah | Desa / Kelurahan / Laut | Kecamatan |
| :--- | :--- | :--- |
| **Sebelah Utara** | {config.get('north', '-')} | {kecamatan} |
| **Sebelah Selatan** | {config.get('south', '-')} | - |
| **Sebelah Timur** | {config.get('east', '-')} | {kecamatan} |
| **Sebelah Barat** | {config.get('west', '-')} | {kecamatan} |

---

### **1.2 PEMBAGIAN WILAYAH RT & NAMA KETUA RT**

**Tabel 2. Daftar Nama Ketua RT & Agen Statistik Desa {name_title}**
| Nama RT | Ketua RT | Agen Statistik Desa | Status |
| :--- | :--- | :--- | :--- |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['ketua_rt']} | {r['petugas']} | {r['status']} |\n"

    md += f"""
---

## **BAB II: KEPENDUDUKAN & KELOMPOK RENTAN**

### **2.1 GAMBARAN UMUM DEMOGRAFI**
Berdasarkan hasil pendataan Desa Cantik {year}, jumlah penduduk Desa {name_title} tercatat sebanyak **{t_pop:,} jiwa**, terdiri dari **{t_l:,} jiwa laki-laki** dan **{t_p:,} jiwa perempuan**. Nilai *Sex Ratio* sebesar **{t_sr:.2f}**.

**Tabel 3. Jumlah Penduduk Desa {name_title} Menurut Wilayah RT dan Jenis Kelamin**
| Nama RT | Laki-Laki | Perempuan | Total Penduduk | Sex Ratio |
| :--- | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['l']} | {r['p']} | **{r['tot']}** | {r['sr']:.2f} |\n"

    md += f"""| **DESA {name_upper}** | **{t_l}** | **{t_p}** | **{t_pop}** | **{t_sr:.2f}** |

---

### **2.2 JUMLAH KARTU KELUARGA (KK) & RATA-RATA ART**
Total Kartu Keluarga (KK) di Desa {name_title} berjumlah **{t_kk:,} KK**, dengan rata-rata anggota rumah tangga sebesar **{t_art:.2f} jiwa per KK**.

**Tabel 4. Jumlah Kartu Keluarga (KK) dan Rata-rata Anggota Rumah Tangga (ART) per RT**
| Nama RT | Total Penduduk | Jumlah KK | Rata-rata ART |
| :--- | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tot']} | {r['kk']} | {r['art']:.2f} |\n"

    md += f"""| **DESA {name_upper}** | **{t_pop}** | **{t_kk}** | **{t_art:.2f}** |

---

### **2.3 PENDUDUK LANSIA, BAYI, BALITA & PENDATANG**
Jumlah penduduk lansia (60 tahun ke atas) tercatat sebanyak **{t_lansia} jiwa**. Jumlah anak usia bayi (0-1 tahun) sebanyak **{t_b1} anak**, balita (2-5 tahun) sebanyak **{t_b2} anak**, dan pendatang sebanyak **{t_pendatang} jiwa**.

**Tabel 5. Sebaran Penduduk Lansia, Bayi (0-1 Th), Balita (2-5 Th), dan Pendatang per RT**
| Nama RT | Lansia (>=60 Th) | Bayi (0-1 Th) | Balita (2-5 Th) | Pendatang |
| :--- | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['lansia']} | {r['b1']} | {r['b2']} | {r['pendatang']} |\n"

    md += f"""| **DESA {name_upper}** | **{t_lansia}** | **{t_b1}** | **{t_b2}** | **{t_pendatang}** |

---

### **2.4 DINAMIKA KELAHIRAN & KEMATIAN**
Dalam 1 tahun terakhir, tercatat **{t_lahir} kelahiran bayi** dan **{t_mati} kejadian kematian** di Desa {name_title}.

**Tabel 6. Angka Kelahiran Bayi dan Kematian Penduduk per RT Tahun {year}**
| Nama RT | Kelahiran Bayi | Kematian |
| :--- | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['lahir']} | {r['mati']} |\n"

    md += f"""| **DESA {name_upper}** | **{t_lahir}** | **{t_mati}** |

---

### **2.5 ANAK PUTUS SEKOLAH**
Terdapat **{t_putus} anak** usia 7–18 tahun yang teridentifikasi putus sekolah di wilayah Desa {name_title}.

**Tabel 7. Jumlah Anak Putus Sekolah (Usia 7-18 Tahun) per RT**
| Nama RT | Anak Putus Sekolah |
| :--- | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['putus']} |\n"

    md += f"""| **DESA {name_upper}** | **{t_putus}** |

---

## **BAB III: PENDIDIKAN & ADMINISTRASI KEPENDUDUKAN**

### **3.1 PENDUDUK MENURUT JENJANG PENDIDIKAN**
Sebaran penduduk menurut jenjang pendidikan mencakup: TK ({t_tk}), SD ({t_sd}), SMP ({t_smp}), SMA ({t_sma}), dan Sarjana/Diploma ({t_sarjana}).

**Tabel 8. Jumlah Penduduk Menurut Jenjang Pendidikan per RT**
| Nama RT | TK/PAUD | SD/MI | SMP/MTs | SMA/MA/SMK | Sarjana/Diploma |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tk']} | {r['sd']} | {r['smp']} | {r['sma']} | {r['sarjana']} |\n"

    md += f"""| **DESA {name_upper}** | **{t_tk}** | **{t_sd}** | **{t_smp}** | **{t_sma}** | **{t_sarjana}** |

---

### **3.2 KEPEMILIKAN KTP-EL**
Sebanyak **{t_ktp:,} penduduk** di Desa {name_title} telah memiliki KTP-el ({t_ktp_pct:.2f}% dari total penduduk).

**Tabel 9. Penduduk Memiliki KTP-el per RT**
| Nama RT | Total Penduduk | Memiliki KTP-el | Persentase (%) |
| :--- | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tot']} | {r['ktp']} | {r['ktp_pct']:.2f}% |\n"

    md += f"""| **DESA {name_upper}** | **{t_pop}** | **{t_ktp}** | **{t_ktp_pct:.2f}%** |

---

## **BAB IV: KESEJAHTERAAN MASYARAKAT & BANTUAN SOSIAL**

### **4.1 SEBARAN PENERIMA BANTUAN SOSIAL**
Pemerintah menyalurkan bantuan sosial meliputi: PKH ({t_pkh}), BPNT ({t_bpnt}), BST ({t_bst}), dan BLT ({t_blt}).

**Tabel 10. Sebaran Keluarga Penerima Bantuan Sosial per RT**
| Nama RT | Penerima PKH | Penerima BPNT | Penerima BST | Penerima BLT | Total Penerima |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['pkh']} | {r['bpnt']} | {r['bst']} | {r['blt']} | **{r['tot_bansos']}** |\n"

    md += f"""| **DESA {name_upper}** | **{t_pkh}** | **{t_bpnt}** | **{t_bst}** | **{t_blt}** | **{t_bansos}** |

---

## **BAB V: PERUMAHAN & INFRASTRUKTUR**

### **5.1 JUMLAH BUMBUNG RUMAH & KEPADATAN HUNIAN**
Total bumbung rumah di Desa {name_title} sebanyak **{t_bumbung:,} unit**, dengan rata-rata kepadatan hunian **{t_kepadatan:.2f} jiwa per rumah**.

**Tabel 11. Jumlah Bumbung Rumah dan Kepadatan Hunian (Jiwa/Rumah) per RT**
| Nama RT | Total Penduduk | Bumbung Rumah | Kepadatan Hunian (Jiwa/Rumah) |
| :--- | :---: | :---: | :---: |
"""

    for r in rows:
        md += f"| **{r['rt_name']}** | {r['tot']} | {r['bumbung']} | {r['kepadatan']:.2f} |\n"

    md += f"""| **DESA {name_upper}** | **{t_pop}** | **{t_bumbung}** | **{t_kepadatan:.2f}** |
"""

    if has_fas:
        ibadah_details = []
        if fas_m.get('tot_masjid', 0) > 0: ibadah_details.append(f"{fas_m['tot_masjid']} Masjid")
        if fas_m.get('tot_musholla', 0) > 0: ibadah_details.append(f"{fas_m['tot_musholla']} Surau/Musholla")
        if fas_m.get('tot_vihara', 0) > 0: ibadah_details.append(f"{fas_m['tot_vihara']} Vihara/Klenteng")
        if fas_m.get('tot_gereja', 0) > 0: ibadah_details.append(f"{fas_m['tot_gereja']} Gereja")
        ibadah_str = ", ".join(ibadah_details) if ibadah_details else "sarana peribadatan"

        edu_details = []
        if fas_m.get('tot_paud_tk', 0) > 0: edu_details.append(f"{fas_m['tot_paud_tk']} PAUD/TK")
        if fas_m.get('tot_sd_mi', 0) > 0: edu_details.append(f"{fas_m['tot_sd_mi']} SD/MI")
        if fas_m.get('tot_smp_mts', 0) > 0: edu_details.append(f"{fas_m['tot_smp_mts']} SMP/MTs")
        if fas_m.get('tot_sma_ma', 0) > 0: edu_details.append(f"{fas_m['tot_sma_ma']} SMA/SMK/MA")
        if fas_m.get('tot_ponpes', 0) > 0: edu_details.append(f"{fas_m['tot_ponpes']} Pondok Pesantren")
        edu_str = ", ".join(edu_details) if edu_details else "sarana pendidikan"

        kes_details = []
        if fas_m.get('tot_posyandu', 0) > 0: kes_details.append(f"{fas_m['tot_posyandu']} Posyandu")
        if fas_m.get('tot_polindes', 0) > 0: kes_details.append(f"{fas_m['tot_polindes']} Polindes/Poskesdes")
        kes_str = ", ".join(kes_details) if kes_details else "sarana kesehatan"

        pem_eko_details = []
        if fas_m.get('tot_kantor', 0) > 0: pem_eko_details.append(f"{fas_m['tot_kantor']} Kantor Desa/Dusun")
        if fas_m.get('tot_ekonomi', 0) > 0: pem_eko_details.append(f"{fas_m['tot_ekonomi']} Sarana Ekonomi/UMKM")
        if fas_m.get('tot_tpu', 0) > 0: pem_eko_details.append(f"{fas_m['tot_tpu']} TPU")
        if fas_m.get('tot_bts', 0) > 0: pem_eko_details.append(f"{fas_m['tot_bts']} Menara BTS")
        if fas_m.get('tot_olahraga', 0) > 0: pem_eko_details.append(f"{fas_m['tot_olahraga']} Lapangan Olahraga")
        pem_eko_str = ", ".join(pem_eko_details) if pem_eko_details else "sarana umum lainnya"
        tot_pem_eko = (fas_m.get('tot_kantor', 0) + fas_m.get('tot_ekonomi', 0) + fas_m.get('tot_tpu', 0) + fas_m.get('tot_bts', 0) + fas_m.get('tot_olahraga', 0) + fas_m.get('tot_fasum_lain', 0))

        md += f"""
---

### **5.2 SEBARAN SARANA PERIBADATAN, PENDIDIKAN, KESEHATAN & PEMERINTAHAN/EKONOMI**
Hasil pendataan fasilitas di Desa {name_title} mengidentifikasi **{fas_m.get('tot_ibadah', 0)} sarana peribadatan** ({ibadah_str}), **{fas_m.get('tot_pendidikan', 0)} sarana pendidikan** ({edu_str}), **{fas_m.get('tot_kesehatan', 0)} sarana kesehatan** ({kes_str}), serta **{tot_pem_eko} sarana pemerintahan, ekonomi & fasilitas umum** ({pem_eko_str}).

**Tabel 12. Sebaran Sarana Peribadatan, Pendidikan, Kesehatan, dan Pemerintahan/Ekonomi per RT**
| Nama RT | Peribadatan (Masjid/Surau) | Pendidikan (TK/SD/SMP/SMA/Ponpes) | Kesehatan (Posyandu/Polindes) | Pemerintahan & Ekonomi | Total Sarana |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
        for fr in fas_rows:
            oth = (fr['kantor'] + fr['ekonomi'] + fr['tpu'] + fr['bts'] + fr['olahraga'] + fr['tot_fasum_lain'])
            tot_sub = fr['tot_ibadah'] + fr['tot_pendidikan'] + fr['tot_kesehatan'] + oth
            md += f"| **{fr['rt_name']}** | {fr['tot_ibadah']} | {fr['tot_pendidikan']} | {fr['tot_kesehatan']} | {oth} | **{tot_sub}** |\n"

        tot_all_fas = fas_m.get('tot_ibadah', 0) + fas_m.get('tot_pendidikan', 0) + fas_m.get('tot_kesehatan', 0) + tot_pem_eko
        md += f"""| **DESA {name_upper}** | **{fas_m.get('tot_ibadah', 0)}** | **{fas_m.get('tot_pendidikan', 0)}** | **{fas_m.get('tot_kesehatan', 0)}** | **{tot_pem_eko}** | **{tot_all_fas}** |

---

### **5.3 KONDISI BANGUNAN & AKSES INFRASTRUKTUR DESA**
Sebanyak **{fas_m.get('tot_kondisi_baik', 0)} fasilitas ({(fas_m.get('tot_kondisi_baik', 0)/max(1, fas_m.get('tot_kondisi_baik', 0)+fas_m.get('tot_kondisi_rusak', 0))*100):.1f}%)** berada dalam kondisi fisik baik. Infrastruktur pendukung mencakup **{fas_m.get('tot_jalan_aspal', 0)} akses jalan beraspal/beton**, **{fas_m.get('tot_listrik_pln', 0)} tersambung listrik PLN 24 jam**, dan **{fas_m.get('tot_sinyal_4g', 0)} terjangkau sinyal seluler 4G/LTE**.

**Tabel 13. Rekapitulasi Kondisi Bangunan dan Akses Infrastruktur Desa per RT**
| Nama RT | Kondisi Baik | Jalan Aspal/Beton | Listrik PLN | Sinyal 4G/LTE |
| :--- | :---: | :---: | :---: | :---: |
"""
        for fr in fas_rows:
            md += f"| **{fr['rt_name']}** | {fr['kondisi_baik']} | {fr['jalan_aspal']} | {fr['listrik_pln']} | {fr['sinyal_4g']} |\n"

        md += f"""| **DESA {name_upper}** | **{fas_m.get('tot_kondisi_baik', 0)}** | **{fas_m.get('tot_jalan_aspal', 0)}** | **{fas_m.get('tot_listrik_pln', 0)}** | **{fas_m.get('tot_sinyal_4g', 0)}** |
"""

    md += f"""
---

# **MENCERDASKAN BANGSA DENGAN DATA STATISTIK DESA**
"""

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-desa-{name_kebab}-dalam-angka-{year}.md"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Markdown file written: {out_path}")
    return out_path
