import json
import os
import re

def main():
    # Load the fixtures to discover necessary teams
    with open('fixtures.json', 'r') as f:
        fixtures = json.load(f)
        
    unique_teams = set()
    for m in fixtures.get('matches', []):
        for t in m.get('teams', []):
            if 'name' in t:
                unique_teams.add(t['name'].strip())
                
    # Load current dictionary
    with open('team_logos.json', 'r') as f:
        logos = json.load(f)

    # We want to re-standardize ALL items in unique_teams to point to our local static assets if they exist!
    local_images = os.listdir('images')
    
    # Strip any old string values out of the mapping if a local equivalent exists
    for t_name in list(logos.keys()):
        if isinstance(logos[t_name], str):
            # Try to see if this corresponds to a valid old file
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', t_name)
            for ext in ['.png', '.jpg', '.svg', '.gif']:
                if f"{safe_name}{ext}" in local_images:
                    logos[t_name] = {
                        "name": t_name,
                        "source_url": logos[t_name],
                        "local_path": f"images/{safe_name}{ext}"
                    }
                    break

    # Now force-map all fixture teams
    matched_count = 0
    
    aliases = {
        # SRA
        "Dogos": "Dogos de Cordoba",
        "Tarucas": "Tarucas Rugby",
        "Pampas": "Pampas XV",
        "Peñarol": "Penarol Rugby",
        "Yacare XV": "Yacare",
        "Cobras": "Cobras Brasil Rugby",
        
        # South Africa
        "Sharks": "Hollywoodbets Sharks",
        "Lions": "Fidelity SecureDrive Lions",

        # Internationals & Regions
        "Black Ferns XV": "New Zealand",
        "Maori All Blacks": "New Zealand",
        "New Zealand Invitation XV": "New Zealand",
        "Great Britain 7s": "Great Britain",
        
        # Club Aliases
        "Anthem Rugby Carolina": "Anthem RC",
        "Chiefs Manawa": "Chiefs",
        "Matatu": "Crusaders", # Super Rugby Aupiki
        "Kobelco Kobe Steelers": "KOBELCO KOBE STEELERS",
        "Saitama Wild Knights": "SAITAMA WILD KNIGHTS",
        "Tokyo Sungoliath": "TOKYO SUNGOLIATH",
        "Leinster": "Leinster Rugby",
        "Lyon Olympique Universitaire": "Lyon",
        "Montpellier Herault Rugby": "Montpellier Herault",
        "Montpellier Herault Rugby Club": "Montpellier Herault",
        "RC Toulonnais": "Toulon",
        "Rugby Club Toulon Provence Mediterranee": "Toulon",
        "USA Perpignan": "USAP",
        "Union Bordeaux-Begles": "Bordeaux Begles",
        "Fijian Drua Women": "Fijiana Drua Women",
        "Fijian Drua": "Fijiana Drua Women", # Generic fallback since they use the same shield
        "Fijiana Drua": "Fijiana Drua Women",
        "Great Britain 7s": "Great_Britain_national_rugby_sevens_team"
    }

    for team in unique_teams:
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', team)
        
        # Determine the base name (no 7s, U20, Women, etc.)
        base_name = re.sub(r'\s+(7s|XV|U20|U20\'s|A|Women)$', '', team, flags=re.IGNORECASE).strip()
        safe_base = re.sub(r'[^a-zA-Z0-9]', '_', base_name)
        
        found_local = None
        
        # Priority 0: Alias mapping
        if team in aliases:
            alias_safe = re.sub(r'[^a-zA-Z0-9]', '_', aliases[team])
            for ext in ['.png', '.gif', '.jpg', '.svg']:
                if f"{alias_safe}{ext}" in local_images:
                    found_local = f"images/{alias_safe}{ext}"
                    break

        # Priority 1: Exact match with extension
        if not found_local:
            for ext in ['.png', '.gif', '.jpg', '.svg']:
                if f"{safe_name}{ext}" in local_images:
                    found_local = f"images/{safe_name}{ext}"
                    break
        
        # Priority 2: Base match with extension (for 7s, U20, etc.)
        if not found_local:
            for ext in ['.png', '.gif', '.jpg', '.svg']:
                if f"{safe_base}{ext}" in local_images:
                    found_local = f"images/{safe_base}{ext}"
                    break
        
        # Priority 3: Check manually mapped aliases in the logos tree 
        # (if logos[team] is already a dict with local_path, keep it)
        if not found_local and team in logos and isinstance(logos[team], dict) and 'local_path' in logos[team]:
            found_local = logos[team]['local_path']
        
        if found_local:
            # Overwrite gracefully
            logos[team] = {
                "name": team,
                "source_url": "local_override",
                "local_path": found_local
            }
            matched_count += 1
        elif team in logos and isinstance(logos[team], str):
             # Remove string matches to force UI-avatars instead of Wikipedia blocking
             del logos[team]
             
    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)

    print(f"Force aligned {matched_count} fixture teams to static local images!")

if __name__ == '__main__':
    main()