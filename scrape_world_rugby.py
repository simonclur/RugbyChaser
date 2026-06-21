import urllib.request
import re
import os
import json
import time

urls = [
    "https://www.rugbyworldcup.com/2027/en/pools",
    "https://www.world.rugby/u20/en/pools",
    "https://www.world.rugby/pacific-nations-cup/en/pools",
    "https://www.world.rugby/tournaments/pacific-four-series/2026",
    "https://www.world.rugby/beta/en/tournaments/pacific-four-series/2026",
    "https://www.world.rugby/sevens-series/en/pools"
]

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

team_images = {}
for url in urls:
    print(f"Scanning {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        
        img_tags = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
        for tag in img_tags:
            if '/wl-assets/flags/' in tag:
                src_m = re.search(r'src=["\']([^"\']+)["\']', tag, re.IGNORECASE)
                title_m = re.search(r'title=["\']([^"\']+)["\']', tag, re.IGNORECASE)
                alt_m = re.search(r'alt=["\']([^"\']+)["\']', tag, re.IGNORECASE)
                
                src = src_m.group(1) if src_m else None
                title = title_m.group(1) if title_m else None
                alt = alt_m.group(1) if alt_m else None
                
                name = title or alt
                
                if src and name and name != "default":
                    if src.startswith('/'):
                        if 'rugbyworldcup.com' in url:
                            src = 'https://www.rugbyworldcup.com' + src
                        else:
                            src = 'https://www.world.rugby' + src
                            
                    team_images[name] = src
    except urllib.error.HTTPError as e:
        print(f"Skipping {url} gracefully ({e.code})")

success_count = 0
for name, url in team_images.items():
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    local_path = f"images/{safe_name}.png"
    
    # Add mapping if it does not exist perfectly matched
    if True:
        try:
            print(f"Downloading {name} -> {local_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(req).read()
            with open(local_path, 'wb') as out_f:
                out_f.write(img_data)
            
            logos[name] = {
                "name": name,
                "source_url": url,
                "local_path": local_path
            }
            success_count += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

if success_count > 0:
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully added {success_count} NEW official team logos from World Rugby!")
else:
    print("\nNo new logos needed downloading.")
