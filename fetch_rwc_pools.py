import urllib.request
import json
import re

def fetch_pools():
    url = "https://www.rugbyworldcup.com/2027/en/pools"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    pools = {}
    
    pool_blocks = html.split('class="full-pools__pool-header"')
    for block in pool_blocks[1:]:
        title_match = re.search(r'class="full-pools__pool-title">(.*?)</span>', block)
        if not title_match:
            continue
        pool_title = title_match.group(1).strip()
        
        teams = []
        rows = block.split('<tr class="full-pools__table-row')
        for row in rows[1:]:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) < 13:
                continue
            
            def clean_html(text):
                return re.sub(r'<[^>]+>', '', text).strip()
            
            position = clean_html(cells[1])
            
            team_match = re.search(r'<span class="full-pools__team u-hide-tablet">(.*?)</span>', cells[2])
            team_name = clean_html(team_match.group(1)) if team_match else "TBC"
            
            played = clean_html(cells[3])
            won = clean_html(cells[4])
            drawn = clean_html(cells[5])
            lost = clean_html(cells[6])
            
            # 7 = pf, 8 = pa, 9 = pd, 10 = tf, 11 = bp, 12 = pts
            points_diff = clean_html(cells[9])
            pts = clean_html(cells[12])
            
            teams.append({
                "position": position,
                "team": team_name,
                "played": played,
                "won": won,
                "drawn": drawn,
                "lost": lost,
                "points_diff": points_diff,
                "points": pts
            })
            
        pools[pool_title] = teams
        
    with open("rwc_pools.json", "w") as f:
        json.dump(pools, f, indent=4)
        
    print(f"Scraped {len(pools)} pools successfully.")

fetch_pools()
