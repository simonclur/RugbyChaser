import re

with open("index.html", "r") as f:
    text = f.read()

old_css = """        .match-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            /* Memory applied: compact match cards with reduced vertical space */
            line-height: 1.3; 
        }"""

new_css = """        .match-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            /* Memory applied: compact match cards with reduced vertical space */
            line-height: 1.3; 
        }

        .match-primary-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-basis: 100%;
        }

        .see-more-badge {
            cursor: pointer;
            padding: 2px 8px;
            background: var(--bg-color);
            border-radius: 4px;
            font-size: 0.75em;
            text-align: center;
            color: var(--muted-text);
            user-select: none;
            display: inline-block;
            margin-top: 8px;
            border: 1px solid var(--card-border);
        }
        .see-more-badge:hover {
            background: var(--card-border);
        }
        .extended-container {
            flex-basis: 100%;
            display: none;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed var(--card-border);
            font-size: 0.9em;
        }"""

text = text.replace(old_css, new_css)
with open("index.html", "w") as f:
    f.write(text)

