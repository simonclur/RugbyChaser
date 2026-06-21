import json
import os
import urllib.request
import re
import time

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

with open('fixtures.json', 'r') as f:
    fixtures = json.load(f)

unique_teams = set()
for m in fixtures.get('matches', []):
    for t in m.get('teams', []):
        if 'name' in t:
            unique_teams.add(t['name'].strip())

needed_keys = set()
for team in unique_teams:
    if team in logos:
        needed_keys.add(team)
    base_name = re.sub(r' (7s|XV|U20|A)$', '', team)
    if base_name in logos:
        needed_keys.add(base_name)
    if base_name + " Flag" in logos:
        needed_keys.add(base_name + " Flag")

for k in logos.keys():
    if k.endswith(" Flag"):
        needed_keys.add(k)
        
print(f"Total needed keys to fetch/verify: {len(needed_keys)}")

updated_logos = {}
success_count = 0

def fetch_image(url, max_retries=5):
    # Wikimedia requires a descriptive user agent
    headers = {
        'User-Agent': 'RugbyChaser/1.0 (https://github.com/simonclur/RugbyChaser; admin@localhost)',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                return res.read()
        except urllib.error.HTTPError as e:
            # 403 Forbidden is often used by Wikimedia for strict rate-limiting / bot-blocking
            if e.code in [403, 429, 500, 502, 503, 504]:
                retry_after = e.headers.get('Retry-After')
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        wait_time = base_delay * (2 ** attempt)
                else:
                    wait_time = base_delay * (2 ** attempt)
                    
                print(f"Rate limited/Blocked ({e.code}) for {url}. Waiting {wait_time}s...")
                time.sleep(wait_time)
            elif e.code == 404:
                print(f"Not found (404) for {url}")
                return None
            else:
                print(f"HTTP Error {e.code} for {url}")
                return None
        except Exception as e:
            wait_time = base_delay * (2 ** attempt)
            print(f"Network error ({e}) for {url}. Backing off for {wait_time}s...")
            time.sleep(wait_time)
            
    return None

for k, v in logos.items():
    if k not in needed_keys:
        updated_logos[k] = v
        continue
        
    url = v if isinstance(v, str) else v.get("wikipedia_url")
    
    # Check if we already have it in the dict struct
    if isinstance(v, dict) and v.get("local_path") and os.path.exists(v["local_path"]):
        updated_logos[k] = v
        continue
        
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', k)
    local_path = f"images/{safe_name}.png"
    
    # Only download if we haven't already grabbed it (in case script restarts)
    if os.path.exists(local_path):
        updated_logos[k] = {
            "name": k,
            "wikipedia_url": url,
            "local_path": local_path
        }
        success_count += 1
        continue
    
    img_data = None
    
    # Pre-process URLs to request 120px thumbnails for Wikimedia images
    fetch_url = url
    if url and "upload.wikimedia.org" in url:
        # If it's already a thumb URL, but might be using an invalid size like 100px, replace it
        if "/thumb/" in url:
            fetch_url = re.sub(r'/(\d+)px-', r'/120px-', url)
        else:
            # It's an original image URL, convert it to a thumb URL
            m = re.search(r"upload\.wikimedia\.org/wikipedia/([^/]+)/([a-z0-9]/[a-z0-9]{2})/([^/]+)$", url)
            if m:
                fetch_url = f"https://upload.wikimedia.org/wikipedia/{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/120px-{m.group(3)}"
                if m.group(3).lower().endswith(".svg"):
                    fetch_url += ".png"

    # Try fetching the URL directly first
    if fetch_url:
        print(f"Fetching {k} (thumbnail)...")
        img_data = fetch_image(fetch_url)
        
        # If it failed and is a wikimedia url, try extracting the base filename and using normal thumb URL
        if not img_data and "upload.wikimedia.org" in fetch_url:
            pass 
            
    if img_data:
        with open(local_path, 'wb') as out_f:
            out_f.write(img_data)
        updated_logos[k] = {
            "name": k,
            "wikipedia_url": fetch_url,
            "local_path": local_path
        }
        success_count += 1
    else:
        print(f"FAILED to fetch {k}: {fetch_url}")
        updated_logos[k] = {
            "name": k,
            "wikipedia_url": fetch_url,
            "local_path": None
        }

    time.sleep(5.0) # Delay each request by 5 seconds to avoid Wikipedia rate limits

with open('team_logos.json', 'w', encoding='utf-8') as f:
    json.dump(updated_logos, f, indent=2, ensure_ascii=False)

print(f"Successfully tracked {success_count} local images!")
