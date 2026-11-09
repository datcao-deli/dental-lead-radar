"""
Dental Lead Scraper - Fullstack REST API & Static Server
Connects the React/Vite DentaLead UI with the Python crawler engine.
"""

import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import List, Dict, Any

from .cli import DentalLeadScanner
from .exporters import CSVExporter, JSONExporter, HTMLExporter
from .models import LeadItem

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(PROJECT_ROOT, "web", "dist")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LEADS_FILE = os.path.join(OUTPUT_DIR, "leads.json")
CSV_FILE = os.path.join(OUTPUT_DIR, "leads.csv")

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

        # API: Scanner status
        if path == "/api/status":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "is_scanning": is_scanning,
                "last_scan": last_scan_result
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

        # Serve static React UI files
        self._serve_static(path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Trigger live scan
        if path == "/api/scan":
            global is_scanning, last_scan_result
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            params = json.loads(body) if body else {}

            query = params.get("query", "")
            limit = int(params.get("limit", 8))
            min_score = int(params.get("min_score", 30))
            sources = params.get("sources", ["all"])

            if is_scanning:
                self._set_headers(409, "application/json")
                self.wfile.write(json.dumps({"error": "Trình cào đang hoạt động, vui lòng đợi."}).encode("utf-8"))
                return

            def background_scan():
                global is_scanning, last_scan_result
                with scanner_lock:
                    is_scanning = True
                    try:
                        scanner = DentalLeadScanner(delay=0.5)
                        new_lead_items = scanner.scan(
                            custom_query=query,
                            limit_per_query=limit,
                            min_score=min_score,
                            sources=sources
                        )
                        existing_leads = load_leads_from_disk()
                        existing_ids = {str(l.get("id")) for l in existing_leads}

                        added_count = 0
                        for nl in new_lead_items:
                            if nl.id not in existing_ids:
                                d = nl.to_dict()
                                # Format matching React UI Lead model
                                d["name"] = nl.author if nl.author != "Ẩn danh" else (nl.title[:35] + "...")
                                d["handle"] = f"@{nl.platform.lower().replace(' ', '')}"
                                d["phone"] = "Chưa có SĐT"
                                d["need"] = nl.category_label
                                d["status"] = "New"
                                d["agent"] = "Chưa phân công"
                                d["agentInitials"] = "—"
                                d["score"] = nl.intent_score
                                d["time"] = "Vừa thu thập"
                                d["post"] = f"{nl.title} - {nl.snippet}"
                                d["note"] = f"Phát hiện qua từ khóa: {', '.join(nl.matched_keywords)}"
                                existing_leads.insert(0, d)
                                added_count += 1

                        save_leads_to_disk(existing_leads)
                        last_scan_result = {
                            "total": len(existing_leads),
                            "added": added_count,
                            "message": f"Đã quét thành công, thêm mới {added_count} leads!"
                        }
                    except Exception as e:
                        last_scan_result = {"error": str(e), "message": f"Lỗi quét: {str(e)}"}
                    finally:
                        is_scanning = False

            thread = threading.Thread(target=background_scan, daemon=True)
            thread.start()

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "message": "Đã bắt đầu tiến trình quét ngầm!",
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
    server = HTTPServer(("0.0.0.0", port), DentalApiHandler)
    print(f"🚀 DentalLead Web App đang chạy tại: http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server(8080)
