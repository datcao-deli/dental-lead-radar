"""
Dental Lead Scraper - Fullstack REST API & Static Server
Connects the React/Vite DentaLead UI with the Python crawler engine.
"""

import os
import json
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .cli import DentalLeadScanner
from .config import COMMERCIAL_BLOG_DOMAINS
from .exporters import CSVExporter, JSONExporter, HTMLExporter
from .models import LeadItem

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(PROJECT_ROOT, "web", "dist")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LEADS_FILE = os.path.join(OUTPUT_DIR, "leads.json")
CSV_FILE = os.path.join(OUTPUT_DIR, "leads.csv")

# Auth Users Configuration
AUTH_USERS = {
    "admin": {
        "passwords": ["123", "admin123", "admin@2026"],
        "user": {
            "id": "usr_admin",
            "username": "admin",
            "name": "Nha Khoa Admin",
            "role": "admin",
            "roleLabel": "Quản trị viên hệ thống",
            "avatar": "AD",
            "email": "admin@dentalead.vn",
        }
    },
    "nhanvien": {
        "passwords": ["123", "123456"],
        "user": {
            "id": "usr_sales1",
            "username": "nhanvien",
            "name": "Linh Nguyễn",
            "role": "sales",
            "roleLabel": "Chuyên viên tư vấn & CSKH",
            "avatar": "LN",
            "email": "linhnguyen@dentalead.vn",
        }
    },
    "linhnguyen": {
        "passwords": ["123", "123456"],
        "user": {
            "id": "usr_sales1",
            "username": "linhnguyen",
            "name": "Linh Nguyễn",
            "role": "sales",
            "roleLabel": "Chuyên viên tư vấn & CSKH",
            "avatar": "LN",
            "email": "linhnguyen@dentalead.vn",
        }
    },
    "huypham": {
        "passwords": ["123", "123456"],
        "user": {
            "id": "usr_sales2",
            "username": "huypham",
            "name": "Huy Phạm",
            "role": "sales",
            "roleLabel": "Tư vấn viên Implant",
            "avatar": "HP",
            "email": "huypham@dentalead.vn",
        }
    },
    "maitran": {
        "passwords": ["123", "123456"],
        "user": {
            "id": "usr_sales3",
            "username": "maitran",
            "name": "Mai Trần",
            "role": "sales",
            "roleLabel": "Trưởng nhóm CSKH",
            "avatar": "MT",
            "email": "maitran@dentalead.vn",
        }
    }
}

# Global scanner lock and status
scanner_lock = threading.Lock()
is_scanning = False
last_scan_result = {"total": 0, "message": "Sẵn sàng"}

def load_leads_from_disk() -> List[Dict[str, Any]]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        return []
    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            formatted = []
            for l in raw:
                item = dict(l)
                if not item.get("name") or item.get("name") == "Ẩn danh":
                    author = l.get("author", "")
                    if author and author != "Ẩn danh":
                        item["name"] = author
                    else:
                        item["name"] = (l.get("title", "")[:35] + "...") if l.get("title") else "Khách hàng"
                if not item.get("handle"):
                    plat = l.get("platform", "Web").lower().replace(" ", "")
                    item["handle"] = f"@{plat}"
                if not item.get("phone"):
                    item["phone"] = "Chưa có SĐT"
                if not item.get("need"):
                    item["need"] = l.get("category_label", "Khám răng")
                if not item.get("status"):
                    item["status"] = "New"
                if not item.get("agent"):
                    item["agent"] = "Chưa phân công"
                if not item.get("agentInitials"):
                    item["agentInitials"] = "—"
                if not item.get("score"):
                    item["score"] = l.get("intent_score", 60)
                if not item.get("time"):
                    item["time"] = l.get("created_at", "Vừa xong")
                if not item.get("post"):
                    title = l.get("title", "")
                    snippet = l.get("snippet", "")
                    item["post"] = f"{title}. {snippet}".strip()
                if not item.get("note"):
                    kw = l.get("matched_keywords", [])
                    item["note"] = f"Từ khóa phát hiện: {', '.join(kw)}" if kw else "Cần liên hệ tư vấn nhu cầu"
                formatted.append(item)
            return formatted
    except Exception:
        return []

def save_leads_to_disk(leads: List[Dict[str, Any]]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)

    # Also update CSV
    lead_items = []
    for l in leads:
        lead_items.append(LeadItem(
            id=str(l.get("id", "")),
            title=l.get("title", l.get("name", "")),
            snippet=l.get("snippet", l.get("post", "")),
            url=l.get("url", ""),
            platform=l.get("platform", "Web"),
            author=l.get("author", l.get("name", "")),
            category=l.get("category", "KHÁM_TỔNG_QUÁT_LẤY_CAO"),
            category_label=l.get("category_label", l.get("need", "")),
            urgency=l.get("urgency", "Trung bình"),
            intent_score=int(l.get("intent_score", l.get("score", 50))),
            lead_quality=l.get("lead_quality", "WARM"),
            location=l.get("location", "Toàn quốc"),
            matched_keywords=l.get("matched_keywords", [])
        ))
    CSVExporter.export(lead_items, CSV_FILE)

# Auto-Crawler & Anti-Sleep configuration
auto_crawler_state = {
    "enabled": True,
    "interval_seconds": 3600,  # 1 hour
    "hourly_target": 10,       # 10 new real leads per run
    "is_crawling": False,
    "last_run": None,
    "next_run": None,
    "leads_added_last_run": 0,
    "total_runs": 0,
    "message": "Đang chạy chế độ tự động cào: 1 tiếng / lần (dừng sau khi đủ 10 bài mới)"
}

anti_sleep_state = {
    "enabled": True,
    "interval_seconds": 540,   # 9 minutes
    "last_ping": None,
    "total_pings": 0,
    "status": "Hoạt động 24/7 (tự động ping mỗi 9 phút)",
    "target_url": os.environ.get("RENDER_EXTERNAL_URL", "https://dental-lead-radar.onrender.com")
}

def extract_phone_from_text(text: str) -> str:
    cleaned = re.sub(r"[\s\.\-]", "", text)
    match = re.search(r"(0[3|5|7|8|9][0-9]{8})\b", cleaned)
    if match:
        raw = match.group(1)
        return f"{raw[:4]} {raw[4:7]} {raw[7:]}"
    return "Chưa có SĐT"

def format_clean_author(item: LeadItem) -> str:
    if item.author and item.author != "Ẩn danh":
        return item.author
    url_lower = item.url.lower()
    if "voz.vn" in url_lower:
        return "Thành viên VOZ"
    if "tinhte.vn" in url_lower:
        return "Thành viên Tinh Tế"
    if "webtretho.com" in url_lower:
        return "Thành viên Webtretho"
    if "reddit.com" in url_lower:
        return "Reddit User"
    if "otofun.net" in url_lower:
        return "Thành viên Otofun"
    return "Bệnh nhân cần tư vấn"

def run_real_lead_scrape(target_new: int = 10, custom_query: str = "") -> int:
    global last_scan_result
    scanner = DentalLeadScanner(delay=0.8)
    existing_leads = load_leads_from_disk()
    existing_urls = {l.get("url") for l in existing_leads if l.get("url")}
    existing_ids = {str(l.get("id")) for l in existing_leads}

    added_leads = []
    
    # Target real Vietnamese patient discussion queries
    queries_to_run = [
        '"nhổ răng khôn" site:voz.vn',
        '"niềng răng" site:voz.vn',
        '"đau răng" site:voz.vn',
        '"implant" site:voz.vn',
        '"nha khoa" site:voz.vn',
        '"nhổ răng khôn" site:tinhte.vn',
        '"cho mình hỏi" "nhổ răng khôn"',
        '"cho mình hỏi" "review nha khoa"',
        '"cho em hỏi" "niềng răng"',
        '"trồng răng implant" "kinh nghiệm"'
    ]

    if custom_query:
        queries_to_run.insert(0, custom_query)

    for q in queries_to_run:
        if len(added_leads) >= target_new:
            break
        try:
            results = scanner.ddg.search(q, limit=5)
            for r in results:
                url_lower = r.url.lower()
                # Exclude commercial clinic ads & blogs
                if any(cd in url_lower for cd in COMMERCIAL_BLOG_DOMAINS):
                    continue
                if r.url in existing_urls or str(r.id) in existing_ids:
                    continue
                if r.lead_quality == "SPAM_AD" or r.intent_score < 35:
                    continue

                existing_urls.add(r.url)
                existing_ids.add(str(r.id))

                lead_dict = r.to_dict()
                lead_dict["name"] = format_clean_author(r)
                if "voz" in r.platform.lower():
                    lead_dict["platform"] = "Voz"
                elif "facebook" in r.platform.lower():
                    lead_dict["platform"] = "Facebook"
                else:
                    lead_dict["platform"] = "Web"
                lead_dict["handle"] = f"@{lead_dict['platform'].lower()}"
                lead_dict["phone"] = extract_phone_from_text(f"{r.title} {r.snippet}")
                lead_dict["need"] = r.category_label
                lead_dict["status"] = "New"
                lead_dict["agent"] = "Chưa phân công"
                lead_dict["agentInitials"] = "—"
                lead_dict["score"] = r.intent_score
                lead_dict["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lead_dict["post"] = f"{r.title} — {r.snippet}".strip()
                lead_dict["note"] = f"Dữ liệu thật từ {r.platform}. Độ tin cậy ý định: {r.intent_score}đ."

                added_leads.append(lead_dict)
                if len(added_leads) >= target_new:
                    break
        except Exception as e:
            print(f"Error querying {q}: {e}")

    if added_leads:
        for nl in reversed(added_leads):
            existing_leads.insert(0, nl)
        save_leads_to_disk(existing_leads)

    last_scan_result = {
        "total": len(existing_leads),
        "added": len(added_leads),
        "message": f"Đã thu thập thành công {len(added_leads)} bài viết thật mới từ diễn đàn!"
    }
    return len(added_leads)

def auto_crawler_loop():
    time.sleep(8)
    while True:
        try:
            auto_crawler_state["is_crawling"] = True
            auto_crawler_state["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [Auto-Crawler] Bắt đầu chu kỳ quét 10 bài viết thật mới...")
            with scanner_lock:
                added = run_real_lead_scrape(target_new=10)
            auto_crawler_state["leads_added_last_run"] = added
            auto_crawler_state["total_runs"] += 1
            auto_crawler_state["is_crawling"] = False
            next_dt = datetime.now() + timedelta(seconds=auto_crawler_state["interval_seconds"])
            auto_crawler_state["next_run"] = next_dt.strftime("%Y-%m-%d %H:%M:%S")
            auto_crawler_state["message"] = f"Đã quét xong: thêm {added} bài mới. Lần quét kế tiếp lúc: {auto_crawler_state['next_run']}"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [Auto-Crawler] {auto_crawler_state['message']}. Nghỉ 1 tiếng...")
        except Exception as e:
            auto_crawler_state["is_crawling"] = False
            auto_crawler_state["message"] = f"Lỗi cào tự động: {e}"
            print(f"[Auto-Crawler] Lỗi: {e}")

        time.sleep(auto_crawler_state["interval_seconds"])

def anti_sleep_keeper_loop():
    time.sleep(20)
    while True:
        try:
            target_url = anti_sleep_state["target_url"].rstrip("/")
            ping_url = f"{target_url}/api/status"
            req = urllib.request.Request(
                ping_url,
                headers={"User-Agent": "DentalLeadRadar-AntiSleep/1.0 (KeepAlive; 24/7)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = resp.getcode()
                anti_sleep_state["last_ping"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                anti_sleep_state["total_pings"] += 1
                anti_sleep_state["status"] = f"Hoạt động 24/7 (Đã ping {anti_sleep_state['total_pings']} lần - HTTP {code})"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [Anti-Sleep] Ping thành công {ping_url} (HTTP {code}) -> Giữ web thức 24/7.")
        except Exception as e:
            anti_sleep_state["status"] = f"Hoạt động 24/7 (Standby: {e})"

        time.sleep(anti_sleep_state["interval_seconds"])

class DentalApiHandler(BaseHTTPRequestHandler):
    """Handles REST API calls and serves the production React bundle."""

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Get leads
        if path == "/api/leads":
            leads = load_leads_from_disk()
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "leads": leads,
                "is_scanning": is_scanning,
                "last_scan": last_scan_result
            }, ensure_ascii=False).encode("utf-8"))
            return

        # API: Scanner status & background workers
        if path == "/api/status":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "is_scanning": is_scanning or auto_crawler_state["is_crawling"],
                "last_scan": last_scan_result,
                "auto_crawler": auto_crawler_state,
                "anti_sleep": anti_sleep_state
            }, ensure_ascii=False).encode("utf-8"))
            return

        # API: Summary Stats
        if path == "/api/stats":
            leads = load_leads_from_disk()
            total = len(leads)
            platforms = {}
            categories = {}
            for l in leads:
                p = l.get("platform", "Web")
                platforms[p] = platforms.get(p, 0) + 1
                c = l.get("category_label", l.get("need", "Khác"))
                categories[c] = categories.get(c, 0) + 1

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "total": total,
                "platforms": platforms,
                "categories": categories,
                "is_scanning": is_scanning
            }, ensure_ascii=False).encode("utf-8"))
            return

        # API: Auth users list
        if path == "/api/auth/users":
            self._set_headers(200, "application/json")
            users_list = [v["user"] for k, v in AUTH_USERS.items() if k in ["admin", "linhnguyen", "huypham", "maitran"]]
            self.wfile.write(json.dumps({"users": users_list}, ensure_ascii=False).encode("utf-8"))
            return

        # Serve static React UI files
        self._serve_static(path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Authentication Login
        if path == "/api/auth/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            payload = json.loads(body) if body else {}
            username = str(payload.get("username", "")).strip().lower()
            password = str(payload.get("password", "")).strip()

            account = AUTH_USERS.get(username)
            if account and password in account["passwords"]:
                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps({
                    "success": True,
                    "token": f"dnt_token_{username}_valid",
                    "user": account["user"]
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self._set_headers(401, "application/json")
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Tên đăng nhập hoặc mật khẩu không chính xác!"
                }, ensure_ascii=False).encode("utf-8"))
            return

        # API: Authentication Logout
        if path == "/api/auth/logout":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"success": True, "message": "Đã đăng xuất"}).encode("utf-8"))
            return

        # API: Trigger live scan
        if path == "/api/scan":
            global is_scanning
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            params = json.loads(body) if body else {}
            query = params.get("query", "")
            limit = int(params.get("limit", 10))

            if is_scanning or auto_crawler_state["is_crawling"]:
                self._set_headers(409, "application/json")
                self.wfile.write(json.dumps({"error": "Trình cào đang hoạt động, vui lòng đợi."}).encode("utf-8"))
                return

            def background_manual_scan():
                global is_scanning
                with scanner_lock:
                    is_scanning = True
                    try:
                        run_real_lead_scrape(target_new=limit, custom_query=query)
                    finally:
                        is_scanning = False

            threading.Thread(target=background_manual_scan, daemon=True).start()

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "message": "Đã bắt đầu tiến trình quét 10 bài viết thật mới từ các diễn đàn thảo luận!",
                "is_scanning": True
            }).encode("utf-8"))
            return

        self._set_headers(404)

    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Update lead status or note (/api/leads/<id>)
        if path.startswith("/api/leads/"):
            lead_id = path.split("/api/leads/")[1].strip()
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            payload = json.loads(body) if body else {}

            leads = load_leads_from_disk()
            updated = False
            for l in leads:
                if str(l.get("id")) == lead_id:
                    if "status" in payload:
                        l["status"] = payload["status"]
                    if "note" in payload:
                        l["note"] = payload["note"]
                    if "agent" in payload:
                        l["agent"] = payload["agent"]
                    updated = True
                    break

            if updated:
                save_leads_to_disk(leads)
                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            else:
                self._set_headers(404, "application/json")
                self.wfile.write(json.dumps({"error": "Không tìm thấy lead"}).encode("utf-8"))
            return

        self._set_headers(404)

    def _serve_static(self, path: str):
        # Default to index.html
        if path == "/" or not path:
            file_path = os.path.join(DIST_DIR, "index.html")
        else:
            clean_path = path.lstrip("/")
            file_path = os.path.join(DIST_DIR, clean_path)

        # Fallback to SPA index.html for client routing
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            file_path = os.path.join(DIST_DIR, "index.html")

        if not os.path.exists(file_path):
            self.send_error(404, f"File not found: {path}")
            return

        # Determine MIME type
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".txt": "text/plain; charset=utf-8"
        }
        content_type = mime_types.get(ext, "application/octet-stream")

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self._set_headers(200, content_type)
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

def run_server(port: int = 8080):
    env_port = os.environ.get("PORT")
    if env_port:
        port = int(env_port)

    # Launch background auto-crawler (1 hour interval, 10 leads target)
    t_crawler = threading.Thread(target=auto_crawler_loop, daemon=True, name="AutoCrawlerThread")
    t_crawler.start()

    # Launch background anti-sleep keep-alive worker (ping every 9 min to prevent Render hibernation)
    t_antisleep = threading.Thread(target=anti_sleep_keeper_loop, daemon=True, name="AntiSleepThread")
    t_antisleep.start()

    server = HTTPServer(("0.0.0.0", port), DentalApiHandler)
    print(f"🚀 DentalLead Web App đang chạy tại: http://0.0.0.0:{port}")
    print("⏰ [Auto-Crawl] Chế độ tự động cào: 1 tiếng / lần (dừng sau khi đủ 10 bài mới)")
    print("🛡️ [Anti-Sleep] Cơ chế chống ngủ đông Render: Kích hoạt 24/7 (ping mỗi 9 phút)")
    server.serve_forever()

if __name__ == "__main__":
    run_server(8080)
