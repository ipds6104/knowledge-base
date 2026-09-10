"""
Summary: BPS Data & Text Formatters
Description: Kumpulan fungsi utilitas baku untuk pemformatan angka, teks bilingual, dan sanitasi data statistik BPS.
"""
from typing import Union, Optional

def format_bps_number(value: Union[int, float, str, None], decimals: int = 2) -> str:
    """
    Format angka sesuai kaidah Bahasa Indonesia baku BPS:
    - Ribuan menggunakan titik (.)
    - Desimal menggunakan koma (,)
    """
    if value is None or value == "" or value == "-":
        return "-"
    try:
        num = float(value)
        if decimals == 0 or num.is_integer():
            formatted = f"{int(round(num)):,}".replace(",", ".")
        else:
            formatted = f"{num:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except (ValueError, TypeError):
        return str(value)

def format_bps_percentage(value: Union[int, float, str, None], decimals: int = 2) -> str:
    """
    Format persentase dengan tanda koma desimal dan simbol %.
    """
    if value is None or value == "" or value == "-":
        return "-"
    val_str = format_bps_number(value, decimals=decimals)
    return f"{val_str}%" if val_str != "-" else "-"

def clean_kecamatan_name(raw_name: str) -> str:
    """
    Standardisasi nama kecamatan di Kabupaten Mempawah.
    """
    name = raw_name.strip()
    if not name.lower().startswith("kecamatan "):
        name = f"Kecamatan {name}"
    return name.title()
