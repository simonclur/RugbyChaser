import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_logic = """
                                let iconStyle = '';
                                if ((ev.typeLabel || ev.type) === 'SubstitutionOn' || (ev.typeLabel || ev.type) === 'Substitute On') {
                                    iconStyle = 'color: #22c55e;'; // Green for going on
                                } else if ((ev.typeLabel || ev.type) === 'SubstitutionOff' || (ev.typeLabel || ev.type) === 'Substitute Off') {
                                    iconStyle = 'color: #ef4444;'; // Red for going off
                                }
"""

new_logic = """
                                let iconStyle = '';
                                const typeStr = String(ev.typeLabel || ev.type || '').toLowerCase();
                                if (typeStr.includes('replacement on') || typeStr.includes('replacementon')) {
                                    iconStyle = 'color: #22c55e;'; // Green for going on
                                } else if (typeStr.includes('replacement off') || typeStr.includes('replacementoff')) {
                                    iconStyle = 'color: #f97316;'; // Orange for going off (distinguish from red card)
                                } else if (typeStr.includes('yellow')) {
                                    iconStyle = 'color: #eab308;'; // Gold/Yellow
                                } else if (typeStr.includes('red')) {
                                    iconStyle = 'color: #ef4444;'; // Red 
                                } else if (typeStr.includes('try')) {
                                    iconStyle = 'color: #3b82f6;'; // Blue
                                } else if (typeStr.includes('conversion')) {
                                    iconStyle = 'color: #0ea5e9;'; // Cyan / Light Blue
                                }
"""

if old_logic.strip() in html:
    html = html.replace(old_logic.strip(), new_logic.strip())
else:
    print("WARNING: Could not find exactly matching block. Manual check needed.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
