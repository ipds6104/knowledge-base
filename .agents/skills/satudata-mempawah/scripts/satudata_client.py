"""
Satu Data Mempawah API Client
Handles communication with Portal Satu Data Kabupaten Mempawah CKAN 2.9 API.
Official Portal: https://satudata.mempawahkab.go.id/
"""

import csv
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_BASE_URL = "https://satudata.mempawahkab.go.id/api/3/action"
DEFAULT_TIMEOUT = 20
USER_AGENT = "SatuDataMempawah-Client/1.0 (BPS Mempawah; Linux)"


class SatuDataAPIError(Exception):
    """Custom exception for Satu Data API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class SatuDataClient:
    """Client for Portal Satu Data Mempawah CKAN API."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        if params:
            clean_params = {}
            for k, v in params.items():
                if v is not None:
                    clean_params[k] = "true" if v is True else ("false" if v is False else str(v))
            if clean_params:
                url = f"{url}?{urllib.parse.urlencode(clean_params)}"

        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                status_code = response.getcode()
                raw_data = response.read().decode("utf-8", errors="replace")
                data = json.loads(raw_data)
                if not data.get("success", False):
                    error_msg = data.get("error", {}).get("message", "API status success=false")
                    raise SatuDataAPIError(f"API Error: {error_msg}", status_code, data)
                return data.get("result")
        except urllib.error.HTTPError as e:
            try:
                err_json = json.loads(e.read().decode("utf-8", errors="replace"))
                msg = err_json.get("error", {}).get("message", str(e))
            except Exception:
                msg = str(e)
            raise SatuDataAPIError(f"HTTP {e.code}: {msg}", e.code)
        except urllib.error.URLError as e:
            raise SatuDataAPIError(f"Koneksi gagal: {e.reason}")
        except TimeoutError:
            raise SatuDataAPIError(f"Permintaan timeout setelah {self.timeout} detik")

    def get_status(self) -> Dict[str, Any]:
        """status_show: Info versi portal & engine."""
        return self._request("status_show")

    def get_statistics(self) -> Dict[str, Any]:
        """site_statistics: Rekap total dataset, resources, dan OPD."""
        return self._request("site_statistics")

    def search_packages(
        self,
        q: Optional[str] = None,
        fq: Optional[str] = None,
        rows: int = 10,
        start: int = 0,
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """package_search: Cari dataset publik dengan filter dan kata kunci."""
        params = {"rows": rows, "start": start}
        if q:
            params["q"] = q
        if fq:
            params["fq"] = fq
        if sort:
            params["sort"] = sort
        return self._request("package_search", params)

    def get_package(self, id_or_name: str) -> Dict[str, Any]:
        """package_show: Detail dataset beserta daftar resources lampirannya."""
        return self._request("package_show", {"id": id_or_name})

    def list_packages(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[str]:
        """package_list: Daftar nama/slug seluruh dataset."""
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._request("package_list", params)

    def list_packages_with_resources(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """current_package_list_with_resources."""
        return self._request("current_package_list_with_resources", {"limit": limit, "offset": offset})

    def list_organizations(self, all_fields: bool = True) -> List[Dict[str, Any]]:
        """organization_list: Daftar seluruh OPD produsen data."""
        return self._request("organization_list", {"all_fields": all_fields})

    def get_organization(self, id_or_name: str) -> Dict[str, Any]:
        """organization_show: Detail satu OPD."""
        return self._request("organization_show", {"id": id_or_name})

    def list_groups(self, all_fields: bool = True) -> List[Dict[str, Any]]:
        """group_list: Daftar topik/kategori sektoral."""
        return self._request("group_list", {"all_fields": all_fields})

    def list_tags(self, query: Optional[str] = None) -> List[str]:
        """tag_list: Daftar tag/kata kunci dataset."""
        tags = self._request("tag_list")
        if query and isinstance(tags, list):
            q_lower = query.lower()
            return [t for t in tags if q_lower in t.lower()]
        return tags

    def search_resources(self, query: Optional[str] = None, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """resource_search: Cari berkas lampiran dataset."""
        params = {"limit": limit, "offset": offset}
        if query:
            params["query"] = query
        return self._request("resource_search", params)

    def resolve_resource_url(self, resource_id_or_url: str) -> Tuple[str, str, str]:
        """Mengambil direct download URL, nama file, dan format dari URL atau ID resource."""
        if resource_id_or_url.startswith("http://") or resource_id_or_url.startswith("https://"):
            parsed = urllib.parse.urlparse(resource_id_or_url)
            filename = os.path.basename(parsed.path) or "downloaded_file"
            ext = os.path.splitext(filename)[1].replace(".", "").upper() or "FILE"
            return resource_id_or_url, filename, ext

        res_data = self.search_resources(limit=50)
        results = res_data.get("results", []) if isinstance(res_data, dict) else []
        for r in results:
            if r.get("id") == resource_id_or_url:
                return r.get("url"), r.get("name", "downloaded_file"), r.get("format", "FILE").upper()

        raise SatuDataAPIError(f"Resource dengan ID '{resource_id_or_url}' tidak ditemukan")

    def download_resource(self, resource_id_or_url: str, output_path: Optional[str] = None) -> Path:
        """Unduh berkas resource ke lokasi lokal."""
        download_url, default_name, _ = self.resolve_resource_url(resource_id_or_url)
        dest = Path(output_path) if output_path else Path(default_name)
        dest.parent.mkdir(parents=True, exist_ok=True)

        req = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            content_disp = resp.getheader("Content-Disposition", "")
            if not output_path and "filename=" in content_disp:
                extracted_name = content_disp.split("filename=")[-1].strip('"\'; ')
                if extracted_name:
                    dest = Path(extracted_name)

            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
        return dest

    def preview_resource(self, resource_id_or_url: str, max_rows: int = 10) -> List[List[str]]:
        """Streaming membaca cuplikan baris data dari CSV atau XLSX tanpa download manual."""
        download_url, name, _ = self.resolve_resource_url(resource_id_or_url)
        req = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})

        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            content_disp = resp.getheader("Content-Disposition", "")
            content_type = resp.getheader("Content-Type", "")
            raw_bytes = resp.read(200000)

        if "filename=" in content_disp:
            extracted_name = content_disp.split("filename=")[-1].strip('"\'; ')
            if extracted_name:
                name = extracted_name

        is_xlsx = raw_bytes.startswith(b"PK\x03\x04") or "sheet" in content_type or name.lower().endswith(".xlsx")
        is_csv = "csv" in content_type or name.lower().endswith(".csv") or ("\n" in raw_bytes[:1000].decode("utf-8", errors="ignore") and (b";" in raw_bytes[:1000] or b"," in raw_bytes[:1000]))

        if is_xlsx:
            try:
                import openpyxl
                wb = openpyxl.load_workbook(io.BytesIO(raw_bytes), read_only=True, data_only=True)
                sheet = wb.active
                rows = []
                for i, row in enumerate(sheet.iter_rows(values_only=True)):
                    if i >= max_rows:
                        break
                    rows.append([str(v) if v is not None else "" for v in row])
                return rows
            except Exception:
                pass

        if is_csv:
            text = raw_bytes.decode("utf-8", errors="replace")
            first_line = text.split("\n")[0] if "\n" in text else ""
            if first_line.count(";") >= first_line.count(",") and first_line.count(";") >= first_line.count("\t"):
                delim = ";"
            elif first_line.count("\t") > first_line.count(","):
                delim = "\t"
            else:
                delim = ","

            reader = csv.reader(io.StringIO(text), delimiter=delim)
            rows = []
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                if any(cell.strip() for cell in row):
                    rows.append([cell.strip() for cell in row])
            return rows

        text = raw_bytes.decode("utf-8", errors="replace")
        lines = [l for l in text.splitlines() if l.strip()][:max_rows]
        return [[line] for line in lines]

