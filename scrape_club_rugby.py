import urllib.request
import re
import os
import json
import time

urls = [
    "https://www.sportslogos.net/teams/list_by_league/194/Aviva-Premiership-Rugby-Logos/Aviva-Logos/",
    "https://www.sportslogos.net/teams/list_by_league/196/Super-Rugby-Logos/Super-Rugby-Logos/",
    "https://www.sportslogos.net/teams/list_by_league/193/Pro12-Logos/Pro12-Logos/"
]

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

extracted_clubs = {}

# Scrape the pages
for url in urls:
    print(f"Scanning {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        
        matches = re.finditer(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"', html, re.IGNORECASE)
        for m in matches:
            img_url = m.group(1)
            alt_text = m.group(2)
            
            # Clean up alt text to get base team name: e.g. "Exeter Chiefs Logo" -> "Exeter Chiefs"
            name = re.sub(r'(?i)\s*Logo$', '', alt_text).strip()
            
            # Skip irrelevant header icons from the site
            if name in ['MLB', 'NHL', 'NBA', 'NFL', 'NCAA', 'Baseball', 'Basketball', 'Football', 'Hockey', 'Soccer', 'College', 'Other Sports', 'News', 'Forums', 'Podcast', 'Search']:
                continue
                
            # If it's a valid remote URL
            if img_url.startswith('https://content.sportslogos.net'):
                extracted_clubs[name] = img_url
    except Exception as e:
        print(f"Failed to scan {url}: {e}")

success_count = 0
for name, url in extracted_clubs.items():
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    local_path = f"images/{safe_name}.gif"
    
    # We'll save it to JSON regardless, but only download if missing
    existing = logos.get(name)
    has_local = False
    
    if isinstance(existing, dict) and existing.get("local_path"):
        if os.path.exists(existing.get("local_path")):
            has_local = True
            
    if not has_local:
        print(f"Downloading {name} -> {local_path}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.sportslogos.net/'})
            img_data = urllib.request.urlopen(req).read()
            with open(local_path, 'wb') as out_f:
                out_f.write(img_data)
            
            logos[name] = {
                "name": name,
                "source_url": url,
                "local_path": local_path
            }
            success_count += 1
            time.sleep(0.2)
        except Exception as e:
            print(f" Failed to fetch {url}: {e}")

if success_count > 0:
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully downloaded {success_count} NEW club crests!")
else:
    print("\nNo new distinctive club logos needed downloading.")
