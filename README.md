# 🦷 Dental Lead Radar AI (Hệ Thống Quét & Quản Lý Khách Hàng Nha Khoa)

Hệ thống thông minh toàn diện (Fullstack) kết hợp bộ cào dữ liệu đa nguồn (Facebook, Voz, Otofun, Webtretho, v.v.), bộ lọc NLP phân tích ý định bệnh nhân (Intent Scoring) và giao diện Web Dashboard quản lý khách hàng chuyên nghiệp (**DentaLead App - Elastic Toggle Switch**).

---

## 🌟 Tổng Quan Tính Năng Tích Hợp

### 1. Giao Diện Web DentaLead Hiện Đại (Figma Make App)
- **Khu vực Kinh doanh (Sales Dashboard)**:
  - Danh sách khách hàng tiềm năng phân loại tự động: *Khách mới, Cần chăm sóc, Đã đặt lịch, Tiềm năng, Không phù hợp*.
  - Bộ lọc tức thì theo: Tên, số điện thoại, nhu cầu, khu vực, nền tảng (Facebook, Voz, Web, TikTok, Threads).
  - Thẻ thống kê chỉ số: Đã đặt lịch, Cần chăm sóc, Khách mới, Tỷ trọng nguồn khách.
  - Hộp chi tiết khách hàng (**Lead Drawer**): Xem điểm nhu cầu AI (0-100), nội dung bài đăng gốc, nút **"Mở bài đăng"** trực tiếp đến link gốc, cập nhật trạng thái và lưu ghi chú tư vấn vào hệ thống.
  - Nút **"Xuất Excel CSV"**: Xuất dữ liệu chuẩn UTF-8 BOM, không lỗi font tiếng Việt trên Microsoft Excel.

- **Trung Tâm Quản Trị (Admin Dashboard)**:
  - **Trình thu thập**: Giám sát trạng thái cào đa nguồn, nhập từ khóa tìm kiếm tùy chỉnh và bấm nút **"Bắt đầu quét ngay"**.
  - **Từ khóa & Nguồn**: Bộ từ khóa chuyên sâu nha khoa (*Nhổ răng khôn, Niềng răng, Trồng răng Implant, v.v.*) với tính năng bấm quét nhanh theo từng từ khóa.
  - **Phân phối khách**: Tự động phân chia khách hàng theo dịch vụ và khu vực phụ trách.
  - **Chế độ Sáng / Tối (Light & Dark theme)**: Chuyển đổi mượt mà theo sở thích.

### 2. Bộ Lõi Cào & Phân Tích Ý Định Bệnh Nhân (Python NLP Engine)
- Tự động nhận diện nhu cầu cá nhân (*đau nhức, viêm tủy, tìm địa chỉ uy tín, hỏi chi phí*).
- Loại bỏ hoàn toàn bài đăng quảng cáo / spam tiếp thị của các phòng khám nha khoa.
- Tự động chấm điểm Intent (0 - 100) và xếp loại: 🔥 **HOT**, ⚡ **WARM**, ❄️ **COLD**.

---

## 🚀 Hướng Dẫn Khởi Chạy

### Cách 1: Khởi chạy Trọn Gói Fullstack (Khuyến nghị)
Một lệnh duy nhất để khởi động toàn bộ hệ thống (Web App + Backend API + Trình cào dữ liệu):

```bash
cd /Users/apple/.gemini/antigravity/scratch/dental-lead-scraper
source .venv/bin/activate
python main.py --web
```
Trình duyệt sẽ tự động mở tại: **`http://localhost:8080`**

---

### Cách 2: Khởi chạy chế độ Phát Triển Frontend (Hot Reload)
Nếu bạn muốn chỉnh sửa trực tiếp giao diện React / Vite:

```bash
# Terminal 1: Chạy Python API Server
cd /Users/apple/.gemini/antigravity/scratch/dental-lead-scraper
source .venv/bin/activate
python -m dental_scraper.server

# Terminal 2: Chạy Vite Dev Server
cd /Users/apple/.gemini/antigravity/scratch/dental-lead-scraper/web
npm run dev
```

---

### Cách 3: Chạy Quét Bằng Dòng Lệnh (CLI)
Nếu muốn chạy cào ngầm xuất file mà không mở trình duyệt:
```bash
# Quét tự động tất cả danh mục
python main.py

# Quét từ khóa cụ thể
python main.py -q "nhổ răng khôn Hà Nội cho em hỏi"

# Chỉ lấy lead nóng (Điểm >= 60)
python main.py --min-score 60
```

---

## 📁 Cấu Trúc Hệ Thống

```
dental-lead-scraper/
├── .venv/                      # Virtual environment Python
├── requirements.txt            # Thư viện Python (requests, beautifulsoup4, ddgs, rich)
├── README.md                   # Tài liệu hướng dẫn
├── main.py                     # Entry point chính
├── dental_scraper/             # Backend Python
│   ├── config.py               # Cấu hình từ khóa intent, dorks, bộ lọc spam
│   ├── models.py               # Data model LeadItem
│   ├── intent_analyzer.py      # Bộ lọc NLP chấm điểm khách hàng
│   ├── engines/                # Engines cào dữ liệu (DDG, Reddit, Voz, Web)
│   ├── exporters/              # Xuất dữ liệu (CSV Excel UTF-8, JSON, HTML)
│   ├── server.py               # REST API Server & phục vụ web app
│   └── cli.py                  # Runner dòng lệnh
├── web/                        # Mã nguồn giao diện React + Vite + Tailwind (Elastic Toggle Switch)
│   ├── src/
│   │   ├── App.tsx             # Giao diện chính DentaLead kết nối API
│   │   ├── index.css           # Toàn bộ styling và hiệu ứng màu sắc
│   │   └── main.tsx            # Điểm nạp React 19
│   ├── dist/                   # Bản build sản phẩm sẵn sàng phục vụ
│   └── package.json
└── output/                     # Thư mục lưu dữ liệu thực tế
    ├── leads.json              # Dữ liệu JSON thời gian thực
    └── leads.csv               # Bảng tính Excel chuẩn UTF-8
```

---

## 🧪 Kiểm Thử Hệ Thống
```bash
python -m unittest discover tests
```
Đã kiểm thử toàn diện: 7/7 bài kiểm tra tự động đạt chuẩn 100%.
