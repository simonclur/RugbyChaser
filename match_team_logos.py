import json

def main():
    with open('fixtures.json', 'r') as f:
        fixtures = json.load(f)
        
    unique_teams = set()
    for m in fixtures.get('matches', []):
        for t in m.get('teams', []):
            if 'name' in t:
                unique_teams.add(t['name'].strip())
                
    with open('team_logos.json', 'r') as f:
        logos = json.load(f)

    # Clean exact hardcoded dictionary overriding buggy fuzzy searches
    exact_map = {
        "Argentina": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Argentine_Rugby_Union_logo_2023.svg/100px-Argentine_Rugby_Union_logo_2023.svg.png",
        "Argentina 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Argentine_Rugby_Union_logo_2023.svg/100px-Argentine_Rugby_Union_logo_2023.svg.png",
        "Argentina U20": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Argentine_Rugby_Union_logo_2023.svg/100px-Argentine_Rugby_Union_logo_2023.svg.png",

        "South Africa": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/South_Africa_national_rugby_union_team.svg/100px-South_Africa_national_rugby_union_team.svg.png",
        "South Africa 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/South_Africa_national_rugby_union_team.svg/100px-South_Africa_national_rugby_union_team.svg.png",
        "South Africa U20": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/South_Africa_national_rugby_union_team.svg/100px-South_Africa_national_rugby_union_team.svg.png",

        "New Zealand": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/New_Zealand_All_Blacks.svg/100px-New_Zealand_All_Blacks.svg.png",
        "New Zealand 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/New_Zealand_All_Blacks.svg/100px-New_Zealand_All_Blacks.svg.png",
        "New Zealand U20": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/New_Zealand_All_Blacks.svg/100px-New_Zealand_All_Blacks.svg.png",
        "Maori All Blacks": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/New_Zealand_All_Blacks.svg/100px-New_Zealand_All_Blacks.svg.png",
        "Black Ferns XV": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/New_Zealand_All_Blacks.svg/100px-New_Zealand_All_Blacks.svg.png",

        "France": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Logo_XV_de_France_masculin_2019.svg/100px-Logo_XV_de_France_masculin_2019.svg.png",
        "France 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Logo_XV_de_France_masculin_2019.svg/100px-Logo_XV_de_France_masculin_2019.svg.png",
        "France U20": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Logo_XV_de_France_masculin_2019.svg/100px-Logo_XV_de_France_masculin_2019.svg.png",

        "Ireland": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Irish_Rugby_Football_Union.svg/100px-Irish_Rugby_Football_Union.svg.png",
        "Ireland 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Irish_Rugby_Football_Union.svg/100px-Irish_Rugby_Football_Union.svg.png",
        "Ireland U20": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Irish_Rugby_Football_Union.svg/100px-Irish_Rugby_Football_Union.svg.png",

        "Australia": "https://upload.wikimedia.org/wikipedia/en/thumb/5/50/Wallabies_national_rugby_union_team_primary_crest.svg/100px-Wallabies_national_rugby_union_team_primary_crest.svg.png",
        "Australia 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/5/50/Wallabies_national_rugby_union_team_primary_crest.svg/100px-Wallabies_national_rugby_union_team_primary_crest.svg.png",
        "Australia A": "https://upload.wikimedia.org/wikipedia/en/thumb/5/50/Wallabies_national_rugby_union_team_primary_crest.svg/100px-Wallabies_national_rugby_union_team_primary_crest.svg.png",
        "Australia U20": "https://upload.wikimedia.org/wikipedia/en/thumb/5/50/Wallabies_national_rugby_union_team_primary_crest.svg/100px-Wallabies_national_rugby_union_team_primary_crest.svg.png",

        "Wales": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4b/Welsh_Rugby_Union_logo.svg/100px-Welsh_Rugby_Union_logo.svg.png",
        "Wales 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4b/Welsh_Rugby_Union_logo.svg/100px-Welsh_Rugby_Union_logo.svg.png",

        "England": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/England_Rugby.svg/100px-England_Rugby.svg.png",
        "England 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/England_Rugby.svg/100px-England_Rugby.svg.png",

        "Scotland": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Scottish_Rugby_Union.svg/100px-Scottish_Rugby_Union.svg.png",
        "Scotland 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Scottish_Rugby_Union.svg/100px-Scottish_Rugby_Union.svg.png",

        "Italy": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Federazione_Italiana_Rugby.svg/100px-Federazione_Italiana_Rugby.svg.png",
        "Italy 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Federazione_Italiana_Rugby.svg/100px-Federazione_Italiana_Rugby.svg.png",
        
        "Fiji": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Logo_Fiji_Rugby_2019.svg/100px-Logo_Fiji_Rugby_2019.svg.png",
        "Fiji 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Logo_Fiji_Rugby_2019.svg/100px-Logo_Fiji_Rugby_2019.svg.png",
        "Fijian Drua": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Fijian_drua.png/100px-Fijian_drua.png",
        
        "Samoa": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/Samoa_Rugby_Union.svg/100px-Samoa_Rugby_Union.svg.png",
        "Samoa 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/Samoa_Rugby_Union.svg/100px-Samoa_Rugby_Union.svg.png",

        "Uruguay": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Uruguayan_Rugby_Union.svg/100px-Uruguayan_Rugby_Union.svg.png",
        "Uruguay 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Uruguayan_Rugby_Union.svg/100px-Uruguayan_Rugby_Union.svg.png",

        "Japan": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Japan_Rugby_Football_Union.svg/100px-Japan_Rugby_Football_Union.svg.png",
        "Japan 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Japan_Rugby_Football_Union.svg/100px-Japan_Rugby_Football_Union.svg.png",
        "Japan XV": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Japan_Rugby_Football_Union.svg/100px-Japan_Rugby_Football_Union.svg.png",

        "USA": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/United_States_Rugby.svg/100px-United_States_Rugby.svg.png",
        "USA 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/United_States_Rugby.svg/100px-United_States_Rugby.svg.png",
        
        "Georgia": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Federation_Georgian_Rugby.svg/100px-Federation_Georgian_Rugby.svg.png",
        "Romania": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Romanian_Rugby_Federation.svg/100px-Romanian_Rugby_Federation.svg.png",
        "Spain": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Spanish_Rugby_Federation.svg/100px-Spanish_Rugby_Federation.svg.png",
        "Great Britain 7s": "https://upload.wikimedia.org/wikipedia/en/thumb/9/93/Great_Britain_national_rugby_sevens_team.png/100px-Great_Britain_national_rugby_sevens_team.png",
        
        "Ospreys": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/Ospreys_%28rugby_union%29_logo.svg/100px-Ospreys_%28rugby_union%29_logo.svg.png",
        "Chiefs": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Chiefs_logo.svg/100px-Chiefs_logo.svg.png",
        "Crusaders": "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Crusaders_logo_2022.svg/100px-Crusaders_logo_2022.svg.png",
        "Hurricanes": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Hurricanes_Rugby_Union_logo.svg/100px-Hurricanes_Rugby_Union_logo.svg.png",
        "Highlanders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Highlanders_Logo.png/100px-Highlanders_Logo.png",
        "Blues": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Blues_%28Super_Rugby%29_logo.svg/100px-Blues_%28Super_Rugby%29_logo.svg.png",
        "Brumbies": "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/ACT_Brumbies_logo.svg/100px-ACT_Brumbies_logo.svg.png",
        "Waratahs": "https://upload.wikimedia.org/wikipedia/en/thumb/4/42/W_Logo_-_Primary_Navy_2024.png/100px-W_Logo_-_Primary_Navy_2024.png",
        "Reds": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Queensland_Reds_Logo.svg/100px-Queensland_Reds_Logo.svg.png",
        "Western Force": "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Waratahs_logo.svg/100px-Waratahs_logo.svg.png",

        "Bath Rugby": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b5/Bath_Rugby_Logo.svg/100px-Bath_Rugby_Logo.svg.png",
        "Bristol Bears": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Bristol_Bears_Logo.svg/100px-Bristol_Bears_Logo.svg.png",
        "Saracens": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Saracens_F.C._logo.svg/100px-Saracens_F.C._logo.svg.png",
        "Stade Toulousain": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4b/Stade_Toulousain.svg/100px-Stade_Toulousain.svg.png",
        "Leicester Tigers": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Leicester_Tigers_logo.svg/100px-Leicester_Tigers_logo.svg.png",
        "Harlequins": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Harlequins_Logo.svg/100px-Harlequins_Logo.svg.png",
        "Gloucester Rugby": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5e/Gloucester_Rugby_Logo.svg/100px-Gloucester_Rugby_Logo.svg.png",
        "Exeter Harlequins": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6f/Exeter_Chiefs.svg/100px-Exeter_Chiefs.svg.png",
        "Exeter Chiefs": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6f/Exeter_Chiefs.svg/100px-Exeter_Chiefs.svg.png"
    }

    # Iterate through unique fixture teams
    for team in unique_teams:
        # Check standard flags for remaining unmapped entries
        if team not in exact_map:
            if team + " Flag" in logos:
                exact_map[team] = logos[team + " Flag"]
            elif team.replace(" 7s", "") + " Flag" in logos:
                exact_map[team] = logos[team.replace(" 7s", "") + " Flag"]
            elif team.replace(" XV", "") + " Flag" in logos:
                exact_map[team] = logos[team.replace(" XV", "") + " Flag"]
            
        # Try to find exactly matched country names against exact URLs
        if team in exact_map:
            logos[team] = exact_map[team]

    with open('team_logos.json', 'w', encoding='utf-8') as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)

    print(f"Applied {len(exact_map)} robust exact mappings (overwriting bad fuzzy math).")

if __name__ == '__main__':
    main()
