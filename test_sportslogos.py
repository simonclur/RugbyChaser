import urllib.request
import re

url = "https://www.sportslogos.net/teams/list_by_league/194/Aviva-Premiership-Rugby-Logos/Aviva-Logos/"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    
    print("Fetched successfully. Length:", len(html))
    
    # Look for list of teams
    matches = re.finditer(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"', html, re.IGNORECASE)
    for m in matches:
        print(f"Match: {m.group(2)} -> {m.group(1)}")

except Exception as e:
    print(f"Error: {e}")
