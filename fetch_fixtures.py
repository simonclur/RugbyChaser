import urllib.request
import json
from datetime import datetime, timezone
import time

VENUE_TZ_BY_COUNTRY = {
    'New Zealand': 'Pacific/Auckland', 'Fiji': 'Pacific/Fiji', 'France': 'Europe/Paris',
    'England': 'Europe/London', 'Scotland': 'Europe/London', 'Wales': 'Europe/London',
    'Ireland': 'Europe/Dublin', 'Italy': 'Europe/Rome', 'Georgia': 'Asia/Tbilisi',
    'Hong Kong China': 'Asia/Hong_Kong', 'Japan': 'Asia/Tokyo', 'Korea': 'Asia/Seoul',
    'South Africa': 'Africa/Johannesburg', 'Uganda': 'Africa/Kampala',
    'Argentina': 'America/Argentina/Buenos_Aires', 'Uruguay': 'America/Montevideo',
    'Chile': 'America/Santiago', 'Barbados': 'America/Barbados', 'Cayman Islands': 'America/Cayman',
}

# Countries spanning several zones, matched on a substring of the venue city.
VENUE_TZ_BY_CITY = {
    'Australia': [('Perth', 'Australia/Perth'), ('Adelaide', 'Australia/Adelaide'),
                  ('Brisbane', 'Australia/Brisbane'), ('Townsville', 'Australia/Brisbane'),
                  ('Melbourne', 'Australia/Melbourne'), ('Sydney', 'Australia/Sydney'),
                  ('Newcastle', 'Australia/Sydney'), ('Canberra', 'Australia/Sydney')],
    'Canada': [('Edmonton', 'America/Edmonton'), ('Winnipeg', 'America/Winnipeg'),
               ('Ottawa', 'America/Toronto'), ('Toronto', 'America/Toronto')],
    'United States': [('Seattle', 'America/Los_Angeles'), ('Denver', 'America/Denver'),
                      ('Chicago', 'America/Chicago')],
}
VENUE_TZ_DEFAULT = {'United States': 'America/New_York'}


# Matches whose feed millis was verified against the official kickoff time while the feed's
# gmtOffset was wrong: keep millis and only fix the offset.
FEED_MILLIS_VERIFIED = {'e92fb0a4-c60d-4f7b-a123-fb85ee0bca06'}  # Force Women v Waratahs Women, 2026-06-27


def venue_timezone(venue):
    if not venue:
        return None
    country, city = venue.get('country'), venue.get('city') or ''
    for key, tz in VENUE_TZ_BY_CITY.get(country, []):
        if key in city:
            return tz
    return VENUE_TZ_BY_COUNTRY.get(country) or VENUE_TZ_DEFAULT.get(country)


def normalize_match_times(matches):
    """Re-derive millis/gmtOffset from the feed's local wall-clock time using the venue's
    IANA timezone, so DST (and any other offset change) is applied for the kickoff date.

    The feed sometimes ships a stale/standard-time gmtOffset (e.g. NZ matches during NZDT),
    which makes millis wrong. The local wall-clock (millis + gmtOffset) is the reliable part.
    Midnight wall-clock times are TBC placeholders and are left untouched.
    """
    from zoneinfo import ZoneInfo
    from datetime import timedelta
    fixed = 0
    for m in matches:
        t = m.get('time') or {}
        tz_name = venue_timezone(m.get('venue'))
        if not tz_name or t.get('millis') is None or t.get('gmtOffset') is None:
            continue
        if m.get('matchId') in FEED_MILLIS_VERIFIED:
            instant = datetime.fromtimestamp(t['millis'] / 1000, timezone.utc).astimezone(ZoneInfo(tz_name))
            t['gmtOffset'] = instant.utcoffset().total_seconds() / 3600
            continue
        wall = datetime.fromtimestamp(t['millis'] / 1000 + t['gmtOffset'] * 3600, timezone.utc).replace(tzinfo=None)
        if wall.hour == 0 and wall.minute == 0:
            continue
        local = wall.replace(tzinfo=ZoneInfo(tz_name))
        offset = local.utcoffset().total_seconds() / 3600
        if offset == t['gmtOffset']:
            continue
        new_millis = int(local.timestamp() * 1000)
        print(f"Corrected {t.get('label')} {(m.get('venue') or {}).get('city')}: "
              f"offset {t['gmtOffset']} -> {offset}, millis {t['millis']} -> {new_millis}")
        t['feedMillis'], t['feedGmtOffset'] = t['millis'], t['gmtOffset']
        t['millis'], t['gmtOffset'] = new_millis, offset
        fixed += 1
    return fixed


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

    normalize_match_times(all_matches)

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

def fetch_rwc_pools():
    import urllib.request
    import re
    url = "https://www.rugbyworldcup.com/2027/en/pools"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        pools = {}
        pool_blocks = html.split('class="full-pools__pool-header"')
        for block in pool_blocks[1:]:
            title_match = re.search(r'class="full-pools__pool-title">(.*?)</span>', block)
            if not title_match: continue
            pool_title = title_match.group(1).strip()
            teams = []
            rows = block.split('<tr class="full-pools__table-row')
            for row in rows[1:]:
                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(cells) < 13: continue
                def clean_html(text): return re.sub(r'<[^>]+>', '', text).strip()
                position = clean_html(cells[1])
                team_match = re.search(r'<span class="full-pools__team u-hide-tablet">(.*?)</span>', cells[2])
                team_name = clean_html(team_match.group(1)) if team_match else "TBC"
                teams.append({
                    "position": position,
                    "team": team_name,
                    "played": clean_html(cells[3]),
                    "won": clean_html(cells[4]),
                    "drawn": clean_html(cells[5]),
                    "lost": clean_html(cells[6]),
                    "points_for": clean_html(cells[7]),
                    "points_against": clean_html(cells[8]),
                    "points_diff": clean_html(cells[9]),
                    "tries_for": clean_html(cells[10]),
                    "points": clean_html(cells[12])
                })
            pools[pool_title] = teams
        with open("rwc_pools.json", "w") as f:
            json.dump(pools, f, indent=4)
        print(f"Scraped {len(pools)} RWC pools.")
    except Exception as e:
        print(f"Failed to fetch RWC pools: {e}")

if __name__ == "__main__":
    fetch_fixtures()
    fetch_rwc_pools()
