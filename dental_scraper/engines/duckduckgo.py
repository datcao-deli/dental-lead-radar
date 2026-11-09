"""
Dental Lead Scraper - DuckDuckGo Search Engine
Crawls public discussions, patient questions, and forum reviews using DDGS.
"""

import ssl
from typing import List
from .base import BaseEngine
from ..intent_analyzer import IntentAnalyzer
from ..models import LeadItem

# Apply safe SSL patch to avoid LibreSSL TLS 1.3 crash on macOS
try:
    from ddgs import http_client2
    def _safe_ssl_context(verify=True):
        ctx = ssl.create_default_context()
        if not verify:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return ctx
    http_client2._get_random_ssl_context = _safe_ssl_context
except Exception:
    pass

from ddgs import DDGS

class DuckDuckGoEngine(BaseEngine):
    """Searches discussions, Q&As, and forum threads via DuckDuckGo."""

    def __init__(self, timeout: int = 15, delay: float = 1.0):
        super().__init__(timeout=timeout, delay=delay)

    def search(self, query: str, limit: int = 15) -> List[LeadItem]:
        leads: List[LeadItem] = []
        clean_query = query.strip()

        # If query is not already quoted, wrap keywords appropriately
        if not ('"' in clean_query or "site:" in clean_query):
            clean_query = f'"{clean_query}"'

        try:
            with DDGS(timeout=self.timeout) as ddgs:
                # Try html backend first for organic SERP
                results = []
                try:
                    results = list(ddgs.text(clean_query, backend="html", max_results=limit))
                except Exception:
                    pass

                # Fallback to api backend if html returns empty
                if not results:
                    try:
                        results = list(ddgs.text(clean_query, backend="api", max_results=limit))
                    except Exception:
                        pass

                for r in results:
                    title = r.get("title", "")
                    snippet = r.get("body", "")
                    url = r.get("href", "")

                    if not title or not url:
                        continue

                    lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url)
                    leads.append(lead)

        except Exception:
            pass

        return leads
