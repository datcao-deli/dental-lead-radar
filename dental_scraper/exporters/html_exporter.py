"""
Dental Lead Scraper - Modern HTML Report Dashboard Exporter
Generates a standalone, interactive HTML dashboard with search, filters, and KPI cards.
"""

import json
from typing import List
from ..models import LeadItem

class HTMLExporter:
    """Exports scraped dental leads into an interactive HTML dashboard."""

    @classmethod
    def export(cls, leads: List[LeadItem], filepath: str) -> None:
        leads_dict = [l.to_dict() for l in leads]
        total = len(leads)
        hot_count = sum(1 for l in leads if l.lead_quality == "HOT")
        warm_count = sum(1 for l in leads if l.lead_quality == "WARM")
        urgent_count = sum(1 for l in leads if l.urgency in ["Khẩn cấp", "Cao"])
        avg_score = round(sum(l.intent_score for l in leads) / total, 1) if total > 0 else 0

        html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dental Lead Scanner - Danh Sách Khách Hàng Nhu Cầu Nha Khoa</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #131b2e;
            --surface-hover: #1b2640;
            --border: #1f2d4d;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.2);
            --hot: #f43f5e;
            --hot-glow: rgba(244, 63, 94, 0.2);
            --warm: #f59e0b;
            --cold: #64748b;
            --urgent: #ef4444;
            --success: #10b981;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 32px 24px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 24px;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .brand-icon {{
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 0 20px var(--primary-glow);
        }}
        .brand h1 {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        .brand p {{
            font-size: 13px;
            color: var(--text-muted);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 18px;
            margin-bottom: 32px;
        }}
        .stat-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }}
        .stat-card::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent, var(--primary)), transparent);
        }}
        .stat-card.hot {{ --accent: var(--hot); }}
        .stat-card.warm {{ --accent: var(--warm); }}
        .stat-card.urgent {{ --accent: var(--urgent); }}
        .stat-card.neutral {{ --accent: var(--primary); }}
        .stat-label {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 8px;
        }}
        .stat-val {{
            font-size: 32px;
            font-weight: 800;
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}
        .stat-val span {{
            font-size: 14px;
            color: var(--text-muted);
            font-weight: 400;
        }}
        .filter-section {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
        }}
        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}
        .search-box input {{
            width: 100%;
            background: #090d16;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 16px 12px 40px;
            color: var(--text-main);
            font-size: 14px;
            outline: none;
            transition: all 0.2s;
        }}
        .search-box input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary-glow);
        }}
        .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
        }}
        .filter-pills {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .pill {{
            background: #0b1120;
            border: 1px solid var(--border);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            color: var(--text-muted);
            transition: all 0.15s;
        }}
        .pill:hover, .pill.active {{
            background: var(--primary);
            color: #0b0f19;
            border-color: var(--primary);
        }}
        .pill.hot-pill.active {{
            background: var(--hot);
            border-color: var(--hot);
            color: white;
        }}
        .leads-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
        }}
        .lead-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            transition: all 0.2s;
        }}
        .lead-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }}
        .lead-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .badge-hot {{
            background: var(--hot-glow);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }}
        .badge-warm {{
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        .badge-cold {{
            background: rgba(100, 116, 139, 0.2);
            color: #94a3b8;
            border: 1px solid rgba(100, 116, 139, 0.3);
        }}
        .lead-title {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--text-main);
        }}
        .lead-snippet {{
            font-size: 13.5px;
            color: #cbd5e1;
            line-height: 1.6;
            background: #0a0e17;
            padding: 12px;
            border-radius: 10px;
            border-left: 3px solid var(--primary);
        }}
        .lead-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: auto;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .tag {{
            background: #1e293b;
            color: #38bdf8;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .lead-actions {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--border);
            padding-top: 14px;
            margin-top: 6px;
        }}
        .btn {{
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            border: none;
        }}
        .btn-primary {{
            background: var(--primary);
            color: #0f172a;
        }}
        .btn-primary:hover {{
            background: #7dd3fc;
        }}
        .btn-ghost {{
            background: #1e293b;
            color: var(--text-main);
        }}
        .btn-ghost:hover {{
            background: #334155;
        }}
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--success);
            color: #0b0f19;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            display: none;
            z-index: 999;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <div class="brand-icon">🦷</div>
                <div>
                    <h1>Dental Lead Radar AI</h1>
                    <p>Hệ thống quét & phân tích nhu cầu khám chữa răng trên mạng xã hội và diễn đàn</p>
                </div>
            </div>
            <div>
                <span class="badge badge-hot">Live Scanner</span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card neutral">
                <div class="stat-label">TỔNG LEADS THU THẬP</div>
                <div class="stat-val">{total} <span>bài viết</span></div>
            </div>
            <div class="stat-card hot">
                <div class="stat-label">LEADS NÓNG (NHU CẦU CAO)</div>
                <div class="stat-val">{hot_count} <span>khách tiềm năng</span></div>
            </div>
            <div class="stat-card warm">
                <div class="stat-label">LEADS ĐANG TÌM HIỂU</div>
                <div class="stat-val">{warm_count} <span>hỏi đáp / review</span></div>
            </div>
            <div class="stat-card urgent">
                <div class="stat-label">TRƯỜNG HỢP CẦN XỬ LÝ GẤP</div>
                <div class="stat-val">{urgent_count} <span>đau răng / sưng tấy</span></div>
            </div>
        </div>

        <div class="filter-section">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" placeholder="Tìm theo từ khóa, khu vực, triệu chứng, người đăng..." onkeyup="filterLeads()">
            </div>
            <div class="filter-pills">
                <button class="pill active" onclick="setQualityFilter('ALL', this)">Tất cả ({total})</button>
                <button class="pill hot-pill" onclick="setQualityFilter('HOT', this)">🔥 Nóng ({hot_count})</button>
                <button class="pill" onclick="setQualityFilter('WARM', this)">⚡ Ấm ({warm_count})</button>
            </div>
        </div>

        <div class="leads-grid" id="leadsGrid"></div>
    </div>

    <div class="toast" id="toast">Đã sao chép thông tin khách hàng vào clipboard!</div>

    <script>
        const leadsData = {json.dumps(leads_dict, ensure_ascii=False)};
        let activeQuality = 'ALL';

        function renderLeads(leads) {{
            const grid = document.getElementById('leadsGrid');
            if (!leads.length) {{
                grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted);">Không tìm thấy bài viết nào phù hợp bộ lọc.</div>';
                return;
            }}

            grid.innerHTML = leads.map(l => {{
                let qualityBadge = '';
                if (l.lead_quality === 'HOT') {{
                    qualityBadge = `<span class="badge badge-hot">🔥 NÓNG • ${{l.intent_score}}đ</span>`;
                }} else if (l.lead_quality === 'WARM') {{
                    qualityBadge = `<span class="badge badge-warm">⚡ TIỀM NĂNG • ${{l.intent_score}}đ</span>`;
                }} else {{
                    qualityBadge = `<span class="badge badge-cold">${{l.lead_quality}} • ${{l.intent_score}}đ</span>`;
                }}

                let urgencyColor = l.urgency === 'Khẩn cấp' ? 'var(--hot)' : (l.urgency === 'Cao' ? 'var(--warm)' : 'var(--primary)');

                return `
                <div class="lead-card">
                    <div class="lead-card-header">
                        <div>${{qualityBadge}}</div>
                        <div style="font-size: 12px; font-weight: 700; color: ${{urgencyColor}};">⚠️ ${{l.urgency}}</div>
                    </div>
                    <div class="lead-title">${{escapeHtml(l.title)}}</div>
                    <div class="lead-snippet">${{escapeHtml(l.snippet)}}</div>
                    <div class="tags">
                        <span class="tag">🏷️ ${{l.category_label}}</span>
                        ${{l.matched_keywords.map(k => `<span class="tag">#${{k}}</span>`).join('')}}
                    </div>
                    <div class="lead-meta">
                        <div class="meta-item">📍 ${{l.location}}</div>
                        <div class="meta-item">🌐 ${{l.platform}}</div>
                        <div class="meta-item">👤 ${{l.author}}</div>
                    </div>
                    <div class="lead-actions">
                        <button class="btn btn-ghost" onclick="copyLead('${{l.id}}')">📋 Sao chép Lead</button>
                        <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Xem bài gốc ↗</a>
                    </div>
                </div>
                `;
            }}).join('');
        }}

        function escapeHtml(str) {{
            if (!str) return '';
            return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }}

        function filterLeads() {{
            const searchVal = document.getElementById('searchInput').value.toLowerCase().trim();
            const filtered = leadsData.filter(l => {{
                const matchesQuality = (activeQuality === 'ALL') || (l.lead_quality === activeQuality);
                const matchesSearch = !searchVal || 
                    l.title.toLowerCase().includes(searchVal) || 
                    l.snippet.toLowerCase().includes(searchVal) ||
                    l.location.toLowerCase().includes(searchVal) ||
                    l.category_label.toLowerCase().includes(searchVal) ||
                    l.author.toLowerCase().includes(searchVal);
                return matchesQuality && matchesSearch;
            }});
            renderLeads(filtered);
        }}

        function setQualityFilter(quality, btn) {{
            activeQuality = quality;
            document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            filterLeads();
        }}

        function copyLead(id) {{
            const lead = leadsData.find(l => l.id === id);
            if (!lead) return;
            const text = `[LEAD NHA KHOA - ${{lead.category_label}}]\\n- Khách: ${{lead.author}} (${{lead.location}})\\n- Điểm tiềm năng: ${{lead.intent_score}}/100 (${{lead.lead_quality}})\\n- Nhu cầu: ${{lead.title}}\\n- Tóm tắt: ${{lead.snippet}}\\n- Link: ${{lead.url}}`;
            navigator.clipboard.writeText(text).then(() => {{
                const toast = document.getElementById('toast');
                toast.style.display = 'block';
                setTimeout(() => toast.style.display = 'none', 2500);
            }});
        }}

        // Initial render
        renderLeads(leadsData);
    </script>
</body>
</html>
"""
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write(html_template)
