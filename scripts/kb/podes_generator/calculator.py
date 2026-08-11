"""Data Calculator & Transformer Module for BPS Potensi Desa (PODES)."""

from typing import List, Dict, Any
from .schemas import PodesMetricsDTO, PodesPublicationData


def safe_int(val: Any, default: int = 0) -> int:
    """Mengonversi nilai ke integer secara aman."""
    if val is None:
        return default
    s = str(val).strip().replace(".", "").replace(",", "")
    try:
        return int(s)
    except (ValueError, TypeError):
        return default


def calculate_podes_metrics(raw_data: List[Dict[str, str]], config: dict) -> PodesPublicationData:
    """Merapikan dan mentransformasikan data mentah PODES 2025 menjadi DTO PodesPublicationData."""
    col_name = config["col_name"]
    var_map = {}

    for row in raw_data:
        code = str(row.get("Potensi Desa Tahun 2025", "")).strip()
        var_name = str(row.get("Variabel", "")).strip()
        val = str(row.get(col_name, "")).strip()

        if code:
            var_map[code] = val
        if var_name:
            var_map[var_name] = val

    m = PodesMetricsDTO()

    m.status_daerah = var_map.get("Status Daerah", var_map.get("105", "Perdesaan"))
    m.alamat_lengkap = var_map.get("Alamat Lengkap", var_map.get("108a", "-"))
    m.kawasan_hutan = var_map.get("Lokasi wilayah desa/kelurahan terhadap kawasan hutan", var_map.get("303a", "Di luar kawasan hutan"))
    m.jumlah_rw = safe_int(var_map.get("Jumlah RW di desa/kelurahan", var_map.get("305a", 0)))
    m.jumlah_rt = safe_int(var_map.get("Jumlah RT di desa/kelurahan", var_map.get("305b", 0)))

    m.penduduk_l = safe_int(var_map.get("Jumlah penduduk laki-laki", var_map.get("401a", 0)))
    m.penduduk_p = safe_int(var_map.get("Jumlah penduduk perempuan", var_map.get("401b", 0)))
    m.total_penduduk = m.penduduk_l + m.penduduk_p
    m.sex_ratio = round((m.penduduk_l / max(1, m.penduduk_p)) * 100, 2)

    m.male_pct = round((m.penduduk_l / max(1, m.total_penduduk)) * 100, 1)
    m.female_pct = round((m.penduduk_p / max(1, m.total_penduduk)) * 100, 1)

    m.jumlah_kk = safe_int(var_map.get("Jumlah keluarga", var_map.get("401c", 0)))
    m.kk_pertanian = safe_int(var_map.get("Jumlah keluarga pertanian", var_map.get("401d", 0)))
    m.kk_pertanian_pct = round((m.kk_pertanian / max(1, m.jumlah_kk)) * 100, 1)

    m.listrik_pln = safe_int(var_map.get("Jumlah keluarga pengguna listrik  (PLN)", var_map.get("501a1", 0)))
    m.listrik_non_pln = safe_int(var_map.get("Jumlah keluarga pengguna listrik  (non-PLN)", var_map.get("501a2", 0)))
    m.bukan_listrik = safe_int(var_map.get("Jumlah keluarga bukan pengguna listrik", var_map.get("501b", 0)))
    m.penerangan_jalan = var_map.get("Penerangan di jalan utama desa/kelurahan", var_map.get("502a", "-"))
    m.bakar_masak = var_map.get("Bahan bakar listrik untuk memasak sebagian besar keluarga", var_map.get("503", "-"))
    m.air_minum = var_map.get("Sumber air untuk minum sebagian besar keluarga", var_map.get("508", var_map.get("504", "-")))

    m.bencana_alam = var_map.get("Kejadian/bencana alam yang merugikan bagi masyarakat setahun terakhir", var_map.get("508", "Tidak ada kejadian/bencana alam"))
    m.mitigasi_bencana = var_map.get("Fasilitas/upaya antisipasi/mitigasi bencana alam yang ada di desa/kelurahan", var_map.get("602", "-"))

    m.sarana_pendidikan = var_map.get("Sarana pendidikan (Jumlah)", var_map.get("701", "-"))
    m.sarana_kesehatan = var_map.get("Sarana kesehatan (Jumlah)", var_map.get("704", "-"))
    m.posyandu_aktif = safe_int(var_map.get("Jumlah posyandu dengan kegiatan/pelayanan setiap sebulan sekali", var_map.get("705a", 0)))
    m.posbindu = safe_int(var_map.get("Jumlah posbindu", var_map.get("705c", 0)))

    m.prasarana_transportasi = var_map.get("prasarana dan sarana transportasi antar desa/kelurahan", var_map.get("901a", "-"))
    m.jenis_jalan = var_map.get("Jenis permukaan jalan darat antar desa/kelurahan", var_map.get("901b1", "-"))
    m.jalan_roda4 = var_map.get(" Jalan darat antar desa/kelurahan dapat dilalui kendaraan bermotor roda 4 atau lebih", var_map.get("901b2", "-"))
    m.angkutan_umum = var_map.get("Keberadaan angkutan umum, operasional, dan jam operasi angkutan umum", var_map.get("901c1, 901c2, dan 901c3", "-"))

    m.jumlah_bts = safe_int(var_map.get("Jumlah menara telepon seluler atau Base Transceiver Station (BTS)", var_map.get("904a", 0)))
    m.operator_seluler = var_map.get("Jumlah operator layanan komunikasi telepon seluler", var_map.get("904b", "-"))
    m.sinyal_hp = var_map.get("sinyal telepon seluler", var_map.get("904c", "-"))
    m.sinyal_internet = var_map.get("sinyal internet telepon seluler", var_map.get("904d", "-"))

    m.sarana_ekonomi = var_map.get("Jumlah fasilitas ekonomi di desa/kelurahan", var_map.get("1007", "-"))
    m.sumber_penghasilan_utama = var_map.get("Sumber penghasilan utama sebagian besar penduduk desa/kelurahan", var_map.get("1008a", "-"))
    m.subsektor_utama = var_map.get("Sub sektor utama (jika pertanian)", var_map.get("1008b", "-"))
    m.jumlah_imk = safe_int(var_map.get("Jumlah industri mikro dan kecil (memiliki tenaga kerja kurang dari 20 pekerja)", var_map.get("1009a", 0)))

    m.sistem_informasi_desa = var_map.get("Keberadaan sistem informasi desa", var_map.get("1201a", "-"))
    m.jumlah_sppg = var_map.get("Jumlah SPPG", var_map.get("1301a", "Tidak ada"))
    m.aparatur_pemdes = safe_int(var_map.get("Jumlah aparatur pemerintah desa", var_map.get("1402", 0)))
    m.keberadaan_bpd = var_map.get("apakah ada Badan Permusyawaratan Desa/Lembaga Musyawarah Kelurahan", var_map.get("1403a", "-"))
    m.musyawarah_desa = safe_int(var_map.get("Jumlah kegiatan musyawaran desa/kelurahan", var_map.get("1403c", 0)))

    return PodesPublicationData(config=config, metrics=m, raw_data=raw_data)
