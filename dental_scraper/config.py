"""
Dental Lead Scraper - Configuration & Lexicons
Optimized for Vietnamese dental care intent detection and multi-source scraping.
"""

from typing import Dict, List

# Target Dental Categories with associated keywords and weights
# Note: Avoid bare "răng" or bare "làm răng" alone because in Central Vietnamese (Đà Nẵng/Huế)
# "răng" means "how/why" (e.g. "làm răng rứa", "giọng gái Đà Nẵng...").
DENTAL_CATEGORIES: Dict[str, Dict[str, any]] = {
    "NHỔ_RĂNG_KHÔN": {
        "label": "Nhổ Răng Khôn (Số 8)",
        "keywords": [
            "răng khôn", "răng số 8", "nhổ răng khôn", "răng mọc lệch", "răng mọc ngầm",
            "lợi trùm", "viêm lợi trùm", "nhổ răng 8", "tiểu phẫu răng khôn",
            "nhổ 2 cái răng khôn", "nhổ 4 cái răng khôn", "nhổ răng"
        ],
        "default_urgency": "Cao"
    },
    "ĐAU_RĂNG_TỦY": {
        "label": "Đau Răng / Sâu Răng / Tủy",
        "keywords": [
            "đau răng", "nhức răng", "sâu răng", "răng bị sâu", "răng sâu",
            "viêm tủy", "diệt tủy", "lấy tủy", "chữa tủy",
            "buốt răng", "ê buốt răng", "mưng mủ", "chết tủy", "hàn răng", "trám răng",
            "đau nhức răng", "răng ê buốt", "răng lung lay", "chảy máu chân răng",
            "viêm nướu", "sưng nướu", "tụt lợi"
        ],
        "default_urgency": "Khẩn cấp"
    },
    "NIỀNG_RĂNG_CHỈNH_NHA": {
        "label": "Niềng Răng / Chỉnh Nha",
        "keywords": [
            "niềng răng", "chỉnh nha", "mắc cài", "invisalign", "khay niềng",
            "hàm duy trì", "răng hô", "răng móm", "răng khấp khểnh", "răng thưa",
            "niềng răng trong suốt", "bắt vít niềng răng", "chỗ niềng", "nơi niềng"
        ],
        "default_urgency": "Trung bình"
    },
    "TRỒNG_RĂNG_IMPLANT": {
        "label": "Trồng Răng / Cấy Ghép Implant",
        "keywords": [
            "trồng răng", "cấy ghép implant", "mất răng", "implant", "cắm implant",
            "răng giả", "lắp răng giả", "cầu răng sứ", "răng bị gãy", "gãy răng",
            "mất răng hàm", "trồng lại răng"
        ],
        "default_urgency": "Trung bình"
    },
    "RĂNG_SỨ_THẨM_MỸ": {
        "label": "Bọc Răng Sứ / Dán Sứ Thẩm Mỹ",
        "keywords": [
            "bọc răng sứ", "dán sứ", "veneer", "bọc sứ", "răng sứ",
            "tẩy trắng răng", "trắng răng", "răng ố vàng", "cười hở lợi", "cắt lợi",
            "làm răng sứ", "làm răng thẩm mỹ"
        ],
        "default_urgency": "Thấp"
    },
    "KHÁM_TỔNG_QUÁT_LẤY_CAO": {
        "label": "Khám Răng / Cạo Vôi / Vệ Sinh",
        "keywords": [
            "khám răng", "cạo vôi răng", "lấy cao răng", "vệ sinh răng", "cạo vôi",
            "nha khoa uy tín", "xin review nha khoa", "review nha khoa", "phòng khám răng",
            "bác sĩ nha khoa", "nha khoa nào", "nha khoa ở đâu", "nha khoa ok",
            "răng mọc đôi", "chụp phim răng"
        ],
        "default_urgency": "Thấp"
    }
}

# Strong signals indicating an actual user with intent / inquiry
INTENT_SIGNALS: List[str] = [
    # Pronouns & personal voice
    "mình", "em ", " em", "tôi", "tui", "cháu", "mẹ mình", "bố mình", "con mình", "bạn mình", "bé nhà",
    "mọi người ơi", "mn ơi", "các bác ơi", "các thím", "các fen", "mấy bà", "mấy má",
    "cho em hỏi", "cho mình hỏi", "cho e hỏi", "cho tui hỏi", "bác sĩ cho em hỏi",
    # Question / Seeking recommendation
    "xin review", "xin địa chỉ", "ở đâu uy tín", "ở đâu tốt", "ở đâu rẻ", "chỗ nào",
    "nha khoa nào", "phòng khám nào", "bác sĩ nào", "chỗ mô",
    "có đau không", "chi phí thế nào", "giá bao nhiêu", "hết bao nhiêu", "tầm nào",
    "có nên", "ai từng", "ai biết", "giới thiệu cho mình", "cần tìm", "đang tìm",
    "đang có ý định", "đang tính", "cân nhắc", "tư vấn giúp", "tham khảo",
    # Urgency / pain
    "đau quá", "cứu em", "sưng mặt", "không ngủ được", "chảy máu",
    "buốt tận óc", "đau phát khóc", "chịu không nổi", "đau nhức", "bị sâu", "bị ê"
]

# Signals indicating marketing / spam / clinics / group rules / off-topic content
AD_SPAM_SIGNALS: List[str] = [
    "khuyến mãi", "ưu đãi", "giảm giá", "voucher", "bảng giá 2024", "bảng giá 2025", "bảng giá 2026",
    "nha khoa chúng tôi", "đội ngũ bác sĩ hàng đầu", "công nghệ châu âu",
    "đặt lịch ngay", "liên hệ hotline", "hotline:", "inbox để được tư vấn",
    "tuyển dụng", "tuyển phụ tá", "tuyển điều dưỡng", "tuyển bác sĩ",
    "chính sách bảo hành", "hệ thống nha khoa", "chuỗi phòng khám",
    "khách hàng sau khi", "cam kết hoàn tiền", "quà tặng hấp dẫn",
    "tài trợ 100%", "piezotome", "sóng siêu âm", "cắt nhẹ nhàng",
    "tách dây chằng", "xâm lấn", "đặt bông cầm máu", "khâu đóng", "làm sạch ổ răng",
    "bác sĩ kiểm tra kỹ", "quy trình thực hiện", "các bước thực hiện",
    "phòng khám chuyên khoa", "bảng giá", "top 5 địa chỉ", "top 10 địa chỉ", "top 7 địa chỉ",
    "top 8 địa chỉ", "chi phí chỉ từ", "liên hệ ngay", "ưu đãi lớn",
    "chăm sóc sau khi nhổ", "lợi ích của việc", "là phương pháp", "giúp bạn khắc phục",
    "nội quy group", "chào mừng các thành viên mới", "tổng hợp 1 số nha khoa",
    "kiểm thử đăng bài", "test openclaw", "bóc trần", "khởi tố", "cảnh sát điều tra",
    "bàn chải điện", "máy tăm nước", "review bên dưới", "mua nha", "quán cháo lòng",
    "xe ghép", "cho thuê xe", "làm nail", "cắt tóc", "tư vấn giảm mỡ",
    "khóa học", "học viên", "hội thảo", "đăng ký tham dự", "đăng ký ngay", "cấp chứng chỉ", "sốc phản vệ"
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
    "tudientiengviet.org", "soha.vn", "sourceforge.net", "chatgpt.com", "openai.com",
    "zhihu.com", "github.com", "stackoverflow.com", "chegg.com", "dafont.com"
]

# Strict Da Nang districts & keywords - ONLY Đà Nẵng leads accepted
DANANG_DISTRICTS: List[str] = [
    "đà nẵng", "da nang", "hải châu", "thanh khê", "sơn trà",
    "ngũ hành sơn", "liên chiểu", "cẩm lệ", "hòa vang"
]

# Phrases indicating the user is asking about ANOTHER city (reject unless clearly about Đà Nẵng)
OTHER_CITY_SIGNALS: List[str] = [
    "ở hà nội", "tại hà nội", "ngoài hà nội", "khu vực hà nội", "ở hn", "tại hn",
    "ở sài gòn", "tại sài gòn", "ở sg", "tại sg", "[sg]", "[hn]",
    "ở tphcm", "tại tphcm", "ở tp.hcm", "tại tp.hcm", "ở tp hcm", "tp hcm", "tp.hcm", "tphcm",
    "quận 1", "quận 3", "quận 7", "bình thạnh", "thủ đức", "gò vấp", "tân bình",
    "cầu giấy", "đống đa", "trà ôn", "vĩnh long", "hải phòng", "cần thơ", "ở quy nhơn"
]

# Geographic locations for location matching (Filtered to Đà Nẵng)
LOCATIONS: Dict[str, List[str]] = {
    "Đà Nẵng": DANANG_DISTRICTS
}

# Public Da Nang Facebook Groups for direct patient inquiry crawling
DANANG_FACEBOOK_GROUPS: List[str] = [
    "HoiniengrangDaNang",
    "niengrangdanang",
]

# Threads search queries targeting Đà Nẵng patients
THREADS_SEARCH_QUERIES: List[str] = [
    "nha khoa đà nẵng",
    "niềng răng đà nẵng",
    "răng sứ đà nẵng",
    "nhổ răng đà nẵng",
    "đau răng đà nẵng",
    "trồng răng đà nẵng",
    "nha khoa",
    "niềng răng",
]

# High-conversion intent queries focused STRICTLY on real patient inquiries in Đà Nẵng
# Note: Only unambiguous multi-word dental phrases! Never bare "răng".
DEFAULT_SEARCH_QUERIES: List[Dict[str, str]] = [
    {
        "name": "Threads Đà Nẵng - Nha khoa & Niềng răng",
        "dork": "nha khoa đà nẵng"
    },
    {
        "name": "Facebook Groups Đà Nẵng - Hội Niềng Răng & Nha Khoa",
        "dork": "HoiniengrangDaNang"
    },
    {
        "name": "Voz Forum Đà Nẵng - Khám & điều trị đau răng",
        "dork": 'site:voz.vn "Đà Nẵng" "đau răng"'
    },
    {
        "name": "Voz Forum Đà Nẵng - Nhổ răng khôn",
        "dork": 'site:voz.vn "Đà Nẵng" "nhổ răng khôn"'
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
        "name": "Voz Forum Đà Nẵng - Bọc răng sứ",
        "dork": 'site:voz.vn "Đà Nẵng" "răng sứ"'
    },
    {
        "name": "Facebook Đà Nẵng - Hỏi đáp nhổ răng khôn & niềng răng",
        "dork": 'site:facebook.com "Đà Nẵng" "niềng răng"'
    },
    {
        "name": "Webtretho Đà Nẵng - Khám răng & nha khoa",
        "dork": 'site:webtretho.com "Đà Nẵng" "nha khoa"'
    }
]

# User agent rotation list for scrapers
USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0"
]
