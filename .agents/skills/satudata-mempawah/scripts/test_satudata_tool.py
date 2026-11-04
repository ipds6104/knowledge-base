#!/usr/bin/env python3
"""
Test Suite for Satu Data Mempawah Tool and Client
Verifies API communication, CLI subcommands, and deterministic JSON schemas.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
CLI_PATH = SCRIPT_DIR / "satudata_tool.py"
sys.path.insert(0, str(SCRIPT_DIR))

from satudata_client import SatuDataClient, SatuDataAPIError


class TestSatuDataMempawah(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = SatuDataClient(timeout=15)

    def test_client_status(self):
        status = self.client.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn("site_title", status)
        self.assertIn("ckan_version", status)
        self.assertTrue("Mempawah" in status["site_title"])

    def test_client_statistics(self):
        stats = self.client.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertGreaterEqual(stats.get("public_datasets", 0), 400)
        self.assertEqual(stats.get("total_organizations"), 23)
        self.assertEqual(stats.get("total_groups"), 10)

    def test_client_organizations(self):
        orgs = self.client.list_organizations(all_fields=True)
        self.assertIsInstance(orgs, list)
        self.assertEqual(len(orgs), 23)
        names = {o["name"] for o in orgs}
        self.assertIn("badan-pengelola-keuangan-dan-aset-daerah", names)
        self.assertIn("dinas-penanaman-modal-koperasi-ukm-dan-pelayanan-terpadu-satu-pintu", names)
        self.assertIn("dinas-komunikasi-dan-informatika", names)

    def test_client_search_bpkad(self):
        res = self.client.search_packages(fq="organization:badan-pengelola-keuangan-dan-aset-daerah", rows=5)
        self.assertIsInstance(res, dict)
        self.assertGreaterEqual(res.get("count", 0), 3)
        slugs = [d["name"] for d in res.get("results", [])]
        self.assertTrue(any("pendapatan" in s for s in slugs))

    def test_cli_status_json(self):
        cmd = [sys.executable, str(CLI_PATH), "status", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        self.assertIn("status", data)
        self.assertIn("statistics", data)
        self.assertEqual(data["statistics"]["total_organizations"], 23)

    def test_cli_stats_json(self):
        cmd = [sys.executable, str(CLI_PATH), "stats", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        self.assertGreaterEqual(data["public_datasets"], 400)

    def test_cli_opds_json(self):
        cmd = [sys.executable, str(CLI_PATH), "opds", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        orgs = json.loads(proc.stdout)
        self.assertIsInstance(orgs, list)
        self.assertEqual(len(orgs), 23)

    def test_cli_dataset_detail_json(self):
        slug = "jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020"
        cmd = [sys.executable, str(CLI_PATH), "dataset", slug, "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pkg = json.loads(proc.stdout)
        self.assertEqual(pkg.get("name"), slug)
        self.assertGreaterEqual(len(pkg.get("resources", [])), 1)

    def test_cli_preview_csv(self):
        url = "https://satudata.mempawahkab.go.id/datasets/jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020/resources/01a0439d-6a8c-73fe-9678-f47fdbf6aae3/download"
        cmd = [sys.executable, str(CLI_PATH), "preview", url, "--rows", "3", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        rows = json.loads(proc.stdout)
        self.assertIsInstance(rows, list)
        self.assertGreaterEqual(len(rows), 2)
        # Check header
        self.assertIn("pendapatan_daerah", rows[0])

    def test_cli_error_invalid_dataset(self):
        cmd = [sys.executable, str(CLI_PATH), "dataset", "dataset-tidak-pernah-ada-12345", "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        data = json.loads(proc.stdout)
        self.assertFalse(data["success"])
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()

