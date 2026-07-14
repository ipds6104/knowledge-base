"""kb/cmd_setup.py — Wizard setup pertama kali di laptop baru.

Mendeteksi apakah pengguna sudah dikonfigurasi. Jika belum,
menampilkan daftar pegawai interaktif dan menulis KB_USER_EMAIL ke .env.
"""

import sys
from pathlib import Path
from .user_identity import load_pegawai, get_current_user, whoami_str
from .colors import Colors

ENV_PATH = Path(".env")
ENV_EXAMPLE_PATH = Path(".env.example")


def _read_env_lines() -> list[str]:
    """Membaca baris .env yang ada, atau mengembalikan template dari .env.example."""
    if ENV_PATH.exists():
        with open(ENV_PATH, encoding="utf-8") as f:
            return f.readlines()
    elif ENV_EXAMPLE_PATH.exists():
        with open(ENV_EXAMPLE_PATH, encoding="utf-8") as f:
            return f.readlines()
    return []


def _write_kb_user_email(email: str) -> None:
    """Menulis atau memperbarui KB_USER_EMAIL di .env."""
    lines = _read_env_lines()
    found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("KB_USER_EMAIL"):
            new_lines.append(f"KB_USER_EMAIL={email}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        # Tambahkan di akhir jika belum ada
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"KB_USER_EMAIL={email}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def cmd_setup(args) -> None:
    """Handler untuk 'kb setup' — wizard identitas pengguna."""
    print(f"\n{Colors.BOLD}{'=' * 55}{Colors.ENDC}")
    print(f"{Colors.BOLD}  🚀 BPS Mempawah Knowledge Base — Setup Awal{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 55}{Colors.ENDC}\n")

    # Cek apakah sudah terkonfigurasi
    current = get_current_user()
    if current and not getattr(args, "force", False):
        print(f"{Colors.GREEN}✓ Identitas pengguna sudah terkonfigurasi:{Colors.ENDC}")
        print(f"  {whoami_str()}\n")
        print(f"Jalankan {Colors.BOLD}kb setup --force{Colors.ENDC} untuk mengubah identitas.")
        return

    # Tampilkan header jika belum terkonfigurasi
    if not current:
        print(f"{Colors.WARNING}⚠  Pengguna belum terkonfigurasi di laptop ini.{Colors.ENDC}")
        print(f"   File {Colors.BOLD}.env{Colors.ENDC} tidak memiliki {Colors.BOLD}KB_USER_EMAIL{Colors.ENDC}.\n")
    else:
        print(f"{Colors.WARNING}Mode paksa (--force). Mengganti identitas pengguna.{Colors.ENDC}\n")

    # Muat daftar pegawai
    pegawai = load_pegawai()
    if not pegawai:
        print(f"{Colors.FAIL}✗ Gagal memuat data pegawai dari data/pegawai/Data_Pegawai.csv{Colors.ENDC}")
        print("  Pastikan file tersebut ada dan berformat benar.")
        return

    # Tampilkan daftar pegawai dalam kolom
    print(f"{Colors.BOLD}Daftar Pegawai BPS Kabupaten Mempawah:{Colors.ENDC}")
    print(f"{'─' * 55}")
    for i, p in enumerate(pegawai):
        num = f"[{i + 1}]"
        print(
            f"  {Colors.GREEN}{num:<5}{Colors.ENDC}"
            f" {Colors.CYAN}{p['Panggilan']:<14}{Colors.ENDC}"
            f" {p['Nama'][:30]:<30}"
        )
    print(f"{'─' * 55}")

    # Prompt pilihan
    while True:
        try:
            raw = input(
                f"\n{Colors.BOLD}Siapa Anda? Masukkan nomor (1-{len(pegawai)}): {Colors.ENDC}"
            ).strip()
            idx = int(raw) - 1
            if 0 <= idx < len(pegawai):
                chosen = pegawai[idx]
                break
            print(f"  {Colors.FAIL}Nomor tidak valid, coba lagi.{Colors.ENDC}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}Setup dibatalkan.{Colors.ENDC}")
            return

    # Konfirmasi
    print(f"\n{Colors.BOLD}Konfirmasi:{Colors.ENDC}")
    print(f"  Nama     : {Colors.CYAN}{chosen['Nama']}{Colors.ENDC}")
    print(f"  Jabatan  : {chosen['Jabatan']}")
    print(f"  Email    : {Colors.GREEN}{chosen['Email']}{Colors.ENDC}")

    try:
        konfirm = input(f"\n{Colors.BOLD}Benar? (y/n): {Colors.ENDC}").strip().lower()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup dibatalkan.{Colors.ENDC}")
        return

    if konfirm != "y":
        print(f"{Colors.WARNING}Setup dibatalkan. Jalankan ulang 'kb setup'.{Colors.ENDC}")
        return

    # Tulis ke .env
    _write_kb_user_email(chosen["Email"])
    print(f"\n{Colors.GREEN}✓ KB_USER_EMAIL={chosen['Email']} berhasil disimpan ke .env{Colors.ENDC}")

    # Verifikasi akhir
    from .user_identity import get_current_user as _get
    verified = _get()
    if verified:
        print(f"\n{Colors.BOLD}🎉 Setup selesai! Selamat datang,{Colors.ENDC}")
        print(f"   {Colors.CYAN}{whoami_str()}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}Tip:{Colors.ENDC} Jalankan {Colors.BOLD}kb schedule --week{Colors.ENDC} untuk melihat agenda minggu ini.")
    else:
        print(f"\n{Colors.FAIL}✗ Verifikasi gagal. Periksa kembali file .env Anda.{Colors.ENDC}")
