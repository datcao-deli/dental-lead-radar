"""
Unit tests for Dental Lead Scraper Exporters.
"""

import os
import unittest
import tempfile
import json
from dental_scraper.models import LeadItem
from dental_scraper.exporters import CSVExporter, JSONExporter, HTMLExporter

class TestExporters(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sample_leads = [
            LeadItem(
                title="Cần tìm phòng khám nhổ răng khôn",
                snippet="Răng số 8 đau nhức quá mn ơi, ở Cầu Giấy chỗ nào tốt?",
                url="https://facebook.com/post/1",
                platform="Facebook",
                author="Trần B",
                category="NHỔ_RĂNG_KHÔN",
                category_label="Nhổ Răng Khôn (Số 8)",
                urgency="Cao",
                intent_score=85,
                lead_quality="HOT",
                location="Hà Nội",
                matched_keywords=["răng khôn", "đau nhức", "cầu giấy"]
            )
        ]

    def test_csv_exporter(self):
        csv_file = os.path.join(self.temp_dir, "test.csv")
        CSVExporter.export(self.sample_leads, csv_file)

        self.assertTrue(os.path.exists(csv_file))
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            content = f.read()
            self.assertIn("Mã Lead", content)
            self.assertIn("Cầu Giấy", content)
            self.assertIn("Trần B", content)

    def test_json_exporter(self):
        json_file = os.path.join(self.temp_dir, "test.json")
        JSONExporter.export(self.sample_leads, json_file)

        self.assertTrue(os.path.exists(json_file))
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["author"], "Trần B")
            self.assertEqual(data[0]["location"], "Hà Nội")

    def test_html_exporter(self):
        html_file = os.path.join(self.temp_dir, "test.html")
        HTMLExporter.export(self.sample_leads, html_file)

        self.assertTrue(os.path.exists(html_file))
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
            self.assertIn("Dental Lead Radar AI", html)
            self.assertIn("Nhổ Răng Khôn", html)
            self.assertIn("Trần B", html)

if __name__ == "__main__":
    unittest.main()
