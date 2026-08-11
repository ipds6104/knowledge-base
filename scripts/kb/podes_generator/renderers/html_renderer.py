"""HTML Renderer Module for BPS Potensi Desa (PODES) Publication Engine."""

from pathlib import Path
from ..schemas import PodesPublicationData


def fmt_val(val: Any) -> str:
    """Format angka atau string menjadi format Indonesia."""
    if isinstance(val, (int, float)):
        return f"{val:,}".replace(",", ".")
    return str(val)


def render_podes_html(pub_data: PodesPublicationData) -> Path:
    """Menggenerasikan naskah HTML BPS A4 Bilingual Siap Cetak Publikasi Potensi Desa 2026 (Tahun Data 2025)."""
    cfg = pub_data.config
    m = pub_data.metrics

    name_title = cfg["name_title"]
    name_kebab = cfg["name_kebab"]
    name_upper = name_title.upper()
    admin_type = cfg["admin_type"]
    admin_upper = admin_type.upper()
    admin_type_en = cfg["admin_type_en"]
    pub_no = cfg["pub_no"]
    kades_title = cfg["kades_title"]
    kades_name = cfg["kades_name"]
    kecamatan = cfg.get("kecamatan", "Mempawah")
    kabupaten = cfg.get("kabupaten", "Mempawah")
    provinsi = cfg.get("provinsi", "Kalimantan Barat")

    year = cfg.get("year", 2026)
    data_year = cfg.get("data_year", 2025)

    tot_pop_str = fmt_val(m.total_penduduk)
    l_str = fmt_val(m.penduduk_l)
    p_str = fmt_val(m.penduduk_p)
    sr_str = f"{m.sex_ratio:.2f}".replace(".", ",")
    kk_str = fmt_val(m.jumlah_kk)

    css = """
    <style>
      @page { size: A4; margin: 0; }
      body { font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; padding: 0; background: #e2e8f0; color: #1e293b; -webkit-print-color-adjust: exact; }
      .page { width: 210mm; min-height: 297mm; padding: 20mm 15mm; margin: 10px auto; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); position: relative; box-sizing: border-box; page-break-after: always; display: flex; flex-direction: column; }
      .cover-page { padding: 0; background: linear-gradient(135deg, #0b3c5d 0%, #1d5c88 100%); color: #ffffff; justify-content: space-between; overflow: hidden; }
      .cover-header { padding: 25mm 20mm 10mm; text-align: left; }
      .cover-logo-box { display: flex; align-items: center; gap: 12px; margin-bottom: 25px; }
      .cover-logo-text { font-size: 11pt; font-weight: 800; tracking: 1px; color: #f8fafc; text-transform: uppercase; }
      .cover-badge { display: inline-block; background: #eb8a3c; color: #ffffff; font-size: 9pt; font-weight: 800; padding: 4px 14px; border-radius: 4px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px; }
      .cover-title { font-size: 26pt; font-weight: 900; line-height: 1.25; margin-bottom: 12px; text-transform: uppercase; color: #ffffff; }
      .cover-subtitle { font-size: 14pt; font-weight: 500; color: #cbd5e1; font-style: italic; margin-bottom: 20px; }
      .cover-meta { border-top: 2px solid rgba(255,255,255,0.2); padding-top: 15px; font-size: 10pt; color: #e2e8f0; }
      .cover-footer { padding: 20mm; background: #072a42; border-top: 4px solid #eb8a3c; text-align: left; }
      .cover-publisher { font-size: 12pt; font-weight: 800; color: #ffffff; text-transform: uppercase; }
      .cover-publisher-sub { font-size: 9.5pt; color: #94a3b8; margin-top: 4px; }
      
      .chapter-header { border-bottom: 3px solid #0b3c5d; padding-bottom: 8px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
      .chapter-title-id { font-size: 14pt; font-weight: 800; color: #0b3c5d; text-transform: uppercase; }
      .chapter-title-en { font-size: 10pt; font-weight: 600; color: #64748b; font-style: italic; }
      
      .section-box { margin-bottom: 18px; }
      .section-title { font-size: 11pt; font-weight: 800; color: #0b3c5d; margin-bottom: 8px; border-left: 4px solid #eb8a3c; padding-left: 8px; text-transform: uppercase; }
      
      .narrative-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; font-size: 8.8pt; line-height: 1.6; }
      .narrative-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
      .narrative-col-id p { margin: 0 0 6px; color: #1e293b; }
      .narrative-col-en p { margin: 0 0 6px; color: #475569; font-style: italic; }
      .narrative-title { font-weight: 800; font-size: 8pt; color: #0b3c5d; text-transform: uppercase; margin-bottom: 4px; }
      .narrative-title.en { color: #64748b; }
      
      table.bps-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 8.2pt; }
      table.bps-table th { background: #0b3c5d; color: #ffffff; font-weight: 700; text-align: center; padding: 7px 8px; border: 1px solid #072a42; vertical-align: middle; }
      table.bps-table th.sub-header { background: #1d5c88; font-size: 7.5pt; }
      table.bps-table th.col-num { background: #2c6e9b; font-size: 7pt; font-weight: 400; }
      table.bps-table td { padding: 6px 8px; border: 1px solid #cbd5e1; color: #1e293b; vertical-align: middle; }
      table.bps-table tr:nth-child(even) td { background: #f8fafc; }
      table.bps-table tr.total-row td { background: #e2e8f0; font-weight: 800; border-top: 2px solid #0b3c5d; }
      .text-center { text-align: center; }
      .text-right { text-align: right; }

      .page-footer { margin-top: auto; padding-top: 10px; border-top: 1px solid #cbd5e1; display: flex; justify-content: space-between; font-size: 7.5pt; color: #64748b; }
      .dots-leader { flex: 1; border-bottom: 1px dotted #94a3b8; margin: 0 6px 4px; }
      .toc-row { display: flex; align-items: baseline; font-size: 9pt; margin-bottom: 6px; }
      .toc-title { font-weight: 700; color: #0b3c5d; }
      .toc-sub { padding-left: 14px; font-weight: 400; color: #334155; }
    </style>
    """

    # Page 1: Cover
    p1_cover = f"""
    <div class="page cover-page">
      <div class="cover-header">
        <div class="cover-logo-box">
          <div class="cover-logo-text">BADAN PUSAT STATISTIK<br>KABUPATEN MEMPAWAH</div>
        </div>
        <div class="cover-badge">PUBLIKASI POTENSI DESA / PODES {data_year}</div>
        <div class="cover-title">POTENSI {admin_upper}<br>{name_upper} {year}</div>
        <div class="cover-subtitle">Potentials of {name_title} {admin_type_en} {year}</div>
        <div class="cover-meta">
          <strong>Kecamatan {kecamatan} — Kabupaten {kabupaten}</strong><br>
          Hasil Pendataan Potensi Desa (PODES) Tahun {data_year}
        </div>
      </div>
      <div class="cover-footer">
        <div class="cover-publisher">BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH</div>
        <div class="cover-publisher-sub">BPS-Statistics Mempawah Regency</div>
      </div>
    </div>
    """

    # Page 2: Catalog Page (Halaman ii)
    p2_catalog = f"""
    <div class="page">
      <div style="font-size: 9pt; line-height: 1.6;">
        <h3 style="color: #0b3c5d; border-bottom: 2px solid #0b3c5d; padding-bottom: 4px; text-transform: uppercase;">KATALOG PUBLIKASI BPS</h3>
        <table style="width: 100%; border: none; font-size: 8.8pt; margin-bottom: 20px;">
          <tr><td style="width: 160px; font-weight: 700;">Judul Publikasi</td><td>: Potensi {admin_type} {name_title} {year}</td></tr>
          <tr><td style="font-weight: 700;">Publication Title</td><td>: <i>Potentials of {name_title} {admin_type_en} {year}</i></td></tr>
          <tr><td style="font-weight: 700;">Nomor Publikasi</td><td>: {pub_no}</td></tr>
          <tr><td style="font-weight: 700;">Ukuran Buku</td><td>: 21 cm x 29,7 cm (A4)</td></tr>
          <tr><td style="font-weight: 700;">Jumlah Halaman</td><td>: iv + 16 halaman</td></tr>
          <tr><td style="font-weight: 700;">Naskah / Text</td><td>: BPS Kabupaten Mempawah</td></tr>
          <tr><td style="font-weight: 700;">Penyunting / Editor</td><td>: BPS Kabupaten Mempawah</td></tr>
          <tr><td style="font-weight: 700;">Penerbit / Publisher</td><td>: © BPS Kabupaten Mempawah</td></tr>
          <tr><td style="font-weight: 700;">Sumber Data</td><td>: Pendataan Potensi Desa (PODES) Tahun {data_year}</td></tr>
        </table>
        
        <div style="border: 1.5px solid #0b3c5d; padding: 12px; border-radius: 6px; background: #f8fafc; margin-top: 40px;">
          <strong style="color: #0b3c5d; text-transform: uppercase;">KLAUSUL HAK CIPTA / COPYRIGHT NOTICE</strong><br>
          <p style="font-size: 8.2pt; color: #334155; margin-top: 6px; text-align: justify;">
            Dilarang mengumumkan, mendistribusikan, mengomunikasikan, dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik Kabupaten Mempawah.<br>
            <i>It is strictly forbidden to publish, distribute, communicate, and/or copy part or all of the contents of this book for commercial purposes without written permission from BPS-Statistics Mempawah Regency.</i>
          </p>
        </div>
      </div>
      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>ii</span>
      </div>
    </div>
    """

    # Page 3: Preface Page (Halaman iii)
    p3_preface = f"""
    <div class="page">
      <h2 style="color: #0b3c5d; border-bottom: 2px solid #eb8a3c; padding-bottom: 6px; text-align: center; text-transform: uppercase;">KATA PENGANTAR / <i>PREFACE</i></h2>
      <div style="font-size: 8.8pt; line-height: 1.7; color: #1e293b; margin-top: 15px;">
        <p>Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi <strong>"Potensi {admin_type} {name_title} {year}"</strong> ini dapat diselesaikan dengan baik. Publikasi ini menyajikan gambaran komprehensif mengenai potensi kewilayahan, kependudukan, perumahan, energi, fasilitas sosial, prasarana komunikasi, hingga kelembagaan dan ekonomi masyarakat di {admin_type} {name_title} berdasarkan Pendataan Potensi Desa (PODES) Tahun {data_year}.</p>
        <p>Data yang disajikan diharapkan dapat menjadi rujukan baku bagi Pemerintah {admin_type} dan para pemangku kepentingan dalam perencanaan pembangunan kewilayahan (<i>evidence-based policy</i>) demi meningkatkan kesejahteraan masyarakat.</p>
        <p>Kami menyampaikan ucapan terima kasih dan penghargaan setinggi-tingginya kepada seluruh pihak yang telah membantu terwujudnya publikasi ini.</p>
        <br>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 30px;">
          <div></div>
          <div style="text-align: center;">
            {name_title}, Agustus {year}<br>
            <strong>{kades_title}</strong><br><br><br><br>
            <u><strong>{kades_name.upper()}</strong></u>
          </div>
        </div>
      </div>
      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>iii</span>
      </div>
    </div>
    """

    # Page 4: TOC & LOT (Halaman iv)
    p4_toc = f"""
    <div class="page">
      <h3 style="color: #0b3c5d; border-bottom: 2px solid #0b3c5d; padding-bottom: 4px; text-transform: uppercase; margin-bottom: 12px;">DAFTAR ISI / <i>TABLE OF CONTENTS</i></h3>
      <div style="font-size: 8.5pt;">
        <div class="toc-row"><span class="toc-title">KATA PENGANTAR / <i>PREFACE</i></span><span class="dots-leader"></span><span>iii</span></div>
        <div class="toc-row"><span class="toc-title">DAFTAR ISI / <i>TABLE OF CONTENTS</i></span><span class="dots-leader"></span><span>iv</span></div>
        <div class="toc-row"><span class="toc-title">PENJELASAN TEKNIS & KONSEP DEFINISI PODES</span><span class="dots-leader"></span><span>1</span></div>
        <div class="toc-row"><span class="toc-title">RINGKASAN STATISTIK KUNCI PODES {data_year}</span><span class="dots-leader"></span><span>2</span></div>
        
        <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">BAB I: WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN</span><span class="dots-leader"></span><span>3</span></div>
        <div class="toc-row"><span class="toc-sub">1.1 Status Wilayah, Kawasan Hutan & Administrasi RT/RW</span><span class="dots-leader"></span><span>3</span></div>
        <div class="toc-row"><span class="toc-sub">1.2 Kependudukan, Sex Ratio & Keluarga Pertanian</span><span class="dots-leader"></span><span>4</span></div>
        
        <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">BAB II: ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA</span><span class="dots-leader"></span><span>5</span></div>
        <div class="toc-row"><span class="toc-sub">2.1 Penggunaan Listrik, Penerangan Jalan & Bahan Bakar</span><span class="dots-leader"></span><span>5</span></div>
        <div class="toc-row"><span class="toc-sub">2.2 Air Minum & Potensi/Mitigasi Bencana Alam</span><span class="dots-leader"></span><span>6</span></div>
        
        <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">BAB III: FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)</span><span class="dots-leader"></span><span>7</span></div>
        <div class="toc-row"><span class="toc-sub">3.1 Sarana Pendidikan Formal & Keagamaan</span><span class="dots-leader"></span><span>7</span></div>
        <div class="toc-row"><span class="toc-sub">3.2 Sarana Kesehatan, Posyandu & Posbindu</span><span class="dots-leader"></span><span>8</span></div>
        
        <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">BAB IV: TRANSPORTASI, KOMUNIKASI, EKONOMI & INDUSTRI</span><span class="dots-leader"></span><span>9</span></div>
        <div class="toc-row"><span class="toc-sub">4.1 Prasarana Transportasi, Akses Jalan & Angkutan</span><span class="dots-leader"></span><span>9</span></div>
        <div class="toc-row"><span class="toc-sub">4.2 Menara BTS, Layanan Seluler & Internet 4G/5G</span><span class="dots-leader"></span><span>10</span></div>
        <div class="toc-row"><span class="toc-sub">4.3 Fasilitas Ekonomi, Mata Pencaharian & IMK</span><span class="dots-leader"></span><span>11</span></div>
        
        <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">BAB V: PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA</span><span class="dots-leader"></span><span>12</span></div>
        <div class="toc-row"><span class="toc-sub">5.1 Aparatur Desa, BPD/LMK & Sistem Informasi Desa</span><span class="dots-leader"></span><span>12</span></div>
      </div>
      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>iv</span>
      </div>
    </div>
    """

    # Page 5: Key Stats Infographic (Arab Page 1)
    p5_keystats = f"""
    <div class="page">
      <div class="chapter-header">
        <div class="chapter-title-id">RINGKASAN STATISTIK KUNCI PODES {data_year}</div>
        <div class="chapter-title-en">KEY STATISTICS SUMMARY OF PODES {data_year}</div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 14px;">
        <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-left: 4px solid #16a34a; padding: 12px; border-radius: 8px;">
          <div style="font-size: 8pt; font-weight: 800; color: #166534; text-transform: uppercase;">Total Penduduk / Population</div>
          <div style="font-size: 18pt; font-weight: 900; color: #15803d; margin: 4px 0;">{tot_pop_str} Jiwa</div>
          <div style="font-size: 7.5pt; color: #166534;">{l_str} Laki-laki | {p_str} Perempuan (Sex Ratio: {sr_str})</div>
        </div>
        <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-left: 4px solid #2563eb; padding: 12px; border-radius: 8px;">
          <div style="font-size: 8pt; font-weight: 800; color: #1e40af; text-transform: uppercase;">Total Keluarga / Households</div>
          <div style="font-size: 18pt; font-weight: 900; color: #1d4ed8; margin: 4px 0;">{kk_str} KK</div>
          <div style="font-size: 7.5pt; color: #1e40af;">Keluarga Pertanian: {fmt_val(m.kk_pertanian)} KK ({m.kk_pertanian_pct}%)</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px;">
        <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 3.5px solid #d97706; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #92400e;">LISTRIK PLN / ELECTRICITY</div>
          <div style="font-size: 13pt; font-weight: 800; color: #b45309; margin-top: 3px;">{fmt_val(m.listrik_pln)} KK</div>
          <div style="font-size: 7pt; color: #78350f;">{((m.listrik_pln/max(1, m.jumlah_kk))*100):.1f}% Cakupan PLN</div>
        </div>
        <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-left: 3.5px solid #9333ea; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #6b21a8;">MENARA BTS / BTS TOWERS</div>
          <div style="font-size: 13pt; font-weight: 800; color: #7e22ce; margin-top: 3px;">{m.jumlah_bts} Menara</div>
          <div style="font-size: 7pt; color: #581c87;">Sinyal: {m.sinyal_hp}</div>
        </div>
        <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-left: 3.5px solid #0d9488; padding: 10px; border-radius: 6px;">
          <div style="font-size: 7.5pt; font-weight: 800; color: #115e59;">INDUSTRI MIKRO (IMK)</div>
          <div style="font-size: 13pt; font-weight: 800; color: #0f766e; margin-top: 3px;">{m.jumlah_imk} Usaha</div>
          <div style="font-size: 7pt; color: #134e4a;">Usaha Pengolahan Mikro</div>
        </div>
      </div>

      <div class="narrative-box">
        <div class="narrative-title">RINGKASAN PROFIL DESA PODES {data_year}</div>
        <p style="margin-bottom: 4px;">{admin_type} {name_title} berstatus wilayah <strong>{m.status_daerah}</strong> dengan lokasi kantor di <strong>{m.alamat_lengkap}</strong>. Jumlah wilayah terbagi atas <strong>{m.jumlah_rw} RW</strong> dan <strong>{m.jumlah_rt} RT</strong>. Mata pencaharian utama sebagian besar masyarakat adalah <strong>{m.sumber_penghasilan_utama} ({m.subsektor_utama})</strong>.</p>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>1</span>
      </div>
    </div>
    """

    # Page 6: Chapter 1 (Wilayah & Demografi)
    p6_ch1 = f"""
    <div class="page">
      <div class="chapter-header">
        <div>
          <div style="font-size: 9pt; font-weight: 800; color: #eb8a3c; text-transform: uppercase;">BAB I / CHAPTER I</div>
          <div class="chapter-title-id">WILAYAH ADMINISTRASI, DEMOGRAFI & KAWASAN</div>
          <div class="chapter-title-en">ADMINISTRATIVE AREA, DEMOGRAPHICS & REGION</div>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">1.1 STATUS WILAYAH, KAWASAN HUTAN & ADMINISTRASI RT/RW</div>
        <div class="narrative-box">
          <div class="narrative-grid">
            <div class="narrative-col-id">
              <p>{admin_type} {name_title} berstatus sebagai wilayah <strong>{m.status_daerah}</strong> dengan alamat kantor di {m.alamat_lengkap}. Keberadaan wilayah terhadap kawasan hutan tercatat <strong>{m.kawasan_hutan}</strong>. Wilayah terbagi menjadi <strong>{m.jumlah_rw} RW</strong> dan <strong>{m.jumlah_rt} RT</strong>.</p>
            </div>
            <div class="narrative-col-en">
              <p>{name_title} {admin_type_en} is classified as a {m.status_daerah} area with office located at {m.alamat_lengkap}. The regional location relative to forest areas is {m.kawasan_hutan}. The area consists of {m.jumlah_rw} RWs and {m.jumlah_rt} RTs.</p>
            </div>
          </div>
        </div>

        <table class="bps-table">
          <thead>
            <tr><th>Indikator Kewilayahan / <i>Regional Indicator</i></th><th>Isian Data PODES {data_year} / <i>Data Value</i></th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Status Klasifikasi Wilayah / <i>Regional Status</i></td><td class="text-center"><strong>{m.status_daerah}</strong></td></tr>
            <tr><td>Alamat Lengkap Kantor / <i>Office Address</i></td><td>{m.alamat_lengkap}</td></tr>
            <tr><td>Lokasi Terhadap Kawasan Hutan / <i>Forest Area Relation</i></td><td>{m.kawasan_hutan}</td></tr>
            <tr><td>Jumlah Rukun Warga (RW) / <i>Number of RWs</i></td><td class="text-center"><strong>{m.jumlah_rw} RW</strong></td></tr>
            <tr><td>Jumlah Rukun Tetangga (RT) / <i>Number of RTs</i></td><td class="text-center"><strong>{m.jumlah_rt} RT</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="section-box">
        <div class="section-title">1.2 KEPENDUDUKAN & KELUARGA PERTANIAN</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Kependudukan / <i>Demographic Indicator</i></th><th>Nilai / <i>Value</i></th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Penduduk Laki-laki / <i>Male Population</i></td><td class="text-right">{l_str} jiwa ({m.male_pct}%)</td></tr>
            <tr><td>Penduduk Perempuan / <i>Female Population</i></td><td class="text-right">{p_str} jiwa ({m.female_pct}%)</td></tr>
            <tr class="total-row"><td>Total Penduduk / <i>Total Population</i></td><td class="text-right">{tot_pop_str} jiwa</td></tr>
            <tr><td>Rasio Jenis Kelamin / <i>Sex Ratio</i></td><td class="text-right"><strong>{sr_str}</strong></td></tr>
            <tr><td>Total Keluarga (KK) / <i>Total Households</i></td><td class="text-right">{kk_str} KK</td></tr>
            <tr><td>Keluarga Pertanian / <i>Agricultural Households</i></td><td class="text-right"><strong>{fmt_val(m.kk_pertanian)} KK ({m.kk_pertanian_pct}%)</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>3</span>
      </div>
    </div>
    """

    # Page 7: Chapter 2 (Energi & Bencana)
    p7_ch2 = f"""
    <div class="page">
      <div class="chapter-header">
        <div>
          <div style="font-size: 9pt; font-weight: 800; color: #eb8a3c; text-transform: uppercase;">BAB II / CHAPTER II</div>
          <div class="chapter-title-id">ENERGI, UTILITAS PERUMAHAN & MITIGASI BENCANA</div>
          <div class="chapter-title-en">ENERGY, HOUSING UTILITIES & DISASTER MITIGATION</div>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">2.1 PENGGUNAAN LISTRIK & BAHAN BAKAR</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Energi & Utilitas / <i>Energy & Utility Indicator</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Pengguna Listrik PLN / <i>PLN Electricity Users</i></td><td class="text-right"><strong>{fmt_val(m.listrik_pln)} KK</strong></td></tr>
            <tr><td>Pengguna Listrik Non-PLN / <i>Non-PLN Users</i></td><td class="text-right">{fmt_val(m.listrik_non_pln)} KK</td></tr>
            <tr><td>Bukan Pengguna Listrik / <i>Non-Electricity Users</i></td><td class="text-right">{fmt_val(m.bukan_listrik)} KK</td></tr>
            <tr><td>Penerangan Jalan Utama / <i>Main Road Lighting</i></td><td>{m.penerangan_jalan}</td></tr>
            <tr><td>Bahan Bakar Memasak / <i>Cooking Fuel</i></td><td><strong>{m.bakar_masak}</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="section-box">
        <div class="section-title">2.2 AIR MINUM & KESIAPSIAGAAN BENCANA ALAM</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Lingkungan & Bencana / <i>Environment & Disaster</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Sumber Air Minum Utama / <i>Main Drinking Water Source</i></td><td><strong>{m.air_minum}</strong></td></tr>
            <tr><td>Kejadian Bencana Alam / <i>Natural Disaster Incident</i></td><td>{m.bencana_alam}</td></tr>
            <tr><td>Upaya & Mitigasi Bencana / <i>Disaster Mitigation Facilities</i></td><td>{m.mitigasi_bencana}</td></tr>
          </tbody>
        </table>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>5</span>
      </div>
    </div>
    """

    # Page 8: Chapter 3 (Fasilitas Sosial)
    p8_ch3 = f"""
    <div class="page">
      <div class="chapter-header">
        <div>
          <div style="font-size: 9pt; font-weight: 800; color: #eb8a3c; text-transform: uppercase;">BAB III / CHAPTER III</div>
          <div class="chapter-title-id">FASILITAS SOSIAL (PENDIDIKAN & KESEHATAN)</div>
          <div class="chapter-title-en">SOCIAL FACILITIES (EDUCATION & HEALTH)</div>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">3.1 SARANA PENDIDIKAN FORMAL & KEAGAMAAN</div>
        <div class="narrative-box">
          <p><strong>Sarana Pendidikan Terdaftar:</strong> {m.sarana_pendidikan}</p>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">3.2 SARANA KESEHATAN, POSYANDU & POSBINDU</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Pelayanan Kesehatan / <i>Health Service Indicator</i></th><th>Jumlah / Keterangan</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Fasilitas Kesehatan Utama / <i>Main Health Facilities</i></td><td>{m.sarana_kesehatan}</td></tr>
            <tr><td>Posyandu Aktif (Pelayanan Rutin Bulanan) / <i>Active Posyandu</i></td><td class="text-right"><strong>{m.posyandu_aktif} unit</strong></td></tr>
            <tr><td>Posbindu / <i>Posbindu Units</i></td><td class="text-right"><strong>{m.posbindu} unit</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>7</span>
      </div>
    </div>
    """

    # Page 9: Chapter 4 (Transportasi & Komunikasi & Ekonomi)
    p9_ch4 = f"""
    <div class="page">
      <div class="chapter-header">
        <div>
          <div style="font-size: 9pt; font-weight: 800; color: #eb8a3c; text-transform: uppercase;">BAB IV / CHAPTER IV</div>
          <div class="chapter-title-id">TRANSPORTASI, KOMUNIKASI & EKONOMI</div>
          <div class="chapter-title-en">TRANSPORTATION, COMMUNICATION & ECONOMY</div>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">4.1 TRANSPORTASI & PRASARANA JALAN</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Transportasi / <i>Transport Indicator</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Prasarana Transportasi Utama / <i>Main Transport Infrastructure</i></td><td>{m.prasarana_transportasi}</td></tr>
            <tr><td>Jenis Permukaan Jalan Utama / <i>Road Surface Type</i></td><td><strong>{m.jenis_jalan}</strong></td></tr>
            <tr><td>Aksesibilitas Roda 4 atau Lebih / <i>4-Wheel Vehicle Access</i></td><td>{m.jalan_roda4}</td></tr>
            <tr><td>Operasional Angkutan Umum / <i>Public Transit Service</i></td><td>{m.angkutan_umum}</td></tr>
          </tbody>
        </table>
      </div>

      <div class="section-box">
        <div class="section-title">4.2 TELEKOMUNIKASI, BTS & SINYAL INTERNET</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Telekomunikasi / <i>Telecom Indicator</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Jumlah Menara BTS / <i>BTS Towers</i></td><td class="text-right"><strong>{m.jumlah_bts} unit</strong></td></tr>
            <tr><td>Operator Telekomunikasi / <i>Mobile Operators</i></td><td>{m.operator_seluler}</td></tr>
            <tr><td>Kekuatan Sinyal Telepon Seluler / <i>Cellular Signal Strength</i></td><td><strong>{m.sinyal_hp}</strong></td></tr>
            <tr><td>Jaringan Internet Seluler / <i>Mobile Internet Network</i></td><td><strong>{m.sinyal_internet}</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="section-box">
        <div class="section-title">4.3 FASILITAS EKONOMI & INDUSTRI MIKRO KECIL (IMK)</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Ekonomi & Industri / <i>Economic & Industry Indicator</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Mata Pencaharian Utama / <i>Main Livelihood</i></td><td><strong>{m.sumber_penghasilan_utama} ({m.subsektor_utama})</strong></td></tr>
            <tr><td>Fasilitas Ekonomi Utama / <i>Economic Facilities</i></td><td>{m.sarana_ekonomi}</td></tr>
            <tr><td>Industri Mikro & Kecil (IMK) / <i>Micro & Small Industries</i></td><td class="text-right"><strong>{fmt_val(m.jumlah_imk)} unit usaha</strong></td></tr>
          </tbody>
        </table>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>9</span>
      </div>
    </div>
    """

    # Page 10: Chapter 5 (Pemerintahan & Kelembagaan)
    p10_ch5 = f"""
    <div class="page">
      <div class="chapter-header">
        <div>
          <div style="font-size: 9pt; font-weight: 800; color: #eb8a3c; text-transform: uppercase;">BAB V / CHAPTER V</div>
          <div class="chapter-title-id">PEMERINTAHAN, KELEMBAGAAN & INFORMASI DESA</div>
          <div class="chapter-title-en">GOVERNMENT, INSTITUTIONS & VILLAGE INFORMATION</div>
        </div>
      </div>

      <div class="section-box">
        <div class="section-title">5.1 APARATUR DESA, BPD/LMK & SISTEM INFORMASI DESA</div>
        <table class="bps-table">
          <thead>
            <tr><th>Indikator Pemerintahan & Kelembagaan / <i>Govt Indicator</i></th><th>Isian Data PODES {data_year}</th></tr>
            <tr><th class="col-num">(1)</th><th class="col-num">(2)</th></tr>
          </thead>
          <tbody>
            <tr><td>Aparatur Pemerintah Desa/Kelurahan / <i>Village Apparatus</i></td><td class="text-right"><strong>{m.aparatur_pemdes} orang</strong></td></tr>
            <tr><td>Keberadaan BPD / LMK / <i>Village Representative Council</i></td><td><strong>{m.keberadaan_bpd}</strong></td></tr>
            <tr><td>Kegiatan Musyawarah Desa / <i>Village Deliberation Meetings</i></td><td class="text-right"><strong>{m.musyawarah_desa} kali</strong></td></tr>
            <tr><td>Sistem Informasi Desa (SID) / <i>Village Info System</i></td><td>{m.sistem_informasi_desa}</td></tr>
            <tr><td>Ketersediaan SPPG / <i>SPPG Status</i></td><td>{m.jumlah_sppg}</td></tr>
          </tbody>
        </table>
      </div>

      <div style="margin-top: 40px; border-top: 2.5px solid #0b3c5d; padding-top: 20px; text-align: center;">
        <h3 style="color: #0b3c5d; font-size: 14pt; font-weight: 900; tracking: 1px;">MENCERDASKAN BANGSA DENGAN DATA STATISTIK DESA</h3>
        <p style="font-size: 9pt; color: #64748b; font-style: italic;">Enlightening the Nation with Village Statistical Data</p>
      </div>

      <div class="page-footer">
        <span>Potensi {admin_type} {name_title} {year}</span>
        <span>12</span>
      </div>
    </div>
    """

    full_html = f"""<!DOCTYPE html>
    <html lang="id">
    <head>
      <meta charset="UTF-8">
      <title>Potensi {admin_type} {name_title} {year}</title>
      {css}
    </head>
    <body>
      {p1_cover}
      {p2_catalog}
      {p3_preface}
      {p4_toc}
      {p5_keystats}
      {p6_ch1}
      {p7_ch2}
      {p8_ch3}
      {p9_ch4}
      {p10_ch5}
    </body>
    </html>
    """

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"publikasi-potensi-{name_kebab}-{year}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"HTML file written: {out_path}")
    return out_path
