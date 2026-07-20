import csv

with open("scratch/kcda_2025_monitoring.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        print(f"Row {i}: {row}")
