import csv
from pathlib import Path

def export_completed_subsls(sls_info: dict, sheet_map: dict) -> None:
    """Ekspor daftar Sub-SLS yang sudah 100% Approved (termasuk tindakan admin) ke berkas CSV."""
    from ..colors import Colors
    from .data import get_sls_metrics
    
    completed_sls = []
    for idsls, info in sls_info.items():
        idsubsls = info["idsubsls"]
        m = get_sls_metrics(sheet_map, idsls, idsubsls)
        if m["target"] > 0 and m["approved"] >= m["target"]:
            completed_sls.append({
                "Kode Wilayah (Sub-SLS)": idsubsls,
                "Nama SLS": info["nmsls"],
                "Kecamatan": info["kecamatan"],
                "PPL Pencacah": info["ppl"],
                "PML Pengawas": info["pml"],
                "PJ-Kuda": info["pj"],
                "Target Unit": m["target"],
                "PML Approved": m["approved"] - m.get("comp_admin", 0) - m.get("edit_admin", 0),
                "Admin Completed": m.get("comp_admin", 0),
                "Admin Edited": m.get("edit_admin", 0),
                "Total Approved": m["approved"]
            })

    # Urutkan berdasarkan kecamatan dan nama SLS
    completed_sls.sort(key=lambda x: (x["Kecamatan"], x["Nama SLS"]))
    
    export_path = Path("kegiatan/sensus-ekonomi-2026/2026/subsls_selesai.csv")
    try:
        export_path.parent.mkdir(parents=True, exist_ok=True)
        with open(export_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "Kode Wilayah (Sub-SLS)", "Nama SLS", "Kecamatan", 
                "PPL Pencacah", "PML Pengawas", "PJ-Kuda", "Target Unit",
                "PML Approved", "Admin Completed", "Admin Edited", "Total Approved"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in completed_sls:
                writer.writerow(row)
        print(
            f"{Colors.GREEN}✓ Sukses memperbarui daftar Sub-SLS selesai "
            f"({len(completed_sls)} wilayah) di {export_path.name}.{Colors.ENDC}"
        )
    except Exception as e:
        print(f"{Colors.FAIL}Peringatan: Gagal mengekspor daftar Sub-SLS selesai ({e}).{Colors.ENDC}")
