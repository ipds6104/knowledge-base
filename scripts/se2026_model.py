#!/usr/bin/env python3
"""
SE2026 Data Model & Repository Layer (Pythonic ORM/ActiveRecord style)
Menyediakan abstraksi terstruktur, cepat, dan lengkap untuk data SE2026 di SurrealDB:
- Keluarga (Assignment)
- ART (nested_dtsen_var)
- Usaha (se2026_nested)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import urllib.request
import json
import base64

SURREAL_URL = "http://100.88.216.97:8900/sql"
SURREAL_NS = "bps_mempawah"
SURREAL_DB = "se2026"
AUTH_USER = "root"
AUTH_PASS = "root"

def execute_surreal(sql: str, timeout: int = 45) -> List[Dict[str, Any]]:
    auth_str = f"{AUTH_USER}:{AUTH_PASS}"
    auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "surreal-ns": SURREAL_NS,
        "surreal-db": SURREAL_DB,
        "Accept": "application/json",
        "Content-Type": "text/plain"
    }
    req = urllib.request.Request(SURREAL_URL, data=sql.encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0 and data[0].get("result") is not None:
                return data[0]["result"]
            return []
    except Exception as e:
        print(f"[Surreal Error]: {e}")
        return []

@dataclass
class ART:
    assignment_id: str
    nama: str
    ijazah: str = ""
    ijazah_code: str = ""
    status_sekolah: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(
            assignment_id=d.get("assignment_id", ""),
            nama=d.get("nama_dtsen_var", "") or d.get("nama", ""),
            ijazah=d.get("ijazah_label", "") or "",
            ijazah_code=str(d.get("ijazah_value", "") or ""),
            status_sekolah=d.get("sekolah_label", "") or "",
            raw=d
        )

    def get_keluarga(self) -> Optional['Keluarga']:
        return Keluarga.find_by_assignment_id(self.assignment_id)

@dataclass
class Usaha:
    assignment_id: str
    nama_usaha: str
    alamat: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(
            assignment_id=d.get("assignment_id", ""),
            nama_usaha=d.get("nama_usaha", "") or d.get("nama_komersial", ""),
            alamat=d.get("alamat_usaha", "") or d.get("alamat_kp", ""),
            raw=d
        )

    def get_keluarga(self) -> Optional['Keluarga']:
        return Keluarga.find_by_assignment_id(self.assignment_id)

@dataclass
class Keluarga:
    assignment_id: str
    nama_kk: str
    desa: str = ""
    kecamatan: str = ""
    sls: str = ""
    alamat: str = ""
    status_alias: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy_m: Optional[float] = None
    umur_krt: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def maps_direction_url(self) -> str:
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/dir/?api=1&destination={self.latitude},{self.longitude}"
        return ""

    @property
    def maps_pin_url(self) -> str:
        if self.latitude and self.longitude:
            return f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return ""

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        lat = d.get("root_geotag_latitude") or d.get("geotag_latitude")
        lon = d.get("root_geotag_longitude") or d.get("geotag_longitude")
        acc = d.get("root_geotag_accuracy") or d.get("geotag_accuracy")
        try:
            lat = float(lat) if lat is not None else None
            lon = float(lon) if lon is not None else None
            acc = float(acc) if acc is not None else None
        except:
            lat, lon, acc = None, None, None

        return cls(
            assignment_id=d.get("assignment_id", ""),
            nama_kk=d.get("root_nama_kk") or d.get("root_dtsen_nama_kk") or "",
            desa=str(d.get("root_desa", "") or ""),
            kecamatan=str(d.get("root_kec", "") or ""),
            sls=str(d.get("root_nama_sls", "") or ""),
            alamat=str(d.get("root_alamat_klrg") or d.get("root_alamat_prelist") or ""),
            status_alias=str(d.get("assignment_status_alias", "") or ""),
            latitude=lat,
            longitude=lon,
            accuracy_m=acc,
            umur_krt=d.get("root_umur_krt"),
            raw=d
        )

    @classmethod
    def find_by_assignment_id(cls, aid: str) -> Optional['Keluarga']:
        sql = f"SELECT * FROM assignment WHERE assignment_id = '{aid}' LIMIT 1;"
        res = execute_surreal(sql)
        if res:
            return cls.from_dict(res[0])
        return None

    def get_art(self) -> List[ART]:
        sql = f"SELECT * FROM nested_dtsen_var WHERE assignment_id = '{self.assignment_id}';"
        rows = execute_surreal(sql)
        return [ART.from_dict(r) for r in rows]

    def get_usaha(self) -> List[Usaha]:
        sql = f"SELECT * FROM se2026_nested WHERE assignment_id = '{self.assignment_id}';"
        rows = execute_surreal(sql)
        return [Usaha.from_dict(r) for r in rows]

    def get_full_bundle(self) -> Dict[str, Any]:
        """Mengambil bundle lengkap keluarga + semua ART + semua usaha"""
        return {
            "keluarga": self,
            "art_list": self.get_art(),
            "usaha_list": self.get_usaha()
        }

class SE2026Repository:
    """Repository API serbaguna untuk kueri terstruktur"""

    @staticmethod
    def search_art(nama: str, ijazah_min_code: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Cari ART berdasarkan nama dan minimal ijazah.
        ijazah_min_code: '05' (S1), '06' (S2/S3)
        """
        where_parts = [
            "nama_dtsen_var != NONE",
            f"string::uppercase(nama_dtsen_var) CONTAINS '{nama.upper()}'"
        ]
        if ijazah_min_code:
            where_parts.append(f"ijazah_value >= '{ijazah_min_code}'")

        where_clause = " AND ".join(where_parts)
        sql = f"SELECT * FROM nested_dtsen_var WHERE {where_clause} LIMIT {limit};"
        rows = execute_surreal(sql)
        
        results = []
        for r in rows:
            art = ART.from_dict(r)
            keluarga = art.get_keluarga()
            results.append({
                "art": art,
                "keluarga": keluarga
            })
        return results

    @staticmethod
    def search_usaha(nama_usaha: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Cari Usaha dan hubungkan ke lokasi keluarga"""
        sql = f"SELECT * FROM se2026_nested WHERE nama_usaha != NONE AND string::uppercase(nama_usaha) CONTAINS '{nama_usaha.upper()}' LIMIT {limit};"
        rows = execute_surreal(sql)
        results = []
        for r in rows:
            u = Usaha.from_dict(r)
            results.append({
                "usaha": u,
                "keluarga": u.get_keluarga()
            })
        return results

    @staticmethod
    def get_full_household(assignment_id: str) -> Optional[Dict[str, Any]]:
        k = Keluarga.find_by_assignment_id(assignment_id)
        if not k:
            return None
        return k.get_full_bundle()
