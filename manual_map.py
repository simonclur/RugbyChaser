import json

with open('team_logos.json', 'r') as f:
    scraped = json.load(f)

print([k for k in scraped.keys() if 'Flag' in k][:20])
