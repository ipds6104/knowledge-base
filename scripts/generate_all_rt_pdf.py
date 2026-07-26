import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

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
            if code:
                kel_by_code[code].append(r)

    us_by_code = defaultdict(list)
    usaha_by_id = {}
    with open(USAHA_CSV, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            code = r.get('level_6_full_code', '').strip()
            if code:
                us_by_code[code].append(r)
            aid = r.get('assignment_id', '').strip()
            if aid:
                usaha_by_id[aid] = r

    all_codes = sorted(list(set(kel_by_code.keys()).union(us_by_code.keys())))
    return alokasi, kel_by_code, us_by_code, all_codes, usaha_by_id

def build_html_for_code(code, alokasi_info, kk_list, us_list, usaha_by_id=None):
    nmsls = alokasi_info.get('nmsls', 'Unknown SLS')
    nmkec = alokasi_info.get('nmkec', '-')
    nmdesa = alokasi_info.get('nmdesa', '-')
    kdkec = alokasi_info.get('kdkec', '-')
    kddesa = alokasi_info.get('kddesa', '-')
    ppl = alokasi_info.get('PPL', '-')
    pml = alokasi_info.get('PML', '-')
    pj = alokasi_info.get('Pj-Kuda', '-')
    target = alokasi_info.get('Target', '0')
    logo_html = get_logo_html()

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Lembar Verifikasi Lapangan - {nmsls}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm 12mm;
        }}
        body {{
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10.5px;
            color: #000;
            line-height: 1.3;
            margin: 0;
            padding: 10px;
        }}
        .kop {{
            display: flex;
            align-items: center;
            border-bottom: 3px double #000;
            padding-bottom: 6px;
            margin-bottom: 10px;
        }}
        .kop-logo {{
            width: 70px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            text-align: center;
        }}
        .kop-text {{
            flex: 1;
            text-align: center;
        }}
        .kop-text h2 {{
            margin: 0;
            font-size: 13.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .kop-text h3 {{
            margin: 2px 0 0 0;
            font-size: 11.5px;
            font-weight: bold;
            color: #111;
        }}
        .kop-text p {{
            margin: 1px 0 0 0;
            font-size: 9px;
            color: #333;
        }}
        
        .meta-box {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
        }}
        .meta-box td {{
            padding: 4px 6px;
            border: 1px solid #444;
            vertical-align: top;
            font-size: 10px;
        }}
        .meta-header {{
            background-color: #eaeaea;
            font-weight: bold;
        }}
        .badge-alert {{
            background-color: #fff0f0;
            color: #b71c1c;
            font-weight: bold;
            padding: 1px 4px;
            border: 1px solid #ffcdd2;
            border-radius: 3px;
        }}
        
        .section-title {{
            font-weight: bold;
            font-size: 10.5px;
            background-color: #1a365d;
            color: #ffffff;
            padding: 4px 8px;
            margin-top: 10px;
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
        }}
        .data-table th {{
            background-color: #f7fafc;
            border: 1px solid #333;
            padding: 5px 3px;
            font-size: 9px;
            text-align: center;
            font-weight: bold;
        }}
        .data-table td {{
            border: 1px solid #444;
            padding: 4px 4px;
            font-size: 9px;
            vertical-align: middle;
        }}
        .text-center {{ text-align: center; }}
        .chk-cell {{
            width: 28px;
            text-align: center;
            font-size: 10px;
            font-family: monospace;
        }}
        
        .catatan-box {{
            border: 1px solid #444;
            padding: 6px;
            min-height: 40px;
            margin-bottom: 10px;
            background: #fafafa;
        }}
        .catatan-title {{
            font-weight: bold;
            font-size: 9.5px;
            margin-bottom: 2px;
        }}

        .signature-grid {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            page-break-inside: avoid;
        }}
        .signature-grid td {{
            width: 33.33%;
            text-align: center;
            vertical-align: top;
            padding: 4px;
            border: none;
        }}
        .sig-space {{
            height: 55px;
        }}
        .sig-name {{
            font-weight: bold;
            text-decoration: underline;
            font-size: 10px;
        }}
        .sig-title {{
            font-size: 9.5px;
            color: #222;
        }}
    </style>
</head>
<body>

    <div class="kop">
        <div class="kop-logo">{logo_html}</div>
        <div class="kop-text">
            <h2>BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH</h2>
            <h3>LEMBAR VERIFIKASI KEBERADAAN RESPONDEN SENSUS EKONOMI 2026</h3>
            <p>Berita Acara Pembuktian Lapangan Bersama Pengurus RT &amp; Pemerintah Desa/Kelurahan (Kondisi Data per 21 Juli 2026)</p>
        </div>
    </div>

    <table class="meta-box">
        <tr>
            <td width="16%" class="meta-header">Kecamatan</td>
            <td width="34%">: <b>[{kdkec}] {nmkec}</b></td>
            <td width="18%" class="meta-header">Kode Sub-SLS (16-Digit)</td>
            <td width="32%">: <b>{code}</b></td>
        </tr>
        <tr>
            <td class="meta-header">Desa / Kelurahan</td>
            <td>: <b>[{kddesa}] {nmdesa}</b></td>
            <td class="meta-header">Petugas Pencacah (PPL)</td>
            <td>: <b>{ppl}</b></td>
        </tr>
        <tr>
            <td class="meta-header">Nama SLS / Sub-SLS</td>
            <td>: <b>{nmsls}</b></td>
            <td class="meta-header">Pengawas (PML)</td>
            <td>: <b>{pml}</b></td>
        </tr>
        <tr>
            <td class="meta-header">Target Prelist SLS</td>
            <td>: <b>{target} Responden</b></td>
            <td class="meta-header">Penanggung Jawab (PJ)</td>
            <td>: <b>{pj}</b></td>
        </tr>
        <tr>
            <td class="meta-header">Laporan Diskonfirmasi</td>
            <td colspan="3">
                : <span class="badge-alert">Keluarga Tidak Ditemukan: {len(kk_list)} KK</span> &nbsp;|&nbsp; 
                <span class="badge-alert">Usaha Tidak Ditemukan: {len(us_list)} Usaha</span> 
                <b>(Data CSV Tarikan per 21 Juli 2026: {len(kk_list)+len(us_list)} dari {target} Prelist)</b>
            </td>
        </tr>
    </table>
"""

    # BAGIAN A: KELUARGA
    if kk_list:
        html += f"""    <div class="section-title">BAGIAN A: DAFTAR KELUARGA (KK) DILAPORKAN "TIDAK DITEMUKAN" ({len(kk_list)} KK)</div>
    <table class="data-table">
        <thead>
            <tr>
                <th width="4%">No</th>
                <th width="24%">Nama Kepala Keluarga (KK)</th>
                <th width="18%">NIK / No. KK Prelist</th>
                <th width="24%">Alamat Prelist / Domisili</th>
                <th width="6%">Ada</th>
                <th width="6%">Tdk Ada</th>
                <th width="6%">Pindah</th>
                <th width="12%">Catatan RT</th>
            </tr>
        </thead>
        <tbody>
"""
        if usaha_by_id is None:
            usaha_by_id = {}

        for idx, r in enumerate(kk_list, 1):
            raw_name = (r.get('data1') or r.get('nama_kk') or r.get('dtsen_nama_kk') or '').strip()
            code_id = (r.get('code_identity') or r.get('nik_kk') or r.get('no_kk') or '-').strip()
            alamat = (r.get('data2') or r.get('alamat_klrg') or r.get('alamat_prelist') or '-').strip()

            if raw_name:
                nama_kk = raw_name
            else:
                aid = r.get('assignment_id', '').strip()
                u_info = usaha_by_id.get(aid, {})
                u_name = (u_info.get('nama_usaha') or u_info.get('nama_komersial') or '').strip()
                if u_name:
                    nama_kk = u_name
                elif 'UMK' in code_id:
                    nama_kk = '[Sampel Prelist UMK]'
                else:
                    nama_kk = '[Sampel Prelist]'

            html += f"""            <tr>
                <td class="text-center">{idx}</td>
                <td><b>{nama_kk}</b></td>
                <td class="text-center">{code_id}</td>
                <td>{alamat}</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td></td>
            </tr>
"""
        html += "        </tbody>\n    </table>\n"

    # BAGIAN B: USAHA
    if us_list:
        html += f"""    <div class="section-title">BAGIAN B: DAFTAR USAHA / PERUSAHAAN DILAPORKAN "TIDAK DITEMUKAN" ({len(us_list)} USAHA)</div>
    <table class="data-table">
        <thead>
            <tr>
                <th width="4%">No</th>
                <th width="24%">Nama Usaha / Komersial</th>
                <th width="18%">Nama Pengusaha / NIK</th>
                <th width="24%">Alamat Usaha / Lokasi</th>
                <th width="6%">Ada</th>
                <th width="6%">Tdk Ada</th>
                <th width="6%">Pindah</th>
                <th width="12%">Catatan RT</th>
            </tr>
        </thead>
        <tbody>
"""
        for idx, r in enumerate(us_list, 1):
            nama_us = r.get('nama_usaha') or r.get('nama_komersial') or '-'
            pengusaha = r.get('pengusaha') or r.get('nik_pengusaha') or '-'
            alamat_us = r.get('alamat_usaha') or r.get('alamat_usaha_utama') or '-'
            skala = r.get('skala_usaha') or 'UMK'
            html += f"""            <tr>
                <td class="text-center">{idx}</td>
                <td><b>{nama_us}</b> <small style="color:#555">({skala})</small></td>
                <td>{pengusaha}</td>
                <td>{alamat_us}</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td class="chk-cell">[ &nbsp; ]</td>
                <td></td>
            </tr>
"""
        html += "        </tbody>\n    </table>\n"

    html += """    <div class="catatan-box">
        <div class="catatan-title">BLOK III. CATATAN &amp; KETERANGAN TAMBAHAN KETUA RT / LURAH:</div>
        <span style="color:#777; font-style:italic; font-size:9px;">(Tuliskan keterangan mengenai kondisi keberadaan lokasi usaha/keluarga, kunjungan PPL, atau penjelasan kepindahan responden)</span>
    </div>

    <table class="signature-grid">
        <tr>
            <td width="33%">
                <div class="sig-title">Petugas Verifikator BPS</div>
                <div class="sig-space"></div>
                <div class="sig-name">( __________________________ )</div>
            </td>
            <td width="34%">
                <div class="sig-title">Pengurus RT / Kepala Wilayah Setempat</div>
                <div class="sig-space"></div>
                <div class="sig-name">( __________________________ )</div>
                <div class="sig-title">Stempel RT / No. HP:</div>
            </td>
            <td width="33%">
                <div class="sig-title">Mengetahui / Mengesahkan:<br><b>Kepala Desa / Lurah Setempat</b></div>
                <div class="sig-space"></div>
                <div class="sig-name">( __________________________ )</div>
                <div class="sig-title">Stempel Basah Desa / Kelurahan</div>
            </td>
        </tr>
    </table>

</body>
</html>
"""
    return html

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

    print(f"Memulai pencetakan massal {len(tasks)} PDF baru/diperbarui dengan multiprocessing pool (8 workers)...")
    success_count = 0
    fail_count = 0

    with ProcessPoolExecutor(max_workers=8) as executor:
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
