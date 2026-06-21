import urllib.request
import re

urls = [
    "https://www.rugbyworldcup.com/2027/en",
    "https://www.world.rugby/u20/en",
    "https://www.world.rugby/pacific-nations-cup/en/",
    "https://www.world.rugby/beta/en/tournaments/pacific-four-series/2026",
    # Typical pools pages:
    "https://www.world.rugby/u20/en/pools",
    "https://www.rugbyworldcup.com/2027/en/pools"
]

for url in urls:
    print(f"--- Fetching {url} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        
        # Look for image tags or team names
        print("Matches for svg/png:", len(re.findall(r'\.(svg|png|webp)', html, re.IGNORECASE)))
        # Specifically look for Next.js data if present
        if '__NEXT_DATA__' in html:
            print("Contains __NEXT_DATA__")
    except Exception as e:
        print(f"Error: {e}")
