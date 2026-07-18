"""kb/cmd_chat.py — Analisis obrolan WhatsApp ekspor ZIP.

Subcommand:
  list      Daftar semua ZIP chat di folder kegiatan
  info      Statistik obrolan & pengirim teraktif
  tail      Tampilkan N pesan terbaru
  links     Ekstrak semua tautan/URL
  search    Cari pesan berdasarkan kata kunci
  extract   Deteksi jadwal/milestone potensial
  digest    Ringkasan komprehensif periode tertentu (default: 7 hari)

Filter waktu (berlaku untuk semua subcommand kecuali list/info):
  --days N      Filter pesan N hari terakhir (contoh: --days 7)
  --since DATE  Filter pesan sejak tanggal (format: YYYY-MM-DD)
  --limit N     Batasi N pesan terbaru (fallback jika --days tidak cukup)
"""

import zipfile
import re
import os
from datetime import datetime, timedelta, date
from pathlib import Path
from collections import Counter
from .colors import Colors

# Pattern Android: "4/7/26, 10:30 - Sender: Message"
msg_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{2}:\d{2})\s*-\s*([^:]+):\s*(.*)$')
sys_pattern  = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{2}:\d{2})\s*-\s*(.*)$')
link_regex   = re.compile(r'https?://[^\s\)\]]+')

REPO_ROOT = Path(".")
TIMELINE_KEYWORDS = [
    "deadline", "batas", "tenggat", "jadwal", "tanggal", "visitasi",
    "interviu", "interview", "rapat", "zoom", "meeting", "selesai",
    "pukul", "pkl", "jam", "besok", "lusa", "minggu", "bulan"
]


# ─── Parsing ────────────────────────────────────────────────────────────────

def _parse_wa_date(date_str: str) -> date | None:
    """Parse tanggal format WA (M/D/YY atau M/D/YYYY) ke objek date."""
    try:
        parts = date_str.strip().split("/")
        m, d, y = int(parts[0]), int(parts[1]), int(parts[2])
        if y < 100:
            y += 2000
        return date(y, m, d)
    except Exception:
        return None


def parse_chat_messages(zip_path) -> list[dict]:
    """Parse semua pesan dalam ZIP ekspor WhatsApp."""
    messages = []
    if not os.path.exists(zip_path):
        return messages
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                with z.open(name) as f:
                    content = f.read().decode("utf-8", errors="ignore")
                current_msg = None
                for line in content.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    m = msg_pattern.match(line)
                    if m:
                        if current_msg:
                            messages.append(current_msg)
                        d, t, sender, text = m.groups()
                        current_msg = {
                            "date": d, "time": t,
                            "sender": sender.strip(), "text": text.strip(),
                            "is_system": False,
                            "date_obj": _parse_wa_date(d),
                        }
                        continue
                    sm = sys_pattern.match(line)
                    if sm:
                        if current_msg:
                            messages.append(current_msg)
                        d, t, text = sm.groups()
                        current_msg = {
                            "date": d, "time": t,
                            "sender": "System", "text": text.strip(),
                            "is_system": True,
                            "date_obj": _parse_wa_date(d),
                        }
                        continue
                    if current_msg:
                        current_msg["text"] += "\n" + line
                if current_msg:
                    messages.append(current_msg)
                break
    return messages


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_zip_files() -> list[Path]:
    kegiatan_dir = REPO_ROOT / "kegiatan"
    data_chats_dir = REPO_ROOT / "data" / "chats"
    zips = []
    if kegiatan_dir.exists():
        zips.extend(kegiatan_dir.glob("**/*.zip"))
    if data_chats_dir.exists():
        zips.extend(data_chats_dir.glob("**/*.zip"))
    return sorted(zips, key=lambda p: p.name)


def _apply_filter(messages: list[dict], args) -> tuple[list[dict], str]:
    """
    Terapkan filter waktu ke daftar pesan.
    Prioritas: --days > --since[+--until] > --limit (jumlah).
    Kembalikan (filtered_messages, label_keterangan).
    """
    days  = getattr(args, "days",  None)
    since = getattr(args, "since", None)
    until = getattr(args, "until", None)
    limit = getattr(args, "limit", None)

    # Mode 1: --days N  (N hari terakhir dari hari ini)
    if days:
        cutoff = date.today() - timedelta(days=days)
        filtered = [m for m in messages if m["date_obj"] and m["date_obj"] >= cutoff]
        label = f"(Pesan {days} hari terakhir: sejak {cutoff.strftime('%d %b %Y')})"
        return filtered, label

    # Mode 2: --since [+ --until]  (rentang tanggal spesifik)
    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()
        except ValueError:
            print(f"{Colors.FAIL}Format --since tidak valid. Gunakan YYYY-MM-DD.{Colors.ENDC}")
            return messages, ""

        until_date = None
        if until:
            try:
                until_date = datetime.strptime(until, "%Y-%m-%d").date()
            except ValueError:
                print(f"{Colors.FAIL}Format --until tidak valid. Gunakan YYYY-MM-DD.{Colors.ENDC}")

        filtered = [
            m for m in messages
            if m["date_obj"]
            and m["date_obj"] >= since_date
            and (until_date is None or m["date_obj"] <= until_date)
        ]
        if until_date:
            label = (
                f"(Rentang: {since_date.strftime('%d %b %Y')} "
                f"s.d. {until_date.strftime('%d %b %Y')})"
            )
        else:
            label = f"(Pesan sejak {since_date.strftime('%d %b %Y')})"
        return filtered, label

    # Mode 3: --limit N  (N pesan terbaru, fallback)
    if limit and limit > 0:
        return messages[-limit:], f"(Menampilkan {limit} pesan terbaru)"

    return messages, ""


def _sender_color(sender: str, is_system: bool) -> str:
    if is_system:
        return Colors.WARNING
    return Colors.BLUE if "Ihza" in sender else Colors.CYAN


def _print_msg(m: dict) -> None:
    color = _sender_color(m["sender"], m["is_system"])
    print(f"{Colors.BOLD}[{m['date']} {m['time']}]{Colors.ENDC} {color}{m['sender']}{Colors.ENDC}:")
    for line in m["text"].splitlines():
        print("    " + line)
    print("-" * 50)


def _resolve_zip(args, zips: list[Path]) -> Path | None:
    try:
        idx = int(args.target) - 1
        if 0 <= idx < len(zips):
            return zips[idx]
    except (ValueError, TypeError, AttributeError):
        pass
    for p in zips:
        if args.target.lower() in p.name.lower():
            return p
    return None


# ─── Command Handler ─────────────────────────────────────────────────────────

def cmd_chat(args) -> None:
    zips = get_zip_files()
    if not zips:
        print(f"{Colors.FAIL}Tidak ditemukan berkas .zip di dalam direktori kegiatan.{Colors.ENDC}")
        return

    # LIST
    if args.chat_subcommand == "list":
        print(f"\n{Colors.BOLD}=== DAFTAR BERKAS EKSPOR WHATSAPP CHAT ==={Colors.ENDC}")
        for i, p in enumerate(zips):
            rel = p.relative_to(REPO_ROOT)
            print(f"  [{Colors.GREEN}{i+1}{Colors.ENDC}] {Colors.CYAN}{p.name}{Colors.ENDC} ({p.stat().st_size/1024:.1f} KB)")
            print(f"       {Colors.WARNING}{rel.parent.as_posix()}{Colors.ENDC}")
        print(f"\nGunakan: kb chat info <index>  |  kb chat digest <index> --days 7")
        return

    # Resolve target ZIP
    target_zip = _resolve_zip(args, zips)
    if not target_zip:
        print(f"{Colors.FAIL}Tidak ditemukan: '{args.target}'. Jalankan 'kb chat list'.{Colors.ENDC}")
        return

    messages = parse_chat_messages(target_zip)
    if not messages:
        print(f"{Colors.FAIL}Gagal membaca pesan dari {target_zip.name}{Colors.ENDC}")
        return

    total = len(messages)
    filtered, filter_label = _apply_filter(messages, args)

    # INFO
    if args.chat_subcommand == "info":
        non_sys = [m for m in messages if not m["is_system"]]
        sys_msgs = [m for m in messages if m["is_system"]]
        counts = Counter(m["sender"] for m in non_sys)
        print(f"\n{Colors.BOLD}=== INFO: {target_zip.name} ==={Colors.ENDC}")
        print(f"Lokasi        : {target_zip.relative_to(REPO_ROOT).as_posix()}")
        print(f"Rentang Waktu : {Colors.CYAN}{messages[0]['date']}{Colors.ENDC} s.d {Colors.CYAN}{messages[-1]['date']}{Colors.ENDC}")
        print(f"Total Pesan   : {Colors.GREEN}{total}{Colors.ENDC} (Sistem: {len(sys_msgs)})")
        print(f"Total Pengirim: {Colors.GREEN}{len(counts)}{Colors.ENDC}\n")
        print(f"{Colors.BOLD}Top 5 Pengirim:{Colors.ENDC}")
        for name, cnt in counts.most_common(5):
            bar = "█" * (cnt * 20 // max(counts.values()))
            print(f"  {Colors.CYAN}{name:<25}{Colors.ENDC} {bar:<20} {cnt}")
        return

    # Tampilkan header filter
    if filter_label:
        print(f"\n{Colors.WARNING}{filter_label}{Colors.ENDC}")
        print(f"  → {Colors.GREEN}{len(filtered)}{Colors.ENDC} dari {total} total pesan.\n")

    # TAIL
    if args.chat_subcommand == "tail":
        limit = getattr(args, "limit", None)
        display = filtered[-limit:] if limit else filtered
        n = len(display)
        print(f"\n{Colors.BOLD}=== {n} PESAN DARI: {target_zip.name} ==={Colors.ENDC}\n")
        for m in display:
            _print_msg(m)

    # LINKS
    elif args.chat_subcommand == "links":
        print(f"\n{Colors.BOLD}=== TAUTAN DI GRUP: {target_zip.name} ==={Colors.ENDC}\n")
        found = []
        for m in filtered:
            for lnk in link_regex.findall(m["text"]):
                found.append((m["date"], m["sender"], lnk))
        if not found:
            print("  Tidak ada tautan ditemukan.")
        else:
            for i, (d, sender, lnk) in enumerate(found):
                print(f"  [{Colors.GREEN}{i+1}{Colors.ENDC}] {Colors.BOLD}[{d}]{Colors.ENDC} {Colors.CYAN}{sender}{Colors.ENDC}")
                print(f"       {Colors.UNDERLINE}{lnk}{Colors.ENDC}\n")

    # SEARCH
    elif args.chat_subcommand == "search":
        q = args.query.lower()
        print(f"\n{Colors.BOLD}=== PENCARIAN: '{args.query}' di {target_zip.name} ==={Colors.ENDC}\n")
        matches = [m for m in filtered if q in m["text"].lower()]
        if not matches:
            print(f"  Tidak ditemukan pesan mengandung '{args.query}'.")
        else:
            print(f"Ditemukan {Colors.GREEN}{len(matches)}{Colors.ENDC} pesan:\n")
            for m in matches:
                _print_msg(m)

    # EXTRACT
    elif args.chat_subcommand == "extract":
        print(f"\n{Colors.BOLD}=== DETEKSI JADWAL/MILESTONE: {target_zip.name} ==={Colors.ENDC}\n")
        hits = [
            m for m in filtered
            if any(k in m["text"].lower() for k in TIMELINE_KEYWORDS)
            and re.search(r'\d', m["text"])
        ]
        if not hits:
            print("  Tidak ada pesan jadwal terdeteksi.")
        else:
            print(f"Terdeteksi {Colors.GREEN}{len(hits)}{Colors.ENDC} pesan:\n")
            for m in hits:
                _print_msg(m)

    # DIGEST — ringkasan otomatis periode tertentu
    elif args.chat_subcommand == "digest":
        # Gunakan _apply_filter agar semua flag (--days, --since, --until) konsisten
        # Default: 7 hari jika tidak ada flag
        if not getattr(args, "days", None) and not getattr(args, "since", None) and not getattr(args, "limit", None):
            args.days = 7
        period_msgs, filter_label = _apply_filter(messages, args)
        non_sys = [m for m in period_msgs if not m["is_system"]]

        print(f"\n{Colors.BOLD}{'═' * 58}{Colors.ENDC}")
        print(f"{Colors.BOLD}  📋 DIGEST CHAT{Colors.ENDC}")
        print(f"{Colors.BOLD}  Grup  : {target_zip.name}{Colors.ENDC}")
        print(f"{Colors.BOLD}  Filter: {filter_label}{Colors.ENDC}")
        print(f"{Colors.BOLD}{'═' * 58}{Colors.ENDC}\n")

        if not period_msgs:
            print(f"{Colors.WARNING}  Tidak ada pesan dalam rentang yang dipilih.{Colors.ENDC}")
            print(f"  Pesan terakhir tercatat: {messages[-1]['date'] if messages else '-'}")
            return

        # Seksi 1: Statistik Keaktifan
        counts = Counter(m["sender"] for m in non_sys)
        print(f"{Colors.BOLD}📊 1. KEAKTIFAN ({len(non_sys)} pesan dari {len(counts)} orang){Colors.ENDC}")
        for name, cnt in counts.most_common():
            bar = "█" * min(cnt * 15 // max(counts.values()), 15)
            print(f"  {Colors.CYAN}{name:<22}{Colors.ENDC} {bar:<15} {cnt} pesan")

        # Seksi 2: Tautan Dibagikan
        links_found = []
        for m in period_msgs:
            for lnk in link_regex.findall(m["text"]):
                links_found.append((m["date"], m["sender"], lnk))

        print(f"\n{Colors.BOLD}🔗 2. TAUTAN DIBAGIKAN ({len(links_found)} link){Colors.ENDC}")
        if not links_found:
            print(f"  {Colors.WARNING}Tidak ada tautan.{Colors.ENDC}")
        else:
            for d, sender, lnk in links_found:
                print(f"  [{d}] {Colors.CYAN}{sender}{Colors.ENDC}")
                print(f"   → {Colors.UNDERLINE}{lnk}{Colors.ENDC}")

        # Seksi 3: Jadwal / Milestone Terdeteksi
        hits = [
            m for m in period_msgs
            if any(k in m["text"].lower() for k in TIMELINE_KEYWORDS)
            and re.search(r'\d', m["text"])
            and not m["is_system"]
        ]
        print(f"\n{Colors.BOLD}📅 3. JADWAL / MILESTONE ({len(hits)} pesan){Colors.ENDC}")
        if not hits:
            print(f"  {Colors.WARNING}Tidak ada pesan jadwal terdeteksi.{Colors.ENDC}")
        else:
            for m in hits:
                color = _sender_color(m["sender"], m["is_system"])
                print(f"  {Colors.BOLD}[{m['date']} {m['time']}]{Colors.ENDC} {color}{m['sender']}{Colors.ENDC}:")
                for line in m["text"].splitlines()[:4]:
                    print(f"    {line}")
                print()

        # Seksi 4: Aktivitas Per Hari
        day_counts: dict[str, int] = {}
        for m in non_sys:
            day_counts[m["date"]] = day_counts.get(m["date"], 0) + 1
        print(f"{Colors.BOLD}📆 4. AKTIVITAS PER HARI{Colors.ENDC}")
        for d in sorted(day_counts.keys(), key=lambda x: _parse_wa_date(x) or date.min):
            cnt = day_counts[d]
            bar = "█" * min(cnt, 30)
            print(f"  {d:<12} {bar} {cnt}")

        print(f"\n{Colors.BOLD}{'═' * 58}{Colors.ENDC}")
        print(f"{Colors.GREEN}  Digest selesai.{Colors.ENDC}")
        print(f"  Drill-down: kb chat search {args.target} -q \"<kata kunci>\" {filter_label.split('(')[-1].replace(')', '')}")
        print(f"{Colors.BOLD}{'═' * 58}{Colors.ENDC}\n")
