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

# Signals indicating marketing / spam / clinics promoting themselves or describing procedures
AD_SPAM_SIGNALS: List[str] = [
    "khuyến mãi", "ưu đãi", "giảm giá", "voucher", "bảng giá 2024", "bảng giá 2025", "bảng giá 2026",
    "nha khoa chúng tôi", "đội ngũ bác sĩ hàng đầu", "công nghệ châu âu",
    "đặt lịch ngay", "liên hệ hotline", "hotline: 0", "inbox để được tư vấn",
    "tuyển dụng", "tuyển phụ tá", "tuyển điều dưỡng", "tuyển bác sĩ",
    "chính sách bảo hành", "hệ thống nha khoa", "chuỗi phòng khám",
    "khách hàng sau khi", "cam kết hoàn tiền", "quà tặng hấp dẫn",
    "tài trợ", "tài trợ 100%", "piezotome", "sóng siêu âm", "cắt nhẹ nhàng",
    "tách dây chằng", "xâm lấn", "đặt bông cầm máu", "khâu đóng", "ổ răng",
    "bác sĩ kiểm tra kỹ", "quy trình thực hiện", "các bước thực hiện", "tại nha khoa",
    "phòng khám chuyên khoa", "bảng giá", "top 5 địa chỉ", "top 10 địa chỉ", "top 7 địa chỉ",
    "top 8 địa chỉ", "địa chỉ uy tín tại", "chi phí chỉ từ", "liên hệ ngay", "ưu đãi lớn",
    "chăm sóc sau khi nhổ", "lợi ích của việc", "là phương pháp", "giúp bạn khắc phục"
]

# Commercial clinic / SEO marketing domains to exclude (not real patient leads)
COMMERCIAL_BLOG_DOMAINS: List[str] = [
    "nhathuoclongchau.com.vn", "tamanhhospital.vn", "nhakhoaident.com", "nhakhoakim.com",
    "drcareimplant.com", "bookingcare.vn", "benhvienthammygangwhoo.com", "nhakhoaparis.vn",
    "nhakhoalacviet.vn", "nhakhoaquoctephuhoa.vn", "nhakhoaparkway.com", "bedental.vn",
    "nhakhoasmileone.vn", "nhakhoashark.vn", "vinmec.com", "medlatec.vn", "hellobacsi.com",
    "nhakhoadana.com", "nhakhoaimplantdanang.com", "benhvienranghammatdn.vn", "nhakhoano1.vn",
    "nhakhoavietphapdn.com", "chingodental.vn", "topnhakhoa.com", "reviewnhakhoa.com",
    "hellodanang.vn", "top10danang.com", "bacsidanang.com", "idcdanang.com", "top360.vn",
    "hanamihotel.com", "topaz.vn", "nhakhoadaisy.vn", "nhakhoathammy.com", "vindentist.vn",
    "wikipedia.org", "youtube.com", "wielkiezarcie.com", "superuser.com", "dell.com",
    "tudientiengviet.org", "soha.vn", "sourceforge.net"
]

# Strict Da Nang districts & keywords - ONLY Đà Nẵng leads accepted
DANANG_DISTRICTS: List[str] = [
    "đà nẵng", "da nang", "hải châu", "thanh khê", "sơn trà", 
    "ngũ hành sơn", "liên chiểu", "cẩm lệ", "hòa vang"
]

# Geographic locations for location matching (Filtered to Đà Nẵng)
LOCATIONS: Dict[str, List[str]] = {
    "Đà Nẵng": DANANG_DISTRICTS
}

# High-conversion intent queries focused STRICTLY on real patient inquiries in Đà Nẵng
DEFAULT_SEARCH_QUERIES: List[Dict[str, str]] = [
    {
        "name": "Voz Forum Đà Nẵng - Khám & điều trị đau răng",
        "dork": 'site:voz.vn "Đà Nẵng" "đau răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Nhổ răng khôn",
        "dork": 'site:voz.vn "Đà Nẵng" "nhổ răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Khám răng & nha khoa",
        "dork": 'site:voz.vn "Đà Nẵng" "khám răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Trồng răng Implant",
        "dork": 'site:voz.vn "Đà Nẵng" "implant"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Niềng răng & chỉnh nha",
        "dork": 'site:voz.vn "Đà Nẵng" "niềng răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Làm răng & bọc sứ",
        "dork": 'site:voz.vn "Đà Nẵng" "làm răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Răng mọc ngầm & mọc lệch",
        "dork": 'site:voz.vn "Đà Nẵng" "răng"'
    },
    {
        "name": "Hỏi đáp Facebook Đà Nẵng - Đau răng & khám răng",
        "dork": 'site:facebook.com "Đà Nẵng" "đau răng"'
    },
    {
        "name": "Hỏi đáp Facebook Đà Nẵng - Nhổ răng khôn review",
        "dork": 'site:facebook.com "Đà Nẵng" "nhổ răng khôn"'
    },
    {
        "name": "Hỏi đáp Facebook Đà Nẵng - Niềng răng review",
        "dork": 'site:facebook.com "Đà Nẵng" "niềng răng"'
    }
]

# User agent rotation list for scrapers
USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0"
]
