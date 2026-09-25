#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image

TARGET_WIDTH = 1762
TARGET_HEIGHT = 2500
QUALITY = 92

base_dir = Path("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/assets/covers")

for subfolder in ["depan", "pembatas", "belakang"]:
    dir_path = base_dir / subfolder
    for png_file in dir_path.glob("*.png"):
        jpg_file = png_file.with_suffix(".jpg")
        try:
            im = Image.open(png_file).convert("RGB")
            # If resolution is larger than 300 DPI A5, downscale smoothly
            if im.width > TARGET_WIDTH or im.height > TARGET_HEIGHT:
                im = im.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
            im.save(jpg_file, "JPEG", quality=QUALITY, optimize=True)
            orig_kb = png_file.stat().st_size / 1024
            new_kb = jpg_file.stat().st_size / 1024
            print(f"[{subfolder}] {png_file.name}: {orig_kb:.0f} KB -> {new_kb:.0f} KB")
        except Exception as e:
            print(f"Error converting {png_file}: {e}")

print("All cover assets optimized to JPG!")
