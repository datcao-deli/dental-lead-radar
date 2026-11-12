"""
Dental Lead Scraper - Command Line Interface & Runner
Executes multi-source scans, intent scoring, filtering, and rich reporting.
"""

import os
import sys
import argparse
import webbrowser
from typing import List, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import DEFAULT_SEARCH_QUERIES, DENTAL_CATEGORIES
from .models import LeadItem
from .engines import DuckDuckGoEngine, FacebookEngine, RedditEngine, ThreadsEngine, VozEngine
from .exporters import CSVExporter, JSONExporter, HTMLExporter

console = Console()

class DentalLeadScanner:
    """Orchestrates scanning across multiple platforms, deduping, and scoring leads."""

    def __init__(self, delay: float = 0.5):
        self.ddg = DuckDuckGoEngine(delay=delay)
        self.facebook = FacebookEngine(delay=delay)
        self.reddit = RedditEngine(delay=delay)
        self.threads = ThreadsEngine(delay=delay)
        self.voz = VozEngine(delay=delay)

    def scan(self, 
             categories: List[str] = None, 
             sources: List[str] = None, 
             custom_query: str = "",
             limit_per_query: int = 10,
             min_score: int = 30,
             include_ads: bool = False) -> List[LeadItem]:
        
        sources = sources or ["all"]
        active_sources = [s.lower() for s in sources]
        all_leads: Dict[str, LeadItem] = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Đang khởi động radar quét leads nha khoa...", total=None)

            # 1. Custom query search if provided
            if custom_query:
                progress.update(task, description=f"[yellow]Đang quét truy vấn tùy chỉnh: '{custom_query}'...")
                if "all" in active_sources or "threads" in active_sources:
                    for l in self.threads.search(custom_query, limit=limit_per_query):
                        all_leads[l.id] = l
                if "all" in active_sources or "facebook" in active_sources:
                    for l in self.facebook.search(custom_query, limit=limit_per_query):
                        all_leads[l.id] = l
                if "all" in active_sources or "web" in active_sources:
                    for l in self.ddg.search(custom_query, limit=limit_per_query):
                        all_leads[l.id] = l
                if "all" in active_sources or "reddit" in active_sources:
                    for l in self.reddit.search(custom_query, limit=limit_per_query):
                        all_leads[l.id] = l
                if "all" in active_sources or "voz" in active_sources:
                    for l in self.voz.search(custom_query, limit=limit_per_query):
                        all_leads[l.id] = l

            # 2. Default target queries across platforms
            else:
                for q_obj in DEFAULT_SEARCH_QUERIES:
                    q_name = q_obj["name"]
                    dork = q_obj["dork"]

                    if "threads" in q_name.lower():
                        if "all" not in active_sources and "threads" not in active_sources:
                            continue
                        progress.update(task, description=f"[cyan]Đang quét: {q_name}...")
                        for l in self.threads.search(dork, limit=limit_per_query):
                            all_leads[l.id] = l
                    elif "facebook" in q_name.lower():
                        if "all" not in active_sources and "facebook" not in active_sources:
                            continue
                        progress.update(task, description=f"[blue]Đang quét: {q_name}...")
                        for l in self.facebook.search(dork, limit=limit_per_query):
                            all_leads[l.id] = l
                    elif "reddit" in q_name.lower():
                        if "all" not in active_sources and "reddit" not in active_sources:
                            continue
                        progress.update(task, description=f"[green]Đang quét: {q_name}...")
                        reddit_results = self.reddit.search(dork, limit=limit_per_query)
                        for l in reddit_results:
                            all_leads[l.id] = l
                    elif "voz" in q_name.lower():
                        if "all" not in active_sources and "voz" not in active_sources:
                            continue
                        progress.update(task, description=f"[blue]Đang quét: {q_name}...")
                        voz_results = self.voz.search(dork, limit=limit_per_query)
                        for l in voz_results:
                            all_leads[l.id] = l
                    else:
                        progress.update(task, description=f"[magenta]Đang quét: {q_name}...")
                        ddg_results = self.ddg.search(dork, limit=limit_per_query)
                        for l in ddg_results:
                            all_leads[l.id] = l

            progress.update(task, description="[bold green]Hoàn tất thu thập! Đang phân tích ý định và lọc bài viết...")

        # Filter results
        filtered_leads: List[LeadItem] = []
        for l in all_leads.values():
            if not include_ads and l.lead_quality == "SPAM_AD":
                continue
            if l.intent_score < min_score:
                continue
            if categories and "ALL" not in categories and l.category not in categories:
                continue
            filtered_leads.append(l)

        # Sort by intent score descending
        filtered_leads.sort(key=lambda x: x.intent_score, reverse=True)
        return filtered_leads

def start_local_server(directory: str, port: int = 8080):
    """Starts a local HTTP server in background to view HTML report."""
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def log_message(self, format, *args):
            pass

    server = HTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def run_cli():
    parser = argparse.ArgumentParser(
        description="Dental Lead Scraper - Tool cào bài viết người dùng có nhu cầu khám chữa răng"
    )
    parser.add_argument("-q", "--query", type=str, default="", help="Từ khóa tìm kiếm tùy chỉnh (ví dụ: 'nhổ răng khôn Hà Nội')")
    parser.add_argument("-s", "--sources", nargs="+", default=["all"], choices=["all", "web", "reddit", "voz"], help="Nguồn cào dữ liệu")
    parser.add_argument("-c", "--category", nargs="+", default=["ALL"], help="Lọc danh mục (NHỔ_RĂNG_KHÔN, ĐAU_RĂNG_TỦY, NIỀNG_RĂNG_CHỈNH_NHA, TRỒNG_RĂNG_IMPLANT, RĂNG_SỨ_THẨM_MỸ, KHÁM_TỔNG_QUÁT_LẤY_CAO, ALL)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Giới hạn số kết quả mỗi truy vấn (mặc định: 10)")
    parser.add_argument("--min-score", type=int, default=30, help="Điểm ý định tối thiểu để lọc lead (0-100, mặc định: 30)")
    parser.add_argument("--include-ads", action="store_true", help="Bao gồm cả bài viết quảng cáo từ phòng khám")
    parser.add_argument("-o", "--output-dir", type=str, default="output", help="Thư mục xuất báo cáo (mặc định: 'output')")
    parser.add_argument("--web", action="store_true", help="Tự động mở dashboard báo cáo trên trình duyệt sau khi quét")
    parser.add_argument("--port", type=int, default=8080, help="Cổng chạy web dashboard (mặc định: 8080)")

    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold cyan]🦷 DENTAL LEAD RADAR AI - BỘ CÀO KHÁCH HÀNG NHU CẦU NHA KHOA[/bold cyan]\n"
        "[dim]Hệ thống quét đa nguồn: Diễn đàn, Mạng xã hội, Google/DDG với bộ lọc Intent NLP[/dim]",
        border_style="cyan"
    ))

    scanner = DentalLeadScanner(delay=0.5)
    leads = scanner.scan(
        categories=args.category,
        sources=args.sources,
        custom_query=args.query,
        limit_per_query=args.limit,
        min_score=args.min_score,
        include_ads=args.include_ads
    )

    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = os.path.join(args.output_dir, "leads.csv")
    json_path = os.path.join(args.output_dir, "leads.json")
    html_path = os.path.join(args.output_dir, "dashboard.html")

    CSVExporter.export(leads, csv_path)
    JSONExporter.export(leads, json_path)
    HTMLExporter.export(leads, html_path)

    hot_count = sum(1 for l in leads if l.lead_quality == "HOT")
    warm_count = sum(1 for l in leads if l.lead_quality == "WARM")
    
    console.print(f"\n[bold green]✓ Đã quét thành công {len(leads)} leads tiềm năng![/bold green] "
                  f"(🔥 Nóng: [bold red]{hot_count}[/bold red] | ⚡ Tiềm năng: [bold yellow]{warm_count}[/bold yellow])")

    if leads:
        table = Table(title="Top Khách Hàng Tiềm Năng Phát Hiện Gần Nhất", show_header=True, header_style="bold magenta")
        table.add_column("Chất lượng", style="bold", width=12)
        table.add_column("Điểm", justify="right", width=6)
        table.add_column("Nhu cầu", width=22)
        table.add_column("Khẩn cấp", width=10)
        table.add_column("Khu vực", width=14)
        table.add_column("Nền tảng", width=12)
        table.add_column("Tiêu đề bài viết", width=42)

        for l in leads[:15]:
            quality_color = "red" if l.lead_quality == "HOT" else ("yellow" if l.lead_quality == "WARM" else "blue")
            urgency_color = "red" if l.urgency == "Khẩn cấp" else ("yellow" if l.urgency == "Cao" else "cyan")
            table.add_row(
                f"[{quality_color}]{l.lead_quality}[/{quality_color}]",
                f"{l.intent_score}",
                l.category_label,
                f"[{urgency_color}]{l.urgency}[/{urgency_color}]",
                l.location,
                l.platform,
                l.title[:40] + ("..." if len(l.title) > 40 else "")
            )
        console.print(table)

    console.print(Panel(
        f"[bold]Đã xuất dữ liệu ra:[/bold]\n"
        f"📄 CSV (Excel tiếng Việt UTF-8): [cyan]{csv_path}[/cyan]\n"
        f"📦 JSON: [cyan]{json_path}[/cyan]\n"
        f"🌐 Web Dashboard HTML: [cyan]{html_path}[/cyan]",
        title="[bold green]Kết quả xuất file[/bold green]",
        border_style="green"
    ))

    if args.web:
        from .server import DentalApiHandler
        console.print(f"[bold cyan]Đang khởi chạy Fullstack DentaLead Web App tại http://127.0.0.1:{args.port} ...[/bold cyan]")
        server = HTTPServer(("0.0.0.0", args.port), DentalApiHandler)
        webbrowser.open(f"http://127.0.0.1:{args.port}")
        console.print("[dim]Nhấn Ctrl+C để dừng server web dashboard.[/dim]")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            console.print("\n[yellow]Đã đóng server.[/yellow]")
