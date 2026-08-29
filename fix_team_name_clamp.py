import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_team_name_old = """
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
css_team_name_new = """
        .team-name {
            /* Memory applied: readable full team names */
            font-weight: 500;
            /* Dynamically scale down font size on small viewports so names fit better without wrapping, cap at 1.05em */
            font-size: clamp(0.8rem, 3.5vw, 1.05rem);
            margin: 0 10px;
            
            /* Enforce bounds and ellipsis shortening if still too long */
            flex-shrink: 1;
            min-width: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
"""

if css_team_name_old.strip() in html:
    html = html.replace(css_team_name_old.strip(), css_team_name_new.strip())
else:
    print("Warning: old team-name css not found")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
