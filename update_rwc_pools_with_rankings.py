import json

with open("rwc_pools.json", "r") as f:
    pools = json.load(f)

with open("rankings.json", "r") as f:
    rankings = json.load(f)["mru"] # Mens rankings

# Build lookup table
rankings_map = { r["name"]: r["pts"] for r in rankings }

# Name adjustments if needed
team_name_map = {
    "Hong Kong China": "Hong Kong China", 
    "USA": "USA", # Verify if World Rugby calls it United States or USA
}

# Add pts to pool data
for pool_name, teams in pools.items():
    for team in teams:
        name = team["team"]
        if name in team_name_map:
            mapped_name = team_name_map[name]
        else:
            mapped_name = name
            
        pts = rankings_map.get(mapped_name)
        if pts is None:
            # try fuzzy matching
            for r_name, r_pts in rankings_map.items():
                if r_name in mapped_name or mapped_name in r_name:
                    pts = r_pts
                    break
                    
        if pts is not None:
             # Just use it as standings/points mapping for prediction mapping
             team["points"] = pts 
             print(f"Mapped {name} to {pts} pts")
        else:
             print(f"WARNING: Could not find ranking for {name}")

# Re-sort pools based on points!
for pool_name, teams in pools.items():
    # Sort descending
    teams.sort(key=lambda x: float(x.get("points", 0)), reverse=True)
    # Re-assign positions
    for i, t in enumerate(teams):
        t["position"] = str(i + 1)

with open("rwc_pools.json", "w") as f:
    json.dump(pools, f, indent=4)
print("Updated rwc_pools.json with MRU ranking points as 'points'")
