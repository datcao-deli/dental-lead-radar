"""
Dental Lead Scraper - Data Models
Defines structured representations of dental leads.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any
import hashlib

@dataclass
class LeadItem:
    id: str = ""
    title: str = ""
    snippet: str = ""
    url: str = ""
    platform: str = "Web"
    author: str = "Ẩn danh"
    published_date: str = ""
    category: str = "KHÁM_TỔNG_QUÁT_LẤY_CAO"
    category_label: str = "Khám Răng / Cạo Vôi / Vệ Sinh"
    urgency: str = "Trung bình"
    intent_score: int = 0
    lead_quality: str = "COLD"  # HOT, WARM, COLD, SPAM_AD
    location: str = "Toàn quốc"
    matched_keywords: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __post_init__(self):
        if not self.id and self.url:
            self.id = hashlib.md5(self.url.encode("utf-8", errors="ignore")).hexdigest()[:12]
        elif not self.id:
            raw = f"{self.title}_{self.snippet}"
            self.id = hashlib.md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["matched_keywords_str"] = ", ".join(self.matched_keywords)
        return data

    @property
    def is_lead(self) -> bool:
        return self.lead_quality in ["HOT", "WARM"]
