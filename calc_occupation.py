# Calculate occupation rankings for 2025 and 2026

# Build occupation mapping from occupation.csv
occupation_map = {}
current_occ = None

with open("occupation.csv", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.endswith(":"):
            current_occ = line[:-1]
            # Normalize occupation names
            if current_occ == "수성초등학교":
                current_occ = "수성초"
            continue
        if current_occ:
            occupation_map[line] = current_occ

# Parse name counts
def parse_counts(filename):
    counts = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            parts = line.rsplit(":", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                count = int(parts[1].strip())
                counts[name] = count
    return counts

counts_2025 = parse_counts("name_counts_2025.csv")
counts_2026 = parse_counts("name_counts_2026.csv")

# Group by occupation
def group_by_occupation(counts):
    occ_groups = {}
    for name, count in counts.items():
        occ = occupation_map.get(name, "Unknown")
        if occ not in occ_groups:
            occ_groups[occ] = []
        occ_groups[occ].append((name, count))
    
    # Sort each group by count descending
    for occ in occ_groups:
        occ_groups[occ].sort(key=lambda x: x[1], reverse=True)
    
    return occ_groups

groups_2025 = group_by_occupation(counts_2025)
groups_2026 = group_by_occupation(counts_2026)

# Calculate total mentions per occupation
def calc_occupation_totals(groups):
    totals = {}
    for occ, members in groups.items():
        if occ != "Unknown":
            totals[occ] = sum(count for name, count in members)
    return totals

totals_2025 = calc_occupation_totals(groups_2025)
totals_2026 = calc_occupation_totals(groups_2026)

# Sort occupations by total mentions
sorted_2025 = sorted(totals_2025.items(), key=lambda x: x[1], reverse=True)
sorted_2026 = sorted(totals_2026.items(), key=lambda x: x[1], reverse=True)

# Write results to file
occupation_order = ["NU", "OSU", "수성초", "MAVERICK", "카카오톡", "행복한교회", "DCU", "NEPES", "무소속", "신천지"]

with open("occupation_rankings.txt", "w", encoding="utf-8") as out:
    # === 2025 Occupation Totals ===
    out.write("=" * 60 + "\n")
    out.write("2025 언급순위 (소속별 총 언급 수)\n")
    out.write("=" * 60 + "\n\n")
    for i, (occ, total) in enumerate(sorted_2025, 1):
        member_count = len(groups_2025.get(occ, []))
        out.write(f"{i}. {occ}: {total}회 ({member_count}명)\n")
    
    out.write("\n\n")
    out.write("=" * 60 + "\n")
    out.write("2025 Occupation Rankings (TOP 10)\n")
    out.write("=" * 60 + "\n")
    for occ in occupation_order:
        if occ in groups_2025:
            out.write(f"\n{occ}:\n")
            for i, (name, count) in enumerate(groups_2025[occ][:10], 1):
                out.write(f"  {i}. {name}: {count}\n")

    # === 2026 Occupation Totals ===
    out.write("\n\n")
    out.write("=" * 60 + "\n")
    out.write("2026 언급순위 (소속별 총 언급 수)\n")
    out.write("=" * 60 + "\n\n")
    for i, (occ, total) in enumerate(sorted_2026, 1):
        member_count = len(groups_2026.get(occ, []))
        out.write(f"{i}. {occ}: {total}회 ({member_count}명)\n")

    out.write("\n\n")
    out.write("=" * 60 + "\n")
    out.write("2026 Occupation Rankings (TOP 10)\n")
    out.write("=" * 60 + "\n")
    for occ in occupation_order:
        if occ in groups_2026:
            out.write(f"\n{occ}:\n")
            for i, (name, count) in enumerate(groups_2026[occ][:10], 1):
                out.write(f"  {i}. {name}: {count}\n")

    # Print unknown occupations
    out.write("\n\n")
    out.write("=" * 60 + "\n")
    out.write("Unknown occupations in 2025:\n")
    if "Unknown" in groups_2025:
        for name, count in groups_2025["Unknown"][:30]:
            out.write(f"  {name}: {count}\n")

    out.write("\nUnknown occupations in 2026:\n")
    if "Unknown" in groups_2026:
        for name, count in groups_2026["Unknown"]:
            out.write(f"  {name}: {count}\n")

print("Results written to occupation_rankings.txt")
print("\n2025 언급순위:")
for i, (occ, total) in enumerate(sorted_2025, 1):
    print(f"  {i}. {occ}: {total}회")
print("\n2026 언급순위:")
for i, (occ, total) in enumerate(sorted_2026, 1):
    print(f"  {i}. {occ}: {total}회")
