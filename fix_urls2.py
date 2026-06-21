import json
import re
import urllib.parse

with open('team_logos.json', 'r') as f:
    logos = json.load(f)

fixed = 0
for k, v in logos.items():
    # If it's a wikimedia image
    if 'upload.wikimedia.org' in v:
        # Extract just the filename at the end
        filename = v.split('/')[-1]
        
        # If it accidentally still has the 100px- at the front from a bad regex
        if filename.startswith('100px-') and filename.endswith('.png'):
            filename = filename[6:-4] # strip 100px- and .png
            
        # URL decode it first just in case
        filename = urllib.parse.unquote(filename)
        
        # Create robust special filepath link
        new_url = f"https://en.wikipedia.org/wiki/Special:FilePath/{urllib.parse.quote(filename)}?width=300"
        logos[k] = new_url
        fixed += 1

with open('team_logos.json', 'w', encoding='utf-8') as f:
    json.dump(logos, f, indent=2, ensure_ascii=False)

print(f"Refactored {fixed} URLs to use robust Special:FilePath!")
