"""
Dental Lead Scraper - DuckDuckGo / Yandex Search Engine
Crawls public discussions, patient questions, and forum reviews using DDGS.
"""

import ssl
from typing import List
from .base import BaseEngine
from ..intent_analyzer import IntentAnalyzer
from ..models import LeadItem

# Apply safe SSL patch to avoid LibreSSL TLS 1.3 crash on macOS / older OpenSSL
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
    """Searches discussions, Q&As, and forum threads via Yandex & DuckDuckGo backends."""

    def __init__(self, timeout: int = 15, delay: float = 1.0):
        super().__init__(timeout=timeout, delay=delay)

    def search(self, query: str, limit: int = 15) -> List[LeadItem]:
        leads: List[LeadItem] = []
        clean_query = query.strip()

        if not ('"' in clean_query or "site:" in clean_query):
            clean_query = f'"{clean_query}"'

        # Enforce site: domain restriction if specified
        required_domain = ""
        if "site:" in clean_query:
            parts = clean_query.split("site:")
            if len(parts) > 1:
                required_domain = parts[1].split()[0].replace('"', "").strip().lower()

        results = []
        try:
            with DDGS(timeout=self.timeout) as ddgs:
                for backend in ("yandex", "duckduckgo"):
                    try:
                        res = list(
                            ddgs.text(
                                clean_query,
                                backend=backend,
                                region="vn-vi",
                                max_results=limit,
                            )
                        )
                        if res:
                            results.extend(res)
                    except Exception:
                        continue
        except Exception:
            pass

        seen_urls = set()
        for r in results:
            title = r.get("title", "")
            snippet = r.get("body", "")
            url = r.get("href", "")

            if not title or not url or url in seen_urls:
                continue

            url_lower = url.lower()
            if required_domain and required_domain not in url_lower:
                continue

            # Exclude forum category / pagination listing pages that mix unrelated replies
            if "voz.vn/f/" in url_lower or "tinhte.vn/forums/" in url_lower:
                continue

            seen_urls.add(url)
            lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url)
            leads.append(lead)

        return leads
