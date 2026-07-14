"""kb/cmd_auto_update.py — Implementasi perintah `kb auto-update`."""

import subprocess
import sys
from .colors import Colors
from .cmd_latsar import cmd_latsar
from .cmd_sync_sheets import cmd_sync_sheets

class MockArgs:
    """Mock argument parser namespace untuk cmd_latsar dan cmd_sync_sheets."""
    def __init__(self):
        self.kelompok = 2
        self.force = False

def cmd_auto_update(args) -> None:
    """Workflow otomasi harian terpadu: git pull -> update latsar -> sync sheets."""
    print(f"{Colors.BLUE}=== MEMULAI WORKFLOW OTOMASI HARIAN ==={Colors.ENDC}\n")
    
    # 1. Jalankan git pull (OS-independent subprocess)
    print(f"{Colors.BLUE}[1/3] Menjalankan 'git pull' untuk membarui repositori...{Colors.ENDC}")
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        print(result.stdout)
        if "Already up to date." in result.stdout:
            print("Repositori sudah sinkron dengan GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.WARNING}Peringatan: Gagal melakukan 'git pull' ({e.stderr.strip()}). Melanjutkan langkah selanjutnya...{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.WARNING}Peringatan: Perintah 'git' tidak ditemukan di path. Melanjutkan langkah selanjutnya...{Colors.ENDC}")

    print("-" * 50)

    # 2. Jalankan pembaruan jadwal latsar dari Pusdiklat
    print(f"{Colors.BLUE}[2/3] Mengunduh jadwal Latsar CPNS terbaru...{Colors.ENDC}")
    mock_args = MockArgs()
    try:
        cmd_latsar(mock_args)
    except Exception as e:
        print(f"{Colors.FAIL}Error pada pembaruan Latsar: {e}{Colors.ENDC}")

    print("-" * 50)

    # 3. Jalankan sinkronisasi final ke Google Sheets pribadi
    print(f"{Colors.BLUE}[3/3] Melakukan sinkronisasi akhir ke Google Sheets...{Colors.ENDC}")
    try:
        cmd_sync_sheets(mock_args)
    except Exception as e:
        print(f"{Colors.FAIL}Error pada sinkronisasi Google Sheets: {e}{Colors.ENDC}")
        sys.exit(1)
        
    print(f"\n{Colors.GREEN}🎉 WORKFLOW OTOMASI HARIAN SELESAI DENGAN SUKSES!{Colors.ENDC}")
