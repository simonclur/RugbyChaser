with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Update active section background to white and text to dark blue (#000033)
html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*background-color:\s*)[^;]+(;)',
    r'\g<1>#ffffff\g<2>',
    html
)

html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*color:\s*)[^;]+(;)',
    r'\g<1>#000033\g<2>',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
