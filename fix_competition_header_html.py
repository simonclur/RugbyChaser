import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I also need to make sure the margin offsets act directly upon the dynamically generated HTML classes containing them otherwise the parent flex-items clamp it!
render_logic_old = """
                    // Add new competition header
                    html += `<div class="competition-header">${compName}</div>`;
"""

render_logic_new = """
                    // Add new competition header
                    // We need to inject an inline margin overwrite otherwise it can't escape its parent wrapper
                    html += `<div class="competition-header" style="margin-left: -15px; margin-right: -15px;">${compName}</div>`;
"""

if render_logic_old.strip() in html:
    html = html.replace(render_logic_old.strip(), render_logic_new.strip())
else:
    print("Could not find old render logic.")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
