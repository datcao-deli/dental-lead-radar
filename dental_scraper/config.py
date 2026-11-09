"""
Dental Lead Scraper - Configuration & Lexicons
Optimized for Vietnamese dental care intent detection and multi-source scraping.
"""

from typing import Dict, List

# Target Dental Categories with associated keywords and weights
DENTAL_CATEGORIES: Dict[str, Dict[str, any]] = {
    "NHỔ_RĂNG_KHÔN": {
        "label": "Nhổ Răng Khôn (Số 8)",
        "keywords": [
            "răng khôn", "răng số 8", "nhổ răng khôn", "răng mọc lệch", 
            "lợi trùm", "viêm lợi trùm", "nhổ răng 8", "tiểu phẫu răng khôn",
            "nhổ 2 cái răng khôn", "nhổ 4 cái răng khôn"
        ],
        "default_urgency": "Cao"
    },
    "ĐAU_RĂNG_TỦY": {
        "label": "Đau Răng / Sâu Răng / Tủy",
        "keywords": [
            "đau răng", "nhức răng", "sâu răng", "viêm tủy", "diệt tủy",
            "buốt răng", "mưng mủ", "chết tủy", "hàn răng", "trám răng",
            "đau nhức răng", "răng ê buốt", "răng lung lay"
        ],
        "default_urgency": "Khẩn cấp"
    },
    "NIỀNG_RĂNG_CHỈNH_NHA": {
        "label": "Niềng Răng / Chỉnh Nha",
        "keywords": [
            "niềng răng", "chỉnh nha", "mắc cài", "invisalign", "khay niềng",
            "răng hô", "răng móm", "răng khấp khểnh", "răng thưa",
            "niềng răng trong suốt", "bắt vít niềng răng", "chi phí niềng răng"
        ],
        "default_urgency": "Trung bình"
    },
    "TRỒNG_RĂNG_IMPLANT": {
        "label": "Trồng Răng / Cấy Ghép Implant",
        "keywords": [
            "trồng răng", "cấy ghép implant", "mất răng", "implant",
            "răng giả", "lắp răng giả", "cầu răng sứ", "răng bị gãy",
            "mất răng hàm", "trồng lại răng"
        ],
        "default_urgency": "Trung bình"
    },
    "RĂNG_SỨ_THẨM_MỸ": {
        "label": "Bọc Răng Sứ / Dán Sứ Thẩm Mỹ",
        "keywords": [
            "bọc răng sứ", "dán sứ", "veneer", "bọc sứ", "răng sứ thẩm mỹ",
            "tẩy trắng răng", "răng ố vàng", "cười hở lợi", "làm răng thẩm mỹ"
        ],
        "default_urgency": "Thấp"
    },
    "KHÁM_TỔNG_QUÁT_LẤY_CAO": {
        "label": "Khám Răng / Cạo Vôi / Vệ Sinh",
        "keywords": [
            "khám răng", "cạo vôi răng", "lấy cao răng", "vệ sinh răng",
            "nha khoa uy tín", "xin review nha khoa", "phòng khám răng tốt",
            "bác sĩ nha khoa giỏi", "khám răng ở đâu"
        ],
        "default_urgency": "Thấp"
    }
}

# Strong signals indicating an actual user with intent / inquiry
INTENT_SIGNALS: List[str] = [
    # Pronouns & personal voice
    "mình", "em", "tôi", "cháu", "mẹ mình", "bố mình", "con mình", "bạn mình",
    "mọi người ơi", "mn ơi", "các bác ơi", "cho em hỏi", "cho mình hỏi", "bác sĩ cho em hỏi",
    # Question / Seeking recommendation
    "xin review", "xin địa chỉ", "ở đâu uy tín", "ở đâu tốt", "ở đâu rẻ",
    "có đau không", "chi phí thế nào", "giá bao nhiêu", "hết bao nhiêu",
    "bác sĩ nào", "phòng khám nào", "có nên", "ai từng", "kinh nghiệm",
    "tư vấn giúp", "cần tìm", "đang muốn", "dự định", "tính đi",
    # Urgency / pain
    "đau quá", "cứu em", "sưng mặt", "không ngủ được", "chảy máu",
    "buốt tận óc", "đau phát khóc", "chịu không nổi"
]

# Signals indicating marketing / spam / clinics promoting themselves
AD_SPAM_SIGNALS: List[str] = [
    "khuyến mãi", "ưu đãi", "giảm giá", "voucher", "bảng giá 2024", "bảng giá 2025", "bảng giá 2026",
    "nha khoa chúng tôi", "đội ngũ bác sĩ hàng đầu", "công nghệ châu âu",
    "đặt lịch ngay", "liên hệ hotline", "hotline: 0", "inbox để được tư vấn",
    "tuyển dụng", "tuyển phụ tá", "tuyển điều dưỡng", "tuyển bác sĩ",
    "chính sách bảo hành", "hệ thống nha khoa", "chuỗi phòng khám",
    "khách hàng sau khi", "cam kết hoàn tiền", "quà tặng hấp dẫn",
    "tài trợ", "tài trợ 100%"
]

# Commercial clinic / SEO marketing domains to exclude (not real patient leads)
COMMERCIAL_BLOG_DOMAINS: List[str] = [
    "nhathuoclongchau.com.vn", "tamanhhospital.vn", "nhakhoaident.com", "nhakhoakim.com",
    "drcareimplant.com", "bookingcare.vn", "benhvienthammygangwhoo.com", "nhakhoaparis.vn",
    "nhakhoalacviet.vn", "nhakhoaquoctephuhoa.vn", "nhakhoaparkway.com", "bedental.vn",
    "nhakhoasmileone.vn", "nhakhoashark.vn", "vinmec.com", "medlatec.vn", "hellobacsi.com",
    "wikipedia.org", "youtube.com", "wielkiezarcie.com", "superuser.com", "dell.com",
    "tudientiengviet.org", "soha.vn", "sourceforge.net"
]

# Geographic locations for location matching
LOCATIONS: Dict[str, List[str]] = {
    "Hà Nội": ["hà nội", "hn", "cầu giấy", "đống đa", "ba đình", "hoàn kiếm", "thanh xuân", "hai bà trưng", "hoàng mai", "hà đông", "long biên", "tây hồ"],
    "TP. Hồ Chí Minh": ["hồ chí minh", "hcm", "tp hcm", "sài gòn", "q1", "q3", "q5", "q7", "q10", "bình thạnh", "thủ đức", "tân bình", "gò vấp", "phú nhuận"],
    "Đà Nẵng": ["đà nẵng", "hải châu", "thanh khê", "sơn trà"],
    "Hải Phòng": ["hải phòng", "ngô quyền", "lê chân"],
    "Cần Thơ": ["cần thơ", "ninh kiều"],
    "Bình Dương": ["bình dương", "thủ dầu một", "dĩ an", "thuận an"],
    "Đồng Nai": ["đồng nai", "biên hòa"]
}

# High-conversion intent queries that discover real patient questions across forums & social media
DEFAULT_SEARCH_QUERIES: List[Dict[str, str]] = [
    {
        "name": "Voz Forum - Nhổ răng khôn kinh nghiệm & review",
        "dork": '"nhổ răng khôn" site:voz.vn'
    },
    {
        "name": "Voz Forum - Niềng răng & chỉnh nha thực tế",
        "dork": '"niềng răng" site:voz.vn'
    },
    {
        "name": "Voz Forum - Đau răng & điều trị tủy",
        "dork": '"đau răng" site:voz.vn'
    },
    {
        "name": "Voz Forum - Cấy ghép & trồng răng Implant",
        "dork": '"implant" site:voz.vn'
    },
    {
        "name": "Voz Forum - Hỏi đáp nha khoa uy tín",
        "dork": '"nha khoa" site:voz.vn'
    },
    {
        "name": "Tinhte Forum - Review nhổ răng & nha khoa",
        "dork": '"nhổ răng khôn" site:tinhte.vn'
    },
    {
        "name": "Hỏi đáp cộng đồng - Nhổ răng khôn kinh nghiệm",
        "dork": '"cho mình hỏi" "nhổ răng khôn"'
    },
    {
        "name": "Hỏi đáp cộng đồng - Xin review nha khoa uy tín",
        "dork": '"cho mình hỏi" "review nha khoa"'
    },
    {
        "name": "Hỏi đáp cộng đồng - Niềng răng chi phí & đau",
        "dork": '"cho em hỏi" "niềng răng"'
    },
    {
        "name": "Hỏi đáp cộng đồng - Trồng răng Implant review",
        "dork": '"trồng răng implant" "kinh nghiệm"'
    }
]

# User agent rotation list for scrapers
USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0"
]
