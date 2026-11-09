"""
Unit tests for Dental Lead Scraper Intent Analyzer.
"""

import unittest
from dental_scraper.intent_analyzer import IntentAnalyzer

class TestIntentAnalyzer(unittest.TestCase):

    def test_wisdom_tooth_lead_hot(self):
        title = "Có ai biết chỗ nhổ răng khôn uy tín ở Hà Nội không ạ?"
        snippet = "Mình đang bị mọc răng số 8 hàm dưới đau quá sưng cả mặt, cho em hỏi chi phí nhổ bao nhiêu và có đau không mn?"
        url = "https://www.facebook.com/groups/reviewnhakhoa/posts/12345"

        lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url, author="Nguyễn Văn A")

        self.assertEqual(lead.platform, "Facebook")
        self.assertEqual(lead.category, "NHỔ_RĂNG_KHÔN")
        self.assertEqual(lead.location, "Hà Nội")
        self.assertEqual(lead.lead_quality, "HOT")
        self.assertGreaterEqual(lead.intent_score, 70)
        self.assertIn("răng khôn", lead.matched_keywords)

    def test_emergency_toothache(self):
        title = "Cứu em với đau răng quá không ngủ được"
        snippet = "Răng hàm của em bị sâu vào tủy, giờ nhức buốt tận óc, có bác sĩ nào mở cửa khám gấp ban đêm ở TP HCM không ạ?"
        url = "https://voz.vn/t/cuu-em-voi-dau-rang-qua.99999/"

        lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url)

        self.assertEqual(lead.platform, "Voz Forum")
        self.assertEqual(lead.category, "ĐAU_RĂNG_TỦY")
        self.assertEqual(lead.location, "TP. Hồ Chí Minh")
        self.assertEqual(lead.urgency, "Khẩn cấp")
        self.assertEqual(lead.lead_quality, "HOT")

    def test_braces_inquiry(self):
        title = "Xin review địa chỉ niềng răng trong suốt uy tín"
        snippet = "Em 22 tuổi, răng hô nhẹ đang muốn niềng invisalign. Ai từng làm cho em xin review chi phí và thời gian với ạ."
        url = "https://www.reddit.com/r/VietNam/comments/xyz/braces/"

        lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url, author="u/dentallover")

        self.assertEqual(lead.platform, "Reddit")
        self.assertEqual(lead.category, "NIỀNG_RĂNG_CHỈNH_NHA")
        self.assertIn(lead.lead_quality, ["HOT", "WARM"])
        self.assertGreaterEqual(lead.intent_score, 50)

    def test_clinic_promotional_ad_filtered(self):
        title = "Nha Khoa Quốc Tế XYZ - Khuyến Mãi 50% Bọc Răng Sứ"
        snippet = "Ưu đãi cực sốc voucher 2 triệu cho khách hàng đặt lịch ngay hôm nay! Đội ngũ bác sĩ hàng đầu tại nha khoa chúng tôi, liên hệ hotline: 0909123456."
        url = "https://nhakhoaxyz.vn/khuyen-mai-boc-su"

        lead = IntentAnalyzer.analyze(title=title, snippet=snippet, url=url)

        self.assertEqual(lead.lead_quality, "SPAM_AD")
        self.assertFalse(lead.is_lead)

if __name__ == "__main__":
    unittest.main()
