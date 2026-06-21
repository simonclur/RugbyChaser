import urllib.request
import re
import os
import json
import time

url = "https://league-one.jp/en/team/"

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

# Find all img tags first
img_matches = re.finditer(r'<img\s+([^>]+)>', html, re.IGNORECASE)

extracted_clubs = {}
for m in img_matches:
    attrs = m.group(1)
    src_match = re.search(r'src=\"([^\"]+)\"', attrs, re.IGNORECASE)
    alt_match = re.search(r'alt=\"([^\"]+)\"', attrs, re.IGNORECASE)
    
    if src_match and alt_match:
        src = src_match.group(1)
        alt = alt_match.group(1).strip()
        
        if "team_info" in src:
            extracted_clubs[alt] = src

# Drop duplicates (since they appear multiple times for conferences likely)
unique_clubs = {k: v for k, v in extracted_clubs.items() if v}

print(f"Found {len(unique_clubs)} unique team logos on Japan Rugby League One.")

success_count = 0
for name, source_url in unique_clubs.items():
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
    print(f"\nSuccessfully downloaded {success_count} NEW Japan League One crests!")
else:
    print("\nNo new Japan League One logos needed downloading.")
