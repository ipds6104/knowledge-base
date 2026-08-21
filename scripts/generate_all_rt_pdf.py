import csv
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

BASE_DIR = 'kegiatan/sensus-ekonomi-2026/2026'
ALOKASI_CSV = os.path.join(BASE_DIR, 'master_data', 'Alokasi Petugas.csv')

def get_latest_csv(pattern_filename, default_filename):
    latest_path = os.path.join(BASE_DIR, 'outputs', pattern_filename)
    if os.path.exists(latest_path):
        return latest_path
    return os.path.join(BASE_DIR, 'outputs', default_filename)

KEL_CSV = get_latest_csv('microdata_tidak_ditemukan_6104_latest.csv', 'keluarga_tidak_ditemukan_6104_20260715030051.csv')
USAHA_CSV = get_latest_csv('usaha_tidak_ditemukan_6104_latest.csv', 'usaha_tidak_ditemukan_6104_20260716030225.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'pdf_verifikasi_rt')
TEMP_HTML_DIR = os.path.join(BASE_DIR, 'temp_html_rt')

def clean_filename_part(text):
    if not text:
        return 'Unknown'
    # Replace non-alphanumeric (except underscore/hyphen) with underscore
    cleaned = re.sub(r'[^\w\-\.]+', '_', text.strip())
    # Remove consecutive underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def get_logo_html():
    import base64
    logo_path = os.path.join(BASE_DIR, 'assets', 'logo_bps.svg')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(BASE_DIR), 'data', 'logo_bps.svg')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{b64}" alt="Logo BPS" style="height: 52px; width: auto;" />'
    return '<div style="border: 1.5px solid #000; padding: 4px; font-weight: bold;">BPS 6104</div>'

def is_empty_entity(name, code_id):
    """Mendeteksi entitas non-orang / bangunan kosong yang tidak relevan untuk verifikasi lapangan."""
    n = (name or '').strip().upper()
    c = (code_id or '').strip().upper()
    keywords = [
        'RUMAH KOSONG', 'BANGUNAN KOSONG', 'LAHAN KOSONG', 'TANAH KOSONG',
        'GEDUNG KOSONG', 'RUKO KOSONG', 'KANDANG KOSONG', 'KOSONG /'
    ]
    for kw in keywords:
        if kw in n or kw in c:
            return True
    return False

def clean_code_id(code_id, sls_code='', name=''):
    """Membersihkan string code_identity dari prefix SLS dan artefak tagging CAPI (misal: '- 2. Tidak', '- 0 - 2. Tidak')."""
    if not code_id or code_id == '-':
        return ''
    s = code_id.strip()
    
    # 1. Hapus prefix kode SLS jika ada (misal: '6104080001002100 - ')
    if sls_code and s.startswith(sls_code):
        s = s[len(sls_code):].strip(' -_')
    elif re.match(r'^\d{16}\s*[-_]\s*', s):
        s = re.sub(r'^\d{16}\s*[-_]\s*', '', s).strip()

    # 2. Hapus suffix status CAPI seperti '- 2. Tidak', '- 0 - 2. Tidak', '- 1 - 2. TIDAK', '/ - 2. Tidak'
    s = re.sub(r'[\s\/\-_]*\d*\.?\s*Tidak(?:\s*Ditemukan)?.*$', '', s, flags=re.IGNORECASE).strip()
    s = re.sub(r'[\s\/\-_]+0$', '', s).strip()
    s = re.sub(r'(\s*[\/\-]\s*)+$', '', s).strip()
    
    # 3. Jika setelah dibersihkan hasilnya kosong atau sama dengan '-', return kosong
    if s == '-' or not s:
        return ''
    return s

def load_data():
    alokasi = {}
    with open(ALOKASI_CSV, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            code = r.get('idsubsls', '').strip()
            if code:
                alokasi[code] = r

    kel_by_code = defaultdict(list)
    with open(KEL_CSV, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            code = r.get('level_6_full_code', '').strip()
            name = (r.get('data1') or '').strip().upper()
            code_id = (r.get('code_identity') or '').strip().upper()
            # Saring entitas DUMMY dan entitas bangunan kosong (No 1)
            if name == 'DUMMY' or 'DUMMY' in code_id or is_empty_entity(name, code_id):
                continue
            if code:
                kel_by_code[code].append(r)

    us_by_code = defaultdict(list)
    usaha_by_id = {}
    with open(USAHA_CSV, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            code = r.get('level_6_full_code', '').strip()
            nama_us = (r.get('nama_usaha') or '').strip().upper()
            code_id = (r.get('code_identity') or '').strip().upper()
            is_act = str(r.get('is_active', '1')).strip()
            # Saring entitas tidak aktif (is_active = 0), dummy, dan bangunan kosong (No 1)
            if is_act == '0' or nama_us == 'DUMMY' or is_empty_entity(nama_us, code_id):
                continue
            if code:
                us_by_code[code].append(r)
            aid = r.get('assignment_id', '').strip()
            if aid:
                usaha_by_id[aid] = r

    all_codes = sorted(list(set(kel_by_code.keys()).union(us_by_code.keys())))
    # Pastikan hanya memproses SLS yang:
    # 1. Memiliki panjang 16 digit dan digit ke-11 (index 10) adalah '0' (tanda wilayah RT/SLS pemukiman, bukan Non-SLS hutan/sawit)
    # 2. Memiliki minimal 1 responden real (non-dummy)
    all_codes = [
        c for c in all_codes
        if len(c) == 16 and c[10] == '0' and (len(kel_by_code.get(c, [])) + len(us_by_code.get(c, []))) > 0
    ]
    return alokasi, kel_by_code, us_by_code, all_codes, usaha_by_id

def build_html_for_code(code, alokasi_info, kk_list, us_list, usaha_by_id=None):
    nmsls  = alokasi_info.get('nmsls', 'Unknown SLS')
    nmkec  = alokasi_info.get('nmkec', '-')
    nmdesa = alokasi_info.get('nmdesa', '-')
    kdkec  = alokasi_info.get('kdkec', '-')
    kddesa = alokasi_info.get('kddesa', '-')
    ppl    = alokasi_info.get('PPL', '-')
    pml    = alokasi_info.get('PML', '-')
    pj     = alokasi_info.get('Pj-Kuda', '-')
    target = alokasi_info.get('Target', '0')
    logo_html    = get_logo_html()
    gen_time_str = datetime.now().strftime("%d %B %Y %H:%M")

    if usaha_by_id is None:
        usaha_by_id = {}

    # ── Prepare KK items ───────────────────────────────────────────────────────
    kk_items = []
    for idx, r in enumerate(kk_list, 1):
        raw_name = (r.get('data1') or r.get('nama_kk') or r.get('dtsen_nama_kk') or '').strip()
        code_id  = (r.get('code_identity') or r.get('nik_kk') or r.get('no_kk') or '-').strip()
        alamat   = (r.get('data2') or r.get('alamat_klrg') or r.get('alamat_prelist') or '-').strip()
        if not raw_name:
            aid    = r.get('assignment_id', '').strip()
            u_info = usaha_by_id.get(aid, {})
            u_name = (u_info.get('nama_usaha') or u_info.get('nama_komersial') or '').strip()
            raw_name = u_name or ('[Sampel UMK]' if 'UMK' in code_id else '[Sampel Prelist]')
        
        esc_name = html.escape(raw_name)
        # Bersihkan string code_identity dari artefak CAPI (No 3)
        cleaned_id = clean_code_id(code_id, code, raw_name)
        sub_id = f'NIK/KK: {html.escape(cleaned_id)}' if cleaned_id else ''
        kk_items.append({'idx': idx, 'label': f'A{idx}', 'nama': esc_name, 'sub_id': sub_id, 'alamat': html.escape(alamat)})

    # ── Prepare Usaha items ────────────────────────────────────────────────────
    us_items = []
    for idx, r in enumerate(us_list, 1):
        raw_nama_us = (r.get('nama_usaha') or r.get('nama_komersial') or '-').strip()
        
        # Ekstrak nama pemilik dari pola <...> (prelist CAPI)
        owners_in_tag = list(dict.fromkeys(re.findall(r'<([^>]+)>', raw_nama_us)))
        clean_nama_us = re.sub(r'<[^>]+>', '', raw_nama_us).strip()
        if not clean_nama_us and raw_nama_us:
            clean_nama_us = raw_nama_us
            
        pengusaha = (r.get('pengusaha') or r.get('nik_pengusaha') or '').strip()
        if not pengusaha and owners_in_tag:
            pengusaha = ', '.join(o.strip() for o in owners_in_tag if o.strip())
            
        prelist_kk = (r.get('nama_prelist_kk') or '').strip()
        if prelist_kk and not pengusaha:
            pengusaha = prelist_kk

        code_id = (r.get('code_identity') or '').strip()
        alamat_us = (r.get('alamat_usaha') or r.get('alamat_usaha_utama') or '-').strip()
        skala = (r.get('skala_usaha') or 'UMK').strip()

        # HTML Escape untuk keamanan rendering
        esc_nama = html.escape(clean_nama_us)
        esc_skala = html.escape(skala)
        nama_disp = f'{esc_nama} <span style="font-weight:normal;font-size:7px">({esc_skala})</span>'

        sub_parts = []
        if pengusaha and pengusaha != '-':
            sub_parts.append(f'Pemilik: {html.escape(pengusaha)}')
        
        # Bersihkan string code_identity dari artefak CAPI (No 3)
        cleaned_id = clean_code_id(code_id, code, clean_nama_us)
        if cleaned_id:
            short_id = cleaned_id.split(' - ', 1)[1] if ' - ' in cleaned_id else cleaned_id
            sub_parts.append(f'ID: {html.escape(short_id)}')

        sub_id = ' | '.join(sub_parts)
        us_items.append({'idx': idx, 'label': f'B{idx}', 'nama': nama_disp, 'sub_id': sub_id, 'alamat': html.escape(alamat_us)})

    total = len(kk_items) + len(us_items)

    html_doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Verifikasi Lapangan SE2026 - {nmsls}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 6mm 8mm 8mm 8mm;
    @bottom-center {{
      content: "Hal. " counter(page) " / " counter(pages) " — {nmsls} — {code}";
      font-size: 7px; color: #333;
    }}
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8px; color: #000; line-height: 1.2;
    background: #fff;
  }}

  /* ── KOP SURAT (HIGH CONTRAST B&W) ─────────────────── */
  .kop {{
    display: flex; align-items: center;
    border-bottom: 2px solid #000;
    padding-bottom: 3px; margin-bottom: 3px;
  }}
  .kop-logo {{ width: 48px; flex-shrink: 0; margin-right: 8px; }}
  .kop-text {{ flex: 1; text-align: center; }}
  .kop-text .k1 {{ font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.3px; }}
  .kop-text .k2 {{ font-size: 9.5px; font-weight: bold; margin-top: 1px; }}
  .kop-text .k3 {{ font-size: 6.8px; color: #222; margin-top: 1px; }}

  /* ── META INFO (CLEAN B&W) ─────────────────────────── */
  .meta {{ width: 100%; border-collapse: collapse; margin-bottom: 3px; }}
  .meta td {{ padding: 1.5px 3.5px; border: 0.75px solid #000; font-size: 7.5px; vertical-align: middle; }}
  .meta .lbl {{ font-weight: bold; width: 13%; }}
  .badge-bw {{
    border: 1px solid #000; padding: 0 3px; font-weight: bold;
  }}

  /* ── PANDUAN PIMPINAN / KONSEP TIDAK DITEMUKAN ────── */
  .konsep-box {{
    border: 1px solid #000;
    padding: 2.5px 5px;
    font-size: 6.8px;
    line-height: 1.25;
    margin-bottom: 3px;
  }}
  .konsep-box b {{ text-transform: uppercase; }}

  /* ── TABEL UTAMA (MAX DATA-TO-INK RATIO) ───────────── */
  .dt {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 3px;
    page-break-inside: auto;
  }}
  .dt thead {{
    display: table-header-group;
  }}
  .dt tbody tr {{
    page-break-inside: avoid;
  }}
  
  /* Thead Section Title */
  .dt thead tr.thead-sec th {{
    background: #000; color: #fff;
    font-weight: bold; font-size: 8px;
    padding: 2px 5px; text-align: left;
    text-transform: uppercase; letter-spacing: 0.3px;
    border: 1px solid #000;
  }}
  
  /* Thead Legend Box */
  .dt thead tr.thead-legend th {{
    background: #fff;
    border: 1px solid #000;
    border-top: none;
    padding: 2px 4px;
    text-align: left;
    font-weight: normal;
    color: #000;
  }}
  .legend-title {{
    font-weight: bold;
    margin-bottom: 1px;
    font-size: 6.8px;
    text-transform: uppercase;
  }}
  .legend-items {{
    display: flex;
    flex-wrap: wrap;
    gap: 2px 8px;
    align-items: center;
    font-size: 6.8px;
    line-height: 1.2;
  }}
  .legend-item b {{
    display: inline-block;
    border: 1px solid #000;
    background: #fff;
    color: #000;
    padding: 0 2.5px;
    font-size: 6.8px;
    margin-right: 2px;
  }}

  /* Thead Column Headers */
  .dt th {{
    border: 0.75px solid #000; padding: 2px 3px;
    font-size: 7px; text-align: center;
    background: #fff; font-weight: bold;
    line-height: 1.15;
  }}
  
  /* Data Rows */
  .dt td {{
    border: 0.5px solid #000; padding: 1.5px 3px;
    font-size: 7.2px; vertical-align: middle;
    background: #fff;
  }}
  .dt td.no  {{ text-align: center; font-size: 7px; font-weight: bold; width: 22px; }}

  /* Nama entitas + sub-id dalam satu sel */
  .ent-nama {{ font-weight: bold; font-size: 7.5px; line-height: 1.15; color: #000; }}
  .ent-sub  {{ font-size: 6.5px; color: #222; margin-top: 0.5px; }}

  /* Kotak Isian Kode Status */
  .code-cell {{ text-align: center; vertical-align: middle; }}
  .code-box {{
    display: inline-block;
    width: 20px;
    height: 16px;
    border: 1.2px solid #000;
    background: #fff;
    vertical-align: middle;
  }}

  /* ── HALAMAN KHUSUS BERITA ACARA PENUTUP ───────────── */
  .ba-page {{
    page-break-before: always;
    padding-top: 8px;
  }}
  .ba-box-standalone {{
    border: 1.5px solid #000;
    padding: 10px 14px;
    font-size: 8.5px;
    line-height: 1.5;
    margin: 8px 0 14px 0;
  }}
  .ba-title-standalone {{
    font-weight: bold;
    text-transform: uppercase;
    font-size: 9.5px;
    text-align: center;
    border-bottom: 1.2px solid #000;
    padding-bottom: 4px;
    margin-bottom: 8px;
    letter-spacing: 0.3px;
  }}
  .ba-rekap-standalone {{
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 8px 0;
    padding: 6px 10px;
    border: 1px solid #000;
    font-size: 8.5px;
  }}
  .box-fill {{
    display: inline-block;
    border: 1px solid #000;
    width: 36px;
    height: 16px;
    vertical-align: middle;
    background: #fff;
    margin: 0 4px;
  }}
  .line-fill {{
    display: inline-block;
    border-bottom: 1px solid #000;
    vertical-align: bottom;
    margin: 0 2px;
  }}
  .ba-notes-standalone {{
    margin-top: 8px;
    font-size: 8px;
    border-top: 0.75px dashed #000;
    padding-top: 6px;
    line-height: 1.6;
  }}

  .sig-3col {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
  .sig-3col td {{
    text-align: center; vertical-align: top;
    padding: 2px 6px; border: none;
    font-size: 8.5px;
  }}
  .sig-space-large {{ height: 50px; }}
  .sig-name {{ font-weight: bold; font-size: 9px; }}
  .sig-sub  {{ font-size: 7.5px; color: #222; margin-top: 2px; }}
</style>
</head>
<body>

<!-- KOP SURAT -->
<div class="kop">
  <div class="kop-logo">{logo_html}</div>
  <div class="kop-text">
    <div class="k1">Badan Pusat Statistik Kabupaten Mempawah</div>
    <div class="k2">Lembar Verifikasi Keberadaan Responden &mdash; Sensus Ekonomi 2026</div>
    <div class="k3">Berita Acara Pembuktian Lapangan &bull; Snapshot Data: {gen_time_str} WIB</div>
  </div>
</div>

<!-- META INFO -->
<table class="meta">
  <tr>
    <td class="lbl">Kecamatan</td><td width="27%">: <b>[{kdkec}] {nmkec}</b></td>
    <td class="lbl">Kode Sub-SLS</td><td width="47%">: <b style="font-family:monospace">{code}</b></td>
  </tr>
  <tr>
    <td class="lbl">Desa / Kelurahan</td><td>: <b>[{kddesa}] {nmdesa}</b></td>
    <td class="lbl">PPL / PML</td><td>: <b>{ppl}</b> / {pml}</td>
  </tr>
  <tr>
    <td class="lbl">Nama SLS / Sub-SLS</td><td>: <b>{nmsls}</b></td>
    <td class="lbl">PJ Wilayah</td><td>: {pj}</td>
  </tr>
  <tr>
    <td class="lbl">Kasus Dilaporkan</td>
    <td colspan="3">:&nbsp;
      <span class="badge-bw">KK Tdk Ditemukan: {len(kk_list)}</span>&nbsp;
      <span class="badge-bw">Usaha Tdk Ditemukan: {len(us_list)}</span>&nbsp;
      <b>(Total Diverifikasi: {total} Kasus)</b>
    </td>
  </tr>
</table>

<!-- PANDUAN PIMPINAN: KONSEP TIDAK DITEMUKAN & PRELIST TERTUKAR -->
<div class="konsep-box">
  <b>PENTING &mdash; KONSEP "TIDAK DITEMUKAN" (STANDAR BPS):</b><br>
  &bull; <b>HANYA</b> berlaku bagi yang <u>benar-benar tidak ada</u> di wilayah ini (<b>BUKAN</b> karena sedang bepergian/bekerja, belum sempat ditemui, atau menolak dicacah).<br>
  &bull; <b>KASUS PRELIST TERTUKAR:</b> Jika responden ternyata warga/usaha di RT/SLS tetangga, gunakan <b>KODE 2</b> dan tulis RT yang benar (Contoh: <i>"Warga RT 04"</i>).<br>
  &bull; <b>PENGISIAN CEPAT (MASSAL):</b> Jika satu blok/halaman seluruhnya tertukar ke RT yang sama, cukup tulis kode <b>2</b> dan keterangan di baris pertama, lalu beri tanda kurung kurawal/panah ke bawah.
</div>
"""

    # ── Fungsi bantu render tabel dengan sistem KODE (THEAD REPEATING) ────────
    def render_table(items, section_label, is_usaha=False):
        """Render tabel verifikasi dengan sistem KODE STATUS yang berulang di setiap halaman."""
        addr_label = 'Alamat Usaha / Lokasi' if is_usaha else 'Alamat Prelist / Domisili'
        
        if is_usaha:
            legend_inner = """
      <div class="legend-title">Petunjuk Kode Status Usaha (Diisi Pengurus RT/RW):</div>
      <div class="legend-items">
        <div class="legend-item"><b>1</b> Ada &amp; Aktif di SLS Ini</div>
        <div class="legend-item"><b>2</b> Tertukar / Masuk SLS Lain <i>(Tulis RT/SLS yang benar di Keterangan)</i></div>
        <div class="legend-item"><b>3</b> Pindah Lokasi Usaha <i>(Tulis lokasi baru)</i></div>
        <div class="legend-item"><b>4</b> Usaha Tutup / Nonaktif Permanen</div>
        <div class="legend-item"><b>5</b> Tidak Pernah Ada / Fiktif</div>
        <div class="legend-item"><b>6</b> Tidak Dapat Dikonfirmasi / Lainnya</div>
      </div>"""
            code_sub_label = "(Kode 1 - 6)"
        else:
            legend_inner = """
      <div class="legend-title">Petunjuk Kode Status Keluarga (Diisi Pengurus RT/RW):</div>
      <div class="legend-items">
        <div class="legend-item"><b>1</b> Ada di SLS Ini</div>
        <div class="legend-item"><b>2</b> Tertukar / Warga SLS Lain <i>(Tulis RT/SLS yang benar di Keterangan)</i></div>
        <div class="legend-item"><b>3</b> Pindah Keluar Wilayah <i>(Tulis tujuan di Keterangan)</i></div>
        <div class="legend-item"><b>4</b> Tidak Pernah Ada / Fiktif <i>(Bukan krn bepergian/menolak)</i></div>
        <div class="legend-item"><b>5</b> Tidak Dapat Dikonfirmasi / Lainnya</div>
      </div>"""
            code_sub_label = "(Kode 1 - 5)"

        out = f"""
<table class="dt">
  <thead>
    <tr class="thead-sec">
      <th colspan="5">{section_label}</th>
    </tr>
    <tr class="thead-legend">
      <th colspan="5">{legend_inner}</th>
    </tr>
    <tr>
      <th width="3%">No</th>
      <th width="28%">Nama{' Usaha &amp; Pengusaha' if is_usaha else ' KK &amp; Identitas'}</th>
      <th width="23%">{addr_label}</th>
      <th width="9%">Kode Status<br><span style="font-weight:normal;font-style:italic;font-size:6.2px">{code_sub_label}</span></th>
      <th width="37%">Keterangan / Lokasi Pindah / Catatan Tindak Lanjut PPL<br><span style="font-weight:normal;font-style:italic;font-size:6.2px">(Wajib diisi jika Tertukar [Kode 2], Pindah [Kode 3], atau catatan hasil pencacahan)</span></th>
    </tr>
  </thead>
  <tbody>
"""
        for item in items:
            sub_id_html = f'<div class="ent-sub">{item["sub_id"]}</div>' if item.get('sub_id') else ''
            out += f"""    <tr>
      <td class="no">{item['label']}</td>
      <td>
        <div class="ent-nama">{item['nama']}</div>
        {sub_id_html}
      </td>
      <td style="font-size:7px;color:#000">{item['alamat']}</td>
      <td class="code-cell"><div class="code-box"></div></td>
      <td style="font-size:6.8px;color:#000">&nbsp;</td>
    </tr>
"""
        out += "  </tbody>\n</table>\n"
        return out

    if kk_items:
        html_doc += render_table(
            kk_items,
            f'Bagian A &mdash; Keluarga (KK) Dilaporkan &ldquo;Tidak Ditemukan&rdquo; ({len(kk_items)} KK)',
            is_usaha=False
        )

    if us_items:
        html_doc += render_table(
            us_items,
            f'Bagian B &mdash; Usaha/Perusahaan Dilaporkan &ldquo;Tidak Ditemukan&rdquo; ({len(us_items)} Usaha)',
            is_usaha=True
        )

    # ── HALAMAN PENUTUP: BERITA ACARA STANDALONE (PAGE BREAK ALWAYS) ──────────
    html_doc += f"""
<div class="ba-page">
  <!-- KOP SURAT BERITA ACARA -->
  <div class="kop">
    <div class="kop-logo">{logo_html}</div>
    <div class="kop-text">
      <div class="k1">Badan Pusat Statistik Kabupaten Mempawah</div>
      <div class="k2">Berita Acara Pembuktian Lapangan &mdash; Sensus Ekonomi 2026</div>
      <div class="k3">Dokumen Pengesahan Hasil Verifikasi Keberadaan Responden Tidak Ditemukan</div>
    </div>
  </div>

  <!-- META INFO SLS -->
  <table class="meta" style="margin-top: 6px;">
    <tr>
      <td class="lbl">Kecamatan</td><td width="27%">: <b>[{kdkec}] {nmkec}</b></td>
      <td class="lbl">Kode Sub-SLS</td><td width="47%">: <b style="font-family:monospace">{code}</b></td>
    </tr>
    <tr>
      <td class="lbl">Desa / Kelurahan</td><td>: <b>[{kddesa}] {nmdesa}</b></td>
      <td class="lbl">PJ Wilayah</td><td>: {pj}</td>
    </tr>
    <tr>
      <td class="lbl">Nama SLS / Sub-SLS</td><td>: <b>{nmsls}</b></td>
      <td class="lbl">Total Diverifikasi</td><td>: <b>{total} Responden Prelist ({len(kk_list)} KK, {len(us_list)} Usaha)</b></td>
    </tr>
  </table>

  <!-- KOTAK PERNYATAAN & REKAPITULASI BERITA ACARA -->
  <div class="ba-box-standalone">
    <div class="ba-title-standalone">BERITA ACARA KESEPAKATAN HASIL VERIFIKASI KEBERADAAN</div>
    <div>Pada hari ini, tanggal <span class="line-fill" style="width:28px;"></span> / <span class="line-fill" style="width:28px;"></span> / 2026, telah dilaksanakan verifikasi, pengecekan, dan pembuktian keberadaan responden secara langsung di lapangan bersama antara Petugas Sensus BPS dengan Pengurus RT/RW/Kepala Wilayah setempat terhadap sejumlah <b>{total}</b> responden prelist (<b>{len(kk_list)} KK</b> dan <b>{len(us_list)} Usaha</b>) yang dilaporkan tidak ditemukan di wilayah SLS <b>{nmsls}</b>, dengan hasil kesepakatan akhir sebagai berikut:</div>
    
    <div class="ba-rekap-standalone">
      <div><b>Total Diverifikasi:</b> <b>{total}</b> Kasus</div>
      <div>&bull;</div>
      <div><b>[Kode 1] Ditemukan di SLS Ini:</b> <span class="box-fill"></span> Kasus <i>(Wajib dicacah ulang PPL)</i></div>
      <div>&bull;</div>
      <div><b>[Kode 2..6] Tidak Ditemukan:</b> <span class="box-fill"></span> Kasus <i>(Tertukar / Pindah / Fiktif / Tutup)</i></div>
    </div>

    <div class="ba-notes-standalone">
      <b>Catatan Khusus Lapangan / Kasus Prelist Tertukar Antar-RT:</b><br>
      [&nbsp;&nbsp;] Sebagian besar responden prelist di atas sebenarnya merupakan warga/usaha di RT/SLS: <span class="line-fill" style="width: 200px;"></span><br>
      [&nbsp;&nbsp;] Catatan Lapangan Lainnya: <span class="line-fill" style="width: 530px;"></span><br>
      <span class="line-fill" style="width: 100%; margin-top: 4px;"></span>
    </div>
  </div>

  <!-- 3 KOLOM TANDA TANGAN RESMI: PPL, PML, KETUA RT/RW -->
  <table class="sig-3col">
    <tr>
      <td width="32%">
        <div>Petugas Pendataan Lapangan<br><b>( PPL )</b></div>
        <div class="sig-space-large"></div>
        <div class="sig-name">( {ppl} )</div>
        <div class="sig-sub">Petugas Pencacah BPS</div>
      </td>
      <td width="34%">
        <div>Petugas Pemeriksa Lapangan<br><b>( PML )</b></div>
        <div class="sig-space-large"></div>
        <div class="sig-name">( {pml} )</div>
        <div class="sig-sub">Pengawas Lapangan BPS</div>
      </td>
      <td width="34%">
        <div>Yang Menyatakan &amp; Membuktikan,<br><b>Pengurus RT / RW / Kepala Wilayah</b></div>
        <div class="sig-space-large"></div>
        <div class="sig-name">( <span class="line-fill" style="width: 160px;"></span> )</div>
        <div class="sig-sub">Nama Terang &bull; No. HP &bull; Stempel RT</div>
      </td>
    </tr>
  </table>
</div>

</body>
</html>
"""
    return html_doc

def render_worker(task):
    code, html_path, pdf_path = task
    try:
        cmd = [
            'google-chrome-stable',
            '--headless',
            '--no-sandbox',
            '--disable-gpu',
            f'--print-to-pdf={pdf_path}',
            html_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode == 0 and os.path.exists(pdf_path):
            return code, True, None
        else:
            return code, False, res.stderr
    except Exception as e:
        return code, False, str(e)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generator PDF Lembar Verifikasi RT SE2026")
    parser.add_argument("--only-completed", action="store_true", help="Hanya memproses SLS yang 100%% Selesai (ada di subsls_selesai.csv)")
    parser.add_argument("--min-not-found", type=int, default=0, help="Batas minimal total kasus Tidak Ditemukan per SLS")
    parser.add_argument("--output-dir", type=str, default=None, help="Folder khusus output PDF (default: pdf_verifikasi_rt_completed jika --only-completed)")
    parser.add_argument("--workers", "-w", type=int, default=12, help="Jumlah worker paralel Chromium (default: 12)")
    parser.add_argument("--force", action="store_true", help="Paksa generasi ulang seluruh PDF tanpa menggunakan cache delta")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = args.output_dir
    elif args.only_completed:
        output_dir = os.path.join(BASE_DIR, 'pdf_verifikasi_rt_completed')
    else:
        output_dir = OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(TEMP_HTML_DIR, exist_ok=True)

    manifest_path = os.path.join(output_dir, '.pdf_manifest.json')
    manifest = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as mf:
                manifest = json.load(mf)
        except Exception:
            manifest = {}

    print("Membaca dan memproses data CSV...")
    alokasi, kel_by_code, us_by_code, all_codes, usaha_by_id = load_data()
    print(f"Total Sub-SLS awal di data CSV: {len(all_codes)}")

    # Load daftar subsls_selesai.csv jika --only-completed aktif
    completed_codes = set()
    subsls_selesai_file = os.path.join(BASE_DIR, 'outputs', 'subsls_selesai.csv')
    if args.only_completed and os.path.exists(subsls_selesai_file):
        with open(subsls_selesai_file, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                c = r.get('Kode Wilayah (Sub-SLS)', '').strip()
                if c:
                    completed_codes.add(c)
        print(f"Filter --only-completed aktif: {len(completed_codes)} SLS 100% selesai ditemukan.")

    tasks = []
    task_hashes = {}
    skipped_count = 0

    for code in all_codes:
        if args.only_completed and code not in completed_codes:
            continue

        kk_list = kel_by_code.get(code, [])
        us_list = us_by_code.get(code, [])
        total_not_found = len(kk_list) + len(us_list)

        if args.min_not_found > 0 and total_not_found < args.min_not_found:
            continue

        alokasi_info = alokasi.get(code, {})
        ppl_str = clean_filename_part(alokasi_info.get('PPL', 'UnknownPPL'))
        sls_str = clean_filename_part(alokasi_info.get('nmsls', 'UnknownSLS'))
        kec_str = clean_filename_part(alokasi_info.get('nmkec', 'UnknownKec'))

        # Format Penamaan: IDSLS_NamaPPL_NamaSLS_Kecamatan.pdf
        pdf_filename = f"{code}_{ppl_str}_{sls_str}_{kec_str}.pdf"
        html_filename = f"{code}.html"

        pdf_path = os.path.abspath(os.path.join(output_dir, pdf_filename))
        html_path = os.path.abspath(os.path.join(TEMP_HTML_DIR, html_filename))

        html_content = build_html_for_code(code, alokasi_info, kk_list, us_list, usaha_by_id)
        content_hash = hashlib.sha256(html_content.encode('utf-8')).hexdigest()

        # Cek cache Delta Generation
        if not args.force and os.path.exists(pdf_path) and manifest.get(code, {}).get('hash') == content_hash:
            skipped_count += 1
            continue

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        tasks.append((code, html_path, pdf_path))
        task_hashes[code] = (content_hash, pdf_filename)

    if skipped_count > 0:
        print(f"⚡ [Delta Generation] {skipped_count} PDF di-SKIP karena data tidak berubah.")

    if not tasks:
        print(f"🟢 Seluruh {skipped_count} PDF sudah mutakhir (Up to Date). Tidak ada rendering yang diperlukan.")
        return

    print(f"Memulai pencetakan massal {len(tasks)} PDF baru/diperbarui dengan multiprocessing pool ({args.workers} workers)...")
    success_count = 0
    fail_count = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(render_worker, t) for t in tasks]
        for i, future in enumerate(as_completed(futures), 1):
            code, success, err = future.result()
            if success:
                success_count += 1
                c_hash, p_file = task_hashes[code]
                manifest[code] = {'hash': c_hash, 'file': p_file}
            else:
                fail_count += 1
                print(f"[FAIL] {code}: {err}")
            
            if i % 100 == 0 or i == len(tasks):
                print(f"Progres: {i}/{len(tasks)} PDF diproses (Sukses: {success_count}, Gagal: {fail_count})")

    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)

    print(f"\n==================================================")
    print(f"SELESAI! {success_count} PDF baru/diperbarui disetujui (Skipped: {skipped_count}, Gagal: {fail_count}) di:")
    print(f"📁 {output_dir}")
    print(f"==================================================")

if __name__ == '__main__':
    main()
