import csv
from pathlib import Path
from ..google_sheets import get_sheets_service
from .hierarchy import build_hierarchy
from .data import download_sheet, get_sls_metrics
from ..colors import Colors

def clean_int(val):
    if not val:
        return 0
    val_str = str(val).strip().replace(',', '').replace('.', '')
    if val_str == '-' or not val_str:
        return 0
    try:
        return int(val_str)
    except ValueError:
        return 0

def get_frozen_pmls():
    try:
        service = get_sheets_service()
        spreadsheet_id = "1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0"
        sheet_title = "Kinerja Petugas DashSE"
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_title}'!A:N"
        ).execute()
        
        values = result.get('values', [])
        rows = values[1:]
        
        pml_data = {}
        for r in rows:
            while len(r) < 14:
                r.append('')
            subsls = r[1].strip()
            if not subsls or subsls == '-' or subsls == 'Kode SubSLS' or subsls == '6104000000000000':
                continue
                
            pml_name = r[6].strip().upper()
            if not pml_name or pml_name == '-':
                continue
                
            cap_pml = clean_int(r[11])
            tgt = clean_int(r[12])
            
            if pml_name not in pml_data:
                pml_data[pml_name] = {}
            if subsls not in pml_data[pml_name]:
                pml_data[pml_name][subsls] = (cap_pml, tgt)
            else:
                prev_cap, prev_tgt = pml_data[pml_name][subsls]
                pml_data[pml_name][subsls] = (max(prev_cap, cap_pml), max(prev_tgt, tgt))
                
        pml_pcts = {}
        for name, subsls_map in pml_data.items():
            total_cap = sum(x[0] for x in subsls_map.values())
            total_tgt = sum(x[1] for x in subsls_map.values())
            pct = (total_cap / total_tgt * 100) if total_tgt > 0 else 0.0
            pml_pcts[name] = (total_cap, total_tgt, pct)
        return pml_pcts
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal memuat data Freeze dari Google Sheets ({e}).{Colors.ENDC}")
        return {}

def print_pml_compare() -> None:
    """Mencetak tabel perbandingan kinerja PML (Freeze 15 Juli vs Sekarang) beserta makna kolom."""
    print(f"\n{Colors.BOLD}Memproses data perbandingan kinerja PML...{Colors.ENDC}")
    
    frozen_pmls = get_frozen_pmls()
    
    # Ambil data real-time sekarang
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    sheet_map, csv_text, data_source = download_sheet()
    
    current_pmls = {}
    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            total_target = 0
            total_approved = 0
            total_approved_rejected = 0
            
            for ppl_name, sls_list in ppls.items():
                for idsls in sls_list:
                    info = sls_info.get(idsls, {})
                    idsubsls = info.get("idsubsls")
                    m = get_sls_metrics(sheet_map, idsls, idsubsls)
                    
                    total_target += m["target"]
                    total_approved += m["approved"]
                    total_approved_rejected += (m["approved"] + m["rejected"])
                    
            pml_name_upper = pml_name.strip().upper()
            current_pmls[pml_name_upper] = {
                "pj": pj_name,
                "target": total_target,
                "approved": total_approved,
                "approved_rejected": total_approved_rejected,
                "approved_pct": (total_approved / total_target * 100) if total_target > 0 else 0.0,
                "approved_rejected_pct": (total_approved_rejected / total_target * 100) if total_target > 0 else 0.0
            }
            
    # Cari semua PML unik dari kedua dataset
    all_pml_names = set(frozen_pmls.keys()).union(set(current_pmls.keys()))
    all_pml_names = sorted(list(all_pml_names))
    
    # Header Tabel
    print(f"\n==========================================================================================")
    print(f"       TABEL PERBANDINGAN KINERJA PML (FREEZE 15 JULI vs SEKARANG REAL-TIME)")
    print(f"==========================================================================================")
    print(f" {Colors.BOLD}{'Nama PML':<25} | {'PJ':<10} | {'Freeze %':<10} | {'Sekarang App%':<13} | {'Sekarang A+R%':<13} | {'Status Pergerakan'}{Colors.ENDC}")
    print(f" ----------------------------------------------------------------------------------------")
    
    for name in all_pml_names:
        # Data Freeze
        f_cap, f_tgt, f_pct = frozen_pmls.get(name, (0, 0, None))
        f_str = f"{f_pct:.2f}%" if f_pct is not None else "-"
        
        # Data Sekarang
        c = current_pmls.get(name)
        if c:
            pj = c["pj"].split()[0] if c["pj"] else "-"
            c_app_pct = c["approved_pct"]
            c_app_str = f"{c_app_pct:.2f}%"
            c_app_rej_pct = c["approved_rejected_pct"]
            c_app_rej_str = f"{c_app_rej_pct:.2f}%"
        else:
            pj = "-"
            c_app_pct = None
            c_app_str = "-"
            c_app_rej_pct = None
            c_app_rej_str = "-"
            
        # Tentukan status pergerakan
        status_str = ""
        # bandingkan menggunakan approved_pct jika c_app_pct ada
        if f_pct is not None and c_app_pct is not None:
            if f_pct < 40.0 and c_app_pct >= 40.0:
                status_str = f"{Colors.GREEN}🎉 Lolos > 40%{Colors.ENDC}"
            elif f_pct >= 40.0 and c_app_pct < 40.0:
                status_str = f"{Colors.FAIL}📉 Turun < 40% (Target Baru){Colors.ENDC}"
            elif c_app_pct < 40.0:
                if c_app_pct > f_pct:
                    status_str = f"{Colors.WARNING}🟡 Ada Kenaikan (Lambat){Colors.ENDC}"
                else:
                    status_str = f"{Colors.FAIL}🔴 Kritis & Menurun{Colors.ENDC}"
            else:
                status_str = f"{Colors.GREEN}🟢 Aman (> 40%){Colors.ENDC}"
        elif f_pct is None and c_app_pct is not None:
            status_str = "Baru Terdaftar"
        else:
            status_str = "Tidak Aktif"
            
        print(f" {name:<25} | {pj:<10} | {f_str:<10} | {c_app_str:<13} | {c_app_rej_str:<13} | {status_str}")
        
    print(f"==========================================================================================")
    
    # Penjelasan makna kolom di bawahnya
    print(f"\n{Colors.BOLD}🔍 PENJELASAN MAKNA KOLOM:{Colors.ENDC}")
    print(f" 1. {Colors.BOLD}Nama PML & PJ{Colors.ENDC}              : Nama Pengawas Mitra Lapangan (PML) dan inisial Penanggung Jawab Kabupaten (PJ-Kuda).")
    print(f" 2. {Colors.BOLD}Freeze % (15 Juli){Colors.ENDC}         : Persentase verifikasi per 15 Juli 2026. Menggunakan rumus kotor:")
    print(f"                                   Formula: (Approved + Rejected) / Target (Prelist Awal)")
    print(f"                                   Data bersumber dari Sheet 'Kinerja Petugas DashSE' (Termin I).")
    print(f" 3. {Colors.BOLD}Sekarang App% (Disetujui){Colors.ENDC}   : Persentase dokumen yang berstatus benar-benar disetujui (Approved) saat ini.")
    print(f"                                   Formula: (APPROVED BY Pengawas + COMPLETED BY Admin + EDITED BY Admin) / Total Target")
    print(f"                                   Data bersumber dari real-time FASIH BPS Mempawah.")
    print(f" 4. {Colors.BOLD}Sekarang A+R% (Diperiksa){Colors.ENDC}   : Persentase dokumen yang sudah diperiksa pengawas (baik disetujui maupun ditolak).")
    print(f"                                   Formula: (Approved + Rejected) / Total Target (Terupdate)")
    print(f"                                   Data bersumber dari real-time FASIH BPS Mempawah (untuk pembanding kriteria kotor).")
    print(f" 5. {Colors.BOLD}Status Pergerakan{Colors.ENDC}          : Evaluasi kinerja PML dibandingkan batas target 40%:")
    print(f"                                   - {Colors.GREEN}🎉 Lolos > 40%{Colors.ENDC}                  : Sebelumnya di bawah 40%, sekarang berhasil melewatinya.")
    print(f"                                   - {Colors.FAIL}📉 Turun < 40% (Target Baru){Colors.ENDC}   : Sebelumnya aman, turun di bawah 40% akibat penyesuaian target baru.")
    print(f"                                   - {Colors.FAIL}🔴 Kritis & Menurun{Colors.ENDC}            : Progres terus berada di bawah 40% dan menurun secara persentase.")
    print(f"                                   - {Colors.GREEN}🟢 Aman (> 40%){Colors.ENDC}                  : Progres tetap stabil berada di atas target 40%.")
    print()
