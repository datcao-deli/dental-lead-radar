"""
Dental Lead Scraper - Intent & Lead Scoring Analyzer
Identifies real patients seeking dental treatments in Đà Nẵng vs clinics posting promotional ads or off-topic posts.
"""

import re
from typing import List
from .config import (
    DENTAL_CATEGORIES,
    INTENT_SIGNALS,
    AD_SPAM_SIGNALS,
    COMMERCIAL_BLOG_DOMAINS,
    DANANG_DISTRICTS,
    OTHER_CITY_SIGNALS,
)
from .models import LeadItem


class IntentAnalyzer:
    """Analyzes text snippets and titles to classify intent, detect spam, and score leads."""

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @classmethod
    def detect_platform(cls, url: str) -> str:
        url_lower = url.lower()
        if "threads.com" in url_lower or "threads.net" in url_lower:
            return "Threads"
        if "facebook.com" in url_lower or "fb.com" in url_lower:
            return "Facebook"
        if "reddit.com" in url_lower:
            return "Reddit"
        if "voz.vn" in url_lower:
            return "Voz"
        if "webtretho.com" in url_lower:
            return "Webtretho"
        if "tiktok.com" in url_lower:
            return "TikTok"
        if "tinhte.vn" in url_lower:
            return "Tinhte"
        return "Web"

    @classmethod
    def is_danang(cls, full_text: str, url_lower: str) -> bool:
        if any(d in full_text for d in DANANG_DISTRICTS):
            return True
        if any(d in url_lower for d in DANANG_DISTRICTS) or "danang" in url_lower:
            return True
        if re.search(r"\b(?:ở|tại|khu\s+vực|tp\.?)\s*đn\b", full_text):
            return True
        return False

    @classmethod
    def extract_location(cls, combined_text: str, url_lower: str = "") -> str:
        if cls.is_danang(combined_text.lower(), url_lower.lower()):
            return "Đà Nẵng"
        return "Ngoài Đà Nẵng"

    @classmethod
    def analyze(
        cls,
        title: str,
        snippet: str,
        url: str = "",
        author: str = "Ẩn danh",
        published_date: str = "",
    ) -> LeadItem:
        title_clean = cls.clean_text(title)
        snippet_clean = cls.clean_text(snippet)
        full_text = f"{title_clean} {snippet_clean}".lower()
        title_lower = title_clean.lower()
        url_lower = url.lower()

        matched_kws: List[str] = []
        platform = cls.detect_platform(url)

        def reject_item(reason_score: int = 0) -> LeadItem:
            return LeadItem(
                title=title_clean,
                snippet=snippet_clean,
                url=url,
                platform=platform,
                author=author,
                published_date=published_date,
                category="KHÁM_TỔNG_QUÁT_LẤY_CAO",
                category_label="Khám Răng / Cạo Vôi / Vệ Sinh",
                urgency="Thấp",
                intent_score=reason_score,
                lead_quality="SPAM_AD",
                location=cls.extract_location(full_text, url_lower),
                matched_keywords=[],
            )

        # 0. Strict Location Filter: ONLY Đà Nẵng accepted
        if not cls.is_danang(full_text, url_lower):
            return reject_item(0)

        # Reject posts clearly asking about OTHER cities unless explicitly asking about Đà Nẵng in text
        explicit_dn_ask = (
            "ở đà nẵng" in full_text
            or "tại đà nẵng" in full_text
            or "vào đà nẵng" in full_text
            or "khu vực đà nẵng" in full_text
            or "ở đn" in full_text
            or "tại đn" in full_text
        )
        if any(oc in full_text for oc in OTHER_CITY_SIGNALS) and not explicit_dn_ask:
            return reject_item(0)

        # Reject clinic / medical organization accounts posting as pages
        author_lower = (author or "").lower()
        if any(
            org_kw in author_lower
            for org_kw in ["nha khoa", "y khoa", "dental", "clinic", "phòng khám", "bệnh viện", "thẩm mỹ"]
        ):
            return reject_item(0)

        # 1. Reject Commercial clinic domains, SEO listicles, and unrelated sites
        if any(cdom in url_lower for cdom in COMMERCIAL_BLOG_DOMAINS):
            return reject_item(0)

        # Reject subforum listing / megathreads that mix unrelated replies on one page
        if "voz.vn/f/" in url_lower or "tinhte.vn/forums/" in url_lower:
            return reject_item(0)
        if any(
            bad_t in title_lower
            for bad_t in [
                "bảng giá",
                "quy trình",
                "chi phí",
                "top 5",
                "top 10",
                "top 7",
                "điểm báo",
                "chuyện trò linh tinh",
                "bóc trần",
                "tuyển dụng",
            ]
        ):
            return reject_item(0)

        # Reject Facebook group descriptions / hidden description placeholders
        if "the site owner hides the web page description" in full_text:
            return reject_item(0)

        # 2. Reject Clinic procedural, ad, & off-topic signals
        if any(ad_kw in full_text for ad_kw in AD_SPAM_SIGNALS):
            return reject_item(0)

        # 3. MANDATORY Explicit Dental Keyword Match (prevents non-dental threads!)
        best_cat_key = "KHÁM_TỔNG_QUÁT_LẤY_CAO"
        best_cat_info = DENTAL_CATEGORIES[best_cat_key]
        max_kw_count = 0
        total_dental_hits = 0

        for cat_key, cat_data in DENTAL_CATEGORIES.items():
            kw_hits = 0
            for kw in cat_data["keywords"]:
                if kw in full_text:
                    kw_hits += 1
                    total_dental_hits += 1
                    if kw not in matched_kws:
                        matched_kws.append(kw)
            if kw_hits > max_kw_count:
                max_kw_count = kw_hits
                best_cat_key = cat_key
                best_cat_info = cat_data

        # Hard Gate: ZERO dental keywords -> immediately reject!
        if max_kw_count == 0 or total_dental_hits == 0:
            return reject_item(0)

        base_score = 20 + min(30, total_dental_hits * 12)

        # 4. Check for Patient Intent Signals (Inquiry, Personal Need, Pain)
        intent_matches = []
        for signal in INTENT_SIGNALS:
            if signal in full_text:
                intent_matches.append(signal)
                if signal not in matched_kws:
                    matched_kws.append(signal)

        has_question = ("?" in title_clean) or ("?" in snippet_clean) or ("ạ" in full_text)
        pain_signals = [
            "đau quá", "cứu em", "sưng mặt", "không ngủ được", "buốt tận óc",
            "chảy máu", "đau nhức", "bị sâu", "đau răng", "nhức răng", "ê buốt"
        ]
        has_pain = any(ps in full_text for ps in pain_signals)

        # Hard Gate: Require genuine patient inquiry / question / pain (not dry news/promo)
        if not intent_matches and not has_question and not has_pain:
            return reject_item(15)

        base_score += min(30, len(intent_matches) * 10)
        if has_question:
            base_score += 12

        # 5. Urgency Detection
        urgency = best_cat_info["default_urgency"]
        if has_pain:
            urgency = "Khẩn cấp"
            base_score += 15

        # 6. Community discussion boost ONLY after passing dental + Da Nang + intent gates
        if any(
            f in url_lower
            for f in ["threads.com", "threads.net", "facebook.com", "voz.vn", "tinhte.vn", "webtretho.com", "reddit.com"]
        ):
            base_score += 10

        final_score = max(0, min(100, base_score))

        if final_score >= 70:
            lead_quality = "HOT"
        elif final_score >= 45:
            lead_quality = "WARM"
        else:
            lead_quality = "COLD"

        return LeadItem(
            title=title_clean,
            snippet=snippet_clean,
            url=url,
            platform=platform,
            author=author,
            published_date=published_date,
            category=best_cat_key,
            category_label=best_cat_info["label"],
            urgency=urgency,
            intent_score=final_score,
            lead_quality=lead_quality,
            location="Đà Nẵng",
            matched_keywords=matched_kws,
        )
