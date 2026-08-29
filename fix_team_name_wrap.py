import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update .team-name to wrap onto new lines instead of cutting off with ellipses.
css_team_name_old = """
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
css_team_name_new = """
        .team-name {
            /* Memory applied: readable full team names */
            font-weight: 500;
            font-size: 1.05em;
            margin: 0 10px;
            /* Allow names to wrap onto multiple lines if container horizontal width is restrictive */
            flex-shrink: 1;
            min-width: 0;
            white-space: normal; /* Enable wrapping */
            word-wrap: break-word; /* Ensure extremely long words don't blow out padding either */
            line-height: 1.1; /* Keep multi-line blocks tight vertically */
        }
"""

if css_team_name_old.strip() in html:
    html = html.replace(css_team_name_old.strip(), css_team_name_new.strip())
else:
    print("Warning: old team-name css not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
