import json

with open("index.html", "r") as f:
    html = f.read()

# 1. Update player row to be left aligned
old_player_row = """        .player-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            overflow: hidden;
        }"""
new_player_row = """        .player-row {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 6px;
            overflow: hidden;
        }"""
html = html.replace(old_player_row, new_player_row)

# 2. Force .lineup to center content as blocks not inside blocks
old_lineup = """        .lineup {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 0.85em;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed var(--card-border);
            text-align: center;
            width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }"""
new_lineup = """        .lineup {
            display: flex;
            justify-content: space-around; /* Distributes the text lists into distinct columns evenly */
            gap: 20px;
            font-size: 0.85em;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed var(--card-border);
            text-align: left; /* Make text inside left aligned! */
            width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }"""
html = html.replace(old_lineup, new_lineup)

# 3. Match Teams header blocks - the flags and text next to each other
old_match_teams = """        .match-teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            width: 100%;
            box-sizing: border-box;
        }"""
new_match_teams = """        .match-teams {
            display: flex;
            justify-content: space-around; /* Center blocks outwards */
            align-items: center;
            margin: 15px 0;
            width: 100%;
            box-sizing: border-box;
        }"""
html = html.replace(old_match_teams, new_match_teams)

# 4. Remove `text-align: right` from the Home Team name html inject that was overriding logic:
html = html.replace("""<div class="team-name" style="text-align: right;">${match.teams[0].name}</div>""", """<div class="team-name">${match.teams[0].name}</div>""")


with open("index.html", "w") as f:
    f.write(html)
