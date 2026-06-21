import json
import re

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

fixed = 0
for k, v in logos.items():
    # Example: https://upload.wikimedia.org/wikipedia/en/thumb/1/13/England_Rugby.svg/100px-England_Rugby.svg.png
    # Target: https://upload.wikimedia.org/wikipedia/en/1/13/England_Rugby.svg
    
    # Or: https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/England_Rugby.svg/100px-...
    m = re.match(r'^(https://upload.wikimedia.org/wikipedia/[^/]+)/thumb/(.*?)/[^/]+\.(png|jpg|jpeg|gif)$', v)
    if m:
        new_url = m.group(1) + '/' + m.group(2)
        logos[k] = new_url
        fixed += 1
        
with open('team_logos.json', 'w', encoding='utf-8') as f:
    json.dump(logos, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed} URL formats in team_logos.json")
