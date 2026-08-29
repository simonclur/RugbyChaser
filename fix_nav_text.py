import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the color mapping which swapped text with border by accident last time
html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*color:\s*)white(;)',
    r'\g<1>#000033\g<2>',
    html
)

html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*border-color:\s*)#000033(;)',
    r'\g<1>#ffffff\g<2>',
    html
)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
