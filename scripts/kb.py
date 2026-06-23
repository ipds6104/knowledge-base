#!/usr/bin/env python3
import os
import sys
import argparse
import re
import json
import base64
import glob
import subprocess
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# --- YAML PARSER & DUMPER (Pure Python, Zero Dependency) ---

def parse_yaml(yaml_str):
    metadata = {}
    lines = yaml_str.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            i += 1
            continue
        
        # Check for list key (e.g. "deadlines:")
        if stripped.endswith(':'):
            key = stripped[:-1].strip()
            i += 1
            list_items = []
            while i < len(lines) and (lines[i].startswith(' ') or lines[i].startswith('\t') or not lines[i].strip()):
                l = lines[i]
                if not l.strip():
                    i += 1
                    continue
                cleaned = l.strip()
                if cleaned.startswith('-'):
                    item = {}
                    val = cleaned[1:].strip()
                    if ':' in val:
                        k, v = val.split(':', 1)
                        item[k.strip()] = v.strip().strip('"\'')
                    
                    # Read subsequent keys for this dictionary item
                    i += 1
                    while i < len(lines) and lines[i].startswith(' ') and not lines[i].strip().startswith('-'):
                        sub_line = lines[i].strip()
                        if sub_line and ':' in sub_line:
                            k, v = sub_line.split(':', 1)
                            item[k.strip()] = v.strip().strip('"\'')
                        i += 1
                    list_items.append(item)
                    continue
                else:
                    i += 1
            metadata[key] = list_items
            continue
        
        # Standard key-value
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip()] = val.strip().strip('"\'')
        i += 1
    return metadata

def dump_yaml(metadata):
    lines = []
    for k, v in metadata.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                if isinstance(item, dict):
                    keys = list(item.keys())
                    if keys:
                        first_key = keys[0]
                        lines.append(f"  - {first_key}: \"{item[first_key]}\"")
                        for sub_k in keys[1:]:
                            lines.append(f"    {sub_k}: \"{item[sub_k]}\"")
                else:
                    lines.append(f"  - \"{item}\"")
        else:
            lines.append(f"{k}: \"{v}\"")
    return "\n".join(lines)

def read_markdown_file(file_path):
    path = Path(file_path)
    if not path.exists():
        return {}, ""
    
    content = path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    metadata = parse_yaml(parts[1])
    body = parts[2].lstrip()
    return metadata, body

def write_markdown_file(file_path, metadata, body):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = dump_yaml(metadata)
    full_content = f"---\n{yaml_str}\n---\n{body}"
    path.write_text(full_content, encoding='utf-8')

# --- CONFIG & HELPERS ---

def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    config = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()
    return config

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

# --- COLOR DEFINITIONS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- CLI COMMAND IMPLEMENTATIONS ---

def cmd_create(args):
    slug_name = slugify(args.nama)
    period_path = Path('kegiatan') / slug_name / args.periode
    readme_path = period_path / 'README.md'
    
    if readme_path.exists() and not args.force:
        print(f"{Colors.FAIL}Error: Kegiatan '{args.nama}' periode '{args.periode}' sudah ada di {readme_path}. Gunakan --force untuk menimpa.{Colors.ENDC}")
        sys.exit(1)
        
    metadata = {
        "nama": args.nama,
        "kategori": args.kategori,
        "rutinitas": args.rutinitas,
        "frekuensi": args.frekuensi,
        "peran": args.peran,
        "status": "aktif",
        "deadlines": [
            {
                "tanggal": datetime.now().strftime("%Y-%m-%d"),
                "kegiatan": "Kick-off / Persiapan awal",
                "status": "belum"
            }
        ]
    }
    
    body = f"# {args.nama} ({args.periode})\n\n## Deskripsi Kegiatan\nTambahkan detail deskripsi kegiatan di sini.\n\n## Catatan Pelaksanaan\nTambahkan catatan penting pelaksanaan di sini.\n"
    
    write_markdown_file(readme_path, metadata, body)
    print(f"{Colors.GREEN}Sukses membuat kegiatan baru!{Colors.ENDC}")
    print(f"Path: {readme_path}")
    print(f"Metadata:")
    print(dump_yaml(metadata))

def cmd_list(args):
    readmes = glob.glob('kegiatan/*/*/README.md')
    if not readmes:
        print(f"{Colors.WARNING}Tidak ada kegiatan yang ditemukan.{Colors.ENDC}")
        return
    
    activities = []
    for r_path in readmes:
        p = Path(r_path)
        periode = p.parent.name
        metadata, _ = read_markdown_file(r_path)
        if metadata:
            activities.append({
                "path": r_path,
                "nama": metadata.get("nama", p.parent.parent.name),
                "periode": periode,
                "kategori": metadata.get("kategori", "N/A"),
                "frekuensi": metadata.get("frekuensi", "N/A"),
                "peran": metadata.get("peran", "N/A"),
                "status": metadata.get("status", "N/A")
            })
            
    # Sort by name and period
    activities.sort(key=lambda x: (x["nama"], x["periode"]))
    
    # Print Table
    header = f"| {'Nama Kegiatan':<25} | {'Periode':<8} | {'Kategori':<11} | {'Frekuensi':<10} | {'Peran':<8} | {'Status':<8} |"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    for act in activities:
        status_color = Colors.GREEN if act['status'].lower() == 'selesai' else Colors.BLUE
        status_str = f"{status_color}{act['status'].upper()}{Colors.ENDC}"
        # Adjusting width dynamically taking color characters into account
        # We write helper print to not mess with length of status string containing ANSI codes
        print(f"| {act['nama'][:25]:<25} | {act['periode']:<8} | {act['kategori']:<11} | {act['frekuensi']:<10} | {act['peran']:<8} | {status_str:<17} |")
    print(divider)

def cmd_schedule(args):
    readmes = glob.glob('kegiatan/*/*/README.md')
    deadlines = []
    
    today = datetime.now().date()
    
    for r_path in readmes:
        p = Path(r_path)
        metadata, _ = read_markdown_file(r_path)
        if metadata and "deadlines" in metadata:
            for dl in metadata["deadlines"]:
                tgl_str = dl.get("tanggal")
                if not tgl_str:
                    continue
                try:
                    tgl = datetime.strptime(tgl_str, "%Y-%m-%d").date()
                except ValueError:
                    continue
                deadlines.append({
                    "nama_kegiatan": metadata.get("nama", p.parent.parent.name),
                    "periode": p.parent.name,
                    "tanggal": tgl,
                    "kegiatan": dl.get("kegiatan", ""),
                    "status": dl.get("status", "belum")
                })
                
    if not deadlines:
        print(f"{Colors.WARNING}Tidak ada deadline yang tercatat.{Colors.ENDC}")
        return
        
    # Sort deadlines by date
    deadlines.sort(key=lambda x: x["tanggal"])
    
    # Calculate Date Ranges
    # We define week range (Monday to Sunday)
    weekday = today.weekday()
    start_of_week = today - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=6)
    
    start_of_next_week = start_of_week + timedelta(days=7)
    end_of_next_week = start_of_next_week + timedelta(days=6)
    
    start_of_month = today.replace(day=1)
    # Next month calculation
    if start_of_month.month == 12:
        end_of_month = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month+1, day=1) - timedelta(days=1)

    # Filtering
    filtered = []
    title_text = "SEMUA DEADLINE"
    
    if args.week:
        filtered = [d for d in deadlines if start_of_week <= d["tanggal"] <= end_of_week]
        title_text = f"DEADLINE MINGGU INI ({start_of_week.strftime('%d %b %Y')} - {end_of_week.strftime('%d %b %Y')})"
    elif args.month:
        filtered = [d for d in deadlines if start_of_month <= d["tanggal"] <= end_of_month]
        title_text = f"DEADLINE BULAN INI ({start_of_month.strftime('%d %b %Y')} - {end_of_month.strftime('%d %b %Y')})"
    elif args.overdue:
        filtered = [d for d in deadlines if d["tanggal"] < today and d["status"].lower() != 'selesai']
        title_text = "DEADLINE OVERDUE (TERLEWAT & BELUM SELESAI)"
    else:
        filtered = deadlines
        
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== {title_text} ==={Colors.ENDC}\n")
    
    if not filtered:
        print("Tidak ada jadwal yang sesuai filter.")
        return
        
    # Group by date for nice printing
    current_date = None
    for dl in filtered:
        if dl["tanggal"] != current_date:
            current_date = dl["tanggal"]
            day_name = current_date.strftime("%A")
            # Translate to Indonesian day names
            translations = {
                "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
                "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
            }
            ind_day = translations.get(day_name, day_name)
            print(f"\n{Colors.BOLD}{Colors.CYAN}[{ind_day.upper()}, {current_date.strftime('%d %b %Y')}]{Colors.ENDC}")
            
        status_char = "[ ]"
        status_color = Colors.BLUE
        if dl["status"].lower() == 'selesai':
            status_char = "[x]"
            status_color = Colors.GREEN
        elif dl["tanggal"] < today:
            status_char = "[OVERDUE]"
            status_color = Colors.FAIL
            
        print(f"  {status_color}{status_char}{Colors.ENDC} {dl['nama_kegiatan']} ({dl['periode']}): {dl['kegiatan']}")
    print()

def cmd_convert(args):
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"{Colors.FAIL}Error: Berkas PDF tidak ditemukan di {pdf_path}{Colors.ENDC}")
        sys.exit(1)
        
    output_md = pdf_path.with_suffix('.md')
    
    if args.ai:
        print(f"{Colors.BLUE}Memulai konversi PDF menggunakan AI Vision (Gemini Proxy)...{Colors.ENDC}")
        
        # Load API Configs
        config = load_env()
        api_url = config.get("AI_PROXY_URL")
        api_key = config.get("AI_API_KEY")
        model = config.get("AI_MODEL", "gemini-3-flash")
        
        if not api_url or not api_key:
            print(f"{Colors.FAIL}Error: API proxy tidak terkonfigurasi. Pastikan berkas .env terisi dengan benar.{Colors.ENDC}")
            sys.exit(1)
            
        print(f"Menggunakan Model: {model}")
        
        # 1. Convert PDF pages to images using pdftoppm
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Mengekstrak halaman PDF menjadi gambar di folder temp...")
            prefix = os.path.join(tmpdir, "page")
            
            try:
                subprocess.run(["pdftoppm", "-png", "-r", "150", str(pdf_path), prefix], check=True)
            except subprocess.SubprocessError as e:
                print(f"{Colors.FAIL}Error saat mengekstrak halaman PDF: {e}{Colors.ENDC}")
                sys.exit(1)
                
            image_files = sorted(glob.glob(os.path.join(tmpdir, "page-*.png")))
            if not image_files:
                print(f"{Colors.FAIL}Error: Tidak ada gambar halaman yang berhasil diekstrak.{Colors.ENDC}")
                sys.exit(1)
                
            print(f"Ditemukan {len(image_files)} halaman untuk diproses.")
            
            markdown_pages = []
            for idx, img_path in enumerate(image_files, 1):
                print(f"Memproses halaman {idx} dari {len(image_files)}...")
                
                with open(img_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Construct OpenAI compatible payload
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "Convert this document page image to Markdown format. "
                                        "Preserve layout, headings, lists, tables (using pipe tables), and exact text. "
                                        "Do not include code block wrappers like ```markdown in the output, just raw markdown."
                                    )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "temperature": 0.1
                }
                
                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    method="POST"
                )
                
                try:
                    with urllib.request.urlopen(req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        text = res_data["choices"][0]["message"]["content"]
                        markdown_pages.append(text)
                except urllib.error.URLError as e:
                    print(f"{Colors.FAIL}API Error di Halaman {idx}: {e}{Colors.ENDC}")
                    sys.exit(1)
                except Exception as e:
                    print(f"{Colors.FAIL}Error tidak dikenal di Halaman {idx}: {e}{Colors.ENDC}")
                    sys.exit(1)
            
            # Combine Markdown pages
            full_markdown = "\n\n<!-- PAGE BREAK -->\n\n".join(markdown_pages)
            output_md.write_text(full_markdown, encoding='utf-8')
            
    else:
        print(f"{Colors.BLUE}Memulai konversi cepat PDF menggunakan pdftotext...{Colors.ENDC}")
        try:
            subprocess.run(["pdftotext", "-layout", str(pdf_path), str(output_md)], check=True)
        except subprocess.SubprocessError as e:
            print(f"{Colors.FAIL}Error: pdftotext gagal melakukan konversi: {e}{Colors.ENDC}")
            sys.exit(1)
            
    print(f"{Colors.GREEN}Sukses! Hasil konversi disimpan di: {output_md}{Colors.ENDC}")

# --- MAIN ---

def cmd_se_monitor(args):
    import csv
    import urllib.request
    import io
    from pathlib import Path

    # 1. Paths & File Checks
    csv_path = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")
    cache_csv_path = Path("kegiatan/sensus-ekonomi-2026/2026/Realisasi - 6104.csv")

    SHEET_URL = "https://docs.google.com/spreadsheets/d/1JNwyb7TsPmSsGl3o1zNTSc-3wzFwIr_t3HPz_a1CVVQ/export?format=csv&gid=1834012774"
    
    sheet_map = {}
    data_source_info = ""

    # Try downloading from Google Sheets
    try:
        print(f"{Colors.BLUE}Mengunduh progres terbaru dari Google Sheets...{Colors.ENDC}")
        req = urllib.request.Request(
            SHEET_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            csv_text = response.read().decode('utf-8')
            
        # Parse downloaded CSV
        reader_sheet = csv.DictReader(io.StringIO(csv_text))
        for row in reader_sheet:
            code = row.get("Kode Wilayah (Sub-SLS)", "").strip()
            if code:
                sheet_map[code] = {
                    "Total Target": int(row.get("Total Target", 0) or 0),
                    "OPEN": int(row.get("OPEN", 0) or 0),
                    "DRAFT": int(row.get("DRAFT", 0) or 0),
                    "SUBMITTED BY Pencacah": int(row.get("SUBMITTED BY Pencacah", 0) or 0),
                    "APPROVED BY Pengawas": int(row.get("APPROVED BY Pengawas", 0) or 0),
                    "SUBMITTED RESPONDENT": int(row.get("SUBMITTED RESPONDENT", 0) or 0),
                    "REJECTED BY Pengawas": int(row.get("REJECTED BY Pengawas", 0) or 0)
                }
        
        # Save to local cache
        try:
            cache_csv_path.write_text(csv_text, encoding='utf-8')
            data_source_info = "Google Sheets (Real-time)"
        except Exception as cache_err:
            print(f"{Colors.WARNING}Peringatan: Gagal menyimpan cache lokal: {cache_err}{Colors.ENDC}")
            data_source_info = "Google Sheets (Real-time, Gagal Cache)"

    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal mengunduh dari Google Sheets ({e}). Mencoba membaca cache lokal...{Colors.ENDC}")
        
        # Fallback: Local Cache CSV only
        if cache_csv_path.exists():
            try:
                with open(cache_csv_path, 'r', encoding='utf-8') as f:
                    csv_text = f.read()
                reader_sheet = csv.DictReader(io.StringIO(csv_text))
                for row in reader_sheet:
                    code = row.get("Kode Wilayah (Sub-SLS)", "").strip()
                    if code:
                        sheet_map[code] = {
                            "Total Target": int(row.get("Total Target", 0) or 0),
                            "OPEN": int(row.get("OPEN", 0) or 0),
                            "DRAFT": int(row.get("DRAFT", 0) or 0),
                            "SUBMITTED BY Pencacah": int(row.get("SUBMITTED BY Pencacah", 0) or 0),
                            "APPROVED BY Pengawas": int(row.get("APPROVED BY Pengawas", 0) or 0),
                            "SUBMITTED RESPONDENT": int(row.get("SUBMITTED RESPONDENT", 0) or 0),
                            "REJECTED BY Pengawas": int(row.get("REJECTED BY Pengawas", 0) or 0)
                        }
                data_source_info = "Cache Lokal (Realisasi - 6104.csv)"
            except Exception as read_err:
                print(f"{Colors.FAIL}Error: Gagal membaca cache lokal: {read_err}{Colors.ENDC}")
        
        if not sheet_map:
            print(f"{Colors.FAIL}Error: Tidak ada data progres dari Google Sheets maupun cache lokal.{Colors.ENDC}")
            print("Pastikan komputer Anda terhubung ke internet untuk penarikan data pertama kali.")
            sys.exit(1)

    # 2. Timeline & expected progress calculations
    start_date = datetime.strptime("2026-06-15", "%Y-%m-%d").date()
    target_date = datetime.strptime("2026-08-15", "%Y-%m-%d").date()
    today_date = datetime.now().date()
    
    # 2. Timeline & expected progress calculations
    start_date = datetime.strptime("2026-06-15", "%Y-%m-%d").date()
    target_date = datetime.strptime("2026-08-15", "%Y-%m-%d").date()
    today_date = datetime.now().date()
    
    total_days = (target_date - start_date).days # 61 days
    elapsed_days = (today_date - start_date).days
    elapsed_days_bounded = max(0, min(total_days, elapsed_days))
    expected_pct = (elapsed_days_bounded / total_days) * 100 if total_days > 0 else 100.0

    def get_target_status(actual_pct):
        if actual_pct >= expected_pct:
            return f"{Colors.GREEN}🟢 ON TARGET{Colors.ENDC}"
        elif actual_pct >= expected_pct - 2.0 or actual_pct >= expected_pct * 0.85:
            return f"{Colors.WARNING}🟡 WARNING (Slightly Behind){Colors.ENDC}"
        else:
            return f"{Colors.FAIL}🔴 BEHIND TARGET{Colors.ENDC}"

    def get_est_completion(actual_pct):
        if elapsed_days > 0 and actual_pct > 0:
            daily_speed = actual_pct / elapsed_days
            remaining_pct = 100.0 - actual_pct
            est_days_left = remaining_pct / daily_speed
            est_completion_date = today_date + timedelta(days=est_days_left)
            est_completion_str = est_completion_date.strftime("%d %b %Y")
            
            if est_completion_date <= target_date:
                est_color = Colors.GREEN
            elif est_completion_date <= datetime.strptime("2026-08-31", "%Y-%m-%d").date():
                est_color = Colors.WARNING
            else:
                est_color = Colors.FAIL
            return f"{est_color}{est_completion_str}{Colors.ENDC}"
        else:
            return f"{Colors.FAIL}Tidak Terprediksi (Belum Ada Progres){Colors.ENDC}"

    # 3. Progress calculations helper
    def get_sls_metrics(idsls, idsubsls):
        row = sheet_map.get(idsubsls)
        if not row:
            # Fallback 14-digit match
            for k in sheet_map:
                if k.startswith(idsls):
                    row = sheet_map[k]
                    break
        
        if not row:
            return {
                "target": 0, "open": 0, "draft": 0, "submitted": 0,
                "approved": 0, "resp_submitted": 0, "rejected": 0,
                "completed": 0, "worked": 0
            }
            
        target = row["Total Target"]
        open_count = row["OPEN"]
        draft_count = row["DRAFT"]
        submitted_count = row["SUBMITTED BY Pencacah"]
        approved_count = row["APPROVED BY Pengawas"]
        resp_submitted = row["SUBMITTED RESPONDENT"]
        rejected_count = row["REJECTED BY Pengawas"]
        
        completed = submitted_count + approved_count + resp_submitted
        worked = completed + draft_count
        return {
            "target": target,
            "open": open_count,
            "draft": draft_count,
            "submitted": submitted_count,
            "approved": approved_count,
            "resp_submitted": resp_submitted,
            "rejected": rejected_count,
            "completed": completed,
            "worked": worked
        }

    def aggregate_metrics(sls_list):
        agg = {
            "target": 0, "open": 0, "draft": 0, "submitted": 0,
            "approved": 0, "resp_submitted": 0, "rejected": 0,
            "completed": 0, "worked": 0, "sls_count": len(sls_list)
        }
        for idsls in sls_list:
            idsubsls = sls_info[idsls]["idsubsls"]
            m = get_sls_metrics(idsls, idsubsls)
            for k in agg:
                if k != "sls_count":
                    agg[k] += m[k]
        
        agg["completed_rate"] = agg["completed"] / agg["target"] if agg["target"] > 0 else 0.0
        agg["worked_rate"] = agg["worked"] / agg["target"] if agg["target"] > 0 else 0.0
        agg["approval_rate"] = agg["approved"] / (agg["approved"] + agg["submitted"]) if (agg["approved"] + agg["submitted"]) > 0 else 0.0
        return agg

    # 4. Read CSV and build hierarchy if present
    pj_kuda_groups = {}  # Pj-Kuda -> PML -> PPL -> [SLS]
    sls_info = {}
    has_alokasi = False
    
    if csv_path.exists():
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    idsls = row.get("idsls")
                    idsubsls = row.get("idsubsls")
                    if not idsls:
                        continue
                    pj = row.get("Pj-Kuda", "").strip()
                    pml = row.get("PML", "").strip()
                    ppl = row.get("PPL", "").strip()
                    nmsls = row.get("nmsls", "").strip()
                    
                    sls_info[idsls] = {
                        "nmsls": nmsls,
                        "ppl": ppl,
                        "pml": pml,
                        "pj": pj,
                        "idsubsls": idsubsls
                    }
                    
                    if pj not in pj_kuda_groups:
                        pj_kuda_groups[pj] = {}
                    if pml not in pj_kuda_groups[pj]:
                        pj_kuda_groups[pj][pml] = {}
                    if ppl not in pj_kuda_groups[pj][pml]:
                        pj_kuda_groups[pj][pml][ppl] = []
                    pj_kuda_groups[pj][pml][ppl].append(idsls)
            has_alokasi = True
        except Exception as e:
            if not args.prov:
                print(f"{Colors.FAIL}Error saat membaca file CSV: {e}{Colors.ENDC}")
                sys.exit(1)

    # 5. Calculate global stats (Kabupaten Mempawah) if alokasi present
    pj_summaries = []
    kab_avg_completed = 0.0
    kab_avg_worked = 0.0
    kab_avg_approval = 0.0
    
    if has_alokasi:
        for pj, pmls in pj_kuda_groups.items():
            if not pj:
                continue
            all_sls = []
            for pml, ppls in pmls.items():
                for ppl, sls_list in ppls.items():
                    all_sls.extend(sls_list)
            agg = aggregate_metrics(all_sls)
            agg["pj"] = pj
            pj_summaries.append(agg)

        total_target = sum(p["target"] for p in pj_summaries)
        total_completed = sum(p["completed"] for p in pj_summaries)
        total_worked = sum(p["worked"] for p in pj_summaries)
        total_approved = sum(p["approved"] for p in pj_summaries)
        total_submitted = sum(p["submitted"] for p in pj_summaries)

        kab_avg_completed = total_completed / total_target if total_target > 0 else 0.0
        kab_avg_worked = total_worked / total_target if total_target > 0 else 0.0
        kab_avg_approval = total_approved / (total_approved + total_submitted) if (total_approved + total_submitted) > 0 else 0.0
        pj_summaries.sort(key=lambda x: x["completed_rate"], reverse=True)

    # 6. Aggregate Kalbar Province data from csv_text
    kab_data = {}
    reader_prov = csv.DictReader(io.StringIO(csv_text))
    for row in reader_prov:
        kab = row.get("Kab/Kota", "").strip()
        if not kab:
            continue
        
        target = int(row.get("Total Target", 0) or 0)
        open_count = int(row.get("OPEN", 0) or 0)
        draft_count = int(row.get("DRAFT", 0) or 0)
        submitted = int(row.get("SUBMITTED BY Pencacah", 0) or 0)
        approved = int(row.get("APPROVED BY Pengawas", 0) or 0)
        resp_submitted = int(row.get("SUBMITTED RESPONDENT", 0) or 0)
        
        completed = submitted + approved + resp_submitted
        worked = completed + draft_count
        
        if kab not in kab_data:
            kab_data[kab] = {
                "target": 0, "open": 0, "draft": 0, "submitted": 0,
                "approved": 0, "completed": 0, "worked": 0
            }
        
        kab_data[kab]["target"] += target
        kab_data[kab]["open"] += open_count
        kab_data[kab]["draft"] += draft_count
        kab_data[kab]["submitted"] += submitted
        kab_data[kab]["approved"] += approved
        kab_data[kab]["completed"] += completed
        kab_data[kab]["worked"] += worked

    kab_list = []
    for kab, m in kab_data.items():
        if m["target"] == 0:
            continue
        m["completed_rate"] = m["completed"] / m["target"]
        m["worked_rate"] = m["worked"] / m["target"]
        m["approval_rate"] = m["approved"] / (m["approved"] + m["submitted"]) if (m["approved"] + m["submitted"]) > 0 else 0.0
        kab_list.append((kab, m))

    kab_list.sort(key=lambda x: x[1]["completed_rate"], reverse=True)

    prov_target = sum(m["target"] for m in kab_data.values())
    prov_completed = sum(m["completed"] for m in kab_data.values())
    prov_worked = sum(m["worked"] for m in kab_data.values())
    prov_approved = sum(m["approved"] for m in kab_data.values())
    prov_submitted = sum(m["submitted"] for m in kab_data.values())

    prov_done_rate = prov_completed / prov_target if prov_target > 0 else 0.0
    prov_worked_rate = prov_worked / prov_target if prov_target > 0 else 0.0
    prov_approval_rate = prov_approved / (prov_approved + prov_submitted) if (prov_approved + prov_submitted) > 0 else 0.0

    prov_actual_pct = prov_done_rate * 100

    # 7. Compile History Snapshot & Compare Delta
    history_path = Path("kegiatan/sensus-ekonomi-2026/2026/monitoring_history.json")

    def load_history():
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
            except Exception as he:
                print(f"{Colors.WARNING}Peringatan: Gagal membaca riwayat ({he}){Colors.ENDC}")
        return []

    def save_history(history_list):
        try:
            history_path.parent.mkdir(parents=True, exist_ok=True)
            with open(history_path, 'w', encoding='utf-8') as fh:
                json.dump(history_list, fh, indent=2, ensure_ascii=False)
        except Exception as se:
            print(f"{Colors.WARNING}Peringatan: Gagal menyimpan riwayat ({se}){Colors.ENDC}")

    current_snapshot = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prov": {
            "completed": prov_completed,
            "worked": prov_worked,
            "target": prov_target,
            "approved": prov_approved,
            "submitted": prov_submitted
        },
        "kab": {}
    }
    
    for kab, m in kab_data.items():
        current_snapshot["kab"][kab] = {
            "completed": m["completed"],
            "worked": m["worked"],
            "target": m["target"],
            "approved": m["approved"],
            "submitted": m["submitted"]
        }

    if has_alokasi:
        current_snapshot["pj"] = {}
        for p in pj_summaries:
            current_snapshot["pj"][p["pj"]] = {
                "completed": p["completed"],
                "worked": p["worked"],
                "target": p["target"],
                "approved": p["approved"],
                "submitted": p["submitted"]
            }
            
        current_snapshot["pml_pending"] = {}
        current_snapshot["ppl_completed"] = {}
        for pj_name, pmls in pj_kuda_groups.items():
            for pml_name, ppls in pmls.items():
                pml_sls = []
                for ppl_name, sls_list in ppls.items():
                    ppl_agg = aggregate_metrics(sls_list)
                    # Store as dict so we can attach supervisor info (epistemological fix)
                    current_snapshot["ppl_completed"][ppl_name] = {
                        "completed": ppl_agg["completed"],
                        "pml": pml_name,
                        "pj": pj_name,
                    }
                    pml_sls.extend(sls_list)
                pml_agg = aggregate_metrics(pml_sls)
                # PJ source is directly from Alokasi Petugas.csv — no guessing
                current_snapshot["pml_pending"][pml_name] = {
                    "pending": pml_agg["submitted"],
                    "pj": pj_name,
                }

    history_list = load_history()
    latest_history = history_list[-1] if history_list else None

    # Save snapshot if there are actual changes
    should_save = True
    if latest_history:
        l_prov = latest_history.get("prov", {})
        c_prov = current_snapshot["prov"]
        if l_prov.get("completed") == c_prov["completed"] and l_prov.get("worked") == c_prov["worked"]:
            l_pml = latest_history.get("pml_pending", {})
            c_pml = current_snapshot.get("pml_pending", {})
            if l_pml == c_pml:
                should_save = False

    if should_save:
        history_list.append(current_snapshot)
        if len(history_list) > 100:
            history_list = history_list[-100:]
        save_history(history_list)

    # Print comparison delta
    if latest_history:
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔄 PERBANDINGAN DENGAN PENGECEKAN TERAKHIR ({latest_history.get('timestamp')}){Colors.ENDC}")
        print("-" * 115)
        
        # Prov Delta
        l_prov = latest_history.get("prov", {})
        if l_prov:
            c_pct = prov_actual_pct
            l_pct = (l_prov["completed"] / l_prov["target"] * 100) if l_prov.get("target", 0) > 0 else 0.0
            diff_pct = c_pct - l_pct
            diff_pct_str = f"+{diff_pct:.2f}%" if diff_pct >= 0 else f"{diff_pct:.2f}%"
            color = Colors.GREEN if diff_pct > 0 else Colors.ENDC
            print(f" * Progres Prov. Kalbar    : {l_pct:.2f}% -> {Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({color}{diff_pct_str}{Colors.ENDC})")
            
        # Mempawah Delta
        c_memp = current_snapshot["kab"].get("MEMPAWAH")
        l_memp = latest_history.get("kab", {}).get("MEMPAWAH")
        if c_memp and l_memp:
            c_pct = (c_memp["completed"] / c_memp["target"] * 100) if c_memp["target"] > 0 else 0.0
            l_pct = (l_memp["completed"] / l_memp["target"] * 100) if l_memp.get("target", 0) > 0 else 0.0
            diff_pct = c_pct - l_pct
            diff_pct_str = f"+{diff_pct:.2f}%" if diff_pct >= 0 else f"{diff_pct:.2f}%"
            color = Colors.GREEN if diff_pct > 0 else Colors.ENDC
            print(f" * Progres Kab. Mempawah   : {l_pct:.2f}% -> {Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({color}{diff_pct_str}{Colors.ENDC})")
            
        # Target PJ Delta
        target_pj_name = args.pj
        c_pj = current_snapshot.get("pj", {}).get(target_pj_name)
        l_pj = latest_history.get("pj", {}).get(target_pj_name)
        if c_pj and l_pj:
            c_pct = (c_pj["completed"] / c_pj["target"] * 100) if c_pj["target"] > 0 else 0.0
            l_pct = (l_pj["completed"] / l_pj["target"] * 100) if l_pj.get("target", 0) > 0 else 0.0
            diff_pct = c_pct - l_pct
            diff_pct_str = f"+{diff_pct:.2f}%" if diff_pct >= 0 else f"{diff_pct:.2f}%"
            color = Colors.GREEN if diff_pct > 0 else Colors.ENDC
            print(f" * Progres Tim PJ {target_pj_name[:15]}: {l_pct:.2f}% -> {Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({color}{diff_pct_str}{Colors.ENDC})")
            
        # PML pending changes — PJ info sourced from Alokasi Petugas.csv via snapshot
        c_pmls = current_snapshot.get("pml_pending", {})
        l_pmls = latest_history.get("pml_pending", {})
        pml_diffs = []
        for pml, c_val in c_pmls.items():
            # Support both old (int) and new (dict) snapshot format
            c_pend = c_val["pending"] if isinstance(c_val, dict) else c_val
            c_pj   = c_val["pj"]      if isinstance(c_val, dict) else ""
            l_val  = l_pmls.get(pml, c_val)
            l_pend = l_val["pending"]  if isinstance(l_val, dict) else l_val
            diff = c_pend - l_pend
            if diff != 0:
                pml_diffs.append((pml, c_pend, diff, c_pj))

        if pml_diffs:
            print("\n Perubahan Antrean PML:")
            for pml, c_pend, diff, c_pj in sorted(pml_diffs, key=lambda x: abs(x[2]), reverse=True)[:5]:
                diff_str = f"+{diff}" if diff > 0 else f"{diff}"
                color = Colors.GREEN if diff < 0 else Colors.FAIL
                pj_short = c_pj.split()[0] if c_pj else ""
                pj_tag = f" (PJ {pj_short})" if pj_short else ""
                print(f"   - PML {pml:<25}{pj_tag}: {c_pend} pending ({color}{diff_str} berkas{Colors.ENDC})")

        # PPL completed changes — PML info sourced from Alokasi Petugas.csv via snapshot
        c_ppls = current_snapshot.get("ppl_completed", {})
        l_ppls = latest_history.get("ppl_completed", {})
        ppl_diffs = []
        for ppl, c_val in c_ppls.items():
            c_comp = c_val["completed"] if isinstance(c_val, dict) else c_val
            c_pml  = c_val.get("pml", "") if isinstance(c_val, dict) else ""
            l_val  = l_ppls.get(ppl, c_val)
            l_comp = l_val["completed"] if isinstance(l_val, dict) else l_val
            diff = c_comp - l_comp
            if diff > 0:
                ppl_diffs.append((ppl, c_comp, diff, c_pml))

        if ppl_diffs:
            print("\n Kemajuan PPL Teratas:")
            for ppl, c_comp, diff, c_pml in sorted(ppl_diffs, key=lambda x: x[2], reverse=True)[:5]:
                pml_tag = f" (PML {c_pml})" if c_pml else ""
                print(f"   - PPL {ppl:<25}{pml_tag}: +{diff} dokumen selesai disubmit (total: {c_comp})")
        print("-" * 115)

    # 8. Render Outputs based on flags
    if args.prov:
        print(f"\n{Colors.BOLD}{Colors.HEADER}=== MONITORING PROGRES SE-2026 PROVINSI KALBAR ==={Colors.ENDC}")
        print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
        print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
        print(f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} (Hari ke-{elapsed_days} dari {total_days} hari lapangan)")
        print(f"Status Prov. Kalbar : {get_target_status(prov_actual_pct)}")
        print(f"Estimasi PPL Selesai (Worked): {get_est_completion(prov_worked_rate * 100)}")
        print(f"Estimasi PML Selesai (Done)  : {get_est_completion(prov_actual_pct)}")
        print("-" * 120)
        print(f"{'Rank':<4} | {'Kabupaten/Kota':<25} | {'Target':<7} | {'Done %':<8} | {'Worked %':<8} | {'Approval %':<10} | {'Status':<30} | {'Est. Selesai'}")
        print("-" * 120)
        for idx, (kab, m) in enumerate(kab_list, 1):
            kab_pct = m["completed_rate"] * 100
            status_raw = get_target_status(kab_pct)
            print(f"{idx:<4} | {kab:<25} | {m['target']:<7} | {kab_pct:>6.2f}% | {m['worked_rate']*100:>8.2f}% | {m['approval_rate']*100:>10.2f}% | {status_raw:<41} | {get_est_completion(kab_pct)}")
        print("-" * 120)
        print(f"{'TOTAL PROVINSI KALBAR':<30} | {prov_target:<7} | {prov_actual_pct:>6.2f}% | {prov_worked_rate*100:>8.2f}% | {prov_approval_rate*100:>10.2f}% | {get_target_status(prov_actual_pct):<41} | {get_est_completion(prov_actual_pct)}")
        print("-" * 120)
        print()
        return

    # Check if alokasi exists for non-prov views
    if not has_alokasi:
        print(f"{Colors.FAIL}Error: Berkas alokasi petugas tidak ditemukan di {csv_path}. Mode ini memerlukan file alokasi.{Colors.ENDC}")
        sys.exit(1)

    # 5. Output rendering

    # A. --intervention flag (Kabupaten Mempawah wide assessment)
    if args.intervention:
        ppl_to_supervisors = {}
        pml_to_supervisors = {}
        ppl_metrics = {}
        pml_metrics = {}

        # Scan through all groups
        for pj, pmls in pj_kuda_groups.items():
            for pml, ppls in pmls.items():
                pml_to_supervisors[pml] = pj
                for ppl, sls_list in ppls.items():
                    ppl_to_supervisors[ppl] = (pml, pj)
                    ppl_metrics[ppl] = aggregate_metrics(sls_list)

        # Aggregate for PMLs
        for pj, pmls in pj_kuda_groups.items():
            for pml, ppls in pmls.items():
                pml_sls = []
                for ppl, sls_list in ppls.items():
                    pml_sls.extend(sls_list)
                pml_metrics[pml] = aggregate_metrics(pml_sls)

        # 1. PPLs with low completed rate (< 3%) and target > 200
        low_ppls = []
        for name, m in ppl_metrics.items():
            if m["target"] > 200 and m["completed_rate"] < 0.03:
                low_ppls.append((name, m))
        low_ppls.sort(key=lambda x: x[1]["completed_rate"])

        # 2. PMLs with low approval rate (< 20%) and pending submissions > 20
        bottleneck_pmls = []
        for name, m in pml_metrics.items():
            if m["submitted"] > 20 and m["approval_rate"] < 0.20:
                bottleneck_pmls.append((name, m))
        bottleneck_pmls.sort(key=lambda x: x[1]["approval_rate"])

        kab_actual_pct = kab_avg_completed * 100
        print(f"\n{Colors.BOLD}{Colors.HEADER}=== LAPORAN INTERVENSI PROGRES SE-2026 KAB. MEMPAWAH ==={Colors.ENDC}")
        print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
        print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
        print(f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} (Hari ke-{elapsed_days} dari {total_days})")
        print(f"Status Kab. Mempawah: {get_target_status(kab_actual_pct)}")
        print(f"Estimasi PPL Selesai (Worked): {get_est_completion(kab_avg_worked * 100)}")
        print(f"Estimasi PML Selesai (Done)  : {get_est_completion(kab_actual_pct)}")
        print("-" * 115)
        print(f"Rata-rata Kabupaten : Worked={kab_avg_worked*100:.2f}%, Completed={kab_avg_completed*100:.2f}%, Approval={kab_avg_approval*100:.2f}%")
        
        print(f"\n{Colors.BOLD}{Colors.FAIL}1. DAFTAR PPL TERLAMBAT (Progres Selesai < 3.00% & Target > 200){Colors.ENDC}")
        print("-" * 115)
        print(f"{'No':<3} | {'Nama PPL':<25} | {'Target':<6} | {'Selesai':<8} | {'Open':<5} | {'Nama PML':<20} | {'PJ-Kuda':<25}")
        print("-" * 115)
        for idx, (name, m) in enumerate(low_ppls, 1):
            pml, pj = ppl_to_supervisors[name]
            print(f"{idx:<3} | {name:<25} | {m['target']:<6} | {m['completed_rate']*100:>6.2f}% | {m['open']:<5} | {pml:<20} | {pj:<25}")
        print("-" * 115)

        print(f"\n{Colors.BOLD}{Colors.WARNING}2. DAFTAR PML BOTTLENECK (Pending > 20 & Approval Rate < 20.00%){Colors.ENDC}")
        print("-" * 105)
        print(f"{'No':<3} | {'Nama PML':<20} | {'Pending':<8} | {'Approved':<8} | {'Approval %':<10} | {'PJ-Kuda':<25}")
        print("-" * 105)
        for idx, (name, m) in enumerate(bottleneck_pmls, 1):
            pj = pml_to_supervisors[name]
            print(f"{idx:<3} | {name:<20} | {m['submitted']:<8} | {m['approved']:<8} | {m['approval_rate']*100:>8.2f}% | {pj:<25}")
        print("-" * 105)

        print(f"\n{Colors.BOLD}{Colors.CYAN}💡 PEDOMAN INTERVENSI PROFESIONAL PJ-KUDA & PML MITRA:{Colors.ENDC}")
        print(" 1. Hubungi PML Bottleneck: Tekankan agar PML memverifikasi berkas yang masuk minimal 2 kali sehari.")
        print("    Ingatkan bahwa PML Mitra wajib menjaga ritme kerja agar PPL tidak terhambat.")
        print(" 2. Hubungi PML dari PPL Terlambat: Tugaskan PML untuk mendampingi PPL tersebut ke lapangan.")
        print("    Identifikasi masalah: apakah ada penolakan usaha, kendala HP/aplikasi, atau masalah personal.")
        print(" 3. Lakukan Tactical Visit: Jika ada penolakan responden besar, PJ-Kuda harus turun bersama PML.")
        print()
        return

    # D. --report flag: Standardized 6-section report (baku)
    if args.report:
        now_str = datetime.now().strftime("%d %B %Y, pukul %H:%M WIB")

        # --- Kalbar rank of Mempawah ---
        memp_rank = next((i+1 for i, (k, _) in enumerate(kab_list) if k == "MEMPAWAH"), "?")
        memp_total = len(kab_list)

        # --- Mempawah metrics ---
        memp_m = kab_data.get("MEMPAWAH", {})
        memp_done_pct  = memp_m.get("completed", 0) / memp_m["target"] * 100 if memp_m.get("target", 0) > 0 else 0.0
        memp_worked_pct = memp_m.get("worked", 0) / memp_m["target"] * 100 if memp_m.get("target", 0) > 0 else 0.0

        # --- Target PJ metrics ---
        target_pj_name = args.pj
        target_pj_data = next((p for p in pj_summaries if p["pj"].lower() == target_pj_name.lower()), None)
        pj_done_pct = target_pj_data["completed_rate"] * 100 if target_pj_data else 0.0

        # --- Build lookup: PML -> PJ (from CSV, epistemologically valid) ---
        pml_to_pj = {}
        ppl_to_pml = {}
        ppl_to_pj  = {}
        for pj_name, pmls in pj_kuda_groups.items():
            for pml_name, ppls in pmls.items():
                pml_to_pj[pml_name] = pj_name
                for ppl_name in ppls:
                    ppl_to_mpl = pml_name
                    ppl_to_mpl_pj = pj_name
                    ppl_to_mml = pml_name
                    ppl_to_mml_pj = pj_name
        # Re-do cleanly
        pml_to_pj.clear()
        ppl_to_mml_map = {}
        for pj_name, pmls in pj_kuda_groups.items():
            for pml_name, ppls in pmls.items():
                pml_to_pj[pml_name] = pj_name
                for ppl_name in ppls:
                    ppl_to_mml_map[ppl_name] = (pml_name, pj_name)

        def pj_short(full_name):
            """Return first name token of PJ for concise display."""
            return full_name.split()[0] if full_name else "?"

        # --- Section 1: Target Harian ---
        print(f"\n{'='*80}")
        print(f"   LAPORAN PROGRES SE-2026 — {now_str}")
        print(f"{'='*80}")
        print(f"\n{'─'*80}")
        print(f" 📅 1. STATUS TARGET HARIAN (Tenggat: 15 Agustus 2026)")
        print(f"{'─'*80}")
        print(f"   Target Progres Ideal Hari Ini : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} (Hari ke-{elapsed_days} dari {total_days} hari lapangan)")

        # --- Section 2: Posisi Makro ---
        print(f"\n{'─'*80}")
        print(f" 📊 2. POSISI MAKRO PROVINSI KALBAR & MEMPAWAH")
        print(f"{'─'*80}")
        prov_status = get_target_status(prov_actual_pct)
        memp_status = get_target_status(memp_done_pct)
        print(f"   Progres Kalbar    : {Colors.BOLD}{prov_actual_pct:.2f}%{Colors.ENDC} | Status: {prov_status}")
        print(f"     Est. PPL Selesai (Worked) : {get_est_completion(prov_worked_rate * 100)}")
        print(f"     Est. PML Selesai (Done)   : {get_est_completion(prov_actual_pct)}")
        print(f"   Progres Mempawah  : {Colors.BOLD}{memp_done_pct:.2f}%{Colors.ENDC} | Status: {memp_status}")
        print(f"     Est. PPL Selesai (Worked) : {get_est_completion(memp_worked_pct)}")
        print(f"     Est. PML Selesai (Done)   : {get_est_completion(memp_done_pct)}")
        print(f"   Peringkat Mempawah: {Colors.BOLD}#{memp_rank} dari {memp_total}{Colors.ENDC} Kab/Kota se-Kalbar")

        # --- Section 3: Delta (hanya jika ada history) ---
        # Pre-initialize so Section 5 can safely reference these even if no history
        good_pmls = []
        ppl_diffs_r = []

        print(f"\n{'─'*80}")
        print(f" 🔄 3. PERBANDINGAN DENGAN PENGECEKAN TERAKHIR")
        print(f"{'─'*80}")
        if latest_history:
            ts_last = latest_history.get('timestamp', '-')
            print(f"   (Delta sejak pengecekan {ts_last})")

            # Prov delta
            l_prov = latest_history.get("prov", {})
            if l_prov and l_prov.get("target", 0) > 0:
                l_pct = l_prov["completed"] / l_prov["target"] * 100
                diff = prov_actual_pct - l_pct
                diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
                c = Colors.GREEN if diff > 0 else Colors.ENDC
                print(f"   Prov. Kalbar  : {l_pct:.2f}% → {Colors.BOLD}{prov_actual_pct:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

            # Mempawah delta
            l_memp = latest_history.get("kab", {}).get("MEMPAWAH", {})
            if l_memp and l_memp.get("target", 0) > 0:
                l_pct = l_memp["completed"] / l_memp["target"] * 100
                diff = memp_done_pct - l_pct
                diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
                c = Colors.GREEN if diff > 0 else Colors.ENDC
                print(f"   Kab. Mempawah : {l_pct:.2f}% → {Colors.BOLD}{memp_done_pct:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

            # PJ Ihza delta
            c_pj_snap = current_snapshot.get("pj", {}).get(target_pj_name)
            l_pj_snap = latest_history.get("pj", {}).get(target_pj_name)
            if c_pj_snap and l_pj_snap and l_pj_snap.get("target", 0) > 0:
                l_pct = l_pj_snap["completed"] / l_pj_snap["target"] * 100
                c_pct2 = c_pj_snap["completed"] / c_pj_snap["target"] * 100
                diff = c_pct2 - l_pct
                diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
                c = Colors.GREEN if diff > 0 else Colors.ENDC
                print(f"   Tim PJ Ihza   : {l_pct:.2f}% → {Colors.BOLD}{c_pct2:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

            # PML pending changes with PJ attribution from CSV
            c_pmls = current_snapshot.get("pml_pending", {})
            l_pmls = latest_history.get("pml_pending", {})
            pml_diffs_r = []
            for pml, c_val in c_pmls.items():
                c_pend = c_val["pending"] if isinstance(c_val, dict) else c_val
                c_pj_v = c_val["pj"]      if isinstance(c_val, dict) else pml_to_pj.get(pml, "")
                l_val  = l_pmls.get(pml)
                if l_val is None:
                    continue
                l_pend = l_val["pending"] if isinstance(l_val, dict) else l_val
                diff = c_pend - l_pend
                if diff != 0:
                    pml_diffs_r.append((pml, c_pend, l_pend, diff, c_pj_v))

            good_pmls = [(p, c, l, d, pj) for p, c, l, d, pj in pml_diffs_r if d < 0]
            bad_pmls  = [(p, c, l, d, pj) for p, c, l, d, pj in pml_diffs_r if d > 0]
            good_pmls.sort(key=lambda x: x[3])   # most decrease first
            bad_pmls.sort(key=lambda x: -x[3])    # most increase first

            if good_pmls or bad_pmls:
                print(f"\n   Perubahan Antrean PML (Kinerja Verifikasi):")
                for pml, c_pend, l_pend, diff, pj_v in good_pmls[:5]:
                    pj_label = f"PJ {pj_short(pj_v)}" if pj_v else "-"
                    print(f"   👍 PML {Colors.BOLD}{pml}{Colors.ENDC} ({pj_label}): memeriksa {Colors.GREEN}{abs(diff)} berkas{Colors.ENDC} (pending: {l_pend} → {c_pend})")
                for pml, c_pend, l_pend, diff, pj_v in bad_pmls[:5]:
                    pj_label = f"PJ {pj_short(pj_v)}" if pj_v else "-"
                    print(f"   ⚠️  PML {Colors.BOLD}{pml}{Colors.ENDC} ({pj_label}): antrean bertambah {Colors.FAIL}+{diff} berkas{Colors.ENDC} (pending: {l_pend} → {c_pend})")

            # PPL completed changes
            c_ppls = current_snapshot.get("ppl_completed", {})
            l_ppls = latest_history.get("ppl_completed", {})
            ppl_diffs_r = []
            for ppl, c_val in c_ppls.items():
                c_comp = c_val["completed"] if isinstance(c_val, dict) else c_val
                c_pml_v = c_val.get("pml", "")  if isinstance(c_val, dict) else ppl_to_mml_map.get(ppl, ("",""))[0]
                c_pj_v  = c_val.get("pj",  "")  if isinstance(c_val, dict) else ppl_to_mml_map.get(ppl, ("",""))[1]
                l_val = l_ppls.get(ppl)
                if l_val is None:
                    continue
                l_comp = l_val["completed"] if isinstance(l_val, dict) else l_val
                diff = c_comp - l_comp
                if diff > 0:
                    ppl_diffs_r.append((ppl, c_comp, diff, c_pml_v, c_pj_v))

            ppl_diffs_r.sort(key=lambda x: -x[2])
            if ppl_diffs_r:
                print(f"\n   Kemajuan PPL Teratas:")
                for ppl, c_comp, diff, c_pml_v, c_pj_v in ppl_diffs_r[:5]:
                    pj_label = f"PJ {pj_short(c_pj_v)}" if c_pj_v else "-"
                    team_note = " (tim Anda)" if c_pj_v.lower() == target_pj_name.lower() else ""
                    print(f"   🚀 PPL {Colors.BOLD}{ppl}{Colors.ENDC} (PML {c_pml_v}, {pj_label}){team_note}: +{diff} dokumen (total: {c_comp})")
        else:
            print(f"   (Belum ada data pengecekan sebelumnya untuk dibandingkan)")

        # --- Section 4: Intervensi ---
        print(f"\n{'─'*80}")
        print(f" 🔍 4. DAFTAR INTERVENSI TAKTIS KABUPATEN MEMPAWAH")
        print(f"{'─'*80}")

        # Build PML & PPL metrics
        ppl_metrics_r = {}
        pml_metrics_r = {}
        for pj_name, pmls in pj_kuda_groups.items():
            for pml_name, ppls in pmls.items():
                pml_sls = []
                for ppl_name, sls_list in ppls.items():
                    ppl_agg = aggregate_metrics(sls_list)
                    ppl_metrics_r[ppl_name] = ppl_agg
                    pml_sls.extend(sls_list)
                pml_metrics_r[pml_name] = aggregate_metrics(pml_sls)

        # 4A. PML Bottleneck
        bottleneck = [
            (name, m, pml_to_pj.get(name, "-"))
            for name, m in pml_metrics_r.items()
            if m["submitted"] > 20 and m["approval_rate"] < 0.20
        ]
        bottleneck.sort(key=lambda x: x[1]["approval_rate"])

        print(f"\n   A. PML Bottleneck (Antrean Verifikasi Kritis)")
        for idx, (name, m, pj_v) in enumerate(bottleneck[:7], 1):
            pj_label = pj_short(pj_v)
            diff_note = ""
            if latest_history:
                l_pmls2 = latest_history.get("pml_pending", {})
                l_val2 = l_pmls2.get(name)
                if l_val2 is not None:
                    l_p = l_val2["pending"] if isinstance(l_val2, dict) else l_val2
                    ddiff = m["submitted"] - l_p
                    if ddiff != 0:
                        diff_note = f" ({'+' if ddiff > 0 else ''}{ddiff} berkas)"
            flag = f"{Colors.FAIL}*(Naik Kritis){Colors.ENDC} " if diff_note.startswith(" (+") else ""
            print(f"   {idx}. {Colors.BOLD}{name}{Colors.ENDC} (PJ: {pj_label}) → {m['submitted']} berkas pending | Approval: {m['approval_rate']*100:.2f}%{diff_note} {flag}")

        # 4B. PPL Terlambat
        low_ppls_r = [
            (name, m, ppl_to_mml_map.get(name, ("-", "-")))
            for name, m in ppl_metrics_r.items()
            if m["target"] > 200 and m["completed_rate"] < 0.03
        ]
        low_ppls_r.sort(key=lambda x: x[1]["completed_rate"])

        print(f"\n   B. PPL Terlambat Terkritis (Selesai < 3.00% & Target > 200)")
        for idx, (name, m, sup) in enumerate(low_ppls_r[:10], 1):
            pml_v, pj_v = sup
            print(f"   {idx}. {Colors.BOLD}{name}{Colors.ENDC} (Selesai: {m['completed_rate']*100:.2f}% | PML: {pml_v} | PJ: {pj_short(pj_v)})")

        # --- Section 5: Rekomendasi Ketua SE ---
        print(f"\n{'─'*80}")
        print(f" 📋 5. REKOMENDASI TAKTIS UNTUK KETUA SE-2026 BPS KAB. MEMPAWAH")
        print(f"{'─'*80}")

        rec_no = 1
        # Rec 5.1 — Bottleneck PMLs (top 2 worst)
        if bottleneck:
            worst2 = bottleneck[:2]
            names_str = " & ".join(f"{n} (PJ {pj_short(pj_v)})" for n, _, pj_v in worst2)
            pend_str = " & ".join(f"{m['submitted']} pending" for _, m, _ in worst2)
            print(f"   {rec_no}. Tegur PML {names_str}: {pend_str} namun approval rate < 5%. Hubungi PJ-Kuda masing-masing untuk mendesak pembersihan antrean siang ini.")
            rec_no += 1

        # Rec 5.2 — Apresiasi PML yang berhasil memeriksa banyak
        if latest_history and good_pmls:
            best_r = good_pmls[:3]
            names_str = ", ".join(f"{n} (PJ {pj_short(pj_v)})" for n, _, _, _, pj_v in best_r)
            print(f"   {rec_no}. Apresiasi untuk PML {names_str}: PML ini terbukti responsif membersihkan antrean.")
            rec_no += 1

        # Rec 5.3 — PPL terlambat kritis
        if low_ppls_r:
            worst_ppl = low_ppls_r[0]
            ppl_name, ppl_m, ppl_sup = worst_ppl
            ppl_pml, ppl_pj = ppl_sup
            print(f"   {rec_no}. PPL terlambat kritis: {Colors.BOLD}{ppl_name}{Colors.ENDC} (PML {ppl_pml}, PJ {pj_short(ppl_pj)}) baru {ppl_m['completed_rate']*100:.2f}% selesai. Minta PML turun lapangan mendampingi.")
            rec_no += 1

        # --- Section 6: Rekomendasi PJ Ihza ---
        print(f"\n{'─'*80}")
        print(f" 💡 6. REKOMENDASI AKSI CEPAT PJ-KUDA (Tim {target_pj_name.split()[0]})")
        print(f"{'─'*80}")

        my_pmls = pj_kuda_groups.get(target_pj_name, {})
        rec_no2 = 1
        for pml_name, ppls in my_pmls.items():
            pml_sls2 = []
            for _, sls_list in ppls.items():
                pml_sls2.extend(sls_list)
            pml_m = aggregate_metrics(pml_sls2)
            if pml_m["submitted"] > 50 and pml_m["approval_rate"] < 0.5:
                # Compare with delta
                delta_note = ""
                if latest_history:
                    l_pmls3 = latest_history.get("pml_pending", {})
                    l_v3 = l_pmls3.get(pml_name)
                    if l_v3 is not None:
                        l_p3 = l_v3["pending"] if isinstance(l_v3, dict) else l_v3
                        ddiff3 = pml_m["submitted"] - l_p3
                        if ddiff3 != 0:
                            delta_note = f", naik {'+' if ddiff3 > 0 else ''}{ddiff3} dari pengecekan terakhir"
                print(f"   {rec_no2}. PML {Colors.BOLD}{pml_name}{Colors.ENDC}: {pml_m['submitted']} berkas pending (Approval: {pml_m['approval_rate']*100:.2f}%{delta_note}). Segera hubungi {pml_name} untuk mempercepat verifikasi.")
                rec_no2 += 1

        # PPL tim Ihza yang terlambat
        my_low_ppls = [
            (ppl_name, ppl_metrics_r[ppl_name], ppl_name)
            for pml_name, ppls in my_pmls.items()
            for ppl_name in ppls
            if ppl_name in ppl_metrics_r and ppl_metrics_r[ppl_name]["target"] > 100 and ppl_metrics_r[ppl_name]["completed_rate"] < 0.05
        ]
        my_low_ppls.sort(key=lambda x: x[1]["completed_rate"])
        if my_low_ppls:
            for ppl_name, ppl_m, _ in my_low_ppls[:3]:
                pml_v2 = ppl_to_mml_map.get(ppl_name, ("-","-"))[0]
                print(f"   {rec_no2}. PPL {Colors.BOLD}{ppl_name}{Colors.ENDC} (PML {pml_v2}): baru {ppl_m['completed_rate']*100:.2f}% selesai. Beri semangat atau tanya kendala lapangan.")
                rec_no2 += 1

        if rec_no2 == 1:
            print(f"   {Colors.GREEN}✔ Semua PML tim berjalan dalam batas normal pagi ini.{Colors.ENDC}")

        print(f"\n{'='*80}\n")
        return

    # B. --all-pj flag (Overall Rankings)
    if args.all_pj:
        kab_actual_pct = kab_avg_completed * 100
        print(f"\n{Colors.BOLD}{Colors.HEADER}=== PERINGKAT PROGRES PJ-KUDA KAB. MEMPAWAH ==={Colors.ENDC}")
        print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
        print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
        print(f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} (Hari ke-{elapsed_days} dari {total_days})")
        print(f"Status Kab. Mempawah: {get_target_status(kab_actual_pct)}")
        print(f"Estimasi Kab. Selesai: {get_est_completion(kab_actual_pct)}")
        print("-" * 88)
        print(f"{'No':<3} | {'Nama PJ-Kuda':<28} | {'SLS':<4} | {'Target':<6} | {'Worked %':<10} | {'Done %':<10} | {'Approved %':<10}")
        print("-" * 88)
        for idx, pj in enumerate(pj_summaries, 1):
            is_target_pj = (pj["pj"].lower() == args.pj.lower())
            row_color = Colors.BOLD + Colors.CYAN if is_target_pj else ""
            end_color = Colors.ENDC if is_target_pj else ""
            print(f"{row_color}{idx:<3} | {pj['pj']:<28} | {pj['sls_count']:<4} | {pj['target']:<6} | {pj['worked_rate']*100:>8.2f}% | {pj['completed_rate']*100:>8.2f}% | {pj['approval_rate']*100:>8.2f}%{end_color}")
        print("-" * 88)
        return

    # C. Default View (Specific PJ-Kuda breakdown)
    target_pj = None
    for pj in pj_summaries:
        if pj["pj"].lower() == args.pj.lower():
            target_pj = pj
            break

    if not target_pj:
        print(f"{Colors.FAIL}Error: PJ-Kuda '{args.pj}' tidak ditemukan.{Colors.ENDC}")
        print("Nama PJ-Kuda yang tersedia:")
        for p in sorted(pj_summaries, key=lambda x: x["pj"]):
            print(f" - {p['pj']}")
        sys.exit(1)

    rank = pj_summaries.index(target_pj) + 1
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== STATUS MONITORING PJ-KUDA: {target_pj['pj']} ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Peringkat Kabupaten : {Colors.BOLD}{rank} dari {len(pj_summaries)}{Colors.ENDC}")
    print(f"Target Total        : {target_pj['target']} unit sensus (SLS: {target_pj['sls_count']})")
    
    pj_actual_pct = target_pj["completed_rate"] * 100
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} (Hari ke-{elapsed_days} dari {total_days} hari lapangan)")
    print(f"Status Target       : {get_target_status(pj_actual_pct)}")
    print(f"Estimasi PPL Selesai (Worked): {get_est_completion(target_pj['worked_rate'] * 100)}")
    print(f"Estimasi PML Selesai (Done)  : {get_est_completion(pj_actual_pct)}")
    print("-" * 55)

    def print_comparison(label, team_val, kab_val):
        color = Colors.GREEN if team_val >= kab_val else Colors.WARNING
        print(f"{label:<19}: {color}{team_val*100:>6.2f}%{Colors.ENDC} (Kabupaten: {kab_val*100:.2f}%)")

    print_comparison("Worked Rate", target_pj["worked_rate"], kab_avg_worked)
    print_comparison("Completed Rate", target_pj["completed_rate"], kab_avg_completed)
    print_comparison("Approval Rate", target_pj["approval_rate"], kab_avg_approval)

    pmls = pj_kuda_groups.get(target_pj["pj"], {})
    warnings = []
    
    for pml, ppls in pmls.items():
        pml_sls = []
        for ppl, sls_list in ppls.items():
            pml_sls.extend(sls_list)
        pml_agg = aggregate_metrics(pml_sls)
        
        pml_done_color = Colors.GREEN if pml_agg["completed_rate"] >= kab_avg_completed else Colors.WARNING
        pml_app_color = Colors.GREEN if pml_agg["approval_rate"] >= 0.7 else (Colors.FAIL if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 0 else Colors.WARNING)
        
        print(f"\n{Colors.BOLD}▶ PML: {pml}{Colors.ENDC} (SLS: {pml_agg['sls_count']}, Target: {pml_agg['target']})")
        print(f"  └─ Progres: {pml_done_color}{pml_agg['completed_rate']*100:.2f}%{Colors.ENDC} Selesai, Approval: {pml_app_color}{pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}")
        print(f"  " + "-" * 88)
        print(f"  {'Nama PPL':<25} | {'SLS':<3} | {'Target':<6} | {'Open':<5} | {'Draft':<5} | {'Submit':<6} | {'Approve':<7} | {'Done %':<8}")
        print(f"  " + "-" * 88)
        
        ppl_list = []
        for ppl, sls_list in ppls.items():
            ppl_agg = aggregate_metrics(sls_list)
            ppl_agg["name"] = ppl
            ppl_list.append(ppl_agg)
            
        ppl_list.sort(key=lambda x: x["completed_rate"])
        
        for ppl in ppl_list:
            done_color = Colors.GREEN if ppl["completed_rate"] >= 0.1 else (Colors.FAIL if ppl["completed_rate"] < 0.03 else Colors.WARNING)
            print(f"  {ppl['name']:<25} | {ppl['sls_count']:<3} | {ppl['target']:<6} | {ppl['open']:<5} | {ppl['draft']:<5} | {ppl['submitted']:<6} | {ppl['approved']:<7} | {done_color}{ppl['completed_rate']*100:>6.2f}%{Colors.ENDC}")
            
            if ppl["completed_rate"] < 0.03:
                warnings.append(f"PPL {Colors.BOLD}{ppl['name']}{Colors.ENDC} di bawah PML {pml} lambat memulai pencacahan ({ppl['completed_rate']*100:.2f}% Selesai, {ppl['open']} Open)")

        if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 5:
            warnings.append(f"PML {Colors.BOLD}{pml}{Colors.ENDC} menumpuk pekerjaan PPL ({Colors.FAIL}Approval Rate: {pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}, {pml_agg['submitted']} kiriman menunggu persetujuan)")

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DIAGNOSIS & TINDAKAN KOREKTIF ==={Colors.ENDC}")
    if warnings:
        for w in warnings:
            print(f" ⚠️  {w}")
    else:
        print(f" {Colors.GREEN}✔ Semua progres tim berjalan sehat sesuai dengan standar rata-rata kabupaten.{Colors.ENDC}")
    print()

# --- MAIN ---

def main():
    parser = argparse.ArgumentParser(
        description="BPS Kabupaten Mempawah Knowledge Base Management Utility",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 1. CREATE command
    parser_create = subparsers.add_parser("create", help="Membuat folder dan template kegiatan baru.")
    parser_create.add_argument("nama", type=str, help="Nama kegiatan (contoh: 'Sakernas')")
    parser_create.add_argument("periode", type=str, help="Periode pelaksanaan (contoh: '2026-06')")
    parser_create.add_argument("--kategori", type=str, choices=["survey", "non-survey"], default="survey", help="Kategori kegiatan (default: survey)")
    parser_create.add_argument("--rutinitas", type=str, choices=["rutin", "non-rutin"], default="rutin", help="Rutinitas kegiatan (default: rutin)")
    parser_create.add_argument("--frekuensi", type=str, choices=["bulanan", "triwulanan", "semesteran", "tahunan", "10-tahunan", "ad-hoc"], default="bulanan", help="Frekuensi kegiatan (default: bulanan)")
    parser_create.add_argument("--peran", type=str, choices=["ketua", "anggota"], default="ketua", help="Peran Anda dalam tim (default: ketua)")
    parser_create.add_argument("--force", action="store_true", help="Paksa buat/timpa jika sudah ada.")
    
    # 2. LIST command
    subparsers.add_parser("list", help="Menampilkan daftar semua kegiatan.")
    
    # 3. SCHEDULE command
    parser_sched = subparsers.add_parser("schedule", help="Menampilkan timeline dan deadline jadwal.")
    group_sched = parser_sched.add_mutually_exclusive_group()
    group_sched.add_argument("--week", action="store_true", help="Tampilkan jadwal minggu ini saja.")
    group_sched.add_argument("--month", action="store_true", help="Tampilkan jadwal bulan ini saja.")
    group_sched.add_argument("--overdue", action="store_true", help="Tampilkan jadwal yang terlambat (overdue) saja.")
    
    # 4. CONVERT command
    parser_conv = subparsers.add_parser("convert", help="Mengonversi dokumen PDF ke Markdown.")
    parser_conv.add_argument("pdf", type=str, help="Path ke berkas PDF")
    parser_conv.add_argument("--ai", action="store_true", help="Gunakan AI Vision (Gemini Proxy) untuk konversi presisi tinggi.")
    
    # 5. SE-MONITOR command
    parser_mon = subparsers.add_parser("se-monitor", help="Monitoring progres petugas Sensus Ekonomi 2026.")
    parser_mon.add_argument("--pj", type=str, default="Ihza Fikri Zaki Karunia", help="Nama PJ-Kuda target (default: 'Ihza Fikri Zaki Karunia')")
    parser_mon.add_argument("--all-pj", action="store_true", help="Tampilkan peringkat seluruh PJ-Kuda.")
    parser_mon.add_argument("-i", "--intervention", action="store_true", help="Tampilkan daftar petugas se-kabupaten yang membutuhkan intervensi langsung.")
    parser_mon.add_argument("--prov", action="store_true", help="Tampilkan ringkasan progres dan peringkat seluruh Kabupaten/Kota di Provinsi Kalbar.")
    parser_mon.add_argument("-r", "--report", action="store_true", help="Cetak laporan 6-seksi baku (format standar pagi/sore).")
    
    args = parser.parse_args()
    
    # Set cwd to repo root to make paths consistent
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    
    if args.command == "create":
        cmd_create(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "se-monitor":
        cmd_se_monitor(args)

if __name__ == "__main__":
    main()
