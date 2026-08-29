import urllib.request
import json
import os

urls = {
    "mru": "https://api.wr-rims-prod.pulselive.com/rugby/v3/rankings/mru",
    "wru": "https://api.wr-rims-prod.pulselive.com/rugby/v3/rankings/wru"
}

rankings_data = {}

for gender, api_url in urls.items():
    print(f"Fetching {gender} rankings...")
    req = urllib.request.Request(api_url, headers={'User-Agent': 'RugbyChaser'})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        
        parsed_entries = []
        for entry in data.get('entries', []):
            if isinstance(entry, str): continue
            team = entry.get('team', {})
            name = team.get('name')
            pts = entry.get('pts')
            pos = entry.get('pos')
            if name and pts is not None:
                parsed_entries.append({
                    "name": name,
                    "pts": pts,
                    "pos": pos
                })
        rankings_data[gender] = parsed_entries
    except Exception as e:
        print(f"Failed to fetch {gender} rankings: {e}")

with open('rankings.json', 'w') as f:
    json.dump(rankings_data, f, indent=2)

print("Saved rankings.json!")
