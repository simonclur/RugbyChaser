import os
import json
import time
import urllib.request
import re

challenge_cup_teams = {
    "Montpellier": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/97930425-f7b9-4daa-ad00-606f4e6354be/large.png",
    "Zebre": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/14d54387-cc7b-4d41-909f-1034e1bcd018/large.png",
    "Connacht": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/99c487df-9c7f-4108-9e6d-c084d776f68b/large.png",
    "Ospreys": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/19de653e-9d0f-47f5-8ed1-f2d9112b226f/large.png",
    "Black Lion": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/9ecea3c7-d44d-43fd-9aeb-46b3977b2df6/large.png",
    "US Montauban": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/30e7866c-c6a4-43c0-b078-ab3f4ce187f6/large.png",
    "Benetton": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/5b3edbba-bfa9-4aba-afb9-3bd3bb68882e/large.png",
    "Newcastle": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/ab05b0a9-b59d-4cdb-bf85-ded89f5be803/large.png",
    "Dragons": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/e4b99d38-cccc-4a2f-91e7-14e648464f84/large.png",
    "Perpignan": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/09bce6ab-25db-4837-971f-e18f84512fe9/large.png",
    "Fidelity SecureDrive Lions": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/2534f3e3-523f-41b4-b107-2a5563580863/large.png",
    "Lyon": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/78328b2f-614a-400b-b55d-1f7e19f6a53a/large.png",
    "Ulster": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/08c83263-adff-448f-a0b8-843657696a6c/large.png",
    "Stade Francais": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/ac960b77-85f9-4d03-9b49-615d636cad69/large.png",
    "Exeter": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/343df512-545d-4bf0-9e0f-6bc42d6dfc2c/large.png",
    "Cardiff": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/def4ca59-fdad-429b-9910-9cbb9832efdb/large.png",
    "Racing 92": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/d077a714-a4ba-4f27-89cc-235171b85ad8/large.png",
    "Toyota Cheetahs": "https://mobiithumbnails.blob.core.windows.net/thumbnails/live/stratus/26dec522-2aeb-4f73-aaa8-ae538c1d1410/large.png"
}

def main():
    if not os.path.exists('images'):
        os.makedirs('images')

    with open('team_logos.json', 'r') as f:
        logos = json.load(f)

    success_count = 0
    for name, source_url in challenge_cup_teams.items():
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        local_path = f"images/{safe_name}.png"
        
        has_local = False
        existing = logos.get(name)
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
                time.sleep(0.1)
            except Exception as e:
                print(f" Failed to fetch {source_url}: {e}")
        else:
            print(f"Already have {name}")

    if success_count > 0:
        with open('team_logos.json', 'w', encoding='utf-8') as f:
            json.dump(logos, f, indent=2, ensure_ascii=False)
        print(f"Successfully downloaded {success_count} NEW Challenge Cup logos!")
    else:
        print("No new Challenge Cup logos needed downloading.")

if __name__ == '__main__':
    main()
