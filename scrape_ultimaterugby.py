import urllib.request
import re
import os
import json
import time

url = "https://www.ultimaterugby.com/super-rugby-americas-2026/table"

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

matches = re.finditer(r'<img[^>]+team-image[^>]+alt=\"([^\"]+)\"[^>]+data-src=\"([^\"]+)\"', html, re.IGNORECASE)

extracted_clubs = {}
for m in matches:
    alt_text = m.group(1).strip()
    img_url = m.group(2).strip()

    # Prepend the domain since it's a relative path in data-src
    if img_url.startswith("/"):
        img_url = "https://www.ultimaterugby.com" + img_url
        
    extracted_clubs[alt_text] = img_url

print(f"Found {len(extracted_clubs)} team logos on UltimateRugby.")

success_count = 0
for name, source_url in extracted_clubs.items():
    if "noimage" in source_url:
        continue

    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    ext = ".png" if ".png" in source_url.lower() else ".jpg" if ".jpg" in source_url.lower() else ".svg"
    local_path = f"images/{safe_name}{ext}"
    
    # We'll save it to JSON regardless, but only download if missing
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
            
            # Use structure {"name", "source_url", "local_path"} as confirmed in summary
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
    print(f"\nSuccessfully downloaded {success_count} NEW Ultimate Rugby crests!")
else:
    print("\nNo new Ultimate Rugby logos needed downloading.")
