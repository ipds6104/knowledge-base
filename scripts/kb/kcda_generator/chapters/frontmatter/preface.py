"""
Frontmatter: Kata Pengantar & Preface for KCDA 2026.
Menangani Halaman Kata Pengantar (v) dan Preface (vi) dengan text-wrapping organik
beresolusi tinggi (50-slice InDesign-style contour wrap) mengitari siluet Kepala BPS.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, List

# Fallback 50-slice contour profile untuk kepala_bps.png jika pymupdf tidak tersedia
_DEFAULT_PROFILE_50 = (
    0.000, 0.000, 0.000, 0.541, 0.582, 0.602, 0.626, 0.639, 0.644, 0.644,
    0.655, 0.651, 0.644, 0.624, 0.614, 0.626, 0.699, 0.781, 0.827, 0.842,
    0.852, 0.861, 0.870, 0.879, 0.888, 0.897, 0.906, 0.915, 0.925, 0.927,
    0.886, 0.882, 0.876, 0.861, 0.809, 0.800, 0.803, 0.808, 0.815, 0.819,
    0.821, 0.822, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823
)


@dataclass(frozen=True)
class PrefaceContentDTO:
    """DTO penyimpan konten teks dan konfigurasi penandatanganan halaman preface."""
    label: str
    title: str
    highlight_prefix: str
    p1_rest: str
    p2: str
    p3: str
    p4: str
    sign_place_date: str
    sign_role: str
    sign_name: str
    is_italic: bool = False
    photo_path: str = "/kegiatan/kecamatan-dalam-angka/2026/assets/kepala_bps.png"
    signature_path: str = "/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png"


def _extract_silhouette_profile(photo_rel_path: str, num_slices: int = 50, margin_ratio: float = 0.04) -> str:
    """
    Mengekstrak siluet transparansi (alpha channel) dari file PNG secara otomatis.
    Menghasilkan array desimal 50 irisan kontur halus yang persis seperti fitur Text Wrap InDesign.
    """
    clean_rel = photo_rel_path.lstrip("/")
    possible_roots = [
        os.getcwd(),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")),
    ]
    target_abs = None
    for r in possible_roots:
        candidate = os.path.join(r, clean_rel)
        if os.path.exists(candidate):
            target_abs = candidate
            break

    if target_abs and os.path.exists(target_abs):
        try:
            import pymupdf
            pix = pymupdf.Pixmap(target_abs)
            w, h = pix.width, pix.height
            samples = pix.samples
            n = pix.n
            profile = []
            step = h / num_slices
            for i in range(num_slices):
                y_mid = int((i + 0.5) * step)
                max_x = 0
                min_x = w
                for x in range(w):
                    alpha = samples[(y_mid * w + x) * n + 3]
                    if alpha > 25:
                        if x < min_x: min_x = x
                        if x > max_x: max_x = x
                if max_x >= min_x:
                    val = min(1.0, round(max_x / w + margin_ratio, 3))
                else:
                    val = 0.0
                profile.append(val)
            return ", ".join(f"{v:.3f}" for v in profile)
        except Exception:
            pass

    return ", ".join(f"{v:.3f}" for v in _DEFAULT_PROFILE_50)


def _build_meander_preface_block(dto: PrefaceContentDTO) -> str:
    """
    Layout Builder: Merender satu halaman Kata Pengantar/Preface berstandar BPS 2026
    dengan kontur text-wrapping organik 50 irisan halus menyerupai Adobe InDesign.
    """
    style_open = '#text(style: "italic")[' if dto.is_italic else ""
    style_close = "]" if dto.is_italic else ""
    title_italic = ', style: "italic"' if dto.is_italic else ""
    name_formatted = f'#text(weight: "bold", style: "normal")[{dto.sign_name}]' if dto.is_italic else f'*{dto.sign_name}*'
    profile_str = _extract_silhouette_profile(dto.photo_path, num_slices=50, margin_ratio=0.04)

    return f"""// ------------------------------------------
// {dto.title} ({dto.label})
// ------------------------------------------
#metadata("{dto.label}") <{dto.label}>

#block(width: 100%)[
  #text(11pt, weight: "bold"{title_italic}, fill: rgb("#1F2937"))[{dto.title}]
  #v(3pt)
  #line(length: 4.5cm, stroke: 1.5pt + rgb("#FFA50C"))
]
#v(6pt)

#import "@preview/meander:0.2.2"

#let profile = ({profile_str})

#block[
  #set text(hyphenate: false, size: 8pt)
  #set par(leading: 0.65em)
  #meander.reflow({{
    import meander: *

    // Kontur organik 50-slice resolusi tinggi menyerupai Adobe InDesign
    placed(
      bottom + left,
      dx: -3.2cm,
      boundary: contour.horiz(div: 50, frac => {{
        let idx = calc.min(49, calc.max(0, calc.floor(frac * 50)))
        let bound = profile.at(idx)
        if bound == 0.0 {{
          (0.0, 0.0)
        }} else {{
          (0.0, bound)
        }}
      }}),
      box(
        width: 10.68cm,
        height: 12.5cm,
        image("{dto.photo_path}", width: 100%, height: 100%)
      )
    )

    container()
    content[
      {style_open}
        #text(fill: rgb("#EA580C"), weight: "bold")[{dto.highlight_prefix}]{dto.p1_rest}

        #v(3.5pt)
        {dto.p2}

        #v(3.5pt)
        {dto.p3}

        #v(3.5pt)
        {dto.p4}

        #v(6pt)
        #align(right)[
          #block(width: 4.8cm)[
            #set align(left)
            {dto.sign_place_date} \\
            {dto.sign_role} \\
            #v(3pt)
            #image("{dto.signature_path}", height: 26pt) \\
            #v(2pt)
            {name_formatted}
          ]
        ]
      {style_close}
      #metadata("p") <page_marker>
    ]
  }})
]
"""


def render_prefaces(cfg: Dict[str, Any]) -> str:
    """
    Orchestrator Frontmatter Preface.
    Tanggung jawab tunggal: Menyiapkan data DTO bahasa Indonesia & Inggris,
    lalu memanggil layout builder untuk merangkai halaman v dan vi.
    """
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()

    # 1. Konten Bahasa Indonesia (Halaman v)
    id_dto = PrefaceContentDTO(
        label="kata_pengantar",
        title="KATA PENGANTAR",
        highlight_prefix=f"Publikasi Kecamatan {nama_singkat} Dalam Angka 2026",
        p1_rest=(
            f" merupakan seri publikasi tahunan BPS Kabupaten Mempawah yang menyajikan "
            f"beragam data statistik sektoral bersumber dari instansi pemerintah daerah, "
            f"kantor camat, desa/kelurahan, serta survei dan sensus BPS. Publikasi ini memuat "
            f"gambaran umum mengenai geografi, pemerintahan, serta perkembangan kondisi "
            f"sosial-demografi dan perekonomian di wilayah Kecamatan {nama_singkat} secara menyeluruh."
        ),
        p2=(
            "Data yang disajikan diharapkan dapat menjadi rujukan empiris dan indikator penting "
            "dalam mendukung perencanaan, pemantauan, serta evaluasi kebijakan pembangunan daerah "
            "demi terwujudnya Satu Data Indonesia. Seiring dinamika pembangunan dan kebutuhan data "
            "berkualitas, publikasi ini terus disempurnakan baik sistematika penyajian maupun visualisasinya."
        ),
        p3=(
            f"Ucapan terima kasih dan penghargaan setinggi-tingginya kami sampaikan kepada Camat {nama_singkat}, "
            f"para Kepala Desa dan Lurah se-Kecamatan {nama_singkat}, serta pimpinan Organisasi Perangkat Daerah "
            "atas koordinasi dan kontribusi data yang diberikan sehingga penyusunan publikasi ini selesai tepat waktu."
        ),
        p4=(
            "Kami menyadari publikasi ini masih memiliki ruang penyempurnaan. Oleh karena itu, "
            "saran dan masukan konstruktif sangat kami harapkan guna perbaikan edisi mendatang. "
            "Semoga publikasi ini memberikan manfaat nyata bagi seluruh pemangku kepentingan."
        ),
        sign_place_date="Mempawah, September 2026",
        sign_role="Kepala BPS Kabupaten Mempawah",
        sign_name="MUNAWIR",
        is_italic=False,
    )

    # 2. Konten Bahasa Inggris (Halaman vi)
    en_dto = PrefaceContentDTO(
        label="preface",
        title="PREFACE",
        highlight_prefix=f"{nama_en} District in Figures 2026",
        p1_rest=(
            f" is an annual publication series issued by BPS-Statistics of Mempawah Regency, "
            f"presenting various sectoral statistical data sourced from regional government "
            f"institutions, the subdistrict office, village administrations, as well as surveys "
            f"and censuses conducted by BPS. This publication provides a comprehensive overview of "
            f"geography, governance, and socio-demographic and economic development in {nama_en} District."
        ),
        p2=(
            "The statistical indicators presented are expected to serve as essential empirical references "
            "to support evidence-based regional development planning, monitoring, and evaluation within the "
            "framework of Satu Data Indonesia (One Data Indonesia). In line with the growing need for high-quality "
            "data, this publication continues to be refined."
        ),
        p3=(
            f"We would like to express our highest gratitude and appreciation to the Head of {nama_en} District, "
            f"Village Heads throughout {nama_en} District, and all collaborating regional agencies for their "
            "valuable data contributions and seamless cooperation."
        ),
        p4=(
            "We realize that there is still room for improvement in this publication. Therefore, constructive "
            "suggestions and feedback are warmly welcomed to enhance future editions. It is our hope that "
            "this publication will be beneficial for policy makers, researchers, and the public."
        ),
        sign_place_date="Mempawah, September 2026",
        sign_role="Chief Statistician of Mempawah Regency",
        sign_name="MUNAWIR",
        is_italic=True,
    )

    # 3. Rakit kedua halaman dengan pemisah pagebreak
    return (
        "// ==========================================\n"
        "// 6. KATA PENGANTAR (HALAMAN v - INDONESIA)\n"
        "// ==========================================\n"
        + _build_meander_preface_block(id_dto)
        + "\n#pagebreak()\n\n"
        "// ==========================================\n"
        "// 7. PREFACE (HALAMAN vi - ENGLISH)\n"
        "// ==========================================\n"
        + _build_meander_preface_block(en_dto)
        + "\n#pagebreak()\n"
    )
