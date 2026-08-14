"""Script to compile SOP Permintaan Data with clean SVG flowchart diagrams, verified titles, and zero browser artifacts."""

import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.kb.dda_generator.config import DESA_CONFIGS

CSS_STYLE = """
<style>
@page {
    size: A4;
    margin: 14mm 16mm 14mm 16mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    font-size: 8.8pt;
    line-height: 1.38;
    margin: 0;
    padding: 0;
}
h1 {
    font-size: 12pt;
    font-weight: 800;
    color: #0b3c5d;
    text-align: center;
    margin-top: 0;
    margin-bottom: 2px;
    text-transform: uppercase;
}
h2 {
    font-size: 9.5pt;
    font-weight: 700;
    color: #334155;
    text-align: center;
    margin-top: 0;
    margin-bottom: 2px;
}
p strong:first-child {
    color: #0b3c5d;
}
hr {
    border: none;
    border-top: 1.2px solid #0b3c5d;
    margin: 4px 0 8px 0;
}
h3 {
    font-size: 9.5pt;
    font-weight: 800;
    color: #0b3c5d;
    margin-top: 8px;
    margin-bottom: 3px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
}
h4 {
    font-size: 8.8pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 6px;
    margin-bottom: 2px;
}
p, ul, ol {
    margin-bottom: 4px;
    text-align: justify;
    text-justify: inter-word;
}
li {
    margin-bottom: 2px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 8px 0;
    font-size: 7.8pt;
    page-break-inside: avoid;
}
th, td {
    border: 1px solid #cbd5e1;
    padding: 3px 5px;
    vertical-align: middle;
}
th {
    background-color: #f1f5f9;
    color: #0b3c5d;
    font-weight: 700;
    text-align: center;
}
code {
    background: #f1f5f9;
    padding: 1px 3px;
    border-radius: 3px;
    font-size: 7.5pt;
    color: #0f172a;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
.flowchart-container {
    text-align: center;
    margin: 4px 0 6px 0;
    page-break-inside: avoid;
}
</style>
"""


def generate_svg_diagram(cfg: dict) -> str:
    slug = cfg["name_kebab"].replace("-", "")
    return f"""<div class="flowchart-container">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 240" width="100%" height="240" style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px;">
  <!-- Start Box -->
  <rect x="220" y="8" width="260" height="34" rx="5" fill="#0b3c5d" />
  <text x="350" y="22" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#ffffff" text-anchor="middle">PEMOHON DATA / MASYARAKAT</text>
  <text x="350" y="34" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7.5" fill="#93c5fd" text-anchor="middle">Kebutuhan Akses Data Statistik {cfg['name_title']}</text>

  <!-- Branch lines -->
  <path d="M 280 42 L 280 62 L 160 62 L 160 76" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <path d="M 420 42 L 420 62 L 540 62 L 540 76" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#arrow-blue)" />

  <!-- Jalur 1 Title Box (Green) -->
  <rect x="30" y="76" width="260" height="28" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.2" />
  <text x="160" y="89" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#065f46" text-anchor="middle">JALUR 1: LAYANAN MANDIRI DIGITAL</text>
  <text x="160" y="99" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#047857" text-anchor="middle">Self-Service Online — Instan (0 Menit)</text>

  <!-- Jalur 1 Steps -->
  <path d="M 160 104 L 160 114" fill="none" stroke="#10b981" stroke-width="1.2" marker-end="url(#arrow-green)" />
  <rect x="30" y="114" width="260" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="160" y="126" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Portal Web: desa-sm.dvlp.asia</text>
  <text x="160" y="137" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#64748b" text-anchor="middle">Pilih menu Daftar Potensi &amp; Unduh Langsung</text>

  <path d="M 160 144 L 160 154" fill="none" stroke="#10b981" stroke-width="1.2" marker-end="url(#arrow-green)" />
  <rect x="30" y="154" width="260" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="160" y="166" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Unduh Spreadsheet Excel / PDF / API</text>
  <text x="160" y="177" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#64748b" text-anchor="middle">Tabel Excel (.xlsx), Publikasi, Monografi, JSON API</text>

  <path d="M 160 184 L 160 194" fill="none" stroke="#10b981" stroke-width="1.2" marker-end="url(#arrow-green)" />
  <rect x="30" y="194" width="260" height="32" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2" />
  <text x="160" y="207" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="8" font-weight="bold" fill="#15803d" text-anchor="middle">DATA BERHASIL DIPEROLEH</text>
  <text x="160" y="218" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#166534" text-anchor="middle">Tanpa registrasi manual &amp; tanpa surat pengantar</text>

  <!-- Jalur 2 Title Box (Blue) -->
  <rect x="410" y="76" width="260" height="28" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" />
  <text x="540" y="89" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#1e40af" text-anchor="middle">JALUR 2: LAYANAN FASILITASI KHUSUS</text>
  <text x="540" y="99" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#1d4ed8" text-anchor="middle">Offline &amp; WhatsApp — Maksimal 1 Hari Kerja</text>

  <!-- Jalur 2 Steps -->
  <path d="M 540 104 L 540 114" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />
  <rect x="410" y="114" width="260" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="540" y="126" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Loket Kantor / Kontak WhatsApp Agen</text>
  <text x="540" y="137" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#64748b" text-anchor="middle">Pengajuan permohonan data kustom / legalisir</text>

  <path d="M 540 144 L 540 154" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />
  <rect x="410" y="154" width="260" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="540" y="166" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Verifikasi &amp; Persetujuan Pimpinan</text>
  <text x="540" y="177" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#64748b" text-anchor="middle">Disetujui oleh {cfg['kades_title']}</text>

  <path d="M 540 184 L 540 194" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />
  <rect x="410" y="194" width="260" height="32" rx="4" fill="#f3e8ff" stroke="#a855f7" stroke-width="1.2" />
  <text x="540" y="207" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="8" font-weight="bold" fill="#6b21a8" text-anchor="middle">PENYERAHAN BERKAS RESMI</text>
  <text x="540" y="218" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="7" fill="#7e22ce" text-anchor="middle">Cetak bertanda tangan atau file elektronik resmi</text>

  <!-- Markers -->
  <defs>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
    </marker>
  </defs>
</svg>
</div>"""


def generate_sop_markdown(cfg: dict) -> str:
    admin_type = cfg["admin_type"]
    name_title = cfg["name_title"]
    kecamatan = cfg["kecamatan"]
    kades_title = cfg["kades_title"]
    kades_name = cfg["kades_name"]
    name_kebab = cfg["name_kebab"]
    year = cfg["year"]
    is_kel = cfg["is_kelurahan"]
    program_title = f"{admin_type} Cinta Statistik ({admin_type} Cantik) {year}"

    web_slug = "kelurahanpasirwansalim" if is_kel else f"desa{name_kebab.replace('-', '')}"
    web_url = f"https://desa-sm.dvlp.asia/desa-cantik/{web_slug}"
    api_slug = name_kebab.replace("-", "")

    fas_desc = ""
    if cfg.get("fas_tab"):
        fas_desc = f"\n*   **Basis Data Fasilitas (`{cfg['fas_tab']}` / AppSheet)**: Pemetaan geospasial sarana peribadatan, pendidikan, kesehatan, fasilitas ekonomi, pemerintahan, kondisi fisik bangunan, jalan, listrik, dan jaringan telekomunikasi."
        api_fas = f"\n     - `GET https://desa-sm.dvlp.asia/desa-cantik/api/{api_slug}/{cfg['fas_tab']}`"
    else:
        api_fas = ""

    wa_contact = cfg.get("wa_contact", "")
    wa_display = f" (`{wa_contact}`)" if wa_contact else ""
    wa_table_label = f" & WhatsApp Agen Statistik{wa_display}" if wa_contact else f" & Kontak Resmi Agen Statistik {admin_type}"

    md_content = f"""# STANDAR OPERASIONAL PROSEDUR (SOP) PERMINTAAN DATA
## Hasil Pembinaan {program_title}
**Pemerintah {admin_type} {name_title}, Kecamatan {kecamatan}, Kabupaten Mempawah**

---

### 1. Latar Belakang
Dalam rangka mewujudkan tata kelola Satu Data Indonesia (SDI) di tingkat {admin_type.lower()} serta mendukung keterbukaan informasi publik, Pemerintah {admin_type} {name_title} bersama Badan Pusat Statistik (BPS) Kabupaten Mempawah menyusun Standar Operasional Prosedur (SOP) Permintaan dan Pemanfaatan Data. SOP ini mengatur mekanisme aksesibilitas data bagi masyarakat, akademisi, perangkat daerah, dan pemangku kepentingan secara transparan, akuntabel, dan cepat.

---

### 2. Sumber Data & Basis Data Terpadu
Data yang dapat diakses bersumber dari basis data hasil sensus dan pendataan potensi kewilayahan Program {admin_type} Cantik {year}:
*   **Basis Data RT & Demografi (`{cfg['rt_tab']}` / AppSheet)**: Karakteristik penduduk (gender, rasio jenis kelamin), rumah tangga (KK), tingkat pendidikan, kepemilikan dokumen adminduk/BPJS, status ketenagakerjaan, kegiatan UMKM, dan sebaran penerima bantuan sosial (PKH, BPNT, BST, BLT).{fas_desc}
*   **Produk Statistik Turunan**: Buku Publikasi *{admin_type} {name_title} Dalam Angka {year}*, Buku *Potensi {admin_type} {name_title} {year}*, Monografi {admin_type}, dan Infografis Statistik Demografi format resolusi tinggi (HD).

---

### 3. Saluran Layanan Permintaan Data (Dual-Channel Delivery)

Layanan penyediaan data statistik {admin_type} Cantik {name_title} diselenggarakan melalui 2 (dua) saluran resmi:

| Saluran Layanan | Jalur Akses | Sasaran Pengguna | Durasi Layanan | Jenis Output |
| :--- | :--- | :--- | :---: | :--- |
| **Jalur 1: Layanan Mandiri Digital** (*Self-Service Online*) | Portal Website Resmi (`desa-sm.dvlp.asia`) & Open Data REST API | Masyarakat umum, akademisi, peneliti, mahasiswa, media massa, dan OPD | **Instan (0 Menit)** | File Spreadsheet Excel (`.xlsx`), Naskah Buku Publikasi PDF, Monografi, Infografis HD, JSON API |
| **Jalur 2: Layanan Fasilitasi Khusus** (*Offline & WhatsApp*) | Loket Kantor {admin_type}{wa_table_label} | Instansi resmi, riset khusus, atau pemohon data disagregasi/legalisir | **Maksimal 1 Hari Kerja** | Berkas Data Rekapitulasi Resmi bertanda tangan {kades_title} |

---

### 4. Prosedur Operasional Rinci

#### A. Jalur 1: Layanan Mandiri Digital (*Self-Service Direct Download & Open API*) — Instan (0 Menit)
Jalur ini ditujukan bagi publik, mahasiswa, akademisi, dan instansi yang memerlukan data terbuka tingkat agregat tanpa memerlukan surat pengantar atau verifikasi birokrasi manual:

1. **Akses Portal Website Resmi**:
   - Pemohon mengunjungi portal web {admin_type} Cantik: `{web_url}`
2. **Pilih Menu Layanan dan Unduh Mandiri**:
   - **Dataset Excel (SDI)**: Masuk ke section *Daftar Potensi RT*, lalu klik tombol **"Unduh Data Tabel (Excel)"** untuk mendapatkan file spreadsheet lengkap (`.xlsx`).
   - **Buku Publikasi Digital**: Masuk ke section *Publikasi & Bukti Dukung*, klik **"Unduh Publikasi"** untuk mengunduh naskah PDF resmi {admin_type} Dalam Angka atau Potensi {admin_type}.
   - **Monografi & Infografis**: Masuk ke section *Produk Statistik & SOP*, klik **"Unduh Monografi"** atau **"Unduh Versi HD"** untuk materi infografis visual.
3. **Integrasi Open API (Bagi Pengembang / Sistem Eksternal)**:
   - Akses data terstruktur via REST API (JSON):
     - `GET https://desa-sm.dvlp.asia/desa-cantik/api/{api_slug}/{cfg['rt_tab']}`{api_fas}

---

#### B. Jalur 2: Layanan Fasilitasi / Permintaan Khusus (*Offline & WhatsApp*) — Maksimal 1 Hari Kerja
Jalur ini ditujukan bagi pemohon yang membutuhkan data disagregasi khusus, konsultasi statistik sektoral, atau berkas data bertanda tangan resmi {kades_title}:

| Tahap | Pelaku | Aktivitas | Durasi | Output |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Pemohon Data | Mengajukan permohonan di loket Kantor {admin_type} {name_title} atau menghubungi Agen Statistik {admin_type} via WhatsApp{wa_display} dengan menyampaikan maksud keperluan. | 10 Menit | Formulir Permohonan Tercatat |
| **2** | Kasi Pemerintahan / {kades_title} | Memverifikasi kesesuaian permohonan data dan memberikan persetujuan rilis data statistik. | Maks 2 Jam | Disposisi Persetujuan Rilis |
| **3** | Agen Statistik {admin_type} | Melakukan ekstraksi data dari basis data terpadu {admin_type} Cantik. | 15 Menit | Berkas Rekapitulasi Data |
| **4** | Agen Statistik {admin_type} | Menyerahkan berkas data resmi (cetak bertanda tangan atau file elektronik terotentikasi via WhatsApp/Email). | 5 Menit | Tanda Terima & Berkas Data |

---

### 5. Aturan Hak Akses & Keamanan Data Pribadi
1. **Perlindungan Data Pribadi (UU No. 27/2022)**: Data individu/mikro (*by name by address*) bersifat rahasia dan **tidak dipublikasikan** untuk melindungi privasi warga.
2. **Level Diseminasi**: Data yang diserahkan kepada publik berupa data agregat tingkat Rukun Tetangga (RT), Dusun/RW, atau inventarisasi fasilitas umum.
3. **Pemanfaatan Non-Komersial**: Data hasil kegiatan {admin_type} Cantik disediakan untuk kepentingan perencanaan pembangunan, perumusan kebijakan, penelitian akademis, dan pelayanan publik. Penggunaan untuk tujuan komersial wajib memperoleh izin tertulis dari Pemerintah {admin_type}.

---

### 6. Pengesahan & Tanda Tangan

{name_title}, 6 Agustus {year}

**Mengesahkan,**  
**{kades_title}**

<br><br><br>

**<u>{kades_name.upper()}</u>**
"""
    return md_content


def compile_sops():
    outputs_dir = BASE_DIR / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    for slug, cfg in DESA_CONFIGS.items():
        v_dir = BASE_DIR / "kegiatan" / "desa-cantik" / "2026" / slug
        v_dir.mkdir(parents=True, exist_ok=True)

        md_stem = "sop-permintaan-data-sbk-2026" if slug == "sungai-bakau-kecil" else f"sop-permintaan-data-{slug}-2026"
        md_file = v_dir / f"{md_stem}.md"

        print(f"Generating & Compiling SOP for {slug}...")

        # 1. Generate clean Markdown with verified config
        md_text = generate_sop_markdown(cfg)
        md_file.write_text(md_text, encoding="utf-8")

        # 2. Compile DOCX via Pandoc
        out_docx_local = v_dir / f"{md_stem}.docx"
        out_docx_global = outputs_dir / f"{md_stem}.docx"
        cmd_docx = [
            "pandoc",
            str(md_file),
            "-o",
            str(out_docx_local),
        ]
        subprocess.run(cmd_docx, check=True)
        subprocess.run(["cp", str(out_docx_local), str(out_docx_global)], check=True)

        # 3. Convert Markdown to HTML snippet via Pandoc
        cmd_html_snippet = [
            "pandoc",
            str(md_file),
            "-t",
            "html",
        ]
        res = subprocess.run(cmd_html_snippet, capture_output=True, text=True, check=True)
        html_body = res.stdout

        # Insert SVG flowchart right after Section 3 table
        svg_diagram = generate_svg_diagram(cfg)
        # Place SVG right after Section 3 table
        if "</table>" in html_body:
            parts = html_body.split("</table>", 1)
            html_body_with_svg = parts[0] + "</table>\n" + svg_diagram + parts[1]
        else:
            html_body_with_svg = html_body + "\n" + svg_diagram

        full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>SOP Permintaan Data {cfg['name_title']}</title>
{CSS_STYLE}
</head>
<body>
{html_body_with_svg}
</body>
</html>"""

        tmp_html = Path(f"/tmp/{md_stem}.html")
        tmp_html.write_text(full_html, encoding="utf-8")

        # 4. Print to PDF via Headless Chrome with NO header and NO footer
        out_pdf_local = v_dir / f"{md_stem}.pdf"
        out_pdf_global = outputs_dir / f"{md_stem}.pdf"

        cmd_pdf = [
            "google-chrome-stable",
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={out_pdf_local}",
            str(tmp_html),
        ]
        subprocess.run(cmd_pdf, check=True)
        subprocess.run(["cp", str(out_pdf_local), str(out_pdf_global)], check=True)

        print(f"  -> Successfully generated: {out_pdf_local.name} (PDF & DOCX & Markdown)")


if __name__ == "__main__":
    compile_sops()
