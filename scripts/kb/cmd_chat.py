import zipfile
import re
import os
import argparse
from pathlib import Path
from collections import Counter
from .colors import Colors

# Pattern for Android format: "4/7/26, 10:30 - Sender: Message" or system message "4/7/26, 08:54 - Message"
msg_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{2}:\d{2})\s*-\s*([^:]+):\s*(.*)$')
sys_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{2}:\d{2})\s*-\s*(.*)$')

# Search path for zip files
REPO_ROOT = Path(".")

def parse_chat_messages(zip_path):
    """Parses messages inside the first .txt file of a WhatsApp zip export."""
    messages = []
    if not os.path.exists(zip_path):
        return messages

    with zipfile.ZipFile(zip_path, 'r') as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                with z.open(name) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    lines = content.splitlines()
                    
                    current_msg = None
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Try matching standard message
                        match = msg_pattern.match(line)
                        if match:
                            if current_msg:
                                messages.append(current_msg)
                            date_str, time_str, sender, text = match.groups()
                            current_msg = {
                                "date": date_str,
                                "time": time_str,
                                "sender": sender.strip(),
                                "text": text.strip(),
                                "is_system": False
                            }
                            continue
                            
                        # Try matching system message
                        sys_match = sys_pattern.match(line)
                        if sys_match:
                            if current_msg:
                                messages.append(current_msg)
                            date_str, time_str, text = sys_match.groups()
                            current_msg = {
                                "date": date_str,
                                "time": time_str,
                                "sender": "System",
                                "text": text.strip(),
                                "is_system": True
                            }
                            continue
                            
                        # Multiline continuation
                        if current_msg:
                            current_msg["text"] += "\n" + line
                            
                    if current_msg:
                        messages.append(current_msg)
                break
    return messages

def get_zip_files():
    """Gets all zip files under the kegiatan directory recursively."""
    kegiatan_dir = REPO_ROOT / "kegiatan"
    if not kegiatan_dir.exists():
        return []
    # Search recursively for *.zip files
    zips = sorted(list(kegiatan_dir.glob("**/*.zip")), key=lambda p: p.name)
    return zips

def cmd_chat(args):
    """Handler for the 'kb chat' command."""
    zips = get_zip_files()
    
    if not zips:
        print(f"{Colors.FAIL}Tidak ditemukan berkas WhatsApp Chat (.zip) di dalam direktori kegiatan.{Colors.ENDC}")
        return

    # Handle 'list' subcommand
    if args.chat_subcommand == "list":
        print(f"\n{Colors.BOLD}=== DAFTAR BERKAS EKSPOR WHATSAPP CHAT (REKURSIF) ==={Colors.ENDC}")
        for idx, path in enumerate(zips):
            size_kb = path.stat().st_size / 1024
            rel_path = path.relative_to(REPO_ROOT)
            print(f"[{Colors.GREEN}{idx + 1}{Colors.ENDC}] {Colors.CYAN}{path.name}{Colors.ENDC} ({size_kb:.1f} KB)")
            print(f"    Lokasi: {Colors.WARNING}{rel_path.parent.as_posix()}{Colors.ENDC}")
        print(f"\nGunakan {Colors.BOLD}kb chat info <index>{Colors.ENDC} untuk melihat ringkasan obrolan.")
        return

    # Get target ZIP file index
    target_idx = -1
    try:
        target_idx = int(args.target) - 1
    except (ValueError, TypeError):
        pass

    target_zip = None
    if 0 <= target_idx < len(zips):
        target_zip = zips[target_idx]
    else:
        # Match by filename
        for p in zips:
            if args.target.lower() in p.name.lower():
                target_zip = p
                break

    if not target_zip:
        print(f"{Colors.FAIL}Berkas/Index '{args.target}' tidak ditemukan. Jalankan 'kb chat list' untuk melihat daftar.{Colors.ENDC}")
        return

    messages = parse_chat_messages(target_zip)
    if not messages:
        print(f"{Colors.FAIL}Gagal membaca pesan atau format tidak sesuai di berkas {target_zip.name}{Colors.ENDC}")
        return

    # Apply message limit if specified
    limit = getattr(args, "limit", None)
    total_messages_count = len(messages)
    
    # Slice messages from end if limit is set
    sliced_messages = messages
    if limit and limit > 0:
        sliced_messages = messages[-limit:]

    if args.chat_subcommand == "info":
        senders = [m["sender"] for m in messages if not m["is_system"]]
        system_msgs = [m for m in messages if m["is_system"]]
        
        sender_counts = Counter(senders)
        start_date = messages[0]["date"] if messages else "-"
        end_date = messages[-1]["date"] if messages else "-"

        print(f"\n{Colors.BOLD}=== INFORMASI OBROLAN: {target_zip.name} ==={Colors.ENDC}")
        print(f"Lokasi File   : {target_zip.relative_to(REPO_ROOT).as_posix()}")
        print(f"Rentang Waktu : {Colors.CYAN}{start_date}{Colors.ENDC} s.d {Colors.CYAN}{end_date}{Colors.ENDC}")
        print(f"Total Pesan   : {Colors.GREEN}{total_messages_count}{Colors.ENDC} (Pesan Sistem: {len(system_msgs)})")
        print(f"Total Pengirim: {Colors.GREEN}{len(sender_counts)}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Keaktifan Pengirim (Top 5):{Colors.ENDC}")
        for name, count in sender_counts.most_common(5):
            print(f"  - {Colors.CYAN}{name:<25}{Colors.ENDC}: {count} pesan")

    elif args.chat_subcommand == "tail":
        show_limit = limit if limit else 100
        print(f"\n{Colors.BOLD}=== {show_limit} PESAN TERBARU DARI: {target_zip.name} ==={Colors.ENDC}")
        display_msgs = messages[-show_limit:]
        
        for m in display_msgs:
            sender_color = Colors.BLUE if m["sender"] == "Ihza Karunia" else Colors.CYAN
            if m["is_system"]:
                sender_color = Colors.WARNING
            print(f"{Colors.BOLD}[{m['date']} {m['time']}]{Colors.ENDC} {sender_color}{m['sender']}{Colors.ENDC}:")
            indented_text = "\n".join("    " + line for line in m["text"].splitlines())
            print(indented_text)
            print("-" * 50)

    elif args.chat_subcommand == "links":
        print(f"\n{Colors.BOLD}=== TAUTAN / LINKS YANG DIBAGIKAN DI GRUP ==={Colors.ENDC}")
        link_regex = re.compile(r'https?://[^\s\)]+')
        
        found_links = []
        for m in sliced_messages:
            links = link_regex.findall(m["text"])
            for link in links:
                found_links.append((m["date"], m["sender"], link))

        if not found_links:
            print("  Tidak ditemukan tautan dalam obrolan.")
        else:
            if limit:
                print(f"  (Menampilkan hasil dari {limit} pesan terbaru)\n")
            for idx, (date, sender, link) in enumerate(found_links):
                print(f"[{Colors.GREEN}{idx + 1}{Colors.ENDC}] {Colors.BOLD}[{date}]{Colors.ENDC} {Colors.CYAN}{sender}{Colors.ENDC}:")
                print(f"    {Colors.UNDERLINE}{link}{Colors.ENDC}\n")

    elif args.chat_subcommand == "search":
        query = args.query.lower()
        print(f"\n{Colors.BOLD}=== HASIL PENCARIAN UNTUK: '{args.query}' ==={Colors.ENDC}")
        if limit:
            print(f"  (Mencari dalam {limit} pesan terbaru)\n")
        
        matches = []
        for m in sliced_messages:
            if query in m["text"].lower():
                matches.append(m)

        if not matches:
            print(f"  Tidak ditemukan pesan yang mengandung kata '{args.query}'.")
        else:
            print(f"Ditemukan {Colors.GREEN}{len(matches)}{Colors.ENDC} pesan cocok:\n")
            for m in matches:
                sender_color = Colors.BLUE if m["sender"] == "Ihza Karunia" else Colors.CYAN
                if m["is_system"]:
                    sender_color = Colors.WARNING
                print(f"{Colors.BOLD}[{m['date']} {m['time']}]{Colors.ENDC} {sender_color}{m['sender']}{Colors.ENDC}:")
                indented_text = "\n".join("    " + line for line in m["text"].splitlines())
                print(indented_text)
                print("-" * 50)

    elif args.chat_subcommand == "extract":
        print(f"\n{Colors.BOLD}=== DETEKSI MILESTONE & TIMELINE EPSS DARI CHAT ==={Colors.ENDC}")
        if limit:
            print(f"  (Memindai {limit} pesan terbaru)\n")
        keywords = ["deadline", "batas", "tenggat", "jadwal", "tanggal", "waktu", "jam", "visitasi", "interviu", "harmon"]
        
        extracted = []
        for m in sliced_messages:
            text_lower = m["text"].lower()
            if any(k in text_lower for k in keywords):
                if re.search(r'\d', text_lower):
                    extracted.append(m)

        if not extracted:
            print("  Tidak terdeteksi pesan jadwal/milestone potensial.")
        else:
            print(f"Mendeteksi {Colors.GREEN}{len(extracted)}{Colors.ENDC} pesan terkait lini masa/jadwal:\n")
            for m in extracted:
                sender_color = Colors.BLUE if m["sender"] == "Ihza Karunia" else Colors.CYAN
                print(f"{Colors.BOLD}[{m['date']} {m['time']}]{Colors.ENDC} {sender_color}{m['sender']}{Colors.ENDC}:")
                indented_text = "\n".join("    " + line for line in m["text"].splitlines())
                print(indented_text)
                print("-" * 50)
