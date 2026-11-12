"""
Dental Lead Scraper - Facebook Public Groups & Post Resolver Engine
Extracts real patient inquiries from public Đà Nẵng Facebook groups and resolves Facebook post URLs.
"""

import json
import re
import time
from datetime import datetime
from typing import List, Dict
import primp
from bs4 import BeautifulSoup
from ddgs import DDGS

from .base import BaseEngine
from ..config import DANANG_FACEBOOK_GROUPS
from ..intent_analyzer import IntentAnalyzer
from ..models import LeadItem


class FacebookEngine(BaseEngine):
    """Scrapes public Đà Nẵng Facebook groups and resolves public Facebook post metadata."""

    def __init__(self, timeout: int = 15, delay: float = 0.8):
        super().__init__(timeout=timeout, delay=delay)
        self.client = primp.Client(impersonate="chrome_131", verify=False, timeout=timeout)

    def _extract_group_posts(self, html: str, base_group_url: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        group_title = soup.title.string.strip() if soup.title and soup.title.string else ""
        posts_by_id: Dict[str, Dict[str, str]] = {}

        for s in soup.find_all("script", {"type": "application/json"}):
            txt = s.string or ""
            if "post_id" not in txt or "message" not in txt:
                continue
            try:
                data = json.loads(txt)
            except Exception:
                continue

            def walk(obj):
                if isinstance(obj, dict):
                    if "post_id" in obj and isinstance(obj.get("comet_sections"), dict):
                        pid = str(obj.get("post_id"))
                        cs = obj["comet_sections"]
                        msg = ""

                        def find_msg(o):
                            nonlocal msg
                            if isinstance(o, dict):
                                m = o.get("message")
                                if isinstance(m, dict) and isinstance(m.get("text"), str):
                                    if len(m["text"]) > len(msg):
                                        msg = m["text"]
                                for v in o.values():
                                    if isinstance(v, (dict, list)):
                                        find_msg(v)
                            elif isinstance(o, list):
                                for v in o:
                                    find_msg(v)

                        find_msg(cs)

                        actor = ""

                        def find_actor(o):
                            nonlocal actor
                            if actor:
                                return
                            if isinstance(o, dict):
                                actors = o.get("actors")
                                if isinstance(actors, list) and actors:
                                    a0 = actors[0]
                                    if isinstance(a0, dict) and a0.get("name"):
                                        actor = a0["name"]
                                        return
                                for v in o.values():
                                    if isinstance(v, (dict, list)):
                                        find_actor(v)
                            elif isinstance(o, list):
                                for v in o:
                                    find_actor(v)

                        find_actor(cs)

                        ctime = 0

                        def find_time(o):
                            nonlocal ctime
                            if ctime:
                                return
                            if isinstance(o, dict):
                                if isinstance(o.get("creation_time"), int):
                                    ctime = o["creation_time"]
                                    return
                                for v in o.values():
                                    if isinstance(v, (dict, list)):
                                        find_time(v)
                            elif isinstance(o, list):
                                for v in o:
                                    find_time(v)

                        find_time(cs)

                        plink = (
                            obj.get("permalink_url")
                            or obj.get("url")
                            or f"{base_group_url.rstrip('/')}/posts/{pid}/"
                        )
                        plink = plink.replace("web.facebook.com", "www.facebook.com")

                        if msg and pid and pid not in posts_by_id:
                            pub_time = ""
                            if ctime:
                                try:
                                    pub_time = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")
                                except Exception:
                                    pub_time = ""
                            posts_by_id[pid] = {
                                "post_id": pid,
                                "group_title": group_title,
                                "author": actor or "Thành viên Facebook",
                                "text": msg.strip(),
                                "url": plink,
                                "time": pub_time,
                            }
                    for v in obj.values():
                        if isinstance(v, (dict, list)):
                            walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        walk(v)

            walk(data)

        return list(posts_by_id.values())

    def fetch_public_post_metadata(self, url: str) -> Dict[str, str]:
        """Resolves real title & description for a Facebook URL when search engines hide snippets."""
        try:
            resp = self.client.get(url)
            if resp.status_code != 200 or not resp.text:
                return {}
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            og_desc = soup.find("meta", {"property": "og:description"})
            desc = og_desc.get("content", "").strip() if og_desc else ""
            # Also try extracting embedded Relay message if available
            msgs = re.findall(r'"message":\{"text":"((?:[^"\\]|\\.)*)"', resp.text)
            if msgs:
                try:
                    decoded = json.loads(f'"{msgs[0]}"')
                    if len(decoded) > len(desc):
                        desc = decoded
                except Exception:
                    pass
            return {"title": title, "snippet": desc}
        except Exception:
            return {}

    def scrape_group(self, group_slug: str) -> List[LeadItem]:
        leads: List[LeadItem] = []
        seen_urls = set()
        base_url = f"https://www.facebook.com/groups/{group_slug}/"

        for sort_mode in ("CHRONOLOGICAL", "TOP_POSTS"):
            try:
                time.sleep(self.delay)
                url = f"{base_url}?sorting_setting={sort_mode}"
                resp = self.client.get(url)
                if resp.status_code != 200 or not resp.text:
                    continue
                posts = self._extract_group_posts(resp.text, base_url)
                for p in posts:
                    post_url = p["url"]
                    if post_url in seen_urls:
                        continue
                    seen_urls.add(post_url)

                    text_clean = p["text"]
                    first_line = text_clean.split("\n")[0].strip()
                    title = first_line[:90] + ("..." if len(first_line) > 90 else "")
                    # Preserve group title context for Da Nang location verification
                    context_title = f"[{p['group_title']}] {title}" if p.get("group_title") else title

                    lead = IntentAnalyzer.analyze(
                        title=context_title,
                        snippet=text_clean,
                        url=post_url,
                        author=p["author"],
                        published_date=p["time"],
                    )
                    lead.title = title
                    lead.platform = "Facebook"
                    leads.append(lead)
            except Exception:
                continue

        return leads

    def search(self, query: str, limit: int = 15) -> List[LeadItem]:
        leads: List[LeadItem] = []
        seen_urls = set()

        clean_q = query.strip()
        if clean_q in DANANG_FACEBOOK_GROUPS:
            return self.scrape_group(clean_q)[:limit]

        # 1. If searching general FB queries, first pull fresh posts from public Da Nang dental groups
        if "facebook.com" not in clean_q.lower():
            for grp in DANANG_FACEBOOK_GROUPS:
                for l in self.scrape_group(grp):
                    if l.url not in seen_urls:
                        seen_urls.add(l.url)
                        leads.append(l)

        # 2. Search Yandex / DDG for public Facebook posts & resolve hidden snippets
        fb_query = clean_q if "site:facebook.com" in clean_q.lower() else f'site:facebook.com "Đà Nẵng" "{clean_q}"'
        try:
            with DDGS(timeout=self.timeout) as ddgs:
                for backend in ("yandex", "duckduckgo"):
                    try:
                        results = list(
                            ddgs.text(fb_query, backend=backend, region="vn-vi", max_results=limit)
                        )
                    except Exception:
                        results = []

                    for r in results:
                        href = r.get("href", "")
                        if not href or "facebook.com" not in href.lower() or href in seen_urls:
                            continue
                        # Skip generic profile / video / reel / about links unless post/group
                        href_low = href.lower()
                        if "/about/" in href_low or "/videos/" in href_low:
                            continue

                        title = r.get("title", "")
                        snippet = r.get("body", "")

                        if (
                            "hides the web page description" in snippet.lower()
                            or title.lower().strip() == "link to facebook.com"
                            or len(snippet) < 30
                        ):
                            meta = self.fetch_public_post_metadata(href)
                            if meta:
                                title = meta.get("title") or title
                                snippet = meta.get("snippet") or snippet

                        if not snippet or "hides the web page description" in snippet.lower():
                            continue

                        seen_urls.add(href)
                        lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=href)
                        lead.platform = "Facebook"
                        leads.append(lead)
                        if len(leads) >= limit:
                            break
        except Exception:
            pass

        return leads[:limit]
