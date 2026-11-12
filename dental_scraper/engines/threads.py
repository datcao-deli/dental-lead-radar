"""
Dental Lead Scraper - Threads Engine (threads.com / Meta Threads)
Extracts real patient posts from public Meta Threads search results without API keys.
"""

import json
import time
import urllib.parse
from datetime import datetime
from typing import List, Dict
import primp
from bs4 import BeautifulSoup

from .base import BaseEngine
from ..intent_analyzer import IntentAnalyzer
from ..models import LeadItem


class ThreadsEngine(BaseEngine):
    """Scrapes public Threads posts (threads.com) discussing dental needs in Đà Nẵng."""

    def __init__(self, timeout: int = 15, delay: float = 0.8):
        super().__init__(timeout=timeout, delay=delay)
        self.client = primp.Client(impersonate="chrome_131", verify=False, timeout=timeout)

    @staticmethod
    def _extract_posts_from_html(html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        extracted: List[Dict[str, str]] = []
        seen_codes = set()

        for s in soup.find_all("script", {"type": "application/json"}):
            txt = s.string or ""
            if "thread_items" not in txt:
                continue
            try:
                data = json.loads(txt)
            except Exception:
                continue

            def walk(obj):
                if isinstance(obj, dict):
                    if "thread_items" in obj and isinstance(obj["thread_items"], list):
                        for item in obj["thread_items"]:
                            post = item.get("post") or {}
                            caption = (post.get("caption") or {}).get("text", "")
                            user = (post.get("user") or {}).get("username", "")
                            code = post.get("code", "")
                            taken_at = post.get("taken_at", 0)
                            if caption and user and code and code not in seen_codes:
                                seen_codes.add(code)
                                pub_time = ""
                                if taken_at:
                                    try:
                                        pub_time = datetime.fromtimestamp(int(taken_at)).strftime("%Y-%m-%d %H:%M:%S")
                                    except Exception:
                                        pub_time = ""
                                extracted.append(
                                    {
                                        "username": user,
                                        "text": caption,
                                        "url": f"https://www.threads.com/@{user}/post/{code}",
                                        "time": pub_time,
                                    }
                                )
                    for v in obj.values():
                        if isinstance(v, (dict, list)):
                            walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        if isinstance(v, (dict, list)):
                            walk(v)

            walk(data)

        return extracted

    def search(self, query: str, limit: int = 20) -> List[LeadItem]:
        leads: List[LeadItem] = []
        seen_urls = set()
        clean_q = query.replace('site:threads.com', '').replace('site:threads.net', '').replace('"', '').strip()
        if not clean_q:
            clean_q = "nha khoa đà nẵng"

        urls_to_fetch = [
            f"https://www.threads.com/search?q={urllib.parse.quote(clean_q)}",
            f"https://www.threads.com/search?q={urllib.parse.quote(clean_q)}&serp_type=recent",
        ]

        valid_count = 0
        for search_url in urls_to_fetch:
            if valid_count >= limit:
                break
            try:
                time.sleep(self.delay)
                resp = self.client.get(search_url)
                if resp.status_code != 200 or not resp.text:
                    continue
                posts = self._extract_posts_from_html(resp.text)
                for p in posts:
                    post_url = p["url"]
                    if post_url in seen_urls:
                        continue
                    seen_urls.add(post_url)

                    text_clean = p["text"].strip()
                    first_line = text_clean.split("\n")[0].strip()
                    title = first_line[:90] + ("..." if len(first_line) > 90 else "")
                    author = f"@{p['username']}"

                    lead = IntentAnalyzer.analyze(
                        title=title,
                        snippet=text_clean,
                        url=post_url,
                        author=author,
                        published_date=p["time"],
                    )
                    lead.platform = "Threads"
                    leads.append(lead)
                    if lead.lead_quality != "SPAM_AD":
                        valid_count += 1
                    if valid_count >= limit:
                        break
            except Exception:
                continue

        return leads
