import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure inline styles don't conflict, allowing the .competition-header CSS to behave accurately full-width.
# It seems those header items explicitly contained styling like `style="background-color: var(--accent-color); color: white; padding: 10px 15px; border-radius: 6px; font-weight: bold; margin-bottom: 10px;"` inside the HTML blocking our CSS logic updates from cascading!

html = re.sub(
    r'(<div class="competition-header") style="[^"]*"(>.*?</div|>)', 
    r'\1\2', 
    html
)

# And now we patch the render logic generator manually specifically 
render_old = """
                    html += `<div class="competition-group">`;
                    html += `<div class="competition-header" style="display: flex; justify-content: space-between; align-items: center;">
"""
render_new = """
                    html += `<div class="competition-group">`;
                    html += `<div class="competition-header" style="display: flex; justify-content: space-between; align-items: center; margin-left: -15px; margin-right: -15px;">
"""
if render_old.strip() in html:
    html = html.replace(render_old.strip(), render_new.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
