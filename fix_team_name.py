import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the team name to shrink dynamically if bounded rather than blowing out
css_team_name_old = """
        .team-name {
            /* Memory applied: readable full team names */
            font-weight: 500;
            font-size: 1.05em;
            margin: 0 10px;
        }
"""
css_team_name_new = """
        .team-name {
            /* Memory applied: readable full team names */
            font-weight: 500;
            font-size: 1.05em;
            margin: 0 10px;
            /* Allow names to scale tightly within bounds */
            flex-shrink: 1;
            min-width: 0;
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
        }
"""
if css_team_name_old.strip() in html:
    html = html.replace(css_team_name_old.strip(), css_team_name_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
