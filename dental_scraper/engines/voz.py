"""
Dental Lead Scraper - Voz Forum Engine
Targeted scraper for Voz.vn dental discussion threads.
"""

from typing import List
from .base import BaseEngine
from .duckduckgo import DuckDuckGoEngine
from ..models import LeadItem

class VozEngine(BaseEngine):
    """Scrapes Voz.vn threads discussing dental experiences, toothache, and orthodontics."""

    def __init__(self, timeout: int = 15, delay: float = 1.0):
        super().__init__(timeout=timeout, delay=delay)
        self.ddg = DuckDuckGoEngine(timeout=timeout, delay=delay)

    def search(self, query: str, limit: int = 25) -> List[LeadItem]:
        if "site:voz.vn" not in query:
            clean_q = query.strip().replace('"', '')
            voz_dork = f'"{clean_q}" site:voz.vn'
        else:
            voz_dork = query

        results = self.ddg.search(voz_dork, limit=limit)
        for item in results:
            if "voz.vn" in item.url:
                item.platform = "Voz Forum"
        return results
