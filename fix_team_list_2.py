import json
import re

with open("index.html", "r") as f:
    html = f.read()

# Reverting `.player-row` to left justify:
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
            text-align: left;
        }"""
html = html.replace(old_player_row, new_player_row)

# Reverting team block stuff
old_home_away = """        .home-team { justify-content: flex-end; }
        .away-team { justify-content: flex-start; }"""
new_home_away = """        .home-team { justify-content: center; text-align: center; }
        .away-team { justify-content: center; text-align: center; }"""
        
# Actually, the user says "you centre-justified the team lists within the team list card instead of centre-justifying the cards themselves. The text within should stand left-justified."

# Let's fix .lineup
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
            justify-content: space-around; /* Put cards strictly spaced out into distinct columns */
            gap: 20px;
            font-size: 0.85em;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed var(--card-border);
            width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }"""
html = html.replace(old_lineup, new_lineup)

# Let's fix .match-teams and .team-block
old_team_block = """        .team-block {
            display: flex;
            align-items: center;
            gap: 15px;
            flex: 1;
            min-width: 0; /* allows text truncation */
        }
        
        .home-team { justify-content: flex-end; }
        .away-team { justify-content: flex-start; }"""

new_team_block = """        .team-block {
            display: flex;
            align-items: center;
            justify-content: center; /* Center justify the flag/name cards themselves */
            gap: 15px;
            flex: 1;
            min-width: 0; 
        }"""
html = html.replace(old_team_block, new_team_block)

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
            justify-content: center;
            align-items: center;
            margin: 15px 0;
            width: 100%;
            box-sizing: border-box;
            gap: 10px;
        }"""
html = html.replace(old_match_teams, new_match_teams)

# Remove the text alignment inside team name blocks for lineup header if it's there
html = html.replace("text-align: center;", "text-align: left;")

with open("index.html", "w") as f:
    f.write(html)
