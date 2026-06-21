import urllib.request
import re

urls = [
    "https://www.rugbyworldcup.com/2027/en/pools",
    "https://www.world.rugby/u20/en/pools",
    "https://www.world.rugby/pacific-nations-cup/en/pools",
    "https://www.world.rugby/tournaments/pacific-four-series/2024"
]

for url in urls:
    print(f"--- Fetching {url} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        
        matches = re.finditer(r'<img[^>]+src="(/wl-assets/flags/[^"]+)"[^>]+title="([^"]+)"', html, re.IGNORECASE)
        found = False
        for m in matches:
            found = True
            print(f"  {m.group(2)} -> {m.group(1)}")
        if not found:
            print("  No flags found.")
    except Exception as e:
        print(f"Error: {e}")
