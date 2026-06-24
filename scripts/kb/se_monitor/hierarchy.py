"""kb/se_monitor/hierarchy.py — Baca Alokasi Petugas.csv dan bangun hierarki.

SUMBER EPISTEMOLOGIS TUNGGAL: Semua relasi PJ→PML→PPL WAJIB berasal dari
modul ini. Tidak ada modul lain yang boleh membaca Alokasi Petugas.csv
atau menebak relasi hierarki secara mandiri.
"""

import csv
import sys
from pathlib import Path

from ..colors import Colors

ALOKASI_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")


def build_hierarchy(
    csv_path: Path = ALOKASI_PATH,
    silent: bool = False,
) -> tuple[dict, dict, bool]:
    """Baca CSV alokasi dan bangun struktur hierarki.

    Returns:
        pj_kuda_groups: {pj: {pml: {ppl: [idsls, ...]}}}
        sls_info:       {idsls: {nmsls, ppl, pml, pj, idsubsls}}
        has_alokasi:    True jika file berhasil dibaca
    """
    pj_kuda_groups: dict = {}
    sls_info: dict = {}
    has_alokasi = False

    if not csv_path.exists():
        return pj_kuda_groups, sls_info, has_alokasi

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                idsls = row.get("idsls")
                idsubsls = row.get("idsubsls")
                if not idsls:
                    continue
                pj  = row.get("Pj-Kuda", "").strip()
                pml = row.get("PML", "").strip()
                ppl = row.get("PPL", "").strip()
                nmsls = row.get("nmsls", "").strip()
                kec = row.get("nmkec", "").strip()

                sls_info[idsls] = {
                    "nmsls": nmsls,
                    "ppl": ppl,
                    "pml": pml,
                    "pj": pj,
                    "idsubsls": idsubsls,
                    "kecamatan": kec,
                }

                pj_kuda_groups.setdefault(pj, {})
                pj_kuda_groups[pj].setdefault(pml, {})
                pj_kuda_groups[pj][pml].setdefault(ppl, [])
                pj_kuda_groups[pj][pml][ppl].append(idsls)

        has_alokasi = True
    except Exception as e:
        if not silent:
            print(f"{Colors.FAIL}Error saat membaca file CSV alokasi: {e}{Colors.ENDC}")
            sys.exit(1)

    return pj_kuda_groups, sls_info, has_alokasi


def build_lookup_maps(pj_kuda_groups: dict) -> tuple[dict, dict]:
    """Bangun tabel lookup PML→PJ dan PPL→(PML, PJ) dari hierarki.

    Returns:
        pml_to_pj:       {pml_name: pj_name}
        ppl_to_supervisor: {ppl_name: (pml_name, pj_name)}
    """
    pml_to_pj: dict = {}
    ppl_to_supervisor: dict = {}

    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            pml_to_pj[pml_name] = pj_name
            for ppl_name in ppls:
                ppl_to_supervisor[ppl_name] = (pml_name, pj_name)

    return pml_to_pj, ppl_to_supervisor


def pj_first_name(full_name: str) -> str:
    """Kembalikan token nama pertama PJ untuk tampilan ringkas."""
    return full_name.split()[0] if full_name else "?"
