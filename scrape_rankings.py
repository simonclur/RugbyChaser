import urllib.request
import json
import os
import re
import time

urls = [
    "https://api.wr-rims-prod.pulselive.com/rugby/v3/rankings/mru",
    "https://api.wr-rims-prod.pulselive.com/rugby/v3/rankings/wru"
]

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

success_count = 0
not_found_count = 0

for api_url in urls:
    print(f"\nFetching rankings from {api_url}...")
    req = urllib.request.Request(api_url, headers={'User-Agent': 'RugbyChaser'})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        
        for entry in data.get('entries', []):
            if isinstance(entry, str):
                continue
                
            team = entry.get('team', {})
            name = team.get('name')
            abbr = team.get('abbreviation')
            
            if not name or not abbr:
                continue

            # Men's teams might have women's teams mapped differently but usually same abbreviation
            # We'll use 'shields' as standard fallback
            flag_url = f"https://www.world.rugby/wl-assets/flags/shields/{abbr}.png"
            
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
            local_path = f"images/{safe_name}.png"
            
            # Check if we already have this exact official image
            existing = logos.get(name)
            if existing and isinstance(existing, dict) and existing.get("source_url") == flag_url and os.path.exists(local_path):
                continue
                
            # If not perfectly matched, or we have a wikipedia fallback, override it with this official one
            print(f"Downloading official shield for {name} ({abbr})...")
            
            try:
                img_req = urllib.request.Request(flag_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(img_req).read()
                
                with open(local_path, 'wb') as out_f:
                    out_f.write(img_data)
                
                logos[name] = {
                    "name": name,
                    "source_url": flag_url,
                    "local_path": local_path
                }
                success_count += 1
                time.sleep(0.05)
            except urllib.error.HTTPError as he:
                if he.code in [404, 403]: # S3 Cloudfront returns 403 when asset is missing
                    # Let's fallback to balls if shields missing
                    fallback_opts = ["squares", "balls"]
                    found_fallback = False
                    for b in fallback_opts:
                        fb_url = f"https://www.world.rugby/wl-assets/flags/{b}/{abbr}.png"
                        try:
                            f_req = urllib.request.Request(fb_url, headers={'User-Agent': 'Mozilla/5.0'})
                            f_data = urllib.request.urlopen(f_req).read()
                            with open(local_path, 'wb') as out_f:
                                out_f.write(f_data)
                            logos[name] = {
                                "name": name,
                                "source_url": fb_url,
                                "local_path": local_path
                            }
                            success_count += 1
                            found_fallback = True
                            print(f"  -> Found fallback format: {b}")
                            time.sleep(0.05)
                            break
                        except Exception:
                            pass
                    
                    if not found_fallback:
                        not_found_count += 1
                else:
                    print(f"HTTP Error {he.code} for {flag_url}")

    except Exception as e:
        print(f"Failed to process API {api_url}: {e}")

if success_count > 0:
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
        
print(f"\nCompleted! Downloaded {success_count} NEW official team logos using World Rugby rankings API.")
print(f"Missing from World Rugby CDN: {not_found_count}")
