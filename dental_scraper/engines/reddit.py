"""
Dental Lead Scraper - Reddit Engine
Scrapes discussions from Vietnamese and dental communities on Reddit via public JSON endpoints.
"""

from datetime import datetime
from typing import List, Optional
from .base import BaseEngine
from ..intent_analyzer import IntentAnalyzer
from ..models import LeadItem

class RedditEngine(BaseEngine):
    """Fetches user discussions from Reddit (r/VietNam, r/Dentistry, etc.) without API keys."""

    SUBREDDITS = ["VietNam", "Dentistry", "hanoi", "saigon"]

    def __init__(self, timeout: int = 15, delay: float = 1.0):
        super().__init__(timeout=timeout, delay=delay)
        # Reddit requires a distinctive custom User-Agent to avoid 429
        self.custom_ua = "DentalLeadResearchBot/1.0 (PatientIntentScraper; research)"

    def _search_subreddit(self, subreddit: str, query: str, limit: int = 25) -> List[LeadItem]:
        leads: List[LeadItem] = []
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {
            "q": query,
            "restrict_sr": 1,
            "sort": "new",
            "limit": limit
        }
        headers = {"User-Agent": self.custom_ua}

        resp = self.safe_get(url, params=params, headers=headers)
        if not resp:
            return leads

        try:
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            for post_obj in posts:
                pdata = post_obj.get("data", {})
                title = pdata.get("title", "")
                selftext = pdata.get("selftext", "")
                permalink = pdata.get("permalink", "")
                author = pdata.get("author", "Ẩn danh")
                created_utc = pdata.get("created_utc", 0)

                post_url = f"https://www.reddit.com{permalink}" if permalink else ""
                pub_date = ""
                if created_utc:
                    pub_date = datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S")

                lead = IntentAnalyzer.analyze(
                    title=title,
                    snippet=selftext[:400] if selftext else title,
                    url=post_url,
                    author=f"u/{author}",
                    published_date=pub_date
                )
                leads.append(lead)
        except Exception:
            pass

        return leads

    def search(self, query: str, limit: int = 25) -> List[LeadItem]:
        all_leads: List[LeadItem] = []
        # Search primary subreddit r/VietNam first
        leads = self._search_subreddit("VietNam", query, limit=limit)
        all_leads.extend(leads)

        # Global Reddit query if under limit
        if len(all_leads) < limit:
            url = "https://www.reddit.com/search.json"
            params = {"q": query, "sort": "new", "limit": limit - len(all_leads)}
            resp = self.safe_get(url, params=params, headers={"User-Agent": self.custom_ua})
            if resp:
                try:
                    data = resp.json()
                    posts = data.get("data", {}).get("children", [])
                    for post_obj in posts:
                        pdata = post_obj.get("data", {})
                        title = pdata.get("title", "")
                        selftext = pdata.get("selftext", "")
                        permalink = pdata.get("permalink", "")
                        author = pdata.get("author", "Ẩn danh")
                        created_utc = pdata.get("created_utc", 0)

                        post_url = f"https://www.reddit.com{permalink}" if permalink else ""
                        pub_date = ""
                        if created_utc:
                            pub_date = datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S")

                        lead = IntentAnalyzer.analyze(
                            title=title,
                            snippet=selftext[:400] if selftext else title,
                            url=post_url,
                            author=f"u/{author}",
                            published_date=pub_date
                        )
                        all_leads.append(lead)
                except Exception:
                    pass

        return all_leads[:limit]
