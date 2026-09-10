"""
Summary: Monitor & Progres Harian KCDA 2026
Description:
### Deskripsi Pipeline
Mengevaluasi timeline dan kesiapan 9 publikasi Kecamatan Dalam Angka (KCDA) 2026 di Kabupaten Mempawah:
- **Tenggat ARC**: 23 September 2026
- **Tenggat Rilis**: 28 September 2026
- **Output**: Rekapitulasi hari tersisa, status per kecamatan, dan pesan briefing pimpinan.
"""
from typing import Dict, Any, List
from datetime import datetime, date

from f.shared.bps_formatters import format_bps_percentage, clean_kecamatan_name
from f.shared.alert_formatter import generate_daily_monitoring_alert

KECAMATAN_DATA = [
    {"id": "61040.26004", "name": "Mempawah Timur", "pic": "Ahmad Aulia Rahman, S.Tr.Stat.", "status": "drafting", "tables_done": 28, "total_tables": 40},
    {"id": "61040.26012", "name": "Mempawah Hilir", "pic": "Sukma Andini, S.Tr.Stat.", "status": "drafting", "tables_done": 32, "total_tables": 40},
    {"id": "61040.26011", "name": "Sungai Pinyuh", "pic": "Vaniya Dewi Wulandari, A.Md.Stat.", "status": "drafting", "tables_done": 26, "total_tables": 40},
    {"id": "61040.26005", "name": "Sungai Kunyit", "pic": "Sarah Pratiwi, S.Tr.Stat.", "status": "drafting", "tables_done": 30, "total_tables": 40},
    {"id": "61040.26010", "name": "Segedong", "pic": "Listio Jati Nandhiko, S.Tr.Stat.", "status": "drafting", "tables_done": 25, "total_tables": 40},
    {"id": "61040.26006", "name": "Toho", "pic": "Arini Faurizah, S.Tr.Stat.", "status": "drafting", "tables_done": 24, "total_tables": 40},
    {"id": "61040.26008", "name": "Jongkat", "pic": "Ihza Fikri Zaki Karunia, S.Tr.Stat.", "status": "peer_review", "tables_done": 38, "total_tables": 40},
    {"id": "61040.26009", "name": "Anjongan", "pic": "Rifky Mullah Syadriawan, A.Md.Stat.", "status": "drafting", "tables_done": 27, "total_tables": 40},
    {"id": "61040.26007", "name": "Sadaniang", "pic": "Budiman Aller Silaban, S.Tr.Stat.", "status": "drafting", "tables_done": 22, "total_tables": 40},
]

ARC_DEADLINE = date(2026, 9, 23)

def main(current_date_override: str = "") -> Dict[str, Any]:
    """
    Entrypoint Windmill Pipeline: Menghitung status monitoring KCDA 2026.
    """
    if current_date_override:
        today = datetime.strptime(current_date_override, "%Y-%m-%d").date()
    else:
        today = date.today()

    days_remaining = max(0, (ARC_DEADLINE - today).days)
    
    total_tables_overall = sum(item["total_tables"] for item in KECAMATAN_DATA)
    total_tables_done = sum(item["tables_done"] for item in KECAMATAN_DATA)
    overall_progress_pct = (total_tables_done / total_tables_overall * 100) if total_tables_overall else 0.0

    processed_kecamatan = []
    critical_items = []
    
    for item in KECAMATAN_DATA:
        pct = (item["tables_done"] / item["total_tables"] * 100) if item["total_tables"] else 0.0
        row = {
            "nomor_publikasi": item["id"],
            "kecamatan": clean_kecamatan_name(item["name"]),
            "pic": item["pic"],
            "status": item["status"],
            "tables_done": item["tables_done"],
            "total_tables": item["total_tables"],
            "progress_pct": round(pct, 1),
            "progress_display": format_bps_percentage(pct, 1)
        }
        processed_kecamatan.append(row)
        if pct < 70.0:
            critical_items.append({
                "name": item["name"],
                "progress_pct": pct,
                "note": f"PIC: {item['pic'].split(',')[0]} (Sisa {item['total_tables'] - item['tables_done']} tabel)"
            })

    # Sort critical by progress ascending
    critical_items.sort(key=lambda x: x["progress_pct"])

    summary_stats = {
        "total_kecamatan": len(KECAMATAN_DATA),
        "total_target": total_tables_overall,
        "total_completed": total_tables_done,
        "progress_pct": round(overall_progress_pct, 2),
        "remaining_days": days_remaining,
        "arc_deadline": ARC_DEADLINE.isoformat()
    }

    alert_text = generate_daily_monitoring_alert(
        title="Monitoring Publikasi KCDA 2026 BPS Mempawah",
        date_str=today.strftime("%d-%m-%Y"),
        summary_stats=summary_stats,
        top_critical_items=critical_items
    )

    return {
        "status": "success",
        "summary": summary_stats,
        "kecamatan": processed_kecamatan,
        "critical_count": len(critical_items),
        "alert_message": alert_text
    }
