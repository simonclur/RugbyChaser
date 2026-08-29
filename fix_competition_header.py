import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the .competition-header styles
old_css = """
        .competition-header {
            font-size: 1.1em;
            font-weight: bold;
            padding: 8px 12px;
            background-color: var(--accent-color);
            color: white;
            border-radius: 6px;
            margin-bottom: 10px;
            position: sticky;
            top: 10px;
            z-index: 10;
        }
"""

new_css = """
        .competition-header {
            font-size: 1.1em;
            font-weight: bold;
            padding: 10px 15px;
            background-color: #000000; /* Black background instead of neon blue accent */
            color: white;
            border-radius: 0; /* Remove rounded corners to sit flush */
            margin: 0 -15px 15px -15px; /* Pull it out to fill full width of parent container ignoring standard container padding */
            position: sticky;
            top: 0; /* Snap directly to the very top edge without a gap */
            z-index: 20; /* Ensure it floats over other elements */
            box-shadow: 0 2px 4px rgba(0,0,0,0.5); /* Add subtle shadow to distinguish when floating */
        }
"""

if old_css.strip() in html:
    html = html.replace(old_css.strip(), new_css.strip())
else:
    print("Could not find old .competition-header style.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
