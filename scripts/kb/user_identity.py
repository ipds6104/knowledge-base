"""kb/user_identity.py — Deteksi identitas pengguna aktif repo ini.

Urutan prioritas (cascade):
  1. KB_USER_EMAIL di .env           <- paling reliable, set sekali saat setup laptop baru
  2. git config user.email           <- fallback otomatis jika email cocok di data pegawai
  3. Fallback ke None                <- modul pemanggil wajib handle kasus ini
"""

import csv
import subprocess
from pathlib import Path
from .utils import load_env

PEGAWAI_CSV = Path("data/pegawai/Data_Pegawai.csv")


def load_pegawai() -> list[dict]:
    """Membaca data pegawai dari CSV dan mengembalikan list dict."""
    if not PEGAWAI_CSV.exists():
        return []
    with open(PEGAWAI_CSV, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def _git_user_email() -> str | None:
    """Mengambil email dari git config secara silent."""
    try:
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True, text=True, timeout=3
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def get_current_user() -> dict | None:
    """
    Mengembalikan dict profil pegawai pengguna aktif, atau None jika tidak dikenali.
    
    Cascade detection:
      1. KB_USER_EMAIL di .env
      2. git config user.email
    """
    env = load_env()
    pegawai = load_pegawai()

    if not pegawai:
        return None

    # Buat index lookup email -> profil
    email_index = {p["Email"].lower().strip(): p for p in pegawai}

    # Prioritas 1: KB_USER_EMAIL di .env
    env_email = env.get("KB_USER_EMAIL", "").strip().lower()
    if env_email and env_email in email_index:
        return email_index[env_email]

    # Prioritas 2: git config user.email
    git_email = _git_user_email()
    if git_email:
        git_email_lower = git_email.lower()
        if git_email_lower in email_index:
            return email_index[git_email_lower]

    return None


def whoami_str() -> str:
    """Mengembalikan string ringkasan identitas pengguna untuk ditampilkan di CLI."""
    user = get_current_user()
    if user:
        return (
            f"{user['Panggilan']} ({user['Nama']}) — "
            f"{user['Jabatan']} | {user['Email']}"
        )
    return "Pengguna tidak dikenali. Tambahkan KB_USER_EMAIL=<email@bps.go.id> ke file .env"
