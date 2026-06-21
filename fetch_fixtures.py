import urllib.request
import json
from datetime import datetime, timezone
import time

def fetch_fixtures():
    start_date = "2026-06-01"
    end_date = "2027-12-31"
    base_url = "https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate={}&endDate={}&pageSize=100&page={}"
    
    all_matches = []
    page = 0
    num_pages = 1

    print(f"Fetching matches from {start_date} to {end_date}...")

    while page < num_pages:
        url = base_url.format(start_date, end_date, page)
        req = urllib.request.Request(url, headers={'User-Agent': 'RugbyChaser/1.0'})
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if page == 0:
                    num_pages = data['pageInfo']['numPages']
                    print(f"Found {data['pageInfo']['numEntries']} matches total across {num_pages} pages.")
                
                all_matches.extend(data['content'])
                page += 1
                
                # Tiny sleep to be polite to the API
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    # Construct the final JSON payload
    output = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "totalMatches": len(all_matches),
        "matches": all_matches
    }

    output_file = "fixtures.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Successfully saved {len(all_matches)} matches and timestamp to {output_file}")

def fetch_rwc_pools():
    import urllib.request
    import re
    url = "https://www.rugbyworldcup.com/2027/en/pools"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        pools = {}
        pool_blocks = html.split('class="full-pools__pool-header"')
        for block in pool_blocks[1:]:
            title_match = re.search(r'class="full-pools__pool-title">(.*?)</span>', block)
            if not title_match: continue
            pool_title = title_match.group(1).strip()
            teams = []
            rows = block.split('<tr class="full-pools__table-row')
            for row in rows[1:]:
                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(cells) < 13: continue
                def clean_html(text): return re.sub(r'<[^>]+>', '', text).strip()
                position = clean_html(cells[1])
                team_match = re.search(r'<span class="full-pools__team u-hide-tablet">(.*?)</span>', cells[2])
                team_name = clean_html(team_match.group(1)) if team_match else "TBC"
                teams.append({
                    "position": position,
                    "team": team_name,
                    "played": clean_html(cells[3]),
                    "won": clean_html(cells[4]),
                    "drawn": clean_html(cells[5]),
                    "lost": clean_html(cells[6]),
                    "points_diff": clean_html(cells[9]),
                    "points": clean_html(cells[12])
                })
            pools[pool_title] = teams
        with open("rwc_pools.json", "w") as f:
            json.dump(pools, f, indent=4)
        print(f"Scraped {len(pools)} RWC pools.")
    except Exception as e:
        print(f"Failed to fetch RWC pools: {e}")

if __name__ == "__main__":
    fetch_fixtures()
    fetch_rwc_pools()
