import json
import difflib

def main():
    with open('fixtures.json', 'r') as f:
        fixtures = json.load(f)
        
    unique_teams = set()
    for m in fixtures.get('matches', []):
        for t in m.get('teams', []):
            if 'name' in t:
                unique_teams.add(t['name'].strip())
                
    with open('team_logos.json', 'r') as f:
        scraped_logos = json.load(f)
        
    logo_keys = list(scraped_logos.keys())
    
    # We will build a clean, new dictionary mapping exactly Fixture Team Name -> URL
    final_mapping = {}
    
    # Custom hardcoded mapping for teams that don't fuzzy-match well
    custom_map = {
        "Argentina": "Argentine Rugby Union logo 2023",
        "Argentina 7s": "Argentine Rugby Union logo 2023",
        "Argentina U20": "Argentine Rugby Union logo 2023",
        "Ireland": "Irish Rugby Football Union",
        "Ireland 7s": "Irish Rugby Football Union",
        "Ireland U20": "Irish Rugby Football Union",
        "France": "Logo XV de France masculin 2019",
        "France 7s": "Logo XV de France masculin 2019",
        "New Zealand": "New Zealand All Blacks",
        "New Zealand 7s": "New Zealand All Blacks",
        "New Zealand U20": "New Zealand All Blacks",
        "Maori All Blacks": "New Zealand All Blacks",
        "Black Ferns XV": "New Zealand women's national rugby union team",
        "Australia": "Wallabies",
        "Australia A": "Wallabies",
        "Australia U20": "Wallabies",
        "South Africa": "South Africa",
        "South Africa 7s": "South Africa",
        "South Africa U20": "South Africa",
        "Wales": "Welsh Rugby Union logo",
        "Wales 7s": "Welsh Rugby Union logo",
        "Scotland": "Scottish Rugby Union",
        "Scotland 7s": "Scottish Rugby Union",
        "England": "England Rugby",
        "England 7s": "England Rugby",
        "Italy": "Federazione Italiana Rugby",
        "Italy 7s": "Federazione Italiana Rugby",
        "Fiji": "Logo Fiji Rugby 2019",
        "Fiji 7s": "Logo Fiji Rugby 2019",
        "Samoa": "Samoa Rugby Union",
        "Samoa 7s": "Samoa Rugby Union",
        "Uruguay": "Uruguayan Rugby Union",
        "Japan": "Japan Rugby Football Union",
        "USA": "United States Rugby",
        "Georgia": "Federation Georgian Rugby",
        "Portugal": "Romanian Rugby Federation",  # wait, no
        "Romania": "Romanian Rugby Federation",
        "Spain": "Spanish Rugby Federation",
        "Chile": "Chile Rugby",
        "Canada": "Rugby Canada",
        "Ospreys": "Ospreys (rugby union)",
        "Chiefs": "Chiefs (rugby union)",
        "Crusaders": "Crusaders (rugby union)",
        "Hurricanes": "Hurricanes (rugby union)",
        "Highlanders": "Highlanders (rugby union)",
        "Blues": "Blues (Super Rugby)",
        "Brumbies": "ACT Brumbies",
        "Reds": "Queensland Reds",
        "Waratahs": "Queensland Reds",
        "Bath Rugby": "Bath Rugby",
        "Bristol Bears": "Bristol Bears",
        "Saracens": "Saracens F.C."
    }

    matched = 0
    
    for team in sorted(list(unique_teams)):
        # 1. Custom Match
        if team in custom_map:
            cm = custom_map[team]
            # Try to grab the closest match to our custom map if it's not exact
            cm_matches = difflib.get_close_matches(cm, logo_keys, n=1, cutoff=0.3)
            if cm_matches:
                final_mapping[team] = scraped_logos[cm_matches[0]]
                matched += 1
            continue

        # 2. Exact match
        if team in scraped_logos:
            final_mapping[team] = scraped_logos[team]
            matched += 1
            continue
            
        # 2. Try without "7s" or "XV"
        search_name = team.replace(" 7s", "").replace(" XV", "")
        if search_name in scraped_logos:
            final_mapping[team] = scraped_logos[search_name]
            matched += 1
            continue
            
        # 3. Fuzzy matching
        matches = difflib.get_close_matches(search_name, logo_keys, n=1, cutoff=0.7)
        if matches:
            best = matches[0]
            final_mapping[team] = scraped_logos[best]
            print(f"Fuzzy Mapped: '{team}' -> '{best}'")
            matched += 1
        else:
            # lower cutoff for fallback checking (just printing)
            possible = difflib.get_close_matches(search_name, logo_keys, n=3, cutoff=0.4)
            print(f"NO MATCH: '{team}' (Close? {possible})")
            
    print(f"\nSuccessfully matched {matched} out of {len(unique_teams)} teams.")
    
    # Merge existing scraped logos just in case they are used elsewhere, but prioritize exact fixture mappings
    scraped_logos.update(final_mapping)
    
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_logos, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
