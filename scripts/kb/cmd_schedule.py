"""kb/cmd_schedule.py — Implementasi perintah `kb schedule`."""

import glob
from datetime import datetime, timedelta
from pathlib import Path

from .colors import Colors
from .markdown_io import read_markdown_file

_DAY_ID = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu",
}


def cmd_schedule(args) -> None:
    """Tampilkan timeline dan deadline jadwal kegiatan."""
    readmes = glob.glob('kegiatan/*/*/README.md')
    deadlines = []
    today = datetime.now().date()

    for r_path in readmes:
        p = Path(r_path)
        metadata, _ = read_markdown_file(r_path)
        if not metadata or "deadlines" not in metadata:
            continue
        for dl in metadata["deadlines"]:
            tgl_str = dl.get("tanggal")
            if not tgl_str:
                continue
            try:
                tgl = datetime.strptime(tgl_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            deadlines.append({
                "nama_kegiatan": metadata.get("nama", p.parent.parent.name),
                "periode": p.parent.name,
                "tanggal": tgl,
                "kegiatan": dl.get("kegiatan", ""),
                "status": dl.get("status", "belum"),
            })

    if not deadlines:
        print(f"{Colors.WARNING}Tidak ada deadline yang tercatat.{Colors.ENDC}")
        return

    deadlines.sort(key=lambda x: x["tanggal"])

    # Date range calculations
    weekday = today.weekday()
    start_of_week = today - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=6)
    start_of_month = today.replace(day=1)
    if start_of_month.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    filtered = deadlines
    title_text = "SEMUA DEADLINE"

    if args.week:
        filtered = [d for d in deadlines if start_of_week <= d["tanggal"] <= end_of_week]
        title_text = (
            f"DEADLINE MINGGU INI "
            f"({start_of_week.strftime('%d %b %Y')} - {end_of_week.strftime('%d %b %Y')})"
        )
    elif args.month:
        filtered = [d for d in deadlines if start_of_month <= d["tanggal"] <= end_of_month]
        title_text = (
            f"DEADLINE BULAN INI "
            f"({start_of_month.strftime('%d %b %Y')} - {end_of_month.strftime('%d %b %Y')})"
        )
    elif args.overdue:
        filtered = [d for d in deadlines if d["tanggal"] < today and d["status"].lower() != 'selesai']
        title_text = "DEADLINE OVERDUE (TERLEWAT & BELUM SELESAI)"

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== {title_text} ==={Colors.ENDC}\n")

    if not filtered:
        print("Tidak ada jadwal yang sesuai filter.")
        return

    current_date = None
    for dl in filtered:
        if dl["tanggal"] != current_date:
            current_date = dl["tanggal"]
            ind_day = _DAY_ID.get(current_date.strftime("%A"), current_date.strftime("%A"))
            print(
                f"\n{Colors.BOLD}{Colors.CYAN}"
                f"[{ind_day.upper()}, {current_date.strftime('%d %b %Y')}]"
                f"{Colors.ENDC}"
            )

        status_char = "[ ]"
        status_color = Colors.BLUE
        if dl["status"].lower() == 'selesai':
            status_char = "[x]"
            status_color = Colors.GREEN
        elif dl["tanggal"] < today:
            status_char = "[OVERDUE]"
            status_color = Colors.FAIL

        print(
            f"  {status_color}{status_char}{Colors.ENDC} "
            f"{dl['nama_kegiatan']} ({dl['periode']}): {dl['kegiatan']}"
        )
    print()
