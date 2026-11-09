"""
Dental Lead Scraper - Base Engine
Provides HTTP session management, rotating headers, and error handling.
"""

import time
import random
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..config import USER_AGENTS
from ..models import LeadItem

class BaseEngine(ABC):
    """Abstract base class for all scraper engines."""

    def __init__(self, timeout: int = 15, delay: float = 1.0):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()

    def get_random_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

    def safe_get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        req_headers = self.get_random_headers()
        if headers:
            req_headers.update(headers)

        try:
            time.sleep(self.delay + random.uniform(0.1, 0.5))
            response = self.session.get(url, params=params, headers=req_headers, timeout=self.timeout)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                # Rate limited, back off slightly
                time.sleep(3.0)
                return None
            else:
                return None
        except Exception:
            return None

    def safe_post(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        req_headers = self.get_random_headers()
        if headers:
            req_headers.update(headers)

        try:
            time.sleep(self.delay + random.uniform(0.1, 0.5))
            response = self.session.post(url, data=data, headers=req_headers, timeout=self.timeout)
            if response.status_code == 200:
                return response
            return None
        except Exception:
            return None

    @abstractmethod
    def search(self, query: str, limit: int = 20) -> List[LeadItem]:
        """Execute search for leads based on query."""
        pass
