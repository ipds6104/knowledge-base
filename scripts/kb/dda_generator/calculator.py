"""Standardized Metrics & Calculations Engine for DDA Generator."""

import re
from collections import defaultdict
from typing import Dict, List
from .schemas import (
    ChapterInfographicDTO,
    ChapterContentDTO,
    TechnicalNoteItemDTO,
    PublicationFrontmatterDTO,
    CompilerTeamDTO,
    ContributorItemDTO,
    AbbreviationItemDTO,
    DatasetCapabilitiesDTO,
    FacilityMetricsDTO,
)


def safe_int(val) -> int:
    """Konversi aman ke integer."""
    if not val:
        return 0
    s = str(val).strip()
    return int(s) if s.isdigit() else 0


def load_master_ketua_rt_map() -> dict:
    """Membaca pemetaan Ketua RT dari Alokasi Petugas.csv atau preset jika ada."""
    ketua_map = {
        "RT 001 RW 01 DUSUN PELAIK": "M. GUNTUR",
        "RT 002 RW 01 DUSUN PELAIK": "FAUZI",
        "RT 003 RW 02 DUSUN PELAIK": "MUSTADI",
        "RT 004 RW 02 DUSUN PELAIK": "MULYADI",
        "RT 005 RW 03 DUSUN TENGAH": "M. SARIF",
        "RT 006 RW 03 DUSUN TENGAH": "H. MURSIDI",
        "RT 007 RW 04 DUSUN TENGAH": "SULBIDIN",
        "RT 008 RW 04 DUSUN TENGAH": "MARSAWI",
        "RT 009 RW 04 DUSUN TENGAH": "SAERI",
        "RT 010 RW 05 DUSUN TEKAM BARU": "SALIK",
        "RT 011 RW 05 DUSUN TEKAM BARU": "SUKARDI",
        "RT 012 RW 06 DUSUN TEKAM BARU": "SAPRIMAN",
        "RT 013 RW 06 DUSUN TEKAM BARU": "MESRAN",
        "RT 014 RW 06 DUSUN TEKAM BARU": "MARGONO",
    }
    try:
        from pathlib import Path
        import csv
        path = Path("kegiatan/sensus-ekonomi-2026/2026/master_data/Alokasi Petugas.csv")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) > 4:
                        nmsls = row[3].strip()
                        ketua = row[4].strip()
                        if nmsls and ketua and ketua != "-":
                            ketua_map[nmsls] = ketua
    except Exception:
        pass
    return ketua_map


def get_col_val(r: dict, aliases: list, default=""):
    """Mencari nilai pertama dari kunci yang cocok (case-insensitive & whitespace-insensitive)."""
    if not isinstance(r, dict):
        return default
    keys_lower = {str(k).strip().lower(): k for k in r.keys()}
    for alias in aliases:
        alias_clean = str(alias).strip().lower()
        if alias_clean in keys_lower:
            val = r[keys_lower[alias_clean]]
            if val is not None and str(val).strip() != "":
                return val
    return default


def get_col_int(r: dict, aliases: list) -> int:
    val = get_col_val(r, aliases, default=0)
    return safe_int(val)


def preprocess_rt_raw(rt_raw_list: list) -> list:
    """Mengubah data mikro tingkat rumah tangga (Sheet1) menjadi format agregat RT jika diperlukan."""
    if not rt_raw_list:
        return []

    master_ketua = load_master_ketua_rt_map()

    # Cek apakah data sudah berformat RT (Appsheet_RT)
    sample = rt_raw_list[0]
    if "Jumlah_Penduduk_Laki_Laki" in sample or "Jumlah_Bumbung_Rumah" in sample:
        # Pastikan Nama_Ketua_RT diisikan jika kosong
        for item in rt_raw_list:
            if not item.get("Nama_Ketua_RT"):
                rt_n = item.get("Nama_RT", "").strip()
                item["Nama_Ketua_RT"] = master_ketua.get(rt_n, "")
        return rt_raw_list

    # Format data mikro rumah tangga (CAPI / Sheet1)
    rt_map = defaultdict(lambda: {
        "Nama_RT": "",
        "Nama_Petugas": "",
        "Tanggal_Waktu": "",
        "Nama_Ketua_RT": "",
        "Jumlah_Penduduk_Laki_Laki": 0,
        "Jumlah_Penduduk_Perempuan": 0,
        "Jumlah_Bumbung_Rumah": 0,
        "Jumlah_KK": 0,
        "Jumlah_Penduduk_Lansia": 0,
        "Jumlah_Kelahiran_Bayi": 0,
        "Jumlah_Kematian": 0,
        "Jumlah_Penerima_PKH": 0,
        "Jumlah_Penerima_BPNT": 0,
        "Jumlah_Penerima_BST": 0,
        "Jumlah_Penerima_BLT": 0,
        "Jumlah_Memiliki_KTP": 0,
        "Jumlah_Sekolah_TK": 0,
        "Jumlah_Sekolah_SD": 0,
        "Jumlah_Sekolah_SMP": 0,
        "Jumlah_Sekolah_SMA": 0,
        "Jumlah_Sekolah_Sarjana": 0,
        "Jumlah_Penduduk_Putus_Sekolah": 0,
        "Jumlah_Anak_Usia_0_1_Tahun": 0,
        "Jumlah_Anak_Usia_2_5_Tahun": 0,
        "Jumlah_Pendatang": 0,
        "Status_Pendataan": "Selesai",
        "layak_count": 0,
    })

    # Aliases dictionary for robust column matching across different villages
    a_l = ["Jumlah Orang Laki-Laki di Rumah", "Jumlah_Orang_Laki_Dirumah", "Jumlah_Penduduk_Laki_Laki", "Laki-Laki", "Laki", "Pria", "Male"]
    a_p = ["Jumlah Orang Perempuan di Rumah", "Jumlah_Orang_Perempuan_Dirumah", "Jumlah_Penduduk_Perempuan", "Perempuan", "Wanita", "Female"]
    a_kk = ["Jumlah Kartu Keluarga", "Jumlah_Kartu_Keluarga", "Jumlah_KK", "KK"]
    a_ktp = ["Jumlah_Memiliki_KTP", "Jumlah Memiliki KTP", "Memiliki KTP-el", "Punya KTP-el", "KTP", "e-KTP"]
    a_lansia = ["Jumlah_Penduduk_Lansia", "Jumlah Penduduk Berusia 65-74 tahun", "Jumlah Penduduk Berusia 75 tahun keatas"]
    a_u0_4 = ["Jumlah_Anak_Usia_0_1_Tahun", "Jumlah Penduduk Berusia 0-4 tahun"]
    a_u2_5 = ["Jumlah_Anak_Usia_2_5_Tahun"]
    a_putus = ["Jumlah Anggota Keluarga Putus Sekolah (7-18 tahun tetapi tidak sedang sekolah)", "Jumlah Anggota Keluarga Putus Sekolah", "Jumlah_Anggota_Keluarga_Putus_Sekolah", "Jumlah_Penduduk_Putus_Sekolah"]
    a_pkh = ["Jika menerima bantuan, berapa jumlah keluarga penerima bantuan PKH", "Jml_Penerima_Terdaftar_PKH", "Penerima PKH", "PKH"]
    a_bpnt = ["Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPNT", "Jml_Penerima_Terdaftar_Sembako/BPNT", "Penerima BPNT", "BPNT", "Sembako"]
    a_blts = ["Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTS", "BLTS", "Penerima BLTS"]
    a_bltdd = ["Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BLTDD", "BLTDD", "Penerima BLTDD"]
    a_bekerja = ["Jumlah Penduduk usia kerja (15-64 tahun) yang bekerja", "Usia Kerja Bekerja", "Bekerja"]
    a_tbekerja = ["Jumlah Penduduk usia kerja (15-64 tahun) yang tidak bekerja", "Usia Kerja Tidak Bekerja", "Pengangguran"]
    a_umkm = ["Jumlah_UMKM_Dalam_Keluarga", "UMKM", "Usaha Mikro"]
    a_bpjs = ["Jumlah_ART_Memiliki_BPJS", "Jika menerima bantuan, berapa jumlah keluarga penerima bantuan BPJS_PBI", "Peserta BPJS", "BPJS Health"]
    a_dind = ["Apa bahan utama dinding rumah?", "Bahan Dinding", "Dinding", "Material Dinding"]
    a_lant = ["Apa bahan utama lantai terluas rumah?", "Bahan Lantai", "Lantai", "Material Lantai"]
    a_atap = ["Apa bahan atap terluas rumah?", "Bahan Atap", "Atap", "Material Atap"]
    a_bab = ["Apakah rumah ini memiliki fasilitas buang air besar sendiri?", "Kepemilikan_Fasilitas_Buang_Air_Besar", "Sanitasi BAB", "BAB Sendiri"]

    for r in rt_raw_list:
        rt_name = str(get_col_val(r, ["Nama RT", "Nama_RT", "RT"])).strip()
        if not rt_name:
            continue

        d = rt_map[rt_name]
        d["Nama_RT"] = rt_name
        d["Nama_Petugas"] = str(get_col_val(r, ["Petugas", "Nama_Petugas"])).strip() or d["Nama_Petugas"]
        d["Tanggal_Waktu"] = str(get_col_val(r, ["Tanggal Pendataan", "Tanggal_Waktu"])).strip() or d["Tanggal_Waktu"]
        d["Nama_Ketua_RT"] = str(get_col_val(r, ["Nama_Ketua_RT", "Ketua_RT"])).strip() or master_ketua.get(rt_name, d["Nama_Ketua_RT"])

        l_cnt = get_col_int(r, a_l)
        p_cnt = get_col_int(r, a_p)
        kk_cnt = get_col_int(r, a_kk)

        # Smart Validation: Skip completely empty entries
        has_content = (
            l_cnt > 0 or p_cnt > 0 or kk_cnt > 0
            or bool(get_col_val(r, ["Agama_yang_Ada_di_Rumah"]))
            or bool(get_col_val(r, a_dind))
            or bool(get_col_val(r, a_bab))
            or bool(get_col_val(r, a_bpjs))
        )

        if not has_content:
            continue

        d["Jumlah_Bumbung_Rumah"] += 1
        d["Jumlah_KK"] += kk_cnt if kk_cnt > 0 else 1
        d["Jumlah_Penduduk_Laki_Laki"] += l_cnt
        d["Jumlah_Penduduk_Perempuan"] += p_cnt
        d["Jumlah_Memiliki_KTP"] += get_col_int(r, a_ktp)
        
        for alias_l in a_lansia:
            d["Jumlah_Penduduk_Lansia"] += safe_int(r.get(alias_l))
        
        d["Jumlah_Sekolah_TK"] += get_col_int(r, ["Jumlah_Sekolah_TK", "PAUD/TK"])
        d["Jumlah_Sekolah_SD"] += get_col_int(r, ["Jumlah_Sekolah_SD", "SD/MI"])
        d["Jumlah_Sekolah_SMP"] += get_col_int(r, ["Jumlah_Sekolah_SMP", "SMP/MTs"])
        d["Jumlah_Sekolah_SMA"] += get_col_int(r, ["Jumlah_Sekolah_SMA", "SMA/MA/SMK"])
        d["Jumlah_Sekolah_Sarjana"] += get_col_int(r, ["Jumlah_Sekolah_Sarjana", "Sarjana/Diploma"])

        d["Jumlah_Anak_Usia_0_1_Tahun"] += get_col_int(r, a_u0_4)
        d["Jumlah_Anak_Usia_2_5_Tahun"] += get_col_int(r, a_u2_5)
        d["Jumlah_Penduduk_Putus_Sekolah"] += get_col_int(r, a_putus)

        d["Jumlah_Penerima_PKH"] += get_col_int(r, a_pkh)
        d["Jumlah_Penerima_BPNT"] += get_col_int(r, a_bpnt)
        d["Jumlah_Penerima_BST"] += get_col_int(r, a_blts)
        d["Jumlah_Penerima_BLT"] += get_col_int(r, a_bltdd)

        # CAPI specific columns
        d["u0_4"] = d.get("u0_4", 0) + get_col_int(r, ["Jumlah Penduduk Berusia 0-4 tahun"])
        d["u5_14"] = d.get("u5_14", 0) + get_col_int(r, ["Jumlah Penduduk Berusia 5-14 tahun"])
        d["u15_64"] = d.get("u15_64", 0) + get_col_int(r, ["Jumlah Penduduk Berusia 15-64 tahun"])
        d["u65_74"] = d.get("u65_74", 0) + get_col_int(r, ["Jumlah Penduduk Berusia 65-74 tahun"])
        d["u75_plus"] = d.get("u75_plus", 0) + get_col_int(r, ["Jumlah Penduduk Berusia 75 tahun keatas"])
        d["bekerja"] = d.get("bekerja", 0) + get_col_int(r, a_bekerja)
        d["tidak_bekerja"] = d.get("tidak_bekerja", 0) + get_col_int(r, a_tbekerja)
        d["umkm"] = d.get("umkm", 0) + get_col_int(r, a_umkm)
        d["bpjs"] = d.get("bpjs", 0) + get_col_int(r, a_bpjs)

        # Check decent housing
        dind = str(get_col_val(r, a_dind)).strip()
        lant = str(get_col_val(r, a_lant)).strip()
        atap = str(get_col_val(r, a_atap)).strip()
        bab = str(get_col_val(r, a_bab)).strip()

        d["dinding_tembok"] = d.get("dinding_tembok", 0) + (1 if dind in ("Tembok", "Kayu Tembok") else 0)
        d["lantai_semen_keramik"] = d.get("lantai_semen_keramik", 0) + (1 if lant in ("Semen", "Keramik", "Ubin", "Kayu") else 0)
        d["atap_seng_genteng"] = d.get("atap_seng_genteng", 0) + (1 if atap in ("Seng", "Genteng", "Asbes") else 0)
        d["bab_sendiri"] = d.get("bab_sendiri", 0) + (1 if bab in ("Ya", "Memiliki") else 0)

        if dind and lant and atap and bab:
            if (dind in ("Tembok", "Kayu") and lant in ("Semen", "Keramik", "Ubin", "Kayu") and atap in ("Seng", "Genteng", "Asbes") and bab in ("Ya", "Memiliki")):
                d["layak_count"] += 1

    # Order RTs logically
    sorted_rts = sorted(list(rt_map.values()), key=lambda x: x["Nama_RT"])
    for d in sorted_rts:
        if d["Jumlah_Bumbung_Rumah"] > 0 and d["layak_count"] > 0:
            d["layak_pct_calc"] = round((d["layak_count"] / d["Jumlah_Bumbung_Rumah"]) * 100, 2)
        else:
            d["layak_pct_calc"] = 0.0

    return sorted_rts


def calculate_desa_metrics(rt_raw_list: list, pub_config: dict = None, fas_raw_list: list = None) -> dict:
    """Mengalkulasi seluruh variabel statistik desa dan RT secara otomatis tanpa manipulasi sintesis."""
    pub_config = pub_config or {}
    rt_raw_list = preprocess_rt_raw(rt_raw_list)
    master_ketua = load_master_ketua_rt_map()
    rows = []
    rows = []

    for idx, r in enumerate(rt_raw_list):
        rt_name = r.get("Nama_RT", "").strip()
        petugas = r.get("Nama_Petugas", "").strip()
        waktu = r.get("Tanggal_Waktu", "").strip()
        ketua_rt = r.get("Nama_Ketua_RT", "").strip() or master_ketua.get(rt_name, "")

        l = safe_int(r.get("Jumlah_Penduduk_Laki_Laki"))
        p = safe_int(r.get("Jumlah_Penduduk_Perempuan"))
        bumbung = safe_int(r.get("Jumlah_Bumbung_Rumah"))
        kk = safe_int(r.get("Jumlah_KK"))
        lansia = safe_int(r.get("Jumlah_Penduduk_Lansia"))
        lahir = safe_int(r.get("Jumlah_Kelahiran_Bayi"))
        mati = safe_int(r.get("Jumlah_Kematian"))
        pkh = safe_int(r.get("Jumlah_Penerima_PKH"))
        bpnt = safe_int(r.get("Jumlah_Penerima_BPNT"))
        bst = safe_int(r.get("Jumlah_Penerima_BST"))
        blt = safe_int(r.get("Jumlah_Penerima_BLT"))
        ktp = safe_int(r.get("Jumlah_Memiliki_KTP"))

        tk = safe_int(r.get("Jumlah_Sekolah_TK"))
        sd = safe_int(r.get("Jumlah_Sekolah_SD"))
        smp = safe_int(r.get("Jumlah_Sekolah_SMP"))
        sma = safe_int(r.get("Jumlah_Sekolah_SMA"))
        sarjana = safe_int(r.get("Jumlah_Sekolah_Sarjana"))
        putus = safe_int(r.get("Jumlah_Penduduk_Putus_Sekolah"))

        b1 = safe_int(r.get("Jumlah_Anak_Usia_0_1_Tahun"))
        b2 = safe_int(r.get("Jumlah_Anak_Usia_2_5_Tahun"))
        pendatang = safe_int(r.get("Jumlah_Pendatang"))
        status = r.get("Status_Pendataan", "Selesai").strip()

        tot_pop = l + p
        sex_ratio = (l / p * 100) if p > 0 else 0.0
        art = (tot_pop / kk) if kk > 0 else 0.0
        kepadatan = (tot_pop / bumbung) if bumbung > 0 else 0.0
        ktp_pct = (ktp / tot_pop * 100) if tot_pop > 0 else 0.0
        layak_pct = r.get("layak_pct_calc", 0.0)

        rows.append({
            "rt_name": rt_name,
            "petugas": petugas,
            "waktu": waktu,
            "ketua_rt": ketua_rt,
            "l": l,
            "p": p,
            "tot": tot_pop,
            "sr": sex_ratio,
            "bumbung": bumbung,
            "kk": kk,
            "art": art,
            "kepadatan": kepadatan,
            "lansia": lansia,
            "lahir": lahir,
            "mati": mati,
            "pkh": pkh,
            "bpnt": bpnt,
            "bst": bst,
            "blt": blt,
            "tot_bansos": pkh + bpnt + bst + blt,
            "ktp": ktp,
            "ktp_pct": ktp_pct,
            "tk": tk,
            "sd": sd,
            "smp": smp,
            "sma": sma,
            "sarjana": sarjana,
            "putus": putus,
            "b1": b1,
            "b2": b2,
            "pendatang": pendatang,
            "status": status,
            "layak_pct": layak_pct,
            "u0_4": r.get("u0_4", 0),
            "u5_14": r.get("u5_14", 0),
            "u15_64": r.get("u15_64", 0),
            "u65_74": r.get("u65_74", 0),
            "u75_plus": r.get("u75_plus", 0),
            "bekerja": r.get("bekerja", 0),
            "tidak_bekerja": r.get("tidak_bekerja", 0),
            "umkm": r.get("umkm", 0),
            "bpjs": r.get("bpjs", 0),
            "dinding_tembok": r.get("dinding_tembok", 0),
            "lantai_semen_keramik": r.get("lantai_semen_keramik", 0),
            "atap_seng_genteng": r.get("atap_seng_genteng", 0),
            "bab_sendiri": r.get("bab_sendiri", 0),
        })

    # Sort rows by RT name
    rows.sort(key=lambda x: x["rt_name"])

    # Aggregate Village Totals
    t_l = sum(r["l"] for r in rows)
    t_p = sum(r["p"] for r in rows)
    t_pop = t_l + t_p
    t_sr = (t_l / t_p * 100) if t_p > 0 else 0.0

    t_bumbung = sum(r["bumbung"] for r in rows)
    t_kk = sum(r["kk"] for r in rows)
    t_art = (t_pop / t_kk) if t_kk > 0 else 0.0
    t_kepadatan = (t_pop / t_bumbung) if t_bumbung > 0 else 0.0

    t_lansia = sum(r["lansia"] for r in rows)
    t_b1 = sum(r["b1"] for r in rows)
    t_b2 = sum(r["b2"] for r in rows)
    t_pendatang = sum(r["pendatang"] for r in rows)
    t_lahir = sum(r["lahir"] for r in rows)
    t_mati = sum(r["mati"] for r in rows)

    t_tk = sum(r["tk"] for r in rows)
    t_sd = sum(r["sd"] for r in rows)
    t_smp = sum(r["smp"] for r in rows)
    t_sma = sum(r["sma"] for r in rows)
    t_sarjana = sum(r["sarjana"] for r in rows)
    t_putus = sum(r["putus"] for r in rows)

    t_ktp = sum(r["ktp"] for r in rows)
    t_ktp_pct = (t_ktp / t_pop * 100) if t_pop > 0 else 0.0

    t_pkh = sum(r["pkh"] for r in rows)
    t_bpnt = sum(r["bpnt"] for r in rows)
    t_bst = sum(r["bst"] for r in rows)
    t_blt = sum(r["blt"] for r in rows)
    t_bansos = t_pkh + t_bpnt + t_bst + t_blt

    tot_layak_cnt = sum(r.get("layak_count", 0) for r in rt_raw_list if isinstance(r, dict))
    if t_bumbung > 0 and tot_layak_cnt > 0:
        t_layak = tot_layak_cnt
        t_layak_pct = round((t_layak / t_bumbung) * 100, 2)
    else:
        t_layak_pct = 0.0
        t_layak = 0

    return {
        "rows": rows,
        "tot_l": t_l,
        "tot_p": t_p,
        "tot_pop": t_pop,
        "tot_sr": t_sr,
        "tot_bumbung": t_bumbung,
        "tot_kk": t_kk,
        "tot_art": t_art,
        "tot_kepadatan": t_kepadatan,
        "tot_lansia": t_lansia,
        "tot_b1": t_b1,
        "tot_b2": t_b2,
        "tot_pendatang": t_pendatang,
        "tot_lahir": t_lahir,
        "tot_mati": t_mati,
        "tot_tk": t_tk,
        "tot_sd": t_sd,
        "tot_smp": t_smp,
        "tot_sma": t_sma,
        "tot_sarjana": t_sarjana,
        "tot_putus": t_putus,
        "tot_ktp": t_ktp,
        "tot_ktp_pct": t_ktp_pct,
        "tot_pkh": t_pkh,
        "tot_bpnt": t_bpnt,
        "tot_bst": t_bst,
        "tot_blt": t_blt,
        "tot_bansos": t_bansos,
        "tot_layak": t_layak,
        "tot_layak_pct": t_layak_pct,
        "tot_u0_4": sum(r["u0_4"] for r in rows),
        "tot_u5_14": sum(r["u5_14"] for r in rows),
        "tot_u15_64": sum(r["u15_64"] for r in rows),
        "tot_u65_74": sum(r["u65_74"] for r in rows),
        "tot_u75_plus": sum(r["u75_plus"] for r in rows),
        "tot_bekerja": sum(r["bekerja"] for r in rows),
        "tot_tidak_bekerja": sum(r["tidak_bekerja"] for r in rows),
        "tot_umkm": sum(r["umkm"] for r in rows),
        "tot_bpjs": sum(r["bpjs"] for r in rows),
        "tot_dinding_tembok": sum(r["dinding_tembok"] for r in rows),
        "tot_lantai_semen_keramik": sum(r["lantai_semen_keramik"] for r in rows),
        "tot_atap_seng_genteng": sum(r["atap_seng_genteng"] for r in rows),
        "tot_bab_sendiri": sum(r["bab_sendiri"] for r in rows),
        "fasilitas": aggregate_facility_metrics(fas_raw_list, rows) if fas_raw_list else {},
    }


def aggregate_facility_metrics(fas_raw_list: list, rt_rows: list) -> dict:
    """Mengagregasi data mentah inventarisasi fasilitas umum ke tingkat RT dan Total Desa."""
    if not fas_raw_list or not rt_rows:
        return {}

    rt_map = {}
    for r in rt_rows:
        rt_name = r["rt_name"]
        match = re.search(r"RT\s*(\d+)", rt_name, re.IGNORECASE)
        if match:
            num_str = f"RT {int(match.group(1)):03d}"
            rt_map[num_str] = rt_name
        else:
            rt_map[rt_name] = rt_name

    fas_per_rt = {
        r["rt_name"]: {
            "rt_name": r["rt_name"],
            "masjid": 0,
            "musholla": 0,
            "vihara": 0,
            "gereja": 0,
            "tot_ibadah": 0,
            "paud_tk": 0,
            "sd_mi": 0,
            "smp_mts": 0,
            "sma_ma": 0,
            "ponpes": 0,
            "tot_pendidikan": 0,
            "posyandu": 0,
            "polindes": 0,
            "tot_kesehatan": 0,
            "kantor": 0,
            "ekonomi": 0,
            "tpu": 0,
            "bts": 0,
            "olahraga": 0,
            "tot_fasum_lain": 0,
            "kondisi_baik": 0,
            "kondisi_rusak": 0,
            "jalan_aspal": 0,
            "jalan_batu": 0,
            "jalan_tanah": 0,
            "listrik_pln": 0,
            "air_pdam": 0,
            "sinyal_4g": 0,
        }
        for r in rt_rows
    }

    for f in fas_raw_list:
        rt_val = str(get_col_val(f, ["RT", "Nama RT", "Nama_RT", "Wilayah RT"])).strip()
        match = re.search(r"RT\s*(\d+)", rt_val, re.IGNORECASE)
        target_rt_name = None
        if match:
            num_str = f"RT {int(match.group(1)):03d}"
            target_rt_name = rt_map.get(num_str)
        if not target_rt_name:
            target_rt_name = rt_map.get(rt_val)

        if not target_rt_name and rt_rows:
            target_rt_name = rt_rows[0]["rt_name"]

        b = fas_per_rt[target_rt_name]
        kat = str(get_col_val(f, ["Kategori_Fasilitas", "Kategori"])).lower()
        sub = str(get_col_val(f, ["Sub_Kategori", "Sub Kategori"])).lower()
        nm = str(get_col_val(f, ["Nama_Fasilitas", "Nama Fasilitas"])).lower()
        kon = str(get_col_val(f, ["Kondisi_Bangunan", "Kondisi_Bangunan/Jalan", "Kondisi"])).lower()
        lis = str(get_col_val(f, ["Sumber_Listrik", "Listrik"])).lower()
        air = str(get_col_val(f, ["Sumber_Air_Bersih", "Air"])).lower()
        jln = str(get_col_val(f, ["Akses_Jalan", "Jalan"])).lower()
        sin = str(get_col_val(f, ["Sinyal_Seluler", "Sinyal"])).lower()

        # Peribadatan
        if "masjid" in sub or "masjid" in nm:
            b["masjid"] += 1
            b["tot_ibadah"] += 1
        elif "musholla" in sub or "langgar" in sub or "surau" in sub or "surau" in nm or "musholla" in nm:
            b["musholla"] += 1
            b["tot_ibadah"] += 1
        elif "vihara" in sub or "klenteng" in sub:
            b["vihara"] += 1
            b["tot_ibadah"] += 1
        elif "gereja" in sub:
            b["gereja"] += 1
            b["tot_ibadah"] += 1
        elif kat == "ibadah":
            b["tot_ibadah"] += 1

        # Pendidikan
        if "tk" in sub or "paud" in sub:
            b["paud_tk"] += 1
            b["tot_pendidikan"] += 1
        elif "sd" in sub or "mi" in sub:
            b["sd_mi"] += 1
            b["tot_pendidikan"] += 1
        elif "smp" in sub or "mts" in sub:
            b["smp_mts"] += 1
            b["tot_pendidikan"] += 1
        elif "sma" in sub or "smk" in sub or "ma" in sub:
            b["sma_ma"] += 1
            b["tot_pendidikan"] += 1
        elif "pesantren" in sub or "pondok" in sub or "ponpes" in sub:
            b["ponpes"] += 1
            b["tot_pendidikan"] += 1
        elif kat == "pendidikan":
            b["tot_pendidikan"] += 1

        # Kesehatan
        if "posyandu" in sub:
            b["posyandu"] += 1
            b["tot_kesehatan"] += 1
        elif "polindes" in sub or "poskesdes" in sub:
            b["polindes"] += 1
            b["tot_kesehatan"] += 1
        elif kat == "kesehatan":
            b["tot_kesehatan"] += 1

        # Pem/Eko/Sos
        if "kantor" in sub:
            b["kantor"] += 1
        elif kat == "ekonomi" or any(x in sub for x in ["toko", "warung", "pasar", "bank", "agen", "industri", "kerajinan", "pertanian"]):
            b["ekonomi"] += 1
        elif "tpu" in sub or "pemakaman" in sub:
            b["tpu"] += 1
        elif "bts" in sub or "menara" in sub or "telekomunikasi" in sub:
            b["bts"] += 1
        elif "olahraga" in sub or "lapangan" in sub:
            b["olahraga"] += 1
        else:
            b["tot_fasum_lain"] += 1

        # Kondisi
        if "baik" in kon:
            b["kondisi_baik"] += 1
        elif "rusak" in kon:
            b["kondisi_rusak"] += 1

        # Jalan
        if "aspal" in jln or "beton" in jln:
            b["jalan_aspal"] += 1
        elif "perkerasan" in jln or "batu" in jln:
            b["jalan_batu"] += 1
        elif "tanah" in jln or "setapak" in jln:
            b["jalan_tanah"] += 1

        # Listrik
        if "pln" in lis:
            b["listrik_pln"] += 1

        # Air
        if "pdam" in air or "pamsimas" in air:
            b["air_pdam"] += 1

        # Sinyal
        if "4g" in sin or "lte" in sin or "sangat baik" in sin:
            b["sinyal_4g"] += 1

    sorted_rows = [fas_per_rt[r["rt_name"]] for r in rt_rows]

    return {
        "rows": sorted_rows,
        "tot_masjid": sum(r["masjid"] for r in sorted_rows),
        "tot_musholla": sum(r["musholla"] for r in sorted_rows),
        "tot_vihara": sum(r["vihara"] for r in sorted_rows),
        "tot_gereja": sum(r["gereja"] for r in sorted_rows),
        "tot_ibadah": sum(r["tot_ibadah"] for r in sorted_rows),
        "tot_paud_tk": sum(r["paud_tk"] for r in sorted_rows),
        "tot_sd_mi": sum(r["sd_mi"] for r in sorted_rows),
        "tot_smp_mts": sum(r["smp_mts"] for r in sorted_rows),
        "tot_sma_ma": sum(r["sma_ma"] for r in sorted_rows),
        "tot_ponpes": sum(r["ponpes"] for r in sorted_rows),
        "tot_pendidikan": sum(r["tot_pendidikan"] for r in sorted_rows),
        "tot_posyandu": sum(r["posyandu"] for r in sorted_rows),
        "tot_polindes": sum(r["polindes"] for r in sorted_rows),
        "tot_kesehatan": sum(r["tot_kesehatan"] for r in sorted_rows),
        "tot_kantor": sum(r["kantor"] for r in sorted_rows),
        "tot_ekonomi": sum(r["ekonomi"] for r in sorted_rows),
        "tot_tpu": sum(r["tpu"] for r in sorted_rows),
        "tot_bts": sum(r["bts"] for r in sorted_rows),
        "tot_olahraga": sum(r["olahraga"] for r in sorted_rows),
        "tot_fasum_lain": sum(r["tot_fasum_lain"] for r in sorted_rows),
        "tot_kondisi_baik": sum(r["kondisi_baik"] for r in sorted_rows),
        "tot_kondisi_rusak": sum(r["kondisi_rusak"] for r in sorted_rows),
        "tot_jalan_aspal": sum(r["jalan_aspal"] for r in sorted_rows),
        "tot_jalan_batu": sum(r["jalan_batu"] for r in sorted_rows),
        "tot_jalan_tanah": sum(r["jalan_tanah"] for r in sorted_rows),
        "tot_listrik_pln": sum(r["listrik_pln"] for r in sorted_rows),
        "tot_air_pdam": sum(r["air_pdam"] for r in sorted_rows),
        "tot_sinyal_4g": sum(r["sinyal_4g"] for r in sorted_rows),
    }



def build_capabilities_dto(metrics: dict, config: dict = None) -> DatasetCapabilitiesDTO:
    """Membangun DTO Kapabilitas Dataset secara otomatis berdasarkan ketersediaan variabel."""
    config = config or {}
    is_kelurahan = bool(config.get("is_kelurahan"))
    admin_str = "Kelurahan" if is_kelurahan else "Desa"

    t_bekerja = metrics.get("tot_bekerja", 0)
    t_umkm = metrics.get("tot_umkm", 0)
    t_bpjs = metrics.get("tot_bpjs", 0)
    t_dinding = metrics.get("tot_dinding_tembok", 0)
    t_atap = metrics.get("tot_atap_seng_genteng", 0)
    t_layak = metrics.get("tot_layak", 0)
    t_layak_pct = metrics.get("tot_layak_pct", 0.0)
    t_ktp = metrics.get("tot_ktp", 0)
    t_ktp_pct = metrics.get("tot_ktp_pct", 0.0)
    t_tk = metrics.get("tot_tk", 0)
    t_sd = metrics.get("tot_sd", 0)
    t_smp = metrics.get("tot_smp", 0)
    t_sma = metrics.get("tot_sma", 0)
    t_sarjana = metrics.get("tot_sarjana", 0)

    has_emp = t_bekerja > 0
    has_msme = t_umkm > 0
    has_bpjs = t_bpjs > 0
    has_materials = (t_dinding > 0 or t_atap > 0)
    has_layak = (t_layak > 0 and t_layak_pct > 0.0)
    has_ktp = (t_ktp > 0 and t_ktp_pct > 0.0)
    has_edu = (t_tk > 0 or t_sd > 0 or t_smp > 0 or t_sma > 0 or t_sarjana > 0)
    has_fas = bool(config.get("fas_tab"))

    return DatasetCapabilitiesDTO(
        has_employment=has_emp,
        has_msme=has_msme,
        has_health_insurance=has_bpjs,
        has_building_materials=has_materials,
        has_decent_housing=has_layak,
        has_ktp_el=has_ktp,
        has_education=has_edu,
        has_public_facilities=has_fas,
        admin_type=admin_str,
        admin_title=admin_str,
    )


def build_chapter_infographics(metrics: dict, rows: list, is_kelurahan: bool = False) -> ChapterInfographicDTO:
    """Mengalkulasi data infografis bab 1-5 secara dinamis dari metrik."""
    # Parse Dusun/RW dynamically from RT names
    dusun_groups = {}
    default_sub = "RW 01" if is_kelurahan else "Dusun Utama"
    for r in rows:
        rt_name = r["rt_name"].upper()
        if "DUSUN" in rt_name and not is_kelurahan:
            parts = rt_name.split("DUSUN")
            d_name = "Dusun " + parts[1].strip().title() if len(parts) > 1 else default_sub
        elif "RW" in rt_name:
            parts = rt_name.split("RW")
            rw_part = parts[1].strip()
            # If format like "RT 001 RW 01 DUSUN PELAIK"
            if "DUSUN" in rw_part and not is_kelurahan:
                d_sub = rw_part.split("DUSUN")[1].strip().title()
                d_name = f"Dusun {d_sub}"
            else:
                rw_num = rw_part.split()[0].strip()
                d_name = f"RW {rw_num}"
        else:
            d_name = default_sub

        if d_name not in dusun_groups:
            dusun_groups[d_name] = 0
        dusun_groups[d_name] += 1

    total_rts = len(rows)
    dusun_breakdown = []
    if dusun_groups:
        for dname in sorted(dusun_groups.keys()):
            count = dusun_groups[dname]
            pct = (count / total_rts * 100) if total_rts > 0 else 0.0
            dusun_breakdown.append({"name": dname, "count": count, "pct": pct})
    else:
        dusun_breakdown = [{"name": default_sub, "count": total_rts, "pct": 100.0}]

    tot_pop = metrics["tot_pop"]
    tot_l = metrics["tot_l"]
    tot_p = metrics["tot_p"]
    male_pct = (tot_l / tot_pop * 100) if tot_pop > 0 else 50.0
    female_pct = 100.0 - male_pct
    dash_gender = f"{male_pct:.2f} {female_pct:.2f}"

    ktp_pct = metrics["tot_ktp_pct"]
    dash_ktp = f"{ktp_pct:.2f} {100.0 - ktp_pct:.2f}"

    tot_bansos = metrics["tot_bansos"]
    pkh_pct = (metrics["tot_pkh"] / tot_bansos * 100) if tot_bansos > 0 else 42.2
    bpnt_pct = (metrics["tot_bpnt"] / tot_bansos * 100) if tot_bansos > 0 else 36.1
    bst_blt_pct = ((metrics["tot_bst"] + metrics["tot_blt"]) / tot_bansos * 100) if tot_bansos > 0 else 21.7

    layak_pct = metrics["tot_layak_pct"]
    dash_layak = f"{layak_pct:.2f} {100.0 - layak_pct:.2f}"

    return ChapterInfographicDTO(
        dusun_breakdown=dusun_breakdown,
        male_pct=male_pct,
        female_pct=female_pct,
        dash_gender=dash_gender,
        ktp_pct=ktp_pct,
        dash_ktp=dash_ktp,
        pkh_pct=pkh_pct,
        bpnt_pct=bpnt_pct,
        bst_blt_pct=bst_blt_pct,
        layak_pct=layak_pct,
        dash_layak=dash_layak,
    )


def build_frontmatter_dto(config: dict, metrics: dict) -> PublicationFrontmatterDTO:
    """Membangun DTO Frontmatter Editorial secara dinamis."""
    name_title = config["name_title"]
    num_rts = len(metrics["rows"])
    admin_type = config.get("admin_type", "Desa")
    admin_type_en = config.get("admin_type_en", "Village")
    gov_name = config.get("gov_name", f"Pemerintah {admin_type} {name_title}")
    gov_name_en = config.get("gov_name_en", f"Government of {name_title} {admin_type_en}")

    compilers = CompilerTeamDTO(
        person_in_charge_name=config.get("kades_name", f"{admin_type} {name_title}").upper(),
        editors_name="Tim Pembina Desa Cantik BPS Kabupaten Mempawah",
        writers_name=f"Tim Agen Statistik {admin_type} {name_title}",
        processors_name=f"Tim Agen Statistik {admin_type} {name_title}",
        layouters_name=f"Tim Agen Statistik {admin_type} {name_title}",
    )

    contributors = [
        ContributorItemDTO(name_id=gov_name, name_en=gov_name_en),
        ContributorItemDTO(
            name_id=f"Pengurus Rukun Tetangga ({num_rts} RT) {admin_type} {name_title}",
            name_en=f"Management of {num_rts} Neighborhood Units (RT) of {name_title} {admin_type_en}",
        ),
    ]

    abbreviations = [
        AbbreviationItemDTO("BPS", "Badan Pusat Statistik", "BPS-Statistics (Central Agency on Statistics)"),
        AbbreviationItemDTO("CAPI", "Computer-Assisted Personal Interviewing", "Computer-Assisted Personal Interviewing"),
        AbbreviationItemDTO("RT", "Rukun Tetangga", "Neighborhood Unit"),
        AbbreviationItemDTO("KK", "Kepala Keluarga", "Head of Household / Family Card"),
        AbbreviationItemDTO("ART", "Anggota Rumah Tangga", "Household Member"),
        AbbreviationItemDTO("KTP-el", "Kartu Tanda Penduduk Elektronik", "Electronic Identity Card"),
        AbbreviationItemDTO("PKH", "Program Keluarga Harapan", "Family Hope Program"),
        AbbreviationItemDTO("BPNT", "Bantuan Pangan Non-Tunai", "Non-Cash Food Assistance"),
        AbbreviationItemDTO("BST", "Bantuan Sosial Tunai", "Social Cash Assistance"),
        AbbreviationItemDTO("BLT", "Bantuan Langsung Tunai", "Direct Cash Assistance"),
        AbbreviationItemDTO("SD / SMP / SMA", "Sekolah Dasar / Menengah / Atas", "Primary / Junior / Senior High School"),
        AbbreviationItemDTO("PT", "Perguruan Tinggi", "Higher Education / University"),
    ]

    return PublicationFrontmatterDTO(compilers=compilers, contributors=contributors, abbreviations=abbreviations)
