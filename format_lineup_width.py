import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_live_lineups_old = """
        .live-lineups {
            display: flex; /* Grid is rigid on narrow screens, flex can wrap/breathe */
            flex-direction: row;
            justify-content: center; /* Center the team blocks */
            gap: 15px; /* Shrink gap to help fit in bounding box */
            margin-top: 20px;
            font-size: 0.85em;
            text-align: left;
            width: 100%;
            flex-wrap: wrap; /* Safety valve for narrow screens */
        }
"""
css_live_lineups_new = """
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
html = html.replace(css_live_lineups_old.strip(), css_live_lineups_new.strip())

css_lineup_team_old = """
        .lineup-team {
            background: var(--bg-color);
            padding: 10px;
            border-radius: 6px;
            margin: 0 auto;
            width: calc(50% - 10px); /* 50% minus the gap space */
            min-width: 140px; /* Base width */
            max-width: 160px; /* Restrict width so it comfortably maps two side by side into 350px card limits */
            box-sizing: border-box;
        }
"""
css_lineup_team_new = """
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
html = html.replace(css_lineup_team_old.strip(), css_lineup_team_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
