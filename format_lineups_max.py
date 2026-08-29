import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Stretch the blocks out to effectively encompass the container space touching in middle
css_lineup_team_old = """
        .lineup-team {
            background: var(--bg-color);
            padding: 10px;
            border-radius: 6px;
            margin: 0 auto;
            width: calc(50% - 3px); /* 50% minus half the gap space */
            min-width: 150px; /* Base width */
            max-width: 180px; /* Restrict width so it comfortably maps two side by side into 350px card limits */
            box-sizing: border-box;
        }
"""
css_lineup_team_new = """
        .lineup-team {
            background: var(--bg-color);
            padding: 8px; /* Slightly less padding to maximize interior text space */
            border-radius: 4px;
            margin: 0; 
            width: calc(50% - 2px); /* Let them stretch directly against the 4px gap center */
            box-sizing: border-box;
            flex: 1; /* Stretch aggressively */
            max-width: calc(50% - 2px);
            min-width: 0; /* Let flex scale them downward */
        }
"""
if css_lineup_team_old.strip() in html:
    html = html.replace(css_lineup_team_old.strip(), css_lineup_team_new.strip())

css_live_lineups_old = """
        .live-lineups {
            display: flex; /* Grid is rigid on narrow screens, flex can wrap/breathe */
            flex-direction: row;
            justify-content: center; /* Center the team blocks */
            gap: 6px; /* Shrink gap to help fit in bounding box and bring closer */
            margin-top: 20px;
            font-size: 0.85em;
            text-align: left;
            width: 100%;
            flex-wrap: wrap; /* Safety valve for narrow screens */
        }
"""
css_live_lineups_new = """
        .live-lineups {
            display: flex; 
            flex-direction: row;
            justify-content: space-between; /* Match the outermost constraints */
            gap: 4px; /* Tiny gap */
            margin-top: 15px;
            font-size: 0.82em; /* Shrink font subtly */
            text-align: left;
            width: 100%;
        }
"""
if css_live_lineups_old.strip() in html:
    html = html.replace(css_live_lineups_old.strip(), css_live_lineups_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
