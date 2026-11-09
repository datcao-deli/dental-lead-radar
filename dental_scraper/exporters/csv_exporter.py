"""
Dental Lead Scraper - CSV Exporter
Exports leads to CSV format with UTF-8 BOM encoding for seamless Microsoft Excel compatibility.
"""

import csv
from typing import List
from ..models import LeadItem

class CSVExporter:
    """Exports a list of LeadItems to CSV file."""

    FIELDNAMES = [
        "id", "lead_quality", "intent_score", "category_label", 
        "urgency", "location", "platform", "author", 
        "title", "snippet", "matched_keywords_str", "url", "created_at"
    ]

    HEADER_NAMES = [
        "Mã Lead", "Chất Lượng Lead", "Điểm Ý Định (0-100)", "Nhu Cầu Nha Khoa",
        "Mức Khẩn Cấp", "Khu Vực", "Nền Tảng", "Tác Giả",
        "Tiêu Đề", "Nội Dung Tóm Tắt", "Từ Khóa Phát Hiện", "Link Bài Viết", "Thời Gian Thu Thập"
    ]

    @classmethod
    def export(cls, leads: List[LeadItem], filepath: str) -> None:
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cls.HEADER_NAMES)
            for lead in leads:
                writer.writerow([
                    lead.id,
                    lead.lead_quality,
                    lead.intent_score,
                    lead.category_label,
                    lead.urgency,
                    lead.location,
                    lead.platform,
                    lead.author,
                    lead.title,
                    lead.snippet,
                    ", ".join(lead.matched_keywords),
                    lead.url,
                    lead.created_at
                ])
