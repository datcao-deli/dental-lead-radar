"""
Dental Lead Scraper - JSON Exporter
Exports leads to formatted JSON.
"""

import json
from typing import List
from ..models import LeadItem

class JSONExporter:
    """Exports a list of LeadItems to JSON file."""

    @classmethod
    def export(cls, leads: List[LeadItem], filepath: str) -> None:
        data = [lead.to_dict() for lead in leads]
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
