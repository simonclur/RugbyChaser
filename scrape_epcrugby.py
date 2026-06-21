import urllib.request
import re
import os
import json
import time

urls = [
    "https://www.epcrugby.com/champions-cup/clubs",
    "https://www.epcrugby.com/challenge-cup/clubs"
]

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

extracted_clubs = {}

for url in urls:
    print(f"Scanning {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to scan {url}: {e}")
        continue

    # The HTML uses lazy loading, alt text has team name, and src has incrowdsports URLs
    matches = re.finditer(r'<img[^>]+src=\"([^\"]+)\"[^>]*alt=\"([^\"]+)\"[^>]*>', html, re.IGNORECASE)

    for m in matches:
        img_url = m.group(1).replace("&amp;", "&")
        alt_text = m.group(2).strip()

        # Skip generic site SVGs
        if alt_text in ["Champions cup", "Challenge cup", "Challenge Cup", "EPCR", "Champions Cup logo", "Challenge Cup logo", "incrowd-logo"]:
            continue
        if not img_url.startswith("https://media-cdn.incrowdsports.com"):
            continue
            
        extracted_clubs[alt_text] = img_url

print(f"Found {len(extracted_clubs)} team logos on EPCRugby.")

success_count = 0
for name, source_url in extracted_clubs.items():
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    ext = ".png" if "png" in source_url.lower() else ".svg"
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
            req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.epcrugby.com/'})
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
    print(f"\nSuccessfully downloaded {success_count} NEW Champion's Cup crests!")
else:
    print("\nNo new Champion's Cup logos needed downloading.")
