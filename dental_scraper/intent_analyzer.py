"""
Dental Lead Scraper - Intent & Lead Scoring Analyzer
Identifies real patients seeking dental treatments vs clinics posting promotional ads.
"""

import re
from typing import Tuple, List, Dict, Any
from .config import DENTAL_CATEGORIES, INTENT_SIGNALS, AD_SPAM_SIGNALS, LOCATIONS
from .models import LeadItem

class IntentAnalyzer:
    """Analyzes text snippets and titles to classify intent, detect spam, and score leads."""

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Remove extra whitespace and linebreaks
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @classmethod
    def detect_platform(cls, url: str) -> str:
        url_lower = url.lower()
        if "facebook.com" in url_lower or "fb.com" in url_lower:
            return "Facebook"
        if "reddit.com" in url_lower:
            return "Reddit"
        if "voz.vn" in url_lower:
            return "Voz Forum"
        if "webtretho.com" in url_lower:
            return "Webtretho"
        if "tiktok.com" in url_lower:
            return "TikTok"
        if "tinhte.vn" in url_lower:
            return "Tinhte"
        return "Web"

    @classmethod
    def extract_location(cls, combined_text: str) -> str:
        text_lower = combined_text.lower()
        for city, keywords in LOCATIONS.items():
            for kw in keywords:
                # Use word boundary where appropriate
                pattern = r'(?<!\w)' + re.escape(kw) + r'(?!\w)'
                if re.search(pattern, text_lower):
                    return city
        return "Toàn quốc"

    @classmethod
    def analyze(cls, title: str, snippet: str, url: str = "", author: str = "Ẩn danh", published_date: str = "") -> LeadItem:
        title_clean = cls.clean_text(title)
        snippet_clean = cls.clean_text(snippet)
        full_text = f"{title_clean} {snippet_clean}".lower()

        matched_kws: List[str] = []
        base_score = 0
        is_spam_ad = False

        # 1. Check for Clinic Ad / Marketing signals (Penalties)
        ad_count = 0
        for ad_kw in AD_SPAM_SIGNALS:
            if ad_kw in full_text:
                ad_count += 1
                base_score -= 25

        if ad_count >= 2:
            is_spam_ad = True

        # 2. Check for Patient Intent Signals (Inquiry, Personal Need, Pain)
        intent_matches = []
        for signal in INTENT_SIGNALS:
            if signal in full_text:
                intent_matches.append(signal)
                base_score += 18
                if signal not in matched_kws:
                    matched_kws.append(signal)

        # 3. Categorize into Dental Category
        best_cat_key = "KHÁM_TỔNG_QUÁT_LẤY_CAO"
        best_cat_info = DENTAL_CATEGORIES[best_cat_key]
        max_kw_count = 0

        for cat_key, cat_data in DENTAL_CATEGORIES.items():
            kw_hits = 0
            for kw in cat_data["keywords"]:
                if kw in full_text:
                    kw_hits += 1
                    if kw not in matched_kws:
                        matched_kws.append(kw)
            
            if kw_hits > max_kw_count:
                max_kw_count = kw_hits
                best_cat_key = cat_key
                best_cat_info = cat_data

        if max_kw_count > 0:
            base_score += (max_kw_count * 15)

        # 4. Urgency Detection
        urgency = best_cat_info["default_urgency"]
        pain_signals = ["đau quá", "cứu em", "sưng mặt", "không ngủ được", "buốt tận óc", "chảy máu", "đau nhức"]
        if any(ps in full_text for ps in pain_signals):
            urgency = "Khẩn cấp"
            base_score += 25

        # 5. Question mark or inquiry structure detection
        if "?" in title_clean or "?" in snippet_clean or "cho em hỏi" in full_text:
            base_score += 15

        # 6. Normalize score between 0 and 100
        final_score = max(0, min(100, base_score))

        # 7. Classify Lead Quality
        if is_spam_ad or final_score < 25:
            lead_quality = "SPAM_AD" if is_spam_ad else "COLD"
        elif final_score >= 70:
            lead_quality = "HOT"
        elif final_score >= 45:
            lead_quality = "WARM"
        else:
            lead_quality = "COLD"

        # Platform & Location
        platform = cls.detect_platform(url)
        location = cls.extract_location(full_text)

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
            location=location,
            matched_keywords=matched_kws
        )
