import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the word "Location: " from the render string
html = re.sub(
    r'<div style="margin-bottom: 3px;">Location:',
    r'<div style="margin-bottom: 3px;">',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
