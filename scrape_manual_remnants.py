import urllib.request
import re
import os
import json
import time

teams_to_scrape = [
    "ASM Romagnat",
    "Blagnac Rugby Féminin",
    "FC Grenoble Amazones",
    "Stade Bordelais",
    "Villeneuve d'Ascq Lille Métropole Rugby"
]

if not os.path.exists('images'):
    os.makedirs('images')

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

extracted_clubs = {}

# Just explicitly grab these ones from Wikipedia or direct links since they are obscure
manual_links = {
    "Cobras": "https://upload.wikimedia.org/wikipedia/en/e/ec/Cobras_xv_logo.png",
    "Peñarol": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Escudo_del_Club_Atl%C3%A9tico_Pe%C3%B1arol.svg",
    "Yacare XV": "https://upload.wikimedia.org/wikipedia/en/4/4c/Yakare_XV_logo.png",
    "Trailfinders Women": "https://upload.wikimedia.org/wikipedia/en/f/f3/Trailfinders_rfc_logo.png",
    "Stade Bordelais": "https://upload.wikimedia.org/wikipedia/fr/0/05/Logo_Stade_bordelais_rugby_-_2015.svg",
    "ASM Romagnat Rugby Feminin": "https://upload.wikimedia.org/wikipedia/fr/1/1a/Logo_ASM_Romagnat_rugby_f%C3%A9minin.svg",
    "Blagnac Sporting Club Rugby": "https://upload.wikimedia.org/wikipedia/fr/7/7b/Blagnac_sporting_club_rugby_2022_logo.svg",
    "FC Grenoble Amazones": "https://upload.wikimedia.org/wikipedia/fr/7/7a/1200px-FC_Grenoble_logo.svg.png",
    "Stade Villeneuvois Lille Metropole": "https://upload.wikimedia.org/wikipedia/fr/4/4d/Logo_Lille_M%C3%A9tropole_RC_villeneuvois_-_2022.svg",
    "AC Bobigny 93 Rugby": "https://upload.wikimedia.org/wikipedia/fr/b/b2/Logo_AC_bobigny_93.png",
    "Great Britain 7s": "https://upload.wikimedia.org/wikipedia/en/9/93/Great_Britain_national_rugby_sevens_team.png"
}

success_count = 0
for name, source_url in manual_links.items():
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
            req = urllib.request.Request(source_url, headers={'User-Agent': 'RugbyChaserScraper/1.0 (test@example.com)'})
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
            time.sleep(1)
        except Exception as e:
            print(f" Failed to fetch {source_url}: {e}")

if success_count > 0:
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully downloaded {success_count} NEW manual crests!")
else:
    print("\nNo new manual logos needed downloading.")
