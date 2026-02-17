#!/usr/bin/env python3
"""
Generate index.html from CSV data files.
Run this script whenever the data is updated to regenerate the HTML report.
"""

import csv
from datetime import datetime

# ============== READ DATA FILES ==============

def parse_counts(filename):
    """Parse name_counts CSV file"""
    counts = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            parts = line.rsplit(":", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                count = int(parts[1].strip())
                counts.append((name, count))
    return counts

def parse_days(filename):
    """Parse name_days CSV file"""
    days = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            parts = line.rsplit(":", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                count = int(parts[1].strip())
                days.append((name, count))
    return days

def parse_special_stats(filename):
    """Parse special_stats CSV file"""
    daily_max = []
    most_active = []
    current_section = None
    
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "하루동안 최다 메시지" in line:
                current_section = "daily_max"
                continue
            elif "가장 활발한 날" in line:
                current_section = "most_active"
                continue
            
            if not line or line.startswith("==="):
                continue
                
            if current_section == "daily_max":
                # Format: 1. 이희루 - 48회 (02-05-2025)
                try:
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        rest = parts[1]
                        name_count = rest.split(" - ")
                        name = name_count[0]
                        count_date = name_count[1].split(" (")
                        count = count_date[0].replace("회", "")
                        date = count_date[1].replace(")", "")
                        # Extract MM-DD from MM-DD-YYYY
                        date_short = date[:5]
                        daily_max.append((name, int(count), date_short))
                except:
                    continue
            elif current_section == "most_active":
                # Format: 1. 04-28-2025 - 233회 (50명 참여)
                try:
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        rest = parts[1]
                        date_rest = rest.split(" - ")
                        date = date_rest[0]
                        count_people = date_rest[1].split(" (")
                        count = count_people[0].replace("회", "")
                        people = count_people[1].replace("명 참여)", "")
                        most_active.append((date, int(count), int(people)))
                except:
                    continue
    
    return daily_max[:20], most_active[:20]

def parse_monthly(filename):
    """Parse top10_per_month CSV file"""
    monthly = {}
    current_month = None
    
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "월 TOP" in line:
                # Extract month: "2025년 01월 TOP 5:"
                parts = line.split("월")[0]
                month = parts.split("년 ")[1]
                current_month = month
                monthly[current_month] = []
                continue
            if current_month and line[0].isdigit():
                # Format: 1. Jasonn Cooney - 76회
                try:
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        rest = parts[1]
                        name_count = rest.split(" - ")
                        name = name_count[0]
                        count = name_count[1].replace("회", "")
                        monthly[current_month].append((name, int(count)))
                except:
                    continue
    
    return monthly

def parse_occupations(filename):
    """Parse occupation.csv file"""
    occupation_map = {}
    current_occ = None
    
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.endswith(":"):
                current_occ = line[:-1]
                if current_occ == "수성초등학교":
                    current_occ = "수성초"
                continue
            if current_occ and not "?" in line:
                occupation_map[line] = current_occ
    
    return occupation_map

# ============== GENERATE HTML ==============

def get_rank_class(rank):
    if rank == 1:
        return "rank-1"
    elif rank == 2:
        return "rank-2"
    elif rank == 3:
        return "rank-3"
    else:
        return "rank-other"

def generate_leaderboard_item(rank, name, count, unit="회", meta=None):
    rank_class = get_rank_class(rank)
    meta_html = f'<span class="meta">{meta}</span>' if meta else ''
    return f'                        <div class="leaderboard-item"><span class="rank {rank_class}">{rank}</span><span class="name">{name}</span><span class="count">{count}{unit}</span>{meta_html}</div>'

def generate_stat_item(rank, date, count, people):
    return f'                        <div class="stat-item"><span class="stat-rank">{rank}</span><div class="stat-info"><div class="stat-name">{date}</div><div class="stat-detail">{people}명 참여</div></div><span class="stat-value">{count}회</span></div>'

def generate_month_card(month_name, items):
    items_html = "\n".join([f'                            <div class="month-item"><span class="rank-num">{i+1}.</span> {name} - {count}회</div>' for i, (name, count) in enumerate(items)])
    return f'''                        <div class="month-card">
                            <div class="month-title">{month_name}</div>
{items_html}
                        </div>'''

def group_by_occupation(counts, occupation_map):
    """Group name counts by occupation"""
    occ_groups = {}
    for name, count in counts:
        occ = occupation_map.get(name, "Unknown")
        if occ not in occ_groups:
            occ_groups[occ] = []
        occ_groups[occ].append((name, count))
    return occ_groups

def calc_occupation_totals(groups):
    """Calculate total mentions per occupation"""
    totals = {}
    for occ, members in groups.items():
        if occ != "Unknown":
            totals[occ] = (sum(count for name, count in members), len(members))
    return totals

def generate_occ_ranking_items(sorted_totals, groups):
    """Generate occupation ranking leaderboard items"""
    items = []
    for rank, (occ, (total, count)) in enumerate(sorted_totals[:10], 1):
        items.append(generate_leaderboard_item(rank, occ, total, "회", f"{count}명"))
    return "\n".join(items)

def generate_occ_card(occ_name, color_class, emoji, members):
    """Generate occupation card HTML"""
    items_html = "\n".join([
        f'                                <div class="occ-list-item"><span class="rank-num">{i+1}.</span><span class="occ-name">{name}</span><span class="occ-count">{count}회</span></div>'
        for i, (name, count) in enumerate(members[:10])
    ])
    return f'''                        <div class="occ-card">
                            <div class="occ-card-header">
                                <span class="occ-card-title {color_class}">{emoji} {occ_name}</span>
                            </div>
                            <div class="occ-list">
{items_html}
                            </div>
                        </div>'''

def generate_html():
    # Read all data
    counts_2025 = parse_counts("name_counts_2025.csv")
    counts_2026 = parse_counts("name_counts_2026.csv")
    days_2025 = parse_days("name_days_2025.csv")
    days_2026 = parse_days("name_days_2026.csv")
    daily_max_2025, most_active_2025 = parse_special_stats("special_stats_2025.csv")
    daily_max_2026, most_active_2026 = parse_special_stats("special_stats_2026.csv")
    monthly_2025 = parse_monthly("top10_per_month_2025.csv")
    monthly_2026 = parse_monthly("top10_per_month_2026.csv")
    occupation_map = parse_occupations("occupation.csv")
    
    # Group by occupation
    groups_2025 = group_by_occupation(counts_2025, occupation_map)
    groups_2026 = group_by_occupation(counts_2026, occupation_map)
    totals_2025 = calc_occupation_totals(groups_2025)
    totals_2026 = calc_occupation_totals(groups_2026)
    sorted_totals_2025 = sorted(totals_2025.items(), key=lambda x: x[1][0], reverse=True)
    sorted_totals_2026 = sorted(totals_2026.items(), key=lambda x: x[1][0], reverse=True)
    
    # Occupation styling
    occ_styles = {
        "카카오톡": ("yellow", "🟡"),
        "NU": ("purple", "🟣"),
        "OSU": ("red", "🔴"),
        "수성초": ("green", "🟢"),
        "MAVERICK": ("blue", "🔵"),
        "DCU": ("skyblue", "🩵"),
        "NEPES": ("orange", "🟠"),
        "행복한교회": ("pink", "💗"),
        "무소속": ("", "⚪"),
        "신천지": ("", "⛪"),
    }
    
    occ_order = ["NU", "OSU", "수성초", "MAVERICK", "카카오톡", "행복한교회", "DCU", "NEPES", "무소속", "신천지"]
    
    # Generate occupation cards for 2025
    occ_cards_2025 = []
    for occ in occ_order:
        if occ in groups_2025 and groups_2025[occ]:
            color, emoji = occ_styles.get(occ, ("", ""))
            style_attr = ""
            if occ == "무소속":
                color = '" style="color: #fff;'
            elif occ == "신천지":
                color = '" style="color: #9ca3af;'
            occ_cards_2025.append(generate_occ_card(occ, color, emoji, groups_2025[occ]))
    
    # Generate occupation cards for 2026
    occ_cards_2026 = []
    for occ in occ_order:
        if occ in groups_2026 and groups_2026[occ]:
            color, emoji = occ_styles.get(occ, ("", ""))
            if occ == "무소속":
                color = '" style="color: #fff;'
            elif occ == "신천지":
                color = '" style="color: #9ca3af;'
            occ_cards_2026.append(generate_occ_card(occ, color, emoji, groups_2026[occ]))
    
    # Month names in Korean
    month_names = {
        "01": "1월", "02": "2월", "03": "3월", "04": "4월",
        "05": "5월", "06": "6월", "07": "7월", "08": "8월",
        "09": "9월", "10": "10월", "11": "11월", "12": "12월"
    }
    
    # Generate monthly cards
    monthly_cards_2025 = "\n".join([
        generate_month_card(month_names[m], monthly_2025[m])
        for m in sorted(monthly_2025.keys())
    ])
    monthly_cards_2026 = "\n".join([
        generate_month_card(month_names[m], monthly_2026[m])
        for m in sorted(monthly_2026.keys())
    ])
    
    # Generate the full HTML
    today = datetime.now().strftime("%b %d, %Y")
    
    # Determine date ranges
    date_range_2025 = "01/01/2025 - 12/31/2025"
    date_range_2026 = f"01/01/2026 - {datetime.now().strftime('%m/%d/%Y')}"
    
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERCF 메시지 통계 리포트</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Bebas+Neue&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0a0a0f;
            --bg-card: #13131a;
            --bg-card-hover: #1a1a24;
            --accent-gold: #ffd700;
            --accent-silver: #c0c0c0;
            --accent-bronze: #cd7f32;
            --accent-blue: #4a9eff;
            --accent-purple: #a855f7;
            --accent-pink: #ec4899;
            --accent-green: #22c55e;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --border-color: #2a2a3a;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            background-image: 
                radial-gradient(ellipse at top, rgba(74, 158, 255, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at bottom right, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }}

        h1 {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 4rem;
            letter-spacing: 0.1em;
            background: linear-gradient(135deg, var(--accent-gold), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 300;
        }}

        .year-tabs {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}

        .year-tab {{
            padding: 0.75rem 2rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            color: var(--text-secondary);
        }}

        .year-tab:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-blue);
        }}

        .year-tab.active {{
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-color: transparent;
            color: white;
            font-weight: 500;
        }}

        .year-content {{
            display: none;
        }}

        .year-content.active {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .date-range {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            padding: 0.75rem 1.5rem;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}

        .section-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-blue);
            box-shadow: 0 10px 40px rgba(74, 158, 255, 0.1);
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .card-icon {{
            font-size: 1.5rem;
        }}

        .card-title {{
            font-size: 1.1rem;
            font-weight: 500;
        }}

        .leaderboard {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .leaderboard-item {{
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            transition: background 0.2s ease;
        }}

        .leaderboard-item:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}

        .rank {{
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 1rem;
        }}

        .rank-1 {{
            background: linear-gradient(135deg, #ffd700, #ffb700);
            color: #000;
        }}

        .rank-2 {{
            background: linear-gradient(135deg, #c0c0c0, #a0a0a0);
            color: #000;
        }}

        .rank-3 {{
            background: linear-gradient(135deg, #cd7f32, #b06b28);
            color: #000;
        }}

        .rank-other {{
            background: var(--border-color);
            color: var(--text-secondary);
        }}

        .name {{
            flex: 1;
            font-weight: 400;
        }}

        .count {{
            font-weight: 700;
            color: var(--accent-blue);
        }}

        .meta {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-left: 0.5rem;
        }}

        .occupation-badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.65rem;
            font-weight: 600;
            margin-left: 6px;
            vertical-align: middle;
        }}

        .occ-카카오톡 {{ background: rgba(250, 204, 21, 0.2); border: 1px solid rgba(250, 204, 21, 0.5); color: #facc15; }}
        .occ-NU {{ background: rgba(168, 85, 247, 0.2); border: 1px solid rgba(168, 85, 247, 0.5); color: #a855f7; }}
        .occ-OSU {{ background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); color: #ef4444; }}
        .occ-수성초 {{ background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.5); color: #22c55e; }}
        .occ-MAVERICK {{ background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.5); color: #3b82f6; }}
        .occ-DCU {{ background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.5); color: #38bdf8; }}
        .occ-NEPES {{ background: rgba(249, 115, 22, 0.2); border: 1px solid rgba(249, 115, 22, 0.5); color: #f97316; }}
        .occ-행복한교회 {{ background: rgba(236, 72, 153, 0.2); border: 1px solid rgba(236, 72, 153, 0.5); color: #ec4899; }}
        .occ-무소속 {{ background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.3); color: #ffffff; }}

        .occupation-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
        }}

        .occ-card {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid var(--border-color);
        }}

        .occ-card-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .occ-card-title {{
            font-size: 0.95rem;
            font-weight: 600;
        }}

        .occ-card-title.yellow {{ color: #facc15; }}
        .occ-card-title.purple {{ color: #a855f7; }}
        .occ-card-title.red {{ color: #ef4444; }}
        .occ-card-title.green {{ color: #22c55e; }}
        .occ-card-title.blue {{ color: #3b82f6; }}
        .occ-card-title.skyblue {{ color: #38bdf8; }}
        .occ-card-title.orange {{ color: #f97316; }}
        .occ-card-title.pink {{ color: #ec4899; }}

        .occ-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .occ-list-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            padding: 4px 0;
        }}

        .occ-list-item .rank-num {{
            color: var(--text-secondary);
            margin-right: 6px;
            font-size: 0.75rem;
        }}

        .occ-list-item .occ-name {{
            flex: 1;
            color: var(--text-primary);
        }}

        .occ-list-item .occ-count {{
            color: var(--accent-blue);
            font-weight: 600;
            font-size: 0.8rem;
        }}

        .monthly-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }}

        .month-card {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 1rem;
        }}

        .month-title {{
            font-weight: 600;
            color: var(--accent-purple);
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
        }}

        .month-item {{
            font-size: 0.85rem;
            padding: 0.25rem 0;
            color: var(--text-secondary);
        }}

        .month-item .rank-num {{
            color: var(--accent-gold);
            font-weight: 600;
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
        }}

        .stat-rank {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-gold);
            min-width: 2rem;
        }}

        .stat-info {{
            flex: 1;
        }}

        .stat-name {{
            font-weight: 500;
            margin-bottom: 0.25rem;
        }}

        .stat-detail {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        .stat-value {{
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--accent-blue);
        }}

        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--bg-dark);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--border-color);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-blue);
        }}

        /* Mobile Responsive Styles */
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            h1 {{
                font-size: 2.5rem;
            }}

            .section-grid {{
                grid-template-columns: 1fr;
                justify-items: center;
            }}

            .card {{
                width: 100%;
                max-width: 100%;
            }}

            .occupation-grid {{
                grid-template-columns: 1fr;
                justify-items: center;
            }}

            .occ-card {{
                width: 100%;
            }}

            .monthly-grid {{
                grid-template-columns: 1fr;
                justify-items: center;
            }}

            .month-card {{
                width: 100%;
            }}

            .stats-row {{
                grid-template-columns: 1fr;
                justify-items: center;
            }}

            .stat-item {{
                width: 100%;
            }}

            .year-tabs {{
                flex-wrap: wrap;
            }}

            .leaderboard-item {{
                padding: 0.5rem 0.75rem;
            }}

            .name {{
                font-size: 0.9rem;
            }}

            .count {{
                font-size: 0.85rem;
            }}

            .meta {{
                font-size: 0.75rem;
            }}
        }}

        @media (max-width: 480px) {{
            h1 {{
                font-size: 2rem;
            }}

            .container {{
                padding: 0.75rem;
            }}

            .card {{
                padding: 1rem;
            }}

            .leaderboard-item {{
                padding: 0.5rem;
            }}

            .rank {{
                width: 1.75rem;
                height: 1.75rem;
                font-size: 0.75rem;
                margin-right: 0.5rem;
            }}

            .name {{
                font-size: 0.85rem;
            }}

            .occupation-badge {{
                font-size: 0.55rem;
                padding: 1px 4px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ERCF MESSAGE STATS</h1>
            <p class="subtitle">메시지 통계 리포트 📊</p>
        </header>

        <div class="year-tabs">
            <button class="year-tab active" onclick="showYear('2026')">2026년</button>
            <button class="year-tab" onclick="showYear('2025')">2025년</button>
        </div>

        <!-- 2026 Content -->
        <div id="year-2026" class="year-content active">
            <div class="date-range">📆 집계 기간: {date_range_2026}</div>
            <div class="section-grid">
                <!-- Total Message Counts -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">💬</span>
                        <h2 class="card-title">총 메시지 수 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count) for i, (name, count) in enumerate(counts_2026[:20])])}
                    </div>
                </div>

                <!-- Active Days -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">📅</span>
                        <h2 class="card-title">활동 일수 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count, "일") for i, (name, count) in enumerate(days_2026[:20])])}
                    </div>
                </div>

                <!-- Daily Max -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">🔥</span>
                        <h2 class="card-title">하루동안 최다 메시지 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count, "회", date) for i, (name, count, date) in enumerate(daily_max_2026)])}
                    </div>
                </div>

                <!-- Monthly TOP 5 -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🏆</span>
                        <h2 class="card-title">월별 TOP 5</h2>
                    </div>
                    <div class="monthly-grid">
{monthly_cards_2026}
                    </div>
                </div>

                <!-- Most Active Days -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🎉</span>
                        <h2 class="card-title">가장 활발한 날 TOP 20</h2>
                    </div>
                    <div class="stats-row">
{chr(10).join([generate_stat_item(i+1, date, count, people) for i, (date, count, people) in enumerate(most_active_2026)])}
                    </div>
                </div>

                <!-- Occupation Mention Ranking 2026 -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">🏆</span>
                        <h2 class="card-title">2026년 소속별 언급순위</h2>
                    </div>
                    <div class="leaderboard">
{generate_occ_ranking_items(sorted_totals_2026, groups_2026)}
                    </div>
                </div>

                <!-- Occupation Rankings 2026 -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🏢</span>
                        <h2 class="card-title">2026년 소속별 TOP 10</h2>
                    </div>
                    <div class="occupation-grid">
{chr(10).join(occ_cards_2026)}
                    </div>
                </div>
            </div>
        </div>

        <!-- 2025 Content -->
        <div id="year-2025" class="year-content">
            <div class="date-range">📆 집계 기간: {date_range_2025}</div>
            <div class="section-grid">
                <!-- Total Message Counts -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">💬</span>
                        <h2 class="card-title">총 메시지 수 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count) for i, (name, count) in enumerate(counts_2025[:20])])}
                    </div>
                </div>

                <!-- Active Days -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">📅</span>
                        <h2 class="card-title">활동 일수 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count, "일") for i, (name, count) in enumerate(days_2025[:20])])}
                    </div>
                </div>

                <!-- Daily Max -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">🔥</span>
                        <h2 class="card-title">하루동안 최다 메시지 TOP 20</h2>
                    </div>
                    <div class="leaderboard">
{chr(10).join([generate_leaderboard_item(i+1, name, count, "회", date) for i, (name, count, date) in enumerate(daily_max_2025)])}
                    </div>
                </div>

                <!-- Monthly TOP 5 -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🏆</span>
                        <h2 class="card-title">월별 TOP 5</h2>
                    </div>
                    <div class="monthly-grid">
{monthly_cards_2025}
                    </div>
                </div>

                <!-- Most Active Days -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🎉</span>
                        <h2 class="card-title">가장 활발한 날 TOP 20</h2>
                    </div>
                    <div class="stats-row">
{chr(10).join([generate_stat_item(i+1, date, count, people) for i, (date, count, people) in enumerate(most_active_2025)])}
                    </div>
                </div>

                <!-- Occupation Mention Ranking 2025 -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-icon">🏆</span>
                        <h2 class="card-title">2025년 소속별 언급순위</h2>
                    </div>
                    <div class="leaderboard">
{generate_occ_ranking_items(sorted_totals_2025, groups_2025)}
                    </div>
                </div>

                <!-- Occupation Rankings 2025 -->
                <div class="card full-width">
                    <div class="card-header">
                        <span class="card-icon">🏢</span>
                        <h2 class="card-title">2025년 소속별 TOP 10</h2>
                    </div>
                    <div class="occupation-grid">
{chr(10).join(occ_cards_2025)}
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>ERCF Message Statistics Report • Generated on {today}</p>
        </footer>
    </div>

    <script>
        function showYear(year) {{
            document.querySelectorAll('.year-content').forEach(el => {{
                el.classList.remove('active');
            }});
            
            document.querySelectorAll('.year-tab').forEach(el => {{
                el.classList.remove('active');
            }});
            
            document.getElementById('year-' + year).classList.add('active');
            event.target.classList.add('active');
        }}

        // Occupation data for badges
        const occupations = {{{occupation_js}}};

        function addOccupationBadges() {{
            document.querySelectorAll('.leaderboard-item .name').forEach(el => {{
                const text = el.textContent.trim();
                for (const [name, occupation] of Object.entries(occupations)) {{
                    if (text.includes(name) && !el.querySelector('.occupation-badge')) {{
                        const badge = document.createElement('span');
                        badge.className = 'occupation-badge occ-' + occupation;
                        badge.textContent = occupation;
                        el.appendChild(badge);
                        break;
                    }}
                }}
            }});
        }}

        addOccupationBadges();
    </script>
</body>
</html>'''
    
    return html

if __name__ == "__main__":
    # Build occupation JS mapping
    occupation_map = parse_occupations("occupation.csv")
    occupation_js = ",\n            ".join([f'"{name}": "{occ}"' for name, occ in occupation_map.items()])
    
    html = generate_html()
    # Inject occupation JS
    html = html.replace("{occupation_js}", occupation_js)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("index.html has been generated successfully!")
