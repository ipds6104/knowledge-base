"""kb/utils.py — Shared stateless helper functions."""

import re
from pathlib import Path


def load_env() -> dict:
    """Baca file .env dari root repositori dan kembalikan sebagai dict."""
    env_path = Path(__file__).parent.parent.parent / '.env'
    config = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()
    return config


def slugify(text: str) -> str:
    """Konversi nama kegiatan ke slug path (huruf kecil, tanpa karakter khusus)."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')
