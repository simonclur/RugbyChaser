import urllib.request
import re
import os
import json
import time

url = "https://www.espn.com.au/rugby/table/_/league/270559"

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

print(f"Scanning {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
except Exception as e:
    print(f"Failed to scan {url}: {e}")
    exit(1)

m = re.search(r'window\[\'__espnfitt__\'\]=(.*?);</script>', html)
if not m:
    print("Could not find __espnfitt__")
    exit(1)

data = json.loads(m.group(1))

extracted_clubs = {}

def find_teams(obj):
    if isinstance(obj, dict):
        if 'logo' in obj and isinstance(obj['logo'], str) and ('displayName' in obj or 'name' in obj):
            name = obj.get('displayName') or obj.get('name')
            if name:
                extracted_clubs[name] = obj['logo']
                
        # Also check list of logos if it exists
        if 'logos' in obj and isinstance(obj['logos'], list) and len(obj['logos']) > 0:
            name = obj.get('displayName') or obj.get('name')
            if name and isinstance(obj['logos'][0], dict) and 'href' in obj['logos'][0]:
                extracted_clubs[name] = obj['logos'][0]['href']

        for k, v in obj.items():
            find_teams(v)
    elif isinstance(obj, list):
        for item in obj:
            find_teams(item)

find_teams(data)

print(f"Found {len(extracted_clubs)} team logos on ESPN.")

success_count = 0
for name, source_url in extracted_clubs.items():
    if not source_url: continue
    
    if 'rugby' not in source_url.lower():
        continue

    # Fix ESPN combiner paths to get original high-res logo
    if "combiner/i" in source_url or "combiner" in source_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(source_url)
        query = urllib.parse.parse_qs(parsed.query)
        if 'img' in query:
            source_url = "https://a.espncdn.com" + query['img'][0]
    
    # Strip any trailing dimension query params
    source_url = source_url.split('&')[0].split('?')[0]
    
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    ext = ".png" if ".png" in source_url.lower() else ".jpg" if ".jpg" in source_url.lower() else ".svg"
    local_path = f"images/{safe_name}{ext}"
    
    existing = logos.get(name)
    has_local = False
    
    if isinstance(existing, dict) and existing.get("local_path"):
        if os.path.exists(existing.get("local_path")):
            has_local = True
            
    if not has_local:
        print(f"Downloading {name} -> {local_path}")
        try:
            req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(req).read()
            with open(local_path, 'wb') as out_f:
                out_f.write(img_data)
            
            logos[name] = {
                "name": name,
                "source_url": source_url,
                "local_path": local_path
            }
            success_count += 1
            time.sleep(0.2)
        except Exception as e:
            print(f" Failed to fetch {source_url}: {e}")

if success_count > 0:
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully downloaded {success_count} NEW ESPN crests!")
else:
    print("\nNo new ESPN logos needed downloading.")
