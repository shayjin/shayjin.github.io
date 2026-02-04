import csv
from collections import Counter, defaultdict
from datetime import datetime


input_file = "message.csv"


# Count names and track distinct days and monthly counts - PER YEAR
# Structure: {year: Counter()}
name_counts_by_year = defaultdict(Counter)
name_days_by_year = defaultdict(lambda: defaultdict(set))
monthly_counts_by_year = defaultdict(lambda: defaultdict(Counter))

# Special stats - per year
# {year: [(name, count, date)]} - all daily counts for finding most active days
all_daily_counts_by_year = defaultdict(list)

current_date = None
current_year = None

with open(input_file, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Detect date lines (format MM-DD-YYYY)
        if line.count('-') == 2 and len(line) == 10:
            current_date = line
            current_year = line[-4:]  # Extract year (YYYY)
            continue
        # Parse name and count
        parts = line.rsplit(' ', 1)
        if len(parts) == 2 and current_date and current_year:
            name, count = parts
            try:
                count = int(count)
                name = name.strip()
                if name:
                    name_counts_by_year[current_year][name] += count
                    name_days_by_year[current_year][name].add(current_date)
                    # Get month in MM format
                    month = current_date[:2]
                    monthly_counts_by_year[current_year][month][name] += count
                    
                    # Track all daily counts for most active days
                    all_daily_counts_by_year[current_year].append((name, count, current_date))
            except ValueError:
                continue


# Write results for each year
for year in sorted(name_counts_by_year.keys()):
    # Write name_counts_YYYY.csv
    output_file = f"name_counts_{year}.csv"
    sorted_counts = sorted(name_counts_by_year[year].items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for name, count in sorted_counts:
            writer.writerow([name + ": " + str(count)])
    print(f"Name counts written to {output_file}")

    # Write name_days_YYYY.csv
    days_file = f"name_days_{year}.csv"
    with open(days_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for name, days in sorted(name_days_by_year[year].items(), key=lambda x: len(x[1]), reverse=True):
            writer.writerow([name + ": " + str(len(days))])
    print(f"Distinct day counts written to {days_file}")

    # Write top10_per_month_YYYY.csv
    top10_file = f"top10_per_month_{year}.csv"
    with open(top10_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for month in sorted(monthly_counts_by_year[year].keys()):
            top10 = monthly_counts_by_year[year][month].most_common(5)
            writer.writerow([f"{year}년 {month}월 TOP 5:"])
            for rank, (name, count) in enumerate(top10, 1):
                writer.writerow([str(rank) + ". " + name + " - " + str(count) + "회"])
            writer.writerow([])
    print(f"Top 10 per month written to {top10_file}")

    # Write special_stats_YYYY.csv
    special_file = f"special_stats_{year}.csv"
    with open(special_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # === DAILY MAX MESSAGES (하루동안 최다 메시지) ===
        writer.writerow([f"=== {year}년 하루동안 최다 메시지 TOP 20 ==="])
        writer.writerow([])
        # Sort all daily counts by count descending
        sorted_daily = sorted(all_daily_counts_by_year[year], key=lambda x: x[1], reverse=True)[:20]
        for rank, (name, count, date) in enumerate(sorted_daily, 1):
            writer.writerow([f"{rank}. {name} - {count}회 ({date})"])
        writer.writerow([])
        
        # === MOST ACTIVE DAYS (TOTAL PEOPLE) ===
        writer.writerow([f"=== {year}년 가장 활발한 날 TOP 20 ==="])
        writer.writerow([])
        daily_activity = defaultdict(lambda: {"people": 0, "messages": 0})
        for name, count, date in all_daily_counts_by_year[year]:
            daily_activity[date]["people"] += 1
            daily_activity[date]["messages"] += count
        
        sorted_days = sorted(daily_activity.items(), key=lambda x: x[1]["messages"], reverse=True)[:20]
        for rank, (date, stats) in enumerate(sorted_days, 1):
            writer.writerow([f"{rank}. {date} - {stats['messages']}회 ({stats['people']}명 참여)"])
        
    print(f"Special stats written to {special_file}")

print("\nAll yearly files generated!")