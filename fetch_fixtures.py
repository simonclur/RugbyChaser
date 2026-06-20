import urllib.request
import json
from datetime import datetime, timezone
import time

def fetch_fixtures():
    start_date = "2026-06-01"
    end_date = "2027-12-31"
    base_url = "https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate={}&endDate={}&pageSize=100&page={}"
    
    all_matches = []
    page = 0
    num_pages = 1

    print(f"Fetching matches from {start_date} to {end_date}...")

    while page < num_pages:
        url = base_url.format(start_date, end_date, page)
        req = urllib.request.Request(url, headers={'User-Agent': 'RugbyChaser/1.0'})
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if page == 0:
                    num_pages = data['pageInfo']['numPages']
                    print(f"Found {data['pageInfo']['numEntries']} matches total across {num_pages} pages.")
                
                all_matches.extend(data['content'])
                page += 1
                
                # Tiny sleep to be polite to the API
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    # Construct the final JSON payload
    output = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "totalMatches": len(all_matches),
        "matches": all_matches
    }

    output_file = "fixtures.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Successfully saved {len(all_matches)} matches and timestamp to {output_file}")

if __name__ == "__main__":
    fetch_fixtures()
