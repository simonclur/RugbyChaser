import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see what the nav items look like in the HTML so we know what classes we need to style.
nav_html = re.search(r'<div class="bottom-nav".*?</div>\s*</div>', html, re.DOTALL)
if nav_html:
    print(nav_html.group(0))

