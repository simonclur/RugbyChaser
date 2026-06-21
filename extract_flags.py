import urllib.request
import re
import json

def get_more_country_flags():
    url = "https://en.wikipedia.org/wiki/Rugby_World_Cup_Sevens"
    req = urllib.request.Request(url, headers={'User-Agent': 'RugbyChaser/1.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print("Error fetching Sevens page:", e)
        return

    # Find flagicon to <a> element text
    pattern = r'<span class="flagicon">.*?<img[^>]*src="([^"]+)".*?</span>\s*<a[^>]*>([^<]+)</a>'
    matches = re.finditer(pattern, html, re.DOTALL)
    
    flags = {}
    for m in matches:
        src = m.group(1)
        country = m.group(2).strip()
        # Ensure it has https and make the image larger for better quality
        if src.startswith("//"):
            src = "https:" + src
        src = re.sub(r'/(\d+)px-', r'/100px-', src)
        flags[country] = src
        
    print(f"Extracted {len(flags)} country flags from Sevens page.")
    
    with open('team_logos.json', 'r') as f:
        team_logos = json.load(f)
        
    with open('fixtures.json', 'r') as f:
        fixtures = json.load(f)
    
    unique_teams = set()
    for match in fixtures.get('matches', []):
        for team in match.get('teams', []):
            if 'name' in team:
                unique_teams.add(team['name'].strip())

    updates = 0
    # Let's just add the extracted flags to team_logos.json so the UI can pick them up
    for country, flag_url in flags.items():
        if country not in team_logos:
            team_logos[country + " Flag"] = flag_url
        
        # also apply to team names if not present
        if country in unique_teams and country not in team_logos:
            team_logos[country] = flag_url
            updates += 1
            
        for ext in [" 7s", " U20", " XV", " A"]:
            t_name = country + ext
            if t_name in unique_teams and t_name not in team_logos:
                team_logos[t_name] = flag_url
                updates += 1
                
    # Also fetch from the general national teams page for World Rugby members
    url2 = "https://en.wikipedia.org/wiki/List_of_national_rugby_union_teams"
    try:
        req2 = urllib.request.Request(url2, headers={'User-Agent': 'RugbyChaser/1.0'})
        html2 = urllib.request.urlopen(req2).read().decode('utf-8')
        matches2 = re.finditer(r'<span class="flagicon">.*?<img[^>]*src="([^"]+)".*?</span>.*?<a[^>]*>([^<]+)</a>', html2, re.DOTALL)
        for m in matches2:
            src = m.group(1)
            country = m.group(2).strip()
            if src.startswith("//"):
                src = "https:" + src
            src = re.sub(r'/(\d+)px-', r'/100px-', src)
            
            # Save it
            flag_key = country + " Flag"
            if flag_key not in team_logos:
                team_logos[flag_key] = src
                
            if country in unique_teams and country not in team_logos:
                team_logos[country] = src
                updates += 1
            for ext in [" 7s", " U20", " XV", " A"]:
                t_name = country + ext
                if t_name in unique_teams and t_name not in team_logos:
                    team_logos[t_name] = src
                    updates += 1
    except Exception as e:
        print("Error fetching National Teams page:", e)

    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(team_logos, f, indent=2, ensure_ascii=False)
        
    print(f"Updated team_logos.json with {updates} additional team matches.")

if __name__ == '__main__':
    get_more_country_flags()
