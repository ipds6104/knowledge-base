import csv
from pathlib import Path

csv_path = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")
kec_counts = {}
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        kec = row.get("nmkec", "").strip()
        kec_counts[kec] = kec_counts.get(kec, 0) + 1

print("Unique nmkec in CSV:")
for kec, count in sorted(kec_counts.items()):
    print(f"- {kec}: {count} rows")
