import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Apply flex configurations to constrict text length gracefully inside `.player-row`
css_player_row_old = """
        .player-row {
            display: grid;
            grid-template-columns: 24px 1fr;
            gap: 10px;
            padding: 5px 0;
            border-bottom: 1px solid var(--card-border);
            text-align: left;
        }
"""
css_player_row_new = """
        .player-row {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 5px 0;
            border-bottom: 1px solid var(--card-border);
            text-align: left;
            width: 100%;
            overflow: hidden;
        }

        .player-row > div:nth-child(2) { /* Targeting the player name div specifically */
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            min-width: 0; /* Important for flexbox truncation */
            flex: 1; /* Allow the name to flexibly take remaining space safely */
        }
"""
html = html.replace(css_player_row_old.strip(), css_player_row_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
