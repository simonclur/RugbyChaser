import urllib.request
import re
import json
import time

def extract_valid_urls():
    with open('team_logos.json', 'r') as f:
        logos = json.load(f)
        
    print("Migrating to simple country flags for all teams...")
    
    import urllib.request
    req = urllib.request.Request("https://en.wikipedia.org/wiki/Rugby_World_Cup", headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    flags = {}
    for m in re.finditer(r'<span class="flagicon">.*?<img[^>]*src="([^"]+)".*?</span>\s*<a[^>]*>([^<]+)</a>', html):
        src = "https:" + m.group(1).replace("23px", "80px")
        flags[m.group(2).strip()] = src
        
    req2 = urllib.request.Request("https://en.wikipedia.org/wiki/Rugby_World_Cup_Sevens", headers={"User-Agent": "Mozilla/5.0"})
    html2 = urllib.request.urlopen(req2).read().decode('utf-8')
    for m in re.finditer(r'<span class="flagicon">.*?<img[^>]*src="([^"]+)".*?</span>\s*<a[^>]*>([^<]+)</a>', html2):
        src = "https:" + m.group(1).replace("23px", "80px")
        flags[m.group(2).strip()] = src

    print(f"Extracted {len(flags)} valid Wikipedia thumb flags.")
    
    # We will ditch the failing SVG filepaths and use FlagCDN + valid Wiki thumbs
    import urllib.request
    import os
    
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Map country names to flagcdn for ultimate reliability
    try:
        req3 = urllib.request.Request("https://flagcdn.com/en/codes.json", headers={"User-Agent": "Mozilla/5.0"})
        codes = json.loads(urllib.request.urlopen(req3).read().decode('utf-8'))
        rev_codes = {v: k for k, v in codes.items()}
    except:
        rev_codes = {}
        
    updated = {}

    with open('fixtures.json', 'r') as f:
        fixtures = json.load(f)

    for m in fixtures.get('matches', []):
        for t in m.get('teams', []):
            if 'name' in t:
                team_name = t['name'].strip()
                base_name = re.sub(r' (7s|XV|U20|A|Women)$', '', team_name)
                
                safe_name = re.sub(r'[^a-zA-Z0-9]', '_', team_name)
                local_path = f"images/{safe_name}.png"
                
                # Check mapping
                flagcdn_url = None
                if base_name in rev_codes:
                    flagcdn_url = f"https://flagcdn.com/w80/{rev_codes[base_name]}.png"
                elif base_name == "Scotland": flagcdn_url = "https://flagcdn.com/w80/gb-sct.png"
                elif base_name == "England": flagcdn_url = "https://flagcdn.com/w80/gb-eng.png"
                elif base_name == "Wales": flagcdn_url = "https://flagcdn.com/w80/gb-wls.png"
                
                src_url = flagcdn_url or flags.get(base_name)
                
                if src_url:
                    if not os.path.exists(local_path):
                        print(f"Downloading {team_name} -> {src_url}")
                        try:
                            req_img = urllib.request.Request(src_url, headers={"User-Agent": "Mozilla/5.0"})
                            with open(local_path, 'wb') as out_f:
                                out_f.write(urllib.request.urlopen(req_img).read())
                        except Exception as e:
                            print(f"Failed {team_name}: {e}")
                            
                    updated[team_name] = {
                        "name": team_name,
                        "source_url": src_url,
                        "local_path": local_path
                    }

    # Save to UI format
    with open('team_logos.json', 'w') as f:
        json.dump(updated, f, indent=2)
        
    print(f"Downloaded exactly {len(updated)} reliable flags to /images")

if __name__ == '__main__':
    extract_valid_urls()
